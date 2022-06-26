from typing import Union
from fastapi import Cookie, Depends, Query, WebSocket, status
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from pydantic import BaseModel 


import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
from app.oauth2 import oauth2_scheme, get_current_user
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Authorize</title>
    </head>
    <body>
        <h1>WebSocket Authorize</h1>
        <p>Token:</p>
        <textarea id="token" rows="4" cols="50"></textarea><br><br>
        <button onclick="websocketfun()">Send</button>
        <ul id='messages'>
        </ul>
        <script>
            const websocketfun = () => {
                let token = document.getElementById("token").value
                let ws = new WebSocket(`ws://192.168.18.202:8000/ws?token=${token}`)
                ws.onmessage = (event) => {
                    let messages = document.getElementById('messages')
                    let message = document.createElement('li')
                    let content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                }
            }
        </script>
    </body>
</html>
"""
router = APIRouter()


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('SECRET_KEY')

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket('/ws')
async def websocket(websocket: WebSocket, token: str = Depends(oauth2_scheme)):
    # await websocket.accept()
    # try:
    #     Authorize.jwt_required("websocket",token=token)
    #     # Authorize.jwt_optional("websocket",token=token)
    #     # Authorize.jwt_refresh_token_required("websocket",token=token)
    #     # Authorize.fresh_jwt_required("websocket",token=token)
    #     await websocket.send_text("Successfully Login!")
    #     decoded_token = Authorize.get_raw_jwt(token)
    #     await websocket.send_text(f"Here your decoded token: {decoded_token}")
    # except AuthJWTException as err:
    #     await websocket.send_text(err.message)
    #     await websocket.close()
    print(token, get_current_user(token))