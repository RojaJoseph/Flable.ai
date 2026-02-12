"""
Redis client for caching and session management
Gracefully handles Redis being unavailable
"""

import redis.asyncio as redis
from typing import Optional, Any
import json
from utils.config import settings
from loguru import logger


class RedisClient:
    """Async Redis client wrapper with fallback support"""
    
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self.available = False
    
    async def connect(self):
        """Connect to Redis (optional)"""
        try:
            self.redis = await redis.from_url(
                settings.REDIS_URL,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=2
            )
            await self.redis.ping()
            self.available = True
            logger.info("Redis connected successfully")
        except Exception as e:
            self.available = False
            self.redis = None
            logger.warning(f"Redis not available: {e}. Running without cache.")
    
    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
    
    async def ping(self) -> bool:
        """Test Redis connection"""
        if not self.redis:
            await self.connect()
        try:
            return await self.redis.ping() if self.redis else False
        except:
            self.available = False
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis (returns None if Redis unavailable)"""
        if not self.available or not self.redis:
            return None
        try:
            value = await self.redis.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            logger.warning(f"Redis get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in Redis (silently fails if Redis unavailable)"""
        if not self.available or not self.redis:
            return False
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            await self.redis.setex(key, expire, value)
            return True
        except Exception as e:
            logger.warning(f"Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        if not self.available or not self.redis:
            return False
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Redis delete error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.available or not self.redis:
            return False
        try:
            return await self.redis.exists(key)
        except Exception as e:
            logger.warning(f"Redis exists error: {e}")
            return False
    
    async def incr(self, key: str) -> int:
        """Increment counter"""
        if not self.available or not self.redis:
            return 0
        try:
            return await self.redis.incr(key)
        except Exception as e:
            logger.warning(f"Redis incr error: {e}")
            return 0
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration on key"""
        if not self.available or not self.redis:
            return False
        try:
            return await self.redis.expire(key, seconds)
        except Exception as e:
            logger.warning(f"Redis expire error: {e}")
            return False
    
    async def keys(self, pattern: str) -> list:
        """Get keys matching pattern"""
        if not self.available or not self.redis:
            return []
        try:
            return await self.redis.keys(pattern)
        except Exception as e:
            logger.warning(f"Redis keys error: {e}")
            return []


# Global Redis client instance
redis_client = RedisClient()
