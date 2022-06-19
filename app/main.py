import uvicorn

from fastapi import FastAPI

from app.api.v1 import api_router
from app.core import settings
from app.models import user, message, inbox
from app.database import session

import sys
sys.dont_write_bytecode = True # annoying pycache remove


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix=settings.API_V1_STR)


user.Base.metadata.create_all(bind=session.engine)
message.Base.metadata.create_all(bind=session.engine)
inbox.Base.metadata.create_all(bind=session.engine)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
