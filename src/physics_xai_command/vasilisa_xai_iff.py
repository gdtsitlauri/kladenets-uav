"""
Vasilisa: Explainable AI & IFF
Parses outputs of Ilya and Baba Yaga, provides explanation matrix, checks mock IFF token to prevent friendly fire.
"""
import numpy as np

def parse_ilya_output():
    # Mock: [class, confidence]
    return [ ["target", 0.92], ["friend", 0.12] ]

def parse_baba_output():
    # Mock: [spike_time, detected]
    return [ [12, True], [25, False] ]

def check_iff_token(token):
    # Mock: valid if sum(byte) % 7 == 0
    return sum(token) % 7 == 0

def explanation_matrix(ilya, baba, iff):
    matrix = []
    for det, spike in zip(ilya, baba):
        explanation = {
            "class": det[0],
            "confidence": det[1],
            "spike": spike[1],
            "IFF": iff
        }
        matrix.append(explanation)
    return matrix

if __name__ == "__main__":
    import os
    results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    ilya = parse_ilya_output()
    baba = parse_baba_output()
    iff_token = np.random.randint(0, 256, 8)
    iff_valid = check_iff_token(iff_token)
    matrix = explanation_matrix(ilya, baba, iff_valid)
    with open(os.path.join(results_dir, "vasilisa_xai_iff.txt"), "w") as f:
        f.write(f"IFF Token: {iff_token}\n")
        f.write(f"IFF Valid: {iff_valid}\n")
        f.write("Explanation Matrix:\n")
        for row in matrix:
            f.write(str(row) + "\n")