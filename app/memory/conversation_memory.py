from app.memory.redis_manager import RedisManager


class ConversationMemory:

    @staticmethod
    def save_message(
        session_id: str,
        role: str,
        message: str
    ):

        redis_client = RedisManager.get_client()

        redis_client.rpush(
            f"chat:{session_id}",
            f"{role}:{message}"
        )

    @staticmethod
    def get_messages(
        session_id: str
    ):

        redis_client = RedisManager.get_client()

        return redis_client.lrange(
            f"chat:{session_id}",
            0,
            -1
        )

    @staticmethod
    def clear(
        session_id: str
    ):

        redis_client = RedisManager.get_client()

        redis_client.delete(
            f"chat:{session_id}"
        )