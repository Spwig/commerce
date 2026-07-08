---
title: Mẫu tin nhắn SMS
---

Các mẫu tin nhắn SMS kiểm soát văn bản của mọi thông báo mà cửa hàng của bạn gửi đến khách hàng qua tin nhắn văn bản. Mỗi mẫu tương ứng với một sự kiện cụ thể - như xác nhận đơn hàng hoặc cập nhật vận chuyển - và sử dụng các biến thay thế mà Spwig thay thế bằng thông tin đơn hàng thực tế khi tin nhắn được gửi.

Truy cập **Hệ thống SMS > Mẫu tin nhắn SMS** để xem và chỉnh sửa các mẫu của bạn.

![Danh sách mẫu tin nhắn SMS](/static/core/admin/img/help/sms-templates/templates-list.webp)

## Các loại mẫu có sẵn

Spwig bao gồm các loại mẫu sau đây được tích hợp sẵn:

| Loại Mẫu | Khi nào được gửi |
|----------|------------------|
| Xác nhận đơn hàng | Khi khách hàng đặt hàng |
| Cập nhật vận chuyển | Khi trạng thái theo dõi đơn hàng thay đổi |
| Thông báo giao hàng | Khi đơn hàng được đánh dấu là đã giao |
| Đặt lại mật khẩu | Khi khách hàng yêu cầu đặt lại mật khẩu |
| Mã xác minh | Khi cần mã một lần cho xác minh tài khoản |
| Hóa đơn POS | Khi xử lý bán hàng tại máy tính tiền |
| Marketing | Cho chiến dịch quảng cáo (yêu cầu đăng ký riêng biệt) |
| Tùy chỉnh | Cho bất kỳ thông báo nào bạn tạo |

## Chỉnh sửa mẫu

1. Truy cập **Hệ thống SMS > Mẫu tin nhắn SMS**
2. Nhấp vào mẫu bạn muốn chỉnh sửa
3. Cập nhật trường **Thông điệp** với văn bản mong muốn của bạn
4. Sử dụng các biến thay thế `{biến}` để bao gồm thông tin cụ thể về đơn hàng (xem các biến bên dưới)
5. Chọn **Kích hoạt** để bật mẫu - các mẫu không kích hoạt sẽ không được gửi
6. Nhấp **Lưu**

![Chỉnh sửa mẫu tin nhắn SMS](/static/core/admin/img/help/sms-templates/template-edit.webp)

## Sử dụng biến

Các biến là các placeholder được viết trong dấu ngoặc nhọn - ví dụ: `{tên}` hoặc `{số đơn hàng}`. Khi Spwig gửi tin nhắn, nó sẽ thay thế mỗi placeholder bằng giá trị thực tế cho khách hàng hoặc đơn hàng đó.

### Các biến phổ biến

| Biến | Được thay thế bằng |
|------|-------------------|
| `{tên}` | Tên của khách hàng |
| `{số đơn hàng}` | Số tham chiếu của đơn hàng |
| `{tổng}` | Tổng số tiền của đơn hàng |
| `{số theo dõi}` | Số theo dõi vận chuyển |
| `{tên cửa hàng}` | Tên cửa hàng của bạn |
| `{mã}` | Mã xác minh hoặc đặt lại mật khẩu |

**Ví dụ thông điệp:**

```
Chào {tên}, đơn hàng #{số đơn hàng} của bạn đã được xác nhận. Tổng: {tổng}. Chúng tôi sẽ cập nhật bạn khi nó được vận chuyển. - {tên cửa hàng}
```

Khi được gửi, nó sẽ trở thành:

```
Chào Sarah, đơn hàng #10045 của bạn đã được xác nhận. Tổng: $89.00. Chúng tôi sẽ cập nhật bạn khi nó được vận chuyển. - Cửa hàng Hoa Tươi
```

> Chỉ bao gồm các biến có sẵn cho loại mẫu cụ thể. Ví dụ, `{số theo dõi}` có sẵn trong mẫu Cập nhật vận chuyển nhưng không có trong mẫu Đặt lại mật khẩu. Nếu bạn sử dụng một biến không có sẵn, nó sẽ xuất hiện nguyên vẹn (không được thay thế) trong tin nhắn.

## Giới hạn ký tự và độ dài tin nhắn

Các tin nhắn SMS tiêu chuẩn bị giới hạn **160 ký tự** cho một phần. Tin nhắn dài hơn sẽ được chia thành nhiều phần và được gửi như một tin nhắn được ghép nối (concatenated SMS), nhưng các nhà cung cấp tính toán từng phần riêng biệt cho mục đích tính phí.

**Mẹo để giữ trong giới hạn:**
- Giữ tin nhắn ngắn gọn - một mục đích cho mỗi tin nhắn
- Viết tắt các cụm từ phổ biến khi tự nhiên (ví dụ: "Ord" thay vì "Order")
- Tránh các từ lấp đầy không cần thiết

Spwig không áp dụng giới hạn ký tự cứng trong trình chỉnh sửa, vì vậy hãy đếm số ký tự (bao gồm giá trị biến) trước khi lưu.

## Kích hoạt và tắt mẫu

Nút **Kích hoạt** trên mỗi mẫu kiểm soát việc thông báo loại đó có được gửi hay không. Nếu mẫu không được kích hoạt, Spwig sẽ bỏ qua việc gửi thông báo đó hoàn toàn - tin nhắn sẽ xuất hiện như **Bỏ qua** trong hộp thư ra SMS với lý do `template_inactive`.

Để kích hoạt mẫu:
1. Mở mẫu
2. Chọn hộp **Kích hoạt**
3. Lưu

Để tắt (ngừng gửi loại thông báo mà không xóa mẫu):
1. Mở mẫu
2. Bỏ chọn **Kích hoạt**
3. Lưu

## Mẹo

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- Viết tin nhắn theo giọng nói phù hợp với thương hiệu của bạn — SMS là kênh trực tiếp và cá nhân, vì vậy giọng điệu thân thiện hoạt động tốt
- Luôn bao gồm tên cửa hàng của bạn trong tin nhắn để khách hàng biết ai đang nhắn tin cho họ
- Giữ tin nhắn xác nhận đơn hàng ngắn gọn: số đơn hàng, tổng số tiền và một chú thích về các bước tiếp theo là đủ
- Thử nghiệm tin nhắn bằng cách đặt một đơn hàng kiểm tra trên cửa hàng của bạn (sử dụng số điện thoại bạn kiểm soát) để xem chính xác khách hàng nhận được gì
- Nếu một thông báo gây nhầm lẫn hoặc nhận được khiếu nại, hãy vô hiệu hóa mẫu đó và sửa đổi thay vì xóa — như vậy bạn có thể kích hoạt lại nó sau khi cập nhật
- Mẫu quảng cáo chỉ có thể được gửi đến những khách hàng đã đồng ý rõ ràng để nhận tin nhắn quảng cáo qua SMS, như yêu cầu bởi các quy định về viễn thông ở hầu hết các quốc gia