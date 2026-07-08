---
title: Cài đặt vận chuyển
---

Cài đặt vận chuyển xác định các nhà vận chuyển thủ công (DHL, FedEx, UPS, nhà vận chuyển tùy chỉnh) cho các đơn hàng được tạo mà không cần tích hợp API—mỗi cài đặt vận chuyển cung cấp biểu tượng nhà vận chuyển, mẫu URL theo dõi và cài đặt hiển thị. Các cài đặt hệ thống (DHL, FedEx, UPS, USPS) đã được cấu hình sẵn và không thể xóa, trong khi các cài đặt tùy chỉnh cho phép các nhà bán hàng thêm các nhà vận chuyển khu vực hoặc chuyên dụng. Cài đặt vận chuyển liên kết với các đơn hàng thủ công nơi các nhà bán hàng nhập số theo dõi thủ công thay vì mua nhãn qua API của nhà cung cấp.

Sử dụng cài đặt vận chuyển khi tạo đơn hàng thủ công hoặc khi bạn muốn có liên kết theo dõi mà không cần tích hợp đầy đủ API.

## Cài đặt hệ thống vs Cài đặt tùy chỉnh

**Cài đặt hệ thống** (Đã cài đặt sẵn):
- DHL, FedEx, UPS, USPS, Royal Mail, Canada Post, Australia Post
- Không thể xóa (is_system=True)
- Có thể thay đổi mẫu URL theo dõi hoặc biểu tượng
- Mẫu URL theo dõi mặc định được cung cấp

**Cài đặt tùy chỉnh** (Tạo bởi nhà bán hàng):
- Các nhà vận chuyển khu vực (OnTrac, LaserShip, dịch vụ bưu điện khu vực)
- Các nhà vận chuyển chuyên dụng (vận chuyển hàng hóa, giao hàng theo yêu cầu đặc biệt)
- Có thể chỉnh sửa hoặc xóa
- Yêu cầu mẫu URL theo dõi thủ công

---

## Cấu hình cài đặt vận chuyển

Mỗi cài đặt xác định:

**Cài đặt cơ bản**:
- **Tên**: Tên hiển thị của nhà vận chuyển (ví dụ: "DHL Express", "Dịch vụ giao hàng địa phương")
- **Mã**: Nhận dạng nội bộ (ví dụ: "dhl", "local_courier")
- **Biểu tượng**: Hình ảnh biểu tượng của nhà vận chuyển (tùy chọn, sử dụng biểu tượng nếu không cung cấp)
- **Biểu tượng**: Biểu tượng FontAwesome làm phương án dự phòng (ví dụ: "fa-truck")
- **Kích hoạt**: Bật/tắt hiển thị

**Cấu hình theo dõi**:
- **Mẫu URL theo dõi**: Mẫu URL có chứa ký tự đặt chỗ {tracking_id}
- **Mẫu URL theo dõi tùy chỉnh**: URL tùy chỉnh (ghi đè mẫu mặc định)

**Cài đặt hệ thống** (chỉ dành cho cài đặt hệ thống):
- **Là hệ thống**: Không thể xóa
- **Là mặc định**: Một mẫu mặc định cho mỗi loại nhà vận chuyển

---

## Mẫu URL theo dõi

Các URL theo dõi sử dụng ký tự đặt chỗ {tracking_id}:

**Ví dụ**:

DHL: `https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx: `https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS: `https://www.ups.com/track?tracknum={tracking_id}`

USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

Tùy chỉnh: `https://track.localcourier.com/tracking/{tracking_id}`

