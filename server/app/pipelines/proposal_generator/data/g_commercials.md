# Commercials: REPO Trading Platform for Affin Moneybrokers

This section details the costs and payment terms associated with developing the REPO trading platform for Affin Moneybrokers. We propose two approaches, each optimized for different priorities: Approach 1 prioritizes speed of development, while Approach 2 prioritizes long-term cost-effectiveness. Both approaches remain within the allocated budget of $25,000.


## Total Cost of Ownership

| Component             | Estimated Cost ($) - Approach 1 | Estimated Cost ($) - Approach 2 |
|----------------------|------------------------------------|------------------------------------|
| Infrastructure cost   | $200 /month                     | $150 /month                     |
| Development cost      | $18,000                           | $19,000                           |
| Power BI Licensing    | $0                                 | $0                                 |
| Development Time      | 10 Weeks                          | 12 Weeks                          |
| **Total Project Cost** | **$18,400**                       | **$19,300**                       |


## Infrastructure Costs

**Approach 1:**

| Services            | Sub-services         | Description                                                                                                                                                                                    | Approx. Monthly Cost (in USD) |
|---------------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| Azure Services      | App Service Plan     | Basic plan sufficient for initial deployment and testing. Scalable as needed.                                                                                                              | $50                          |
|                     | SQL Database         | Basic tier sufficient for initial data storage. Scalable as needed.                                                                                                                       | $50                          |
|                     | Azure DevOps         | Basic plan for version control, CI/CD.                                                                                                                                               | $100                         |
| Third-Party APIs    | Market Data (Bloomberg)|  Subscription costs will be determined based on Affin's existing Bloomberg contract and specific data requirements.                                                                | $0 (included in existing contract)                 |
| **Total infrastructure costs (per month)** |                      |                                                                                                                                                                            | **$200**                         |

**Approach 2:** (Emphasizes cost optimization. Uses less resource intensive services)

| Services            | Sub-services         | Description                                                                                                                                                                                    | Approx. Monthly Cost (in USD) |
|---------------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| Azure Services      | App Service Plan     | Consumption plan, only pay for actual usage. More cost-effective for fluctuating workloads.                                                                                                              | $25                          |
|                     | Cosmos DB             | Serverless option, cost-effective for initially lower data volume. Scales as needed.                                                                                                    | $25                          |
|                     | Azure DevOps         | Basic plan for version control, CI/CD.                                                                                                                                               | $100                         |
| Third-Party APIs    | Market Data (Bloomberg)|  Subscription costs will be determined based on Affin's existing Bloomberg contract and specific data requirements.                                                                | $0 (included in existing contract)                 |
| **Total infrastructure costs (per month)** |                      |                                                                                                                                                                            | **$150**                         |


## Milestones for Approach 1

| Milestone   | Deliverable                                                                                           | Delivery Timeline (In Weeks) | Amount   |
|-------------|-------------------------------------------------------------------------------------------------------|------------------------------|----------|
| Milestone 0 | Project Kickoff, Requirements Gathering                                                              | Week 0                       | $1000    |
| Milestone 1 | System Design and Architecture Documentation                                                          | Week 2                       | $2000    |
| Milestone 2 | Development of Core Trading Engine                                                                     | Week 6                       | $7000    |
| Milestone 3 | Integration with Market Data and Existing Systems                                                   | Week 8                       | $5000    |
| Milestone 4 | Testing and Quality Assurance                                                                        | Week 9                       | $2000    |
| Milestone 5 | Deployment and Go-Live Support                                                                       | Week 10                      | $1000    |
| **Total Amount** |                                                                                                       |                              | **$18000** |


## Milestones for Approach 2

| Milestone   | Deliverable                                                                                           | Delivery Timeline (In Weeks) | Amount   |
|-------------|-------------------------------------------------------------------------------------------------------|------------------------------|----------|
| Milestone 0 | Project Kickoff, Requirements Gathering                                                              | Week 0                       | $1000    |
| Milestone 1 | System Design and Architecture Documentation                                                          | Week 3                       | $2000    |
| Milestone 2 | Development of Core Trading Engine (Phased approach)                                                | Week 8                       | $8000    |
| Milestone 3 | Integration with Market Data and Existing Systems (Phased approach)                                   | Week 10                      | $6000    |
| Milestone 4 | Testing and Quality Assurance                                                                        | Week 11                      | $2000    |
| **Total Amount** |                                                                                                       |                              | **$19000** |



## License Cost

No Power BI licensing is required for this project.  The platform will be custom-developed and will not rely on Power BI for its core functionality.


## Payment Terms and Conditions

*   **Currency:** USD
*   **Payment Schedule:** Milestone-based payments as outlined in the Milestone tables above.  50% upfront upon signing of contract; remaining 50% upon successful completion of milestones.
*   **Invoice Terms:** Invoices will be issued upon completion of each milestone. Payment is due within 15 days of invoice date.
*   **Interest on Late Payments:** A late payment fee of 1% per month will be applied to any overdue invoices.
*   **Right to Halt Work for Non-Payment:** We reserve the right to halt work on the project until outstanding payments are received.