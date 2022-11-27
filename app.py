import datetime
from time import sleep

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()


def data_gen(delay, num_points):
    for i in range(num_points):
        sleep(delay)
        yield (i)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            ws_data = await websocket.receive_json()
            try:

                delay = float(ws_data["streamRate"])
                num_points = int(ws_data["numPoints"])
                for i in data_gen(delay, num_points):
                    print(i)
                    # await websocket.send_text(str(i))
                    await websocket.send_json(
                        {"temp": i, "timestamp": str(datetime.datetime.now())}
                    )
            except ValueError:
                continue
    except WebSocketDisconnect:
        await websocket.close()
