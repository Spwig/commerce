---
title: Tài khoản và Khách hàng
---

Các nhà bán hàng thường đặt câu hỏi: "Sự khác biệt giữa tài khoản và khách hàng là gì?" Sự nhầm lẫn này phổ biến vì mỗi khách hàng đều là một tài khoản, nhưng không phải tài khoản nào cũng là khách hàng. Hướng dẫn này làm rõ sự khác biệt và giải thích khi nào nên sử dụng mỗi giao diện quản trị.

![Danh sách người dùng](/static/core/admin/img/help/accounts-vs-customers/user-list.webp)

## Tài khoản là gì?

Một **tài khoản** là đối tượng xác thực cốt lõi trong Spwig. Bất kỳ ai có thể đăng nhập vào nền tảng của bạn — nhân viên hoặc khách hàng — đều có tài khoản. Các tài khoản được quản lý trong hệ thống xác thực Spwig và được lưu trữ trong mô hình `User`.

Tất cả tài khoản đều có:
- **Địa chỉ email** — Nhận dạng chính và thông tin xác thực đăng nhập
- **Tên người dùng** — Tên người dùng duy nhất (mặc định được tạo tự động từ email)
- **Mật khẩu** — Được mã hóa và lưu trữ an toàn
- **Cờ is_staff** — Xác định tài khoản có thể truy cập giao diện quản trị hay không

Các tài khoản cũng có thể xác thực thông qua các nhà cung cấp OAuth (Google, Facebook, v.v.) được cấu hình tại **Cài đặt > Xác thực**.

## Khách hàng là gì?

Một **khách hàng** là một loại tài khoản đặc biệt với `is_staff=False`. Khách hàng mua sắm tại cửa hàng của bạn, đặt hàng và quản lý hồ sơ của họ. Mỗi tài khoản khách hàng được mở rộng tự động với:

- **CustomerProfile** — Lưu trữ sở thích, trạng thái đăng ký bản tin và giá trị của trường tùy chỉnh
- **CustomerMetrics** — Theo dõi giá trị vòng đời (LTV), điểm RFM, lịch sử đơn hàng và dữ liệu phân khúc
- **OrderHistory** — Liên kết đến tất cả các đơn hàng được đặt bởi khách hàng này

Khách hàng có thể là:
- **Khách hàng đã đăng ký** — Được tạo thông qua đăng ký cửa hàng hoặc quản trị
- **Người dùng tạm thời** — Tài khoản tạm thời được tạo trong quá trình thanh toán như khách hàng (tên người dùng bắt đầu bằng `guest_`)
- **Khách hàng được nhập khẩu** — Được di chuyển từ các nền tảng khác qua việc nhập CSV

## Sự khác biệt chính

| Thuộc tính | Tài khoản | Khách hàng |
|-----------|---------|----------|
| **Mục đích** | Xác thực và ủy quyền | Mua sắm, đặt hàng và phân tích |
| **Phạm vi** | Nhân viên và khách hàng | Chỉ khách hàng |
| **Cờ is_staff** | True hoặc False | Luôn False |
| **Dữ liệu mở rộng** | Không (chỉ các trường cốt lõi) | CustomerProfile + CustomerMetrics |
| **Vị trí quản trị** | Cài đặt > Người dùng | Khách hàng > Hồ sơ khách hàng |
| **Có thể đăng nhập** | Có | Có |
| **Có thể đặt hàng** | Chỉ khi có CustomerProfile | Có |
| **Có thể truy cập quản trị** | Chỉ khi is_staff=True | Không |

Tóm lại:
- Một **tài khoản** là bất kỳ ai có thể đăng nhập
- Một **khách hàng** là tài khoản mua sắm và đặt hàng

## Nhân viên cũng là tài khoản

Nhân viên là tài khoản với `is_staff=True`. Họ có thể đăng nhập vào giao diện quản trị và thực hiện các hành động dựa trên quyền **StaffRole** được chỉ định.

Nhân viên có thể có tùy chọn **CustomerProfile** nếu họ cũng mua sắm tại cửa hàng. Ví dụ, nếu bạn (nhà bán hàng) đặt một đơn hàng kiểm tra trên cửa hàng của mình, một CustomerProfile sẽ được tạo cho tài khoản nhân viên của bạn. Điều này **không ảnh hưởng** đến quyền truy cập quản trị của bạn.

Quyền của nhân viên được kiểm soát bởi:
- **StaffRole** — Xác định các phần quản trị và hành động mà nhân viên có thể truy cập
- **Cờ is_superuser** — Cấp quyền truy cập đầy đủ không giới hạn (sử dụng thận trọng)

Quản lý nhân viên tại **Cài đặt > Quản lý nhân viên**.

## Người dùng tạm thời

