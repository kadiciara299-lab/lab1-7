# BÁO CÁO THỰC HÀNH LAB 1 — CHUẨN BỊ MÔI TRƯỜNG LÀM VIỆC
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Thời lượng:** 75 phút · Thực hành cá nhân  
**Sinh viên thực hiện:** Nguyễn Nguyên Phương  
**Vị trí việc làm hướng tới:** Mọi vị trí tài sản số (BA, AML/KYC, Kế toán, Kiểm toán viên Web3)  

---

## 1. MỤC TIÊU VÀ CHUẨN ĐẦU RA

Mọi vị trí trong lĩnh vực tài sản số đều bắt đầu bằng việc sở hữu một địa chỉ ví Web3 an toàn và một môi trường làm việc chuẩn mực. Buổi học này giúp sinh viên thiết lập các công cụ nền tảng thiết yếu:
1. **Công cụ AI hỗ trợ lập trình:** Cài đặt và kích hoạt thành công Google Antigravity IDE.
2. **Ví cá nhân Web3:** Tạo lập và bảo mật ví MetaMask, kết nối mạng thử nghiệm Ethereum Sepolia.
3. **Nguồn vốn thử nghiệm:** Nhận Sepolia ETH phục vụ thực hành các bài lab xuyên suốt học kỳ.
4. **Kho mã nguồn cá nhân:** Khởi tạo kho GitHub cá nhân và thiết lập tệp quy ước chỉ dẫn AI `AGENTS.md`.

---

## 2. QUÁ TRÌNH THỰC HIỆN CÁC BƯỚC

### Bước 1: Cài đặt và kiểm tra công cụ Antigravity IDE
- Tải, cài đặt và đăng nhập thành công Antigravity IDE bằng tài khoản Google sinh viên.
- Kiểm tra hoạt động trợ lý AI: Đặt câu hỏi *"Giải thích ngắn gọn: blockchain khác cơ sở dữ liệu thông thường ở điểm nào?"*.
  - *Kết luận cốt lõi:* Cơ sở dữ liệu truyền thống có tính tập trung (Centralized), người quản trị (Admin) có toàn quyền sửa/xóa (CRUD); Blockchain là sổ cái phân tán (Decentralized Ledger), chỉ có thao tác ghi thêm (Append-only), dữ liệu được bảo vệ bằng mật mã học và cơ chế đồng thuận, có **tính bất biến (Immutability)** tuyệt đối.

### Bước 2: Tạo lập và bảo mật ví MetaMask
- Cài đặt tiện ích mở rộng MetaMask trên trình duyệt.
- Lựa chọn: **Create a new wallet**.
- **Quy tắc an toàn sống còn:** Ghi chép 12 từ khôi phục (Secret Recovery Phrase / Mnemonic Phrase) ra sổ tay giấy, cất giữ an toàn. Tuyệt đối không chụp ảnh màn hình, không lưu trữ trên cloud hay gửi qua tin nhắn.
  - *Ý nghĩa pháp lý:* 12 từ khóa này là chìa khóa gốc (Master Key) đại diện cho quyền sở hữu tối cao đối với toàn bộ tài sản trong ví. Không có tổng đài hay ngân hàng nào có thể cấp lại nếu làm mất.
- Bật hiển thị mạng thử nghiệm: `Settings` $\rightarrow$ `Advanced` $\rightarrow$ Bật `Show test networks` $\rightarrow$ Chuyển mạng sang **Sepolia Testnet**.

### Bước 3: Nhận Sepolia ETH thử nghiệm
- Thực hiện faucet nhận Sepolia ETH thông qua cổng Google Cloud Web3 Faucet hoặc nhận cấp phát từ ví kho bạc của giảng viên.
- Điền thông tin địa chỉ ví vào bảng tính quản lý của lớp học.
- **Địa chỉ ví cá nhân thực nghiệm:** `0x6f69897D262D99Fc705bF7549631ca1b498d1F14`

### Bước 4: Thiết lập kho mã nguồn và tệp chỉ dẫn `AGENTS.md`
- Tạo tài khoản GitHub nghề nghiệp nghiêm túc.
- Khởi tạo kho mã nguồn cá nhân, tải cấu trúc khởi đầu dự án `hce-web3-starter`.
- Mở tệp [`AGENTS.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/AGENTS.md), đọc và quán triệt từng quy ước nội bộ cho công cụ AI:
  - Sử dụng Solidity `^0.8.20`, OpenZeppelin v5 (dùng `_update`).
  - Mọi hàm thay đổi trạng thái phải phát `event`.
  - Tuân thủ thứ tự **Checks – Effects – Interactions**.
  - Không ghi khóa API trực tiếp trong mã nguồn, đọc từ biến môi trường.
  - Đổi wei sang ETH trước khi hiển thị (chia $10^{18}$).
- Bổ sung quy ước cá nhân vào cuối tệp:
  ```markdown
  - Chú thích trong mã viết bằng tiếng Việt không dấu.
  ```
- Tạo bản ghi thay đổi đầu tiên trên Git:
  ```bash
  git add .
  git commit -m "chore: thiet lap moi truong lam viec"
  git push origin main
  ```

---

## 3. SẢN PHẨM VÀ MINH CHỨNG NGHIỆM THU

1. **Địa chỉ ví cá nhân (Sepolia):**  
   [`0x6f69897D262D99Fc705bF7549631ca1b498d1F14`](https://sepolia.etherscan.io/address/0x6f69897D262D99Fc705bF7549631ca1b498d1F14)
2. **Tệp chỉ dẫn AI:** [`AGENTS.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/AGENTS.md)
3. **Commit đầu tiên trên Git:** `chore: thiet lap moi truong lam viec`
