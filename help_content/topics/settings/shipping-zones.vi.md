---
title: Khu vực vận chuyển
---

Khu vực vận chuyển xác định các vùng địa lý cho các mức giá vận chuyển nhắm mục tiêu - nhóm các quốc gia, bang hoặc mã bưu kiện thành các khu vực, sau đó liên kết các phương thức vận chuyển với các khu vực cụ thể để kiểm soát chính xác mức giá. Các khu vực sử dụng việc khớp dựa trên độ ưu tiên khi địa chỉ phù hợp với nhiều khu vực (khu vực có độ ưu tiên cao nhất thắng). Hệ thống này cho phép các chiến lược định giá phức tạp: tính phí cao hơn cho các khu vực hẻo lánh, cung cấp vận chuyển miễn phí trong nước, hoặc cung cấp mức giá giảm cho các khu vực cụ thể.

Sử dụng các khu vực khi bạn cần các chi phí vận chuyển khác nhau cho các khu vực địa lý khác nhau, từ việc chia tách đơn giản trong nước so với quốc tế đến định giá theo cấp bậc đa khu vực phức tạp.

## Hiểu về Khu vực Vận chuyển

**Khu vực là gì**: Các vùng địa lý được đặt tên, được xác định bởi các mã quốc gia, bang/tỉnh và các mẫu mã bưu kiện.

**Cách Khu vực Hoạt động**:
1. Khách hàng nhập địa chỉ vận chuyển tại bước thanh toán
2. Hệ thống đánh giá tất cả các khu vực đang hoạt động
3. Các khu vực khớp với địa chỉ của khách hàng là các ứng cử viên
4. Nếu nhiều khu vực khớp, khu vực có độ ưu tiên cao nhất thắng
5. Các phương thức vận chuyển được liên kết với khu vực thắng sẽ được hiển thị
6. Các phương thức không được liên kết với bất kỳ khu vực nào (hoặc được liên kết với khu vực khớp) sẽ được hiển thị

**Thành phần Khu vực**:
- **Tên**: Nhận diện khu vực (ví dụ: "Trong nước", "EU", "Khu vực Hẻo Lánh")
- **Quốc gia**: Danh sách mã quốc gia được bao gồm (trống = tất cả quốc gia)
- **Bang/Tỉnh**: Các hạn chế bang theo quốc gia cụ thể (tùy chọn)
- **Mẫu mã bưu kiện**: Các mẫu biểu thức chính quy cho khớp mã ZIP/mã bưu kiện (tùy chọn)
- **Ưu tiên**: Số cao hơn = ưu tiên cao hơn khi nhiều khu vực khớp

---

## Logic khớp khu vực

Các khu vực sử dụng **thu hẹp dần** để khớp địa chỉ:

### Mức 1: Khớp quốc gia

**Danh sách quốc gia trống** → Khu vực khớp TẤT CẢ các quốc gia

**Danh sách quốc gia được cung cấp** → Quốc gia của địa chỉ phải có trong danh sách

Ví dụ:
```
Khu vực: "Trong nước"
Quốc gia: ["US"]
→ Khớp: bất kỳ địa chỉ Mỹ nào
→ Không khớp: Canada, Vương quốc Anh, v.v.
```

### Mức 2: Khớp bang/tỉnh

**Không có bang được xác định** → Khu vực khớp TẤT CẢ các bang trong quốc gia được phép

**Bang được xác định cho các quốc gia cụ thể** → Bang của địa chỉ phải khớp

Ví dụ:
```
Khu vực: "West Coast"
Quốc gia: ["US"]
Bang: {"US": ["CA", "OR", "WA"]}
→ Khớp: địa chỉ California, Oregon, Washington
→ Không khớp: New York, Texas, v.v.
```

### Mức 3: Khớp mã bưu kiện

**Không có mẫu nào được xác định** → Khu vực khớp TẤT CẢ các mã bưu kiện trong quốc gia/bang được phép

