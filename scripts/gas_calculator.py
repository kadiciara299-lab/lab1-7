"""
Công cụ Tính toán Chi phí Vận hành Thực tế On-chain (Lab 07 - ECO2432)
Tuân thủ công thức Sổ tay thực hành ECO2432:
- 1 Gwei = 10^-9 ETH
- Chi phí 1 giao dịch (ETH) = Gas Used * Gas Price (Gwei) * 10^-9
- Chi phí 1 giao dịch (USD) = Phí (ETH) * Giá ETH (USD)
- Chi phí 1 giao dịch (VNĐ) = Phí (USD) * Tỷ giá USD/VNĐ
"""

def calculate_tx_fee(gas_used: int, gas_price_gwei: float, eth_price_usd: float = 3000.0, exchange_rate_vnd: float = 25400.0):
    fee_eth = gas_used * gas_price_gwei * 1e-9
    fee_usd = fee_eth * eth_price_usd
    fee_vnd = fee_usd * exchange_rate_vnd
    return fee_eth, fee_usd, fee_vnd

def main():
    eth_price = 3000.0
    gas_l1 = 20.0
    gas_l2 = 0.2  # Rẻ hơn 100 lần
    exchange_rate = 25400.0
    num_txs = 1000

    print("=" * 95)
    print(" BÀI TOÁN BƯỚC 2: MÔ HÌNH THẺ TÍCH ĐIỂM CLB SINH VIÊN (1,000 LƯỢT GIAO DỊCH/THÁNG)")
    print(f" Tham số: Giá ETH = ${eth_price:,.2f} | Gas L1 = {gas_l1:.1f} Gwei | Tỷ lệ giảm L2 = 100x")
    print("=" * 95)

    # 1. Ghi biến Storage (~20,000 gas)
    gas_storage = 20000
    fee_eth_l1_s, fee_usd_l1_s, fee_vnd_l1_s = calculate_tx_fee(gas_storage, gas_l1, eth_price, exchange_rate)
    fee_eth_l2_s, fee_usd_l2_s, fee_vnd_l2_s = calculate_tx_fee(gas_storage, gas_l2, eth_price, exchange_rate)

    print("\n[KỊCH BẢN]: Ghi biến Storage đơn giản (~20.000 gas)")
    print(f"{'Chỉ số':<35} | {'Mạng L1 Ethereum':<25} | {'Mạng Layer 2 (100x Rẻ hơn)'}")
    print("-" * 95)
    print(f"{'Phí 1 giao dịch (ETH)':<35} | {fee_eth_l1_s:>21.6f} ETH | {fee_eth_l2_s:>21.6f} ETH")
    print(f"{'Phí 1 giao dịch (USD)':<35} | ${fee_usd_l1_s:>20.4f} USD | ${fee_usd_l2_s:>20.4f} USD")
    print(f"{'Phí 1 giao dịch (VND)':<35} | {fee_vnd_l1_s:>21,.0f} VNĐ | {fee_vnd_l2_s:>21,.0f} VNĐ")
    print("-" * 95)
    print(f"{'Tổng chi phí 1 tháng (ETH)':<35} | {fee_eth_l1_s * num_txs:>21.4f} ETH | {fee_eth_l2_s * num_txs:>21.4f} ETH")
    print(f"{'Tổng chi phí 1 tháng (USD)':<35} | ${fee_usd_l1_s * num_txs:>20.2f} USD | ${fee_usd_l2_s * num_txs:>20.2f} USD")
    print(f"{'Tổng chi phí 1 tháng (VND)':<35} | {fee_vnd_l1_s * num_txs:>21,.0f} VNĐ | {fee_vnd_l2_s * num_txs:>21,.0f} VNĐ")
    print("-" * 95)

    # 2. Mint ERC-20 (~50,000 gas)
    gas_erc20 = 50000
    fee_eth_l1_e, fee_usd_l1_e, fee_vnd_l1_e = calculate_tx_fee(gas_erc20, gas_l1, eth_price, exchange_rate)
    fee_eth_l2_e, fee_usd_l2_e, fee_vnd_l2_e = calculate_tx_fee(gas_erc20, gas_l2, eth_price, exchange_rate)

    print("\n[KỊCH BẢN]: Mint / Chuyển Token ERC-20 (~50.000 gas)")
    print(f"{'Chỉ số':<35} | {'Mạng L1 Ethereum':<25} | {'Mạng Layer 2 (100x Rẻ hơn)'}")
    print("-" * 95)
    print(f"{'Phí 1 giao dịch (ETH)':<35} | {fee_eth_l1_e:>21.6f} ETH | {fee_eth_l2_e:>21.6f} ETH")
    print(f"{'Phí 1 giao dịch (USD)':<35} | ${fee_usd_l1_e:>20.4f} USD | ${fee_usd_l2_e:>20.4f} USD")
    print(f"{'Phí 1 giao dịch (VND)':<35} | {fee_vnd_l1_e:>21,.0f} VNĐ | {fee_vnd_l2_e:>21,.0f} VNĐ")
    print("-" * 95)
    print(f"{'Tổng chi phí 1 tháng (ETH)':<35} | {fee_eth_l1_e * num_txs:>21.4f} ETH | {fee_eth_l2_e * num_txs:>21.4f} ETH")
    print(f"{'Tổng chi phí 1 tháng (USD)':<35} | ${fee_usd_l1_e * num_txs:>20.2f} USD | ${fee_usd_l2_e * num_txs:>20.2f} USD")
    print(f"{'Tổng chi phí 1 tháng (VND)':<35} | {fee_vnd_l1_e * num_txs:>21,.0f} VNĐ | {fee_vnd_l2_e * num_txs:>21,.0f} VNĐ")
    print("-" * 95)

    # 3. Ký quỹ đồ cũ KTX (200 đơn/tháng)
    orders = 200
    gas_per_order = 80000  # 45k fund + 35k confirm
    revenue_monthly = orders * 20.0 * 0.01  # 40 USD
    cost_order_l1_usd = gas_per_order * gas_l1 * 1e-9 * eth_price
    cost_order_l2_usd = gas_per_order * gas_l2 * 1e-9 * eth_price
    cost_month_l1_usd = cost_order_l1_usd * orders
    cost_month_l2_usd = cost_order_l2_usd * orders

    print("\n" + "=" * 95)
    print(" BÀI TOÁN BƯỚC 3: DỰ TOÁN CHI PHÍ DỰ ÁN NHÓM — KÝ QUỸ ĐỒ CŨ KTX (200 ĐƠN HÀNG/THÁNG)")
    print("=" * 95)
    print(f"Tổng số giao dịch ký quỹ / tháng : {orders * 2} giao dịch (2 giao dịch/đơn)")
    print(f"Tổng lượng gas tiêu thụ / tháng  : {orders * gas_per_order:,.0f} gas")
    print("-" * 95)
    print(f"{'Mạng triển khai':<25} | {'Chi phí / đơn (USD)':<20} | {'Tổng chi phí / tháng (USD)':<26} | {'Tổng chi phí (VND)'}")
    print("-" * 95)
    print(f"{'Ethereum Mainnet (L1)':<25} | ${cost_order_l1_usd:>18.2f} | ${cost_month_l1_usd:>24.2f} | {cost_month_l1_usd * exchange_rate:>18,.0f} VNĐ")
    print(f"{'Layer 2 (Arbitrum/Base)':<25} | ${cost_order_l2_usd:>18.4f} | ${cost_month_l2_usd:>24.2f} | {cost_month_l2_usd * exchange_rate:>18,.0f} VNĐ")
    print("-" * 95)
    print(f"Doanh thu dự kiến từ phí nền tảng (1% x $20 x 200 đơn): ${revenue_monthly:.2f} USD/tháng ({revenue_monthly * exchange_rate:,.0f} VNĐ)")
    print(f"-> Lợi nhuận ròng trên L2 sau khi trừ toàn bộ gas Paymaster: ${revenue_monthly - cost_month_l2_usd:.2f} USD/tháng (DƯƠNG, BỀN VỮNG)")
    print(f"-> Lỗ ròng trên L1 Mainnet nếu bao cấp phí: ${revenue_monthly - cost_month_l1_usd:.2f} USD/tháng (PHÁ SẢN HOÀN TOÀN)")

    # 4. Stress Test
    scenarios = [
        ("1. Bear Market", 2000.0, 15.0),
        ("2. Base Case (Hiện hành)", 3000.0, 20.0),
        ("3. Bull Market", 4000.0, 40.0),
        ("4. Extreme Gas Spike", 5000.0, 80.0),
    ]

    print("\n" + "=" * 105)
    print(" BÀI TOÁN BƯỚC 4: PHÂN TÍCH ĐỘ NHẠY & KIỂM THỬ ÁP LỰC THỊ TRƯỜNG (SENSITIVITY & STRESS TEST)")
    print(" Xét tác động lên dự án Ký quỹ KTX (200 đơn/tháng, 80.000 gas/đơn, doanh thu $40.00/tháng)")
    print("=" * 105)
    print(f"{'Kịch bản thị trường':<25} | {'Tham số (ETH / Gas)':<20} | {'Phí/đơn L1':<12} | {'Phí/đơn L2':<12} | {'Lợi nhuận L1/tháng':<18} | {'Lợi nhuận L2/tháng'}")
    print("-" * 105)
    for name, p_eth, g_l1 in scenarios:
        g_l2 = g_l1 / 100.0
        c_l1 = gas_per_order * g_l1 * 1e-9 * p_eth
        c_l2 = gas_per_order * g_l2 * 1e-9 * p_eth
        tot_l1 = c_l1 * orders
        tot_l2 = c_l2 * orders
        profit_l1 = revenue_monthly - tot_l1
        profit_l2 = revenue_monthly - tot_l2
        param_str = f"${p_eth:,.0f} / {g_l1:.0f} Gwei"
        print(f"{name:<25} | {param_str:<20} | ${c_l1:>10.2f} | ${c_l2:>10.4f} | ${profit_l1:>16.2f} USD | ${profit_l2:>16.2f} USD")
    print("-" * 105)


if __name__ == "__main__":
    main()
