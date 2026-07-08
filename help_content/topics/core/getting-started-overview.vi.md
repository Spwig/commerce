---
title: Bắt đầu với Cửa hàng Spwig của bạn
---

Chào mừng bạn đến với Spwig! Hướng dẫn này cung cấp cho bạn một tour nhanh về bảng điều khiển quản trị của bạn và hướng dẫn bạn qua các bước thiết yếu để triển khai cửa hàng trực tuyến của bạn.

## Bảng điều khiển

Sau khi đăng nhập, bạn sẽ đến **Bảng điều khiển Cửa hàng** — trung tâm kiểm soát để theo dõi hiệu suất cửa hàng.

![Bảng điều khiển quản trị](/static/core/admin/img/help/getting-started-overview/admin-dashboard.webp)

Bảng điều khiển hiển thị:
- **Hành động cần thực hiện** — đơn hàng đang chờ xử lý, cảnh báo hàng tồn kho thấp, giỏ hàng bị bỏ lại và các bản cập nhật có sẵn
- **Doanh thu bán hàng** — biểu đồ doanh thu và đơn hàng được nhóm theo ngày, tuần hoặc tháng
- **Điều hướng nhanh** — nhảy đến bất kỳ phần nào từ danh sách thả xuống

## Thanh bên quản trị

Thanh bên bên trái tổ chức mọi thứ thành các phần:

| Phần | Nội dung bên trong |
|---------|--------------|
| **Sản phẩm** | Danh mục sản phẩm, danh mục, kế hoạch đăng ký, thẻ quà tặng |
| **Đơn hàng** | Quản lý đơn hàng, giỏ hàng, vận chuyển, cài đặt vận chuyển, thuế |
| **Khách hàng** | Hồ sơ khách hàng, phân tích, cài đặt LTV |
| **Tìm kiếm** | Phân tích tìm kiếm, từ đồng nghĩa, chuyển hướng |
| **Marketing** | Khuyến mãi, phiếu giảm giá, đại lý, trung thành, blog, thông báo |
| **Cài đặt** | Cài đặt cửa hàng, thanh toán, thiết kế, email, bản dịch, POS |

Nhấn vào **biểu tượng hamburger** (☰) ở phía dưới để thu gọn thanh bên để có thêm không gian màn hình.

## Các bước đầu tiên

### 1. Cấu hình Cài đặt Cửa hàng

Đi đến **Cài đặt > Cài đặt Cửa hàng** để thiết lập danh tính cửa hàng của bạn:
- Tên cửa hàng và khẩu hiệu
- URL trang web
- Favicon và logo
- Ngôn ngữ và múi giờ mặc định

Xem [Cấu hình Cài đặt Cửa hàng](#) để biết chi tiết.

### 2. Thêm Sản phẩm của bạn

Di chuyển đến **Sản phẩm > Tất cả Sản phẩm** và nhấn **+ Thêm Sản phẩm**:
- Nhập tên sản phẩm, mô tả và SKU
- Tải lên hình ảnh qua Thư viện Truyền thông
- Thiết lập giá cả và tùy chọn bán hàng
- Cấu hình theo dõi tồn kho

Xem [Thêm Sản phẩm](#) để có hướng dẫn đầy đủ.

### 3. Thiết lập Thanh toán

Đi đến **Cài đặt > Bảng điều khiển Thanh toán** để kết nối nhà cung cấp thanh toán:
- Xem các nhà cung cấp có sẵn (Stripe, PayPal và nhiều hơn nữa)
- Theo dõi hướng dẫn thiết lập để nhập thông tin API của bạn
- Kiểm tra kết nối trước khi đi vào sản xuất

### 4. Thiết lập Vận chuyển

Truy cập **Đơn hàng > Vận chuyển** để thiết lập các tùy chọn giao hàng:
- Tạo phương thức vận chuyển với giá cố định
- Định nghĩa các vùng vận chuyển theo quốc gia hoặc khu vực
- Tùy chọn kết nối tích hợp vận chuyển để có giá thời gian thực

Xem [Thiết lập Vận chuyển](#) để biết chi tiết.

### 5. Tùy chỉnh Thiết kế của bạn

Di chuyển đến **Cài đặt > Thiết kế & Giao diện** để cá nhân hóa cửa hàng của bạn:
- Chọn giao diện đang hoạt động
- Tùy chỉnh thương hiệu (màu sắc, typography, khoảng cách)
- Xây dựng phần đầu và chân trang bằng công cụ kéo thả
- Cấu hình menu điều hướng

Xem [Thiết kế & Giao diện](#) để biết chi tiết.

### 6. Bắt đầu vận hành

Khi mọi thứ đã sẵn sàng:
1. Đặt trạng thái sản phẩm thành **Đã xuất bản**
2. Kiểm tra URL cửa hàng của bạn trong Cài đặt Cửa hàng
3. Kiểm tra quy trình thanh toán bằng cách đặt một đơn hàng kiểm tra
4. Đảm bảo trạng thái trang web của bạn hiển thị **Trang web đang hoạt động**

## Một số mẹo

- Sử dụng nút **Trợ giúp** ở góc trên bên phải của bất kỳ trang nào để nhận hỗ trợ theo ngữ cảnh cho trang bạn đang ở.
- Các thẻ **Hành động cần thực hiện** trên bảng điều khiển liên kết trực tiếp đến các mục cần chú ý — nhấn vào chúng để nhảy trực tiếp đến đó.
- Đánh dấu trang bảng điều khiển là điểm bắt đầu hàng ngày của bạn để theo dõi tình trạng cửa hàng.