---
title: Quy tắc vận chuyển
---

Các quy tắc vận chuyển áp dụng các điều chỉnh chi phí dựa trên nội dung giỏ hàng, thuộc tính khách hàng và khu vực giao hàng—tự động cung cấp vận chuyển miễn phí khi hóa đơn trên $50, thêm phí cho khu vực hẻo lánh, hoặc giảm giá vận chuyển cho khách hàng VIP. Các quy tắc sử dụng trình tự ưu tiên (ưu tiên cao hơn trước) với cờ dừng tùy chọn để ngăn việc xử lý tiếp theo. Mỗi quy tắc đánh giá nhiều điều kiện (giá trị giỏ hàng, trọng lượng, khu vực, sản phẩm, nhóm khách hàng) và thực hiện một trong 6 loại điều chỉnh khi tất cả các điều kiện khớp nhau.

Sử dụng các quy tắc vận chuyển khi bạn cần chi phí vận chuyển động, thay đổi dựa trên bối cảnh đơn hàng, không chỉ các mức giá cố định từ phương thức vận chuyển.

## Các loại quy tắc vận chuyển

Các quy tắc vận chuyển áp dụng 6 loại điều chỉnh chi phí:

### Giảm giá theo phần trăm

**Nó làm gì**: Giảm chi phí vận chuyển theo phần trăm (ví dụ: 25% off).

**Công thức**: `new_cost = base_cost × (1 - percent/100)`

**Ví dụ**:
```
Chi phí cơ sở: $20
Chiết khấu: 25%
Kết quả: $15
```

**Trường hợp sử dụng**:
- Giảm giá cho khách hàng VIP (20% off tất cả chi phí vận chuyển)
- Chiến dịch theo mùa (15% off vận chuyển vào tháng 12)
- Giảm giá theo số lượng (10% off vận chuyển cho 5+ mặt hàng)

---

### Giảm giá cố định

**Nó làm gì**: Trừ một khoản cố định khỏi chi phí vận chuyển.

**Công thức**: `new_cost = base_cost - amount` (tối thiểu $0)

**Ví dụ**:
```
Chi phí cơ sở: $15
Chiết khấu: $5
Kết quả: $10
```

**Trường hợp sử dụng**:
- Thưởng cho khách hàng lần đầu ($5 off chi phí vận chuyển đơn hàng đầu tiên)
- Phần thưởng đăng ký bản tin ($3 off vận chuyển)
- Lợi ích chương trình trung thành ($10 off vận chuyển mỗi tháng)

---

### Thiết lập chi phí

**Nó làm gì**: Ghi đè chi phí vận chuyển thành số tiền cụ thể.

**Công thức**: `new_cost = fixed_amount`

**Ví dụ**:
```
Chi phí cơ sở: $25
Thiết lập thành: $9.99
Kết quả: $9.99
```

**Trường hợp sử dụng**:
- Cuộc sale nhanh (giá cố định $5 cho tất cả đơn hàng hôm nay)
- Vận chuyển theo danh mục (sách luôn có giá $3.99 cho vận chuyển)
- Chiến dịch dựa trên thời gian (giá vận chuyển tối đa $9.99 trong tuần này)

---

### Vận chuyển miễn phí

**Nó làm gì**: Thiết lập chi phí vận chuyển thành $0.

**Công thức**: `new_cost = $0`

**Ví dụ**:
```
Chi phí cơ sở: $18
Quy tắc áp dụng
Kết quả: $0
```

**Trường hợp sử dụng**:
- Vận chuyển miễn phí khi hóa đơn trên $50
- Vận chuyển miễn phí cho các sản phẩm cụ thể (mặt hàng khuyến mãi)
- Vận chuyển miễn phí cho khách hàng VIP
- Vận chuyển miễn phí cho đơn hàng có 3+ mặt hàng

---

### Phí phụ trội (Cố định)

**Nó làm gì**: Thêm khoản cố định vào chi phí vận chuyển.

**Công thức**: `new_cost = base_cost + amount`

**Ví dụ**:
```
Chi phí cơ sở: $12
Phí phụ trội: $5
Kết quả: $17
```

**Trường hợp sử dụng**:
- Phí giao hàng đến khu vực hẻo lánh
- Phí xử lý hàng cồng kềnh
- Phí giao hàng vào thứ Bảy
- Phí đóng gói hàng dễ vỡ

---

