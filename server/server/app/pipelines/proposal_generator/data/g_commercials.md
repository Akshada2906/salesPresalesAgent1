# Commercials: REPO Trading Platform for Affin Moneybrokers

This section details the costs and payment terms associated with developing the REPO trading platform for Affin Moneybrokers. We present two approaches, each designed to meet project requirements while optimizing cost-effectiveness.  Both approaches adhere to the \$50,000 budget.

## Total Cost of Ownership

| Component             | Estimated Cost ($) - Approach 1 | Estimated Cost ($) - Approach 2 |
|----------------------|------------------------------------|------------------------------------|
| Infrastructure cost   | \$1,500 /month                    | \$2,000 /month                    |
| Development cost      | \$30,000                          | \$25,000                          |
| Power BI Licensing    | \$0.00 per user/month             | \$0.00 per user/month             |
| Development Time      | 12 Weeks                           | 10 Weeks                           |
| **Total (6 Months)** | **\$40,500**                       | **\$37,000**                       |


## Infrastructure Costs

**Approach 1:**

| Services            | Sub-services         | Description                                                                                                                                | Approx. Monthly Cost (in USD) |
|---------------------|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| Azure Services      | App Service Plan     | Basic Plan for hosting the API and web application.                                                                                | \$500                         |
|                     | Azure SQL Database   | Basic tier for storing transactional data.                                                                                            | \$100                         |
|                     | Azure Storage Account | Standard tier for storing large volumes of data, including market data feeds and collateral information.                              | \$300                         |
|                     | Azure DevOps         | Basic plan for version control, CI/CD, and collaboration tools                                                                         | \$600                         |
| Terraform           | HCP Free             |                                                                                                                                       | \$0.00                         |
| **Total infrastructure costs (per month)** |                      |                                                                                                                                       | **\$1,500**                     |


**Approach 2:** (Utilizes a more streamlined cloud architecture)

| Services            | Sub-services         | Description                                                                                                                               | Approx. Monthly Cost (in USD) |
|---------------------|----------------------|----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| AWS Services        | EC2                  | Instance for hosting the application (Optimized for cost with auto-scaling).                                                              | \$1000                        |
|                     | RDS                  | Database instance for storing data.                                                                                                   | \$500                         |
|                     | S3                   | Storage for data and collateral.                                                                                                      | \$200                         |
|                     | AWS CodePipeline     | CI/CD pipeline (included in AWS free tier up to certain limits)                                                                          | \$0                           |
| AWS CodeCommit       |                       | Version control repository (Included in AWS free tier up to certain limits)                                                            | \$0                           |
| **Total infrastructure costs (per month)** |                      |                                                                                                                                      | **\$2,000**                     |



## Milestones for Approach 1:

| Milestone   | Deliverable                                                                                           | Delivery Timeline (In Weeks) | Amount   |
|-------------|-------------------------------------------------------------------------------------------------------|------------------------------|----------|
| Milestone 0 | Project Kickoff                                                                                       | Week 0                       | \$2,000   |
| Milestone 1 | Requirements Gathering and System Design                                                              | Week 1-2                      | \$3,000   |
| Milestone 2 | Development of Core Trading Engine                                                                     | Week 3-6                      | \$10,000  |
| Milestone 3 | Integration with Market Data Feeds (Bloomberg)                                                        | Week 7-8                      | \$5,000   |
| Milestone 4 | Collateral Management Module Development                                                              | Week 9-10                     | \$5,000   |
| Milestone 5 | Compliance & Security Testing & Refinements                                                           | Week 11-12                    | \$5,000   |
| Total Amount |                                                                                                       |                              | **\$30,000** |


## Milestones for Approach 2:

| Milestone   | Deliverable                                                                                           | Delivery Timeline (In Weeks) | Amount   |
|-------------|-------------------------------------------------------------------------------------------------------|------------------------------|----------|
| Milestone 0 | Project Kickoff                                                                                       | Week 0                       | \$2,000   |
| Milestone 1 | Requirements Gathering and System Design                                                              | Week 1-2                      | \$3,000   |
| Milestone 2 | Development of Core Trading Engine and API Integration                                                 | Week 3-7                      | \$10,000  |
| Milestone 3 | Collateral Management Module Development and UI Development                                           | Week 8-9                      | \$5,000  |
| Milestone 4 | Compliance & Security Testing & Deployment                                                          | Week 10                        | \$5,000   |
| Total Amount |                                                                                                       |                              | **\$25,000** |


## License Cost

No specific Power BI licensing is required for this project as per the initial brief, therefore, the cost for Power BI licensing is $0.00 in both approaches.


## Payment Terms and Conditions

*   **Currency:** USD
*   **Payment Schedule:** Milestone-based payments (refer to Milestone tables above). 50% upfront payment upon signing of the contract. Remaining payments upon successful completion of each milestone.
*   **Invoice Terms:** Invoices are due within 15 days of the invoice date. Acceptance period of 5 business days from the date of invoice issuance.
*   **Interest on Late Payments:** A 1.5% monthly interest will be charged on any overdue payments.
*   **Right to Halt Work for Non-Payment:**  We reserve the right to halt work on the project if payments are not received according to the agreed-upon schedule.


**Note:** These cost estimates are based on current market rates and are subject to change based on project scope adjustments or unforeseen technical challenges.  The choice between Approach 1 and Approach 2 will depend on Affin Moneybrokers' preference for specific cloud platforms and desired level of service.  A detailed project scope will be defined prior to finalizing the budget and payment schedule.