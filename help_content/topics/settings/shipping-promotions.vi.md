---
title: Khuyến mãi vận chuyển
---

Các quy tắc vận chuyển áp dụng các điều chỉnh chi phí có điều kiện đến các phương thức vận chuyển dựa trên nội dung giỏ hàng, thuộc tính khách hàng và khu vực giao hàng—tự động cung cấp miễn phí vận chuyển cho đơn hàng trên $50, thêm phụ phí cho khu vực hẻo lánh, hoặc giảm giá vận chuyển cho khách hàng VIP. Các quy tắc sử dụng việc thực thi dựa trên độ ưu tiên (ưu tiên cao trước) với cờ dừng tùy chọn để ngăn xử lý tiếp theo. Mỗi quy tắc đánh giá nhiều điều kiện (giá trị giỏ hàng, trọng lượng, khu vực, sản phẩm, nhóm khách hàng) và thực thi một trong 6 loại điều chỉnh khi tất cả điều kiện khớp nhau.

Sử dụng khuyến mãi vận chuyển khi bạn cần chi phí vận chuyển động thay đổi dựa trên ngữ cảnh đơn hàng, không chỉ là tỷ lệ cố định từ phương thức vận chuyển.

## Loại khuyến mãi vận chuyển

Các quy tắc vận chuyển áp dụng 6 loại điều chỉnh chi phí:

### Giảm giá theo tỷ lệ

**Chức năng**: Giảm chi phí vận chuyển theo tỷ lệ (ví dụ: giảm 25%)

**Công thức**: `new_cost = base_cost × (1 - percent/100)`

**Ví dụ**:
```
Chi phí cơ bản: $20
Giảm giá: 25%
Kết quả: $15
```

**Trường hợp sử dụng**:
- Giảm giá cho khách hàng VIP (giảm 20% cho tất cả vận chuyển)
- Khuyến mãi theo mùa (giảm 15% vận chuyển vào tháng 12)
- Giảm giá cho đơn hàng số lượng lớn (giảm 10% vận chuyển cho 5+ sản phẩm)

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
- Ưu đãi cho khách hàng mới (giảm $5 cho vận chuyển đơn hàng đầu tiên)
- Phần thưởng đăng ký bản tin (giảm $3 cho vận chuyển)
- Lợi ích chương trình khách hàng thân thiết (giảm $10 cho vận chuyển mỗi tháng)

---

### Thay đổi chi phí

**Chức năng**: Thay đổi chi phí vận chuyển thành một khoản cố định.

**Công thức**: `new_cost = fixed_amount`

**Ví dụ**:
```
Chi phí cơ bản: $25
Đặt thành: $9.99
Kết quả: $9.99
```

**Trường hợp sử dụng**:
- Khuyến mãi flash (vận chuyển cố định $5 cho tất cả đơn hàng hôm nay)
- Vận chuyển theo danh mục cụ thể (sách luôn có chi phí vận chuyển $3.99)
- Khuyến mãi theo thời gian (giới hạn chi phí vận chuyển ở $9.99 trong tuần này)

---

### Miễn phí vận chuyển

**Chức năng**: Đặt chi phí vận chuyển thành $0.

**Công thức**: `new_cost = $0`

**Ví dụ**:
```
Chi phí cơ bản: $18
Quy tắc áp dụng
Kết quả: $0
```

**Trường hợp sử dụng**:
- Miễn phí vận chuyển cho đơn hàng trên $50
- Miễn phí vận chuyển cho sản phẩm cụ thể (sản phẩm khuyến mãi)
- Miễn phí vận chuyển cho khách hàng VIP
- Miễn phí vận chuyển cho đơn hàng có 3+ sản phẩm

---

### Phụ phí (cố định)

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

### Phụ phí (theo tỷ lệ)

**Chức năng**: Tăng chi phí vận chuyển theo tỷ lệ.

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

## Điều kiện khuyến mãi

