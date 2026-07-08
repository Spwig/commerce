---
title: Thông báo tồn kho
---

Thông báo tồn kho cho phép khách hàng đăng ký nhận email khi sản phẩm hết hàng trở lại có sẵn. Cài đặt hiển thị tồn kho kiểm soát những gì khách hàng thấy trên các trang sản phẩm — như nhãn trạng thái tồn kho, cảnh báo tồn kho thấp, và điều gì xảy ra khi sản phẩm hết hàng.

## Cài đặt hiển thị tồn kho

Cài đặt hiển thị tồn kho là cài đặt mặc định cho toàn bộ cửa hàng, áp dụng cho tất cả sản phẩm trừ khi bị ghi đè ở cấp độ danh mục hoặc sản phẩm.

Truy cập **Catalog > Stock Display Settings** để cấu hình các tùy chọn này. Có một bản ghi cài đặt cho cửa hàng của bạn — nhấp vào để chỉnh sửa.

### Hiển thị trạng thái tồn kho

| Cài đặt | Mô tả |
|---------|-------------|
| **Hiển thị trạng thái tồn kho** | Hiển thị nhãn "In Stock" hoặc "Out of Stock" trên các trang sản phẩm |
| **Hiển thị cảnh báo tồn kho thấp** | Hiển thị thông báo "Chỉ còn X sản phẩm" khi tồn kho đang giảm |
| **Ngưỡng tồn kho thấp** | Số lượng tại hoặc dưới mức mà cảnh báo tồn kho thấp hiển thị (mặc định: 5) |
| **Hiển thị số lượng chính xác** | Hiển thị số lượng cụ thể còn lại (ví dụ: "Chỉ còn 3 sản phẩm!") thay vì cảnh báo chung |

### Hành vi khi hết hàng

Cài đặt **Hành động khi hết hàng** xác định những gì khách hàng thấy khi sản phẩm không còn tồn kho:

| Hành động | Những gì khách hàng thấy |
|--------|-------------------|
| **Ẩn khỏi danh sách** | Sản phẩm bị xóa khỏi trang danh mục và kết quả tìm kiếm |
| **Hiển thị là không có sẵn** | Sản phẩm vẫn hiển thị nhưng không thể thêm vào giỏ hàng |
| **Hiển thị nút "Thông báo cho tôi"** | Khách hàng có thể đăng ký email để được thông báo khi sản phẩm trở lại có sẵn |
| **Cho phép đặt hàng trước** | Khách hàng có thể mua sản phẩm ngay cả khi tồn kho bằng 0 |

Đặt **Thông báo khi hết hàng** để tùy chỉnh văn bản hiển thị khi sản phẩm không có sẵn (mặc định: `Out of Stock`).

Đặt **Thông báo đặt hàng trước** để tùy chỉnh văn bản hiển thị cho các sản phẩm có thể đặt hàng trước (mặc định: `Available on backorder`).

### Hiển thị vận chuyển và giao hàng

| Cài đặt | Mô tả |
|---------|-------------|
| **Hiển thị vị trí "Giao từ"** | Hiển thị tên kho trên trang sản phẩm |
| **Hiển thị thời gian giao hàng ước tính** | Hiển thị thời gian giao hàng được tính toán từ vị trí kho |

### Cho phép đặt hàng trước (toàn trang web)

Chọn **Cho phép đặt hàng trước** để cho phép khách hàng mua bất kỳ sản phẩm nào hết hàng theo mặc định. Các sản phẩm và danh mục riêng lẻ có thể ghi đè cài đặt này.

## Thông báo trở lại tồn kho

Khi bạn đặt hành động khi hết hàng thành **Hiển thị nút "Thông báo cho tôi"**, khách hàng có thể nhập địa chỉ email của họ trên trang sản phẩm để nhận email khi sản phẩm được bổ sung tồn kho.

### Xem yêu cầu thông báo

Truy cập **Catalog > Stock Notifications** để xem tất cả yêu cầu thông báo của khách hàng. Mỗi bản ghi hiển thị:
- Địa chỉ email của khách hàng
- Sản phẩm và biến thể (nếu có)
- Kho ưa thích (nếu khách hàng chọn sở thích khu vực)
- Thời gian yêu cầu được tạo
- Thời gian thông báo được gửi (trống nếu chưa gửi)

### Khi nào thông báo được gửi

Spwig tự động gửi email thông báo trở lại tồn kho khi mức tồn kho của sản phẩm tăng lên trên 0. Trường **Notified At** ghi lại thời điểm email được gửi.

Khách hàng nhận được một email thông báo. Một khi đã được thông báo, họ cần đăng ký lại nếu sản phẩm hết hàng lần thứ hai.

### Lọc yêu cầu thông báo

Sử dụng bộ lọc quản trị để tìm:
- Yêu cầu cho sản phẩm cụ thể
- Yêu cầu đã được thông báo (để xem ai đã được liên hệ)
- Yêu cầu vẫn đang chờ (khách hàng đang chờ sản phẩm được bổ sung)

## Ghi đè theo cấp độ sản phẩm

Các cài đặt hiển thị tồn kho toàn trang web có thể bị ghi đè theo từng sản phẩm hoặc danh mục. Trên biểu mẫu chỉnh sửa sản phẩm, tìm phần **Stock** nơi bạn có thể đặt hành động **Out of Stock Action** riêng cho sản phẩm, khác với cài đặt mặc định toàn cục.

Điều này hữu ích khi bạn muốn hầu hết các sản phẩm cho phép đặt hàng trước nhưng giữ một vài sản phẩm ở chế độ "Thông báo cho tôi" — hoặc khi một sản phẩm cụ thể nên bị ẩn khi hết hàng.

## Mẹo

Bảo toàn tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- Đặt **Ngưỡng Hàng Tồn Kho Thấp** thành điểm đặt hàng bạn thường sử dụng, để khách hàng được cảnh báo về tình trạng hàng hóa khan hiếm trước khi bạn hết hàng hoàn toàn.
- Sử dụng tùy chọn **Hiển thị Nút "Thông Báo"** thay vì ẩn sản phẩm hết hàng — những khách hàng đăng ký đại diện cho nhu cầu thực tế có thể chứng minh cho việc đặt hàng bổ sung.
- Bật tính năng **Hiển Thị Số Lượng Chính Xác** một cách tiết chế.

Đối với hầu hết các cửa hàng, việc hiển thị "Chỉ còn 3 sản phẩm!" hiệu quả hơn việc hiển thị số lượng chính xác, vì nó tạo ra sự khẩn cấp mà không tiết lộ toàn bộ tình hình tồn kho của bạn.
- Kiểm tra danh sách thông báo tồn kho trước khi đặt hàng mới — số lượng yêu cầu thông báo đang chờ cho bạn biết mức độ nhu cầu đối với sản phẩm đó.
- Nếu bạn sử dụng đặt hàng trước, hãy cập nhật **Thông Báo Đặt Hàng Trước** để thiết lập kỳ vọng chính xác (ví dụ: "Giao hàng trong 2-3 tuần — đặt hàng ngay để giữ chỗ của bạn").
- Kết hợp thông báo hết hàng với marketing qua email: khi bạn bổ sung hàng cho một sản phẩm phổ biến, hãy gửi chiến dịch đến tất cả những người đã đăng ký, không chỉ email thông báo tự động.