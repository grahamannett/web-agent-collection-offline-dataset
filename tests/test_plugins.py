import unittest
from threading import Thread

from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from wac_plugins.clippy.clippy import ConnectionManager, websocket_endpoint


app = FastAPI()
app.websocket_route("/ws/{client_id}")(websocket_endpoint)


class TestSendPersonalMessage(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.server_thread = Thread(target=cls.client.__enter__)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.client.__exit__(None, None, None)
        cls.server_thread.join()

    async def test_send_personal_message(self):
        async with self.client.websocket_connect("/ws/1") as websocket:
            manager = ConnectionManager()
            test_websocket = WebSocket(websocket=websocket, client=None)
            await manager.connect(test_websocket)
            message, url = "click(100, 500)", "https://url.com"
            await manager.send_personal_message(message, test_websocket)
            data = await websocket.receive_text()
            self.assertIn(message, data)

    async def asyncTearDown(self):
        # Close any active connections to clean up after tests
        for connection in ConnectionManager().active_connections:
            await connection.close()


if __name__ == "__main__":
    unittest.main()
