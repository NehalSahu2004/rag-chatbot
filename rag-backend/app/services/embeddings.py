from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en"
)

def generate_embeddings(texts):

    embeddings = model.encode(texts)

    return embeddings.tolist()