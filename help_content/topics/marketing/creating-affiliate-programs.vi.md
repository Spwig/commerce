---
title: Tạo chương trình đại lý
---

Các chương trình đại lý xác định cách các đối tác của bạn kiếm hoa hồng khi họ giới thiệu khách hàng đến cửa hàng của bạn. Mỗi chương trình có cấu trúc hoa hồng riêng, quy tắc theo dõi và ngưỡng thanh toán. Bạn có thể tạo nhiều chương trình để phục vụ các phân khúc đại lý khác nhau - như các nhà ảnh hưởng, nhà sáng tạo nội dung hoặc đối tác giới thiệu theo khối lượng lớn.

![Danh sách chương trình](/static/core/admin/img/help/creating-affiliate-programs/programs-list.webp)

## Các thành phần của chương trình

Mỗi chương trình đại lý bao gồm:

- **Tên và Mô tả** — Nhận diện chương trình và giải thích cho các đại lý
- **Cấu trúc hoa hồng** — Số tiền đại lý kiếm được cho mỗi đơn hàng (tỷ lệ phần trăm hoặc số tiền cố định)
- **Thời gian sống của cookie** — Thời gian theo dõi giới thiệu kéo dài sau khi nhấp chuột (1-365 ngày)
- **Tự động duyệt** — Liệu các đại lý mới có tham gia tự động hay cần xem xét thủ công
- **Ngưỡng thanh toán tối thiểu** — Số tiền đại lý phải kiếm được trước khi yêu cầu thanh toán
- **Trạng thái** — Hoạt động, tạm dừng hoặc lưu trữ

## Loại hoa hồng

Chọn giữa hai mô hình hoa hồng khi tạo chương trình của bạn:

| Loại | Cách hoạt động | Khi sử dụng | Ví dụ tính toán |
|------|-------------|-------------|---------------------|
| **Tỷ lệ phần trăm** | Đại lý kiếm được tỷ lệ phần trăm của tổng số đơn hàng | Phần thưởng có thể mở rộng tăng theo giá trị đơn hàng | 10% của đơn hàng $150 = $15 hoa hồng |
| **Số tiền cố định** | Đại lý kiếm được một khoản cố định cho mỗi đơn hàng | Chi phí dự đoán được; phù hợp nhất với các sản phẩm khối lượng lớn, biên lợi nhuận thấp | $25 cho mỗi đơn hàng bất kể giá trị đơn hàng |

**Các khoản hoa hồng theo tỷ lệ phần trăm** mở rộng tự nhiên — đại lý kiếm được nhiều hơn khi họ giới thiệu các khách hàng có giá trị cao. Điều này phù hợp với mục tiêu của bạn và là mô hình phổ biến nhất (thường là 5–15%).

**Các khoản hoa hồng cố định** hoạt động tốt cho các dịch vụ, đăng ký hoặc chương trình giới thiệu theo khối lượng lớn nơi bạn muốn chi phí mỗi đơn hàng có thể dự đoán được. Chúng dễ hiểu và lập ngân sách, nhưng có thể không đủ để bù đắp cho các đại lý mang lại các đơn hàng lớn.

## Tạo một chương trình

Chuyển đến **Marketing > Chương trình đại lý** và nhấp **+ Thêm chương trình**.

### Thiết lập từng bước

1. **Tên chương trình**
   Nhập tên mô tả có thể nhìn thấy bởi các đại lý (ví dụ: "Chương trình Đối tác" hoặc "Cấp bậc Nhà ảnh hưởng").

2. **Slug**
   Một định danh thân thiện với URL được tạo tự động từ tên. Được sử dụng trong URL và tham chiếu nội bộ. Bạn có thể tùy chỉnh nó nếu cần.

3. **Mô tả**
   Văn bản tùy chọn giải thích lợi ích và điều khoản của chương trình. Các đại lý sẽ thấy điều này khi xem xét các chương trình họ có thể tham gia.

4. **Loại hoa hồng**
   Chọn **Tỷ lệ phần trăm** hoặc **Số tiền cố định**.

5. **Giá trị hoa hồng**
   - Đối với tỷ lệ phần trăm: Nhập giá trị từ 0 đến 100 (ví dụ: `10` cho 10%)
   - Đối với số tiền cố định: Nhập số tiền theo đô la cho mỗi đơn hàng (ví dụ: `25.00` cho $25)

