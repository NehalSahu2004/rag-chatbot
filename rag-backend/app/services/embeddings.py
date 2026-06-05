from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(
            "BAAI/bge-small-en"
        )

    return _model


def generate_embeddings(texts):

    model = get_model()

    embeddings = model.encode(
        texts
    )

    return embeddings.tolist()