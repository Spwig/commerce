---
title: Theo dõi sự kiện
---

Các sự kiện theo dõi ghi lại các mốc trạng thái vận chuyển trong suốt vòng đời giao hàng—mỗi sự kiện ghi lại trạng thái (đang vận chuyển, đang được giao, đã giao), thời gian, vị trí, mô tả và dữ liệu nhà vận chuyển gốc. Các sự kiện được tạo tự động qua thông báo webhook của nhà vận chuyển hoặc được tạo thủ công bởi người bán hàng. Khách hàng có thể xem lịch sử sự kiện theo dõi trong tài khoản của họ và email xác nhận đơn hàng, cung cấp khả năng theo dõi giao hàng thời gian thực.

Trang quản trị này hiển thị lịch sử sự kiện chỉ đọc để kiểm toán và hỗ trợ khách hàng.

## Cấu trúc sự kiện theo dõi

Mỗi sự kiện chứa:

**Thông tin trạng thái**:
- **Trạng thái**: in_transit, out_for_delivery, delivered, exception, failed, returned
- **Mô tả**: Trạng thái dễ đọc (ví dụ: "Gói hàng đã đến cơ sở phân loại")
- **Mã trạng thái nhà vận chuyển**: Trạng thái gốc của nhà vận chuyển (ví dụ: "DEP" cho đã rời đi)

**Dữ liệu vị trí**:
- **Thành phố**: Thành phố vị trí sự kiện
- **Tỉnh/Thành phố**: Tỉnh/Thành phố vị trí sự kiện
- **Quốc gia**: Quốc gia vị trí sự kiện
- **Mã bưu chính**: Mã ZIP/mã bưu chính vị trí sự kiện

**Thời gian ghi nhận**:
- **Xảy ra lúc**: Thời điểm sự kiện thực sự xảy ra (thời gian nhà vận chuyển)
- **Tạo lúc**: Thời điểm sự kiện được ghi nhận trong Spwig (thời gian hệ thống)

**Thông tin bổ sung**:
- **Dữ liệu gốc**: Trả lời đầy đủ từ API nhà vận chuyển dưới dạng JSON
- **Giao hàng**: ID giao hàng liên kết

---

## Các loại trạng thái sự kiện

**in_transit**: Gói hàng đang di chuyển trong mạng lưới nhà vận chuyển
- Ví dụ: "Đã rời cơ sở", "Đã đến trung tâm", "Đang vận chuyển đến cơ sở tiếp theo"

**out_for_delivery**: Gói hàng đang trên xe giao hàng
- Ví dụ: "Đang được giao", "Đang trên xe giao hàng"

**delivered**: Gói hàng đã được giao thành công
- Ví dụ: "Đã giao đến cửa trước", "Để lại tại phòng lễ tân", "Giao cho người nhận"

**exception**: Vấn đề giao hàng cần được xử lý
- Ví dụ: "Chậm do thời tiết", "Địa chỉ sai", "Thử giao hàng thất bại"

**failed**: Giao hàng thất bại vĩnh viễn
- Ví dụ: "Không thể giao theo địa chỉ", "Bị từ chối bởi người nhận"

**returned**: Gói hàng đang được trả lại cho người gửi
- Ví dụ: "Khởi động trả lại người gửi", "Gói hàng đang được trả lại"

---

## Cách tạo sự kiện theo dõi

### Tự động (Webhook nhà vận chuyển)

**Luồng công việc**:
1. Nhà vận chuyển quét gói hàng (rời đi, đến, giao hàng)
2. Nhà vận chuyển gửi webhook đến điểm cuối webhook của Spwig
3. Webhook được ghi lại trong bảng WebhookLog
4. Hệ thống phân tích tải trọng webhook
5. Tạo TrackingEvent với dữ liệu được trích xuất
6. Gửi thông báo email cho khách hàng (nếu được cấu hình)

**Lợi ích**:
- Cập nhật thời gian thực (không cần polling)
- Thời gian chính xác từ nhà vận chuyển
- Lịch sử sự kiện đầy đủ được duy trì tự động

### Thủ công (Nhập bởi người bán)

**Luồng công việc**:
1. Truy cập chi tiết giao hàng
2. Nhấp vào "Thêm sự kiện theo dõi"
3. Chọn trạng thái từ danh sách thả xuống
4. Nhập mô tả
5. Tùy chọn: Nhập dữ liệu vị trí
6. Thiết lập thời gian xảy ra occurred_at
7. Lưu

**Các trường hợp sử dụng**:
- Nhà vận chuyển không hỗ trợ webhook
- Sửa đổi giao hàng thủ công
- Giao hàng địa phương (không qua nhà vận chuyển)
- Cập nhật trạng thái nội bộ

---

## Thứ tự hiển thị sự kiện

Các sự kiện được hiển thị theo **thứ tự ngược thời gian** (mới nhất trước):

