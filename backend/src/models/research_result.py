from pydantic import BaseModel

class ResearchResult(BaseModel):
    query: str
    result: str