Khuyến mãi đánh giá **tất cả điều kiện phải được đáp ứng** để quy tắc áp dụng:

### Thời gian hiệu lực

- **Ngày bắt đầu**: Quy tắc chỉ hoạt động sau ngày này
- **Ngày kết thúc**: Quy tắc chỉ hoạt động trước ngày này
- **Trường hợp sử dụng**: Khuyến mãi theo mùa, ưu đãi giới hạn thời gian

**Ví dụ**: Miễn phí vận chuyển chỉ trong cuối tuần Black Friday
```
Bắt đầu: 2026-11-27 00:00
Kết thúc: 2026-11-30 23:59
```

---

### Phạm vi giá trị giỏ hàng

- **Giá trị giỏ hàng tối thiểu**: Tổng giá trị giỏ hàng phải ≥ số tiền
- **Giá trị giỏ hàng tối đa**: Tổng giá trị giỏ hàng phải ≤ số tiền
- **Trường hợp sử dụng**: Ngưỡng miễn phí vận chuyển, giảm giá theo cấp bậc

**Ví dụ**: Miễn phí vận chuyển cho đơn hàng từ $50 đến $200
```
Tối thiểu: $50
Tối đa: $200
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


- **Min Item Count**: Giỏ hàng phải có ≥ số lượng mặt hàng
- **Max Item Count**: Giỏ hàng phải có ≤ số lượng mặt hàng
- **Use Case**: Giảm giá theo đơn hàng số lượng lớn, phí cho mặt hàng đơn lẻ

**Example**: Miễn phí vận chuyển cho 5+ mặt hàng
```
Min Items: 5
Max Items: null
```

---

### Shipping Zone

- **Zones**: Quy tắc chỉ áp dụng nếu địa chỉ khách hàng khớp với ít nhất một khu vực đã chọn
- **Empty selection**: Quy tắc áp dụng cho TẤT CẢ các khu vực
- **Use Case**: Phí phụ thêm hoặc giảm giá theo khu vực

**Example**: Miễn phí vận chuyển chỉ cho khu vực Domestic
```
Zones: ["Domestic USA"]
```

---

### Shipping Method

- **Methods**: Quy tắc chỉ áp dụng cho các phương thức vận chuyển cụ thể
- **Empty selection**: Quy tắc áp dụng cho TẤT CẢ các phương thức
- **Use Case**: Khuyến mãi theo phương thức vận chuyển

**Example**: Giảm 25% cho phương thức vận chuyển Express
```
Methods: ["Express Delivery"]
```

---

### Product Requirements

**Requires Products**: Giỏ hàng phải chứa ít nhất một trong những sản phẩm này

**Requires Categories**: Giỏ hàng phải chứa ít nhất một sản phẩm từ các danh mục này

**Use Case**: Miễn phí vận chuyển theo sản phẩm cụ thể, gói hàng khuyến mãi

**Example**: Miễn phí vận chuyển khi giỏ hàng chứa "Promotion Item A"
```
Requires Products: [Product ID 123]
```

---

### Product Exclusions

**Excludes Products**: Quy tắc không áp dụng nếu giỏ hàng chứa bất kỳ sản phẩm nào trong số này

**Excludes Categories**: Quy tắc không áp dụng nếu giỏ hàng chứa bất kỳ sản phẩm nào từ các danh mục này

**Use Case**: Loại bỏ các sản phẩm nặng/đồ cồng kềnh khỏi miễn phí vận chuyển

**Example**: Miễn phí vận chuyển ngoại trừ danh mục Nội thất
```
Excludes Categories: [Furniture]
```

---

### Customer Group

- **Customer Groups**: Quy tắc chỉ áp dụng cho khách hàng thuộc nhóm đã chọn (VIP, Wholesale, v.v.)
- **Empty selection**: Quy tắc áp dụng cho TẤT CẢ các nhóm khách hàng
- **Use Case**: Lợi ích dành cho khách hàng VIP, giảm giá theo nhóm sỉ

**Example**: Giảm 15% phí vận chuyển cho thành viên VIP
```
Customer Groups: ["VIP"]
```

---

### First-Time Customer

- **First Time Customer**: Bật/tắt để giới hạn quy tắc chỉ áp dụng cho khách hàng chưa từng đặt hàng trước đó
- **Use Case**: Ưu đãi chào mừng khách hàng mới

**Example**: Giảm 5 USD phí vận chuyển cho đơn hàng đầu tiên
```
First Time Customer: Yes
```

---

## Promotion Priority & Execution

Các chương trình khuyến mãi được thực thi theo **thứ tự ưu tiên** (số càng cao thì càng được thực thi trước):

### Priority Mechanics

**Example Execution**:
```
Promotion A (Priority 100): Free shipping if cart > $50
Promotion B (Priority 50): 10% discount on all shipping
Promotion C (Priority 1): $2 surcharge for remote zones

