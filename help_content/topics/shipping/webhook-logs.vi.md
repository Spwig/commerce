---
title: Lịch sử Webhook
---

Lịch sử Webhook cung cấp bản ghi kiểm toán vĩnh viễn cho tất cả các yêu cầu Webhook đầu vào từ nhà vận chuyển—ghi lại phương thức yêu cầu, URL điểm cuối, tiêu đề, tải trọng, trạng thái xử lý (đang chờ/đã xử lý/thất bại), và phản hồi. Mỗi Webhook được ghi lại trước khi xử lý để đảm bảo không có sự kiện nào bị mất nếu xử lý thất bại. Các bản ghi cho phép gỡ lỗi các vấn đề tích hợp Webhook, giám sát độ tin cậy API nhà vận chuyển, và tái tạo lịch trình giao hàng cho hỗ trợ khách hàng.

Trang quản trị chỉ đọc này giúp khắc phục sự cố Webhook và xác minh sức khỏe tích hợp nhà vận chuyển.

## Cấu trúc Lịch sử Webhook

Mỗi bản ghi ghi lại:

**Chi tiết Yêu cầu**:
- **Provider Key**: Nhà vận chuyển đã gửi Webhook (fedex, ups, dhl)
- **Endpoint**: Đường dẫn URL Webhook (ví dụ: `/webhooks/shipping/fedex/`)
- **Method**: Phương thức HTTP (thường là POST)
- **Headers**: Tiêu đề yêu cầu (JSON)
- **Payload**: Nội dung yêu cầu (JSON)

**Xử lý**:
- **Processing Status**: đang chờ, đã xử lý, thất bại
- **Error Message**: Lý do thất bại (nếu trạng thái=thất bại)
- **Response**: Phản hồi HTTP gửi đến nhà vận chuyển
- **Response Status Code**: 200, 400, 500, v.v.

**Thời gian**:
- **Received At**: Khi Webhook đến
- **Processed At**: Khi xử lý hoàn thành

---

## Giá trị Trạng thái Xử lý

**đang chờ**: Webhook đã nhận, đang chờ xử lý
- Bình thường trong vài giây sau khi nhận
- Nếu bị kẹt ở trạng thái đang chờ, cho thấy hàng đợi xử lý bị nghẽn

**đã xử lý**: Webhook đã được xử lý thành công
- Tạo TrackingEvent
- Gửi thông báo cho khách hàng (nếu áp dụng)
- Gửi phản hồi 200 đến nhà vận chuyển

**thất bại**: Xử lý Webhook thất bại
- Kiểm tra trường error_message để biết lý do
- Nguyên nhân phổ biến: JSON không hợp lệ, kiện hàng không tồn tại, sự kiện trùng lặp

---

## Luồng Webhook

**Luồng làm việc bình thường**:
```
1. Nhà vận chuyển quét kiện hàng
   ↓
2. Nhà vận chuyển gửi POST đến điểm cuối Webhook của Spwig
   ↓
3. Spwig tạo WebhookLog (trạng thái=đang chờ)
   ↓
4. Công việc nền tảng xử lý Webhook
   ↓
5. Phân tích tải trọng JSON
   ↓
6. Tìm kiện hàng khớp (theo số theo dõi)
   ↓
7. Tạo TrackingEvent
   ↓
8. Cập nhật WebhookLog (trạng thái=đã xử lý)
   ↓
9. Gửi phản hồi HTTP 200 đến nhà vận chuyển
```

**Tình huống thất bại**:
- **JSON không hợp lệ**: Nhà vận chuyển gửi dữ liệu bị lỗi → trạng thái=thất bại, lỗi="Lỗi phân tích JSON"
- **Không tìm thấy kiện hàng**: Số theo dõi không khớp với bất kỳ kiện hàng nào → trạng thái=thất bại, lỗi="Không tìm thấy kiện hàng"
- **Bản sao**: Sự kiện đã tồn tại → trạng thái=thất bại, lỗi="Sự kiện trùng lặp"

---

