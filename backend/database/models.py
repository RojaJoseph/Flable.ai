"""
Database Models for Flable.ai
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, 
    ForeignKey, JSON, Text, Enum as SQLEnum, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class IntegrationStatus(str, enum.Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PENDING = "pending"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String(500))
    company_name = Column(String(255))
    phone = Column(String(50))
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")
    integrations = relationship("Integration", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"


class Campaign(Base):
    """Marketing Campaign model"""
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT)
    platform = Column(String(50))
    external_id = Column(String(255))
    
    # Budget and bidding
    daily_budget = Column(Float)
    total_budget = Column(Float)
    bid_strategy = Column(String(100))
    target_roas = Column(Float)
    target_cpa = Column(Float)
    
    # Targeting
    target_audience = Column(JSON)
    target_locations = Column(JSON)
    target_keywords = Column(JSON)
    
    # Performance metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    ctr = Column(Float, default=0.0)
    cpc = Column(Float, default=0.0)
    cpa = Column(Float, default=0.0)
    roas = Column(Float, default=0.0)
    
    # AI optimization
    ai_enabled = Column(Boolean, default=True)
    ai_recommendations = Column(JSON)
    optimization_score = Column(Float, default=0.0)
    
    # Dates
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="campaigns")
    ad_sets = relationship("AdSet", back_populates="campaign", cascade="all, delete-orphan")
    analytics = relationship("CampaignAnalytics", back_populates="campaign", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_campaign_user_status', 'user_id', 'status'),
        Index('idx_campaign_platform', 'platform'),
    )


class AdSet(Base):
    """Ad Set within a Campaign"""
    __tablename__ = "ad_sets"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    name = Column(String(255), nullable=False)
    external_id = Column(String(255))
    status = Column(String(50), default="active")
    budget = Column(Float)
    bid_amount = Column(Float)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    optimization_goal = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    campaign = relationship("Campaign", back_populates="ad_sets")
    ads = relationship("Ad", back_populates="ad_set", cascade="all, delete-orphan")


class Ad(Base):
    """Individual Ad"""
    __tablename__ = "ads"
    
    id = Column(Integer, primary_key=True, index=True)
    ad_set_id = Column(Integer, ForeignKey("ad_sets.id"), nullable=False)
    name = Column(String(255), nullable=False)
    external_id = Column(String(255))
    status = Column(String(50), default="active")
    headline = Column(String(500))
    description = Column(Text)
    image_url = Column(String(500))
    video_url = Column(String(500))
    landing_page_url = Column(String(500))
    call_to_action = Column(String(100))
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    ad_set = relationship("AdSet", back_populates="ads")


class Integration(Base):
    """Third-party platform integrations"""
    __tablename__ = "integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    status = Column(SQLEnum(IntegrationStatus), default=IntegrationStatus.PENDING)
    access_token = Column(Text)
    refresh_token = Column(Text)
    api_key = Column(String(255))
    api_secret = Column(String(255))
    shop_domain = Column(String(255))
    account_id = Column(String(255))
    settings = Column(JSON)
    last_sync = Column(DateTime)
    sync_status = Column(String(50))
    sync_errors = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="integrations")
    
    __table_args__ = (
        Index('idx_integration_user_platform', 'user_id', 'platform'),
    )


class CampaignAnalytics(Base):
    """Time-series analytics data"""
    __tablename__ = "campaign_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    ctr = Column(Float, default=0.0)
    cpc = Column(Float, default=0.0)
    cpa = Column(Float, default=0.0)
    roas = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    mobile_impressions = Column(Integer, default=0)
    desktop_impressions = Column(Integer, default=0)
    tablet_impressions = Column(Integer, default=0)
    geo_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    campaign = relationship("Campaign", back_populates="analytics")
    
    __table_args__ = (
        Index('idx_analytics_campaign_date', 'campaign_id', 'date'),
    )


class MLModel(Base):
    """ML Model tracking"""
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    version = Column(String(50), nullable=False)
    model_type = Column(String(100))
    algorithm = Column(String(100))
    file_path = Column(String(500))
    parameters = Column(JSON)
    metrics = Column(JSON)
    training_data_size = Column(Integer)
    training_date = Column(DateTime)
    is_active = Column(Boolean, default=False)
    is_deployed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class APIKey(Base):
    """API Keys for programmatic access"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), unique=True, nullable=False)
    key_preview = Column(String(20))
    scopes = Column(JSON)
    last_used = Column(DateTime)
    usage_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="api_keys")


class AuditLog(Base):
    """Audit trail"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    details = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_audit_user_action', 'user_id', 'action'),
        Index('idx_audit_created_at', 'created_at'),
    )
