import json
from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'telemetry-consumer',
    'auto.offset.reset': 'earliest',
}

# Create a Kafka consumer instance
consumer = Consumer(consumer_config)

# Subscribe to the Kafka topic
consumer.subscribe(['telemetry_data']) 

# Define SQLAlchemy database and telemetry data model
Base = declarative_base()

class TelemetryData(Base):
    __tablename__ = 'telemetry_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String)
    sensor_id = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    location = Column(JSON)

# PostgreSQL connection string
db_url = "postgresql://Datapipeline_DB_user:Datapipeline_DB_pwd@0.0.0.0:5432/Datapipeline_DB"  

# Create the database engine
engine = create_engine(db_url)

# Create the database tables
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print('Reached end of partition')
            else:
                print('Error while consuming message:', msg.error())
        else:
            try:
                # Parse the received message's value as JSON
                telemetry_data = json.loads(msg.value())

                # Create a TelemetryData object and insert it into the database
                telemetry_entry = TelemetryData(
                    timestamp=telemetry_data['timestamp'],
                    sensor_id=telemetry_data['sensor_id'],
                    temperature=telemetry_data['temperature'],
                    humidity=telemetry_data['humidity'],
                    location=telemetry_data['location']
                )
                session.add(telemetry_entry)
                session.commit()
                print("Inserted telemetry data into PostgreSQL")

            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
            except Exception as e:
                print("Error inserting data into PostgreSQL:", e)

except KeyboardInterrupt:
    pass
finally:
    session.close()
    consumer.close()
