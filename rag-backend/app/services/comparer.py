from collections import defaultdict

from app.services.llm import client


def compare_documents(question, docs):

    if not docs:
        return "No relevant documents found."

    grouped_docs = defaultdict(list)

    for doc in docs:

        grouped_docs[
            doc["pdf_name"]
        ].append(
            doc["text"]
        )


    context = ""


    for pdf_name, chunks in grouped_docs.items():

        context += f"""

====================
DOCUMENT NAME:
{pdf_name}
====================

"""

        context += "\n".join(
            chunks[:5]
        )


    prompt = f"""

You are an expert PDF comparison assistant.

Your job is to compare multiple PDF documents.

User Question:
{question}


PDF Content:

{context}


Rules:

1. Always create a markdown comparison table.

Example:

| Feature | Document A | Document B |
|---------|------------|------------|
| Topic | Value | Value |


2. Compare important differences.

3. Mention similarities separately.

4. Mention which document provides more details.

5. Finish with a short conclusion.

6. Use document names in the table columns.

"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )


    return response.choices[0].message.content