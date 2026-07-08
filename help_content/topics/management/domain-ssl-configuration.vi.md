---
title: Cấu hình tên miền & SSL
---

Hướng dẫn này giải thích cách kết nối tên miền tùy chỉnh với cửa hàng Spwig của bạn và thiết lập chứng chỉ SSL để truy cập HTTPS an toàn. Bạn có thể cấu hình tên miền trong quá trình cài đặt hoặc thêm sau đó.

## Thêm tên miền sau khi cài đặt

Nếu bạn đã cài đặt Spwig mà không có tên miền (sử dụng địa chỉ IP của máy chủ), bạn có thể thêm tên miền bất kỳ lúc nào.

### Bước 1: Thiết lập DNS

Với nhà đăng ký tên miền hoặc nhà cung cấp DNS của bạn:

1. Tạo **A record** chỉ định tên miền (hoặc tên miền con) của bạn đến địa chỉ IP của máy chủ
2. Nếu bạn sử dụng tên miền con như `shop.example.com`, tạo A record cho `shop`
3. Chờ đợi quá trình lan truyền DNS — điều này thường mất 5–60 phút

Kiểm tra xem bản ghi DNS đã hoạt động:

```bash
 dig +short shop.example.com
```

Điều này nên trả về địa chỉ IP của máy chủ của bạn.

### Bước 2: Chạy kịch bản cấu hình tên miền

SSH vào máy chủ của bạn và di chuyển đến thư mục cài đặt Spwig:

```bash
 ./configure-domain.sh
```

Kịch bản sẽ:

1. Yêu cầu tên miền của bạn
2. Kiểm tra xem DNS có chỉ định đến máy chủ của bạn không
3. Cập nhật cấu hình cửa hàng
4. Nhận một chứng chỉ SSL miễn phí từ Let's Encrypt
5. Cấu hình máy chủ web để sử dụng HTTPS
6. Khởi động lại các dịch vụ liên quan

Cửa hàng của bạn giờ đây có thể truy cập tại `https://yourdomain.com`.

### Bước 3: Cập nhật cài đặt cửa hàng

Sau khi thêm tên miền, đăng nhập vào bảng điều khiển quản trị của bạn và đi đến **Store Settings**. Kiểm tra xem **Store URL** khớp với tên miền mới của bạn. Điều này đảm bảo rằng email, hóa đơn và các liên kết sử dụng địa chỉ đúng.

## Chứng chỉ SSL

### SSL tự động (Let's Encrypt)

Trong **chế độ standalone**, trình cài đặt tự động nhận một chứng chỉ SSL miễn phí từ Let's Encrypt. Các chứng chỉ này:

- Được tất cả các trình duyệt chính thức tin cậy
- Có hiệu lực trong 90 ngày
- Tự động gia hạn — kiểm tra gia hạn diễn ra hàng ngày, và chứng chỉ sẽ được gia hạn khi còn ít hơn 30 ngày hiệu lực
- Bao phủ tên miền chính xác của bạn (ví dụ: `shop.example.com`)

Bạn không cần quản lý việc gia hạn thủ công.

### Chứng chỉ tự ký

Trong một số trường hợp, Spwig sử dụng chứng chỉ tự ký thay thế:

- **Chế độ local** (phát triển/test)
- Khi Let's Encrypt không thể truy cập máy chủ của bạn (cổng 80 bị tường lửa chặn, DNS chưa lan truyền)
- Khi không có tên miền được cấu hình (truy cập chỉ qua IP)

Chứng chỉ tự ký mã hóa lưu lượng nhưng không được trình duyệt tin cậy — người truy cập sẽ thấy cảnh báo bảo mật. Điều này chấp nhận được cho mục đích test nhưng không nên sử dụng trong môi trường sản xuất.

### SSL chế độ Sidecar

Trong **chế độ sidecar**, máy chủ web hiện tại của bạn (Apache, Nginx, Caddy, v.v.) xử lý việc chấm dứt SSL. Spwig chạy trên cổng HTTP phía sau proxy của bạn. Cấu hình SSL trên máy chủ web chính của bạn như bình thường.

Trình cài đặt tạo một khối cấu hình proxy bạn có thể thêm vào máy chủ web của bạn. Đối với Nginx, nó trông giống như:

```nginx
 location / {
     proxy_pass http://127.0.0.1:8080;
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
 }
```

## Thay đổi tên miền

Để chuyển sang tên miền khác:

1. Thiết lập DNS cho tên miền mới (A record chỉ đến máy chủ của bạn)
2. Chạy lại `./configure-domain.sh` với tên miền mới
3. Kịch bản sẽ cập nhật tất cả cấu hình, nhận chứng chỉ mới và khởi động lại các dịch vụ
4. Cập nhật **Store Settings** trong bảng điều khiển quản trị với URL mới

Tên miền cũ sẽ ngừng hoạt động sau khi cấu hình được cập nhật.

## Khắc phục sự cố

### "DNS validation failed"

Kịch bản configure-domain kiểm tra xem tên miền của bạn có chỉ đến máy chủ của bạn không trước khi yêu cầu chứng chỉ. Nếu kiểm tra này thất bại:

- Kiểm tra lại A record bằng `dig +short yourdomain.com`
- Chờ thêm vài phút để DNS lan truyền
- Kiểm tra xem bạn có đang cấu hình tên miền hoặc tên miền con chính xác (không phải wildcard)

### "Let's Encrypt rate limit reached"

Let's Encrypt giới hạn yêu cầu chứng chỉ là 5 lần mỗi tên miền mỗi tuần. Nếu bạn đạt giới hạn này:



- Chờ 7 ngày trước khi thử lại
- Trong thời gian đó, hãy sử dụng một subdomain khác
- Cửa hàng vẫn có thể truy cập được qua HTTP hoặc bằng chứng chỉ tự ký trong khi bạn chờ

### "Cổng 80 không thể truy cập"

Let's Encrypt phải kết nối đến máy chủ của bạn qua cổng 80 để xác minh quyền sở hữu tên miền. Đảm bảo:

- Tường lửa của bạn cho phép kết nối TCP vào cổng 80
- Không có ứng dụng nào đang chặn cổng 80
- Nhóm bảo mật hoặc tường lửa mạng của nhà cung cấp đám mây cho phép cổng 80

### Lỗi gia hạn chứng chỉ

Nếu gia hạn tự động thất bại, chứng chỉ sẽ hết hạn sau 90 ngày. Để gia hạn thủ công:

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

Kiểm tra nhật ký gia hạn để xem chi tiết nếu việc này thất bại. Nguyên nhân phổ biến nhất là cổng 80 bị chặn bởi thay đổi tường lửa sau khi cài đặt ban đầu.