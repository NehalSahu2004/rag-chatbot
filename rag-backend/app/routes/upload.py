from typing import List
import os

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from app.services.dependencies import (
    get_current_user
)

from app.services.pdf_loader import (
    extract_pdf_text
)

from app.services.chunker import (
    chunk_documents
)

from app.services.embeddings import (
    generate_embeddings
)

from app.db.chroma import (
    store_embeddings
)

router = APIRouter()


@router.post("/upload")
async def upload_pdfs(
    files: List[UploadFile] = File(...),
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user["user_id"]

    upload_dir = os.path.join(
        "uploads",
        f"user_{user_id}"
    )

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    all_chunks = []

    uploaded_files = []

    for file in files:

        file_path = os.path.join(
            upload_dir,
            file.filename
        )

        with open(file_path, "wb") as f:

            f.write(
                await file.read()
            )

        uploaded_files.append(
            file.filename
        )

        print(
            f"\nPDF SAVED: {file.filename}"
        )

        print(
            f"USER ID: {user_id}"
        )

        pages = extract_pdf_text(
            file_path
        )

        print(
            f"PAGES RETURNED: {len(pages)}"
        )

        chunks = chunk_documents(
            pages,
            pdf_name=file.filename
        )

        print(
            f"TOTAL CHUNKS: {len(chunks)}"
        )

        all_chunks.extend(
            chunks
        )

    if not all_chunks:

        return {
            "error":
            "No text chunks generated"
        }

    texts = [

        chunk["text"]

        for chunk in all_chunks

    ]

    embeddings = generate_embeddings(
        texts
    )

    store_embeddings(
        user_id,
        all_chunks,
        embeddings
    )

    return {

        "message":
        "PDFs uploaded successfully",

        "user_id":
        user_id,

        "files_uploaded":
        len(uploaded_files),

        "filenames":
        uploaded_files,

        "total_chunks":
        len(all_chunks)

    }