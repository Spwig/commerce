---
title: Bảng điều khiển Cửa hàng
---

Bảng điều khiển Cửa hàng cung cấp cho bạn cái nhìn toàn diện về hiệu suất của cửa hàng — doanh thu, đơn hàng, sản phẩm bán chạy, lưu lượng truy cập khách hàng và nhiều hơn nữa — tất cả tại một nơi. Sử dụng nó để hiểu rõ những gì đang được bán, khách hàng của bạn đến từ đâu và xu hướng cửa hàng theo thời gian như thế nào.

Truy cập **Quản lý > Chỉ số hệ thống** và nhấp vào **Bảng điều khiển Cửa hàng** từ thanh công cụ.

![Tổng quan Bảng điều khiển Cửa hàng](/static/core/admin/img/help/shop-dashboard/overview.webp)

## Chọn khoảng thời gian

Bảng điều khiển lọc tất cả các chỉ số theo khoảng thời gian đã chọn. Sử dụng trình chọn khoảng thời gian ở đầu trang để chọn:

| Khoảng thời gian | Nội dung hiển thị |
|------------------|------------------|
| Hôm nay | Ngày hôm nay so với hôm qua |
| Tuần này | Từ thứ Hai đến hôm nay so với tuần trước |
| Tháng này | Tháng hiện tại so với tháng trước |
| Năm nay | Từ đầu năm đến nay so với cùng kỳ năm trước |
| 30 ngày gần đây | Khoảng thời gian 30 ngày di động |
| 90 ngày gần đây | Khoảng thời gian 90 ngày di động |
| Tùy chỉnh | Nhập ngày bắt đầu và ngày kết thúc cụ thể |

Hầu hết các biểu đồ hiển thị **sự so sánh** với khoảng thời gian tương ứng trong quá khứ, vì vậy bạn có thể thấy hiệu suất đang cải thiện hay suy giảm. Tắt công tắc **So sánh** nếu bạn chỉ muốn xem các con số hiện tại.

## Thẻ hành động

Ở đầu bảng điều khiển, các thẻ hành động làm nổi bật các mục cần sự chú ý của bạn ngay lúc này:

- **Đơn hàng chưa hoàn tất** — các đơn hàng đang chờ xử lý
- **Giỏ hàng bị bỏ lại** — các phiên làm việc mà khách hàng đã thêm sản phẩm nhưng chưa hoàn tất thanh toán
- **Tin nhắn chưa đọc** — các câu hỏi của khách hàng đang chờ trả lời
- **Thông báo tồn kho thấp** — các sản phẩm đang thiếu tồn kho

Nhấp vào bất kỳ thẻ hành động nào để di chuyển trực tiếp đến phần quản trị liên quan.

## Hiệu suất bán hàng

Phần hiệu suất bán hàng hiển thị các con số doanh thu chính của bạn cho khoảng thời gian đã chọn:

- **Doanh thu tổng cộng** — doanh thu thô trước khi trừ các khoản chi phí
- **Tổng số đơn hàng** — số lượng đơn hàng đã hoàn tất
- **Giá trị đơn hàng trung bình** — doanh thu chia cho số lượng đơn hàng
- **Lợi nhuận ròng** — doanh thu trừ đi chi phí hàng hóa và các khoản chi phí (nếu được cấu hình)

Mỗi con số hiển thị một mũi tên và phần trăm cho thấy sự thay đổi từ khoảng thời gian so sánh.

## Biểu đồ doanh thu theo thời gian

Biểu đồ chính vẽ ra doanh thu hoặc đơn hàng của bạn trong khoảng thời gian đã chọn. Spwig tự động chọn cách phân nhóm hữu ích nhất:

- Các khoảng thời gian ngắn (tối đa một tuần) phân nhóm theo ngày
- Các khoảng thời gian trung bình (tối đa ba tháng) phân nhóm theo tuần
- Các khoảng thời gian dài phân nhóm theo tháng

Bạn có thể ghi đè cách phân nhóm bằng điều khiển **Phân nhóm theo** phía trên biểu đồ. Di chuột qua bất kỳ điểm nào để xem giá trị chính xác cho ngày đó.

## Sản phẩm bán chạy

Bảng **Sản phẩm bán chạy** liệt kê các sản phẩm bán chạy nhất trong khoảng thời gian đã chọn, được xếp hạng theo doanh thu. Mỗi hàng hiển thị:

- **Tên sản phẩm**
- **Số lượng đã bán**
- **Doanh thu tạo ra**

Sử dụng để xác định các sản phẩm mạnh nhất của bạn và quyết định nơi tập trung vào các chương trình khuyến mãi hoặc bổ sung tồn kho.

## Phân tích người truy cập

Phần phân tích người truy cập hiển thị số lượng người đã truy cập cửa hàng của bạn và hành vi của họ:

- **Tổng số người truy cập** — số lượng người truy cập duy nhất vào cửa hàng của bạn
- **Lượt xem trang** — tổng số trang được xem
- **Tỷ lệ thoát** — tỷ lệ phần trăm người truy cập chỉ xem một trang
- **Lượt xem theo thời gian** — biểu đồ hiển thị lượng truy cập theo khoảng thời gian đã chọn