Cart: $60, Remote zone
Base shipping cost: $15

Step 1: Promotion A evaluates (Priority 100)
  Cart > $50? YES
  Apply: Set cost to $0
  Cost now: $0

Step 2: Promotion B evaluates (Priority 50)
  Apply 10% discount to $0
  Cost now: $0 (still free)

Step 3: Promotion C evaluates (Priority 1)
  Add $2 surcharge to $0
  Cost now: $2

Final cost: $2
```

**Stop Further Promotions Flag**:

Nếu Promotion A có `stop_further_promotions = True`:
```
Promotion A (Priority 100, stop_further_promotions=True): Free shipping if cart > $50
Promotion B (Priority 50): 10% discount
Promotion C (Priority 1): $2 surcharge

Cart: $60
Base: $15

Step 1: Promotion A applies, sets cost to $0
        stop_further_promotions = True → STOP

Final cost: $0 (Rules B and C never execute)
```

---

## Creating Shipping Promotions

**Step-by-Step Workflow**:

1. **Navigate to Rules**
   - Settings > Shipping > Shipping Promotions
   - Click "Add Shipping Promotion"

2. **Basic Configuration**
   - **Name**: Internal identifier (e.g., "Free Shipping Over $50")
   - **Description**: Optional notes (not shown to customers)
   - **Active**: Toggle to enable/disable
   - **Priority**: Set execution order (100 for high priority, 1 for low)

3. **Choose Promotion Type**
   - Select adjustment type (discount %, discount fixed, set cost, free, surcharge %, surcharge fixed)
   - Enter amount or percentage


4. **Đặt cờ dừng** (Tùy chọn)
   - Chọn "Ngừng khuyến mãi tiếp theo" nếu quy tắc này nên ngăn các khuyến mãi có độ ưu tiên thấp hơn từ việc thực thi
   - Sử dụng cho các quy tắc cuối cùng/uyên bản (ví dụ: giao hàng miễn phí không nên có phụ phí được thêm vào sau)

5. **Định nghĩa điều kiện** (Tùy chọn - để trống để "luôn áp dụng")
   - Thời gian hiệu lực: Ngày bắt đầu/kết thúc
   - Giá trị giỏ hàng: Tối thiểu/tối đa
   - Trọng lượng giỏ hàng: Tối thiểu/tối đa
   - Số lượng mặt hàng: Tối thiểu/tối đa
   - Khu vực: Chọn các khu vực áp dụng
   - Phương thức: Chọn các phương thức áp dụng
   - Sản phẩm: Yêu cầu hoặc loại trừ
   - Khách hàng: Nhóm hoặc chỉ dành cho khách hàng mới

6. **Lưu quy tắc**
   - Nhấp vào Lưu
   - Quy tắc trở nên hoạt động ngay lập tức (nếu nút bật/tắt là Có)

---

## Các tình huống khuyến mãi vận chuyển phổ biến

### Tình huống 1: Miễn phí vận chuyển khi tổng giỏ hàng ≥ $50

**Mục tiêu**: Cung cấp miễn phí vận chuyển khi tổng giỏ hàng ≥ $50.

**Cấu hình**:
```
Tên: Miễn phí vận chuyển khi tổng giỏ hàng ≥ $50
Loại: Miễn phí vận chuyển
Ưu tiên: 100
Điều kiện:
  Giá trị giỏ hàng tối thiểu: $50
