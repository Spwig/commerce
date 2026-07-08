---
title: Quy tắc vận chuyển
---

Các quy tắc vận chuyển áp dụng các điều chỉnh chi phí có điều kiện cho các phương thức vận chuyển dựa trên nội dung giỏ hàng, thuộc tính khách hàng và khu vực giao hàng - tự động cung cấp vận chuyển miễn phí cho đơn hàng trên $50, thêm phụ phí cho khu vực hẻo lánh hoặc giảm giá vận chuyển cho khách hàng VIP. Các quy tắc sử dụng việc thực thi dựa trên độ ưu tiên (ưu tiên cao trước) với tùy chọn cờ dừng để ngăn xử lý tiếp theo. Mỗi quy tắc đánh giá nhiều điều kiện (giá trị giỏ hàng, trọng lượng, khu vực, sản phẩm, nhóm khách hàng) và thực thi một trong 6 loại điều chỉnh khi tất cả điều kiện khớp.

Sử dụng quy tắc vận chuyển khi bạn cần chi phí vận chuyển động thay đổi dựa trên ngữ cảnh đơn hàng, không chỉ là tỷ lệ cố định từ phương thức vận chuyển.

## Loại quy tắc vận chuyển

Các quy tắc áp dụng 6 loại điều chỉnh chi phí:

### Giảm giá phần trăm

**Chức năng**: Giảm chi phí vận chuyển theo tỷ lệ phần trăm (ví dụ: giảm 25%)

**Công thức**: `new_cost = base_cost × (1 - percent/100)`

**Ví dụ**:
```
Chi phí cơ bản: $20
Giảm giá: 25%
Kết quả: $15
```

**Trường hợp sử dụng**:
- Giảm giá vận chuyển cho khách hàng VIP (giảm 20% cho tất cả vận chuyển)
- Khuyến mãi theo mùa (giảm 15% vận chuyển trong tháng 12)
- Giảm giá vận chuyển cho đơn hàng số lượng lớn (giảm 10% vận chuyển cho 5+ mặt hàng)

---

### Giảm giá cố định

**Chức năng**: Trừ một khoản cố định khỏi chi phí vận chuyển.

**Công thức**: `new_cost = base_cost - amount` (tối thiểu $0)

**Ví dụ**:
```
Chi phí cơ bản: $15
Giảm giá: $5
Kết quả: $10
```

**Trường hợp sử dụng**:
- Ưu đãi cho khách hàng mới (giảm $5 phí vận chuyển cho đơn hàng đầu tiên)
- Phần thưởng đăng ký bản tin (giảm $3 phí vận chuyển)
- Lợi ích chương trình khách hàng thân thiết (giảm $10 phí vận chuyển mỗi tháng)

---

### Đặt chi phí

**Chức năng**: Ghi đè chi phí vận chuyển thành một số cụ thể.

**Công thức**: `new_cost = fixed_amount`

**Ví dụ**:
```
Chi phí cơ bản: $25
Đặt thành: $9.99
Kết quả: $9.99
```

**Trường hợp sử dụng**:
- Khuyến mãi flash (phí vận chuyển cố định $5 cho tất cả đơn hàng hôm nay)
- Vận chuyển theo danh mục cụ thể (sách luôn có phí vận chuyển $3.99)
- Khuyến mãi theo thời gian (phí vận chuyển tối đa $9.99 trong tuần này)

---

### Vận chuyển miễn phí

**Chức năng**: Đặt chi phí vận chuyển thành $0.

**Công thức**: `new_cost = $0`

**Ví dụ**:
```
Chi phí cơ bản: $18
Quy tắc áp dụng
Kết quả: $0
```

**Trường hợp sử dụng**:
- Vận chuyển miễn phí cho đơn hàng trên $50
- Vận chuyển miễn phí cho sản phẩm cụ thể (sản phẩm khuyến mãi)
- Vận chuyển miễn phí cho khách hàng VIP
- Vận chuyển miễn phí cho đơn hàng có 3+ mặt hàng

---

### Phụ phí (Cố định)

**Chức năng**: Thêm một khoản cố định vào chi phí vận chuyển.

**Công thức**: `new_cost = base_cost + amount`

**Ví dụ**:
```
Chi phí cơ bản: $12
Phụ phí: $5
Kết quả: $17
```

