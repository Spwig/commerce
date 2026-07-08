---
title: Giỏ hàng bị bỏ lại
---

Giỏ hàng bị bỏ lại được tạo ra khi một khách hàng đã đăng nhập thêm các mặt hàng vào giỏ hàng nhưng không hoàn tất thanh toán trong vòng 24 giờ. Spwig tự động theo dõi các giỏ hàng này để bạn có thể hiểu rõ doanh thu bị mất, xác định các mô hình tại sao khách hàng rời đi và thực hiện hành động để thu hồi doanh số.

Truy cập **Khách hàng > Giỏ hàng bị bỏ lại** để xem tất cả các trường hợp bỏ lại đã được ghi lại.

## Những thứ bạn có thể thấy trong danh sách giỏ hàng bị bỏ lại

Danh sách hiển thị mỗi giỏ hàng bị bỏ lại với thông tin sau đây:

| Cột | Mô tả |
|---|---|
| **Khách hàng** | Tên và địa chỉ email của khách hàng |
| **Bỏ lại lúc** | Ngày và giờ giỏ hàng được đánh dấu là bị bỏ lại |
| **Giá trị tổng cộng** | Giá trị tiền của các mặt hàng trong giỏ hàng tại thời điểm bị bỏ lại |
| **Tổng số mặt hàng** | Số lượng mặt hàng trong giỏ hàng |
| **Lý do ước tính** | Dự đoán tốt nhất của Spwig về lý do giỏ hàng bị bỏ lại |
| **Trạng thái thu hồi** | Giỏ hàng này đã được thu hồi (biến thành đơn hàng hoàn tất) hay chưa |
| **Số ngày kể từ khi bỏ lại** | Thời gian đã trôi qua kể từ khi giỏ hàng bị bỏ lại |

### Lọc giỏ hàng bị bỏ lại

Sử dụng các bộ lọc bên phải để thu hẹp danh sách:

- **Lý do ước tính** — lọc theo lý do bỏ lại (ví dụ: chỉ hiển thị các giỏ hàng mà lý do ước tính là chi phí vận chuyển cao)
- **Đã thu hồi** — lọc để chỉ hiển thị các giỏ hàng đã thu hồi hoặc chưa thu hồi
- **Bỏ lại lúc** — lọc theo khoảng thời gian để tập trung vào các trường hợp bỏ lại gần đây hoặc một giai đoạn chiến dịch cụ thể

## Hiểu lý do bỏ lại

Spwig ghi lại lý do ước tính cho mỗi trường hợp bỏ lại. Các lý do này dựa trên các tín hiệu được thu thập trong quá trình thanh toán và không đảm bảo chính xác hoàn toàn, nhưng chúng cung cấp một điểm khởi đầu hữu ích để chẩn đoán các mô hình từ bỏ.

| Lý do | Điều này có thể cho thấy |
|---|---|
| **Không xác định** | Không có tín hiệu cụ thể nào được thu thập — lý do phổ biến nhất |
| **Chi phí vận chuyển cao** | Khách hàng có thể đã bị ngăn cản bởi chi phí vận chuyển được hiển thị tại thời điểm thanh toán |
| **Tổng giá quá cao** | Tổng giá đơn hàng có thể cao hơn mức kỳ vọng |
| **Vấn đề thanh toán** | Khách hàng gặp phải vấn đề trong quá trình thanh toán |
| **Thanh toán thất bại** | Một lần thanh toán đã được thực hiện nhưng thất bại |
| **So sánh giá** | Khách hàng có thể đã truy cập để so sánh giá cả |
| **Lưu lại sau** | Khách hàng cố ý lưu các mặt hàng để sử dụng trong lần ghé thăm sau |

Nếu bạn thấy một tỷ lệ lớn các giỏ hàng có cùng lý do — ví dụ, một cụm đáng kể các trường hợp bỏ lại do "Chi phí vận chuyển cao" — đó là một tín hiệu đáng chú ý để bạn kiểm tra lại cài đặt vận chuyển hoặc cách trình bày thanh toán của bạn.

## Xem chi tiết giỏ hàng bị bỏ lại

Nhấp vào bất kỳ hàng nào trong danh sách để mở chế độ xem chi tiết. Bạn sẽ thấy:

