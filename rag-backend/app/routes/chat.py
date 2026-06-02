from fastapi import APIRouter
from pydantic import BaseModel


from app.services.retriever import retrieve_documents
from app.services.reranker import rerank
from app.services.llm import generate_answer
from app.services.comparer import compare_documents


from app.services.chat_store import save_message


from app.memory_store import chat_memory



router = APIRouter()



class ChatRequest(BaseModel):

    question: str

    compare: bool = False

    session_id: str = "default"




@router.post("/chat")
def chat(
    request: ChatRequest
):


    # =========================
    # SAVE USER MESSAGE
    # =========================

    save_message(
        request.session_id,
        "user",
        request.question
    )



    # =========================
    # RETRIEVE DOCUMENTS
    # =========================

    docs = retrieve_documents(
        request.question
    )


    docs = rerank(
        request.question,
        docs
    )



    # =========================
    # MEMORY
    # =========================

    if request.session_id not in chat_memory:

        chat_memory[
            request.session_id
        ] = []



    history = chat_memory[
        request.session_id
    ]



    # =========================
    # GENERATE RESPONSE
    # =========================


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




    # =========================
    # SAVE ASSISTANT MESSAGE
    # =========================


    save_message(
        request.session_id,
        "assistant",
        answer
    )



    # old memory system
    history.append(
        {
            "question":
                request.question,

            "answer":
                answer
        }
    )




    # =========================
    # RESPONSE
    # =========================


    return {

        "question":
            request.question,


        "answer":
            answer,


        "sources":
            docs
    }