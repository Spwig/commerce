---
title: Hướng dẫn cài đặt
---

Hướng dẫn này sẽ hướng dẫn bạn cách cài đặt Spwig trên máy chủ của riêng bạn. Toàn bộ quy trình được tự động hóa — một lệnh duy nhất sẽ xử lý việc thiết lập Docker, tạo cơ sở dữ liệu, cấu hình dịch vụ và chứng chỉ SSL.

## Trước khi bắt đầu

Bạn cần:

- Một máy chủ chạy **Ubuntu 22.04 hoặc 24.04** (Debian 12 cũng được hỗ trợ)
- **Quyền root hoặc sudo** trên máy chủ
- Ít nhất **4 GB RAM** và **20 GB không gian đĩa** (khuyến nghị 8 GB RAM)
- Một **token giấy phép** từ việc mua Spwig của bạn (kiểm tra hóa đơn email của bạn)
- Tùy chọn, một **tên miền** được chỉ định đến địa chỉ IP của máy chủ

> **Lưu ý:** Bạn có thể cài đặt mà không cần tên miền và thêm tên miền sau này bằng công cụ cấu hình tên miền. Trong thời gian đó, cửa hàng của bạn sẽ có thể truy cập được qua địa chỉ IP của máy chủ.

## Chạy trình cài đặt

Kết nối với máy chủ của bạn qua SSH và chạy lệnh cài đặt từ email xác nhận mua hàng của bạn. Nó trông như thế này:

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash -s -- --token YOUR_LICENSE_TOKEN
```

Thay thế `YOUR_LICENSE_TOKEN` bằng token từ email của bạn.

Trình cài đặt sẽ tự động chạy qua tám giai đoạn:

1. **Kiểm tra trước (Pre-flight checks)** — xác minh máy chủ của bạn đáp ứng các yêu cầu (hệ điều hành, đĩa, RAM, cổng)
2. **Xác minh token** — xác nhận giấy phép của bạn và trích xuất cấu hình cửa hàng của bạn
3. **Phát hiện chế độ** — xác định chế độ cài đặt phù hợp nhất cho máy chủ của bạn (xem bên dưới)
4. **Cấu hình** — tạo mật khẩu an toàn, thông tin xác thực cơ sở dữ liệu và cấu hình dịch vụ
5. **Tải xuống hình ảnh** — tải hình ảnh ứng dụng Spwig từ kho
6. **Khởi động dịch vụ** — khởi động cơ sở dữ liệu, bộ đệm, ứng dụng và các công việc nền theo thứ tự
7. **Cấu hình SSL** — nhận chứng chỉ SSL nếu bạn đã cấu hình tên miền
8. **Hoàn tất** — tạo tài khoản quản trị của bạn và tạo các kịch bản tiện lợi

Quy trình mất 5–15 phút tùy thuộc vào tốc độ internet của máy chủ của bạn.

## Các chế độ cài đặt

Trình cài đặt tự động phát hiện môi trường máy chủ của bạn và chọn chế độ phù hợp nhất. Bạn cũng có thể chỉ định một chế độ cụ thể bằng cờ `--mode`.

### Chế độ độc lập

**Phù hợp nhất với:** Máy chủ chuyên dụng và các bản sao máy ảo nơi Spwig là ứng dụng web duy nhất.

- Sử dụng trực tiếp cổng 80 và 443
- Tự động xử lý chứng chỉ SSL thông qua Let's Encrypt
- Đây là chế độ phổ biến và được khuyến nghị nhất

### Chế độ Sidecar

**Phù hợp nhất với:** Máy chủ đã chạy một ứng dụng web khác (WordPress, trang web công ty, v.v.) trên cổng 80/443.

- Spwig chạy trên cổng thay thế (tự động phát hiện, thường là 8080 hoặc 8443)
- Trình cài đặt tạo một khối cấu hình proxy nginx để bạn thêm vào máy chủ web hiện có của bạn
- Máy chủ web hiện có của bạn xử lý SSL và proxy lưu lượng đến Spwig

### Chế độ cục bộ

**Phù hợp nhất với:** Phát triển và kiểm tra trên máy tính của riêng bạn.

- Chỉ có thể truy cập tại `localhost` hoặc `127.0.0.1`
- Sử dụng chứng chỉ SSL tự ký (trình duyệt của bạn sẽ hiển thị cảnh báo bảo mật — điều này là bình thường)
- Kích hoạt tính năng gỡ lỗi
- Không yêu cầu xác minh giấy phép

## Điều gì xảy ra trong quá trình cài đặt

### Docker

Nếu Docker chưa được cài đặt, trình cài đặt sẽ đề xuất cài đặt nó cho bạn. Spwig chạy hoàn toàn bên trong các container Docker — không có gì được cài đặt trực tiếp trên hệ điều hành máy chủ của bạn ngoài Docker.

### Các dịch vụ được tạo

Trình cài đặt tạo ra các dịch vụ sau:

| Dịch vụ | Mục đích |
|---------|---------|
| **Cơ sở dữ liệu** (PostgreSQL 16) | Lưu trữ tất cả dữ liệu cửa hàng của bạn — sản phẩm, đơn hàng, khách hàng, cài đặt |
| **Bộ nhớ đệm** (Redis) | Tăng tốc độ tải trang và quản lý hàng đợi tác vụ nền |
| **Bộ điều phối kết nối** (PgBouncer) | Quản lý kết nối cơ sở dữ liệu hiệu quả |
| **Lưu trữ đối tượng** (MinIO) | Lưu trữ hình ảnh, tệp và phương tiện đã tải lên |
| **Ứng dụng** (Spwig) | Bản thân cửa hàng — bảng điều khiển quản trị và giao diện người dùng |
| **Máy chủ web** (Nginx) | Cung cấp cửa hàng cho khách truy cập với nén và bộ nhớ đệm |
| **Công việc nền** (Celery) | Xử lý email, bản dịch, phân tích và các tác vụ nền khác |
| **Lịch trình công việc** (Celery Beat) | Chạy các tác vụ được lên lịch như sao lưu tự động và chiến dịch email |
| **Bộ dịch** | Dịch vụ dịch thuật được hỗ trợ bởi AI cho cửa hàng đa ngôn ngữ |
| **Bộ nâng cấp** | Xử lý việc cập nhật các thành phần từ thị trường Spwig |

### Tài khoản quản trị

Sau khi cài đặt xong, bạn sẽ được yêu cầu tạo tài khoản quản trị. Đây là tài khoản bạn sẽ sử dụng để đăng nhập vào bảng điều khiển quản trị cửa hàng của mình.

### Chế độ bảo trì

Cửa hàng của bạn bắt đầu ở **chế độ bảo trì** — người truy cập sẽ thấy trang "Sắp ra mắt". Điều này cho phép bạn thời gian để cấu hình cửa hàng (thêm sản phẩm, thiết lập phương thức thanh toán, tùy chỉnh giao diện của bạn) trước khi chính thức đi vào hoạt động.

Khi bạn đã sẵn sàng, hãy chạy kịch bản tiện lợi mà trình cài đặt đã tạo:

```bash
./go-live.sh
```

Hoặc tắt chế độ bảo trì từ **Quản trị > Cài đặt Cửa hàng > Bảo trì**.

## Sau khi cài đặt

Sau khi trình cài đặt hoàn tất, bạn sẽ thấy một bản tóm tắt với:

- URL cửa hàng của bạn
- URL bảng điều khiển quản trị (thường là `https://yourdomain.com/en/admin/`)
- Vị trí tệp cấu hình của bạn
- Các kịch bản tiện lợi có sẵn

