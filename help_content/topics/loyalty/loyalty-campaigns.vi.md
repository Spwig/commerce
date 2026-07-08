---
title: Chiến dịch trung thành
---

Chiến dịch trung thành cho phép bạn chạy các chương trình khuyến mãi có thời hạn và phần thưởng tự động vượt qua các quy tắc kiếm điểm hàng ngày của bạn. Sử dụng chúng để chạy các chương trình điểm đôi vào cuối tuần, thưởng khách hàng vào ngày sinh nhật, thu hút lại những khách hàng không hoạt động và cung cấp các phần thưởng nhắm mục tiêu cho các nhóm thành viên cụ thể.

Mỗi chiến dịch xác định một sự kiện kích hoạt hoặc lịch trình, các thành viên áp dụng và các hành động cần thực hiện. Khi đã kích hoạt, các chiến dịch sẽ tự động kích hoạt — bạn chỉ cần thiết lập một lần và Spwig sẽ xử lý phần còn lại.

## Các loại chiến dịch

| Loại | Khi nào kích hoạt |
|------|---------------|
| **Dựa trên sự kiện** | Khi một sự kiện cụ thể xảy ra (ví dụ: một đơn hàng được đặt, ngày sinh nhật được phát hiện) |
| **Lịch trình** | Theo lịch trình lặp lại (hàng ngày, hàng tuần, hàng tháng) |
| **Tay** | Chỉ khi bạn chạy nó một cách rõ ràng từ bảng điều khiển |
| **Hành vi** | Khi khách hàng phù hợp với mô hình hành vi (ví dụ: xem nhưng không mua) |

## Tạo chiến dịch

Truy cập **Khuyến mãi > Chiến dịch trung thành** và nhấp **+ Thêm chiến dịch trung thành**.

### Bước 1: Thông tin cơ bản

- **Tên** — tên rõ ràng, mô tả chỉ hiển thị trong bảng điều khiển (ví dụ: `Phần thưởng sinh nhật — 200 điểm`)
- **Slug** — được tạo tự động từ tên; sử dụng nội bộ
- **Mô tả** — ghi chú tùy chọn về mục đích của chiến dịch
- **Loại chiến dịch** — chọn loại từ bảng trên

### Bước 2: sự kiện kích hoạt hoặc lịch trình

**Đối với chiến dịch dựa trên sự kiện**, hãy thiết lập **Sự kiện kích hoạt** kích hoạt chiến dịch. Các sự kiện kích hoạt có sẵn bao gồm:

| Sự kiện kích hoạt | Mô tả |
|---------|-------------|
| Đơn hàng được đặt | Kích hoạt khi thành viên hoàn tất đơn hàng |
| Đơn hàng đầu tiên | Kích hoạt trên đơn hàng đầu tiên của thành viên |
| Sinh nhật khách hàng | Kích hoạt vào ngày sinh nhật của thành viên |
| Cứu sinh nhật thành viên | Kích hoạt mỗi năm vào ngày kỷ niệm tham gia của thành viên |
| Giỏ hàng bị bỏ lại | Kích hoạt khi giỏ hàng bị bỏ lại mà không thanh toán |
| Thăng hạng | Kích hoạt khi thành viên thăng hạng lên cấp cao hơn |
| Điểm sắp hết hạn | Kích hoạt khi thành viên có điểm sắp hết hạn |
| Không mua trong 90 ngày | Kích hoạt khi thành viên không mua trong 90 ngày |
| Đánh giá được gửi | Kích hoạt khi thành viên gửi đánh giá sản phẩm |
| Khách hàng được giới thiệu | Kích hoạt khi khách hàng được giới thiệu thực hiện mua hàng |

Bạn có thể thêm **Điều kiện kích hoạt** dưới dạng đối tượng JSON để lọc thêm khi chiến dịch kích hoạt. Ví dụ, chỉ kích hoạt cho các đơn hàng trên 100 đô la:

```json
{
  "min_order_amount": 100
}
```

**Đối với chiến dịch lịch trình**, hãy thiết lập **Loại lịch trình** (Hàng ngày, Hàng tuần, Hàng tháng hoặc Cron tùy chỉnh) và cấu hình thời gian trong trường **Cấu hình lịch trình**:

```json
{
  "hour": 9,
  "minute": 0
}
```

### Bước 3: hành động

Trường **Hành động** xác định điều gì xảy ra khi chiến dịch kích hoạt. Nhập một mảng JSON của các đối tượng hành động. Hành động phổ biến nhất là trao điểm thưởng:

