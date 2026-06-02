from fastapi import APIRouter

from app.services.chat_store import (

    get_sessions,

    get_messages,

    delete_session,

    clear_history

)


router = APIRouter()



@router.get("/history")
def history():

    return {

        "chats":
        get_sessions()

    }




@router.get(
    "/history/{session_id}"
)
def chat_messages(
    session_id: str
):

    return {

        "messages":
        get_messages(
            session_id
        )

    }




# ==========================
# DELETE SINGLE CHAT
# ==========================

@router.delete(
    "/history/{session_id}"
)
def remove_chat(
    session_id: str
):

    deleted = delete_session(
        session_id
    )

    return {

        "deleted":
        deleted

    }




# ==========================
# CLEAR ALL HISTORY
# ==========================

@router.delete(
    "/history"
)
def clear_all_history():

    clear_history()

    return {

        "message":
        "History cleared"

    }