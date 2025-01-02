from pydantic import BaseModel

class NewsCreate(BaseModel):
    title: str
    content: str
