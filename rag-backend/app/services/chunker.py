from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(pages, pdf_name):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = []

    chunk_id = 0

    for page in pages:

        page_num = page["page"]
        page_text = page["text"]

        if not page_text.strip():
            continue

        split_texts = splitter.split_text(page_text)

        for text in split_texts:

            chunks.append({
                "text": text,
                "pdf_name": pdf_name,
                "page": page_num,
                "chunk_id": chunk_id
            })

            chunk_id += 1

    return chunks