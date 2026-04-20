"""
Zhar-ptitsa: Federated Mesh Learning
Simulates 3 agents updating a tiny local PyTorch model and exchanging only weight deltas (Federated Averaging).
No central server; mesh communication.
"""
import torch
import torch.nn as nn
import numpy as np

# Tiny model: 1-layer perceptron
class TinyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(4, 2)
    def forward(self, x):
        return self.fc(x)

def get_weights(model):
    return [p.data.clone() for p in model.parameters()]

def set_weights(model, weights):
    for p, w in zip(model.parameters(), weights):
        p.data.copy_(w)

def average_weights(weights_list):
    avg = []
    for params in zip(*weights_list):
        avg.append(sum(params)/len(params))
    return avg

np.random.seed(42)
torch.manual_seed(42)
N_AGENTS = 3
N_ROUNDS = 5

# Each agent has its own model and data
data = [torch.randn(10,4) for _ in range(N_AGENTS)]
targets = [torch.randint(0,2,(10,)) for _ in range(N_AGENTS)]
models = [TinyNet() for _ in range(N_AGENTS)]
optims = [torch.optim.SGD(m.parameters(), lr=0.1) for m in models]

for rnd in range(N_ROUNDS):
    # Local update
    for i in range(N_AGENTS):
        optims[i].zero_grad()
        out = models[i](data[i])
        loss = nn.CrossEntropyLoss()(out, targets[i])
        loss.backward()
        optims[i].step()
    # Exchange weight deltas (mesh)
    weights = [get_weights(m) for m in models]
    avg = average_weights(weights)
    for m in models:
        set_weights(m, avg)

# Save final weights
import os
results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
with open(os.path.join(results_dir, "zhar_ptitsa_final_weights.txt"), "w") as f:
    for i, m in enumerate(models):
        f.write(f"Agent {i} weights:\n{[p.data.numpy() for p in m.parameters()]}\n")