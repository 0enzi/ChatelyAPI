from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()


# @app.get("/")
# async def get():
#     return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")