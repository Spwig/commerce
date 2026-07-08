---
title: Tài khoản Cung cấp Vận chuyển
---

Các tài khoản cung cấp vận chuyển kết nối cửa hàng của bạn với API của các hãng vận chuyển (FedEx, UPS, DHL) để tính toán giá vận chuyển theo thời gian thực và mua nhãn vận chuyển tự động. Mỗi tài khoản lưu trữ thông tin xác thực API được mã hóa, giám sát tình trạng kết nối và liên kết với phương thức vận chuyển theo thời gian thực. Các nhà cung cấp sẽ lấy giá vận chuyển trực tiếp tại thời điểm thanh toán dựa trên kích thước, trọng lượng, điểm xuất phát và điểm đến của gói hàng—loại bỏ việc bảo trì bảng giá vận chuyển thủ công và đảm bảo giá vận chuyển chính xác.

Sử dụng tài khoản cung cấp vận chuyển khi bạn cần giá vận chuyển được tính toán bởi hãng vận chuyển hoặc tạo nhãn tự động thay vì tạo vận chuyển thủ công.

## Các nhà cung cấp vận chuyển được hỗ trợ

Spwig hỗ trợ các hãng vận chuyển lớn thông qua các thành phần cung cấp có thể cài đặt:

### FedEx

**Dịch vụ**: Ground, Express, International
**API**: FedEx Web Services
**Tính năng**: Giá vận chuyển theo thời gian thực, mua nhãn, theo dõi, quốc tế và hải quan

### UPS

**Dịch vụ**: Ground, Air, Worldwide
**API**: UPS Developer API
**Tính năng**: Giá vận chuyển theo thời gian thực, tạo nhãn, theo dõi, xác minh địa chỉ

### DHL

**Dịch vụ**: Express, eCommerce, International
**API**: DHL Express API
**Tính năng**: Giá vận chuyển quốc tế, tài liệu hải quan, theo dõi

### Các nhà cung cấp khác

Cài đặt từ thị trường thành phần khi cần (USPS, Canada Post, Australia Post, v.v.)

---

## Cấu hình Tài khoản Cung cấp Vận chuyển

Mỗi tài khoản cung cấp vận chuyển yêu cầu:

### Thông tin cơ bản

- **Tên hiển thị**: Cách tài khoản hiển thị trong quản trị (ví dụ: "Tài khoản Sản xuất FedEx")
- **Nhà cung cấp**: Chọn thành phần cung cấp đã cài đặt từ danh sách thả xuống
- **Kích hoạt**: Chuyển đổi để bật/tắt mà không xóa thông tin xác thực
- **Mặc định**: Thiết lập làm tài khoản mặc định cho nhà cung cấp này (chỉ một tài khoản mặc định cho mỗi nhà cung cấp)

### Thông tin xác thực API (được mã hóa)

**Thay đổi tùy theo nhà cung cấp**, thường bao gồm:

**FedEx**:
- Số tài khoản
- Số máy đo
- Khóa API
- Mật khẩu API

**UPS**:
- Số giấy phép truy cập
- Tên người dùng
- Mật khẩu
- Số tài khoản

**DHL**:
- ID trang web
- Mật khẩu
- Số tài khoản

**Tất cả thông tin xác thực đều được mã hóa khi lưu trữ** và chỉ được giải mã khi thực hiện gọi API.

### Địa chỉ xuất phát

- **Địa chỉ mặc định gửi từ**: Địa chỉ kho hàng/xuất phát để tính giá vận chuyển
- Một số nhà cung cấp yêu cầu thiết lập địa chỉ xuất phát cụ thể trong bảng điều khiển của họ

### Cài đặt

Tùy chọn riêng cho nhà cung cấp (thay đổi tùy theo hãng vận chuyển):

- **Chế độ kiểm tra**: Sử dụng các điểm cuối API thử nghiệm/sandbox của hãng vận chuyển
- **Giá đã đàm phán**: Sử dụng giá vận chuyển đã đàm phán của bạn (nếu có)
- **Bao gồm bảo hiểm**: Tự động báo giá bảo hiểm trong giá vận chuyển
- **Phí giao hàng đến nhà**: Áp dụng phí giao hàng đến nhà
- **Yêu cầu chữ ký**: Yêu cầu chữ ký mặc định

---

## Tạo Tài khoản Cung cấp Vận chuyển

**Quy trình thiết lập 6 bước**:

**Bước 1: Nhận quyền truy cập API của hãng vận chuyển**
1. Tạo tài khoản với hãng vận chuyển (FedEx.com, UPS.com, DHL.com)
2. Đăng ký quyền truy cập API/Tài nguyên phát triển
3. Hoàn thành quy trình hướng dẫn API của hãng vận chuyển (có thể mất 1-3 ngày làm việc)
4. Nhận thông tin xác thực API qua email hoặc cổng thông tin phát triển

