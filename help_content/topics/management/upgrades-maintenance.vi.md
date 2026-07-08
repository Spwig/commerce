---
title: Cập nhật & Bảo trì
---

Spwig nhận được các bản cập nhật định kỳ với các tính năng mới, cải tiến hiệu suất và sửa lỗi bảo mật. Hướng dẫn này sẽ hướng dẫn bạn cách nâng cấp cài đặt của mình, sử dụng công cụ chẩn đoán và xử lý các nhiệm vụ bảo trì.

## Cập nhật Spwig

### Trước khi nâng cấp

1. **Tạo bản sao lưu** — truy cập **Quản lý > Chỉ số hệ thống > Tạo bản sao lưu đầy đủ** hoặc chạy kịch bản sao lưu từ dòng lệnh. Đây là mạng lưới an toàn của bạn nếu có điều gì đó đi sai.
2. **Kiểm tra phiên bản hiện tại** — hiển thị tại **Quản lý > Chỉ số hệ thống** hoặc trên chân trang bảng điều khiển quản trị.
3. **Đọc ghi chú phát hành** — có sẵn trong bảng điều khiển quản trị dưới **Quản lý > Cập nhật thành phần** khi phát hiện phiên bản mới.

### Chạy nâng cấp

SSH vào máy chủ của bạn và di chuyển đến thư mục cài đặt Spwig (thường là `/opt/spwig`):

```bash
./upgrade.sh
```

Kịch bản nâng cấp:

1. **Kiểm tra trước bay** — xác minh không gian đĩa, tình trạng sức khỏe của Docker và trạng thái dịch vụ
2. **Chạy thử di chuyển cơ sở dữ liệu** — kiểm tra xem các thay đổi cơ sở dữ liệu sẽ được áp dụng một cách sạch sẽ mà không thực sự thay đổi bất cứ điều gì
3. **Vào chế độ bảo trì** — cửa hàng của bạn sẽ hiển thị trang bảo trì cho khách truy cập trong quá trình nâng cấp
4. **Tạo bản sao lưu** — bản sao lưu an toàn tự động trước khi thực hiện thay đổi
5. **Xả các công việc nền** — chờ các nhiệm vụ đang thực hiện (gửi email, dịch thuật) hoàn tất một cách trơn tru
6. **Tải xuống hình ảnh mới** — tải xuống ứng dụng đã cập nhật từ kho Spwig
7. **Áp dụng di chuyển cơ sở dữ liệu** — cập nhật lược đồ cơ sở dữ liệu cho phiên bản mới
8. **Khởi động lại dịch vụ** — chạy ứng dụng với phiên bản mới
9. **Kiểm tra sức khỏe** — xác minh tất cả dịch vụ đang chạy đúng cách
10. **Thoát khỏi chế độ bảo trì** — cửa hàng của bạn trở lại trực tuyến

Nếu kiểm tra sức khỏe thất bại sau khi nâng cấp, kịch bản sẽ **tự động quay lại** phiên bản trước đó và khôi phục bản sao lưu.

### Tùy chọn nâng cấp

```bash
./upgrade.sh              # Nâng cấp tiêu chuẩn với chế độ bảo trì
./upgrade.sh --dry-run    # Kiểm tra những thay đổi sẽ xảy ra mà không áp dụng
```

## Công cụ chẩn đoán

Spwig bao gồm một công cụ chẩn đoán tích hợp kiểm tra toàn bộ cài đặt của bạn để phát hiện vấn đề:

```bash
./doctor.sh
```

Bác sĩ kiểm tra:

| Danh mục | Điều gì nó kiểm tra |
|----------|---------------|
| **Hệ thống** | Không gian đĩa, sử dụng RAM, tải CPU |
| **Docker** | Sức khỏe của động cơ Docker, trạng thái container, phiên bản hình ảnh |
| **Cơ sở dữ liệu** | Kết nối PostgreSQL, trạng thái di chuyển, sức khỏe của bể chứa kết nối |
| **Bộ nhớ đệm** | Kết nối Redis, sử dụng bộ nhớ |
| **Lưu trữ đối tượng** | Kết nối MinIO, khả năng truy cập thùng chứa |
| **Mạng** | Giải quyết DNS, khả năng truy cập cổng, tính hợp lệ của chứng chỉ SSL |
| **Ứng dụng** | Các điểm cuối kiểm tra sức khỏe dịch vụ, trạng thái công việc nền |

Mỗi kiểm tra hiển thị kết quả thông qua hoặc thất bại với chi tiết nếu có điều gì đó sai.

