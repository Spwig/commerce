---
title: Di Chuyển Hệ Thống Toàn Phần
---

Di chuyển hệ thống toàn phần chuyển toàn bộ cửa hàng của bạn - cài đặt, sản phẩm, khách hàng, đơn hàng, tệp phương tiện và tất cả dữ liệu khác - từ một cài đặt Spwig này sang cài đặt Spwig khác. Sử dụng tính năng này khi di chuyển đến máy chủ mới hoặc thiết lập bản sao đầy đủ của cửa hàng bạn.

## Khi Nên Sử Dụng Di Chuyển Toàn Phần

- **Di chuyển máy chủ**: Di chuyển cửa hàng của bạn đến nhà cung cấp lưu trữ hoặc máy chủ mới
- **Tạo bản sao môi trường staging**: Thiết lập môi trường staging đầy đủ từ môi trường sản xuất
- **Phục hồi thảm họa**: Khôi phục toàn bộ cửa hàng từ một bản sao dự phòng

Di chuyển toàn phần bao gồm tất cả những gì mà đồng bộ cài đặt thực hiện, cộng thêm tất cả dữ liệu giao dịch (sản phẩm, khách hàng, đơn hàng, đánh giá, tồn kho, phương tiện, v.v.).

## Những Nội Dung Được Di Chuyển

Di chuyển toàn phần có thể chuyển tất cả các danh mục cài đặt cùng với các danh mục dữ liệu sau:

| Danh Mục | Mô Tả |
|----------|-------------|
| **Các Thành Phần Đã Cài Đặt** | Chủ đề, tích hợp nhà cung cấp và các thành phần tiện ích cùng với các tệp gói của chúng |
| **Sản Phẩm, Danh Mục & Thương Hiệu** | Sản phẩm, biến thể, hình ảnh, danh mục, thương hiệu và thuộc tính |
| **Thư Viện Phương Tiện** | Tất cả các tệp phương tiện và tài sản đã tải lên |
| **Khách Hàng & Địa Chỉ** | Tài khoản khách hàng, hồ sơ và địa chỉ |
| **Lịch Sử Đơn Hàng** | Đơn hàng, mục đơn hàng và bản ghi giao dịch |
| **Đánh Giá Sản Phẩm** | Đánh giá và xếp hạng của khách hàng |
| **Mức Tồn Kho** | Số lượng tồn kho theo kho và điểm đặt lại |
| **Sản Phẩm Số & Mẫu Licenses** | Tài sản số, mẫu license và nhóm license |
| **Thẻ Tặng & Sử Dụng Voucher** | Số dư thẻ quà tặng và bản ghi sử dụng voucher |
| **Tín Dụng Cửa Hàng & Ví** | Số dư ví khách hàng và lịch sử giao dịch |
| **Thành Viên Chương Trình Thẻ Tín Dụng** | Thành viên chương trình, điểm, giao dịch và biểu tượng |
| **Ký Hợp Đồng Hoạt Động** | Kế hoạch đăng ký, các hợp đồng đang hoạt động và lịch sử thanh toán |
| **Giao Hàng & Theo Dõi** | Bản ghi giao hàng và các sự kiện theo dõi |
| **Hoàn Tiền, Trả Lại & Ghi Chú Đơn Hàng** | Bản ghi hoàn tiền, yêu cầu trả lại và ghi chú |
| **Thành Viên Liên Kết** | Tài khoản liên kết, mã giới thiệu và lịch sử hoa hồng |

## Hướng Dẫn Bước Bước

### Bước 1: Kết Nối Đến Trạng Thái Nguồn

1. Di chuyển đến **Data Migration > Spwig-to-Spwig Sync** trong thanh bên quản trị
2. Nhấp **Start Full Migration**
3. Kết nối đến cửa hàng nguồn (cửa hàng bạn đang di chuyển **từ**):
   - Nhập URL cửa hàng nguồn
   - Dán mã token đồng bộ từ cửa hàng nguồn
   - Đặt tên cho kết nối (ví dụ: "Old Production Server")
4. Nhấp **Test Connection** để kiểm tra
5. Nhấp **Next**

> **Lưu ý:** Di chuyển toàn phần luôn **kéo** dữ liệu từ cửa hàng đã kết nối vào cửa hàng này. Chạy hướng dẫn trên **mục tiêu** (cửa hàng mới).

### Bước 2: Chọn Phạm Vi

Chọn các danh mục dữ liệu cần bao gồm trong quá trình di chuyển. Các danh mục được tổ chức thành các nhóm:

- **Cài đặt**: Cấu hình cửa hàng, chủ đề, nhà cung cấp, nội dung
- **Dữ liệu**: Sản phẩm, khách hàng, đơn hàng, phương tiện và các dữ liệu giao dịch khác

Một số danh mục có phụ thuộc (ví dụ: Đơn hàng phụ thuộc vào Khách hàng và Sản phẩm). Các phụ thuộc sẽ được tự động bao gồm khi bạn chọn một danh mục.

