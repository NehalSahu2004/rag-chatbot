import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.upload_test import router as upload_test_router


from app.db.sqlite import init_db
from app.routes.auth import router as auth_router
from app.routes.documents import router as documents_router
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.routes.history import router as history_router
from app.routes.stream_chat import router as stream_router


# ======================
# DATABASE INITIALIZATION
# ======================

init_db()


app = FastAPI(
    title="Multi PDF RAG Assistant"
)


# ======================
# CORS
# ======================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)


# ======================
# STATIC PDF SERVER
# ======================

UPLOAD_DIR = os.path.join(
    os.getcwd(),
    "uploads"
)

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

app.mount(

    "/files",

    StaticFiles(
        directory=UPLOAD_DIR
    ),

    name="files"

)


# ======================
# ROUTES
# ======================

app.include_router(
    upload_router
)

'''app.include_router(
    chat_router
)'''

app.include_router(
    history_router
)

'''app.include_router(
    stream_router
)'''

app.include_router(
    documents_router
)

app.include_router(
    auth_router
)

app.include_router(upload_test_router)

# ======================
# HEALTH CHECK
# ======================

@app.get("/")
def root():

    return {
        "message":
        "RAG Backend Running"
    }


@app.get("/test123")
def test():

    return {
        "status":
        "NEW MAIN FILE RUNNING"
    }