**Trường hợp sử dụng**:
- Phí giao hàng khu vực hẻo lánh
- Phí xử lý mặt hàng cồng kềnh
- Phụ phí giao hàng thứ Bảy
- Phí đóng gói mặt hàng dễ vỡ

---

### Phụ phí (Phần trăm)

**Chức năng**: Tăng chi phí vận chuyển theo tỷ lệ phần trăm.

**Công thức**: `new_cost = base_cost × (1 + percent/100)`

**Ví dụ**:
```
Chi phí cơ bản: $20
Phụ phí: 15%
Kết quả: $23
```

**Trường hợp sử dụng**:
- Phụ phí cao điểm (20% trong dịp lễ)
- Phụ phí giao hàng nhanh (phụ phí 50%)
- Phụ phí nhiên liệu (biến đổi dựa trên tỷ lệ hiện tại)

---

## Điều kiện quy tắc

Các quy tắc đánh giá **Tất cả điều kiện phải được đáp ứng** để áp dụng quy tắc:

### Thời gian hiệu lực

- **Ngày bắt đầu**: Quy tắc chỉ hoạt động sau ngày này
- **Ngày kết thúc**: Quy tắc chỉ hoạt động trước ngày này
- **Trường hợp sử dụng**: Khuyến mãi theo mùa, ưu đãi giới hạn thời gian

**Ví dụ**: Vận chuyển miễn phí chỉ trong cuối tuần Black Friday
```
Ngày bắt đầu: 2026-11-27 00:00
Ngày kết thúc: 2026-11-30 23:59
```

---

### Phạm vi giá trị giỏ hàng

- **Giá trị giỏ hàng tối thiểu**: Tổng giá giỏ hàng phải ≥ số tiền
- **Giá trị giỏ hàng tối đa**: Tổng giá giỏ hàng phải ≤ số tiền
- **Trường hợp sử dụng**: Ngưỡng vận chuyển miễn phí, giảm giá theo cấp bậc

**Ví dụ**: Vận chuyển miễn phí cho đơn hàng từ $50 đến $200
```
Giá trị tối thiểu: $50
Giá trị tối đa: $200
```

---

### Phạm vi trọng lượng giỏ hàng

- **Trọng lượng tối thiểu**: Tổng trọng lượng giỏ hàng phải ≥ số tiền
- **Trọng lượng tối đa**: Tổng trọng lượng giỏ hàng phải ≤ số tiền
- **Trường hợp sử dụng**: Giảm giá cho hàng nhẹ, phụ phí cho mặt hàng nặng

**Ví dụ**: Phụ phí $5 cho đơn hàng trên 20kg
```
Trọng lượng tối thiểu: 20kg
Trọng lượng tối đa: null (không giới hạn)
```

---

### Phạm vi số lượng mặt hàng

- **Số lượng mặt hàng tối thiểu**: Giỏ hàng phải có ≥ số lượng mặt hàng
- **Số lượng mặt hàng tối đa**: Giỏ hàng phải có ≤ số lượng mặt hàng
- **Trường hợp sử dụng**: Giảm giá cho đơn hàng số lượng lớn, phí cho mặt hàng đơn lẻ

**Ví dụ**: Vận chuyển miễn phí cho 5+ mặt hàng
```
Số lượng mặt hàng tối thiểu: 5
Số lượng mặt hàng tối đa: null
```

---

### Khu vực vận chuyển

- **Khu vực**: Quy tắc chỉ áp dụng nếu địa chỉ khách hàng khớp với ít nhất một khu vực đã chọn
- **Không chọn gì**: Quy tắc áp dụng cho TẤT CẢ các khu vực
- **Trường hợp sử dụng**: Phụ phí hoặc giảm giá theo khu vực

**Ví dụ**: Vận chuyển miễn phí chỉ cho khu vực Nội địa
```
Khu vực: ["Domestic USA"]
```

---

### Phương thức vận chuyển

- **Phương thức**: Quy tắc chỉ áp dụng cho các phương thức vận chuyển cụ thể
- **Không chọn gì**: Quy tắc áp dụng cho TẤT CẢ các phương thức
- **Trường hợp sử dụng**: Khuyến mãi theo phương thức vận chuyển

**Ví dụ**: Giảm 25% cho phương thức Giao hàng Nhanh
```
Phương thức: ["Express Delivery"]
```

---

### Yêu cầu sản phẩm

**Yêu cầu sản phẩm**: Giỏ hàng phải chứa ít nhất một trong những sản phẩm này

