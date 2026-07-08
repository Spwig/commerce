---
title: Gói vận chuyển
---

Gói vận chuyển xác định các kích thước hộp và phong bì được định nghĩa trước để tính cước phí và tự động đóng gói—chỉ định kích thước bên trong (không gian sử dụng được), độ dày tường (kích thước bên ngoài cho API của nhà vận chuyển), giới hạn trọng lượng và chi phí đóng gói. Các nhà vận chuyển sử dụng kích thước bên ngoài để tính trọng lượng theo kích thước để báo giá cước phí chính xác. Các gói hàng có thứ tự ưu tiên cho các thuật toán đóng gói theo thùng nhằm tự động chọn các tổ hợp gói hàng tối ưu để phù hợp với các mục trong giỏ hàng.

Cấu hình gói hàng khi sử dụng API của nhà vận chuyển để tính cước phí thời gian thực hoặc khi bạn cần tính toán trọng lượng theo kích thước chính xác.

## Cấu hình gói hàng

Mỗi gói hàng xác định:

**Kích thước**:
- **Chiều dài bên trong**: Không gian sử dụng được bên trong (cm)
- **Chiều rộng bên trong**: Không gian sử dụng được bên trong (cm)
- **Chiều cao bên trong**: Không gian sử dụng được bên trong (cm)
- **Độ dày tường**: Độ dày của vật liệu đóng gói (cm)

**Kích thước bên ngoài** (tự động tính toán):
```
Chiều dài bên ngoài = Chiều dài bên trong + (2 × Độ dày tường)
Chiều rộng bên ngoài = Chiều rộng bên trong + (2 × Độ dày tường)
Chiều cao bên ngoài = Chiều cao bên trong + (2 × Độ dày tường)
```

**Trọng lượng & Chi phí**:
- **Trọng lượng rỗng**: Trọng lượng của gói hàng trống (gram)
- **Trọng lượng tối đa**: Khả năng chịu tải tối đa (gram)
- **Chi phí**: Chi phí vật liệu đóng gói (để tối ưu hóa chi phí)

**Thuộc tính**:
- **Tên**: Nhận dạng gói hàng (ví dụ: "Hộp nhỏ", "Phong bì lớn")
- **Loại**: Hộp hoặc Phong bì
- **Ưu tiên**: Thứ tự chọn gói hàng tự động (số nhỏ hơn = ưu tiên cao hơn)
- **Hoạt động**: Bật/tắt tính khả dụng

---

## Tại sao kích thước bên ngoài quan trọng

Các nhà vận chuyển tính toán **trọng lượng theo kích thước** từ kích thước bên ngoài:

**Công thức trọng lượng theo kích thước**:
```
Trọng lượng theo kích thước = (Chiều dài × Chiều rộng × Chiều cao) / Hệ số

Các hệ số phổ biến:
- DHL: 5000
- FedEx/UPS: 5000 (trong nước), 6000 (quốc tế)
```

**Ví dụ**:
```
Hộp nhỏ:
Bên trong: 20cm × 15cm × 10cm
Độ dày tường: 0.5cm
Bên ngoài: 21cm × 16cm × 11cm

Trọng lượng theo kích thước = (21 × 16 × 11) / 5000 = 0.74kg

Nếu trọng lượng thực tế = 0.5kg → Nhà vận chuyển tính theo 0.74kg (trọng lượng theo kích thước cao hơn)
```

**Tại sao độ chính xác quan trọng**: Kích thước không chính xác → báo giá cước phí sai → khách hàng bị tính quá mức hoặc thiếu.

---

## Các kích thước gói hàng phổ biến

### Phong bì nhỏ có đệm

```
Bên trong: 25cm × 18cm × 2cm
Độ dày tường: 0.3cm
Trọng lượng tối đa: 500g
Loại: Phong bì
Sử dụng: Tài liệu, sách, trang sức
```

### Hộp nhỏ

```
Bên trong: 20cm × 15cm × 10cm
Độ dày tường: 0.5cm
Trọng lượng tối đa: 5kg
Loại: Hộp
Sử dụng: Điện tử nhỏ, mỹ phẩm, phụ kiện
```

### Hộp trung bình

```
Bên trong: 30cm × 25cm × 20cm
Độ dày tường: 0.5cm
Trọng lượng tối đa: 15kg
Loại: Hộp
Sử dụng: Quần áo, giày, đồ dùng nhà bếp
```

### Hộp lớn

```
Bên trong: 45cm × 35cm × 30cm
Độ dày tường: 0.6cm
Trọng lượng tối đa: 30kg
Loại: Hộp
Sử dụng: Hàng hóa số lượng lớn, nhiều sản phẩm, thiết bị điện tử lớn
```

---

## Thuật toán tự động đóng gói

Hệ thống tự động chọn gói hàng cho các mục trong giỏ hàng:

**Cách hoạt động**:
1. Tính thể tích tổng của các mục trong giỏ hàng
2. Sắp xếp các gói hàng theo thứ tự ưu tiên (số nhỏ nhất trước)
3. Thử đóng gói các mục vào một gói hàng
4. Nếu không vừa, thử gói hàng lớn hơn tiếp theo
5. Nếu không gói hàng nào vừa, kết hợp nhiều gói hàng
6. Tối ưu dựa trên cài đặt `optimize_for`

