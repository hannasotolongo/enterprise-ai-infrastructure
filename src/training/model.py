import torch
import torch.nn as nn


class AIModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        return self.network(x)


if __name__ == "__main__":
    model = AIModel()

    test_input = torch.randn(1, 10)

    output = model(test_input)

    print("Model created successfully!")
    print("Input shape:", test_input.shape)