- **Chi tiết bỏ lại** — khách hàng, tham chiếu giỏ hàng, thời điểm bỏ lại và lý do ước tính
- **Tóm tắt giỏ hàng** — số lượng mặt hàng và giá trị tổng cộng tại thời điểm bỏ lại
- **Theo dõi thu hồi** — giỏ hàng có được thu hồi không, thời điểm thu hồi và đơn hàng nào nó đã chuyển đổi thành

Trường **Giỏ hàng** liên kết trực tiếp đến bản ghi giỏ hàng gốc, vì vậy bạn có thể xem chính xác những sản phẩm nào có trong giỏ hàng.

## Quy trình thu hồi

Spwig theo dõi xem mỗi giỏ hàng bị bỏ lại có chuyển đổi thành đơn hàng hoàn tất hay không. Khi khách hàng quay lại và hoàn tất mua hàng từ giỏ hàng bị bỏ lại, bản ghi sẽ tự động được đánh dấu là **Đã thu hồi** và đơn hàng kết quả sẽ được liên kết.

Đếm **Số lượng email thu hồi đã gửi** cho thấy số lượng email thu hồi tự động đã được gửi đến khách hàng cho giỏ hàng này. Điều này giúp bạn hiểu liệu chiến dịch email của bạn có đang khuyến khích khách hàng quay lại hay không.

### Hành động thu hồi thủ công

Trang xem giỏ hàng bị bỏ lại chỉ đọc — đây là bản ghi về những gì đã xảy ra, không phải là công cụ để chỉnh sửa nội dung giỏ hàng. Để thực hiện hành động với các giỏ hàng bị bỏ lại:

1.

Ghi lại địa chỉ email của khách hàng từ bản ghi giỏ hàng bị bỏ lại
2.

Sử dụng hệ thống email hoặc công cụ tiếp thị của bạn để gửi một thông điệp cá nhân hóa
3.

Xét đến việc đính kèm mã phiếu giảm giá để cung cấp cho khách hàng động lực hoàn tất việc mua hàng
4.

Bảo toàn tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

Theo dõi trạng thái **Recovered** trong những ngày tới để xem liệu chiến dịch outreach có hiệu quả hay không

## Phân tích xu hướng giỏ hàng bị bỏ lại

Kiểm tra danh sách giỏ hàng bị bỏ lại thường xuyên như một phần kiểm tra sức khỏe cho quy trình thanh toán của bạn:

- Một sự gia tăng đột biến trong các giỏ hàng bị bỏ lại có thể cho thấy vấn đề kỹ thuật trong quy trình thanh toán hoặc thanh toán
- Các giá trị giỏ hàng cao liên tục trong các giỏ hàng chưa được phục hồi đại diện cho phân khúc phục hồi có cơ hội cao nhất
- So sánh tỷ lệ giỏ hàng được phục hồi và chưa được phục hồi theo thời gian để đo lường hiệu quả của các email phục hồi của bạn

Phần **Customer Analytics** trong hồ sơ của mỗi khách hàng cũng hiển thị tỷ lệ bỏ lại giỏ hàng cá nhân của họ, vì vậy bạn có thể xác định những khách hàng thường xuyên thêm sản phẩm vào giỏ nhưng hiếm khi hoàn tất một lần mua hàng.

## Mẹo

- Sắp xếp theo **Tổng giá trị** (giảm dần) để xác định các giỏ hàng có giá trị cao nhất cần ưu tiên cho outreach cá nhân
- Sử dụng bộ lọc **Abandoned At** để xem xét các giỏ hàng bị bỏ lại từ một chiến dịch hoặc giai đoạn khuyến mãi cụ thể — một sự gia tăng trong một đợt bán hàng nhanh có thể có nghĩa là chiến dịch khuyến mãi của bạn thu hút người xem thay vì người mua
- Kết hợp dữ liệu giỏ hàng bị bỏ lại với các chiến dịch phiếu giảm giá: gửi mã giảm giá có thời hạn cho các khách hàng có giỏ hàng chưa phục hồi có giá trị cao để tạo sự cấp bách
- Một giỏ hàng bị bỏ lại hơn 7 ngày không có khả năng phục hồi tự động — nếu email phục hồi được bật, đây là những giỏ hàng cần được chú ý nhất
- Các khách hàng không đăng ký sẽ không xuất hiện trong giỏ hàng bị bỏ lại — việc theo dõi này chỉ áp dụng cho các khách hàng có tài khoản đã đăng ký