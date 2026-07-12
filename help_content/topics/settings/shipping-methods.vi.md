---
title: Phương thức vận chuyển
---

Phương thức vận chuyển là các tùy chọn giao hàng được hiển thị cho khách hàng tại bước thanh toán—mỗi phương thức tính phí vận chuyển bằng các chiến lược định giá khác nhau. Spwig hỗ trợ 7 loại phương thức từ các mức giá cố định đơn giản đến định giá thời gian thực phức tạp được tính bởi nhà vận chuyển. Các phương thức có thể bị giới hạn bởi giá trị đơn hàng tối thiểu/tối đa, trọng lượng và các khu vực địa lý. Khách hàng chọn phương thức ưa thích của họ trong quá trình thanh toán, và chi phí được tính sẽ được thêm vào tổng đơn hàng.

Sử dụng hướng dẫn này để cấu hình các phương thức vận chuyển phù hợp với mô hình kinh doanh của bạn, từ vận chuyển theo mức giá cố định cơ bản đến định giá theo cấp bậc dựa trên khu vực phức tạp.

## Loại phương thức vận chuyển

Spwig cung cấp 7 loại phương thức vận chuyển, mỗi loại có logic tính chi phí khác nhau:

### Vận chuyển theo mức giá cố định

**Đây là gì**: Chi phí cố định, không phụ thuộc vào nội dung giỏ hàng, địa điểm hoặc trọng lượng.

**Khi sử dụng**:
- Cửa hàng đơn giản với chi phí vận chuyển dễ dự đoán
- Một loại sản phẩm (kích thước/trọng lượng tương tự)
- Giao hàng trong nước với mức giá tiêu chuẩn của nhà vận chuyển
- Khuyến mãi miễn phí vận chuyển (kết hợp với khuyến mãi vận chuyển)

**Cấu hình**:
- Thiết lập **Loại phương thức** = Vận chuyển theo mức giá cố định
- Nhập **Chi phí cố định** (ví dụ: $9.99)
- Tùy chọn: Thiết lập giới hạn giá trị đơn hàng tối thiểu/tối đa

**Ví dụ**: "Vận chuyển tiêu chuẩn - $9.99" cho tất cả các đơn hàng trong nước.

---

### Vận chuyển miễn phí

**Đây là gì**: Tùy chọn vận chuyển không mất phí (khách hàng không phải trả phí).

**Khi sử dụng**:
- Khuyến mãi vận chuyển miễn phí
- Đơn hàng có giá trị cao (kết hợp với giá trị đơn hàng tối thiểu)
- Lựa chọn nhận hàng tại chỗ địa phương
- Lợi ích chương trình khách hàng thân thiết

**Cấu hình**:
- Thiết lập **Loại phương thức** = Vận chuyển miễn phí
- Tùy chọn: Thiết lập **Giá trị đơn hàng tối thiểu** (ví dụ: miễn phí khi đơn hàng trên $50)
- Kết hợp hiệu quả với khuyến mãi vận chuyển để có vận chuyển miễn phí có điều kiện

**Ví dụ**: "Vận chuyển miễn phí cho đơn hàng trên $50" với min_order_value = $50.

---

### Vận chuyển theo trọng lượng

**Đây là gì**: Chi phí được tính dựa trên bảng giá theo cấp bậc dựa trên trọng lượng tổng giỏ hàng.

**Khi sử dụng**:
- Sản phẩm có trọng lượng biến đổi (sách, thiết bị, thực phẩm)
- Mô hình định giá của nhà vận chuyển dựa trên trọng lượng
- Tỷ lệ trọng lượng đến chi phí dễ dự đoán

**Cấu hình**:
1. Thiết lập **Loại phương thức** = Vận chuyển theo trọng lượng
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

### Vận chuyển theo giá trị đơn hàng

**Đây là gì**: Chi phí được tính dựa trên bảng giá theo cấp bậc dựa trên tổng giá trị giỏ hàng.

