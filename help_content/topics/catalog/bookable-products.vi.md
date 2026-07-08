---
title: Sản phẩm có thể đặt chỗ
---

Sản phẩm có thể đặt chỗ cho phép khách hàng đặt một ngày và giờ cụ thể khi họ mua hàng. Điều này hỗ trợ các cuộc hẹn, thuê thiết bị, lớp học, sự kiện và đặt chỗ lưu trú — tất cả đều được quản lý trực tiếp từ bảng điều khiển Spwig của bạn.

## Loại đặt chỗ

| Loại | Phù hợp nhất |
|------|----------|
| **Cuộc hẹn** | Dịch vụ: tư vấn, cắt tóc, huấn luyện cá nhân |
| **Thuê** | Thuê thiết bị, thuê xe, thuê phòng |
| **Lớp học / Workshop** | Các buổi học nhóm với số lượng người tham gia cố định |
| **Lưu trú** | Các chuyến lưu trú nhiều đêm với giờ check-in/check-out |
| **Sự kiện** | Các sự kiện một lần hoặc lặp lại có vé |

## Thiết lập sản phẩm có thể đặt chỗ

### Bước 1: Tạo sản phẩm

1. Truy cập **Sản phẩm > Tất cả sản phẩm** và nhấp **+ Thêm sản phẩm**
2. Thiết lập **Loại sản phẩm** thành **Sản phẩm đặt chỗ**
3. Hoàn tất các trường sản phẩm tiêu chuẩn (tên, mô tả, giá)
4. Lưu sản phẩm

### Bước 2: Cấu hình cài đặt đặt chỗ

Sau khi lưu, phần **Cấu hình đặt chỗ** sẽ xuất hiện trên biểu mẫu chỉnh sửa sản phẩm. Điền các cài đặt đặt chỗ:

#### Loại đặt chỗ và thời gian

- **Loại đặt chỗ** — Chọn loại phù hợp nhất với dịch vụ của bạn (Cuộc hẹn, Thuê, Lớp học, v.v.)
- **Loại thời gian** — Chọn **Thời gian cố định** cho các buổi có độ dài cố định, hoặc chọn **Khách hàng chọn thời gian** để cho phép khách hàng chọn thời gian họ cần
- **Thời gian** và **Đơn vị thời gian** — Thiết lập độ dài (ví dụ: `60` phút, `1` giờ, `2` ngày)
- **Thời gian tối thiểu/tối đa** — Nếu khách hàng có thể chọn thời gian, hãy thiết lập khoảng thời gian cho phép

#### Thời gian đệm

Thời gian đệm được thêm tự động giữa các cuộc đặt chỗ để cho phép chuẩn bị hoặc dọn dẹp:
- **Thời gian đệm trước** — Số phút được dành trước khi cuộc đặt chỗ bắt đầu
- **Thời gian đệm sau** — Số phút được dành sau khi cuộc đặt chỗ kết thúc

Ví dụ, một cuộc hẹn massage 60 phút với 15 phút thời gian đệm sau sẽ cho phép 15 phút để chuẩn bị cho khách hàng tiếp theo.

#### Thời gian đặt chỗ trước

- **Thông báo đặt chỗ tối thiểu** — Thời gian khách hàng phải đặt chỗ trước (ví dụ: `24 giờ` để không cho phép đặt chỗ cùng ngày)
- **Thời gian đặt chỗ tối đa** — Thời gian trong tương lai khách hàng có thể đặt chỗ (ví dụ: `365 ngày`)

#### Số lượng

- **Số lượng đặt chỗ tối đa mỗi khung giờ** — Đối với lớp học và sự kiện, hãy thiết lập số lượng khách hàng có thể đặt cùng một khung giờ. Thiết lập thành `1` cho các cuộc hẹn riêng tư.

#### Xác nhận

- **Yêu cầu xác nhận thủ công** — Khi được chọn, các cuộc đặt chỗ sẽ không được xác nhận tự động. Bạn phải xác nhận từng cuộc đặt chỗ từ danh sách đặt chỗ. Hữu ích khi bạn muốn kiểm tra khách hàng trước khi xác nhận.

