from fastapi import (
    APIRouter,
    Depends
)

import os

from app.services.dependencies import (
    get_current_user
)

from app.db.chroma import (
    get_all_documents,
    delete_document
)

router = APIRouter()


@router.get("/documents")
def list_documents(
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user[
        "user_id"
    ]

    return {

        "user_id":
        user_id,

        "documents":
        get_all_documents(
            user_id
        )

    }


@router.delete(
    "/documents/{filename}"
)
def remove_document(
    filename: str,
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user[
        "user_id"
    ]

    deleted_chunks = (
        delete_document(
            user_id,
            filename
        )
    )

    user_folder = os.path.join(
        "uploads",
        f"user_{user_id}"
    )

    file_path = os.path.join(
        user_folder,
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

        "user_id":
        user_id,

        "filename":
        filename,

        "chunks_removed":
        deleted_chunks

    }