from app.graph.state.travel_state import TravelState
from app.memory.redis_manager import RedisManager


class TravelMemory:

    PREFIX = "travel"

    @staticmethod
    def save(
        state: TravelState
    ):

        key = f"{TravelMemory.PREFIX}:{state.session_id}"

        RedisManager.get_client().set(
            key,
            state.model_dump_json(),
            ex=3600
        )

    @staticmethod
    def load(
        session_id: str
    ) -> TravelState | None:

        key = f"{TravelMemory.PREFIX}:{session_id}"

        value = RedisManager.get_client().get(key)

        if value is None:
            return None

        if isinstance(value, bytes):
            value = value.decode()

        return TravelState.model_validate_json(value)