---
title: Các nhà cung cấp vận chuyển
---

Các nhà cung cấp vận chuyển kết nối cửa hàng của bạn với các API của hãng vận chuyển để tính cước vận chuyển theo thời gian thực, tạo nhãn vận chuyển và theo dõi kiện hàng. Spwig hỗ trợ các hãng vận chuyển lớn trên toàn thế giới và cũng cho phép bạn thiết lập bảng giá thủ công cho các hãng không có tích hợp API.

![Các nhà cung cấp vận chuyển](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Các nhà cung cấp có sẵn

| Nhà cung cấp | Khu vực | Tính năng chính |
|---------|---------|-------------|
| **FedEx** | Toàn cầu | Cước vận chuyển theo thời gian thực, in nhãn, theo dõi, nhiều kiện hàng |
| **UPS** | Toàn cầu | Cước vận chuyển theo thời gian thực, in nhãn, theo dõi, xác minh địa chỉ |
| **USPS** | Hoa Kỳ | Cước nội địa và quốc tế, theo dõi |
| **NinjaVan** | Đông Nam Á | Giao hàng cuối dặm, hỗ trợ thanh toán khi nhận hàng |
| **Canada Post** | Canada | Nội địa và quốc tế, cước kiện hàng và thư |
| **Australia Post** | Úc | Nội địa và quốc tế, cước kiện hàng và nhanh chóng |

## Kết nối nhà cung cấp

Truy cập **Cài đặt > Nhà cung cấp vận chuyển** và nhấn **Kết nối nhà cung cấp** để khởi động trình hướng dẫn thiết lập.

### Bước 1: Chọn nhà cung cấp

Chọn từ các nhà cung cấp vận chuyển có sẵn. Mỗi thẻ hiển thị khu vực và tính năng được hỗ trợ bởi nhà cung cấp.

### Bước 2: Hướng dẫn thiết lập

Xem hướng dẫn thiết lập riêng cho từng nhà cung cấp:
- Cách tạo tài khoản phát triển/kinh doanh với nhà cung cấp
- Nơi nào để tìm thông tin xác thực API của bạn
- Cài đặt tài khoản cần thiết (ví dụ: số người gửi, số máy đo)

### Bước 3: Nhập thông tin xác thực

Nhập thông tin xác thực API cho tài khoản nhà cung cấp của bạn. Các trường bắt buộc thay đổi tùy theo nhà cung cấp:

- **Khóa API / Bí mật** — Thông tin xác thực
- **Số tài khoản** — Số tài khoản hoặc số người gửi của bạn
- **Số máy đo** — Được yêu cầu bởi một số nhà cung cấp (ví dụ: FedEx)
- **Chế độ Sandbox** — Bật để kiểm tra với API Sandbox của nhà cung cấp trước khi triển khai

### Bước 4: Kiểm tra kết nối

Nhấn **Kiểm tra kết nối** để xác minh thông tin xác thực của bạn. Trình hướng dẫn xác nhận:
- Xác thực API thành công
- Quyền tài khoản hợp lệ
- Truy vấn cước trả về kết quả mong đợi

### Bước 5: Cấu hình và lưu

Hoàn tất cài đặt:
- **Kích hoạt** — Bật hoặc tắt nhà cung cấp
- **Tên hiển thị** — Tên hiển thị cho khách hàng tại bước thanh toán
- **Địa chỉ nguồn** — Địa chỉ kho hoặc địa chỉ xử lý hàng hóa để tính cước

## Khu vực vận chuyển

Khu vực vận chuyển xác định các khu vực địa lý cho tính cước. Truy cập **Cài đặt > Khu vực vận chuyển** để quản lý chúng.

### Tạo khu vực

1. Nhấn **+ Thêm khu vực**
2. Đặt tên cho khu vực (ví dụ: "Nội địa", "Châu Âu", "Châu Á - Thái Bình Dương")
3. Định nghĩa phạm vi khu vực bằng một hoặc nhiều mục sau:
   - **Quốc gia** — Chọn các quốc gia cụ thể
   - **Tỉnh/Thành phố** — Thu hẹp xuống các khu vực cụ thể trong một quốc gia
   - **Mẫu mã bưu điện** — Phù hợp với mã bưu điện/ZIP bằng mẫu (ví dụ: "90*" cho khu vực Los Angeles)
4. Đặt **Ưu tiên** — Khi các khu vực chồng lấn, khu vực có ưu tiên cao nhất sẽ được sử dụng

### Phù hợp khu vực

Khi khách hàng nhập địa chỉ vận chuyển của họ tại bước thanh toán, hệ thống:
1. Kiểm tra mẫu mã bưu điện trước (chính xác nhất)
2. Sau đó là phù hợp tỉnh/thành phố
3. Sau đó là phù hợp quốc gia
4. Sử dụng khu vực phù hợp nhất theo ưu tiên cao nhất

## Khuyến mãi vận chuyển

Khuyến mãi vận chuyển áp dụng các điều chỉnh điều kiện lên cước vận chuyển. Truy cập **Cài đặt > Khuyến mãi vận chuyển** để cấu hình chúng.

### Loại khuyến mãi

| Loại khuyến mãi | Mô tả |
|-----------|-------------|
| **Giảm %** | Giảm cước vận chuyển theo tỷ lệ phần trăm |
| **Giảm cố định** | Giảm cước vận chuyển theo một khoản cố định |
| **Ghi đè chi phí** | Ghi đè cước bằng một khoản cụ thể |
| **Miễn phí vận chuyển** | Đặt chi phí vận chuyển thành 0 |
| **Thu phụ phí %** | Thêm một tỷ lệ phụ phí vào cước |
| **Thu phụ phí cố định** | Thêm một khoản phụ phí cố định vào cước |

### Điều kiện

Mỗi khuyến mãi có thể có một hoặc nhiều điều kiện cần được đáp ứng:

| Điều kiện | Ví dụ |
|-----------|---------|
| **Giá trị giỏ hàng** | Miễn phí vận chuyển cho đơn hàng trên 100 đô la |
| **Tổng trọng lượng** | Phí phụ thu cho đơn hàng trên 30 kg |
| **Số lượng mặt hàng** | Giảm giá cho đơn hàng có 5 mặt hàng trở lên |
| **Khu vực vận chuyển** | Áp dụng khuyến mãi chỉ cho các đơn hàng trong nước |
| **Phương thức vận chuyển** | Áp dụng cho các phương thức vận chuyển cụ thể |
| **Sản phẩm** | Giá đặc biệt cho các sản phẩm cụ thể |
| **Nhóm khách hàng** | Khách hàng VIP được miễn phí vận chuyển |
| **Khoảng thời gian** | Khuyến mãi vận chuyển dịp lễ |

### Ưu tiên khuyến mãi

- Các khuyến mãi được đánh giá theo thứ tự ưu tiên (số nhỏ nhất trước)
- **Ngừng kiểm tra khuyến mãi tiếp theo** — Khi được bật, nếu khuyến mãi này khớp, sẽ không kiểm tra các khuyến mãi khác nữa
- Nhiều khuyến mãi có thể chồng chéo (ví dụ: khuyến mãi giảm 10% và khuyến mãi miễn phí vận chuyển khi đạt giá trị đơn hàng nhất định)

## Bảng giá

Bảng giá cung cấp định giá theo cấp bậc dựa trên các thuộc tính đơn hàng. Truy cập **Cài đặt > Bảng giá vận chuyển** để cấu hình chúng.

### Loại bảng

Tạo các cấp giá dựa trên:
- **Trọng lượng** — Cấp giá theo trọng lượng tổng đơn hàng (ví dụ: 0-1 kg = 5 đô la, 1-5 kg = 10 đô la)
- **Giá trị đơn hàng** — Cấp giá theo tổng giá trị giỏ hàng
- **Số lượng** — Cấp giá theo số lượng mặt hàng

### Tạo bảng giá

1. Nhấp **+ Thêm bảng giá**
2. Đặt tên bảng và chọn loại cấp bậc
3. Thêm các cấp bậc với khoảng giá trị tối thiểu/tối đa và giá
4. Gán bảng giá cho một khu vực vận chuyển

Bảng giá rất hữu ích khi bạn không sử dụng giá từ API của nhà vận chuyển và muốn tự định nghĩa cấu trúc giá của mình.

## Gói vận chuyển

Định nghĩa các kích thước gói tiêu chuẩn để tính toán giá vận chuyển chính xác. Truy cập **Cài đặt > Gói vận chuyển**.

Đối với mỗi loại gói, hãy thiết lập:
- **Tên** — Mô tả (ví dụ: "Hộp nhỏ", "Gói lớn giá cố định")
- **Kích thước** — Chiều dài, chiều rộng, chiều cao
- **Trọng lượng tối đa** — Trọng lượng tối đa mà gói có thể chứa
- **Mặc định** — Sử dụng gói này khi không có gói đóng gói cụ thể được chỉ định

Các nhà vận chuyển sử dụng kích thước gói để tính trọng lượng theo kích thước, điều này có thể ảnh hưởng đến giá vận chuyển.

## Nhà vận chuyển thủ công (Cài đặt nhà vận chuyển)

Đối với các nhà vận chuyển không có tích hợp API, hãy tạo các cài đặt nhà vận chuyển thủ công:

1. Truy cập **Cài đặt > Cài đặt nhà vận chuyển**
2. Nhấp **+ Thêm cài đặt**
3. Cấu hình:
   - **Tên nhà vận chuyển** — Tên hiển thị tại thanh toán
   - **Mẫu URL theo dõi** — Mẫu URL với chỗ giữ {tracking_number} (ví dụ: `https://track.carrier.com/?id={tracking_number}`)
   - **Thời gian giao hàng ước tính** — Khoảng thời gian giao hàng hiển thị cho khách hàng
4. Gắn với bảng giá để xác định giá

Các nhà vận chuyển thủ công cung cấp liên kết theo dõi và ước tính thời gian giao hàng mà không cần tích hợp API trực tiếp.

## Vận chuyển đa kho hàng

Nếu bạn có nhiều kho hàng, vận chuyển có thể được tính toán từ các nguồn khác nhau:

- **Kho hàng theo quốc gia** — Gán kho hàng cho các quốc gia cụ thể để giảm khoảng cách vận chuyển
- **Chuỗi dự phòng** — Định nghĩa kho hàng nào sẽ giao hàng khi kho hàng chính không có hàng
- **Gán theo sản phẩm** — Một số sản phẩm chỉ có thể giao từ kho hàng cụ thể

Hệ thống tự động chọn kho hàng tốt nhất dựa trên vị trí khách hàng và tình trạng hàng tồn kho.

## Một số mẹo

- Kết nối API của nhà vận chuyển để có **giá vận chuyển trực tiếp** khi có thể — chúng chính xác hơn các bảng giá cố định và điều chỉnh theo trọng lượng, kích thước và điểm đến.
- Tạo **khu vực vận chuyển "Các nước khác"** làm khu vực dự phòng cho các quốc gia không được bao phủ bởi các khu vực cụ thể.
- Sử dụng loại khuyến mãi **Miễn phí vận chuyển** với điều kiện giá trị giỏ hàng như một động lực bán hàng (ví dụ: "Miễn phí vận chuyển cho đơn hàng trên 75 đô la").
- Kiểm tra tính toán giá vận chuyển với các địa chỉ và nội dung giỏ hàng khác nhau trước khi đưa vào vận hành.
- Thiết lập **Cài đặt nhà vận chuyển** với mẫu URL theo dõi cho bất kỳ nhà vận chuyển địa phương nào không có tích hợp API — khách hàng vẫn có thể theo dõi đơn hàng.
- Sử dụng **Gói vận chuyển** để nhận giá trọng lượng theo kích thước chính xác từ các nhà vận chuyển như FedEx và UPS.