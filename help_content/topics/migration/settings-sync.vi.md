---
title: Cài đặt Đồng bộ
---

Cài đặt Đồng bộ cho phép bạn sao chép cấu hình cửa hàng giữa hai cài đặt Spwig. Điều này lý tưởng để duy trì môi trường staging và production, nơi bạn cấu hình và kiểm tra các thay đổi trên staging trước khi triển khai chúng đến cửa hàng trực tuyến của bạn.

## Khi Nên Sử Dụng Đồng Bộ Cài Đặt

- **Staging đến Production**: Cấu hình cài đặt trên cửa hàng staging của bạn, sau đó đẩy chúng đến production
- **Production đến Staging**: Kéo cài đặt production vào staging để bắt đầu với môi trường phù hợp
- **Sao Lưu Cài Đặt**: Kéo cài đặt từ production vào một phiên bản sao lưu như một biện pháp bảo vệ

Cài đặt Đồng bộ chỉ xử lý dữ liệu cấu hình - nó không chuyển sản phẩm, khách hàng, đơn hàng hoặc tệp phương tiện. Để chuyển dữ liệu hoàn chỉnh, hãy sử dụng Di chuyển Hệ thống Toàn bộ thay vào đó.

## Những Điều Có Thể Đồng Bộ

Cài đặt Đồng bộ hỗ trợ các danh mục sau:

| Nhóm | Danh Mục |
|-------|-----------|
| **Cài Đặt** | Cài Đặt Website, Thuế & Tiền Tệ, Mức Thuế, Ngôn Ngữ, Cài Đặt Blog, Chia Sẻ Xã Hội, Khu Vực Bán Hàng & Kho, Cấu Hình Tìm Kiếm, Trường Tùy Chỉnh, Vai Trò Nhân Viên, Phân Tích Khách Hàng |
| **Thiết Kế** | Thiết Kế & Giao Diện, Tiêu Đề/Chân Trang/Menú |
| **Nhà Cung Cấp** | Email, SMS/WhatsApp, Nhà Cung Cấp Thanh Toán, Giao Hàng, Nhà Cung Cấp SEO, Feeds Sản Phẩm, Kết Nối Xã Hội Blog, Cấu Hình POS |
| **Nội Dung** | Trang & Mẫu, Bài Viết Blog, Thông Báo, Biểu Mẫu, Bộ Sưu Tập Sản Phẩm |
| **Thương Mại** | Quy Tắc Thương Mại (Voucher, Khuyến Mãi, Trung Thành, Đăng Ký), Chương Trình Liên Kết, Webhook & Tích Hợp |

> **Lưu ý:** Các danh mục chứa thông tin xác thực (nhà cung cấp thanh toán, tài khoản giao hàng, v.v.) được đánh dấu bằng biểu tượng khóa. Các khóa API và bí mật được chuyển một cách an toàn nhưng có thể cần được nhập lại cho các tích hợp dựa trên OAuth.

## Hướng Dẫn Bước Bước

### Bước 1: Thiết Lập Kết Nối

1. Di chuyển đến **Di Chuyển Dữ Liệu > Đồng Bộ Spwig đến Spwig** trong thanh bên quản trị
2. Nhấp **Bắt Đầu Đồng Bộ Cài Đặt**
3. Chọn kết nối đã lưu hoặc tạo một kết nối mới:
   - Nhập URL cửa hàng từ xa (ví dụ: `https://staging.yourstore.com`)
   - Dán mã đồng bộ được tạo trên cửa hàng từ xa
   - Đặt tên cho kết nối một cách mô tả
   - Thiết lập vai trò (Staging, Production, Backup hoặc Other)
4. Nhấp **Kiểm Tra Kết Nối** để xác minh nó hoạt động
5. Nhấp **Tiếp Theo** để tiếp tục

### Bước 2: Chọn Danh Mục và Hướng Đồng Bộ

**Hướng:**
- **Kéo** -- Sao chép cài đặt từ cửa hàng đã kết nối đến cửa hàng này
- **Đẩy** -- Sao chép cài đặt từ cửa hàng này đến cửa hàng đã kết nối

**Chế Độ Đồng Bộ:**
- **Thêm & Cập Nhật** -- Thêm các mục mới và cập nhật các mục hiện có, nhưng không bao giờ xóa bất cứ thứ gì. Đây là tùy chọn an toàn nhất.
- **Sao Chép Chính Xác** -- Làm cho mục tiêu khớp hoàn toàn với nguồn, bao gồm việc xóa các mục tồn tại trên mục tiêu nhưng không tồn tại trên nguồn. Sử dụng cẩn thận.

Chọn các danh mục bạn muốn bao gồm, sau đó nhấp **Tiếp Theo**.

### Bước 3: Xem Trước Các Thay Đổi

Trước khi áp dụng bất kỳ thay đổi nào, bạn sẽ thấy một bản xem trước chi tiết hiển thị chính xác những gì sẽ được thêm, sửa đổi hoặc xóa cho mỗi danh mục. Hãy xem xét kỹ điều này.

Nếu bạn đang đẩy đến kết nối production, bạn sẽ cần xác nhận rằng bạn hiểu các thay đổi sẽ ảnh hưởng đến cửa hàng trực tuyến của bạn.

Nhấp **Bắt Đầu Đồng Bộ** khi đã sẵn sàng.

### Bước 4: Theo Dõi Tiến Trình

Việc đồng bộ chạy ở nền. Bạn có thể an toàn rời khỏi trang tiến trình - việc đồng bộ sẽ tiếp tục chạy.

Trang tiến trình hiển thị:
- Tỷ lệ hoàn thành tổng thể với thời gian còn lại ước tính
- Tiến trình theo danh mục với số lượng thành công/thất bại
- Nhật ký hoạt động trực tiếp bạn có thể mở rộng để xem đầu ra chi tiết

## Hoàn Nguyên

Sau khi đồng bộ hoàn tất, bạn có **24 giờ** để hoàn nguyên các thay đổi. Hoàn nguyên khôi phục trạng thái trước đó của tất cả các cài đặt bị ảnh hưởng.

Để hoàn nguyên:
1. Đi đến **Bảng Điều Khiển Đồng Bộ**
2. Tìm công việc đã hoàn thành
3. Nhấp **Hoàn Nguyên** và xác nhận

Sau 24 giờ, tùy chọn hoàn nguyên hết hạn và các thay đổi trở thành vĩnh viễn.

## Một Số Lưu Ý

Bảo tồn tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và thuật ngữ kỹ thuật.

- **Thử nghiệm trên môi trường staging trước**:

Luôn đồng bộ với môi trường staging trước để kiểm tra kết quả trước khi đẩy lên production

- **Sử dụng chế độ Add & Update**:

Đây là chế độ an toàn nhất vì nó không bao giờ xóa dữ liệu hiện có

- **Kiểm tra bản xem trước cẩn thận**:

Bản xem trước sự khác biệt sẽ hiển thị chính xác những gì sẽ thay đổi trước khi bất cứ thứ gì được áp dụng

- **Kết nối production hiển thị cảnh báo**:

Khi đẩy đến kết nối được đánh dấu là Production, cần xác nhận an toàn bổ sung