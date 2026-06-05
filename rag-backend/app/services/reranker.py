from sentence_transformers import CrossEncoder

_reranker = None


def get_reranker():
    global _reranker

    if _reranker is None:
        print("Loading reranker model...")

        _reranker = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    return _reranker


def rerank(question, docs):

    if not docs:
        return []

    reranker = get_reranker()

    pairs = [
        (question, doc["text"])
        for doc in docs
    ]

    scores = reranker.predict(
        pairs
    )

    scored_docs = list(
        zip(scores, docs)
    )

    scored_docs.sort(
        key=lambda x: x[0],
        reverse=True
    )

    reranked_docs = [
        doc
        for score, doc in scored_docs
    ]

    return reranked_docs[:5]