---
title: Tùy chỉnh Mẫu Phiếu thu
---

Mẫu phiếu thu kiểm soát kiểu dáng và nội dung của các phiếu thu in nhiệt được in tại các máy POS của bạn. Tùy chỉnh văn bản tiêu đề và chân trang, thêm biểu tượng logo của bạn, cấu hình các trường tuân thủ (số thuế, số đăng ký kinh doanh), và bao gồm mã QR quảng bá. Các mẫu hỗ trợ nhắm mục tiêu phạm vi - tạo mẫu mặc định cho tất cả các cửa hàng, mẫu cụ thể cho nhóm khu vực, hoặc mẫu cụ thể cho từng địa điểm. Hệ thống sử dụng các quy tắc ưu tiên phạm vi để xác định mẫu nào được áp dụng khi in phiếu thu.

Sử dụng mẫu phiếu thu để duy trì tính nhất quán thương hiệu, đáp ứng các yêu cầu tuân thủ khu vực và tăng cường sự tương tác của khách hàng thông qua các yếu tố quảng bá.

![Danh sách Mẫu Phiếu thu](/static/core/admin/img/help/receipt-template-customization/receipt-list.webp)

## Cơ bản về Mẫu Phiếu thu

Mẫu phiếu thu xác định cấu trúc và nội dung của các phiếu thu được in từ máy in nhiệt ESC/POS. Mỗi mẫu chỉ định:

**Cấu hình vật lý**:
- Chiều rộng giấy (58mm hoặc 80mm)
- Hình ảnh logo (đơn sắc cho in nhiệt)
- Kích thước và khoảng cách chữ

**Các phần nội dung**:
- Văn bản tiêu đề (tên cửa hàng, địa chỉ, thông tin liên hệ)
- Dữ liệu giao dịch động (sản phẩm, giá cả, tổng số, phương thức thanh toán)
- Văn bản chân trang (chính sách hoàn tiền, lời cảm ơn, mạng xã hội)
- Các trường tuân thủ (số thuế, số đăng ký kinh doanh)
- Mã QR quảng bá có nhãn

**Mục tiêu phạm vi**:
- Mẫu mặc định (áp dụng cho tất cả các cửa hàng trừ khi bị ghi đè)
- Mẫu nhóm (áp dụng cho tất cả các cửa hàng trong nhóm)
- Mẫu cửa hàng (áp dụng cho một cửa hàng/kho cụ thể)

## Quy tắc Ưu tiên Phạm vi

Khi máy POS in phiếu thu, hệ thống chọn mẫu bằng cách sử dụng thứ tự phân cấp này (ưu tiên cao nhất đến thấp nhất):

| Ưu tiên | Phạm vi | Ví dụ | Trường hợp sử dụng |
|----------|-------|---------|----------|
| **1** | Cửa hàng cụ thể | Mẫu phiếu thu Paris Store | Yêu cầu tuân thủ thuế riêng biệt của Pháp |
| **2** | Nhóm cụ thể | Mẫu phiếu thu European Stores | Hiển thị thuế VAT cho tất cả các địa điểm tại châu Âu |
| **3** | Mặc định | Mẫu phiếu thu toàn cầu | Mẫu dự phòng cho tất cả các cửa hàng chưa được cấu hình |

**Cách hoạt động**:
1. Kiểm tra xem cửa hàng có mẫu riêng (cụ thể cho kho) hay không
2. Nếu không, kiểm tra xem nhóm cửa hàng có mẫu nhóm hay không
3. Nếu không, sử dụng mẫu mặc định

**Ví dụ**:
- Mẫu mặc định: "Standard Receipt" (không gán phạm vi)
- Mẫu nhóm: "EU Receipt" (gán cho nhóm European Stores) - bao gồm đăng ký VAT
- Mẫu cửa hàng: "Paris Receipt" (gán cho kho Paris) - bao gồm số SIRET của Pháp

