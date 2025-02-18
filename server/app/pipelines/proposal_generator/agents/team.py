import os
from crewai import Agent, Crew, Process, Task, LLM
from dotenv import load_dotenv
from rich import print

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_team_structure(company_name, project_title, requirements, timeline, amount):
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)

    team_structurer = Agent(
        role="Team Structure Architect",
        goal="Design and propose an optimal team structure for a software development project, considering the project requirements, timeline, and budget to ensure efficient resource allocation and successful project execution.",
        backstory="You are a seasoned project manager with 15+ years of experience in leading and structuring development teams for diverse projects. You excel at identifying the necessary skill sets and resource levels to meet project objectives within budget and time constraints. You are adept at matching team roles to project requirements, optimizing team communication, and ensuring efficient collaboration.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    team_task = Task(
        description=f"""Given the project details below, define the optimal team structure for the project.

        Company Name: {company_name}
        Project Title: {project_title}
        Project Timeline: {timeline} months
        Project Requirements: {requirements}

        Consider the project title, timeline, and requirements to determine the appropriate roles and resource levels.

        Follow these guidelines:

        1.  **Roles:** Identify the essential roles needed for the project. Consider roles such as Solutions Architect, [specialized] Engineer (e.g., NLP, Data, Backend, Frontend), QA Engineer, and Project Manager.  Infer the necessity of the role based on the project requirements.
        2.  **Resource Count:** Determine the appropriate number of resources needed for each role. Base this on the project complexity, timeline, and budget.
        3.  **Justification:** Briefly justify the need for each role and the corresponding resource count.
        4.  **Format:** Present the team structure in a clear and professional format, as shown in the example. Ensure it is easily readable and understandable.

        Example Output:

        **Team Structure:**
        The project team will consist of experienced professionals with expertise in [relevant technologies] and software development. The team will be structured as follows:

        Sr. | Role | Resource Count | Justification
        ---|-----------------------|----------------|-----------------------------------------------------------------------
        1  | Solutions Architect    | 1              | Provides overall technical direction and ensures alignment with client needs.
        2  | [Specific] Engineer  | [Number]              | [Reason for the number of engineers]
        ...

        ---
        Example for NLP Project:

        **Team Structure:**
        The project team will consist of experienced professionals with expertise in NLP, database technologies, and software development. The team will be structured as follows:

        Sr. | Role | Resource Count | Justification
        ---|-----------------------|----------------|-----------------------------------------------------------------------
        1  | Solutions Architect    | 1              | Provides overall technical direction and ensures alignment with client needs.
        2  | NLP Engineer           | 2              | Develops and implements the NLP models and algorithms. Two engineers are needed due to the complexity of the NLP tasks.
        3  | Database Engineer      | 1              | Designs and manages the database infrastructure for storing and retrieving data.
        4  | Frontend Developer     | 1              | Develops the user interface for the application.
        5  | Backend Developer      | 2              | Develops the server-side logic and APIs. Two developers are needed to handle the API development for NLP models and implement complex features.
        6  | QA Engineer            | 1              | Ensures the quality and reliability of the application through thorough testing.
        7  | Project Manager        | 1              | Manages the project timeline, budget, and resources.

        ---
        Example for Cloud Migration Project:

        **Team Structure:**
        The project team will consist of experienced professionals with expertise in cloud technologies, data migration, and software development. The team will be structured as follows:

        Sr. | Role | Resource Count | Justification
        ---|-----------------------|----------------|-----------------------------------------------------------------------
        1  | Solutions Architect    | 1              | Provides overall technical direction and ensures alignment with client needs.
        2  | Cloud Engineer         | 2              | Migrates and configures the cloud infrastructure. Two engineers are needed to handle the complexity of the cloud migration.
        3  | Database Engineer      | 1              | Designs and manages the database infrastructure on the cloud.
        4  | Frontend Developer     | 1              | Develops the user interface for the application.
        5  | Backend Developer      | 2              | Develops the server-side logic and APIs. Two developers are needed to handle the API development for migrated data and implement complex features.
        6  | QA Engineer            | 1              | Ensures the quality and reliability of the application through thorough testing.
        7  | Project Manager        | 1              | Manages the project timeline, budget, and resources.

        """,
        expected_output="A well-defined team structure for the project, including roles, resource counts, and justifications.",
        agent=team_structurer
    )

    crew = Crew(
        agents=[team_structurer],
        tasks=[team_task],
        verbose=True,
        process=Process.sequential,
    )

    crew_output = crew.kickoff()
    result = str(crew_output.raw)

    with open(f"server/app/pipelines/proposal_generator/data/f_team_structure.md", "w") as file:
        file.write(result)

    return str(crew_output.raw)


def main(company_name, project_title, requirements, timeline, amount):
    result = generate_team_structure(company_name, project_title, requirements, timeline, amount)

    output_dir = "server/app/pipelines/proposal_generator/data/f_team_structure"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/team_structure.md", "w") as file:
        file.write(result)

    return result


if __name__ == "__main__":
    print("\n=== Team Structure Generator ===\n")

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