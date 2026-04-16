"""
Knyaz Vladimir: Unified C2 Dashboard
Streamlit app displaying VRAM savings, EW hopping, Swarm map, and Threat alerts from all modules.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")
st.title("Knyaz Vladimir: Unified C2 Dashboard")

# VRAM savings (Ilya Muromets)
st.header("Edge AI VRAM Savings")
st.write("INT8 quantization reduces VRAM by ~75% vs FP32.")
st.progress(75)

# EW hopping (Dobrynya Nikitich)

# Set results directory robustly
results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")

st.header("EW Frequency Hopping Success")
rewards_path = os.path.join(results_dir, 'dobrynya_rewards.txt')
if os.path.exists(rewards_path):
    rewards = np.loadtxt(rewards_path)
else:
    rewards = np.random.normal(30,5,200)
st.line_chart(rewards)

# Swarm map (Alyosha Popovich)
st.header("Swarm Map: Decoys & Strikers")
traj_path = os.path.join(results_dir, 'alyosha_traj.npy')
roles_path = os.path.join(results_dir, 'alyosha_roles.npy')
try:
    traj = np.load(traj_path)
    roles = np.load(roles_path)
except:
    traj = np.random.rand(51,10,2)*100
    roles = np.array(["decoy"]*3 + ["striker"]*7)
    np.random.shuffle(roles)
fig, ax = plt.subplots(figsize=(5,5))
colors = ["red" if r=="decoy" else "blue" for r in roles]
for i in range(10):
    ax.plot(traj[:,i,0], traj[:,i,1], color=colors[i], alpha=0.7)
    ax.scatter(traj[0,i,0], traj[0,i,1], color=colors[i])
ax.set_xlim(0,100)
ax.set_ylim(0,100)
st.pyplot(fig)

# Threat alerts (Solovey, Svyatogor, Vasilisa)
st.header("Threat Alerts & XAI")

thermal_path = os.path.join(results_dir, 'solovey_thermal.npy')
gps_trust_path = os.path.join(results_dir, 'svyatogor_gps.npy')
if os.path.exists(thermal_path):
    thermal = np.load(thermal_path)
else:
    thermal = np.random.normal(25,5,60)
if os.path.exists(gps_trust_path):
    gps_trust = np.load(gps_trust_path)
else:
    gps_trust = np.clip(np.random.normal(1,0.2,50),0,1)
iff_valid = np.random.choice([True,False])
st.metric("Thermal (C)", f"{thermal[-1]:.1f}", delta=None)
st.metric("GPS Trust", f"{gps_trust[-1]:.2f}", delta=None)
st.metric("IFF Token Valid", iff_valid)

st.success("Dashboard running with synthetic/mock data.")