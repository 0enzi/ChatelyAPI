from typing import List, Union
from urllib.request import Request
from fastapi import Cookie, Depends, Query, WebSocket, WebSocketDisconnect, status
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi import WebSocket, Depends
from fastapi.templating import Jinja2Templates


from app.utils import get_current_user, oauth2_scheme

templates = Jinja2Templates(directory="templates")
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Chately [WebSockets Lab]</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Contact ID: <input type="text" id="itemId" autocomplete="off" value="Ali"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value=""/></label>
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
                ws = new WebSocket("ws://localhost:8000/api/v1/ws/chat" + "?token=" + token.value);
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

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()



@router.get("/")
async def get(current_user : str = Depends(get_current_user)):
    # print(get_current_user(token))
    return {'user': current_user}

async def get_cookie_or_token(
    websocket: WebSocket,
    session: Union[str, None] = Cookie(default=None),
    token: Union[str, None] = Query(default=None),
):

    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@router.websocket('/chat/{client_id}')
async def websocket(websocket: WebSocket,   
                    client_id: int):
    
    await manager.connect(websocket)
    await websocket.send_text(f"Connected Successfully!!")
    await websocket.send_text(f"Access Token for this session will be {token}")
    try:
        while True:
           data = await websocket.receive_text()
           await manager.send_personal_message(f"You wrote: {data}", websocket)
           await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")