import pytest
from unittest.mock import patch
from app.services.ipqs import IPQSClient

def test_get_ip_reputation_valid_score():
    with patch('app.services.ipqs.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True, 'fraud_score': 50}

        client = IPQSClient(api_key="test_api_key")
        risk_score = client.get_ip_reputation("127.0.0.1")

        assert 0 <= risk_score <= 100

def test_get_ip_reputation_invalid_score_below_0():
    with patch('app.services.ipqs.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True, 'fraud_score': -10}
        
        client = IPQSClient(api_key="test_api_key")
        risk_score = client.get_ip_reputation("127.0.0.1")
        
        assert 0 <= risk_score <= 100

def test_get_ip_reputation_invalid_score_above_100():
    with patch('app.services.ipqs.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True, 'fraud_score': 110}
        
        client = IPQSClient(api_key="test_api_key")
        risk_score = client.get_ip_reputation("127.0.0.1")
        
        assert 0 <= risk_score <= 100