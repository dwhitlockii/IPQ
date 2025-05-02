from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.wsgi import WSGIMiddleware
from prometheus_client import make_asgi_app
import secrets
import time
from datetime import datetime, timezone
from typing import Optional
import asyncio

from .config.settings import settings
from .config.monitoring import MetricsCollector
from .services.ipqs import ipqs_service
from .services.cache import cache_service
from .models.database import database, AuditLog, WhitelistedIP

app = FastAPI(title=settings.APP_NAME)
security = HTTPBasic()

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", WSGIMiddleware(metrics_app))

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Record metrics
    MetricsCollector.record_request(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    )
    MetricsCollector.record_latency(request.url.path, duration)
    
    return response

@app.on_event("startup")
async def startup():
    await database.connect()
    await cache_service.init()
    
    # Initialize metrics
    whitelist_count = await database.fetch_val(
        "SELECT COUNT(*) FROM whitelisted_ips WHERE expires_at > ?",
        [datetime.now(timezone.utc).timestamp()]
    )
    MetricsCollector.set_whitelisted_ips(whitelist_count)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await cache_service.close()

async def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    is_admin = secrets.compare_digest(credentials.username, settings.ADMIN_USERNAME) and \
               secrets.compare_digest(credentials.password, settings.ADMIN_PASSWORD)
    if not is_admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

async def log_request(request_data: dict, action: str):
    """Log request details to database and update metrics"""
    query = AuditLog.__table__.insert().values(
        ip_address=request_data["ip_address"],
        device_fingerprint=request_data.get("device_fingerprint"),
        risk_score=request_data["risk_score"],
        is_proxy=request_data["is_proxy"],
        is_vpn=request_data["is_vpn"],
        is_tor=request_data["is_tor"],
        country_code=request_data["country_code"],
        city=request_data.get("city"),
        action_taken=action,
        request_path=request_data["request_path"],
        user_agent=request_data["user_agent"]
    )
    await database.execute(query)
    
    # Update metrics
    MetricsCollector.record_risk_score(request_data["risk_score"])
    if action == "high":
        MetricsCollector.record_blocked_ip()

@app.middleware("http")
async def shield_middleware(request: Request, call_next):
    # Skip admin dashboard, metrics, and static files
    if request.url.path.startswith(("/admin", "/static", "/metrics")):
        return await call_next(request)
    
    # Get IP and headers
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    device_fingerprint = request.headers.get("x-device-fingerprint")
    
    # Check whitelist
    if await cache_service.is_whitelisted(ip_address):
        MetricsCollector.record_cache_hit()
        return await call_next(request)
    
    # Check cache first
    cache_key = f"ip:{ip_address}"
    cached_data = await cache_service.get(cache_key)
    
    if cached_data:
        MetricsCollector.record_cache_hit()
    else:
        MetricsCollector.record_cache_miss()
        # Get IP reputation
        ip_data = await ipqs_service.check_ip(ip_address, user_agent)
        
        # Get device reputation if fingerprint provided
        device_data = None
        if device_fingerprint:
            device_data = await ipqs_service.check_device(device_fingerprint)
        
        # Calculate risk level
        risk_level = ipqs_service.calculate_risk_level(ip_data, device_data)
        
        # Cache the results
        cached_data = {
            "ip_address": ip_address,
            "device_fingerprint": device_fingerprint,
            "risk_score": ip_data.get("fraud_score", 0),
            "is_proxy": ip_data.get("proxy", False),
            "is_vpn": ip_data.get("vpn", False),
            "is_tor": ip_data.get("tor", False),
            "country_code": ip_data.get("country_code", "Unknown"),
            "city": ip_data.get("city", None),
            "risk_level": risk_level,
            "request_path": str(request.url),
            "user_agent": user_agent
        }
        await cache_service.set(cache_key, cached_data)
    
    # Log request and update metrics
    await log_request(cached_data, cached_data["risk_level"])
    
    # Handle based on risk level
    if cached_data["risk_level"] == "high":
        return JSONResponse(
            status_code=403,
            content={"error": "Access denied due to high risk score"}
        )
    elif cached_data["risk_level"] == "medium" and settings.CHALLENGE_ENABLED:
        # Redirect to challenge page
        return HTMLResponse(content="""
            <html>
                <head><title>Security Challenge</title></head>
                <body>
                    <h1>Please Complete Security Challenge</h1>
                    <div class="g-recaptcha" data-sitekey="YOUR_RECAPTCHA_SITE_KEY"></div>
                    <script src='https://www.google.com/recaptcha/api.js'></script>
                </body>
            </html>
        """)
    elif cached_data["risk_level"] == "medium":
        # Apply throttling
        await asyncio.sleep(settings.THROTTLE_DELAY)
    
    return await call_next(request)

