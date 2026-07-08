---
title: Quản lý Token Đồng bộ
---

Token đồng bộ là các thông tin xác thực an toàn cho phép hai cài đặt Spwig giao tiếp với nhau. Trước khi bạn có thể đồng bộ cài đặt hoặc di chuyển dữ liệu giữa các cửa hàng, bạn cần tạo một token trên cửa hàng **nhận** và cung cấp nó cho cửa hàng **gửi**.

## Cách Token Đồng bộ Hoạt động

Token đồng bộ là một khóa API chỉ hiển thị một lần, được sử dụng để xác thực các yêu cầu giữa hai cài đặt Spwig. Khi bạn thiết lập kết nối, cửa hàng từ xa sử dụng token này để chứng minh rằng nó có quyền đọc hoặc ghi vào cửa hàng của bạn.

- Token được tạo trên cửa hàng sẽ **kết nối đến** (mục tiêu)
- Mỗi token chỉ có thể được xem một lần, ngay sau khi tạo
- Token có thể bị thu hồi bất kỳ lúc nào để ngay lập tức cắt quyền truy cập
- Một cửa hàng có thể có nhiều token đang hoạt động cho các kết nối khác nhau

## Tạo Token

1. Di chuyển đến **Data Migration > Spwig-to-Spwig Sync** trong thanh bên quản trị
2. Nhấn **Manage Tokens** trên bảng điều khiển đồng bộ
3. Nhập tên mô tả cho token (ví dụ: "Staging Server" hoặc "Production Sync")
4. Nhấn **Generate Token**
5. **Sao chép token ngay lập tức** -- nó sẽ không được hiển thị lại

> **Lưu ý:** Lưu trữ token một cách an toàn. Nếu bạn mất token, bạn sẽ cần tạo một token mới.

## Sử dụng Token

Sau khi bạn có token từ cửa hàng mục tiêu:

1. Di chuyển đến bảng điều khiển **Spwig-to-Spwig Sync** trên cửa hàng sẽ khởi động kết nối
2. Bắt đầu một **Settings Sync** hoặc **Full Migration** mới
3. Trong bước Kết nối, nhập URL cửa hàng mục tiêu và dán token
4. Nhấn **Test Connection** để kiểm tra xem nó có hoạt động không
5. Kết nối sẽ được lưu lại để sử dụng sau này

## Thu hồi Token

Nếu token bị rò rỉ hoặc không còn cần thiết:

1. Di chuyển đến **Manage Tokens** trên bảng điều khiển đồng bộ
2. Tìm token bạn muốn thu hồi
3. Nhấn nút **Revoke**
4. Xác nhận việc thu hồi

Việc thu hồi token có hiệu lực ngay lập tức. Mọi kết nối đang hoạt động sử dụng token đó sẽ ngừng hoạt động và cần được cấu hình lại với một token mới.

## Thực hành Tốt nhất

- **Đặt tên token một cách mô tả** để bạn biết token đó thuộc về kết nối nào
- **Thu hồi các token không sử dụng** để giảm thiểu rủi ro bảo mật
- **Tạo token riêng biệt** cho mỗi cửa hàng kết nối thay vì chia sẻ một token cho nhiều cửa hàng
- **Tạo lại token định kỳ** làm một phần trong thói quen bảo mật của bạn, đặc biệt sau khi có sự thay đổi nhân sự