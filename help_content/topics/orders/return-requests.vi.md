---
title: Yêu cầu trả hàng & Xử lý
---

Yêu cầu trả hàng theo dõi các khoản hoàn tiền của khách hàng từ khi khởi tạo đến khi hoàn tất hoàn tiền—khách hàng chọn các mục để trả hàng cùng lý do, người bán chấp thuận hoặc từ chối yêu cầu, tạo nhãn trả hàng, kiểm tra các mặt hàng đã trả và xử lý hoàn tiền. Quy trình tiến hành qua 9 giai đoạn trạng thái (đang chờ → đã chấp thuận → nhãn_đã_gửi → đang vận chuyển → đã nhận → đã kiểm tra → hoàn tất/từ chối/hủy bỏ) với lý do trả hàng theo từng mặt hàng, ghi chú kiểm tra và phí tái nhập kho (tùy chọn).

Sử dụng trang quản trị này để xem xét, chấp thuận và xử lý các yêu cầu trả hàng của khách hàng hiệu quả.

## Quy trình Yêu cầu Trả hàng

**Quy trình 9 Giai đoạn**:

### 1. Đang chờ (Khách hàng khởi tạo)

Khách hàng gửi yêu cầu trả hàng:
- Chọn các mặt hàng từ đơn hàng
- Cung cấp lý do trả hàng cho từng mặt hàng
- Ghi chú (tùy chọn) của khách hàng
- Trạng thái: `đang chờ`

### 2. Đã chấp thuận/Từ chối (Người bán xem xét)

Người bán xem xét yêu cầu:
- **Chấp thuận**: Cho phép trả hàng, tiếp tục tạo nhãn
- **Từ chối**: Từ chối trả hàng với lý do từ chối
- Trạng thái: `đã chấp thuận` hoặc `đã từ chối`

### 3. Nhãn đã gửi (Vận chuyển trả hàng)

Tạo nhãn trả hàng:
- Người bán tạo vận chuyển trả hàng (tùy chọn)
- Nhãn trả hàng được gửi qua email cho khách hàng
- Khách hàng gửi hàng trở lại
- Trạng thái: `nhãn_đã_gửi`

### 4. Đang vận chuyển (Khách hàng gửi hàng)

Khách hàng gửi hàng:
- Theo dõi chuyển động
- Cập nhật trạng thái tự động từ webhook của nhà vận chuyển
- Trạng thái: `đang_vận_chuyển`

### 5. Đã nhận (Đến kho hàng)

Hàng hóa đến:
- Kho quét vận chuyển
- Hàng hóa được kiểm tra vào
- Trạng thái: `đã nhận`

### 6. Đã kiểm tra (Kiểm tra chất lượng)

Người bán kiểm tra mặt hàng:
- Ghi lại tình trạng mặt hàng (tuyệt vời/tốt/chấp nhận được/hỏng/độc hại)
- Thêm ghi chú kiểm tra
- Áp dụng phí tái nhập kho nếu cần
- Trạng thái: `đã kiểm tra`

### 7. Hoàn tất (Xử lý hoàn tiền)

Hoàn tiền được phát hành:
- Tạo hoàn tiền liên quan
- Xử lý thanh toán
- Yêu cầu trả hàng được đóng
- Trạng thái: `hoàn tất`

**Kết quả thay thế**:
- **Đã hủy bỏ**: Khách hàng hủy bỏ trước khi gửi hàng
- **Đã từ chối**: Người bán từ chối sau khi xem xét

---

## Xử lý Yêu cầu Trả hàng

**Bước-by-Bước**:

**Bước 1: Xem xét các yêu cầu đang chờ**
- Di chuyển đến Đơn hàng > Yêu cầu Trả hàng
- Lọc theo trạng thái = "Đang chờ"
- Nhấp vào yêu cầu để xem chi tiết

**Bước 2: Đánh giá Yêu cầu**
- Xem xét chi tiết đơn hàng
- Kiểm tra lý do trả hàng
- Xác minh tuân thủ chính sách hoàn tiền (trong thời gian hoàn tiền, mặt hàng đủ điều kiện)

**Bước 3: Chấp thuận hoặc Từ chối**
- Nhấp "Chấp thuận" để chấp nhận trả hàng
- HOẶC nhấp "Từ chối" và nhập lý do từ chối
- Lưu quyết định

**Bước 4: Tạo nhãn trả hàng** (nếu được chấp thuận)
- Nhấp "Tạo vận chuyển trả hàng"
- Chọn nhà vận chuyển/dịch vụ
- Hệ thống tạo nhãn trả hàng
- Nhãn tự động được gửi qua email cho khách hàng
- Trạng thái → `nhãn_đã_gửi`

**Bước 5: Theo dõi vận chuyển**
- Cập nhật theo dõi tự động đồng bộ từ webhook nhà vận chuyển
- Trạng thái tự động chuyển sang `đang_vận_chuyển` khi nhà vận chuyển quét gói hàng

**Bước 6: Nhận hàng**
- Khi hàng hóa đến, nhấp "Đánh dấu là đã nhận"
- Trạng thái → `đã nhận`

**Bước 7: Kiểm tra hàng hóa**
- Mở yêu cầu trả hàng
- Chọn tình trạng mặt hàng từ danh sách thả xuống:
  - Tuyệt vời (như mới, có thể bán lại)
  - Tốt (sử dụng nhẹ, có thể bán lại)
  - Chấp nhận được (sử dụng rõ rệt, có thể bán lại với giảm giá)
  - Hỏng (không thể bán lại)
  - Độc hại (lỗi sản xuất)
- Thêm ghi chú kiểm tra
- Tùy chọn: Áp dụng phí tái nhập kho (tỷ lệ phần trăm hoặc cố định)
- Trạng thái → `đã kiểm tra`