**Kết quả**:
- Máy POS tại Paris Store: Sử dụng "Paris Receipt" (cụ thể nhất)
- Máy POS tại Berlin Store (thuộc nhóm European Stores, không có mẫu cửa hàng): Sử dụng "EU Receipt" (mức độ nhóm)
- Máy POS tại New York Store (không có nhóm, không có mẫu cửa hàng): Sử dụng "Standard Receipt" (mẫu dự phòng mặc định)

## Cấu hình Chiều rộng Giấy

Máy in nhiệt phiếu thu sử dụng giấy có chiều rộng 58mm hoặc 80mm. Chọn tùy theo phần cứng máy in của bạn:

| Chiều rộng giấy | Số ký tự mỗi dòng | Tốt nhất cho | Mục đích sử dụng điển hình |
|-------------|---------------------|----------|-------------|
| **58mm** | ~32 ký tự | Kích thước nhỏ, di động | Xe bán hàng ăn nhẹ, POS di động, quầy tự phục vụ |
| **80mm** | ~48 ký tự | Bán lẻ tiêu chuẩn | Hầu hết các cửa hàng bán lẻ, nhà hàng |

**Không thể trộn lẫn chiều rộng**: Tất cả các máy POS sử dụng cùng một mẫu phải có cùng chiều rộng giấy in. Nếu bạn có các loại máy in khác nhau, hãy tạo các mẫu riêng biệt cho từng chiều rộng.

**Giới hạn kích thước logo**:
- **58mm**: Chiều rộng tối đa 384 pixel (khuyến nghị: 350px)
- **80mm**: Chiều rộng tối đa 576 pixel (khuyến nghị: 550px)

Các logo vượt quá chiều rộng tối đa sẽ được thu nhỏ tự động, điều này có thể làm giảm chất lượng.

## Cấu hình Logo

Logo phiếu thu phải là **đơn sắc** (chỉ đen và trắng) để tương thích với máy in nhiệt:

**Yêu cầu về logo**:
- Định dạng tệp: PNG, JPG hoặc WebP
- Chế độ màu: Đơn sắc (đen trên nền trắng)
- Kích thước khuyến nghị:
  - Giấy 58mm: 350px chiều rộng × 100-150px chiều cao
  - Giấy 80mm: 550px chiều rộng × 150-200px chiều cao
- Kích thước tệp: <100KB (máy in nhiệt có bộ nhớ hạn chế)

**Tạo logo đơn sắc**:
1. Bắt đầu với logo thường của bạn (màu sắc hoặc xám)
2. Sử dụng trình chỉnh sửa hình ảnh để chuyển đổi thành đen và trắng thuần túy (không xám)
3. Tăng độ tương phản để đảm bảo các phần đen là rắn chắc
4. Xuất file dưới dạng PNG với nền trong suốt hoặc trắng

**Vị trí logo**:
- Luôn được căn giữa theo chiều ngang
- In ở đầu phiếu thu (trên văn bản tiêu đề)
- Có khoảng trống tự động sau đó (tránh chen chúc với nội dung)

**Chọn logo**:
- Nhấp vào **Tìm kiếm Thư viện Truyền thông** trong biểu mẫu mẫu
- Chọn tài sản logo đơn sắc
- Xem trước hiển thị cách logo sẽ xuất hiện trên phiếu thu

**Không có logo**: Để trống trường logo nếu bạn muốn thương hiệu chỉ bằng văn bản (văn bản tiêu đề có thể bao gồm tên cửa hàng).

## Văn bản Tiêu đề

Văn bản tiêu đề xuất hiện ngay sau logo (hoặc ở đầu nếu không có logo). Nội dung điển hình:

**Tên cửa hàng và địa chỉ**:
```
Your Store Name
123 Main Street
City, State 12345
Phone: (555) 123-4567
```

**Giờ làm việc**:
```
Monday-Friday: 9am-9pm
Saturday-Sunday: 10am-6pm
```

**Dòng slogan**:
```
Quality Products, Exceptional Service
```

