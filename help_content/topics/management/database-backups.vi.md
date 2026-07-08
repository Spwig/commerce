---
title: Sao lưu CSDL
---

Các bản sa lưu định kỳ giúp bảo vệ dữ liệu cửa hàng của bạn — các đơn hàng, khách hàng, sản phẩm và cài đặt — khỏi sự cố phần cứng, xóa nhầm và các sự kiện bất ngờ khác. Hệ thống sa lưu của Spwig cho phép bạn tạo sa lưu theo yêu cầu, thiết lập lịch tự động, tải xuống sa lưu cục bộ, khôi phục từ bất kỳ bản sa lưu nào đã lưu, và sao chép sa lưu đến các đích lưu trữ từ xa như Amazon S3 hoặc Google Drive.

Truy cập **Quản lý > Chỉ số hệ thống** và sử dụng các liên kết thanh công cụ để truy cập các công cụ sa lưu.

![Bảng điều khiển hệ thống với các công cụ sa lưu](/static/core/admin/img/help/database-backups/system-dashboard.webp)

## Tạo sa lưu thủ công

Chạy sa lưu bất kỳ lúc nào trước khi thực hiện các thay đổi quan trọng — như nhập sản phẩm, cập nhật giao diện, hoặc nâng cấp nền tảng.

1. Truy cập **Quản lý > Chỉ số hệ thống**
2. Nhấp **Tạo sa lưu toàn bộ** từ thanh công cụ
3. Nhập một tên mô tả cho sa lưu (ví dụ: `before-july-import`)
4. Tùy chọn thêm **Mô tả** để nhắc nhở bản thân lý do tại sao bạn đã tạo sa lưu này
5. Chọn **Loại sa lưu**:
   - **Toàn bộ hệ thống** — sa lưu cơ sở dữ liệu và tất cả tệp phương tiện (khuyến nghị)
   - **Chỉ cơ sở dữ liệu** — sa lưu dữ liệu cửa hàng, không bao gồm hình ảnh và tệp đã tải lên
6. Chọn **Nén** (`gzip` là mặc định và hoạt động tốt cho hầu hết các cửa hàng)
7. Nhấp **Tạo sa lưu**

Spwig tạo sa lưu trong nền. Một chỉ báo tiến trình hiển thị giai đoạn hiện tại. Khi hoàn tất, sa lưu sẽ xuất hiện trong danh sách **Sao lưu CSDL** với trạng thái **Hoàn thành** và kích thước tệp của nó.

## Tải xuống sa lưu

Bạn có thể tải xuống bất kỳ sa lưu nào đã hoàn thành để lưu trữ bản sao cục bộ trên máy tính của bạn.

1. Truy cập **Quản lý > Sao lưu CSDL**
2. Tìm sa lưu bạn muốn tải xuống
3. Nhấp vào nút **Tải xuống** bên cạnh nó

Tệp sa lưu được tải xuống dưới dạng tệp nén. Lưu trữ nó ở một nơi an toàn — trên thiết bị riêng biệt hoặc lưu trữ đám mây — để bạn có bản sao độc lập với máy chủ của mình.

## Lên lịch sa lưu tự động

Các bản sa lưu tự động chạy trong nền mà không cần bất kỳ hành động nào từ bạn, vì vậy dữ liệu của bạn được bảo vệ ngay cả khi bạn quên tạo sa lưu thủ công.

1. Truy cập **Quản lý > Chỉ số hệ thống**
2. Nhấp **Lịch sa lưu**
3. Chọn **Kích hoạt sa lưu tự động**
4. Thiết lập **Tần suất**:
   - **Hàng ngày** — chạy một lần mỗi ngày vào thời gian bạn chỉ định
   - **Hàng tuần** — chạy một lần mỗi tuần vào ngày bạn chọn
   - **Hàng tháng** — chạy vào một ngày cụ thể trong tháng
5. Thiết lập **Thời gian** sa lưu nên chạy (thời gian máy chủ, thường là UTC — 03:00 sáng là thời điểm ít lưu lượng truy cập tốt)
6. Chọn **Loại sa lưu** (Toàn bộ hệ thống hoặc Chỉ cơ sở dữ liệu)
7. Thiết lập **Số ngày lưu trữ** — các sa lưu cũ hơn số ngày này sẽ bị xóa tự động (mặc định: 30 ngày)
8. Tùy chọn chọn **Mã hóa sa lưu** để mã hóa tệp sa lưu khi lưu trữ
9. Nếu bạn đã cấu hình các đích lưu trữ từ xa, hãy chọn chúng dưới **Đích lưu trữ từ xa** để tải lên tự động các sa lưu đã lên lịch
10. Nhấp **Lưu lịch**

Thời điểm **Lần chạy tiếp theo** được cập nhật ngay lập tức và hiển thị thời điểm lần sa lưu tự động tiếp theo sẽ diễn ra.

## Khôi phục từ sa lưu

Khôi phục thay thế dữ liệu cửa hàng hiện tại bằng nội dung của sa lưu. Sử dụng để phục hồi từ mất dữ liệu hoặc hủy bỏ các thay đổi không mong muốn.

