import time
from typing import Optional
import redis
from app.config import settings

_client: Optional[redis.Redis] = None

def get_client() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(settings.REDIS_URL)
    return _client

def acquire_lock(key: str, ttl: int = 600) -> bool:
    r = get_client()
    # SETNX-like via set(name, value, nx=True, ex=ttl)
    return bool(r.set(key, "1", nx=True, ex=ttl))

def release_lock(key: str):
    try:
        get_client().delete(key)
    except Exception:
        pass
