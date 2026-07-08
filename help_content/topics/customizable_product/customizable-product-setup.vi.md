---
title: Cấu hình sản phẩm có thể tùy chỉnh
---

Hướng dẫn này sẽ hướng dẫn bạn qua toàn bộ quy trình thiết lập sản phẩm có thể tùy chỉnh, từ việc tạo sản phẩm đến cấu hình bề mặt, giá cả và các hạn chế tải lên. Hai ví dụ thực tế được sử dụng trong suốt hướng dẫn: một **áo phông tùy chỉnh** (sản phẩm có nhiều bề mặt) và một **poster tùy chỉnh** (in trên một bề mặt).

## Bước 1: Tạo sản phẩm

1. Di chuyển đến **Products > All Products** và nhấp vào **+ Add Product**
2. Thiết lập **Product Type** thành **Customizable Product**
3. Điền tên sản phẩm, mô tả, hình ảnh và giá cả như bạn sẽ làm với bất kỳ sản phẩm nào
4. Lưu sản phẩm

Sau khi lưu, nút **Open Design Editor Setup** mới xuất hiện trên biểu mẫu sản phẩm. Nút này sẽ đưa bạn đến trang thiết lập chuyên dụng nơi bạn cấu hình trình chỉnh sửa thiết kế trực quan.

## Bước 2: Truy cập thiết lập trình chỉnh sửa thiết kế

1. Mở sản phẩm bạn vừa tạo trong phần quản trị
2. Nhấp vào nút **Open Design Editor Setup** (trong phần **Customizable Product**)
3. Trang thiết lập mở ra với ba tab: **Surfaces**, **Settings**, và **Pricing**

Trang thiết lập là nơi bạn xác định mọi thứ liên quan đến trình chỉnh sửa thiết kế cho sản phẩm này.

## Bước 3: Thêm các bề mặt thiết kế

Một bề mặt đại diện cho một mặt có thể thiết kế của sản phẩm của bạn. Nhấp vào **+ Add Surface** để tạo mỗi bề mặt.

### Ví dụ áo phông: 3 bề mặt

| Surface | Name | Dimensions | Design zone | Notes |
|---------|------|-----------|-------------|-------|
| 1 | Front | 300 x 400 mm | Centered chest area | Main design area |
| 2 | Back | 300 x 400 mm | Upper back area | Secondary design area |
| 3 | Left Sleeve | 100 x 100 mm | Upper arm area | Small logo area only |

### Ví dụ poster: 1 bề mặt

| Surface | Name | Dimensions | Design zone | Notes |
|---------|------|-----------|-------------|-------|
| 1 | Front | 210 x 297 mm (A4) | Full printable area | Single surface, high DPI |

### Cấu hình từng bề mặt

Đối với mỗi bề mặt, bạn cấu hình các mục sau:

**Thông tin cơ bản:**
- **Name** — Điều khách hàng nhìn thấy trong các tab bề mặt (ví dụ: "Front", "Back")
- **Slug** — Nhận dạng an toàn cho URL, được tạo tự động từ tên
- **Sort Order** — Điều khiển thứ tự các bề mặt xuất hiện (số nhỏ hơn sẽ xuất hiện trước)

**Hình ảnh mô phỏng:**
- Nhấp vào khu vực hình ảnh mô phỏng để mở thư viện phương tiện và chọn một hình ảnh sản phẩm hiển thị bề mặt này
- Sử dụng hình ảnh chất lượng cao của sản phẩm từ góc nhìn đúng

**Vị trí khu vực thiết kế:**
- Sau khi chọn hình ảnh mô phỏng, một lớp phủ hình chữ nhật xuất hiện trên bản xem trước
- **Kéo** lớp phủ để đặt vị trí khu vực thiết kế nên có trên hình ảnh mô phỏng
- **Thay đổi kích thước** lớp phủ bằng cách kéo các cạnh để xác định ranh giới khu vực thiết kế
- Khu vực được lưu dưới dạng tọa độ dựa trên phần trăm, do đó nó sẽ mở rộng theo bất kỳ kích thước màn hình nào

