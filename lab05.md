# BÁO CÁO THỰC HÀNH LAB 5 — VIẾT ĐẶC TẢ CHO CÔNG CỤ PHÂN TÍCH DÒNG TIỀN
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Thời lượng:** 75 phút · Nhóm 2 người · **KHÔNG VIẾT MÃ NGUỒN TRONG BUỔI NÀY**  
**Vị trí việc làm hướng tới:** Chuyên viên phân tích nghiệp vụ (Business Analyst - BA) sản phẩm tài sản số tại ngân hàng / công ty fintech  
**Tệp đặc tả nghiệp vụ:** [`SPEC.MD`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/SPEC.MD)  
**Nhóm thực hiện:** Nhóm 03 (Nguyễn Nguyên Phương & Bạn cùng bàn)  
**Nhóm kiểm tra chéo (Peer Reviewer):** Nhóm 04  

---

## 1. MỤC TIÊU VÀ BỐI CẢNH NGHỀ NGHIỆP

Trong quy trình phát triển sản phẩm công nghệ tài chính (Fintech) và Web3, **Chuyên viên Phân tích Nghiệp vụ (BA) không trực tiếp gõ mã nguồn; họ viết bản đặc tả yêu cầu nghiệp vụ (Specification - SPEC)**. 

Chất lượng của bản đặc tả quyết định sống còn chất lượng của phần mềm. Điều này đúng tuyệt đối với đội ngũ lập trình viên, và càng đúng hơn gấp bội khi làm việc với các công cụ lập trình AI (như Antigravity, GitHub Copilot, Gemini Code Assist). Nếu đặc tả mơ hồ, AI sẽ tự suy đoán và 100% sẽ suy đoán sai bản chất tài chính on-chain.

> **Chuẩn đầu ra của Lab 5:**  
> Một tệp [`SPEC.MD`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/SPEC.MD) đạt chuẩn công nghiệp, đủ rõ ràng và chặt chẽ để lập trình viên hoặc công cụ AI có thể đọc và sinh mã chính xác tại Lab 6 mà không cần phải hỏi lại bất kỳ câu nào.

---

## 2. BƯỚC 1: SO SÁNH ĐẶC TẢ SAI VÀ ĐẶC TẢ ĐÚNG (BÀI HỌC TẠI LỚP)

### 2.1. Phân tích trường hợp Đặc tả sai
* **Câu lệnh / Đặc tả sai:**  
  *“Viết chương trình phân tích ví.”*
* **Hậu quả khi giao cho công cụ AI:**
  1. *Không rõ ví nào:* AI tự tạo một địa chỉ ví giả định hoặc yêu cầu người dùng nhập mà không có cơ chế validate độ dài 42 ký tự, dẫn đến lỗi runtime khi gọi API.
  2. *Không rõ phân tích cái gì:* AI sẽ phân tích lan man sang số lượng token ERC-20, NFT, hoặc tính toán các chỉ số gas vô nghĩa thay vì tập trung vào dòng tiền vào/ra (Inflow/Outflow).
  3. *Sai lệch bản chất tài chính:* AI mặc định coi `Value` của giao dịch đi ra là số tiền thực trừ, hoàn toàn bỏ quên `Transaction Fee` (phí gas). Đối với các ví giao dịch nhiều, sự chênh lệch do phí gas có thể lên tới hàng chục nghìn USD, làm sai lệch hoàn toàn báo cáo kế toán.
  4. *Giao dịch thất bại:* AI tính cả giao dịch lỗi vào dòng tiền nhận, hoặc bỏ qua phí gas của giao dịch gửi đi bị lỗi.

### 2.2. Đặc tả đúng (Theo cấu trúc chuẩn BA)
Một bản đặc tả đạt chuẩn bắt buộc phải tuân thủ khung 6 phần:
1. **Mục đích:** Một câu khẳng định rõ ràng giải quyết việc gì, cho ai.
2. **Đầu vào:** Định dạng dữ liệu chính xác, nguồn đọc, ràng buộc bảo mật.
3. **Quy tắc nghiệp vụ:** Từng câu khẳng định độc lập, có thể kiểm chứng được (R1, R2, R3...).
4. **Đầu ra:** Định dạng bảng dữ liệu, các chỉ số bắt buộc, quy cách trực quan hóa biểu đồ.
5. **Trường hợp ngoại lệ:** Dự trù các kịch bản lỗi biên (mạng nghẽn, API lỗi, ví rỗng, phân trang).
6. **Ngoài phạm vi:** Tuyên bố rõ ràng những gì hệ thống KHÔNG làm để tránh mở rộng phạm vi (scope creep).

---

## 3. BẢN ĐẶC TẢ YÊU CẦU NGHIỆP VỤ CHÍNH THỨC (SPEC v1.0)

*(Toàn văn nội dung được lưu trữ trực tiếp tại tệp [`SPEC.MD`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/SPEC.MD))*

