from enum import Enum


class LLMProvider(str, Enum):
    GEMINI = "GEMINI"
    OLLAMA = "OLLAMA"