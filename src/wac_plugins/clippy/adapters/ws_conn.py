from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

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


# @plugin_route("/control/{client_id}", is_ws=True, name="clippy_plugin")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connection_manager.connect(websocket)
    PluginState.num_clients += 1
    try:
        while True:
            data = await websocket.receive_json()
            # update web app with data
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        PluginState.num_clients -= 1