**Cách hoạt động**:
1. Nhà bán hàng tạo đơn hàng với số theo dõi là "1234567890"
2. Hệ thống thay thế {tracking_id} bằng số thực tế
3. Khách hàng nhấp vào liên kết theo dõi → chuyển hướng đến trang web của nhà vận chuyển
4. Kết quả: `https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## Tạo cài đặt vận chuyển tùy chỉnh

**Bước-by-step**:

1. Điều hướng đến Cài đặt > Giao hàng > Cài đặt vận chuyển
2. Nhấp vào "Thêm cài đặt vận chuyển"
3. Nhập tên (ví dụ: "OnTrac")
4. Nhập mã (slug: "ontrac")
5. Tùy chọn: Tải lên hình ảnh biểu tượng
6. Chọn biểu tượng (fa-truck, fa-shipping-fast, v.v.)
7. Nhập mẫu URL theo dõi với {tracking_id}
8. Bật chế độ kích hoạt = Có
9. Lưu

**Ví dụ - OnTrac**:
```
Tên: OnTrac
Mã: ontrac
Mẫu URL theo dõi: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
Biểu tượng: fa-truck
Kích hoạt: Có
```

---

## Ghi đè URL theo dõi của cài đặt hệ thống

Các cài đặt hệ thống có thể có URL theo dõi được ghi đè:

**Trường hợp sử dụng**: Tài khoản nhà vận chuyển của bạn có cổng theo dõi đặc biệt

**Cách ghi đè**:
1. Chỉnh sửa cài đặt hệ thống (ví dụ: DHL)
2. Nhập URL ghi đè trong trường "Mẫu URL theo dõi ghi đè"
3. URL ghi đè sẽ ưu tiên hơn mẫu mặc định
4. Lưu

**Ví dụ**:
```
Hệ thống: DHL
URL mặc định: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
URL ghi đè: https://track.dhl.com/special-account/{tracking_id}
Kết quả: URL ghi đè được sử dụng cho tất cả các đơn hàng DHL
```

---

## Biểu tượng nhà vận chuyển

**Hướng dẫn biểu tượng**:
- Định dạng: PNG hoặc SVG (SVG được khuyến khích vì khả năng mở rộng)
- Kích thước: 200×60px được khuyến nghị
- Nền: Trong suốt hoặc trắng
- Màu sắc: Thương hiệu đầy màu sắc của nhà vận chuyển

**Biểu tượng dự phòng**:
Nếu không tải lên biểu tượng, hệ thống sẽ hiển thị biểu tượng FontAwesome:
- fa-truck (mặc định)
- fa-shipping-fast (giao hàng nhanh)
- fa-plane (vận chuyển hàng không)
- fa-box (đơn hàng)

---

## Sử dụng cài đặt vận chuyển trong đơn hàng

Khi tạo đơn hàng thủ công:

1. Đơn hàng > Chi tiết đơn hàng > Tạo đơn hàng
2. Chọn chế độ "Đơn hàng thủ công"
3. Chọn nhà vận chuyển từ danh sách thả xuống cài đặt
4. Nhập số theo dõi
5. Tùy chọn: Ghi đè URL theo dõi cho đơn hàng này
6. Lưu

**Hiển thị đơn hàng**:
- Biểu tượng nhà vận chuyển được hiển thị (hoặc biểu tượng)
- Số theo dõi được hiển thị
- Liên kết theo dõi có thể nhấp (sử dụng mẫu URL cài đặt)

---

## Nhà vận chuyển mặc định

Một cài đặt có thể được đặt làm mặc định cho hệ thống:

**Trường hợp sử dụng**: Nhà vận chuyển được sử dụng phổ biến nhất được chọn tự động khi tạo đơn hàng

**Cách thiết lập**:
1. Chỉnh sửa cài đặt vận chuyển
2. Chọn "Là mặc định"
3. Lưu
4. Cài đặt mặc định trước đó (nếu có) sẽ tự động hủy kích hoạt

**Chỉ cho phép một cài đặt mặc định** - thiết lập cài đặt mặc định mới sẽ xóa cờ mặc định trước đó.

---

## Một số lưu ý

- **Sử dụng tên mô tả** - "DHL Express" tốt hơn "DHL"
- **Kiểm tra URL theo dõi** - Xác minh mẫu hoạt động với số theo dõi thực tế
- **Tải lên biểu tượng nhà vận chuyển** - Tạo kiểu chuyên nghiệp trong email gửi đến khách hàng
- **Không xóa cài đặt hệ thống** - Chúng đã được cấu hình sẵn đúng cách
- **Sử dụng ghi đè một cách tiết kiệm** - Chỉ khi nhà vận chuyển thay đổi hệ thống theo dõi
- **Thiết lập mặc định cho nhà vận chuyển chính** - Tiết kiệm thời gian khi tạo đơn hàng
- **Giữ cài đặt vận chuyển đang hoạt động** - Chỉ tắt kích hoạt nếu nhà vận chuyển ngừng hoạt động
- **Ghi chú các nhà vận chuyển tùy chỉnh** - Thêm ghi chú về các nhà vận chuyển khu vực

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.