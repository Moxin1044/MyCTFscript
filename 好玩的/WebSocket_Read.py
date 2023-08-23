import asyncio
import websockets

async def read_data():
    url = "ws://30.10.1.1/ws"
    async with websockets.connect(url, ping_timeout=3600) as websocket:
        while True:
            try:
                data = await asyncio.wait_for(websocket.recv(), timeout=10)
                print(f"Received data: {data}")
            except asyncio.TimeoutError:
                print("Timeout: No data received within 10 seconds")
                break

asyncio.get_event_loop().run_until_complete(read_data())
