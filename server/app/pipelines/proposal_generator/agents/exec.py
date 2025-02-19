import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import Field
from rich import print
from pathlib import Path
 
 
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
 
def generate_executive_summary(company_name, project_title, requirements, timeline, amount):
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)
 
    summary_writer = Agent(
        role="Executive Summary Writer",
        goal=f"Craft a compelling, concise, and persuasive executive summary (500-700 words) that immediately grabs the reader's attention and highlights why Nitor Infotech is the ONLY choice to solve {company_name}'s problems with the project '{project_title}'. Emphasize Nitor's value proposition and close with a strong call to action.",
        backstory="You are a top-tier executive summary writer known for your ability to create highly effective summaries that drive sales. You understand that an executive summary is the most important part of a proposal. You distill complex information into a clear, concise, and persuasive narrative that leaves a lasting impression. You are ruthless in highlighting the client's needs, showcasing Nitor Infotech's unique strengths, and emphasizing the financial benefits of the engagement. You are obsessed with emulating the persuasive writing style of successful Nitor Infotech proposals. You ALWAYS close with a clear call to action. Your summaries are designed to win deals.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
 
    summary_task = Task(
        description=f"""Compose an executive summary for a proposal to {company_name}. The project is titled "{project_title}". Timeline is {timeline} months and total amount is {amount} USD.
 
            Company Name: {company_name}
            Project Title: {project_title}
            Project Timeline: {timeline} months
            Project Amount: {amount} USD
            Project Requirements: {requirements}
 
            Your goal is to create a POWERFUL and PERSUASIVE executive summary (500-700 words) that convinces {company_name} that Nitor Infotech is the ONLY solution to their problems.  Follow these guidelines:
 
            1.  **Immediately** grab the reader's attention by stating the key problem implied by the project requirements facing {company_name} and the urgent need for a solution. Infer the problem the customer is facing based on the requirements they have.
            2.  **Concise and Direct:** Avoid generalities and focus on the most critical issues.
            3.  **Showcase Nitor Infotech:** Emphasize Nitor's specific expertise, experience, and unique value proposition that directly addresses {company_name}'s problems.  Don't be shy about highlighting our successes! Tailor the Nitor Infotech's expertise to the requirements the client is looking for.
            4.  **Financial Focus:** Clearly state the project title, timeline and estimated amount, emphasizing the ROI (Return on Investment) for {company_name}. Justify the amount by relating Nitor's expertise to the ROI the client will get
            5.  **Call to Action:** End with a strong and direct call to action, urging the reader to take the next step (e.g., schedule a meeting, sign the contract, etc.).
            6.  **Tone:** Confident, persuasive, and results-oriented.  Project authority and expertise.
            7.  **Do not use '*' in the output**
 
            **Follow the style of the example executive summaries below. These examples are your guide to crafting a winning summary.**
 
            **Executive Summary: {project_title}**
            ---
 
            **Company:** Atlassian
            **Project Title:** Integrated Project Management Platform
            **Timeline:** 6 months
            **Amount:** [Amount to be determined]
            **Requirements:** Integration of existing project management tools, improved workflow automation, enhanced reporting capabilities.
 
            **Executive Summary: Integrated Project Management Platform**
            Effective project execution demands clear instructions, deadlines, and assigned responsibilities. **But to truly scale and dominate, Atlassian needs a project management platform that integrates seamlessly with its existing ecosystem.** Atlassian Corporation (henceforth “Atlassian”) is already building a powerful SaaS platform, but **Ascendion is the ONLY partner that can unlock its full potential.**
            Ascendion, a tech-first organization revolutionizing enterprise software, understands this imperative. With 7000+ employees across 20 global hubs, Ascendion delivers unparalleled technological capabilities that drive real business value for software leaders like Atlassian. We've curated a solution that optimizes efforts, slashes costs, and rapidly scales Atlassian's integration needs through a focused, phased approach.  Our expertise in workflow automation and reporting ensures a solution tailored to Atlassian's needs. **Our proactive approach, combined with our unique Ethical GenAI framework, guarantees not only delivery commitment but also repeatability for future initiatives. Let's schedule a meeting to discuss the details in depth.**
 
            ---
 
            **Company:** Ramsoft
            **Project Title:** FinOps Dashboard Development
            **Timeline:** 3 months
            **Amount:** $36,750
            **Requirements:** Real-time cloud cost tracking, budget monitoring, and customizable reporting.
 
            **Executive Summary: FinOps Dashboard Development**
            The healthcare industry is rapidly embracing cloud services, yet RamSoft is struggling to control the escalating costs and complexity.  **Without real-time insights and optimized spending, RamSoft is leaving money on the table.** This proposal outlines how Nitor Infotech Pvt. Ltd., an Ascendion Company (henceforth “Nitor”), will build custom FinOps dashboards using Power BI, empowering RamSoft with the clarity and control it desperately needs.
            As a Microsoft Gold Partner with 18+ years of data engineering experience and 150+ in-house data experts, Nitor delivers robust, scalable, and future-proof dashboards with confidence. Our expertise in real-time data visualization and custom reporting will allow RamSoft to proactively manage their cloud expenditure. **For a $36,750 investment over 3 months, RamSoft will gain real-time insights, optimized cloud spending, and improved financial governance, unlocking significant long-term benefits and cost savings that off-the-shelf products simply can't match.** Let's schedule a demo, so you can witness how our experts can save more of your finances!.
 
            ---
 
            **Company:** OOISS
            **Project Title:** Web and Mobile Application Development
            **Timeline:** 4 months
            **Amount:** $40,000
            **Requirements:** Develop web and mobile applications for contract management, vendor onboarding, and payment tracking.
 
            **Executive Summary: Web and Mobile Application Development**
            In today's hyper-connected world, OOISS needs to be seamlessly connected with its stakeholders, but outdated systems are holding them back.  **OOISS requires cutting-edge web and mobile applications to achieve true business enablement, and Nitor Infotech is the ONLY partner capable of delivering the results they need.**
            Nitor Infotech ("Nitor") thanks OOISS for the opportunity to submit this proposal. Our web and mobility solutions are specifically designed to capitalize on this opportunity, delivering tailored web and mobile application development services that add value at every stage.  Our expertise in contract management, vendor management, and secure payment gateway integration ensures a comprehensive solution tailored to OOISS' needs. **For an investment of $40,000 over 4 months, Nitor will transform OOISS's operations, providing them with a genuinely competitive edge. This will give the client higher sales and operational effectiveness in the long run. Reach us out, now.**
        """,
        expected_output="A highly persuasive, concise (500-700 words) executive summary that immediately grabs the reader's attention, clearly articulates Nitor Infotech's value proposition as the ONLY solution, and ends with a strong call to action.",
        agent=summary_writer
    )
 
    crew = Crew(
        agents=[summary_writer],
        tasks=[summary_task],
        verbose=True,
        process=Process.sequential,
    )
 
    crew_output = crew.kickoff()
    result = str(crew_output.raw)
 
    # Create the directory path if it doesn't exist
    output_dir = Path("server/app/pipelines/proposal_generator/data")
    output_dir.mkdir(parents=True, exist_ok=True)
 
    # Write the file
    output_file = output_dir / "a_executive_summary.md"
    with open(output_file, "w") as file:
        file.write(result)
 
    return str(crew_output.raw)
 
def main(company_name, project_title, requirements, timeline, amount):
    result = generate_executive_summary(company_name, project_title, requirements, timeline, amount)
   
    output_dir = "server/app/pipelines/proposal_generator/data/a_executive_summary"
    os.makedirs(output_dir, exist_ok=True)
   
    with open(f"{output_dir}/executive_summary.md", "w") as file:
        file.write(result)
 
 
    return result
 
 
if __name__ == "__main__":
    print("\n=== Executive Summary Generator for Nitor Infotech ===\n")
 
 
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