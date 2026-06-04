from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    print("\n========== AUTH DEBUG ==========")
    print("Received Token:", token)

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("Decoded Payload:", payload)

        user_id = payload.get("user_id")

        if user_id is None:
            print("ERROR: user_id missing in token")
            raise credentials_exception

        print("Authenticated User ID:", user_id)
        print("================================\n")

        return payload

    except JWTError as e:
        print("JWT ERROR:", str(e))
        print("================================\n")
        raise credentials_exception