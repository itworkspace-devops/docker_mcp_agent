from backend.realtime.manager import (
    manager
)

async def publish_finding(
    finding
):

    await manager.broadcast({

        "event":
            "finding",

        "data":
            finding,
    })