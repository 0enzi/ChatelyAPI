import sys
sys.dont_write_bytecode = True # annoying pycache remove
import uvicorn

from fastapi import FastAPI

from app.api.v1 import api_router
from app.core import settings
from app.models import user, message, inbox
from app.database import session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix=settings.API_V1_STR)


user.Base.metadata.create_all(bind=session.engine)     
inbox.Base.metadata.create_all(bind=session.engine)

origins = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8080",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:1234",
    "http://localhost:4321"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
