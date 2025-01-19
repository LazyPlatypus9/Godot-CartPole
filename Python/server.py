import asyncio
import websockets
import json
from websocket_message import WebSocketMessage
from global_enum import MessageTypeEnum
from types import SimpleNamespace

async def echo(websocket):
    # connection ping
    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.CONFIRMATION.value, f"Connection established").__dict__))
    
    try:
        async for message in websocket:
            trans_message = WebSocketMessage(**json.loads(message))

            # message ping
            await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.CONFIRMATION.value, f"Received").__dict__))

            print(f"message_type: {trans_message.message_type}, content: {trans_message.content}")
    except websockets.exceptions.ConnectionClosed:
        pass

async def main():
    port = 8765

    print(f"Starting websocket on {port}")

    async with websockets.serve(echo, "localhost", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())