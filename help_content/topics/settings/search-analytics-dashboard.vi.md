---
title: Bảng điều khiển Phân tích Tìm kiếm
---

Bảng điều khiển Phân tích Tìm kiếm theo dõi mọi truy vấn tìm kiếm trên cửa hàng của bạn, cung cấp thông tin về những gì khách hàng tìm kiếm, những truy vấn nào thành công hoặc thất bại, và tốc độ hệ thống tìm kiếm của bạn phản hồi như thế nào. Sử dụng dữ liệu này để xác định các sản phẩm phổ biến, phát hiện các mặt hàng thiếu hụt, tạo các từ đồng nghĩa, và tối ưu hiệu suất tìm kiếm.

Việc theo dõi phân tích phải được bật trong **Cài đặt Tìm kiếm > Tab Phân tích** để dữ liệu hiển thị.

![Bảng điều khiển Phân tích](/static/core/admin/img/help/search-analytics-dashboard/analytics-dashboard.webp)

## Tổng quan Bảng điều khiển

Truy cập vào **Tìm kiếm > Phân tích Tìm kiếm** để vào bảng điều khiển. Trang hiển thị:

**Thẻ Thống kê** - Chỉ số nhanh cho hôm nay và tuần trước:
- Tổng số lần tìm kiếm hôm nay
- Tổng số lần tìm kiếm trong tuần này
- Truy vấn không có kết quả (tìm kiếm trả về không sản phẩm nào)
- Thời gian phản hồi trung bình tính bằng miligiây

**Bảng Truy vấn Hàng Đầu** - Các từ tìm kiếm phổ biến nhất với số lượng kết quả

**Truy vấn Không có Kết quả** - Các tìm kiếm trả về không kết quả (rất quan trọng để cải thiện)

**Danh sách Truy vấn** - Tất cả các bản ghi tìm kiếm cá nhân với các bộ lọc

## Thống kê Hôm nay

**Tổng Số Lần Tìm Kiếm Hôm Nay** - Số lượng tất cả các yêu cầu tìm kiếm kể từ nửa đêm theo múi giờ cửa hàng của bạn. Bao gồm cả các yêu cầu tự động hoàn thành và trang tìm kiếm đầy đủ.

**Truy vấn Độc Lập Hôm Nay** - Số lượng các từ tìm kiếm khác nhau được sử dụng hôm nay. Nếu 5 khách hàng đều tìm kiếm "laptop", điều này được tính là 1 truy vấn độc lập dù có tổng cộng 5 lần tìm kiếm.

**Truy vấn Không Có Kết Quả Hôm Nay** - Các lần tìm kiếm hôm nay trả về không sản phẩm nào. Số lượng truy vấn không có kết quả cao cho thấy thiếu sản phẩm hoặc bao phủ từ đồng nghĩa kém.

Dữ liệu được cập nhật theo thời gian thực khi các lần tìm kiếm diễn ra.

## Thống kê Hàng Tuần

**Tổng Số Lần Tìm Kiếm Tuần** - Tổng số lần tìm kiếm trong 7 ngày qua

**Truy vấn Độc Lập** - Các từ tìm kiếm khác nhau được sử dụng trong tuần này

**Tăng trưởng So Với Tuần Trước** - Phần trăm thay đổi so với tuần trước (nếu được hiển thị)

Sử dụng dữ liệu hàng tuần để phát hiện xu hướng: sự gia tăng lượng tìm kiếm thường liên quan đến sự tăng trưởng lưu lượng truy cập hoặc chiến dịch tiếp thị.

## Thời Gian Phản Hồi Trung Bình

⚠️ **GIÁM SÁT HIỆN THỜI**

Thời gian trung bình (tính bằng miligiây) để thực thi các truy vấn tìm kiếm. Thời gian phản hồi mục tiêu:

| Loại Truy vấn | Mục Tiêu | Ngưỡng Cảnh Báo |
|----------------|----------|------------------|
| Tự động hoàn thành | < 200ms | > 300ms liên tục |
| Tìm kiếm đầy đủ | < 500ms | > 800ms liên tục |

Nếu thời gian phản hồi trung bình vượt quá ngưỡng cảnh báo:
1. Kiểm tra **Cài đặt Tìm kiếm > Tab Lưu trữ** - tăng TTL lưu trữ
2. Xem xét **Tab Chỉ Số Sâu** - tắt các tính năng tốn kém (chỉ số tài liệu, chỉ số đánh giá trên các danh mục lớn)
3. Xem hướng dẫn [Tối ưu Hiệu suất Tìm kiếm](/en/admin/help/search-performance-optimization/)

