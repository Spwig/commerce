---
title: Cấu hình Thuế
---

Các mức thuế xác định thuế bán hàng, thuế giá trị gia tăng (VAT) và các loại thuế tiêu dùng khác được áp dụng tại thời điểm thanh toán dựa trên vị trí của khách hàng và loại sản phẩm—cấu hình các mức thuế theo cấp quốc gia/tỉnh/thành phố với tùy chọn miễn thuế theo loại sản phẩm. Spwig hỗ trợ thuế phức hợp (thuế trên thuế), lựa chọn mức thuế dựa trên độ ưu tiên và các nhóm thuế mặc định để thiết lập nhanh chóng hệ thống thuế khu vực (VAT EU, Thuế bán hàng Mỹ). Các mức thuế có thể miễn cho các loại sản phẩm cụ thể (thức ăn, sách, hàng hóa số) hoặc các danh mục để tuân thủ luật thuế địa phương.

Sử dụng cấu hình thuế để đảm bảo tuân thủ các yêu cầu thu thuế pháp lý trong các khu vực bán hàng của bạn.

## Cấu hình Mức Thuế

Mỗi mức thuế xác định:

**Phạm vi địa lý**:
- Quốc gia (bắt buộc)
- Tỉnh/Tiểu bang (tùy chọn)
- Thành phố (tùy chọn)
- Mẫu mã bưu chính (tùy chọn, regex)

**Chi tiết Mức Thuế**:
- **Mức Thuế**: Phần trăm (ví dụ: 8,5%)
- **Tên**: Tên hiển thị (ví dụ: "Thuế bán hàng California")
- **Ưu tiên**: Ưu tiên cao hơn sẽ được áp dụng khi nhiều mức thuế khớp
- **Kích hoạt**: Bật/tắt mà không xóa

**Miễn Thuế**:
- **Loại Sản phẩm Được Miễn Thuế**: Hàng hóa số, hàng hóa vật lý, dịch vụ
- **Danh Mục Được Miễn Thuế**: Các danh mục sản phẩm cụ thể (Thức ăn, Sách, Y tế)

**Thuế Phức Hợp**:
- **Là Thuế Phức Hợp**: Áp dụng mức thuế này trên các thuế trước đó (thuế trên thuế)
- Ví dụ: Thuế PST Quebec được áp dụng trên thuế GST

---

## Các Tình Huống Thuế Thường Gặp

### Thuế Bán Hàng Mỹ (Mức Tỉnh)

```
Tên: Thuế bán hàng California
Quốc gia: US
Tỉnh: CA
Mức thuế: 7.25%
Ưu tiên: 50
```

### Thuế VAT EU (Mức Quốc Gia)

```
Tên: VAT Anh
Quốc gia: GB
Mức thuế: 20%
Ưu tiên: 50

Tên: VAT Đức
Quốc gia: DE
Mức thuế: 19%
Ưu tiên: 50
```

### Thuế GST/PST Canada (Phức hợp)

```
Mức thuế 1: Thuế GST Liên bang
Quốc gia: CA
Mức thuế: 5%
Ưu tiên: 100
Là thuế phức hợp: Không

Mức thuế 2: Thuế PST Quebec
Quốc gia: CA
Tỉnh: QC
Mức thuế: 9.975%
Ưu tiên: 50
Là thuế phức hợp: Có (áp dụng cho tổng số tiền + GST)
```

### Thuế cấp thành phố

```
Tên: Thuế bán hàng Seattle
Quốc gia: US
Tỉnh: WA
Thành phố: Seattle
Mức thuế: 10.1%
Ưu tiên: 100
```

---

## Miễn Thuế

### Miễn Thuế Loại Sản Phẩm

Miễn toàn bộ loại sản phẩm:

- **Hàng hóa số**: Phần mềm, sách điện tử, âm nhạc
- **Hàng hóa vật lý**: Sản phẩm hữu hình
- **Dịch vụ**: Tư vấn, lắp đặt

Ví dụ: Thuế VAT EU không áp dụng cho hàng hóa số dành cho người tiêu dùng (trong một số trường hợp)

### Miễn Thuế Danh Mục

Miễn các danh mục sản phẩm cụ thể:

- Thức ăn & Thực phẩm (thường miễn hoặc giảm thuế)
- Sách & Tài liệu Giáo dục
- Thiết bị Y tế & Thuốc
- Trang phục (một số khu vực)

