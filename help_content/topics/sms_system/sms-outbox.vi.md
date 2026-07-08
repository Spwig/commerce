---
title: Hộp thư ra SMS
---

Hộp thư ra SMS là bản ghi đầy đủ của mọi tin nhắn văn bản mà cửa hàng của bạn đã cố gắng gửi. Sử dụng nó để xác nhận rằng thông báo đã đến được khách hàng, điều tra các lỗi giao hàng và hiểu rõ hoạt động nhắn tin tổng thể của bạn.

Truy cập **Hệ thống SMS > Hộp thư ra SMS** để xem nhật ký tin nhắn.

![Danh sách Hộp thư ra SMS với nhãn trạng thái](/static/core/admin/img/help/sms-outbox/outbox-list.webp)

## Đọc hộp thư ra

Mỗi hàng trong hộp thư ra đại diện cho một lần gửi tin nhắn và hiển thị:

- **Số điện thoại** — số điện thoại của người nhận
- **Loại tin nhắn** — SMS hoặc WhatsApp
- **Trạng thái** — trạng thái giao hàng hiện tại (xem bên dưới)
- **Tạo lúc** — thời điểm tin nhắn được tạo
- **Gửi lúc** — thời điểm tin nhắn được gửi đến nhà cung cấp

Thanh tổng quan ở trên hiển thị số lượng tổng hợp cho các trạng thái quan trọng nhất để bạn dễ dàng xem qua.

## Trạng thái tin nhắn

| Trạng thái | Ý nghĩa |
|------------|---------|
| Chờ xử lý | Tin nhắn đang chờ được lấy vào hàng đợi gửi |
| Đã xếp hàng | Tin nhắn đã được xếp hàng và sẽ được gửi trong vài phút |
| Đã gửi | Nhà cung cấp đã chấp nhận tin nhắn để giao |
| Đã giao | Nhà cung cấp đã xác nhận tin nhắn đã đến thiết bị người nhận |
| Thất bại | Nhà cung cấp đã từ chối hoặc không thể giao tin nhắn |
| Bỏ qua | Việc gửi đã được bỏ qua cố ý (xem lý do bỏ qua bên dưới) |
| Ghi lại trong môi trường sandbox | Tin nhắn chỉ được ghi lại (cửa hàng đang ở chế độ kiểm thử/môi trường sandbox) |

> **Đã gửi vs Đã giao:** Trạng thái **Đã gửi** có nghĩa là tin nhắn đã rời khỏi cửa hàng và được nhà cung cấp chấp nhận. Trạng thái **Đã giao** có nghĩa là nhà cung cấp đã nhận được biên lai giao hàng từ nhà mạng. Không phải tất cả nhà cung cấp đều hỗ trợ biên lai giao hàng — nếu nhà cung cấp của bạn không hỗ trợ, tin nhắn có thể hiển thị **Đã gửi** nhưng sẽ không bao giờ tiến đến **Đã giao**, điều này là bình thường.

## Xem chi tiết tin nhắn

Nhấp vào bất kỳ hàng nào trong hộp thư ra để xem chi tiết đầy đủ của tin nhắn đó:

- Nội dung **Tin nhắn** đầy đủ đã được gửi
- **ID tin nhắn của nhà cung cấp** — số tham chiếu từ nhà cung cấp SMS (hữu ích khi liên hệ với bộ phận hỗ trợ nhà cung cấp)
- **Thông báo lỗi** (cho tin nhắn thất bại) — thông báo lỗi chính xác được trả về từ nhà cung cấp
- **Số lần thử lại** — số lần Spwig đã cố gắng gửi tin nhắn
- Tất cả các thời điểm (tạo, xếp hàng, gửi, giao)

## Lọc hộp thư ra

Sử dụng các bộ lọc ở bên phải để thu hẹp danh sách:

- **Trạng thái** — chỉ hiển thị tin nhắn với trạng thái cụ thể
- **Loại tin nhắn** — chỉ hiển thị SMS hoặc chỉ hiển thị tin nhắn WhatsApp
- **Ngày** — lọc theo ngày tin nhắn được tạo

