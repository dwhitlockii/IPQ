# app/config/settings.py

import os
from typing import List

APP_NAME = os.getenv("APP_NAME", "Sentinel Shield")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password")
IPQS_API_KEY = os.getenv("IPQS_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./audit.db")
WHITELIST_TTL = int(os.getenv("WHITELIST_TTL", 3600))  # Default to 1 hour
RISK_THRESHOLD_HIGH = float(os.getenv("RISK_THRESHOLD_HIGH", 85.0))
RISK_THRESHOLD_MEDIUM = float(os.getenv("RISK_THRESHOLD_MEDIUM", 60.0))
RISK_THRESHOLD_LOW = float(os.getenv("RISK_THRESHOLD_LOW", 30.0))
CHALLENGE_ENABLED = os.getenv("CHALLENGE_ENABLED", "False").lower() == "true"
THROTTLE_DELAY = int(os.getenv("THROTTLE_DELAY", 5))  # Default to 5 seconds

def validate_settings():
    if not IPQS_API_KEY:
        raise ValueError("IPQS_API_KEY must be set.")
    if not REDIS_HOST:
        raise ValueError("REDIS_HOST must be set.")
    if not isinstance(REDIS_PORT, int):
        raise ValueError("REDIS_PORT must be an integer.")
    if not isinstance(RISK_THRESHOLD_HIGH, float):
        raise ValueError("RISK_THRESHOLD_HIGH must be a float.")
    if not isinstance(RISK_THRESHOLD_MEDIUM, float):
        raise ValueError("RISK_THRESHOLD_MEDIUM must be a float.")
    if not isinstance(RISK_THRESHOLD_LOW, float):
        raise ValueError("RISK_THRESHOLD_LOW must be a float.")

validate_settings()