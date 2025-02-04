import math
import random

import torch
import torch.nn as nn
from cart_state import CartState
from dqn import DQN
from replay_memory import ReplayMemory
from config import CONFIG
import torch.optim as optim


class Model():
    DEVICE = torch.device(
        "cuda" if torch.cuda.is_available() else
        "mps" if torch.backends.mps.is_available() else
        "cpu"
    )
    
    def __init__(self, state_dimensions, action_dimensions):
        self.epsilon_end = CONFIG['training']['epsilon_end']

        self.state_dimensions = state_dimensions
        self.action_dimensions = action_dimensions

        self.policy_network = DQN(self.state_dimensions, self.action_dimensions)

        self.target_network = DQN(self.state_dimensions, self.action_dimensions)
        self.target_network.load_state_dict(self.policy_network.state_dict())

        self.optimizer = optim.Adam(self.policy_network.parameters(), lr=CONFIG['training']['learning_rate'], amsgrad=True)

        self.memory = ReplayMemory(CONFIG['model']['memory_size'])

        self.steps = 0
        self.current_episode = 0
        self.episode_duration = 0
        self.durations = []

        self.current_state: CartState = None
        self.action_taken = None

    def get_action(self, cart_state: CartState):
        sample = random.random()

        epsilon_threshold = self.epsilon_end + (CONFIG['training']['epsilon_start'] - self.epsilon_end) * math.exp(-1 * self.steps / CONFIG['training']['epsilon_decay'])

        # the agent needs to be able to pick a random action to gain new experiences
        if sample > epsilon_threshold:
            with torch.no_grad():
                # return the action with the highest q-value
                return self.policy_network(cart_state.to_tensor(self.DEVICE)).max(1).indices.view(1, 1)
        else:
            return torch.tensor([[random.choice([0, 1])]], device=self.DEVICE, dtype=torch.long) 
        
    def optimize_model(self):
        states, actions, rewards, next_states, dones = self.memory.sample(CONFIG['training']['batch_size'])

        # convert everything to a tensor
        # you need to shrink the dimensions of states, next_state, and rewards so that they are 2D
        # you need to expand the dimsions of actions so that it is 2D
        states = torch.FloatTensor(states).squeeze(1)
        next_states = torch.FloatTensor(next_states).squeeze(1)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards).squeeze(1)
        dones = torch.FloatTensor(dones)

        # get q-values of policy network
        q_values = self.policy_network(states)
        q_values = q_values.gather(1, actions).squeeze(-1)

        # get q-values of target network
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]

        # if done, there is no future reward
        target_q_values = rewards + CONFIG['training']['gamma'] * next_q_values * (1 - dones)

        # calculate loss between current and target Q-values
        loss = nn.MSELoss()(q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss

    def get_reward(self, cart_state: CartState):
        if abs(cart_state.pole_rotation) > math.radians(15):
            return torch.tensor([[-10]], device=self.DEVICE, dtype=torch.int32)
        else:
            return torch.tensor([[1]], device=self.DEVICE, dtype=torch.int32)