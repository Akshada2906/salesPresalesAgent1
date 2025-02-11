from __future__ import annotations
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from ...core.llm_provider import azure_llm
from .prompts.tech_extractor import system_prompt, user_prompt_template

from typing import List

from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=GEMINI_API_KEY)

class TechDescriptions(BaseModel):
    name: str
    description: str
    usage: str


class TechModel(BaseModel):
    tech_lists: List[TechDescriptions]


tech_extractor_chat_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", str(user_prompt_template))
])

tech_extractor_chain = (
    tech_extractor_chat_template | 
    llm | 
    SimpleJsonOutputParser()
)

if __name__ == "__main__":
    result = tech_extractor_chain.invoke({
        "json_output": TechModel.model_json_schema(),
        "user_query": "We need to build a web application using React and FastAPI, with authentication handled by Azure AD. The app will be deployed on Azure App Service and use Azure SQL Database for data storage."
    })
    print(result)