### Phí phụ trội (Phần trăm)

**Nó làm gì**: Tăng chi phí vận chuyển theo phần trăm.

**Công thức**: `new_cost = base_cost × (1 + percent/100)`

**Ví dụ**:
```
Chi phí cơ sở: $20
Phí phụ trội: 15%
Kết quả: $23
```

**Trường hợp sử dụng**:
- Phí phụ trội vào mùa cao điểm (20% trong kỳ lễ)
- Phí cao cho giao hàng nhanh (50% phụ trội)
- Phí nhiên liệu (tùy theo giá hiện tại)

---

## Điều kiện quy tắc

Các quy tắc đánh giá **Tất cả các điều kiện phải đạt** để quy tắc được áp dụng:

### Tính hợp lệ về thời gian

- **Ngày bắt đầu**: Quy tắc chỉ hoạt động sau ngày này
- **Ngày kết thúc**: Quy tắc chỉ hoạt động trước ngày này
- **Trường hợp sử dụng**: Chiến dịch theo mùa, ưu đãi thời gian giới hạn

**Ví dụ**: Vận chuyển miễn phí vào cuối tuần Black Friday
```
Ngày bắt đầu: 2026-11-27 00:00
Ngày kết thúc: 2026-11-30 23:59
```

---

### Khoảng giá trị giỏ hàng

- **Giá trị giỏ hàng tối thiểu**: Tổng giá trị giỏ hàng phải ≥ số tiền
- **Giá trị giỏ hàng tối đa**: Tổng giá trị giỏ hàng phải ≤ số tiền
- **Trường hợp sử dụng**: Ngưỡng vận chuyển miễn phí, giảm giá theo cấp bậc

**Ví dụ**: Vận chuyển miễn phí cho đơn hàng $50-$200
```
Giá trị tối thiểu: $50
Giá trị tối đa: $200
```

---

### Khoảng trọng lượng giỏ hàng

- **Trọng lượng tối thiểu**: Trọng lượng tổng giỏ hàng phải ≥ số tiền
- **Trọng lượng tối đa**: Trọng lượng tổng giỏ hàng phải ≤ số tiền
- **Trường hợp sử dụng**: Giảm giá vận chuyển cho hàng nhẹ, phí phụ trội cho hàng nặng

**Ví dụ**: Phí phụ trội $5 cho đơn hàng trên 20kg
```
Trọng lượng tối thiểu: 20kg
Trọng lượng tối đa: null (không giới hạn)
```

---

### Khoảng số lượng mặt hàng


- **Số lượng mặt hàng tối thiểu**: Giỏ hàng phải có ≥ số lượng mặt hàng
- **Số lượng mặt hàng tối đa**: Giỏ hàng phải có ≤ số lượng mặt hàng
- **Trường hợp sử dụng**: Giảm giá theo số lượng, phí cho mặt hàng duy nhất

**Ví dụ**: Miễn phí vận chuyển cho 5+ mặt hàng
```
Số lượng tối thiểu: 5
Số lượng tối đa: null
```


### Khu vực vận chuyển

- **Khu vực**: Quy tắc chỉ áp dụng nếu địa chỉ khách hàng khớp với ít nhất một khu vực được chọn
- **Lựa chọn trống**: Quy tắc áp dụng cho TẤT CẢ các khu vực
- **Trường hợp sử dụng**: Phụ phí hoặc giảm giá theo khu vực

**Ví dụ**: Miễn phí vận chuyển cho khu vực Nội địa
```
Khu vực: ["Khu vực Nội địa USA"]
```


### Phương thức vận chuyển

- **Phương thức**: Quy tắc chỉ áp dụng cho các phương thức vận chuyển cụ thể
- **Lựa chọn trống**: Quy tắc áp dụng cho TẤT CẢ các phương thức
- **Trường hợp sử dụng**: Khuyến mãi theo phương thức

**Ví dụ**: Giảm 25% cho vận chuyển Giao hàng nhanh
```
Phương thức: ["Giao hàng nhanh"]
```


### Yêu cầu sản phẩm

**Yêu cầu sản phẩm**: Giỏ hàng phải chứa ít nhất một sản phẩm trong số các sản phẩm này

**Yêu cầu danh mục**: Giỏ hàng phải chứa ít nhất một sản phẩm từ các danh mục này

**Trường hợp sử dụng**: Miễn phí vận chuyển cho sản phẩm cụ thể, bộ sản phẩm khuyến mãi