@app.get("/admin/dashboard")
async def admin_dashboard(_: bool = Depends(verify_admin)):
    """Admin dashboard HTML page"""
    with open("app/static/dashboard.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/admin/logs")
async def get_logs(_: bool = Depends(verify_admin)):
    """Get recent audit logs"""
    query = "SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 100"
    logs = await database.fetch_all(query)
    return {"logs": logs}

@app.post("/admin/whitelist/{ip_address}")
async def whitelist_ip(ip_address: str, _: bool = Depends(verify_admin)):
    """Whitelist an IP address"""
    await cache_service.whitelist_ip(ip_address)
    # Also store in database
    query = WhitelistedIP.__table__.insert().values(
        ip_address=ip_address,
        expires_at=datetime.now(timezone.utc).timestamp() + settings.WHITELIST_TTL
    )
    await database.execute(query)
    return {"message": f"IP {ip_address} has been whitelisted"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/api/check-ip")
async def check_ip(ip: str, request: Request):
    """
    Check IP reputation and return detailed results
    """
    # Check whitelist
    if await cache_service.is_whitelisted(ip):
        return {"status": "whitelisted", "risk_level": "low"}
    
    # Check cache first
    cache_key = f"ip:{ip}"
    cached_data = await cache_service.get(cache_key)
    
    if not cached_data:
        # Get IP reputation
        user_agent = request.headers.get("user-agent", "Unknown")
        ip_data = await ipqs_service.check_ip(ip, user_agent)
        
        # Calculate risk level
        risk_level = ipqs_service.calculate_risk_level(ip_data, None)
        
        # Cache the results
        cached_data = {
            "ip_address": ip,
            "risk_score": ip_data.get("fraud_score", 0),
            "is_proxy": ip_data.get("proxy", False),
            "is_vpn": ip_data.get("vpn", False),
            "is_tor": ip_data.get("tor", False),
            "country_code": ip_data.get("country_code", "Unknown"),
            "city": ip_data.get("city", None),
            "risk_level": risk_level,
            "request_path": str(request.url),
            "user_agent": user_agent
        }
        await cache_service.set(cache_key, cached_data)
        
        # Log request
        await log_request(cached_data, risk_level)
    
    return cached_data 

@app.get("/admin/metrics")
async def admin_metrics(_: bool = Depends(verify_admin)):
    """Get detailed system metrics"""
    return {
        "requests": {
            "total": REQUEST_COUNT._value.sum(),
            "by_status": {
                "200": REQUEST_COUNT.labels(status=200)._value,
                "403": REQUEST_COUNT.labels(status=403)._value,
                "500": REQUEST_COUNT.labels(status=500)._value
            }
        },
        "performance": {
            "avg_latency": REQUEST_LATENCY._sum.sum() / REQUEST_LATENCY._count.sum(),
            "cache_hit_rate": CACHE_HITS._value.sum() / (CACHE_HITS._value.sum() + CACHE_MISSES._value.sum()) if (CACHE_HITS._value.sum() + CACHE_MISSES._value.sum()) > 0 else 0
        },
        "security": {
            "blocked_ips": BLOCKED_IPS._value.sum(),
            "whitelisted_ips": WHITELISTED_IPS._value,
            "avg_risk_score": RISK_SCORE._sum.sum() / RISK_SCORE._count.sum() if RISK_SCORE._count.sum() > 0 else 0
        }
    } 