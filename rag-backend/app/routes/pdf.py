import os

from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from fastapi.responses import (
    FileResponse
)

from app.services.dependencies import (
    get_current_user
)

router = APIRouter()


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)


UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)


@router.get("/pdf/{filename}")
def get_pdf(
    filename: str,
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user["user_id"]

    user_upload_dir = os.path.join(
        UPLOAD_DIR,
        f"user_{user_id}"
    )

    file_path = os.path.join(
        user_upload_dir,
        filename
    )

    if not os.path.exists(
        file_path
    ):

        raise HTTPException(
            status_code=404,
            detail="PDF not found"
        )

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename
    )