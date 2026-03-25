from models import AskRequest, SourceChunk, AskResponse
from fastapi import HTTPException, APIRouter, Request
import service


router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask(request: Request):
    body = await request.json()
    question = body.get("question", "").strip()
    
    if not question:
        raise HTTPException(status_code=400, detail="Вопрос не валидный")
    
    vectorstore = request.app.state.vectorstore
    client = request.app.state.client

    # RAG pipeline
    chunks = service.retrieve_chunks(question, vectorstore)
    prompt = service.build_prompt(question, chunks)
    answer = service.ask_llm(prompt)

    # Формируем источники для ответа
    sources = [
        SourceChunk(
            source=chunk.metadata.get("source", "unknown"),
            chunk_id=chunk.metadata.get("chunk_id", 0),
            text_preview=chunk.page_content[:150] + "..."
        )
        for chunk in chunks
    ]

    return AskResponse(
        question=question,
        answer=answer,
        sources=sources,
        chunks_used=len(chunks)
    )