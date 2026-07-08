---
title: Sản phẩm có thể cấu hình
---

Sản phẩm có thể cấu hình cho phép khách hàng tự xây dựng sản phẩm của họ bằng cách chọn các tùy chọn từ các khoảng trống cấu hình khác nhau. Điều này lý tưởng cho các sản phẩm đặt hàng theo yêu cầu như máy tính cá nhân tùy chỉnh, hộp quà cá nhân hóa hoặc nội thất đặt hàng, nơi mỗi thành phần là một sản phẩm thực tế trong danh mục của bạn.

![Trình cấu hình sản phẩm (Admin)](/static/core/admin/img/help/configurable-products/product-configurator.webp)

## Cách hoạt động

Một sản phẩm có thể cấu hình bao gồm **khoảng trống** (loại lựa chọn) và **tùy chọn** (các sản phẩm thực tế mà khách hàng có thể chọn). Ví dụ, một máy tính cá nhân tùy chỉnh có thể có các khoảng trống cho Bộ xử lý, Card đồ họa, RAM và Lưu trữ — mỗi khoảng trống chứa nhiều tùy chọn sản phẩm để chọn.

## Chiến lược định giá

Chọn cách tính giá cuối cùng:

| Chiến lược | Mô tả |
|-----------|-------|
| **Tổng các thành phần** | Giá cuối cùng = tổng giá của tất cả tùy chọn đã chọn. Không cần giá cơ bản. |
| **Giá cơ bản + điều chỉnh** | Bắt đầu với giá cơ bản của sản phẩm, sau đó thêm/trừ giá điều chỉnh theo từng tùy chọn. |
| **Giá cố định** | Một giá cố định bất kể khách hàng chọn tùy chọn nào. |

## Thiết lập sản phẩm có thể cấu hình

### Bước 1: Tạo sản phẩm

1. Di chuyển đến **Sản phẩm > Tất cả sản phẩm** và nhấn **+ Thêm sản phẩm**
2. Đặt **Loại sản phẩm** thành **Sản phẩm có thể cấu hình**
3. Chọn **Chiến lược định giá** của bạn (Tổng các thành phần là phổ biến nhất)
4. Điền tên sản phẩm, mô tả và các chi tiết cơ bản khác
5. Lưu sản phẩm

### Bước 2: Thêm khoảng trống cấu hình

Sau khi lưu, chuyển sang **Thẻ Cấu hình** để thiết lập các khoảng trống của bạn.

1. Nhấn **+ Thêm khoảng trống** để tạo một danh mục cấu hình mới
2. Đối với mỗi khoảng trống, thiết lập:
   - **Tên** — Điều khách hàng nhìn thấy (ví dụ: "Bộ xử lý", "Màu sắc")
   - **Biểu tượng** — Lớp biểu tượng Font Awesome để nhận diện trực quan
   - **Bắt buộc** — Khách hàng có phải chọn không
   - **Số lượng tối thiểu/tối đa** — Số tùy chọn khách hàng có thể chọn (mặc định: chính xác 1)
   - **Thứ tự hiển thị** — Điều khiển thứ tự các khoảng trống xuất hiện trong trình hướng dẫn cấu hình

### Bước 3: Thêm tùy chọn cho mỗi khoảng trống

Mỗi khoảng trống cần có các tùy chọn sản phẩm để khách hàng chọn:

1. Nhấn **Quản lý tùy chọn** trên một khoảng trống
2. Tìm kiếm và thêm các sản phẩm hiện có từ danh mục của bạn
3. Đối với mỗi tùy chọn, thiết lập:
   - **Điều chỉnh giá** — Số tiền thêm hoặc trừ (dùng với chiến lược định giá Giá cơ bản + điều chỉnh)
   - **Mặc định** — Chọn tùy chọn này khi trình cấu hình được tải
   - **Phổ biến** — Hiển thị biểu tượng "Phổ biến" để giúp khách hàng quyết định
   - **Số lượng** — Số lượng đơn vị thành phần được bao gồm
   - **Thẻ tương thích** — Các thẻ được sử dụng để tạo quy tắc tương thích theo lô

