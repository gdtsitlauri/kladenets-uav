"""
Ilya Muromets: Edge AI Extreme Quantization Simulation
Simulates INT8 quantized YOLO-nano/MobileNet-like detection on synthetic data.
Benchmarks FP32 vs INT8 inference on GTX 1650-class hardware.
"""
import torch
import torch.nn as nn
import torch.quantization
import numpy as np
import time

# Lightweight MobileNet-like block
class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.depthwise = nn.Conv2d(in_channels, in_channels, 3, stride, 1, groups=in_channels, bias=False)
        self.pointwise = nn.Conv2d(in_channels, out_channels, 1, 1, 0, bias=False)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        x = self.bn(x)
        return self.relu(x)

class TinyMobileNet(nn.Module):
    def __init__(self, num_classes=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 8, 3, 2, 1, bias=False),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),
            DepthwiseSeparableConv(8, 16, 2),
            DepthwiseSeparableConv(16, 32, 2),
            DepthwiseSeparableConv(32, 64, 2),
            nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Linear(64, num_classes)
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)

def benchmark(model, data, dtype="FP32", device="cuda"):
    model.eval()
    model.to(device)
    with torch.no_grad():
        # Warmup
        for _ in range(10):
            _ = model(data)
        torch.cuda.synchronize()
        t0 = time.time()
        for _ in range(100):
            _ = model(data)
        torch.cuda.synchronize()
        t1 = time.time()
    print(f"{dtype} inference time: {(t1-t0):.4f} s/100 runs")

if __name__ == "__main__":
    import os
    results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    import io
    output = io.StringIO()
    import sys
    old_stdout = sys.stdout
    sys.stdout = output

    # Initialize device, model, and input

    # FP32 benchmark (use GPU if available)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_fp32 = TinyMobileNet(num_classes=2)
    model_fp32.eval()
    x = torch.randn(8, 3, 64, 64, device=device)
    print("Benchmarking FP32 model...")
    benchmark(model_fp32, x, dtype="FP32", device=device)

    # INT8 quantization must run on CPU (QuantizedCPU backend)
    x_cpu = x.cpu()
    try:
        # Quantize to INT8 (static quantization)
        model_int8 = TinyMobileNet(num_classes=2)
        model_int8.eval()
        model_int8.qconfig = torch.quantization.get_default_qconfig('fbgemm')
        torch.quantization.prepare(model_int8, inplace=True)
        # Calibrate with synthetic data
        with torch.no_grad():
            model_int8(x_cpu)
        torch.quantization.convert(model_int8, inplace=True)
        model_int8.to("cpu")
        print("Benchmarking INT8 quantized model (CPU only)...")
        benchmark(model_int8, x_cpu, dtype="INT8", device="cpu")
        int8_size = sum(p.numel() for p in model_int8.parameters()) * 1 / 1024
    except NotImplementedError:
        print("[WARNING] INT8 quantized conv2d not supported on this PyTorch build/platform. Skipping INT8 benchmark.")
        int8_size = 0

    # Model size comparison
    fp32_size = sum(p.numel() for p in model_fp32.parameters()) * 4 / 1024
    print(f"Model size: FP32={fp32_size:.2f} KB, INT8={int8_size:.2f} KB")
    sys.stdout = old_stdout
    with open(os.path.join(results_dir, "ilya_muromets_bench.txt"), "w") as f:
        f.write(output.getvalue())