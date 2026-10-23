"""
Công cụ Phân tích Dòng tiền Ví Ethereum (Lab 06 - ECO2432)
Tuân thủ đặc tả SPEC.md và quy ước AGENTS.md
"""

import os
import sys
import time
from datetime import datetime, timezone
import requests
import matplotlib
matplotlib.use("Agg")  # Hỗ trợ render headless / không phụ thuộc GUI
import matplotlib.pyplot as plt


def parse_env_api_key() -> str:
    """Đọc khóa API từ biến môi trường theo quy ước AGENTS.md."""
    api_key = os.getenv("ETHERSCAN_API_KEY")
    if not api_key:
        print("[LỖI BẢO MẬT] Không tìm thấy biến môi trường ETHERSCAN_API_KEY.")
        print("Vui lòng thiết lập biến môi trường trước khi chạy:")
        print("  export ETHERSCAN_API_KEY='khoa_api_cua_ban'")
        sys.exit(1)
    return api_key.strip()


def validate_address(address: str) -> str:
    """Kiểm tra định dạng địa chỉ ví (chuỗi 42 ký tự hex bắt đầu bằng 0x)."""
    address = address.strip()
    if not (
        len(address) == 42
        and address.startswith("0x")
        and all(c in "0123456789abcdefABCDEF" for c in address[2:])
    ):
        print(f"[LỖI ĐẦU VÀO] Địa chỉ ví không hợp lệ: '{address}'.")
        print("Yêu cầu: Chuỗi 42 ký tự hex hợp lệ bắt đầu bằng '0x'.")
        sys.exit(1)
    return address.lower()


def fetch_transactions(address: str, api_key: str, days: int = 90) -> list:
    """
    Lấy toàn bộ giao dịch của ví trong `days` ngày gần nhất qua Etherscan API V2.
    Hỗ trợ phân trang đầy đủ (tránh bẫy thiếu dữ liệu khi >10.000 giao dịch).
    Sắp xếp 'desc' khi gọi API để tối ưu tốc độ và số lượng request.
    """
    now_ts = int(time.time())
    start_ts = now_ts - (days * 24 * 60 * 60)

    all_txs = []
    page = 1
    offset = 10000  # Giới hạn tối đa một trang của Etherscan
    base_url = "https://api.etherscan.io/v2/api"

    print(f"[*] Đang truy vấn dữ liệu on-chain cho ví: {address}")
    print(
        f"[*] Phạm vi phân tích: {days} ngày gần nhất (từ {datetime.fromtimestamp(start_ts, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')})..."
    )

    while True:
        params = {
            "chainid": 1,
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": page,
            "offset": offset,
            "sort": "desc",
            "apikey": api_key,
        }

        try:
            response = requests.get(base_url, params=params, timeout=15)
        except requests.RequestException as e:
            print(f"[LỖI MẠNG] Không thể kết nối tới Etherscan: {e}")
            sys.exit(1)

        # Kiểm tra mã trạng thái HTTP (AGENTS.md)
        if response.status_code != 200:
            print(f"[LỖI HTTP] Mã trạng thái phản hồi: {response.status_code}")
            sys.exit(1)

        data = response.json()
        status = data.get("status")
        message = data.get("message")
        result = data.get("result")

        # Kiểm tra xử lý lỗi API (Ngoại lệ trong SPEC.md)
        if status == "0":
            if message == "No transactions found" or not result:
                break  # Không có giao dịch nào
            else:
                print(f"[LỖI ETHERSCAN API] Mã lỗi: {status} - Thông báo: {result or message}")
                sys.exit(1)

        if not isinstance(result, list):
            print(f"[LỖI ĐỊNH DẠNG] Dữ liệu trả về không phải danh sách: {result}")
            sys.exit(1)

        reached_end_of_window = False
        for tx in result:
            tx_ts = int(tx.get("timeStamp", 0))
            if tx_ts >= start_ts:
                all_txs.append(tx)
            else:
                reached_end_of_window = True
                break

        # Nếu đã vượt quá mốc 90 ngày hoặc hết trang thì dừng
        if reached_end_of_window or len(result) < offset:
            break

        page += 1
        time.sleep(0.25)  # Tránh vượt rate limit của Etherscan Free Tier (5 req/sec)

    # R6: Sắp xếp danh sách giao dịch theo thời gian tăng dần
    sorted_txs = sorted(all_txs, key=lambda x: int(x.get("timeStamp", 0)))
    return sorted_txs


