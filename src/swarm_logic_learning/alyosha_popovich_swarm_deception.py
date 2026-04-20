"""
Alyosha Popovich: Multi-Agent Swarm Deception
Simulates 10 drones in 2D: 3 high-RF decoys, 7 stealth strikers.
Decoys draw simulated SAM fire; strikers avoid detection.
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
N_DRONES = 10
N_DECOYS = 3
N_STRIKERS = 7
N_STEPS = 50
AREA = 100

# Drone roles
roles = np.array(["decoy"]*N_DECOYS + ["striker"]*N_STRIKERS)
np.random.shuffle(roles)

# Initial positions
positions = np.random.rand(N_DRONES, 2) * AREA
trajectories = [positions.copy()]

# Simulated SAM site
sam_pos = np.array([AREA/2, AREA/2])
sam_range = 40

# Decoy: move toward SAM, emit RF
# Striker: move randomly, avoid SAM
for t in range(N_STEPS):
    for i in range(N_DRONES):
        if roles[i] == "decoy":
            direction = sam_pos - positions[i]
            positions[i] += 2 * direction / (np.linalg.norm(direction)+1e-6)
        else:
            # Striker: random walk, avoid SAM
            away = positions[i] - sam_pos
            move = np.random.randn(2) + 1.5 * away / (np.linalg.norm(away)+1e-6)
            positions[i] += move / 3
        # Keep in bounds
        positions[i] = np.clip(positions[i], 0, AREA)
    trajectories.append(positions.copy())

trajectories = np.array(trajectories)

# Simulate SAM fire: targets decoys in range
sam_fires = []
for t in range(N_STEPS):
    fires = []
    for i in range(N_DRONES):
        if roles[i] == "decoy":
            dist = np.linalg.norm(trajectories[t, i] - sam_pos)
            if dist < sam_range:
                fires.append(i)
    sam_fires.append(fires)

# Plot
colors = ["red" if r=="decoy" else "blue" for r in roles]
import os
results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
plt.figure(figsize=(8,8))
for i in range(N_DRONES):
    plt.plot(trajectories[:,i,0], trajectories[:,i,1], color=colors[i], alpha=0.7)
    plt.scatter(trajectories[0,i,0], trajectories[0,i,1], marker="o", color=colors[i], label=f"{roles[i].capitalize()}" if i==0 or i==N_DECOYS else None)
plt.scatter(sam_pos[0], sam_pos[1], marker="*", color="green", s=200, label="SAM Site")
plt.xlim(0, AREA)
plt.ylim(0, AREA)
plt.legend()
plt.title("Alyosha Popovich: Swarm Deception (Decoys vs Strikers)")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "alyosha_swarm_deception.png"))
plt.close()
# Save simulation data
np.save(os.path.join(results_dir, "alyosha_traj.npy"), trajectories)
np.save(os.path.join(results_dir, "alyosha_roles.npy"), roles)
np.save(os.path.join(results_dir, "alyosha_samfires.npy"), np.array(sam_fires, dtype=object))