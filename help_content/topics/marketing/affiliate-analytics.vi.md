---
title: Phân tích & Báo cáo Đối tác
---

Phân tích đối tác giúp bạn theo dõi hiệu suất của chương trình đối tác và xác định các đối tác có hiệu suất cao nhất. Hướng dẫn này sẽ chỉ cho bạn cách sử dụng bảng điều khiển người bán, diễn giải các thống kê, phân tích xu hướng doanh thu và đưa ra các quyết định dựa trên dữ liệu để tối ưu hóa chương trình đối tác của bạn.

## Bảng điều khiển Người bán

Truy cập **Chương trình Đối tác > Bảng điều khiển** để xem tổng quan phân tích đối tác toàn diện.

Bảng điều khiển người bán cung cấp cái nhìn thời gian thực về hiệu suất toàn bộ chương trình đối tác của bạn, bao gồm các chương trình đang hoạt động, số lượng đối tác, hoạt động hoa hồng và xu hướng doanh thu. Đây là trung tâm của bạn để giám sát sức khỏe chương trình và đưa ra các quyết định chiến lược.

![Bảng điều khiển Người bán](/static/core/admin/img/help/affiliate-analytics/merchant-dashboard.webp)

## Thống kê Bảng điều khiển

Bảng điều khiển hiển thị các chỉ số hiệu suất chính ở định dạng thẻ tại đầu trang.

### Thống kê Tổng quan

| Thống kê | Mô tả | Giá trị mẫu |
|-----------|-------------|---------------|
| **Tổng số chương trình** | Tổng số chương trình được tạo (số lượng đang hoạt động được hiển thị trong ngoặc đơn) | 3 chương trình (2 đang hoạt động) |
| **Đối tác đang hoạt động** | Các đối tác đã được phê duyệt hiện đang quảng bá sản phẩm của bạn | 47 đối tác |
| **Ứng dụng đang chờ xử lý** | Các ứng dụng đối tác mới đang chờ bạn xem xét | 8 đang chờ xử lý |
| **Tổng số lượt nhấp** | Tổng số lượt nhấp trên tất cả các liên kết theo dõi đối tác | 12.543 lượt nhấp |
| **Tổng số hoa hồng** | Số lượng hồ sơ hoa hồng từng được tạo | 287 hoa hồng |
| **Số tiền đang chờ** | Tổng giá trị các khoản hoa hồng đã được phê duyệt nhưng đang chờ thanh toán | $4.235,50 |

Những thống kê này cho bạn cái nhìn tổng quan về quy mô chương trình và nghĩa vụ tài chính.

### Hiểu Về Các Chỉ Số

- **Số lượng đang hoạt động** — Hiển thị số lượng chương trình hiện đang chấp nhận ứng dụng và tạo ra hoa hồng
- **Ứng dụng đang chờ xử lý** — Chỉ ra khối lượng công việc xem xét của bạn (số lượng cao cho thấy bạn nên xem xét ứng dụng thường xuyên hơn)
- **Tổng số lượt nhấp** — Đo lường mức độ tham gia tổng thể của đối tác và hoạt động quảng bá
- **Số tiền đang chờ** — Đại diện cho nghĩa vụ thanh toán hiện tại của bạn cho các đối tác

## Biểu đồ Doanh thu

Bảng điều khiển bao gồm biểu đồ doanh thu 30 ngày được cung cấp bởi Chart.js, hiển thị xu hướng hoa hồng theo thời gian.

### Tính Năng Biểu đồ

- **Khoảng thời gian** — Hiển thị hoạt động hoa hồng trong 30 ngày gần nhất
- **Phân tích hàng ngày** — Mỗi thanh đại diện cho các khoản hoa hồng được tạo vào ngày đó
- **Chi tiết khi di chuột** — Di chuột lên bất kỳ thanh nào để xem ngày cụ thể và tổng hoa hồng
- **Phân tích xu hướng** — Nhận biết nhanh các mô hình tăng trưởng, xu hướng theo mùa và các bất thường

### Đọc Biểu đồ

**Phân tích mẫu:"

