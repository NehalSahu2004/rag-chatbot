import json
import os
from datetime import datetime


CHAT_FILE = "chat_history.json"


def load_data():

    if not os.path.exists(CHAT_FILE):
        return {}

    with open(
        CHAT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_data(data):

    with open(
        CHAT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def save_message(
    session_id,
    role,
    content
):

    data = load_data()

    if session_id not in data:

        data[session_id] = {

            "created":
            str(datetime.now()),

            "title":
            content[:40],

            "messages":
            []
        }

    data[session_id]["messages"].append(

        {
            "role":
            role,

            "content":
            content
        }

    )

    save_data(data)


def get_sessions():

    data = load_data()

    result = []

    for sid, chat in data.items():

        result.append(

            {
                "session_id":
                sid,

                "title":
                chat["title"]
            }

        )

    return result


def get_messages(
    session_id
):

    data = load_data()

    if session_id not in data:

        return []

    return data[
        session_id
    ]["messages"]


# ==========================
# NEW FUNCTIONS
# ==========================

def delete_session(
    session_id
):

    data = load_data()

    if session_id in data:

        del data[
            session_id
        ]

        save_data(data)

        return True

    return False


def clear_history():

    save_data({})

    return True