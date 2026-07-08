---
title: API Tokens
---

API tokens là các khóa an toàn cho phép các dịch vụ bên ngoài và tích hợp giao tiếp với cửa hàng của bạn. Khi một dịch vụ bên thứ ba hoặc công cụ cần truy cập dữ liệu cửa hàng của bạn hoặc kích hoạt các hành động, nó sẽ gửi một API token cùng với mỗi yêu cầu để cửa hàng của bạn có thể xác minh yêu cầu đó đã được ủy quyền. Bạn tạo và quản lý tất cả các token từ phần API Tokens trong bảng điều khiển quản trị của bạn.

## Khi bạn cần một API token

Bạn thường sẽ cần tạo một API token khi:

- Kết nối một dịch vụ bên ngoài hoặc công cụ tự động hóa cần đọc từ hoặc ghi vào cửa hàng của bạn
- Thiết lập một receiver webhook cần xác thực các cuộc gọi đến
- Cấu hình Hệ thống Hỗ trợ Spwig cho cài đặt của bạn
- Xây dựng một tích hợp tùy chỉnh sử dụng API của Spwig
- Đồng bộ dữ liệu giữa cửa hàng Spwig của bạn và hệ thống khác

Mỗi tích hợp nên có riêng một token để bạn có thể thu hồi quyền truy cập cho một dịch vụ mà không ảnh hưởng đến các dịch vụ khác.

## Loại token

Khi tạo một token, bạn chọn một loại mô tả mục đích của nó. Loại này dành cho tham khảo của bạn và giúp bạn theo dõi được mỗi token làm gì.

| Loại | Mục đích |
|------|---------|
| **Hệ thống Hỗ trợ** | Được sử dụng bởi hệ thống tài liệu hỗ trợ Spwig |
| **Tích hợp bên ngoài** | Các dịch vụ bên thứ ba, công cụ tự động hóa (ví dụ: Zapier), hoặc công cụ đồng bộ dữ liệu |
| **Webhook** | Xác thực cho các receiver webhook hoặc endpoint |
| **Tùy chỉnh** | Bất kỳ mục đích nào không phù hợp với các danh mục trên |
| **Đồng bộ Cài đặt** | Đồng bộ giữa các cài đặt Spwig hoặc dịch vụ Spwig bên ngoài |

## Tạo một API token

1. Di chuyển đến **Cài đặt > API Tokens**
2. Nhấp **+ Thêm API Token**
3. Nhập một **Tên** mô tả rõ ràng mục đích của token (ví dụ: `Zapier Product Sync` hoặc `Help System API`)
4. Chọn loại **Token** phù hợp
5. Tùy chọn thêm **Mô tả** với chi tiết hơn về tích hợp
6. Cấu hình trạng thái **Hoạt động**, **Ngày hết hạn**, và **IP được phép** theo nhu cầu (xem bên dưới)
7. Nhấp **Lưu**

Sau khi lưu, giá trị đầy đủ của token sẽ được hiển thị trên trang chi tiết. **Sao chép ngay lập tức** — token sẽ được che giấu trong danh sách xem để đảm bảo an ninh và không thể lấy lại đầy đủ sau khi bạn rời khỏi trang này.

