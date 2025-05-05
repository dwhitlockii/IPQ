from prometheus_client import Counter, Histogram, Gauge
from typing import Dict


# Request metrics
REQUEST_COUNT = Counter(
    'sentinel_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'sentinel_http_request_duration_seconds',
    'HTTP request latency',
    ['endpoint']
)

# IP Quality metrics
RISK_SCORE = Histogram(
    'sentinel_ip_risk_scores',
    'Distribution of IP risk scores',
    buckets=[0, 25, 50, 75, 90, 100]
)

BLOCKED_IPS = Counter(
    'sentinel_blocked_ips_total',
    'Number of blocked IP addresses'
)

TOTAL_REQUESTS = Counter(
    'sentinel_total_requests',
    'Total number of requests'
)

REQUESTS_BY_STATUS = Counter(
    'sentinel_requests_by_status',
    'Total requests by status',
    ['status']
)

AVERAGE_LATENCY = Gauge('sentinel_average_latency_seconds', 'Average request latency in seconds')
# Cache metrics
CACHE_HITS = Counter(
    'sentinel_cache_hits_total',
    'Number of cache hits'
)

CACHE_MISSES = Counter(
    'sentinel_cache_misses_total',
    'Number of cache misses'
)

# System metrics
ACTIVE_CONNECTIONS = Gauge(
    'sentinel_active_connections',
    'Number of active connections'
)

WHITELISTED_IPS = Gauge(
    'sentinel_whitelisted_ips',
    'Number of whitelisted IPs'
)

class MetricsCollector:
    """Centralized metrics collection"""
    
    
    @classmethod
    def record_request(cls, method: str, endpoint: str, status: int):
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    
    @classmethod
    def record_latency(cls, endpoint: str, duration: float):
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
    
    @classmethod
    def record_risk_score(cls, score: float):
        RISK_SCORE.observe(score)
    
    @classmethod
    def record_blocked_ip(cls):
        BLOCKED_IPS.inc()
    
    @classmethod
    def increment_total_requests(cls):
        TOTAL_REQUESTS.inc()

    @classmethod
    def increment_requests_by_status(cls, status: str):
        REQUESTS_BY_STATUS.labels(status=status).inc()

    @classmethod
    def set_average_latency(cls, latency: float):
        AVERAGE_LATENCY.set(latency)

    @classmethod
    def record_cache_hit(cls):
        CACHE_HITS.inc()
    
    @classmethod
    def record_cache_miss(cls):
        CACHE_MISSES.inc()
    
    @classmethod
    def set_active_connections(cls, count: int):
        ACTIVE_CONNECTIONS.set(count)
    
    @classmethod
    def set_whitelisted_ips(cls, count: int):
        WHITELISTED_IPS.set(count) 