import pytest
from unittest.mock import MagicMock
from app.services import cache
from app.config import settings

@pytest.fixture
def mock_redis():
    mock = MagicMock()
    cache.redis_client = mock
    return mock

def test_cache_set_and_get(mock_redis):
    key = "test_key"
    value = "test_value"
    cache.set_value(key, value)
    mock_redis.set.assert_called_once_with(key, value, ex=settings.CACHE_TTL)

    retrieved_value = cache.get_value(key)
    mock_redis.get.assert_called_once_with(key)

    assert retrieved_value == mock_redis.get.return_value

def test_cache_delete(mock_redis):
    key = "test_key"
    cache.delete_value(key)
    mock_redis.delete.assert_called_once_with(key)