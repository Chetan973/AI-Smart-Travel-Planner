from langchain_ollama import ChatOllama

from app.config import settings


class OllamaClient:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:
            cls._client = ChatOllama(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model,
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