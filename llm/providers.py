import os
import requests
from .base import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL")
        if not self.model:
            raise ValueError("OLLAMA_MODEL environment variable not set")

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = requests.post(
            f"{self.host}/api/generate",
            json={"model": self.model, "prompt": full_prompt, "stream": False}
        )
        return response.json().get("response", "")

class OpenRouterOrOpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        if not self.api_key:
            raise ValueError("LLM_API_KEY environment variable not set")
        self.base_url = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("LLM_MODEL")
        if not self.model:
            raise ValueError("LLM_MODEL environment variable not set")

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json={"model": self.model, "messages": messages}
        )
        
        data = response.json()
        if response.status_code != 200 or "choices" not in data:
            raise ValueError(f"OpenRouter Error ({response.status_code}): {data}")
            
        return data["choices"][0]["message"]["content"]

def get_llm_provider() -> BaseLLMProvider:
    provider_type = os.getenv("LLM_PROVIDER", "ollama").lower()
    if provider_type == "ollama":
        return OllamaProvider()
    elif provider_type in ["openrouter", "openai", "custom"]:
        return OpenRouterOrOpenAIProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider_type}")
