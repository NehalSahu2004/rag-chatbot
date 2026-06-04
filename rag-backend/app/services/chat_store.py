import json
import os
from datetime import datetime


CHAT_FILE = "chat_history.json"


def load_data():

    if not os.path.exists(
        CHAT_FILE
    ):
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
            indent=4,
            ensure_ascii=False
        )


def save_message(
    user_id,
    session_id,
    role,
    content,
    sources=None
):

    data = load_data()

    user_key = (
        f"user_{user_id}"
    )

    if user_key not in data:

        data[user_key] = {}

    if session_id not in data[user_key]:

        data[user_key][session_id] = {

            "created":
                str(datetime.now()),

            "title":
                content[:40],

            "messages":
                []
        }

    data[user_key][session_id][
        "messages"
    ].append(
        {
            "role":
                role,

            "content":
                content,

            "sources":
                sources or []
        }
    )

    save_data(data)


def get_sessions(
    user_id
):

    data = load_data()

    user_key = (
        f"user_{user_id}"
    )

    if user_key not in data:

        return []

    result = []

    for sid, chat in data[
        user_key
    ].items():

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
    user_id,
    session_id
):

    data = load_data()

    user_key = (
        f"user_{user_id}"
    )

    if user_key not in data:

        return []

    if session_id not in data[
        user_key
    ]:

        return []

    return data[
        user_key
    ][session_id][
        "messages"
    ]


def delete_session(
    user_id,
    session_id
):

    data = load_data()

    user_key = (
        f"user_{user_id}"
    )

    if user_key not in data:

        return False

    if session_id in data[
        user_key
    ]:

        del data[
            user_key
        ][session_id]

        save_data(data)

        return True

    return False


def clear_history(
    user_id
):

    data = load_data()

    user_key = (
        f"user_{user_id}"
    )

    if user_key in data:

        data[user_key] = {}

        save_data(data)

    return True