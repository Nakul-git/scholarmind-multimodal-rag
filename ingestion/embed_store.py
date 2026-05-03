from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from core.config import SETTINGS


EMBEDDING_DIR = SETTINGS.embedding_dir


def get_embedding_model():
    return OllamaEmbeddings(model=SETTINGS.embedding_model)


def create_vector_db(docs):
    embedding_model = get_embedding_model()
    db = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=EMBEDDING_DIR,
        collection_metadata={"hnsw:space": "cosine"},
    )
    print("Embeddings stored in ChromaDB")
    return db


def load_vector_db():
    embedding_model = get_embedding_model()
    return Chroma(
        persist_directory=EMBEDDING_DIR,
        embedding_function=embedding_model,
        collection_metadata={"hnsw:space": "cosine"},
    )
