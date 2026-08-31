---
title: Vệ sinh danh sách và các địa chỉ bị chặn
---

Mọi địa chỉ email bị trả về lỗi vĩnh viễn (hard-bounce), được đánh dấu là thư rác, hoặc liên tục không nhận được tin nhắn đều đặt phần còn lại của danh sách của bạn vào tình trạng rủi ro — các nhà cung cấp hộp thư đánh giá uy tín người gửi của bạn dựa trên mức độ sạch sẽ của việc gửi, và một danh sách "bẩn" có nghĩa là nhiều chiến dịch *hơn* sẽ rơi vào thư rác. Campaign Studio bảo vệ bạn khỏi điều này một cách tự động với **vệ sinh danh sách**: nó theo dõi các địa chỉ không thể giao và các địa chỉ khiếu nại, sau đó ngừng gửi email marketing cho chúng, mà không cần bạn phải thiết lập gì.

Điều này khác với việc hủy đăng ký. Một địa chỉ đã hủy đăng ký là địa chỉ đã rút lại sự đồng ý; một địa chỉ **bị chặn** (suppressed) là địa chỉ mà Spwig đã xác định là không an toàn hoặc không thể tiếp tục gửi thư, bất kể tình trạng đồng ý.

## Cách các địa chỉ bị chặn

Spwig tự động thêm một địa chỉ vào **Danh sách chặn** (Suppression list) khi:

| Kích hoạt | Ý nghĩa |
|---------|---------------|
| **Trả về lỗi vĩnh viễn** (Hard bounce) | Địa chỉ không tồn tại, hoặc tên miền từ chối nhận thư cho địa chỉ đó — không thể giao vĩnh viễn. |
| **Khiếu nại thư rác** | Người nhận đã đánh dấu email của bạn là thư rác hoặc thư không mong muốn. |
| **Trả về lỗi tạm thời lặp lại** (Repeated soft bounces) | Địa chỉ bị trả về lỗi tạm thời (hộp thư đầy, máy chủ tạm thời không khả dụng) 5 lần trong một cửa sổ 30 ngày liên tục. Một lần trả về lỗi tạm thời được coi là sự cố nhất thời và bị bỏ qua — chỉ một mô hình các lần thất bại lặp lại mới kích hoạt việc chặn. |
| **Chặn thủ công** | Bạn đã tự thêm địa chỉ đó. |

Một khi một địa chỉ bị chặn, Spwig sẽ ngừng gửi mọi **chiến dịch** (campaigns) hoặc email **hành trình** (journey) cho địa chỉ đó ngay lập tức — bạn không cần thực hiện bất kỳ hành động nào khác.

## Nguồn tín hiệu đến từ đâu

Spwig có thể biết về một lần trả về lỗi hoặc khiếu nại từ một số nơi khác nhau, được hiển thị dưới dạng **Nguồn** (Source) trên mỗi địa chỉ bị chặn:

- **Bị từ chối khi gửi** — máy chủ email của bạn đã từ chối địa chỉ ngay lập tức khi Spwig cố gắng gửi cho nó.
- **Webhook của nhà cung cấp** — nếu bạn đã kết nối một nhà cung cấp email (chẳng hạn như SendGrid, Amazon SES, Mailgun, hoặc Postmark), nhà cung cấp đó sẽ báo cáo các lần trả về lỗi và khiếu nại về Spwig khi chúng xảy ra.
- **Cổng thư** (Mail gateway) — nếu cửa hàng của bạn gửi thông qua cổng thư do Spwig lưu trữ, Spwig sẽ lấy báo cáo trả về lỗi từ cổng thay mặt cho bạn.
- **Thêm thủ công** — bạn đã tự nhập địa chỉ từ trang quản trị.

Bạn không cần phải cấu hình bất cứ điều gì để hưởng lợi từ điều này — bất kể bạn gửi email bằng cách nào, Spwig đều đang theo dõi các sự cố và giữ cho danh sách của bạn sạch sẽ.

## Bảng điều khiển Campaign Studio

Mở **Campaign Studio** và tìm thẻ **Địa chỉ bị chặn** (Suppressed addresses). Thẻ này hiển thị tổng số địa chỉ hiện đang bị chặn, cùng với số lượng địa chỉ mới trong 30 ngày qua. Nhấp vào thẻ để mở danh sách Chặn (Suppressions) đầy đủ.

![Thẻ thống kê Địa chỉ bị chặn trên bảng điều khiển Campaign Studio, hiển thị tổng số và số lượng "mới trong 30 ngày qua"](/static/core/admin/img/help/list-hygiene/dashboard-suppressed-card.webp)

Một số lượng tăng dần đều là bình thường — mọi danh sách đều tích lũy một số địa chỉ xấu theo thời gian khi mọi người thay đổi công việc, đóng tài khoản hoặc bỏ mặc hộp thư. Một sự tăng đột biến đáng để điều tra; xem [Hộp thư đi](email-outbox) để kiểm tra xem một lần gửi cụ thể có gặp phải số lượng sự cố bất thường hay không.

## Danh sách Chặn (Suppressions)

