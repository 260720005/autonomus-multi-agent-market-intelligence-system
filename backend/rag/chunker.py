from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 150,
)

def chunk_document(document: str) -> list[str]:
    """
    Split a RAG Ready document into smaller overlapping chunks.
    """
    chunks = text_splitter.split_text(document)

    return chunks
