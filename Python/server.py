import asyncio
import math
import websockets
import json
import random
from replay_memory import ReplayMemory
from dqn import DQN
from cart_state import CartState
from cart_driver import CartDriver
from websocket_message import WebSocketMessage
from global_enum import InputsEnum, MessageTypeEnum
from types import SimpleNamespace

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

import matplotlib.pyplot as plt

DEBUG = True
PERFECT_RADIAN = 0.5
BETTER_RADIAN = 1
GOOD_RADIAN = 1.5
FAIR_RADIAN = 2
EFFORT_RADIAN = 3
EPISODES = 500
CURRENT_EPISODE = 0
GLOBAL_STEP = 0
STEPS_DONE = 0

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

async def echo(websocket):
    global CURRENT_EPISODE
    global GLOBAL_STEP

    gamma = 0.99
    epsilon_start = 0.9
    epsilon_end = 0.05
    epsilon_decay = 200
    batch_size = 100
    learning_rate = 1e-4

    # this will be equivalent to the number of properties in the CartState class
    number_of_states = 4

    # the total number of actions the agent can perform, this would be left and right
    number_of_actions = 2
    
    # this would be the main model used by the agent
    policy_network = DQN(number_of_states, number_of_actions)
    
    # a separate model to act as an antagonist against the main model. It will help to
    # stabalize the main model
    target_network = DQN(number_of_states, number_of_actions)
    target_network.load_state_dict(policy_network.state_dict())

    # Adam optimizer updates the weights based on the gradients calcuated during backpropagation.
    # lr is the learning rate
    optimizer = optim.Adam(policy_network.parameters(), lr=learning_rate, amsgrad=True)

    # stores the memory as a double-ended queue
    memory = ReplayMemory(10000)

    # how often the target policy will update, i.e. once every x steps
    target_policy_update_rate = 1000

    # track how long each individual episode runs so that you can graph it
    episode_duration = 0

    # connection ping
    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.SERVER_READY.value, str(MessageTypeEnum.SERVER_READY), None, None).__dict__))
    
    old_cart_state = None
    action = None
    durations = []
    done = False

    client_ready = False

    try:
        async for message in websocket:
            trans_message = WebSocketMessage(**json.loads(message))

            if DEBUG:
                print(f"{trans_message.message_type}, Episode: {CURRENT_EPISODE}, Global Step: {GLOBAL_STEP}")

            if trans_message.message_type == MessageTypeEnum.CLIENT_READY.value and not client_ready:
                client_ready = True

            if not client_ready:
                if DEBUG:
                    print(f"Ignoring: {trans_message.message_type}")
                
                continue

            if CURRENT_EPISODE > EPISODES:
                plt.plot(durations)
                plt.xlabel("Episode")  # add X-axis label
                plt.ylabel("Duration")  # add Y-axis label
                plt.title("Training")  # add title
                plt.show()

                break

            if trans_message.message_type == MessageTypeEnum.DATA.value:
                old_cart_state = CartState(0, 0, 0, 0, trans_message.cart_state)

                action = get_action(old_cart_state, policy_network, epsilon_start, epsilon_end, epsilon_decay)

                if action == InputsEnum.MOVE_LEFT.value:
                    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), None, CartDriver(0)).__dict__, 
                                                    default=lambda o: o.__dict__))
                else:
                    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), None, CartDriver(1)).__dict__, 
                                                    default=lambda o: o.__dict__))
            elif trans_message.message_type == MessageTypeEnum.FEEDBACK.value:
                new_cart_state = CartState(0, 0, 0, 0, trans_message.cart_state)

                reward = get_reward(new_cart_state)

                if reward < 0:
                    done = True

                memory.add(old_cart_state.to_tensor(DEVICE), action, reward, new_cart_state.to_tensor(DEVICE), done)

                if len(memory.buffer) > batch_size:
                    loss = optimize_model(batch_size, policy_network, target_network, memory, gamma, optimizer)
                    
                    if (DEBUG):
                        print(f"Loss: {loss}")

                    # Update target network periodically
                    if GLOBAL_STEP % target_policy_update_rate == 0:
                        target_network.load_state_dict(policy_network.state_dict())

                if DEBUG:
                    print(f"Old state: {old_cart_state.__dict__}")
                    print(f"New state: {new_cart_state.__dict__}")

                episode_duration = episode_duration + 1
                GLOBAL_STEP = GLOBAL_STEP + 1

                if done:
                    old_cart_state = None
                    action = None
                    done = False
                    CURRENT_EPISODE = CURRENT_EPISODE + 1
                    durations.append(episode_duration)
                    episode_duration = 0
                    client_ready = False

                    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.TERMINATION.value, str(MessageTypeEnum.TERMINATION), None, CartDriver(0)).__dict__, 
                                                    default=lambda o: o.__dict__))
                    
                    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.SERVER_READY.value, str(MessageTypeEnum.SERVER_READY), None, None).__dict__))
    except websockets.exceptions.ConnectionClosed:
        pass

def get_action(cart_state: CartState, policy_network: DQN, epsilon_start, epsilon_end, epsilon_decay):
    global STEPS_DONE

    sample = random.random()

    epsilon_threshold = epsilon_end + (epsilon_start - epsilon_end) * math.exp(-1 * STEPS_DONE / epsilon_decay)

    STEPS_DONE = STEPS_DONE + 1

    # the agent needs to be able to pick a random action to gain new experiences
    if sample > epsilon_threshold:
        with torch.no_grad():
            # return the action with the highest q-value
            return policy_network(cart_state.to_tensor(DEVICE)).max(1).indices.view(1, 1)
    else:
        return torch.tensor([[random.choice([0, 1])]], device=DEVICE, dtype=torch.long) 

def optimize_model(batch_size, policy_network: DQN, target_network: DQN, memory: ReplayMemory, gamma, optimizer):
    states, actions, rewards, next_states, dones = memory.sample(batch_size)

    # convert everything to a tensor
    # you need to shrink the dimensions of states, next_state, and rewards so that they are 2D
    # you need to expand the dimsions of actions so that it is 2D
    states = torch.FloatTensor(states).squeeze(1)
    next_states = torch.FloatTensor(next_states).squeeze(1)
    actions = torch.LongTensor(actions).unsqueeze(1)
    rewards = torch.FloatTensor(rewards).squeeze(1)
    dones = torch.FloatTensor(dones)

    # get q-values of policy network
    q_values = policy_network(states)
    q_values = q_values.gather(1, actions).squeeze(-1)

    # get q-values of target network
    with torch.no_grad():
        next_q_values = target_network(next_states).max(1)[0]

    # if done, there is no future reward
    target_q_values = rewards + gamma * next_q_values * (1 - dones)

    # calculate loss between current and target Q-values
    loss = nn.MSELoss()(q_values, target_q_values)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss

def get_reward(cart_state: CartState):
    if abs(cart_state.pole_rotation) > math.radians(15):
        return torch.tensor([[-10]], device=DEVICE, dtype=torch.int32)
    else:
        return torch.tensor([[1]], device=DEVICE, dtype=torch.int32)

def scaling_radian(value):
    return (math.radians(180) - value) * 0.1

async def main():
    port = 8765

    print(f"Starting websocket on {port}")

    async with websockets.serve(echo, "localhost", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())