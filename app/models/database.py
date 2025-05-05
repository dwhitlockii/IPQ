from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from databases import Database
import logging
from ..config.settings import settings

# Database URL
database = Database(settings.DATABASE_URL)
Base = declarative_base()

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    device_fingerprint = Column(String, nullable=True)
    risk_score = Column(Float)
    is_proxy = Column(Boolean)
    is_vpn = Column(Boolean)
    is_tor = Column(Boolean)
    country_code = Column(String)
    city = Column(String, nullable=True)
    action_taken = Column(String)  # "block", "throttle", "challenge", "allow"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    request_path = Column(String)
    user_agent = Column(String)

class WhitelistedIP(Base):
    __tablename__ = "whitelisted_ips"
    
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Create tables
try:
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
except exc.SQLAlchemyError as e:
    logging.error(f"Database error: {e}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")