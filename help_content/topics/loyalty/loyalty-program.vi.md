---
title: Chương trình khách hàng thân thiết
---

Chương trình khách hàng thân thiết cho phép bạn thưởng khách hàng cho các lần mua hàng và sự tương tác thông qua hệ thống điểm. Khách hàng tích lũy điểm, thăng cấp và đổi lấy quà tặng. Di chuyển đến **Marketing > Chương trình khách hàng thân thiết** trong thanh bên quản trị.

![Bảng điều khiển khách hàng thân thiết](/static/core/admin/img/help/loyalty-program/loyalty-dashboard.webp)

## Bảng điều khiển khách hàng thân thiết

Bảng điều khiển cung cấp cái nhìn tổng quát về chương trình khách hàng thân thiết của bạn:

### Chỉ số chính

- **Tổng số thành viên** — Tổng số khách hàng đã đăng ký
- **Thành viên hoạt động (30 ngày)** — Những thành viên đã tích lũy hoặc đổi điểm trong 30 ngày qua
- **Điểm chưa đổi** — Tổng số điểm chưa được đổi của tất cả thành viên
- **Tỷ lệ đổi điểm** — Phần trăm điểm đã được đổi so với tổng điểm đã tích lũy
- **Điểm tích lũy (30 ngày)** — Điểm tích lũy trong 30 ngày qua
- **Điểm đã đổi (30 ngày)** — Điểm đã đổi trong 30 ngày qua
- **Điểm trung bình/Thành viên** — Số điểm trung bình mỗi thành viên
- **Quy tắc đang hoạt động** — Số lượng quy tắc tích điểm đang được kích hoạt

### Hành động nhanh

Bảng điều khiển có các thẻ tắt để quản lý mọi khía cạnh của chương trình:
- **Thành viên** — Xem và quản lý các thành viên khách hàng thân thiết
- **Cấp bậc** — Cấu hình các cấp bậc thành viên
- **Quà tặng** — Thiết lập danh mục quà tặng
- **Lịch sử đổi quà** — Xem lịch sử đổi quà
- **Quy tắc** — Cấu hình cách tích điểm
- **Huy hiệu** — Quản lý các huy hiệu thành tích
- **Chiến dịch** — Tổ chức các chiến dịch khách hàng thân thiết đặc biệt
- **Nhóm** — Tạo các nhóm thành viên để nhắm mục tiêu

### Biểu đồ và phân tích

- **Xu hướng đăng ký thành viên** — Số lượng thành viên mới đăng ký theo thời gian
- **Điểm tích lũy vs. Điểm đã đổi** — Theo dõi sự cân bằng luồng điểm
- **Phân bố cấp bậc** — Xem cách các thành viên được phân bố theo cấp bậc

## Thiết lập chương trình

### Bước 1: Tạo cấp bậc

Cấp bậc xác định các cấp độ thành viên với các quyền lợi ngày càng cao:

1. Di chuyển đến **Chương trình khách hàng thân thiết > Cấp bậc**
2. Tạo các cấp bậc như Đồng, Bạc, Vàng, Bạch kim
3. Đối với mỗi cấp bậc, hãy thiết lập:
   - **Tên** — Tên hiển thị của cấp bậc
   - **Hạng** — Thứ tự sắp xếp (hạng thấp hơn = cấp bậc thấp hơn, ví dụ: Đồng = 1, Bạc = 2)
   - **Màu sắc** — Màu sắc nhấn mạnh được hiển thị trên huy hiệu thành viên
   - **Điểm tối thiểu để đạt cấp bậc** — Số điểm tích lũy suốt đời để đủ điều kiện đạt cấp bậc này
   - **Mức chi tiêu tối thiểu** — Tổng số tiền chi tiêu để đủ điều kiện đạt cấp bậc này
   - **Số đơn hàng tối thiểu** — Số lượng đơn hàng để đủ điều kiện đạt cấp bậc này
   - **Hệ số nhân điểm** — Tỷ lệ tích điểm bổ sung cho các thành viên ở cấp bậc này (ví dụ: 2.0 = 2 lần điểm)

Một thành viên đủ điều kiện đạt cấp bậc nếu **bất kỳ** trong ba ngưỡng được đáp ứng. Bạn có thể chỉ sử dụng một ngưỡng hoặc kết hợp cả ba.

### Bước 2: Cấu hình quy tắc tích điểm

Quy tắc xác định cách khách hàng tích điểm:

1. Di chuyển đến **Chương trình khách hàng thân thiết > Quy tắc**
2. Tạo quy tắc bằng một trong bốn loại quy tắc sau:

| Loại quy tắc | Mô tả | Ví dụ |
|-------------|-------|-------|
| **Chi tiêu** | Điểm cho mỗi số tiền chi tiêu | 1 điểm cho mỗi $1 |
| **Sản phẩm** | Điểm cho mỗi sản phẩm mua | 50 điểm cho mỗi sản phẩm trong một danh mục cụ thể |
| **Hành động** | Điểm cho một hành động cụ thể | 200 điểm cho việc đăng ký |
| **Sự kiện** | Điểm cho một sự kiện trong lịch | Điểm thưởng sinh nhật |

3. Cấu hình các cài đặt quy tắc bổ sung:
   - **Phạm vi / Lọc phạm vi** — Giới hạn quy tắc cho các sản phẩm, danh mục cụ thể hoặc cấp bậc thành viên
   - **Số tiền đơn hàng tối thiểu** — Số tiền giỏ hàng tối thiểu để quy tắc áp dụng
   - **Cấp bậc được phép** — Giới hạn quy tắc cho các cấp bậc thành viên cụ thể
   - **Là độc quyền** — Khi được bật, quy tắc này không thể chồng chéo với các quy tắc khác
   - **Số ngày điểm chờ** — Số ngày trước khi điểm tích lũy trở nên có thể sử dụng (có thể hữu ích để tính đến thời gian hoàn tiền)
   - **Số ngày điểm hết hạn** — Số ngày sau khi tích lũy trước khi điểm hết hạn (trống để không có ngày hết hạn)
   - **Bắt đầu / Kết thúc** — Giới hạn quy tắc cho một khoảng thời gian cụ thể