```
Ngày 1-7:   $150-$200/ngày  → Hiệu suất cơ bản
Ngày 8-14:  $300-$450/ngày  → Tăng đột biến do chiến dịch (nghiên cứu xem điều gì đã hiệu quả)
Ngày 15-21: $100-$150/ngày  → Suy giảm sau chiến dịch (dự kiến)
Ngày 22-30: $200-$250/ngày  → Trở lại hiệu suất cơ bản
```

Sử dụng biểu đồ này để:

- **Xác định chiến dịch thành công** — Các đợt tăng đột biến cho thấy các chiến dịch quảng bá hiệu quả
- **Nhận biết xu hướng theo mùa** — Lên kế hoạch hàng tồn kho và tiếp cận đối tác xung quanh các thời điểm có lượng truy cập cao
- **Phát hiện vấn đề** — Sự giảm đột ngột có thể chỉ ra các liên kết theo dõi bị hỏng hoặc vấn đề chương trình
- **Xác minh các thay đổi** — So sánh doanh thu trước và sau khi điều chỉnh tỷ lệ hoa hồng

## Đối tác Có Hiệu suất Cao Nhất

Bảng điều khiển bao gồm bảng hiển thị 10 đối tác có doanh thu cao nhất.

### Chỉ số Hiệu suất Đối tác

| Cột | Mô tả | Ví dụ |
|--------|-------------|---------|
| **Đối tác** | Tên và mã duy nhất của đối tác | Sarah Johnson (AFF-12345) |
| **Tổng doanh thu** | Doanh thu bán hàng liên quan đến đối tác này | $18.450,00 |
| **Đơn hàng** | Số lượng đơn hàng thành công được giới thiệu | 87 đơn hàng |
| **Số lượng hoa hồng** | Số lượng hồ sơ hoa hồng được tạo | 87 hoa hồng |
| **Tổng số tiền thanh toán** | Số tiền đã thanh toán cho đối tác này đến nay | $2.767,50 |

Bảng này được **sắp xếp theo tổng doanh thu** (từ cao đến thấp) để giúp bạn nhanh chóng xác định các đối tác có giá trị nhất.

### Sử dụng Dữ liệu Đối tác Hiệu suất Cao

**Xác định Đối tác VIP:"

Xem xét các đối tác hiệu suất cao và cân nhắc:

- **Tỷ lệ ưu đãi** — Cung cấp tỷ lệ hoa hồng cao hơn cho 3 đối tác hàng đầu của bạn (ví dụ: tăng từ 10% lên 12%)
- **Thông báo sớm** — Cho các đối tác hàng đầu biết sớm về sản phẩm mới hoặc chương trình khuyến mãi
- **Tạo nội dung tùy chỉnh** — Cung cấp banner cá nhân hóa hoặc hình ảnh sản phẩm
- **Hỗ trợ trực tiếp** — Giao cho đối tác hàng đầu một người liên hệ trực tiếp

**Ví dụ:"

```
Đối tác: Emily Chen (AFF-00123)
Doanh thu:   $24.500
Đơn hàng:    142
Thanh toán:   $2.450 (10% hoa hồng)

Hành động: Cung cấp mức hoa hồng 12% + quyền truy cập sản phẩm sớm
Tác động dự kiến: Tăng 20-30% doanh thu từ đối tác này
```

## Hoạt động Gần Đây

Bảng điều khiển hiển thị hoạt động đối tác gần đây để giúp bạn theo dõi các hành động đang chờ xử lý.

### Ứng dụng Mới

Hiển thị 5 ứng dụng đối tác gần đây nhất đang chờ xử lý với:

- Tên đối tác
- Ngày nộp đơn
- Chương trình nộp đơn
- Liên kết **Xem xét nhanh** để phê duyệt hoặc từ chối

Phần này giúp bạn ưu tiên xem xét đối tác mới và tránh tình trạng xếp hàng ứng dụng.

### Hoa hồng Mới

Hiển thị 10 khoản hoa hồng mới nhất được tạo (trạng thái đang chờ) với:

- Số đơn hàng (nhấp để xem chi tiết đơn hàng)
- Tên đối tác
- Số tiền hoa hồng
- Ngày tạo
- Hành động **Phê duyệt** hoặc **Từ chối** nhanh

Xem xét phần này hàng ngày để đảm bảo các khoản hoa hồng di chuyển qua ống dẫn phê duyệt.

## Thống kê Theo Chương Trình

