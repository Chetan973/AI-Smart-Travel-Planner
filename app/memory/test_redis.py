from app.memory.redis_client import redis_client


def test():

    redis_client.set("project", "AI Smart Travel Planner")

    print(redis_client.get("project"))


if __name__ == "__main__":
    test()