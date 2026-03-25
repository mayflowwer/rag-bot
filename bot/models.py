from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str

    class Config:
        json_schema_extra = {
            "example": {"question": "Who is Kael Voryn and what is his role in the story?"}
        }

class SourceChunk(BaseModel):
    source: str
    chunk_id: int
    text_preview: str

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk]
    chunks_used: int