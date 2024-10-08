from fastapi import APIRouter, HTTPException
from confluent_kafka import Consumer, KafkaException

from .config import (
    BOOTSTRAP_SERVER,
    GROUP_ID,
    TOPIC,
)
from .schemas import ResponseModel, DataPipelineRequestModel
from .data_pipeline import handle_csv_billing_data

router = APIRouter()
# Kafka consumer configuration
consumer_conf = {
    'bootstrap.servers': BOOTSTRAP_SERVER,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC])


@router.get(
    '/consume',
    tags = ['consumer'],
    summary='Consume message from Kafka topic.',
    response_model=ResponseModel
)
def consume():
    try:
        msg = consumer.poll(timeout = 15.0)
        if msg is None:
            return ResponseModel(
                content={'message': 'No message found'}, 
                status_code=200
            )
        if msg.error():
            raise KafkaException(msg.error())
        else:
            handle_csv_billing_data(msg.value().decode('utf-8'))
        return ResponseModel(
            content={'message': msg.value().decode('utf-8')},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    