---
title: Khu vực vận chuyển
---

Khu vực vận chuyển xác định các vùng địa lý cho các mức giá vận chuyển nhắm mục tiêu - nhóm các quốc gia, bang hoặc mã bưu kiện thành các khu vực, sau đó liên kết các phương thức vận chuyển với các khu vực cụ thể để kiểm soát chính xác mức giá. Các khu vực sử dụng phương pháp khớp dựa trên độ ưu tiên khi địa chỉ phù hợp với nhiều khu vực (khu vực có độ ưu tiên cao nhất thắng). Hệ thống này cho phép các chiến lược định giá tinh vi: tính phí cao hơn cho các khu vực hẻo lánh, cung cấp vận chuyển miễn phí trong nước, hoặc cung cấp mức giá giảm cho các khu vực cụ thể.

Sử dụng các khu vực khi bạn cần các chi phí vận chuyển khác nhau cho các khu vực địa lý khác nhau, từ việc chia đơn giản giữa trong nước và quốc tế đến định giá theo cấp bậc đa khu vực phức tạp.

## Hiểu về Khu vực Vận chuyển

**Khu vực là gì**: Các khu vực địa lý được đặt tên, được xác định bởi các quốc gia, bang/tỉnh và các mẫu mã bưu kiện.

**Cách Khu vực hoạt động**:
1. Khách hàng nhập địa chỉ vận chuyển tại bước thanh toán
2. Hệ thống đánh giá tất cả các khu vực đang hoạt động
3. Các khu vực khớp với địa chỉ của khách hàng là các ứng cử viên
4. Nếu nhiều khu vực khớp, khu vực có độ ưu tiên cao nhất thắng
5. Các phương thức vận chuyển được liên kết với khu vực thắng sẽ được hiển thị
6. Các phương thức không được liên kết với bất kỳ khu vực nào (hoặc được liên kết với khu vực khớp) sẽ được hiển thị

**Thành phần Khu vực**:
- **Tên**: Nhận dạng khu vực (ví dụ: "Trong nước", "EU", "Khu vực Hẻo Lánh")
- **Quốc gia**: Danh sách mã quốc gia được bao gồm (trống = tất cả quốc gia)
- **Bang/Tỉnh**: Các hạn chế bang theo quốc gia cụ thể (tùy chọn)
- **Mẫu mã bưu kiện**: Các mẫu biểu thức chính quy cho khớp mã bưu kiện (tùy chọn)
- **Độ ưu tiên**: Số cao hơn = độ ưu tiên cao hơn khi nhiều khu vực khớp

---

## Logic khớp khu vực

Các khu vực sử dụng **thu hẹp dần** để khớp địa chỉ:

### Mức 1: Khớp quốc gia

**Danh sách quốc gia trống** → Khu vực khớp với TẤT CẢ các quốc gia

**Danh sách quốc gia được cung cấp** → Quốc gia của địa chỉ phải có trong danh sách

Ví dụ:
```
Khu vực: "Trong nước"
Quốc gia: ["US"]
→ Khớp: Bất kỳ địa chỉ Mỹ nào
→ Không khớp: Canada, Vương quốc Anh, v.v.
```

### Mức 2: Khớp bang/tỉnh

**Không có bang được định nghĩa** → Khu vực khớp với TẤT CẢ các bang trong các quốc gia được phép

**Bang được định nghĩa cho các quốc gia cụ thể** → Bang của địa chỉ phải khớp

Ví dụ:
```
Khu vực: "West Coast"
Quốc gia: ["US"]
Bang: {"US": ["CA", "OR", "WA"]}
→ Khớp: Địa chỉ California, Oregon, Washington
→ Không khớp: New York, Texas, v.v.
```

### Mức 3: Khớp mã bưu kiện

**Không có mẫu được định nghĩa** → Khu vực khớp với TẤT CẢ các mã bưu kiện trong các quốc gia/bang được phép

**Mẫu được định nghĩa** → Mã bưu kiện của địa chỉ phải khớp ít nhất một mẫu

Ví dụ:
```
Khu vực: "Los Angeles Metro"
Quốc gia: ["US"]
Bang: {"US": ["CA"]}
Mẫu mã bưu kiện: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Khớp: 90001, 91210, 90245
→ Không khớp: 94102 (San Francisco)
```

