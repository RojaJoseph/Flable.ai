"""
Integrations API Routes - Shopify OAuth, Google Ads, Facebook
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import secrets
from datetime import datetime

from database.connection import get_db
from database.models import User, Integration, IntegrationStatus
from schemas import schemas
from utils.auth_utils import get_current_user
from integrations.shopify_oauth import shopify_oauth, ShopifyClient
from integrations.shopify_integration import sync_shopify_data
from utils.redis_client import redis_client

router = APIRouter()


@router.get("/", response_model=List[schemas.IntegrationResponse])
async def get_integrations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all integrations for current user"""
    integrations = db.query(Integration).filter(
        Integration.user_id == current_user.id
    ).all()
    return integrations


@router.get("/{integration_id}", response_model=schemas.IntegrationResponse)
async def get_integration(
    integration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific integration"""
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.user_id == current_user.id
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    return integration


@router.get("/shopify/auth")
async def shopify_auth_initiate(
    shop: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Initiate Shopify OAuth flow
    
    Step 1: Generate authorization URL and redirect user to Shopify
    """
    # Generate random state for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Store state in Redis with user ID (expires in 10 minutes)
    await redis_client.set(
        f"shopify_oauth_state:{state}",
        str(current_user.id),
        expire=600
    )
    
    # Generate authorization URL
    auth_url = shopify_oauth.get_authorization_url(shop, state)
    
    return {"auth_url": auth_url}


@router.get("/shopify/callback")
async def shopify_auth_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Handle Shopify OAuth callback
    
    Step 2: Exchange code for access token and create integration
    """
    # Get query parameters
    params = dict(request.query_params)
    
    # Verify required parameters
    if 'code' not in params or 'shop' not in params or 'state' not in params:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required parameters"
        )
    
    code = params['code']
    shop_domain = params['shop']
    state = params['state']
    
    # Verify state (CSRF protection)
    user_id_str = await redis_client.get(f"shopify_oauth_state:{state}")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired state"
        )
    
    user_id = int(user_id_str)
    
    # Delete used state
    await redis_client.delete(f"shopify_oauth_state:{state}")
    
    # Verify HMAC
    if not shopify_oauth.verify_hmac(params.copy()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid HMAC signature"
        )
    
    # Exchange code for access token
    access_token = await shopify_oauth.exchange_code_for_token(shop_domain, code)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get access token from Shopify"
        )
    
    # Get shop information
    shop_info = shopify_oauth.get_shop_info(shop_domain, access_token)
    if not shop_info:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get shop information"
        )
    
    # Check if integration already exists
    existing = db.query(Integration).filter(
        Integration.user_id == user_id,
        Integration.platform == "shopify",
        Integration.shop_domain == shop_domain
    ).first()
    
    if existing:
        # Update existing integration
        existing.access_token = access_token
        existing.status = IntegrationStatus.CONNECTED
        existing.account_id = str(shop_info.get("id", ""))
        existing.settings = {
            "shop_name": shop_info.get("name", ""),
            "shop_email": shop_info.get("email", ""),
            "currency": shop_info.get("currency", "USD"),
            "timezone": shop_info.get("timezone", "UTC")
        }
        db.commit()
        integration_id = existing.id
    else:
        # Create new integration
        new_integration = Integration(
            user_id=user_id,
            platform="shopify",
            status=IntegrationStatus.CONNECTED,
            access_token=access_token,
            shop_domain=shop_domain,
            account_id=str(shop_info.get("id", "")),
            settings={
                "shop_name": shop_info.get("name", ""),
                "shop_email": shop_info.get("email", ""),
                "currency": shop_info.get("currency", "USD"),
                "timezone": shop_info.get("timezone", "UTC")
            }
        )
        db.add(new_integration)
        db.commit()
        db.refresh(new_integration)
        integration_id = new_integration.id
    
    # Trigger initial sync in background
    background_tasks.add_task(sync_shopify_data, integration_id, db)
    
    # Redirect to frontend integrations page with success
    return RedirectResponse(
        url=f"http://localhost:3000/integrations?success=true&shop={shop_domain}",
        status_code=status.HTTP_302_FOUND
    )


@router.post("/shopify", response_model=schemas.IntegrationResponse, status_code=status.HTTP_201_CREATED)
async def connect_shopify_manual(
    integration_data: schemas.IntegrationCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Connect Shopify store manually (for backward compatibility)
    
    Use this if you have a private app access token
    """
    
    # Check if Shopify integration already exists
    existing = db.query(Integration).filter(
        Integration.user_id == current_user.id,
        Integration.platform == "shopify",
        Integration.shop_domain == integration_data.shop_domain
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shopify store already connected. Disconnect first or use OAuth flow."
        )
    
    # Test Shopify connection
    try:
        client = ShopifyClient(
            shop_domain=integration_data.shop_domain,
            access_token=integration_data.access_token
        )
        
        if not client.test_connection():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to connect to Shopify store. Please check your credentials."
            )
        
        # Get shop info
        shop_info = shopify_oauth.get_shop_info(
            integration_data.shop_domain,
            integration_data.access_token
        )
        client.close()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Shopify connection error: {str(e)}"
        )
    
    # Create integration
    new_integration = Integration(
        user_id=current_user.id,
        platform="shopify",
        status=IntegrationStatus.CONNECTED,
        access_token=integration_data.access_token,
        shop_domain=integration_data.shop_domain,
        account_id=str(shop_info.get("id", "") if shop_info else ""),
        settings={
            "shop_name": shop_info.get("name", "") if shop_info else "",
            "shop_email": shop_info.get("email", "") if shop_info else "",
            "currency": shop_info.get("currency", "USD") if shop_info else "USD",
            "timezone": shop_info.get("timezone", "UTC") if shop_info else "UTC"
        }
    )
    
    db.add(new_integration)
    db.commit()
    db.refresh(new_integration)
    
    # Trigger initial sync in background
    background_tasks.add_task(sync_shopify_data, new_integration.id, db)
    
    return new_integration


