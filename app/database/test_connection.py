from sqlalchemy import text

from app.database import engine


def test_connection():

    try:

        with engine.connect() as connection:

            version = connection.execute(
                text("SELECT version();")
            )

            print("\n✅ Database Connected\n")

            print(version.scalar())

    except Exception as ex:

        print(ex)


if __name__ == "__main__":
    test_connection()