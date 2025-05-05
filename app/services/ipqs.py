from typing import Optional, Dict, Any
import httpx
import logging
from ..config.settings import settings

class IPQSService:
    def __init__(self):
        self.api_key = settings.IPQS_API_KEY
        self.base_url = settings.IPQS_BASE_URL
        self.device_base_url = settings.IPQS_DEVICE_BASE_URL
        
    async def check_ip(self, ip_address: str, user_agent: Optional[str] = None) -> Dict[str, Any]:
        """
        Check IP reputation using IPQS API
        """
        params = {
            "user_agent": user_agent or "Unknown",
            "strictness": 1,
            "fast": "1",
            "mobile": "1"
        }        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/{self.api_key}/{ip_address}",
                    params=params
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            return {"error": "HTTP error", "details": str(e)}
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return {"error": "Unexpected error", "details": str(e)}
    
    async def check_device(self, fingerprint: str) -> Dict[str, Any]:
        """
        Check device fingerprint using IPQS API
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.device_base_url}/{self.api_key}/{fingerprint}"
            )
            response.raise_for_status()
            return response.json()
    
    def calculate_risk_level(self, ip_data: Dict[str, Any], device_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Calculate risk level based on IP and device data
        Returns: "high", "medium", or "low"
        """
        risk_score = ip_data.get("fraud_score", 0)
        
        # Increase risk score if device fingerprint shows fraud
        if device_data and device_data.get("fraud_score", 0) > risk_score:
            risk_score = device_data["fraud_score"]
        
        if risk_score >= settings.HIGH_RISK_THRESHOLD:
            return "high"
        elif risk_score >= settings.MEDIUM_RISK_THRESHOLD:
            return "medium"
        return "low"

# Create singleton instance
ipqs_service = IPQSService() 