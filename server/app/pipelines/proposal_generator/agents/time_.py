import os
from crewai import Agent, Crew, Process, Task, LLM
from dotenv import load_dotenv
from rich import print

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_timeline_deliverables(company_name, project_title, requirements, timeline, amount):
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)

    timeline_architect = Agent(
        role="Project Timeline and Deliverables Architect",
        goal="Create a professional and comprehensive project timeline with clearly defined phases, milestones, deliverables, and resource allocation considerations, ensuring realistic planning and successful project execution.",
        backstory="You are a highly experienced project manager with a proven track record of successfully delivering complex projects on time and within budget. You excel at breaking down projects into manageable phases, identifying critical dependencies, and allocating resources effectively. You are adept at creating realistic timelines and tracking progress to ensure project success.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    timeline_task = Task(
        description=f"""Given the project details below, create a detailed project timeline and deliverables plan.

        Company Name: {company_name}
        Project Title: {project_title}
        Project Timeline: {timeline} months
        Project Requirements: {requirements}

        Consider the project title, timeline, and requirements to create a realistic project schedule with distinct phases, milestones, and deliverables.

        Follow these guidelines:

        1.  **Phases:** Divide the project into distinct, logical phases. Common phases include Requirements Gathering, Design, Development, Testing, Deployment, and Support.  Infer the required phases based on the project requirements.
        2.  **Timeline Allocation:** Allocate an appropriate amount of time (in weeks) to each phase, ensuring the total timeline aligns with the specified {timeline} months.
        3.  **Deliverables:** Define specific and measurable deliverables for each phase.
        4.  **Resource Allocation:** Briefly mention how resources will be allocated based on the project phases, emphasizing key personnel assignments.
        5.  **Dependencies:** Briefly mention how dependencies will be managed and monitored.
        6.  **Format:** Present the timeline and deliverables in a professional paragraph format, as shown in the example.
        7.  **Conciseness:** Keep the description concise and focused on the key aspects of the project timeline and deliverables.

        Example Output:
        **Project Timeline and Deliverables:**
        The project will be divided into distinct phases, with clearly defined milestones and deliverables. Phase 1: Requirements Gathering and Analysis (2 weeks). Deliverable: Comprehensive requirements document. Phase 2: System Design and Architecture (1 week). Deliverable: Technical architecture document. Phase 3: [Specific Activity based on Requirements] (4 weeks). Deliverable: [Deliverable for Specific Activity]. Phase 4: [Specific Activity based on Requirements] (2 weeks). Deliverable: [Deliverable for Specific Activity]. Phase 5: [Specific Activity based on Requirements] (3 weeks). Deliverable: [Deliverable for Specific Activity]. Phase 6: Testing and Quality Assurance (2 weeks). Deliverable: Thoroughly tested and validated system. Phase 7: Deployment and Support (1 week). Deliverable: Deployed and supported system. Resource allocation will be based on the project phases, with key personnel assigned to critical path activities. Dependencies will be carefully managed through regular communication and collaboration. The critical path activities will be closely monitored to ensure timely completion of the project. A detailed Gantt chart illustrating the project timeline and dependencies will be provided separately.

        ---
        Example for AI Chatbot Project:

        **Project Timeline and Deliverables:**
        The project will be divided into distinct phases, with clearly defined milestones and deliverables. Phase 1: Requirements Gathering and Analysis (2 weeks). Deliverable: Comprehensive requirements document. Phase 2: System Design and Architecture (1 week). Deliverable: Technical architecture document. Phase 3: NLP Model Development and Training (4 weeks). Deliverable: Trained NLP model with acceptable accuracy metrics. Phase 4: Database Integration (2 weeks). Deliverable: Integrated system with efficient data access. Phase 5: User Interface Development (3 weeks). Deliverable: Functional user interface. Phase 6: Testing and Quality Assurance (2 weeks). Deliverable: Thoroughly tested and validated system. Phase 7: Deployment and Support (1 week). Deliverable: Deployed and supported system. Resource allocation will be based on the project phases, with key personnel assigned to critical path activities. Dependencies will be carefully managed through regular communication and collaboration. The critical path activities will be closely monitored to ensure timely completion of the project. A detailed Gantt chart illustrating the project timeline and dependencies will be provided separately.

        ---
        Example for Cloud Migration Project:

        **Project Timeline and Deliverables:**
        The project will be divided into distinct phases, with clearly defined milestones and deliverables. Phase 1: Assessment and Planning (2 weeks). Deliverable: Detailed migration plan. Phase 2: Infrastructure Setup (2 weeks). Deliverable: Configured cloud infrastructure. Phase 3: Data Migration (6 weeks). Deliverable: Migrated data to the cloud environment. Phase 4: Application Deployment (4 weeks). Deliverable: Deployed applications in the cloud. Phase 5: Testing and Validation (2 weeks). Deliverable: Validated cloud environment. Phase 6: Optimization and Go-Live (2 weeks). Deliverable: Optimized and live cloud environment. Phase 7: Support and Monitoring (Ongoing). Deliverable: Continuous support and monitoring. Resource allocation will be based on the project phases, with key personnel assigned to critical path activities. Dependencies will be carefully managed through regular communication and collaboration. The critical path activities will be closely monitored to ensure timely completion of the project. A detailed Gantt chart illustrating the project timeline and dependencies will be provided separately.
        """,
        expected_output="A comprehensive project timeline and deliverables plan with clearly defined phases, milestones, and resource allocation considerations.",
        agent=timeline_architect
    )

    crew = Crew(
        agents=[timeline_architect],
        tasks=[timeline_task],
        verbose=True,
        process=Process.sequential,
    )

    crew_output = crew.kickoff()
    result = str(crew_output.raw)

    with open(f"server/app/pipelines/proposal_generator/data/e_timeline_deliverables.md", "w") as file:
        file.write(result)

    return str(crew_output.raw)


def main(company_name, project_title, requirements, timeline, amount):
    result = generate_timeline_deliverables(company_name, project_title, requirements, timeline, amount)
    
    output_dir = "server/app/pipelines/proposal_generator/data/e_timeline_deliverables"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/timeline_deliverables.md", "w") as file:
        file.write(result)

    return result


if __name__ == "__main__":
    print("\n=== Project Timeline and Deliverables Generator ===\n")

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