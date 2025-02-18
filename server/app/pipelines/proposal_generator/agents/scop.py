import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import Field
from rich import print

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_scope_of_work(company_name, project_title, requirements, timeline, amount):
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)

    scope_writer = Agent(
        role="Scope of Work Specialist",
        goal="Create a technically sound and client-focused Scope of Work document that accurately reflects Nitor Infotech's capabilities and clearly defines project boundaries to ensure successful project delivery and client satisfaction.",
        backstory="You are a senior engineer at Nitor Infotech with extensive experience in defining project scopes for software development projects. You excel at translating client requirements into technically feasible and well-defined deliverables. You are meticulous in identifying potential risks and dependencies, and you are committed to creating Scope of Work documents that set clear expectations for both Nitor Infotech and the client. You leverage your deep technical knowledge to ensure that the scope is realistic, achievable, and aligned with Nitor's expertise and capabilities.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    scope_task = Task(
        description=f"""Compose a Scope of Work document for a project with {company_name}, titled "{project_title}".  The project timeline is {timeline} months, and the budget is {amount} USD.

        Company Name: {company_name}
        Project Title: {project_title}
        Project Timeline: {timeline} months
        Project Budget: {amount} USD
        Project Requirements: {requirements}

        Based on the provided information and your technical expertise, define the project's Scope of Work, following these guidelines:

        1.  **In Scope:** List the specific tasks, deliverables, and functionalities that Nitor Infotech will *definitely* deliver to address the given requirements, considering the timeline and budget. Focus on realistic and achievable outcomes within the constraints.  Infer the necessary tasks and deliverables from the requirements.
        2.  **Out of Scope:** List the tasks, deliverables, and functionalities that Nitor Infotech will *not* deliver, based on technical limitations, budget constraints, timeline constraints, or perceived unrealistic expectations given the requirements. Be explicit about what is excluded to avoid misunderstandings.  Specifically exclude any data governance, compliance, or post-migration support unless explicitly stated in the requirements.
        3.  **Client Responsibilities:** List the key responsibilities of the client to help for the project be successful. This includes access to systems, data, and people with enough knowledege.
        4.  **Assumptions:** List the key assumptions that Nitor Infotech is making about the project, the client, and the project environment. These assumptions should cover areas such as:
            *   Client providing timely access to systems and data.
            *   Stability and reliability of third-party APIs (if applicable, infer if APIs are required from the 'requirements').
            *   Client's technical expertise and ability to support certain aspects of the project.
            *   Sufficient client resources dedicated to the project.
        5.  **Format:** Follow the standard Scope of Work format:
            *   "1.1 In Scope," "1.2 Out of Scope," "1.3 Client Responsibilities", "1.4 Assumptions"
            *   Use bullet points or numbered lists.
            *   Maintain a professional tone.
            *   Include general sections after the main scope: "Acceptance Criteria" (content can be placeholders - this section need to exist).

        Here are some examples of Scope of Work documents:

        ---

        **Company:** Atlassian
        **Project Title:** Integrated Project Management Platform
        **Timeline:** 6 months
        **Amount:** $150,000
        **Requirements:** Integrate MS Teams, Figma, and Loom into Atlassian's platform; improve workflow automation.

        **Scope of Work:**

        1.1 In Scope
        - Integration of MS Teams, Figma, and Loom systems with the Atlassian platform using REST APIs and SDKs.
        - Development of automated workflows to streamline project management processes.
        - Implementation of user authentication and authorization for integrated systems.
        - Testing and quality assurance of integrated functionalities.

        1.2 Out of Scope
        - Development of new features for MS Teams, Figma, or Loom.
        - Support for unsupported versions of Atlassian, MS Teams, Figma, or Loom.
        - Maintenance of third-party systems.

        1.3 Client Responsibilities
        - Provide timely access to their development environment and API keys.
        - Actively participate in testing and provide feedback.

        1.4 Assumptions
        - MS Teams, Figma, and Loom APIs are stable and reliable.

        2. Acceptance Criteria
        The project will be considered complete upon successful integration of the specified systems, successful UAT by Atlassian, and final sign-off on the delivered system.

        ---

        **Company:** Ramsoft
        **Project Title:** FinOps Dashboard Development
        **Timeline:** 3 months
        **Amount:** $36,750
        **Requirements:** Real-time cloud cost tracking, budget monitoring, customizable reporting.

        **Scope of Work:**

        1.1 In Scope
        - Development of a FinOps dashboard using Power BI to track cloud costs in real-time.
        - Integration with Azure billing APIs to collect cost data.
        - Implementation of budget monitoring and alerting functionalities.
        - Creation of customizable reports for different stakeholders.

        1.2 Out of Scope
        - Integration with cloud providers other than Azure.
        - Advanced data analytics or machine learning features.
        - Development of a mobile app for the dashboard.

        1.3 Client Responsibilities
        - Provide access to Azure billing APIs and necessary credentials.
        - Provide clear requirements for customizable reports.

        1.4 Assumptions
        - Power BI licenses are available for all users.


        2. Acceptance Criteria
        The project will be considered complete upon successful deployment of the FinOps dashboard, accurate cloud cost tracking, and successful UAT by Ramsoft.
        """ ,
        expected_output="A technically sound and client-focused Scope of Work document that accurately reflects Nitor Infotech's capabilities and clearly defines project boundaries.",
        agent=scope_writer
    )

    crew = Crew(
        agents=[scope_writer],
        tasks=[scope_task],
        verbose=True,
        process=Process.sequential,
    )

    crew_output = crew.kickoff()
    result = str(crew_output.raw)

    with open(f"server/app/pipelines/proposal_generator/data/c_scope_of_work.md", "w") as file:
        file.write(result)

    return str(crew_output.raw)

def main(company_name, project_title, requirements, timeline, amount):
    result = generate_scope_of_work(company_name, project_title, requirements, timeline, amount)
    

    output_dir = "server/app/pipelines/proposal_generator/data/c_scope_of_work"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/scope_of_work.md", "w") as file:
        file.write(result)

    return result


if __name__ == "__main__":
    print("\n=== Scope of Work Generator for Nitor Infotech ===\n")

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
    