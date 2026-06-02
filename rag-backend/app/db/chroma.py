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


collection = client.get_or_create_collection(
    name="rag_collection"
)




def store_embeddings(
    chunks,
    embeddings
):

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
                chunk["chunk_id"]
            }
        )



    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )






def query_embeddings(
    query_embedding,
    n_results=10
):

    return collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=n_results
    )






# =========================
# NEW FUNCTIONS
# =========================


def get_all_documents():

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
    filename
):


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