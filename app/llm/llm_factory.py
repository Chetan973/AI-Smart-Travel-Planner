# app/llm/llm_factory.py
from app.llm.gemini_client import GeminiClient
from app.llm.ollama_client import OllamaClient

class LLMFactory:
    
    @staticmethod
    def get_client():
        """Exposes the raw LangChain client for structured binding."""
        return GeminiClient.get_client()

    @staticmethod
    def invoke(prompt: str) -> str:
        try:
            print("\nUsing Gemini...\n")
            return GeminiClient.invoke(prompt)
        except Exception as ex:
            print(ex)
            print("\nGemini Failed")
            print("Using Ollama...\n")
            return OllamaClient.invoke(prompt)