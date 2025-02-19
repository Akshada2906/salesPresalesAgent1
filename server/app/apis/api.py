from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
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
from tenacity import RetryError
from litellm import InternalServerError, APIError
# from ..pipelines.proposal_generator.word_converter import md_to_docx
from ..pipelines.proposal_generator.word_converter import create_docx



# from ..pipelines.generation.market_proposal_generator import conditions_chain
# from ..pipelines.generation.update_proposal import update_proposal

# Add this before creating the FastAPI app
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["CREWAI_TELEMETRY_TIMEOUT"] = "60"  # 60 seconds instead of default 30

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
from ..pipelines.proposal_generator.main_proposal_generator import generate_proposal

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
        result = generate_proposal(
            request.customer, 
            request.title, 
            request.requirements,
            request.completion, 
            request.amount
        )
        return ProposalResponse(proposal=result["proposal"])
        
    except InternalServerError as e:
        raise HTTPException(
            status_code=503,
            detail="AI service temporarily unavailable. Please retry in a few moments."
        )
    except Exception as e:
        print(f"Error generating proposal: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

class ProposalSection(BaseModel):
    title: str
    content: str
    layout_rank: int

class SaveProposalRequest(BaseModel):
    sections: List[ProposalSection]
    title: str

@app.post("/save_proposal")
async def save_proposal(request: SaveProposalRequest):
    try:
        # Get absolute base path
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Create the proposals directory if it doesn't exist
        save_dir = os.path.join(base_dir, "app", "pipelines", "proposal_generator", "proposals")
        os.makedirs(save_dir, exist_ok=True)
        print(f"Save directory: {save_dir}")  # Debug log
        
        # Generate filename for markdown
        md_filename = f"{request.title.lower().replace(' ', '_')}_proposal.md"
        md_filepath = os.path.join(save_dir, md_filename)
        print(f"Markdown filepath: {md_filepath}")  # Debug log
        
        # Convert sections to markdown content and save
        content = ""
        for section in sorted(request.sections, key=lambda x: x.layout_rank):
            content += f"# {section.title}\n\n{section.content}\n\n"
            
        with open(md_filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        # Generate DOCX
        docx_filename = f"{request.title.lower().replace(' ', '_')}_proposal.docx"
        docx_filepath = os.path.join(save_dir, docx_filename)
        
        # Get paths for images
        first_image_1 = os.path.join(base_dir, "app", "pipelines", "proposal_generator", "first_image_1.png")
        first_image_2 = os.path.join(base_dir, "app", "pipelines", "proposal_generator", "first_image_2.png")
        logo_path = os.path.join(base_dir, "app", "pipelines", "proposal_generator", "nitor_logo.png")
        
        print(f"DOCX filepath: {docx_filepath}")  # Debug log
        print(f"Logo path: {logo_path}")  # Debug log
        
        # Verify required files exist
        for path in [logo_path, first_image_1, first_image_2]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Required file not found: {path}")
        
        # Convert markdown to DOCX using updated create_docx function
        create_docx([md_filepath], docx_filepath, logo_path, first_image_1, first_image_2)
        
        # Verify DOCX was created
        if not os.path.exists(docx_filepath):
            raise FileNotFoundError(f"Failed to create DOCX at: {docx_filepath}")
        
        # Return the DOCX file
        return FileResponse(
            docx_filepath,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=docx_filename
        )
            
    except Exception as e:
        import traceback
        error_msg = f"Error in save_proposal: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # Print detailed error for debugging
        raise HTTPException(status_code=500, detail=str(e))


# class ProposalRequest2(BaseModel):
#     customer: str
#     title: str
#     requirements: str
#     completion: str | None = None
#     amount: str | None = None

# class ProposalResponse2(BaseModel):
#     proposal: Dict[str, Any]

# @app.post("/generate_proposal2", response_model=ProposalResponse2, operation_id="generate_proposal2")
# async def handle_proposal2(request: ProposalRequest2):
#     try:
#         result = generate_proposal(
#             request.customer,
#             request.title,
#             request.requirements,
#             request.completion,
#             request.amount
#         )
#         if result is None:
#             raise HTTPException(status_code=400, detail="Failed to generate proposal")
#         return ProposalResponse(proposal=result)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))



@app.get("/health")
async def health_check():
    return {"status": "healthy"}