### Bước 3: Thiết lập quà tặng

Quà tặng là những gì khách hàng có thể đổi điểm:

1. Di chuyển đến **Chương trình khách hàng thân thiết > Quà tặng**
2. Tạo các quà tặng như:
   - **Mã giảm giá $5** — 500 điểm
   - **Miễn phí vận chuyển** — 300 điểm
   - **Giảm 10%** — 1000 điểm

> **Mã giảm giá không thể được sử dụng lúc này.** Một phần thưởng có **Loại phần thưởng** được đặt thành **Mã giảm giá** — như ví dụ về phiếu giảm giá 5 USD hoặc phiếu giảm giá 10% ở trên — hiện tại không thể sử dụng được.

Thành viên sẽ thấy một lỗi rõ ràng và điểm của họ sẽ tự động được hoàn lại vào số dư, vì vậy không có gì bị mất, nhưng phần thưởng vẫn chưa thể sử dụng được.

Đây là một sự sửa lỗi cố ý: việc sử dụng trước đây báo cáo thành công trong khi âm thầm trừ điểm và không cấp bất cứ thứ gì.

Nếu thành viên nói rằng việc sử dụng "không hoạt động", đó chính là lỗi này — không phải là vấn đề mới.

Các phần thưởng theo điểm sẽ bắt đầu hoạt động trở lại trong một bản phát hành sắp tới.

Điều này không ảnh hưởng đến các phần thưởng Miễn phí vận chuyển, Miễn phí sản phẩm hoặc Trải nghiệm/Tri ân.

### Bước 4: Tạo Huy hiệu (Tùy chọn)

Huy hiệu ghi nhận các thành tựu của khách hàng:

1. Di chuyển đến **Loyalty > Badges**
2. Tạo huy hiệu cho các mốc quan trọng:
   - **Lần mua đầu tiên** — Được trao sau lần đặt hàng đầu tiên
   - **Người chi tiêu lớn** — Được trao sau khi chi tiêu 500 USD trở lên
   - **Khách hàng trung thành** — Được trao sau 10 đơn hàng

Huy hiệu có thể bao gồm việc trao thêm điểm khi đạt được.

## Quản lý Thành viên

### Danh sách Thành viên

Xem tất cả các thành viên trung thành cùng với:
- Mức độ và trạng thái hiện tại
- Số dư điểm
- Ngày đăng ký
- Hoạt động gần đây

### Những người kiếm điểm cao nhất

Bảng điều khiển nổi bật các thành viên tích cực nhất của bạn với bảng xếp hạng hiển thị thứ hạng, tên, mức độ và điểm đã kiếm được trong khoảng thời gian.

### Giao dịch gần đây

Lịch sử giao dịch hiển thị tất cả hoạt động điểm gần đây. Các loại giao dịch bao gồm:

| Loại | Ý nghĩa |
|------|---------|
| **Kiếm được** | Điểm được cộng từ một lần mua hàng đạt tiêu chuẩn hoặc quy tắc |
| **Sử dụng** | Điểm được sử dụng cho một phần thưởng |
| **Tặng thêm** | Điểm bổ sung từ một huy hiệu, chiến dịch hoặc trao điểm thủ công |
| **Điều chỉnh** | Sửa đổi điểm thủ công được thực hiện bởi nhân viên |
| **Hủy bỏ** | Điểm bị xóa (ví dụ sau khi hủy đơn hàng) |
| **Hết hạn** | Điểm đã hết hạn |

### Điều chỉnh điểm thủ công

Bạn có thể thêm hoặc trừ điểm thủ công cho bất kỳ thành viên nào:

1. Mở trang chi tiết của thành viên
2. Nhấp vào **Điều chỉnh điểm**
3. Nhập số điểm (dương để thêm, âm để trừ)
4. Nhập lý do cho việc điều chỉnh
5. Nhấp vào **Lưu**

Việc điều chỉnh được ghi lại như một giao dịch và hiển thị trong lịch sử giao dịch của thành viên.

## Chiến dịch

Chiến dịch trung thành cho phép bạn chạy các chương trình khuyến mãi đặc biệt:
- **Tuần lễ nhân đôi điểm** — Tăng tạm thời tỷ lệ kiếm điểm
- **Sự kiện tặng điểm bổ sung** — Tặng thêm điểm cho các hành động cụ thể
- **Chiến dịch nâng cấp mức độ** — Giảm ngưỡng để nâng cấp mức độ

## Một số lưu ý

- Bắt đầu với các quy tắc kiếm điểm đơn giản (1 điểm cho mỗi 1 USD chi tiêu) và mở rộng theo thời gian.
- Thiết lập ngưỡng phần thưởng khả thi để duy trì sự tham gia của thành viên — nếu phần thưởng cảm giác không thể đạt được, thành viên sẽ mất hứng thú.
- Sử dụng huy hiệu để gamify trải nghiệm và khuyến khích hành vi cụ thể.
- Theo dõi tỷ lệ sử dụng — một chương trình lành mạnh có tỷ lệ sử dụng 10-30%.
- Chạy chiến dịch trong các giai đoạn ít hoạt động để tăng cường sự tham gia.
- Sử dụng biểu đồ Điểm kiếm được so với Điểm sử dụng để đảm bảo chương trình của bạn có thể duy trì được.