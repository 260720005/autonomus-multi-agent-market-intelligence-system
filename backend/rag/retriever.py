from backend.rag.embeddings import embed_query
from backend.rag.vector_store import search_similar

def retrieve_relevant_chunks(
    query: str,
    top_k: int = 3
) -> list[str]:
    """
    Retrieve the most relevant stored chunks for a user query.
    """

    query_embedding = embed_query(query)

    results = search_similar(
        query_embedding,
        top_k=top_k
    )

    documents = results["documents"][0]

    return documents