#### Chính sách hủy

- **Cho phép hủy** — Khách hàng có thể hủy cuộc đặt chỗ của họ hay không
- **Thời hạn hủy** — Số giờ/ngày trước cuộc đặt chỗ mà khách hàng có thể hủy (ví dụ: `24 giờ`)

#### Hiển thị lịch

Cách khách hàng chọn ngày và giờ trên trang sản phẩm:

| Chế độ hiển thị | Phù hợp nhất |
|-------------|----------|
| **Xem lịch** | Sử dụng chung — lịch đầy đủ theo tháng |
| **Chọn ngày** | Chọn đơn giản một ngày |
| **Danh sách ngày có sẵn** | Sản phẩm có số lượng chỗ trống giới hạn |
| **Chọn khoảng ngày** | Lưu trú và thuê nhiều ngày |

#### Tiền cọc

Để yêu cầu tiền cọc tại thanh toán thay vì thanh toán đầy đủ:
1. Chọn **Bật tiền cọc**
2. Thiết lập **Loại tiền cọc** thành **Số tiền cố định** hoặc **Tỷ lệ phần trăm của tổng số**
3. Nhập **Số tiền cọc** (ví dụ: `50` cho $50, hoặc `25` cho 25%)

#### Cài đặt đặc biệt cho lưu trú

Đối với đặt chỗ lưu trú, các trường bổ sung sẽ xuất hiện:
- **Giờ check-in** và **Giờ check-out** — Thời gian tiêu chuẩn cho tài sản
- **Số lượng khách tiêu chuẩn** — Số lượng khách mặc định được bao gồm trong giá cơ bản

### Bước 3: Thêm tài nguyên đặt chỗ (tùy chọn)

Các tài nguyên là các vật thể vật lý hoặc nhân viên được gán cho một cuộc đặt chỗ — ví dụ: "Phòng 1", "Sân A" hoặc "Giáo viên Sam".

1. Trên biểu mẫu chỉnh sửa sản phẩm, đi đến phần **Tài nguyên đặt chỗ**
2. Nhấp **Thêm tài nguyên**
3. Đặt tên cho tài nguyên và thiết lập **Sức chứa** (số lượng cuộc đặt chỗ mà tài nguyên có thể xử lý cùng lúc)
4. Tùy chọn thêm hình ảnh tài nguyên


Tài nguyên cho phép bạn theo dõi tính khả dụng theo từng tài sản hoặc nhân viên cụ thể, không chỉ theo từng khoảng thời gian.

### Bước 4: Thiết lập quy tắc tính khả dụng

Các quy tắc tính khả dụng xác định thời điểm đặt chỗ có thể được thực hiện:

1. Trong phần **Tính khả dụng** của sản phẩm, nhấp vào **Thêm quy tắc tính khả dụng**
2. Chọn **Tài nguyên** mà quy tắc này áp dụng
3. Thiết lập **Các ngày trong tuần** mà đặt chỗ có thể thực hiện
4. Thiết lập **Thời gian bắt đầu** và **Thời gian kết thúc** cho khoảng thời gian khả dụng
5. Tùy chọn thiết lập khoảng thời gian (**Bắt đầu từ**) / (**Kết thúc vào**) cho tính khả dụng theo mùa
6. Lưu

## Xem và quản lý đặt chỗ

### Danh sách đặt chỗ

Truy cập **Catalog > Đặt chỗ** để xem tất cả các đặt chỗ. Bạn có thể lọc theo:
- Trạng thái (Chờ xác nhận, Đã xác nhận, Đã hủy, Đã hoàn thành, Không đến)
- Sản phẩm
- Khoảng thời gian

### Trạng thái đặt chỗ

