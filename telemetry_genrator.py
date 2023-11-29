from faker import Faker
import json
import random
from decimal import Decimal

fake = Faker()

telemetry_data = []

for _ in range(10000):
    data_point = {
        "timestamp": str(fake.date_time_between(start_date="-1y", end_date="now")),
        "sensor_id": fake.uuid4(),
        "temperature": float(random.uniform(-10, 40)),  # Convert to float
        "humidity": float(random.uniform(0, 100)),      # Convert to float
        "location": {
            "latitude": float(fake.latitude()),         # Convert to float
            "longitude": float(fake.longitude()),       # Convert to float
        },
    }
    telemetry_data.append(data_point)

# Save the generated telemetry data to a JSON file
with open("telemetry_data.json", "w") as file:
    json.dump(telemetry_data, file, indent=2, default=str)  # Use `default=str` to serialize Decimals as strings
