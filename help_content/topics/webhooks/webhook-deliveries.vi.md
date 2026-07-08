---
title: Lịch sử giao webhook
---

Mỗi lần cửa hàng của bạn cố gắng gửi một webhook, một mục nhật ký giao hàng sẽ được tạo. Những nhật ký này cho phép bạn xem chính xác những gì đã được gửi, liệu nó có thành công hay không, và điều gì đã xảy ra trong bất kỳ lần thử lại nào. Hướng dẫn này giải thích cách đọc nhật ký giao hàng và gỡ lỗi khi giao hàng thất bại.

## Xem lịch sử giao hàng

Truy cập **Tích hợp > Giao hàng webhook** để xem toàn bộ lịch sử các lần giao webhook cho tất cả các điểm cuối của bạn.

![Lịch sử giao webhook](/static/core/admin/img/help/webhook-deliveries/delivery-list.webp)

Danh sách hiển thị tên điểm cuối, loại sự kiện, trạng thái, mã phản hồi HTTP, thời gian phản hồi và số lần thử đã được thực hiện cho mỗi lần giao hàng.

Nhật ký giao hàng chỉ đọc — chúng được tạo tự động khi sự kiện xảy ra và không thể chỉnh sửa.

## Trạng thái giao hàng

Mỗi lần giao hàng có một trong những trạng thái sau:

| Trạng thái | Ý nghĩa |
|------------|---------|
| **Chờ xử lý** | Lần giao hàng đang được xếp hàng và chưa được thực hiện |
| **Thành công** | Máy chủ nhận đã phản hồi với mã trạng thái HTTP 2xx — giao hàng được xác nhận |
| **Thất bại** | Tất cả các lần thử giao hàng đã được sử dụng hết — giao hàng sẽ không được thử lại |
| **Đang thử lại** | Lần thử gần nhất đã thất bại, nhưng hệ thống sẽ thử lại vào thời gian thử lại đã lên lịch |
| **Bị chặn trong môi trường sandbox** | Lần giao hàng bị chặn vì URL điểm cuối không thể truy cập trong môi trường hiện tại |

Một lần giao hàng được coi là thành công khi máy chủ nhận trả về bất kỳ mã phản hồi HTTP 2xx nào (200, 201, 202, v.v.). Mọi mã phản hồi khác — bao gồm cả 3xx chuyển hướng hoặc lỗi 4xx/5xx — được coi là thất bại.

## Lọc giao hàng

Sử dụng bảng điều khiển lọc bên phải để thu hẹp danh sách:

- **Trạng thái** — Chỉ xem giao hàng thất bại, đang thử lại hoặc thành công
- **Loại sự kiện** — Xem tất cả giao hàng cho một sự kiện cụ thể (ví dụ: tất cả giao hàng `order.created`)
- **Điểm cuối** — Xem giao hàng cho một điểm cuối cụ thể
- **Tạo lúc** — Lọc theo khoảng thời gian

Sử dụng thanh tìm kiếm để tìm kiếm theo loại sự kiện hoặc tên điểm cuối, hoặc tìm một giao hàng cụ thể theo ID của nó.

## Xem chi tiết giao hàng

Nhấp vào bất kỳ giao hàng nào để xem chi tiết đầy đủ. Các bản ghi giao hàng chỉ đọc.

### Tóm tắt

- **ID** — Nhận dạng duy nhất cho lần giao hàng này
- **Điểm cuối** — Điểm cuối webhook nào đã nhận được lần giao này (liên kết đến bản ghi điểm cuối)
- **Loại sự kiện** — Sự kiện nào đã kích hoạt lần giao này (ví dụ: `order.paid`)
- **Trạng thái** — Trạng thái giao hàng hiện tại

### Gói tin (Payload)

Phần **Gói tin** hiển thị dữ liệu JSON chính xác đã được gửi đến điểm cuối của bạn. Điều này bao gồm loại sự kiện, thời gian dấu thời gian và dữ liệu sự kiện đầy đủ. Sử dụng phần này để xác minh máy chủ nhận của bạn có nhận được cấu trúc dữ liệu đúng hay không.

### Phản hồi (Response)

Phần **Phản hồi** hiển thị nội dung mà máy chủ của bạn đã trả về:

- **Mã trạng thái phản hồi** — Mã trạng thái HTTP do máy chủ của bạn trả về. Màu sắc được mã hóa: xanh cho 2xx (thành công), vàng cho 4xx (lỗi phía khách hàng), đỏ cho 5xx (lỗi phía máy chủ).
- **Thời gian phản hồi** — Thời gian máy chủ của bạn mất để phản hồi, tính bằng miligiây. Màu sắc được mã hóa: xanh nếu dưới 500ms, vàng nếu lên đến 2 giây, đỏ nếu trên 2 giây.
- **Nội dung phản hồi** — Nội dung phản hồi từ máy chủ của bạn (giới hạn 1.000 ký tự). Điều này có thể giúp xác định lý do máy chủ của bạn từ chối webhook.
- **Tiêu đề phản hồi** — Các tiêu đề được trả về bởi máy chủ của bạn.