**Mẫu được xác định** → Mã bưu kiện của địa chỉ phải khớp ít nhất một mẫu

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
- `^SW[0-9]{1,2}` - Mã bưu kiện London, Anh bắt đầu bằng SW

---

## Chọn khu vực dựa trên độ ưu tiên

Khi nhiều khu vực khớp với địa chỉ, **độ ưu tiên** xác định khu vực nào áp dụng:

**Cách độ ưu tiên hoạt động**:
- Số cao hơn = độ ưu tiên cao hơn
- Nếu địa chỉ khớp với các khu vực có độ ưu tiên 100 và 50, độ ưu tiên 100 thắng
- Chỉ các phương thức vận chuyển của khu vực thắng mới có sẵn

**Các trường hợp sử dụng**:

**Tình huống 1: Khu vực cụ thể thay thế khu vực tổng quát**
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

**Tình huống 2: Mã bưu kiện thay thế bang**
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

**Quy trình làm việc từng bước**:

1. **Di chuyển đến Khu vực**
   - Đi đến Cài đặt > Vận chuyển > Khu vực Vận chuyển
   - Nhấp vào "Thêm Khu vực Vận chuyển"

2. **Cấu hình cơ bản**
   - **Tên**: Nhận diện mô tả (ví dụ: "Liên minh châu Âu", "West Coast", "Khu vực hẻo lánh")
   - **Ưu tiên**: Thiết lập tầm quan trọng tương đối (100 cho cụ thể, 50 cho tổng quát, 1 cho dự phòng)
   - **Hoạt động**: Bật/tắt để kích hoạt/tắt

3. **Định nghĩa phạm vi địa lý**

   **Tùy chọn A: Tất cả quốc gia** (trống danh sách quốc gia)
   - Khu vực khớp mọi địa chỉ trên toàn cầu
   - Sử dụng cho các khu vực mặc định/dự phòng

   **Tùy chọn B: Quốc gia cụ thể**
   - Nhấp vào "Thêm Quốc gia"
   - Chọn quốc gia từ danh sách thả xuống (US, CA, UK, v.v.)
   - Lặp lại cho tất cả các quốc gia được bao gồm

   **Tùy chọn C: Bang/Tỉnh cụ thể**
   - Sau khi thêm quốc gia, nhấp vào "Thêm Bang" cho mỗi quốc gia
   - Chọn bang từ danh sách thả xuống
   - Ví dụ: US → CA, OR, WA cho West Coast

   **Tùy chọn D: Mẫu mã bưu kiện** (nâng cao)
   - Nhập các mẫu biểu thức chính quy (một mẫu mỗi dòng)
   - Kiểm tra mẫu với các mã bưu kiện mẫu
   - Nhấp vào "Xác minh Mẫu" để kiểm tra cú pháp

4. **Liên kết với phương thức vận chuyển**
   - Các phương thức có thể được liên kết khi chỉnh sửa phương thức (không phải trong cấu hình khu vực)
   - Hoặc liên kết khu vực với phương thức hiện có: Chỉnh sửa Phương thức → Khu vực Vận chuyển → Chọn khu vực

5. **Thiết lập độ ưu tiên hiển thị**
   - Các khu vực có độ ưu tiên cao hơn sẽ thay thế các khu vực có độ ưu tiên thấp hơn khi khớp nhiều khu vực
   - Khuyến nghị: Khu vực cụ thể (100), Khu vực khu vực (50), Khu vực mặc định (1)

6. **Kích hoạt Khu vực**
   - Bật "Hoạt động" = Có
   - Lưu

---

## Các thiết lập khu vực phổ biến

### Thiết lập 1: Trong nước vs Quốc tế

**Mục tiêu**: Các mức giá khác nhau cho trong nước so với tất cả các quốc gia khác.

