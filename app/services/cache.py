import json
from typing import Optional, Any
import logging
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
            
    async def _execute_redis_command(self, command, *args, **kwargs):
        """Execute a Redis command with error handling."""
        try:
            return await command(*args, **kwargs)
        except aioredis.exceptions.ConnectionError as e:
            logging.error(f"Redis connection error: {e}")
            return None
        except aioredis.exceptions.RedisError as e:
            logging.error(f"Redis error: {e}")
            return None
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        await self.init()
        value = await self._execute_redis_command(self.redis.get, key)
        if value:
            return json.loads(value)
        return None
    
    async def set(self, key: str, value: Any, expire: int = None) -> bool:
        """Set value in cache with optional expiration"""
        await self.init()
        result = await self._execute_redis_command(self.redis.set,
            key,
            json.dumps(value),
            ex=expire or settings.CACHE_TTL
        )
        return result is not None
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        await self.init()
        result = await self._execute_redis_command(self.redis.delete,key)
        return result is not None and result > 0
    
    async def is_whitelisted(self, ip: str) -> bool:
        """Check if IP is whitelisted"""
        result = await self.get(f"whitelist:{ip}")
        return result is not None
    
    async def whitelist_ip(self, ip: str) -> bool:
        """Whitelist an IP address"""
        result = await self.set(
            f"whitelist:{ip}",
            True,
            expire=settings.WHITELIST_TTL
        )
        return result is not None
    
    async def close(self):
        """Close Redis connection"""
        try:
            if self.redis:
                await self.redis.close()
        except Exception as e:
            logging.error(f"Error closing Redis connection: {e}")

# Create singleton instance
cache_service = CacheService() 