**Yêu cầu danh mục**: Giỏ hàng phải chứa ít nhất một sản phẩm từ những danh mục này

**Trường hợp sử dụng**: Vận chuyển miễn phí theo sản phẩm, bộ sản phẩm khuyến mãi

**Ví dụ**: Vận chuyển miễn phí khi giỏ hàng chứa "Sản phẩm khuyến mãi A"
```
Yêu cầu sản phẩm: [ID sản phẩm 123]
```

---

### Loại trừ sản phẩm

**Loại trừ sản phẩm**: Quy tắc không áp dụng nếu giỏ hàng chứa bất kỳ sản phẩm nào trong số này

**Loại trừ danh mục**: Quy tắc không áp dụng nếu giỏ hàng chứa bất kỳ sản phẩm nào từ những danh mục này

**Trường hợp sử dụng**: Loại trừ các mặt hàng nặng/cồng kềnh khỏi vận chuyển miễn phí

**Ví dụ**: Vận chuyển miễn phí ngoại trừ danh mục Nội thất
```
Loại trừ danh mục: [Nội thất]
```

---

### Nhóm khách hàng

- **Nhóm khách hàng**: Quy tắc chỉ áp dụng cho khách hàng trong các nhóm đã chọn (VIP, Bán buôn, v.v.)
- **Không chọn gì**: Quy tắc áp dụng cho TẤT CẢ các nhóm khách hàng
- **Trường hợp sử dụng**: Lợi ích VIP, giảm giá bán buôn

**Ví dụ**: Giảm 15% phí vận chuyển cho thành viên VIP
```
Nhóm khách hàng: ["VIP"]
```

---

### Khách hàng mới

- **Khách hàng mới**: Chuyển đổi để giới hạn quy tắc chỉ áp dụng cho khách hàng không có đơn hàng trước
- **Trường hợp sử dụng**: Ưu đãi chào mừng khách hàng mới

**Ví dụ**: Giảm $5 phí vận chuyển cho đơn hàng đầu tiên
```
Khách hàng mới: Có
```

---

## Độ ưu tiên và thực thi quy tắc

Các quy tắc được thực thi theo **thứ tự ưu tiên** (số càng cao càng được thực thi trước):

### Cơ chế ưu tiên

**Ví dụ thực thi**:
```
Quy tắc A (Ưu tiên 100): Vận chuyển miễn phí nếu giỏ hàng > $50
Quy tắc B (Ưu tiên 50): Giảm 10% cho tất cả vận chuyển
Quy tắc C (Ưu tiên 1): Phụ phí $2 cho khu vực hẻo lánh

Giỏ hàng: $60, Khu vực hẻo lánh
Chi phí vận chuyển cơ bản: $15

Bước 1: Quy tắc A được đánh giá (Ưu tiên 100)
  Giỏ hàng > $50? CÓ
  Áp dụng: Đặt chi phí thành $0
  Chi phí hiện tại: $0

Bước 2: Quy tắc B được đánh giá (Ưu tiên 50)
  Áp dụng giảm 10% cho $0
  Chi phí hiện tại: $0 (vẫn miễn phí)

Bước 3: Quy tắc C được đánh giá (Ưu tiên 1)
  Thêm $2 phụ phí cho $0
  Chi phí hiện tại: $2

Chi phí cuối cùng: $2
```

**Cờ dừng quy tắc tiếp theo**:

Nếu Quy tắc A có `stop_further_rules = True`:
```
Quy tắc A (Ưu tiên 100, stop_further_rules=True): Vận chuyển miễn phí nếu giỏ hàng > $50
Quy tắc B (Ưu tiên 50): Giảm 10%
Quy tắc C (Ưu tiên 1): Phụ phí $2 cho khu vực hẻo lánh

Giỏ hàng: $60
Chi phí cơ bản: $15

Bước 1: Quy tắc A áp dụng, đặt chi phí thành $0
        stop_further_rules = True → DỪNG

Chi phí cuối cùng: $0 (Quy tắc B và C không bao giờ thực thi)
```

---

## Tạo quy tắc vận chuyển

**Quy trình làm việc từng bước**:

1. **Di chuyển đến Quy tắc**
   - Cài đặt > Vận chuyển > Quy tắc Vận chuyển
   - Nhấp vào "Thêm Quy tắc Vận chuyển"