def analyze_cash_flow(address: str, txs: list):
    """
    Phân tích dòng tiền theo đúng 6 quy tắc nghiệp vụ (R1 - R6) trong SPEC.md.
    """
    if not txs:
        print("\n=> [KẾT QUẢ] Vi khong co giao dich trong ky\n")
        return None

    # R6: Đảm bảo thứ tự thời gian tăng dần
    sorted_txs = sorted(txs, key=lambda x: int(x.get("timeStamp", 0)))

    records = []
    total_in = 0.0
    total_out = 0.0
    cumulative_balance = 0.0

    WEI_TO_ETH = 10**18

    for tx in sorted_txs:
        ts = int(tx.get("timeStamp", 0))
        tx_time = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        tx_hash = tx.get("hash", "")
        from_addr = tx.get("from", "").lower()
        to_addr = (tx.get("to") or "").lower()
        value_wei = int(tx.get("value", 0))
        value_eth = value_wei / WEI_TO_ETH  # R5: đổi wei sang ETH

        gas_used = int(tx.get("gasUsed", 0))
        gas_price = int(tx.get("gasPrice", 0))
        fee_wei = gas_used * gas_price
        fee_eth = fee_wei / WEI_TO_ETH  # R5: đổi wei sang ETH

        is_error = tx.get("isError", "0") != "0"

        # Tự chuyển cho chính mình (Self-transfer: from == to == address)
        if from_addr == address and to_addr == address:
            flow_type = "TỰ CHUYỂN"
            fee_paid_eth = fee_eth
            amount_eth = value_eth
            # Tiền chuyển và nhận triệt tiêu lẫn nhau, số dư ví chỉ mất phí gas
            actual_deduction = fee_eth
            cumulative_balance -= actual_deduction
            total_out += actual_deduction

        # R1: to == address -> Dòng tiền VÀO
        elif to_addr == address:
            if not is_error:
                flow_type = "VÀO"
                amount_eth = value_eth
                fee_paid_eth = 0.0  # Người nhận không trả gas
                cumulative_balance += amount_eth
                total_in += amount_eth
            else:
                # Giao dịch gửi đến nhưng thất bại thì số dư ví không thay đổi
                continue

        # R2: from == address -> Dòng tiền RA
        elif from_addr == address:
            flow_type = "RA"
            fee_paid_eth = fee_eth

            # R4: Giao dịch thất bại vẫn bị trừ phí, không trừ value
            if is_error:
                amount_eth = 0.0
                actual_deduction = fee_eth
            else:
                # R3: Số tiền thực trừ = giá trị chuyển + phí giao dịch
                amount_eth = value_eth
                actual_deduction = value_eth + fee_eth

            cumulative_balance -= actual_deduction
            total_out += actual_deduction
        else:
            continue

        records.append({
            "timestamp": ts,
            "time_str": tx_time,
            "hash": tx_hash,
            "flow_type": flow_type,
            "amount_eth": amount_eth,
            "fee_eth": fee_paid_eth,
            "cumulative_balance": cumulative_balance,
            "is_error": is_error,
        })

    return {
        "records": records,
        "total_in": total_in,
        "total_out": total_out,
        "final_balance": cumulative_balance,
    }


def display_report_and_chart(address: str, analysis: dict):
    """Hiển thị bảng dữ liệu tóm tắt và vẽ biểu đồ số dư theo thời gian."""
    if not analysis:
        return

    records = analysis["records"]
    total_in = analysis["total_in"]
    total_out = analysis["total_out"]
    final_balance = analysis["final_balance"]

    print("\n" + "=" * 90)
    print(f"BÁO CÁO DÒNG TIỀN ON-CHAIN: {address}")
    print("=" * 90)
    print(
        f"{'Thời gian (UTC)':<18} | {'Loại':<10} | {'Số tiền (ETH)':<14} | {'Phí Gas (ETH)':<14} | {'Số dư lũy kế':<14} | {'Ghi chú'}"
    )
    print("-" * 90)

    # In tối đa 15 dòng đầu và 5 dòng cuối nếu danh sách quá dài
    display_records = records if len(records) <= 25 else records[:15] + ["..."] + records[-5:]

    for item in display_records:
        if item == "...":
            print(f"{'...':<18} | {'...':<10} | {'...':<14} | {'...':<14} | {'...':<14} | Đã ẩn bớt các dòng giữa...")
            continue
        note = "Thất bại (chỉ trừ gas)" if item["is_error"] else "Thành công"
        print(
            f"{item['time_str']:<18} | {item['flow_type']:<10} | {item['amount_eth']:<14.6f} | {item['fee_eth']:<14.6f} | {item['cumulative_balance']:<14.6f} | {note}"
        )

    print("-" * 90)
    print(
        f"TỔNG HỢP: Tổng vào = {total_in:.6f} ETH  |  Tổng ra = {total_out:.6f} ETH  |  Biến động lũy kế = {final_balance:.6f} ETH"
    )
    print("=" * 90)

    # Vẽ biểu đồ số dư theo thời gian
    timestamps = [datetime.fromtimestamp(r["timestamp"], tz=timezone.utc) for r in records]
    balances = [r["cumulative_balance"] for r in records]

    plt.figure(figsize=(10, 5))
    plt.plot(
        timestamps,
        balances,
        marker="o",
        markersize=3,
        linestyle="-",
        color="#1f77b4",
        label="Số dư biến động lũy kế",
    )
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title(f"Biến động số dư lũy kế ví {address[:10]}... trong 90 ngày", fontsize=12, fontweight="bold")
    plt.xlabel("Thời gian (UTC)", fontsize=10)
    plt.ylabel("ETH lũy kế", fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    chart_file = "balance_chart.png"
    plt.savefig(chart_file, dpi=150)
    print(f"\n[THÀNH CÔNG] Đã xuất biểu đồ ra tệp: '{chart_file}'")


if __name__ == "__main__":
    api_key = parse_env_api_key()
    if len(sys.argv) > 1:
        target_address = sys.argv[1]
    else:
        try:
            target_address = input("Nhập địa chỉ ví Ethereum (0x...): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nĐã hủy thao tác.")
            sys.exit(0)

        if not target_address:
            target_address = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe"
            print(f"[*] Không nhập địa chỉ, sử dụng ví mẫu: {target_address}")

    valid_addr = validate_address(target_address)

    txs = fetch_transactions(valid_addr, api_key, days=90)
    analysis = analyze_cash_flow(valid_addr, txs)
    display_report_and_chart(valid_addr, analysis)
