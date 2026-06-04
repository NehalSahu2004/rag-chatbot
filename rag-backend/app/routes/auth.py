from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import UserRegister
from app.db.sqlite import get_connection
from app.services.auth import (
    hash_password,
    verify_password
)
from app.services.jwt_handler import create_access_token
from app.services.dependencies import get_current_user

router = APIRouter()


@router.post("/signup")
def signup(user: UserRegister):

    conn = get_connection()

    existing_user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (user.email,)
    ).fetchone()

    if existing_user:

        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    conn.execute(
        """
        INSERT INTO users (
            username,
            email,
            password
        )
        VALUES (?, ?, ?)
        """,
        (
            user.username,
            user.email,
            hashed_password
        )
    )

    conn.commit()
    conn.close()

    return {
        "message": "User created successfully"
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    conn = get_connection()

    db_user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (form_data.username,)
    ).fetchone()

    conn.close()

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        db_user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "user_id": db_user["id"],
            "email": db_user["email"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def me(
    current_user=Depends(
        get_current_user
    )
):

    return {
        "user": current_user
    }