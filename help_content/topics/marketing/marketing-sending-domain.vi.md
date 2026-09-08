---
title: Mạng gửi email tiếp thị
---

# Mạng gửi email tiếp thị

Cửa hàng của bạn gửi hai loại email rất khác nhau:

- **Giao dịch** — xác nhận đơn hàng, cập nhật vận chuyển, khôi phục mật khẩu. Những email này
  phải luôn đến hộp thư đến.
- **Tiếp thị** — bản tin, ưu đãi, khôi phục giỏ hàng, thông báo hàng về lại kho.

Mặc định cả hai đều được gửi từ cùng một danh tính gửi, điều này có nghĩa là chúng **cùng chia sẻ một uy tín người gửi**. Nếu một chiến dịch tiếp thị bị khiếu nại là thư rác hoặc gặp phải các địa chỉ lỗi thời, uy tín này sẽ giảm xuống — và các xác nhận đơn hàng và khôi phục mật khẩu của bạn có thể bắt đầu bị chặn.

Một **mạng gửi email tiếp thị** sẽ giải quyết vấn đề này. Bạn thiết lập một danh tính gửi thứ hai — trên một tên miền con riêng biệt như `news.cuacuahang.com` — và đánh dấu nó là tiếp thị. Spwig sau đó sẽ gửi mọi chiến dịch từ danh tính đó và giữ email giao dịch trên tên miền chính của bạn. Một chiến dịch kém chất lượng sẽ không còn kéo theo mail mà khách hàng *cần* nhận được nữa.

> Điều này áp dụng cho các cửa hàng tự host. Trên các kế hoạch được host bởi Spwig, uy tín gửi email sẽ được quản lý thay bạn.

## Cách Spwig quyết định danh tính nào sẽ sử dụng

Một khi đã có một tài khoản gửi email tiếp thị, việc định tuyến sẽ tự động — bạn không cần phải gắn thẻ gì cả:

- **Email tiếp thị** (chiến dịch, hành trình, bản tin, khôi phục giỏ hàng, thông báo hàng về lại kho) →
  mạng gửi email tiếp thị.
- **Email giao dịch** (đơn hàng, vận chuyển, khôi phục mật khẩu, xác minh) → tên miền chính của bạn.

Nếu bạn chưa bao giờ thiết lập mạng gửi email tiếp thị, mọi thứ sẽ vẫn như cũ: mọi thứ vẫn được gửi từ tài khoản mặc định của bạn như trước đây.

## Thiết lập

Bạn có thể bắt đầu từ bất kỳ điểm vào nào:

- Nút **"Thiết lập mạng gửi email tiếp thị"** trên thanh banner của Campaign Studio, hoặc
- **Email → "Mạng gửi email tiếp thị"**.

![Cửa sổ chính của Campaign Studio với thanh banner "Bảo vệ email giao dịch của bạn" và nút Thiết lập mạng gửi email tiếp thị](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

![Nút Mạng gửi email tiếp thị trên danh sách Email, bên cạnh Browse Providers](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)

Cả hai đều mở trình hướng dẫn thiết lập email với cờ cho tài khoản tiếp thị. Sau đó:

1. **Chọn một tên miền con.** Sử dụng một cái như `news.cuacuahang.com` hoặc
   `mail.cuacuahang.com`. Đây là bước quan trọng nhất: danh tính tiếp thị phải là một
   **tên miền (con) khác** so với tên miền mà email giao dịch của bạn sử dụng — sự tách biệt
   này chính xác là điều bảo vệ uy tín email giao dịch của bạn. Việc gửi email tiếp thị từ tên miền chính của bạn sẽ không mang lại sự tách biệt nào.
2. **Nhập địa chỉ người gửi** trên tên miền con đó, ví dụ: `news@news.cuacuahang.com`.
3. **Thêm các bản ghi DNS.** Trình hướng dẫn tạo các bản ghi SPF, DKIM và DMARC cho tên miền con — bao gồm một khóa DKIM duy nhất cho danh tính tiếp thị này. Thêm chúng tại nhà cung cấp DNS của bạn (trình hướng dẫn có nút sao chép và các tab theo nhà cung cấp), sau đó chạy kiểm tra cho đến khi tất cả các bản ghi đều đạt.
4. **Hoàn tất.** Tài khoản được tạo và được đánh dấu là **Chỉ tiếp thị**. Từ nay về sau, các chiến dịch của bạn sẽ được gửi từ đó.

Bạn có thể xác minh nó hoạt động trên danh sách **Email Accounts**: bạn sẽ thấy một tài khoản thứ hai với mục đích là **Chỉ tiếp thị**, và thanh banner của Campaign Studio sẽ biến mất.

## Một số điều cần biết

- **Bạn không thể vô tình làm hỏng email giao dịch.** Spwig sẽ không cho phép bạn đặt tài khoản duy nhất của mình thành "Chỉ tiếp thị", hoặc vô hiệu hóa/xóa tài khoản giao dịch cuối cùng của bạn — luôn có nơi nào đó để xác nhận đơn hàng và khôi phục mật khẩu đến.
- **Làm quen dần.** Một mạng gửi email mới sẽ không có uy tín nào cả.

Tăng khối lượng lên trong vài tuần thay vì gửi toàn bộ danh sách của bạn vào ngày đầu tiên.
- **Giữ cho DNS của tên miền con luôn khỏe mạnh.** SPF, DKIM và DMARC trên tên miền con tiếp thị cần phải luôn hợp lệ, giống như tên miền chính của bạn.

Giữ cho DNS của tên miền con luôn khỏe mạnh. SPF, DKIM và DMARC trên tên miền con tiếp thị cần phải luôn hợp lệ, giống như tên miền chính của bạn.

Xem [Email Deliverability Runbook](deliverability) để có cái nhìn đầy đủ.
- **Sự đồng ý vẫn được áp dụng.** Thư quảng cáo chỉ được gửi đến các người đăng ký đã đồng ý,
  và mỗi chiến dịch đều có liên kết hủy đăng ký — việc tách biệt tên miền không làm thay đổi bất kỳ điều gì trong số đó.