# app/memory/redis_manager.py
import redis
from app.config import settings

class RedisManager:
    _pool = None

    @classmethod
    def get_conn_pool(cls):
        if cls._pool is None:
            cls._pool = redis.ConnectionPool.from_url(
                settings.redis_url, 
                decode_responses=False # LangGraph checkpointers require raw byte transfer
            )
        return cls._pool

    @classmethod
    def get_client(cls) -> redis.Redis:
        return redis.Redis(connection_pool=cls.get_conn_pool())