**Chế độ tối ưu**:
- **Chi phí**: Tối thiểu hóa chi phí đóng gói
- **Thể tích**: Tối thiểu hóa không gian bị lãng phí
- **Số lượng**: Tối thiểu hóa số gói hàng

**Ví dụ**:
```
Các mục trong giỏ hàng:
- Mục A: 10cm × 8cm × 5cm, 200g
- Mục B: 15cm × 12cm × 8cm, 400g

Các gói hàng (theo thứ tự ưu tiên):
1. Hộp nhỏ (20×15×10, Ưu tiên=1)
2. Hộp trung bình (30×25×20, Ưu tiên=2)

Thuật toán:
Thử gói nhỏ: Cả hai mục vừa
Kết quả: 1× Hộp nhỏ (tối ưu theo số lượng)
```

---

## Thứ tự ưu tiên gói hàng

**Ưu tiên xác định thứ tự đóng gói**:

Ưu tiên 1 (cao nhất): Gói hàng nhỏ được thử trước
Ưu tiên 10: Gói hàng lớn là lựa chọn cuối cùng

**Chiến lược**:
- Gói hàng nhỏ = số ưu tiên thấp (1-3)
- Gói hàng trung bình = ưu tiên trung bình (4-6)
- Gói hàng lớn = số ưu tiên cao (7-10)

**Tại sao**: Bắt đầu với gói hàng nhỏ nhất, mở rộng nếu cần → tối thiểu hóa chi phí vận chuyển.

---

## Độ chính xác của độ dày tường

Đo đạc thực tế các gói hàng:

**Cách đo**:
1. Lấy hộp trống
2. Đo kích thước bên trong (bên trong)
3. Đo kích thước bên ngoài (bên ngoài)
4. Tính toán: `(Bên ngoài - Bên trong) / 2 = Độ dày tường`

**Ví dụ**:
```
Chiều rộng bên trong: 20cm
Chiều rộng bên ngoài: 21cm
Độ dày tường: (21 - 20) / 2 = 0.5cm
```

**Độ dày phổ biến**:
- Phong bì có đệm: 0.2-0.4cm
- Gỗ bì đơn: 0.4-0.6cm
- Gỗ bì đôi: 0.8-1.0cm

---

## Tạo gói hàng mặc định

**Bước-by-bước**:

1. Cài đặt > Vận chuyển > Gói vận chuyển
2. Nhấp vào "Thêm gói vận chuyển"
3. Nhập tên (ví dụ: "Hộp trung bình")
4. Chọn loại (Hộp hoặc Phong bì)
5. Nhập kích thước bên trong (L × W × H theo cm)
6. Nhập độ dày tường (cm)
7. Hệ thống tự động tính toán kích thước bên ngoài
8. Nhập trọng lượng rỗng (trọng lượng gói hàng trống theo gram)
9. Nhập trọng lượng tối đa (khả năng chịu tải theo gram)
10. Tùy chọn: Nhập chi phí (để tối ưu hóa chi phí)
11. Thiết lập ưu tiên (1-10)
12. Bật tính năng hoạt động = Có
13. Lưu

---

## Kiểm tra lựa chọn gói hàng

**Kiểm tra thủ công**:
1. Thêm sản phẩm vào giỏ hàng kiểm tra
2. Tiến hành thanh toán
3. Chọn phương thức vận chuyển thời gian thực (sử dụng gói hàng)
4. Xác nhận báo giá cước phí hợp lý
5. Kiểm tra phản hồi nhà vận chuyển (log API hiển thị gói hàng đã chọn)

**Xem trước đóng gói tự động**:
- Một số tài khoản cung cấp vận chuyển hiển thị phân tích gói hàng
- Xem gói hàng nào được chọn cho giỏ hàng
- Xác nhận đóng gói tối ưu

---

## Gợi ý

- **Đo đạc chính xác** - Kích thước không chính xác → báo giá cước phí sai
- **Bao gồm độ dày tường** - Quan trọng cho trọng lượng theo kích thước
- **Bắt đầu với 3-4 kích thước** - Hộp nhỏ, trung bình, lớn sẽ đáp ứng hầu hết các tình huống
- **Thiết lập trọng lượng tối đa thực tế** - Khả năng chứa của hộp, không phải giới hạn lý thuyết
- **Sử dụng ưu tiên hợp lý** - Hộp nhỏ ưu tiên 1, hộp lớn ưu tiên 10
- **Kiểm tra với sản phẩm thực tế** - Xác nhận đóng gói tự động chọn kích thước đúng
- **Cập nhật khi thay đổi đóng gói** - Nhà cung cấp mới = đo đạc lại kích thước
- **Cân nhắc các mặt hàng đặc biệt** - Các mặt hàng dễ vỡ có thể cần kích thước hộp cụ thể
- **Giữ gói hàng hoạt động tối thiểu** - Quá nhiều tùy chọn làm chậm thuật toán đóng gói tự động
- **Ghi chú về đóng gói** - Ghi rõ các sản phẩm phù hợp với từng gói hàng