**Định dạng**:
- Sử dụng ký tự xuống dòng để phân tách thông tin
- Được căn giữa tự động
- Giữ các dòng dưới giới hạn ký tự cho chiều rộng giấy (32 ký tự cho 58mm, 48 cho 80mm)

**Biến số có sẵn** (tùy chọn):
- `{store_name}` - Được thay thế bằng tên kho
- `{order_date}` - Được thay thế bằng ngày giao dịch
- `{order_number}` - Được thay thế bằng mã đơn hàng

Hầu hết các nhà bán hàng sử dụng văn bản tĩnh thay vì biến số để duy trì tính nhất quán của tiêu đề.

## Văn bản Chân trang

Văn bản chân trang xuất hiện sau các chi tiết giao dịch (sản phẩm, tổng số, phương thức thanh toán). Nội dung điển hình:

**Chính sách hoàn tiền**:
```
Returns within 30 days with receipt
Store credit or exchange only
```

**Thông điệp cảm ơn**:
```
Thank you for shopping with us!
Follow us @yourstore
```

**Dịch vụ khách hàng**:
```
Questions? Call (555) 123-4567
or email support@yourstore.com
```

**Lời khuyên định dạng**:
- Giữ thông tin quan trọng nhất ở đầu (chính sách hoàn tiền, liên hệ)
- Sử dụng ký tự xuống dòng để dễ đọc
- Xem xét thêm dòng phân cách (`---`) giữa các phần

## Các trường Tuân thủ

Nhiều khu vực pháp lý yêu cầu thông tin cụ thể trên phiếu thu:

**Nhãn số thuế** - nhãn tùy chỉnh cho số nhận dạng thuế:
- Hoa Kỳ: "Tax ID" hoặc "EIN"
- EU: "VAT Number" hoặc "VAT Reg No"
- Canada: "GST/HST Number"
- Úc: "ABN"

**Giá trị số thuế** - số nhận dạng thực tế:
- Được nhập một lần trong mẫu, xuất hiện trên tất cả các phiếu thu
- Ví dụ: "VAT Number: GB123456789"

**Nhãn đăng ký doanh nghiệp** - nhãn tùy chỉnh cho đăng ký doanh nghiệp:
- Pháp: "SIRET"
- Đức: "Handelsregister"
- Vương quốc Anh: "Company Registration Number"

**Giá trị đăng ký doanh nghiệp** - số đăng ký thực tế:
- Ví dụ: "SIRET: 123 456 789 00010"

**Hiển thị Powered by Spwig** - bật/tắt hiển thị thương hiệu "Powered by Spwig":
- Mặc định bật (hỗ trợ phát triển nền tảng)
- Tắt để vận hành theo kiểu trắng nhãn

**Ví dụ tuân thủ theo khu vực**:

**Liên minh châu Âu**:
- Nhãn số thuế: "VAT Number"
- Giá trị số thuế: "GB123456789"
- Hiển thị số đăng ký công ty nếu yêu cầu bởi quốc gia

**Hoa Kỳ**:
- Thường không có yêu cầu số thuế trên phiếu thu (thay đổi theo bang)
- Có thể bao gồm EIN cho các giao dịch B2B

**Pháp (Cụ thể)**:
- Số SIRET bắt buộc trên tất cả các phiếu thu
- Nhãn đăng ký doanh nghiệp: "SIRET"
- Giá trị đăng ký doanh nghiệp: "123 456 789 00010"

**Úc**:
- Khuyến khích sử dụng ABN (số doanh nghiệp Úc) cho các doanh nghiệp đăng ký GST
- Nhãn số thuế: "ABN"

Kiểm tra yêu cầu phiếu thu của khu vực pháp lý địa phương trước khi triển khai.

## Quảng bá qua Mã QR

Bao gồm mã QR ở cuối phiếu thu để tăng cường tương tác với khách hàng:

