import numpy as np
import random

class ReplayMemory:
    def __init__(self, max_size=10000):
        self.buffer = []
        self.max_size = max_size
        self.index = 0

    def add(self, state, action, reward, next_state, done):
        if len(self.buffer) < self.max_size:
            self.buffer.append((state, action, reward, next_state, done))
        # handle overwritting old memories
        else:
            self.buffer[self.index] = (state, action, reward, next_state, done)
            self.index = (self.index + 1) % self.max_size

            # cycle back to 0
            if self.index >= self.max_size:
                self.index = 0

    def sample(self, batch_size):
        samples = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*samples)
        return (np.array(states), 
                actions, 
                np.array(rewards), 
                np.array(next_states), 
                dones)