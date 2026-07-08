---
title: Hộp thư ra
---

Hộp thư ra là bản ghi đầy đủ của mọi email mà cửa hàng của bạn đã gửi hoặc cố gắng gửi — xác nhận đơn hàng, cập nhật vận chuyển, báo cáo quản trị, và tất cả các thông báo giao dịch khác. Sử dụng nó để xác nhận việc giao hàng, điều tra các lỗi và quản lý hàng đợi email.

Truy cập **Hệ thống Email > Hộp thư ra** để xem bản ghi email.

![Danh sách Hộp thư ra với nhãn trạng thái](/static/core/admin/img/help/email-outbox/outbox-list.webp)

## Đọc hộp thư ra

Thanh tổng quan ở trên hiển thị số lượng cho mỗi danh mục trạng thái. Danh sách bên dưới hiển thị các email cá nhân với:

- **Tiêu đề** — dòng tiêu đề của email
- **Đến** — địa chỉ email của người nhận
- **Từ** — địa chỉ người gửi được sử dụng
- **Trạng thái** — trạng thái giao hàng hiện tại
- **Được xếp hàng lúc** — thời điểm email được đưa vào hàng đợi
- **Gửi lúc** — thời điểm email được gửi đến nhà cung cấp
- **Số lần thử lại** — số lần gửi đã được thực hiện

## Trạng thái email

| Trạng thái | Ý nghĩa |
|------------|---------|
| Đang xếp hàng | Email đang chờ trong hàng đợi để gửi |
| Đang gửi | Email đang được gửi đến nhà cung cấp |
| Đã gửi | Nhà cung cấp đã chấp nhận email |
| Đang giữ | Email bị tạm dừng và sẽ không được gửi cho đến khi được giải phóng |
| Đã ghi lại | Email đã được ghi lại nhưng chưa được gửi (chế độ kiểm tra hoặc thiết lập chỉ ghi lại) |
| Thất bại | Nhà cung cấp đã từ chối hoặc không thể giao email |
| Bounced | Email đã được gửi nhưng bị phản hồi từ máy chủ email của người nhận |
| Bỏ qua | Việc gửi đã bị bỏ qua do lý do hệ thống |

## Xem chi tiết email

Nhấp vào bất kỳ email nào trong danh sách để xem đầy đủ chi tiết:

- Nội dung **HTML đầy đủ** và **Nội dung văn bản** của email
- **ID thông báo nhà cung cấp** — tham chiếu từ nhà cung cấp email của bạn (sử dụng khi liên hệ hỗ trợ nhà cung cấp)
- **Thông báo lỗi** — thông báo lỗi chính xác cho các email thất bại hoặc bị phản hồi
- **Số lần thử lại** và **Số lần thử lại tối đa** — số lần gửi đã được thực hiện
- Tất cả các thời điểm: tạo, xếp hàng, gửi và thất bại

## Lọc hộp thư ra

Sử dụng các bộ lọc bên phải để thu hẹp phạm vi xem:

- **Trạng thái** — hiển thị các email có trạng thái giao hàng cụ thể
- **Ngày** — lọc theo thời điểm email được tạo hoặc gửi
- **Loại mẫu** — chỉ hiển thị các email có loại thông báo cụ thể (ví dụ: chỉ xác nhận đơn hàng)

Ô tìm kiếm ở trên đầu sẽ tìm kiếm theo tiêu đề, địa chỉ người nhận, địa chỉ người gửi hoặc ID thông báo nhà cung cấp.

## Giải phóng email đang giữ

Các email có trạng thái **Đang giữ** bị tạm dừng — chúng sẽ không được gửi cho đến khi bạn giải phóng chúng. Một email có thể bị giữ nếu cửa hàng của bạn đang ở chế độ bảo trì khi nó được tạo, hoặc nếu một hành động quản trị đã đặt nó vào trạng thái giữ.

Để giải phóng các email đang giữ:
1. Chọn các email bạn muốn giải phóng (tích vào các hộp bên trái)
2. Chọn **Giải phóng email đang giữ để gửi** từ danh sách **Hành động**
3. Nhấp **Tiến hành**

Các email đã được giải phóng sẽ chuyển sang trạng thái **Đang xếp hàng** và sẽ được gửi trong chu kỳ xử lý hàng đợi tiếp theo.

## Email được lên lịch

Một số email được lên lịch để gửi vào một thời điểm trong tương lai — ví dụ, các báo cáo tổng hợp hàng tuần được lên lịch để gửi vào một ngày và giờ cụ thể. Truy cập **Hệ thống Email > Email được lên lịch** để xem các lần gửi được lên lịch sắp tới.

Danh sách email được lên lịch hiển thị:

