from app.services.embeddings import model
from app.db.chroma import query_embeddings


def retrieve_documents(question):

    query_embedding = model.encode(question).tolist()

    results = query_embeddings(query_embedding)

    retrieved_docs = []

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for doc, meta in zip(docs, metas):

        retrieved_docs.append({
            "text": doc,
            "pdf_name": meta["pdf_name"],
            "page": meta["page"]
        })

    return retrieved_docs