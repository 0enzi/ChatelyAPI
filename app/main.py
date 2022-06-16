import uvicorn

from fastapi import FastAPI

from app.api.v1 import api_router
from app.core import settings
from app.models import product
from app.database import session

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix=settings.API_V1_STR)

product.Base.metadata.create_all(bind=session.engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
