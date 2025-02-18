import os
from crewai import Agent, Crew, Process, Task, LLM
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from rich import print

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_our_understanding(company_name, project_title, requirements, timeline, amount):
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)

    understanding_writer = Agent(
        role="Senior Solutions Architect",
        goal="Create a comprehensive and professional proposal section that demonstrates deep understanding of client needs with minimal input",
        backstory="""You are an expert solutions architect with years of experience in enterprise implementations.
        You excel at extrapolating detailed solutions from high-level requirements and creating compelling proposals.
        You have deep knowledge of industry best practices, common pain points, and solution patterns across various sectors.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    understanding_task = Task(
        description=f"""Create a detailed 'Our Understanding' section for {company_name}'s {project_title} proposal.
        
        Core Information:
        - Company: {company_name}
        - Project: {project_title}
        - Timeline: {timeline} months
        - Budget: ${float(amount):,.2f}
        - Requirements: {requirements}
        
        Based on the requirements and project scope:
        1. Infer the likely industry challenges and pain points
        2. Suggest appropriate technical architecture and solutions
        3. Define a realistic implementation methodology
        4. Identify potential risks and mitigation strategies
        
        Create a comprehensive proposal following this structure:
        **Our Understanding:**
        1. About {company_name}'s Project
           - Inferred current state and challenges
           - Project objectives and success criteria
           - Proposed technical approach

        2. Implementation Methodology
           - Phase 0: Discovery & Assessment
           - Phase 1: Planning & Design
           - Phase 2: Implementation
           - Phase 3: Go-Live & Support

        3. Roles & Responsibilities
           - Create detailed tables for each phase
           - Include both Nitor and client responsibilities

        4. Implementation Challenges & Solutions
           - Anticipate potential challenges based on requirements
           - Provide specific mitigation strategies
           - Consider timeline and budget constraints

        5. Benefits of Partnership with Nitor
           - Quantifiable benefits aligned with requirements
           - Strategic advantages
           - ROI considerations within {timeline} months

        6. Our Implementation Practices
           - Quality assurance approach
           - Risk management framework
           - Communication and reporting structure
           - Support model

        Required Elements:
        - Create tables for roles and challenges
        - Use professional yet accessible language
        - Maintain realistic timelines within {timeline} months
        - Consider ${float(amount):,.2f} budget constraints
        """,
        expected_output="A comprehensive 'Our Understanding' section that appears to be based on deep knowledge despite minimal input",
        agent=understanding_writer
    )

    crew = Crew(
        agents=[understanding_writer],
        tasks=[understanding_task],
        verbose=True,
        process=Process.sequential,
    )

    crew_output = crew.kickoff()
    result = str(crew_output.raw)

    with open(f"server/app/pipelines/proposal_generator/data/b_our_understanding.md", "w") as file:
        file.write(result)

    return str(crew_output.raw)


def main(company_name, project_title, requirements, timeline, amount):
    result = generate_our_understanding(company_name, project_title, requirements, timeline, amount)
    
    output_dir = "server/app/pipelines/proposal_generator/data/b_our_understanding"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/our_understanding.md", "w") as file:
        file.write(result)

    return result

# Example usage
if __name__ == "__main__":
    print("\n=== Our Understanding Generator for Nitor Infotech ===\n")
    
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
    
    result = main(company_name, project_title, requirements, timeline, amount)
    
    print(result)