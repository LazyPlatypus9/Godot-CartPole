import asyncio
import websockets
import json
import random
from cart_state import CartState
from websocket_message import WebSocketMessage
from global_enum import MessageTypeEnum
from types import SimpleNamespace

DEBUG = True

async def echo(websocket):
    # connection ping
    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.CONFIRMATION.value, str(MessageTypeEnum.CONFIRMATION), None).__dict__))
    
    try:
        async for message in websocket:
            trans_message = WebSocketMessage(**json.loads(message))

            if DEBUG:
                # message ping
                await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.CONFIRMATION.value, str(MessageTypeEnum.CONFIRMATION), None).__dict__))

            if not trans_message.cart_state is None:
                if DEBUG:
                    print(f"message_type: {trans_message.message_type}, content: {trans_message.cart_state['pole_rotation']}")
    
            await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), CartState(0, random.choice([0, 1]))).__dict__, 
                                            default=lambda o: o.__dict__))
    except websockets.exceptions.ConnectionClosed:
        pass

async def main():
    port = 8765

    print(f"Starting websocket on {port}")

    async with websockets.serve(echo, "localhost", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())