---
title: Mẫu email
---

Các mẫu email kiểm soát thiết kế và nội dung của mọi email tự động mà cửa hàng của bạn gửi đến khách hàng và đến bạn — xác nhận đơn hàng, cập nhật vận chuyển, đặt lại mật khẩu, thông báo hoàn tiền, và nhiều hơn nữa. Việc chỉnh sửa một mẫu sẽ thay đổi tất cả các email tương lai cùng loại; các email trước đó đã có trong hộp thư ra sẽ không bị ảnh hưởng.

Truy cập **Hệ thống email > Mẫu email** để xem và quản lý các mẫu của bạn.

![Danh sách mẫu email](/static/core/admin/img/help/email-templates/templates-list.webp)

## Loại mẫu

Cửa hàng của bạn bao gồm các mẫu cho một loạt các sự kiện rộng lớn. Chúng được phân nhóm theo danh mục:

### Các mẫu gửi đến khách hàng
| Mẫu | Gửi khi |
|----------|-----------|
| Xác nhận đơn hàng | Một khách hàng hoàn tất một lần mua hàng |
| Xác nhận thanh toán | Một thanh toán được xử lý thành công |
| Đơn hàng đã gửi | Một đơn hàng được đánh dấu là đã gửi |
| Xác nhận vận chuyển | Một số theo dõi vận chuyển được thêm vào |
| Xác nhận giao hàng | Một đơn hàng được đánh dấu là đã giao |
| Đơn hàng đã hủy | Một đơn hàng bị hủy |
| Thông báo chậm trễ đơn hàng | Một sự chậm trễ được ghi nhận trên đơn hàng |
| Thông báo hoàn tiền | Một khoản hoàn tiền được phát hành |

### Các mẫu liên quan đến tài khoản
| Mẫu | Gửi khi |
|----------|-----------|
| Chào mừng tài khoản | Một khách hàng tạo tài khoản |
| Mời tài khoản | Bạn mời một khách hàng tạo tài khoản |
| Xác minh email | Một khách hàng xác minh địa chỉ email của họ |
| Đặt lại mật khẩu | Một khách hàng yêu cầu đặt lại mật khẩu |

### Hoàn trả
| Mẫu | Gửi khi |
|----------|-----------|
| Hoàn trả: Yêu cầu đã nhận | Một khách hàng gửi yêu cầu hoàn trả |
| Hoàn trả: Được chấp thuận | Yêu cầu hoàn trả được chấp thuận |
| Hoàn trả: Bị từ chối | Yêu cầu hoàn trả bị từ chối |
| Hoàn trả: Gói đã nhận | Mặt hàng hoàn trả đến tại địa điểm của bạn |
| Hoàn trả: Hoàn tiền đã xử lý | Hoàn tiền cho một lần hoàn trả được phát hành |

### Thông báo quản trị (gửi đến bạn)
| Mẫu | Gửi khi |
|----------|-----------|
| Quản trị: Đơn hàng mới | Một đơn hàng mới được đặt |
| Quản trị: Thanh toán thất bại | Một lần thanh toán thất bại |
| Quản trị: Báo cáo doanh thu hàng ngày | Tóm tắt doanh thu hàng ngày được tạo |
| Quản trị: Cảnh báo hàng tồn kho thấp | Một sản phẩm giảm xuống dưới ngưỡng hàng tồn kho |
| Quản trị: Tóm tắt hàng tuần | Tóm tắt cửa hàng hàng tuần được tạo |

Các mẫu bổ sung bao gồm các mốc theo dõi vận chuyển, hoạt động chương trình liên kết, xác nhận đặt chỗ (nếu tính năng đặt chỗ được bật), và các sự kiện chương trình trung thành.

## Chỉnh sửa mẫu

1. Truy cập **Hệ thống email > Mẫu email**
2. Tìm mẫu bạn muốn chỉnh sửa. Bạn có thể lọc theo **Loại mẫu**, **Ngôn ngữ**, hoặc **Trạng thái** bằng cách sử dụng các bộ lọc bên phải
3. Nhấp vào mẫu để mở nó
4. Chỉnh sửa dòng **Tiêu đề** (tiêu đề email được hiển thị trong hộp thư của khách hàng)
5. Chỉnh sửa **Nội dung HTML** cho phiên bản thiết kế đầy đủ của email
6. Tùy chọn chỉnh sửa **Nội dung văn bản** — một phiên bản văn bản đơn giản làm phương án dự phòng cho các trình khách hàng email không hỗ trợ HTML
7. Nhấp **Lưu**

> **Email HTML:** Trường nội dung HTML chấp nhận HTML tiêu chuẩn bao gồm CSS inline. Spwig sẽ hiển thị nội dung này thành một email được định dạng đúng. Nếu bạn sử dụng mã MJML, nó sẽ được biên dịch tự động khi lưu.

## Xem trước mẫu

Trước khi lưu, bạn có thể xem trước cách mẫu sẽ hiển thị trong trình khách hàng email:

1. Mở mẫu bạn muốn xem trước
2. Nhấp vào nút **Xem trước** (hiển thị trong danh sách mẫu hoặc trên trang chi tiết mẫu)
3. Một xem trước sẽ mở ra trong một tab trình duyệt mới hiển thị email đã được hiển thị