**Lưu ý:** Các sản phẩm thành phần có thể được ẩn khỏi cửa hàng bằng cách đánh dấu **Ẩn khỏi Trang web** trên thẻ **Thông tin cơ bản** của sản phẩm thành phần. Điều này giữ chúng có sẵn như tùy chọn cấu hình nhưng không làm lộn xộn danh mục sản phẩm của bạn.

### Bước 4: Định nghĩa quy tắc tương thích

Quy tắc tương thích ngăn khách hàng chọn các kết hợp không tương thích:

| Loại quy tắc | Mô tả |
|-------------|-------|
| **Yêu cầu** | Khi tùy chọn A được chọn, chỉ có các tùy chọn được liệt kê mới có sẵn trong khoảng trống mục tiêu |
| **Loại bỏ** | Khi tùy chọn A được chọn, các tùy chọn được liệt kê sẽ bị ẩn khỏi khoảng trống mục tiêu |

Để thêm quy tắc:

1. Cuộn xuống phần **Quy tắc tương thích** trên thẻ Cấu hình
2. Nhấn **+ Thêm quy tắc**
3. Chọn **tùy chọn nguồn** (tùy chọn kích hoạt)
4. Chọn **loại quy tắc** (Yêu cầu hoặc Loại bỏ)
5. Chọn **khoảng trống mục tiêu** và **các tùy chọn bị ảnh hưởng**

Bạn cũng có thể tự động tạo quy tắc từ các thẻ tương thích được gán cho tùy chọn, điều này nhanh hơn khi quản lý nhiều kết hợp.

### Bước 5: Tạo cấu hình mặc định (tùy chọn)

Các cấu hình mặc định là các cấu hình được xây dựng sẵn cho phép khách hàng bắt đầu nhanh chóng:

1. Cuộn xuống phần **Cấu hình mặc định**
2. Nhấn **+ Thêm cấu hình mặc định**
3. Đặt tên và mô tả cho cấu hình mặc định (ví dụ: "Cấu hình chơi game", "Cấu hình khởi đầu tiết kiệm")
4. Chọn các tùy chọn cho mỗi khoảng trống
5. Tùy chọn tải lên hình ảnh xem trước và đánh dấu là **Nổi bật**

Khách hàng có thể bắt đầu từ cấu hình mặc định và sau đó tùy chỉnh từng khoảng trống theo sở thích của họ.

## Trải nghiệm của khách hàng

Khi khách hàng xem sản phẩm có thể cấu hình trên cửa hàng của bạn:

1. **Giao diện hướng dẫn** — Các khoảng trống được trình bày như các bước, hướng dẫn khách hàng qua từng lựa chọn
2. **Lọc** — Các tùy chọn không tương thích sẽ được ẩn tự động dựa trên quy tắc tương thích
3. **Biểu tượng phổ biến** — Các tùy chọn được đánh dấu phổ biến sẽ hiển thị biểu tượng để hỗ trợ quyết định
4. **Cấu hình mặc định** — Các cấu hình nổi bật sẽ xuất hiện như các tùy chọn bắt đầu nhanh
5. **Cập nhật giá** — Giá tổng sẽ được cập nhật theo thời gian thực khi các tùy chọn được chọn
6. **Tóm tắt** — Một bước xem xét hiển thị tất cả tùy chọn đã chọn trước khi thêm vào giỏ hàng

## Một số lưu ý

- Bắt đầu với chiến lược định giá "Tổng các thành phần" — đây là cách dễ hiểu nhất cho khách hàng và dễ bảo trì nhất.
- Sử dụng quy tắc tương thích để ngăn các cấu hình không hợp lệ thay vì dựa vào kiến thức của khách hàng.
- Tạo 2-3 cấu hình mặc định cho các cấu hình phổ biến nhất của bạn để giảm sự mệt mỏi khi ra quyết định.
- Ẩn các sản phẩm thành phần khỏi cửa hàng nếu chúng chỉ nên được sử dụng thông qua trình cấu hình.
- Kiểm tra toàn bộ quy trình cấu hình trên giao diện phía trước sau khi thiết lập để đảm bảo tất cả quy tắc hoạt động như mong đợi.