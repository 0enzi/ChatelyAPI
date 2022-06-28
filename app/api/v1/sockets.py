from typing import Union
from fastapi import Cookie, Depends, Query, WebSocket, status
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi import WebSocket, Depends


from app.utils import get_current_user
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


@router.get("/")
async def get():
    return HTMLResponse(html)

async def get_cookie_or_token(
    websocket: WebSocket,
    session: Union[str, None] = Cookie(default=None),
    token: Union[str, None] = Query(default=None),
):

    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@router.websocket('/chat')
async def websocket(websocket: WebSocket, 
                    token: str = Depends(get_cookie_or_token)):
    await websocket.accept()
    

    data = await websocket.receive_text()
    await websocket.send_text(data)
    await websocket.send_text("Login Successful!")
    await websocket.send_text(f"Query Token value for this session is: {token}")
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message Text was: {data}")
        