**URL mã QR** - địa chỉ khi quét:
- Yêu cầu đánh giá: `https://yourstore.com/reviews/leave-review`
- Chương trình khách hàng thân thiết: `https://yourstore.com/loyalty/join`
- Giảm giá cho lần mua tiếp theo: `https://yourstore.com/discount/THANKYOU`
- Mạng xã hội: `https://instagram.com/yourstore`
- Trang chủ website: `https://yourstore.com`

**Nhãn mã QR** - văn bản hiển thị trên mã QR:
- "Quét để để lại đánh giá và nhận 10% giảm giá cho lần mua tiếp theo"
- "Tham gia chương trình khách hàng thân thiết - Quét tại đây"
- "Theo dõi chúng tôi trên Instagram - Quét để kết nối"
- "Đánh giá trải nghiệm của bạn"

**Lời khuyên sử dụng mã QR**:
- Sử dụng URL ngắn (URL dài tạo mã QR dày đặc, khó quét)
- Kiểm tra mã QR với nhiều camera điện thoại trước khi triển khai
- Bao gồm giá trị rõ ràng trong nhãn (khách hàng nhận được gì khi quét)
- Theo dõi lượt quét mã QR để đo lường hiệu quả (sử dụng URL có tham số theo dõi)

**Mã QR động** (Nâng cao):
- Sử dụng dịch vụ chuyển hướng QR (bit.ly, tinyurl) để tạo URL ngắn
- Chuyển hướng đến các địa chỉ khác nhau theo mùa mà không cần in lại phiếu thu
- Ví dụ: `https://bit.ly/yourstoreqr` → chuyển hướng đến chương trình khuyến mãi hiện tại

## Tạo Mẫu cho Các Phạm vi Khác nhau

**Mẫu Mặc định** (điểm bắt đầu được khuyến nghị):
1. Di chuyển đến **POS > Mẫu Phiếu thu**
2. Nhấp **+ Thêm Mẫu Phiếu thu**
3. Để trống các trường **Kho** và **Nhóm Cửa hàng** (điều này làm cho nó trở thành mẫu mặc định)
4. Cấu hình chiều rộng giấy phù hợp với loại máy in phổ biến nhất của bạn
5. Thêm logo, tiêu đề, chân trang
6. Cấu hình các trường tuân thủ cho thị trường chính của bạn
7. Lưu lại

Mẫu này áp dụng cho tất cả các cửa hàng trừ khi bị ghi đè.

**Mẫu Nhóm** (cho các biến thể khu vực):
1. Tạo mẫu mới
2. Chọn **Nhóm Cửa hàng** (ví dụ: "European Stores")
3. Để trống trường **Kho**
4. Điều chỉnh các trường tuân thủ cho khu vực (ví dụ: định dạng VAT)
5. Điều chỉnh văn bản tiêu đề (ví dụ: địa chỉ khu vực)
6. Lưu lại

Mẫu này áp dụng cho tất cả các cửa hàng trong nhóm.

**Mẫu Cửa hàng** (cho nhu cầu cụ thể theo địa điểm):
1. Tạo mẫu mới
2. Chọn **Kho** (ví dụ: "Paris Store")
3. Điều chỉnh tất cả các trường cho địa điểm cụ thể này
4. Lưu lại

Mẫu này chỉ áp dụng cho cửa hàng này.

**Kiểm tra Mẫu**:
- Xử lý giao dịch kiểm tra trên máy POS
- In phiếu thu
- Kiểm tra độ rõ nét của logo, căn chỉnh văn bản, các trường tuân thủ, khả năng quét mã QR
- Điều chỉnh mẫu và kiểm tra lại nếu cần

## Bố cục Phiếu thu Thường gặp

**Phiếu thu tối giản** (xe bán hàng ăn nhẹ, sự kiện tạm thời):
- Không có logo (tiết kiệm không gian)
- Tiêu đề: Chỉ tên cửa hàng và số điện thoại
- Chân trang: Thông điệp cảm ơn
- Không có mã QR

