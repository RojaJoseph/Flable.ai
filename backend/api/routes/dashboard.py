"""
Dashboard and Users API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from database.connection import get_db
from database.models import User, Campaign, CampaignAnalytics, Integration
from schemas import schemas
from utils.auth_utils import get_current_user, hash_password

dashboard_router = APIRouter()
users_router = APIRouter()


# ========== DASHBOARD ROUTES ==========

@dashboard_router.get("", response_model=schemas.DashboardResponse)
@dashboard_router.get("/", response_model=schemas.DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard overview with stats and insights"""
    
    # Get campaigns
    campaigns = db.query(Campaign).filter(
        Campaign.user_id == current_user.id
    ).all()
    
    active_campaigns = [c for c in campaigns if c.status == "active"]
    
    # Calculate totals
    total_spend = sum(c.cost for c in campaigns)
    total_revenue = sum(c.revenue for c in campaigns)
    total_impressions = sum(c.impressions for c in campaigns)
    total_clicks = sum(c.clicks for c in campaigns)
    total_conversions = sum(c.conversions for c in campaigns)
    
    # Calculate averages
    avg_roas = (total_revenue / total_spend) if total_spend > 0 else 0
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
    
    stats = schemas.DashboardStats(
        total_campaigns=len(campaigns),
        active_campaigns=len(active_campaigns),
        total_spend=total_spend,
        total_revenue=total_revenue,
        total_impressions=total_impressions,
        total_clicks=total_clicks,
        total_conversions=total_conversions,
        average_roas=avg_roas,
        average_ctr=avg_ctr,
        average_cpc=avg_cpc
    )
    
    # Top performing campaigns
    top_campaigns = sorted(campaigns, key=lambda c: c.roas, reverse=True)[:5]
    top_campaigns_response = [schemas.CampaignResponse.from_orm(c) for c in top_campaigns]
    
    # Recent activity (simplified)
    recent_activity = [
        {
            "type": "campaign_created",
            "campaign_id": c.id,
            "campaign_name": c.name,
            "timestamp": c.created_at.isoformat()
        }
        for c in sorted(campaigns, key=lambda c: c.created_at, reverse=True)[:5]
    ]
    
    # AI insights (placeholder)
    ai_insights = [
        {
            "type": "recommendation",
            "title": "Optimize Budget Allocation",
            "description": "Your top performing campaign could benefit from 20% budget increase",
            "priority": "high"
        },
        {
            "type": "alert",
            "title": "Low ROAS Detected",
            "description": "2 campaigns have ROAS below target. Consider pausing or optimizing.",
            "priority": "medium"
        }
    ]
    
    return schemas.DashboardResponse(
        stats=stats,
        top_campaigns=top_campaigns_response,
        recent_activity=recent_activity,
        ai_insights=ai_insights
    )


@dashboard_router.get("/stats/weekly")
async def get_weekly_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weekly performance statistics"""
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    campaigns = db.query(Campaign).filter(
        Campaign.user_id == current_user.id
    ).all()
    
    campaign_ids = [c.id for c in campaigns]
    
    analytics = db.query(CampaignAnalytics).filter(
        CampaignAnalytics.campaign_id.in_(campaign_ids),
        CampaignAnalytics.date >= start_date
    ).all()
    
    return {
        "period": "last_7_days",
        "total_spend": sum(a.cost for a in analytics),
        "total_revenue": sum(a.revenue for a in analytics),
        "total_conversions": sum(a.conversions for a in analytics),
        "daily_breakdown": {}  # Could add daily breakdown here
    }


# ========== USERS ROUTES ==========

@users_router.get("/me", response_model=schemas.UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@users_router.put("/me", response_model=schemas.UserResponse)
async def update_my_profile(
    user_update: schemas.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    
    return current_user


@users_router.put("/me/password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    
    from utils.auth_utils import verify_password
    
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters"
        )
    
    current_user.hashed_password = hash_password(new_password)
    current_user.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Password changed successfully"}


@users_router.get("/me/integrations")
async def get_my_integrations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all integrations for current user"""
    
    integrations = db.query(Integration).filter(
        Integration.user_id == current_user.id
    ).all()
    
    return {
        "user_id": current_user.id,
        "total_integrations": len(integrations),
        "integrations": [
            {
                "id": i.id,
                "platform": i.platform,
                "status": i.status,
                "last_sync": i.last_sync.isoformat() if i.last_sync else None
            }
            for i in integrations
        ]
    }


@users_router.delete("/me")
async def delete_my_account(
    password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account"""
    
    from utils.auth_utils import verify_password
    
    if not verify_password(password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is incorrect"
        )
    
    # Delete user (cascading will delete related data)
    db.delete(current_user)
    db.commit()
    
    return {"message": "Account deleted successfully"}
