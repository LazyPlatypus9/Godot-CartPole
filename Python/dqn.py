import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self, input_dimension, output_dimension):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dimension, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dimension)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x