**Ví dụ**: Miễn phí vận chuyển khi giỏ hàng chứa "Mặt hàng khuyến mãi A"
```
Yêu cầu sản phẩm: [Mã sản phẩm 123]
```


### Loại bỏ sản phẩm

**Loại bỏ sản phẩm**: Quy tắc không áp dụng nếu giỏ hàng chứa bất kỳ sản phẩm nào trong số các sản phẩm này

**Loại bỏ danh mục**: Quy tắc không áp dụng nếu giỏ hàng chứa bất kỳ sản phẩm nào trong các danh mục này

**Trường hợp sử dụng**: Loại bỏ các sản phẩm nặng/đa dạng kích thước khỏi phí vận chuyển miễn phí

**Ví dụ**: Miễn phí vận chuyển trừ danh mục đồ nội thất
```
Loại bỏ danh mục: ["Đồ nội thất"]
```


### Nhóm khách hàng

- **Nhóm khách hàng**: Quy tắc chỉ áp dụng cho khách hàng trong các nhóm được chọn (VIP, Bán buôn, v.v.)
- **Lựa chọn trống**: Quy tắc áp dụng cho TẤT CẢ các nhóm khách hàng
- **Trường hợp sử dụng**: Ưu đãi cho khách hàng VIP, giảm giá bán buôn

**Ví dụ**: Giảm 15% phí vận chuyển cho thành viên VIP
```
Nhóm khách hàng: ["VIP"]
```


### Khách hàng lần đầu

- **Khách hàng lần đầu**: Bật tính năng giới hạn quy tắc cho khách hàng chưa có đơn hàng trước đây
- **Trường hợp sử dụng**: Chương trình cảm ơn khách hàng mới

**Ví dụ**: Giảm $5 phí vận chuyển cho đơn hàng đầu tiên
```
Khách hàng lần đầu: Có
```


## Thứ tự ưu tiên và thực thi quy tắc

Các quy tắc được thực thi theo **thứ tự ưu tiên** (số lớn hơn = thực thi trước):

### Cơ chế ưu tiên

**Ví dụ thực thi**:
```
Quy tắc A (Ưu tiên 100): Miễn phí vận chuyển nếu giỏ hàng > $50
Quy tắc B (Ưu tiên 50): Giảm 10% cho tất cả phí vận chuyển
Quy tắc C (Ưu tiên 1): Phụ phí $2 cho các khu vực hẻo lánh

Giỏ hàng: $60, Khu vực hẻo lánh
Phí vận chuyển cơ bản: $15

Bước 1: Quy tắc A đánh giá (Ưu tiên 100)
  Giỏ hàng > $50? CÓ
  Áp dụng: Thiết lập chi phí thành $0
  Chi phí hiện tại: $0

Bước 2: Quy tắc B đánh giá (Ưu tiên 50)
  Áp dụng giảm 10% cho $0
  Chi phí hiện tại: $0 ( vẫn miễn phí )

Bước 3: Quy tắc C đánh giá (Ưu tiên 1)
  Thêm phụ phí $2 cho $0
  Chi phí hiện tại: $2

Chi phí cuối cùng: $2
```

**Cờ Dừng Quy tắc Khác**:

Nếu Quy tắc A có `stop_further_rules = True`:
```
Quy tắc A (Ưu tiên 100, stop_further_rules=True): Miễn phí vận chuyển nếu giỏ hàng > $50
Quy tắc B (Ưu tiên 50): Giảm 10% cho tất cả phí vận chuyển
Quy tắc C (Ưu tiên 1): Phụ phí $2 cho các khu vực hẻo lánh

Giỏ hàng: $60
Cơ bản: $15

Bước 1: Quy tắc A áp dụng, thiết lập chi phí thành $0
        stop_further_rules = True → DỪNG

Chi phí cuối cùng: $0 (Quy tắc B và C không bao giờ thực thi)
```


## Tạo quy tắc vận chuyển

**Quy trình từng bước**:

1. **Điều hướng đến Quy tắc**
   - Cài đặt > Vận chuyển > Quy tắc Vận chuyển
   - Nhấn "Thêm Quy tắc Vận chuyển"

