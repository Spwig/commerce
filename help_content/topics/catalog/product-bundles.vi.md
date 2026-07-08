---
title: Gói sản phẩm
---

Gói sản phẩm cho phép bạn bán các gói sản phẩm được ghép sẵn với giá ưu đãi. Đây là lựa chọn lý tưởng cho các bộ quà tặng, bộ khởi đầu, hoặc bất kỳ sự kết hợp sản phẩm nào mà bạn muốn cung cấp cùng nhau với mức giảm giá.

![Thành phần gói sản phẩm trong phần quản trị](/static/core/admin/img/help/product-bundles/bundle-components.webp)

## Chiến lược định giá

Chọn cách tính giá gói sản phẩm:

| Chiến lược | Mô tả |
|----------|-------------|
| **Giá cố định** | Đặt một mức giá cố định cho toàn bộ gói, bất kể giá các thành phần. |
| **Giảm giá theo phần trăm** | Tự động tính toán giá theo tỷ lệ phần trăm giảm từ tổng giá các thành phần. |
| **Tổng các thành phần** | Giá gói bằng tổng giá tất cả các thành phần (phù hợp khi hiển thị nhóm mà không có giảm giá). |

## Tạo một Gói

### Bước 1: Tạo sản phẩm

1. Truy cập **Sản phẩm > Tất cả sản phẩm** và nhấn **+ Thêm sản phẩm**
2. Thiết lập **Loại sản phẩm** thành **Gói sản phẩm**
3. Điền tên gói, mô tả và hình ảnh
4. Lưu sản phẩm

### Bước 2: Thêm thành phần

Chuyển sang tab **Các mục trong gói** để thêm sản phẩm vào gói của bạn:

1. Nhấn **+ Thêm thành phần**
2. Tìm kiếm và chọn sản phẩm từ danh sách thả xuống
3. Thiết lập **Số lượng** cho mỗi thành phần (ví dụ: 2x mặt nạ dưỡng da trong bộ chăm sóc da)
4. Thiết lập **Thứ tự hiển thị** để kiểm soát thứ tự hiển thị
5. Tùy chọn đánh dấu thành phần là **Tùy chọn** (khách hàng có thể loại bỏ)
6. Nếu thành phần là sản phẩm biến thể, chọn một trong hai tùy chọn:
   - **Biến thể cố định** — tất cả khách hàng nhận cùng một biến thể
   - **Cho phép chọn biến thể** — khách hàng chọn biến thể mong muốn tại thời điểm thanh toán

Tóm tắt ở phần cuối hiển thị **Tổng số thành phần** và **Giá trị gói** (tổng giá các thành phần).

### Bước 3: Cấu hình định giá

Chuyển sang tab **Định giá**:

1. Chọn **Chiến lược định giá gói** của bạn
2. Với **Giá cố định** — nhập giá gói trực tiếp
3. Với **Giảm giá theo phần trăm** — thiết lập tỷ lệ giảm giá (ví dụ: 15% giảm)
4. Với **Tổng các thành phần** — giá được tính toán tự động

## Những loại sản phẩm nào có thể được ghép

| Loại sản phẩm | Có thể là thành phần? |
|-------------|-------------------|
| Sản phẩm đơn giản | Có |
| Sản phẩm biến thể | Có (biến thể cố định hoặc lựa chọn của khách hàng) |
| Sản phẩm số | Có |
| Sản phẩm tùy chỉnh | Không |
| Sản phẩm cấu hình | Không |
| Gói sản phẩm | Không (gói không thể lồng ghép) |
| Thẻ quà tặng | Không |

## Quản lý tồn kho

Tồn kho gói được quản lý thông qua các thành phần:

- **Tất cả các thành phần phải có sẵn** để gói có thể được mua
- Khi một gói được đặt hàng, tồn kho sẽ được trừ đi từ từng sản phẩm thành phần
- Nếu bất kỳ thành phần nào hết tồn kho, gói sẽ không còn khả dụng
- Mức tồn kho của các thành phần được kiểm tra thời gian thực trong quá trình thanh toán

## Các thành phần tùy chọn

Đánh dấu thành phần là **Tùy chọn** để cho phép khách hàng tùy chỉnh gói của họ:

- Các thành phần tùy chọn được bao gồm theo mặc định nhưng khách hàng có thể loại bỏ
- Giá gói sẽ điều chỉnh tương ứng khi các thành phần tùy chọn bị loại bỏ
- Ít nhất phải có một thành phần không phải là tùy chọn (bắt buộc)

## Trải nghiệm của khách hàng

Khi khách hàng xem gói trên cửa hàng của bạn:

1. **Danh sách thành phần** — Tất cả sản phẩm được bao gồm sẽ được hiển thị với hình ảnh và số lượng
2. **Tiết kiệm từ gói** — Hiển thị mức giảm giá so với việc mua từng sản phẩm riêng lẻ
3. **Chọn biến thể** — Đối với các thành phần có tùy chọn biến thể, khách hàng chọn biến thể mong muốn
4. **Các mục tùy chọn** — Khách hàng có thể bật/tắt các thành phần tùy chọn
5. **Thêm vào giỏ hàng một lần** — Toàn bộ gói được thêm vào giỏ hàng như một mặt hàng

## Một số mẹo

- Sử dụng chiến lược **Giảm giá theo phần trăm** cho định giá linh hoạt nhất — nó tự động điều chỉnh khi giá các thành phần thay đổi.
- Hiển thị rõ ràng mức tiết kiệm trong mô tả sản phẩm để khuyến khích mua theo gói.
- Giữ gói sản phẩm ở mức 3-5 thành phần để có trải nghiệm khách hàng tốt nhất. Quá nhiều mặt hàng có thể khiến khách hàng cảm thấy bối rối.
- Sử dụng các thành phần tùy chọn để cung cấp phiên bản "cơ bản" và "nâng cao" của cùng một gói.
- Thường xuyên kiểm tra xem tất cả các sản phẩm thành phần vẫn còn hoạt động và có sẵn.