Khu vực thiết kế cho trình chỉnh sửa biết chính xác nơi trên hình ảnh sản phẩm thiết kế của khách hàng sẽ xuất hiện. Hãy đặt nó cẩn thận để khớp với khu vực in thực tế của sản phẩm của bạn.

**Kích thước vật lý:**
- **Width** và **Height** — Kích thước thực tế của khu vực thiết kế
- **Unit** — Milimét, inch hoặc pixel
- Các kích thước này xác định tỷ lệ khung thiết kế và được sử dụng để tính toán DPI in

**Cài đặt in:**
- **Minimum DPI** — Số DPI tối thiểu chấp nhận được. Khách hàng sẽ thấy một cảnh báo nếu hình ảnh tải lên của họ dưới mức này. Mặc định: 150
- **Recommended DPI** — Độ phân giải lý tưởng cho chất lượng in tốt nhất. Mặc định: 300
- **Bleed (mm)** — Khoảng trống bổ sung bên ngoài khu vực thiết kế để in bleed. Đặt thành 0 nếu không cần bleed (thường gặp ở quần áo), hoặc 3mm cho sản phẩm in chuyên nghiệp
- **Max Colors** — Đối với in lưới, bạn có thể giới hạn số lượng màu. Để trống để không giới hạn (in kỹ thuật số)
- **Background Color** — Màu nền mặc định của khung thiết kế

### Cài đặt in áo phông và poster

| Setting | T-shirt | Poster |
|---------|---------|--------|
| Minimum DPI | 150 | 200 |
| Recommended DPI | 300 | 300 |
| Bleed | 0 mm | 3 mm |
| Max Colors | 6 (screen printing) | Blank (unlimited) |
| Background Color | Match garment color | `#ffffff` (white) |

## Bước 4: Các ràng buộc theo bề mặt

Mỗi bề mặt có thể ghi đè cài đặt tính năng toàn cục. Điều này cho phép bạn cho phép các công cụ khác nhau trên các bề mặt khác nhau.

Các tùy chọn ràng buộc là:

| Cài đặt | Tùy chọn | Mô tả |
|---------|---------|-------------|
| **Cho phép văn bản** | Kế thừa / Có / Không | Khách hàng có thể thêm văn bản trên bề mặt này hay không |
| **Cho phép tải lên hình ảnh** | Kế thừa / Có / Không | Khách hàng có thể tải lên hình ảnh cho bề mặt này hay không |
| **Cho phép hình minh họa** | Kế thừa / Có / Không | Khách hàng có thể sử dụng hình minh họa trên bề mặt này hay không |
| **Số lượng tối đa phần tử** | Số hoặc trống | Số phần tử thiết kế tối đa cho phép trên bề mặt này |

Khi đặt thành **Kế thừa**, bề mặt sẽ sử dụng cài đặt được cấu hình trong cài đặt toàn cục (Bước 6). Khi đặt thành **Có** hoặc **Không**, nó sẽ ghi đè cài đặt toàn cục cho bề mặt cụ thể đó.

### Ví dụ: Ràng buộc bề mặt tay áo áo phông

Đối với bề mặt tay áo của áo phông, bạn có thể muốn giới hạn tùy chỉnh chỉ cho phép logo nhỏ:

| Cài đặt | Giá trị | Lý do |
|---------|-------|--------|
| Cho phép văn bản | Không | Quá nhỏ để hiển thị văn bản |
| Cho phép tải lên hình ảnh | Có | Cho phép tải lên logo nhỏ |
| Cho phép hình minh họa | Không | Giữ đơn giản |
| Số lượng tối đa phần tử | 1 | Chỉ một logo |