```
Khu vực 1: "Trong nước"
  Quốc gia: [Mã quốc gia của bạn]
  Độ ưu tiên: 50

Khu vực 2: "Quốc tế"
  Quốc gia: [Trống hoặc chọn tất cả các quốc gia khác]
  Độ ưu tiên: 1
```

**Phương thức vận chuyển**:
- "Tiêu chuẩn trong nước" → Liên kết với khu vực Trong nước
- "Vận chuyển quốc tế" → Liên kết với khu vực Quốc tế

---

### Thiết lập 2: Quốc tế đa khu vực

**Mục tiêu**: Các mức giá khác nhau cho EU, Bắc Mỹ, Châu Á, Thế giới còn lại.

```
Khu vực 1: "Liên minh châu Âu"
  Quốc gia: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Độ ưu tiên: 100

Khu vực 2: "Bắc Mỹ"
  Quốc gia: [US, CA, MX]
  Độ ưu tiên: 100

Khu vực 3: "Châu Á Thái Bình Dương"
  Quốc gia: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Độ ưu tiên: 100

Khu vực 4: "Thế giới còn lại"
  Quốc gia: [Trống]
  Độ ưu tiên: 1
```

**Phương thức vận chuyển**:
- "Vận chuyển EU" → Khu vực EU
- "Vận chuyển Bắc Mỹ" → Khu vực Bắc Mỹ
- "Vận chuyển Châu Á Thái Bình Dương" → Khu vực Châu Á Thái Bình Dương
- "Tiêu chuẩn quốc tế" → Khu vực Thế giới còn lại

---

### Thiết lập 3: Phụ phí khu vực hẻo lánh

**Mục tiêu**: Thêm phụ phí cho các mã bưu kiện hẻo lánh trong khu vực trong nước.

```
Khu vực 1: "Khu vực hẻo lánh trong nước"
  Quốc gia: [US]
  Mẫu mã bưu kiện: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Độ ưu tiên: 100

Khu vực 2: "Tiêu chuẩn trong nước"
  Quốc gia: [US]
  Độ ưu tiên: 50
```

**Phương thức vận chuyển**:
- "Vận chuyển hẻo lánh" → Khu vực Khu vực hẻo lánh trong nước (chi phí cao hơn)
- "Vận chuyển tiêu chuẩn" → Khu vực Tiêu chuẩn trong nước

---

### Thiết lập 4: Khu vực theo bang

**Mục tiêu**: Các mức giá khác nhau cho mỗi khu vực của Mỹ.

```
Khu vực 1: "West Coast"
  Quốc gia: [US]
  Bang: {"US": ["CA", "OR", "WA"]}
  Độ ưu tiên: 100

Khu vực 2: "East Coast"
  Quốc gia: [US]
  Bang: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Độ ưu tiên: 100

Khu vực 3: "Midwest"
  Quốc gia: [US]
  Bang: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Độ ưu tiên: 100

Khu vực 4: "South"
  Quốc gia: [US]
  Bang: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Độ ưu tiên: 100

Khu vực 5: "Các bang khác của Mỹ"
  Quốc gia: [US]
  Độ ưu tiên: 50
```

---

## Ví dụ về mẫu mã bưu kiện

Mã bưu kiện sử dụng **biểu thức chính quy** (regular expressions) để khớp mẫu:

### Hoa Kỳ (Mã ZIP)

**Định dạng**: 5 chữ số (ví dụ: 90210)

