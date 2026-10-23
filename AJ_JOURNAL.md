# NHẬT KÝ LÀM VIỆC VỚI AI — HỌC PHẦN ECO2432 (LAB 1 ĐẾN LAB 7)
**Sinh viên thực hiện:** Nguyễn Nguyên Phương  
**Địa chỉ ví cá nhân (Sepolia):** [`0x6f69897D262D99Fc705bF7549631ca1b498d1F14`](https://sepolia.etherscan.io/address/0x6f69897D262D99Fc705bF7549631ca1b498d1F14)  
**Tệp quy ước:** [`AGENTS.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/AGENTS.md)  

---

## 📋 MỤC TIÊU VÀ NGUYÊN TẮC QUẢN TRỊ AI
Nhật ký này lưu vết toàn bộ các lần tương tác với Trợ lý AI (Google Antigravity / Gemini) theo đúng tiêu chuẩn đánh giá của Sổ tay thực hành ECO2432:
- Rèn luyện kỹ năng **Prompt Engineering** có cấu trúc, kèm vai trò và ràng buộc chống ảo giác (Anti-hallucination constraints).
- Nâng cao năng lực **thẩm định, phản biện độc lập** của con người đối với sản phẩm do AI sinh ra.
- Ghi nhận chi tiết: Prompt, Phản hồi của AI, Đánh giá (Dùng được / Phải sửa / Bỏ), Vị trí lỗi cụ thể (số dòng), Cách sửa và Ai là người phát hiện.

---

## Lần 1: Nhận diện hợp đồng có rủi ro (Lab 04)

**Prompt:**
```text
Bạn là chuyên viên thẩm định rủi ro tài sản số.
Dưới đây là mã nguồn một hợp đồng token. Hãy liệt kê mọi quyền đặc biệt mà
chủ sở hữu hợp đồng có thể thực hiện, và với mỗi quyền, nêu rõ:
- Tên hàm và số dòng
- Người nắm giữ token chịu rủi ro gì
Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy.
[dán mã nguồn]
```

**AI trả về:**
- Nhận diện vị trí `[dán mã nguồn]` chưa có nội dung và thông báo *"Không tìm thấy mã nguồn"* theo đúng câu cấm chặn ảo giác của prompt.
- Đồng thời phát hiện và đối chiếu tệp `ClubTokens.sol` có sẵn trong repo, cung cấp bảng phân tích rủi ro chi tiết kèm số dòng chính xác cho cả 3 hợp đồng: `ClubTokenA` (an toàn), `ClubTokenB` (hàm `mint` dòng 18–20), `ClubTokenC` (hàm `setRestricted` dòng 30–32).

**Đánh giá:** ✅ Dùng được

**Chỗ sai:** Không có thông tin bịa đặt. Số dòng và tên hàm khớp chính xác với mã nguồn.

**Cách sửa:** Sinh viên mở file `ClubTokens.sol` để đối chiếu từng số dòng, sau đó lập bảng kết luận chính thức vào `lab04.md`.

**Ai phát hiện:** AI tự nhận diện prompt thiếu mã nguồn; Sinh viên đối chiếu và xác nhận tính chuẩn xác của số dòng và logic nghiệp vụ.

### So sánh kết quả: Đọc thủ công vs AI hỗ trợ (Lab 04)
1. **Đọc thủ công tự tìm ra được gì?**
   - **ClubTokenA:** Kế thừa `ERC20`, mint 1.000.000 token ở constructor, không có hàm `mint` hay modifier `onlyOwner` nào khác.
   - **ClubTokenB:** Phát hiện hàm `mint` có modifier `onlyOwner` ở dòng 18–20, biết rằng chủ sở hữu có thể tạo thêm token.
   - **ClubTokenC:** Phát hiện hàm `setRestricted` có `onlyOwner` ở dòng 30–32 và mapping `restricted` liên kết tới điều kiện chặn tại hàm `_update` (dòng 34–37).
2. **AI tìm thêm được gì?**
   - **Định danh chính xác rủi ro tài chính / kinh tế:** AI diễn giải rõ hậu quả từ góc nhìn chuyên viên thẩm định rủi ro tài sản số:
     - Token B: Rủi ro **Lạm phát vô hạn (Unlimited Minting)**, **Pha loãng giá trị (Dilution)** và nguy cơ **Rug pull** (chủ sở hữu tự đúc token rồi xả ra thị trường thanh khoản làm sập giá trị token của người nắm giữ).
     - Token C: Rủi ro **Đóng băng tài sản đơn phương (Censorship / Blacklist Risk)**, phân tích rõ cơ chế hàm `_update` chặn giao dịch gửi đi khiến người dùng mất thanh khoản hoàn toàn (bẫy Honeypot).
   - **Bổ sung các quyền quản trị kế thừa:** AI chỉ ra các hàm kế thừa ngầm từ thư viện `Ownable` của OpenZeppelin (`transferOwnership`, `renounceOwnership`) mà sinh viên dễ bỏ sót khi chỉ nhìn lướt qua các hàm tự viết trong file.
3. **AI có phân tích sai hoặc tự bịa thêm chỗ nào không?**
   - **Không tự bịa nội dung:** Nhờ câu lệnh có ràng buộc nghiêm ngặt (*"Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy"*), AI không tự bịa ra các lỗi phổ biến khác (như Reentrancy, Selfdestruct, Fee-on-transfer...).
   - **Số dòng chính xác 100%:** AI trích đúng dòng 18–20 cho `ClubTokenB` và dòng 30–32, 34–37 cho `ClubTokenC`, không bị lệch dòng.

---

## Lần 2: Ví và Giao dịch đầu tiên (Lab 02)

**Prompt:**
```text
Bạn là chuyên viên phân tích nghiệp vụ blockchain. 
Giải thích điều gì xảy ra trong 2 trường hợp:
1. Sửa 1 ký tự trong địa chỉ người nhận trên MetaMask.
2. Chuyển toàn bộ số dư ETH có trong ví.
Nêu rõ mã băm giao dịch có xuất hiện trên Etherscan không và người gửi có bị mất phí gas không?
Chỉ trả lời dựa trên cơ chế kỹ thuật của Ethereum và MetaMask.
```

**AI trả về:**
- Trường hợp 1: AI cho rằng giao dịch vẫn được gửi lên blockchain nhưng sẽ bị thất bại on-chain với lỗi "Địa chỉ không tồn tại" và người gửi bị mất phí gas.
- Trường hợp 2: AI nói rằng MetaMask sẽ tự động trừ phí gas vào số tiền gửi, người nhận sẽ nhận được số tiền ít hơn.

**Đánh giá:** ❌ Sai, bỏ (Mắc 2 lỗi sai bản chất nghiêm trọng).

**Chỗ sai:**
1. *Sai ở Trường hợp 1:* MetaMask có cơ chế kiểm tra mã checksum EIP-55 ở phía Client. Khi sửa 1 ký tự, MetaMask chặn ngay tại giao diện, không phát sóng vào mạng lưới nên không có TxHash và không tốn phí gas.
2. *Sai ở Trường hợp 2:* Phí gas là khoản phí độc lập được tính bằng Native ETH và cộng thêm vào giao dịch (`Total = Value + Gas Fee`), không tự động trừ vào số tiền gửi. MetaMask sẽ báo lỗi "Insufficient funds for gas" và vô hiệu hóa nút chuyển.

**Cách sửa:** Sinh viên trực tiếp thao tác thực nghiệm trên MetaMask, ghi nhận lỗi thực tế và prompt phản biện lại AI để AI thừa nhận và giải thích đúng cơ chế kỹ thuật.

**Ai phát hiện:** **Sinh viên phát hiện** qua thực nghiệm tại lớp.

---

## Lần 6: Sinh mã phân tích dòng tiền từ đặc tả SPEC.md (Lab 06)

**Prompt:**
```text
Đọc tệp SPEC.md trong dự án và viết chương trình Python thực hiện đúng đặc tả đó.
Tuân thủ các quy ước trong AGENTS.md.
Trước khi viết mã, hãy tóm tắt lại cách bạn hiểu yêu cầu để tôi xác nhận.
Nếu có chỗ nào trong đặc tả chưa rõ, hãy hỏi tôi thay vì tự quyết định.
```

**AI trả về:**
- Tóm tắt yêu cầu nghiệp vụ và sinh hàm `analyze_cash_flow(address, txs)`.
- Trong vòng lặp duyệt danh sách giao dịch, AI sinh đoạn mã xử lý giao dịch lỗi như sau:
```python
if tx.get("isError") == "1":
    continue  # Bỏ qua giao dịch thất bại vì không chuyển tiền
```

**Đánh giá:** ❌ Sai, bỏ (Mắc lỗi nghiêm trọng về bản chất chi phí gas on-chain).

**Chỗ sai:**
- AI ngộ nhận rằng giao dịch lỗi (revert) thì không có dòng tiền nào phát sinh.
- Trên thực tế blockchain: Khi một giao dịch gửi đi bị lỗi (`from == target_address` và `isError == "1"`), số tiền chuyển `Value` được mạng hoàn lại (không bị trừ), nhưng **toàn bộ chi phí gas (`gasUsed * gasPrice`) vẫn bị trừ vĩnh viễn khỏi ví của người gửi** để bù đắp tài nguyên tính toán cho Validator.
- Nếu bỏ qua giao dịch này (`continue`), số dư lũy kế trên báo cáo sẽ cao hơn số dư thực tế trong ví, làm sai lệch hoàn toàn sổ sách kế toán và đối soát AML.

**Cách sửa (Sinh viên đã làm gì):**
- Sinh viên phát hiện lỗ hổng khi đối chiếu Danh mục kiểm tra bắt buộc mục 4 (Sổ tay trang 15).
- Sửa lại logic trong `wallet_analyzer.py`:
```python
# R4: Giao dịch thất bại vẫn bị trừ phí, không trừ value
if is_error:
    amount_eth = 0.0
    actual_deduction = fee_eth
else:
    amount_eth = value_eth
    actual_deduction = value_eth + fee_eth

cumulative_balance -= actual_deduction
total_out += actual_deduction
```

**Ai phát hiện:** **Sinh viên phát hiện** khi kiểm tra ca kiểm thử giao dịch lỗi.

---

## Lần 7: Cấu hình kết nối API Etherscan và Bảo mật khóa (Lab 06)

**Prompt:**
```text
Hãy viết hàm kết nối và truy xuất dữ liệu lịch sử giao dịch từ Etherscan API cho mạng Ethereum Mainnet và Sepolia Testnet.
```

**AI trả về:**
- AI sinh mã với URL endpoint cũ của từng mạng riêng rẽ:
```python
API_KEY = "YOUR_API_KEY_HERE"  # AI hardcode chuỗi dự phòng
base_url = "https://api-sepolia.etherscan.io/api"  # Endpoint v1 cũ
```

**Đánh giá:** ❌ Sai, bỏ (Vi phạm 2 tiêu chí an toàn và cập nhật công nghệ).

**Chỗ sai:**
1. *Vi phạm bảo mật AGENTS.md (Quy tắc 1):* AI gợi ý hardcode khóa API vào mã nguồn thay vì đọc từ biến môi trường. Điều này dễ dẫn đến nguy cơ lộ khóa API lên kho mã nguồn GitHub công khai.
2. *Lỗi phiên bản API (Danh mục kiểm tra mục 6):* AI sử dụng endpoint API v1 cũ (`api-sepolia.etherscan.io`). Etherscan hiện nay đã chuyển sang giao diện hợp nhất **Unified Multichain API v2** (`https://api.etherscan.io/v2/api?chainid=...`). Dữ liệu huấn luyện của AI cũ hơn nên AI không tự biết thay đổi này nếu sinh viên không mở tài liệu chính thức đối chiếu.

**Cách sửa (Sinh viên đã làm gì):**
- Xóa bỏ hoàn toàn việc gán cứng khóa API, cài đặt hàm `parse_env_api_key()` đọc từ `os.getenv("ETHERSCAN_API_KEY")`.
- Cập nhật URL endpoint sang Etherscan Multichain API v2 với tham số `chainid=1` (Mainnet) hoặc `chainid=11155111` (Sepolia).
- Thêm cơ chế xử lý ngoại lệ và kiểm tra mã phản hồi HTTP `response.status_code == 200` và `status == "1"`.

**Ai phát hiện:** **Sinh viên phát hiện** qua việc tra cứu Etherscan API Documentation mới nhất và rà soát theo `AGENTS.md`.

---

## Lần 8: Tính toán chi phí vận hành và Lựa chọn mạng triển khai (Lab 07)

**Prompt:**
```text
Hãy ước tính chi phí vận hành hàng tháng cho một DApp thẻ tích điểm của CLB sinh viên (1.000 lượt cộng điểm/tháng) trên mạng Ethereum Mainnet và đề xuất phương án tài chính phù hợp.
```

**AI trả về:**
- AI tính toán chi phí gas trên Ethereum Mainnet khoảng $1.200 - $3.000 USD/tháng (~30 - 76 triệu VNĐ).
- AI đề xuất câu lạc bộ nên "thu phí thành viên từ sinh viên hoặc xin tài trợ doanh nghiệp để duy trì chi phí trên Ethereum Mainnet". AI không hề đề cập tới giải pháp Layer 2.

**Đánh giá:** ❌ Sai, bỏ (Mắc lỗi nghiêm trọng về tư duy kinh tế sản phẩm Web3).

**Chỗ sai:**
1. *Phi lý về mặt hành vi kinh tế:* Một cốc nước mía hay ổ bánh mì sinh viên chỉ từ 10.000 - 20.000 VNĐ mà phí tích điểm mỗi lần lên tới 30.000 - 76.000 VNĐ thì không người dùng nào chấp nhận.
2. *Phi lý về mặt tài chính CLB:* Quỹ sinh viên chỉ có 1 - 3 triệu VNĐ/tháng, chi trả 30 - 76 triệu VNĐ tiền gas sẽ phá sản ngay tháng đầu tiên.
3. *Bỏ sót giải pháp Layer 2 & ERC-4337:* AI không nhận thức được việc dịch chuyển sang Layer 2 (Base, Arbitrum) giúp giảm phí 100 lần (chỉ còn ~300 VNĐ/lượt) và kết hợp Paymaster để tạo trải nghiệm miễn phí gas (Zero-gas UX) cho sinh viên.

**Cách sửa (Sinh viên đã làm gì):**
- Bác bỏ đề xuất triển khai trên Layer 1 của AI.
- Xây dựng bảng phân tích so sánh L1 vs L2 và phân tích độ nhạy (Stress Test) chứng minh tính khả thi kinh tế vượt trội của Layer 2 trong [`lab07.md`](file:///Users/phuongnguyennguyen/Desktop/solidity-project/lab1-7/lab07.md).

**Ai phát hiện:** **Sinh viên phát hiện** qua tư duy phân tích kinh tế thực tiễn.
