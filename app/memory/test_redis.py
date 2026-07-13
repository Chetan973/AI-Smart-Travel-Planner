import redis

from app.config import settings


def test_redis():

    client = redis.from_url(settings.redis_url)

    client.set(
        "project",
        "AI Smart Travel Planner"
    )

    value = client.get("project")

    print("=" * 50)
    print("Redis Connected Successfully")
    print("Stored Value :", value.decode())
    print("=" * 50)


if __name__ == "__main__":
    test_redis()