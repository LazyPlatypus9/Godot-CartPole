import asyncio
import websockets
import json
import random
from cart_state import CartState
from cart_driver import CartDriver
from websocket_message import WebSocketMessage
from global_enum import MessageTypeEnum
from types import SimpleNamespace

DEBUG = True
TERMINATE_RADIAN = 0.4

async def echo(websocket):
    # connection ping
    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.CONFIRMATION.value, str(MessageTypeEnum.CONFIRMATION), None, None).__dict__))
    
    try:
        async for message in websocket:
            trans_message = WebSocketMessage(**json.loads(message))

            if DEBUG:
                # message ping
                await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.CONFIRMATION.value, str(MessageTypeEnum.CONFIRMATION), None, None).__dict__))

            if not trans_message.cart_state is None:
                if DEBUG:
                    print(f"message_type: {trans_message.message_type}, content: {trans_message.cart_state}")
    
            if trans_message.cart_state['pole_rotation'] < 0 and trans_message.cart_state['pole_rotation'] > -TERMINATE_RADIAN:
                await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), None, CartDriver(0)).__dict__, 
                                            default=lambda o: o.__dict__))
            elif trans_message.cart_state['pole_rotation'] > 0 and trans_message.cart_state['pole_rotation'] < TERMINATE_RADIAN:
                await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), None, CartDriver(1)).__dict__, 
                                            default=lambda o: o.__dict__))
            elif trans_message.cart_state['pole_rotation'] == 0:
                await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), None, CartDriver(random.choice([0, 1]))).__dict__, 
                                                default=lambda o: o.__dict__))
            elif trans_message.cart_state['pole_rotation'] < -TERMINATE_RADIAN or trans_message.cart_state['pole_rotation'] > TERMINATE_RADIAN:
                await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.TERMINATION.value, str(MessageTypeEnum.TERMINATION), None, CartDriver(0)).__dict__, 
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