**Khi sử dụng**:
- Chi phí vận chuyển tương quan với giá trị đơn hàng
- Khuyến khích giá trị giỏ hàng cao hơn (giá mỗi đô la thấp hơn ở cấp bậc cao hơn)
- Lựa chọn đơn giản thay thế cho vận chuyển theo trọng lượng cho các mặt hàng có giá tương tự

**Cấu hình**:
1. Thiết lập **Loại phương thức** = Vận chuyển theo giá trị đơn hàng
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

### Mức giá vận chuyển thời gian thực

**Đây là gì**: Mức giá thời gian thực được lấy từ API của nhà vận chuyển (FedEx, UPS, DHL) tại bước thanh toán.

**Khi sử dụng**:
- Chi phí vận chuyển thay đổi theo địa điểm
- Nhiều lựa chọn nhà vận chuyển cho khách hàng
- Định giá chính xác của nhà vận chuyển mà không cần bảng giá thủ công
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
- Các gói vận chuyển được định nghĩa (để tính trọng lượng theo kích thước)


**Ví dụ**: Phương thức "FedEx Ground" lấy giá FedEx theo thời gian thực dựa trên trọng lượng, kích thước và điểm đến của giỏ hàng tại thời điểm thanh toán.

**Cách hoạt động**:
1. Khách hàng nhập địa chỉ tại thời điểm thanh toán
2. Hệ thống gọi API của nhà vận chuyển với điểm xuất phát, điểm đến, kích thước và trọng lượng gói hàng
3. Nhà vận chuyển trả về báo giá
4. Áp dụng markup (nếu có)
5. Hiển thị giá cho khách hàng

---

### Lấy hàng tại chỗ

**Đây là gì**: Khách hàng tự đến lấy hàng tại địa điểm vật lý (không có phí giao hàng).

**Khi nào nên sử dụng**:
- Cửa hàng bán lẻ cung cấp dịch vụ lấy hàng
- Lấy hàng tại kho
- Các sự kiện hoặc chợ
- Loại bỏ phí vận chuyển cho khách hàng địa phương

**Cấu hình**:
1. Thiết lập **Loại phương thức** = Lấy hàng tại chỗ
2. Tạo **Địa điểm** (Cài đặt > Vận chuyển > Địa điểm)
   - Thiết lập địa chỉ, giờ làm việc, khả năng lấy hàng
3. Liên kết địa điểm với phương thức
4. Tùy chọn: Thiết lập thời gian chuẩn bị lấy hàng (ví dụ: "Sẵn sàng trong 2 giờ")

**Trải nghiệm của khách hàng**:
- Chọn "Lấy hàng tại chỗ" tại thời điểm thanh toán
- Chọn địa điểm lấy hàng (nếu có nhiều địa điểm)
- Chọn ngày/giờ lấy hàng dựa trên khả năng
- Nhận thông báo khi đơn hàng sẵn sàng

**Ví dụ**: "Lấy hàng tại cửa hàng - Miễn phí" với 3 địa điểm bán lẻ, sẵn sàng trong vòng 24 giờ.

---

### Vận chuyển theo bảng giá

**Đây là gì**: Giá vận chuyển linh hoạt theo cấp bậc dựa trên trọng lượng, giá hoặc số lượng với mục tiêu khu vực nâng cao.

**Khi nào nên sử dụng**:
- Giá vận chuyển phức tạp (khác nhau theo khu vực và trọng lượng)
- Cần kiểm soát nhiều hơn so với chỉ dựa trên trọng lượng hoặc giá
- Nhiều yếu tố giá (ví dụ: trọng lượng + điểm đến + số lượng)

**Cấu hình**:
1. Thiết lập **Loại phương thức** = Vận chuyển theo bảng giá
2. Tạo **Bảng giá vận chuyển**
3. Định nghĩa **Loại cơ sở**: trọng lượng, giá hoặc số lượng
4. Thêm **Cấp bậc giá vận chuyển** với giá trị tối thiểu/tối đa
5. Tùy chọn: Giới hạn cấp bậc theo khu vực cụ thể hoặc quốc gia

