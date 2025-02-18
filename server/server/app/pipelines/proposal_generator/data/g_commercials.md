# Commercials

This section details the costs and payment terms associated with developing the automated Malaysian REPO/Reverse REPO trading application for Apple.  We propose two approaches, each optimized for different priorities: Approach 1 prioritizes speed to market with a slightly higher initial investment, while Approach 2 emphasizes long-term cost efficiency with a more gradual rollout. Both approaches remain within the specified budget of $24,234.0 USD.


## Total Cost of Ownership

| Component             | Estimated Cost ($) - Approach 1 | Estimated Cost ($) - Approach 2 |
|----------------------|------------------------------------|------------------------------------|
| Infrastructure cost   | $200 /month                      | $150 /month                      |
| Development cost      | $18,000                           | $15,000                           |
| Power BI Licensing    | $0 per user/month                 | $0 per user/month                 |
| Development Time      | 26 Weeks                          | 30 Weeks                          |
| **Total Project Cost** | **$18,420**                       | **$15,300**                       |


## Infrastructure Costs

**Approach 1**

| Services            | Sub-services         | Description                                                                                                                                                                                    | Approx. Monthly Cost (in USD) |
|---------------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| Azure Services      | App Service          | Hosting for the trading application.                                                                                                                                                           | $100                          |
|                     | Data Lake Storage    | Storage for market data and transaction records.                                                                                                                                                 | $50                           |
|                     | Azure DevOps         | Basic Plan (for 2 users): $12 per user/month. Provides access to Azure Boards, Repos, Pipelines (limited), Test Plans (read-only), Artifacts.                                           | $24                           |
| Terraform           | HCP Free             | UP TO 500 resources per month. Get started with all capabilities needed for infrastructure as code provisioning.                                                                             | $0.00                          |
| **Total infrastructure costs (per month)** |                      |                                                                                                                                                                                               | **$174**                         |


**Approach 2**

| Services            | Sub-services         | Description                                                                                                                                                                                    | Approx. Monthly Cost (in USD) |
|---------------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| AWS Services        | EC2                  | Cost-effective hosting for the application.                                                                                                                                                    | $75                           |
|                     | S3                   | Storage for market data and transaction records. Utilizes cheaper storage options than Azure.                                                                                              | $50                           |
|                     | AWS CodePipeline     |  For CI/CD Pipelines. Cheaper than Azure DevOps Basic for this use case                                                                                                                      | $25                           |
| Terraform           | HCP Free             | UP TO 500 resources per month. Get started with all capabilities needed for infrastructure as code provisioning.                                                                             | $0.00                          |
| **Total infrastructure costs (per month)** |                      |                                                                                                                                                                                               | **$150**                        |


## Milestones for Approach 1

| Milestone   | Deliverable                                                                                           | Delivery Timeline (In Weeks) | Amount     |
|-------------|-------------------------------------------------------------------------------------------------------|------------------------------|------------|
| Milestone 0 | Project Kickoff                                                                                       | Week 0                       | $1,000     |
| Milestone 1 | Requirements Gathering and System Design                                                              | Weeks 1-4                     | $2,000     |
| Milestone 2 | Development of Core Trading Engine                                                                     | Weeks 5-13                    | $5,000     |
| Milestone 3 | Integration with Market Data and Existing Systems                                                    | Weeks 14-18                   | $4,000     |
| Milestone 4 | Compliance Testing and Refinement                                                                     | Weeks 19-22                   | $3,000     |
| Milestone 5 | User Acceptance Testing and Deployment                                                                 | Weeks 23-26                   | $3,000     |
| **Total Amount** |                                                                                                       |                              | **$18,000** |


## Milestones for Approach 2

| Milestone   | Deliverable                                                                                           | Delivery Timeline (In Weeks) | Amount     |
|-------------|-------------------------------------------------------------------------------------------------------|------------------------------|------------|
| Milestone 0 | Project Kickoff                                                                                       | Week 0                       | $1,000     |
| Milestone 1 | Requirements Gathering and System Design                                                              | Weeks 1-5                     | $2,000     |
| Milestone 2 | MVP Development (Core Functionality)                                                                   | Weeks 6-15                    | $4,000     |
| Milestone 3 | Integration with Market Data (Phased Approach)                                                        | Weeks 16-20                   | $3,000     |
| Milestone 4 | Compliance Testing and Refinement (Iterative)                                                          | Weeks 21-25                   | $3,000     |
| Milestone 5 | User Acceptance Testing and Deployment (MVP)                                                           | Weeks 26-30                   | $2,000     |
| **Total Amount** |                                                                                                       |                              | **$15,000** |


## License Cost

This project does not require any Power BI licensing.  All data visualization and reporting will be handled within the application itself or through standard tools already available to Apple.


## Payment Terms and Conditions

*   **Currency:** USD
*   **Payment Schedule:** Milestone-based payments as outlined in the Milestone tables for each approach.  50% upfront upon contract signing, and the remaining amount distributed according to milestone completion and approval.
*   **Invoice Terms:** Invoices will be issued upon completion of each milestone. Payment is due within 15 days of invoice date.
*   **Interest on Late Payments:**  A late payment fee of 1% per month will be applied to any overdue payments.
*   **Right to Halt Work for Non-Payment:** We reserve the right to halt work on the project if payment is not received within 30 days of the invoice due date.


We believe both approaches offer compelling solutions within the stipulated budget, with Approach 1 offering a faster time-to-market and Approach 2 providing long-term cost savings.  We are prepared to discuss these options further and tailor them to Apple's specific needs and preferences.