| Trạng thái | Ý nghĩa |
|------------|---------|
| **Chờ xác nhận** | Đang chờ phê duyệt thủ công (nếu yêu cầu xác nhận) |
| **Đã xác nhận** | Đặt chỗ đã được xác nhận và đang hoạt động |
| **Đã hủy** | Đặt chỗ đã bị hủy bởi khách hàng hoặc bạn |
| **Đã hoàn thành** | Ngày đặt chỗ đã qua và được thực hiện |
| **Không đến** | Khách hàng không đến |

### Xác nhận đặt chỗ đang chờ

1. Mở đặt chỗ từ **Catalog > Đặt chỗ**
2. Thay đổi **Trạng thái** thành **Đã xác nhận**
3. Lưu — khách hàng sẽ tự động nhận được email xác nhận

### Hủy đặt chỗ

1. Mở đặt chỗ
2. Thay đổi **Trạng thái** thành **Đã hủy**
3. Nhập **Lý do hủy** (hiển thị trong email của khách hàng)
4. Lưu

## Quản lý danh sách chờ

Khi một khoảng thời gian đã đầy, khách hàng có thể thêm mình vào danh sách chờ. Spwig sẽ tự động thông báo cho các khách hàng đang trong danh sách chờ khi có sự hủy bỏ tạo ra một vị trí trống.

### Xem danh sách chờ

Truy cập **Catalog > Danh sách chờ đặt chỗ** để xem tất cả các mục trong danh sách chờ. Mỗi mục hiển thị:
- Tên và email của khách hàng
- Sản phẩm và ngày mong muốn
- Trạng thái: **Đang chờ**, **Đã thông báo**, **Đã chuyển thành đặt chỗ**, hoặc **Hết hạn**

### Trạng thái danh sách chờ

| Trạng thái | Ý nghĩa |
|------------|---------|
| **Đang chờ** | Khách hàng đang xếp hàng, vị trí chưa khả dụng |
| **Đã thông báo** | Khách hàng đã được gửi email về vị trí khả dụng |
| **Đã chuyển thành đặt chỗ** | Khách hàng đã chọn vị trí và hoàn tất đặt chỗ |
| **Hết hạn** | Ngày mong muốn đã qua mà không có vị trí khả dụng |

### Thông báo thủ công cho khách hàng đang chờ

Nếu bạn muốn liên hệ với một khách hàng cụ thể trong danh sách chờ trước khi thông báo tự động:
1. Mở mục danh sách chờ
2. Sao chép địa chỉ email của họ và liên hệ trực tiếp
3. Khi họ hoàn tất đặt chỗ, trạng thái mục danh sách chờ của họ sẽ được cập nhật thành **Đã chuyển thành đặt chỗ**

## Một số mẹo

- Bật xác nhận thủ công cho các đặt chỗ có giá trị cao (ví dụ: buổi chụp ảnh, sự kiện riêng tư) để bạn có thể kiểm tra tính khả dụng và phù hợp yêu cầu trước khi cam kết.
- Thiết lập thời gian đệm một cách rộng rãi khi bắt đầu — bạn luôn có thể giảm nó sau khi hiểu được nhu cầu thực tế.
- Đối với các lớp học nhóm, hãy thiết lập **Số lượng đặt chỗ tối đa mỗi khoảng thời gian** bằng sức chứa của lớp và bật danh sách chờ để các buổi học phổ biến tự động xây dựng hàng đợi.
- Sử dụng chế độ hiển thị trình chọn khoảng thời gian cho sản phẩm lưu trú — khách hàng mong muốn chọn ngày đến và ngày đi cùng lúc.
- Thiết lập thông báo trước tối thiểu để ngăn đặt chỗ vào phút chót nếu bạn cần thời gian chuẩn bị (ví dụ: 48 giờ tối thiểu cho các đơn đặt hàng ẩm thực tùy chỉnh).
- Kiểm tra danh sách chờ thường xuyên trong các mùa cao điểm — việc liên hệ thủ công với các khách hàng đang trong danh sách chờ có thể lấp đầy các sự hủy bỏ nhanh hơn so với thông báo tự động.