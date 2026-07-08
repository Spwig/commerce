---
title: Tùy chỉnh Cổng đại lý
---

Cổng đại lý Spwig là trang đích hướng tới công chúng, nơi các đại lý tiềm năng tìm hiểu về chương trình của bạn và đăng ký. Việc tùy chỉnh cổng này giúp bạn đồng bộ hóa thông điệp, thương hiệu và lời kêu gọi hành động với vị thế độc đáo của cửa hàng bạn. Một cổng được thiết kế tốt sẽ thu hút các đại lý chất lượng cao và chuyển đổi khách truy cập thành đối tác tích cực.

## Cổng đại lý là gì?

Cổng đại lý có thể truy cập tại `/affiliate/` trên tên miền cửa hàng của bạn. Nó đóng vai trò là:

- **Trang khám phá** — Nơi các đại lý tiềm năng tìm hiểu về cấu trúc hoa hồng, lợi ích và yêu cầu của bạn
- **Điểm truy cập đăng ký** — Biểu mẫu đăng ký cho các đại lý mới (đăng ký khách hoặc dựa trên tài khoản)
- **Cổng đăng nhập** — Các đại lý hiện tại có thể đăng nhập để truy cập bảng điều khiển của họ
- **Trưng bày thương hiệu** — Phản ánh bản sắc cửa hàng và giá trị cốt lõi của chương trình đại lý

Cổng có thể tùy chỉnh hoàn toàn thông qua phần cài đặt đại lý trong quản trị, bao gồm thông điệp nổi bật, các tính năng nổi bật, quy trình từng bước và tùy chọn đăng ký.

