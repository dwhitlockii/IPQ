# API Documentation

This document describes the API endpoints exposed by the SentinelShield application.

## Endpoints

### `/health`

*   **Method:** `GET`
*   **Description:** The health endpoint. This endpoint is used to check if the service is up and running.
*   **Request Format:** None.
*   **Response Format:** JSON
```
json
    {
        "message": "SentinelShield is running"
    }
    
```
*   **Status Codes:**
    *   `200 OK`: The service is running.

### `/admin/metrics`

*   **Method:** `GET`
*   **Description:** Returns the collected application metrics.
*   **Request Format:** None.
*   **Response Format:** Text.
```
text
    # HELP sentinel_shield_total_requests Total number of requests.
    # TYPE sentinel_shield_total_requests counter
    sentinel_shield_total_requests 10
    # HELP sentinel_shield_requests_by_status Total requests by status.
    # TYPE sentinel_shield_requests_by_status counter
    sentinel_shield_requests_by_status{status="200"} 5
    sentinel_shield_requests_by_status{status="403"} 5
    # HELP sentinel_shield_average_latency Average latency of the requests.
    # TYPE sentinel_shield_average_latency gauge
    sentinel_shield_average_latency 0.123
    
```
*   **Status Codes:**
    *   `200 OK`: Metrics returned successfully.

### `/risk`

*   **Method:** `GET`
*   **Description:** Checks the risk score of an IP address.
*   **Request Format:**
    *   Query Parameter: `ip` (string) - The IP address to check.
*   **Response Format:** JSON
```
json
    {
        "ip": "192.168.1.1",
        "risk_score": 20,
        "status": "low"
    }
    
```
*   **Response Details:**