@router.post("/{integration_id}/sync")
async def sync_integration(
    integration_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sync data from integration"""
    
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.user_id == current_user.id
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    if integration.platform == "shopify":
        background_tasks.add_task(sync_shopify_data, integration_id, db)
        return {"message": "Shopify sync started", "integration_id": integration_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sync not supported for platform: {integration.platform}"
        )


@router.delete("/{integration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_integration(
    integration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disconnect an integration"""
    
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.user_id == current_user.id
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    db.delete(integration)
    db.commit()
    
    return None


@router.get("/shopify/{integration_id}/products")
async def get_shopify_products(
    integration_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get products from connected Shopify store"""
    
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.user_id == current_user.id,
        Integration.platform == "shopify"
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopify integration not found"
        )
    
    try:
        client = ShopifyClient(
            shop_domain=integration.shop_domain,
            access_token=integration.access_token
        )
        products = client.get_products(limit=limit)
        client.close()
        
        return {
            "integration_id": integration_id,
            "shop_domain": integration.shop_domain,
            "products_count": len(products),
            "products": products
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching Shopify products: {str(e)}"
        )


@router.get("/shopify/{integration_id}/orders")
async def get_shopify_orders(
    integration_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get orders from connected Shopify store"""
    
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.user_id == current_user.id,
        Integration.platform == "shopify"
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopify integration not found"
        )
    
    try:
        client = ShopifyClient(
            shop_domain=integration.shop_domain,
            access_token=integration.access_token
        )
        orders = client.get_orders(limit=limit)
        client.close()
        
        return {
            "integration_id": integration_id,
            "shop_domain": integration.shop_domain,
            "orders_count": len(orders),
            "orders": orders
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching Shopify orders: {str(e)}"
        )
