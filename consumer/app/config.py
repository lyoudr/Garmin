import os 
from dotenv import load_dotenv
from confluent_kafka import Consumer

# Load environment variable from .env file, if present
load_dotenv()


# Get environment variable
BOOTSTRAP_SERVER = os.getenv('KAFKA_BROKER_URL', '127.0.0.1:9092')
GROUP_ID = os.getenv('GROUP_ID', 'consumer-group')
TOPIC = os.getenv('TOPIC', 'test-topic')
CASSANDRA_CONTACT_POINTS = os.getenv('CASSANDRA_CONTACT_POINTS', '127.0.0.1')
CASSANDRA_PORT = os.getenv('CASSANDRA_PORT', 9042)
CASSANDRA_KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'ann')

# Kafka consumer configuration
consumer_conf = {
    'bootstrap.servers': BOOTSTRAP_SERVER,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC])