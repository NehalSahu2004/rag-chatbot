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

You are a professional Multi-PDF RAG Assistant.

You must answer ONLY from the provided documents.

====================================================
RULES
====================================================

1. Never invent information.

2. If information is not present in the documents, say:

   "The documents do not contain enough information."

3. Always use markdown formatting.

4. Cite supporting sources whenever possible.

5. Be concise but complete.

====================================================
COMPARISON RULES
====================================================

If the user asks to:

- compare
- difference
- differences
- contrast
- vs
- versus

AND information comes from multiple PDFs,

THEN create a MARKDOWN TABLE.

Example:

| Policy | Employee Handbook | HR Policy |
|----------|----------|----------|
| Annual Leave | 15 Days | 20 Days |
| Sick Leave | 5 Days | 10 Days |

After the table provide:

## Key Findings

- Finding 1
- Finding 2
- Finding 3

Do NOT write long paragraphs before the table.

The table must appear first.

====================================================
CHAT HISTORY
====================================================

{memory_context}

====================================================
DOCUMENT CONTEXT
====================================================

{context}

====================================================
QUESTION
====================================================

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
                    "role": "user",
                    "content": prompt
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
                    "role": "user",
                    "content": prompt
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