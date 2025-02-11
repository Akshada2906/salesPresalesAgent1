from enum import Enum
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


# Get the base directory path
BASE_DIR = Path(__file__).resolve().parent.parent

class LLMProvider(str, Enum):
    AZURE = "azure"
    OPENAI = "openai"
    GEMINI = "gemini"


class BaseLLMConfig(BaseSettings):
    provider: LLMProvider
    openai_api_key: str
    openai_api_version: Optional[str] = None
    azure_deployment: Optional[str] = None 
    openai_api_base: Optional[str] = None
    openai_organization: Optional[str] = None
    model_name: Optional[str] = "gpt-4"
    temperature: float = 0.0
    google_api_key: str

    class Config:
        env_file = BASE_DIR / "configs" / ".env.secret"
        env_file_encoding = "utf-8"

class Config(BaseSettings):
    postgres_uri: str

    class Config:
        env_file = BASE_DIR / "configs" / ".env"
        env_file_encoding = "utf-8"



base_llm_config = BaseLLMConfig()
config = Config()


class AzureLLMConfig(BaseLLMConfig):
    provider: LLMProvider = LLMProvider.AZURE
    openai_api_version: str
    openai_api_base: str
    openai_api_key: str
    azure_deployment: str


class OpenAILLMConfig(BaseLLMConfig):
    provider: LLMProvider = LLMProvider.OPENAI
    openai_api_key: str
    openai_organization: str
    model_name: str

class GeminiLLMConfig(BaseLLMConfig):
    provider: LLMProvider = LLMProvider.OPENAI
    openai_api_key: str
    openai_organization: str
    model_name: str


if __name__ == "__main__":
    print(base_llm_config.model_dump_json())