2. **Cấu hình cơ bản**
   - **Tên**: Nhận dạng nội bộ (ví dụ: "Vận chuyển miễn phí cho đơn hàng trên $50")
   - **Mô tả**: Ghi chú tùy chọn (không hiển thị cho khách hàng)
   - **Kích hoạt**: Chuyển đổi để bật/tắt
   - **Ưu tiên**: Thiết lập thứ tự thực thi (100 cho ưu tiên cao, 1 cho ưu tiên thấp)

3. **Chọn loại quy tắc**
   - Chọn loại điều chỉnh (giảm giá %, giảm giá cố định, đặt chi phí, miễn phí, phụ phí %, phụ phí cố định)
   - Nhập số tiền hoặc tỷ lệ phần trăm

4. **Đặt cờ dừng** (Tùy chọn)
   - Chọn "Dừng quy tắc tiếp theo" nếu quy tắc này nên ngăn các quy tắc ưu tiên thấp hơn từ thực thi
   - Sử dụng cho các quy tắc cuối cùng/uyên tắc (ví dụ: vận chuyển miễn phí không nên có phụ phí được thêm vào sau)

5. **Định nghĩa điều kiện** (Tùy chọn - để trống để "luôn áp dụng")
   - Thời gian hiệu lực: Ngày bắt đầu/kết thúc
   - Giá trị giỏ hàng: Tối thiểu/tối đa
   - Trọng lượng giỏ hàng: Tối thiểu/tối đa
   - Số lượng mặt hàng: Tối thiểu/tối đa
   - Khu vực: Chọn khu vực áp dụng
   - Phương thức: Chọn phương thức áp dụng
   - Sản phẩm: Yêu cầu hoặc loại trừ
   - Khách hàng: Nhóm hoặc chỉ dành cho khách hàng mới

6. **Lưu quy tắc**
   - Nhấp Lưu
   - Quy tắc trở nên hoạt động ngay lập tức (nếu chuyển đổi kích hoạt là Có)

---

## Các tình huống quy tắc vận chuyển phổ biến

### Tình huống 1: Vận chuyển miễn phí cho đơn hàng trên $50

**Mục tiêu**: Cung cấp vận chuyển miễn phí khi tổng giá giỏ hàng ≥ $50.

**Cấu hình**:
```
Tên: Vận chuyển miễn phí cho đơn hàng trên $50
Loại: Vận chuyển miễn phí
Ưu tiên: 100
Điều kiện:
  Giá trị giỏ hàng tối thiểu: $50
Dừng quy tắc tiếp theo: Có
```

---

### Tình huống 2: Phụ phí khu vực hẻo lánh

**Mục tiêu**: Thêm $10 phụ phí cho giao hàng đến khu vực hẻo lánh.

**Cấu hình**:
```
Tên: Phụ phí khu vực hẻo lánh
Loại: Phụ phí (Cố định)
Số tiền: $10
Ưu tiên: 50
Điều kiện:
  Khu vực: ["Khu vực hẻo lánh"]
Dừng quy tắc tiếp theo: Không
```

---

### Tình huống 3: Giảm giá 20% cho khách hàng VIP

**Mục tiêu**: Khách hàng VIP được giảm 20% cho tất cả vận chuyển.

**Cấu hình**:
```
Tên: Giảm giá vận chuyển VIP
Loại: Giảm giá (Phần trăm)
Tỷ lệ: 20
Ưu tiên: 75
Điều kiện:
  Nhóm khách hàng: ["VIP"]
Dừng quy tắc tiếp theo: Không
```

---

### Tình huống 4: Mức giá cố định trong tháng 12

**Mục tiêu**: Tất cả vận chuyển được giới hạn ở $9.99 trong tháng 12.

**Cấu hình**:
```
Tên: Khuyến mãi giá cố định tháng 12
Loại: Đặt chi phí
Số tiền: $9.99
Ưu tiên: 100
Điều kiện:
  Ngày bắt đầu: 2026-12-01
  Ngày kết thúc: 2026-12-31
Dừng quy tắc tiếp theo: Có
```

---

### Tình huống 5: Phụ phí cho mặt hàng nặng

**Mục tiêu**: Thêm $15 phí cho đơn hàng trên 25kg.

**Cấu hình**:
```
Tên: Phụ phí đơn hàng nặng
Loại: Phụ phí (Cố định)
Số tiền: $15
Ưu tiên: 50
Điều kiện:
  Trọng lượng tối thiểu: 25kg
Dừng quy tắc tiếp theo: Không
```

---

