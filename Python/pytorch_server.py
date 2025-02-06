import asyncio
import math
import websockets
import json
import requests
from config import CONFIG
from model import Model
from replay_memory import ReplayMemory
from dqn import DQN
from cart_state import CartState
from cart_driver import CartDriver
from websocket_message import WebSocketMessage
from global_enum import InputsEnum, MessageTypeEnum
from types import SimpleNamespace
from state_machine import StateMachine

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

import matplotlib.pyplot as plt

DEBUG = True
FLASK_URL = 'http://localhost:5000'

async def echo(websocket):
    # connection ping
    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.SERVER_READY.value, str(MessageTypeEnum.SERVER_READY), None, None).__dict__))
    
    model = Model(4, 2)

    state_machine = StateMachine(model, websocket)

    id = json.loads(requests.get(FLASK_URL + '/data/get_last_row').text)['id'] + 1

    try:
        async for message in websocket:
            trans_message = WebSocketMessage(**json.loads(message))

            await state_machine.on_event(trans_message)

            if model.current_episode > CONFIG['training']['episodes']:
                requests.post(FLASK_URL + '/data/add', json={'id': id, 'durations': model.durations})

                plt.plot(model.durations)
                plt.xlabel("Episode")
                plt.ylabel("Duration")
                plt.title("Training")
                plt.show()

                break
    except websockets.exceptions.ConnectionClosed:
        pass

def scaling_radian(value):
    return (math.radians(180) - value) * 0.1

async def main():
    port = 8765

    print(f"Starting websocket on {port}")

    async with websockets.serve(echo, "localhost", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())