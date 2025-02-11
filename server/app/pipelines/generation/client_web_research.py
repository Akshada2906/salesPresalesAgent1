import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import BaseTool
from dotenv import load_dotenv
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper
from pydantic import Field
from rich import print
from crewai_tools import SerperDevTool

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Useful for searching current information about any topic to create comprehensive outlines."
    search_engine: DuckDuckGoSearchAPIWrapper = Field(default_factory=DuckDuckGoSearchAPIWrapper)
 
    def _run(self, query: str) -> str:
        """Execute the search query and return results"""
        try:
            return self.search_engine.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"

class GoogleSearchTool(BaseTool):
    name: str = "Google Search"
    description: str = "Useful for searching current and accurate information about companies and business topics."
    search_engine: GoogleSearchAPIWrapper = Field(default_factory=GoogleSearchAPIWrapper)

    def _run(self, query: str) -> str:
        """Execute the Google search query and return formatted results"""
        try:
            results = self.search_engine.results(query, num_results=4)
            formatted_results = []
            
            for result in results:
                formatted_results.append(
                    f"Title: {result['title']}\n"
                    f"URL: {result['link']}\n"
                    f"Snippet: {result.get('snippet', 'No snippet available')}\n"
                )
            
            return "\n\n".join(formatted_results)
        except Exception as e:
            return f"Error performing search: {str(e)}"

def agent_search(company_name, prospect_name, prospect_position):
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)


    serper_search_tool = SerperDevTool(n=15)
    duckduckgo_search_tool = WebSearchTool()
    google_search_tool = GoogleSearchTool()


    research_analyst = Agent(
        role="Senior Business Intelligence Analyst",
        goal=f"Conduct comprehensive research on {company_name} and {prospect_name} ({prospect_position})",
        backstory="You are an elite business intelligence analyst with 15 years of experience in corporate research. "
                "You specialize in uncovering valuable business insights that sales teams can leverage. "
                "Your analysis is known for being thorough, accurate, and sales-oriented, with expertise in "
                "understanding different stakeholder perspectives based on their roles.",
        # verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[serper_search_tool, google_search_tool, duckduckgo_search_tool]
    )


    research_task = Task(
        description=f"""Conduct a **comprehensive and detailed** research on {company_name}. 
        Your research should be **thorough and well-structured**, covering all **key aspects** of the company. 

        **Requirements:**
        - Ensure the response is **detailed and extensive** (minimum 1000 words).  
        - Gather insights on **company background, leadership, market position, financials, products, competitors, trends, and challenges**.  
        - If certain data is unavailable, mention potential sources where it can be found.
        - Structure the report **logically**, ensuring it is **easy to read and insightful** for sales or business intelligence teams.  
        - Prioritize **actionable insights** rather than just raw data.  

        **Output Format:**  
        - A **long-form structured report** with sections based on the most relevant findings.
        - Use **clear headings, bullet points, and summaries** to improve readability.
        - The final report should be **comprehensive, informative, and sales-focused**.
        - Add a section on details of {prospect_name} ({prospect_position}) and their role in {company_name}.
        """,
        expected_output="A **detailed, well-structured** company research report (minimum 1000 words) with key insights.",
        agent=research_analyst
    )



    crew = Crew(
        agents=[research_analyst],
        tasks=[research_task],
        # verbose=True,
        process=Process.sequential,
    )

    crew_output = crew.kickoff()
    return crew_output

def main(company_name, prospect_name, prospect_position):
    result = agent_search(company_name, prospect_name, prospect_position)
    
    with open("company_research_report.md", "w") as file:
        file.write(result.raw)

    return result.raw



if __name__ == "__main__":

    print("\n=== Sales Script Generator for Nitor Infotech ===\n")
    company_name = input("Enter the prospect company name: ")
    prospect_name = input("Enter the prospect name: ")
    prospect_position = input("Enter the prospect position: ")
    result = main(company_name, prospect_name, prospect_position)
    print(result)





# import os
# from crewai import Agent, Crew, Process, Task, LLM
# from crewai_tools import SerperDevTool, WebsiteSearchTool
# from rich import print

# from dotenv import load_dotenv
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# def agent_search(company_name):
#    llm = LLM(
#       model="gemini/gemini-2.0-flash-exp",
#       api_key=GEMINI_API_KEY
#    )

#    web_search_tool = SerperDevTool(n=10)
#    # url_search_tool = WebsiteSearchTool(web_url)

#    research_analyst = Agent(
#       role="Senior Business Intelligence Analyst",
#       goal=f"Conduct comprehensive research on {company_name} focusing on sales opportunities and business insights",
#       backstory="You are an elite business intelligence analyst with 15 years of experience in corporate research. "
#                "You specialize in uncovering valuable business insights that sales teams can leverage. "
#                "Your analysis is known for being thorough, accurate, and sales-oriented.",
#       allow_delegation=False,
#       verbose=True,
#       llm=llm,
#       tools=[web_search_tool]
#    )

#    sales_strategist = Agent(
#       role="Enterprise Sales Strategy Consultant",
#       goal=f"Develop targeted sales approaches for {company_name}",
#       backstory="You are a seasoned sales strategy consultant with expertise in enterprise B2B sales. "
#                "You excel at identifying pain points, growth opportunities, and creating strategic questions "
#                "that help establish meaningful business relationships. Your recommendations have helped "
#                "close multiple million-dollar deals.",
#       allow_delegation=False,
#       verbose=True,
#       llm=llm
#    )

