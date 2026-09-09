from backend.models.report import ReportResult

from backend.rag.document_builder import report_to_document
from backend.rag.chunker import chunk_document
from backend.rag.embeddings import embed_chunks
from backend.rag.vector_store import store_chunks


def store_report_in_memory(report: ReportResult):
    """
    Convert a final report into chunks,
    generate embeddings, and store them in ChromaDB.
    """

    document = report_to_document(report)

    chunks = chunk_document(document)

    embeddings = embed_chunks(chunks)

    report_id = store_chunks(
        chunks,
        embeddings,
        report.title
    )

    return report_id