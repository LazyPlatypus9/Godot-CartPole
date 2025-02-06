import torch
import datetime

class CartState:
    def __init__(self, pole_rotation, x, velocity, angular_velocity, dict=None):
        if dict is not None:
            for key, value in dict.items():
                setattr(self, key, value)
        else:
            self.pole_rotation = pole_rotation
            self.x = x
            self.velocity = velocity
            self.angular_velocity = angular_velocity
            self.datetime = datetime.datetime.now()

    def to_tensor(self, device):
        return torch.tensor((self.pole_rotation, self.x, self.velocity, self.angular_velocity), dtype=torch.float32, device=device).unsqueeze(0)
        