#    research_task = Task(
#       description=f"""Conduct detailed research on {company_name} focusing on sales-relevant information. 
#       Provide a comprehensive summary covering:

#       1. Company Overview:
#          - Company size (employee count, revenue if available)
#          - Industry position and market share
#          - Geographic presence and target markets

#       2. Business Intelligence:
#          - Core products/services and their unique value propositions
#          - Primary customer segments and key clients
#          - Main competitors and competitive advantages

#       3. Growth & Challenges:
#          - Recent growth initiatives or expansion plans
#          - Current business challenges or pain points
#          - Digital transformation or innovation projects

#       4. Financial & Market Position:
#          - Recent financial performance or funding rounds
#          - Stock performance (if public)
#          - Major partnerships or acquisitions

#       5. Recent Developments:
#          - Latest product launches or service offerings
#          - Strategic initiatives or organizational changes
#          - Notable press releases or news coverage

#       Organize the information clearly and focus on aspects most relevant to sales opportunities.""",
#       expected_output="A detailed, sales-focused company analysis covering all requested aspects",
#       agent=research_analyst
#    )

#    sales_task = Task(
#       description=f"""Using the comprehensive research on {company_name}, create a sales-ready briefing package:

#       1. EXECUTIVE SUMMARY (2-3 lines)
#          - Highlight the most compelling opportunities for engagement
#          - Identify key decision triggers

#       2. OPPORTUNITY ANALYSIS
#          A. Potential Pain Points
#             - List identified business challenges
#             - Areas where our solutions could add value
         
#          B. Growth Opportunities
#             - Align their initiatives with our capabilities
#             - Identify potential expansion areas
         
#          C. Competitive Position
#             - Their current solution landscape
#             - Our unique value proposition for them

#       3. STAKEHOLDER INSIGHTS
#          - Key decision-makers and their roles
#          - Recent organizational changes
#          - Current priorities and initiatives

#       4. ENGAGEMENT STRATEGY
#          A. Value Proposition Alignment
#             - How our solutions match their needs
#             - Potential ROI areas
         
#          B. Risk Factors
#             - Potential objections
#             - Competition presence
#             - Budget/timing considerations

#       5. STRATEGIC CONVERSATION GUIDE
#          Develop 5 high-impact questions that:
#          - Build on identified pain points
#          - Explore growth opportunities
#          - Demonstrate industry knowledge
#          - Lead to solution discussions
#          - Focus on value creation

#       Format the output in a clear, structured manner that sales teams can quickly digest and use in client conversations.
#       Make it actionable and focused on driving meaningful business discussions.""",
#       expected_output="A comprehensive sales briefing package including strategic analysis and engagement questions",
#       agent=sales_strategist
#    )

#    crew = Crew(
#       agents=[research_analyst, sales_strategist],
#       tasks=[research_task, sales_task],
#       process=Process.sequential,
#       verbose=True
#    )

#    return crew.kickoff(inputs={"company_name": company_name})


# def main(topic):
#    result = agent_search(topic)
#    print(result)


# if __name__ == "__main__":
#    name = input("Enter the company name: ")
#    main(name)




# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from .client_search_agents import agent_search
# from ...core.llm_provider import azure_llm

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# llm = azure_llm

# global_company_details = None
# main_chain = None
# conversational_chain = None
# config = {"configurable": {"session_id": "session_1"}}

# store = {}
# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]

# def create_template():
#     return f'''You are an experienced B2B Sales Intelligence Assistant with extensive knowledge of business analysis and market research.
#         Role & Context:
#         - You have access to verified information about the company: {global_company_details}
#         - Your purpose is to assist sales professionals in understanding and engaging with this company

#         Guidelines:
#         - Provide accurate, factual responses based solely on the provided company information
#         - Focus on business-relevant details that could be valuable for sales interactions
#         - When information is not available in the context, clearly state that rather than making assumptions

#         Areas of Expertise:
#         - Company overview and business model
#         - Products and services
#         - Market presence and positioning
#         - Key business metrics (when available)
#         - Recent developments and company news

#         Remember: Only use information explicitly provided in the context. Maintain professional tone and confidentiality at all times.
#         '''

# def initialize_chains():
#     global main_chain, conversational_chain
#     template = create_template()
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", template), 
#         MessagesPlaceholder(variable_name="chat_history"), 
#         ("human", "{input}")
#     ])
#     main_chain = prompt | llm
#     conversational_chain = RunnableWithMessageHistory(
#         main_chain,
#         get_session_history,
#         input_messages_key="input",
#         history_messages_key="chat_history"
#     )

# def set_company_details(details):
#     global global_company_details
#     global_company_details = details
#     initialize_chains()

# def get_global_company_details():
#     return global_company_details

# def main(query):
#     if not global_company_details:
#         return "Please set company details first"
#     if conversational_chain is None:
#         initialize_chains()
#     response = conversational_chain.invoke({"input": query}, config=config)
#     return response.content

# if __name__ == '__main__':
#     company_name = input('Enter company name: ')
#     speaker_name = input('Enter speaker name: ')
#     speaker_position = input('Enter speaker position: ')
#     company_details = agent_search(company_name, speaker_name, speaker_position)
#     set_company_details(company_details)
#     print(f"\nInitialized with company details: {company_details}\n")
    
#     while True:
#         query = input('\nAsk : ')
#         if query.lower() == 'exit': 
#             break
#         response = main(query)
#         print('\nSystem : ', response)