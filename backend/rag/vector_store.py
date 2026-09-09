# Persistent is used to save in memory permanently
import chromadb
import uuid
from datetime import datetime

chroma_client = chromadb.PersistentClient(
    path="./data/chroma"
)

collection = chroma_client.get_or_create_collection(
    name="market_intelligence"
)

def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    report_title: str
):
    """
    Store text chunks, embeddings, and metadata in ChromaDB.
    """

    report_id = str(uuid.uuid4())

    created_at = datetime.now().isoformat()

    ids = [
        f"report_{report_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "report_id": report_id,
            "report_title": report_title,
            "report_type": "market_intelligence",
            "created_at": created_at
        }
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return report_id

def get_stored_chunks():
    """
    Retrieve stored documents and metadata from ChromaDB.
    """

    results = collection.get(
        include=["documents", "metadatas"]
    )

    return results

def search_similar(
    query_embedding: list[float],
    top_k : int = 3
):
    """
    Search ChromaDB for documents similar to the query.
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results