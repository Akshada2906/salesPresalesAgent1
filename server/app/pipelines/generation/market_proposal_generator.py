# from langchain.prompts import ChatPromptTemplate
# from langchain.schema import StrOutputParser

# # from ...core.llm_provider import azure_llm
# from .prompts.market_proposal import system_prompt, user_prompt_template


# intent_classification_chat_template = ChatPromptTemplate.from_messages(
#     [
#         ('system', system_prompt),
#         ('human', str(user_prompt_template)),
#     ]
# )


# conditions_chain = (
#     intent_classification_chat_template | azure_llm | StrOutputParser()
# )

# if __name__ == "__main__":
#     response = conditions_chain.invoke({
#             "dollar_per_hour": "$130 per hour",
#             "estimate_hour": "120 hours",
#             "requirements": "Develop a web application integrating with genAI chat assistant for existing company Docs using specified technologies", 
#             "scope_of_work": "Full-cycle development including design, development, and deployment of a web application",
#             "tech_to_include": "Include: Azure SQL, ReactJS, Static Web Apps, Entra ID authentication, Azure Functions written in Python; Exclude: Technologies not compatible with Azure environments",
#             "terms_and_conditions": "50% payment required at project start 50% upon completion; Non-disclosure agreement (NDA) required",
#             "milestones" : "Initial Design by Jan 2023, Development by Feb-Mar 2023, Testing & Launch by Apr 2023",
#             "calendar_dates": "Project start: January 2023, Project end: April 2023"
#         })
#     print(response)