**Bước 8: Xử lý hoàn tiền**
- Nhấp "Tạo hoàn tiền"
- Hệ thống tính toán số tiền hoàn tiền:
  - Giá gốc của mặt hàng
  - Trừ phí tái nhập kho (nếu áp dụng)
  - Trừ chi phí vận chuyển (nếu không hoàn tiền)
- Tạo hoàn tiền (liên kết với yêu cầu trả hàng)
- Trạng thái → `hoàn tất`

---

## Lý do Trả hàng theo từng mặt hàng

Khách hàng chọn lý do cho từng mặt hàng:

**Lý do phổ biến**:
- Nhận sai mặt hàng
- Mặt hàng hỏng/hư hại
- Thay đổi ý định/không cần nữa
- Mặt hàng không khớp mô tả
- Tìm thấy giá tốt hơn
- Đặt nhầm
- Chất lượng không như mong đợi

**Sử dụng lý do để**:
- Phân tích (theo dõi nguyên nhân trả hàng phổ biến)
- Kiểm soát chất lượng (xác định sản phẩm hỏng)
- Cải thiện quy trình (giảm trả hàng có thể tránh được)

---

## Phí Tái nhập kho

Áp dụng phí để bù đắp chi phí xử lý trả hàng:

**Cấu hình**:
- **Loại**: Phần trăm (ví dụ, 15%) hoặc Cố định (ví dụ, $5)
- **Khi áp dụng**: Trả hàng không hỏng, mặt hàng đã mở, đặt hàng đặc biệt

**Ví dụ**:
```
Mua ban đầu: $100
Phí tái nhập kho: 15%
Số tiền hoàn tiền: $85
```

**Thực hành tốt nhất**:
- Truyền đạt rõ ràng chính sách phí tái nhập kho
- Không áp dụng cho mặt hàng hỏng
- Xem xét miễn phí cho khách hàng VIP

---

## Hướng dẫn Kiểm tra Trả hàng

Thiết lập tiêu chí kiểm tra nhất quán:

**Tuyệt vời**:
- Bao bì nguyên chưa mở
- Không có dấu hiệu mài mòn
- Tất cả phụ kiện đi kèm
- Có thể bán lại với đầy đủ giá

**Tốt**:
- Đã mở nhưng sử dụng ít
- Mài mòn bao bì nhẹ
- Tất cả các bộ phận có mặt
- Có thể bán lại với đầy đủ giá

**Chấp nhận được**:
- Dấu hiệu sử dụng/mài mòn rõ rệt
- Bao bì bị hư hại
- Thiếu phụ kiện không thiết yếu
- Có thể bán lại với giảm giá

**Hỏng**:
- Bị hư hại vật lý
- Thiếu linh kiện
- Không thể bán lại
- Cần loại bỏ hoặc sửa chữa

**Độc hại**:
- Lỗi sản xuất
- Sự cố chức năng
- Yêu cầu bảo hành
- Trả lại nhà sản xuất

---

## Lựa chọn Vận chuyển Trả hàng

**Tùy chọn 1: Khách hàng thanh toán vận chuyển trả hàng**
- Không cung cấp nhãn trả hàng
- Khách hàng chọn nhà vận chuyển riêng
- Nhập số theo dõi thủ công

**Tùy chọn 2: Người bán cung cấp nhãn trả hàng đã thanh toán**
- Tạo nhãn trả hàng qua tài khoản nhà cung cấp
- Chi phí được trừ khỏi hoàn tiền HOẶC người bán chịu chi phí
- Theo dõi được đồng bộ tự động

**Tùy chọn 3: Vận chuyển trả hàng miễn phí**
- Người bán chịu chi phí vận chuyển trả hàng
- Nâng cao sự hài lòng của khách hàng
- Tăng tỷ lệ trả hàng (xem xét sự đánh đổi)

---

## Lọc & Báo cáo

**Lọc hữu ích**:
- Trạng thái: Đang chờ (cần hành động)
- Khoảng thời gian: 30 ngày gần đây
- Đơn hàng: Tra cứu đơn hàng cụ thể
- Lý do: Theo dõi nguyên nhân trả hàng

**Phân tích Trả hàng**:
- Tỷ lệ trả hàng theo sản phẩm
- Lý do trả hàng phổ biến nhất
- Thời gian xử lý trung bình (đang chờ → hoàn tất)
- Doanh thu phí tái nhập kho

---

## Mẹo

- **Thiết lập chính sách hoàn tiền rõ ràng** - Truyền đạt thời gian (30 ngày), điều kiện, phí
- **Xử lý yêu cầu nhanh chóng** - Trả lời các yêu cầu đang chờ trong vòng 24 giờ
- **Kiểm tra kỹ lưỡng** - Ghi lại tình trạng để tránh tranh chấp
- **Theo dõi lý do trả hàng** - Sử dụng dữ liệu để cải thiện sản phẩm/mô tả
- **Tự động hóa khi có thể** - Webhook nhà vận chuyển tự động cập nhật trạng thái vận chuyển
- **Giao tiếp với khách hàng** - Gửi email cập nhật tại mỗi thay đổi trạng thái
- **Công bằng với phí tái nhập kho** - Áp dụng nhất quán, miễn phí cho lỗi sản phẩm
- **Theo dõi gian lận trả hàng** - Đánh dấu khách hàng có nhiều lần trả hàng
- **Cải thiện bao bì** - Giảm trả hàng liên quan đến hư hỏng
- **Cập nhật tồn kho kịp thời** - Khôi phục tồn kho sau khi kiểm tra
- **Học hỏi từ các mô hình** - Tỷ lệ trả hàng cao cho sản phẩm cụ thể có thể chỉ ra vấn đề chất lượng