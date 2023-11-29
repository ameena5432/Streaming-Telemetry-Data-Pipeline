import json
from confluent_kafka import Producer

# Kafka broker settings
bootstrap_servers = "localhost:9092"  

# Kafka topic where telemetry data will be published
topic = "telemetry_data"

# Path to your telemetry data file
telemetry_file_path = "/Users/ameena/Documents/Telemetry_Pipeline/telemetry_data.json"

# Kafka producer configuration
producer_config = {
    "bootstrap.servers": bootstrap_servers,
}

# Callback function to handle delivery reports
def delivery_report(err, msg):
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

# Creating a Kafka producer instance
producer = Producer(producer_config)

# Reading the telemetry data from the file and publishing it to Kafka topic telemetry_data
with open(telemetry_file_path, "r") as file:
    telemetry_data = json.load(file)
    for data_point in telemetry_data:
        # Convert the data point to a JSON string
        json_data = json.dumps(data_point)
        
        # Produce the JSON data to the Kafka topic
        producer.produce(topic, key=None, value=json_data, callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery reports to be received
producer.flush()
