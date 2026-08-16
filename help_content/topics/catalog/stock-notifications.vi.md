---
title: Thông báo tồn kho
---

Thông báo tồn kho cho phép khách hàng đăng ký nhận email khi sản phẩm hết hàng trở lại. Cài đặt hiển thị tồn kho kiểm soát những gì khách hàng thấy trên trang sản phẩm — bao gồm các nhãn trạng thái tồn kho, cảnh báo tồn kho thấp, và điều gì xảy ra khi sản phẩm hết hàng.

## Cài đặt hiển thị tồn kho

Cài đặt hiển thị tồn kho là cài đặt mặc định cho toàn bộ cửa hàng, áp dụng cho tất cả sản phẩm trừ khi bị ghi đè ở cấp độ danh mục hoặc sản phẩm.

Đi tới **Catalog > Cài đặt hiển thị tồn kho** để cấu hình các tùy chọn này. Có một bản ghi cài đặt cho cửa hàng của bạn — nhấp vào để chỉnh sửa.

### Hiển thị trạng thái tồn kho

| Cài đặt | Mô tả |
|---------|-------------|
| **Hiển thị trạng thái tồn kho** | Hiển thị nhãn "Còn hàng" hoặc "Hết hàng" trên trang sản phẩm |
| **Hiển thị cảnh báo tồn kho thấp** | Hiển thị thông báo "Chỉ còn X" khi tồn kho giảm xuống mức thấp |
| **Ngưỡng tồn kho thấp** | Số lượng tại hoặc dưới mức mà cảnh báo tồn kho thấp xuất hiện (mặc định: 5) |
| **Hiển thị số lượng chính xác** | Hiển thị số lượng còn lại chính xác (ví dụ: "Chỉ còn 3"!) thay vì cảnh báo chung |

### Hành vi khi hết hàng

Cài đặt **Hành vi khi hết hàng** xác định điều gì khách hàng thấy khi sản phẩm hết hàng:

| Hành vi | Điều khách hàng thấy |
|--------|-------------------|
| **Ẩn khỏi danh sách** | Sản phẩm bị xóa khỏi trang danh mục và kết quả tìm kiếm |
| **Hiển thị là không khả dụng** | Sản phẩm có thể nhìn thấy nhưng không thể thêm vào giỏ hàng |
| **Hiển thị nút "Nhắc tôi"** | Khách hàng có thể đăng ký email của họ để nhận thông báo khi hàng về |
| **Cho phép đặt hàng trước** | Khách hàng có thể mua sản phẩm ngay cả khi tồn kho bằng 0 |

Thiết lập **Thông báo hết hàng** để tùy chỉnh văn bản hiển thị khi sản phẩm không khả dụng (mặc định: `Hết hàng`).

Thiết lập **Thông báo đặt hàng trước** để tùy chỉnh văn bản hiển thị cho sản phẩm có thể đặt hàng trước (mặc định: `Có sẵn để đặt hàng trước`).

### Hiển thị vận chuyển và giao hàng

| Cài đặt | Mô tả |
|---------|-------------|
| **Hiển thị vị trí "Giao từ"** | Hiển thị tên kho hàng trên trang sản phẩm |
| **Hiển thị ngày giao hàng dự kiến** | Hiển thị ngày giao hàng dự kiến được tính toán từ vị trí kho hàng |

### Cho phép đặt hàng trước (toàn trang)

Kiểm tra **Cho phép đặt hàng trước** để cho phép khách hàng mua bất kỳ sản phẩm nào hết hàng nào theo mặc định. Các sản phẩm và danh mục riêng lẻ có thể ghi đè cài đặt này.

## Thông báo sản phẩm trở lại tồn kho

Khi bạn đặt hành vi hết hàng thành **Hiển thị nút "Nhắc tôi"**, khách hàng có thể nhập địa chỉ email của họ trên trang sản phẩm để nhận email khi sản phẩm có hàng trở lại.

### Xem các yêu cầu thông báo

Đi tới **Catalog > Thông báo tồn kho** để xem tất cả các yêu cầu thông báo của khách hàng. Mỗi bản ghi hiển thị:
- Địa chỉ email của khách hàng
- Sản phẩm và biến thể (nếu có)
- Kho hàng ưa thích (nếu khách hàng chọn sở thích khu vực)
- Khi nào yêu cầu được tạo
- Khi nào thông báo được gửi (trống nếu chưa gửi)

### Khi nào thông báo được gửi

Spwig gửi email thông báo khi sản phẩm hết hàng tự động khi mức tồn kho của sản phẩm vượt lên trên 0. Trường **Đã gửi lúc** ghi lại thời điểm email được gửi.

Khách hàng nhận được một email thông báo. Sau khi được thông báo, họ cần đăng ký lại nếu sản phẩm hết hàng lần nữa.

### Lọc các yêu cầu thông báo

Sử dụng bộ lọc admin để tìm:
- Các yêu cầu cho một sản phẩm cụ thể
- Các yêu cầu đã được thông báo (để xem ai đã được liên hệ)
- Các yêu cầu đang chờ (khách hàng đang chờ hàng về)

## Ghi đè ở cấp độ sản phẩm

Cài đặt hiển thị tồn kho toàn trang có thể bị ghi đè theo từng sản phẩm hoặc danh mục. Trên biểu mẫu chỉnh sửa sản phẩm, hãy tìm phần **Tồn kho** nơi bạn có thể đặt **Hành vi hết hàng** cụ thể cho sản phẩm khác với mặc định toàn trang.

Điều này hữu ích khi bạn muốn hầu hết sản phẩm cho phép đặt hàng trước nhưng giữ một số sản phẩm ở chế độ "Nhắc tôi" — hoặc khi một sản phẩm cụ thể nên bị ẩn khi hết hàng.

## Mẹo

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- Thiết lập **Ngưỡng hàng tồn kho thấp** ở mức điểm đặt hàng bạn thường sử dụng, để khách hàng được cảnh báo về tình trạng tồn kho hạn chế trước khi hết hàng hoàn toàn.
- Sử dụng tùy chọn **Hiện nút "Thông báo cho tôi"** thay vì ẩn sản phẩm hết hàng — những khách hàng đăng ký thể hiện nhu cầu thực tế có thể đưa ra lý do để đặt hàng bổ sung.
- Bật **Hiện số lượng chính xác** một cách có chọn lọc.

Đối với hầu hết các cửa hàng, việc hiển thị "Chỉ còn 3 cái!" hiệu quả hơn việc hiển thị số lượng chính xác, vì nó tạo ra cảm giác khẩn cấp mà không tiết lộ toàn bộ hình ảnh tồn kho của bạn.
- Kiểm tra danh sách thông báo tồn kho trước khi đặt đơn hàng mới — số lượng yêu cầu thông báo đang chờ cho thấy mức độ nhu cầu tồn tại cho sản phẩm đó.
- Nếu bạn sử dụng đặt hàng trước, cập nhật **Thông báo đặt hàng trước** để thiết lập kỳ vọng chính xác (ví dụ: "Giao hàng trong 2-3 tuần — đặt hàng ngay hôm nay để giữ chỗ của bạn").
- Kết hợp thông báo hết hàng với tiếp thị qua email: khi bạn nhập hàng cho sản phẩm được ưa chuộng, hãy gửi một chiến dịch đến tất cả những người đã đăng ký, chứ không chỉ gửi email thông báo tự động.