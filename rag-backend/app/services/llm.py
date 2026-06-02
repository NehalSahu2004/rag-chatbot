import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


MODEL_NAME = (
    "llama-3.3-70b-versatile"
)



def build_prompt(
    question,
    docs,
    history
):


    context = ""


    for doc in docs:

        context += f"""

SOURCE:
PDF: {doc['pdf_name']}
PAGE: {doc['page']}

CONTENT:
{doc['text']}

"""



    memory_context = ""


    for item in history[-5:]:

        memory_context += f"""

USER:
{item['question']}


ASSISTANT:
{item['answer']}

"""




    prompt = f"""

You are a conversational RAG assistant.

Use:
1. chat history
2. retrieved documents


Rules:

- Answer only from documents
- Use markdown formatting
- Be clear and helpful



====================
CHAT HISTORY
====================

{memory_context}



====================
DOCUMENT CONTEXT
====================

{context}



====================
QUESTION
====================

{question}

"""


    return prompt






def generate_answer(
    question,
    docs,
    history
):


    prompt = build_prompt(
        question,
        docs,
        history
    )



    response = (
        client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]

        )
    )



    return (
        response
        .choices[0]
        .message
        .content
    )







def stream_answer(
    question,
    docs,
    history
):


    prompt = build_prompt(
        question,
        docs,
        history
    )



    stream = (
        client.chat.completions.create(

            model=MODEL_NAME,


            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],


            stream=True

        )
    )



    for chunk in stream:


        token = (
            chunk
            .choices[0]
            .delta
            .content
        )


        if token:

            yield token