### Tình huống 6: Vận chuyển miễn phí cho đơn hàng đầu tiên

**Mục tiêu**: Khách hàng mới được vận chuyển miễn phí cho đơn hàng đầu tiên.

**Cấu hình**:
```
Tên: Vận chuyển miễn phí cho đơn hàng đầu tiên
Loại: Vận chuyển miễn phí
Ưu tiên: 100
Điều kiện:
  Khách hàng mới: Có
Dừng quy tắc tiếp theo: Có
```

---

### Tình huống 7: Vận chuyển miễn phí cho danh mục khuyến mãi

**Mục tiêu**: Vận chuyển miễn phí cho đơn hàng chứa sản phẩm thuộc danh mục khuyến mãi.

**Cấu hình**:
```
Tên: Vận chuyển miễn phí danh mục khuyến mãi
Loại: Vận chuyển miễn phí
Ưu tiên: 90
Điều kiện:
  Yêu cầu danh mục: ["Khuyến mãi"]
Dừng quy tắc tiếp theo: Có
```

---

### Tình huống 8: Loại trừ nội thất khỏi vận chuyển miễn phí

**Mục tiêu**: Vận chuyển miễn phí cho đơn hàng trên $50, ngoại trừ nếu giỏ hàng chứa nội thất.

**Giải pháp**: Hai quy tắc

**Quy tắc 1**:
```
Tên: Vận chuyển miễn phí chung
Loại: Vận chuyển miễn phí
Ưu tiên: 50
Điều kiện:
  Giá trị giỏ hàng tối thiểu: $50
  Loại trừ danh mục: ["Nội thất"]
Dừng quy tắc tiếp theo: Không
```

**Quy tắc 2**:
```
Tên: Giảm $5 cho đơn hàng nội thất
Loại: Giảm giá (Cố định)
Số tiền: $5
Ưu tiên: 40
Điều kiện:
  Yêu cầu danh mục: ["Nội thất"]
  Giá trị giỏ hàng tối thiểu: $50
Dừng quy tắc tiếp theo: Không
```

---

## Chiến lược kết hợp quy tắc

### Chiến lược 1: Kết hợp giảm giá

**Cho phép nhiều giảm giá được kết hợp**:
```
Quy tắc A (Ưu tiên 100): Giảm 10% cho khách hàng VIP → stop_further_rules=Không
Quy tắc B (Ưu tiên 50): Giảm 15% cho đơn hàng >$100 → stop_further_rules=Không

Khách hàng VIP với đơn hàng $120:
Chi phí cơ bản: $15
Sau Quy tắc A: $13.50 (giảm 10%)
Sau Quy tắc B: $11.48 (giảm 15% từ $13.50)
```

### Chiến lược 2: Quy tắc độc quyền

**Chỉ có một quy tắc áp dụng** (ưu tiên cao nhất):
```
Quy tắc A (Ưu tiên 100): Vận chuyển miễn phí >$50 → stop_further_rules= Có
Quy tắc B (Ưu tiên 50): Giảm 20% cho tất cả vận chuyển → stop_further_rules= Có

Giỏ hàng > $50:
Quy tắc A áp dụng → Vận chuyển miễn phí → DỪNG
Quy tắc B không bao giờ thực thi
```

### Chiến lược 3: Phụ phí điều kiện

**Giảm giá trước, phụ phí sau**:
```
Quy tắc A (Ưu tiên 100): Vận chuyển miễn phí >$75
Quy tắc B (Ưu tiên 75): Giảm 15% cho khách hàng VIP
Quy tắc C (Ưu tiên 50): Giảm 10% chung
Quy tắc D (Ưu tiên 25): Phụ phí $5 cho khu vực hẻo lánh
Quy tắc E (Ưu tiên 1): Phụ phí nhiên liệu 10%

Đơn hàng: $80, Khu vực hẻo lánh, Khách hàng VIP
Chi phí cơ bản: $20
A: $80 > $75 → Miễn phí ($0)
B: VIP → Giảm 15% từ $0 = $0
C: Giảm 10% từ $0 = $0
D: Khu vực hẻo lánh +$5 = $5
E: Nhiên liệu +10% của $5 = $5.50

Kết quả cuối cùng: $5.50 (không miễn phí do phụ phí)
```

**Để ngăn điều này, sử dụng stop_further_rules= Có**:
```
Quy tắc A (Ưu tiên 100, stop= Có): Vận chuyển miễn phí >$75

Đơn hàng cùng như trên:
A: $80 > $75 → Miễn phí ($0) → DỪNG
Kết quả cuối cùng: $0 (truly miễn phí)
```