Ô tìm kiếm ở trên đầu cho phép bạn tìm kiếm theo số điện thoại, nội dung tin nhắn hoặc ID tin nhắn của nhà cung cấp.

## Hiểu lý do bỏ qua

Các tin nhắn bị bỏ qua không được gửi vì Spwig xác định việc gửi là không phù hợp hoặc không cần thiết. Các lý do bỏ qua phổ biến:

| Lý do bỏ qua | Ý nghĩa |
|--------------|---------|
| `user_preference_disabled` | Khách hàng đã tắt thông báo SMS trong cài đặt tài khoản của họ |
| `unsubscribed` | Khách hàng đã hủy đăng ký nhận tin nhắn SMS |
| `no_provider` | Không có tài khoản nhà cung cấp SMS mặc định hoạt động được cấu hình |
| `template_inactive` | Mẫu tin nhắn cho loại thông báo này đang không hoạt động |

Một tin nhắn bị bỏ qua không phải là lỗi — điều này có nghĩa là hệ thống đã hoạt động như dự kiến. Tuy nhiên, số lượng cao của các lần bỏ qua `no_provider` cho thấy bạn cần cấu hình và kích hoạt tài khoản nhà cung cấp SMS.

## Khắc phục lỗi giao hàng thất bại

Nếu tin nhắn hiển thị trạng thái **Thất bại**, hãy thực hiện các bước sau:

1. Nhấp vào tin nhắn thất bại để xem **Thông báo lỗi**
2. Các nguyên nhân lỗi phổ biến:

   | Lỗi | Nguyên nhân có thể |
   |-------|-------------|
   | Số điện thoại không hợp lệ | Số điện thoại của khách hàng bị thiếu hoặc không ở định dạng E.164 |
   | Xác thực thất bại | Thông tin xác thực của nhà cung cấp không hợp lệ hoặc đã hết hạn — cập nhật chúng trong **Tài khoản Nhà cung cấp SMS** |
   | Tài khoản bị đình chỉ | Tài khoản nhà cung cấp của bạn đã bị đình chỉ — đăng nhập vào bảng điều khiển của nhà cung cấp |
   | Thiếu số dư | Số dư tài khoản nhà cung cấp của bạn quá thấp — nạp thêm số dư |
   | Nhà mạng từ chối | Nhà mạng đích đã chặn tin nhắn (thường do bộ lọc nội dung) |

3. Sau khi khắc phục nguyên nhân gốc, các tin nhắn trong tương lai sẽ được gửi bình thường — hộp thư ra là một bản ghi chỉ đọc và các tin nhắn riêng lẻ không thể được gửi lại thủ công

## Hộp thư ra chỉ đọc

Hộp thư ra SMS là một bản ghi chỉ đọc. Bạn không thể thêm tin nhắn vào hộp thư ra một cách thủ công, và bạn không thể gửi lại các tin nhắn riêng lẻ từ đây. Các tin nhắn được Spwig gửi tự động khi các sự kiện liên quan xảy ra (ví dụ, một đơn hàng được đặt).

## Một số lưu ý

- Kiểm tra hộp thư ra sau một khoảng thời gian bận rộn để xác nhận tất cả các tin nhắn xác nhận đơn hàng đã được gửi thành công
- Nếu khách hàng nói rằng họ không nhận được tin nhắn SMS, hãy tìm kiếm hộp thư ra theo số điện thoại của họ để xem tin nhắn có được gửi, thất bại hoặc bỏ qua không
- Một sự gia tăng đột ngột trong các tin nhắn **Thất bại** thường cho thấy có vấn đề với thông tin xác thực hoặc số dư tài khoản nhà cung cấp — kiểm tra ngay các yếu tố này
- Nếu bạn thấy nhiều tin nhắn **Bỏ qua** với lý do `no_provider`, hãy chuyển đến **Hệ thống SMS > Tài khoản Nhà cung cấp SMS** và đảm bảo rằng một tài khoản mặc định đang hoạt động được cấu hình
- Cấu trúc ngày ở đầu danh sách cho phép bạn dễ dàng điều hướng theo ngày, tháng hoặc năm để xem các tin nhắn lịch sử