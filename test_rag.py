from backend.rag.document_builder import report_to_document
from backend.rag.chunker import chunk_document
from backend.models.report import ReportResult
from backend.rag.embeddings import embed_chunks, embed_query
from backend.rag.vector_store import (
    search_similar,
    store_chunks,
    get_stored_chunks
)

report = ReportResult(
    title="AI Market Intelligence Report",

    executive_summary=(
        "The AI market continues to experience strong growth "
        "driven by increasing enterprise adoption and demand "
        "for AI infrastructure."
    ),

    market_analysis=[
        "AI infrastructure demand continues to increase.",
        "Enterprise adoption is expanding across multiple industries."
    ],

    competitive_landscape=[
        "Competition remains strong among major technology companies."
    ],

    trend_analysis=[
        "Generative AI adoption continues to expand.",
        "AI infrastructure remains a major area of investment."
    ],

    growth_drivers=[
        "Enterprise AI adoption",
        "Increasing demand for AI infrastructure"
    ],

    risks=[
        "High infrastructure costs",
        "Rapid technological changes"
    ],

    opportunities=[
        "Enterprise AI solutions",
        "AI infrastructure services"
    ],

    strategic_outlook=(
        "The market is expected to remain highly competitive "
        "with continued investment in AI technologies."
    )
)

document = report_to_document(report)
chunks = chunk_document(document)
embeddings = embed_chunks(chunks)
store_chunks(chunks, embeddings)
query = "What are the major growth drivers in the AI market?"

query_embedding = embed_query(query)

results = search_similar(
    query_embedding,
    top_k=3
)

print("\n========== SIMILARITY SEARCH ==========")

print("Query:")
print(query)

print("\nRetrieved Documents:")

for document in results["documents"][0]:
    print("\n--- Retrieved Chunk ---")
    print(document)

print("=======================================")


print("\n========== RAG DOCUMENT ==========")
print(document)

print("\n========== CHUNKS ==========")
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)

print("\n===================================")
print(f"Total chunks: {len(chunks)}")

print("\n========== EMBEDDINGS ==========")

for i, embedding in enumerate(embeddings):
    print(f"Chunk {i + 1} vector dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")

print("================================")

stored_data = get_stored_chunks()

print("\n========== STORED DATA ==========")

print("Stored IDs:")
print(stored_data["ids"])

print("\nStored Documents:")

for document in stored_data["documents"]:
    print(document)

print("=================================")