> **Lưu ý quan trọng:** Khôi phục sẽ thay thế tất cả dữ liệu hiện tại bằng dữ liệu từ sa lưu. Cửa hàng của bạn sẽ được đặt ở chế độ bảo trì trong quá trình khôi phục. Thông báo cho nhóm của bạn trước khi thực hiện khôi phục.

1. Truy cập **Quản lý > Chỉ số hệ thống**
2. Nhấp **Khôi phục** từ thanh công cụ
3. Danh sách khôi phục hiển thị tất cả các sa lưu khả dụng với ngày và kích thước của chúng
4. Nhấp **Khôi phục** bên cạnh sa lưu bạn muốn sử dụng
5. Xem màn hình xác nhận — nó liệt kê chính xác những gì sẽ được thay thế
6. Nhập cụm từ xác nhận nếu được yêu cầu, sau đó nhấp **Thực thi khôi phục**

Spwig hiển thị thanh tiến trình khi khôi phục thực hiện qua các giai đoạn của nó (sao lưu trạng thái hiện tại, tải xuống sa lưu nếu từ xa, khôi phục cơ sở dữ liệu, khôi phục tệp phương tiện). Khi hoàn tất, cửa hàng tự động thoát khỏi chế độ bảo trì.

## Thiết lập lưu trữ từ xa

Lưu trữ từ xa tự động sao chép các bản sao lưu của bạn đến một vị trí bên ngoài — Amazon S3, Google Drive, Dropbox, hoặc một máy chủ SFTP. Điều này bảo vệ bạn khỏi sự cố ở cấp độ máy chủ.

1. Di chuyển đến **Quản lý > Chỉ số hệ thống**
2. Nhấp **Lưu trữ từ xa**
3. Nhấp **Thêm vị trí**
4. Trình hướng dẫn thiết lập sẽ hướng dẫn bạn qua ba bước:
   - **Bước 1**: Chọn loại lưu trữ của bạn (S3, Google Drive, Dropbox, hoặc SFTP)
   - **Bước 2**: Nhập thông tin xác thực cho nhà cung cấp đã chọn (xem chi tiết bên dưới)
   - **Bước 3**: Đặt tên cho vị trí và kiểm tra kết nối
5. Sau khi kiểm tra kết nối thành công, nhấp **Lưu**

### Amazon S3 (và dịch vụ S3 tương thích)

Bạn sẽ cần:
- **Access Key ID** và **Secret Access Key** từ người dùng IAM AWS của bạn
- **Tên bucket** — bucket S3 để tải lên các bản sao lưu
- **Khu vực** — khu vực AWS mà bucket nằm ở đó (ví dụ: `us-east-1`)
- Tùy chọn một **Prefix** (đường dẫn thư mục bên trong bucket, ví dụ: `spwig-backups/`)

Các dịch vụ S3 tương thích (Backblaze B2, Wasabi, MinIO, v.v.) hoạt động theo cùng cách — nhập URL điểm cuối tùy chỉnh khi được yêu cầu.

### Google Drive

Nhấp **Kết nối với Google** trên bước thông tin xác thực. Spwig mở một cửa sổ OAuth Google — đăng nhập và cấp quyền để tải lên tệp. Không cần sao chép thông tin xác thực thủ công.

### Dropbox

Nhấp **Kết nối với Dropbox** trên bước thông tin xác thực. Đăng nhập vào Dropbox và phê duyệt quyền truy cập. Các bản sao lưu được tải lên vào thư mục `Apps/Spwig` trong Dropbox của bạn.

### SFTP

Bạn sẽ cần:
- **Hostname** của máy chủ SFTP
- **Cổng** (mặc định: 22)
- **Tên người dùng** và **Mật khẩu** (hoặc khóa SSH riêng tư)
- **Đường dẫn từ xa** — thư mục trên máy chủ để tải lên các bản sao lưu

### Thiết lập vị trí mặc định

Trên trang **Lưu trữ từ xa**, nhấp vào nút bật/tắt bên cạnh bất kỳ vị trí nào để thiết lập nó làm **mặc định**. Vị trí mặc định sẽ tự động nhận tất cả các bản sao lưu — thủ công và đã lên lịch — mà không cần chọn nó mỗi lần.

## Mẹo

- Thực hiện bản sao lưu thủ công trước mỗi thay đổi quan trọng: nhập sản phẩm, chỉnh sửa giao diện, nâng cấp nền tảng, hoặc chiến dịch giảm giá
- Lên lịch sao lưu hàng ngày vào thời gian ít lưu lượng (ví dụ: 03:00 sáng) để giảm thiểu bất kỳ tác động hiệu suất nào
- Thiết lập ít nhất một vị trí lưu trữ từ xa để đảm bảo các bản sao lưu vẫn tồn tại ngay cả khi máy chủ gặp sự cố
- Cài đặt **Retention Days** kiểm soát thời gian lưu trữ bản sao lưu cục bộ — 30 ngày là giá trị mặc định hợp lý cho hầu hết các cửa hàng, nhưng hãy tăng nó nếu không gian lưu trữ cho phép
- Sau khi khôi phục, kiểm tra một vài đơn hàng và sản phẩm để xác nhận dữ liệu trông đúng trước khi tắt chế độ bảo trì của cửa hàng thủ công
- Các bản sao lưu được mã hóa thêm một lớp bảo mật nhưng yêu cầu khóa giải mã để khôi phục — không được mất nó