**Khác với vận chuyển theo trọng lượng/giá**: Vận chuyển theo bảng giá hỗ trợ giới hạn địa lý theo từng cấp bậc, cho phép giá khác nhau cho cùng trọng lượng/giá trong các khu vực khác nhau.

**Ví dụ**:
```
Khu vực A (Trong nước):
  0-5kg: $10
  5-10kg: $15

Khu vực B (Ngoài khu vực):
  0-5kg: $18
  5-10kg: $25
```

**Cách hoạt động**: Giỏ hàng tính giá trị cơ sở (trọng lượng/giá/số lượng) → tìm cấp bậc phù hợp với khu vực của khách hàng → trả về giá của cấp bậc đó.

---

## Cấu hình phương thức vận chuyển

Tất cả phương thức vận chuyển đều chia sẻ các cài đặt chung sau:

### Cài đặt cơ bản

- **Tên**: Tên nội bộ (không hiển thị cho khách hàng)
- **Tên hiển thị**: Tên hiển thị cho khách hàng tại thời điểm thanh toán (ví dụ: "Vận chuyển tiêu chuẩn", "Giao hàng nhanh")
- **Mô tả**: Văn bản hỗ trợ tùy chọn hiển thị tại thời điểm thanh toán (ví dụ: "Giao hàng trong 3-5 ngày làm việc")
- **Loại phương thức**: Một trong 7 loại trên
- **Kích hoạt**: Chuyển đổi để bật/tắt phương thức mà không xóa

### Cài đặt chi phí

- **Chi phí cố định**: Chỉ dành cho phương thức giá cố định
- **Bảng giá**: Dành cho phương thức theo trọng lượng, theo giá, theo bảng giá
- **Tài khoản nhà cung cấp**: Dành cho phương thức vận chuyển theo thời gian thực
- **Lớp thuế**: Áp dụng thuế cho chi phí vận chuyển (nếu có)

### Giới hạn

**Giới hạn giá trị đơn hàng**:
- **Giá trị đơn hàng tối thiểu**: Phương thức chỉ có sẵn nếu tổng giỏ hàng ≥ số tiền (ví dụ: giao hàng miễn phí khi mua trên $50)
- **Giá trị đơn hàng tối đa**: Phương thức ẩn nếu tổng giỏ hàng > số tiền (ví dụ: giá cố định chỉ dành cho đơn hàng dưới $100)

**Giới hạn trọng lượng**:
- **Trọng lượng tối thiểu**: Phương thức chỉ có sẵn nếu trọng lượng giỏ hàng ≥ số lượng
- **Trọng lượng tối đa**: Phương thức ẩn nếu trọng lượng giỏ hàng > số lượng (thường gặp ở các phương thức vận chuyển dành cho hàng nhẹ)

**Giới hạn địa lý**:
- **Khu vực vận chuyển**: Liên kết phương thức với khu vực cụ thể (trong nước, quốc tế, khu vực)
- Khu vực trống = có sẵn cho tất cả địa chỉ
- Nhiều khu vực = có sẵn cho bất kỳ khu vực nào phù hợp

### Cài đặt nâng cao

- **Ưu tiên**: Thứ tự hiển thị tại thời điểm thanh toán (số nhỏ hơn = hiển thị cao hơn trong danh sách)
- **Phí xử lý**: Phí cố định bổ sung được thêm vào chi phí đã tính
- **Ngưỡng miễn phí vận chuyển**: Đặt chi phí thành $0 nếu tổng giỏ hàng ≥ ngưỡng (thay thế cho min_order_value)

---

## Tạo phương thức vận chuyển

**Quy trình từng bước**:

1. **Di chuyển đến phương thức vận chuyển**
   - Đi đến Cài đặt > Giỏ hàng > Phương thức vận chuyển
   - Nhấp vào "Thêm phương thức vận chuyển"


2. **Chọn Loại Phương Pháp**
   - Chọn loại phù hợp dựa trên chiến lược giá của bạn
   - Loại xác định các trường cấu hình chi phí có sẵn