Truy cập trang chi tiết của chương trình cụ thể để xem phân tích theo chương trình.

### Truy cập Thống kê Chương Trình

1. Truy cập **Chương trình Đối tác > Chương trình**
2. Nhấp vào tên chương trình bạn muốn phân tích
3. Xem bảng thống kê trên trang chi tiết chương trình

### Chỉ số Theo Chương Trình

| Chỉ số | Mô tả | Ý nghĩa |
|--------|-------------|---------------|
| **Đối tác đang hoạt động** | Các đối tác đã được phê duyệt trong chương trình này | 23 đối tác |
| **Tổng số lượt nhấp** | Số lượt nhấp trên các liên kết theo dõi của chương trình này | 5.432 lượt nhấp |
| **Tổng số hoa hồng** | Số hồ sơ hoa hồng được tạo cho chương trình này | 127 hoa hồng |
| **Hoa hồng đang chờ** | Giá trị hoa hồng chưa thanh toán cho chương trình này | $1.245,00 |

### Đối tác Mới Của Chương Trình

Trang chi tiết chương trình hiển thị 10 đối tác mới nhất đã tham gia chương trình này, bao gồm:

- Tên và mã đối tác
- Ngày tham gia
- Trạng thái ứng dụng

Sử dụng để theo dõi sự phát triển của chương trình và xác định chương trình nào thu hút nhiều sự quan tâm nhất.

## Hiệu suất Đối tác Theo Chương Trình

Xem các thống kê theo đối tác trong chương trình cụ thể.

### Xem Đối tác Theo Chương Trình

1. Truy cập **Chương trình Đối tác > Chương trình**
2. Nhấp vào tên chương trình
3. Cuộn xuống phần **Đối tác**
4. Nhấp **Xem tất cả đối tác** để xem danh sách đầy đủ

Danh sách đối tác được **sắp xếp theo tổng số hoa hồng** để làm nổi bật các đối tác hiệu suất cao trong mỗi chương trình.

### Phân tích So Sánh

**Ví dụ: So sánh hai chương trình"

**Chương trình Người ảnh hưởng (10% hoa hồng):"
- 47 đối tác đang hoạt động
- 8.234 lượt nhấp
- 187 hoa hồng
- Giá trị hoa hồng trung bình: $32,50

**Chương trình Giới thiệu theo khối (hoàn trả cố định $25):"
- 23 đối tác đang hoạt động
- 3.421 lượt nhấp
- 94 hoa hồng
- Giá trị hoa hồng trung bình: $25,00

**Nhận định: Chương trình Người ảnh hưởng có mức độ tương tác và giá trị hoa hồng cao hơn, cho thấy các khoản hoa hồng theo tỷ lệ phần trăm hoạt động tốt hơn cho cửa hàng này.

## Báo cáo Hoa Hồng

Chức năng quản lý hoa hồng cung cấp khả năng lọc và xuất dữ liệu chi tiết cho báo cáo.

### Truy cập Báo cáo Hoa Hồng

Truy cập **Marketing > Hoa hồng** để xem danh sách đầy đủ các khoản hoa hồng với các bộ lọc.

### Lọc Nâng Cao

Sử dụng thanh bên lọc để tạo báo cáo tùy chỉnh:

- **Theo khoảng thời gian** — Chọn các khoản hoa hồng được tạo giữa các ngày cụ thể (ví dụ: tháng 1 ngày 1-31 cho báo cáo hàng tháng)
- **Theo đối tác** — Xem tất cả các khoản hoa hồng cho một đối tác duy nhất
- **Theo chương trình** — Xem các khoản hoa hồng từ chương trình cụ thể
- **Theo trạng thái** — Lọc để chỉ hiển thị các khoản hoa hồng đang chờ, đã phê duyệt, đã từ chối hoặc đã thanh toán

### Khả năng Xuất Dữ Liệu

Giao diện quản trị Spwig bao gồm khả năng xuất dữ liệu tích hợp:

1. Áp dụng bộ lọc để thu hẹp danh sách các khoản hoa hồng
2. Chọn các khoản hoa hồng bạn muốn xuất (hoặc sử dụng "Chọn tất cả")
3. Chọn **Xuất các khoản đã chọn** từ **Hành động** dropdown
4. Chọn định dạng (CSV, Excel)
5. Tải xuống báo cáo để phân tích ngoại tuyến

