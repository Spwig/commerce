---
title: Ví dụ về Voucher
---

Hướng dẫn này cung cấp các ví dụ cụ thể, theo từng trường, cho các loại voucher phổ biến nhất. Mỗi ví dụ sẽ hiển thị chính xác những gì cần nhập khi tạo voucher tại **Marketing > Vouchers** → **+ Thêm Voucher**.

![Thẻ Voucher](/static/core/admin/img/help/voucher-examples/voucher-card.webp)

## Ví dụ 1: Giảm giá theo tỷ lệ với giới hạn tối đa

**Tình huống:** Cung cấp giảm 20% cho toàn bộ giỏ hàng, nhưng giới hạn mức giảm tối đa là 50 USD để đảm bảo các đơn hàng có giá trị cao vẫn mang lại lợi nhuận. Không có ngày hết hạn.

| Trường | Giá trị |
|-------|-------|
| Mã | `SAVE20` |
| Tên | 20% Giảm — Tối đa 50 USD |
| Loại Giảm giá | Tỷ lệ |
| Giá trị Giảm giá | 20 |
| Mức Giảm Tối đa | 50 |
| Phạm vi Áp dụng | Toàn bộ Giỏ hàng |
| Số lần Sử dụng Tối đa | *(trống — không giới hạn)* |
| Số lần Sử dụng Mỗi Khách hàng | 1 |
| Giá trị Đơn hàng Tối thiểu | *(trống — không có giá trị tối thiểu)* |

**Cách giới hạn hoạt động:** Trên đơn hàng 200 USD, mức giảm là 40 USD. Trên đơn hàng 300 USD, mức giảm sẽ là 60 USD, nhưng giới hạn sẽ giới hạn nó xuống 50 USD. Trên đơn hàng 500 USD, mức giảm vẫn là 50 USD. Điều này cho phép bạn chạy một chương trình khuyến mãi nghe có vẻ hào phóng nhưng vẫn giữ mức giảm thực tế có thể dự đoán được.

## Ví dụ 2: Giảm giá cố định với giá trị tối thiểu

**Tình huống:** Cung cấp giảm 10 USD cho bất kỳ đơn hàng nào trên 75 USD để khuyến khích khách hàng mua hàng với số lượng lớn hơn.

| Trường | Giá trị |
|-------|-------|
| Mã | `TAKE10` |
| Tên | Giảm 10 USD cho đơn hàng trên 75 USD |
| Loại Giảm giá | Giảm giá cố định |
| Giá trị Giảm giá | 10 |
| Phạm vi Áp dụng | Toàn bộ Giỏ hàng |
| Giá trị Đơn hàng Tối thiểu | 75 |
| Số lần Sử dụng Mỗi Khách hàng | 0 *(không giới hạn)* |
| Ngày Kết thúc | *(trống — không có ngày hết hạn)* |

> **Lưu ý:** Việc thiết lập giá trị đơn hàng tối thiểu giúp bảo vệ biên lợi nhuận của bạn. Nếu không có giá trị tối thiểu này, khách hàng có thể sử dụng mã này cho đơn hàng 12 USD và xóa lợi nhuận của bạn. Luôn kết hợp các voucher giảm giá cố định với một giá trị tối thiểu hợp lý.

## Ví dụ 3: Miễn phí vận chuyển

**Tình huống:** Cung cấp miễn phí vận chuyển cho bất kỳ đơn hàng nào mà không có giá trị tối thiểu.

| Trường | Giá trị |
|-------|-------|
| Mã | `FREESHIP` |
| Tên | Miễn phí Vận chuyển |
| Loại Giảm giá | Miễn phí Vận chuyển |
| Phạm vi Áp dụng | Toàn bộ Giỏ hàng |
| Số lần Sử dụng Tối đa | *(trống — không giới hạn)* |
| Số lần Sử dụng Mỗi Khách hàng | 1 |
| Giá trị Đơn hàng Tối thiểu | *(trống — không có giá trị tối thiểu)* |

> **Lưu ý:** Chọn loại giảm giá **Miễn phí Vận chuyển**, điều này sẽ tự động loại bỏ phí vận chuyển khỏi đơn hàng. Đây là phương pháp sạch sẽ nhất và hoạt động bất kể khách hàng chọn phương thức vận chuyển nào.

## Ví dụ 4: Mã chào mừng cho khách hàng mới

**Tình huống:** Cung cấp giảm 15% cho đơn hàng đầu tiên của khách hàng mới để khuyến khích chuyển đổi.

| Trường | Giá trị |
|-------|-------|
| Mã | `WELCOME15` |
| Tên | Chào mừng — Giảm 15% cho đơn hàng đầu tiên |
| Loại Giảm giá | Tỷ lệ |
| Giá trị Giảm giá | 15 |
| Phạm vi Áp dụng | Toàn bộ Giỏ hàng |
| Số lần Sử dụng Mỗi Khách hàng | 1 |
| Chỉ dành cho khách hàng mới | Đã chọn |