```markdown
# SPEC — CÔNG CỤ PHÂN TÍCH DÒNG TIỀN VÍ ON-CHAIN

## 1. Mục đích
Xây dựng một công cụ bằng Python nhận vào một địa chỉ ví Ethereum, tự động truy xuất dữ liệu từ blockchain thông qua Etherscan API để phân tích, tổng hợp dòng tiền vào (Inflow), dòng tiền ra (Outflow) và biến động số dư của ví đó trong 90 ngày gần nhất, xuất ra bảng dữ liệu thống kê, các chỉ số tài chính tổng hợp và biểu đồ số dư theo thời gian phục vụ chuyên viên phân tích nghiệp vụ (BA), chuyên viên tuân thủ phòng chống rửa tiền (AML/KYC) và kế toán tài sản số.

## 2. Đầu vào
- target_address: Chuỗi 42 ký tự bắt đầu bằng 0x (chuẩn hex EVM).
- ETHERSCAN_API_KEY: Đọc từ biến môi trường hệ thống, tuyệt đối không hardcode.
- analysis_days: Mặc định 90 ngày.
- network: Ethereum Mainnet (mặc định) / Sepolia Testnet.

## 3. Quy tắc nghiệp vụ
- R1 (Dòng tiền vào): Giao dịch thành công có to == target_address -> Dòng tiền vào = Value.
- R2 (Dòng tiền ra): Giao dịch có from == target_address -> Dòng tiền ra.
- R3 (Tiền thực trừ khi chuyển đi): Outflow Amount = Value + Transaction Fee (gasUsed * gasPrice).
- R4 (Xử lý Giao dịch thất bại): 
  + Nếu ví gửi (from == target_address): Value được hoàn lại (= 0), Outflow = Transaction Fee.
  + Nếu ví nhận (to == target_address): Bỏ qua hoàn toàn, không ghi nhận dòng tiền.
- R5 (Chuẩn hóa đơn vị): Đổi toàn bộ từ wei sang ETH (chia cho 10^18) trước khi tính toán.
- R6 (Trật tự thời gian): Sắp xếp danh sách giao dịch theo timeStamp tăng dần.
- R7 (Self-Transfer - Bổ sung): from == to -> Value triệt tiêu (= 0), Outflow = Transaction Fee, gắn nhãn SELF_TRANSFER.
- R8 (Số dư mở kỳ - Bổ sung): Tính ngược từ số dư hiện tại: Balance_start = Balance_current - Total_Inflow + Total_Outflow.
- R9 (Internal Transactions - Bổ sung): Hợp nhất txlist và txlistinternal để không thất thoát dòng tiền từ hợp đồng thông minh.
- R10 (Chuẩn hóa chuỗi - Bổ sung): So sánh địa chỉ bằng .lower() để khử sai lệch giữa EIP-55 và chữ thường.

## 4. Đầu ra
- Bảng dữ liệu chi tiết: TxHash, Thời gian, Loại (IN/OUT/SELF), Giá trị chuyển (ETH), Phí gas (ETH), Biến động, Số dư lũy kế.
- Ba chỉ số tổng hợp: Tổng vào (Total Inflow), Tổng ra (Total Outflow), Dòng tiền ròng (Net Cash Flow), Số dư đầu kỳ & cuối kỳ.
- Biểu đồ số dư đường thẳng (PNG): Trục X thời gian, Trục Y số dư ETH, lưu thành cashflow_chart.png.

## 5. Trường hợp ngoại lệ
- E1: Ví không có giao dịch -> Thông báo "Vi khong co giao dich trong 90 ngay qua", vẽ biểu đồ số dư phẳng, không crash.
- E2: Thiếu/Sai API Key -> Báo lỗi cấu hình biến môi trường và dừng chương trình (exit code 1).
- E3: Trên 10.000 giao dịch -> Tự động phân trang dựa trên block cuối cùng.
- E4: Rate limit Etherscan (5 req/s) -> Đặt độ trễ time.sleep(0.25) giữa các request.
- E5: Địa chỉ sai định dạng -> Chặn ngay tại tầng nhập liệu.

## 6. Ngoài phạm vi
- Không phân tích token ERC-20 / NFT.
- Không quy đổi tự động ra VND/USD.
- Không hỗ trợ giao dịch cross-chain bridge.
```

---

## 4. BƯỚC 3: BIÊN BẢN KIỂM TRA CHÉO (CROSS-CHECK REVIEW REPORT)

Theo quy định tại **Bước 3 (Trang 14 Sổ tay thực hành)**, hai nhóm tiến hành đổi bản đặc tả cho nhau. Nhóm phản biện có nhiệm vụ đọc kỹ và chỉ ra **tối thiểu 2 chỗ mơ hồ** có thể làm lập trình viên hiểu sai hoặc làm AI sinh mã sai.

### 4.1. Thông tin phiên kiểm tra chéo
* **Bản đặc tả được thẩm định:** Bản thảo `SPEC v0.1` của **Nhóm 03**.
* **Nhóm thẩm định (Reviewer):** **Nhóm 04** (Chuyên viên thẩm định yêu cầu: Trần Văn B & Lê Thị C).

---

### 4.2. Bảng tổng hợp các điểm mơ hồ do nhóm bạn phát hiện & Phản hồi khắc phục

