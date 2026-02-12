"""
Campaign Management API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.connection import get_db
from database.models import User, Campaign, CampaignStatus
from schemas import schemas
from utils.auth_utils import get_current_user

router = APIRouter()


@router.get("", response_model=List[schemas.CampaignResponse])
@router.get("/", response_model=List[schemas.CampaignResponse])
async def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = None,
    platform: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all campaigns for current user"""
    
    query = db.query(Campaign).filter(Campaign.user_id == current_user.id)
    
    if status:
        query = query.filter(Campaign.status == status)
    if platform:
        query = query.filter(Campaign.platform == platform)
    
    campaigns = query.offset(skip).limit(limit).all()
    return campaigns


@router.get("/{campaign_id}", response_model=schemas.CampaignResponse)
async def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific campaign"""
    
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    return campaign


@router.post("/", response_model=schemas.CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: schemas.CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new campaign"""
    
    new_campaign = Campaign(
        user_id=current_user.id,
        name=campaign_data.name,
        description=campaign_data.description,
        platform=campaign_data.platform,
        status=CampaignStatus.DRAFT,
        daily_budget=campaign_data.daily_budget,
        total_budget=campaign_data.total_budget,
        bid_strategy=campaign_data.bid_strategy,
        target_roas=campaign_data.target_roas,
        target_cpa=campaign_data.target_cpa,
        target_audience=campaign_data.target_audience,
        target_locations=campaign_data.target_locations,
        target_keywords=campaign_data.target_keywords,
        start_date=campaign_data.start_date,
        end_date=campaign_data.end_date,
        ai_enabled=campaign_data.ai_enabled
    )
    
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    
    return new_campaign


@router.put("/{campaign_id}", response_model=schemas.CampaignResponse)
async def update_campaign(
    campaign_id: int,
    campaign_data: schemas.CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a campaign"""
    
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Update only provided fields
    update_data = campaign_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)
    
    campaign.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(campaign)
    
    return campaign


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a campaign"""
    
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    db.delete(campaign)
    db.commit()
    
    return None


@router.post("/{campaign_id}/activate", response_model=schemas.CampaignResponse)
async def activate_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activate a campaign"""
    
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign.status = CampaignStatus.ACTIVE
    campaign.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(campaign)
    
    return campaign


@router.post("/{campaign_id}/pause", response_model=schemas.CampaignResponse)
async def pause_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Pause a campaign"""
    
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign.status = CampaignStatus.PAUSED
    campaign.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(campaign)
    
    return campaign


@router.get("/{campaign_id}/performance")
async def get_campaign_performance(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get campaign performance metrics"""
    
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    return {
        "campaign_id": campaign.id,
        "name": campaign.name,
        "status": campaign.status,
        "metrics": {
            "impressions": campaign.impressions,
            "clicks": campaign.clicks,
            "conversions": campaign.conversions,
            "cost": campaign.cost,
            "revenue": campaign.revenue,
            "ctr": campaign.ctr,
            "cpc": campaign.cpc,
            "cpa": campaign.cpa,
            "roas": campaign.roas
        },
        "optimization_score": campaign.optimization_score,
        "ai_recommendations": campaign.ai_recommendations
    }