3. **Cấu Hình Thông Tin Cơ Bản**
   - Tên: Tham chiếu nội bộ (ví dụ: "domestic_ground")
   - Tên Hiển Thị: Hướng đến khách hàng (ví dụ: "Ground Shipping")
   - Mô Tả: Khung thời gian giao hàng (ví dụ: "5-7 ngày làm việc")

4. **Thiết Lập Tính Toán Chi Phí**
   - **Giá Cố Định**: Nhập chi phí cố định
   - **Cân Nặng/Giá/Bảng Giá**: Tạo bảng giá (xem bên dưới)
   - **Thực Tế**: Liên kết tài khoản nhà cung cấp
   - **Miễn Phí/Lấy Tại Tiệm**: Không cần cấu hình chi phí

5. **Thêm Các Giới Hạn (Tùy Chọn)**
   - Giá trị đơn hàng tối thiểu/tối đa
   - Cân nặng tối thiểu/tối đa
   - Khu vực giao hàng

6. **Thiết Lập Ưu Tiên**
   - Số nhỏ hơn sẽ hiển thị trước tại thanh toán
   - Thứ tự được khuyến nghị: Miễn phí (1), Lấy tại tiệm (2), Tiêu chuẩn (3), Nhanh (4)

7. **Kích Hoạt Phương Pháp**
   - Bật "Hoạt động" = Có
   - Lưu

---

## Tạo Bảng Giá

Đối với phương pháp dựa trên cân nặng, giá và bảng giá:

**Bước 1: Tạo Bảng Giá**
- Đi đến Cài đặt > Giao hàng > Bảng Giá
- Nhấp vào "Thêm Bảng Giá"
- Thiết lập **Tên** (ví dụ: "Domestic Weight Tiers")
- Thiết lập **Loại Cơ Sở**: cân nặng, giá hoặc số lượng

**Bước 2: Thêm Các Cấp**
- Nhấp vào "Thêm Cấp"
- Thiết lập **Giá Trị Tối Thiểu** và **Giá Trị Tối Đa** (khoảng để khớp)
- Thiết lập **Giá** (chi phí cho cấp này)
- Tùy chọn: Giới hạn cho các khu vực hoặc quốc gia cụ thể
- Lưu cấp

**Bước 3: Lặp Lại Cho Tất Cả Các Cấp**
- Bao phủ toàn bộ phạm vi (từ 0 đến giá trị tối đa dự kiến)
- Đảm bảo không có khoảng trống (ví dụ: 0-5, 5-10, 10-20, 20+)
- Sử dụng `null` cho giá trị tối đa trong cấp cuối cùng (vô hạn)

**Bước 4: Liên Kết Với Phương Pháp Giao Hàng**
- Chỉnh sửa phương pháp giao hàng
- Chọn bảng giá từ danh sách thả xuống
- Lưu

**Ví Dụ Bảng Giá Dựa Trên Cân Nặng**:
```
Tên: Domestic Weight Tiers
Cơ Sở: Cân nặng

Các Cấp:
1. Min: 0g, Max: 2000g, Rate: $8
2. Min: 2000g, Max: 5000g, Rate: $12
3. Min: 5000g, Max: 10000g, Rate: $18
4. Min: 10000g, Max: null, Rate: $25
```

---

## Các Tình Huống Giao Hàng Thường Gặp

### Tình Huống 1: Giao Hàng Nội Địa Cơ Bản

**Mục tiêu**: Giá cố định $9.99 cho tất cả các đơn hàng nội địa.

**Giải Pháp**:
- Loại Phương Pháp: Giá Cố Định
- Chi Phí Cố Định: $9.99
- Khu Vực Giao Hàng: "Nội Địa" (chỉ quốc gia của bạn)

---

### Tình Huống 2: Miễn Phí Giao Hàng Trên $50

**Mục tiêu**: Khuyến khích giá trị giỏ hàng cao hơn với ngưỡng miễn phí giao hàng.