**Báo cáo thường gặp:"

- **Tóm tắt hoa hồng hàng tháng** — Lọc theo khoảng thời gian, xuất tất cả các khoản đã phê duyệt
- **Hiệu suất đối tác** — Lọc theo đối tác, xuất tất cả các khoản hoa hồng để tính toán ROI
- **So sánh chương trình** — Xuất các khoản hoa hồng cho mỗi chương trình riêng biệt, so sánh trong bảng tính

## Báo cáo Thanh toán

Chức năng quản lý thanh toán cung cấp công cụ theo dõi tài chính và đối chiếu.

### Truy cập Báo cáo Thanh toán

Truy cập **Chương trình Đối tác > Thanh toán** để xem lịch sử thanh toán và thống kê.

### Thống kê Thanh toán

Bảng điều khiển thanh toán hiển thị:

| Trạng thái | Mô tả |
|--------|-------------|
| **Đang chờ** | Các khoản thanh toán đã được tạo nhưng chưa được xử lý |
| **Đang xử lý** | Các khoản thanh toán đã được gửi đến nhà cung cấp thanh toán (PayPal/Airwallex) |
| **Đã hoàn thành** | Đã thanh toán thành công cho các đối tác |
| **Thất bại** | Lỗi xử lý thanh toán |

### Phân tích Tài khoản Nhà cung cấp

Xem các khoản thanh toán được tổ chức theo nhà cung cấp thanh toán:

- **PayPal** — Các khoản thanh toán được xử lý qua PayPal (hiển thị tổng số lượng và số tiền)
- **Airwallex** — Các khoản thanh toán được xử lý qua chuyển khoản ngân hàng (hiển thị tổng số lượng và số tiền)

Phân tích này giúp bạn:

- Theo dõi chi phí nhà cung cấp (so sánh phí PayPal với phí Airwallex)
- Cân bằng phương thức thanh toán (khuyến khích các đối tác sử dụng phương thức có chi phí thấp hơn)
- Nhận biết các vấn đề xử lý (tỷ lệ thất bại cao trên một nhà cung cấp)

### Dữ liệu Thanh toán Lịch sử

Lọc và xuất lịch sử thanh toán cho:

- **Báo cáo quý** — Tính toán chi phí chương trình đối tác theo quý
- **Tài liệu thuế** — Xuất dữ liệu thanh toán hàng năm cho các biểu mẫu 1099 (Mỹ) hoặc tương đương
- **Truy vấn của đối tác** — Nhanh chóng tra cứu ngày và số tiền thanh toán khi đối tác có câu hỏi

## Sử dụng Phân tích để Tối ưu hóa

Sử dụng dữ liệu phân tích của bạn để liên tục cải thiện hiệu suất chương trình.

### Xác định Đối tác Hiệu suất Cao

**Hành động:** Xem bảng đối tác hiệu suất cao hàng tháng và:

- **Tưởng thưởng cho sự xuất sắc** — Tăng tỷ lệ hoa hồng cho 10% đối tác hàng đầu
- **Hiểu các chiến lược** — Liên hệ để hỏi xem phương pháp quảng bá nào hiệu quả nhất
- **Lặp lại thành công** — Chia sẻ chiến lược của đối tác hiệu suất cao với các đối tác khác (với sự cho phép)

**Ví dụ:"

```
Đối tác hàng đầu: Marcus Lee (AFF-00456)
Doanh thu:       $31.200 trong 3 tháng
Phương pháp:        Đánh giá sản phẩm trên YouTube

Hành động:
1. Tăng hoa hồng từ 10% lên 12%
2. Yêu cầu Marcus tạo một trường hợp nghiên cứu về đối tác
3. Tuyển dụng thêm nhiều người ảnh hưởng YouTube hơn bằng câu chuyện thành công của Marcus
```

### Hỗ trợ Đối tác Hiệu suất Thấp

**Hành động:** Lọc đối tác theo số lượng hoa hồng và xác định những đối tác có < 5 hoa hồng trong 90 ngày:

