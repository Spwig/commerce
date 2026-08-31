---
title: Cấu hình Email
---

Cấu hình email kiểm soát cách cửa hàng của bạn gửi email giao dịch — xác nhận đơn hàng, thông báo vận chuyển, khôi phục mật khẩu, v.v. Spwig bao gồm máy chủ SMTP tích hợp và hỗ trợ các nhà cung cấp email bên ngoài để đảm bảo khả năng đến cao hơn.

![Tài khoản email](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Nhà cung cấp có sẵn

| Nhà cung cấp | Mô tả |
|----------|-------------|
| **SMTP tích hợp** | Máy chủ email tự host, miễn phí đi kèm với Spwig. Ký DKIM tự động. |
| **API Gmail** | Gửi qua tài khoản Gmail hoặc Google Workspace của bạn bằng xác thực OAuth. |
| **SMTP tổng quát** | Kết nối bất kỳ máy chủ SMTP nào (SendGrid, Mailgun, Amazon SES, hoặc máy chủ email của bạn). |

## Thiết lập Email

Đi đến **Cài đặt > Tài khoản Email** và nhấp vào **Thêm Tài khoản Email** để khởi chạy trình hướng dẫn thiết lập.

### Bước 1: Chọn Nhà cung cấp

Chọn nhà cung cấp email của bạn. Máy chủ SMTP tích hợp là tùy chọn đơn giản nhất để bắt đầu — nó không yêu cầu tài khoản bên ngoài.

### Bước 2: Cấu hình Thông tin đăng nhập

Nhập thông tin đăng nhập cho nhà cung cấp đã chọn:

- **SMTP tích hợp** — Không cần thông tin đăng nhập. Máy chủ chạy trên cài đặt Spwig của bạn.
- **API Gmail** — Xác thực qua Google OAuth. Bạn sẽ được chuyển hướng để đăng nhập bằng tài khoản Google của mình.
- **SMTP tổng quát** — Nhập địa chỉ máy chủ SMTP, cổng, tên người dùng và mật khẩu.

### Bước 3: Cấu hình Người gửi

Thiết lập danh tính người gửi cho email đến:

- **Email Người gửi** — Địa chỉ email xuất hiện trong trường "Người gửi" (ví dụ: orders@yourstore.com)
- **Tên Người gửi** — Tên hiển thị bên cạnh địa chỉ email (ví dụ: "Tên Cửa hàng của bạn")
- **Email Trả lời** — Nơi mà các cuộc trả lời của khách hàng được hướng đến (có thể khác với địa chỉ Người gửi)

### Bước 4: Xác minh DNS

Xác minh các bản ghi xác thực email của miền của bạn. Trình hướng dẫn kiểm tra ba bản ghi DNS:

| Bản ghi | Mục đích |
|--------|---------|
| **SPF** | Phê duyệt máy chủ của bạn để gửi email thay mặt cho miền của bạn |
| **DKIM** | Ký điện tử email để chứng minh chúng không bị thay đổi |
| **DMARC** | Nói với các máy chủ nhận điều gì nên được thực hiện với email vượt qua kiểm tra SPF/DKIM |

Đối với mỗi bản ghi, trình hướng dẫn hiển thị:
- **Trạng thái hiện tại** — Liệu bản ghi được cấu hình chính xác hay không
- **Giá trị được yêu cầu** — Bản ghi DNS chính xác để thêm tại nhà cung cấp đăng ký miền của bạn
- **Trạng thái lan truyền** — Liệu các thay đổi gần đây đã có hiệu lực hay chưa (các thay đổi DNS có thể mất đến 48 giờ)

Máy chủ SMTP tích hợp tự động tạo khóa DKIM cho miền của bạn.

### Bước 5: Gửi Email Thử

Gửi một email thử để kiểm tra mọi thứ hoạt động:
1. Nhập địa chỉ email người nhận
2. Nhấp vào **Gửi Email Thử**
3. Kiểm tra hộp thư đến của bạn cho thông báo thử
4. Xác minh email đến mà không có cảnh báo spam

### Bước 6: Lưu và Kích hoạt

Lưu cấu hình và đặt tài khoản thành **Hoạt động**. Đánh dấu nó là **Mặc định** nếu nó nên là tài khoản email chính.

## Mẫu Email

Spwig bao gồm 30+ mẫu email cho mọi sự kiện giao dịch. Đi đến **Cài đặt > Mẫu Email** để quản lý chúng.

### Loại Mẫu

Các mẫu bao gồm tất cả các sự kiện cửa hàng bao gồm:
- **Vòng đời Đơn hàng** — Xác nhận, đang xử lý, đã giao, đã nhận, đã hủy
- **Thanh toán** — Hóa đơn, xác nhận hoàn tiền, thanh toán thất bại
- **Tài khoản Khách hàng** — Chào mừng, khôi phục mật khẩu, xác minh email
- **Thẻ Quà tặng** — Giao hàng, thông báo số dư
- **Vận chuyển** — Cập nhật theo dõi, xác nhận giao hàng
- **Sản phẩm Số** — Liên kết tải xuống, khóa giấy phép
- **Tiếp thị** — Khôi phục giỏ hàng bỏ lỡ, yêu cầu đánh giá

### Tùy chỉnh Mẫu

1. Đi đến danh sách mẫu
2. Nhấp vào một mẫu để chỉnh sửa
3. Sửa tiêu đề, tiêu đề, nội dung chính và chân trang
4. Sử dụng các biến mẫu (ví dụ: `{{ order.number }}`, `{{ customer.name }}`) cho nội dung động
5. Xem trước email trước khi lưu

### Hỗ trợ Nhiều Ngôn ngữ

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

Mẫu email hỗ trợ nhiều ngôn ngữ:
- Mỗi mẫu có thể có bản dịch cho tất cả các ngôn ngữ đang hoạt động của cửa hàng bạn
- Hệ thống gửi email bằng ngôn ngữ ưa thích của khách hàng
- **Chuỗi dự phòng ngôn ngữ** — Nếu không có bản dịch, hệ thống sẽ chuyển sang ngôn ngữ mặc định của cửa hàng
- Sử dụng tính năng **Dịch AI** để tự động dịch các mẫu sang các ngôn ngữ khác

### Nhân bản Mẫu

Để tạo một phiên bản tùy chỉnh của mẫu hệ thống:
1. Mở mẫu bạn muốn chỉnh sửa
2. Nhấp vào **Nhân bản Mẫu**
3. Chỉnh sửa phiên bản đã nhân bản
4. Bản nhân bản có ưu tiên cao hơn so với mẫu hệ thống gốc

## Hàng đợi Email

Giám sát email đi tại **Cài đặt > Hàng đợi Email**:

- **Trong hàng đợi** — Email đang chờ được gửi
- **Đang gửi** — Đang được truyền tải
- **Đã gửi** — Đã được giao thành công
- **Thất bại** — Không thể giao (kèm chi tiết lỗi)
- **Bật lại** — Bị từ chối bởi máy chủ email của người nhận

Nhấp vào bất kỳ email nào để xem chi tiết đầy đủ bao gồm người nhận, tiêu đề, thời gian gửi và trạng thái giao hàng.

## Theo dõi Giao hàng

Theo dõi mức độ tương tác với email:
- **Mở** — Số lượng người nhận đã mở email
- **Nhấp** — Số lần nhấp vào liên kết trong email
- **Bật lại** — Theo dõi bật lại cứng và mềm
- **Khiếu nại** — Báo cáo spam từ người nhận

## Nhiều Tài khoản

Bạn có thể cấu hình nhiều tài khoản email:
- **Tài khoản Mặc định** — Được sử dụng cho tất cả email đi trừ khi bị ghi đè
- **Dự phòng** — Nếu tài khoản mặc định thất bại, email sẽ được đưa vào hàng đợi để thử lại
- Sử dụng các tài khoản khác nhau cho các mục đích khác nhau (ví dụ: một tài khoản cho email giao dịch, một tài khoản khác cho tiếp thị)

## Chế độ Giao hàng Email

Điều hướng đến **Cài đặt > Cài đặt Cửa hàng** để kiểm soát cách cửa hàng của bạn xử lý email đi. Các cài đặt này hữu ích trong quá trình phát triển và kiểm thử.

| Chế độ | Mô tả |
|------|-------------|
| **Trực tiếp** | Email được giao bình thường cho người nhận thực |
| **Tạm dừng** | Email được giữ trong hàng đợi và không được gửi cho đến khi bạn chuyển lại sang Trực tiếp |
| **Chỉ ghi log** | Email được ghi vào hộp thư đi nhưng không bao giờ được giao |

### Email Chuyển hướng Kiểm thử

Đặt một địa chỉ **Email Chuyển hướng Kiểm thử** để chặn tất cả email đi và chuyển hướng chúng đến một địa chỉ duy nhất. Khi được đặt, mọi email — bất kể người nhận thực là ai — sẽ được gửi đến địa chỉ đó thay vì người nhận gốc. Điều này hữu ích để kiểm thử các mẫu email mà không vô tình gửi cho khách hàng thực. Để trống để gửi email cho người nhận thực.

### Danh sách trắng Email Sandbox

Trong chế độ sandbox hoặc phát triển, bạn có thể hạn chế việc giao email cho một danh sách trắng các địa chỉ được phê duyệt. Chỉ các email gửi đến các địa chỉ trong danh sách trắng mới được giao. Tất cả các email khác sẽ được ghi log nhưng không bao giờ được gửi. Email quản trị viên luôn được bao gồm tự động. Bạn có thể thêm tối đa 10 địa chỉ.

## Mẹo

- Bắt đầu với máy chủ **SMTP tích hợp** để thiết lập nhanh, sau đó chuyển sang nhà cung cấp bên ngoài nếu bạn cần khối lượng gửi cao hơn hoặc khả năng giao hàng tốt hơn.
- Luôn cấu hình các bản ghi **SPF, DKIM và DMARC** — nếu không có chúng, email có nhiều khả năng rơi vào thư mục spam hơn.
- Gửi một **email kiểm thử** sau bất kỳ thay đổi cấu hình nào để xác nhận việc giao hàng hoạt động.
- Giám sát hàng đợi email thường xuyên để tìm các email **thất bại** hoặc **bật lại** — những điều này cho thấy các vấn đề về khả năng giao hàng.
- Sử dụng một **địa chỉ người gửi chuyên nghiệp** (ví dụ: orders@yourstore.com) thay vì địa chỉ email miễn phí để tăng độ tin cậy và khả năng giao hàng.
- Giữ các mẫu của bạn ngắn gọn — email giao dịch nên cung cấp thông tin nhanh chóng, không phải là bản tin tiếp thị.