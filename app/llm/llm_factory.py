from app.llm.gemini_client import GeminiClient
from app.llm.ollama_client import OllamaClient


class LLMFactory:

    @staticmethod
    def invoke(
        prompt: str
    ) -> str:

        try:

            print("\nUsing Gemini...\n")

            return GeminiClient.invoke(prompt)

        except Exception as ex:

            print(ex)

            print("\nGemini Failed")

            print("Using Ollama...\n")

            return OllamaClient.invoke(prompt)