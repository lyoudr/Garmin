from fastapi import FastAPI
from confluent_kafka.admin import AdminClient, NewTopic
from prometheus_fastapi_instrumentator import Instrumentator

from .routes import router
from .config import (
    BOOTSTRAP_SERVER,
    TOPIC
)

app = FastAPI()
app.include_router(router) 

# Kafka
admin_client = AdminClient({
    'bootstrap.servers': BOOTSTRAP_SERVER
})
topic_list = [NewTopic(TOPIC, 1, 1)]
admin_client.create_topics(topic_list)


# Initialize the instrumentator
instrumentator = Instrumentator()
# Register the instrumentator to the app
instrumentator.instrument(app).expose(app)