---
title: Quản lý các gói đăng ký của khách hàng
---

Phần đăng ký khách hàng cung cấp cái nhìn toàn diện về tất cả các gói đăng ký lặp lại đang hoạt động, tạm dừng và đã hủy trong cửa hàng của bạn. Từ đây, bạn có thể theo dõi tình trạng thanh toán, xem chi tiết từng gói đăng ký và thực hiện hành động khi có sự cố.

## Xem các gói đăng ký của khách hàng

Đi đến **Subscriptions > Customer Subscriptions** để xem danh sách đầy đủ các gói đăng ký của tất cả khách hàng.

![Danh sách các gói đăng ký của khách hàng](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

Danh sách hiển thị khách hàng, tên gói, trạng thái hiện tại, ngày thanh toán tiếp theo và số lượng chu kỳ thanh toán đã hoàn thành của mỗi gói đăng ký.

### Lọc và tìm kiếm

Sử dụng bảng lọc bên phải để thu hẹp các gói đăng ký theo:

- **Trạng thái** — Lọc theo Đang hoạt động, Thử nghiệm, Đến hạn, Tạm dừng, Hủy bỏ, hoặc Hết hạn
- **Gói** — Xem các gói đăng ký cho một gói cụ thể
- **Chế độ nhà cung cấp** — Bản địa (Stripe/PayPal quản lý) hoặc Phục vụ (hệ thống thanh toán nội bộ)

Sử dụng thanh tìm kiếm để tìm các gói đăng ký theo địa chỉ email khách hàng.

## Các trạng thái của gói đăng ký

Việc hiểu rõ từng trạng thái giúp bạn xác định được các gói đăng ký cần chú ý:

| Trạng thái | Ý nghĩa của nó |
|--------|---------------|
| **Thử nghiệm** | Khách hàng đang ở trong giai đoạn thử nghiệm miễn phí hoặc giá giảm |
| **Đang hoạt động** | Gói đăng ký khỏe mạnh — thanh toán đang cập nhật và quyền truy cập đang hoạt động |
| **Đến hạn** | Một lần thanh toán thất bại — hệ thống đang thử lại. Khách hàng vẫn giữ quyền truy cập trong giai đoạn chờ |
| **Tạm dừng** | Gói đăng ký bị tạm dừng — không có thanh toán, không có quyền truy cập |
| **Hủy bỏ** | Yêu cầu hủy đã được gửi. Khách hàng có thể vẫn còn quyền truy cập cho đến ngày kết thúc kỳ |
| **Hết hạn** | Gói đăng ký đã kết thúc hoàn toàn — giai đoạn thử nghiệm hết hạn, đạt số chu kỳ thanh toán tối đa, hoặc khoảng thời gian hủy đã qua |

Các gói đăng ký ở trạng thái **Đến hạn** cần được chú ý nhiều nhất — nếu việc thanh toán tiếp tục thất bại và khoảng thời gian chờ hết hạn, gói đăng ký sẽ bị tạm dừng.

## Xem chi tiết một gói đăng ký

Nhấp vào bất kỳ gói đăng ký nào để mở chế độ xem chi tiết. Điều này hiển thị:

### Kỳ thanh toán hiện tại

- **Ngày bắt đầu / kết thúc kỳ hiện tại** — Ngày của cửa sổ thanh toán đang hoạt động
- **Ngày thanh toán tiếp theo** — Ngày mà lần thanh toán tiếp theo sẽ được thực hiện
- **Ngày thanh toán gần đây** và **Trạng thái thanh toán gần đây** — Kết quả của lần thanh toán gần đây nhất
- **Số chu kỳ thanh toán** — Số lượng chu kỳ thanh toán thành công đã hoàn thành

### Thông tin gói đăng ký

- **Gói** và **Cấp độ giá** — Gói nào và tần suất thanh toán mà khách hàng đang sử dụng
- **Sản phẩm / Phiên bản** — Sản phẩm thư viện được liên kết với gói đăng ký này (nếu có)
- **Số lượng** — Số lượng ghế hoặc đơn vị (cho các gói dựa trên số lượng)
- **Mã thanh toán** — Phương thức thanh toán được lưu trữ đang được sử dụng cho thanh toán lặp lại

### Chi tiết giai đoạn thử nghiệm

Nếu gói đăng ký đang ở trong giai đoạn thử nghiệm, **Ngày kết thúc giai đoạn thử nghiệm** cho biết ngày khách hàng hết hạn giai đoạn thử nghiệm và bắt đầu thanh toán đầy đủ.

### Chi tiết hủy bỏ

Với các gói đăng ký đã hủy, bạn có thể xem:

- **Loại hủy bỏ** — Hủy ngay lập tức, vào cuối kỳ, hoặc được lên kế hoạch
- **Ngày hủy bỏ** — Ngày mà yêu cầu hủy đã được gửi
- **Lý do hủy bỏ** — Ghi chú về lý do khách hàng hủy (nếu được ghi nhận)
- **Ngày hết hạn để kích hoạt lại** — Ngày cuối cùng khách hàng có thể kích hoạt lại mà không cần đăng ký lại từ đầu

### Giai đoạn chờ và cam kết

- **Ngày kết thúc giai đoạn chờ** — Nếu một lần thanh toán thất bại, điều này cho thấy thời hạn trước khi truy cập bị tạm dừng
- **Ngày kết thúc cam kết tối thiểu** — Đối với các gói có cam kết tối thiểu, đây là ngày hủy bỏ sớm nhất

## Tạm dừng một gói đăng ký

Một gói đăng ký bị tạm dừng sẽ dừng thanh toán tạm thời đồng thời làm gián đoạn quyền truy cập. Điều này hữu ích cho các khách hàng muốn nghỉ ngơi mà không cần hủy bỏ hoàn toàn.

Để xem các gói đăng ký bị tạm dừng, lọc theo **Trạng thái: Tạm dừng**. Chế độ xem chi tiết hiển thị:

- **Ngày bắt đầu tạm dừng** — Ngày mà việc tạm dừng bắt đầu
- **Lý do tạm dừng** — Ghi chú về lý do gói đăng ký bị tạm dừng
- **Ngày tự động kích hoạt lại** — Nếu được đặt, đây là ngày gói đăng ký sẽ tự động kích hoạt lại thanh toán và quyền truy cập

Các gói đăng ký sẽ tiếp tục vào ngày tự động kích hoạt lại hoặc khi khách hàng kích hoạt lại thủ công.

## Nhật ký chu kỳ thanh toán

Mọi lần thanh toán — thành công hoặc thất bại — đều được ghi nhận trong nhật ký chu kỳ thanh toán. Truy cập **Cài đặt > Nhật ký chu kỳ thanh toán** để xem lịch sử này.

![Danh sách nhật ký chu kỳ thanh toán](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Đọc một mục nhật ký chu kỳ thanh toán

Mỗi mục nhật ký ghi nhận:

- **Gói đăng ký** — Gói đăng ký nào mà lần thanh toán này thuộc về
- **Số chu kỳ** — Chu kỳ thanh toán tuần tự (Chu kỳ 1 = lần thanh toán đầu tiên sau giai đoạn thử)
- **Ngày thanh toán** — Ngày đã thực hiện thanh toán
- **Trạng thái** — Đang chờ, Đang xử lý, Thành công, Thất bại, hoặc Đang thử lại
- **Phân tích số tiền**:
  - **Số tiền cơ bản** — Giá gói trước khi có bất kỳ điều chỉnh nào
  - **Số tiền cho số lượng** — Tiền thêm cho số lượng chỗ ngồi/đơn vị
  - **Số tiền phụ kiện** — Tổng chi phí của các phụ kiện đang hoạt động
  - **Số tiền giảm giá** — Tổng số tiền giảm giá đã áp dụng
  - **Số tiền tổng cộng** — Số tiền cuối cùng đã được tính (hoặc đã thử tính)
- **Phương thức thanh toán** — Thẻ hoặc phương thức thanh toán được sử dụng
- **Mã giao dịch của nhà cung cấp** — Số tham chiếu của nhà cung cấp thanh toán (rất hữu ích cho việc tra cứu hoàn tiền)
- **Lý do thất bại** — Nếu việc thanh toán thất bại, lý do thất bại là gì (ví dụ: thẻ bị từ chối, số dư tài khoản không đủ)

### Chẩn đoán các lỗi thanh toán

Nếu khách hàng liên hệ bạn về một vấn đề thanh toán, hãy tìm gói đăng ký của họ và kiểm tra nhật ký chu kỳ thanh toán. Trường **Lý do thất bại** giải thích điều gì đã sai. Các lý do thất bại phổ biến bao gồm:

- **Thẻ bị từ chối** — Thẻ của khách hàng bị ngân hàng từ chối
- **Số dư không đủ** — Số dư tài khoản quá thấp vào thời điểm thanh toán
- **Thẻ hết hạn** — Phương thức thanh toán đã lưu đã hết hạn
- **Lỗi mạng** — Một vấn đề kết nối tạm thời với nhà cung cấp thanh toán — thường được giải quyết khi thử lại

Đối với các lần thất bại liên tục, hãy hướng dẫn khách hàng cập nhật phương thức thanh toán trong phần cài đặt tài khoản của họ.

## Cách các lần gia hạn được thực hiện

Mỗi lần thanh toán gia hạn thành công tạo ra một đơn hàng được thanh toán mới cho chu kỳ thanh toán đó — không chỉ là một bản ghi thanh toán. Đơn hàng này đi qua quy trình giao hàng thông thường của bạn giống như một đơn hàng được đặt tại quầy thanh toán:

- **Sản phẩm vật lý** — Đơn hàng gia hạn được đưa vào hàng đợi giao hàng thông thường của bạn để chọn, đóng gói và giao hàng. Nó không được phân bổ tồn kho ngay lập tức khi thẻ được thanh toán, do đó một tình trạng thiếu tồn kho tạm thời không bao giờ làm gián đoạn một lần thanh toán đã thành công — bạn vẫn sẽ thấy đơn hàng và có thể giao hàng khi có tồn kho.
- **Sản phẩm kỹ thuật số** — Truy cập (liên kết tải xuống, khóa giấy phép) được cấp lại tự động ngay khi đơn hàng gia hạn được tạo, giống như cách nó sẽ được cho một lần mua hàng đầu tiên.

Đơn hàng gia hạn sao chép thông tin giao hàng và thanh toán từ đơn hàng đã bắt đầu gói đăng ký, do đó bạn không cần phải nhập lại bất kỳ thứ gì. Chúng không có nhãn đặc biệt nào trong danh sách **Đơn hàng** của bạn, nhưng bạn luôn có thể truy xuất một chu kỳ cụ thể trở lại đơn hàng của nó: mở **Cài đặt > Nhật ký chu kỳ thanh toán**, nhấp vào mục nhật ký cho chu kỳ đó, và trường **Đơn hàng** sẽ liên kết trực tiếp đến nó.

## Email vòng đời gói đăng ký

Spwig gửi các email vòng đời gói đăng ký tự động — bạn không cần phải kích hoạt chúng thủ công. Những email mà các chủ cửa hàng thường hỏi nhiều nhất:

| Email | Khi nào gửi | 
|-------|----------------| 
| **Nhắc nhở gia hạn** | Trước một lần gia hạn thanh toán tiếp theo | 
| **Hết hạn thử** | Trước khi giai đoạn thử miễn phí hoặc giảm giá chuyển sang thanh toán đầy đủ | 
| **Thất bại thanh toán** | Ngay sau khi lần thanh toán gia hạn thất bại, và một lần nữa như một thông báo cuối cùng nếu khoảng thời gian chờ sắp hết (dunning) | 
| **Xác nhận hủy bỏ** | Khi một gói đăng ký bị hủy | 

Spwig cũng gửi các email chào mừng, thành công thanh toán, tạm dừng/kích hoạt lại, hết hạn, kích hoạt lại, thay đổi gói, và hết hạn phương thức thanh toán tại các thời điểm phù hợp trong vòng đời của một gói đăng ký.

Tất cả những điều này là mẫu email thông thường — xem [Mẫu email](/help/email-templates) để xem lại hoặc tùy chỉnh nội dung của chúng và xác minh chúng đang hoạt động.

## Tự quản lý của khách hàng

Khách hàng không cần liên hệ với bạn để thay đổi đăng ký thông thường — họ có thể quản lý đăng ký của riêng họ từ tài khoản của họ: xem chi tiết và lịch sử thanh toán, tạm dừng, tiếp tục, hủy bỏ và cập nhật phương thức thanh toán đã lưu. Điều này bao gồm phần lớn những gì sẽ đến trong hàng đợi hỗ trợ của bạn, vì vậy khi khách hàng liên hệ về đăng ký của họ, hãy kiểm tra xem họ đã thử trang tài khoản của họ trước khi bạn thực hiện thay đổi cho họ trong admin.

## Mẹo

- Kiểm tra bộ lọc **Hết hạn** mỗi tuần để phát hiện các đăng ký có nguy cơ bị chấm dứt. Một email nhanh đến khách hàng thường giải quyết các vấn đề thanh toán trước khi khoảng thời gian miễn phí kết thúc.
- Các ghi chép chu kỳ thanh toán là đọc duy nhất — chúng được tạo tự động và không thể chỉnh sửa. Điều này đảm bảo một hồ sơ kiểm toán đáng tin cậy.
- Nếu đăng ký của khách hàng hiển thị **Hết hạn** nhưng họ đã cập nhật phương thức thanh toán, lần thử tự động tiếp theo sẽ bắt đầu với thẻ mới. Các lần thử lại tuân theo lịch trình khoảng thời gian miễn phí được cấu hình trong gói.
- Các đăng ký **Hết hạn** không bị xóa — chúng vẫn hiển thị để báo cáo. Sử dụng bộ lọc ngày để tập trung vào các đăng ký đang hoạt động.
- Đối với các đăng ký đang ở **Thử thách**, kiểm tra **Ngày kết thúc thử thách** để dự đoán các khoản thanh toán đầu tiên sắp tới và chủ động giải quyết bất kỳ vấn đề nào về phương thức thanh toán nào.
- Nếu khách hàng nói rằng một lần tái ký vật lý "chưa được giao", hãy kiểm tra hàng đợi giao hàng thông thường của bạn thay vì hồ sơ đăng ký — các đơn hàng tái ký được giao hàng theo cùng một cách như các đơn hàng khác và không vượt hàng đợi.