from fastapi import APIRouter, HTTPException

from .schemas import ResponseModel
from .services.background_task import poll_kafka_messages

import threading

router = APIRouter()

@router.get(
    '/consume',
    tags = ['consumer'],
    summary='Consume message from Kafka topic.',
    response_model=ResponseModel
)
def consume():
    try:
        # Start Kafka polling in a separate thread, continously poll event from topic
        polling_thread = threading.Thread(target=poll_kafka_messages, daemon=True)
        polling_thread.start()
        
        return ResponseModel(
            content={'message': 'Consumer started polling messages from Kafka.'},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    