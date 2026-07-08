---
title: Phương thức vận chuyển
---

Phương thức vận chuyển là các tùy chọn giao hàng được hiển thị cho khách hàng tại bước thanh toán—mỗi phương thức tính toán chi phí vận chuyển bằng các chiến lược định giá khác nhau. Spwig hỗ trợ 7 loại phương thức từ các mức giá cố định đơn giản đến định giá thời gian thực phức tạp được tính toán bởi nhà vận chuyển. Các phương thức có thể bị giới hạn bởi giá trị đơn hàng tối thiểu/tối đa, trọng lượng và các khu vực địa lý. Khách hàng chọn phương thức ưa thích của họ trong quá trình thanh toán, và chi phí được tính sẽ được thêm vào tổng số tiền đơn hàng.

Sử dụng hướng dẫn này để cấu hình các phương thức vận chuyển phù hợp với mô hình kinh doanh của bạn, từ vận chuyển mức giá cố định cơ bản đến định giá theo cấp bậc dựa trên khu vực phức tạp.

## Các loại phương thức vận chuyển

Spwig cung cấp 7 loại phương thức vận chuyển, mỗi loại có logic tính toán chi phí khác nhau:

### Vận chuyển mức giá cố định

**Đây là gì**: Chi phí cố định, không phụ thuộc vào nội dung giỏ hàng, địa điểm hoặc trọng lượng.

**Khi sử dụng**:
- Cửa hàng đơn giản với chi phí vận chuyển dễ dự đoán
- Một loại sản phẩm (kích thước/trọng lượng tương tự)
- Giao hàng trong nước với mức giá tiêu chuẩn của nhà vận chuyển
- Khuyến mãi miễn phí vận chuyển (sử dụng cùng với các quy tắc vận chuyển)

**Cấu hình**:
- Thiết lập **Loại phương thức** = Mức giá cố định
- Nhập **Chi phí cố định** (ví dụ: $9.99)
- Tùy chọn: Thiết lập giới hạn giá trị đơn hàng tối thiểu/tối đa

**Ví dụ**: "Vận chuyển tiêu chuẩn - $9.99" cho tất cả các đơn hàng trong nước.

---

### Miễn phí vận chuyển

**Đây là gì**: Tùy chọn vận chuyển không mất phí (khách hàng không phải trả tiền).

**Khi sử dụng**:
- Khuyến mãi miễn phí vận chuyển
- Đơn hàng có giá trị cao (kết hợp với giá trị đơn hàng tối thiểu)
- Lựa chọn lấy hàng tại địa phương
- Quyền lợi của chương trình khách hàng thân thiết

**Cấu hình**:
- Thiết lập **Loại phương thức** = Miễn phí vận chuyển
- Tùy chọn: Thiết lập **Giá trị đơn hàng tối thiểu** (ví dụ: miễn phí khi đơn hàng trên $50)
- Kết hợp tốt với các quy tắc vận chuyển để có miễn phí vận chuyển có điều kiện

**Ví dụ**: "Miễn phí vận chuyển cho đơn hàng trên $50" với min_order_value = $50.

---

### Vận chuyển theo trọng lượng

**Đây là gì**: Chi phí được tính dựa trên bảng giá theo cấp bậc dựa trên trọng lượng tổng giỏ hàng.

**Khi sử dụng**:
- Sản phẩm có trọng lượng biến đổi (sách, thiết bị điện tử, thực phẩm)
- Mô hình định giá của nhà vận chuyển dựa trên trọng lượng
- Tỷ lệ trọng lượng đến chi phí dễ dự đoán

