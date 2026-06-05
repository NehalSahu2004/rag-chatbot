from fastapi import APIRouter, Depends
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
    generate_answer
)

from app.services.comparer import (
    compare_documents
)

from app.services.chat_store import (
    save_message
)

from app.memory_store import (
    chat_memory
)

router = APIRouter()


class ChatRequest(BaseModel):

    question: str

    compare: bool = False

    session_id: str = "default"


@router.post("/chat")
def chat(
    request: ChatRequest,
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user["user_id"]

    memory_key = (
        f"user_{user_id}_"
        f"{request.session_id}"
    )

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

    if memory_key not in chat_memory:

        chat_memory[
            memory_key
        ] = []

    history = chat_memory[
        memory_key
    ]

    if request.compare:

        answer = compare_documents(
            request.question,
            docs
        )

    else:

        answer = generate_answer(
            request.question,
            docs,
            history
        )

    save_message(
        user_id,
        request.session_id,
        "assistant",
        answer
    )

    history.append(
        {
            "question":
                request.question,

            "answer":
                answer
        }
    )

    return {

        "user_id":
            user_id,

        "session_id":
            request.session_id,

        "question":
            request.question,

        "answer":
            answer,

        "sources":
            docs
    }