"""
Analytics API Routes - Campaign Performance Analysis
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta

from database.connection import get_db
from database.models import User, Campaign, CampaignAnalytics
from schemas import schemas
from utils.auth_utils import get_current_user

router = APIRouter()


@router.post("/query", response_model=schemas.AnalyticsResponse)
async def query_analytics(
    query_params: schemas.AnalyticsQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query analytics data for campaigns"""
    
    # Build base query
    analytics_query = db.query(CampaignAnalytics).join(Campaign).filter(
        Campaign.user_id == current_user.id,
        CampaignAnalytics.date >= query_params.start_date,
        CampaignAnalytics.date <= query_params.end_date
    )
    
    # Filter by campaign if specified
    if query_params.campaign_id:
        analytics_query = analytics_query.filter(
            CampaignAnalytics.campaign_id == query_params.campaign_id
        )
    
    analytics_data = analytics_query.all()
    
    # Group data if requested
    if query_params.group_by:
        # Implementation for grouping by day/week/month
        pass
    
    # Calculate summary metrics
    total_impressions = sum(a.impressions for a in analytics_data)
    total_clicks = sum(a.clicks for a in analytics_data)
    total_conversions = sum(a.conversions for a in analytics_data)
    total_cost = sum(a.cost for a in analytics_data)
    total_revenue = sum(a.revenue for a in analytics_data)
    
    summary = {
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "total_conversions": total_conversions,
        "total_cost": total_cost,
        "total_revenue": total_revenue,
        "average_ctr": (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
        "average_cpc": (total_cost / total_clicks) if total_clicks > 0 else 0,
        "average_cpa": (total_cost / total_conversions) if total_conversions > 0 else 0,
        "total_roas": (total_revenue / total_cost) if total_cost > 0 else 0
    }
    
    # Format response
    data_points = [
        schemas.AnalyticsDataPoint(
            date=a.date,
            impressions=a.impressions,
            clicks=a.clicks,
            conversions=a.conversions,
            cost=a.cost,
            revenue=a.revenue,
            ctr=a.ctr,
            cpc=a.cpc,
            cpa=a.cpa,
            roas=a.roas,
            conversion_rate=a.conversion_rate
        )
        for a in analytics_data
    ]
    
    return schemas.AnalyticsResponse(
        campaign_id=query_params.campaign_id,
        start_date=query_params.start_date,
        end_date=query_params.end_date,
        data=data_points,
        summary=summary
    )


@router.get("/campaign/{campaign_id}/trends")
async def get_campaign_trends(
    campaign_id: int,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get performance trends for a campaign"""
    
    # Verify campaign belongs to user
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Get analytics data for the period
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    analytics = db.query(CampaignAnalytics).filter(
        CampaignAnalytics.campaign_id == campaign_id,
        CampaignAnalytics.date >= start_date,
        CampaignAnalytics.date <= end_date
    ).order_by(CampaignAnalytics.date).all()
    
    # Calculate trends
    trends = {
        "period_days": days,
        "data_points": len(analytics),
        "daily_data": [
            {
                "date": a.date.isoformat(),
                "impressions": a.impressions,
                "clicks": a.clicks,
                "conversions": a.conversions,
                "cost": a.cost,
                "revenue": a.revenue,
                "roas": a.roas
            }
            for a in analytics
        ],
        "totals": {
            "impressions": sum(a.impressions for a in analytics),
            "clicks": sum(a.clicks for a in analytics),
            "conversions": sum(a.conversions for a in analytics),
            "cost": sum(a.cost for a in analytics),
            "revenue": sum(a.revenue for a in analytics)
        }
    }
    
    return trends


@router.get("/overview")
async def get_analytics_overview(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics overview for all campaigns"""
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get all campaigns for user
    campaigns = db.query(Campaign).filter(
        Campaign.user_id == current_user.id
    ).all()
    
    campaign_ids = [c.id for c in campaigns]
    
    # Get analytics data
    analytics = db.query(CampaignAnalytics).filter(
        CampaignAnalytics.campaign_id.in_(campaign_ids),
        CampaignAnalytics.date >= start_date,
        CampaignAnalytics.date <= end_date
    ).all()
    
    # Calculate metrics
    total_spend = sum(a.cost for a in analytics)
    total_revenue = sum(a.revenue for a in analytics)
    total_impressions = sum(a.impressions for a in analytics)
    total_clicks = sum(a.clicks for a in analytics)
    total_conversions = sum(a.conversions for a in analytics)
    
    return {
        "period": f"Last {days} days",
        "total_campaigns": len(campaigns),
        "active_campaigns": len([c for c in campaigns if c.status == "active"]),
        "metrics": {
            "total_spend": total_spend,
            "total_revenue": total_revenue,
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "average_ctr": (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
            "average_roas": (total_revenue / total_spend) if total_spend > 0 else 0
        }
    }


@router.get("/compare")
async def compare_campaigns(
    campaign_ids: str,  # Comma-separated campaign IDs
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare performance of multiple campaigns"""
    
    # Parse campaign IDs
    try:
        ids = [int(id.strip()) for id in campaign_ids.split(",")]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid campaign IDs format"
        )
    
    # Verify campaigns belong to user
    campaigns = db.query(Campaign).filter(
        Campaign.id.in_(ids),
        Campaign.user_id == current_user.id
    ).all()
    
    if len(campaigns) != len(ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more campaigns not found"
        )
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get analytics for each campaign
    comparison = []
    for campaign in campaigns:
        analytics = db.query(CampaignAnalytics).filter(
            CampaignAnalytics.campaign_id == campaign.id,
            CampaignAnalytics.date >= start_date,
            CampaignAnalytics.date <= end_date
        ).all()
        
        total_cost = sum(a.cost for a in analytics)
        total_revenue = sum(a.revenue for a in analytics)
        
        comparison.append({
            "campaign_id": campaign.id,
            "campaign_name": campaign.name,
            "status": campaign.status,
            "metrics": {
                "impressions": sum(a.impressions for a in analytics),
                "clicks": sum(a.clicks for a in analytics),
                "conversions": sum(a.conversions for a in analytics),
                "cost": total_cost,
                "revenue": total_revenue,
                "roas": (total_revenue / total_cost) if total_cost > 0 else 0
            }
        })
    
    return {
        "period": f"Last {days} days",
        "campaigns_compared": len(comparison),
        "comparison": comparison
    }
