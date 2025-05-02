from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "SentinelShield"
    DEBUG: bool = False
    
    # IPQS API Settings
    IPQS_API_KEY: str
    IPQS_BASE_URL: str = "https://www.ipqualityscore.com/api/json/ip"
    IPQS_DEVICE_BASE_URL: str = "https://www.ipqualityscore.com/api/json/device"
    
    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # SQLite Settings
    DATABASE_URL: str = "sqlite:///./sentinel_shield.db"
    
    # Security Settings
    HIGH_RISK_THRESHOLD: float = 75.0
    MEDIUM_RISK_THRESHOLD: float = 50.0
    CHALLENGE_ENABLED: bool = True
    THROTTLE_DELAY: int = 5  # seconds
    
    # Cache Settings
    CACHE_TTL: int = 3600  # 1 hour
    WHITELIST_TTL: int = 86400  # 24 hours
    
    # Admin Settings
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str
    SECRET_KEY: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 