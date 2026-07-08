---
title: Quản lý đăng ký khách hàng
---

Phần đăng ký khách hàng cho phép bạn có cái nhìn toàn diện về tất cả các đăng ký định kỳ đang hoạt động, tạm dừng và đã hủy trong cửa hàng của bạn. Từ đây bạn có thể theo dõi tình trạng thanh toán, xem chi tiết từng đăng ký và thực hiện hành động khi có sự cố xảy ra.

## Xem đăng ký khách hàng

Truy cập **Đăng ký > Đăng ký khách hàng** để xem danh sách đầy đủ các đăng ký của tất cả khách hàng.

![Danh sách đăng ký khách hàng](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

Danh sách hiển thị khách hàng, tên gói, trạng thái hiện tại, ngày thanh toán tiếp theo và số lượng chu kỳ thanh toán đã hoàn thành của mỗi đăng ký.

### Lọc và tìm kiếm

Sử dụng bảng điều khiển lọc bên phải để thu hẹp đăng ký theo:

- **Trạng thái** — Lọc theo Hoạt động, Thử nghiệm, Quá hạn, Tạm dừng, Đã hủy hoặc Hết hạn
- **Gói** — Xem các đăng ký cho gói cụ thể
- **Chế độ nhà cung cấp** — Nguyên bản (Stripe/PayPal quản lý) hoặc Chế độ dự phòng (thanh toán nội bộ)

Sử dụng thanh tìm kiếm để tìm đăng ký theo địa chỉ email của khách hàng.

## Trạng thái đăng ký

Hiểu rõ từng trạng thái giúp bạn xác định các đăng ký cần được chú ý:

| Trạng thái | Ý nghĩa của nó |
|------------|----------------|
| **Thử nghiệm** | Khách hàng đang trong giai đoạn thử nghiệm miễn phí hoặc giá thấp hơn |
| **Hoạt động** | Đăng ký khỏe mạnh — thanh toán đúng hạn và quyền truy cập đang hoạt động |
| **Quá hạn** | Một lần thanh toán thất bại — hệ thống đang thử lại. Khách hàng vẫn giữ quyền truy cập trong giai đoạn ân hạn |
| **Tạm dừng** | Đăng ký tạm dừng tạm thời — không thanh toán, không quyền truy cập |
| **Đã hủy** | Yêu cầu hủy đã được thực hiện. Khách hàng có thể vẫn còn quyền truy cập cho đến ngày kết thúc chu kỳ |
| **Hết hạn** | Đăng ký đã kết thúc hoàn toàn — giai đoạn thử nghiệm đã hết, đạt số chu kỳ thanh toán tối đa hoặc thời gian hủy đã trôi qua |

Các đăng ký **Quá hạn** cần được chú ý nhất — nếu thanh toán tiếp tục thất bại và giai đoạn ân hạn kết thúc, đăng ký sẽ bị tạm dừng.

## Xem chi tiết đăng ký

Click vào bất kỳ đăng ký nào để mở chế độ xem chi tiết. Điều này hiển thị:

### Giai đoạn thanh toán hiện tại

- **Bắt đầu / Kết thúc giai đoạn hiện tại** — Ngày bắt đầu và kết thúc của cửa sổ thanh toán đang hoạt động
- **Ngày thanh toán tiếp theo** — Ngày mà lần thanh toán tiếp theo sẽ được thực hiện
- **Ngày thanh toán lần trước và Trạng thái thanh toán lần trước** — Kết quả của lần thanh toán gần nhất
- **Số chu kỳ thanh toán** — Số lượng chu kỳ thanh toán thành công đã hoàn tất

### Thông tin đăng ký

- **Gói và Cấp bậc giá** — Gói và tần suất thanh toán mà khách hàng đang sử dụng
- **Sản phẩm / Biến thể** — Sản phẩm trong danh mục liên kết với đăng ký này (nếu có)
- **Số lượng** — Số lượng chỗ ngồi hoặc đơn vị (đối với các gói dựa trên số lượng)
- **Mã thanh toán** — Phương thức thanh toán được lưu trữ đang được sử dụng cho thanh toán định kỳ

### Chi tiết thử nghiệm

Nếu đăng ký đang trong giai đoạn thử nghiệm, **Ngày kết thúc thử nghiệm** sẽ hiển thị thời điểm thử nghiệm của khách hàng kết thúc và thanh toán đầy đủ bắt đầu.

### Chi tiết hủy bỏ

Đối với các đăng ký đã hủy, bạn có thể xem:

- **Loại hủy bỏ** — Liệu hủy bỏ có được thực hiện ngay lập tức, tại cuối chu kỳ hoặc được lên lịch
- **Đã hủy vào** — Thời điểm hủy bỏ được yêu cầu
- **Lý do hủy bỏ** — Ghi chú về lý do khách hàng hủy bỏ (nếu có ghi lại)
- **Ngày hết hạn khôi phục** — Ngày cuối cùng khách hàng có thể khôi phục mà không cần đăng ký lại từ đầu

### Giai đoạn ân hạn và cam kết

- **Ngày kết thúc giai đoạn ân hạn** — Nếu thanh toán thất bại, đây là thời hạn cuối cùng trước khi quyền truy cập bị tạm dừng
- **Ngày kết thúc cam kết tối thiểu** — Đối với các gói có cam kết tối thiểu, ngày sớm nhất để hủy bỏ

## Tạm dừng đăng ký

Một đăng ký được tạm dừng sẽ dừng thanh toán tạm thời đồng thời cũng tạm dừng quyền truy cập. Điều này hữu ích cho các khách hàng muốn nghỉ ngơi mà không hủy bỏ hoàn toàn.

Để xem các đăng ký được tạm dừng, hãy lọc theo **Trạng thái: Tạm dừng**. Chế độ xem chi tiết hiển thị:

- **Đã tạm dừng vào** — Thời điểm tạm dừng bắt đầu
- **Lý do tạm dừng** — Ghi chú về lý do tạm dừng
- **Ngày khôi phục tự động** — Nếu được thiết lập, ngày đăng ký sẽ tự động tiếp tục thanh toán và quyền truy cập

Các đăng ký sẽ tiếp tục vào ngày tự động khôi phục hoặc khi khách hàng kích hoạt lại thủ công.

## Nhật ký chu kỳ thanh toán

Mọi nỗ lực thanh toán — thành công hoặc thất bại — đều được ghi lại trong nhật ký chu kỳ thanh toán. Truy cập **Subscriptions > Billing Cycle Logs** để xem lịch sử này.

![Billing cycle log list](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Đọc một mục nhật ký chu kỳ thanh toán

Mỗi mục nhật ký ghi lại:

- **Subscription** — Đăng ký khách hàng nào mục thanh toán này thuộc về
- **Cycle Number** — Chu kỳ thanh toán tuần tự (Cycle 1 = lần thanh toán đầu tiên sau giai đoạn dùng thử)
- **Billing Date** — Thời điểm thanh toán được thực hiện
- **Status** — Chờ xử lý, Đang xử lý, Thành công, Thất bại, hoặc Thử lại
- **Amount breakdown**:
  - **Base Amount** — Giá gói trước khi áp dụng bất kỳ điều chỉnh nào
  - **Quantity Amount** — Chi phí bổ sung cho số lượng chỗ/đơn vị
  - **Add-ons Amount** — Tổng chi phí của các tính năng bổ sung đang hoạt động
  - **Discount Amount** — Tổng số tiền giảm giá được áp dụng
  - **Total Amount** — Số tiền cuối cùng được tính (hoặc được cố gắng tính)
- **Payment Method** — Thẻ hoặc phương thức thanh toán được sử dụng
- **Provider Transaction ID** — Số tham chiếu của nhà cung cấp thanh toán (hữu ích để tra cứu hoàn tiền)
- **Failure Reason** — Nếu thanh toán thất bại, lý do tại sao thanh toán thất bại (ví dụ: thẻ bị từ chối, tài khoản thiếu số dư)

### Chẩn đoán lỗi thanh toán

Nếu khách hàng liên hệ với bạn về vấn đề thanh toán, hãy tìm đăng ký của họ và kiểm tra nhật ký chu kỳ thanh toán. Trường **Failure Reason** sẽ giải thích điều gì đã xảy ra. Các lý do thất bại phổ biến bao gồm:

- **Card declined** — Thẻ khách hàng bị ngân hàng từ chối
- **Insufficient funds** — Số dư tài khoản quá thấp vào thời điểm thanh toán
- **Card expired** — Phương thức thanh toán được lưu trữ đã hết hạn
- **Network error** — Một vấn đề kết nối tạm thời với nhà cung cấp thanh toán — thường được khắc phục khi thử lại

Đối với các lỗi liên tục, hướng dẫn khách hàng cập nhật phương thức thanh toán của họ trong cài đặt tài khoản.

## Mẹo

- Kiểm tra bộ lọc **Past Due** hàng tuần để phát hiện các đăng ký có nguy cơ churning. Một email nhanh chóng cho khách hàng thường giải quyết các vấn đề thanh toán trước khi thời gian ân hạn kết thúc.
- Nhật ký chu kỳ thanh toán chỉ đọc — chúng được tạo tự động và không thể chỉnh sửa. Điều này đảm bảo một hồ sơ kiểm toán đáng tin cậy.
- Nếu đăng ký của khách hàng hiển thị **Past Due** nhưng họ đã cập nhật phương thức thanh toán, lần thử lại tự động tiếp theo sẽ sử dụng thẻ mới. Các lần thử lại tuân theo lịch trình thời gian ân hạn được cấu hình trong gói.
- Các đăng ký **Expired** không bị xóa — chúng vẫn hiển thị để báo cáo. Sử dụng bộ lọc theo ngày để tập trung vào các đăng ký đang hoạt động hiện tại.
- Đối với các đăng ký trong **Trial**, kiểm tra **Trial End Date** để dự đoán các lần thanh toán đầu tiên sắp tới và chủ động giải quyết bất kỳ vấn đề phương thức thanh toán nào.