Thanh toán như khách hàng tạo ra các tài khoản tạm thời với tên người dùng được tạo tự động bắt đầu bằng `guest_`. Các tài khoản này:
- Có `is_staff=False` (chúng là khách hàng)
- Có CustomerProfile (để liên kết đơn hàng)
- Có mật khẩu ngẫu nhiên (khách hàng không thể đăng nhập trừ khi họ chuyển đổi thành tài khoản đã đăng ký)
- Bị loại khỏi phân tích khách hàng theo mặc định

Người dùng tạm thời có thể chuyển đổi thành khách hàng đã đăng ký bằng cách:
1. Tạo tài khoản trên cửa hàng với cùng địa chỉ email
2. Xác minh địa chỉ email
3. Hệ thống hợp nhất lịch sử đơn hàng của khách hàng tạm thời vào tài khoản đã đăng ký mới

Quản lý cài đặt chuyển đổi khách hàng tạm thời tại **Cài đặt > Thanh toán > Thanh toán như khách hàng**.

## Vị trí tìm thấy từng loại

| Vị trí quản trị | Nội dung bạn quản lý | Các trường hợp sử dụng chính |
|----------------|---------------------|-----------------------------|
| **Cài đặt > Người dùng** | Tất cả tài khoản (nhân viên + khách hàng) | Đặt lại mật khẩu, kích hoạt/tắt tài khoản, gán quyền nhân viên |
| **Cài đặt > Quản lý nhân viên** | Chỉ tài khoản nhân viên (is_staff=True) | Gán vai trò, quản lý quyền truy cập của thành viên nhóm, cấu hình quyền |
| **Khách hàng > Hồ sơ khách hàng** | Chỉ tài khoản khách hàng (is_staff=False) | Xem sở thích của khách hàng, lịch sử đơn hàng, LTV, điểm RFM, phân khúc |
| **Khách hàng > Phân tích** | Chỉ số và phân khúc khách hàng | Phân tích hành vi khách hàng, tạo phân khúc tiếp thị, theo dõi tỷ lệ giữ chân |

![Danh sách hồ sơ khách hàng](/static/core/admin/img/help/accounts-vs-customers/customer-profile-list.webp)

## Khi nào nên sử dụng từng giao diện

Sử dụng **Cài đặt > Người dùng** khi bạn cần:
- Đặt lại mật khẩu cho khách hàng
- Tắt tài khoản bị xâm nhập
- Tạo thủ công tài khoản khách hàng
- Xem kết nối đăng nhập OAuth
- Xem tất cả tài khoản (nhân viên + khách hàng) trong một danh sách

Sử dụng **Cài đặt > Quản lý nhân viên** khi bạn cần:
- Thêm thành viên mới vào nhóm
- Gán hoặc thay đổi vai trò của nhân viên
- Cấu hình quyền truy cập chi tiết
- Kiểm tra nhật ký hoạt động của nhân viên

Sử dụng **Khách hàng > Hồ sơ khách hàng** khi bạn cần:
- Xem lịch sử đơn hàng của khách hàng
- Xem sở thích và giá trị trường tùy chỉnh của khách hàng
- Kiểm tra trạng thái đăng ký bản tin
- Xem chỉ số LTV và RFM của khách hàng
- Quản lý phân khúc khách hàng

Sử dụng **Khách hàng > Phân tích** khi bạn cần:
- Nhận diện khách hàng có giá trị cao
- Tạo phân khúc tiếp thị (ví dụ, "khách hàng chưa đặt hàng trong 90 ngày")
- Phân tích xu hướng giá trị vòng đời khách hàng
- Xuất danh sách khách hàng cho chiến dịch

## Một số mẹo

- **Hồ sơ khách hàng được tạo tự động** — Khi khách hàng đặt đơn hàng đầu tiên (khách hàng hoặc đã đăng ký), Spwig tạo hồ sơ CustomerProfile và CustomerMetrics cho phân tích.
- **Nhân viên cũng có thể là khách hàng** — Nếu nhân viên đặt đơn hàng trên cửa hàng, họ sẽ có CustomerProfile. Điều này là bình thường và không ảnh hưởng đến quyền truy cập quản trị của họ.
- **Tài khoản khách hàng tạm thời làm lộn xộn danh sách người dùng** — Sử dụng giao diện hồ sơ khách hàng để tập trung vào các khách hàng thực sự và có tương tác. Danh sách người dùng bao gồm tất cả tài khoản khách hàng tạm thời.
- **Phân khúc theo is_staff=False** — Khi xuất danh sách khách hàng cho chiến dịch email, luôn lọc theo `is_staff=False` để loại bỏ các thành viên nhóm.
- **Tài khoản OAuth cũng là tài khoản** — Khi khách hàng đăng nhập qua Google hoặc Facebook, Spwig tạo tài khoản và liên kết nó với hồ sơ OAuth của họ. Trường email được điền từ nhà cung cấp OAuth.