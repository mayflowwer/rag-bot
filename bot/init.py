import os
from pathlib import Path
from openai import OpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import configs


def init():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print("Загрузка модели эмбеддингов...")
    embeddings = HuggingFaceEmbeddings(
        model_name=configs.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    print("Загрузка FAISS индекса...")
    if not Path(configs.INDEX_DIR).exists():
        raise RuntimeError(f"Индекс не найден: {configs.INDEX_DIR}. Запустите build_index.py")

    vectorstore = FAISS.load_local(
        configs.INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print(f"Индекс загружен. Векторов: {vectorstore.index.ntotal}")

    return client, vectorstore
