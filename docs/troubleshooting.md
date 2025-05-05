# Troubleshooting Guide

This guide will help you diagnose and resolve common issues that may occur while running the SentinelShield application.

## Common Issues

### 1. IPQS API Connection Issue

**Symptoms:**

*   Requests are failing to be processed.
*   Errors in the logs indicating problems connecting to the IPQS API or invalid responses.
*   The application may appear to be unresponsive.
* Error : Error calling ipqs api

**Root Cause:**

*   Incorrect IPQS API key.
*   Network connectivity problems between the application and the IPQS servers.
*   IPQS API service is temporarily down or experiencing issues.
*   Rate limiting from IPQS due to too many requests.

**Solution:**

1.  **Verify API Key:** Ensure that the `IPQS_API_KEY` environment variable is set correctly and matches the API key in your IPQS account. Check for any typos or extra spaces.
2.  **Network Connectivity:** Check if the server where the application is running has internet access and can reach `www.ipqualityscore.com`.
3.  **Check IPQS Status:** Visit the IPQS status page (if available) or their documentation to check for any known outages.
4. **Check Rate Limiting**: If you are making too many requests to the API, you might be rate-limited. Check your IPQS dashboard and try to reduce the number of requests to the API.
5.  **Check Logs:** Examine the application logs for detailed error messages related to the IPQS API.
6. **Retry**: If you are having issues connecting to the API, try again later.

### 2. Redis Connection Issue

**Symptoms:**

*   Requests are slow to be processed.
*   The cache is not working (every request is a cache miss).
*   Errors in the logs indicating problems connecting to Redis.
*   The application may crash or be unresponsive.
* Error : Error connecting to Redis

**Root Cause:**

*   Redis server is not running.
*   Incorrect Redis host or port in the configuration.
*   Network connectivity problems between the application and the Redis server.
*   Incorrect Redis password.

**Solution:**

1.  **Verify Redis Server Status:** Ensure that the Redis server is running. Check the Redis server logs for any errors. If you are using docker, check the status of the container `docker ps`.
2.  **Check Configuration:** Verify the `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, and `REDIS_PASSWORD` settings in the `docs/configuration.md` file are correct.
3.  **Network Connectivity:** If Redis is running in a different container or on a different server, make sure there's network connectivity between the application and the Redis instance. Verify that the firewall is not blocking the connections.
4. **Check Password**: Verify that the redis password used is the correct one.
5.  **Check Logs:** Examine the application logs for detailed error messages related to Redis.
6. **Restart Redis**: If you are having issues connecting to Redis, try restarting the Redis server.

### 3. Database Connection Issue

**Symptoms:**

*   Requests are failing to be processed.
*   Errors in the logs indicating problems connecting to the database.
*   The application may crash or be unresponsive.
*   No data is being stored or loaded from the database.

**Root Cause:**

*   Incorrect database URL in the configuration.
*   Database file is corrupted.
*   Lack of permissions to access the database.

**Solution:**

1.  **Verify Database URL:** Ensure that the `DATABASE_URL` setting in the configuration file (`docs/configuration.md`) is correct.
2.  **Check Database file**: If the database file has been corrupted, try to delete it and restart the application.
3.  **Permissions:** If the database is in a separate container or server, make sure the application has the necessary permissions to access it.
4.  **Check Logs:** Examine the application logs for detailed error messages related to the database.

### 4. Wrong Configuration Settings

**Symptoms:**

*   Unexpected application behavior.
*   Errors related to missing or invalid configuration settings.
* The application is not starting.

**Root Cause:**

*   Incorrect values set in the environment variables.
*   Incorrect values set in the configuration file.
*   Missing environment variables.

**Solution:**

1.  **Review Settings:** Carefully review all the configuration settings in the `docs/configuration.md` file.
2.  **Check Environment Variables:** Ensure that all required environment variables are set correctly.
3.  **Restart Application:** After making changes to the configuration, restart the application to apply the new settings.
4.  **Check logs**: If the application is not starting, the logs may contain useful information to determine what the problem is.
5. **Check validation**: Verify that all the values set in the configuration file and environment variables pass the validation.

If you are having troubles with the app, please check the logs and follow this troubleshooting guide. If you are still having problems, please contact the support team.