### Kịch bản tiện lợi

Trình cài đặt tạo ra các kịch bản này trong thư mục cài đặt của bạn:

- **`./go-live.sh`** — đưa cửa hàng của bạn ra khỏi chế độ bảo trì
- **`./configure-domain.sh`** — thêm hoặc thay đổi tên miền và nhận chứng chỉ SSL

### Các bước tiếp theo

1. Đăng nhập vào bảng điều khiển quản trị của bạn
2. Hoàn thành **Chỉ dẫn Cài đặt** — nó sẽ hướng dẫn bạn qua tên cửa hàng, tiền tệ, múi giờ và cài đặt cơ bản
3. Thêm sản phẩm của bạn
4. Thiết lập phương thức thanh toán
5. Chọn và tùy chỉnh một giao diện
6. Chạy `./go-live.sh` khi đã sẵn sàng

## Cài đặt trên các thị trường điện toán đám mây

Spwig có sẵn dưới dạng ứng dụng một cú nhấp chuột trên một số nhà cung cấp đám mây:

- **DigitalOcean** — triển khai từ DigitalOcean Marketplace
- **Akamai (Linode)** — triển khai từ Linode Marketplace
- **Vultr** — triển khai từ Vultr Marketplace

Các hình ảnh thị trường này đi kèm với trình cài đặt đã được tải trước. Sau khi tạo máy chủ, SSH vào và làm theo hướng dẫn trên màn hình để hoàn tất cài đặt bằng mã token giấy phép của bạn.

## Nhận hỗ trợ

Nếu việc cài đặt thất bại hoặc bạn gặp lỗi:

1. Chạy **công cụ chẩn đoán**: `./doctor.sh` (tạo ra trong quá trình cài đặt)
2. Công cụ kiểm tra tất cả các dịch vụ, kết nối, SSL và các vấn đề phổ biến
3. Sử dụng `./doctor.sh --fix` để cố gắng sửa chữa tự động
4. Liên hệ với hỗ trợ Spwig cùng với đầu ra của công cụ chẩn đoán nếu vấn đề vẫn tồn tại