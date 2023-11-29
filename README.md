Telemetry Data Pipeline

This project facilitates the ingestion, processing, and storage of telemetry data using Kafka messaging and PostgreSQL database.

Overview

The Telemetry Data Pipeline is designed to:
Read telemetry data in JSON format.
Publish the telemetry data to a Kafka topic.
Consume the data from the Kafka topic.
Store the telemetry data in a PostgreSQL database.


Components

Producer
telemetry_data_generator.py: Generates fake telemetry data as a JSON file.

Functionality:
Generates or reads telemetry data. Publishes data to the Kafka topic "telemetry_data."

Consumer
telemetry_data_consumer.py: Consumes messages from the "telemetry_data" Kafka topic.
Functionality:
Parses JSON messages received from Kafka. Inserts telemetry data into a PostgreSQL database.


Setup

Prerequisites
Python 3.x
Kafka broker running locally or accessible through bootstrap_servers variable.
PostgreSQL database with required permissions.

Installation
Clone the repository.

Install dependencies using pip install -r requirements.txt.

Configuration

Kafka Configuration:
Update bootstrap_servers in producer/consumer scripts to your Kafka broker.

PostgreSQL Configuration:
Update db_url in the consumer script to your PostgreSQL connection string.

Running the Pipeline

Producer Side:
Run telemetry_data_generator.py to generate and publish telemetry data to Kafka.

Consumer Side:
Execute telemetry_data_consumer.py to consume data from Kafka and store it in the PostgreSQL database.


Notes
Ensure Kafka and PostgreSQL are running and accessible before executing the pipeline.
Handle exceptions, retries, and error logging for robustness and fault tolerance.
Consider scalability and performance improvements for handling larger data volumes or concurrent requests.