## Gỡ lỗi sự cố Webhook

**Bước-by-bước**:

**1. Lọc theo Trạng thái=Thất bại**
- Điều hướng đến Giao hàng > Lịch sử Webhook
- Lọc: Trạng thái Xử lý = "thất bại"
- Xem các sự cố gần đây

**2. Kiểm tra Thông báo lỗi**
- Nhấp vào mục ghi nhật ký
- Đọc trường error_message
- Lỗi phổ biến:
  - "Không tìm thấy kiện hàng" → Mismatch số theo dõi
  - "Lỗi giải mã JSON" → Nhà vận chuyển gửi JSON không hợp lệ
  - "Thiếu trường bắt buộc" → Tải trọng thiếu dữ liệu mong đợi

**3. Kiểm tra Tải trọng**
- Xem tải trọng JSON gốc
- Đảm bảo cấu trúc khớp với định dạng mong đợi
- Kiểm tra các trường bị thiếu (tracking_id, event_type, v.v.)

**4. Xác minh Kiện hàng tồn tại**
- Trích xuất số theo dõi từ tải trọng
- Tìm kiếm Kiện hàng theo số theo dõi
- Đảm bảo kiện hàng tồn tại và sử dụng nhà vận chuyển đúng

**5. Kiểm tra Cấu hình Nhà vận chuyển**
- Xác minh tài khoản nhà vận chuyển đang hoạt động
- Xác nhận URL điểm cuối Webhook chính xác
- Kiểm tra thông tin xác thực API nhà vận chuyển

**6. Thử lại Xử lý** (nếu áp dụng)
- Một số công cụ xử lý Webhook hỗ trợ thử lại thủ công
- Sửa lỗi nền tảng trước
- Thử lại Webhook thất bại

---

## Các vấn đề Webhook phổ biến

**Vấn đề 1: 'Không tìm thấy kiện hàng'**

**Nguyên nhân**: Số theo dõi trong Webhook không khớp với bất kỳ kiện hàng nào
- Sai chính tả khi tạo kiện hàng
- Webhook cho tài khoản khác
- Kiện hàng đã xóa trước khi nhận Webhook

**Giải pháp**:
- Xác minh chính tả số theo dõi
- Kiểm tra nhà vận chuyển kiện hàng khớp với nhà cung cấp Webhook
- Tạo lại kiện hàng nếu cần

---

**Vấn đề 2: 'Lỗi giải mã JSON'**

**Nguyên nhân**: Nhà vận chuyển gửi JSON bị lỗi
- Hiếm gặp, thường do lỗi API nhà vận chuyển
- Vấn đề mã hóa ký tự

**Giải pháp**:
- Liên hệ hỗ trợ nhà vận chuyển với tải trọng gốc
- Kiểm tra tiêu đề để xem mã hóa charset
- Xác minh URL điểm cuối trong bảng điều khiển nhà vận chuyển

---

**Vấn đề 3: Webhook trùng lặp**

**Nguyên nhân**: Nhà vận chuyển gửi cùng sự kiện nhiều lần
- Cơ chế thử lại (nhà vận chuyển không nhận được phản hồi 200)
- Lỗi nhà vận chuyển

**Giải pháp**:
- Hệ thống tự động từ chối các bản sao (hành vi bình thường)
- Xác minh response_status_code là 200
- Nếu tình trạng kéo dài, liên hệ hỗ trợ nhà vận chuyển

---

**Vấn đề 4: Webhook bị thiếu**

**Nguyên nhân**: Webhook mong đợi chưa bao giờ nhận được
- Nhà vận chuyển không gửi (quét bị bỏ sót)
- URL điểm cuối được cấu hình sai trong bảng điều khiển nhà vận chuyển
- Tường lửa chặn yêu cầu

**Giải pháp**:
- Kiểm tra thiết lập Webhook trong bảng điều khiển nhà vận chuyển
- Xác minh URL điểm cuối công khai và có thể truy cập
- Thử URL điểm cuối bằng curl/Postman
- Kiểm tra quy tắc tường lửa máy chủ

