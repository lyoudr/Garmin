from fastapi import APIRouter, HTTPException
from confluent_kafka import Producer

from .config import BOOTSTRAP_SERVER
from .helper import delivery_report
from .schemas import KafkaMessage, ResponseModel

router = APIRouter()
# Kafka producer configuration
conf = {
    'bootstrap.servers': BOOTSTRAP_SERVER
}
producer = Producer(conf)


@router.post(
    '/produce',
    tags = ['producer'],
    summary='Produce message to Kafka topic.',
    response_model=ResponseModel
)
def produce(kafka_msg: KafkaMessage):
    try:
        producer.produce(
            kafka_msg.topic,
            kafka_msg.message.encode('utf-8'),
            callback=delivery_report
        )
        producer.flush() # Force delivery of the message.
        return ResponseModel(status='Deliver message to Kafka topic successfully.')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to produce message: {str(e)}")
    