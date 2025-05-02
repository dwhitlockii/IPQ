import json
from typing import Optional, Any
from redis import asyncio as aioredis
from ..config.settings import settings

class CacheService:
    def __init__(self):
        self.redis = None
        
    async def init(self):
        """Initialize Redis connection"""
        if not self.redis:
            self.redis = aioredis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        await self.init()
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def set(self, key: str, value: Any, expire: int = None) -> bool:
        """Set value in cache with optional expiration"""
        await self.init()
        return await self.redis.set(
            key,
            json.dumps(value),
            ex=expire or settings.CACHE_TTL
        )
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        await self.init()
        return await self.redis.delete(key) > 0
    
    async def is_whitelisted(self, ip: str) -> bool:
        """Check if IP is whitelisted"""
        return await self.get(f"whitelist:{ip}") is not None
    
    async def whitelist_ip(self, ip: str) -> bool:
        """Whitelist an IP address"""
        return await self.set(
            f"whitelist:{ip}",
            True,
            expire=settings.WHITELIST_TTL
        )
    
    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()

# Create singleton instance
cache_service = CacheService() 