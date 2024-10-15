### Author: Baraka

### Date: 2023-06-10

# CLoud Pulse Migration.

### Table of Contents

-   [Overview](#overview)
-   [Different Data To Be Hosted](#hosted-data)
-   [Architecture](#architecture)
-   [Tools and Technologies](#tools-and-technologies)
-   [Features](#features)
-   [Project Structure](#project-structure)
-   [Reflect and Learnings](#reflect-and-learnings)
-   [Future Work](#future-work)
-   [Contact](#contact)

### Overview

The main goal of this project is to design and build an end-to-end data engineering pipeline by ingesting, processing, and transforming data from a source system into a relational database and migrating it to a cloud data warehouse, all while implementing batch and stream processing pipelines and integrating with both SQL and NoSQL databases.

The main use of this ETL pipeline is to have data ready to be queried for analytics in PowerBi and Running different Trading Algorithms using this readily available data solution. 

### Different Data To Be Hosted
-  **Model Cars**: A dataset containing specifications, prices, and features of various model cars.
-  **Data Jobs Salaries**: Salary information for different roles in the data industry, including positions like data scientists, analysts, and engineers.
-  **Northwind Traders**: Data from the Northwind Traders database, commonly used for business examples, containing orders, customers, suppliers, and employee records.
-  **world Economic Indicators**: Global economic data, including GDP, inflation rates, unemployment, and other key financial metrics from different countries.
-  **CRM Sales Opportunities**: Customer relationship management (CRM) data showing potential sales opportunities, including leads, deal size, and sales stages.
-  **Nvidia Stock Prices**: Historical and current stock prices of Nvidia Corporation, including daily open, close, high, low, and volume.

### Tools and Technologies

-   **Astro**: Data orchestration Tool. https://www.astronomer.io/docs/astro
-   **Data Ingestion and Cleaning**: Python, Pandas, Numpy.
-   **Database**: PostgreSQL, Databricks.
-   **Data Processing**: Apache Spark, Apache Kafka.
-   **Pipeline Management**: Apache Airflow.
-   **NoSQL Database**: ElasticSearch.
-   **Cloud Platform**: Databricks.
-   **Data Migration**: Postgres to Databricks, Postgres to NoSQL.
-   **Production Iac**: Terraform and Azure Databricks 

## Running the Application

This project uses Pulumi for infrastructure provisioning and Astro for Airflow deployment. Below are the steps to run the project locally:

### Prerequisites
- Python 3.x installed
- Pulumi CLI installed
- Docker installed (for Airflow and Astro)
- Astro CLI installed
- Google Cloud SDK installed (for deploying to BigQuery)

### Step 1: Install Dependencies
First, clone the repository and install the required Python packages:

```bash
git clone https://github.com/your-repo/project-name.git
cd project-name
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd pulumi
python3 -m venv venv
source venv/bin/activate
pulumi up

cd ../  # Back to the root directory
astro dev start

pytest

astro dev stop

```

### Features

-   **Scalability**: Designed to handle large-scale data processing with ease.
-   **Fault Tolerance**: Ensures data integrity and availability even in the event of failures.
-   **Real-Time Processing**: Combines batch processing with real-time data streams for up-to-date results.
-   **Flexible Architecture**: Modular components that can be easily replaced or upgraded.


### Reflect and Learnings

- Gained hands-on experience with the entire lifecycle of data engineering: ingestion, transformation, pipeline building, and data processing.
- Familiarity with multiple databases (PostgreSQL, Databricks, NoSQL) and the specific challenges of migrating data between them.
- Improved proficiency in batch and stream data processing using tools like Apache Kafka and Apache Spark.
- Learned to automate workflows and pipeline scheduling with Apache Airflow.

### Future Work

- **Advanced Streaming Architectures**: Implement more advanced streaming use cases with real-time data pipelines using Apache Kafka.   
- **Data Lake Integration**: Integrate with a cloud data lake for large-scale data storage and processing.
- **Machine Learning Pipelines**: Use the processed data to feed into machine learning models.
- **Advanced Data Modeling**: Implement more complex schema designs in Databricks or PostgreSQL.
- **Cloud Infrastructure**: Deploy the entire pipeline on a cloud platform like AWS, GCP, or Azure.

### Contact

For any questions or inquiries, please contact:

-   **Name**: Baraka
-   **Email**: bmsakamali@gmail.com
-   **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/bm-827832234/)


