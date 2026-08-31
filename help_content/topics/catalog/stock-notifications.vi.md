---
title: Thông báo tồn kho
---

Thông báo tồn kho cho phép khách hàng đăng ký để nhận email khi một sản phẩm hết hàng có sẵn trở lại. Các cài đặt hiển thị tồn kho kiểm soát những gì khách hàng nhìn thấy trên trang sản phẩm — chẳng hạn như nhãn trạng thái tồn kho, cảnh báo sắp hết hàng và những gì xảy ra khi một sản phẩm hết hàng.

## Cài đặt hiển thị tồn kho

Các cài đặt hiển thị tồn kho là mặc định trên toàn bộ cửa hàng, áp dụng cho tất cả các sản phẩm trừ khi được ghi đè ở cấp danh mục hoặc cấp sản phẩm.

Điều hướng đến **Catalog > Stock Display Settings** để cấu hình các tùy chọn này. Có một bản ghi cài đặt cho cửa hàng của bạn — nhấp vào đó để chỉnh sửa.

### Hiển thị trạng thái tồn kho

| Cài đặt | Mô tả |
|---------|-------------|
| **Show Stock Status** | Hiển thị nhãn "In Stock" hoặc "Out of Stock" trên trang sản phẩm |
| **Show Low Stock Warning** | Hiển thị thông báo "Only X left" khi tồn kho sắp hết |
| **Low Stock Threshold** | Số lượng mà tại hoặc dưới mức đó cảnh báo sắp hết hàng sẽ xuất hiện (mặc định: 5) |
| **Show Exact Quantity** | Hiển thị số lượng chính xác còn lại (ví dụ: "Only 3 left!") thay vì cảnh báo chung chung |

### Hành vi khi hết hàng

Cài đặt **Out of Stock Action** xác định những gì khách hàng nhìn thấy khi một sản phẩm không có sẵn hàng:

| Hành động | Khách hàng nhìn thấy gì |
|--------|-------------------|
| **Hide from listings** | Sản phẩm bị xóa khỏi các trang danh mục và kết quả tìm kiếm |
| **Show as unavailable** | Sản phẩm hiển thị nhưng không thể thêm vào giỏ hàng |
| **Show "Notify Me" button** | Khách hàng có thể đăng ký email của họ để được thông báo khi hàng có lại |
| **Allow backorders** | Khách hàng có thể mua sản phẩm ngay cả khi tồn kho bằng không |

Đặt **Out of Stock Message** để tùy chỉnh văn bản hiển thị khi một sản phẩm không có sẵn (mặc định: `Out of Stock`).

Đặt **Backorder Message** để tùy chỉnh văn bản hiển thị cho các sản phẩm có thể đặt trước (mặc định: `Available on backorder`).

### Hiển thị vận chuyển và giao hàng

| Cài đặt | Mô tả |
|---------|-------------|
| **Show "Ships From" location** | Hiển thị tên kho trên trang sản phẩm |
| **Show Estimated Delivery** | Hiển thị ngày giao hàng ước tính được tính từ vị trí kho |

### Cho phép đặt trước (toàn bộ trang web)

Đánh dấu **Allow Backorders** để cho phép khách hàng mua bất kỳ sản phẩm nào hết hàng theo mặc định. Các sản phẩm và danh mục riêng lẻ có thể ghi đè cài đặt này.

## Thông báo có hàng trở lại

Khi bạn đặt hành động hết hàng thành **Show "Notify Me" button**, khách hàng có thể nhập địa chỉ email của họ trên trang sản phẩm để nhận email khi sản phẩm được bổ sung hàng.

### Xem các yêu cầu thông báo

Điều hướng đến **Catalog > Stock Notifications** để xem tất cả các yêu cầu thông báo từ khách hàng. Mỗi bản ghi hiển thị:
- Địa chỉ email của khách hàng
- Sản phẩm và biến thể (nếu có)
- Kho ưu tiên (nếu khách hàng đã chọn tùy chọn khu vực)
- Thời điểm yêu cầu được tạo
- Thời điểm thông báo được gửi (trống nếu chưa gửi)