### Chế độ sửa lỗi tự động

Đối với các vấn đề phổ biến, bác sĩ có thể cố gắng sửa lỗi tự động:

```bash
./doctor.sh --fix
```

Chế độ sửa lỗi tự động có thể giải quyết:

- Container đã dừng (khởi động lại chúng)
- Kết nối cơ sở dữ liệu lỗi thời (tái tạo bể chứa kết nối)
- Chứng chỉ SSL đã hết hạn (khởi động lại gia hạn)
- Ổ đĩa đầy do hình ảnh Docker cũ (xóa hình ảnh không sử dụng)

Bác sĩ luôn giải thích những gì nó sẽ sửa trước khi thực hiện hành động.

## Chế độ bảo trì

Chế độ bảo trì hiển thị cho khách truy cập một trang "cửa hàng tạm thời không khả dụng" khi bạn thực hiện các thay đổi. Bảng điều khiển quản trị vẫn có thể truy cập được.

### Kích hoạt chế độ bảo trì

Từ bảng điều khiển quản trị: **Cài đặt cửa hàng > Bảo trì > Kích hoạt chế độ bảo trì**

Hoặc từ dòng lệnh:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Tắt chế độ bảo trì

Từ bảng điều khiển quản trị: bật/tắt công tắc chế độ bảo trì.

Hoặc từ dòng lệnh:

```bash
./go-live.sh
```

### Bỏ qua quyền truy cập trong khi bảo trì

Khi chế độ bảo trì đang hoạt động, bạn có thể truy cập cửa hàng bình thường bằng cách thêm một tham số bí mật vào URL. Bí mật bỏ qua được hiển thị trong tệp cấu hình `.env` của bạn dưới `MAINTENANCE_SECRET`.

## Quản lý dịch vụ

### Xem trạng thái dịch vụ

Kiểm tra trạng thái của tất cả các dịch vụ Spwig:

```bash
docker compose ps
```

Điều này hiển thị từng dịch vụ, trạng thái của nó (đang chạy, đã dừng, đang khởi động lại) và trạng thái sức khỏe.

### Xem nhật ký

Kiểm tra nhật ký cho một dịch vụ cụ thể:

```bash
docker logs spwig_shop          # Nhật ký ứng dụng
docker logs spwig_celery         # Nhật ký công việc nền
docker logs spwig_nginx          # Nhật ký truy cập máy chủ web
docker logs spwig_db             # Nhật ký cơ sở dữ liệu
```

Thêm `--tail 100` để xem 100 dòng cuối cùng, hoặc `--follow` để theo dõi nhật ký theo thời gian thực.

### Khởi động lại dịch vụ

Nếu cần khởi động lại một dịch vụ cụ thể:

```bash
docker compose restart shop      # Khởi động lại ứng dụng
docker compose restart celery    # Khởi động lại công việc nền
docker compose restart nginx     # Khởi động lại máy chủ web
```

Để khởi động lại tất cả các dịch vụ:

```bash
docker compose restart
```

## Cập nhật thành phần

Spwig có một thị trường thành phần nơi bạn có thể cài đặt các chủ đề, nhà cung cấp thanh toán, tích hợp vận chuyển và các phần mở rộng khác. Các thành phần được cập nhật độc lập với nền tảng cốt lõi.

Truy cập **Management > Component Updates** để kiểm tra các bản cập nhật thành phần có sẵn. Các bản cập nhật được tải xuống và áp dụng tự động khi bạn phê duyệt chúng.

## Mẹo

- **Cập nhật thường xuyên** — việc duy trì phiên bản mới nhất đảm bảo bạn có các bản vá bảo mật và truy cập vào các tính năng mới
- **Luôn sao lưu trước** — mặc dù kịch bản nâng cấp tạo ra bản sao lưu tự động, việc có bản sao lưu riêng của bạn sẽ cung cấp thêm sự an toàn
- **Chạy doctor sau khi xảy ra sự cố** — nếu cửa hàng của bạn hoạt động bất thường, `./doctor.sh` là cách nhanh nhất để xác định vấn đề
- **Lên lịch nâng cấp vào thời gian ít lưu lượng truy cập** — chế độ bảo trì sẽ tạm thời làm gián đoạn quyền truy cập của khách hàng, vì vậy hãy nâng cấp vào giờ thấp điểm
- **Giữ không gian đĩa trống** — các bản nâng cấp cần không gian tạm thời cho các hình ảnh và bản sao lưu mới. Duy trì ít nhất 5 GB không gian trống.