## Truy vấn Hàng Đầu

Bảng Truy vấn Hàng Đầu hiển thị các từ tìm kiếm phổ biến nhất:

**Sử dụng Dữ Liệu Này Để**:
- **Đưa sản phẩm phổ biến lên đầu** - Nếu "tai nghe không dây" là truy vấn hàng đầu, hãy đưa những sản phẩm này nổi bật trên trang chủ của bạn
- **Quyết định hàng tồn kho** - Lượng tìm kiếm cao cho một danh mục cho thấy nhu cầu
- **Phát hiện xu hướng** - Các tìm kiếm theo mùa tiết lộ những thứ đang phổ biến hiện tại
- **Tạo nội dung** - Viết bài đăng blog hoặc hướng dẫn về các chủ đề được tìm kiếm thường xuyên

Xem xét lại các truy vấn hàng đầu hàng tháng để đồng bộ hóa việc kinh doanh của bạn với sở thích của khách hàng.

## Truy vấn Không Có Kết Quả

**RẤT QUAN TRỌNG CHO VIỆC CẢI TIẾN** - Các truy vấn không có kết quả là kho báu để tối ưu cửa hàng của bạn.

Các truy vấn không có kết quả xảy ra vì ba lý do chính:

### 1. Thiếu Sản Phẩm

Khách hàng tìm kiếm các sản phẩm bạn không bán.

**Ví dụ**: Nhiều lần tìm kiếm "mat yoga" nhưng bạn chỉ bán thiết bị thể thao, không phải dụng cụ yoga.

**Hành động**: Nếu các lần tìm kiếm thường xuyên, hãy cân nhắc thêm các sản phẩm này vào danh mục của bạn.

### 2. Thiếu Từ Đồng Nghĩa

Khách hàng sử dụng các từ không khớp với mô tả sản phẩm của bạn.

**Ví dụ**: Khách hàng tìm kiếm "laptop" nhưng tất cả sản phẩm của bạn đều ghi là "máy tính xách tay".

**Hành động**: Tạo bản đồ từ đồng nghĩa, ánh xạ các từ khách hàng sử dụng đến ngôn ngữ sản phẩm của bạn. Xem [Quản lý Từ Đồng Nghĩa và Chuyển hướng](/en/admin/help/managing-synonyms-redirects/).

### 3. Chỉ Số Mờ Đục Kém

Những lỗi chính tả hoặc sai chính tả không khớp ngay cả khi đã bật tìm kiếm mờ.

**Ví dụ**: Tìm kiếm "accomodate" không tìm thấy sản phẩm "accommodate".

**Hành động**:
- Giảm ngưỡng độ tương tự trong **Cài đặt Tìm kiếm > Tab Tìm kiếm Mờ** (từ 0.80 xuống 0.75)
- Thêm các từ đồng nghĩa một chiều cho các lỗi chính tả phổ biến

**Quy Trình Hàng Tuần**:
1. Xem xét các truy vấn không có kết quả mỗi thứ Hai
2. Phân loại: Thiếu sản phẩm, thiếu từ đồng nghĩa, hoặc lỗi chính tả
3. Thêm từ đồng nghĩa cho các truy vấn được tìm kiếm thường xuyên
4. Ghi chú các khoảng trống sản phẩm để lập kế hoạch hàng tồn kho

## Chi Tiết Truy Vấn

Nhấp vào bất kỳ truy vấn nào trong danh sách để xem chi tiết đầy đủ:

**Các Trường Được Theo Dõi**:
- **Văn bản truy vấn** - Điều khách hàng đã tìm kiếm
- **Thời gian dấu thời gian** - Khi nào tìm kiếm xảy ra
- **Số lượng kết quả** - Số lượng kết quả được trả về
- **Thời gian phản hồi** - Miligiây để thực thi (giám sát hiệu suất)
- **Người dùng** - Khách hàng đã đăng nhập (nếu theo dõi người dùng được bật)
- **ID phiên** - Nhận dạng phiên ẩn danh
- **Ngôn ngữ** - Ngôn ngữ cửa hàng trong lúc tìm kiếm
- **Động cơ** - Động cơ tìm kiếm nào đã xử lý truy vấn

## Lọc và Tìm Kiếm

Sử dụng bộ lọc để phân tích các phân khúc cụ thể:

**Cấp bậc Ngày** - Lọc theo ngày, tháng hoặc năm