Các danh mục có biểu tượng đặc biệt:
- **Biểu tượng khóa**: Chứa thông tin xác thực được chuyển một cách an toàn
- **Biểu tượng tệp**: Bao gồm các tệp nhị phân (hình ảnh, phương tiện, gói)
- **Biểu tượng cảnh báo**: Có các lưu ý đặc biệt cho môi trường sản xuất

### Bước 3: Kiểm Tra Trước Di Chuyển

Trước khi bắt đầu di chuyển, các kiểm tra tự động trước di chuyển sẽ xác minh:

- **Tình trạng kết nối**: Cửa hàng nguồn có thể truy cập và xác thực được
- **Tương thích phiên bản**: Cả hai cửa hàng đều chạy các phiên bản Spwig tương thích
- **Không gian đĩa**: Có đủ không gian lưu trữ cho các tệp phương tiện
- **Sẵn sàng cơ sở dữ liệu**: Cơ sở dữ liệu đích có thể nhận dữ liệu

Nếu bất kỳ kiểm tra nào thất bại, bạn sẽ thấy hướng dẫn cụ thể về cách khắc phục vấn đề trước khi tiếp tục.

### Bước 4: Tiến Độ Di Chuyển

Quá trình di chuyển chạy ở nền. Bạn có thể an toàn rời khỏi trang - quy trình sẽ tiếp tục.

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

Trang tiến độ hiển thị:
- Tỷ lệ phần trăm tổng thể cùng với thời gian còn lại ước tính
- Tình trạng hoàn thành theo từng danh mục
- Nhật ký hoạt động trực tiếp với chi tiết chuyển đổi
- Thống kê chuyển đổi phương tiện (tệp và byte đã chuyển) cho danh mục phương tiện

Đối với các cửa hàng lớn với nhiều sản phẩm và tệp phương tiện, quá trình di chuyển có thể mất một thời gian. Giai đoạn chuyển phương tiện thường là giai đoạn dài nhất.

### Bước 5: Kết quả

Sau khi quá trình di chuyển hoàn tất, trang kết quả sẽ hiển thị:

- Thống kê tổng quan (số mục đã di chuyển, bỏ qua, thất bại)
- Phân tích theo danh mục cùng với trạng thái
- Chi tiết lỗi cho các mục thất bại

## Danh sách kiểm tra sau di chuyển

Sau khi di chuyển thành công, hãy thực hiện các bước sau trên cửa hàng mới của bạn:

1. **Kích hoạt giấy phép** trên cài đặt mới
2. **Nhập lại thông tin xác thực nhà cung cấp thanh toán** đã bị bỏ qua trong quá trình di chuyển (khóa kiểm thử/sandbox không được chuyển sang môi trường sản xuất)
3. **Cấu hình DNS** để hướng tên miền của bạn đến máy chủ mới
4. **Kiểm tra quy trình thanh toán** với một đơn hàng kiểm tra
5. **Xác nhận việc gửi email** hoạt động đúng
6. **Kiểm tra tệp phương tiện** và hình ảnh có tải lên đúng không

## Quay lại

Sau khi hoàn tất Di chuyển Toàn bộ, bạn có **24 giờ** để quay lại. Thao tác quay lại sẽ xóa tất cả dữ liệu đã di chuyển khỏi cửa hàng đích, khôi phục lại trạng thái trước khi di chuyển.

Để quay lại:
1. Truy cập trang kết quả hoặc bảng điều khiển Đồng bộ
2. Nhấp vào **Quay lại Di chuyển** và xác nhận
3. Chờ cho quá trình quay lại hoàn tất

> **Cảnh báo:** Thao tác quay lại sẽ xóa vĩnh viễn tất cả dữ liệu đã di chuyển. Mọi thay đổi được thực hiện trên cửa hàng đích sau khi di chuyển (đơn hàng mới, đăng ký khách hàng, v.v.) cũng sẽ bị ảnh hưởng.

Sau 24 giờ, tùy chọn quay lại sẽ hết hạn.

## Một số lưu ý

- **Thực hiện trên cửa hàng đích**: Trình hướng dẫn Di chuyển Toàn bộ nên được chạy trên **cửa hàng mới**, trích xuất dữ liệu từ cửa hàng cũ
- **Di chuyển sang cài đặt sạch**: Để đạt kết quả tốt nhất, hãy chạy quá trình di chuyển trên một cài đặt Spwig mới trước khi đưa vào vận hành
- **Kiểm tra không gian đĩa**: Đảm bảo cửa hàng đích có đủ không gian lưu trữ cho tất cả tệp phương tiện
- **Giữ nguyên cửa hàng nguồn hoạt động**: Đừng tắt cửa hàng nguồn cho đến khi bạn đã xác nhận mọi thứ hoạt động đúng trên cửa hàng đích
- **Lên kế hoạch chuyển đổi DNS**: Sau khi xác nhận quá trình di chuyển, hãy cập nhật bản ghi DNS của bạn để hướng đến máy chủ mới