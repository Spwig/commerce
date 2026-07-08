---
title: Thẻ quà tặng
---

Thẻ quà tặng cho phép khách hàng mua tín dụng cửa hàng có thể gửi cho người khác làm quà hoặc giữ lại để sử dụng cá nhân. Người nhận sẽ nhận được một mã duy nhất qua email mà họ có thể sử dụng để thanh toán khi mua hàng.

![Quản lý thẻ quà tặng](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Loại mệnh giá

Kiểm soát cách khách hàng chọn mệnh giá thẻ quà tặng:

| Loại | Mô tả |
|------|-------------|
| **Mệnh giá cố định** | Khách hàng chọn từ các mệnh giá được đặt trước (ví dụ: $25, $50, $100) |
| **Mệnh giá tùy chỉnh** | Khách hàng nhập bất kỳ mệnh giá nào trong khoảng tối thiểu/tối đa |
| **Cả hai** | Cung cấp các mệnh giá được đặt trước cùng với tùy chọn mệnh giá tùy chỉnh |

## Tạo sản phẩm thẻ quà tặng

### Bước 1: Thiết lập sản phẩm

1. Di chuyển đến **Sản phẩm > Tất cả sản phẩm** và nhấn **+ Thêm sản phẩm**
2. Thiết lập **Loại sản phẩm** thành **Thẻ quà tặng**
3. Điền tên và mô tả sản phẩm
4. Cấu hình cài đặt mệnh giá:
   - Chọn **Loại mệnh giá** (Cố định, Tùy chỉnh hoặc Cả hai)
   - Với Cố định: thiết lập các mệnh giá có sẵn
   - Với Tùy chỉnh: thiết lập **Tối thiểu** và **Tối đa** các mệnh giá được phép
5. Thiết lập **Số ngày hết hạn** (0 = không bao giờ hết hạn) — điều này xác định thời gian hiệu lực của thẻ quà tặng sau khi mua
6. Lưu và xuất bản sản phẩm

### Bước 2: Xuất bản và bán hàng

Sau khi xuất bản, thẻ quà tặng sẽ hiển thị trên cửa hàng của bạn giống như bất kỳ sản phẩm nào khác. Khách hàng có thể duyệt sản phẩm, chọn một mệnh giá và thêm vào giỏ hàng của họ.

## Chu kỳ sống của thẻ quà tặng

Một thẻ quà tặng trải qua chu kỳ sống sau:

1. **Mua hàng** — Khách hàng mua sản phẩm thẻ quà tặng và cung cấp thông tin người nhận
2. **Giao hàng** — Một email chứa mã thẻ quà tặng được gửi tự động đến người nhận
3. **Sử dụng** — Người nhận nhập mã tại thanh toán để áp dụng số dư
4. **Theo dõi số dư** — Mỗi lần sử dụng sẽ làm giảm số dư cho đến khi đạt 0

## Quy trình mua hàng của khách hàng

Khi khách hàng mua thẻ quà tặng:

1. **Chọn mệnh giá** — Chọn một mệnh giá hoặc nhập một mệnh giá tùy chỉnh
2. **Thông tin người nhận** — Nhập địa chỉ email và tên của người nhận
3. **Thông điệp cá nhân** — Thêm một thông điệp tùy chọn để bao gồm trong email giao hàng
4. **Tên người gửi** — Cung cấp tên người gửi cho email
5. **Giao hàng theo lịch** — Tùy chọn lên lịch email cho một ngày trong tương lai (ví dụ: sinh nhật)
6. **Thanh toán** — Hoàn tất mua hàng như bất kỳ sản phẩm nào khác

## Giao hàng tự động

Sau khi mua hàng, thẻ quà tặng được giao tự động:

- Một email được thiết kế sẽ được gửi đến người nhận với:
  - Mã thẻ quà tặng duy nhất
  - Giá trị thẻ quà tặng
  - Thông điệp cá nhân từ người gửi
  - Liên kết để kiểm tra số dư còn lại
- Nếu đã thiết lập giao hàng theo lịch, email sẽ được gửi vào ngày và thời gian đã chỉ định
- Người gửi nhận được xác nhận đơn hàng với chi tiết thẻ quà tặng

## Quản lý thẻ quà tặng trong Admin

Di chuyển đến **Sản phẩm > Thẻ quà tặng** để quản lý tất cả thẻ quà tặng:

### Bảng điều khiển thống kê

Tại đầu trang, bốn thẻ hiển thị các chỉ số chính:

- **Tổng số thẻ quà tặng** — Tổng số thẻ quà tặng đã phát hành
- **Đang hoạt động** — Các thẻ đang hoạt động với số dư có sẵn
- **Tổng số dư** — Số dư còn lại tổng cộng trên tất cả các thẻ
- **Đã sử dụng một phần** — Các thẻ đã được sử dụng một phần

### Lọc

Lọc thẻ quà tặng theo:

- **Tìm kiếm** — Tìm theo mã, email hoặc tên người nhận
- **Trạng thái** — Đang hoạt động, Không hoạt động, Hết hạn, Đã sử dụng hết hoặc Đã sử dụng một phần
- **Số dư** — Có số dư hoặc Số dư bằng 0
- **Tạo** — Khoảng thời gian (Hôm nay, Tuần này, Tháng này, Năm này)

### Chi tiết thẻ quà tặng

Mỗi thẻ quà tặng hiển thị:

- **Mã** — Mã sử dụng duy nhất (ví dụ: GC-XXXX-XXXX-XXXX)
- **Người nhận** — Email và tên
- **Biểu tượng trạng thái** — Trạng thái hiện tại với mã màu
- **Số dư / Số dư ban đầu / Số dư đã sử dụng** — Tổng quan tài chính với phần trăm đã sử dụng
- **Ngày quan trọng** — Ngày tạo, ngày phát hành, ngày sử dụng lần đầu
- **Người gửi** — Người đã mua thẻ quà tặng

### Hành động

Đối với mỗi thẻ quà tặng, bạn có thể:

- **Chỉnh sửa** — Xem và chỉnh sửa chi tiết thẻ quà tặng
- **Xem giao dịch** — Xem lịch sử giao dịch đầy đủ
- **Gửi lại email** — Gửi lại email giao hàng đến người nhận
- **Vô hiệu hóa** — Vô hiệu hóa thẻ (số dư được giữ lại nhưng không thể sử dụng)

## Sử dụng thẻ quà tặng tại thanh toán

Khi khách hàng nhập mã thẻ quà tặng tại thanh toán:

1. Mã được xác minh (đang hoạt động, chưa hết hạn, có số dư)
2. Số dư có sẵn được hiển thị
3. Số dư được áp dụng cho tổng đơn hàng
4. Nếu số dư đủ để thanh toán toàn bộ đơn hàng, không cần thanh toán bổ sung
5. Nếu số dư ít hơn tổng đơn hàng, khách hàng thanh toán phần còn lại
6. Giao dịch được ghi lại và số dư được cập nhật

## Xử lý hoàn tiền

Khi hoàn tiền các đơn hàng đã sử dụng thẻ quà tặng:

- **Thẻ quà tặng chưa sử dụng** — Vô hiệu hóa hoàn toàn thẻ quà tặng
- **Thẻ đã sử dụng một phần** — Số dư phải được điều chỉnh thủ công thông qua giao dịch
- **Hoàn tiền đầy đủ** — Hoàn tiền số tiền về số dư thẻ quà tặng thông qua giao dịch hoàn tiền

## Một số mẹo

- Thiết lập các khoảng thời gian hết hạn hợp lý (ví dụ: 365 ngày) để tuân thủ các quy định về thẻ quà tặng tại địa phương — một số khu vực yêu cầu thời gian hiệu lực tối thiểu.
- Sử dụng loại mệnh giá **Cả hai** để cung cấp sự tiện lợi (mệnh giá được đặt trước) và tính linh hoạt (mệnh giá tùy chỉnh).
- Theo dõi chỉ số **Tổng số dư** thường xuyên — nó đại diện cho khoản nợ tiềm tàng trên sổ sách của bạn.
- Sử dụng giao hàng theo lịch cho các chương trình khuyến mãi theo mùa — khách hàng có thể mua thẻ quà tặng sớm và có chúng được giao vào đúng ngày.
- Kiểm tra toàn bộ quy trình (mua hàng, giao email, sử dụng) với một đơn hàng kiểm tra trước khi ra mắt.
- Nếu bạn bán hàng cho khách hàng ở nhiều quốc gia, bạn có thể phát hành thẻ quà tặng theo các loại tiền tệ cụ thể — xem chủ đề giúp đỡ **Thẻ quà tặng đa tiền tệ** để biết thêm chi tiết.