6. **Thời gian sống của cookie (ngày)**
   Số ngày cookie theo dõi kéo dài (1–365). Xem phần dưới đây để biết hướng dẫn.

7. **Tự động duyệt đại lý**
   - **Đánh dấu** — Các đại lý mới tham gia tự động
   - **Không đánh dấu** — Bạn xem xét và duyệt từng ứng dụng thủ công

8. **Ngưỡng thanh toán tối thiểu**
   Số dư tối thiểu mà đại lý phải tích lũy trước khi yêu cầu thanh toán (ví dụ: `50.00` cho $50).

9. **Trạng thái**
   Thiết lập thành **Hoạt động** để chấp nhận các đại lý mới và theo dõi các giới thiệu.

10. **Lưu** chương trình.

## Giải thích thời gian sống của cookie

Thời gian sống của cookie xác định thời gian Spwig nhớ rằng một khách hàng đã nhấp vào liên kết giới thiệu của đại lý.

### Cách hoạt động

1. Một khách hàng nhấp vào liên kết của đại lý
2. Spwig thiết lập cookie theo dõi trong trình duyệt của khách hàng
3. Nếu khách hàng hoàn thành một đơn hàng **trong thời gian sống của cookie**, đơn hàng sẽ được ghi công cho đại lý
4. Nếu cookie hết hạn trước khi mua hàng, đại lý sẽ không nhận được hoa hồng

### Chọn thời gian

| Thời gian | Trường hợp sử dụng | Tình huống điển hình |
|----------|----------|------------------|
| **1–7 ngày** | Mua sắm tức thời, khuyến mãi flash | Hàng hóa tiêu dùng nhanh, ưu đãi giới hạn |
| **30 ngày** | Thương mại điện tử tiêu chuẩn | Bán lẻ trực tuyến thông thường, khuyến nghị mặc định |
| **60–90 ngày** | Mua sắm được cân nhắc | Các mặt hàng có giá cao, B2B, dịch vụ |
| **180+ ngày** | Chu kỳ bán hàng dài | Phần mềm doanh nghiệp, đăng ký, hàng xa xỉ |

**Tiêu chuẩn ngành là 30 ngày.** Điều này cân bằng giữa việc ghi công công bằng cho đại lý và giới hạn theo dõi thực tế. Thời gian sống ngắn hơn có lợi cho khách hàng chuyển đổi nhanh; thời gian sống dài hơn cho phép khách hàng thời gian nghiên cứu và quay lại hoàn tất mua hàng của họ.

### Ghi chú kỹ thuật

Thời gian sống của cookie chỉ ảnh hưởng đến **ghi công**. Các khoản hoa hồng đã được phê duyệt vẫn hợp lệ vĩnh viễn — thời gian sống của cookie chỉ xác định liệu đơn hàng có được ghi công cho đại lý từ đầu hay không.

## Cài đặt tự động duyệt

Cài đặt tự động duyệt kiểm soát liệu các ứng dụng đại lý mới có yêu cầu xem xét thủ công hay không.

### Khi bật tự động duyệt

- **Chương trình công khai** — Bạn muốn mở rộng cơ sở đại lý nhanh chóng mà không có điểm nghẽn
- **Sản phẩm rủi ro thấp** — Rủi ro gian lận hoặc thương hiệu là tối thiểu
- **Chương trình khối lượng cao** — Bạn kỳ vọng có nhiều ứng dụng và không thể xem xét từng cái một

### Khi yêu cầu xem xét thủ công

- **Chương trình mời** — Bạn chỉ chấp nhận các đối tác đã được kiểm tra trước
- **Chương trình cao cấp** — Tỷ lệ hoa hồng cao hoặc lợi ích độc quyền
- **Sản phẩm nhạy cảm thương hiệu** — Bạn cần đảm bảo đại lý phù hợp với giá trị thương hiệu của bạn
- **Ngăn chặn gian lận** — Bạn muốn sàng lọc các tài khoản đáng ngờ

### Xét về bảo mật

Xem xét thủ công các đại lý giúp ngăn chặn:
- Các chương trình tự giới thiệu (đại lý tạo các tài khoản giả để kiếm hoa hồng)
- Vi phạm thương hiệu (đại lý đấu giá các từ khóa thương hiệu của bạn trong tìm kiếm trả phí)
- Không phù hợp thương hiệu (đại lý quảng bá sản phẩm của bạn trong các bối cảnh không phù hợp)

