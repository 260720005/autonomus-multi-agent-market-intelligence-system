from sentence_transformers import SentenceTransformer  # Converts the text to Vectors

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Convert text chunks into numerical vector embeddings.

    """
    embeddings = embedding_model.encode( # encode converts chunks to embeddings
        chunks,
        convert_to_numpy= True
    ) 
    return embeddings.tolist()

def embed_query(query: str) -> list[float]:
    """
    Convert a user query into numerical embedding.
    """

    embedding = embedding_model.encode(
        query,
        convert_to_numpy= True
    )
    return embedding.tolist()