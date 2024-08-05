### Author: Baraka

### Date: 2023-06-10

# CLoud Pulse Database by Baraka.

### Details

This project is a minimal representation of a scalable and fault-tolerant database using Lambda Architecture on Google Cloud. This is a high-level complex database that will be developed over the next several sprints.

![cloude](https://github.com/xrbams/cloudpulsep1/assets/112469099/f6209543-8ee8-4d92-bdb6-a47813a696a7)

### Table of Contents

-   [Overview](#overview)
-   [Architecture](#architecture)
-   [Tools and Technologies](#tools-and-technologies)
-   [Features](#features)
-   [Setup and Installation](#setup-and-installation)
-   [Usage](#usage)
-   [Contributing](#contributing)
-   [Future Work](#future-work)
-   [Contact](#contact)

### Overview

Cloud Pulse Database is designed to be a robust and scalable solution for handling large volumes of data with fault tolerance and high availability. It leverages the power of Google Cloud Platform and various open-source technologies to provide a comprehensive database solution.

### Architecture

The project implements Lambda Architecture, which combines batch and real-time processing to provide accurate and up-to-date results. The architecture consists of:

-   **Batch Layer**: Processes large volumes of historical data using Apache Spark.
-   **Speed Layer**: Handles real-time data streams using Kafka.
-   **Serving Layer**: Merges results from the batch and speed layers to provide query results.

### Tools and Technologies

-   **Google Cloud Platform (GCP)**: Provides the infrastructure for the entire solution.
-   **Pulumi IaC**: Used for infrastructure as code to manage and provision cloud resources.
-   **Apache Beam (Google Cloud Dataflow)**: Transitioning to **Apache Spark** for data processing.
-   **Google Cloud Pub/Sub**: Transitioning to **Kafka** for real-time messaging.
-   **Google Cloud Storage**: Used for storing raw data and intermediate results.
-   **BigQuery**: Transitioning to **MySQL** for data warehousing.
-   **Cloud Functions / App Engine**: Transitioning to **Kubernetes** for container orchestration.
-   **Stackdriver**: Transitioning to **Prometheus / Grafana** for monitoring and logging.

### Features

-   **Scalability**: Designed to handle large-scale data processing with ease.
-   **Fault Tolerance**: Ensures data integrity and availability even in the event of failures.
-   **Real-Time Processing**: Combines batch processing with real-time data streams for up-to-date results.
-   **Flexible Architecture**: Modular components that can be easily replaced or upgraded.

### Setup and Installation

1.  **Clone the repository**:

    ```
    git clone https://github.com/xrbams/cloudpulsep1.git
    cd cloudpulsep1
    ```

2.  **Install dependencies**:

    #### Install Python dependencies
    ```
    pip install -r requirements.txt
    ```

3.  **Provision infrastructure**:

    #### Using Pulumi
    ```
    pulumi up
    ```

4.  **Deploy applications**:

    #### Example for Kubernetes
    ```
    kubectl apply -f kubernetes/deployment.yaml
    ```

### Usage

-   **Running Batch Jobs**:

    #### Example Spark job
    ```
    spark-submit jobs/batch_job.py
    ```

-   **Consuming Real-Time Data**:

    #### Example Kafka consumer
    ```
    python consumers/real_time_consumer.py
    
    ```

-   **Querying Data**:

    #### Example MySQL query
    ```
    mysql -u user -p -e 'SELECT * FROM data_table;'
    ```

### Contributing

We welcome contributions from the community. To contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature-branch`).
3.  Commit your changes (`git commit -m 'Add new feature'`).
4.  Push to the branch (`git push origin feature-branch`).
5.  Create a pull request.

### Future Work

-   **Integration with Machine Learning**: Adding capabilities to process and analyze data using machine learning algorithms.
-   **Enhanced Security**: Implementing advanced security features to protect data and infrastructure.
-   **Optimized Performance**: Continuously improving the performance of batch and real-time processing.

### Contact

For any questions or inquiries, please contact:

-   **Name**: Baraka
-   **Email**: bmsakamali@gmail.com
-   **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/bm-827832234/)

## Instructions to setup and run.

### get all players & post a player at: 
- <site-name>/players

### get a player by id: 
- <site-name>/players/:id

### update a players team at: 
- <site-name>/players/:id/teams


### get all teams and post a team at: 
- <site-name>/teams

### get a team by the name
- <site-name>/teams/:team

### update a teams city at: 
- <site-name>/teams/:place