Đối với hầu hết các cửa hàng, bắt đầu với **xem xét thủ công** là an toàn hơn. Bạn luôn có thể bật tự động duyệt sau này khi bạn đã thiết lập các mẫu tin cậy.

## Ngưỡng thanh toán tối thiểu

Ngưỡng thanh toán tối thiểu ngăn ngừa chi phí hành chính từ việc xử lý nhiều khoản thanh toán nhỏ.

### Tại sao cần thiết lập ngưỡng

- **Giảm phí giao dịch** — Các nhà cung cấp thanh toán tính phí theo giao dịch, do đó việc gộp các khoản thanh toán tiết kiệm chi phí
- **Đơn giản hóa kế toán** — Ít sự kiện thanh toán hơn có nghĩa là ít công việc đối chiếu hơn
- **Tiêu chuẩn ngành** — Hầu hết các chương trình đại lý đều có ngưỡng (từ $25–$100)

### Ngưỡng điển hình

| Ngưỡng | Trường hợp sử dụng |
|-----------|----------|
| **$25–$50** | Các chương trình khối lượng cao nơi các đại lý đạt ngưỡng nhanh chóng |
| **$50–$100** | Ngưỡng tiêu chuẩn cho hầu hết các chương trình |
| **$100–$200** | Các chương trình cao cấp hoặc thanh toán quốc tế với phí xử lý cao |

### Cân bằng sự hài lòng của đại lý

Thiết lập ngưỡng **quá cao** làm phiền các đại lý có thể phải chờ hàng tháng để nhận khoản thanh toán đầu tiên của họ. Thiết lập nó **quá thấp** tạo gánh nặng hành chính và làm giảm biên lợi nhuận của bạn với các khoản phí.

**Khuyến nghị:** Bắt đầu ở $50. Đây là mức thấp đủ để các đại lý tích cực đạt được trong vài lần bán hàng đầu tiên của họ, nhưng cao đủ để gộp các khoản thanh toán hiệu quả.

### Không có giới hạn tối đa

Không có giới hạn số dư — các đại lý có thể tích lũy lợi nhuận vô hạn trước khi yêu cầu thanh toán. Một số đại lý ưa thích việc gộp các yêu cầu của họ hàng quý hoặc hàng năm để lập kế hoạch thuế.

## Quản lý trạng thái chương trình

Các chương trình có thể ở một trong ba trạng thái:

| Trạng thái | Mô tả | Hành vi |
|--------|-------------|----------|
| **Hoạt động** | Chương trình đang chạy | Chấp nhận các đại lý mới, theo dõi giới thiệu, tính toán hoa hồng |
| **Tạm dừng** | Vô hiệu hóa tạm thời | Các đại lý hiện tại vẫn tồn tại nhưng không có đăng ký mới; các cookie giới thiệu hiện tại vẫn hoạt động |
| **Lưu trữ** | Đã đóng vĩnh viễn | Không có đại lý mới, không theo dõi giới thiệu mới; dữ liệu lịch sử được bảo tồn để báo cáo |

### Khi tạm dừng chương trình

- Bạn đang điều chỉnh tỷ lệ hoa hồng hoặc điều khoản
- Bạn đang vượt ngân sách thanh toán đại lý cho quý này
- Bạn đang thử nghiệm cấu trúc chương trình mới và muốn ngăn các đại lý mới tham gia chương trình cũ

Các chương trình được tạm dừng vẫn tôn trọng các cookie theo dõi hiện có và các khoản hoa hồng đang chờ — bạn chỉ đang ngăn chặn các đại lý mới tham gia.

### Khi lưu trữ chương trình

- Bạn đã thay thế chương trình bằng cấu trúc mới
- Chương trình có thời hạn (ví dụ: chiến dịch theo mùa)
- Bạn đang hợp nhất nhiều chương trình thành một

Các chương trình đã lưu trữ vẫn tồn tại trong cơ sở dữ liệu để báo cáo lịch sử nhưng bị loại khỏi các view quản lý hoạt động.

## Các chương trình mẫu

### Ví dụ 1: Chương trình Nhà ảnh hưởng (Tỷ lệ phần trăm)