Các bề mặt phía trước và phía sau sẽ vẫn được đặt thành **Kế thừa**, cho phép tất cả các công cụ như được định nghĩa trong cài đặt toàn cục.

### Ví dụ: Ràng buộc poster

Đối với poster, tất cả các bề mặt thường kế thừa từ cài đặt toàn cục vì chỉ có một bề mặt và tất cả các công cụ nên được sử dụng. Không cần ghi đè theo bề mặt.

## Bước 5: Cấu hình hạn chế tải lên

Trên tab **Cài đặt**, hãy cấu hình cách khách hàng có thể tải lên tệp:

| Cài đặt | Mô tả | Ví dụ áo phông | Ví dụ poster |
|---------|-------------|-----------------|----------------|
| **Kích thước tải lên tối đa** | Kích thước tệp tối đa cho mỗi lần tải lên | 10 MB | 20 MB |
| **Số lượng tải lên mỗi bề mặt** | Số lượng hình ảnh mỗi bề mặt | 5 | 3 |
| **Loại tệp được phép tải lên** | Định dạng tệp được chấp nhận | JPG, PNG, WebP | JPG, PNG, WebP |

Đề xuất kích thước tệp lớn hơn cho sản phẩm in, nơi khách hàng cần tải lên hình ảnh độ phân giải cao.

## Bước 6: Cài đặt trình chỉnh sửa

Trên tab **Cài đặt**, hãy cấu hình hành vi trình chỉnh sửa toàn cục:

**Chế độ trình chỉnh sửa:**
- **Trình chỉnh sửa Canvas** — Trình chỉnh sửa trực quan đầy đủ với xem trước canvas trực tiếp. Được khuyến nghị cho hầu hết các sản phẩm.
- **Biểu mẫu đơn giản** — Các trường biểu mẫu truyền thống cho tùy chỉnh cơ bản (ví dụ: chỉ văn bản khắc).

**Chuyển đổi tính năng (mặc định toàn cục):**
- **Cho phép văn bản** — Cho phép khách hàng thêm các phần tử văn bản
- **Cho phép tải lên hình ảnh** — Cho phép khách hàng tải lên hình ảnh của riêng họ
- **Cho phép hình minh họa** — Cho phép khách hàng duyệt và sử dụng thư viện hình minh họa của bạn

Các cài đặt toàn cục này áp dụng cho tất cả các bề mặt trừ khi bị ghi đè bởi các ràng buộc theo bề mặt (Bước 4).

## Bước 7: Cấu hình giá cả

Trên tab **Giá cả**, hãy đặt các khoản phí thiết kế được thêm vào giá cơ bản của sản phẩm:

| Phí | Mô tả |
|-----|-------------|
| **Phí thiết kế cơ bản** | Phí cố định được thêm khi áp dụng bất kỳ tùy chỉnh nào |
| **Phí theo bề mặt** | Phí bổ sung cho mỗi bề mặt được sử dụng ngoài bề mặt đầu tiên |
| **Phí theo tải lên** | Phí cho mỗi hình ảnh do khách hàng tải lên |
| **Phí theo văn bản** | Phí cho mỗi phần tử văn bản được thêm vào |

### Ví dụ: Giá cả áo phông

| Phí | Số tiền | Lý do |
|-----|--------|-----------|
| Phí thiết kế cơ bản | $5.00 | Bao phủ chi phí thiết lập cho bất kỳ đơn hàng tùy chỉnh nào |
| Phí theo bề mặt | $2.00 | Mỗi bề mặt bổ sung thêm chi phí in |
| Phí theo tải lên | $1.00 | Hình ảnh tùy chỉnh yêu cầu xử lý |
| Phí theo văn bản | $0.50 | Văn bản đơn giản hơn hình ảnh để sản xuất |