```
California (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Canada (Mã bưu kiện)

**Định dạng**: A1A 1A1 (chữ cái-số-chữ cái khoảng trắng số-chữ cái-số)

```
Tất cả mã bưu kiện Canada:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$
Ontario (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$\nQuebec (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$\n```

### Vương quốc Anh (Mã bưu kiện)

**Định dạng**: AA1A 1AA hoặc A1A 1AA

```
London (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}
Manchester (M):                        ^M[0-9]{1,2}
Birmingham (B):                        ^B[0-9]{1,2}
```

### Úc (Mã bưu kiện)

**Định dạng**: 4 chữ số (ví dụ: 2000)

```
New South Wales (1000-2999):  ^[12][0-9]{3}$
Victoria (3000-3999, 8000-8999):  ^[38][0-9]{3}$
Queensland (4000-4999, 9000-9999):  ^[49][0-9]{3}$
```

### Kiểm tra mẫu

**Trước khi lưu mẫu**, kiểm tra với các mã bưu kiện đã biết:

1. Nhập mẫu: `^90[0-9]{3}$`
2. Đầu vào kiểm tra: "90210" → Nên khớp
3. Đầu vào kiểm tra: "10001" → Nên KHÔNG khớp
4. Đầu vào kiểm tra: "9021" → Nên KHÔNG khớp (chỉ 4 chữ số)

Sử dụng các công cụ kiểm tra biểu thức chính quy trực tuyến (regex101.com) để xác minh các mẫu phức tạp.

---

## Tóm tắt phạm vi khu vực

Các khu vực hiển thị **tóm tắt phạm vi** trong chế độ xem danh sách quản trị, cho thấy những gì được bao gồm:

**Ví dụ**:
- "Tất cả các quốc gia" → Không có hạn chế quốc gia
- "US, CA, MX" → 3 quốc gia
- "US (CA, OR, WA)" → Mỹ với 3 bang
- "US (90xxx-91xxx)" → Mỹ với các mẫu mã bưu kiện

**Sử dụng tóm tắt để**:
- Kiểm tra nhanh phạm vi khu vực mà không cần mở ra
- Phát hiện các khu vực chồng chéo hoặc thiếu
- Xem xét cấu hình khu vực một cách nhanh chóng

---

## Liên kết Khu vực với Phương thức Vận chuyển

Khu vực và phương thức có **mối quan hệ đa-nhiều**:

**Từ phía phương thức** (Khuyến nghị):
1. Chỉnh sửa Phương thức Vận chuyển
2. Cuộn xuống phần "Khu vực Vận chuyển"
3. Chọn các khu vực phù hợp (chọn nhiều)
4. Lưu phương thức

**Từ phía khu vực**:
- Các khu vực không liên kết trực tiếp với phương thức
- Liên kết luôn được thực hiện từ cấu hình phương thức

**Hành vi phương thức-khu vực**:

**Không có khu vực nào được liên kết** → Phương thức có sẵn cho TẤT CẢ các địa chỉ

**Các khu vực được liên kết** → Phương thức chỉ có sẵn nếu địa chỉ khách hàng khớp với ít nhất một khu vực được liên kết

**Ví dụ**:
```
Phương thức: "Tiêu chuẩn trong nước"
Khu vực được liên kết: ["Mỹ trong nước"]
→ Chỉ hiển thị cho các địa chỉ Mỹ

Phương thức: "Vận chuyển quốc tế nhanh"
Khu vực được liên kết: ["EU", "Châu Á Thái Bình Dương", "Thế giới còn lại"]
→ Hiển thị cho tất cả các địa chỉ không phải Mỹ
```

---

## Kiểm tra khớp khu vực

Trước khi đưa vào vận hành, kiểm tra cấu hình khu vực:

1. **Tạo đơn hàng kiểm tra**
   - Sử dụng các địa chỉ trong các khu vực khác nhau
   - Xác nhận khớp khu vực đúng

2. **Kiểm tra giải quyết độ ưu tiên**
   - Sử dụng địa chỉ khớp với nhiều khu vực
   - Xác nhận khu vực có độ ưu tiên cao nhất thắng
   - Xác nhận các phương thức vận chuyển mong muốn hiển thị

3. **Kiểm tra các trường hợp biên**
   - Các mã bưu kiện biên giới (ví dụ: 90999 so với 91000)
   - Biên giới bang
   - Địa chỉ quốc tế với mã bưu kiện tương tự

4. **Sử dụng công cụ xem trước khu vực** (nếu có)
   - Nhập địa chỉ kiểm tra
   - Xem khu vực nào khớp
   - Xem giải quyết độ ưu tiên

---

## Khắc phục sự cố

**Vấn đề 1: Không có phương thức vận chuyển nào có sẵn tại bước thanh toán**

**Nguyên nhân**:
- Địa chỉ khách hàng không khớp với bất kỳ khu vực nào
- Tất cả phương thức được liên kết với các khu vực không khớp
- Không có phương thức nào tồn tại mà không có hạn chế khu vực

**Giải pháp**:
- Tạo khu vực dự phòng (tất cả quốc gia, độ ưu tiên 1)
- HOẶC loại bỏ hạn chế khu vực từ ít nhất một phương thức
- Xác nhận các mẫu quốc gia/bang/mã bưu kiện của khu vực

---

**Vấn đề 2: Khớp khu vực sai**

**Nguyên nhân**:
- Khu vực có độ ưu tiên thấp hơn được chọn mặc dù có khu vực có độ ưu tiên cao hơn khớp
- Lỗi cú pháp mẫu mã bưu kiện (mẫu thất bại âm thầm)
- Mismatch mã bang (CA so với California)

**Giải pháp**:
- Xác nhận các giá trị độ ưu tiên (số cao hơn = độ ưu tiên cao hơn)
- Kiểm tra mẫu mã bưu kiện với công cụ xác minh biểu thức chính quy
- Sử dụng mã bang 2 chữ cái (CA, không phải California)

---

**Vấn đề 3: Phương thức không mong muốn được hiển thị**

**Nguyên nhân**:
- Phương thức không có khu vực nào được liên kết (có sẵn ở mọi nơi)
- Nhiều khu vực khớp, khu vực không mong muốn có độ ưu tiên cao hơn
- Phạm vi khu vực chồng chéo không mong muốn

**Giải pháp**:
- Xem xét lại các khu vực được liên kết với phương thức
- Kiểm tra độ ưu tiên của các khu vực khớp
- Xem xét tóm tắt phạm vi khu vực để phát hiện chồng chéo

---

## Một số mẹo

- **Bắt đầu với 2 khu vực** - Trong nước và Quốc tế, mở rộng khi cần thiết
- **Sử dụng độ ưu tiên một cách khôn ngoan** - Khu vực cụ thể 100, khu vực khu vực 50, khu vực dự phòng 1
- **Kiểm tra kỹ các mẫu mã bưu kiện** - Lỗi biểu thức chính quy sẽ thất bại âm thầm, gây ra các khu vực không khớp
- **Ghi chú logic khu vực** - Thêm ghi chú vào mô tả khu vực để giải thích mục đích phạm vi
- **Tránh tạo quá nhiều khu vực** - Quá nhiều khu vực làm phức tạp cấu hình; sử dụng các quy tắc vận chuyển cho các tình huống phức tạp
- **Sử dụng mã bang, không phải tên** - "CA" không phải "California", "NY" không phải "New York"
- **Tạo khu vực dự phòng** - Tất cả quốc gia, độ ưu tiên 1, đảm bảo luôn có ít nhất một phương thức vận chuyển có sẵn
- **Theo dõi hiệu suất khu vực** - Nếu nhiều khách hàng thấy "không có phương thức vận chuyển nào", xem xét lại phạm vi khu vực
- **Cập nhật khu vực cho các khu vực mới** - Thêm quốc gia vào khu vực EU khi có quốc gia mới tham gia
- **Sử dụng tên mô tả** - "EU (Không bao gồm Vương quốc Anh)" tốt hơn "Khu vực 3"
- **Kiểm tra với các địa chỉ thực tế** - Sử dụng địa chỉ thực tế của khách hàng trong quá trình kiểm tra, không phải các địa chỉ giả tạo

Nhớ: Bảo tồn toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật chính xác như được hiển thị trong các quy tắc bảo tồn.