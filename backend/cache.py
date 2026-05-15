from datetime import datetime, timedelta
from typing import Any, Optional

class InMemoryCache:
    def __init__(self, ttl_seconds: int = 60):
        self._cache = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        value, expires_at = self._cache[key]
        if datetime.utcnow() > expires_at:
            del self._cache[key]
            return None
        return value

    def set(self, key: str, value: Any):
        expires_at = datetime.utcnow() + timedelta(seconds=self._ttl)
        self._cache[key] = (value, expires_at)

    def delete(self, key: str):
        if key in self._cache:
            del self._cache[key]

    def delete_pattern(self, pattern: str):
        keys_to_delete = [k for k in self._cache if pattern in k]
        for key in keys_to_delete:
            del self._cache[key]

cache = InMemoryCache(ttl_seconds=60)