from pydantic import BaseModel
    

class DataPipelineRequestModel(BaseModel):
    file_path: str

class ResponseModel(BaseModel):
    content: dict
    status_code: int


