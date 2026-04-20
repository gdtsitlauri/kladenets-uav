"""
Svyatogor: Anti-Spoofing EKF
Simulates an Extended Kalman Filter (EKF) that drops GPS trust when variance spikes, using mock IMU/Optical Flow data.
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
N_STEPS = 50

# State: [x, y, vx, vy]
F = np.array([[1,0,1,0], [0,1,0,1], [0,0,1,0], [0,0,0,1]])
H_gps = np.array([[1,0,0,0], [0,1,0,0]])
H_imu = np.array([[0,0,1,0], [0,0,0,1]])
Q = np.eye(4)*0.01
R_gps = np.eye(2)*2.0
R_imu = np.eye(2)*0.1

x = np.array([0,0,1,1])
P = np.eye(4)

# Mock data: true trajectory, noisy GPS, IMU
true_traj = [x[:2].copy()]
gps_trust = []
for t in range(N_STEPS):
    # True motion
    x_true = F @ x + np.random.randn(4)*0.05
    # GPS: sometimes spoofed (large noise)
    gps_noise = np.random.randn(2)*2
    if 20 < t < 30:
        gps_noise += np.random.randn(2)*10  # spoofing burst
    z_gps = H_gps @ x_true + gps_noise
    # IMU: velocity
    z_imu = H_imu @ x_true + np.random.randn(2)*0.1
    # Predict
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    # GPS update
    y_gps = z_gps - H_gps @ x_pred
    S_gps = H_gps @ P_pred @ H_gps.T + R_gps
    K_gps = P_pred @ H_gps.T @ np.linalg.inv(S_gps)
    x_upd = x_pred + K_gps @ y_gps
    P_upd = (np.eye(4) - K_gps @ H_gps) @ P_pred
    # Drop GPS trust if variance spikes
    if np.trace(S_gps) > 20:
        gps_weight = 0.1
    else:
        gps_weight = 1.0
    gps_trust.append(gps_weight)
    x = gps_weight * x_upd + (1-gps_weight) * x_pred
    P = P_upd
    # IMU update
    y_imu = z_imu - H_imu @ x
    S_imu = H_imu @ P @ H_imu.T + R_imu
    K_imu = P @ H_imu.T @ np.linalg.inv(S_imu)
    x = x + K_imu @ y_imu
    P = (np.eye(4) - K_imu @ H_imu) @ P
    true_traj.append(x[:2].copy())

true_traj = np.array(true_traj)
import os
results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
plt.figure(figsize=(8,4))
plt.plot(true_traj[:,0], true_traj[:,1], label="EKF Estimate")
plt.axvspan(20,30, color='red', alpha=0.2, label="GPS Spoofing")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Svyatogor: EKF Anti-Spoofing with GPS Trust Drop")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "svyatogor_ekf_traj.png"))
plt.close()
plt.figure(figsize=(6,2))
plt.plot(gps_trust)
plt.title("GPS Trust Weight Over Time")
plt.xlabel("Step")
plt.ylabel("GPS Weight")
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "svyatogor_gps_trust.png"))
plt.close()
# Save simulation data
np.save(os.path.join(results_dir, "svyatogor_traj.npy"), true_traj)
np.save(os.path.join(results_dir, "svyatogor_gps.npy"), np.array(gps_trust))