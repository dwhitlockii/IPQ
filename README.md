# SentinelShield

SentinelShield is a Python-based microservice that integrates with IPQualityScore's IP reputation and device fingerprint APIs to provide real-time threat filtering for web applications. It can be easily integrated with NGINX reverse proxy, AWS WAF, or Cloudflare Workers.

## Features

- Real-time IP reputation checking
- Device fingerprint analysis
- Risk-based request handling:
  - High-risk: Block (HTTP 403)
  - Medium-risk: Challenge (CAPTCHA) or Throttle
  - Low-risk: Allow
- Redis caching for improved performance
- SQLite audit logging
- Admin dashboard for monitoring and management
- Docker support for easy deployment
- NGINX reverse proxy configuration
- Configurable risk thresholds and actions

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- IPQS API Key
- Redis (included in Docker setup)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sentinelshield.git
   cd sentinelshield
   ```

2. Create a `.env` file:
   ```env
   IPQS_API_KEY=your_ipqs_api_key
   REDIS_PASSWORD=your_redis_password
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your_admin_password
   SECRET_KEY=your_secret_key
   ```

3. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the admin dashboard at:
   ```
   http://localhost/admin/dashboard
   ```

## Manual Setup (without Docker)

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (see `.env` example above)

4. Start the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Integration Options

### NGINX Reverse Proxy

The NGINX configuration is already included in `docker/nginx.conf`. If you're using a standalone NGINX installation, copy the configuration and adjust the upstream server address.

### AWS WAF Integration

1. Create a Lambda function using the provided code
2. Configure AWS WAF web ACL:
   - Create a custom rule
   - Add a rate-based rule if desired
   - Set up AWS WAF to invoke the Lambda function

### Cloudflare Workers

1. Create a new Worker
2. Implement the request handling logic using the provided code as a reference
3. Configure Worker routes in Cloudflare dashboard

## Configuration

Key settings in `app/config/settings.py`:

- `HIGH_RISK_THRESHOLD`: Score threshold for high-risk requests (default: 75)
- `MEDIUM_RISK_THRESHOLD`: Score threshold for medium-risk requests (default: 50)
- `CHALLENGE_ENABLED`: Enable/disable CAPTCHA challenges
- `THROTTLE_DELAY`: Delay in seconds for throttled requests
- `CACHE_TTL`: Cache duration for IP reputation data
- `WHITELIST_TTL`: Duration for whitelisted IPs

## Admin Dashboard

The admin dashboard provides:

- Real-time monitoring of requests
- Risk score visualization
- IP whitelisting capabilities
- Audit log viewing
- Flag indicators for proxy/VPN/TOR usage

## API Endpoints

- `/health`: Health check endpoint
- `/admin/dashboard`: Admin dashboard
- `/admin/logs`: Get recent audit logs
- `/admin/whitelist/{ip_address}`: Whitelist an IP address

## Security Considerations

1. Always use strong passwords for Redis and admin access
2. Keep the IPQS API key secure
3. Regularly update the whitelist
4. Monitor the audit logs for suspicious patterns
5. Use HTTPS in production
6. Consider implementing rate limiting

## Logging

Logs are stored in:
- SQLite database (`data/sentinel_shield.db`)
- NGINX access logs
- Application logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 