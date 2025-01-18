import asyncio
import websockets

async def echo(websocket):
    await websocket.send("Connection established")
    
    try:
        async for message in websocket:
            await websocket.send(f"Received '{message}'")

            print(f"Received message from client: {message}")
    except websockets.exceptions.ConnectionClosed:
        pass

async def main():
    port = 8765

    print(f"Starting websocket on {port}")

    async with websockets.serve(echo, "localhost", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())