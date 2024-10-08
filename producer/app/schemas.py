from pydantic import BaseModel

class KafkaMessage(BaseModel):
    topic: str
    message: str
    
class ResponseModel(BaseModel):
    status: str