Panel **Địa lý** hiển thị nơi người truy cập của bạn đến từ, được phân chia theo quốc gia và (nếu có sẵn) thành phố.

## Nguồn lưu lượng

Panel nguồn lưu lượng hiển thị cách người truy cập tìm thấy cửa hàng của bạn:

| Nguồn | Mô tả |
|--------|-------------|
| Trực tiếp | Người truy cập đã nhập URL của bạn hoặc sử dụng bookmark |
| Tìm kiếm tự nhiên | Người truy cập đến từ các công cụ tìm kiếm |
| Mạng xã hội | Người truy cập đến từ các nền tảng mạng xã hội |
| Giới thiệu | Người truy cập đến từ các trang web khác liên kết đến bạn |
| Email | Người truy cập nhấp vào các liên kết trong email |

Sử dụng thông tin này để hiểu rõ các kênh marketing nào tạo ra lượng truy cập lớn nhất và nơi nên đầu tư.

## Kênh chuyển đổi

Kênh chuyển đổi hiển thị cách người truy cập di chuyển từ việc xem sản phẩm đến hoàn tất mua hàng:

1. **Khách truy cập** — tổng số khách truy cập duy nhất
2. **Lượt xem sản phẩm** — khách truy cập đã xem ít nhất một sản phẩm
3. **Thêm vào giỏ hàng** — khách truy cập đã thêm một mặt hàng vào giỏ hàng
4. **Bắt đầu thanh toán** — khách truy cập đã bắt đầu quy trình thanh toán
5. **Đơn hàng hoàn tất** — khách truy cập đã đặt hàng

Tỷ lệ phần trăm ở mỗi bước cho thấy tỷ lệ giảm. Sự giảm lớn giữa **Thêm vào giỏ hàng** và **Bắt đầu thanh toán** cho thấy có sự cản trở trong quy trình thanh toán của bạn.

## Hiệu suất phiếu giảm giá

Nếu bạn chạy các chương trình khuyến mãi phiếu giảm giá, phần này sẽ hiển thị hiệu suất của chúng trong khoảng thời gian đã chọn:

- **Tổng số lần sử dụng** — số lần phiếu giảm giá được sử dụng
- **Tổng số chiết khấu** — tổng số tiền chiết khấu từ các phiếu giảm giá đã áp dụng
- **Doanh thu có phiếu giảm giá** — tổng doanh thu từ các đơn hàng có sử dụng phiếu giảm giá

## Phân khúc khách hàng

Bảng điều khiển phân khúc khách hàng chia cơ sở khách hàng của bạn thành các nhóm:

- **Khách hàng mới** — những người mua hàng lần đầu trong khoảng thời gian đã chọn
- **Khách hàng quay lại** — những khách hàng đã mua hàng trước đó
- **Thanh toán khách truy cập** — các đơn hàng được đặt mà không cần tạo tài khoản

Việc hiểu tỷ lệ giữa khách hàng mới và khách hàng quay lại giúp bạn quyết định xem nên đầu tư nhiều hơn vào việc thu hút (quảng cáo) hay giữ chân (chương trình khách hàng thân thiết).

## Tổng quan về đại lý và chương trình khách hàng thân thiết

Nếu cửa hàng của bạn có chương trình đại lý hoặc chương trình khách hàng thân thiết đang hoạt động, các chỉ số hiệu suất tổng hợp sẽ hiển thị tại đây — tổng số hoa hồng đã kiếm được, tổng số điểm đã phát hành, và các đại lý hoặc người sử dụng điểm hiệu quả nhất.

## Một số mẹo

- Kiểm tra bảng điều khiển mỗi sáng thứ Hai để có cái nhìn nhanh về tuần qua — khoảng thời gian **Tuần này** cung cấp cái nhìn rõ ràng về hiệu suất gần đây
- Sử dụng phạm vi thời gian **Tùy chỉnh** để đo lường tác động của một chiến dịch cụ thể: đặt ngày bắt đầu và kết thúc cho giai đoạn chiến dịch
- Nếu biểu đồ chuyển đổi cho thấy sự giảm mạnh tại **Bắt đầu thanh toán**, hãy cân nhắc đơn giản hóa quy trình thanh toán của bạn hoặc thêm các biểu tượng tin cậy
- Số lượng giỏ hàng bị bỏ qua cao đi kèm với tỷ lệ chuyển đổi thấp có thể cho thấy vấn đề về giá cả hoặc chi phí vận chuyển — hãy xem lại các chi phí thanh toán của bạn
- So sánh các khoảng thời gian theo năm bằng cách sử dụng khoảng thời gian **Năm nay** để hiểu rõ hơn về các xu hướng theo mùa trong kinh doanh của bạn
- Xuất hoặc chụp ảnh bảng danh sách sản phẩm hàng đầu trước các quyết định nhập hàng lớn để đảm bảo bạn đặt đúng số lượng