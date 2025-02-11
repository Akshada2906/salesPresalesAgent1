import os, json
from typing import List, Optional
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import BaseTool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper
from pydantic import BaseModel, Field, ConfigDict
 
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
 
 
class PainPoint(BaseModel):
    id: str = Field(..., pattern=r'^p\d+$')
    description: str = Field(..., min_length=10, max_length=200)
    impact: str = Field(..., min_length=10, max_length=200)
    discovery_questions: List[str] = Field(..., min_items=2, max_items=4)
 
class SolutionPosition(BaseModel):
    pain_point_id: str = Field(..., pattern=r'^p\d+$')
    solution: str = Field(..., min_length=10)
    benefits: List[str] = Field(..., min_items=2, max_items=4)
    success_story: str = Field(..., min_length=20)
 
class ObjectionHandler(BaseModel):
    objection: str
    response: str
    follow_up: str
 
class SalesScript(BaseModel):
    model_config = ConfigDict(extra='forbid')
   
    opening_approaches: List[str] = Field(..., min_items=2, max_items=4)
    pain_points: List[PainPoint] = Field(..., min_items=2, max_items=3)
    solution_positioning: List[SolutionPosition]
    objection_handlers: List[ObjectionHandler] = Field(..., min_items=2, max_items=4)
    value_based_closing: List[str] = Field(..., min_items=1, max_items=3)
 
class GoogleSearchTool(BaseTool):
    name: str = "Google Search"
    description: str = "Useful for searching current and accurate information about companies and business topics."
   
    def _run(self, query: str) -> str:
        try:
            search = GoogleSearchAPIWrapper(
                google_api_key=GOOGLE_API_KEY,
                google_cse_id=GOOGLE_CSE_ID
            )
           
            if query.startswith('{'):
                try:
                    import json
                    query_dict = json.loads(query)
                    query = query_dict.get('query', query)
                except:
                    pass
           
            results = search.results(query, num_results=10)
            formatted_results = []
           
            for result in results:
                formatted_results.append(
                    f"Title: {result['title']}\n"
                    f"URL: {result['link']}\n"
                    f"Snippet: {result.get('snippet', 'No snippet available')}\n"
                )
           
            return "\n\n".join(formatted_results)
        except Exception as e:
            print(f"Detailed error: {str(e)}")
            return f"Error performing search: {str(e)}"
 
class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Search"
    description: str = "Useful for searching current information about any topic to create comprehensive outlines."
    search_engine: DuckDuckGoSearchAPIWrapper = Field(default_factory=DuckDuckGoSearchAPIWrapper)
 
    def _run(self, query: str) -> str:
        try:
            return self.search_engine.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"
 
 
def validate_and_parse_script(raw_script: str) -> str:
    """Validate and parse the raw script into a JSON string."""
    try:
        cleaned_script = raw_script.replace('```json', '').replace('```', '').strip()
        script_dict = json.loads(cleaned_script)
       
        # Return just the JSON string
        if isinstance(script_dict, dict) and 'script' in script_dict:
            return json.dumps(script_dict['script'])
        return json.dumps(script_dict)
    except Exception as e:
        raise ValueError(f"Failed to parse script: {str(e)}")
   
 
