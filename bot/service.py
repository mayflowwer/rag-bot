import os
from openai import OpenAI
from dotenv import load_dotenv
import configs


def retrieve_chunks(question: str, vectorstore) -> list:
    return vectorstore.similarity_search(question, k=configs.TOP_K)

def build_prompt(question: str, chunks: list) -> str:
    """Шаг 3: Формируем промпт с найденными чанками."""
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.metadata.get("source", "unknown")
        context_parts.append(f"[Document {i} — {source}]\n{chunk.page_content}")

    context = "\n\n".join(context_parts)

    return f"""CONTEXT DOCUMENTS:
{context}

USER QUESTION: {question}

Remember: answer ONLY based on the context above. Think step by step."""

def ask_llm(prompt: str) -> str:
    """Шаг 4: Отправляем промпт в GPT-4o mini."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=configs.LLM_MODEL,
        messages=[
            {"role": "system", "content": configs.SYSTEM_PROMPT},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.1,
        max_tokens=800
    )
    return response.choices[0].message.content