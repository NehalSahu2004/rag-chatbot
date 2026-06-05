from app.services.embeddings import get_model
from app.db.chroma import query_embeddings


def retrieve_documents(
    question,
    user_id
):

    model = get_model()

    query_embedding = model.encode(
        question
    ).tolist()

    results = query_embeddings(
        user_id,
        query_embedding
    )

    retrieved_docs = []

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for doc, meta in zip(
        docs,
        metas
    ):

        retrieved_docs.append(
            {
                "text": doc,
                "pdf_name": meta["pdf_name"],
                "page": meta["page"]
            }
        )

    return retrieved_docs