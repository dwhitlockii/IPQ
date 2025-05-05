import pytest
from app.config.settings import validate_settings, settings

def test_validate_settings_valid():
    settings.IPQS_API_KEY = "test_key"
    settings.REDIS_HOST = "localhost"
    settings.REDIS_PORT = 6379
    settings.RISK_THRESHOLD_HIGH = 80.0
    settings.RISK_THRESHOLD_MEDIUM = 50.0
    settings.RISK_THRESHOLD_LOW = 20.0
    
    validate_settings() 

def test_validate_settings_invalid_api_key():
    settings.IPQS_API_KEY = ""
    settings.REDIS_HOST = "localhost"
    settings.REDIS_PORT = 6379
    settings.RISK_THRESHOLD_HIGH = 80.0
    settings.RISK_THRESHOLD_MEDIUM = 50.0
    settings.RISK_THRESHOLD_LOW = 20.0

    with pytest.raises(ValueError):
        validate_settings()

def test_validate_settings_invalid_redis_host():
    settings.IPQS_API_KEY = "test_key"
    settings.REDIS_HOST = ""
    settings.REDIS_PORT = 6379
    settings.RISK_THRESHOLD_HIGH = 80.0
    settings.RISK_THRESHOLD_MEDIUM = 50.0
    settings.RISK_THRESHOLD_LOW = 20.0

    with pytest.raises(ValueError):
        validate_settings()

def test_validate_settings_invalid_redis_port():
    settings.IPQS_API_KEY = "test_key"
    settings.REDIS_HOST = "localhost"
    settings.REDIS_PORT = "invalid"
    settings.RISK_THRESHOLD_HIGH = 80.0
    settings.RISK_THRESHOLD_MEDIUM = 50.0
    settings.RISK_THRESHOLD_LOW = 20.0
    with pytest.raises(ValueError):
        validate_settings()
        
def test_validate_settings_invalid_risk_threshold():
    settings.IPQS_API_KEY = "test_key"
    settings.REDIS_HOST = "localhost"
    settings.REDIS_PORT = 6379
    settings.RISK_THRESHOLD_HIGH = "invalid"
    settings.RISK_THRESHOLD_MEDIUM = 50.0
    settings.RISK_THRESHOLD_LOW = 20.0
    with pytest.raises(ValueError):
        validate_settings()