---

## Kiểm tra quy tắc vận chuyển

**Trước khi đưa vào vận hành**:

1. **Tạo giỏ hàng kiểm tra**
   - Giỏ hàng A: $25 (dưới ngưỡng)
   - Giỏ hàng B: $55 (trên ngưỡng)
   - Giỏ hàng C: $200 + Khu vực hẻo lánh
   - Giỏ hàng D: Khách hàng VIP

2. **Kiểm tra từng quy tắc**
   - Tiến hành thanh toán
   - Xác nhận chi phí vận chuyển được hiển thị đúng
   - Kiểm tra thứ tự thực thi quy tắc

3. **Kiểm tra giải quyết độ ưu tiên**
   - Nhiều quy tắc khớp
   - Xác nhận quy tắc ưu tiên cao nhất được thực thi trước
   - Kiểm tra hành vi cờ dừng quy tắc tiếp theo

4. **Kiểm tra các trường hợp biên**
   - Giá trị giỏ hàng chính xác tại ngưỡng
   - Nhiều điều kiện khớp
   - Các quy tắc xung đột

---

## Khắc phục sự cố

**Vấn đề 1: Quy tắc không áp dụng**

**Nguyên nhân**:
- Quy tắc không hoạt động
- Một hoặc nhiều điều kiện không được đáp ứng
- Quy tắc ưu tiên cao hơn đã thiết lập stop_further_rules=Yes
- Thời gian hiệu lực ngoài ngày hiện tại

**Giải pháp**: Xem lại tất cả điều kiện, kiểm tra độ ưu tiên, xác nhận trạng thái hoạt động.

---

**Vấn đề 2: Số tiền giảm giá bất ngờ**

**Nguyên nhân**:
- Nhiều quy tắc được kết hợp
- Tỷ lệ phần trăm được áp dụng cho chi phí đã được giảm giá
- Độ ưu tiên quy tắc không đúng

**Giải pháp**: Kiểm tra thứ tự ưu tiên, xem lại cờ stop_further_rules, theo dõi thực thi thủ công.

---

**Vấn đề 3: Vận chuyển miễn phí không hoạt động**

**Nguyên nhân**:
- Quy tắc phụ phí ưu tiên thấp hơn thêm chi phí sau quy tắc miễn phí
- Giá trị giỏ hàng không đạt ngưỡng tối thiểu
- Sản phẩm bị loại trừ trong giỏ hàng

**Giải pháp**: Sử dụng stop_further_rules=Yes trên quy tắc miễn phí, xác nhận điều kiện, kiểm tra các loại trừ.

---

## Một số mẹo

- **Sử dụng độ ưu tiên cao cho vận chuyển miễn phí** - Ưu tiên 100 đảm bảo nó được thực thi trước các điều chỉnh khác
- **Thiết lập cờ dừng cho các quy tắc tuyệt đối** - Vận chuyển miễn phí nên dừng xử lý tiếp theo
- **Kiểm tra sự kết hợp quy tắc** - Nhiều quy tắc có thể tương tác bất ngờ
- **Sử dụng tên mô tả** - "Giảm giá 20% VIP (Ưu tiên 75)" tốt hơn "Quy tắc 3"
- **Ghi chú logic phức tạp** - Thêm ghi chú trong trường mô tả
- **Bắt đầu với các quy tắc đơn giản** - Thêm độ phức tạp dần dần
- **Theo dõi hiệu suất quy tắc** - Kiểm tra xem quy tắc có được sử dụng hay gây hiểu lầm không
- **Tránh quá nhiều quy tắc** - Quá nhiều quy tắc làm chậm quá trình thanh toán, sử dụng 5-10 tối đa
- **Sử dụng khu vực cho địa lý** - Tốt hơn là nhiều quy tắc tương tự cho mỗi quốc gia
- **Kết hợp với phương thức** - Quy tắc + Phương thức làm việc cùng nhau cho định giá phức tạp
- **Thiết lập thời gian hiệu lực rõ ràng** - Luôn bao gồm ngày kết thúc cho khuyến mãi
- **Kiểm tra các trường hợp biên** - Chính xác $50, chính xác 5 mặt hàng, v.v.

Lưu ý: Bảo tồn toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật chính xác như được hiển thị trong các quy tắc bảo tồn.