2. **Cấu hình Cơ bản**
   - **Tên**: Mã hóa nội bộ (ví dụ: "Miễn phí vận chuyển khi hơn $50")
   - **Mô tả**: Ghi chú tùy chọn (không hiển thị cho khách hàng)
   - **Hoạt động**: Bật/Tắt để kích hoạt/vô hiệu hóa
   - **Ưu tiên**: Thiết lập thứ tự thực thi (100 cho ưu tiên cao, 1 cho ưu tiên thấp)

3. **Chọn Loại Quy tắc**
   - Chọn loại điều chỉnh (giảm %, giảm cố định, thiết lập chi phí, miễn phí, phụ phí %, phụ phí cố định)
   - Nhập số tiền hoặc phần trăm

4. **Thiết lập Cờ Dừng** (Tùy chọn)
   - Chọn "Dừng Quy tắc Khác" nếu quy tắc này nên ngăn các quy tắc có ưu tiên thấp hơn thực thi
   - Sử dụng cho các quy tắc cuối/cố định (ví dụ: miễn phí vận chuyển nên không có phụ phí được thêm sau)

5. **Xác định điều kiện** (Tùy chọn - để trống cho 'luôn áp dụng')
  - Tính hợp lệ theo thời gian: Ngày bắt đầu/ngày kết thúc
  - Giá trị giỏ hàng: Giá trị tối thiểu/giá trị tối đa
  - Trọng lượng giỏ hàng: Giá trị tối thiểu/giá trị tối đa
  - Số lượng mặt hàng: Giá trị tối thiểu/giá trị tối đa
  - Khu vực: Chọn các khu vực phù hợp
  - Phương thức: Chọn các phương thức phù hợp
  - Sản phẩm: Yêu cầu hoặc loại bỏ
  - Khách hàng: Nhóm khách hàng hoặc chỉ khách hàng mới

6. **Lưu quy tắc**
  - Nhấp Lưu
  - Quy tắc sẽ được kích hoạt ngay lập tức (nếu tùy chọn 'Hoạt động' là Có)


## Các tình huống quy tắc giao hàng phổ biến

### Tình huống 1: Giao hàng miễn phí trên $50

**Mục tiêu**: Cung cấp giao hàng miễn phí khi tổng giá trị giỏ hàng ≥ $50.

**Cấu hình**:
```
Tên: Giao hàng miễn phí trên $50
Loại: Giao hàng miễn phí
Ưu tiên: 100
Điều kiện:
  Giá trị giỏ hàng tối thiểu: $50
Dừng các quy tắc khác: Có
```


### Tình huống 2: Phí phụ trội cho khu vực hẻo lánh

**Mục tiêu**: Thêm phí $10 cho các đơn hàng đến khu vực hẻo lánh.

**Cấu hình**:
```
Tên: Phí phụ trội khu vực hẻo lánh
Loại: Phí phụ trội (Cố định)
Số tiền: $10
Ưu tiên: 50
Điều kiện:
  Khu vực: ["Khu vực hẻo lánh"]
Dừng các quy tắc khác: Không
```


### Tình huống 3: Giảm giá 20% cho khách hàng VIP

**Mục tiêu**: Khách hàng VIP được giảm 20% cho mọi đơn hàng giao hàng.

**Cấu hình**:
```
Tên: Giảm giá giao hàng cho khách hàng VIP
Loại: Giảm giá (Phần trăm)
Phần trăm: 20
Ưu tiên: 75
Điều kiện:
  Nhóm khách hàng: ["VIP"]
Dừng các quy tắc khác: Không
```


### Tình huống 4: Giao hàng cố định trong kỳ lễ

**Mục tiêu**: Tất cả đơn hàng bị giới hạn ở $9.99 trong tháng 12.

**Cấu hình**:
```
Tên: Khuyến mãi giá cố định tháng 12
Loại: Giá cố định
Số tiền: $9.99
Ưu tiên: 100
Điều kiện:
  Ngày bắt đầu: 2026-12-01
  Ngày kết thúc: 2026-12-31
Dừng các quy tắc khác: Có
```


### Tình huống 5: Phí phụ trội cho hàng hóa nặng

**Mục tiêu**: Thêm phí $15 cho đơn hàng trên 25kg.

**Cấu hình**:
```
Tên: Phí phụ trội cho đơn hàng nặng
Loại: Phí phụ trội (Cố định)
Số tiền: $15
Ưu tiên: 50
Điều kiện:
  Trọng lượng tối thiểu: 25kg
Dừng các quy tắc khác: Không
```


