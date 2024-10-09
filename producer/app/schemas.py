from pydantic import BaseModel

class KafkaMessage(BaseModel):
    topic: str
    msg: str
    
class ResponseModel(BaseModel):
    status: str