---

## Cấu hình URL điểm cuối Webhook

**URL Webhook tiêu biểu**:
```
FedEx: https://yourdomain.com/webhooks/shipping/fedex/
UPS: https://yourdomain.com/webhooks/shipping/ups/
DHL: https://yourdomain.com/webhooks/shipping/dhl/
```

**Thiết lập trong Bảng điều khiển Nhà vận chuyển**:
1. Đăng nhập vào cổng thông tin phát triển nhà vận chuyển
2. Điều hướng đến cài đặt Webhook
3. Nhập URL Webhook của Spwig
4. Chọn các sự kiện cần đăng ký (cập nhật theo dõi, giao hàng, ngoại lệ)
5. Lưu cấu hình
6. Thử Webhook bằng công cụ kiểm tra của nhà vận chuyển

**Bảo mật**:
- Webhook yêu cầu HTTPS (không phải HTTP)
- Một số nhà vận chuyển ký yêu cầu (xác minh chữ ký)
- Danh sách trắng IP (nếu nhà vận chuyển cung cấp IP tĩnh)

---

## Giám sát sức khỏe Webhook

**Chỉ số chính**:

**Tỷ lệ thành công**:
```
Tỷ lệ thành công = (Đã xử lý / Tổng số) × 100%

Mục tiêu: >98%
```

**Thời gian xử lý**:
```
Thời gian trung bình = Thời gian xử lý - Thời gian nhận

Mục tiêu: <2 giây
```

**Mẫu thất bại**:
- Sudden tăng đột biến thất bại → Thay đổi hoặc sự cố API nhà vận chuyển
- Luôn "Không tìm thấy kiện hàng" → Vấn đề đồng bộ số theo dõi
- Tất cả Webhook thất bại → Vấn đề cấu hình điểm cuối

**Chiến lược giám sát**:
- Kiểm tra tỷ lệ thất bại hàng ngày
- Cảnh báo nếu tỷ lệ thất bại >5%
- Xem xét thông báo lỗi hàng tuần
- So sánh với bảng trạng thái nhà vận chuyển

---

## Lưu trữ Webhook

**Lịch sử là vĩnh viễn** - không bao giờ tự động xóa

**Lý do vĩnh viễn**:
- Tuân thủ kiểm toán
- Hỗ trợ khách hàng (tái tạo lịch trình giao hàng)
- Giải quyết tranh chấp
- Gỡ lỗi Webhook

**Lưu trữ**: Lịch sử được lưu trữ hiệu quả (JSON nén)

---

## Gợi ý

- **Webhook là bản ghi kiểm toán vĩnh viễn** - Không bao giờ xóa, ngay cả khi xử lý thành công
- **Kiểm tra Webhook thất bại hàng ngày** - Phát hiện sớm vấn đề tích hợp
- **Giám sát độ trễ xử lý** - Độ trễ dài cho thấy vấn đề hiệu suất
- **Lưu trữ tải trọng gốc** - Thiết yếu để gỡ lỗi thay đổi API nhà vận chuyển
- **Kiểm tra cấu hình điểm cuối** - Sử dụng công cụ kiểm tra của nhà vận chuyển để xác minh thiết lập
- **Kích hoạt chữ ký Webhook** - Xác minh yêu cầu thực sự đến từ nhà vận chuyển
- **Danh sách trắng IP nhà vận chuyển** - Nếu nhà vận chuyển cung cấp dải IP tĩnh
- **Thiết lập cảnh báo** - Thông báo khi tỷ lệ thất bại vượt ngưỡng
- **So sánh với trạng thái nhà vận chuyển** - Khoảng trống Webhook có thể chỉ ra sự cố nhà vận chuyển
- **Ghi lại định dạng tải trọng nhà vận chuyển** - Hỗ trợ khi nhà vận chuyển cập nhật API
- **Giữ URL Webhook ổn định** - Thay đổi URL yêu cầu cập nhật bảng điều khiển nhà vận chuyển