- **Loại mẫu** — loại email được lên lịch
- **Email người nhận** — địa chỉ sẽ được gửi đến
- **Được lên lịch cho** — ngày và giờ dự kiến gửi
- **Trạng thái** — Chưa gửi (chưa gửi), Đã gửi, hoặc Thất bại

Các email được lên lịch được xử lý tự động khi thời gian lên lịch đến — không cần hành động thủ công.

## Khắc phục sự cố giao hàng thất bại

Nếu email hiển thị trạng thái **Thất bại**, nhấp vào để xem thông báo lỗi và thực hiện các bước sau:

### Nguyên nhân phổ biến và cách khắc phục

| Triệu chứng | Nguyên nhân có thể | Điều nên làm |
|---------|-------------|------------|
| "Xác thực thất bại" | Thông tin xác thực nhà cung cấp email không hợp lệ | Cập nhật thông tin xác thực trong **Hệ thống Email > Tài khoản Email** |
| "Kết nối bị từ chối" / "Hết thời gian" | Máy chủ email của bạn không thể truy cập được | Kiểm tra trang trạng thái của nhà cung cấp email; kiểm tra kết nối trong **Tài khoản Email** |
| "Người nhận không hợp lệ" | Địa chỉ email của khách hàng bị sai | Kiểm tra tài khoản khách hàng và sửa lại địa chỉ email |
| Email bị trả lại | Máy chủ email của người nhận đã từ chối email | Địa chỉ có thể không tồn tại hoặc hộp thư của họ đã đầy; không nên thử lại quá nhiều lần |
| Tỷ lệ thất bại cao đột ngột | Vấn đề nhà cung cấp hoặc thông tin xác thực đã hết hạn | Kiểm tra trạng thái nhà cung cấp; kiểm tra lại kết nối trong **Tài khoản Email** |

### Kiểm tra kết nối tài khoản email của bạn

Nếu nhiều email đang thất bại, hãy kiểm tra tài khoản email của bạn:

1. Di chuyển đến **Hệ thống Email > Tài khoản Email**
2. Tìm tài khoản đang hoạt động của bạn và kiểm tra trạng thái **Kết nối** của nó
3. Nếu kết nối hiển thị lỗi, hãy nhấp vào tài khoản và sử dụng tùy chọn **Kiểm tra Kết nối** để chẩn đoán vấn đề

### Hành vi thử lại

Spwig tự động thử lại các email thất bại lên đến giới hạn **Số lần thử tối đa**. Số lần thử hiển thị trên mỗi email cho bạn biết số lần đã thực hiện. Khi đạt đến giới hạn thử lại, email sẽ giữ ở trạng thái **Thất bại** và không có lần thử tự động nào nữa xảy ra.

## Email bị trả lại

Một email **bị trả lại** đã được gửi nhưng bị máy chủ email của người nhận trả lại. Có hai loại trả lại:

- **Trả lại cứng** — địa chỉ email không tồn tại hoặc miền không chấp nhận email. Không nên thử lại các trả lại cứng; địa chỉ là không hợp lệ
- **Trả lại mềm** — vấn đề tạm thời (hộp thư đầy, máy chủ tạm thời không khả dụng). Có thể thành công khi thử lại

Việc trả lại lặp lại đến cùng một địa chỉ có thể làm tổn hại đến danh tiếng gửi email của bạn với các nhà cung cấp email. Nếu bạn thấy các trả lại lặp lại đến cùng một địa chỉ khách hàng, hãy cập nhật hoặc xóa địa chỉ đó khỏi tài khoản khách hàng.

## Một số mẹo

- Kiểm tra hộp thư ra sau các sự kiện lớn như một đợt bán hàng nhanh hoặc ra mắt sản phẩm lớn để xác nhận tất cả các email xác nhận đơn hàng đã được gửi thành công
- Nếu khách hàng nói họ không nhận được email, hãy tìm kiếm hộp thư ra theo địa chỉ email của họ để xem liệu nó đã được gửi, thất bại hoặc bỏ qua
- Sự gia tăng đột ngột trong các lần thất bại thường chỉ ra vấn đề về thông tin xác thực hoặc tài khoản — kiểm tra **Tài khoản Email** ngay lập tức
- Trạng thái **Đang giữ** không phải là thất bại — nó chỉ có nghĩa là email đang chờ. Giải phóng các email đang giữ khi bạn sẵn sàng gửi chúng
- Sử dụng bộ lọc **Loại Mẫu** để nhanh chóng kiểm tra tất cả các email của một loại — ví dụ, kiểm tra xem tất cả các xác nhận đơn hàng trong 7 ngày qua có trạng thái **Đã gửi** hay không
- Bảng điều hướng phân cấp theo ngày / tháng / năm ở đầu danh sách rất hữu ích để xem hộp thư ra cho một khoảng thời gian cụ thể