### Khi nào thông báo được gửi

Spwig tự động gửi email có hàng trở lại khi mức tồn kho của một sản phẩm tăng lên trên không. Trường **Notified At** ghi lại thời điểm email được gửi.

Khách hàng nhận một email thông báo. Sau khi được thông báo, họ cần đăng ký lại nếu sản phẩm hết hàng lần thứ hai.

Nếu bạn muốn gửi nhiều hơn một cảnh báo đơn giản — ví dụ, hiển thị sản phẩm có hàng trở lại với một khối nội dung **Featured Product**, hoặc theo dõi một ngày sau đó — hãy xây dựng một hành trình **Product back in stock** trong **Campaign Studio > Journeys** và đặt nó ở trạng thái **Active**. Một khi hành trình đó tồn tại, các khách hàng đang chờ sẽ được ghi danh vào đó thay vì nhận email đơn giản một lần; nếu không có hành trình nào đang hoạt động, email một lần này sẽ tiếp tục gửi đúng như đã mô tả ở trên. Xem [Triggered Journeys](/help/triggered-journeys) để biết cách hoạt động của bộ kích hoạt.

### Lọc các yêu cầu thông báo

Sử dụng bộ lọc quản trị để tìm:
- Các yêu cầu cho một sản phẩm cụ thể
- Các yêu cầu đã được thông báo (để xem ai đã được liên hệ)
- Các yêu cầu vẫn đang chờ (khách hàng đang chờ hàng có lại)

## Ghi đè ở cấp độ sản phẩm

Cài đặt hiển thị tồn kho trên toàn bộ trang web có thể được ghi đè theo từng sản phẩm hoặc danh mục. Trong biểu mẫu chỉnh sửa sản phẩm, hãy tìm phần **Tồn kho** nơi bạn có thể thiết lập **Hành động hết hàng** cụ thể cho sản phẩm, khác với mặc định toàn cục.

Điều này hữu ích khi bạn muốn hầu hết các sản phẩm cho phép đặt hàng trước nhưng giữ một số sản phẩm ở chế độ "Thông báo cho tôi" — hoặc khi một sản phẩm cụ thể nên được ẩn khi hết hàng.

## Mẹo

- Đặt **Ngưỡng tồn kho thấp** thành điểm đặt lại hàng mà bạn thường sử dụng, để khách hàng được cảnh báo về số lượng có hạn trước khi bạn hết hàng hoàn toàn.
- Sử dụng tùy chọn **Hiển thị nút "Thông báo cho tôi"** thay vì ẩn các sản phẩm hết hàng — khách hàng đăng ký đại diện cho nhu cầu thực tế có thể hợp lý hóa một đơn đặt hàng bổ sung.
- Bật **Hiển thị số lượng chính xác** một cách thận trọng. Đối với hầu hết các cửa hàng, hiển thị "Chỉ còn 3!" hoạt động tốt hơn so với việc hiển thị số lượng chính xác, vì nó tạo ra sự khẩn cấp mà không tiết lộ toàn bộ bức tranh tồn kho của bạn.
- Kiểm tra danh sách thông báo tồn kho trước khi đặt một đơn hàng mới — số lượng yêu cầu thông báo đang chờ cho bạn biết mức độ nhu cầu tồn tại cho sản phẩm đó.
- Nếu bạn sử dụng đặt hàng trước, hãy cập nhật **Thông báo đặt hàng trước** để thiết lập kỳ vọng chính xác (ví dụ: "Giao hàng trong 2-3 tuần — đặt hàng ngay để giữ chỗ của bạn").
- Kết hợp thông báo hết hàng với tiếp thị qua email: khi bạn bổ sung hàng cho một sản phẩm phổ biến, hãy gửi chiến dịch đến tất cả những người đã đăng ký, không chỉ email thông báo tự động.