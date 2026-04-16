"""
Dobrynya Nikitich: Cognitive Radio & EW Resilience
Simulates a Markov Decision Process (MDP) with Q-Learning for dynamic frequency hopping against a jammer.
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

NUM_FREQS = 8  # Number of available frequencies
NUM_EPISODES = 200
STEPS_PER_EPISODE = 50
ALPHA = 0.1  # Learning rate
GAMMA = 0.95  # Discount factor
EPSILON = 0.2  # Exploration rate

# Jammer randomly jams 2 frequencies per step
def jammer_action():
    return np.random.choice(NUM_FREQS, 2, replace=False)

def reward_fn(agent_freq, jammed_freqs):
    return 1.0 if agent_freq not in jammed_freqs else -1.0

Q = np.zeros((NUM_FREQS, NUM_FREQS))  # Q[state, action]
rewards_log = []

for episode in range(NUM_EPISODES):
    state = np.random.randint(NUM_FREQS)  # Start at random frequency
    total_reward = 0
    for step in range(STEPS_PER_EPISODE):
        if np.random.rand() < EPSILON:
            action = np.random.randint(NUM_FREQS)
        else:
            action = np.argmax(Q[state])
        jammed = jammer_action()
        r = reward_fn(action, jammed)
        next_state = action
        Q[state, action] += ALPHA * (r + GAMMA * np.max(Q[next_state]) - Q[state, action])
        state = next_state
        total_reward += r
    rewards_log.append(total_reward)

import os
results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
plt.figure(figsize=(8,4))
plt.plot(rewards_log)
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.title("Dobrynya Nikitich: Q-Learning Frequency Hopping vs Jammer")
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "dobrynya_qlearning_rewards.png"))
plt.close()
np.savetxt(os.path.join(results_dir, "dobrynya_rewards.txt"), rewards_log)