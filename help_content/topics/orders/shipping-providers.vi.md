---
title: Các nhà cung cấp vận chuyển
---

Các nhà cung cấp vận chuyển kết nối cửa hàng của bạn với các API của hãng vận chuyển để tính toán giá vận chuyển theo thời gian thực, tạo nhãn vận chuyển và theo dõi kiện hàng. Spwig hỗ trợ các hãng vận chuyển lớn trên toàn thế giới và cũng cho phép bạn thiết lập bảng giá vận chuyển thủ công cho các hãng không có tích hợp API.

![Các nhà cung cấp vận chuyển](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Các nhà cung cấp có sẵn

| Nhà cung cấp | Khu vực | Tính năng chính |
|---------|---------|-------------|
| **FedEx** | Toàn cầu | Giá vận chuyển theo thời gian thực, in nhãn vận chuyển, theo dõi, đa gói hàng |
| **UPS** | Toàn cầu | Giá vận chuyển theo thời gian thực, in nhãn vận chuyển, theo dõi, xác minh địa chỉ |
| **USPS** | Hoa Kỳ | Giá vận chuyển trong nước và quốc tế, theo dõi |
| **NinjaVan** | Đông Nam Á | Giao hàng cuối dặm, hỗ trợ thanh toán khi nhận hàng |
| **Canada Post** | Canada | Trong nước và quốc tế, giá vận chuyển bưu kiện và thư |
| **Australia Post** | Úc | Trong nước và quốc tế, giá vận chuyển bưu kiện và nhanh |

## Kết nối nhà cung cấp

Truy cập **Cài đặt > Các nhà cung cấp vận chuyển** và nhấn **Kết nối nhà cung cấp** để khởi động trình hướng dẫn thiết lập.

### Bước 1: Chọn nhà cung cấp

Chọn từ các nhà cung cấp vận chuyển có sẵn. Mỗi thẻ hiển thị khu vực và tính năng được hỗ trợ của nhà cung cấp.

### Bước 2: Hướng dẫn thiết lập

Xem hướng dẫn thiết lập riêng cho nhà cung cấp:
- Cách tạo tài khoản phát triển/kinh doanh với nhà cung cấp
- Vị trí tìm thấy thông tin xác thực API của bạn
- Cài đặt tài khoản cần thiết (ví dụ: số người gửi, số máy đo)

### Bước 3: Nhập thông tin xác thực

Nhập thông tin xác thực API cho tài khoản nhà cung cấp của bạn. Các trường cần thiết sẽ thay đổi tùy theo nhà cung cấp:

- **API Key / Secret** — Thông tin xác thực
- **Số tài khoản** — Số tài khoản nhà cung cấp hoặc số người gửi của bạn
- **Số máy đo** — Yêu cầu bởi một số nhà cung cấp (ví dụ: FedEx)
- **Chế độ Sandbox** — Kích hoạt để kiểm tra với API sandbox của nhà cung cấp trước khi triển khai

### Bước 4: Kiểm tra kết nối

Nhấn **Kiểm tra kết nối** để xác minh thông tin xác thực của bạn. Trình hướng dẫn xác nhận:
- Xác thực API thành công
- Quyền tài khoản hợp lệ
- Truy vấn giá vận chuyển trả về kết quả mong đợi

### Bước 5: Cấu hình và lưu

Hoàn tất thiết lập:
- **Hoạt động** — Bật hoặc tắt nhà cung cấp
- **Tên hiển thị** — Tên hiển thị cho khách hàng tại bước thanh toán
- **Địa chỉ nguồn** — Địa chỉ kho hàng hoặc địa chỉ giao hàng để tính toán giá vận chuyển

## Khu vực vận chuyển

Các khu vực vận chuyển xác định các khu vực địa lý cho tính toán giá vận chuyển. Truy cập **Cài đặt > Khu vực vận chuyển** để quản lý chúng.

### Tạo khu vực

1. Nhấn **+ Thêm khu vực**
2. Đặt tên khu vực (ví dụ: "Trong nước", "Âu", "Đại dương châu Á")
3. Xác định phạm vi khu vực bằng một hoặc nhiều cách sau:
   - **Quốc gia** — Chọn các quốc gia cụ thể
   - **Tỉnh/Thành phố** — Thu hẹp đến các khu vực cụ thể trong một quốc gia
   - **Mẫu mã bưu điện** — Phù hợp với mã bưu điện/ZIP bằng mẫu (ví dụ: "90*" cho khu vực Los Angeles)
4. Thiết lập **Ưu tiên** — Khi các khu vực chồng chéo, khu vực có ưu tiên cao nhất sẽ được sử dụng

### Phù hợp khu vực

Khi khách hàng nhập địa chỉ vận chuyển tại bước thanh toán, hệ thống:
1. Kiểm tra mẫu mã bưu điện trước (chính xác nhất)
2. Sau đó là phù hợp tỉnh/thành phố
3. Sau đó là phù hợp quốc gia
4. Sử dụng khu vực phù hợp nhất có ưu tiên cao nhất

## Quy tắc vận chuyển

Các quy tắc vận chuyển áp dụng các điều chỉnh điều kiện đến giá vận chuyển. Truy cập **Cài đặt > Quy tắc vận chuyển** để cấu hình chúng.

### Loại quy tắc

| Loại quy tắc | Mô tả |
|-----------|-------------|
| **Giảm %** | Giảm giá vận chuyển theo tỷ lệ phần trăm |
| **Giảm cố định** | Giảm giá vận chuyển theo một khoản cố định |
| **Đặt giá** | Thay thế giá vận chuyển bằng một khoản cụ thể |
| **Miễn phí vận chuyển** | Đặt giá vận chuyển thành 0 |
| **Thu phụ phí %** | Thêm một tỷ lệ phụ phí vào giá vận chuyển |
| **Thu phụ phí cố định** | Thêm một khoản phụ phí cố định vào giá vận chuyển |

### Điều kiện

Mỗi quy tắc có thể có một hoặc nhiều điều kiện cần được đáp ứng:

| Điều kiện | Ví dụ |
|-----------|---------|
| **Giá trị giỏ hàng** | Miễn phí vận chuyển cho đơn hàng trên 100 đô la |
| **Tổng trọng lượng** | Thu phụ phí cho đơn hàng trên 30 kg |
| **Số lượng mặt hàng** | Giảm giá cho đơn hàng có 5 mặt hàng trở lên |
| **Khu vực vận chuyển** | Áp dụng quy tắc chỉ cho các đơn hàng nội địa |
| **Phương thức vận chuyển** | Áp dụng cho các phương thức cụ thể của nhà cung cấp |
| **Sản phẩm** | Giá đặc biệt cho các sản phẩm cụ thể |
| **Nhóm khách hàng** | Khách hàng VIP được miễn phí vận chuyển |
| **Khoảng thời gian** | Khuyến mãi vận chuyển dịp lễ |

### Ưu tiên quy tắc

- Các quy tắc được đánh giá theo thứ tự ưu tiên (số nhỏ nhất trước)
- **Ngừng kiểm tra quy tắc tiếp theo** — Khi được kích hoạt, nếu quy tắc này phù hợp, không quy tắc nào khác sẽ được kiểm tra
- Nhiều quy tắc có thể chồng chéo (ví dụ: quy tắc giảm 10% cộng với quy tắc miễn phí vận chuyển theo ngưỡng giá trị giỏ hàng)

## Bảng giá vận chuyển

Bảng giá vận chuyển cung cấp giá theo cấp bậc dựa trên thuộc tính đơn hàng. Truy cập **Cài đặt > Bảng giá vận chuyển** để cấu hình chúng.

### Loại bảng

Tạo các cấp giá dựa trên:
- **Trọng lượng** — Giá theo cấp bậc trọng lượng tổng đơn hàng (ví dụ: 0-1 kg = 5 đô la, 1-5 kg = 10 đô la)
- **Giá trị đơn hàng** — Giá theo cấp bậc tổng giá trị giỏ hàng
- **Số lượng** — Giá theo cấp bậc số lượng mặt hàng

### Tạo bảng giá vận chuyển

1. Nhấn **+ Thêm bảng giá vận chuyển**
2. Đặt tên bảng và chọn loại cấp bậc
3. Thêm các cấp bậc với khoảng giá trị tối thiểu/tối đa và giá
4. Gán bảng giá vận chuyển đến một khu vực vận chuyển

Bảng giá vận chuyển rất hữu ích khi bạn không sử dụng giá vận chuyển từ API nhà cung cấp và muốn xác định cấu trúc giá của riêng bạn.

## Gói hàng vận chuyển

Định nghĩa các kích thước gói hàng tiêu chuẩn để tính toán giá vận chuyển chính xác. Truy cập **Cài đặt > Gói hàng vận chuyển**.

Đối với mỗi loại gói hàng, hãy thiết lập:
- **Tên** — Mô tả (ví dụ: "Hộp nhỏ", "Gói vận chuyển lớn")
- **Kích thước** — Chiều dài, chiều rộng, chiều cao
- **Trọng lượng tối đa** — Trọng lượng tối đa mà gói hàng có thể chứa
- **Mặc định** — Sử dụng gói này khi không có gói hàng cụ thể được gán

Các nhà cung cấp sử dụng kích thước gói hàng để tính toán trọng lượng theo kích thước, điều này có thể ảnh hưởng đến giá vận chuyển.

## Nhà cung cấp thủ công (Mẫu nhà cung cấp)

Đối với các nhà cung cấp không có tích hợp API, tạo các mẫu nhà cung cấp thủ công:

1. Truy cập **Cài đặt > Mẫu nhà cung cấp**
2. Nhấn **+ Thêm mẫu**
3. Cấu hình:
   - **Tên nhà cung cấp** — Tên hiển thị tại bước thanh toán
   - **Mẫu URL theo dõi** — Mẫu URL có chỗ giữ {tracking_number} (ví dụ: `https://track.carrier.com/?id={tracking_number}`)
   - **Thời gian giao hàng dự kiến** — Khoảng thời gian giao hàng hiển thị cho khách hàng
4. Gắn với bảng giá vận chuyển để định giá

Các nhà cung cấp thủ công cung cấp liên kết theo dõi và ước tính thời gian giao hàng mà không cần tích hợp API theo thời gian thực.

## Vận chuyển đa kho hàng

Nếu bạn có nhiều kho hàng, vận chuyển có thể được tính toán từ các nguồn khác nhau:

- **Kho hàng theo quốc gia** — Gán kho hàng cho các quốc gia cụ thể để rút ngắn khoảng cách vận chuyển
- **Chuỗi dự phòng** — Định nghĩa kho hàng nào sẽ giao hàng khi kho hàng chính không có sẵn
- **Phân bổ theo từng sản phẩm** — Một số sản phẩm chỉ có thể giao hàng từ kho hàng cụ thể

Hệ thống tự động chọn kho hàng tốt nhất dựa trên vị trí của khách hàng và sự có sẵn của sản phẩm.

## Một số mẹo

- Kết nối API nhà cung cấp để có **giá vận chuyển theo thời gian thực** khi có thể — chúng chính xác hơn các bảng giá cố định và điều chỉnh theo trọng lượng, kích thước và điểm đến.
- Tạo khu vực vận chuyển **"Các nước còn lại"** như một khu vực dự phòng cho các quốc gia không được bao phủ bởi các khu vực cụ thể.
- Sử dụng loại quy tắc **Miễn phí vận chuyển** với điều kiện giá trị giỏ hàng như một động lực bán hàng (ví dụ: "Miễn phí vận chuyển cho đơn hàng trên 75 đô la").
- Kiểm tra tính toán giá vận chuyển với các địa chỉ và nội dung giỏ hàng khác nhau trước khi triển khai.
- Thiết lập **Mẫu nhà cung cấp** với mẫu URL theo dõi cho bất kỳ nhà cung cấp địa phương nào không có tích hợp API — khách hàng vẫn nhận được liên kết theo dõi.
- Sử dụng **Gói hàng vận chuyển** để nhận được giá theo trọng lượng kích thước chính xác từ các nhà cung cấp như FedEx và UPS.