**Bước 2: Cài đặt thành phần cung cấp** (nếu chưa được cài đặt trước)
1. Đi đến Cài đặt > Thành phần > Thị trường
2. Tìm kiếm tên hãng vận chuyển (ví dụ: "FedEx")
3. Cài đặt thành phần cung cấp vận chuyển
4. Chờ đến khi cài đặt hoàn tất

**Bước 3: Tạo tài khoản cung cấp trong Spwig**
1. Di chuyển đến Cài đặt > Vận chuyển > Tài khoản Cung cấp
2. Nhấp vào "Thêm Tài khoản Cung cấp"
3. Chọn nhà cung cấp từ danh sách thả xuống
4. Nhập tên hiển thị

**Bước 4: Nhập thông tin xác thực API**
1. Điền các trường thông tin xác thực (thay đổi tùy theo nhà cung cấp)
2. Thông tin xác thực được mã hóa tự động khi lưu
3. Tùy chọn: Bật chế độ kiểm tra để kiểm tra ban đầu

**Bước 5: Kiểm tra kết nối**
1. Nhấp vào nút "Kiểm tra Kết nối"
2. Hệ thống sẽ cố gắng gọi API đến hãng vận chuyển
3. Xác nhận trạng thái "Đã Kết nối" xuất hiện
4. Kiểm tra thời gian dấu thời gian last_tested_at

**Bước 6: Liên kết đến phương thức vận chuyển**
1. Tạo hoặc chỉnh sửa phương thức vận chuyển (Cài đặt > Giỏ hàng > Phương thức Vận chuyển)
2. Đặt method_type = "Thời gian thực"
3. Chọn tài khoản cung cấp từ danh sách thả xuống
4. Lưu phương thức

---

## Giám sát Tình trạng Kết nối

Các tài khoản cung cấp theo dõi tình trạng kết nối:

### Giá trị Tình trạng

**Không xác định** (xám): Chưa được kiểm tra hoặc chưa kết nối

**Đã kết nối** (xanh): Gọi API lần cuối thành công, thông tin xác thực hợp lệ

**Lỗi** (đỏ): Gọi API lần cuối thất bại, thông tin xác thực có thể không hợp lệ

### Lần kiểm tra cuối cùng

- **Thời gian dấu**: Khi kết nối được xác minh lần cuối
- **Cập nhật tự động**: Mỗi lần sử dụng nhà cung cấp (lấy giá, mua nhãn)
- **Kiểm tra thủ công**: Nhấp vào nút "Kiểm tra Kết nối" bất kỳ lúc nào

### Khắc phục kết nối thất bại

**Nguyên nhân phổ biến**:
- Thông tin xác thực API không đúng (nhập sai, sao chép kèm khoảng trắng)
- Khóa API của hãng vận chuyển đã hết hạn hoặc bị hủy bỏ
- Chế độ kiểm tra được bật nhưng sử dụng thông tin xác thực sản xuất (hoặc ngược lại)
- Địa chỉ IP không được liệt kê trắng với hãng vận chuyển
- Hãng vận chuyển đang có sự cố API

**Bước khắc phục**:
1. Xác nhận thông tin xác thực khớp hoàn toàn với bảng điều khiển của hãng vận chuyển
2. Kiểm tra cài đặt chế độ kiểm tra khớp với loại thông tin xác thực
3. Xem trang trạng thái API của hãng vận chuyển để kiểm tra sự cố
4. Liên hệ hỗ trợ của hãng vận chuyển để xác minh tài khoản

---

## Quy trình Tìm kiếm Giá vận chuyển

Cách giá vận chuyển theo thời gian thực hoạt động tại thời điểm thanh toán:

**1. Khách hàng nhập địa chỉ**
- Địa chỉ vận chuyển được nhập
- Tổng trọng lượng + kích thước được tính toán từ giỏ hàng

**2. Hệ thống Chuẩn bị Yêu cầu Giá**
- Lấy thông tin xác thực tài khoản cung cấp (giải mã)
- Tính toán kích thước gói hàng từ các mục trong giỏ hàng (sử dụng gói hàng vận chuyển nếu được định nghĩa)
- Chuẩn bị yêu cầu API với điểm xuất phát, điểm đến, gói hàng

**3. Gọi API của Nhà cung cấp**
- Yêu cầu được gửi đến API của hãng vận chuyển với thông tin xác thực
- Hãng vận chuyển tính toán giá dựa trên khu vực, trọng lượng, kích thước
- Phản hồi bao gồm các tùy chọn dịch vụ (Ground, Express, v.v.)

**4. Giá được hiển thị**
- Hệ thống phân tích phản hồi từ hãng vận chuyển
- Chuẩn hóa thành định dạng tiêu chuẩn
- Áp dụng markup (nếu được cấu hình)
- Giá được hiển thị cho khách hàng tại thời điểm thanh toán

