import asyncio
import math
import websockets
import json
import random
from replay_memory import TRANSITION, ReplayMemory
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

DEBUG = True
PERFECT_RADIAN = 0.5
BETTER_RADIAN = 1
GOOD_RADIAN = 1.5
FAIR_RADIAN = 2
EFFORT_RADIAN = 3
EPISODES = 1000
CURRENT_EPISODE = 0
STEPS_DONE = 0

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

async def echo(websocket):
    global CURRENT_EPISODE

    gamma = 0.99
    epsilon = 0.9
    epsilon_end = 0.05
    epsilon_decay = 1000
    tau = 0.005
    batch_size = 32
    learning_rate = 1e-4

    # this will be equivalent to the number of properties in the CartState class
    number_of_states = 3

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

    # MSE calculates the difference between the predicted Q-values and targetQ-value, helping
    # the agent minimize errors during training
    loss_fn = nn.MSELoss()

    # stores the memory as a double-ended queue
    memory = ReplayMemory(10000)

    # connection ping
    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.PING.value, str(MessageTypeEnum.PING), None, None).__dict__))
    
    old_cart_state = None
    action = None

    try:
        async for message in websocket:
            if CURRENT_EPISODE > EPISODES:
                break

            trans_message = WebSocketMessage(**json.loads(message))

            if DEBUG:
                print(f"Episode {CURRENT_EPISODE}")
                print(f"{trans_message.message_type}")

            if trans_message.message_type == MessageTypeEnum.DATA.value:
                old_cart_state = CartState(0, 0, 0, trans_message.cart_state)

                action = get_action(old_cart_state, policy_network, epsilon, epsilon_end, epsilon_decay)

                if action == InputsEnum.MOVE_LEFT.value:
                    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), None, CartDriver(0)).__dict__, 
                                                    default=lambda o: o.__dict__))
                else:
                    await websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), None, CartDriver(1)).__dict__, 
                                                    default=lambda o: o.__dict__))
            elif trans_message.message_type == MessageTypeEnum.FEEDBACK.value:
                new_cart_state = CartState(0, 0, 0, trans_message.cart_state)

                reward = get_reward(new_cart_state)

                memory.push(old_cart_state.to_tensor(DEVICE), action, new_cart_state.to_tensor(DEVICE), reward)

                optimize_model(memory, batch_size, policy_network, target_network, gamma, optimizer)

                old_cart_state = new_cart_state

                target_net_state_dict = target_network.state_dict()

                policy_net_state_dict = policy_network.state_dict()

                for key in policy_net_state_dict:
                    target_net_state_dict[key] = policy_net_state_dict[key]*tau + target_net_state_dict[key]*(1-tau)
                
                target_network.load_state_dict(target_net_state_dict)

                CURRENT_EPISODE = CURRENT_EPISODE + 1
    except websockets.exceptions.ConnectionClosed:
        pass

def get_action(cart_state: CartState, policy_network: DQN, epsilon, epsilon_end, epsilon_decay):
    global STEPS_DONE

    sample = random.random()

    epsilon_threshold = epsilon_end + (epsilon - epsilon_end) * math.exp(-1 * STEPS_DONE / epsilon_decay)

    STEPS_DONE = STEPS_DONE + 1

    # the agent needs to be able to pick a random action to gain new experiences
    if sample > epsilon_threshold:
        with torch.no_grad():
            state_tensor = cart_state.to_tensor(DEVICE)
            q_values = policy_network(state_tensor)

            # return the action with the highest q-value
            return torch.tensor([[torch.argmax(q_values).item()]], device=DEVICE, dtype=torch.long)
    else:
        return torch.tensor([[random.choice([0, 1])]], device=DEVICE, dtype=torch.long) 

def optimize_model(memory: ReplayMemory, batch_size, policy_network: DQN, target_network: DQN, gamma, optimizer: optim.Adam):
    if len(memory) < batch_size:
        return
    
    transitions = memory.sample(batch_size)

    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = TRANSITION(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=DEVICE, dtype=torch.bool)
    
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    state_action_values = policy_network(state_batch).gather(1, action_batch)

    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1).values
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    next_state_values = torch.zeros(batch_size, device=DEVICE)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_network(non_final_next_states).max(1).values
    # Compute the expected Q values
    expected_state_action_values = (next_state_values * gamma) + reward_batch

    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_network.parameters(), 100)
    optimizer.step()

def get_reward(cart_state: CartState):
    abs_pole_rotation = abs(cart_state.pole_rotation)

    print(abs_pole_rotation)

    if abs_pole_rotation <= math.radians(10):
        return torch.tensor([[100]], device=DEVICE, dtype=torch.int32)
    elif abs_pole_rotation <= math.radians(44):
        return torch.tensor([[100 * scaling_radian(abs_pole_rotation)]], device=DEVICE, dtype=torch.int32)
    elif abs_pole_rotation <= math.radians(89):
        return torch.tensor([[75 * scaling_radian(abs_pole_rotation)]], device=DEVICE, dtype=torch.int32)
    elif abs_pole_rotation <= math.radians(134):
        return torch.tensor([[50 * scaling_radian(abs_pole_rotation)]], device=DEVICE, dtype=torch.int32)
    elif abs_pole_rotation <= math.radians(179):
        return torch.tensor([[25 * scaling_radian(abs_pole_rotation)]], device=DEVICE, dtype=torch.int32)
    else:
        return torch.tensor([[-100]], device=DEVICE, dtype=torch.int32)

def scaling_radian(value):
    return (math.radians(180) - value) * 0.1

async def main():
    port = 8765

    print(f"Starting websocket on {port}")

    async with websockets.serve(echo, "localhost", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())