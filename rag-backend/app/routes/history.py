from fastapi import (
    APIRouter,
    Depends
)

from app.services.dependencies import (
    get_current_user
)

from app.services.chat_store import (
    get_sessions,
    get_messages,
    delete_session,
    clear_history
)

router = APIRouter()


@router.get("/history")
def history(
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user["user_id"]

    return {

        "user_id":
            user_id,

        "chats":
            get_sessions(user_id)

    }


@router.get("/history/{session_id}")
def chat_messages(
    session_id: str,
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user["user_id"]

    return {

        "user_id":
            user_id,

        "messages":
            get_messages(
                user_id,
                session_id
            )

    }


@router.delete("/history/{session_id}")
def remove_chat(
    session_id: str,
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user["user_id"]

    deleted = delete_session(
        user_id,
        session_id
    )

    return {

        "user_id":
            user_id,

        "deleted":
            deleted

    }


@router.delete("/history")
def clear_all_history(
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user["user_id"]

    clear_history(
        user_id
    )

    return {

        "user_id":
            user_id,

        "message":
            "History cleared"

    }