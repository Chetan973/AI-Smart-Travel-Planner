from app.enums.travel_mode import TravelMode
from app.providers.provider_factory import ProviderFactory


def test():

    provider = ProviderFactory.get_provider(
        TravelMode.TRAIN
    )

    results = provider.search(
        source="Bangalore",
        destination="Shimoga",
        journey_date="2026-07-15"
    )

    print()

    print("=" * 60)

    for option in results:
        print(option.model_dump())

    print("=" * 60)


if __name__ == "__main__":
    test()