| Trường | Giá trị |
|-------|-------|
| Tên | Chương trình Nhà ảnh hưởng |
| Loại hoa hồng | Tỷ lệ phần trăm |
| Giá trị hoa hồng | 10 |
| Thời gian sống của cookie (ngày) | 30 |
| Tự động duyệt | Không đánh dấu (xem xét thủ công) |
| Ngưỡng thanh toán tối thiểu | 50.00 |
| Trạng thái | Hoạt động |

**Trường hợp sử dụng:** Tuyển dụng các nhà ảnh hưởng mạng xã hội và nhà sáng tạo nội dung. Hoa hồng 10% mở rộng theo giá trị đơn hàng, thưởng các đại lý thu hút được các khách hàng chi tiêu cao. Xem xét thủ công đảm bảo bạn kiểm tra từng đối tượng của nhà ảnh hưởng và sự phù hợp thương hiệu.

### Ví dụ 2: Chương trình Giới thiệu theo khối lượng (Số tiền cố định)

| Trường | Giá trị |
|-------|-------|
| Tên | Chương trình Đối tác Giới thiệu |
| Loại hoa hồng | Số tiền cố định |
| Giá trị hoa hồng | 25.00 |
| Thời gian sống của cookie (ngày) | 7 |
| Tự động duyệt | Đánh dấu |
| Ngưỡng thanh toán tối thiểu | 100.00 |
| Trạng thái | Hoạt động |

**Trường hợp sử dụng:** Hợp tác với các trang deal, các trang tổng hợp phiếu giảm giá và mạng lưới giới thiệu nơi mang lại khối lượng lớn. Hoa hồng cố định $25 giữ chi phí dự đoán được, và thời gian sống cookie ngắn (7 ngày) nhắm đến các khách hàng chuyển đổi nhanh. Tự động duyệt được bật vì các đối tác này thường tự phục vụ.

### Ví dụ 3: Đối tác cao cấp (Tỷ lệ phần trăm cao)

| Trường | Giá trị |
|-------|-------|
| Tên | Cấp bậc Đối tác Cao cấp |
| Loại hoa hồng | Tỷ lệ phần trăm |
| Giá trị hoa hồng | 15 |
| Thời gian sống của cookie (ngày) | 90 |
| Tự động duyệt | Không đánh dấu |
| Ngưỡng thanh toán tối thiểu | 200.00 |
| Trạng thái | Hoạt động |

**Trường hợp sử dụng:** Chương trình độc quyền dành cho các đại lý hiệu quả cao hoặc đối tác chiến lược. Hoa hồng cao hơn (15%) thưởng cho lưu lượng truy cập chất lượng của họ, và thời gian sống cookie 90 ngày phù hợp với chu kỳ cân nhắc dài hơn. Chỉ xem xét thủ công — đây là cấp bậc chỉ dành cho các đối tác được mời.

## Một số mẹo

- Bắt đầu với **hoa hồng theo tỷ lệ phần trăm** (5–15%) cho hầu hết các chương trình — dễ giải thích hơn cho các đại lý và mở rộng tự nhiên theo giá trị đơn hàng.
- Sử dụng **thời gian sống cookie 30 ngày** làm cơ sở — đây là tiêu chuẩn ngành và cân bằng giữa ghi công công bằng và giới hạn theo dõi thực tế.
- Bật **xem xét thủ công** ban đầu để kiểm tra các đại lý, sau đó chuyển sang tự động duyệt khi bạn đã thiết lập các mẫu tin cậy và kiểm soát gian lận.
- Thiết lập **ngưỡng thanh toán** của bạn từ $50–$100 để cân bằng giữa sự hài lòng của đại lý (không quá cao để đạt được) và hiệu quả hành chính (không quá nhiều các khoản thanh toán nhỏ).
- Tạo **các chương trình riêng biệt** cho các phân khúc đại lý khác nhau (nhà ảnh hưởng, các trang nội dung, các trang tổng hợp deal) để bạn có thể theo dõi hiệu suất và điều chỉnh hoa hồng độc lập.
- Theo dõi **bảng điều khiển phân tích** thường xuyên để phát hiện các đại lý hiệu quả cao và điều chỉnh tỷ lệ hoa hồng để giữ chân các đối tác hàng đầu.