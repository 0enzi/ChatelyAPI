from typing import Union
from fastapi import Cookie, Depends, HTTPException, Query, Request, WebSocket, status
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from pydantic import BaseModel 
from fastapi.security import OAuth2PasswordBearer


from typing import Optional

from fastapi import WebSocket, Depends, FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.testclient import TestClient
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
from app.utils import get_current_user, oauth2_scheme


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None):
        return await super().__call__(request or websocket)


# oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/api/v1/ws/ws2" + "?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
router = APIRouter()


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('SECRET_KEY')

@router.get("/")
async def get(token: str = Depends(oauth2_scheme)):

    return HTMLResponse(html)

@router.websocket('/chat')
async def websocket(websocket: WebSocket,
    
                    token: str = Depends(oauth2_scheme)):
    await websocket.accept()
    try:
        user = get_current_user(token)
        await websocket.send_text("Login Successful!")
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
            await websocket.send_text("Login Successful!")
            await websocket.send_text(f"You are {get_current_user(token)}")
    except Exception as e:
        await websocket.send_text(e)
        await websocket.close()


class JWTAuth(HTTPBearer):

    async def __call__(self, request: Request=None, websocket: WebSocket=None) -> Optional[HTTPAuthorizationCredentials]:
        request = request or websocket
        if not request:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authenticated"
                )
            return None
        return await super().__call__(request)


@router.websocket('/ws2')
async def socket(
    websocket: WebSocket,
    bearer_token: HTTPAuthorizationCredentials = Depends(JWTAuth())
):
    await websocket.accept()
    await websocket.send_text("hello there")
    await websocket.close()


# def test_socket():
#     client = TestClient(app)
#     with client.websocket_connect("/", headers={'authorization': 'Bearer this works'}) as ws:
#         ws.receive_text()
#         ws.close()