**Bộ Lọc Ngôn Ngữ** - Xem các tìm kiếm theo ngôn ngữ (rất hữu ích cho các cửa hàng đa ngôn ngữ)

**Bộ Lọc Động Cơ** - So sánh hành vi tìm kiếm giữa các động cơ khác nhau

**Bộ Chuyển Đổi Không Kết Quả** - Chỉ hiển thị các truy vấn trả về không kết quả

**Hộp Tìm Kiếm** - Tìm kiếm văn bản truy vấn cụ thể

## Xuất Dữ Liệu

Nhấp vào **Xuất** để tải xuống dữ liệu truy vấn dưới dạng CSV để phân tích sâu hơn trong Excel hoặc các công cụ dữ liệu.

**CSV bao gồm**:
- Tất cả văn bản truy vấn
- Thời gian dấu thời gian
- Số lượng kết quả
- Thời gian phản hồi
- Dữ liệu ngôn ngữ và động cơ

Sử dụng các bản xuất để:
- Phân tích xu hướng theo thời gian
- Nhận biết các mẫu tìm kiếm theo mùa
- Kiểm toán hiệu suất
- Trình bày cho các bên liên quan

## Xét Đến Quyền Riêng Tư

Theo dõi phân tích tìm kiếm tôn trọng quyền riêng tư:

**Theo dõi Người Dùng** (tùy chọn) - Liên kết các truy vấn với tài khoản khách hàng đã đăng nhập. Vô hiệu hóa để tuân thủ GDPR/CCPA trong **Cài đặt Tìm kiếm > Tab Phân tích**.

**Theo dõi Phiên** (mặc định) - Sử dụng ID phiên ẩn danh để theo dõi các mẫu tìm kiếm mà không xác định khách hàng. Tôn trọng quyền riêng tư.

**Giữ Lại Dữ Liệu** - Các truy vấn tìm kiếm sẽ tồn tại trong cơ sở dữ liệu vĩnh viễn. Thực hiện chính sách giữ lại tùy chỉnh nếu cần thiết để tuân thủ.

## Sử Dụng Phân Tích Để Cải Thiện Tìm Kiếm

Những hiểu biết có thể áp dụng từ phân tích tìm kiếm:

**Công Việc Hàng Tuần**:
- Xem xét các truy vấn không có kết quả và thêm từ đồng nghĩa cho các từ phổ biến
- Theo dõi thời gian phản hồi và tối ưu nếu chậm liên tục
- Nhận biết các truy vấn hàng đầu và đảm bảo các sản phẩm đó được cung cấp đầy đủ

**Công Việc Hàng Tháng**:
- Phân tích các truy vấn hàng đầu để hướng dẫn lựa chọn sản phẩm
- Xuất dữ liệu để nhận biết xu hướng theo mùa
- Xem xét các mẫu tìm kiếm theo ngôn ngữ cụ thể
- Theo dõi số lần chuyển hướng để tối ưu các đường tắt điều hướng

**Công Việc Hàng Quý**:
- Kiểm tra hiệu quả từ đồng nghĩa (liệu số truy vấn không có kết quả đã giảm chưa?)
- So sánh sự tăng trưởng lượng tìm kiếm với lưu lượng truy cập tổng thể
- Thử nghiệm A/B thay đổi trọng số và đo lường tính liên quan của kết quả
- Xem xét liệu có nên thêm các danh mục sản phẩm mới dựa trên nhu cầu tìm kiếm

## Mẹo

- **Các truy vấn không có kết quả là kho báu để cải thiện** - Chúng trực tiếp cho bạn biết những gì khách hàng muốn mà bạn chưa cung cấp
- **Xem xét phân tích vào những ngày thứ Hai đầu tuần** - Bắt đầu tuần của bạn bằng cách tối ưu hóa dựa trên dữ liệu tuần trước
- **Thời gian phản hồi >300ms liên tục = điều tra** - Kiểm tra cài đặt lưu trữ trước, sau đó là các tính năng chỉ số sâu
- **Xuất CSV để phân tích xu hướng** - Phân tích bảng tính tiết lộ các mẫu không rõ ràng trong giao diện quản trị
- **Tạo từ đồng nghĩa trước khi thêm sản phẩm** - Nếu khách hàng tìm kiếm "bìa máy tính bảng" nhưng bạn gọi chúng là "bìa bảo vệ", hãy thêm từ đồng nghĩa trước
- **Theo dõi các mẫu tìm kiếm theo mùa** - "Giày mùa đông" vào tháng 10, "bộ đồ bơi" vào tháng 3 - điều chỉnh hàng tồn kho tương ứng

