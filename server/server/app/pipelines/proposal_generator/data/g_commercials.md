# Commercials: Affin Moneybrokers REPO Trading Platform

This section details the costs and payment terms associated with developing the REPO Trading Platform for Affin Moneybrokers. We present two approaches, each designed to meet the project requirements while remaining within the allocated budget of $20,000.  Both approaches prioritize a robust, secure, and compliant solution.

## Total Cost of Ownership

The following table compares the estimated costs for two development approaches: a Cloud-Native Approach (Approach 1) and a Hybrid Approach (Approach 2).  Approach 1 leverages fully managed cloud services for scalability and reduced infrastructure management, while Approach 2 uses a combination of cloud and on-premise solutions for greater control and potential cost savings in the long run.

| Component             | Estimated Cost ($) - Approach 1 | Estimated Cost ($) - Approach 2 |
|----------------------|------------------------------------|------------------------------------|
| Infrastructure cost   | $250 /month                       | $150 /month                       |
| Development cost      | $15,000                          | $12,000                          |
| Power BI Licensing    | $0 (No Power BI required)         | $0 (No Power BI required)         |
| Development Time      | 16 Weeks                           | 12 Weeks                           |
| **Total Project Cost** | **$15,400**                        | **$12,180**                        |


## Infrastructure Costs

**Approach 1: Cloud-Native (Azure)**

| Services            | Sub-services         | Description                                                                                                                                                                                    | Approx. Monthly Cost (in USD) |
|---------------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| Azure Services      | App Service Plan     | Hosting the application. Tier selected based on anticipated traffic.                                                                                                                            | $150                          |
|                     | Azure SQL Database   | Managed relational database for storing transactional data.                                                                                                                               | $50                           |
|                     | Azure Cosmos DB      | NoSQL database for handling high-volume, real-time data feeds and potentially market data.                                                                                            | $50                           |
|                     | Azure Key Vault       | Securely stores cryptographic keys and secrets.                                                                                                                                               | $0                            |
|                     | Azure Monitor        | Monitoring and logging service for application health and performance.                                                                                                                      | $0 (included in App Service)|
| Terraform           | HCP Free             | Infrastructure as Code provisioning.                                                                                                                                                       | $0                            |
| **Total infrastructure costs (per month)** |                      |                                                                                                                                                                            | **$250**                       |


**Approach 2: Hybrid (On-Premise & Cloud)**

| Services            | Sub-services         | Description                                                                                                                                                                                    | Approx. Monthly Cost (in USD) |
|---------------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| On-Premise Server   | Server Hosting       |  Existing on-premise server used for some components; costs associated with power and maintenance are assumed covered by existing IT budget.                                                      | $0                            |
| Azure Services      | Azure Blob Storage   | Stores large amounts of market data.                                                                                                                                                          | $50                           |
|                     | Azure Functions      | Serverless compute for specific tasks.                                                                                                                                                      | $50                           |
|                     | Azure Active Directory | Security and user management.                                                                                                                                                           | $0                            |
| Terraform           | HCP Free             | Infrastructure as Code provisioning.                                                                                                                                                       | $0                            |
| **Total infrastructure costs (per month)** |                      |                                                                                                                                                                            | **$100**                       |


## Milestones for Approach 1: Cloud-Native

| Milestone   | Deliverable                                                                                           | Delivery Timeline (In Weeks) | Amount     |
|-------------|-------------------------------------------------------------------------------------------------------|------------------------------|------------|
| Milestone 0 | Project Kickoff, Requirements Gathering & Design                                                       | Week 0                       | $1,000     |
| Milestone 1 | System Architecture Design & Prototyping                                                              | Weeks 1-4                    | $2,000     |
| Milestone 2 | Development of Core Trading Engine & Market Data Integration                                          | Weeks 5-8                    | $4,000     |
| Milestone 3 | Compliance Module Integration & Testing                                                                | Weeks 9-12                   | $4,000     |
| Milestone 4 | Collateral Management Module Integration & Testing                                                      | Weeks 13-16                  | $4,000     |
| **Total Amount** |                                                                                                      |                              | **$15,000** |


## Milestones for Approach 2: Hybrid

| Milestone   | Deliverable                                                                                           | Delivery Timeline (In Weeks) | Amount     |
|-------------|-------------------------------------------------------------------------------------------------------|------------------------------|------------|
| Milestone 0 | Project Kickoff, Requirements Gathering & Design                                                       | Week 0                       | $1,000     |
| Milestone 1 | System Architecture Design & Prototyping                                                              | Weeks 1-3                    | $1,500     |
| Milestone 2 | Development of Core Trading Engine & On-Premise Integration                                          | Weeks 4-7                    | $3,500     |
| Milestone 3 | Compliance Module Integration & Testing                                                                | Weeks 8-10                   | $3,500     |
| Milestone 4 | Collateral Management Module Integration & Testing                                                      | Weeks 11-12                  | $2,500     |
| **Total Amount** |                                                                                                      |                              | **$12,000** |


## License Cost

No specific software licenses (like Power BI) are required for either approach.  The costs are already incorporated into the development and infrastructure costs.


## Payment Terms and Conditions

*   **Currency:** USD
*   **Payment Schedule:** Milestone-based payments as detailed in the Milestone tables above.  50% upfront payment upon signing the contract, followed by 50% upon successful completion and acceptance of each milestone.
*   **Invoice Terms:** Invoices will be issued upon completion of each milestone. Payment is due within 15 days of invoice date.
*   **Interest on Late Payments:** A 1% late payment fee will be applied per month on any outstanding balance.
*   **Right to Halt Work:** We reserve the right to halt work on the project if payment is not received within the stipulated timeframe.