### Tình huống 6: Giao hàng miễn phí cho đơn hàng đầu tiên

**Mục tiêu**: Khách hàng mới được giao hàng miễn phí cho đơn hàng đầu tiên.

**Cấu hình**:
```
Tên: Giao hàng miễn phí cho đơn hàng đầu tiên
Loại: Giao hàng miễn phí
Ưu tiên: 100
Điều kiện:
  Khách hàng mới: Có
Dừng các quy tắc khác: Có
```


### Tình huống 7: Giao hàng miễn phí theo danh mục

**Mục tiêu**: Giao hàng miễn phí cho đơn hàng chứa mặt hàng thuộc danh mục khuyến mãi.

**Cấu hình**:
```
Tên: Giao hàng miễn phí theo danh mục khuyến mãi
Loại: Giao hàng miễn phí
Ưu tiên: 90
Điều kiện:
  Yêu cầu danh mục: ["Khuyến mãi"]
Dừng các quy tắc khác: Có
```


### Tình huống 8: Loại bỏ đồ nội thất khỏi giao hàng miễn phí

**Mục tiêu**: Giao hàng miễn phí trên $50, trừ khi giỏ hàng chứa đồ nội thất.

Giải pháp: Hai quy tắc

**Quy tắc 1**:
```
Tên: Giao hàng miễn phí tổng quát
Loại: Giao hàng miễn phí
Ưu tiên: 50
Điều kiện:
  Giá trị giỏ hàng tối thiểu: $50
  Loại bỏ danh mục: ["Đồ nội thất"]
Dừng các quy tắc khác: Không
```

**Quy tắc 2**:
```
Tên: Giảm $5 cho đơn hàng đồ nội thất
Loại: Giảm giá (Cố định)
Số tiền: $5
Ưu tiên: 40
Điều kiện:
  Yêu cầu danh mục: ["Đồ nội thất"]
  Giá trị giỏ hàng tối thiểu: $50
Dừng các quy tắc khác: Không
```


## Chiến lược kết hợp quy tắc

### Chiến lược 1: Giảm giá chồng chéo

**Cho phép nhiều giảm giá được áp dụng đồng thời**:
```
Quy tắc A (Ưu tiên 100): Giảm 10% cho khách hàng VIP → stop_further_rules=Không
Quy tắc B (Ưu tiên 50): Giảm 15% cho đơn hàng >$100 → stop_further_rules=Không

Khách hàng VIP với đơn hàng $120:
Cơ sở: $15
Sau Quy tắc A: $13.50 (giảm 10%)
Sau Quy tắc B: $11.48 (giảm 15% từ $13.50)
```


### Chiến lược 2: Quy tắc loại trừ

**Chỉ có một quy tắc được áp dụng** (ưu tiên cao nhất):
```
Quy tắc A (Ưu tiên 100): Giao hàng miễn phí >$50 → stop_further_rules=Có
Quy tắc B (Ưu tiên 50): Giảm 20% cho mọi đơn hàng giao hàng → stop_further_rules=Có

Giỏ hàng > $50:
Quy tắc A được áp dụng → Giao hàng miễn phí → DỪNG
Quy tắc B không bao giờ được thực thi
```


### Chiến lược 3: Phí phụ trội có điều kiện

**Giảm giá trước, phí phụ trội sau**:
```
Quy tắc A (Ưu tiên 100): Giao hàng miễn phí >$75
Quy tắc B (Ưu tiên 75): Giảm 15% cho khách hàng VIP
Quy tắc C (Ưu tiên 50): Giảm 10% cho đơn hàng tổng quát
Quy tắc D (Ưu tiên 25): Phí phụ trội $5 cho khu vực hẻo lánh
Quy tắc E (Ưu tiên 1): Phí phụ trội nhiên liệu 10%

Đơn hàng: $80, Khu vực hẻo lánh, Khách hàng VIP
Cơ sở: $20
A: $80 > $75 → Miễn phí ($0)
B: Khách hàng VIP → Giảm 15% từ $0 = $0
C: Giảm 10% từ $0 = $0
D: Khu vực hẻo lánh +$5 = $5
E: Phí nhiên liệu +10% của $5 = $5.50
```

Cuối cùng: $5.50 (không miễn phí do phụ phí)
```

**Để ngăn điều này, sử dụng stop_further_rules=Yes**:
```
Quy tắc A (Ưu tiên 100, stop=Yes): Giao hàng miễn phí >$75

