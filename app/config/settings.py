from pydantic_settings import BaseSettings, SettingsConfigDict
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
    RISK_THRESHOLD_HIGH: float = 75.0
    RISK_THRESHOLD_MEDIUM: float = 50.0
    RISK_THRESHOLD_LOW: float = 25.0
    CHALLENGE_ENABLED: bool = True
    THROTTLE_DELAY: int = 5  # seconds

    # Cache Settings
    CACHE_TTL: int = 3600  # 1 hour
    WHITELIST_TTL: int = 86400  # 24 hours

    # Admin Settings
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

def validate_settings(settings):
    """Validates the settings to ensure they are valid."""
    if not settings.IPQS_API_KEY:
        raise ValueError("IPQS_API_KEY cannot be empty.")
    if not settings.REDIS_HOST:
        raise ValueError("REDIS_HOST cannot be empty.")
    if not isinstance(settings.REDIS_PORT, int):
        raise ValueError("REDIS_PORT must be an integer.")
    if not isinstance(settings.RISK_THRESHOLD_HIGH, float):
        raise ValueError("RISK_THRESHOLD_HIGH must be a float.")
    if not isinstance(settings.RISK_THRESHOLD_MEDIUM, float):
        raise ValueError("RISK_THRESHOLD_MEDIUM must be a float.")
    if not isinstance(settings.RISK_THRESHOLD_LOW, float):
        raise ValueError("RISK_THRESHOLD_LOW must be a float.")




settings = Settings()
validate_settings(settings)


settings = Settings() 