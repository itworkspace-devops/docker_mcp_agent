from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.connections = []

    async def connect(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.connections.append(
            websocket
        )

    def disconnect(
        self,
        websocket: WebSocket
    ):

        if websocket in self.connections:

            self.connections.remove(
                websocket
            )

    async def broadcast(
        self,
        message
    ):

        dead_connections = []

        for conn in self.connections:

            try:

                await conn.send_json(
                    message
                )

            except Exception:

                dead_connections.append(
                    conn
                )

        for conn in dead_connections:

            self.disconnect(
                conn
            )


manager = ConnectionManager()