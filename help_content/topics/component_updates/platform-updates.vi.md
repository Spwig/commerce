---
title: Cập nhật nền tảng
---

Lắp đặt Spwig của bạn được xây dựng từ một tập hợp các thành phần — chủ đề, tiện ích, tích hợp, phần tử xây dựng trang và kết nối nhà cung cấp — mỗi thành phần có phiên bản riêng có thể được cập nhật độc lập. Bảng Đăng ký Thành phần cung cấp cho bạn cái nhìn tổng quan về mọi thứ đã cài đặt, hiển thị các thành phần nào có cập nhật đang chờ, và cho phép bạn cài đặt hoặc quay lại các bản cập nhật bất kỳ lúc nào.

![Tổng quan bảng Đăng ký Thành phần](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Hiểu về bảng Đăng ký Thành phần

Truy cập **Extensions > Component Registry** để xem tất cả các thành phần đã cài đặt trên cửa hàng của bạn. Mỗi hàng hiển thị:

- **Tên** — tên hiển thị của thành phần
- **Loại** — loại thành phần (chủ đề, tiện ích, tích hợp, v.v.)
- **Phiên bản hiện tại** — phiên bản đang chạy trên cửa hàng của bạn
- **Trạng thái cập nhật** — có bản cập nhật mới hay không
- **Kênh** — kênh cập nhật mà thành phần theo
- **Cập nhật tự động** — cập nhật được cài đặt tự động hay không
- **Khóa** — thành phần có bị khóa ở phiên bản hiện tại hay không

Bảng điều khiển ở đầu trang hiển thị các con số tổng quan: tổng số thành phần đã cài đặt, số lượng thành phần có bản cập nhật mới, và số lượng thành phần đã cập nhật đầy đủ.

### Loại thành phần

| Loại | Là gì |
|------|------------|
| Theme | Thiết kế trực quan của cửa hàng |
| Widget | Các khối xây dựng trang có thể tái sử dụng |
| Phần tử Xây dựng Trang | Các phần tử tùy chỉnh cho công cụ xây dựng trang |
| Công cụ Xây dựng Trang | Các công cụ và tiện ích cho trình chỉnh sửa |
| Mẫu Tiêu đề / Chân trang | Bố cục tiêu đề và chân trang |
| Nhà cung cấp Giao hàng | Tích hợp nhà vận chuyển (FedEx, UPS, v.v.) |
| Nhà cung cấp Email | Dịch vụ giao email |
| Nhà cung cấp Thanh toán | Tích hợp cổng thanh toán |
| Nhà cung cấp Tỷ giá Hối đoái | Nguồn dữ liệu tỷ giá hối đoái |
| Nhà cung cấp Dịch vụ Dịch thuật | Dịch vụ dịch thuật AI |
| Bộ ngôn ngữ | Các tệp dịch thuật giao diện |

## Kênh cập nhật

Mỗi thành phần theo một kênh cập nhật kiểm soát các bản phát hành mà nó nhận được. Bạn có thể gán mỗi thành phần vào kênh khác nhau dựa trên mức độ rủi ro bạn có thể chấp nhận.

| Kênh | Mô tả | Phù hợp nhất |
|---------|-------------|----------|
| **Stable** | Các bản phát hành đã được kiểm tra kỹ lưỡng, sẵn sàng cho sản xuất | Tất cả các thành phần trên cửa hàng đang hoạt động |
| **Beta** | Các bản xây dựng trước khi phát hành để kiểm tra tính năng mới trước khi ổn định | Các thành phần không quan trọng mà bạn muốn xem trước |
| **Development** | Các tính năng mới nhất, có thể không ổn định | Chỉ môi trường kiểm thử |
| **Security** | Chỉ các bản vá bảo mật quan trọng, được ưu tiên cao nhất | Các thành phần mà tính ổn định là tối quan trọng |

Để thay đổi kênh của một thành phần, hãy nhấp vào tên của nó để mở chế độ xem chi tiết, sau đó chọn giá trị mới trong trường **Kênh Cập nhật** và lưu lại.

## Kiểm tra cập nhật

Spwig kiểm tra cập nhật tự động theo khoảng thời gian được cấu hình trong cài đặt máy chủ cập nhật của bạn (mặc định: mỗi 24 giờ). Để kiểm tra ngay lập tức:

1. Truy cập **Extensions > Component Registry**
2. Nhấp vào nút **Check for Updates** ở đầu trang
3. Hệ thống sẽ liên hệ với máy chủ cập nhật Spwig và làm mới trạng thái cập nhật cho tất cả các thành phần
4. Các thành phần có bản cập nhật sẵn sàng sẽ được đánh dấu nổi bật, và con số **Updates Available** sẽ được cập nhật

Bạn cũng có thể kích hoạt kiểm tra cập nhật cho các thành phần riêng lẻ bằng hành động **Check for Updates** từ menu hành động của danh sách.

## Cài đặt cập nhật

### Cập nhật một thành phần

1. Truy cập **Extensions > Component Registry**
2. Tìm thành phần bạn muốn cập nhật — các thành phần có bản cập nhật sẵn sàng sẽ hiển thị chỉ báo cập nhật bên cạnh phiên bản của chúng
3. Nhấp vào nút **Install Update** trên hàng của thành phần đó
4. Xác nhận cập nhật khi được nhắc
5. Bản cập nhật sẽ tải xuống, kiểm tra và cài đặt — chỉ báo tiến trình sẽ hiển thị từng giai đoạn
6. Khi hoàn tất, số phiên bản hiện tại của thành phần sẽ được cập nhật thành số phiên bản mới

### Cập nhật nhiều thành phần

1.

Chọn các ô kiểm bên cạnh các thành phần bạn muốn cập nhật
2.

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và thuật ngữ kỹ thuật.

Chọn **Cài đặt bản cập nhật** từ danh sách thả xuống **Hành động**
3.

Nhấn **Tiến hành** để tiếp tục
4.

Các bản cập nhật được cài đặt theo thứ tự phụ thuộc — các thành phần mà các thành phần khác phụ thuộc vào sẽ được cập nhật trước

### Điều gì xảy ra trong quá trình cập nhật

Quy trình cập nhật thực hiện qua các giai đoạn sau:

1. **Kiểm tra** — xác nhận bản cập nhật có sẵn và giấy phép của bạn hợp lệ
2. **Tải xuống** — lấy gói từ máy chủ cập nhật Spwig
3. **Kiểm tra tính toàn vẹn** — kiểm tra tính toàn vẹn của gói dựa trên mã băm SHA-256
4. **Trích xuất** — giải nén các tệp mới
5. **Triển khai** — kích hoạt phiên bản mới
6. **Kiểm tra tình trạng** — xác nhận thành phần đang hoạt động sau khi cập nhật

Nếu bất kỳ giai đoạn nào thất bại, hệ thống sẽ tự động cố gắng khôi phục phiên bản trước đó.

## Cập nhật cấp nền tảng

Ngoài các thành phần riêng lẻ, Spwig có thể nhận được các bản cập nhật cấp nền tảng cập nhật động cơ cửa hàng cốt lõi. Các bản cập nhật này trải qua quy trình kỹ lưỡng hơn bao gồm di chuyển cơ sở dữ liệu và thời gian bảo trì ngắn.

Lịch sử cập nhật nền tảng có thể xem được trong phần **Cập nhật nền tảng** của sổ đăng ký. Mỗi mục hiển thị chuyển đổi phiên bản (ví dụ: `v1.3.2 → v1.3.3`), trạng thái và thời gian thực hiện quá trình cập nhật.

Các bản cập nhật bảo mật được đánh dấu riêng biệt và, nếu tùy chọn **Tự động cài đặt cập nhật bảo mật** được bật trong cấu hình máy chủ cập nhật của bạn, sẽ được cài đặt tự động mà không cần hành động thủ công.

## Xem lịch sử phiên bản

Để xem tất cả các phiên bản đã cài đặt trước đây của một thành phần:

1. Nhấn vào tên thành phần để mở chế độ xem chi tiết
2. Cuộn xuống phần **Phiên bản thành phần** ở cuối trang
3. Mỗi mục phiên bản hiển thị số phiên bản, thời gian cài đặt, phương pháp cài đặt và tình trạng sức khỏe

Hệ thống lưu trữ ba phiên bản đã cài đặt gần nhất để khôi phục. Các phiên bản vượt quá giới hạn này sẽ được xóa tự động.

## Khôi phục một thành phần

Nếu một bản cập nhật gây ra vấn đề, bạn có thể khôi phục về phiên bản trước:

1. Mở chế độ xem chi tiết của thành phần
2. Cuộn xuống phần **Khôi phục**
3. Chọn phiên bản bạn muốn khôi phục
4. Nhấn **Khôi phục về phiên bản này**

Chỉ các phiên bản được đánh dấu **Khôi phục khả dụng** mới có thể được khôi phục. Mỗi mục nhật ký khôi phục ghi lại người đã khởi động khôi phục và thời gian thực hiện.

## Khóa các thành phần

Khóa một thành phần sẽ ngăn bất kỳ bản cập nhật nào được cài đặt, bao cả những bản cập nhật tự động. Điều này hữu ích khi bạn có các tùy chỉnh hoặc tích hợp phụ thuộc vào phiên bản cụ thể.

1. Mở chế độ xem chi tiết của thành phần
2. Chọn ô **Đã khóa** trong phần **Khóa và đóng băng**
3. Nhập lý do trong **Lý do khóa** để nhóm của bạn hiểu lý do tại sao nó bị đóng băng
4. Lưu bản ghi

Các thành phần bị khóa được hiển thị với chỉ báo khóa trong danh sách sổ đăng ký. Để gỡ khóa, bỏ chọn **Đã khóa** và lưu.

## Đọc nhật ký cập nhật

Nhật ký cập nhật ghi lại mọi thao tác cài đặt, cập nhật, khôi phục và kiểm tra tình trạng:

1. Mở chế độ xem chi tiết của thành phần
2. **Nhật ký cập nhật** hiển thị trực tiếp ở cuối trang
3. Mỗi mục hiển thị: hành động được thực hiện, thời gian bắt đầu và kết thúc, phiên bản cũ và mới, liệu nó có tự động hay thủ công, và bất kỳ thông báo lỗi nào nếu thao tác thất bại

Các mục nhật ký có trạng thái **Thất bại** bao gồm toàn bộ thông báo lỗi để hỗ trợ chẩn đoán sự cố.

## Kích hoạt cập nhật tự động

Bạn có thể cho phép Spwig cài đặt các bản cập nhật tự động khi chúng trở nên có sẵn:

1. Mở chế độ xem chi tiết của thành phần
2. Chọn **Cập nhật tự động** trong phần **Phiên bản và trạng thái cập nhật**
3. Lưu bản ghi

Khi cập nhật tự động được bật, hệ thống sẽ cài đặt các bản cập nhật trong chu kỳ kiểm tra kế hoạch tiếp theo. Các bản cập nhật bảo mật tuân theo cài đặt toàn cầu **Tự động cài đặt cập nhật bảo mật** bất kể cài đặt thành phần riêng lẻ.

## Một số mẹo

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- Luôn cập nhật trên kênh **Stable** cho các chủ đề và nhà cung cấp thanh toán — đây là các thành phần trực diện với khách hàng nhất và tính ổn định là quan trọng nhất
- Khóa một thành phần trước khi thực hiện các thay đổi tùy chỉnh trên nó, và ghi rõ lý do để các thành viên trong nhóm sau biết không nên cập nhật nó
- Kiểm tra **Release Notes** trên mục ghi chú phiên bản của thành phần trước khi cài đặt một lần nâng cấp phiên bản chính — các thay đổi phá vỡ sẽ được đánh dấu tại đây
- Sau khi cập nhật, truy cập khu vực bị ảnh hưởng của cửa hàng của bạn để xác nhận mọi thứ trông và hoạt động như mong đợi trước khi tuyên bố cập nhật đã hoàn tất
- Nếu cập nhật tự động được bật trên một thành phần, theo dõi **Update Logs** định kỳ để đảm bảo các cập nhật tự động được hoàn thành thành công