Cấu hình:
```
Tên: Thuế bán hàng California
Mức thuế: 7.25%
Danh mục miễn thuế: ["Thức ăn & Đồ uống", "Thuốc kê đơn"]
```

---

## Nhóm Thuế Mặc Định

Tải nhanh các cấu hình thuế phổ biến:

**Nhóm Thuế Bán Hàng Mỹ Mặc Định**:
- Tất cả 50 tiểu bang + DC
- Mức thuế theo cấp tỉnh
- Cập nhật tự động khi mức thuế thay đổi

**Nhóm Thuế VAT EU Mặc Định**:
- Tất cả 27 nước thành viên EU
- Mức thuế VAT tiêu chuẩn
- Logic thu thuế ngược cho B2B

**Để Sử Dụng Nhóm Thuế Mặc Định**:
1. Cài đặt > Giỏ hàng > Cài đặt Thuế
2. Chọn nhóm thuế mặc định (ví dụ: "Thuế bán hàng Mỹ 2026")
3. Nhấn "Tải nhóm thuế"
4. Mức thuế được nhập tự động
5. Tùy chỉnh theo nhu cầu

---

## Giải Quyết Ưu Tiên

Khi nhiều mức thuế khớp, mức ưu tiên cao nhất sẽ được áp dụng:

Ví dụ:
```
Khách hàng ở Seattle, WA:

Mức thuế A: Liên bang Mỹ (Ưu tiên 1) - 0%
Mức thuế B: Tiểu bang Washington (Ưu tiên 50) - 6.5%
Mức thuế C: Thành phố Seattle (Ưu tiên 100) - 3.6%

Kết quả: Áp dụng mức thuế Seattle (tổng cộng 10.1%)
```

---

## Tùy Chọn Hiển Thị Thuế

Cấu hình trong Cài đặt > Giỏ hàng > Cài đặt Thuế:

- **Giá Bao Gồm Thuế**: Hiển thị giá bao gồm thuế (phong cách EU)
- **Hiển Thị Thuế Riêng Lẻ**: Hiển thị thuế như một mục riêng (phong cách Mỹ)
- **Làm Tròn Thuế**: Theo từng mặt hàng hoặc theo đơn hàng
- **Nhãn Thuế**: Tùy chỉnh nhãn ("VAT", "Thuế bán hàng", "GST")

---

## Kiểm Thử Cấu Hình Thuế

Trước khi đưa vào vận hành:

1. Tạo các đơn hàng kiểm tra từ các khu vực khác nhau
2. Xác nhận mức thuế đúng được áp dụng
3. Kiểm tra các danh mục miễn thuế hoạt động cho các danh mục bị loại trừ
4. Kiểm tra tính toán thuế phức hợp
5. Xem lại các mục thuế trên hóa đơn

---

## Ghi Chú Tuân Thủ

- **Mỹ**: Quy tắc Nexus yêu cầu thu thuế ở các tiểu bang mà bạn có mặt vật lý hoặc mối liên hệ kinh tế
- **EU**: Các doanh nghiệp đã đăng ký VAT phải thu VAT từ khách hàng EU
- **Canada**: GST/HST/PST thay đổi theo tỉnh
- **Tư vấn chuyên gia thuế**: Luật thuế thay đổi thường xuyên, xác minh các yêu cầu hiện tại

---

## Mẹo

- **Sử dụng các nhóm thuế mặc định** - Nhanh hơn so với nhập thủ công, được cập nhật tự động
- **Theo dõi ngưỡng Nexus** - Theo dõi doanh số theo tiểu bang cho mối liên hệ kinh tế Mỹ
- **Đặt độ ưu tiên đúng** - Thành phố > Tỉnh > Quốc gia
- **Kiểm tra thuế phức hợp** - Xác minh các tính toán khớp với số tiền mong muốn
- **Cập nhật hàng năm** - Mức thuế thay đổi, xem xét mỗi tháng 1
- **Ghi lại các miễn thuế** - Lưu hồ sơ lý do các danh mục được miễn thuế
- **Sử dụng tên mô tả** - "Thuế bán hàng California 2026" tốt hơn "Thuế 1"
- **Bật thuế mặc định** - An toàn hơn là quên áp dụng thuế

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.