**5. Khách hàng chọn dịch vụ**
- Khách hàng chọn tùy chọn ưa thích
- Giá được chọn lưu vào đơn hàng

**Ví dụ luồng API**:
```
Yêu cầu gửi đến API FedEx:
{
  "origin": {"postal_code": "90210", "country": "US"},
  "destination": {"postal_code": "10001", "country": "US"},
  "parcels": [{
    "weight": 2500,  // gram
    "dimensions": {"length": 30, "width": 20, "height": 15}  // cm
  }]
}

Phản hồi FedEx:
[
  {"service": "FEDEX_GROUND", "rate": 12.50, "delivery_days": 5},
  {"service": "FEDEX_EXPRESS", "rate": 28.75, "delivery_days": 2}
]
```

---

## Mua nhãn (Tùy chọn)

Nếu nhà cung cấp hỗ trợ tạo nhãn:

**Quy trình**:
1. Khách hàng hoàn tất đơn hàng
2. Người bán tạo vận chuyển (Đơn hàng > Chi tiết đơn hàng > Tạo Vận chuyển)
3. Chọn tài khoản cung cấp + dịch vụ
4. Hệ thống gọi API tạo nhãn của nhà cung cấp
5. Tạo PDF nhãn và đính kèm vào vận chuyển
6. Số theo dõi được điền tự động
7. Nhãn sẵn sàng để in

**Lợi ích**:
- Không cần đăng nhập vào trang web của hãng vận chuyển thủ công
- Theo dõi được đồng bộ tự động
- Tự động tạo các biểu mẫu hải quan (quốc tế)
- Có thể tạo nhãn theo lô

---

## Markup Giá vận chuyển

Thêm markup của người bán vào giá vận chuyển của hãng:

**Cấu hình** (trong phương thức vận chuyển, không phải tài khoản cung cấp):
- **Loại markup**: Phần trăm hoặc Cố định
- **Số lượng markup**: Ví dụ, 15% hoặc $2.50

**Ví dụ**:
```
Giá vận chuyển của hãng: $12.50
Markup: 15%
Khách hàng phải trả: $14.38

HOẶC

Giá vận chuyển của hãng: $12.50
Markup: $2.50 (cố định)
Khách hàng phải trả: $15.00
```

**Các trường hợp sử dụng**:
- Bù đắp chi phí đóng gói/xử lý
- Thêm biên lợi nhuận cho vận chuyển
- Bù đắp phí thẻ tín dụng trên vận chuyển

---

## Nhiều Tài khoản Cung cấp Vận chuyển

Bạn có thể tạo nhiều tài khoản cho cùng một nhà cung cấp:

**Các trường hợp sử dụng**:
1. **Kiểm tra vs Sản xuất**
   - Tài khoản kiểm tra: Thông tin xác thực sandbox của hãng vận chuyển
   - Tài khoản sản xuất: Thông tin xác thực trực tiếp

2. **Nhiều kho hàng**
   - Tài khoản kho A: Điểm xuất phát = Los Angeles
   - Tài khoản kho B: Điểm xuất phát = New York

3. **Các mức giá đã đàm phán khác nhau**
   - Tài khoản A: Giá tiêu chuẩn
   - Tài khoản B: Giá giảm theo khối lượng

**Mỗi tài khoản có thể liên kết với các phương thức vận chuyển khác nhau** để cấu hình linh hoạt.

---

## Một số mẹo

- **Kiểm tra trong sandbox trước** - Sử dụng thông tin xác thực kiểm tra của hãng vận chuyển trước khi đưa vào sản xuất
- **Giám sát tình trạng kết nối** - Kiểm tra bảng điều khiển thường xuyên để xem trạng thái lỗi
- **Định nghĩa gói hàng vận chuyển** - Kích thước chính xác cải thiện báo giá giá vận chuyển
- **Sử dụng giá đã đàm phán** - Bật nếu bạn có giảm giá theo khối lượng với hãng vận chuyển
- **Đặt điểm xuất phát thực tế** - Sử dụng địa chỉ thực tế gửi từ để có khu vực chính xác
- **Giữ thông tin xác thực an toàn** - Không bao giờ chia sẻ khóa API, thay đổi định kỳ
- **Có phương pháp dự phòng** - Giữ phương pháp giá cố định hoạt động nếu API của hãng vận chuyển không hoạt động
- **Giám sát giới hạn API của hãng vận chuyển** - Một số hãng vận chuyển giới hạn số lần gọi API mỗi ngày
- **Cập nhật thông tin xác thực kịp thời** - Khi hãng vận chuyển thay đổi khóa, cập nhật ngay lập tức
- **Sử dụng tên mô tả** - "FedEx Kho Los Angeles" tốt hơn "FedEx 1"