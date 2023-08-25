import asyncio
import websockets


async def read_data():
    url = "ws://30.10.1.1/wsng"
    async with websockets.connect(url, ping_timeout=3600) as websocket:
        while True:
            data = await websocket.recv()
            print(f"Received data: {data}")

asyncio.get_event_loop().run_until_complete(read_data())
