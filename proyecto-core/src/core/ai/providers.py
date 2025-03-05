from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, Optional
from openai import OpenAI

class AIProvider(Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    # Futuros proveedores
    # ANTHROPIC = "anthropic"
    # LOCAL_LLAMA = "local_llama"

class BaseAIClient(ABC):
    @abstractmethod
    def analyze_text(self, prompt: str) -> Dict:
        pass

class OpenAIClient(BaseAIClient):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"  # Configurable

    def analyze_text(self, prompt: str) -> Dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a document analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return {"content": response.choices[0].message.content}

class DeepSeekClient(BaseAIClient):
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = "deepseek-chat"

    def analyze_text(self, prompt: str) -> Dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a document analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return {"content": response.choices[0].message.content}
