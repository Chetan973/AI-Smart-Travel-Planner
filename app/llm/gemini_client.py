from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings


class GeminiClient:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = ChatGoogleGenerativeAI(

                model="gemini-2.5-flash",

                google_api_key=settings.google_api_key,

                temperature=0.3

            )

        return cls._client

    @classmethod
    def invoke(
        cls,
        prompt: str
    ) -> str:

        llm = cls.get_client()

        response = llm.invoke(prompt)

        return response.content