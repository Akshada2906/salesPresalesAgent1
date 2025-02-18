from .agents.exec import generate_executive_summary
from .agents.unst import generate_our_understanding
from .agents.scop import generate_scope_of_work
from .agents.soln import generate_solution_approach
from .agents.n_exp import search_nitor_relevant_experience
from .agents.time_ import generate_timeline_deliverables
from .agents.team import generate_team_structure
from .agents.comm_ import generate_commercials

import json
import litellm
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(5),  # Increased from 3 to 5
    wait=wait_exponential(multiplier=2, min=4, max=30),
    reraise=True
)
def generate_proposal(company_name, project_title, requirements, timeline, amount):
    try:
        litellm.set_verbose = True  # Enable debug logging
        proposal = {
            "proposal": {  # Add this wrapper to match the expected interface
                "executive_summary": {
                    "title": "Executive Summary",
                    "content": generate_executive_summary(company_name, project_title, requirements, timeline, amount),
                    "layout_rank": 1
                },
                "our_understanding": {
                    "title": "Our Understanding",
                    "content": generate_our_understanding(company_name, project_title, requirements, timeline, amount),
                    "layout_rank": 2
                },
                "scope_of_work": {
                    "title": "Scope of Work",
                    "content": generate_scope_of_work(company_name, project_title, requirements, timeline, amount),
                    "layout_rank": 3
                },
                "solution_approach": {
                    "title": "Solution Approach",
                    "content": generate_solution_approach(company_name, project_title, requirements, timeline, amount),
                    "layout_rank": 4
                },
                "nitor_relevant_experience": {
                    "title": "Nitor's Relevant Experience",
                    "content": search_nitor_relevant_experience(requirements),
                    "layout_rank": 5
                },
                "timeline_and_deliverables": {
                    "title": "Project Timeline & Deliverables",
                    "content": generate_timeline_deliverables(company_name, project_title, requirements, timeline, amount),
                    "layout_rank": 6
                },
                "team_structure": {
                    "title": "Team Structure",
                    "content": generate_team_structure(company_name, project_title, requirements, timeline, amount),
                    "layout_rank": 7
                },
                "commercials": {
                    "title": "Commercials",
                    "content": generate_commercials(company_name, project_title, requirements, timeline, amount),
                    "layout_rank": 8
                }
            }
        }
        
        # Fix the file saving part
        output_file = r"server\app\pipelines\proposal_generator\proposal_template_1.json"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(proposal, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save proposal to file: {str(e)}")
            # Continue execution even if file save fails
            pass
            
        return proposal
    except litellm.InternalServerError as e:
        print(f"Model overload error: {str(e)}")
        raise  # Allow retry to handle it
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise


if __name__ == "__main__":
    company_name = "Affin Moneybrokers"
    project_title = "REPO Trading Platform"
    requirements = """
        -Automate Malaysian REPO/Reverse REPO transactions, ensuring GMRA compliance and support for key participants (Affin, interbank, Bursa Malaysia, BNM).
        -Prioritize automated trade execution, real-time compliance monitoring, and efficient collateral management.
        -Integrate seamlessly with market data (e.g., Bloomberg) and existing systems.
        -Ensure robust security, reliability, and scalability to handle increasing volumes and new instruments, complying with all Malaysian regulations.
    """
    timeline = "4 months"
    amount = "25000"

    result = generate_proposal(company_name, project_title, requirements, timeline, amount)

    
    # with open(r"server/app/pipelines/proposal_generator/data/z_proposal.md", "w") as file:
    #     file.write(str(result))