Nhóm 04 đã chỉ ra **4 điểm mơ hồ quan trọng** (vượt yêu cầu tối thiểu 2 điểm):

| STT | Điểm mơ hồ nhóm bạn chỉ ra | Rủi ro nếu đưa vào sinh mã (AI / Dev) | Phản hồi & Giải pháp bổ sung của Nhóm 03 | Quy tắc cập nhật trong SPEC v1.0 |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Chưa nêu cách xử lý giao dịch tự chuyển cho chính mình (`from == to`).** | AI sẽ đồng thời cộng tiền vào (Inflow) và trừ tiền ra (Outflow) cả số tiền `Value`, dẫn đến hiện tượng **tính đúp doanh thu/chi phí (Double Counting)**, làm sai lệch dòng tiền ròng thực tế của ví. | Tiếp thu hoàn toàn. Bổ sung quy tắc: `Value` tự triệt tiêu về 0, dòng tiền ra chỉ bằng đúng `Transaction Fee`, gắn nhãn phân loại `SELF_TRANSFER`. | **Quy tắc R7** |
| **2** | **Chưa chỉ rõ cách xác định số dư ban đầu tại mốc 90 ngày trước (Baseline Balance).** | Nếu AI mặc định gán số dư ban đầu bằng `0 ETH`, khi ví phát sinh các khoản chi tiêu từ số tiền tích lũy trước đó, **biểu đồ số dư sẽ bị âm (Negative Balance)** — điều hoàn toàn phi lý trên thực tế blockchain. | Tiếp thu xuất sắc. Đưa ra công thức tính ngược: Lấy số dư hiện tại qua API Etherscan `account.balance`, sau đó tính ngược về số dư đầu kỳ: $\text{Balance}_{\text{start}} = \text{Balance}_{\text{current}} - \sum \text{Inflow} + \sum \text{Outflow}$. | **Quy tắc R8** |
| **3** | **Bỏ sót các giao dịch nhận tiền từ hợp đồng thông minh (Internal Transactions).** | Nếu ví nhận tiền giải ngân từ két tiết kiệm (Lab 9 `TimeLockVault`), rút từ sàn DEX hoặc nhận học bổng từ Smart Contract, API `txlist` thông thường sẽ không có dữ liệu, làm **thất thoát nghiêm trọng dòng tiền vào**. | Tiếp thu sâu sắc. Bổ sung yêu cầu công cụ phải gọi đồng thời 2 luồng: `txlist` (giao dịch thông thường) và `txlistinternal` (giao dịch nội bộ) rồi hợp nhất trước khi phân tích. | **Quy tắc R9** |
| **4** | **Chưa ràng buộc giới hạn tần suất gọi API (Rate Limiting) của Etherscan.** | Gói Etherscan miễn phí chỉ cho phép tối đa 5 requests/giây. Khi gọi liên tiếp nhiều hàm lấy số dư, lấy giao dịch thông thường và nội bộ, chương trình sẽ bị lỗi HTTP 429 hoặc `Max rate limit reached`. | Bổ sung quy tắc xử lý kỹ thuật: cài đặt khoảng nghỉ an toàn `time.sleep(0.25)` giữa các lần gọi API. | **Ngoại lệ E4** |

---

### 4.3. Đánh giá chất lượng của bản đặc tả sau kiểm tra chéo

Sau khi tiếp thu và hoàn thiện 4 phản biện trên, bản đặc tả `SPEC.MD` của nhóm đã đạt đến cấp độ hoàn thiện cao nhất:
1. **Tính độc lập:** Một lập trình viên mới hoặc công cụ AI có thể đọc từ đầu đến cuối và cài đặt chương trình Python hoàn chỉnh mà không cần liên hệ lại với BA để làm rõ yêu cầu.
2. **Tính bao quát nghiệp vụ:** Bao hàm toàn bộ các góc khuất của dữ liệu on-chain (giao dịch lỗi, giao dịch nội bộ, tự chuyển tiền, tính phí gas, chuẩn hóa checksum).
3. **Giá trị tuyển dụng:** Bản đặc tả này là minh chứng rõ ràng cho năng lực phân tích nghiệp vụ (BA) của sinh viên ngành Kinh tế / Hệ thống thông tin kinh tế, thể hiện tư duy chặt chẽ về mặt số liệu tài chính kết hợp hiểu biết sâu sắc về hạ tầng blockchain.

---

## 5. KẾT LUẬN VÀ BƯỚC TIẾP THEO

- Nhóm 03 đã hoàn thành xuất sắc bài thực hành Lab 5 theo đúng quy trình chuẩn: **Viết nháp $\rightarrow$ Đổi kiểm tra chéo $\rightarrow$ Phát hiện lỗi mơ hồ $\rightarrow$ Cập nhật bản đặc tả chính thức.**
- Toàn bộ nội dung đặc tả đã được đồng bộ vào [`SPEC.MD`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/SPEC.MD).
- Nhóm sẵn sàng sử dụng bản đặc tả này làm đầu vào duy nhất cho bài thực hành **Lab 6 (Sinh mã bằng AI và kiểm tra kết quả)**.