def web_prospect_research(prospect_name: str, prospect_position: str, company_name: str) -> dict:
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY, temperature=0.3)
 
    google_search_tool = GoogleSearchTool()
    duckduckgo_search_tool = DuckDuckGoSearchTool()
 
    research_agent = Agent(
        role="Executive Intelligence Analyst",
        goal=f"Research {prospect_name} and {company_name} to identify business needs and challenges.",
        backstory="You are an expert in business research and analysis.",
        verbose=True,
        allow_delegation=False,
        tools=[duckduckgo_search_tool],
        llm=llm,
    )
 
    research_task = Task(
        description=f"""
        Research {prospect_name} ({prospect_position}) and {company_name}, focusing on:
        1. Company overview and recent developments
        2. Technology stack and digital initiatives
        3. Business challenges and opportunities
        4. Prospect's role and responsibilities
       
        Keep the research concise and focused on actionable insights.
        """,
        expected_output="A concise research summary with key insights about the company and prospect.",
        agent=research_agent,
    )
 
    pain_points_agent = Agent(
        role="Business Analyst",
        goal=f"Identify key business challenges for {company_name}",
        backstory="You are an expert in identifying business pain points.",
        verbose=True,
        allow_delegation=False,
        tools=[duckduckgo_search_tool],
        llm=llm,
    )
 
    pain_points_task = Task(
        description=f"""
        Based on the research, identify 2-3 key business challenges that {company_name} faces.
        Focus on challenges that Nitor's services could address:
        - Data and analytics needs
        - Digital transformation requirements
        - Technology modernization needs
        - Quality assurance challenges
       
        Format as a simple list with brief descriptions.
        """,
        expected_output="A list of 2-3 key business challenges.",
        agent=pain_points_agent,
        context=[research_task]
    )
 
    script_writer_agent = Agent(
        role="Sales Script Writer",
        goal=f"Create a sales script for {prospect_name}",
        backstory="You are an expert in creating effective sales scripts.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
 
    script_writer_task = Task(
        description=f"""
        Create a sales script in this JSON format:
        {{
            "script": {{
                "opening_approaches": [
                    "Opening line 1",
                    "Opening line 2",
                    "Opening line 3"
                ],
                "pain_points": [
                    {{
                        "id": "p1",
                        "description": "Brief pain point description",
                        "impact": "Business impact",
                        "discovery_questions": [
                            "Question 1",
                            "Question 2"
                        ]
                    }}
                ],
                "solution_positioning": [
                    {{
                        "pain_point_id": "p1",
                        "solution": "Nitor's solution",
                        "benefits": [
                            "Benefit 1",
                            "Benefit 2"
                        ],
                        "success_story": "Focus on qualitative outcomes without specific numbers"
                    }}
                ],
                "objection_handlers": [
                    {{
                        "objection": "Common objection",
                        "response": "Response",
                        "follow_up": "Follow-up question"
                    }}
                ],
                "value_based_closing": [
                    "Closing statement 1",
                    "Closing statement 2"
                ]
            }}
        }}
 
        IMPORTANT GUIDELINES:
        1. DO NOT use any specific numbers, percentages, or metrics in success stories or benefits
        2. Focus on qualitative outcomes rather than quantitative results
        3. Use phrases like "significant improvement", "substantial reduction", "notable increase" instead of specific percentages
        4. For success stories, focus on the transformation and business impact without specific metrics
        5. Keep all claims verifiable and general
        6. Give atleast 3 responses for each field
 
        Use Nitor's capabilities:
        - Data Engineering & Analytics
        - Application Development
        - AI/ML Solutions
        - Digital Transformation
        - Quality Assurance
 
        Keep responses concise and focused.
        """,
        expected_output="A JSON formatted sales script with no specific metrics or percentages",
        agent=script_writer_agent,
        context=[research_task, pain_points_task],
        output_pydantic=SalesScript
    )
 
    crew = Crew(
        agents=[research_agent, pain_points_agent, script_writer_agent],
        tasks=[research_task, pain_points_task, script_writer_task],
        verbose=True,
        process=Process.sequential,
    )
 
    crew_output = crew.kickoff()
    return validate_and_parse_script(crew_output.raw)
 
def main(prospect_name: str, prospect_position: str, company_name: str) -> dict:
    return web_prospect_research(prospect_name, prospect_position, company_name)
 
 
if __name__ == "__main__":
    script = main('Vivek Sharma', 'Chief Strategy Officer', 'Brandscapes Worldwide')
    print('-----------------------------------------------')
    print(script)

# import os
# import json
# from crewai import Agent, Crew, Process, Task, LLM
# from crewai.tools import BaseTool
# from dotenv import load_dotenv
# from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
# from langchain_google_community import GoogleSearchAPIWrapper
# from pydantic import Field

# from rich import print
# from crewai_tools import SerperDevTool
# from typing import List
# from pydantic import BaseModel



# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# class DuckDuckGoSearchTool(BaseTool):
#     name: str = "Web Search"
#     description: str = "Useful for searching current information about any topic to create comprehensive outlines."
#     search_engine: DuckDuckGoSearchAPIWrapper = Field(default_factory=DuckDuckGoSearchAPIWrapper)
 
#     def _run(self, query: str) -> str:
#         """Execute the search query and return results"""
#         try:
#             return self.search_engine.run(query)
#         except Exception as e:
#             return f"Error performing search: {str(e)}"

# class GoogleSearchTool(BaseTool):
#     name: str = "Google Search"
#     description: str = "Useful for searching current and accurate information about companies and business topics."
#     search_engine: GoogleSearchAPIWrapper = Field(default_factory=GoogleSearchAPIWrapper)

#     def _run(self, query: str) -> str:
#         """Execute the Google search query and return formatted results"""
#         try:
#             results = self.search_engine.results(query, num_results=4)
#             formatted_results = []
            
#             for result in results:
#                 formatted_results.append(
#                     f"Title: {result['title']}\n"
#                     f"URL: {result['link']}\n"
#                     f"Snippet: {result.get('snippet', 'No snippet available')}\n"
#                 )
            
#             return "\n\n".join(formatted_results)
#         except Exception as e:
#             return f"Error performing search: {str(e)}"

# class SalesScriptOutput(BaseModel):
#         opening_approaches: List[str] = Field(description="2-3 variations of opening approaches")
#         pain_points: List[dict] = Field(description="List of pain points with description and impact")
#         solution_positioning: List[dict] = Field(description="Solutions mapped to pain points")
#         objection_handlers: List[dict] = Field(description="Responses to common objections")
#         value_based_closing: List[str] = Field(description="2-3 closing variations")
#         supporting_elements: dict = Field(description="Statistics, case studies, and ROI calculations")

# def agent_search(company_name):
#     llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)


#     serper_search_tool = SerperDevTool(n=10)
#     duckduckgo_search_tool = DuckDuckGoSearchTool()
#     google_search_tool = GoogleSearchTool()



#     research_analyst = Agent(
#         role="Senior Business Intelligence Analyst",
#         goal=f"Conduct comprehensive research on {company_name}",
#         backstory="You are an elite business intelligence analyst with 15 years of experience in corporate research. "
#                 "You specialize in uncovering valuable business insights that sales teams can leverage. "
#                 "Your analysis is known for being thorough, accurate, and sales-oriented, with expertise in "
#                 "understanding different stakeholder perspectives based on their roles.",
#         # verbose=True,
#         allow_delegation=False,
#         llm=llm,
#         tools=[serper_search_tool, google_search_tool, duckduckgo_search_tool]
#     )


#     research_task = Task(
#         description=f"""Conduct a **comprehensive and detailed** research on {company_name}. 
#         Your research should be **thorough and well-structured**, covering all **key aspects** of the company. 

#         **Requirements:**
#         - Ensure the response is **detailed and extensive** (minimum 1000 words).  
#         - Gather insights on **company background, leadership, market position, financials, products, competitors, trends, and challenges**.  
#         - If certain data is unavailable, mention potential sources where it can be found.
#         - Structure the report **logically**, ensuring it is **easy to read and insightful** for sales or business intelligence teams.  
#         - Prioritize **actionable insights** rather than just raw data.  

#         **Output Format:**  
#         - A **long-form structured report** with sections based on the most relevant findings.
#         - Use **clear headings, bullet points, and summaries** to improve readability.
#         - The final report should be **comprehensive, informative, and sales-focused**.
#         """,
#         expected_output="A **detailed, well-structured** company research report (minimum 1000 words) with key insights.",
#         agent=research_analyst
#     )

#     crew = Crew(
#         agents=[research_analyst],
#         tasks=[research_task],
#         # verbose=True,
#         process=Process.sequential,
#     )

#     crew_output = crew.kickoff()
#     return crew_output

# def person_research(prospect_name, prospect_position, company_name, status_callback=None):
#     llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)

#     serper_search_tool = SerperDevTool(n=10)
#     duckduckgo_search_tool = DuckDuckGoSearchTool()
#     google_search_tool = GoogleSearchTool()
    

#     person_analyst = Agent(
#         role="Executive Research Specialist",
#         goal=f"Research and profile {prospect_name} ({prospect_position} at {company_name})",
#         backstory="""You are an expert in executive profiling and relationship intelligence with 10 years of experience. 
#                 You excel at gathering and analyzing information about business leaders to support meaningful sales conversations. 
#                 Your insights help sales teams build rapport and understand stakeholder perspectives.""",
#         allow_delegation=False,
#         llm=llm,
#         tools=[serper_search_tool, google_search_tool, duckduckgo_search_tool]
#     )


#     research_task = Task(
#         description=f"""Conduct detailed research on {prospect_name}, who is {prospect_position} at {company_name}.
        
#         **Research Requirements:**
#         1. Professional Background:
#            - Career history and progression
#            - Educational background
#            - Notable achievements and recognition
           
#         2. Current Role & Responsibilities:
#            - Key responsibilities in current position
#            - Time in current role
#            - Notable initiatives or projects led
           
#         3. Professional Insights:
#            - Leadership style and priorities
#            - Published articles, interviews, or speeches
#            - Industry involvement (speaking engagements, board positions)
           
#         4. Digital Presence:
#            - LinkedIn and other professional social media presence
#            - Recent professional activities or posts
#            - Engagement with industry trends/topics
           
#         5. Conversation Starters:
#            - Shared connections or interests
#            - Recent professional achievements
#            - Areas of expertise or passion projects
           
#         6. Sales Engagement Insights:
#            - Likely priorities and pain points based on role
#            - Potential areas of interest for your solution
#            - Communication preferences (if available)

#         Format the output as a clear, structured report focused on helping sales teams prepare for meaningful engagement.
#         Include specific conversation starters and engagement recommendations.""",
#         expected_output="A comprehensive executive profile with actionable insights for sales engagement",
#         agent=person_analyst
#     )

#     sales_strategist = Agent(
#         role="Enterprise Sales Script Consultant",
#         goal=f"Create a cold call sales script for Rohit from Nitor Infotech engaging with {prospect_name}, {prospect_position} at {company_name}",
#         backstory="You are a master sales script writer with deep experience in enterprise B2B sales. "
#                 "You craft personalized cold call scripts that resonate with different organizational roles. "
#                 "Your scripts always include Nitor Infotech's value propositions and are known for "
#                 "being natural, engaging, and highly effective at building rapport.",
#         allow_delegation=False,
#         # verbose=True,
#         llm=llm
#     )

#     sales_task = Task(
#         description=f"""Using the research insights, create a cold call sales script for Rohit from Nitor Infotech engaging with {prospect_name}, {prospect_position} at {company_name}.
            
#             CRITICAL INSTRUCTION FOR OPENING APPROACHES:
#             You MUST replace ALL placeholder suggestions with ACTUAL, SPECIFIC information from your research about {company_name}.
#             Do not add any imaginary numbers or numerical data like 15%, .
            
#             INCORRECT EXAMPLE (DO NOT DO THIS):
#             "Hi [Name], I noticed your company's [recent achievement] and wanted to discuss..."
            
#             CORRECT EXAMPLE:
#             "Hi John, I noticed your company's recent $50M Series C funding round led by Sequoia Capital and wanted to discuss..."
            
#             Each opening approach MUST include actual, researched details about:
#             - Specific company achievements (exact numbers, dates, names)
#             - Real market challenges they're currently facing
#             - Concrete industry trends affecting their business
#             - Actual details about their digital transformation initiatives
#             - Recent news or announcements with precise details
            
#             When crafting solution_positioning, specifically reference Nitor's proven capabilities from these actual case studies:
#             - Data Engineering & Analytics: ETL processes, data warehousing, BI platforms, real-time analytics
#             - Application Development: Web apps, mobile apps (iOS/Android/Windows), cloud-native solutions
#             - AI/ML Solutions: Machine learning models, forecasting, optimization algorithms
#             - Digital Transformation: Legacy modernization, cloud migration, process automation
#             - Quality Assurance: Automated testing, regression testing, performance testing
            
#             Reference actual case studies like:
#             - Built analytics platforms using technologies like PowerBI, AWS, Azure
#             - Developed AI/ML solutions for forecasting and optimization
#             - Created mobile/web applications using modern frameworks (Angular, React, Flutter)
#             - Implemented data engineering solutions with tools like Hadoop, Spark, AWS/Azure services
#             - Modernized legacy applications with latest technologies and frameworks

#             Your response MUST be in the following JSON format:
#             {{{{
#                 "opening_approaches": [
#                     "Complete opening script with actual company details - NO PLACEHOLDERS",
#                     "Complete opening script with actual company details - NO PLACEHOLDERS",
#                     "Complete opening script with actual company details - NO PLACEHOLDERS"
#                 ],
#                 "pain_points": [
#                     {{{{
#                         "id": "p1",
#                         "description": "pain point description",
#                         "impact": "business impact",
#                         "discovery_questions": ["question1", "question2"]
#                     }}}}
#                 ],
#                 "solution_positioning": [
#                     {{{{
#                         "pain_point_id": "p1",
#                         "solution": "solution description with specific Nitor case study reference",
#                         "benefits": ["benefit1", "benefit2"],
#                         "success_story": "brief success story from Nitor's actual experience"
#                     }}}}
#                 ],
#                 "objection_handlers": [
#                     {{{{
#                         "objection": "specific objection",
#                         "response": "handling response",
#                         "follow_up": "follow up question or statement"
#                     }}}}
#                 ],
#                 "value_based_closing": [
#                     "closing1",
#                     "closing2"
#                 ],
#                 "supporting_elements": {{{{
#                     "statistics": ["stat1", "stat2"],
#                     "roi_calculations": ["roi1", "roi2"]
#                 }}}}
#             }}}}
            
#             FINAL CHECKS:
#             1. Have you removed ALL placeholder text like [mention X] or [specific Y]?
#             2. Have you included ACTUAL, RESEARCHED details about {company_name}?
#             3. Is every opening approach COMPLETE and READY TO USE without any modifications?
            
#             DO NOT use ANY placeholder text, brackets, or suggestions for insertion. Every detail must be specific and complete based on your research.""",

#         expected_output="A JSON formatted sales script with structured components",
#         agent=sales_strategist,
#         output_pydantic=SalesScriptOutput,
#         context_callback=lambda msg: status_callback(f"📝 Script Generation: {msg}", 70) if status_callback else None
#     )

#     crew = Crew(
#         agents=[person_analyst, sales_strategist],
#         tasks=[research_task, sales_task],
#         process=Process.sequential,
#     )


#     crew_output = crew.kickoff()
#     return crew_output

# def main(prospect_name, prospect_position, company_name):
#     if all([company_name, prospect_name, prospect_position]):
#         company_result = agent_search(company_name)
#         person_result = person_research(prospect_name, prospect_position, company_name)

#         formatted_output = json.dumps({
#             "opening_approaches": person_result["opening_approaches"],
#             "pain_points": person_result["pain_points"],
#             "solution_positioning": person_result["solution_positioning"],
#             "objection_handlers": person_result["objection_handlers"],
#             "value_based_closing": person_result["value_based_closing"],
#             "supporting_elements": person_result["supporting_elements"]
#         }, indent=2)
        
#         return formatted_output
        

#         # Save both reports
#         with open("company_research_report.md", "w") as file:
#             file.write(company_result.raw)
        
#         with open("person_research_report.md", "w") as file:
#             file.write(person_result.raw)
            
#         return {
#             "company_research": company_result.raw,
#             "person_research": person_result.raw,
#             "sales_script": sales_result.raw
#         }
#     else:
#         # Fallback to just company research

#         result = agent_search(company_name)
        
#         with open("company_research_report.md", "w") as file:
#             file.write(result.raw)
            
#         return {"company_research": result.raw}

# if __name__ == "__main__":
#     print("\n=== Sales Intelligence Research Tool ===\n")
#     prospect_name = input("Enter the Prospect's name: ")
#     prospect_position = input("Enter Prospect's position: ") if prospect_name else None
#     company_name = input("Enter the Prospect company name: ")
    
#     results = main(prospect_name, prospect_position, company_name)
    
#     if "person_research" in results:
#         print("\n=== Person Research Results ===\n")
#         print(results["person_research"])
        
#     print("\n=== Company Research Results ===\n")
#     print(results["company_research"])




# import os
# from dotenv import load_dotenv
# from crewai import Agent, Crew, Process, Task, LLM
# from crewai.tools import BaseTool
# from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
# from langchain_google_community import GoogleSearchAPIWrapper
# from pydantic import Field
 
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
 
 
# class GoogleSearchTool(BaseTool):
#     name: str = "Google Search"
#     description: str = "Useful for searching current and accurate information about companies and business topics."
   
#     def _run(self, query: str) -> str:
#         try:
#             search = GoogleSearchAPIWrapper(
#                 google_api_key=GOOGLE_API_KEY,
#                 google_cse_id=GOOGLE_CSE_ID
#             )
           
#             if query.startswith('{'):
#                 try:
#                     import json
#                     query_dict = json.loads(query)
#                     query = query_dict.get('query', query)
#                 except:
#                     pass
           
#             results = search.results(query, num_results=10)
#             formatted_results = []
           
#             for result in results:
#                 formatted_results.append(
#                     f"Title: {result['title']}\n"
#                     f"URL: {result['link']}\n"
#                     f"Snippet: {result.get('snippet', 'No snippet available')}\n"
#                 )
           
#             return "\n\n".join(formatted_results)
#         except Exception as e:
#             print(f"Detailed error: {str(e)}")
#             return f"Error performing search: {str(e)}"
 
# class DuckDuckGoSearchTool(BaseTool):
#     name: str = "DuckDuckGo Search"
#     description: str = "Useful for searching current information about any topic to create comprehensive outlines."
#     search_engine: DuckDuckGoSearchAPIWrapper = Field(default_factory=DuckDuckGoSearchAPIWrapper)
 
#     def _run(self, query: str) -> str:
#         try:
#             return self.search_engine.run(query)
#         except Exception as e:
#             return f"Error performing search: {str(e)}"
 
 
# def web_company_research(company_name, prospect_name, prospect_position):
#     llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY, temperature=0.2)
 
#     google_search_tool = GoogleSearchTool()
#     duckduckgo_search_tool = DuckDuckGoSearchTool()
 
#     research_agent = Agent(
#         role='Senior Market Intelligence Analyst',
#         goal=f"Perform an **in-depth business research** on {company_name}.",
#         backstory=(
#             "You are an expert in corporate strategy, financial research, and competitive intelligence. "
#             "Your insights help sales teams identify opportunities and tailor their pitches. "
#             "You analyze available data, infer missing details, and provide actionable insights."
#         ),
#         verbose=True,
#         allow_delegation=True,
#         tools=[google_search_tool, duckduckgo_search_tool],
#         llm=llm,
#     )
 
#     research_task = Task(
#         description=f"""
#         Conduct **deep research** on {company_name}, analyzing all available data and inferring missing details.
 
#         **1. Company Overview**  
#         - Industry, headquarters, size, and global presence.  
#         - Mission, vision, strategic priorities.  
 
#         **2. Leadership & Key Stakeholders**  
#         - CEO, CFO, CTO, and other executives.  
#         - **Recent activities:** LinkedIn posts, interviews, statements.  
#         - **Buying signals:** Are they discussing AI, digital transformation, or cost-cutting?  
 
#         **3. Financial Health (Infer If No Data Available)**  
#         - Revenue, funding rounds, and growth signals.  
#         - If direct financials are unavailable, **analyze hiring trends, investments, and business expansion** as a proxy.  
 
#         **4. Technology & Digital Strategy**  
#         - Identify tech stack using website analysis, job postings, and external reports.  
#         - Look for AI, cloud, CRM, ERP, data analytics usage.  
#         - **If tech stack isn't listed, infer based on industry trends.**  
 
#         **5. Competitor Analysis**  
#         - Identify top 3-5 competitors.  
#         - **Key differentiators:** Pricing, services, customer base.  
#         - Compare Brandscapes' strengths vs. competitors' weaknesses.  
 
#         **6. Hiring Trends & Expansion Plans**  
#         - What roles are they hiring for? (AI, sales, engineering?)  
#         - Indications of new offices or global expansion.  
#         - Use job postings and LinkedIn insights.  
 
#         **7. Market Trends & Industry Challenges**  
#         - What disruptions are happening in their industry?  
#         - Regulatory risks or major changes affecting them?  
#         - How they are adapting to competition?  
 
#         **8. Personalized Insights for {prospect_name} ({prospect_position})**  
#         - **Role-specific insights:** What are they responsible for?  
#         - **Recent activities:** LinkedIn posts, interviews, past career history.  
#         - How to position your solutions based on their priorities.  
 
#         **9. "Why Now?" - Sales Timing Insights**  
#         - **Trigger events:** Recent funding, leadership changes, product launches.  
#         - **Pain points:** Financial stress, hiring shifts, market slowdowns.  
#         - **Competitive pressure:** Are rivals launching something new?  
 
#         **Expected Output:**  
#         - A **detailed research report** (minimum **1200 words**).  
#         - **Actionable sales insights** (not just raw data).  
#         - **Bullet points, executive summary, competitor benchmarks.**  
#         - If data is missing, **infer insights instead of stating "Not Available".**  
#         """,
#         expected_output="A well-structured, sales-focused research report covering all key areas with inferred insights when direct data is unavailable.",
#         agent=research_agent,
#     )
 
#     crew = Crew(
#         agents=[research_agent],
#         tasks=[research_task],
#         verbose=True,
#         process=Process.sequential,
#     )
 
#     crew_output = crew.kickoff()
   
#     return str(crew_output.raw)
 
# def main(company_name, prospect_name, prospect_position):
#     research_report = web_company_research(company_name, prospect_name, prospect_position)
#     return research_report
 
 
# if __name__ == "__main__":
#     result = main('Brandscapes Worldwide', 'Vivek Sharma', 'Chief Strategy Officer')
#     print(result)
