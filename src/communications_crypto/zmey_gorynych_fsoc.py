"""
Zmey Gorynych: Orbital FSOC (Free-Space Optical Communication)
Simulates line-of-sight calculation to a moving LEO satellite for optical comms when RF is jammed.
"""
import numpy as np
import matplotlib.pyplot as plt

# Ground station coordinates (lat, lon, alt)
ground = np.array([45.0, 40.0, 0.0])  # degrees, meters

# Simulate LEO satellite orbit (circular, 400km altitude)
R_EARTH = 6371e3  # meters
ALT = 400e3  # meters
T_ORBIT = 5400  # seconds (90 min)

# 1 min simulation, 1s steps
times = np.arange(0, 60, 1)

# Satellite moves eastward, simple model
sat_lats = ground[0] * np.ones_like(times)
sat_lons = (ground[1] + (360 * times / T_ORBIT)) % 360
sat_alts = ALT * np.ones_like(times)

# Line-of-sight: satellite is visible if elevation > 10 deg
def elevation_angle(gs_lat, gs_lon, gs_alt, sat_lat, sat_lon, sat_alt):
    # Convert to ECEF
    def to_ecef(lat, lon, alt):
        lat, lon = np.deg2rad(lat), np.deg2rad(lon)
        x = (R_EARTH + alt) * np.cos(lat) * np.cos(lon)
        y = (R_EARTH + alt) * np.cos(lat) * np.sin(lon)
        z = (R_EARTH + alt) * np.sin(lat)
        return np.array([x, y, z])
    gs = to_ecef(gs_lat, gs_lon, gs_alt)
    sat = to_ecef(sat_lat, sat_lon, sat_alt)
    diff = sat - gs
    dist = np.linalg.norm(diff)
    up = gs / np.linalg.norm(gs)
    elev = np.arcsin(np.dot(diff, up) / dist)
    return np.rad2deg(elev)

visible = []
for lat, lon, alt in zip(sat_lats, sat_lons, sat_alts):
    elev = elevation_angle(ground[0], ground[1], ground[2], lat, lon, alt)
    visible.append(elev > 10)

import os
results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
plt.figure(figsize=(8,3))
plt.plot(times, visible, drawstyle='steps-post')
plt.xlabel("Time (s)")
plt.ylabel("FSOC Link (1=LOS)")
plt.title("Zmey Gorynych: FSOC Line-of-Sight to LEO Satellite")
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "zmey_fsoc_los.png"))
plt.close()
np.save(os.path.join(results_dir, "zmey_fsoc_visible.npy"), np.array(visible))