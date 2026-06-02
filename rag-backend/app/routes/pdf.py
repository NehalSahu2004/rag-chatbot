import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse


router = APIRouter()



# =========================
# FIXED UPLOAD PATH
# =========================


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
    filename: str
):


    print(
        "PDF REQUEST:",
        filename
    )


    print(
        "SEARCHING:",
        UPLOAD_DIR
    )



    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )



    print(
        "FULL PATH:",
        file_path
    )



    if not os.path.exists(
        file_path
    ):


        print(
            "PDF NOT FOUND"
        )


        print(
            "AVAILABLE FILES:",
            os.listdir(
                UPLOAD_DIR
            )
        )



        raise HTTPException(

            status_code=404,

            detail=
            "PDF not found"

        )




    return FileResponse(

        file_path,

        media_type=
        "application/pdf",

        filename=
        filename

    )