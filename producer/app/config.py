import os 
from dotenv import load_dotenv

# Load environment variables from .env file, if present
load_dotenv()

# Get environment variables
BOOTSTRAP_SERVER = os.getenv('KAFKA_BROKER_URL', '127.0.0.1:9092')
TOPIC = os.getenv('TOPIC', 'test-topic')