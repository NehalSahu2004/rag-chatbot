from fastapi import APIRouter
import os


from app.db.chroma import (
    get_all_documents,
    delete_document
)


router = APIRouter()


UPLOAD_DIR = "uploads"




@router.get(
    "/documents"
)
def list_documents():

    return {
        "documents":
        get_all_documents()
    }






@router.delete(
    "/documents/{filename}"
)
def remove_document(
    filename: str
):


    deleted_chunks = (
        delete_document(
            filename
        )
    )



    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )



    if os.path.exists(
        file_path
    ):

        os.remove(
            file_path
        )



    return {

        "message":
        "Deleted",

        "chunks_removed":
        deleted_chunks

    }