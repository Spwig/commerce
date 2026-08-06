---
title: Cài đặt thanh toán
---

Các nhà cung cấp thanh toán kết nối cửa hàng của bạn với cổng thanh toán để bạn có thể chấp nhận thẻ tín dụng, ví kỹ thuật số và các phương thức thanh toán khác tại bước thanh toán. Spwig hỗ trợ nhiều nhà cung cấp cùng lúc, mang lại cho khách hàng của bạn các lựa chọn thanh toán linh hoạt.

![Các nhà cung cấp thanh toán](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Các nhà cung cấp có sẵn

| Nhà cung cấp | Mô tả |
|----------|-------------|
| **Stripe** | Thẻ tín dụng, Apple Pay, Google Pay và 135+ loại tiền tệ |
| **PayPal** | Số dư PayPal, thẻ tín dụng/thẻ ghi nợ và tùy chọn Thanh toán sau này |
| **Airwallex** | Các giao dịch đa tiền tệ tối ưu cho thương mại xuyên biên giới |
| **Square** | Thanh toán trực tiếp và trực tuyến với hỗ trợ POS tích hợp |
| **Revolut** | Các giao dịch châu Âu nhanh chóng với tỷ giá hối đoái cạnh tranh |

## Kết nối nhà cung cấp

Truy cập **Cài đặt > Nhà cung cấp thanh toán** và nhấp **Kết nối nhà cung cấp** để khởi động trình hướng dẫn cài đặt.

### Bước 1: Chọn nhà cung cấp

Chọn từ các nhà cung cấp thanh toán có sẵn. Mỗi thẻ hiển thị các tính năng và khu vực được nhà cung cấp hỗ trợ.

### Bước 2: Hướng dẫn thiết lập

Xem hướng dẫn thiết lập cụ thể cho nhà cung cấp. Điều này bao gồm:
- Cách tạo tài khoản với nhà cung cấp (nếu bạn chưa có)
- Vị trí tìm thấy thông tin API của bạn trong bảng điều khiển nhà cung cấp
- Các điều kiện tiên quyết (ví dụ: xác minh doanh nghiệp)

### Bước 3: Nhập thông tin xác thực

Nhập thông tin API của bạn:
- **Khóa API / Khóa bí mật** — Thông tin xác thực của bạn từ bảng điều khiển nhà cung cấp
- **Chế độ thanh toán** — Chọn cách khách hàng tương tác với biểu mẫu thanh toán:

| Chế độ | Mô tả |
|------|-------------|
| **Hosted** | Khách hàng được chuyển hướng đến trang thanh toán của nhà cung cấp (ví dụ: Stripe Checkout). Thiết lập đơn giản nhất, tuân thủ PCI do nhà cung cấp xử lý. |
| **Integrated** | Biểu mẫu thanh toán được nhúng trực tiếp vào trang thanh toán của bạn. Trải nghiệm liền mạch, nhưng yêu cầu SDK JavaScript của nhà cung cấp. |

- **Chế độ Sandbox / Live** — Bắt đầu với chế độ Sandbox để kiểm tra, sau đó chuyển sang chế độ live khi sẵn sàng

### Bước 4: Kiểm tra kết nối

Nhấp **Kiểm tra kết nối** để xác minh thông tin xác thực của bạn là hợp lệ. Trình hướng dẫn kiểm tra:
- Xác thực khóa API
- Quyền truy cập tài khoản
- Khả năng truy cập điểm cuối Webhook

### Bước 5: Cấu hình và lưu

Hoàn tất cài đặt nhà cung cấp:
- **Kích hoạt** — Bật hoặc tắt nhà cung cấp
- **Nhà cung cấp mặc định** — Thiết lập làm phương thức thanh toán chính tại bước thanh toán
- **Tên hiển thị** — Tên hiển thị cho khách hàng trong bước thanh toán
- **Thứ tự hiển thị** — Điều khiển thứ tự các nhà cung cấp xuất hiện tại bước thanh toán (số nhỏ hơn sẽ xuất hiện trước)

## Bảng điều khiển thanh toán

Truy cập **Cài đặt > Bảng điều khiển thanh toán** để có cái nhìn tổng quan về hoạt động thanh toán của bạn:

### Hành động cần thực hiện

Các thẻ cảnh báo ở đầu trên sẽ làm nổi bật các vấn đề cần chú ý:
- **Giao dịch thất bại** — Các khoản thanh toán không thể được xử lý
- **Giao dịch chờ thu** — Các khoản thanh toán đã được phê duyệt nhưng đang chờ thu
- **Lỗi kết nối** — Các nhà cung cấp có vấn đề về kết nối

### Phân tích doanh thu

- **Biểu đồ doanh thu** — Phân tích trực quan về khối lượng thanh toán theo thời gian, được nhóm theo ngày, tuần hoặc tháng
- **Chỉ số hiệu suất** — Tổng doanh thu, tỷ lệ thành công, giá trị giao dịch trung bình và tỷ lệ hoàn tiền
- **So sánh nhà cung cấp** — Các thẻ hiệu suất song song cho mỗi nhà cung cấp đã kết nối

### Phân tích giao dịch

- **Phân phối trạng thái** — Số lượng giao dịch hoàn thành, đang chờ, thất bại và hoàn tiền
- **Tỷ lệ phương thức thanh toán** — Phương thức thanh toán mà khách hàng sử dụng nhiều nhất (thẻ tín dụng, PayPal, ví kỹ thuật số)

## Quản lý phương thức thanh toán

Mỗi nhà cung cấp hỗ trợ các phương thức thanh toán khác nhau. Bạn có thể bật hoặc tắt các phương thức cụ thể theo quốc gia:

1. Truy cập trang cấu hình của nhà cung cấp
2. Cuộn xuống phần **Phương thức thanh toán**
3. Bật hoặc tắt các phương thức riêng lẻ
4. Sử dụng điều khiển cấp quốc gia để giới hạn phương thức cho các thị trường cụ thể

Điều này rất hữu ích khi một phương thức thanh toán phổ biến ở một khu vực nhưng không phổ biến ở khu vực khác (ví dụ: iDEAL ở Hà Lan, Bancontact ở Bỉ).

## Webhooks

Webhooks giúp cửa hàng của bạn đồng bộ hóa với nhà cung cấp thanh toán theo thời gian thực.

Chúng xử lý các sự kiện như:
- Giao dịch thanh toán hoàn tất hoặc thất bại
- Hoàn tiền được xử lý
- Tranh chấp và hoàn tiền được mở
- Gia hạn đăng ký

### Cài đặt tự động

Khi bạn kết nối một nhà cung cấp, Spwig sẽ tự động đăng ký một điểm cuối webhook với nhà cung cấp. URL webhook sẽ được hiển thị trên trang cấu hình của nhà cung cấp để tham khảo.

### Giám sát Webhook

Mỗi webhook đến đều được ghi lại với:
- **Loại sự kiện** (ví dụ: payment_intent.succeeded)
- **Thời gian** và trạng thái xử lý
- **Payload** để gỡ lỗi

Nếu webhook không thể xử lý, nó sẽ được ghi lại dưới dạng lỗi để bạn có thể điều tra.

## Sử dụng Nhiều Nhà Cung Cấp

Bạn có thể kết nối nhiều nhà cung cấp thanh toán cùng lúc:

- **Nhà cung cấp mặc định** — Nhà cung cấp được chọn mặc định tại bước thanh toán. Đánh dấu một nhà cung cấp là mặc định trong cấu hình của nó.
- **Thứ tự sắp xếp** — Điều khiển thứ tự hiển thị tại bước thanh toán. Khách hàng sẽ thấy tất cả các nhà cung cấp đang hoạt động và có thể chọn nhà cung cấp ưa thích của họ.
- **Chuyển tiếp** — Nếu một nhà cung cấp gặp sự cố, khách hàng vẫn có thể thanh toán bằng một nhà cung cấp thay thế.

## Một số mẹo

- Bắt đầu với **Stripe** hoặc **PayPal** — chúng hỗ trợ phạm vi phương thức thanh toán và khu vực rộng nhất.
- Sử dụng **chế độ thử nghiệm/sandbox** để xử lý các giao dịch thử trước khi triển khai. Mỗi nhà cung cấp đều có số thẻ thử nghiệm trong tài liệu của họ.
- Kích hoạt **nhiều nhà cung cấp** để khách hàng có phương thức thanh toán dự phòng nếu một nhà cung cấp gặp sự cố.
- Đặt **thứ tự sắp xếp thấp** cho nhà cung cấp ưa thích của bạn để nó hiển thị đầu tiên tại bước thanh toán.
- Theo dõi bảng điều khiển thanh toán hàng tuần để phát hiện sớm các giao dịch thất bại và vấn đề kết nối.
- Luôn giữ **thông tin xác thực API** an toàn — chúng được lưu trữ mã hóa trong cơ sở dữ liệu nhưng không bao giờ nên được chia sẻ.