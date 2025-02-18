import os
from crewai import Agent, Crew, Process, Task, LLM
from dotenv import load_dotenv
from rich import print

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_solution_approach(company_name, project_title, requirements, timeline, amount):
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=GEMINI_API_KEY)

    solution_architect = Agent(
        role="Solution Architect and Technical Strategist",
        goal="Develop a detailed, technical solution approach for the given project, outlining phases, technologies, integration strategies, and risk mitigation plans.",
        backstory="You are a highly experienced Solution Architect with a deep understanding of various technologies and architectures. You excel at translating business requirements into technical solutions, designing scalable and reliable systems, and identifying potential risks. Your expertise includes system integration, cloud technologies, and security best practices. You have a proven track record of creating comprehensive solution approaches that lead to successful project outcomes.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    solution_task = Task(
        description=f"""Given the project details below, create a detailed technical solution approach.

        Company Name: {company_name}
        Project Title: {project_title}
        Project Timeline: {timeline}
        Project Amount: {amount}
        Project Requirements: {requirements}

        Consider the project title, timeline, and requirements to create a comprehensive technical solution approach with distinct phases, technologies, integration strategies, and risk mitigation plans.

        Follow these guidelines:

        1.  **Solution Overview:** Provide a brief overview of the proposed technical solution, including the key technologies and architectural patterns.
        2.  **Phases:** Divide the project into distinct, logical phases. Common phases include Assessment and Planning, Design and Architecture, Development, Testing, Deployment, Integration, Security Hardening, and Monitoring and Support. Infer the required phases based on the project requirements.
        3.  **Technology Stack:** Specify the recommended technology stack for each phase, including programming languages, frameworks, databases, cloud services, and integration tools.
        4.  **Integration Strategy:** Describe the integration strategy for connecting the new system with existing systems and third-party services, including APIs, message queues, and data synchronization techniques.
        5.  **Risk Mitigation:** Identify potential risks and outline mitigation strategies for each phase, including technical risks, security risks, and integration risks.
        6.  **Security Considerations:** Describe the security measures that will be implemented to protect the system from threats and vulnerabilities, including authentication, authorization, encryption, and intrusion detection.
        7.  **Scalability and Performance:** Outline the strategies for ensuring the system is scalable and performs efficiently, including load balancing, caching, and database optimization.
        8.  **Monitoring and Support:** Describe the monitoring and support plan for the deployed system, including performance monitoring, error tracking, and incident response.
        9.  **Format:** Present the solution approach in a detailed and professional paragraph format, as shown in the example.
        10. **Conciseness:** Keep the description concise and focused on the key aspects of the technical solution.

        Example Output:
        **Solution Overview:**
        The proposed technical solution will leverage a microservices architecture, utilizing Python with the Flask framework for API development, PostgreSQL for data storage, and RabbitMQ for asynchronous messaging. Phase 1: Assessment and Planning (2 weeks). Activity: Conduct a thorough assessment of the existing systems and infrastructure. Deliverable: Detailed technical requirements document. Phase 2: Design and Architecture (3 weeks). Activity: Design the microservices architecture and integration strategy. Deliverable: Technical architecture diagram and API specifications. Phase 3: Development (8 weeks). Activity: Develop and test the microservices. Deliverable: Functional microservices with unit tests. Phase 4: Integration (4 weeks). Activity: Integrate the microservices with existing systems. Deliverable: Integrated system with end-to-end functionality. Phase 5: Security Hardening (2 weeks). Activity: Implement security best practices and conduct penetration testing. Deliverable: Secure system with no critical vulnerabilities. Phase 6: Deployment (1 week). Activity: Deploy the system to a production environment. Deliverable: Deployed and operational system. Phase 7: Monitoring and Support (Ongoing). Activity: Monitor system performance and provide ongoing support. Deliverable: Stable and reliable system. Risk mitigation strategies include code reviews, automated testing, and continuous integration. Security will be ensured through encryption, authentication, and authorization mechanisms. Scalability will be achieved through load balancing and database optimization. A comprehensive monitoring and support plan will be implemented to ensure system availability and reliability.

        ---
        Example for E-commerce Platform:
        **Solution Overview:**
        The proposed technical solution will leverage a microservices architecture, utilizing Java with the Spring Boot framework for API development, MySQL for data storage, and Kafka for asynchronous messaging. Phase 1: Requirements Gathering and Analysis (2 weeks). Activity: Gather detailed requirements from stakeholders. Deliverable: Comprehensive requirements document. Phase 2: System Design and Architecture (3 weeks). Activity: Design the microservices architecture and database schema. Deliverable: Technical architecture diagram and data model. Phase 3: Microservices Development (8 weeks). Activity: Develop and test the microservices. Deliverable: Functional microservices with unit tests. Phase 4: Payment Gateway Integration (4 weeks). Activity: Integrate with a secure payment gateway. Deliverable: Secure payment processing functionality. Phase 5: Security Hardening (2 weeks). Activity: Implement security best practices and conduct penetration testing. Deliverable: Secure system with no critical vulnerabilities. Phase 6: Deployment (1 week). Activity: Deploy the system to a cloud environment. Deliverable: Deployed and operational system. Phase 7: Monitoring and Support (Ongoing). Activity: Monitor system performance and provide ongoing support. Deliverable: Stable and reliable system. Risk mitigation strategies include code reviews, automated testing, and continuous integration. Security will be ensured through encryption, authentication, and authorization mechanisms. Scalability will be achieved through load balancing and database optimization. A comprehensive monitoring and support plan will be implemented to ensure system availability and reliability.

        ---
        Example for Mobile App Development:
        **Solution Overview:**
        The proposed technical solution will leverage a native mobile app development approach, utilizing Swift for iOS and Kotlin for Android, with a RESTful API backend built using Node.js and MongoDB. Phase 1: Requirements Gathering and Analysis (2 weeks). Activity: Gather detailed requirements from stakeholders. Deliverable: Comprehensive requirements document. Phase 2: UI/UX Design (3 weeks). Activity: Design the user interface and user experience. Deliverable: UI/UX design prototypes. Phase 3: Mobile App Development (8 weeks). Activity: Develop and test the mobile apps. Deliverable: Functional mobile apps with unit tests. Phase 4: API Development (4 weeks). Activity: Develop the RESTful API backend. Deliverable: Functional API endpoints. Phase 5: Security Hardening (2 weeks). Activity: Implement security best practices and conduct penetration testing. Deliverable: Secure apps and API. Phase 6: Deployment (1 week). Activity: Deploy the apps to app stores. Deliverable: Deployed and operational apps. Phase 7: Monitoring and Support (Ongoing). Activity: Monitor app performance and provide ongoing support. Deliverable: Stable and reliable apps. Risk mitigation strategies include code reviews, automated testing, and continuous integration. Security will be ensured through encryption, authentication, and authorization mechanisms. Scalability will be achieved through cloud infrastructure and database optimization. A comprehensive monitoring and support plan will be implemented to ensure app availability and reliability.
        """,
        expected_output="A detailed technical solution approach with clearly defined phases, technologies, integration strategies, and risk mitigation plans.",
        agent=solution_architect
    )

    crew = Crew(
        agents=[solution_architect],
        tasks=[solution_task],
        verbose=True,
        process=Process.sequential,
    )

    crew_output = crew.kickoff()
    result = str(crew_output.raw)

    with open(f"server/app/pipelines/proposal_generator/data/d_solution_approach.md", "w") as file:
        file.write(result)

    return str(crew_output.raw)


def main(company_name, project_title, requirements, timeline, amount):
    result = generate_solution_approach(company_name, project_title, requirements, timeline, amount)
    
    output_dir = "server/app/pipelines/proposal_generator/data/d_solution_approach"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/solution_approach.md", "w") as file:
        file.write(result)

    return result


if __name__ == "__main__":
    print("\n=== Technical Solution Approach Generator ===\n")

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