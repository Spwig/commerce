---
title: Quản lý đơn hàng
---

Hướng dẫn này bao gồm tất cả những gì bạn cần để quản lý đơn hàng của khách hàng — từ việc xem xét các đơn hàng mới đến xử lý vận chuyển và xử lý hoàn tiền.

## Danh sách đơn hàng

Truy cập **Đơn hàng > Tất cả đơn hàng** trong thanh bên để xem tất cả đơn hàng. Danh sách hiển thị số đơn hàng, trạng thái, khách hàng, tổng số tiền và ngày đặt hàng.

![Danh sách đơn hàng](/static/core/admin/img/help/manage-orders/order-list.webp)

Sử dụng các bộ lọc ở đầu trang để thu hẹp danh sách đơn hàng theo trạng thái, khoảng thời gian hoặc tìm kiếm theo số đơn hàng hoặc tên khách hàng.

## Chi tiết đơn hàng

Click vào bất kỳ đơn hàng nào để mở trang chi tiết. Tại đây bạn sẽ tìm thấy tất cả thông tin về đơn hàng được tổ chức thành các phần rõ ràng.

![Chi tiết đơn hàng](/static/core/admin/img/help/manage-orders/order-detail.webp)

### Thông tin đơn hàng

Phần đầu hiển thị:

- **Số đơn hàng** — Nhận dạng duy nhất cho đơn hàng này
- **Trạng thái** — Trạng thái đơn hàng hiện tại (Chờ xử lý, Đang xử lý, Đã vận chuyển, Đã giao hàng, Hoàn tất, Hủy bỏ)
- **Khách hàng** — Tên và email của khách hàng đã đặt hàng
- **Tạo lúc** — Thời điểm đơn hàng được đặt

### Các mặt hàng đơn hàng

Phần này liệt kê tất cả mặt hàng mà khách hàng đã đặt:

- Tên sản phẩm và SKU
- Số lượng đặt
- Giá đơn vị và tổng số tiền hàng
- Các phiếu giảm giá được áp dụng

### Chi tiết thanh toán

Hiển thị phương thức thanh toán được sử dụng, mã giao dịch và trạng thái thanh toán. Đối với các đơn hàng đang chờ thanh toán, bạn có thể theo dõi trạng thái của cổng thanh toán tại đây.

### Địa chỉ vận chuyển

Địa chỉ giao hàng của khách hàng. Nếu địa chỉ thanh toán khác, cả hai sẽ được hiển thị.

## Chu kỳ sống của đơn hàng

Đơn hàng thường di chuyển qua các trạng thái sau:

1. **Chờ xử lý** — Đơn hàng mới nhận được, đang chờ xác nhận thanh toán
2. **Đang xử lý** — Thanh toán đã được xác nhận, đang chuẩn bị vận chuyển
3. **Đã vận chuyển** — Đơn hàng đã được gửi đi kèm theo mã theo dõi
4. **Đã giao hàng** — Khách hàng đã nhận được đơn hàng
5. **Hoàn tất** — Đơn hàng đã được hoàn tất

## Xử lý đơn hàng

### 1. Xem xét đơn hàng

Kiểm tra:

- Các mặt hàng và số lượng có đúng không
- Địa chỉ vận chuyển đã đầy đủ chưa
- Thanh toán đã được nhận chưa
- Các ghi chú của khách hàng đã được xử lý chưa

### 2. Tạo vận chuyển

Để vận chuyển đơn hàng:

1. Click **Tạo vận chuyển** trên trang chi tiết đơn hàng
2. Chọn các mặt hàng cần bao gồm (đối với vận chuyển từng phần, chỉ chọn một số mặt hàng)
3. Chọn nhà vận chuyển và dịch vụ vận chuyển
4. Nhập mã theo dõi
5. Click **Lưu vận chuyển**

Trạng thái đơn hàng sẽ tự động cập nhật thành **Đã vận chuyển** và khách hàng sẽ nhận được email thông báo vận chuyển kèm theo mã theo dõi.

### 3. Đánh dấu là đã giao hàng

Khi khách hàng xác nhận đã nhận hàng hoặc mã theo dõi cho thấy đã giao hàng, cập nhật trạng thái thành **Đã giao hàng** và sau đó là **Hoàn tất**.

## Các hành động đơn hàng

### Thêm ghi chú

Thêm ghi chú nội bộ hoặc tin nhắn hiển thị cho khách hàng:

1. Cuộn xuống phần **Ghi chú** trên trang chi tiết đơn hàng
2. Nhập tin nhắn của bạn
3. Chọn xem đây là ghi chú nội bộ (chỉ dành cho nhân viên) hoặc thông báo cho khách hàng
4. Click **Thêm ghi chú**

Các ghi chú hiển thị cho khách hàng sẽ kích hoạt thông báo qua email.

### Xử lý hoàn tiền

Để thực hiện hoàn tiền:

1. Click **Hoàn tiền** trên trang chi tiết đơn hàng
2. Chọn các mặt hàng cần hoàn tiền (hoặc nhập số tiền tùy chỉnh)
3. Chọn lý do hoàn tiền
4. Xác nhận hoàn tiền

Các khoản hoàn tiền được xử lý thông qua cổng thanh toán ban đầu. Khách hàng sẽ nhận được email xác nhận.

### Hủy đơn hàng

Để hủy:

1. Click **Hủy đơn hàng**
2. Chọn lý do hủy
3. Chọn xem có nên hoàn lại hàng hóa hay không
4. Xác nhận

Khách hàng sẽ được thông báo tự động và hoàn tiền sẽ được khởi tạo nếu thanh toán đã được thực hiện.

## Các hành động theo khối

Từ danh sách đơn hàng, bạn có thể chọn nhiều đơn hàng và áp dụng các hành động theo khối:

- **Cập nhật trạng thái** — Di chuyển nhiều đơn hàng đến cùng một trạng thái
- **Xuất** — Tải xuống các đơn hàng đã chọn dưới dạng CSV
- **In** — Tạo phiếu đóng gói hoặc hóa đơn

## Thông báo đơn hàng

Khách hàng sẽ tự động nhận được email tại các giai đoạn quan trọng:

- **Xác nhận đơn hàng** — Ngay sau khi đặt hàng
- **Xác nhận thanh toán** — Khi thanh toán được xác nhận
- **Thông báo vận chuyển** — Khi tạo vận chuyển (bao gồm liên kết theo dõi)
- **Xác nhận giao hàng** — Khi đánh dấu là đã giao hàng

Cấu hình mẫu email trong **Cài đặt > Cấu hình email**.

## Mẹo

- Xử lý đơn hàng hàng ngày để duy trì thời gian giao hàng nhanh.
- Sử dụng bộ lọc trạng thái để tập trung vào các đơn hàng cần xử lý (Chờ xử lý và Đang xử lý).
- Thêm ghi chú nội bộ để theo dõi bất kỳ yêu cầu xử lý đặc biệt nào.
- Trong các giai đoạn lượng đơn hàng cao, hãy sử dụng các hành động theo khối để cập nhật nhiều đơn hàng cùng lúc.
- Thiết lập các quy tắc vận chuyển để tự động chọn nhà vận chuyển dựa trên trọng lượng đơn hàng và địa điểm đến.