**Giải Pháp Tùy Chọn A** (Khuyến nghị):
- Loại Phương Pháp: Miễn Phí Giao Hàng
- Giá Trị Đơn Hàng Tối Thiểu: $50
- Tên Hiển Thị: "Free Shipping (Orders $50+)"

**Giải Pháp Tùy Chọn B** (Sử dụng Quy tắc):
- Loại Phương Pháp: Giá Cố Định
- Chi Phí Cố Định: $9.99
- Tạo Khuyến Mãi Giao Hàng:
  - Điều Kiện: Giá trị giỏ hàng ≥ $50
  - Hành Động: Đặt chi phí thành $0

---

### Tình Huống 3: Giao Hàng Nội Địa + Quốc Tế Dựa Trên Cân Nặng

**Mục tiêu**: Các mức giá khác nhau cho nội địa và quốc tế dựa trên cân nặng.

**Giải Pháp**:
1. Tạo 2 khu vực: "Nội Địa", "Quốc Tế"
2. Tạo 2 bảng giá: "Domestic Weight", "International Weight"
3. Tạo 2 phương pháp:
   - "Giao Hàng Nội Địa" → liên kết với khu vực Nội Địa + bảng giá Domestic Weight
   - "Giao Hàng Quốc Tế" → liên kết với khu vực Quốc Tế + bảng giá International Weight

---

### Tình Huống 4: Nhiều Lựa Chọn Nhà Cung Cấp

**Mục tiêu**: Cho phép khách hàng chọn giữa FedEx Ground, FedEx Express, UPS Ground.

**Giải Pháp**:
1. Tạo Tài Khoản Nhà Cung Cấp cho API của FedEx
2. Tạo Tài Khoản Nhà Cung Cấp cho API của UPS
3. Tạo 3 phương pháp thời gian thực:
   - "FedEx Ground" → nhà cung cấp FedEx, mã dịch vụ = "FEDEX_GROUND"
   - "FedEx Express" → nhà cung cấp FedEx, mã dịch vụ = "FEDEX_EXPRESS"
   - "UPS Ground" → nhà cung cấp UPS, mã dịch vụ = "UPS_GROUND"
4. Tất cả 3 phương pháp sẽ truy vấn API của nhà cung cấp tại thời điểm thanh toán và hiển thị giá hiện tại

---

### Tình Huống 5: Lấy Tại Tiệm + Giao Hàng

**Mục tiêu**: Cửa hàng bán lẻ cung cấp cả tùy chọn lấy tại tiệm và giao hàng.

**Giải Pháp**:
1. Tạo Địa Điểm: "Main Store" với địa chỉ, giờ làm việc, thời gian chuẩn bị
2. Tạo 2 phương pháp:
   - "Lấy Tại Tiệm" → loại Lấy Tại Tiệm, liên kết với địa điểm Main Store
   - "Giao Hàng Tiêu Chuẩn" → loại Giá Cố Định $9.99
3. Khách hàng sẽ thấy cả hai tùy chọn tại thời điểm thanh toán

---

## Kiểm Thử Các Phương Pháp Giao Hàng

Trước khi triển khai, kiểm thử tất cả các phương pháp:


1. **Tạo giỏ hàng kiểm tra**
   - Thêm các sản phẩm với trọng lượng/giá khác nhau
   - Tiếp tục thanh toán

2. **Kiểm tra từng phương pháp**
   - Nhập địa chỉ ở các khu vực khác nhau
   - Xác nhận các phương pháp phù hợp hiển thị
   - Kiểm tra chi phí tính toán khớp với kỳ vọng

3. **Kiểm tra các hạn chế**
   - Thêm các mặt hàng cho đến khi đạt giá trị đơn hàng tối thiểu → xác nhận phương pháp giao hàng miễn phí hiển thị
   - Thêm các mặt hàng nặng → xác nhận các cấp độ dựa trên trọng lượng hoạt động
   - Kiểm tra các hạn chế khu vực → xác nhận phương pháp bị ẩn đối với các khu vực bị loại trừ

