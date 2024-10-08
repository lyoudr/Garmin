import os 
from dotenv import load_dotenv

# Load environment variable from .env file, if present
load_dotenv()

# Get environment variable
BOOTSTRAP_SERVER = os.getenv('KAFKA_BROKER_URL', 'kafka-container:9092')
GROUP_ID = os.getenv('GROUP_ID', 'consumer-group')
TOPIC = os.getenv('TOPIC', 'test-topic')
CASSANDRA_CONTACT_POINTS = os.getenv('CASSANDRA_CONTACT_POINTS')
CASSANDRA_PORT = os.getenv('CASSANDRA_PORT')
CASSANDRA_KEYSPACE = os.getenv('CASSANDRA_KEYSPACE')