- **Cung cấp tài nguyên** — Gửi tài liệu quảng bá, hình ảnh sản phẩm, nội dung mẫu
- **Cung cấp đào tạo** — Tạo một buổi webcast hướng dẫn các chiến lược quảng bá hiệu quả
- **Điều chỉnh vị trí** — Nếu đối tượng người dùng của đối tác không phù hợp với chương trình, đề xuất chuyển sang chương trình khác
- **Loại bỏ đối tác không hoạt động** — Sau 6-12 tháng không có hoạt động, cân nhắc loại bỏ họ khỏi chương trình

### So sánh Chương trình

**Hành động:** So sánh tổng số hoa hồng và tỷ lệ chuyển đổi từ lượt nhấp theo chương trình:

| Chương trình | Lượt nhấp | Hoa hồng | Tỷ lệ chuyển đổi | Hoa hồng trung bình |
|---------|--------|-------------|-----------------|----------------|
| Chương trình A | 8.234 | 187 | 2,27% | $32,50 |
| Chương trình B | 3.421 | 94 | 2,75% | $25,00 |

**Nhận định:"

- Chương trình B có **tỷ lệ chuyển đổi cao hơn** mặc dù có ít lượt nhấp hơn (định vị tốt hơn)
- Chương trình A tạo ra **giá trị hoa hồng cao hơn** (tốt hơn cho doanh thu)

**Tối ưu hóa:"

- Tăng tỷ lệ hoa hồng cho Chương trình B để thu hút thêm nhiều đối tác (chuyển đổi đã được chứng minh)
- Phân tích điều gì khiến Chương trình B chuyển đổi tốt hơn và áp dụng các học hỏi đó cho Chương trình A

### Xu hướng Theo Mùa

**Hành động:** Sử dụng biểu đồ doanh thu để xác định xu hướng theo mùa:

```
Tháng 1:  $5.200   → Suy giảm sau kỳ nghỉ lễ
Tháng 2:  $4.800   → Tiếp tục mùa thấp
Tháng 3:    $6.100   → Tăng trưởng mùa xuân
Tháng 4:    $7.300   → Tiếp tục tăng trưởng
Tháng 5:      $6.800   → Ổn định
```

**Lên kế hoạch chiến dịch:"

- **Giảm tốc độ quý 1** — Khởi động chiến dịch "Bán hàng Mùa xuân" vào tháng 2 để tăng doanh thu tháng 3/4
- **Chuẩn bị cho kỳ nghỉ lễ** — Tuyển dụng thêm đối tác vào tháng 9/10 cho các chương trình bán hàng dịp lễ cuối năm
- **Lên kế hoạch hàng tồn kho** — Tăng cường hàng tồn kho trước các đợt tăng doanh thu do đối tác thúc đẩy

## Mẹo

- Kiểm tra **bảng điều khiển người bán hàng ngày** để bắt kịp các ứng dụng và hoa hồng đang chờ xử lý trước khi chúng tích tụ — việc kiểm tra 5 phút mỗi ngày hiệu quả hơn việc dành 2 giờ mỗi tuần để xử lý
- Sử dụng **biểu đồ doanh thu để xác minh các thay đổi chương trình** — nếu bạn điều chỉnh tỷ lệ hoa hồng, hãy so sánh 30 ngày trước và sau để đo lường tác động
- Xuất dữ liệu hoa hồng **tháng** và lưu trữ báo cáo trong hệ thống kế toán của bạn để dễ dàng chuẩn bị thuế và dự báo tài chính
- Liên hệ với **3 đối tác hàng đầu mỗi quý** để duy trì mối quan hệ và thu thập phản hồi về cải tiến chương trình
- Theo dõi **các đợt tăng đột biến trong biểu đồ doanh thu** và điều tra xem điều gì gây ra — các chiến dịch thành công có thể được lặp lại với các đối tác khác hoặc trong các mùa sau
- Thiết lập **lịch kiểm tra hàng tháng**: Tuần 1 = kiểm tra phân tích, Tuần 2 = liên hệ với các đối tác hiệu suất cao, Tuần 3 = hỗ trợ các đối tác hiệu suất thấp, Tuần 4 = lên kế hoạch chiến dịch cho tháng tới
- So sánh **số lượt nhấp với số lượng hoa hồng** cho từng đối tác để xác định chất lượng chuyển đổi — một đối tác có 5.000 lượt nhấp nhưng chỉ có 10 hoa hồng có thể đang tạo ra lưu lượng truy cập chất lượng thấp