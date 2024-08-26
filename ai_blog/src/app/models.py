from pydantic import BaseModel, Field
from typing import List, Annotated


class BlogPost(BaseModel):
    title: str
    tags: List[str]
    content: str



class RequestModel(BaseModel):
    topic: Annotated[str, Field(max_length=150)]