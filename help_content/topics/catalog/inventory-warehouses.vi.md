---
title: Kho hàng & Kho
---

Hệ thống kho hàng cho phép bạn quản lý tồn kho tại nhiều vị trí, thiết lập ưu tiên xử lý đơn hàng và theo dõi mức tồn kho theo thời gian thực. Di chuyển đến **Settings > License Management** trong thanh bên, hoặc truy cập kho hàng từ tab tồn kho sản phẩm.

![Danh sách kho hàng](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Kho hàng

### Danh sách kho hàng

Trang kho hàng hiển thị tất cả vị trí tồn kho của bạn dưới dạng các thẻ với:

- **Tên và mã** — Mã nhận dạng kho hàng (ví dụ: "Main Warehouse", mã "MAIN-WH")
- **Khu vực bán hàng** — Gán khu vực địa lý
- **Biểu tượng trạng thái** — Hoạt động/đang tắt, vị trí bán lẻ
- **Thống kê** — Số lượng sản phẩm tồn kho, ưu tiên xử lý, tỷ lệ đệm tồn kho
- **Vị trí** — Thành phố và quốc gia
- **Cập nhật lần cuối** — Khi mức tồn kho được sửa đổi lần cuối

### Tạo kho hàng

1. Nhấp **+ Thêm Kho**
2. Điền thông tin kho hàng:
   - **Tên** — Nhãn mô tả (ví dụ: "US East Warehouse")
   - **Mã** — Mã duy nhất ngắn (ví dụ: "US-EAST")
   - **Khu vực bán hàng** — Gán khu vực địa lý để định tuyến xử lý đơn hàng
   - **Địa chỉ** — Địa chỉ kho hàng đầy đủ để tính toán vận chuyển
3. Cấu hình cài đặt:
   - **Hoạt động** — Bật để bao gồm trong xử lý đơn hàng
   - **Vị trí bán lẻ** — Đánh dấu nếu kho này cũng phục vụ như một cửa hàng vật lý
   - **Ưu tiên xử lý** — Số cao hơn = ưu tiên cao hơn cho xử lý đơn hàng
   - **Đệm tồn kho** — Phần trăm tồn kho được dự trữ như đệm an toàn
4. Nhấp **Lưu**

### Ưu tiên xử lý

Khi một đơn hàng đến, hệ thống chọn kho hàng tốt nhất dựa trên:

1. **Giá trị ưu tiên** — Kho hàng có ưu tiên cao hơn được ưa tiên
2. **Sự có sẵn của tồn kho** — Phải có đủ tồn kho
3. **Phù hợp khu vực** — Kho hàng trong khu vực của khách hàng được ưa tiên

Ví dụ, nếu bạn có kho hàng ở Mỹ (ưu tiên 100) và kho hàng ở EU (ưu tiên 60), đơn hàng Mỹ sẽ được xử lý từ kho hàng Mỹ trước.

### Đệm tồn kho

Đệm tồn kho dự trữ một phần trăm tồn kho sẽ không được bán trực tuyến. Điều này hữu ích cho:
- Các cửa hàng bán lẻ vật lý cần tồn kho trên sàn
- Tồn kho an toàn để tránh bán quá mức
- Tồn kho được đặt hàng cho các đơn hàng sỉ

Một đệm 10% trên 100 đơn vị có nghĩa là chỉ có 90 đơn vị có sẵn cho các đơn hàng trực tuyến.

## Các mục tồn kho

Các mục tồn kho đại diện cho tồn kho thực tế của một sản phẩm cụ thể tại một kho hàng cụ thể.

### Xem mức tồn kho

1. Nhấp vào **biểu tượng tồn kho** trên bất kỳ thẻ kho hàng nào để xem các mục tồn kho của nó
2. Hoặc di chuyển đến tab **Tồn kho** của sản phẩm để xem tồn kho trên tất cả kho hàng

Mỗi mục tồn kho hiển thị:
- **Tên sản phẩm** và biến thể (nếu có)
- **Có sẵn** — Tổng tồn kho vật lý
- **Đã phân bổ** — Số lượng được đặt giữ cho các đơn hàng đang chờ
- **Sẵn sàng** — Có sẵn trừ đi đã phân bổ (điều có thể được bán)

### Thêm tồn kho

1. Từ trang xem tồn kho kho hàng, nhấp **Thêm mục tồn kho**
2. Chọn sản phẩm và biến thể
3. Nhập số lượng **có sẵn**
4. Lưu

### Các hoạt động tồn kho

Mọi thay đổi đối với tồn kho được theo dõi như một **hoạt động tồn kho**:

| Loại hoạt động | Mô tả |
|--------------|-------------|
| **Nhận hàng** | Tồn kho mới nhận từ nhà cung cấp |
| **Bán hàng** | Tồn kho bị trừ đi cho đơn hàng đã được xử lý |
| **Trả hàng** | Tồn kho được trả lại từ khách hàng |
| **Điều chỉnh** | Sửa đổi thủ công (sai số đếm) |
| **Chuyển kho** | Chuyển giữa các kho hàng |
| **Đặt giữ** | Được giữ tạm thời cho giỏ hàng đang hoạt động |

Các hoạt động tồn kho cung cấp một bản ghi kiểm toán đầy đủ về các thay đổi tồn kho.

## Theo dõi tồn kho trên sản phẩm

### Bật theo dõi tồn kho

Trên tab **Tồn kho** của sản phẩm:

1. Chuyển đổi **Track Inventory** để bật quản lý tồn kho
2. Thiết lập **Low Stock Threshold** — kích hoạt cảnh báo khi tồn kho giảm xuống dưới mức này
3. Cấu hình **Allow Backorders** nếu bạn muốn chấp nhận đơn hàng khi hết hàng

### Tồn kho đa kho hàng

Khi theo dõi tồn kho được bật, tab Tồn kho hiển thị mức tồn kho trên tất cả kho hàng trong bảng tổng quan:

- Tổng số lượng có sẵn trên tất cả các vị trí
- Phân tích theo từng kho hàng
- Số lượng có sẵn sau khi trừ đi các đặt giữ và phân bổ

## Cảnh báo tồn kho thấp

Hệ thống tự động theo dõi mức tồn kho và cảnh báo bạn khi:
- Một sản phẩm giảm xuống dưới **ngưỡng tồn kho thấp** của nó
- Một sản phẩm đạt **số lượng tồn kho sẵn sàng bằng 0**

Cảnh báo tồn kho thấp xuất hiện tại:
- **Bảng điều khiển Cửa hàng** trong phần **Hành động cần thực hiện**
- Danh sách sản phẩm với chỉ báo trực quan

## Mẹo

- Bắt đầu với một kho hàng và thêm nhiều hơn khi doanh nghiệp phát triển.
- Thiết lập ưu tiên xử lý dựa trên tốc độ và chi phí vận chuyển đến từng khu vực.
- Sử dụng đệm tồn kho cho các vị trí bán lẻ để đảm bảo sẵn sàng tồn kho trên sàn.
- Kiểm tra thường xuyên các hoạt động tồn kho để phát hiện sự suy giảm hoặc sai lệch.
- Thiết lập ngưỡng tồn kho thấp dựa trên thời gian đặt hàng lại của bạn — nếu mất 2 tuần để bổ sung hàng, hãy đặt ngưỡng để bao phủ 2 tuần doanh số.
- Bật theo dõi tồn kho trước khi chính thức vận hành để tránh bán quá mức.