```json
[
  {
    "type": "award_points",
    "points": 200,
    "description": "Phần thưởng sinh nhật — cảm ơn bạn đã là thành viên!"
  }
]
```

Các hành động khác có sẵn bao gồm gửi thông báo qua email hoặc trao một biểu tượng. Vui lòng tham khảo tài liệu thành phần nhà cung cấp của bạn để biết danh sách đầy đủ.

### Bước 4: nhắm mục tiêu

Sử dụng các trường nhắm mục tiêu để kiểm soát các thành viên chiến dịch áp dụng:

- **Nhắm mục tiêu tất cả các thành viên** — được chọn mặc định; chiến dịch áp dụng cho mọi thành viên trung thành đang hoạt động
- **Nhắm mục tiêu phân khúc** — giới hạn chiến dịch cho các thành viên trong phân khúc cụ thể (xem [Phân khúc](#managing-member-segments) bên dưới)
- **Nhắm mục tiêu cấp bậc** — giới hạn chiến dịch cho các thành viên trong cấp bậc trung thành cụ thể

### Bước 5: giới hạn và thời gian làm lạnh

- **Số lần kích hoạt tối đa mỗi thành viên** — số lần cùng một thành viên có thể hưởng lợi từ chiến dịch này. Đặt thành `1` cho các phần thưởng một lần như phần thưởng sinh nhật. Để trống để không giới hạn.
- **Thời gian làm lạnh (ngày)** — số ngày tối thiểu giữa các lần kích hoạt chiến dịch cho cùng một thành viên. Ví dụ, đặt thành `365` để ngăn chiến dịch sinh nhật kích hoạt nhiều hơn một lần mỗi năm.

### Bước 6: ngày chiến dịch

Đặt **Ngày bắt đầu** và **Ngày kết thúc** để làm cho chiến dịch có thời hạn. Để trống cả hai để chiến dịch diễn ra liên tục.

Chiến dịch có thể ở một trong những trạng thái sau:

| Trạng thái | Mô tả |
|----------|--------|
| **Bản nháp** | Đã tạo nhưng chưa kích hoạt; an toàn để cấu hình và kiểm tra |
| **Kích hoạt** | Đang chạy và sẽ được kích hoạt khi điều kiện được đáp ứng |
| **Tạm dừng** | Được dừng tạm thời mà không làm mất cấu hình |
| **Kết thúc** | Quá ngày kết thúc; không còn được kích hoạt |
| **Lưu trữ** | Ẩn khỏi danh sách đang hoạt động nhưng được lưu trữ để tham khảo |

Sau khi điền đầy đủ các trường, nhấp **Lưu**. Sau đó thay đổi trạng thái thành **Kích hoạt** để bắt đầu chiến dịch.

## Các ví dụ thực tế

### Ví dụ: điểm thưởng gấp đôi vào cuối tuần

**Tình huống:** Trao 2 lần điểm thưởng cho tất cả các đơn hàng được đặt vào một cuối tuần cụ thể.

| Trường | Giá trị |
|-------|--------|
| Tên | `Double Points Weekend — March` |
| Loại chiến dịch | Dựa trên sự kiện |
| Sự kiện kích hoạt | Đơn hàng được đặt |
| Hành động | `["{\"type\": \"award_points_multiplier\", \"multiplier\": 2.0}"]` |
| Ngày bắt đầu | Buổi tối thứ Sáu |
| Ngày kết thúc | Giờ 00:00 Chủ Nhật |
| Mục tiêu tất cả thành viên | Đã chọn |

### Ví dụ: phần thưởng sinh nhật

**Tình huống:** Trao 200 điểm thưởng cho mỗi thành viên trung thành vào ngày sinh nhật của họ.

| Trường | Giá trị |
|-------|--------|
| Tên | `Birthday Bonus` |
| Loại chiến dịch | Dựa trên sự kiện |
| Sự kiện kích hoạt | Sinh nhật khách hàng |
| Hành động | `["{\"type\": \"award_points\", \"points\": 200, \"description\": \"Happy birthday from us!\"}"]` |
| Số lần kích hoạt tối đa cho mỗi thành viên | 1 |
| Thời gian làm nóng | 365 |
| Mục tiêu tất cả thành viên | Đã chọn |

### Ví dụ: chiến dịch thu hút lại

**Tình huống:** Gửi 100 điểm thưởng cho các thành viên chưa mua hàng trong 90 ngày.

| Trường | Giá trị |
|-------|--------|
| Tên | `90-Day Win-Back Bonus` |
| Loại chiến dịch | Dựa trên sự kiện |
| Sự kiện kích hoạt | Không hoạt động trong 90 ngày |
| Hành động | `["{\"type\": \"award_points\", \"points\": 100, \"description\": \"We miss you — here are some bonus points\"}"]` |
| Số lần kích hoạt tối đa cho mỗi thành viên | 1 |
| Thời gian làm nóng | 180 |
| Mục tiêu tất cả thành viên | Đã chọn |

## Quản lý các nhóm thành viên

Các nhóm giúp bạn nhắm mục tiêu các chiến dịch đến các nhóm cụ thể của các thành viên trung thành. Di chuyển đến **Khuyến mãi > Nhóm thành viên trung thành** để quản lý chúng.

### Loại nhóm

| Loại | Mô tả |
|------|--------|
| **Dựa trên quy tắc** | Thành viên được xác định bởi các quy tắc (ví dụ: các thành viên có hơn 1.000 điểm) |
| **Tính toán động** | Thành viên được tính toán theo yêu cầu từ các tiêu chí thời gian thực |
| **Gán thủ công** | Các thành viên được thêm vào nhóm một cách thủ công |

### Tạo một nhóm

1. Di chuyển đến **Khuyến mãi > Nhóm thành viên trung thành** và nhấp **+ Thêm nhóm thành viên trung thành**
2. Điền vào:
   - **Tên** — tên mô tả (ví dụ: `Khách hàng cao cấp`, `Thành viên cấp Bạc`)
   - **Slug** — được tạo tự động
   - **Loại tiêu chí** — cách xác định thành viên
   - **Cấu hình tiêu chí** — đối tượng JSON xác định các quy tắc thành viên
3. Nhấp **Lưu**

#### Ví dụ: nhóm cho các thành viên có 500 điểm trở lên

```json
{
  "min_available_points": 500
}
```

#### Ví dụ: nhóm chỉ dành cho thành viên cấp Vàng

```json
{
  "tier_slugs": ["gold"]
}
```

Cột **Số lượng thành viên** trong danh sách nhóm hiển thị số lượng thành viên hiện tại phù hợp. Nhấp vào một nhóm và sử dụng hành động **Tái tính số lượng thành viên** để tính lại nếu dữ liệu của bạn đã thay đổi.

## Theo dõi hiệu suất chiến dịch

### Lịch sử thực thi chiến dịch

Di chuyển đến **Khuyến mãi > Thực thi chiến dịch** để xem bản ghi mỗi lần chiến dịch được kích hoạt cho bất kỳ thành viên nào. Mỗi bản ghi thực thi hiển thị chiến dịch nào đã chạy, thành viên nào đã chạy và kết quả.

### Xem lại phạm vi chiến dịch

Mở bất kỳ bản ghi chiến dịch nào để xem số **Lần kích hoạt** và thời điểm chiến dịch cuối cùng được kích hoạt. Điều này cho bạn cái nhìn nhanh về số lượng thành viên đã được hưởng lợi từ chiến dịch.

## Một số mẹo

Bảo tồn toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- Tạo chiến dịch ở trạng thái **Draft** trước để bạn có thể xem lại tất cả các cài đặt trước khi chúng được kích hoạt
- Sử dụng **Max Triggers Per Member** cho tất cả các chiến dịch thưởng một lần (sinh nhật, lần mua hàng đầu tiên, đăng ký) để ngăn khách hàng nhận thưởng nhiều hơn một lần
- Kết hợp **Target Segment** với chiến dịch dựa trên sự kiện để chạy các chương trình khuyến mãi dành riêng cho từng cấp độ — ví dụ, gấp đôi điểm thưởng cho các giao dịch chỉ dành cho thành viên Gold và Platinum
- Thiết lập giá trị **Cooldown Days** cho các chiến dịch thu hút khách hàng cũ để các thành viên không bị làm phiền nếu họ thực hiện một lần mua hàng nhỏ và sau đó trở lại không hoạt động trong thời gian ngắn
- Danh sách chiến dịch là công cụ tốt nhất để theo dõi các chương trình khuyến mãi đang hoạt động hiện tại — xem lại trước khi triển khai các ưu đãi mới để đảm bảo các chiến dịch không chồng chéo một cách vô tình
- Lưu trữ các chiến dịch đã kết thúc thay vì xóa chúng để bạn có thể có hồ sơ lịch sử về các chương trình khuyến mãi bạn đã chạy và thời gian thực hiện