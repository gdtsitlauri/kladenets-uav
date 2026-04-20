"""
Baba Yaga: Neuromorphic Spiking AI (LIF SNN Simulation)
Simulates a Leaky Integrate-and-Fire (LIF) Spiking Neural Network reacting to high-speed targets.
"""
import numpy as np
import matplotlib.pyplot as plt

# LIF neuron parameters
TAU_M = 10.0  # ms
V_REST = -65.0  # mV
V_RESET = -70.0  # mV
V_THRESH = -50.0  # mV
R_M = 10.0  # MOhm
DT = 1.0  # ms

class LIFNeuron:
    def __init__(self, tau_m=TAU_M, v_rest=V_REST, v_reset=V_RESET, v_thresh=V_THRESH, r_m=R_M, dt=DT):
        self.tau_m = tau_m
        self.v_rest = v_rest
        self.v_reset = v_reset
        self.v_thresh = v_thresh
        self.r_m = r_m
        self.dt = dt
        self.v = v_rest
        self.spike_times = []
    def reset(self):
        self.v = self.v_rest
        self.spike_times = []
    def step(self, I, t):
        dv = (-(self.v - self.v_rest) + self.r_m * I) / self.tau_m
        self.v += dv * self.dt
        if self.v >= self.v_thresh:
            self.spike_times.append(t)
            self.v = self.v_reset
        return self.v

def simulate_lif(duration_ms=100, input_current=None):
    neuron = LIFNeuron()
    v_trace = []
    t_axis = np.arange(0, duration_ms, neuron.dt)
    if input_current is None:
        # Simulate a fast target: strong current pulse at t=20ms
        input_current = np.zeros_like(t_axis)
        input_current[20:25] = 3.0  # nA pulse
    for i, t in enumerate(t_axis):
        v = neuron.step(input_current[i], t)
        v_trace.append(v)
    return t_axis, v_trace, neuron.spike_times

if __name__ == "__main__":
    import os
    results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    t, v, spikes = simulate_lif(50)
    plt.figure(figsize=(8,4))
    plt.plot(t, v, label="Membrane Potential (mV)")
    plt.scatter(spikes, [V_THRESH]*len(spikes), color='red', label="Spikes")
    plt.axhline(V_THRESH, color='gray', linestyle='--', label="Threshold")
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Potential (mV)")
    plt.title("LIF Neuron Response to Fast Target")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "baba_yaga_lif_response.png"))
    plt.close()
    np.save(os.path.join(results_dir, "baba_yaga_v_trace.npy"), np.array(v))
    np.save(os.path.join(results_dir, "baba_yaga_spikes.npy"), np.array(spikes))