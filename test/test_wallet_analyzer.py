"""
Bộ kiểm thử tự động cho Công cụ Phân tích Dòng tiền Ví On-Chain (Lab 06 - ECO2432)
Bao gồm:
- Ca 1: Luồng bình thường (Normal Inflow/Outflow)
- Ca 2: Trường hợp biên (Failed Transactions & Self-Transfer)
- Ca 3: Kiểm thử gian lận & tấn công (Adversarial Fraud: Address Poisoning / Dust Attack)
"""

import unittest
import sys
import os

# Thêm đường dẫn thư mục gốc lab1-7 vào sys.path để import wallet_analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wallet_analyzer import analyze_cash_flow


class TestWalletAnalyzer(unittest.TestCase):

    def setUp(self):
        self.target_address = "0x6f69897d262d99fc705bf7549631ca1b498d1f14"
        self.partner_address = "0x1111111111111111111111111111111111111111"
        self.merchant_address = "0x2222222222222222222222222222222222222222"
        self.attacker_address = "0x6f69999999999999999999999999999999991f14"

    def test_ca1_normal_flow(self):
        """Ca 1: Kiểm thử luồng giao dịch nạp và rút bình thường (Normal Flow)."""
        txs = [
            # Giao dịch 1: Nhận nạp 2.0 ETH từ bạn học, gas = 0.00042 ETH (người gửi chịu)
            {
                "hash": "0x1111111111111111111111111111111111111111111111111111111111111111",
                "timeStamp": "1720853710",
                "from": self.partner_address,
                "to": self.target_address,
                "value": str(2 * 10**18),  # 2.0 ETH
                "gasUsed": "21000",
                "gasPrice": "20000000000",  # 20 Gwei = 0.00042 ETH
                "isError": "0",
            },
            # Giao dịch 2: Chuyển 0.5 ETH cho đối tác, gasUsed = 21000, gasPrice = 20 Gwei (0.00042 ETH)
            {
                "hash": "0x2222222222222222222222222222222222222222222222222222222222222222",
                "timeStamp": "1722149710",
                "from": self.target_address,
                "to": self.merchant_address,
                "value": str(int(0.5 * 10**18)),  # 0.5 ETH
                "gasUsed": "21000",
                "gasPrice": "20000000000",  # 0.00042 ETH
                "isError": "0",
            },
        ]

        result = analyze_cash_flow(self.target_address, txs)
        self.assertIsNotNone(result)

        # Kiểm tra tổng vào: 2.0 ETH
        self.assertAlmostEqual(result["total_in"], 2.0, places=6)

        # Kiểm tra tổng ra: 0.5 + 0.00042 = 0.50042 ETH (Quy tắc R3)
        self.assertAlmostEqual(result["total_out"], 0.50042, places=6)

        # Kiểm tra số dư lũy kế cuối kỳ: 2.0 - 0.50042 = 1.49958 ETH
        self.assertAlmostEqual(result["final_balance"], 1.49958, places=6)

    def test_ca2_edge_cases_failed_and_self_transfer(self):
        """Ca 2: Kiểm thử trường hợp biên (Giao dịch thất bại và Tự chuyển tiền)."""
        txs = [
            # Giao dịch 1: Lệnh chuyển 5 ETH bị Revert on-chain (isError = '1'), gas = 0.001 ETH
            {
                "hash": "0x3333333333333333333333333333333333333333333333333333333333333333",
                "timeStamp": "1723445710",
                "from": self.target_address,
                "to": self.merchant_address,
                "value": str(5 * 10**18),  # 5 ETH bị revert
                "gasUsed": "50000",
                "gasPrice": "20000000000",  # 0.001 ETH
                "isError": "1",
            },
            # Giao dịch 2: Tự chuyển tiền (Self-transfer) 0 ETH để cancel/speed up lệnh, gas = 0.00042 ETH
            {
                "hash": "0x4444444444444444444444444444444444444444444444444444444444444444",
                "timeStamp": "1724741710",
                "from": self.target_address,
                "to": self.target_address,
                "value": "0",
                "gasUsed": "21000",
                "gasPrice": "20000000000",  # 0.00042 ETH
                "isError": "0",
            },
        ]

        result = analyze_cash_flow(self.target_address, txs)
        self.assertIsNotNone(result)

        # Tiền vào danh nghĩa = 0
        self.assertAlmostEqual(result["total_in"], 0.0, places=6)

        # Quy tắc R4 & R7: Tổng tiền ra phải bằng tổng chi phí gas của 2 lệnh = 0.001 + 0.00042 = 0.00142 ETH
        # Tiền chuyển 5 ETH không bị trừ
        expected_outflow = 0.001 + 0.00042
        self.assertAlmostEqual(result["total_out"], expected_outflow, places=6)
        self.assertAlmostEqual(result["final_balance"], -expected_outflow, places=6)

    def test_ca3_adversarial_address_poisoning(self):
        """Ca 3: Kiểm thử tình huống gian lận - Tấn công đầu độc địa chỉ (Address Poisoning / Dust Attack)."""
        txs = [
            # Kẻ tấn công gửi 0 ETH (hoặc 1 wei) từ một địa chỉ vanity giả mạo giống địa chỉ người dùng
            {
                "hash": "0x5555555555555555555555555555555555555555555555555555555555555555",
                "timeStamp": "1726037710",
                "from": self.attacker_address,
                "to": self.target_address,
                "value": "1",  # 1 wei = 1e-18 ETH
                "gasUsed": "21000",
                "gasPrice": "15000000000",
                "isError": "0",
            }
        ]

        result = analyze_cash_flow(self.target_address, txs)
        self.assertIsNotNone(result)

        # Phải bảo đảm an toàn dữ liệu:
        # 1. Không phát sinh Outflow cho ví mục tiêu (phí gas do kẻ tấn công chịu)
        self.assertAlmostEqual(result["total_out"], 0.0, places=6)

        # 2. Giá trị Inflow chỉ xấp xỉ 1e-18 ETH (không bị làm tròn sai số hoặc tràn số)
        self.assertAlmostEqual(result["total_in"], 1e-18, places=18)
        self.assertAlmostEqual(result["final_balance"], 1e-18, places=18)


if __name__ == "__main__":
    unittest.main()
