---
title: Cài đặt vận chuyển
---

Hướng dẫn này giải thích cách cấu hình vận chuyển cho cửa hàng của bạn — từ thiết lập phương pháp vận chuyển cơ bản đến kết nối tích hợp nhà cung cấp vận chuyển trực tiếp để có giá vận chuyển thời gian thực.

## Tổng quan về vận chuyển

Spwig cung cấp hai phương pháp vận chuyển:

- **Phương pháp vận chuyển thủ công** — Các phương pháp có giá cố định mà bạn định nghĩa (ví dụ: "Vận chuyển tiêu chuẩn — 5,99 USD")
- **Tích hợp nhà cung cấp** — Giá vận chuyển thời gian thực từ các nhà cung cấp như FedEx, UPS và DHL

Bạn có thể sử dụng phương pháp này hoặc phương pháp kia, hoặc kết hợp cả hai.

## Phương pháp vận chuyển

Phương pháp vận chuyển là các tùy chọn khách hàng nhìn thấy khi thanh toán. Di chuyển đến **Đơn hàng > Giao hàng** trong thanh bên để quản lý chúng.

![Phương pháp vận chuyển](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### Tạo phương pháp vận chuyển

1. Nhấp **Thêm phương pháp vận chuyển**
2. Điền thông tin:
   - **Tên** — Tên hiển thị cho khách hàng (ví dụ: "Giao hàng nhanh")
   - **Mô tả** — Mô tả ngắn gọn về dịch vụ
   - **Giá** — Chi phí vận chuyển cố định
   - **Thời gian giao hàng dự kiến** — Thời gian giao hàng ước tính (ví dụ: "3-5 ngày làm việc")
3. Nhấp **Lưu**

## Khu vực vận chuyển

Khu vực vận chuyển xác định các khu vực địa lý mà phương pháp vận chuyển của bạn áp dụng. Di chuyển đến phần **Khu vực vận chuyển** để quản lý chúng.

![Khu vực vận chuyển](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### Tạo khu vực

1. Nhấp **Thêm khu vực vận chuyển**
2. Cấu hình khu vực:
   - **Tên khu vực** — Tên nội bộ (ví dụ: "Trong nước Mỹ", "Châu Âu")
   - **Quốc gia** — Chọn các quốc gia thuộc khu vực này
   - **Tỉnh/Thành phố** — Tùy chọn thu hẹp xuống các tỉnh cụ thể
   - **Mẫu mã bưu điện** — Sử dụng mẫu như "9*" để nhắm đến các khu vực cụ thể
3. Gán phương pháp vận chuyển cho khu vực này
4. Nhấp **Lưu**

### Ưu tiên khu vực

Khi địa chỉ của khách hàng khớp với nhiều khu vực, khu vực cụ thể nhất sẽ được ưu tiên. Một khu vực có mục tiêu cấp tỉnh sẽ có quyền ưu tiên hơn khu vực cấp quốc gia.

## Tích hợp nhà cung cấp

Kết nối với các nhà cung cấp vận chuyển để cung cấp giá vận chuyển được tính toán thời gian thực tại lúc thanh toán.

![Nhà cung cấp vận chuyển](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### Các nhà cung cấp có sẵn

Duyệt và cài đặt nhà cung cấp vận chuyển từ thị trường.

![Nhà cung cấp vận chuyển](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

Các nhà cung cấp được hỗ trợ bao gồm:

- **FedEx** — Giao hàng, Giao hàng nhanh, Quốc tế
- **UPS** — Giao hàng, 2 ngày, Giao hàng đêm, Toàn cầu
- **DHL** — Giao hàng nhanh, Giao hàng thương mại điện tử
- **USPS** — Giao hàng ưu tiên, Giao hàng cấp một, Giao hàng thư báo
- Và nhiều hơn nữa có sẵn qua Thị trường

### Thiết lập nhà cung cấp

1. Đến trang nhà cung cấp vận chuyển và nhấp **Cài đặt** trên nhà cung cấp bạn chọn
2. Theo dõi hướng dẫn thiết lập:
   - **Bước 1** — Xem xét chi tiết nhà cung cấp
   - **Bước 2** — Cấu hình cài đặt chung
   - **Bước 3** — Nhập thông tin xác thực API của bạn (số tài khoản, khóa API, v.v.)
   - **Bước 4** — Kích hoạt các dịch vụ cụ thể (Giao hàng, Giao hàng nhanh, v.v.)
   - **Bước 5** — Kiểm tra kết nối
3. Sau khi kết nối, giá vận chuyển của nhà cung cấp sẽ xuất hiện tự động tại lúc thanh toán

### Thông tin xác thực API

Mỗi nhà cung cấp yêu cầu tài khoản API:

- **FedEx** — Đăng ký tại Trang web phát triển của FedEx, tạo ứng dụng và sao chép khóa API và bí mật của bạn
- **UPS** — Đăng ký tại Kit phát triển UPS, yêu cầu khóa truy cập
- **DHL** — Liên hệ DHL để nhận thông tin xác thực API qua cổng thông tin doanh nghiệp của họ

## Quy tắc vận chuyển

Tạo các quy tắc nâng cao để kiểm soát khi và cách phương pháp vận chuyển được cung cấp.

### Các quy tắc phổ biến

- **Miễn phí vận chuyển cho đơn hàng trên 50 USD** — Đặt mức tối thiểu cho giỏ hàng để được miễn phí vận chuyển
- **Giá cố định cho đơn hàng nhẹ** — Giá cố định khi trọng lượng đơn hàng dưới ngưỡng nhất định
- **Tắt giao hàng nhanh cho khu vực hẻo lánh** — Ẩn tùy chọn giao hàng nhanh dựa trên mã bưu điện
- **Markup tỷ lệ phần trăm** — Thêm phí xử lý dưới dạng tỷ lệ phần trăm của giá vận chuyển

### Tạo quy tắc

1. Di chuyển đến phần quy tắc vận chuyển
2. Nhấp **Thêm quy tắc**
3. Thiết lập điều kiện (tổng giỏ hàng, trọng lượng, khu vực, v.v.)
4. Định nghĩa hành động (điều chỉnh giá, ẩn phương pháp, kích hoạt miễn phí vận chuyển)
5. Lưu quy tắc

Các quy tắc được đánh giá theo thứ tự — quy tắc khớp đầu tiên sẽ được áp dụng.

## Vận chuyển miễn phí

### Vận chuyển miễn phí toàn cửa hàng

Kích hoạt vận chuyển miễn phí toàn cầu trong **Cài đặt > Cài đặt cửa hàng**:

- Bật **Vận chuyển miễn phí**
- Tùy chọn thiết lập giá trị đơn hàng tối thiểu
- Chọn các khu vực đủ điều kiện

### Vận chuyển miễn phí khuyến mãi

Tạo các ưu đãi miễn phí vận chuyển có thời hạn:

1. Đi đến **Tiếp thị > Bán hàng và khuyến mãi**
2. Tạo một khuyến mãi mới
3. Thiết lập điều kiện: "Tổng giỏ hàng trên X"
4. Thiết lập hành động: "Vận chuyển miễn phí"
5. Cấu hình ngày bắt đầu và kết thúc

## Vận chuyển quốc tế

Đối với các đơn hàng quốc tế, hãy đảm bảo sản phẩm của bạn có:

- **Mã HS** — Phân loại thuế theo hệ thống hài hòa
- **Quốc gia xuất xứ** — Quốc gia sản xuất
- **Giá trị hải quan** — Giá khai báo cho hải quan

Các trường này nằm trong tab **Kho hàng** của từng sản phẩm. Các nhà cung cấp sử dụng thông tin này để tạo tài liệu hải quan tự động.

## Mẹo

- Bắt đầu với phương pháp vận chuyển thủ công để cửa hàng của bạn hoạt động nhanh chóng, sau đó thêm tích hợp nhà cung cấp sau này.
- Tạo các khu vực vận chuyển cho các điểm đến phổ biến nhất của bạn trước.
- Luôn kiểm tra cấu hình vận chuyển của bạn bằng cách đặt các đơn hàng thử với các địa chỉ khác nhau.
- Sử dụng tính năng markup giá để bù đắp chi phí xử lý và đóng gói.
- Thiết lập ngưỡng vận chuyển miễn phí để tăng giá trị đơn hàng trung bình.