![Trang đích Cổng đại lý](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## Truy cập Cài đặt

Di chuyển đến **Marketing > Chương trình đại lý > Cài đặt cổng** để tùy chỉnh cổng.

Mô hình Cài đặt đại lý là một **đơn thể** — bạn chỉ có đúng một bản ghi cài đặt cho toàn bộ cửa hàng của mình. Tất cả các trường đều **có thể dịch** bằng hệ thống dịch của Spwig, vì vậy bạn có thể tùy chỉnh thông điệp cho mỗi ngôn ngữ mà cửa hàng của bạn hỗ trợ.

## Phần nổi bật

Phần nổi bật là điều đầu tiên mà các đại lý tiềm năng nhìn thấy. Nó bao gồm:

- **Tiêu đề** — Tiêu đề chính (ví dụ: "Tham gia Chương trình Đại lý của Chúng Tôi")
- **Phần phụ đề** — Văn bản hỗ trợ giải thích giá trị chương trình (ví dụ: "Kiếm hoa hồng bằng cách quảng bá sản phẩm cao cấp cho khán giả của bạn")
- **Thống kê** — Chỉ số được hiển thị tự động:
  - Tổng số chương trình đang hoạt động
  - Tổng số đại lý đang hoạt động
  - Tỷ lệ hoa hồng trung bình (tính toán trên tất cả các chương trình đang hoạt động)
- **Nút CTA** — Được tạo tự động:
  - **Đăng nhập** — Cho các đại lý hiện tại
  - **Trở thành đại lý** — Kích hoạt quy trình đăng ký

### Tùy chỉnh thông điệp nổi bật

| Trường | Giá trị ví dụ | Mục đích |
|-------|--------------|---------|
| **Tiêu đề nổi bật** | "Hợp tác Với Chúng Tôi & Kiếm Tiền" | Thu hút sự chú ý bằng tiêu đề tập trung vào lợi ích |
| **Phần phụ đề nổi bật** | "Tham gia 500+ đại lý đang kiếm hoa hồng cạnh tranh cho mỗi lần bán hàng bạn giới thiệu" | Cung cấp bằng chứng xã hội và làm rõ đề xuất |

Các thống kê được **tính toán tự động** và cập nhật theo thời gian thực dựa trên các chương trình và đại lý đang hoạt động của bạn. Bạn không thể chỉnh sửa các giá trị này một cách thủ công.

## Phần tính năng

Phần tính năng nổi bật **6 thẻ lợi ích có thể tùy chỉnh** giải thích lý do tại sao các đại lý nên tham gia chương trình của bạn. Mỗi thẻ tính năng chứa:

- **Biểu tượng** — Lớp biểu tượng FontAwesome (ví dụ: `fa-dollar-sign`, `fa-chart-line`, `fa-headset`)
- **Tiêu đề** — Tiêu đề lợi ích (ví dụ: "Hoa hồng cạnh tranh")
- **Mô tả** — Giải thích 1-2 câu (ví dụ: "Kiếm được tới 15% cho mỗi lần bán hàng bạn giới thiệu")

### Tính năng mặc định

Spwig cung cấp các tính năng mặc định khi bạn lần đầu cài đặt ứng dụng đại lý:

| Biểu tượng | Tiêu đề | Mô tả |
|------|-------|-------------|
| `fa-dollar-sign` | Hoa hồng cạnh tranh | Kiếm được hoa hồng hậu hĩnh cho mỗi lần bán hàng bạn giới thiệu |
| `fa-link` | Liên kết theo dõi dễ dàng | Nhận được các liên kết theo dõi duy nhất hoạt động ở bất kỳ đâu |
| `fa-chart-line` | Phân tích thời gian thực | Theo dõi lượt nhấp, chuyển đổi và thu nhập trong bảng điều khiển của bạn |
| `fa-calendar-check` | Thanh toán đáng tin cậy | Nhận tiền đúng hạn qua PayPal hoặc chuyển khoản ngân hàng |
| `fa-headset` | Hỗ trợ chuyên dụng | Đội ngũ của chúng tôi luôn sẵn sàng giúp bạn thành công |
| `fa-gift` | Tài liệu tiếp thị | Truy cập các banner, hình ảnh và nội dung quảng bá |

### Tùy chỉnh tính năng

Các tính năng được lưu trữ dưới dạng **mảng JSON** trong cơ sở dữ liệu. Chỉnh sửa chúng trực tiếp trong biểu mẫu quản trị:

```json
[
  {
    "icon": "fa-percent",
    "title": "Lên đến 20% Hoa hồng",
    "description": "Kiếm được hoa hồng hàng đầu ngành từ các lần bán hàng sản phẩm cao cấp"
  },
  {
    "icon": "fa-rocket",
    "title": "Phê duyệt Nhanh",
    "description": "Được phê duyệt trong 24 giờ và bắt đầu quảng bá ngay lập tức"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Bảng điều khiển Di động",
    "description": "Quản lý các liên kết của bạn và theo dõi thu nhập từ bất kỳ thiết bị nào"
  }
]
```

**Tham khảo biểu tượng:** Sử dụng bất kỳ lớp biểu tượng nào từ FontAwesome 5 Free. Xem các biểu tượng tại [fontawesome.com/icons](https://fontawesome.com/icons) và sử dụng tên lớp (ví dụ: `fa-trophy`, `fa-users`, `fa-star`).

## Phần "Cách hoạt động"

Phần "Cách hoạt động" hiển thị **luồng trực quan 4 bước** giải thích hành trình đại lý. Mỗi bước bao gồm:

- **Tiêu đề** — Tên bước (ví dụ: "Đăng ký")
- **Mô tả** — Giải thích 1-2 câu về điều gì sẽ xảy ra

### Các bước mặc định

| Bước | Tiêu đề | Mô tả |
|------|-------|-------------|
| 1 | Đăng ký | Tạo tài khoản đại lý miễn phí trong vài phút |
| 2 | Nhận liên kết của bạn | Tạo các liên kết theo dõi duy nhất cho bất kỳ sản phẩm hoặc trang nào |
| 3 | Quảng bá | Chia sẻ liên kết của bạn với khán giả của bạn thông qua nội dung, mạng xã hội hoặc email |
| 4 | Kiếm hoa hồng | Nhận tiền khi khách hàng mua hàng bằng các liên kết giới thiệu của bạn |

### Tùy chỉnh các bước

Các bước được lưu trữ dưới dạng **mảng JSON**. Bạn có thể chỉnh sửa chúng trong quản trị:

```json
[
  {
    "title": "Đăng ký để tham gia",
    "description": "Gửi đơn đăng ký và cho chúng tôi biết về nền tảng của bạn"
  },
  {
    "title": "Nhận được phê duyệt",
    "description": "Đội ngũ của chúng tôi xem xét đơn đăng ký của bạn trong vòng 24 giờ"
  },
  {
    "title": "Tạo liên kết",
    "description": "Truy cập bảng điều khiển của bạn và tạo liên kết theo dõi ngay lập tức"
  },
  {
    "title": "Bắt đầu kiếm tiền",
    "description": "Kiếm hoa hồng cho mỗi lần bán hàng bạn giới thiệu — thanh toán hàng tháng qua PayPal"
  }
]
```

Luồng trực quan tự động đánh số từng bước (1, 2, 3, 4) trên trang đích.

## Phần CTA

Phần cuối cùng trước biểu mẫu đăng ký là **phần Kêu gọi hành động (CTA)**. Nó cung cấp một cú đẩy cuối cùng để khuyến khích việc đăng ký.

| Trường | Giá trị ví dụ | Mục đích |
|-------|--------------|---------|
| **Tiêu đề CTA** | "Sẵn sàng bắt đầu kiếm tiền?" | Câu hỏi trực tiếp tạo sự khẩn cấp |
| **Mô tả CTA** | "Tham gia chương trình đại lý của chúng tôi ngay hôm nay và bắt đầu kiếm hoa hồng trên các sản phẩm bạn đã yêu thích và giới thiệu." | Củng cố lợi ích và loại bỏ rào cản |

Phần CTA tự động hiển thị nút **Trở thành đại lý** bên dưới văn bản.

## Cài đặt Đăng ký

Kiểm soát cách các đại lý mới đăng ký và thông tin họ cung cấp.

### Biểu mẫu đăng ký tùy chỉnh

**Trường:** `custom_form` (Khóa ngoại đến biểu mẫu FormBuilder)

Nếu bạn có biểu mẫu đăng ký tùy chỉnh được xây dựng bằng FormBuilder của Spwig, hãy chọn nó ở đây. Điều này cho phép bạn thu thập thêm thông tin trong quá trình đăng ký (ví dụ: URL trang web, quy mô khán giả, kênh quảng bá).

**Để trống** để sử dụng biểu mẫu đăng ký đại lý mặc định (email, mật khẩu, chi tiết thanh toán).

### Cho phép đăng ký khách

**Trường:** `allow_guest_registration` (Giá trị Boolean)

- **Đánh dấu** — Người truy cập có thể ứng tuyển mà không cần tạo tài khoản Spwig trước
- **Không đánh dấu** — Người truy cập phải đăng nhập hoặc tạo tài khoản khách hàng trước khi ứng tuyển

**Khuyến nghị:** Bật đăng ký khách để giảm bớt sự cản trở. Bạn luôn có thể yêu cầu phê duyệt để kiểm tra các đại lý trước khi kích hoạt họ.

### Yêu cầu phê duyệt

**Trường:** `require_approval` (Giá trị Boolean)

- **Đánh dấu** — Các đại lý mới phải chờ phê duyệt thủ công trước khi truy cập bảng điều khiển của họ
- **Không đánh dấu** — Các đại lý mới được phê duyệt tự động và có thể tạo liên kết ngay lập tức

**Khuyến nghị:** Bật phê duyệt thủ công nếu bạn muốn kiểm tra các đại lý về sự phù hợp thương hiệu, ngăn chặn gian lận hoặc chương trình độc quyền.

### Liên kết Điều khoản và Điều kiện

**Trường:** `terms_url` (URL)

Liên kết tùy chọn đến điều khoản và điều kiện của chương trình đại lý của bạn. Nếu được cung cấp, biểu mẫu đăng ký sẽ hiển thị một hộp kiểm yêu cầu các đại lý chấp thuận điều khoản của bạn trước khi đăng ký.

**Ví dụ:** `/pages/affiliate-terms/`

### Thông điệp chào mừng

**Trường:** `welcome_message` (Văn bản)

Thông điệp được hiển thị cho các đại lý ngay sau khi đăng ký thành công. Sử dụng nó để:

- Cảm ơn họ đã tham gia
- Giải thích các bước tiếp theo (ví dụ: "Chúng tôi sẽ xem xét đơn đăng ký của bạn trong vòng 24 giờ")
- Liên kết đến các tài nguyên bắt đầu

**Ví dụ:*
```
Chào mừng bạn đến với chương trình đại lý của chúng tôi! Chúng tôi đã nhận được đơn đăng ký của bạn và sẽ xem xét trong vòng 24 giờ. Kiểm tra email của bạn để xác nhận phê duyệt và hướng dẫn đăng nhập.
```

## Hỗ trợ đa ngôn ngữ

Tất cả các trường văn bản trong Cài đặt đại lý đều **có thể dịch** bằng tiện ích dịch của Spwig:

- Tiêu đề nổi bật
- Phụ đề nổi bật
- Tính năng (JSON được dịch theo ngôn ngữ)
- Các bước "Cách hoạt động" (JSON được dịch theo ngôn ngữ)
- Tiêu đề CTA
- Mô tả CTA
- Thông điệp chào mừng

### Cách hoạt động của dịch thuật

Khi bạn chỉnh sửa một trường có thể dịch, bạn sẽ thấy tiện ích dịch cho phép bạn cung cấp nội dung cho mỗi ngôn ngữ được bật. Đối với các trường JSON (tính năng, bước), bạn cung cấp các đối tượng JSON riêng biệt cho mỗi ngôn ngữ:

**Tiếng Anh:*
```json
[
  {"icon": "fa-dollar-sign", "title": "Hoa hồng cạnh tranh", "description": "Kiếm được tới 15% cho mỗi lần bán hàng"}
]
```

**Tiếng Tây Ban Nha:*
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones Competitivas", "description": "Gana hasta el 15% en cada venta"}
]
```

Cổng tự động hiển thị phiên bản ngôn ngữ phù hợp dựa trên sở thích ngôn ngữ của người truy cập.

## Xem trước thay đổi của bạn

Sau khi tùy chỉnh cài đặt cổng:

1. **Lưu** thay đổi của bạn trong quản trị
2. Truy cập `/affiliate/` trên frontend cửa hàng của bạn (mở trong tab mới)
3. **Kiểm tra quy trình đăng ký** bằng cách nhấp vào "Trở thành đại lý"
4. **Xác minh tính nhất quán thương hiệu** — cổng có khớp với thiết kế và thông điệp của cửa hàng bạn không?

Bạn có thể thực hiện các thay đổi lặp lại và làm tươi trang để xem các cập nhật ngay lập tức.

## Các tùy chỉnh ví dụ

### Tình huống 1: Cửa hàng thời trang thương mại điện tử

**Mục tiêu:** Thu hút các nhà ảnh hưởng và blogger thời trang.

| Cài đặt | Giá trị |
|---------|-------|
| Tiêu đề nổi bật | "Khuyến khích các phong cách bạn yêu thích và kiếm tiền" |
| Phụ đề nổi bật | "Tham gia 1,200+ nhà ảnh hưởng kiếm được 12% hoa hồng cho mỗi lần bán hàng" |
| Tính năng 1 | Biểu tượng: `fa-tshirt`, Tiêu đề: "Bộ sưu tập thời trang được chọn lọc", Mô tả: "Khuyến khích quần áo cao cấp và phụ kiện" |
| Tính năng 2 | Biểu tượng: `fa-percentage`, Tiêu đề: "12% Hoa hồng", Mô tả: "Tỷ lệ hàng đầu ngành cho tất cả các sản phẩm" |
| Tính năng 3 | Biểu tượng: `fa-camera`, Tiêu đề: "Nội dung độc quyền", Mô tả: "Truy cập hình ảnh sản phẩm, video và tài sản chiến dịch" |
| Cho phép đăng ký khách | Đánh dấu |
| Yêu cầu phê duyệt | Đánh dấu (xem xét thủ công cho sự phù hợp thương hiệu) |

### Tình huống 2: Chương trình đối tác SaaS B2B

**Mục tiêu:** Thu hút các chuyên gia kinh doanh và công ty đại lý cho các giới thiệu phần mềm doanh nghiệp.

| Cài đặt | Giá trị |
|---------|-------|
| Tiêu đề nổi bật | "Hợp tác Với Chúng Tôi để Tăng Doanh Thu" |
| Phụ đề nổi bật | "Kiếm được $500 cho mỗi lần giới thiệu doanh nghiệp thông qua chương trình đối tác B2B của chúng tôi" |
| Tính năng 1 | Biểu tượng: `fa-handshake`, Tiêu đề: "$500 mỗi lần giới thiệu", Mô tả: "Hoa hồng cố định cho các khách hàng doanh nghiệp đủ điều kiện" |
| Tính năng 2 | Biểu tượng: `fa-clock`, Tiêu đề: "Cookie 180 ngày", Mô tả: "Cửa sổ ghi nhận dài cho các chu kỳ bán hàng phức tạp" |
| Tính năng 3 | Biểu tượng: `fa-user-tie`, Tiêu đề: "Quản lý đối tác chuyên dụng", Mô tả: "Hỗ trợ đặc biệt cho khách hàng của bạn" |
| Cho phép đăng ký khách | Không đánh dấu (B2B yêu cầu tài khoản) |
| Yêu cầu phê duyệt | Đánh dấu (chương trình mời) |
| Liên kết điều khoản | `/pages/partner-program-terms/` |

## Một số mẹo

- Tùy chỉnh **tiêu đề nổi bật** để tập trung vào lợi ích, không phải tính năng — "Kiếm tiền khi ngủ" hấp dẫn hơn "Đăng ký chương trình đại lý"
- Sử dụng **bằng chứng xã hội** trong phụ đề (ví dụ: "Tham gia 500+ đại lý") để xây dựng lòng tin và uy tín
- Chọn **biểu tượng FontAwesome** giúp củng cố trực quan cho từng lợi ích — biểu tượng phải truyền đạt giá trị ngay lập tức
- Giữ mô tả tính năng **1-2 câu** — cổng là về chuyển đổi, không phải giải thích chi tiết
- Kiểm tra **quy trình đăng ký** của bạn trước khi quảng bá cổng — phát hiện các điểm cản trở như trường biểu mẫu gây nhầm lẫn hoặc liên kết bị hỏng
- Bật **đăng ký khách** để giảm bớt sự cản trở đăng ký, sau đó sử dụng **yêu cầu phê duyệt** để kiểm tra các đại lý sau khi họ đã nộp đơn
- Sử dụng **thông điệp chào mừng** để thiết lập kỳ vọng (thời gian phê duyệt, các bước tiếp theo, liên hệ hỗ trợ) và giảm các câu hỏi hỗ trợ
- Cập nhật cổng **theo mùa** để phù hợp với chiến dịch — làm nổi bật các chương trình hoa hồng đặc biệt hoặc ra mắt sản phẩm mới

Hãy nhớ: Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật như được hiển thị trong các quy tắc bảo tồn.