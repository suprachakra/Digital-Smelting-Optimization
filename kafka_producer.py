"""
kafka_producer.py
A sample script sending synthetic sensor data to a Kafka topic in real-time.
Usage:
  python kafka_producer.py
Requires:
  pip install kafka-python
Ensure you have a running Kafka broker at localhost:9092
"""

from kafka import KafkaProducer
import json
import time
import random
import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'metalx_sensors'

def generate_sensor_message():
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "voltage": round(random.uniform(4.0, 4.5), 2),
        "current": round(random.uniform(100, 125), 2),
        "temperature": round(random.uniform(775, 785), 1),
        "anode_position": round(random.uniform(0.14, 0.16), 2),
        "chemical_composition": round(random.uniform(0.97, 0.99), 2)
    }

if __name__ == "__main__":
    print(f"Starting Kafka producer on topic '{TOPIC_NAME}'")
    while True:
        msg = generate_sensor_message()
        producer.send(TOPIC_NAME, msg)
        print("Sent message:", msg)
        time.sleep(1)