**Ví dụ về mẫu biểu thức chính quy**:
- `^90[0-9]{3}$` - Khu vực Los Angeles (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Định dạng mã bưu kiện Canada (K1A 0B1)
- `^SW[0-9]{1,2}` - Mã bưu kiện Anh bắt đầu bằng SW

---

## Chọn khu vực dựa trên độ ưu tiên

Khi nhiều khu vực khớp với địa chỉ, **độ ưu tiên** xác định khu vực nào áp dụng:

**Cách độ ưu tiên hoạt động**:
- Số cao hơn = độ ưu tiên cao hơn
- Nếu địa chỉ khớp với các khu vực có độ ưu tiên 100 và 50, độ ưu tiên 100 thắng
- Chỉ các phương thức vận chuyển của khu vực thắng mới có sẵn

**Các trường hợp sử dụng**:

**Tình huống 1: Khu vực cụ thể ghi đè khu vực chung**
```
Khu vực A: "Khu vực hẻo lánh Alaska"
  Quốc gia: ["US"]
  Bang: {"US": ["AK"]}
  Độ ưu tiên: 100

Khu vực B: "Mỹ trong nước"
  Quốc gia: ["US"]
  Độ ưu tiên: 50

Địa chỉ: Anchorage, AK
→ Khớp cả hai khu vực
→ Độ ưu tiên 100 thắng
→ Khu vực "Khu vực hẻo lánh Alaska" áp dụng (chi phí vận chuyển cao hơn)
```

**Tình huống 2: Mã bưu kiện ghi đè bang**
```
Khu vực A: "Manhattan cao cấp"
  Quốc gia: ["US"]
  Bang: {"US": ["NY"]}
  Mẫu mã bưu kiện: ["^100[0-2][0-9]$"]
  Độ ưu tiên: 100

Khu vực B: "Bang New York"
  Quốc gia: ["US"]
  Bang: {"US": ["NY"]}
  Độ ưu tiên: 50

Địa chỉ: New York, NY 10001
→ Khớp cả hai khu vực
→ Độ ưu tiên 100 thắng
→ "Manhattan cao cấp" áp dụng (dịch vụ giao hàng cao cấp)
```

---

## Tạo Khu vực Vận chuyển

**Quy trình từng bước**:

1. **Di chuyển đến Khu vực**
   - Đi đến Cài đặt > Vận chuyển > Khu vực Vận chuyển
   - Nhấp vào "Thêm Khu vực Vận chuyển"


2. **Cấu hình cơ bản**
   - **Tên**: Nhận dạng mô tả (ví dụ: "Liên minh châu Âu", "Bờ Tây", "Khu vực từ xa")
   - **Ưu tiên**: Thiết lập tầm quan trọng tương đối (100 cho cụ thể, 50 cho chung, 1 cho dự phòng)
   - **Kích hoạt**: Bật/tắt để kích hoạt/tắt

3. **Định nghĩa phạm vi địa lý**

   **Tùy chọn A: Tất cả các quốc gia** (trống danh sách quốc gia)
   - Khu vực phù hợp với mọi địa chỉ trên toàn cầu
   - Sử dụng cho khu vực mặc định/dự phòng

   **Tùy chọn B: Các quốc gia cụ thể**
   - Nhấp vào "Thêm quốc gia"
   - Chọn quốc gia từ danh sách thả xuống (US, CA, UK, v.v.)
   - Lặp lại cho tất cả các quốc gia được bao gồm

   **Tùy chọn C: Các tiểu bang/Tỉnh cụ thể**
   - Sau khi thêm quốc gia, nhấp vào "Thêm tiểu bang" cho mỗi quốc gia
   - Chọn các tiểu bang từ danh sách thả xuống
   - Ví dụ: US → CA, OR, WA cho khu vực Bờ Tây

   **Tùy chọn D: Mẫu mã bưu chính** (nâng cao)
   - Nhập các mẫu biểu thức chính quy (một mẫu mỗi dòng)
   - Kiểm tra mẫu với mã bưu chính mẫu
   - Nhấp vào "Xác minh mẫu" để kiểm tra cú pháp

4. **Liên kết với phương thức vận chuyển**
   - Các phương thức có thể được liên kết khi chỉnh sửa phương thức (không phải trong cấu hình khu vực)
   - Hoặc liên kết khu vực với các phương thức hiện có: Chỉnh sửa Phương thức → Khu vực vận chuyển → Chọn các khu vực

5. **Thiết lập độ ưu tiên hiển thị**
   - Các khu vực có độ ưu tiên cao hơn sẽ ghi đè lên các khu vực có độ ưu tiên thấp hơn khi nhiều khu vực khớp
   - Khuyến nghị: Khu vực cụ thể (100), Khu vực khu vực (50), Khu vực mặc định (1)

6. **Kích hoạt khu vực**
   - Bật "Kích hoạt" = Có
   - Lưu

---

## Các thiết lập khu vực phổ biến

### Thiết lập 1: Trong nước vs Quốc tế

**Mục tiêu**: Giá vận chuyển khác nhau cho khu vực trong nước và tất cả các quốc gia khác.

```
Khu vực 1: "Trong nước"
  Quốc gia: [Mã quốc gia của bạn]
  Ưu tiên: 50

Khu vực 2: "Quốc tế"
  Quốc gia: [Trống hoặc chọn tất cả các quốc gia khác]
  Ưu tiên: 1
```

**Phương thức vận chuyển**:
- "Tiêu chuẩn trong nước" → Liên kết với khu vực Trong nước
- "Vận chuyển quốc tế" → Liên kết với khu vực Quốc tế

---

### Thiết lập 2: Quốc tế đa khu vực

**Mục tiêu**: Giá vận chuyển khác nhau cho EU, Bắc Mỹ, châu Á, và các khu vực còn lại.

```
Khu vực 1: "Liên minh châu Âu"
  Quốc gia: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Ưu tiên: 100

Khu vực 2: "Bắc Mỹ"
  Quốc gia: [US, CA, MX]
  Ưu tiên: 100

Khu vực 3: "Châu Á Thái Bình Dương"
  Quốc gia: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Ưu tiên: 100

Khu vực 4: "Các khu vực còn lại"
  Quốc gia: [Trống]
  Ưu tiên: 1
```

**Phương thức vận chuyển**:
- "Vận chuyển EU" → Khu vực EU
- "Vận chuyển Bắc Mỹ" → Khu vực Bắc Mỹ
- "Vận chuyển châu Á Thái Bình Dương" → Khu vực châu Á Thái Bình Dương
- "Tiêu chuẩn quốc tế" → Khu vực Các khu vực còn lại

---

### Thiết lập 3: Phụ phí khu vực từ xa

**Mục tiêu**: Thêm phụ phí cho các mã bưu chính từ xa trong khu vực trong nước.

```
Khu vực 1: "Khu vực từ xa trong nước"
  Quốc gia: [US]
  Mẫu mã bưu chính: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Ưu tiên: 100

Khu vực 2: "Tiêu chuẩn trong nước"
  Quốc gia: [US]
  Ưu tiên: 50
```

**Phương thức vận chuyển**:
- "Vận chuyển từ xa" → Khu vực Khu vực từ xa trong nước (chi phí cao hơn)
- "Vận chuyển tiêu chuẩn" → Khu vực Tiêu chuẩn trong nước

---

### Thiết lập 4: Khu vực theo tiểu bang

**Mục tiêu**: Giá vận chuyển khác nhau cho mỗi khu vực của Mỹ.

```
Khu vực 1: "Bờ Tây"
  Quốc gia: [US]
  Tiểu bang: {"US": ["CA", "OR", "WA"]}
  Ưu tiên: 100

Khu vực 2: "Bờ Đông"
  Quốc gia: [US]
  Tiểu bang: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Ưu tiên: 100

Khu vực 3: "Trung tâm"
  Quốc gia: [US]
  Tiểu bang: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Ưu tiên: 100

Khu vực 4: "Miền Nam"
  Quốc gia: [US]
  Tiểu bang: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Ưu tiên: 100

Khu vực 5: "Các tiểu bang khác của Mỹ"
  Quốc gia: [US]
  Ưu tiên: 50
```

---

## Ví dụ mẫu mã bưu chính

Mã bưu chính sử dụng **regex** (biểu thức chính quy) để khớp mẫu:

### Hoa Kỳ (Mã ZIP)

**Định dạng**: 5 chữ số (ví dụ: 90210)

```
California (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Canada (Mã bưu chính)

**Định dạng**: A1A 1A1 (chữ-số-chữ khoảng trắng số-chữ-số)


Tất cả mã bưu chính Canada:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$

- **Bắt đầu với 2 khu vực** - Nội địa và Quốc tế, mở rộng khi cần
- **Sử dụng độ ưu tiên một cách hợp lý** - Các khu vực cụ thể 100, khu vực vùng 50, khu vực dự phòng 1
- **Kiểm tra kỹ các mẫu bưu kiện** - Lỗi regex sẽ không báo cáo, gây ra việc khu vực không khớp
- **Ghi chú về logic khu vực** - Thêm ghi chú vào mô tả khu vực để giải thích mục đích phạm vi áp dụng
- **Tránh sử dụng quá nhiều khu vực** - Quá nhiều khu vực làm phức tạp cấu hình; sử dụng khuyến mãi vận chuyển cho các tình huống phức tạp
- **Sử dụng mã vùng, không phải tên** - "CA" thay vì "California", "NY" thay vì "New York"
- **Tạo khu vực dự phòng** - Tất cả các quốc gia, độ ưu tiên 1, đảm bảo luôn có ít nhất một tùy chọn vận chuyển
- **Theo dõi hiệu suất khu vực** - Nếu nhiều khách hàng thấy "không có phương thức vận chuyển nào", hãy kiểm tra lại phạm vi khu vực
- **Cập nhật khu vực cho các khu vực mới** - Thêm các quốc gia vào khu vực EU khi có quốc gia mới gia nhập
- **Sử dụng tên mô tả** - "EU (Không bao gồm Vương quốc Anh)" tốt hơn "Khu vực 3"
- **Kiểm tra với địa chỉ thực tế** - Sử dụng địa chỉ thực tế của khách hàng trong quá trình kiểm tra, không phải địa chỉ giả tạo