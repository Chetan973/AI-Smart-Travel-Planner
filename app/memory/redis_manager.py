import redis

from app.config import settings


class RedisManager:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = redis.from_url(
                settings.redis_url,
                decode_responses=True
            )

        return cls._client