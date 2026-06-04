import chromadb
import uuid
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


client = chromadb.PersistentClient(
    path=os.path.join(
        BASE_DIR,
        "../../chroma_db"
    )
)


def get_user_collection(
    user_id: int
):

    return client.get_or_create_collection(
        name=f"user_{user_id}_docs"
    )


def store_embeddings(
    user_id,
    chunks,
    embeddings
):

    collection = get_user_collection(
        user_id
    )

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(
            str(uuid.uuid4())
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            {
                "pdf_name":
                chunk["pdf_name"],

                "page":
                chunk["page"],

                "chunk_id":
                chunk["chunk_id"],

                "user_id":
                user_id
            }
        )

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


def query_embeddings(
    user_id,
    query_embedding,
    n_results=10
):

    collection = get_user_collection(
        user_id
    )

    return collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=n_results
    )


def get_all_documents(
    user_id
):

    collection = get_user_collection(
        user_id
    )

    data = collection.get()

    pdfs = set()

    for meta in data["metadatas"]:

        pdfs.add(
            meta["pdf_name"]
        )

    return sorted(
        list(pdfs)
    )


def delete_document(
    user_id,
    filename
):

    collection = get_user_collection(
        user_id
    )

    data = collection.get()

    ids_to_delete = []

    for idx, meta in zip(
        data["ids"],
        data["metadatas"]
    ):

        if (
            meta["pdf_name"]
            ==
            filename
        ):

            ids_to_delete.append(
                idx
            )

    if ids_to_delete:

        collection.delete(
            ids=ids_to_delete
        )

    return len(
        ids_to_delete
    )