**Cấu hình**:
1. Thiết lập **Loại phương thức** = Theo trọng lượng
2. Tạo **Bảng giá vận chuyển** với basis_type = "weight"
3. Thêm **Cấp bậc giá vận chuyển** (ví dụ: 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Tùy chọn: Giới hạn cho các khu vực cụ thể

**Ví dụ**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**Cách hoạt động**: Giỏ hàng tính tổng trọng lượng → tìm cấp bậc phù hợp → trả về giá của cấp bậc đó.

---

### Vận chuyển theo giá trị

**Đây là gì**: Chi phí được tính dựa trên bảng giá theo cấp bậc dựa trên tổng giá trị giỏ hàng.

**Khi sử dụng**:
- Chi phí vận chuyển tương quan với giá trị đơn hàng
- Khuyến khích giá trị giỏ hàng cao hơn (giảm tỷ lệ mỗi đô la ở cấp bậc cao hơn)
- Lựa chọn đơn giản hơn vận chuyển theo trọng lượng cho các mặt hàng có giá tương tự

**Cấu hình**:
1. Thiết lập **Loại phương thức** = Theo giá trị
2. Tạo **Bảng giá vận chuyển** với basis_type = "price"
3. Thêm **Cấp bậc giá vận chuyển** (ví dụ: $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Ví dụ**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Miễn phí
```

**Cách hoạt động**: Giỏ hàng tính tổng giá trị → tìm cấp bậc phù hợp → trả về giá của cấp bậc đó.

---

### Mức giá thời gian thực từ nhà vận chuyển

**Đây là gì**: Mức giá thời gian thực được truy xuất từ API của nhà vận chuyển (FedEx, UPS, DHL) tại bước thanh toán.

**Khi sử dụng**:
- Chi phí vận chuyển thay đổi theo địa điểm
- Nhiều lựa chọn nhà vận chuyển cho khách hàng
- Định giá chính xác từ nhà vận chuyển mà không cần bảng giá thủ công
- Giao hàng quốc tế với định giá phức tạp

**Cấu hình**:
1. Thiết lập **Loại phương thức** = Thời gian thực
2. Tạo **Tài khoản nhà cung cấp** (Cài đặt > Vận chuyển > Tài khoản nhà cung cấp)
3. Nhập thông tin xác thực API của nhà vận chuyển (số tài khoản, khóa API, bí mật)
4. Liên kết tài khoản nhà cung cấp với phương thức vận chuyển
5. Tùy chọn: Thêm phần trăm markup hoặc markup cố định

**Yêu cầu**:
- Tài khoản nhà vận chuyển đang hoạt động (FedEx, UPS, DHL, v.v.)
- Thông tin xác thực API từ nhà vận chuyển
- Các gói vận chuyển được định nghĩa (để tính toán trọng lượng theo kích thước)

**Ví dụ**: Phương thức "FedEx Ground" truy xuất mức giá FedEx thời gian thực dựa trên trọng lượng, kích thước và địa điểm của giỏ hàng tại bước thanh toán.

**Cách hoạt động**:
1. Khách hàng nhập địa chỉ tại bước thanh toán
2. Hệ thống gọi API nhà vận chuyển với điểm xuất phát, điểm đến, kích thước và trọng lượng gói hàng
3. Nhà vận chuyển trả về mức giá
4. Markup tùy chọn được áp dụng
5. Mức giá được hiển thị cho khách hàng

---

### Lấy hàng tại địa điểm

**Đây là gì**: Khách hàng tự đến lấy hàng tại địa điểm vật lý (không có chi phí giao hàng).

**Khi sử dụng**:
- Cửa hàng bán lẻ cung cấp dịch vụ lấy hàng
- Lựa chọn lấy hàng tại kho
- Sự kiện hoặc quầy hàng chợ
- Loại bỏ chi phí vận chuyển cho khách hàng địa phương

**Cấu hình**:
1. Thiết lập **Loại phương thức** = Lấy hàng tại địa điểm
2. Tạo **Địa điểm** (Cài đặt > Vận chuyển > Địa điểm)
   - Thiết lập địa chỉ, giờ làm việc, khả năng lấy hàng
3. Liên kết địa điểm (các địa điểm) với phương thức
4. Tùy chọn: Thiết lập thời gian chuẩn bị lấy hàng (ví dụ: "Sẵn sàng trong 2 giờ")

**Trải nghiệm của khách hàng**:
- Chọn "Lấy hàng tại địa điểm" tại bước thanh toán
- Chọn địa điểm lấy hàng (nếu có nhiều địa điểm)
- Chọn ngày/giờ lấy hàng dựa trên khả năng có sẵn
- Nhận thông báo khi đơn hàng sẵn sàng

**Ví dụ**: "Lấy hàng tại cửa hàng - Miễn phí" với 3 địa điểm bán lẻ, sẵn sàng trong vòng 24 giờ.

---

### Vận chuyển theo bảng giá

**Đây là gì**: Định giá theo cấp bậc linh hoạt dựa trên trọng lượng, giá trị hoặc số lượng với mục tiêu khu vực nâng cao.

**Khi sử dụng**:
- Định giá phức tạp (mức giá khác nhau theo khu vực và trọng lượng)
- Cần kiểm soát nhiều hơn so với vận chuyển theo trọng lượng hoặc theo giá trị
- Nhiều yếu tố định giá (ví dụ: trọng lượng + điểm đến + số lượng)

**Cấu hình**:
1. Thiết lập **Loại phương thức** = Vận chuyển theo bảng giá
2. Tạo **Bảng giá vận chuyển**
3. Định nghĩa **basis_type**: trọng lượng, giá trị hoặc số lượng
4. Thêm **Cấp bậc giá vận chuyển** với giá trị tối thiểu/tối đa
5. Tùy chọn: Giới hạn cấp bậc cho khu vực hoặc quốc gia cụ thể

**Sự khác biệt so với vận chuyển theo trọng lượng/giá trị**: Vận chuyển theo bảng giá hỗ trợ giới hạn địa lý theo cấp bậc, cho phép mức giá khác nhau cho cùng trọng lượng/giá trị trong các khu vực khác nhau.

**Ví dụ**:
```
Khu vực A (Trong nước):
  0-5kg: $10
  5-10kg: $15

Khu vực B (Khu vực hẻo lánh):
  0-5kg: $18
  5-10kg: $25
```

**Cách hoạt động**: Giỏ hàng tính giá trị cơ sở (trọng lượng/giá trị/số lượng) → tìm cấp bậc phù hợp với khu vực của khách hàng → trả về giá của cấp bậc đó.

---

## Cấu hình phương thức vận chuyển

Tất cả phương thức vận chuyển chia sẻ các cài đặt chung sau:

### Cài đặt cơ bản

- **Tên**: Tên nội bộ (không hiển thị cho khách hàng)
- **Tên hiển thị**: Tên hiển thị cho khách hàng tại bước thanh toán (ví dụ: "Vận chuyển tiêu chuẩn", "Giao hàng nhanh")
- **Mô tả**: Văn bản hỗ trợ tùy chọn hiển thị tại bước thanh toán (ví dụ: "Giao hàng trong 3-5 ngày làm việc")
- **Loại phương thức**: Một trong 7 loại trên
- **Kích hoạt**: Chuyển đổi để bật/tắt phương thức mà không xóa nó

### Cài đặt chi phí

- **Chi phí cố định**: Chỉ dành cho phương thức mức giá cố định
- **Bảng giá**: Dành cho phương thức theo trọng lượng, theo giá trị, theo bảng giá
- **Tài khoản nhà cung cấp**: Dành cho phương thức thời gian thực
- **Lớp thuế**: Áp dụng thuế cho chi phí vận chuyển (nếu cần)

### Giới hạn

**Giới hạn giá trị đơn hàng**:
- **Giá trị đơn hàng tối thiểu**: Phương thức chỉ có sẵn nếu tổng giá trị giỏ hàng ≥ số tiền (ví dụ: miễn phí vận chuyển khi đơn hàng trên $50)
- **Giá trị đơn hàng tối đa**: Phương thức bị ẩn nếu tổng giá trị giỏ hàng > số tiền (ví dụ: mức giá cố định chỉ dành cho đơn hàng dưới $100)

**Giới hạn trọng lượng**:
- **Trọng lượng tối thiểu**: Phương thức chỉ có sẵn nếu trọng lượng giỏ hàng ≥ số tiền
- **Trọng lượng tối đa**: Phương thức bị ẩn nếu trọng lượng giỏ hàng > số tiền (thường gặp ở các phương thức vận chuyển nhẹ)

**Giới hạn địa lý**:
- **Khu vực vận chuyển**: Liên kết phương thức với các khu vực cụ thể (trong nước, quốc tế, khu vực)
- Khu vực trống = có sẵn cho tất cả địa chỉ
- Nhiều khu vực = có sẵn cho bất kỳ khu vực nào phù hợp

### Cài đặt nâng cao

- **Ưu tiên**: Thứ tự hiển thị tại bước thanh toán (số nhỏ hơn = hiển thị cao hơn trong danh sách)
- **Phí xử lý**: Phí cố định bổ sung được thêm vào chi phí đã tính
- **Ngưỡng miễn phí vận chuyển**: Đặt chi phí thành $0 nếu tổng giá trị giỏ hàng ≥ ngưỡng (lựa chọn thay thế cho min_order_value)

---

## Tạo phương thức vận chuyển

**Quy trình làm việc từng bước**:

1. **Di chuyển đến Phương thức Vận chuyển**
   - Đi đến Cài đặt > Giỏ hàng > Phương thức Vận chuyển
   - Nhấp vào "Thêm Phương thức Vận chuyển"

2. **Chọn Loại Phương thức**
   - Chọn loại phù hợp dựa trên chiến lược định giá của bạn
   - Loại xác định các trường cấu hình chi phí có sẵn

3. **Cấu hình Thông tin Cơ bản**
   - Tên: Tên tham chiếu nội bộ (ví dụ: "domestic_ground")
   - Tên hiển thị: Tên hiển thị cho khách hàng (ví dụ: "Vận chuyển đường bộ")
   - Mô tả: Khung thời gian giao hàng (ví dụ: "5-7 ngày làm việc")

4. **Thiết lập Tính toán Chi phí**
   - **Mức giá cố định**: Nhập chi phí cố định
   - **Theo trọng lượng/Theo giá trị/Theo bảng giá**: Tạo bảng giá (xem bên dưới)
   - **Thời gian thực**: Liên kết tài khoản nhà cung cấp
   - **Miễn phí/Lấy hàng**: Không cần cấu hình chi phí

5. **Thêm Giới hạn (Tùy chọn)**
   - Giá trị đơn hàng tối thiểu/tối đa
   - Trọng lượng tối thiểu/tối đa
   - Khu vực vận chuyển

6. **Thiết lập Ưu tiên**
   - Số nhỏ hơn hiển thị trước tại bước thanh toán
   - Gợi ý thứ tự: Miễn phí (1), Lấy hàng tại địa điểm (2), Tiêu chuẩn (3), Nhanh (4)

7. **Kích hoạt Phương thức**
   - Chuyển đổi "Kích hoạt" = Có
   - Lưu

---

## Tạo Bảng Giá

Đối với phương thức theo trọng lượng, theo giá trị và theo bảng giá:

**Bước 1: Tạo Bảng Giá**
- Đi đến Cài đặt > Vận chuyển > Bảng Giá
- Nhấp vào "Thêm Bảng Giá"
- Thiết lập **Tên** (ví dụ: "Cấp bậc trọng lượng trong nước")
- Thiết lập **Loại cơ sở**: trọng lượng, giá trị hoặc số lượng

**Bước 2: Thêm Cấp bậc**
- Nhấp vào "Thêm Cấp bậc"
- Thiết lập **Giá trị tối thiểu** và **Giá trị tối đa** (khoảng giá trị để khớp)
- Thiết lập **Giá** (chi phí cho cấp bậc này)
- Tùy chọn: Giới hạn cho khu vực hoặc quốc gia cụ thể
- Lưu cấp bậc

**Bước 3: Lặp lại cho tất cả các cấp bậc**
- Bao phủ toàn bộ khoảng (từ 0 đến giá trị tối đa dự kiến)
- Đảm bảo không có khoảng trống (ví dụ: 0-5, 5-10, 10-20, 20+)
- Sử dụng `null` cho giá trị tối đa trong cấp bậc cuối cùng (vô hạn)

**Bước 4: Liên kết với Phương thức Vận chuyển**
- Chỉnh sửa phương thức vận chuyển
- Chọn bảng giá từ danh sách thả xuống
- Lưu

**Ví dụ Bảng Giá theo trọng lượng**:
```
Tên: Cấp bậc trọng lượng trong nước
Loại cơ sở: Trọng lượng

Cấp bậc:
1. Giá trị tối thiểu: 0g, Giá trị tối đa: 2000g, Giá: $8
2. Giá trị tối thiểu: 2000g, Giá trị tối đa: 5000g, Giá: $12
3. Giá trị tối thiểu: 5000g, Giá trị tối đa: 10000g, Giá: $18
4. Giá trị tối thiểu: 10000g, Giá trị tối đa: null, Giá: $25
```

---

## Các tình huống vận chuyển phổ biến

### Tình huống 1: Vận chuyển trong nước cơ bản

**Mục tiêu**: Mức giá cố định $9.99 cho tất cả các đơn hàng trong nước.

**Giải pháp**:
- Loại phương thức: Mức giá cố định
- Chi phí cố định: $9.99
- Khu vực vận chuyển: "Trong nước" (chỉ quốc gia của bạn)

---

### Tình huống 2: Miễn phí vận chuyển khi đơn hàng trên $50

**Mục tiêu**: Khuyến khích giá trị giỏ hàng cao hơn bằng ngưỡng miễn phí vận chuyển.

**Giải pháp Tùy chọn A** (Khuyến nghị):
- Loại phương thức: Miễn phí vận chuyển
- Giá trị đơn hàng tối thiểu: $50
- Tên hiển thị: "Miễn phí vận chuyển (Đơn hàng $50+)")

**Giải pháp Tùy chọn B** (Sử dụng quy tắc):
- Loại phương thức: Mức giá cố định
- Chi phí cố định: $9.99
- Tạo quy tắc vận chuyển:
  - Điều kiện: Giá trị giỏ hàng ≥ $50
  - Hành động: Đặt chi phí thành $0

---

### Tình huống 3: Vận chuyển theo trọng lượng trong nước + quốc tế

**Mục tiêu**: Mức giá khác nhau cho trong nước và quốc tế dựa trên trọng lượng.

**Giải pháp**:
1. Tạo 2 khu vực: "Trong nước", "Quốc tế"
2. Tạo 2 bảng giá: "Trọng lượng trong nước", "Trọng lượng quốc tế"
3. Tạo 2 phương thức:
   - "Vận chuyển trong nước" → liên kết với khu vực trong nước + bảng giá trọng lượng trong nước
   - "Vận chuyển quốc tế" → liên kết với khu vực quốc tế + bảng giá trọng lượng quốc tế

---

### Tình huống 4: Nhiều lựa chọn nhà vận chuyển

**Mục tiêu**: Cho phép khách hàng chọn giữa FedEx Ground, FedEx Express, UPS Ground.

**Giải pháp**:
1. Tạo Tài khoản Nhà cung cấp cho API FedEx
2. Tạo Tài khoản Nhà cung cấp cho API UPS
3. Tạo 3 phương thức thời gian thực:
   - "FedEx Ground" → nhà cung cấp FedEx, mã dịch vụ = "FEDEX_GROUND"
   - "FedEx Express" → nhà cung cấp FedEx, mã dịch vụ = "FEDEX_EXPRESS"
   - "UPS Ground" → nhà cung cấp UPS, mã dịch vụ = "UPS_GROUND"
4. Tất cả 3 phương thức sẽ truy xuất API nhà cung cấp tại bước thanh toán và hiển thị mức giá thời gian thực

---

### Tình huống 5: Lấy hàng tại địa điểm + Giao hàng

**Mục tiêu**: Cửa hàng bán lẻ cung cấp cả lựa chọn lấy hàng và giao hàng.

**Giải pháp**:
1. Tạo Địa điểm: "Cửa hàng chính" với địa chỉ, giờ làm việc, thời gian chuẩn bị
2. Tạo 2 phương thức:
   - "Lấy hàng tại địa điểm" → loại phương thức Lấy hàng tại địa điểm, liên kết với địa điểm Cửa hàng chính
   - "Giao hàng tiêu chuẩn" → phương thức mức giá cố định $9.99
3. Khách hàng sẽ thấy cả hai lựa chọn tại bước thanh toán

---

## Kiểm tra phương thức vận chuyển

Trước khi đưa vào vận hành, hãy kiểm tra tất cả phương thức:

1. **Tạo giỏ hàng kiểm tra**
   - Thêm các sản phẩm với trọng lượng/giá trị khác nhau
   - Tiến hành thanh toán

2. **Kiểm tra từng phương thức**
   - Nhập địa chỉ ở các khu vực khác nhau
   - Xác nhận các phương thức phù hợp hiển thị
   - Kiểm tra chi phí tính toán khớp với kỳ vọng

3. **Kiểm tra giới hạn**
   - Thêm mặt hàng cho đến khi đạt giá trị đơn hàng tối thiểu → xác nhận miễn phí vận chuyển hiển thị
   - Thêm mặt hàng nặng → xác nhận các cấp bậc theo trọng lượng hoạt động
   - Kiểm tra giới hạn khu vực → xác nhận phương thức bị ẩn cho các khu vực bị loại

4. **Kiểm tra phương thức thời gian thực** (nếu áp dụng)
   - Sử dụng thông tin xác thực nhà cung cấp kiểm tra
   - Xác nhận mức giá được trả về thành công
   - Kiểm tra tính chính xác của mức giá so với trang web nhà cung cấp

---

## Khắc phục sự cố

**Vấn đề 1: Phương thức không hiển thị tại bước thanh toán**

**Nguyên nhân**:
- Phương thức không được kích hoạt
- Giá trị giỏ hàng không đạt giá trị đơn hàng tối thiểu/tối đa
- Trọng lượng giỏ hàng không đạt trọng lượng tối thiểu
- Địa chỉ khách hàng không khớp với bất kỳ khu vực nào được liên kết
- Không có cấp bậc bảng giá nào bao phủ trọng lượng/giá trị giỏ hàng

**Giải pháp**: Kiểm tra giới hạn, xác nhận trạng thái kích hoạt, đảm bảo các khu vực/cấp bậc bao phủ tình huống của khách hàng.

---

**Vấn đề 2: Mức giá thời gian thực không thành công**

**Nguyên nhân**:
- Thông tin xác thực API không hợp lệ
- Tài khoản nhà cung cấp không hoạt động
- Không có gói vận chuyển được định nghĩa (nhà cung cấp cần kích thước)
- Địa chỉ xuất phát không được thiết lập
- API nhà cung cấp bị lỗi

**Giải pháp**: Kiểm tra kết nối nhà cung cấp, xác nhận thông tin xác thực, đảm bảo gói được cấu hình, kiểm tra địa chỉ xuất phát trong cài đặt.

---

**Vấn đề 3: Chi phí được tính sai**

**Nguyên nhân**:
- Các cấp bậc bảng giá có khoảng trống hoặc chồng chéo
- Giá trị tối thiểu/tối đa của cấp bậc không đúng đơn vị (gram vs kg)
- Phí xử lý được thêm bất ngờ
- Quy tắc vận chuyển thay đổi chi phí

**Giải pháp**: Xem lại các cấp bậc bảng giá, xác nhận đơn vị, kiểm tra độ ưu tiên của quy tắc vận chuyển.

---

## Một số mẹo

- **Bắt đầu đơn giản** - Sử dụng phương thức mức giá cố định cho phương thức đầu tiên, thêm độ phức tạp khi cần thiết
- **Kiểm tra kỹ lưỡng** - Xác nhận tất cả phương thức hoạt động trong môi trường thử nghiệm trước khi kích hoạt trong sản xuất
- **Sử dụng tên mô tả** - "Vận chuyển tiêu chuẩn (5-7 ngày)" tốt hơn "Phương thức 1"
- **Đặt khung thời gian giao hàng thực tế** - Hứa hẹn ít hơn, giao hàng nhiều hơn để đảm bảo sự hài lòng của khách hàng
- **Cung cấp tùy chọn lấy hàng nếu có thể** - Giảm chi phí vận chuyển, cải thiện sự tiện lợi cho khách hàng
- **Theo dõi độ tin cậy API nhà cung cấp** - Có phương thức mức giá cố định dự phòng nếu mức giá thời gian thực không hoạt động
- **Sử dụng khu vực cho vận chuyển quốc tế** - Mức giá khác nhau theo khu vực giúp tránh tổn thất trên các điểm đến đắt đỏ
- **Kết hợp với quy tắc vận chuyển** - Quy tắc thêm logic điều kiện (khuyến mãi miễn phí vận chuyển, phụ phí cho khu vực hẻo lánh)
- **Giữ phương thức giới hạn** - 2-4 lựa chọn tại bước thanh toán giúp tránh tình trạng bế tắc trong quyết định
- **Cập nhật bảng giá theo mùa** - Mức giá nhà cung cấp thay đổi, xem xét hàng năm
- **Sử dụng ưu tiên một cách khôn ngoan** - Đặt các phương thức miễn phí/đắt tiền ở đầu, phương thức đắt tiền ở cuối
