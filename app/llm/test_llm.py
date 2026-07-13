from app.llm.llm_factory import LLMFactory


def test():

    prompt = """
You are an AI Travel Assistant.

Suggest the best travel mode from Bangalore to Shimoga.

Return only 5 lines.
"""

    response = LLMFactory.invoke(prompt)

    print()

    print("=" * 60)

    print(response)

    print("=" * 60)


if __name__ == "__main__":

    test()