from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any
import json
from ..pipelines.generation.client_web_research import main as client_research_main

# from ..pipelines.generation.script_generator import main as generate_script_main
from ..pipelines.generation.client_person_research import main as generate_script_main

from ..pipelines.generation.sales_chatbot import main as sales_chat_agent_main
from ..pipelines.generation.tech_extractor_generator import tech_extractor_chain, TechModel, TechDescriptions
from ..pipelines.generation.market_proposal_generator_2 import main as market_proposal_generator
import os

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["CREWAI_TELEMETRY_TIMEOUT"] = "60"

app = FastAPI(title="Market Proposal Generator API")



# --- Research Agent ---

class ClientRequest(BaseModel):
    company_name: str
    prospect_name: str | None = None
    prospect_position: str | None = None

class ClientResponse(BaseModel):
    research_report: str

@app.post("/client_research", response_model=ClientResponse)
async def handle_client_research(request: ClientRequest):
    try:
        result = client_research_main(
            request.company_name,
            request.prospect_name,
            request.prospect_position
        )        
        return ClientResponse(research_report=result)
    except Exception as e:
        print(f"Error in handle_client_research: {str(e)}")

        raise HTTPException(status_code=500, detail=str(e))



# --- Script Generator Agent ---

class ScriptRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    prospect_name: str
    prospect_position: str
    company_name: str
 
class ScriptResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')
    script: str
 
@app.post("/generate_script", response_model=ScriptResponse)
async def handle_generate_script(request: ScriptRequest):
    try:
        print(f"Generating scripts for: {request.prospect_name} at {request.company_name}")
       
        result = generate_script_main(
            request.prospect_name,
            request.prospect_position,
            request.company_name
        )
       
        if not result:
            raise HTTPException(status_code=400, detail="Failed to generate script")
       
        # If result is a dictionary, convert it to string
        if isinstance(result, dict):
            if 'script' in result:
                result = result['script']
            result = json.dumps(result)
           
        # Ensure result is a string
        if not isinstance(result, str):
            result = json.dumps(result)
           
        return ScriptResponse(script=result)
       
    except Exception as e:
        print(f"Error generating scripts: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))



# --- Chat Agent ---

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    message: str
    companies_list: List[Dict[str, str]]
    techs: List[TechDescriptions]

@app.post("/chat_assistant", response_model=ChatResponse, operation_id="chat_assistant")
async def handle_chat(request: ChatRequest):
    try:
        answer = sales_chat_agent_main(request.query)
        
        tech_list = tech_extractor_chain.invoke({
            "json_output": TechModel.model_json_schema(),
            "user_query": answer
        })
        
        # Parse the sales chatbot response
        sales_response = json.loads(answer)
        
        return ChatResponse(
            message=sales_response["message"],
            companies_list=sales_response["companies_list"],
            techs=tech_list['tech_lists']
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Proposal Generator ---

class ProposalRequest(BaseModel):
    customer: str
    title: str
    requirements: str
    completion: str | None = None
    amount: float | None = None

class ProposalResponse(BaseModel):
    proposal: Dict[str, Any]

@app.post("/generate_proposal", response_model=ProposalResponse, operation_id="generate_proposal")
async def handle_proposal(request: ProposalRequest):
    try:
        result = market_proposal_generator(
            request.customer, 
            request.title, 
            request.requirements,
            request.completion, 
            request.amount
        )
        if result is None:
            raise HTTPException(status_code=400, detail="Failed to generate proposal")
        return ProposalResponse(proposal=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


# class ProposalRequest(BaseModel):
#     dollar_per_hour: Optional[str] = None
#     estimate_hour: Optional[str] = None
#     requirements: Optional[str] = None
#     scope_of_work: Optional[str] = None
#     tech_to_include: Optional[str] = None
#     terms_and_conditions: Optional[str] = None
#     milestones: Optional[str] = None
#     calendar_dates: Optional[str] = None

# @app.post("/generate_proposal", response_model=ProposalResponse, operation_id="generate_proposal")
# async def handle_proposal(request: ProposalRequest):
#     try:
#         result = conditions_chain.invoke({
#         #
#             "dollar_per_hour": request.dollar_per_hour,
#             "estimate_hour": request.estimate_hour,
#             "requirements": request.requirements,
#             "scope_of_work": request.scope_of_work,
#             "tech_to_include": request.tech_to_include,
#             "terms_and_conditions": request.terms_and_conditions,
#             "milestones": request.milestones,
#             "calendar_dates": request.calendar_dates
#         #
#             # "dollar_per_hour": "$130 per hour",
#             # "estimate_hour": "120 hours",
#             # # "requirements": "Develop a web application integrating with genAI chat assistant for existing company Docs using specified technologies", 
#             # "requirements": request.requirements,
#             # "scope_of_work": "Full-cycle development including design, development, and deployment of a web application",
#             # "tech_to_include": "Include: Azure SQL, ReactJS, Static Web Apps, Entra ID authentication, Azure Functions written in Python; Exclude: Technologies not compatible with Azure environments",
#             # "terms_and_conditions": "50% payment required at project start 50% upon completion; Non-disclosure agreement (NDA) required",
#             # "milestones" : "Initial Design by Jan 2023, Development by Feb-Mar 2023, Testing & Launch by Apr 2023",
#             # "calendar_dates": "Project start: January 2023, Project end: April 2023"
#         })

#         return ProposalResponse(proposal=result)
    
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))



@app.get("/health")
async def health_check():
    return {"status": "healthy"}