### Chi tiết lỗi

Nếu giao hàng thất bại, phần **Chi tiết lỗi** hiển thị thông báo lỗi — ví dụ: `Kết nối bị từ chối`, `Hết thời gian sau 30 giây`, hoặc lỗi HTTP từ máy chủ của bạn.

### Thông tin thử lại

- **Số lần thử** — Số lần giao hàng đã được thực hiện (bao gồm cả lần thử đầu tiên)
- **Lần thử tiếp theo lúc** — Thời gian thử lại tiếp theo sẽ được thực hiện (chỉ hiển thị cho các giao hàng có trạng thái **Đang thử lại**)

Các lần thử lại tuân theo lịch trình giảm dần theo cấp số nhân — khoảng thời gian giữa các lần thử tăng lên theo từng lần thử để tránh làm quá tải máy chủ tạm thời không khả dụng. Với tối đa 5 lần thử lại (mặc định), lịch trình thử lại kéo dài qua nhiều giờ.

## Thử lại giao hàng thất bại bằng tay

Nếu bạn muốn thử lại giao hàng ngay lập tức mà không cần chờ lịch tự động:

1. Chọn các ô kiểm bên cạnh các giao hàng bạn muốn thử lại
2. Từ danh sách thả xuống **Action**, chọn **Retry selected deliveries**
3. Nhấn **Go**

Chỉ các giao hàng không ở trạng thái **Success** sẽ được xếp hàng để thử lại. Các giao hàng thành công sẽ bị bỏ qua.

Điều này hữu ích khi bạn đã khắc phục vấn đề trên máy chủ nhận của mình và muốn xử lý lại các sự kiện thất bại mà không cần chờ đợi.

## Chẩn đoán các lỗi phổ biến

### Mã phản hồi HTTP 4xx

Một phản hồi 4xx từ máy chủ của bạn thường có nghĩa là có vấn đề với yêu cầu — xác thực thất bại, URL điểm đến đã thay đổi, hoặc máy chủ của bạn đã từ chối định dạng payload. Kiểm tra:

- URL điểm đến có đúng không?
- Máy chủ của bạn có đang kiểm tra chữ ký HMAC đúng cách không? Sự không khớp sẽ khiến nhiều máy chủ trả về 401 hoặc 403.
- Cấu trúc payload có thay đổi không? So sánh payload trong nhật ký giao hàng với điều mà máy chủ của bạn kỳ vọng.

### Mã phản hồi HTTP 5xx

Một phản hồi 5xx có nghĩa là máy chủ của bạn đã gặp lỗi nội bộ khi xử lý webhook. Kiểm tra nhật ký lỗi của riêng máy chủ để chẩn đoán vấn đề.

### Connection refused / Timeout

Các lỗi này có nghĩa là Spwig hoàn toàn không thể kết nối đến máy chủ của bạn:

- Máy chủ có đang chạy và có thể truy cập công khai không?
- URL có đúng không (bao gồm giao thức đúng — http hoặc https)?
- Tường lửa có đang chặn các yêu cầu đến không?
- Thời gian phản hồi của máy chủ có vượt quá thời gian chờ được cấu hình không? Nếu có, hãy tăng cài đặt **Timeout** trên điểm đến hoặc tối ưu hóa trình xử lý webhook của máy chủ để phản hồi nhanh chóng (tốt nhất là trong vòng 5 giây).

### Sandbox Blocked

Các giao hàng bị chặn đến các URL localhost hoặc địa chỉ mạng nội bộ. Các điểm đến webhook phải có thể truy cập công khai. Sử dụng một công cụ như ngrok trong quá trình phát triển để mở máy chủ cục bộ ra bên ngoài.

## Mẹo

- Xử lý các giao hàng **Failed** kịp thời — dữ liệu sự kiện vẫn còn trong payload, và bạn có thể thử lại thủ công sau khi khắc phục vấn đề.
- Nếu bạn thấy nhiều giao hàng **Retrying** cho một điểm đến, hãy mở bản ghi điểm đến và kiểm tra phần **Health** — điểm đến có thể sắp bị tắt tự động.
- Thời gian phản hồi quan trọng: cấu hình trình xử lý webhook của bạn để phản hồi nhanh chóng (trong vài giây) và xử lý payload một cách bất đồng bộ ở phía sau. Một trình xử lý chậm sẽ gây ra lỗi timeout ngay cả khi logic của bạn là chính xác.
- Sử dụng bộ lọc **Event Type** để kiểm tra lịch sử giao hàng cho một loại sự kiện cụ thể khi điều tra xem tích hợp của bạn có đang nhận các sự kiện đúng không.
- Nhật ký giao hàng tích lũy theo thời gian. Sử dụng bộ lọc ngày để tập trung vào các giao hàng gần đây và tránh phải lướt qua lịch sử cũ.