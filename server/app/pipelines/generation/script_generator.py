# import json, os
# from crewai import Agent, Crew, Process, Task, LLM
# from pydantic import BaseModel, Field
# from dotenv import load_dotenv
# from rich import print
# from crewai_tools import SerperDevTool
# from typing import List, Dict
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# def agent_search(company_name, speaker_name, speaker_position, status_callback=None):
#     llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)
#     web_search_tool = SerperDevTool(n=10)

#     class SalesScriptOutput(BaseModel):
#         opening_approaches: List[str] = Field(description="2-3 variations of opening approaches")
#         pain_points: List[dict] = Field(description="List of pain points with description and impact")
#         solution_positioning: List[dict] = Field(description="Solutions mapped to pain points")
#         objection_handlers: List[dict] = Field(description="Responses to common objections")
#         value_based_closing: List[str] = Field(description="2-3 closing variations")
#         supporting_elements: dict = Field(description="Statistics, case studies, and ROI calculations")


#     research_analyst = Agent(
#         role="Senior Business Intelligence Analyst",
#         goal=f"Conduct comprehensive research on {company_name} and analyze communication approach for {speaker_position}",
#         backstory="You are an elite business intelligence analyst with 15 years of experience in corporate research. "
#                 "You specialize in uncovering valuable business insights that sales teams can leverage. "
#                 "Your analysis is known for being thorough, accurate, and sales-oriented, with expertise in "
#                 "understanding different stakeholder perspectives based on their roles.",
#         # verbose=True,
#         allow_delegation=False,
#         llm=llm,
#         tools=[web_search_tool]
#     )

#     research_task = Task(
#         description=f"""Conduct detailed research on {company_name} and {speaker_position} role with special focus on PAIN POINTS. 
#         Provide analysis covering:

#         1. Role-Specific Pain Points Analysis:
#             - Key challenges faced by {speaker_position}s in {company_name}'s industry
#             - Specific operational bottlenecks in their department
#             - Resource constraints and efficiency challenges
#             - Compliance and risk management issues
#             - Technology adoption and integration challenges
#             - Team management and scaling difficulties

#         2. Company-Specific Context:
#             - Recent company challenges or setbacks
#             - Public statements about problems or needs
#             - Competitor pressures and market challenges
#             - Technology gaps or outdated systems
#             - Growth-related pain points

#         3. Industry Pain Points:
#             - Current industry-wide challenges
#             - Regulatory pressures
#             - Market dynamics causing stress
#             - Technology disruption impacts

#         4. Decision-Making Context:
#             - Budget constraints and financial pressures
#             - Internal stakeholder challenges
#             - Implementation and adoption hurdles
#             - ROI justification needs

#         Organize findings by priority and impact level.""",
#         expected_output="A detailed pain points analysis with supporting evidence and context",
#         agent=research_analyst,
#         context_callback=lambda msg: status_callback(f"📊 Research Analysis: {msg}", 30) if status_callback else None
#     )

#     sales_strategist = Agent(
#         role="Enterprise Sales Script Consultant",
#         goal=f"Create a cold call sales script for Rohit from Nitor Infotech engaging with {speaker_name}, {speaker_position} at {company_name}",
#         backstory="You are a master sales script writer with deep experience in enterprise B2B sales. "
#                 "You craft personalized cold call scripts that resonate with different organizational roles. "
#                 "Your scripts always include Nitor Infotech's value propositions and are known for "
#                 "being natural, engaging, and highly effective at building rapport.",
#         allow_delegation=False,
#         # verbose=True,
#         llm=llm
#     )

#     sales_task = Task(
#         description=f"""Using the research insights, create a cold call sales script for Rohit from Nitor Infotech engaging with {speaker_name}, {speaker_position} at {company_name}.
            
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
#         agents=[research_analyst, sales_strategist],
#         tasks=[research_task, sales_task],
#         verbose=True,
#         process=Process.sequential,
#     )

#     result = crew.kickoff()
#     if status_callback:
#         status_callback("✅ Generation Complete!", 100)
#     return result

# def main(prospect_name, prospect_position, company_name):
#     result = agent_search(company_name, prospect_name, prospect_position)
    
#     # Format the results as a string instead of printing
#     formatted_output = json.dumps({
#         "opening_approaches": result["opening_approaches"],
#         "pain_points": result["pain_points"],
#         "solution_positioning": result["solution_positioning"],
#         "objection_handlers": result["objection_handlers"],
#         "value_based_closing": result["value_based_closing"],
#         "supporting_elements": result["supporting_elements"]
#     }, indent=2)
    
#     return formatted_output

# if __name__ == "__main__":
#     print("\n=== Sales Script Generator for Nitor Infotech ===\n")
#     prospect_name = input("Enter the prospect's name: ")
#     prospect_position = input("Enter the prospect's position: ")
#     company_name = input("Enter the prospect company name: ")
#     print(main(prospect_name, prospect_position, company_name))



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
 
 
def validate_and_parse_script(raw_script: str) -> dict:
    """Validate and parse the raw script into a structured dict."""
    try:
        cleaned_script = raw_script.replace('```json', '').replace('```', '').strip()
        script_dict = json.loads(cleaned_script)
       
        # Create a dict with just the script content
        if isinstance(script_dict, dict) and 'script' in script_dict:
            return {'script': json.dumps(script_dict['script'], indent=2)}
        return {'script': json.dumps(script_dict, indent=2)}
    except Exception as e:
        raise ValueError(f"Failed to parse script: {str(e)}")
   
 
def web_prospect_research(prospect_name: str, prospect_position: str, company_name: str) -> dict:
    # Lower temperature for more focused responses
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
 