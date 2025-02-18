import os
from crewai import Agent, Crew, Process, Task, LLM
from dotenv import load_dotenv
from rich import print

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_commercials(company_name, project_title, requirements, timeline, amount):
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)

    commercial_expert = Agent(
        role="Commercial Proposal Specialist",
        goal="Develop a comprehensive and professional Commercials section for a project proposal, including detailed cost breakdowns, milestone schedules, licensing information, and clear payment terms, ensuring that the total project cost stays within the specified budget.",
        backstory="You are a highly experienced Commercial Proposal Specialist with a deep understanding of project costing, licensing models, and contract negotiation. You excel at presenting financial information in a clear and compelling manner, while also adhering to strict budgetary constraints. Your goal is to create a Commercials section that is both informative, persuasive, and financially responsible.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    commercials_task = Task(
        description=f"""Create a complete and detailed "Commercials" section for the project proposal. The output *must* be in Markdown format. This is extremely important, make sure you follow the instructions.
        You are required to estimate costs for 2 approaches and it is better to come up with two solution to fit the best solutions.

            **Project Details:**

            *   Company Name: {company_name}
            *   Project Title: {project_title}
            *   Project Requirements: {requirements}
            *   Project Timeline: {timeline}
            *   Project Budget: {amount} USD. **Important:** Ensure the total project costs for both approaches *remain at or below this budget*.  If exceeding the budget is unavoidable, provide a clear explanation and justification.  The goal is to find a solution that delivers maximum value within the budgetary constraints.

            **Instructions:**

            1.  **Commercials:** - Introductory paragraph

            2.  **Total Cost of Ownership:** - A table comparing the estimated costs of two or more approaches (the agent gets to determine the optimal number of approaches), including:

                *   Infrastructure Cost (per month)
                *   Development Cost (one-time)
                *   Power BI Licensing (per user/month) - if applicable
                *   Development Time (in weeks)

                | Component             | Estimated Cost ($) - Approach 1 | Estimated Cost ($) - Approach 2 |
                |----------------------|------------------------------------|------------------------------------|
                | Infrastructure cost   | \$ [Estimate] /month              | \$ [Estimate] /month              |
                | Development cost      | \$ [Estimate]                       | \$ [Estimate]                       |
                | Power BI Licensing    | \$ [Estimate] per user/month       | \$ [Estimate] per user/month       |
                | Development Time      | [Estimate] Weeks                    | [Estimate] Weeks                    |

            3.  **Infrastructure Costs:** - A table detailing the service-wise infrastructure costs for each approach.
                Include:

                * Services
                * Sub-services
                * Description
                * Approx. Monthly Cost (in USD)

                   | Services            | Sub-services         | Description                                                                                                                                                                                    | Approx. Monthly Cost (in USD) |
                   |---------------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
                   | Azure Services      | Data Factory         | -                                                                                                                                                                                                | \$ [Estimate]                 |
                   |                     | Data Lake Storage    | -                                                                                                                                                                                                | \$ [Estimate]                 |
                   |                     | Cost Management APIs | There is no charge for managed Azure spend.                                                                                                                                                    | \$ 0.00                       |
                   |                     | Azure DevOps         | Basic Plan (for additional users): \$6 per user/month. Provides access to Azure Boards, Repos, Pipelines (limited), Test Plans (read-only), Artifacts. Total: \$ [Estimate] /month.          | \$ [Estimate]                |
                   | Terraform           | HCP Free             | UP TO 500 resources per month Get started with all capabilities needed for infrastructure as code provisioning.                                                                             | \$ 0.00                       |
                   | Total infrastructure costs (per month) |                      |                                                                                                                                                                            | \$ [Estimate]                 |

            4.  **Milestones for Approach [Number]:** - A table outlining the project milestones for *each* approach.

                | Milestone   | Deliverable                                                                                           | Delivery Timeline (In Weeks) | Amount   |
                |-------------|-------------------------------------------------------------------------------------------------------|------------------------------|----------|
                | Milestone 0 | Project Kickoff                                                                                       | Week 0                       | \$ [Estimate] |
                | Milestone 1 | [Description]                                                                                         | [Estimate] Weeks             | \$ [Estimate] |
                | Total Amount |                                                                                                       |                              | \$ [Sum to Approach Total] |

                *Ensure that the sum of the milestone amounts matches the total development cost specified in the Total Cost of Ownership table for each approach.*

            5.  **License Cost:** - Details of licensing costs for any relevant software (e.g., Power BI).
                Include different licensing options (e.g., Power BI Desktop, Power BI Pro, Power BI Premium) with costs. Provide descriptions as in the example.

            6.  **Payment Terms and Conditions:** - Clear and concise payment terms and conditions.
                *   Currency: USD
                *   Payment schedule (milestone-based)
                *   Invoice terms (due date, acceptance period)
                *   Interest on late payments
                *   Right to halt work for non-payment

            The output *must* be in Markdown format and the total amount for each approach should stay inside {amount}.
            """,
        expected_output="A complete and detailed Commercials section for the project proposal, in Markdown format, ensuring total project costs remain at or below the specified budget.",
        agent=commercial_expert,
    )

    crew = Crew(
        agents=[commercial_expert],
        tasks=[commercials_task],
        verbose=True,
        process=Process.sequential,
    )

    crew_output = crew.kickoff()
    result = str(crew_output.raw)

    with open(f"server/app/pipelines/proposal_generator/data/g_commercials.md", "w") as file:
        file.write(result)

    return str(crew_output.raw)


def main(company_name, project_title, requirements, timeline, amount):
    result = generate_commercials(company_name, project_title, requirements, timeline, amount)

    output_dir = "server/app/pipelines/proposal_generator/data/g_commercials"
    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/commercials.md", "w") as file:
        file.write(result)

    return result


if __name__ == "__main__":
    print("\n=== Commercials Section Generator ===\n")

    company_name = "Affin Moneybrokers"
    project_title = "REPO Trading Platform"
    requirements = """
        Automate Malaysian REPO/Reverse REPO transactions, ensuring GMRA compliance and support for key participants (Affin, interbank, Bursa Malaysia, BNM).
        Prioritize automated trade execution, real-time compliance monitoring, and efficient collateral management.
        Integrate seamlessly with market data (e.g., Bloomberg) and existing systems.
        Ensure robust security, reliability, and scalability to handle increasing volumes and new instruments, complying with all Malaysian regulations.
    """
    timeline = "4 months"
    amount = "25000"

    result = main(company_name, project_title, requirements, timeline, amount)
    print(result)