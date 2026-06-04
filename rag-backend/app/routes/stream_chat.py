import json

from fastapi import (
    APIRouter,
    Depends
)

from fastapi.responses import (
    StreamingResponse
)

from pydantic import BaseModel

from app.services.dependencies import (
    get_current_user
)

from app.services.retriever import (
    retrieve_documents
)

from app.services.reranker import (
    rerank
)

from app.services.llm import (
    stream_answer
)

from app.services.chat_store import (
    save_message
)

from app.memory_store import (
    chat_memory
)

router = APIRouter()


class StreamRequest(BaseModel):

    question: str

    session_id: str = "default"

    compare: bool = False


@router.post("/chat/stream")
def chat_stream(
    request: StreamRequest,
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user["user_id"]

    save_message(
        user_id,
        request.session_id,
        "user",
        request.question
    )

    docs = retrieve_documents(
        request.question,
        user_id
    )

    docs = rerank(
        request.question,
        docs
    )

    memory_key = (
        f"user_{user_id}_"
        f"{request.session_id}"
    )

    if memory_key not in chat_memory:

        chat_memory[
            memory_key
        ] = []

    history = chat_memory[
        memory_key
    ]

    def generate():

        full_answer = ""

        for chunk in stream_answer(
            request.question,
            docs,
            history
        ):

            full_answer += chunk

            yield (
                json.dumps(
                    {
                        "type":
                            "answer",

                        "data":
                            chunk
                    }
                )
                +
                "\n"
            )

        sources = []

        for doc in docs:

            sources.append(
                {
                    "pdf_name":
                        doc.get(
                            "pdf_name",
                            "Unknown PDF"
                        ),

                    "page":
                        doc.get(
                            "page",
                            1
                        ),

                    "text":
                        doc.get(
                            "text",
                            ""
                        )[:400]
                }
            )

        save_message(
            user_id,
            request.session_id,
            "assistant",
            full_answer,
            sources
        )

        history.append(
            {
                "question":
                    request.question,

                "answer":
                    full_answer
            }
        )

        yield (
            json.dumps(
                {
                    "type":
                        "sources",

                    "data":
                        sources
                }
            )
            +
            "\n"
        )

    return StreamingResponse(
        generate(),
        media_type=
        "application/x-ndjson"
    )