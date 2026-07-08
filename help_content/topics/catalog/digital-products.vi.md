---
title: Sản phẩm số
---

Sản phẩm số cho phép bạn bán các tệp tải xuống, giấy phép phần mềm và các hàng hóa phi vật lý khác. Spwig hỗ trợ sản phẩm số độc lập cũng như các sản phẩm hỗn hợp kết hợp cả giao hàng vật lý và số.

![Nhà cung cấp giấy phép](/static/core/admin/img/help/digital-products/license-providers.webp)

## Loại sản phẩm số

### Sản phẩm số độc lập

Chọn **Loại sản phẩm** là **Sản phẩm số** cho các mặt hàng thuần túy số:
- Ứng dụng phần mềm
- Sách điện tử và PDF
- Tệp âm thanh và nhạc
- Tác phẩm nghệ thuật số và mẫu thiết kế

### Sản phẩm hỗn hợp

Bất kỳ loại sản phẩm nào cũng có thể bao gồm giao hàng số bằng cách đánh dấu **Là sản phẩm số** trên tab Thông tin cơ bản. Điều này hữu ích cho:
- **Sản phẩm số có thể thay đổi** — Phần mềm với các phiên bản Cơ bản/Chuyên nghiệp/Doanh nghiệp
- **Sản phẩm số có thể tùy chỉnh** — Tài sản số được thiết kế riêng
- **Gói vật lý + số** — Một cuốn sách bao gồm tệp tải xuống số

## Thiết lập sản phẩm số

### Bước 1: Tạo sản phẩm

1. Di chuyển đến **Sản phẩm > Tất cả sản phẩm** và nhấn **+ Thêm sản phẩm**
2. Thiết lập **Loại sản phẩm** thành **Sản phẩm số** (hoặc đánh dấu **Là sản phẩm số** trên loại sản phẩm khác)
3. Điền chi tiết sản phẩm (tên, mô tả, giá)
4. Lưu sản phẩm

### Bước 2: Thêm tệp tải xuống

1. Chuyển đến tab **Kho hàng** của sản phẩm
2. Trong phần **Tệp số**, tải lên các tệp khách hàng sẽ nhận được sau khi mua
3. Với mỗi tệp, bạn có thể thiết lập:
   - **Tên tệp** — Tên hiển thị cho khách hàng
   - **Giới hạn tải xuống** — Số lần tối đa tệp có thể được tải xuống (0 = không giới hạn)
   - **Ngày hết hạn** — Số ngày mà liên kết tải xuống vẫn còn hiệu lực

### Bước 3: Cấu hình giao hàng giấy phép (Tùy chọn)

Nếu sản phẩm số của bạn yêu cầu khóa giấy phép:

1. Di chuyển đến **Cài đặt > Quản lý giấy phép**
2. Kết nối nhà cung cấp giấy phép (xem dưới đây)
3. Trên biểu mẫu chỉnh sửa sản phẩm, chỉ định nhà cung cấp giấy phép

## Nhà cung cấp giấy phép

Nhà cung cấp giấy phép là các dịch vụ bên ngoài tạo và quản lý tự động các khóa giấy phép phần mềm khi khách hàng mua sản phẩm của bạn.

### Các loại nhà cung cấp có sẵn

| Nhà cung cấp | Mô tả |
|--------------|--------|
| **Máy chủ giấy phép tích hợp của Spwig** | Tạo khóa giấy phép đơn giản được tích hợp trong nền tảng |
| **Keygen.sh** | API quản lý giấy phép đầy đủ tính năng |
| **LicenseSpring** | Quản lý giấy phép doanh nghiệp |
| **Cryptlex** | Giấy phép phần mềm với hỗ trợ ngoại tuyến |
| **API tùy chỉnh** | Kết nối bất kỳ hệ thống giấy phép nào qua API REST |

### Kết nối nhà cung cấp giấy phép

1. Di chuyển đến **Cài đặt > Quản lý giấy phép**
2. Nhấn **Kết nối nhà cung cấp**
3. Làm theo hướng dẫn thiết lập:
   - **Bước 1** — Chọn loại nhà cung cấp
   - **Bước 2** — Thiết lập cài đặt chung
   - **Bước 3** — Nhập thông tin xác thực API
4. Kiểm tra kết nối để xác nhận hoạt động
5. Lưu cấu hình

### Thẻ nhà cung cấp

Mỗi nhà cung cấp đã kết nối hiển thị:
- **Thẻ trạng thái** — Hoạt động/Không hoạt động và trạng thái kết nối
- **Điểm cuối API** — URL máy chủ đã cấu hình
- **Khả năng đồng bộ** — Hỗ trợ đồng bộ hóa Đơn hàng, Kích hoạt và Hủy kích hoạt
- **Nút hành động** — Cấu hình, Kiểm tra và Đồng bộ ngay

### Khả năng đồng bộ

Nhà cung cấp giấy phép có thể đồng bộ hóa trên ba sự kiện:

- **Đơn hàng** — Tự động tạo khóa giấy phép khi khách hàng hoàn tất mua hàng
- **Kích hoạt** — Theo dõi khi khách hàng kích hoạt giấy phép của họ
- **Hủy kích hoạt** — Xử lý hủy kích hoạt giấy phép cho hoàn tiền hoặc chuyển nhượng

## Trải nghiệm khách hàng

### Sau khi mua hàng

Khi khách hàng mua sản phẩm số:

1. **Xác nhận đơn hàng** — Hiển thị rằng giao hàng số được bao gồm
2. **Giao hàng qua email** — Liên kết tải xuống và/hoặc khóa giấy phép được gửi tự động
3. **Trang tài khoản** — Khách hàng có thể truy cập các tệp tải xuống của họ từ bảng điều khiển tài khoản
4. **Trang tải xuống** — Liên kết tải xuống an toàn, có thời hạn

### An toàn tải xuống

Các tệp tải xuống sản phẩm số được bảo vệ bởi:
- Các mã token tải xuống duy nhất, có thời hạn
- Giới hạn số lần tải xuống tùy chọn
- Ngày hết hạn sau đó liên kết trở nên không còn hiệu lực
- Yêu cầu đăng nhập (cho khách hàng đã đăng ký)

## Một số lưu ý

- Thiết lập giới hạn tải xuống hợp lý (3-5 lần tải xuống) để ngăn chặn lạm dụng nhưng vẫn cho phép tải lại.
- Sử dụng số ngày hết hạn phù hợp với thời gian hỗ trợ của bạn (ví dụ: 365 ngày cho một năm truy cập).
- Kiểm tra toàn bộ quy trình mua hàng với đơn hàng kiểm tra để đảm bảo liên kết tải xuống và khóa giấy phép được giao đúng cách.
- Với sản phẩm phần mềm, kết nối nhà cung cấp giấy phép để tự động tạo khóa thay vì quản lý khóa thủ công.
- Sử dụng tính năng sản phẩm hỗn hợp khi bán các mặt hàng vật lý bao gồm các tiện ích số (ví dụ: sách in + PDF).
