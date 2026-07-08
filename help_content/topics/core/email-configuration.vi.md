---
title: Cấu hình Email
---

Cấu hình email kiểm soát cách cửa hàng của bạn gửi email giao dịch — xác nhận đơn hàng, thông báo vận chuyển, đặt lại mật khẩu và nhiều hơn nữa. Spwig bao gồm một máy chủ SMTP tích hợp và hỗ trợ các nhà cung cấp email bên ngoài để tăng khả năng giao hàng.

![Tài khoản email](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Các nhà cung cấp có sẵn

| Nhà cung cấp | Mô tả |
|----------|-------------|
| **SMTP tích hợp** | Máy chủ email tự lưu trữ miễn phí được bao gồm với Spwig. Ký tên DKIM tự động. |
| **Gmail API** | Gửi qua tài khoản Gmail hoặc Google Workspace của bạn bằng xác thực OAuth. |
| **SMTP chung** | Kết nối bất kỳ máy chủ SMTP nào (SendGrid, Mailgun, Amazon SES hoặc máy chủ email của riêng bạn). |

## Thiết lập email

Truy cập **Cài đặt > Tài khoản Email** và nhấn **Thêm Tài khoản Email** để khởi động trình hướng dẫn thiết lập.

### Bước 1: Chọn nhà cung cấp

Chọn nhà cung cấp email của bạn. Máy chủ SMTP tích hợp là tùy chọn đơn giản nhất để bắt đầu — nó không yêu cầu bất kỳ tài khoản bên ngoài nào.

### Bước 2: Cấu hình thông tin xác thực

Nhập thông tin xác thực cho nhà cung cấp đã chọn của bạn:

- **SMTP tích hợp** — Không cần thông tin xác thực. Máy chủ chạy trên cài đặt Spwig của bạn.
- **Gmail API** — Xác thực qua Google OAuth. Bạn sẽ được chuyển hướng đến đăng nhập bằng tài khoản Google của bạn.
- **SMTP chung** — Nhập địa chỉ máy chủ SMTP, cổng, tên người dùng và mật khẩu.

### Bước 3: Cấu hình người gửi

Thiết lập danh tính người gửi cho các email đi ra:

- **Email người gửi** — Địa chỉ email hiển thị trong trường "Từ" (ví dụ: orders@yourstore.com)
- **Tên người gửi** — Tên hiển thị bên cạnh địa chỉ email (ví dụ: "Tên Cửa Hàng Của Bạn")
- **Email trả lời** — Nơi khách hàng trả lời được chuyển hướng (có thể khác với địa chỉ người gửi)

### Bước 4: Xác minh DNS

Kiểm tra các bản ghi xác thực email của miền của bạn. Trình hướng dẫn kiểm tra ba bản ghi DNS:

| Bản ghi | Mục đích |
|--------|---------|
| **SPF** | Phê chuẩn máy chủ của bạn gửi email thay mặt cho miền của bạn |
| **DKIM** | Ký tên số hóa email để chứng minh chúng không bị sửa đổi |
| **DMARC** | Thông báo cho các máy chủ nhận biết làm gì với các email thất bại kiểm tra SPF/DKIM |

Đối với mỗi bản ghi, trình hướng dẫn hiển thị:
- **Trạng thái hiện tại** — Bản ghi có được cấu hình đúng cách hay không
- **Giá trị yêu cầu** — Bản ghi DNS chính xác để thêm vào nhà đăng ký miền của bạn
- **Trạng thái lan truyền** — Các thay đổi gần đây có hiệu lực hay không (thay đổi DNS có thể mất đến 48 giờ)

Máy chủ SMTP tích hợp tự động tạo khóa DKIM cho miền của bạn.

### Bước 5: Gửi email kiểm tra

Gửi một email kiểm tra để xác minh mọi thứ hoạt động:
1. Nhập địa chỉ email người nhận
2. Nhấn **Gửi Kiểm Tra**
3. Kiểm tra hộp thư đến của bạn để xem tin nhắn kiểm tra
4. Xác minh email đến mà không có cảnh báo spam

### Bước 6: Lưu và kích hoạt

Lưu cấu hình và thiết lập tài khoản là hoạt động. Đánh dấu nó là **Mặc định** nếu nó nên là tài khoản email chính.

## Mẫu email

Spwig bao gồm hơn 30 mẫu email cho mọi sự kiện giao dịch. Truy cập **Cài đặt > Mẫu Email** để quản lý chúng.

### Loại mẫu

Các mẫu bao gồm tất cả các sự kiện cửa hàng như:
- **Chu kỳ đơn hàng** — Xác nhận, đang xử lý, đã gửi, đã giao, đã hủy
- **Thanh toán** — Hóa đơn, xác nhận hoàn tiền, thanh toán thất bại
- **Tài khoản khách hàng** — Chào mừng, đặt lại mật khẩu, xác minh email
- **Thẻ quà tặng** — Giao hàng, thông báo số dư
- **Vận chuyển** — Cập nhật theo dõi, xác nhận giao hàng
- **Sản phẩm kỹ thuật số** — Liên kết tải xuống, khóa giấy phép
- **Tiếp thị** — Phục hồi giỏ hàng bị bỏ lại, yêu cầu đánh giá

### Tùy chỉnh mẫu

1. Truy cập danh sách mẫu
2. Nhấn vào mẫu để chỉnh sửa
3. Thay đổi tiêu đề, phần đầu, nội dung chính và phần chân trang
4. Sử dụng các biến mẫu (ví dụ: `{{ order.number }}`, `{{ customer.name }}`) cho nội dung động
5. Xem trước email trước khi lưu

### Hỗ trợ đa ngôn ngữ

Mẫu email hỗ trợ nhiều ngôn ngữ:
- Mỗi mẫu có thể có bản dịch cho tất cả các ngôn ngữ đang hoạt động của cửa hàng bạn
- Hệ thống gửi email bằng ngôn ngữ ưa thích của khách hàng
- **Chuỗi phản hồi ngôn ngữ** — Nếu bản dịch không có sẵn, hệ thống sẽ chuyển về ngôn ngữ mặc định của cửa hàng
- Sử dụng tính năng **Dịch thuật AI** để tự động dịch mẫu sang các ngôn ngữ khác

### Sao chép mẫu

Để tạo phiên bản tùy chỉnh của mẫu hệ thống:
1. Mở mẫu bạn muốn chỉnh sửa
2. Nhấn **Sao chép Mẫu**
3. Chỉnh sửa phiên bản sao chép
4. Phiên bản sao chép có quyền ưu tiên hơn mẫu hệ thống gốc

## Hàng đợi email

Theo dõi các email đi ra tại **Cài đặt > Hàng đợi Email**:

- **Đang chờ** — Các email đang chờ để gửi
- **Đang gửi** — Hiện đang được truyền tải
- **Đã gửi** — Giao hàng thành công
- **Thất bại** — Không thể giao hàng (với chi tiết lỗi)
- **Bounce** — Bị từ chối bởi máy chủ email của người nhận

Nhấn vào bất kỳ email nào để xem chi tiết đầy đủ bao gồm người nhận, tiêu đề, thời gian gửi và trạng thái giao hàng.

## Theo dõi giao hàng

Theo dõi sự tương tác với email:
- **Mở** — Số lượng người nhận đã mở email
- **Click** — Lượt nhấp vào liên kết trong email
- **Bounce** — Theo dõi bounce cứng và mềm
- **Khiếu nại** — Báo cáo thư rác từ người nhận

## Nhiều tài khoản

Bạn có thể cấu hình nhiều tài khoản email:
- **Tài khoản mặc định** — Được sử dụng cho tất cả các email đi ra trừ khi bị ghi đè
- **Tài khoản dự phòng** — Nếu tài khoản mặc định thất bại, email sẽ được xếp hàng để gửi lại
- Sử dụng các tài khoản khác nhau cho các mục đích khác nhau (ví dụ: một tài khoản cho email giao dịch, tài khoản khác cho tiếp thị)

## Một số mẹo

- Bắt đầu với máy chủ **SMTP tích hợp** để thiết lập nhanh chóng, sau đó chuyển sang nhà cung cấp bên ngoài nếu bạn cần thể tích gửi cao hơn hoặc khả năng giao hàng tốt hơn.
- Luôn cấu hình **SPF, DKIM và DMARC** — không có chúng, email có nhiều khả năng hơn sẽ rơi vào thư mục spam.
- Gửi một **email kiểm tra** sau bất kỳ thay đổi cấu hình nào để xác minh việc giao hàng hoạt động.
- Theo dõi hàng đợi email thường xuyên để kiểm tra các email **thất bại** hoặc **bounced** — điều này cho thấy có vấn đề về khả năng giao hàng.
- Sử dụng địa chỉ người gửi **chuyên nghiệp** (ví dụ: orders@yourstore.com) thay vì địa chỉ email miễn phí để tăng độ tin cậy và khả năng giao hàng.
- Giữ các mẫu ngắn gọn — email giao dịch nên cung cấp thông tin nhanh chóng, không phải là các bản tin tiếp thị.