from langchain_community.chat_models import AzureChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.messages import HumanMessage, SystemMessage

from ..common.config import base_llm_config, LLMProvider, BaseLLMConfig

class AIComponent:

    @staticmethod
    def get_llm(llm_config: BaseLLMConfig):
        if llm_config.provider == LLMProvider.AZURE:
            return AzureChatOpenAI(
                openai_api_version=llm_config.openai_api_version,
                azure_deployment=llm_config.azure_deployment,
                openai_api_key=llm_config.openai_api_key,
                azure_endpoint=llm_config.openai_api_base,
                temperature=llm_config.temperature,
            )
        elif llm_config.provider == LLMProvider.OPENAI:
            return ChatOpenAI(
                openai_api_key=llm_config.openai_api_key,
                openai_organization=llm_config.openai_organization,
                model_name=llm_config.model_name,
                temperature=llm_config.temperature,
            )
        elif llm_config.provider == LLMProvider.GEMINI:
            return ChatGoogleGenerativeAI(
                model=llm_config.model_name,
                temperature=llm_config.temperature,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=llm_config.google_api_key
                # other params...
            )
        else:
            raise ValueError("Unsupported LLM provider")

azure_llm = AIComponent.get_llm(base_llm_config)

if __name__ == "__main__":
    llm = AIComponent.get_llm(base_llm_config)

    messages = [
        SystemMessage(content="You are an intelligent assistant designed to analyze user queries and extract all relevant key entities and concepts."),
        HumanMessage(content="who is the winner of EURO cup 2016 ?")
    ]

    response = llm.invoke(messages)
    print(response.content)