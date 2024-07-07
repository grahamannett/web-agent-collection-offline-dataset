import unittest
from wac_lab.plugins import clippy_controller


class TestPlugins(unittest.IsolatedAsyncioTestCase):
    async def test_clippy(self):
        import asyncio
        from websockets.sync.client import connect

        backend_route = "ws://localhost:8000/ws/clippy"

        def send():
            with connect(backend_route) as websocket:
                websocket.send("Hello world!")
                message = websocket.recv()
                return message


if __name__ == "__main__":
    unittest.main()