Ngừng khuyến mãi tiếp theo: Có
```

---

### Tình huống 2: Phụ phí khu vực hẻo lánh

**Mục tiêu**: Thêm phụ phí $10 cho các đơn hàng giao đến khu vực hẻo lánh.

**Cấu hình**:
```
Tên: Phụ phí khu vực hẻo lánh
Loại: Phụ phí (Cố định)
Số tiền: $10
Ưu tiên: 50
Điều kiện:
  Khu vực: ["Khu vực hẻo lánh"]
Ngừng khuyến mãi tiếp theo: Không
```

---

### Tình huống 3: Giảm 20% cho khách hàng VIP

**Mục tiêu**: Khách hàng VIP được giảm 20% trên tất cả phí vận chuyển.

**Cấu hình**:
```
Tên: Giảm giá vận chuyển VIP
Loại: Giảm giá (Tỷ lệ phần trăm)
Tỷ lệ: 20
Ưu tiên: 75
Điều kiện:
  Nhóm khách hàng: ["VIP"]
Ngừng khuyến mãi tiếp theo: Không
```

---

### Tình huống 4: Mức giá cố định vào mùa lễ

**Mục tiêu**: Tất cả phí vận chuyển được giới hạn ở $9.99 trong tháng 12.

**Cấu hình**:
```
Tên: Khuyến mãi giá cố định tháng 12
Loại: Ghi đè chi phí
Số tiền: $9.99
Ưu tiên: 100
Điều kiện:
  Ngày bắt đầu: 2026-12-01
  Ngày kết thúc: 2026-12-31
Ngừng khuyến mãi tiếp theo: Có
```

---

### Tình huống 5: Phụ phí cho mặt hàng nặng

**Mục tiêu**: Thêm phụ phí $15 cho các đơn hàng nặng hơn 25kg.

**Cấu hình**:
```
Tên: Phụ phí đơn hàng nặng
Loại: Phụ phí (Cố định)
Số tiền: $15
Ưu tiên: 50
Điều kiện:
  Trọng lượng tối thiểu: 25kg
Ngừng khuyến mãi tiếp theo: Không
```

---

### Tình huống 6: Miễn phí vận chuyển cho đơn hàng đầu tiên

**Mục tiêu**: Khách hàng mới được miễn phí vận chuyển cho đơn hàng đầu tiên.

**Cấu hình**:
```
Tên: Miễn phí vận chuyển cho đơn hàng đầu tiên
Loại: Miễn phí vận chuyển
Ưu tiên: 100
Điều kiện:
  Khách hàng mới: Có
Ngừng khuyến mãi tiếp theo: Có
```

---

### Tình huống 7: Miễn phí vận chuyển theo danh mục

**Mục tiêu**: Miễn phí vận chuyển cho các đơn hàng chứa mặt hàng thuộc danh mục khuyến mãi.

**Cấu hình**:
```
Tên: Miễn phí vận chuyển danh mục khuyến mãi
Loại: Miễn phí vận chuyển
Ưu tiên: 90
Điều kiện:
  Yêu cầu danh mục: ["Khuyến mãi"]
