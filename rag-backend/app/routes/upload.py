from typing import List
import os

from fastapi import APIRouter, UploadFile, File

from app.services.pdf_loader import extract_pdf_text
from app.services.chunker import chunk_documents
from app.services.embeddings import generate_embeddings
from app.db.chroma import store_embeddings

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdfs(
    files: List[UploadFile] = File(...)
):

    all_chunks = []

    for file in files:

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("\nPDF SAVED:", file.filename)

        pages = extract_pdf_text(file_path)

        print("PAGES RETURNED:", len(pages))

        print("FIRST PAGE DATA:")
        print(pages[0] if pages else "NO PAGES")

        chunks = chunk_documents(
            pages,
            pdf_name=file.filename
        )

        print("TOTAL CHUNKS:", len(chunks))

        if chunks:
            print("FIRST CHUNK:")
            print(chunks[0])

        all_chunks.extend(chunks)

    print("FINAL TOTAL CHUNKS:", len(all_chunks))

    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    print("TEXTS COUNT:", len(texts))

    if not texts:
        return {
            "error": "No text chunks generated"
        }

    embeddings = generate_embeddings(texts)

    print("EMBEDDINGS COUNT:", len(embeddings))

    store_embeddings(
        all_chunks,
        embeddings
    )

    return {
        "message": "PDFs uploaded successfully",
        "total_chunks": len(all_chunks)
    }