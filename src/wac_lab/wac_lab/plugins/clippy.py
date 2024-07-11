from fastapi import WebSocket, WebSocketDisconnect

import reflex as rx
from wac_lab.templates.template import plugin_route
from wac_lab.plugins.plugin import Plugin, PluginManager
from wac_lab.common.external_tools import generate_from_cohere


class PluginState(rx.State):
    running: bool = False
    url: str = ""
    last_action: str = ""
    task: str = ""
    generated_tasks: list[str] = []

    def llm_gen_tasks(self):
        self.generated_tasks = generate_from_cohere()


class ClippyPlugin(Plugin):
    plugin_name: str = "clippy_plugin"
    base_text_val = "nada"

    def home(self) -> rx.Component:
        return rx.box(
            rx.heading("Clippy Plugin"),
            rx.cond(
                PluginState.running,
                self.running_component(),
                self.not_running_component(),
            ),
            margin_top="10%",
        )

    def running_component(self) -> rx.Component:
        return rx.box(
            rx.heading("Clippy Plugin is running"),
            rx.text("Last action: "),
            rx.text(PluginState.last_action),
            rx.text("Current URL: "),
            rx.text(PluginState.url),
        )

    def not_running_component(self) -> rx.Component:
        return rx.box(
            rx.heading("Setup Clippy Plugin"),
            rx.input(placeholder="Enter task", on_change=PluginState.set_task),
            rx.button("Generate Task From LLM", on_click=PluginState.llm_gen_tasks),
            rx.foreach(PluginState.generated_tasks, rx.button),
        )


# this is so it wont instantiate if its rx.state but will otherwise
ClippyPlugin = ClippyPlugin.setup()


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


manager = ConnectionManager()


@plugin_route("/control/{client_id}", is_ws=True, name="clippy_plugin")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
