"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class CampaignStatusEnum(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class IntegrationStatusEnum(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PENDING = "pending"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    timezone: str = "UTC"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    timezone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: UserRoleEnum
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Campaign Schemas
class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    platform: str
    daily_budget: Optional[float] = Field(None, gt=0)
    total_budget: Optional[float] = Field(None, gt=0)
    bid_strategy: Optional[str] = None
    target_roas: Optional[float] = Field(None, gt=0)
    target_cpa: Optional[float] = Field(None, gt=0)
    target_audience: Optional[Dict[str, Any]] = None
    target_locations: Optional[List[str]] = None
    target_keywords: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class CampaignCreate(CampaignBase):
    ai_enabled: bool = True


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CampaignStatusEnum] = None
    daily_budget: Optional[float] = Field(None, gt=0)
    total_budget: Optional[float] = Field(None, gt=0)
    bid_strategy: Optional[str] = None
    target_roas: Optional[float] = None
    target_cpa: Optional[float] = None
    ai_enabled: Optional[bool] = None


class CampaignResponse(CampaignBase):
    id: int
    user_id: int
    status: CampaignStatusEnum
    external_id: Optional[str] = None
    impressions: int
    clicks: int
    conversions: int
    cost: float
    revenue: float
    ctr: float
    cpc: float
    cpa: float
    roas: float
    ai_enabled: bool
    ai_recommendations: Optional[Dict[str, Any]] = None
    optimization_score: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Integration Schemas
class IntegrationBase(BaseModel):
    platform: str = Field(..., pattern="^(shopify|google_ads|facebook)$")
    shop_domain: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class IntegrationCreate(IntegrationBase):
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    access_token: Optional[str] = None


class IntegrationUpdate(BaseModel):
    status: Optional[IntegrationStatusEnum] = None
    settings: Optional[Dict[str, Any]] = None


class IntegrationResponse(BaseModel):
    id: int
    user_id: int
    platform: str
    status: IntegrationStatusEnum
    shop_domain: Optional[str] = None
    account_id: Optional[str] = None
    last_sync: Optional[datetime] = None
    sync_status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Analytics Schemas
class AnalyticsQuery(BaseModel):
    campaign_id: Optional[int] = None
    start_date: datetime
    end_date: datetime
    metrics: List[str] = ["impressions", "clicks", "conversions", "cost", "revenue"]
    group_by: Optional[str] = Field(None, pattern="^(day|week|month)$")


class AnalyticsDataPoint(BaseModel):
    date: datetime
    impressions: int
    clicks: int
    conversions: int
    cost: float
    revenue: float
    ctr: float
    cpc: float
    cpa: float
    roas: float
    conversion_rate: float


class AnalyticsResponse(BaseModel):
    campaign_id: Optional[int] = None
    start_date: datetime
    end_date: datetime
    data: List[AnalyticsDataPoint]
    summary: Dict[str, Any]


# Dashboard Schemas
class DashboardStats(BaseModel):
    total_campaigns: int
    active_campaigns: int
    total_spend: float
    total_revenue: float
    total_impressions: int
    total_clicks: int
    total_conversions: int
    average_roas: float
    average_ctr: float
    average_cpc: float


class DashboardResponse(BaseModel):
    stats: DashboardStats
    top_campaigns: List[CampaignResponse]
    recent_activity: List[Dict[str, Any]]
    ai_insights: List[Dict[str, Any]]


# Shopify Schemas
class ShopifyProduct(BaseModel):
    id: int
    title: str
    handle: str
    vendor: str
    product_type: str
    price: float
    inventory_quantity: int
    image_url: Optional[str] = None


class ShopifyOrder(BaseModel):
    id: int
    order_number: str
    created_at: datetime
    total_price: float
    customer_email: Optional[str] = None
    line_items_count: int
    fulfillment_status: Optional[str] = None


class ShopifyStats(BaseModel):
    total_products: int
    total_orders: int
    total_revenue: float
    total_customers: int
    average_order_value: float


# ML Schemas
class MLPredictionRequest(BaseModel):
    campaign_id: int
    features: Dict[str, Any]


class MLPredictionResponse(BaseModel):
    campaign_id: int
    predicted_roas: float
    predicted_conversions: int
    recommended_budget: float
    confidence: float
    recommendations: List[str]


class MLModelInfo(BaseModel):
    id: int
    name: str
    version: str
    model_type: str
    algorithm: str
    metrics: Dict[str, Any]
    is_active: bool
    training_date: datetime
    
    class Config:
        from_attributes = True


# API Response Schemas
class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[Any] = None