Nhấp vào **Chặn** (Suppressions) để xem mọi địa chỉ bị chặn, lý do bị chặn và nguồn tín hiệu đến từ đâu.

![Danh sách Chặn hiển thị các địa chỉ bị chặn với các cột Lý do và Nguồn](/static/core/admin/img/help/list-hygiene/suppressions-list.webp)

Sử dụng các bộ lọc bên phải để thu hẹp danh sách theo **Lý do** (Reason) hoặc **Nguồn** (Source) — ví dụ, để xem xét mọi địa chỉ bị chặn thủ công, hoặc mọi thứ đến thông qua webhook của nhà cung cấp.

## Thêm một địa chỉ thủ công

Để tự chặn một địa chỉ — một địa chỉ lạm dụng đã biết, một đối thủ đang cào dữ liệu bản tin của bạn, hoặc bất kỳ thứ gì bạn muốn giữ khỏi danh sách của mình — nhấp vào **+ Thêm địa chỉ bị chặn** và điền vào:

- **Email** — địa chỉ để chặn
- **Lý do** — chọn **Bị chặn thủ công** cho một mục được thêm tự động
- **Nguồn** — chọn **Được thêm thủ công"
- **Chi tiết** — ghi chú tùy chọn giải thích lý do (rất hữu ích cho ghi chép của bạn và cho bất kỳ nhân viên nào xem danh sách sau này)

Lưu mục này và Spwig sẽ dừng gửi email chiến dịch hoặc hành trình đến địa chỉ đó ngay lập tức.

## Khi nào bạn nên giải phóng một địa chỉ?

Việc giải phóng (bỏ chặn) một địa chỉ nên là điều hiếm và có chủ đích. Chỉ thực hiện khi bạn chắc chắn rằng vấn đề cơ bản đã được khắc phục — ví dụ:

- Một khách hàng nói với bạn rằng hộp thư của họ đầy và đã được dọn dẹp.
- Một địa chỉ đã bị chặn do chuỗi lỗi mềm mà bạn biết là do sự cố tạm thời tại nhà cung cấp dịch vụ email của họ, không phải do hộp thư bị hỏng.
- Bạn đã chặn địa chỉ thủ công và sau đó quyết định rằng việc chặn là sai lầm.

Để giải phóng một địa chỉ, mở nó trong danh sách chặn và xóa mục — điều này bỏ chặn địa chỉ để nó có thể nhận email lại. Không nên giải phóng một địa chỉ bị lỗi cứng chỉ vì việc mất người đăng ký là bất tiện; địa chỉ đó không tồn tại, và việc gửi lại sẽ chỉ bị lỗi và làm mất uy tín của bạn lần nữa. Tương tự, việc giải phóng một địa chỉ bị khiếu nại spam hiếm khi giúp gì — người nhận đã nói với nhà cung cấp hộp thư của họ rằng họ không muốn nhận email của bạn, và việc gửi lại có thể dẫn đến khiếu nại lần nữa.

## Điều gì không bị ảnh hưởng

Việc chặn chỉ áp dụng cho các **chiến dịch tiếp thị và hành trình** được gửi qua Studio Chiến dịch. Nó không ảnh hưởng đến **email giao dịch** — các email xác nhận đơn hàng, cập nhật vận chuyển, khôi phục mật khẩu, và các email khác mà cửa hàng của bạn gửi như một phần của hành động đơn hàng hoặc tài khoản luôn đi qua, ngay cả với địa chỉ đã bị chặn. Việc chặn tồn tại để bảo vệ uy tín người gửi tiếp thị của bạn; nó không phải là danh sách chặn email tổng quát cho cửa hàng của bạn.

## Mẹo

- Không nên chống hệ thống bằng cách giải phóng thủ công mọi lỗi cứng bạn thấy — lỗi cứng có nghĩa là địa chỉ đó không còn tồn tại, và việc thêm lại nó vào danh sách gửi sẽ chỉ bị lỗi lần nữa.
- Kiểm tra danh sách chặn sau một đợt gửi lớn nếu tỷ lệ mở email của bạn trông bất thường thấp — một làn sóng lỗi mềm trên cùng một miền (ví dụ: máy chủ email doanh nghiệp gặp sự cố) có thể là dấu hiệu của vấn đề giao hàng tạm thời đáng để điều tra với nhà cung cấp của bạn.
- Nếu bạn đang chuyển sang Spwig từ nền tảng khác, đừng nhập thủ công toàn bộ danh sách chặn cũ của bạn làm các mục chặn — hãy để Spwig học từ các lỗi và khiếu nại thực tế trên danh sách này thay vào đó, để bạn không vô tình chặn các địa chỉ sẽ giao hàng tốt.
- Xem lại cột **Nguồn** thỉnh thoảng — rất nhiều mục **Webhook nhà cung cấp** xác nhận rằng báo cáo lỗi email của nhà cung cấp của bạn đã được kết nối và hoạt động.
- Giữ trường **Chi tiết** có ý nghĩa khi thêm một mục chặn thủ công; đây là ghi chép duy nhất lý do tại sao quyết định đó được đưa ra một khi thời gian đã qua.