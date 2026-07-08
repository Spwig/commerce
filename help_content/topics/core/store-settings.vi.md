---
title: Cấu hình Cài đặt Cửa hàng
---

Cài đặt Cửa hàng là nơi trung tâm để cấu hình danh tính, địa phương hóa, thương hiệu và các tùy chọn vận hành của cửa hàng của bạn. Truy cập **Cài đặt > Cài đặt Cửa hàng** để bắt đầu.

![Cài đặt cửa hàng tab tổng quan](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Tab Tổng quan

Tab **Tổng quan** chứa các cài đặt danh tính cốt lõi của cửa hàng của bạn.

### Danh tính Cửa hàng

- **Tên Cửa hàng** — Tên hiển thị được hiển thị trong tiêu đề trang, email và tiêu đề quản trị.
- **Chú thích** — Mô tả ngắn gọn về cửa hàng của bạn, được sử dụng trong SEO và chia sẻ mạng xã hội.
- **URL Trang web** — Địa chỉ web công khai của cửa hàng của bạn. Điều này được sử dụng trong email, tạo bản đồ trang web và xây dựng liên kết.

### Thông tin Liên hệ

- **Email Liên hệ** — Nhận thông báo đơn hàng và được hiển thị trong giao tiếp với khách hàng.
- **Số điện thoại** — Số điện thoại hỗ trợ tùy chọn được hiển thị trong chân trang và email.

### Địa chỉ Kinh doanh

Nhập địa chỉ đầy đủ của bạn (đường, thành phố, tỉnh, mã bưu chính, quốc gia). Điều này được sử dụng cho:
- Tính toán nguồn vận chuyển
- Tính toán thuế
- Yêu cầu pháp lý và hóa đơn

## Thương hiệu

### Biểu tượng

Tải lên biểu tượng cửa hàng của bạn (khuyến khích PNG hoặc SVG, ~200x50px với nền trong suốt). Biểu tượng xuất hiện ở:
- Tiêu đề cửa hàng
- Mẫu email
- Bảng điều khiển quản trị

### Biểu tượng yêu thích (Favicon)

Tải lên biểu tượng yêu thích hình vuông (ICO hoặc PNG, 32x32px). Nó xuất hiện như:
- Biểu tượng tab trình duyệt
- Biểu tượng bookmark
- Biểu tượng màn hình chính di động

## Địa phương hóa

### Ngôn ngữ Mặc định

Chọn ngôn ngữ chính của cửa hàng từ 10 tùy chọn được hỗ trợ:

| Ngôn ngữ | Mã |
|----------|------|
| Tiếng Anh | en |
| Tiếng Tây Ban Nha | es |
| Tiếng Pháp | fr |
| Tiếng Đức | de |
| Tiếng Bồ Đào Nha | pt |
| Tiếng Nhật | ja |
| Tiếng Trung giản thể | zh-hans |
| Tiếng Trung truyền thống | zh-hant |
| Tiếng Nga | ru |
| Tiếng Ả Rập | ar |

Ngôn ngữ mặc định kiểm soát ngôn ngữ giao diện quản trị và làm nền tảng cho nội dung cửa hàng.

### Khu vực giờ

Chọn khu vực giờ của cửa hàng để có thời gian đặt hàng chính xác, khuyến mãi được lên lịch và báo cáo.

### Tiền tệ

- **Tiền tệ Mặc định** — Tiền tệ chính cho định giá và kế toán.
- **Tiền tệ Đa ngôn ngữ** — Bật để cho phép khách hàng xem giá theo tiền tệ ưa thích của họ với chuyển đổi tự động sử dụng tỷ giá hối đoái thời gian thực.

Cấu hình tiền tệ bổ sung trong **Cài đặt > Cài đặt Cửa hàng > Tiền tệ**.

## Cài đặt Thương mại điện tử

### Mua hàng Khách truy cập

Cho phép mua hàng mà không cần tạo tài khoản:
- Luồng thanh toán nhanh hơn
- Giảm ma sát cho khách hàng mới
- Thu thập ít dữ liệu khách hàng hơn

### Định dạng Số đơn hàng

Tùy chỉnh cách hiển thị số đơn hàng:
- **Tiền tố** — ví dụ: "ORD-"
- **Số bắt đầu** — Số đơn hàng đầu tiên
- **Bù đắp** — ví dụ: 00001

### Mặc định Kho hàng

- **Theo dõi Kho hàng** — Bật theo dõi tồn kho toàn cầu
- **Ngưỡng Kho hàng Thấp** — Mức cảnh báo (mặc định: 5 đơn vị)
- **Cho phép Đặt hàng Trả sau** — Chấp nhận đơn hàng khi hết hàng

## Cài đặt Email

### Thông tin Người gửi

- **Tên Người gửi** — Hiển thị như người gửi email (thường là tên cửa hàng của bạn)
- **Email Người gửi** — Phải đến từ một miền đã xác minh
- **Email Trả lời** — Nơi khách hàng trả lời được định hướng

### Nhà cung cấp Email

Cấu hình dịch vụ giao email của bạn trong **Cài đặt > Cấu hình Email**. Các nhà cung cấp được hỗ trợ bao gồm SMTP, SendGrid, Mailgun và Amazon SES.

## Pháp lý & Tuân thủ

Thêm chính sách cửa hàng của bạn để đáp ứng các yêu cầu pháp lý:

- **Điều khoản & Điều kiện** — Yêu cầu cho thanh toán; khách hàng phải chấp nhận trước khi mua hàng
- **Chính sách Quyền riêng tư** — Tuân thủ GDPR/CCPA; được liên kết trong chân trang
- **Chính sách Trả hàng** — Định nghĩa cửa sổ trả hàng, điều kiện và quy trình hoàn tiền của bạn

## Chế độ Bảo trì

Bật chế độ bảo trì để tạm thời đưa cửa hàng của bạn offline:
- Hiển thị một thông báo bảo trì tùy chỉnh cho khách truy cập
- Giới hạn truy cập chỉ cho người dùng quản trị
- Hữu ích khi cập nhật hoặc di chuyển lớn

## Cài đặt Thuế

Cấu hình thu thuế tại **Cài đặt > Cài đặt Thuế**:

1. **Phương pháp Tính thuế** — Theo địa chỉ vận chuyển, địa chỉ thanh toán hoặc vị trí cửa hàng
2. **Mức thuế** — Định nghĩa mức thuế theo khu vực và lớp thuế sản phẩm
3. **Hiển thị Thuế** — Hiển thị giá cả có thuế, không thuế hoặc cả hai

## Một số lưu ý

- Đặt khu vực giờ chính xác trước khi xử lý bất kỳ đơn hàng nào — nó ảnh hưởng đến tất cả các thời gian và báo cáo.
- Bật mua hàng khách truy cập để cải thiện tỷ lệ chuyển đổi.
- Điền đầy đủ địa chỉ kinh doanh để tính toán vận chuyển và thuế chính xác.
- Tải lên cả biểu tượng và favicon để có trải nghiệm thương hiệu chuyên nghiệp.
- Thường xuyên xem lại các trang pháp lý của bạn để đảm bảo tuân thủ các quy định địa phương.

## Khắc phục sự cố

**Các thay đổi không hiển thị trên cửa hàng:**
- Xóa bộ nhớ cache trình duyệt của bạn
- Chạy lệnh xóa cache từ bảng điều khiển quản trị
- Kiểm tra xem chế độ bảo trì có bị kích hoạt không

**Email không được gửi:**
- Xác minh cài đặt nhà cung cấp email của bạn trong Cấu hình Email
- Kiểm tra miền "Email Người gửi" đã được xác minh
- Thử kiểm tra kết nối từ trang thiết lập nhà cung cấp

**Chuyển đổi tiền tệ không hoạt động:**
- Xác minh nhà cung cấp tỷ giá hối đoái của bạn đã được kết nối
- Kiểm tra thông tin xác thực API trong cài đặt tỷ giá hối đoái
- Thử cập nhật tỷ giá thủ công