**Phiếu thu bán lẻ tiêu chuẩn**:
- Logo (biểu tượng thương hiệu đơn sắc)
- Tiêu đề: Tên cửa hàng đầy đủ, địa chỉ, giờ làm việc
- Tuân thủ: Số thuế
- Chân trang: Chính sách hoàn tiền, thông điệp cảm ơn
- Mã QR: Yêu cầu đánh giá

**Phiếu thu bán lẻ cao cấp**:
- Logo (biểu tượng thương hiệu đầy đủ)
- Tiêu đề: Dòng slogan, địa chỉ, thông tin liên hệ
- Tuân thủ: Số thuế, số đăng ký doanh nghiệp
- Chân trang: Chính sách hoàn tiền, dịch vụ khách hàng, mạng xã hội
- Mã QR: Đăng ký chương trình khách hàng thân thiết

**Chuỗi cửa hàng đa địa điểm**:
- Mẫu mặc định: Thương hiệu doanh nghiệp, chính sách tiêu chuẩn
- Mẫu nhóm: Tuân thủ khu vực (VAT cho EU, GST cho Canada)
- Mẫu cửa hàng: Địa chỉ và số điện thoại theo địa điểm

## Quản lý Nhiều Mẫu

**Quy tắc đặt tên mẫu**:
- Sử dụng phạm vi trong tên: "Mẫu Mặc định", "Mẫu Nhóm EU", "Mẫu Cửa hàng Paris"
- Giúp xác định mẫu nào được áp dụng ở đâu khi xem danh sách

**Thay đổi mẫu**:
- Các thay đổi áp dụng ngay lập tức cho các phiếu thu trong tương lai
- Các phiếu thu trước đó (đã được in) không bị ảnh hưởng
- Kiểm tra thay đổi trên máy POS ít người dùng trước khi triển khai đến tất cả các cửa hàng

**Sao chép mẫu**:
- Khi tạo mẫu mới tương tự mẫu hiện có, sao chép mẫu hiện có và chỉnh sửa
- Tránh bắt đầu từ đầu

**Xóa mẫu**:
- Không thể xóa mẫu mặc định khi có máy POS đang hoạt động (phải có một mẫu dự phòng)
- Có thể xóa mẫu nhóm/cửa hàng (máy POS sẽ quay về cấp độ tiếp theo trong phân cấp)
- Xác nhận không có máy POS nào đang sử dụng mẫu trước khi xóa

## Một số Lời khuyên

- **Bắt đầu với 80mm nếu không chắc** - Chiều rộng giấy tiêu chuẩn phù hợp với hầu hết bán lẻ; 58mm là chuyên dụng
- **Kiểm tra logo trên máy in thực tế** - Điều gì trông đẹp trên màn hình có thể in kém; kiểm tra sớm
- **Giữ các trường tuân thủ được cập nhật** - Số đăng ký thuế đã hết hạn trên phiếu thu gây ra vấn đề pháp lý
- **Mã QR có giá trị quét tốt hơn** - "Quét để nhận 10% giảm giá" hiệu quả hơn "Quét tại đây" 10 lần
- **Kiểm tra giới hạn ký tự** - Việc bọc dòng làm hỏng định dạng; đếm ký tự mỗi dòng trước khi triển khai
- **Một mẫu cho mỗi chiều rộng giấy** - Đừng gán mẫu 80mm cho máy in 58mm (logo sẽ không vừa)
- **In phiếu thu kiểm tra hàng tháng** - Máy in suy giảm theo thời gian; xác nhận chất lượng vẫn chấp nhận được
- **Sử dụng biến số một cách tiết kiệm** - Văn bản tĩnh đáng tin cậy hơn các biến số động (ít điểm thất bại hơn)
- **Sao lưu cấu hình mẫu** - Chụp màn hình hoặc xuất cài đặt mẫu trước khi thực hiện thay đổi lớn (dễ dàng quay lại)
- **Tuân thủ khu vực thay đổi** - Nghiên cứu yêu cầu phiếu thu địa phương trước khi triển khai; phạt nặng nếu không tuân thủ