Đơn hàng cùng lúc:
A: $80 > $75 → Miễn phí ($0) → DỪNG
Cuối cùng: $0 (thực sự miễn phí)
```

---

## Kiểm tra quy tắc giao hàng

**Trước khi triển khai**:

1. **Tạo giỏ hàng kiểm tra**
   - Giỏ A: $25 (dưới ngưỡng)
   - Giỏ B: $55 (trên ngưỡng)
   - Giỏ C: $200 + khu vực hẻo lánh
   - Giỏ D: Khách hàng VIP

2. **Kiểm tra từng quy tắc**
   - Tiến hành thanh toán
   - Xác minh chi phí giao hàng được hiển thị chính xác
   - Kiểm tra thứ tự thực hiện quy tắc

3. **Kiểm tra giải quyết ưu tiên**
   - Nhiều quy tắc phù hợp
   - Xác minh quy tắc có ưu tiên cao nhất được thực hiện trước
   - Kiểm tra hành vi của stop_further_rules

4. **Kiểm tra trường hợp biên**
   - Giá trị giỏ hàng đúng bằng ngưỡng
   - Nhiều điều kiện phù hợp
   - Các quy tắc mâu thuẫn

---

## Giải quyết sự cố

**Vấn đề 1: Quy tắc không được áp dụng**

**Nguyên nhân**:
- Quy tắc đang bị vô hiệu
- Một hoặc nhiều điều kiện không được đáp ứng
- Quy tắc có ưu tiên cao hơn đặt stop_further_rules=Yes
- Thời gian hợp lệ nằm ngoài ngày hiện tại

**Giải pháp**: Xem xét lại tất cả các điều kiện, kiểm tra ưu tiên, xác minh trạng thái hoạt động.

---

**Vấn đề 2: Số tiền giảm giá không mong muốn**

**Nguyên nhân**:
- Nhiều quy tắc chồng chéo
- Phần trăm được áp dụng cho giá đã được giảm
- Ưu tiên quy tắc sai

**Giải pháp**: Kiểm tra thứ tự ưu tiên, xem xét cờ stop_further_rules, theo dõi quá trình thực hiện thủ công.

---

**Vấn đề 3: Giao hàng miễn phí không hoạt động**

**Nguyên nhân**:
- Quy tắc phụ phí có ưu tiên thấp hơn làm phát sinh chi phí sau khi quy tắc giao hàng miễn phí được áp dụng
- Giỏ hàng không đáp ứng giá trị tối thiểu
- Sản phẩm bị loại trong giỏ hàng

**Giải pháp**: Sử dụng stop_further_rules=Yes cho quy tắc giao hàng miễn phí, xác minh điều kiện, kiểm tra các sản phẩm bị loại.

---

## Mẹo

- **Sử dụng ưu tiên cao cho giao hàng miễn phí** - Ưu tiên 100 đảm bảo nó được thực hiện trước các điều chỉnh khác
- **Thiết lập stop_further_rules cho các quy tắc tuyệt đối** - Giao hàng miễn phí nên dừng quá trình xử lý tiếp theo
- **Kiểm tra các tổ hợp quy tắc** - Nhiều quy tắc có thể tương tác một cách không mong muốn
- **Sử dụng tên mô tả** - "Khách hàng VIP Giảm 20% (Ưu tiên 75)" tốt hơn so với "Quy tắc 3"
- **Tài liệu cho logic phức tạp** - Thêm ghi chú trong trường mô tả
- **Bắt đầu với các quy tắc đơn giản** - Thêm độ phức tạp dần dần
- **Theo dõi hiệu suất của quy tắc** - Kiểm tra xem các quy tắc có được sử dụng hoặc gây hiểu nhầm hay không
- **Tránh tạo quá nhiều quy tắc** - Quá nhiều quy tắc làm chậm quá trình thanh toán, nên giới hạn ở 5-10
- **Sử dụng khu vực cho địa lý** - Tốt hơn so với nhiều quy tắc tương tự cho mỗi quốc gia
- **Kết hợp với phương thức** - Các quy tắc + Phương thức làm việc cùng nhau cho giá cả phức tạp
- **Thiết lập khoảng thời gian rõ ràng** - Luôn bao gồm ngày kết thúc cho các chương trình khuyến mãi
- **Kiểm tra các trường hợp biên** - Đúng $50, đúng 5 mặt hàng, v.v.