Hệ thống xác minh trạng thái khách hàng mới bằng cách kiểm tra xem khách hàng có bất kỳ đơn hàng nào đã hoàn thành trước đó hay không. Nếu một khách hàng có lịch sử đơn hàng cố gắng áp dụng mã này, họ sẽ thấy một thông báo lỗi rõ ràng tại bước thanh toán.

## Ví dụ 5: Voucher dành riêng cho sản phẩm

**Tình huống:** Cung cấp giảm 5 USD cho các sản phẩm được chọn — ví dụ, để thúc đẩy hàng tồn kho bán chậm.

| Trường | Giá trị |
|-------|-------|
| Mã | `PICK5` |
| Tên | Giảm 5 USD cho các mặt hàng được chọn |
| Loại Giảm giá | Giảm giá cố định |
| Giá trị Giảm giá | 5 |
| Phạm vi Áp dụng | Các sản phẩm cụ thể |
| Sản phẩm Đủ điều kiện | *(chọn các sản phẩm mục tiêu)* |
| Số lần Sử dụng Mỗi Khách hàng | 1 |

> **Lưu ý:** Sử dụng phạm vi sản phẩm khi bạn muốn giảm giá cho các SKU riêng lẻ. Sử dụng phạm vi danh mục (ví dụ tiếp theo) khi bạn muốn giảm giá tất cả các mặt hàng trong một bộ phận. Phạm vi sản phẩm cho phép bạn kiểm soát chính xác; phạm vi danh mục dễ bảo trì hơn khi danh mục của bạn thay đổi thường xuyên.

## Ví dụ 6: Voucher theo danh mục

**Tình huống:** Chạy chương trình khuyến mãi giảm 25% cho tất cả các mặt hàng trong danh mục Điện tử.

| Trường | Giá trị |
|-------|-------|
| Mã | `ELEC25` |
| Tên | Giảm 25% cho Điện tử |
| Loại Giảm giá | Tỷ lệ |
| Giá trị Giảm giá | 25 |
| Phạm vi Áp dụng | Các danh mục cụ thể |
| Danh mục Đủ điều kiện | Điện tử |
| Số lần Sử dụng Tối đa | *(trống — không giới hạn)* |
| Số lần Sử dụng Mỗi Khách hàng | 1 |


Khi áp dụng cho một danh mục, khuyến mãi chỉ áp dụng cho các mặt hàng đủ điều kiện trong giỏ hàng.

Các mặt hàng không phải là Điện tử sẽ được tính giá đầy đủ.

## So sánh loại khuyến mãi

| Loại | Cách hoạt động | Phù hợp nhất | Ví dụ |
|------|-------------|----------|---------|
| **Phần trăm** | Trừ đi một phần trăm của tổng số tiền đủ điều kiện | Khuyến mãi mở rộng theo quy mô đơn hàng | Giảm 20% toàn bộ giỏ hàng |
| **Số tiền cố định** | Trừ đi một khoản tiền cố định | Khuyến mãi đơn giản và dễ dự đoán | Giảm $10 cho đơn hàng trên $75 |
| **Miễn phí vận chuyển** | Loại bỏ phí vận chuyển khỏi đơn hàng | Giảm tỷ lệ bỏ giỏ hàng tại thanh toán | Miễn phí vận chuyển, không có mức tối thiểu |

## So sánh phạm vi

| Phạm vi | Cách hoạt động | Phù hợp nhất |
|-------|-------------|----------|
| **Toàn bộ giỏ hàng** | Khuyến mãi áp dụng cho tổng số tiền toàn bộ đơn hàng | Khuyến mãi toàn cửa hàng và mã chào mừng |
| **Sản phẩm cụ thể** | Khuyến mãi chỉ áp dụng cho các sản phẩm được chọn trong giỏ hàng | Xử lý tồn kho cụ thể hoặc các chương trình nổi bật |
| **Danh mục cụ thể** | Khuyến mãi chỉ áp dụng cho các mặt hàng trong danh mục được chọn | Bán hàng theo phòng ban và khuyến mãi theo mùa |

## Mẹo

- **Sử dụng mã dễ nhớ** — `SUMMER20` hiệu quả hơn so với `COUPONX1600406498`. Hãy lưu các mã được tạo tự động cho các chiến dịch theo khối lượng.
- **Kiểm tra trước khi phân phối** — Đặt một đơn hàng kiểm tra với mã voucher để xác minh rằng nó áp dụng đúng và tuân thủ tất cả các giới hạn.
- **Theo dõi việc sử dụng** — Kiểm tra số lượng Redemptions trên mỗi thẻ voucher để theo dõi hiệu suất chiến dịch theo thời gian thực.
- **Kết hợp với thanh công bố** — Quảng bá mã voucher của bạn trong thanh thông báo toàn trang web để khách hàng nhìn thấy trước khi bắt đầu mua sắm.