Điều này cho phép bạn kiểm tra bố cục, định dạng và cách hiển thị biến thay thế trước khi mẫu được đưa vào sử dụng.

## Biến mẫu

Các biến là các vị trí thay thế trong mẫu của bạn mà Spwig thay thế bằng dữ liệu thực tế khi gửi email. Chúng được viết dưới dạng `{{ variable_name }}`.

Các biến phổ biến có sẵn trong hầu hết các mẫu:

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Biến | Được thay thế bằng |
|----------|---------------|
| `{{ customer_name }}` | Họ và tên đầy đủ của khách hàng |
| `{{ order_number }}` | Số tham chiếu đơn hàng |
| `{{ order_total }}` | Tổng số tiền đơn hàng |
| `{{ store_name }}` | Tên cửa hàng của bạn |
| `{{ store_url }}` | Địa chỉ web của cửa hàng bạn |
| `{{ tracking_number }}` | Số theo dõi vận chuyển |
| `{{ tracking_url }}` | Liên kết có thể nhấp để theo dõi vận chuyển |

Các biến cụ thể có sẵn phụ thuộc vào loại mẫu. Các biến liên quan đến mẫu liên quan đến đơn hàng (như `{{ order_number }}`) không có sẵn trong mẫu tài khoản (như Khôi phục mật khẩu). Nếu bạn bao gồm một biến không áp dụng, nó sẽ xuất hiện trống hoặc không được thay thế.

## Hỗ trợ ngôn ngữ

Mỗi loại mẫu có thể có một phiên bản cho mỗi ngôn ngữ mà cửa hàng của bạn hỗ trợ. Trường **Ngôn ngữ** trên mỗi mẫu kiểm soát phiên bản ngôn ngữ nào đang hoạt động.

Spwig tự động chọn phiên bản ngôn ngữ đúng dựa trên sở thích ngôn ngữ của khách hàng khi gửi. Nếu không có mẫu nào tồn tại cho ngôn ngữ của khách hàng, Spwig sẽ chuyển hướng đến phiên bản tiếng Anh.

Để thêm mẫu cho ngôn ngữ mới:
1. Mở một mẫu hiện có
2. Nhấp vào **Clone Template** từ menu **Actions**
3. Đặt **Language Code** trên bản sao thành ngôn ngữ mới
4. Dịch nội dung
5. Kích hoạt mẫu đã sao chép

## Sao chép, kích hoạt và ngừng kích hoạt mẫu

### Sao chép mẫu

Sao chép tạo ra bản sao chính xác của một mẫu — hữu ích để tạo các biến thể ngôn ngữ hoặc kiểm tra các phiên bản khác nhau mà không ảnh hưởng đến mẫu đang chạy.

1. Chọn một hoặc nhiều mẫu trong danh sách
2. Chọn **Clone selected templates** từ dropdown **Actions**
3. Bản sao được tạo ra là không hoạt động — chỉnh sửa nó và kích hoạt khi sẵn sàng

### Kích hoạt và ngừng kích hoạt mẫu

Một mẫu phải được **Active** để được sử dụng để gửi. Chỉ có một mẫu hoạt động cho mỗi loại và kết hợp ngôn ngữ được sử dụng tại một thời điểm.

Để kích hoạt hoặc ngừng kích hoạt theo lô:
1. Chọn các mẫu
2. Chọn **Activate selected templates** hoặc **Deactivate selected templates** từ dropdown **Actions**

Hoặc mở một mẫu riêng lẻ và chuyển đổi hộp kiểm **Active**.

## Mẫu hệ thống

Các mẫu được đánh dấu với nhãn **System** là các mẫu mặc định được cung cấp bởi Spwig. Chúng không thể bị xóa. Bạn có thể chỉnh sửa chúng trực tiếp hoặc sao chép chúng để tạo phiên bản tùy chỉnh.

## Một số lưu ý

- Luôn xem trước mẫu sau khi chỉnh sửa để phát hiện các vấn đề định dạng trước khi khách hàng nhìn thấy chúng
- Giữ tiêu đề ngắn gọn và cụ thể — `Đơn hàng #10045 của bạn đã được giao hàng` hiệu quả hơn so với các tiêu đề chung như `Cập nhật từ cửa hàng của chúng tôi`
- Chỉnh sửa nội dung văn bản đơn giản cũng — một số trình khách hàng chỉ hiển thị phiên bản văn bản đơn giản, và một số khách hàng ưa thích nó hơn
- Sao chép phiên bản tiếng Anh của một mẫu làm điểm bắt đầu trước khi tạo phiên bản đã dịch
- Nếu bạn muốn kiểm tra một thay đổi mà không ảnh hưởng đến các email đang chạy, sao chép mẫu, chỉnh sửa bản sao, và giữ cả hai hoạt động trong thời gian ngắn khi bạn xác minh bản xem trước — sau đó ngừng kích hoạt mẫu gốc
- Các mẫu thông báo quản trị (như **Admin: New Order**) được gửi đến địa chỉ email quản trị của cửa hàng bạn — đảm bảo rằng địa chỉ email đó chính xác trong cài đặt cửa hàng của bạn