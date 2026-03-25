"""
build_index.py — Задание 3: Создание векторного индекса базы знаний

Модель эмбеддингов: all-MiniLM-L6-v2 (Sentence-Transformers)
  - Репозиторий: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
  - Размер вектора: 384
  - Лицензия: Apache 2.0, бесплатно, работает локально

Запуск:
    pip install langchain langchain-community sentence-transformers faiss-cpu
    python build_index.py

Результат:
    faiss_index/index.faiss   — бинарный индекс FAISS
    faiss_index/index.pkl     — метаданные чанков (источник, текст, позиция)
"""

import os
import time
import json
import pickle
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ─── Настройки ────────────────────────────────────────────────────────────────

KNOWLEDGE_BASE_DIR = "./knowledge_base"   # папка с .md файлами
INDEX_DIR          = "./faiss_index"      # куда сохранять индекс
EMBEDDING_MODEL    = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE    = 500   # размер чанка в символах
CHUNK_OVERLAP = 50    # перекрытие между чанками (для сохранения контекста)

# ─── Шаг 1: Читаем документы ──────────────────────────────────────────────────

print("=" * 60)
print("Шаг 1: Загрузка документов из knowledge_base/")
print("=" * 60)

docs_raw = []
kb_path = Path(KNOWLEDGE_BASE_DIR)

for md_file in sorted(kb_path.glob("*.md")):
    if md_file.name == "terms_map_explanation.md":
        # этот файл — служебный, не включаем в индекс
        continue
    text = md_file.read_text(encoding="utf-8")
    docs_raw.append({
        "text":   text,
        "source": md_file.name,
        "title":  text.split("\n")[0].replace("# ", "").strip()
    })

print(f"Загружено файлов: {len(docs_raw)}")
for d in docs_raw:
    print(f"  • {d['source']} — {len(d['text'])} символов")

# ─── Шаг 2: Нарезаем на чанки ─────────────────────────────────────────────────

print("\n" + "=" * 60)
print(f"Шаг 2: Нарезка на чанки (размер={CHUNK_SIZE}, перекрытие={CHUNK_OVERLAP})")
print("=" * 60)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""]
)

from langchain_core.documents import Document

all_chunks = []
for doc in docs_raw:
    chunks = splitter.split_text(doc["text"])
    for i, chunk_text in enumerate(chunks):
        all_chunks.append(Document(
            page_content=chunk_text,
            metadata={
                "source":    doc["source"],
                "title":     doc["title"],
                "chunk_id":  i,
                "total_chunks": len(chunks)
            }
        ))

print(f"Всего чанков: {len(all_chunks)}")
print(f"Среднее на документ: {len(all_chunks) / len(docs_raw):.1f} чанков")

# Показываем пример чанка
print("\nПример чанка #0:")
print(f"  Источник: {all_chunks[0].metadata['source']}")
print(f"  Размер:   {len(all_chunks[0].page_content)} символов")
print(f"  Текст:    {all_chunks[0].page_content[:150]}...")

# ─── Шаг 3: Загружаем модель эмбеддингов ──────────────────────────────────────

print("\n" + "=" * 60)
print(f"Шаг 3: Загрузка модели {EMBEDDING_MODEL}")
print("=" * 60)

t0 = time.time()

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

print(f"Модель загружена за {time.time() - t0:.1f}с")
print(f"Размер вектора: 384")

# ─── Шаг 4: Создаём FAISS индекс ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("Шаг 4: Генерация эмбеддингов и создание FAISS индекса")
print("=" * 60)

t0 = time.time()

vectorstore = FAISS.from_documents(
    documents=all_chunks,
    embedding=embeddings
)

elapsed = time.time() - t0
print(f"Индекс создан за {elapsed:.1f}с")
print(f"Векторов в индексе: {vectorstore.index.ntotal}")

# ─── Шаг 5: Сохраняем индекс ──────────────────────────────────────────────────

print("\n" + "=" * 60)
print(f"Шаг 5: Сохранение индекса в {INDEX_DIR}/")
print("=" * 60)

os.makedirs(INDEX_DIR, exist_ok=True)
vectorstore.save_local(INDEX_DIR)

print(f"Сохранено:")
for f in Path(INDEX_DIR).iterdir():
    print(f"  • {f.name}  ({f.stat().st_size // 1024} KB)")

# ─── Шаг 6: Тестовый запрос ───────────────────────────────────────────────────

print("\n" + "=" * 60)
print("Шаг 6: Тестовые запросы к индексу")
print("=" * 60)

test_queries = [
    "Who is Kael Voryn?",
    "What is Flux Essence and where does it come from?",
    "How do the Eremai ride duneserpents?",
]

for query in test_queries:
    print(f"\nЗапрос: '{query}'")
    results = vectorstore.similarity_search(query, k=3)
    for i, r in enumerate(results):
        print(f"  [{i+1}] {r.metadata['source']} (чанк {r.metadata['chunk_id']})")
        print(f"       {r.page_content[:100]}...")

# ─── Итоговая статистика ───────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("ИТОГОВЫЙ ОТЧЁТ")
print("=" * 60)
print(f"  Модель эмбеддингов : {EMBEDDING_MODEL}")
print(f"  Размер вектора     : 384")
print(f"  База знаний        : {len(docs_raw)} документов")
print(f"  Размер чанка       : {CHUNK_SIZE} символов (overlap={CHUNK_OVERLAP})")
print(f"  Всего чанков       : {len(all_chunks)}")
print(f"  Векторов в индексе : {vectorstore.index.ntotal}")
print(f"  Время генерации    : {elapsed:.1f}с")
print(f"  Индекс сохранён в  : {INDEX_DIR}/")
print("=" * 60)
print("Готово! Индекс можно загружать в RAG-бота:")
print("  vectorstore = FAISS.load_local(INDEX_DIR, embeddings)")