Ngừng khuyến mãi tiếp theo: Có
```

---

### Tình huống 8: Loại trừ nội thất khỏi miễn phí vận chuyển

**Mục tiêu**: Miễn phí vận chuyển khi tổng giỏ hàng ≥ $50, ngoại trừ khi giỏ hàng chứa nội thất.

**Giải pháp**: Hai quy tắc

**Khuyến mãi 1**:
```
Tên: Miễn phí vận chuyển chung
Loại: Miễn phí vận chuyển
Ưu tiên: 50
Điều kiện:
  Giá trị giỏ hàng tối thiểu: $50
  Loại trừ danh mục: ["Nội thất"]
Ngừng khuyến mãi tiếp theo: Không
```

**Khuyến mãi 2**:
```
Tên: Giảm $5 cho đơn hàng nội thất
Loại: Giảm giá (Cố định)
Số tiền: $5
Ưu tiên: 40
Điều kiện:
  Yêu cầu danh mục: ["Nội thất"]
  Giá trị giỏ hàng tối thiểu: $50
Ngừng khuyến mãi tiếp theo: Không
```

---

## Chiến lược kết hợp khuyến mãi

### Chiến lược 1: Kết hợp giảm giá

**Cho phép nhiều giảm giá chồng lên nhau**:
```
Khuyến mãi A (Ưu tiên 100): Giảm 10% cho khách hàng VIP → stop_further_promotions=Không
Khuyến mãi B (Ưu tiên 50): Giảm 15% cho đơn hàng >$100 → stop_further_promotions=Không

Khách hàng VIP với đơn hàng $120:
Giá gốc: $15
Sau khuyến mãi A: $13.50 (giảm 10%)
Sau khuyến mãi B: $11.48 (giảm 15% từ $13.50)
```

### Chiến lược 2: Quy tắc độc quyền

**Chỉ có một quy tắc áp dụng** (ưu tiên cao nhất):
```
Khuyến mãi A (Ưu tiên 100): Miễn phí vận chuyển >$50 → stop_further_promotions= Có
Khuyến mãi B (Ưu tiên 50): Giảm 20% trên tất cả phí vận chuyển → stop_further_promotions= Có

Giỏ hàng > $50:
Khuyến mãi A áp dụng → Miễn phí vận chuyển → DỪNG
Khuyến mãi B không bao giờ được thực thi
```

### Chiến lược 3: Phụ phí điều kiện


**Ưu đãi trước, phụ phí sau**:
```
Khuyến mãi A (Ưu tiên 100): Miễn phí vận chuyển >$75
Khuyến mãi B (Ưu tiên 75): Giảm 15% cho khách hàng VIP
Khuyến mãi C (Ưu tiên 50): Giảm 10% chung
Khuyến mãi D (Ưu tiên 25): Phụ phí 5$ cho khu vực hẻo lánh
Khuyến mãi E (Ưu tiên 1): Phụ phí nhiên liệu 10%

Đơn hàng: $80, Khu vực hẻo lánh, Khách hàng VIP
Cơ sở: $20
A: $80 > $75 → Miễn phí ($0)
B: VIP → Giảm 15% $0 = $0
C: Giảm 10% $0 = $0
D: Khu vực hẻo lánh +$5 = $5
E: Nhiên liệu +10% của $5 = $5.50

Kết quả cuối cùng: $5.50 (không miễn phí do phụ phí)
```

**Để tránh điều này, hãy sử dụng stop_further_promotions=Yes**:
```
Khuyến mãi A (Ưu tiên 100, stop=Yes): Miễn phí vận chuyển >$75