4. **Kiểm tra phương pháp thời gian thực** (nếu áp dụng)
   - Sử dụng thông tin xác thực kiểm tra của nhà vận chuyển
   - Xác nhận các mức giá được trả về thành công
   - Kiểm tra tính chính xác của mức giá so với trang web của nhà vận chuyển

---

## Khắc phục sự cố

**Vấn đề 1: Phương pháp không hiển thị tại thanh toán**

**Nguyên nhân**:
- Phương pháp không hoạt động
- Giỏ hàng không đạt giá trị đơn hàng tối thiểu/tối đa
- Giỏ hàng không đạt trọng lượng tối thiểu/tối đa
- Địa chỉ khách hàng không khớp với bất kỳ khu vực nào được liên kết
- Không có cấp độ bảng giá nào bao phủ trọng lượng/giá của giỏ hàng

**Giải pháp**: Kiểm tra các hạn chế, xác nhận trạng thái hoạt động, đảm bảo các khu vực/cấp độ bao phủ tình huống của khách hàng.

---

**Vấn đề 2: Mức giá thời gian thực thất bại**

**Nguyên nhân**:
- Thông tin xác thực API không hợp lệ
- Tài khoản nhà cung cấp không hoạt động
- Không có gói giao hàng được định nghĩa (nhà cung cấp cần kích thước)
- Địa chỉ nguồn chưa được thiết lập
- API nhà cung cấp bị lỗi

**Giải pháp**: Kiểm tra kết nối nhà cung cấp, xác nhận thông tin xác thực, đảm bảo các gói được cấu hình, kiểm tra địa chỉ nguồn trong cài đặt.

---

**Vấn đề 3: Chi phí tính toán không chính xác**

**Nguyên nhân**:
- Các cấp độ bảng giá có khoảng trống hoặc chồng chéo
- Giá trị tối thiểu/tối đa của cấp độ ở đơn vị sai (gram so với kg)
- Phí xử lý được thêm bất ngờ
- Quy tắc giao hàng thay đổi chi phí

**Giải pháp**: Xem xét lại các cấp độ bảng giá, xác nhận đơn vị, kiểm tra độ ưu tiên của chương trình khuyến mãi giao hàng.

---

## Mẹo

- **Bắt đầu đơn giản** - Sử dụng phương pháp giá cố định cho phương pháp đầu tiên, thêm độ phức tạp khi cần
- **Kiểm tra kỹ lưỡng** - Xác nhận tất cả phương pháp hoạt động trong môi trường staging trước khi kích hoạt trong sản xuất
- **Sử dụng tên mô tả** - "Giao hàng tiêu chuẩn (5-7 ngày)" tốt hơn "Phương pháp 1"
- **Thiết lập thời gian giao hàng thực tế** - Hứa hẹn ít hơn, giao hàng nhiều hơn để đảm bảo sự hài lòng của khách hàng
- **Cung cấp tùy chọn nhận hàng nếu có thể** - Giảm chi phí giao hàng, cải thiện sự tiện lợi cho khách hàng
- **Theo dõi độ tin cậy API nhà cung cấp** - Có phương pháp giá cố định dự phòng nếu mức giá thời gian thực thất bại
- **Sử dụng khu vực cho quốc tế** - Các mức giá khác nhau theo khu vực giúp tránh thua lỗ trên các điểm đến đắt đỏ
- **Kết hợp với chương trình khuyến mãi giao hàng** - Các quy tắc thêm logic điều kiện (chương trình miễn phí giao hàng, phụ phí cho khu vực hẻo lánh)
- **Giữ phương pháp giới hạn** - 2-4 tùy chọn tại thanh toán giúp tránh tình trạng bế tắc trong quyết định
- **Cập nhật bảng giá theo mùa** - Mức giá nhà cung cấp thay đổi, xem xét hàng năm
- **Sử dụng độ ưu tiên một cách khôn ngoan** - Đặt các phương pháp miễn phí/đắt tiền ở đầu, các phương pháp đắt đỏ ở cuối