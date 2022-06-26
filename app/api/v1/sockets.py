from typing import Union
from fastapi import Cookie, Depends, Query, WebSocket, status
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from pydantic import BaseModel 


router = APIRouter()

import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('SECRET_KEY')
    