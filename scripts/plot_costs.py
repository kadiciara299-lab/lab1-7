"""
Vẽ Biểu đồ So sánh Chi phí Vận hành L1 vs L2 (Lab 07 - ECO2432)
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def generate_comparison_chart():
    os.makedirs("evidence/lab-07", exist_ok=True)

    categories = [
        "Thẻ tích điểm CLB\n(Storage ~20k gas)",
        "Thẻ tích điểm CLB\n(ERC-20 ~50k gas)",
        "Ký quỹ đồ cũ KTX\n(200 đơn ~80k gas)"
    ]

    # Chi phí tháng USD
    costs_l1 = [1200.0, 3000.0, 960.0]
    costs_l2 = [12.0, 30.0, 9.6]

    x = np.arange(len(categories))
    width = 0.35

    plt.figure(figsize=(10, 6), dpi=150)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # Bar chart
    bars_l1 = plt.bar(x - width/2, costs_l1, width, label="Ethereum L1 Mainnet (20 Gwei)", color="#ef4444", alpha=0.9)
    bars_l2 = plt.bar(x + width/2, costs_l2, width, label="Layer 2 Arbitrum / Base (0.2 Gwei)", color="#10b981", alpha=0.9)

    plt.ylabel("Chi phí vận hành hàng tháng (USD)", fontsize=11, fontweight="bold", labelpad=10)
    plt.title("SO SÁNH CHI PHÍ VẬN HÀNH THỰC TẾ: ETHEREUM L1 VS LAYER 2 (LAB 07)\n(Giá ETH = $3,000 USD | Giả định 100x rẻ hơn trên Layer 2)", fontsize=12, fontweight="bold", pad=15)
    plt.xticks(x, categories, fontsize=10, fontweight="bold")
    plt.yscale("log")  # Thang đo logarit do chênh lệch 100 lần
    plt.grid(True, linestyle="--", alpha=0.5, which="both")
    plt.legend(fontsize=10, loc="upper right")

    # Annotations on bars
    for bar in bars_l1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval * 1.15, f"${yval:,.0f}/tháng\n({yval*25400/1e6:.1f} tr VNĐ)", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#881337")

    for bar in bars_l2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval * 1.15, f"${yval:,.1f}/tháng\n({yval*25400/1e3:.0f} k VNĐ)", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#065f46")

    plt.tight_layout()

    chart_file = "cost_comparison.png"
    plt.savefig(chart_file)
    plt.savefig("evidence/lab-07/cost_comparison.png")
    print(f"[THÀNH CÔNG] Đã lưu biểu đồ so sánh chi phí ra '{chart_file}' và 'evidence/lab-07/{chart_file}'.")

if __name__ == "__main__":
    generate_comparison_chart()
