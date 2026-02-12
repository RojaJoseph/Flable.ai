"""
Shopify OAuth Integration - Proper OAuth 2.0 flow
"""

import shopify
import hmac
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from loguru import logger
import httpx

from database.models import Integration, IntegrationStatus
from utils.config import settings


class ShopifyOAuth:
    """Shopify OAuth authentication handler"""
    
    def __init__(self):
        self.client_id = settings.SHOPIFY_CLIENT_ID
        self.client_secret = settings.SHOPIFY_CLIENT_SECRET
        self.redirect_uri = settings.SHOPIFY_REDIRECT_URI
        self.scopes = settings.SHOPIFY_SCOPES
    
    def get_authorization_url(self, shop_domain: str, state: str) -> str:
        """
        Generate Shopify OAuth authorization URL
        
        Args:
            shop_domain: The shop domain (e.g., store.myshopify.com)
            state: Random state string for CSRF protection
            
        Returns:
            Authorization URL to redirect user to
        """
        # Ensure shop domain has .myshopify.com
        if not shop_domain.endswith('.myshopify.com'):
            shop_domain = f"{shop_domain}.myshopify.com"
        
        auth_url = (
            f"https://{shop_domain}/admin/oauth/authorize?"
            f"client_id={self.client_id}&"
            f"scope={self.scopes}&"
            f"redirect_uri={self.redirect_uri}&"
            f"state={state}"
        )
        
        return auth_url
    
    def verify_hmac(self, params: Dict[str, str]) -> bool:
        """
        Verify HMAC signature from Shopify
        
        Args:
            params: Query parameters from callback
            
        Returns:
            True if HMAC is valid
        """
        if 'hmac' not in params:
            return False
        
        received_hmac = params.pop('hmac')
        
        # Sort params and create message
        message = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
        
        # Calculate expected HMAC
        calculated_hmac = hmac.new(
            self.client_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(calculated_hmac, received_hmac)
    
    async def exchange_code_for_token(self, shop_domain: str, code: str) -> Optional[str]:
        """
        Exchange authorization code for access token
        
        Args:
            shop_domain: The shop domain
            code: Authorization code from callback
            
        Returns:
            Access token or None if failed
        """
        # Ensure shop domain has .myshopify.com
        if not shop_domain.endswith('.myshopify.com'):
            shop_domain = f"{shop_domain}.myshopify.com"
        
        token_url = f"https://{shop_domain}/admin/oauth/access_token"
        
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, json=payload)
                response.raise_for_status()
                
                data = response.json()
                return data.get('access_token')
        except Exception as e:
            logger.error(f"Failed to exchange code for token: {e}")
            return None
    
    def get_shop_info(self, shop_domain: str, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get shop information using access token
        
        Args:
            shop_domain: The shop domain
            access_token: OAuth access token
            
        Returns:
            Shop information dict or None
        """
        try:
            # Ensure shop domain has .myshopify.com
            if not shop_domain.endswith('.myshopify.com'):
                shop_domain = f"{shop_domain}.myshopify.com"
            
            # Create session
            session = shopify.Session(shop_domain, "2024-01", access_token)
            shopify.ShopifyResource.activate_session(session)
            
            # Get shop info
            shop = shopify.Shop.current()
            
            shop_info = {
                "id": shop.id,
                "name": shop.name,
                "email": shop.email,
                "domain": shop.domain,
                "myshopify_domain": shop.myshopify_domain,
                "currency": shop.currency,
                "timezone": shop.timezone,
                "plan_name": shop.plan_name,
                "created_at": shop.created_at
            }
            
            shopify.ShopifyResource.clear_session()
            
            return shop_info
            
        except Exception as e:
            logger.error(f"Failed to get shop info: {e}")
            return None


class ShopifyClient:
    """Shopify API client wrapper"""
    
    def __init__(self, shop_domain: str, access_token: str):
        self.shop_domain = shop_domain
        self.access_token = access_token
        
        # Ensure shop domain has .myshopify.com
        if not self.shop_domain.endswith('.myshopify.com'):
            self.shop_domain = f"{self.shop_domain}.myshopify.com"
        
        self._activate_session()
    
    def _activate_session(self):
        """Activate Shopify session"""
        session = shopify.Session(self.shop_domain, "2024-01", self.access_token)
        shopify.ShopifyResource.activate_session(session)
    
    def test_connection(self) -> bool:
        """Test Shopify API connection"""
        try:
            shop = shopify.Shop.current()
            return shop is not None
        except Exception as e:
            logger.error(f"Shopify connection test failed: {e}")
            return False
    
    def get_products(self, limit: int = 250):
        """Get products from Shopify"""
        try:
            products = shopify.Product.find(limit=limit)
            return [
                {
                    "id": p.id,
                    "title": p.title,
                    "handle": p.handle,
                    "vendor": p.vendor,
                    "product_type": p.product_type,
                    "variants": [
                        {
                            "id": v.id,
                            "title": v.title,
                            "price": float(v.price),
                            "inventory_quantity": v.inventory_quantity,
                        }
                        for v in p.variants
                    ],
                    "images": [img.src for img in p.images] if p.images else [],
                }
                for p in products
            ]
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []
    
    def get_orders(self, start_date: Optional[datetime] = None, limit: int = 250):
        """Get orders from Shopify"""
        try:
            params = {"limit": limit, "status": "any"}
            if start_date:
                params["created_at_min"] = start_date.isoformat()
            
            orders = shopify.Order.find(**params)
            return [
                {
                    "id": o.id,
                    "order_number": o.order_number,
                    "email": o.email,
                    "total_price": float(o.total_price),
                    "created_at": o.created_at,
                    "financial_status": o.financial_status,
                    "fulfillment_status": o.fulfillment_status,
                    "line_items_count": len(o.line_items) if o.line_items else 0,
                }
                for o in orders
            ]
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            return []
    
    def close(self):
        """Close Shopify session"""
        shopify.ShopifyResource.clear_session()


# Global OAuth handler
shopify_oauth = ShopifyOAuth()