![Chi tiết Token API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## An ninh giá trị token

Spwig chỉ hiển thị giá trị đầy đủ của token một lần: ngay sau khi bạn lưu một token mới. Sau đó, danh sách chỉ hiển thị một phiên bản được che giấu (ví dụ: `spw_••••••••••••••••••••3f8a`).

Nếu bạn mất giá trị token, bạn không thể khôi phục lại. Bạn sẽ cần xóa token cũ và tạo một token mới, sau đó cập nhật tích hợp đang sử dụng nó.

**Không bao giờ chia sẻ giá trị token qua email, tin nhắn chat, hoặc mã nguồn.** Xử lý chúng như mật khẩu.

## Thiết lập ngày hết hạn

Trường **Hết hạn lúc** thiết lập một ngày và giờ sau đó token sẽ ngừng hoạt động tự động. Để trống nếu token không nên hết hạn.

Ngày hết hạn hữu ích cho:

- Các tích hợp tạm thời với ngày kết thúc cố định
- Các token được cấp cho bên thứ ba mà bạn muốn tự động xóa quyền truy cập
- Thêm một lớp bảo mật bổ sung cho các tích hợp có quyền cao

Khi token hết hạn, các yêu cầu sử dụng nó sẽ bị từ chối. Bạn có thể mở rộng quyền truy cập bằng cách cập nhật ngày **Hết hạn lúc** hoặc tạo một token thay thế.

## Giới hạn đến các địa chỉ IP cụ thể

Trường **IP được phép** chấp nhận danh sách các địa chỉ IP. Khi danh sách không trống, token chỉ hoạt động khi yêu cầu đến từ một trong những địa chỉ đó.

Ví dụ, nếu công cụ phân tích của bạn chạy trên máy chủ tại `203.0.113.42`, việc thêm địa chỉ IP này có nghĩa là token không thể bị lạm dụng từ bất kỳ vị trí nào khác, ngay cả khi nó bị rò rỉ.

Để trống **IP được phép** để cho phép yêu cầu đến từ bất kỳ địa chỉ IP nào.

## Theo dõi việc sử dụng token

Danh sách token hiển thị:

- **Số lần sử dụng** — tổng số lần token đã được sử dụng
- **Lần sử dụng cuối cùng** — khi token được sử dụng lần cuối để thực hiện yêu cầu

Các trường này giúp bạn xác định các token không được sử dụng (ứng viên cho việc thu hồi) và phát hiện hoạt động bất thường.

Một sự gia tăng đột ngột trong số lần sử dụng có thể cho thấy token đang được sử dụng bởi người khác ngoài tích hợp được chỉ định.

## Hủy bỏ một token

Để ngay lập tức dừng hoạt động của một token mà không xóa nó:

1. Nhấp vào tên token
2. Bỏ chọn **Active**
3. Lưu

Token vẫn tồn tại trong danh sách của bạn để tham khảo nhưng sẽ bị từ chối trong mọi yêu cầu tiếp theo. Điều này hữu ích khi bạn cần tạm dừng một tích hợp trong khi điều tra một vấn đề.

Để xóa vĩnh viễn một token:

1. Chọn ô kiểm của nó trong danh sách
2. Chọn **Delete selected API tokens** từ menu hành động
3. Xác nhận xóa

Sau khi xóa, token không thể phục hồi. Nếu tích hợp vẫn cần truy cập, hãy tạo một token mới và cập nhật cấu hình của tích hợp.

## Ví dụ: thiết lập tích hợp Zapier

**Tình huống:** Bạn muốn kết nối cửa hàng của mình với Zapier để tự động hóa thông báo đơn hàng.

| Field | Value |
|-------|-------|
| Name | `Zapier Order Automation` |
| Token Type | External Integration |
| Description | Used by Zapier to read new orders and trigger notifications |
| Active | Yes |
| Expires At | *(leave blank)* |
| Allowed IPs | *(leave blank — Zapier uses dynamic IPs)* |

Sau khi lưu, sao chép giá trị token đầy đủ và dán vào cài đặt tích hợp Spwig của Zapier.

## Mẹo

- Đặt tên rõ ràng và cụ thể cho mỗi token — `Shopify Sync v2` hữu ích hơn nhiều so với `Token 3` khi bạn đang khắc phục sự cố vài tháng sau
- Tạo một token cho mỗi tích hợp — nếu một tích hợp bị xâm nhập, bạn có thể hủy bỏ chỉ token đó mà không làm gián đoạn bất kỳ tích hợp nào khác
- Đặt ngày hết hạn cho các token được sử dụng trong các dự án một lần hoặc tích hợp tạm thời — điều này giảm nguy cơ các token bị quên vẫn hoạt động vô thời hạn
- Kiểm tra danh sách token của bạn mỗi vài tháng và ngừng hoạt động bất kỳ token nào có ngày **Last Used** bất thường cũ, vì những token này có thể thuộc về các tích hợp không còn đang chạy
- Nếu bạn nghi ngờ một token đã bị tiết lộ, hãy ngừng hoạt động nó ngay lập tức, tạo một token thay thế, và cập nhật tích hợp bị ảnh hưởng trước khi bật lại quyền truy cập