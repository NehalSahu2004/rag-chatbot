import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from pydantic import BaseModel


from app.services.retriever import retrieve_documents
from app.services.reranker import rerank
from app.services.llm import stream_answer

from app.memory_store import chat_memory



router = APIRouter()



class StreamRequest(BaseModel):

    question: str

    session_id: str = "default"

    compare: bool = False





@router.post("/chat/stream")
def chat_stream(
    request: StreamRequest
):


    docs = retrieve_documents(
        request.question
    )


    docs = rerank(
        request.question,
        docs
    )



    if request.session_id not in chat_memory:

        chat_memory[
            request.session_id
        ] = []



    history = chat_memory[
        request.session_id
    ]





    def generate():


        # =====================
        # STREAM TOKENS
        # =====================


        for chunk in stream_answer(
            request.question,
            docs,
            history
        ):


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






        # =====================
        # SEND SOURCES
        # =====================


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
                    )
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