**Ví dụ tính toán:** Một khách hàng thiết kế áo phông với văn bản ở phía trước và logo ở phía sau:
- Phí thiết kế cơ bản: $5.00
- 1 bề mặt bổ sung (phía sau): $2.00
- 1 logo được tải lên: $1.00
- 1 phần tử văn bản: $0.50
- **Tổng phí thiết kế: $8.50** (được thêm vào giá cơ bản của sản phẩm)

### Ví dụ: Giá cả poster

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

| Phí | Số tiền | Lý do |
|-----|--------|-----------|
| Phí thiết kế cơ bản | $0.00 | Không có phí cơ bản — giá sản phẩm đã bao gồm |
| Phí theo bề mặt | $0.00 | Chỉ một bề mặt, không áp dụng |
| Phí tải lên | $2.00 | Xử lý độ phân giải cao |
| Phí theo văn bản | $0.00 | Văn bản được bao gồm trong trải nghiệm cơ bản |

**Ví dụ tính toán:** Một khách hàng tạo một poster với 2 hình ảnh đã tải lên và 3 phần văn bản:
- Phí thiết kế cơ bản: $0.00
- 2 hình ảnh đã tải lên: $4.00
- 3 phần văn bản: $0.00
- **Tổng phí thiết kế: $4.00**

Phí thiết kế được hiển thị cho khách hàng theo thời gian thực khi họ thêm các yếu tố, vì vậy họ có thể thấy tác động chi phí của từng yếu tố trước khi thêm vào giỏ hàng.

## So sánh thiết lập tổng quan

| Tiêu chí | Áo phông tùy chỉnh | Poster tùy chỉnh |
|--------|---------------|---------------|
| Bề mặt | 3 (trước, sau, tay) | 1 (trước) |
| Hình ảnh mô phỏng | 3 hình ảnh sản phẩm | 1 hình ảnh sản phẩm |
| Vị trí vùng | Khu vực ngực/đằng sau/tay | Toàn bộ khu vực in |
| Kích thước | 300x400mm, 100x100mm | 210x297mm (A4) |
| DPI tối thiểu | 150 | 200 |
| Khe hở (bleed) | 0 mm | 3 mm |
| Số màu tối đa | 6 | Vô hạn |
| Ràng buộc theo bề mặt | Tay bị giới hạn | Không cần |
| Mô hình định giá | Cơ bản + bề mặt + tải lên + văn bản | Chỉ phí tải lên |

## Mẹo

- Luôn kiểm tra trình chỉnh sửa thiết kế từ góc nhìn của khách hàng sau khi hoàn tất thiết lập. Truy cập trang sản phẩm trên cửa hàng và thử thêm văn bản, tải lên hình ảnh và chuyển đổi bề mặt.
- Tải lên các hình ảnh mô phỏng khớp gần với hình dạng thực tế của sản phẩm. Đối với áo phông, chụp từng góc riêng biệt. Đối với poster, sử dụng hình ảnh phẳng sạch sẽ hoặc hình ảnh mô phỏng khung.
- Đặt vùng thiết kế một cách thận trọng — tốt hơn là xác định một vùng nhỏ hơn một chút thay vì để thiết kế in vào đường may hoặc mép.
- Thiết lập DPI tối thiểu dựa trên phương pháp in của bạn: 150 cho in lưới, 200 cho in kỹ thuật số tiêu chuẩn, 300 cho in offset chất lượng cao.
- Sử dụng 3mm khe hở (bleed) cho bất kỳ sản phẩm nào sẽ được cắt sau khi in (poster, thiệp kinh doanh, tờ rơi). Đặt khe hở thành 0 cho các sản phẩm mà thiết kế được áp dụng lên bề mặt hiện có (áo phông, cốc, vỏ điện thoại).
- Bắt đầu với định giá đơn giản và điều chỉnh dựa trên phản hồi của khách hàng. Nhiều nhà bán hàng bắt đầu chỉ với phí thiết kế cơ bản và sau đó thêm các phí theo yếu tố.