Cùng đơn hàng:
A: $80 > $75 → Miễn phí ($0) → DỪNG
Kết quả cuối cùng: $0 (thật sự miễn phí)
```

---

## Kiểm tra khuyến mãi vận chuyển

**Trước khi đưa vào vận hành**:

1. **Tạo giỏ hàng kiểm tra**
   - Giỏ hàng A: $25 (dưới ngưỡng)
   - Giỏ hàng B: $55 (trên ngưỡng)
   - Giỏ hàng C: $200 + Khu vực hẻo lánh
   - Giỏ hàng D: Khách hàng VIP

2. **Kiểm tra từng quy tắc**
   - Tiến hành thanh toán
   - Xác nhận chi phí vận chuyển hiển thị đúng
   - Kiểm tra thứ tự thực thi quy tắc

3. **Kiểm tra giải quyết ưu tiên**
   - Nhiều quy tắc khớp
   - Xác nhận quy tắc ưu tiên cao nhất thực thi trước
   - Kiểm tra hành vi của stop_further_promotions

4. **Kiểm tra các trường hợp biên**
   - Giá trị giỏ hàng chính xác ở ngưỡng
   - Nhiều điều kiện khớp
   - Các quy tắc mâu thuẫn

---

## Khắc phục sự cố

**Vấn đề 1: Khuyến mãi không áp dụng**

**Nguyên nhân**:
- Quy tắc không hoạt động
- Một hoặc nhiều điều kiện không được đáp ứng
- Quy tắc ưu tiên cao hơn đã thiết lập stop_further_promotions=Yes
- Thời gian hiệu lực ngoài phạm vi ngày hiện tại

**Giải pháp**: Xem lại tất cả điều kiện, kiểm tra ưu tiên, xác nhận trạng thái hoạt động.

---

**Vấn đề 2: Số tiền giảm không như mong đợi**

**Nguyên nhân**:
- Nhiều khuyến mãi chồng chéo
- Phần trăm được áp dụng trên chi phí đã được giảm
- Ưu tiên quy tắc không đúng

**Giải pháp**: Kiểm tra thứ tự ưu tiên, xem lại cờ stop_further_promotions, theo dõi quá trình thực thi thủ công.

---

**Vấn đề 3: Miễn phí vận chuyển không hoạt động**

**Nguyên nhân**:
- Quy tắc phụ phí có ưu tiên thấp hơn thêm chi phí sau khuyến mãi miễn phí vận chuyển
- Giá trị giỏ hàng không đạt ngưỡng tối thiểu
- Sản phẩm bị loại trong giỏ hàng

**Giải pháp**: Sử dụng stop_further_promotions=Yes cho khuyến mãi miễn phí vận chuyển, xác nhận điều kiện, kiểm tra các sản phẩm bị loại.

---

## Một số lưu ý

- **Sử dụng ưu tiên cao cho miễn phí vận chuyển** - Ưu tiên 100 đảm bảo nó thực thi trước các điều chỉnh khác
- **Thiết lập stop_further_promotions cho các quy tắc tuyệt đối** - Miễn phí vận chuyển nên dừng xử lý tiếp theo
- **Kiểm tra sự kết hợp quy tắc** - Nhiều khuyến mãi có thể tương tác bất ngờ
- **Sử dụng tên mô tả** - "Giảm 20% cho khách VIP (Ưu tiên 75)" tốt hơn "Khuyến mãi 3"
- **Ghi chú logic phức tạp** - Thêm ghi chú trong trường mô tả
- **Bắt đầu với các khuyến mãi đơn giản** - Thêm độ phức tạp dần dần
- **Theo dõi hiệu suất quy tắc** - Kiểm tra xem các quy tắc có được sử dụng hay gây hiểu lầm không
- **Tránh quá nhiều khuyến mãi** - Quá nhiều khuyến mãi làm chậm quá trình thanh toán, hãy sử dụng 5-10 khuyến mãi tối đa
- **Sử dụng khu vực cho địa lý** - Tốt hơn là nhiều quy tắc tương tự cho mỗi quốc gia
- **Kết hợp với phương pháp** - Quy tắc + Phương pháp làm việc cùng nhau cho định giá phức tạp
- **Thiết lập khoảng thời gian rõ ràng** - Luôn bao gồm ngày kết thúc cho khuyến mãi
- **Kiểm tra các trường hợp biên** - Chính xác $50, chính xác 5 sản phẩm, v.v.