**Ví dụ hiển thị**:
```
13 tháng 2, 2026 10:30 AM - Đã giao (Brooklyn, NY)
13 tháng 2, 2026 08:15 AM - Đang được giao (Brooklyn, NY)
12 tháng 2, 2026 11:45 PM - Đã đến cơ sở địa phương (Brooklyn, NY)
12 tháng 2, 2026 06:30 PM - Đang vận chuyển (Newark, NJ)
12 tháng 2, 2026 02:15 PM - Đã rời điểm xuất phát (Philadelphia, PA)
12 tháng 2, 2026 09:00 AM - Đã nhận (Philadelphia, PA)
```

---

## Tính năng hiển thị cho khách hàng

Các sự kiện theo dõi được hiển thị cho khách hàng trong:

**Email xác nhận đơn hàng**:
- Trạng thái sự kiện mới nhất
- Ngày giao hàng dự kiến
- Liên kết theo dõi

**Tài khoản khách hàng > Chi tiết đơn hàng**:
- Toàn bộ dòng thời gian sự kiện
- Mô tả sự kiện
- Lịch sử vị trí
- Thời gian ghi nhận

**Trang theo dõi** (nếu được kích hoạt):
- URL theo dõi riêng
- Dòng thời gian trực quan
- Biểu tượng nhà vận chuyển
- Bản đồ giao hàng (nếu có dữ liệu vị trí)

---

## Lọc sự kiện theo dõi

**Lọc hữu ích**:
- **Giao hàng**: Xem sự kiện cho giao hàng cụ thể
- **Trạng thái**: Lọc theo loại sự kiện (đã giao, in_transit, v.v.)
- **Khoảng thời gian**: Sự kiện trong khoảng thời gian
- **Vị trí**: Sự kiện tại thành phố/tỉnh cụ thể

**Các trường hợp sử dụng**:
- "Hiển thị tất cả các giao hàng đã giao hôm nay"
- "Tìm tất cả các ngoại lệ trong tuần trước"
- "Theo dõi các giao hàng đang trong quá trình vận chuyển"

---

## Dữ liệu gốc (Gỡ lỗi)

**Trường dữ liệu gốc**:
- Lưu trữ đầy đủ phản hồi API nhà vận chuyển dưới dạng JSON
- Hữu ích để gỡ lỗi các vấn đề webhook
- Chứa thông tin trung gian đặc thù của nhà vận chuyển

**Ví dụ dữ liệu gốc** (FedEx):
```json
{
  "event_type": "OD",
  "event_description": "Out for delivery",
  "timestamp": "2026-02-13T08:15:00Z",
  "location": {
    "city": "Brooklyn",
    "state": "NY",
    "postal_code": "11201",
    "country": "US"
  },
  "delivery_signature": null,
  "estimated_delivery": "2026-02-13T17:00:00Z"
}
```

**Khi kiểm tra dữ liệu gốc**:
- Mô tả sự kiện không rõ ràng
- Thiếu dữ liệu vị trí
- Lỗi xử lý webhook
- Nâng cấp hỗ trợ nhà vận chuyển

---

## Thời gian sự kiện

**Occurred At** vs **Created At**:

**Occurred At**: Thời điểm sự kiện vận chuyển thực sự xảy ra
- Ví dụ: Gói hàng được quét lúc 10:30 AM

**Created At**: Thời điểm Spwig nhận được webhook
- Ví dụ: Webhook được nhận lúc 10:32 AM (chênh lệch 2 phút)

**Tại sao khác nhau?**:
- Độ trễ mạng
- Xử lý theo lô của nhà vận chuyển
- Độ trễ retry webhook

**Sử dụng Occurred At để hiển thị cho khách hàng** - phản ánh chính xác hơn tiến độ giao hàng thực tế.

---

## Một số mẹo

- **Sự kiện là chỉ đọc** - Không thể chỉnh sửa sau khi tạo (đảm bảo tính toàn vẹn kiểm toán)
- **Kiểm tra dữ liệu gốc để có chi tiết** - Nhiều thông tin hơn các trường được hiển thị
- **Theo dõi độ trễ webhook** - Độ trễ lớn giữa occurred_at và created_at cho thấy vấn đề webhook
- **Sử dụng cho hỗ trợ khách hàng** - Dòng thời gian sự kiện giúp chẩn đoán vấn đề giao hàng
- **Theo dõi mô hình giao hàng** - Phân tích thời gian sự kiện để đánh giá hiệu suất nhà vận chuyển
- **Cấu hình thông báo** - Gửi email tự động cho khách hàng khi xảy ra sự kiện quan trọng (out_for_delivery, delivered)
- **Không xóa sự kiện** - Giữ nguyên toàn bộ dòng thời gian kiểm toán
- **Kiểm tra WebhookLog để phát hiện lỗi** - Thiếu sự kiện có thể chỉ ra lỗi xử lý webhook
- **Dữ liệu vị trí thay đổi tùy nhà vận chuyển** - Một số nhà vận chuyển cung cấp vị trí chi tiết, một số ít nhất
- **Sự kiện ngoại lệ cần được chú ý** - Theo dõi và xử lý các ngoại lệ giao hàng