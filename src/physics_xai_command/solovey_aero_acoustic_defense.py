"""
Solovey: Aero/Acoustic Defense
Simulates thermal accumulation from a Directed Energy Weapon (Laser) and Doppler-acoustic detection of FPV interceptors.
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
N_STEPS = 60

# Thermal accumulation (laser)
thermal = [20.0]
laser_on = np.zeros(N_STEPS)
laser_on[10:30] = 1  # Laser fires for 20 steps
for t in range(1, N_STEPS):
    dT = 2.0*laser_on[t] - 0.5*(thermal[-1]-20)  # Heat in, cool to ambient
    thermal.append(thermal[-1] + dT)
thermal = np.array(thermal)

# Acoustic detection (Doppler)
time = np.arange(N_STEPS)
fpv_speed = 30 + 10*np.sin(0.2*time)  # m/s, FPV drone
sound_speed = 343  # m/s
f0 = 2000  # Hz
f_obs = f0 * (sound_speed/(sound_speed-fpv_speed))
# Evasion triggered if Doppler freq > threshold
thresh = 2100
trigger = f_obs > thresh

import os
results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
plt.figure(figsize=(8,3))
plt.subplot(1,2,1)
plt.plot(thermal, label="Thermal (C)")
plt.axhline(40, color='r', linestyle='--', label="Thermal Roll Trigger")
plt.title("Laser Thermal Accumulation")
plt.xlabel("Time")
plt.ylabel("Temp (C)")
plt.legend()
plt.subplot(1,2,2)
plt.plot(f_obs, label="Doppler Freq (Hz)")
plt.axhline(thresh, color='g', linestyle='--', label="Evasion Trigger")
plt.title("FPV Doppler Detection")
plt.xlabel("Time")
plt.ylabel("Freq (Hz)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "solovey_aero_acoustic.png"))
plt.close()
# Save simulation data
np.save(os.path.join(results_dir, "solovey_thermal.npy"), thermal)
np.save(os.path.join(results_dir, "solovey_f_obs.npy"), f_obs)
np.save(os.path.join(results_dir, "solovey_trigger.npy"), trigger)