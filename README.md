# HỒ SƠ THỰC HÀNH CÁ NHÂN (LAB 1 — LAB 7)
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Trường Đại học Kinh tế - Đại học Huế (HCE)** — Khoa Hệ thống Thông tin Kinh tế  
**Sinh viên thực hiện:** Nguyễn Nguyên Phương  
**Địa chỉ ví cá nhân (Sepolia):** [`0x6f69897D262D99Fc705bF7549631ca1b498d1F14`](https://sepolia.etherscan.io/address/0x6f69897D262D99Fc705bF7549631ca1b498d1F14)  
**Tệp quy ước AI:** [`AGENTS.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/AGENTS.md)  
**Nhật ký làm việc với AI:** [`AI_JOURNAL.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/AI_JOURNAL.md) *(đồng bộ cùng [`AJ_JOURNAL.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/AJ_JOURNAL.md))*  

---

## 🧭 BẢN ĐỒ TIẾN ĐỘ THỰC HÀNH (LAB 1 ĐẾN LAB 7)

Kho mã nguồn này lưu trữ toàn bộ các sản phẩm thực hành, báo cáo phân tích, mã nguồn và chứng từ on-chain trong giai đoạn nền tảng (Tuần 1 – Tuần 3) trước khi bước vào dự án nhóm (Lab 8 – Lab 15):

| Bài Lab | Tên bài thực hành | Vị trí việc làm hướng tới | Tệp báo cáo & Sản phẩm chính | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| **Lab 1** | **Chuẩn bị môi trường làm việc** | Mọi vị trí Web3 | [`lab01.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/lab01.md) (Antigravity, MetaMask, Sepolia Faucet, Commit đầu tiên) | ✅ Hoàn thành |
| **Lab 2** | **Ví và giao dịch đầu tiên** | Chuyên viên Tuân thủ & Kế toán số | [`lab02.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/lab02.md) (Bảng đối chiếu Tx thành công vs thất bại, EIP-55 Checksum, Insufficient gas) | ✅ Hoàn thành |
| **Lab 3** | **Đọc giao dịch & Hợp đồng trên Etherscan** | Chuyên viên AML/KYC & Kế toán số | [`lab03.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/lab03.md) / [`forensics.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/forensics.md) (Mổ xẻ 10 trường on-chain, đối soát USDT/USDC, Proxy Contract) | ✅ Hoàn thành |
| **Lab 4** | **Nhận diện hợp đồng có rủi ro** | Chuyên viên Thẩm định rủi ro (Risk Analyst) | [`lab04.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/lab04.md) + [`ClubTokensHardened.sol`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/contracts/lab04/ClubTokensHardened.sol) (Phát hiện bẫy Honeypot, Unlimited Mint) | ✅ Hoàn thành |
| **Lab 5** | **Viết đặc tả cho công cụ phân tích dòng tiền** | Chuyên viên Phân tích nghiệp vụ (BA) | [`lab05.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/lab05.md) + [`SPEC.MD`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/SPEC.MD) (Quy tắc R1–R10, biên bản kiểm tra chéo) | ✅ Hoàn thành |
| **Lab 6** | **Sinh mã bằng AI và kiểm tra kết quả** | Chuyên viên Dữ liệu On-chain & BA | [`lab06.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/lab06.md) + [`wallet_analyzer.py`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/wallet_analyzer.py) + [`test/test_wallet_analyzer.py`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/test/test_wallet_analyzer.py) | ✅ Hoàn thành |
| **Lab 7** | **Tính chi phí vận hành thực tế** | Quản lý tài chính & Kế toán tài sản số | [`lab07.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/lab07.md) + [`scripts/gas_calculator.py`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/scripts/gas_calculator.py) + [`cost_comparison.png`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/cost_comparison.png) | ✅ Hoàn thành |

---

## 🛠️ CẤU TRÚC THƯ MỤC REPO CÁ NHÂN

```text
lab1-7/
├── README.md                           # Tổng quan hồ sơ thực hành cá nhân
├── AGENTS.md                           # Bản quy ước chỉ dẫn dành riêng cho trợ lý AI
├── AI_JOURNAL.md                       # Nhật ký làm việc với AI và các lỗi bắt được (AI/AJ)
├── AJ_JOURNAL.md                       # Bản sao đồng bộ của AI_JOURNAL.md
├── SPEC.MD                             # Bản đặc tả yêu cầu nghiệp vụ chuẩn BA (Lab 5 & 6)
├── lab01.md                            # Báo cáo Lab 1: Môi trường, ví và Git
├── lab02.md                            # Báo cáo Lab 2: Giao dịch thành công & thất bại
├── lab03.md                            # Báo cáo Lab 3: Đọc dữ liệu sổ cái Etherscan
├── forensics.md                        # Báo cáo phân tích chuyên sâu on-chain (Lab 3)
├── lab04.md                            # Báo cáo Lab 4: Thẩm định mã độc và rủi ro hợp đồng
├── lab05.md                            # Báo cáo Lab 5: Đặc tả hệ thống phân tích dòng tiền
├── lab06.md                            # Báo cáo Lab 6: Sinh mã Python & kiểm thử gian lận
├── lab07.md                            # Báo cáo Lab 7: Bảng tính chi phí vận hành & độ nhạy L1/L2
├── wallet_analyzer.py                  # Mã nguồn công cụ phân tích dòng tiền on-chain
├── cashflow_chart.png                  # Biểu đồ số dư lũy kế xuất ra từ Lab 6
├── cost_comparison.png                 # Biểu đồ so sánh chi phí L1 vs L2 xuất ra từ Lab 7
├── contracts/                          # Các hợp đồng thông minh thẩm định và mẫu
│   └── lab04/
│       ├── ClubTokens.sol              # 3 token bài tập Lab 4 (A, B, C)
│       └── ClubTokensHardened.sol      # Bản vá an toàn do sinh viên thiết kế
├── test/
│   └── test_wallet_analyzer.py         # Bộ kiểm thử tự động 3 ca (Normal, Edge, Fraud)
├── scripts/
│   ├── gas_calculator.py               # Công cụ tự động tính toán chi phí gas L1 vs L2
│   └── plot_costs.py                   # Script vẽ biểu đồ so sánh chi phí vận hành
└── evidence/                           # Thư mục lưu trữ hình ảnh và bằng chứng thực nghiệm
    ├── lab-06/                         # Minh chứng biểu đồ Lab 6
    └── lab-07/                         # Minh chứng biểu đồ Lab 7
```

---

## 🎯 TIÊU CHUẨN ĐÁNH GIÁ VÀ LIÊM CHÍNH HỌC THUẬT

Toàn bộ các bài lab trong thư mục này đều được hoàn thiện ở cấp độ **⭐⭐⭐ Giỏi (9,0 – 10,0 điểm)**:
1. **Có chứng từ on-chain xác thực:** Tra cứu trực tiếp trên Etherscan Sepolia với các mã băm thực tế.
2. **Có kiểm thử cho trường hợp gian lận:** Tấn công đầu độc địa chỉ (Address Poisoning), bẫy Honeypot, Unlimited Minting.
3. **Phản biện công cụ AI có bằng chứng:** Mọi phát hiện lỗi của AI (về Checksum, chi phí gas lệnh lỗi, phiên bản API v2, đề xuất L1 phi lý) đều được lưu trữ đầy đủ trong [`AJ_JOURNAL.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/AJ_JOURNAL.md) với số dòng mã cụ thể.
4. **Gắn kết chặt chẽ với khung pháp lý Việt Nam:** Luật Công nghiệp Công nghệ số (hiệu lực 01/2026), Nghị quyết 05/2025/NQ-CP và các Thông tư kế toán / thuế tài sản mã hóa (15/2026/TT-BTC, 41/2026/TT-BTC).
