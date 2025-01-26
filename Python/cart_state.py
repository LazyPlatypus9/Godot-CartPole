import torch


class CartState:
    def __init__(self, pole_rotation, x, y, dict=None):
        if dict is not None:
            for key, value in dict.items():
                setattr(self, key, value)
        else:
            self.pole_rotation = pole_rotation
            self.x = x
            self.y = y

    def to_tensor(self, device):
        return torch.tensor((self.pole_rotation, self.x, self.y), dtype=torch.float32, device=device).unsqueeze(0)
        