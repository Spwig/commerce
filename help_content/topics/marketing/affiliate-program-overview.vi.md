---
title: Tổng quan chương trình đại lý
---

Tính năng chương trình đại lý của Spwig cho phép bạn tuyển dụng các đối tác quảng bá sản phẩm của bạn để đổi lấy hoa hồng. Kênh tiếp thị này mở rộng phạm vi của bạn thông qua các nhà ảnh hưởng, blogger, nhà sáng tạo nội dung và đại sứ thương hiệu chia sẻ các liên kết theo dõi duy nhất với khán giả của họ. Khi ai đó nhấp vào liên kết đại lý và thực hiện mua hàng, đại lý sẽ nhận được hoa hồng và bạn sẽ có được một khách hàng.

Tổng quan này giải thích chương trình đại lý là gì, đối tượng sử dụng và cách các nhà bán lẻ sử dụng nó để xây dựng mạng lưới đối tác thúc đẩy doanh số.

![Bảng điều khiển nhà bán hàng](/static/core/admin/img/help/affiliate-program-overview/merchant-dashboard.webp)

## Khái niệm chính

Hiểu rõ các thuật ngữ cốt lõi sau sẽ giúp bạn cấu hình và quản lý chương trình đại lý của mình:

| Thuật ngữ | Định nghĩa |
|----------|-----------|
| **Đại lý** | Một đối tác quảng bá sản phẩm của bạn và nhận được hoa hồng từ các giao dịch được giới thiệu |
| **Chương trình** | Một cấu trúc hoa hồng với tỷ lệ, quy tắc và cài đặt (bạn có thể tạo nhiều chương trình) |
| **Liên kết theo dõi** | Một URL duy nhất chứa mã đại lý (ví dụ: `yourstore.com/?ref=CODE`) |
| **Hoa hồng** | Số tiền đại lý nhận được cho một giao dịch được giới thiệu, được tính dựa trên quy tắc của chương trình |
| **Thời gian sống cookie** | Thời gian (tính bằng ngày) mà cookie theo dõi duy trì sau khi khách hàng nhấp vào liên kết đại lý |
| **Thanh toán** | Một khoản thanh toán theo khối để thanh toán nhiều khoản hoa hồng đã được phê duyệt cùng lúc |
| **Bảng điều khiển nhà bán hàng** | Giao diện quản trị của bạn để quản lý chương trình, đại lý, hoa hồng và thanh toán |
| **Bảng điều khiển đại lý** | Bảng điều khiển hướng tới công chúng nơi các đại lý xem doanh thu, nhận liên kết theo dõi và yêu cầu thanh toán |

## Cách hoạt động

Quy trình đại lý tuân theo bốn giai đoạn chính:

### 1. Ứng tuyển

Đại lý tìm thấy chương trình của bạn và nộp đơn thông qua bảng điều khiển đại lý công khai tại `/affiliate/` trên cửa hàng của bạn. Bạn có thể bật **phê duyệt tự động** cho các chương trình mở hoặc **xem xét thủ công** cho các đối tác mời.

### 2. Phê duyệt

Bạn xem xét các đơn ứng tuyển đang chờ xử lý tại **Marketing > Affiliates**. Kiểm tra trang web, sự hiện diện trên mạng xã hội và sự phù hợp với khán giả của từng ứng viên trước khi phê duyệt. Sau khi được phê duyệt, đại lý nhận được thông tin đăng nhập và có thể truy cập bảng điều khiển của họ.

### 3. Quảng bá

Các đại lý đã được phê duyệt nhận được các liên kết giới thiệu duy nhất từ bảng điều khiển của họ. Họ chia sẻ các liên kết này trong các bài đăng blog, mạng xã hội, bản tin email hoặc bất cứ nơi nào họ kết nối với khán giả của mình. Spwig thiết lập cookie theo dõi khi ai đó nhấp vào liên kết.

### 4. Nhận hoa hồng

Khi khách hàng được giới thiệu hoàn tất mua hàng trong thời gian sống cookie, Spwig tạo ra bản ghi hoa hồng. Bạn xem xét và phê duyệt các khoản hoa hồng tại **Marketing > Commissions**, sau đó xử lý các khoản thanh toán khi đại lý đạt đến ngưỡng thanh toán tối thiểu.

## Tổng quan quy trình nhà bán hàng

Là nhà bán hàng, bạn quản lý toàn bộ vòng đời chương trình từ bảng điều khiển quản trị của mình:

### Tạo chương trình

Bắt đầu bằng cách tạo một hoặc nhiều chương trình đại lý tại **Marketing > Affiliate Programs**. Mỗi chương trình có cấu trúc hoa hồng riêng, thời gian sống cookie và cài đặt phê duyệt. Bạn có thể tạo các chương trình riêng biệt cho các nhà ảnh hưởng (hoa hồng cao hơn) và đối tác chung (hoa hồng thấp hơn).

### Xem xét đơn ứng tuyển

Các đơn ứng tuyển đại lý mới xuất hiện tại **Marketing > Affiliates** với trạng thái **Đang chờ**. Xem xét từng đơn ứng tuyển để xác minh đối tác có phù hợp với thương hiệu của bạn hay không. Phê duyệt để kích hoạt tài khoản của họ hoặc từ chối với lý do.

### Phê duyệt hoa hồng

Khi đại lý tạo ra doanh số, các khoản hoa hồng sẽ xuất hiện tại **Marketing > Commissions** với trạng thái **Đang chờ**. Xem xét đơn hàng liên kết để xác minh nó là hợp lệ (không phải tự giới thiệu, không phải đơn hàng hoàn tiền), sau đó phê duyệt hoặc từ chối tương ứng.

### Xử lý thanh toán

Khi đại lý tích lũy các khoản hoa hồng đã được phê duyệt vượt quá ngưỡng thanh toán tối thiểu của bạn, xử lý các khoản thanh toán theo khối tại **Marketing > Payouts**. Spwig tích hợp với PayPal và Airwallex để thanh toán tự động, hoặc bạn có thể ghi lại các chuyển khoản ngân hàng thủ công.

## Tổng quan quy trình đại lý

Hiểu cách đại lý trải nghiệm chương trình của bạn giúp bạn thiết kế quy trình hướng dẫn và hỗ trợ tốt hơn:

### Ứng tuyển

Đại lý truy cập bảng điều khiển đại lý của bạn, đọc chi tiết chương trình (tỷ lệ hoa hồng, thời gian sống cookie, điều khoản thanh toán) và nộp đơn với thông tin liên lạc và các kênh quảng bá của họ.

### Tạo liên kết

Sau khi được phê duyệt, đại lý đăng nhập vào bảng điều khiển của họ để tạo các liên kết theo dõi. Họ có thể tạo các liên kết chung cho cửa hàng hoặc các liên kết đến các sản phẩm/danh mục cụ thể mà họ muốn quảng bá.

### Quảng bá

Đại lý chia sẻ các liên kết theo dõi của họ ở bất cứ nơi nào họ kết nối với khách hàng tiềm năng — bài đăng blog, video YouTube, câu chuyện Instagram, bản tin email hoặc các trang so sánh.

### Yêu cầu thanh toán

Đại lý theo dõi doanh thu của họ theo thời gian thực thông qua bảng điều khiển đại lý. Khi số dư đã được phê duyệt đạt đến ngưỡng thanh toán tối thiểu, họ có thể yêu cầu thanh toán.

## Nơi tìm thấy từng tính năng

| Tính năng | Vị trí quản trị | Mô tả |
|----------|----------------|--------|
| **Chương trình** | Marketing > Affiliate Programs | Tạo và cấu hình cấu trúc hoa hồng |
| **Đại lý** | Marketing > Affiliates | Xem xét đơn ứng tuyển, quản lý tài khoản đại lý |
| **Hoa hồng** | Marketing > Commissions | Xem xét và phê duyệt các khoản hoa hồng đang chờ |
| **Thanh toán** | Marketing > Payouts | Xử lý các khoản thanh toán theo khối cho đại lý |
| **Cài đặt** | Marketing > Affiliate Settings | Cài đặt toàn cầu, nhà cung cấp thanh toán, tùy chỉnh bảng điều khiển |
| **Bảng điều khiển** | Marketing > Affiliate Dashboard | Tổng quan phân tích với số lần nhấp, đơn hàng và tổng số hoa hồng |

Bảng điều khiển dành cho đại lý tự động có sẵn tại `/affiliate/` trên URL công khai của cửa hàng bạn.

## Các trường hợp sử dụng phổ biến

Dưới đây là bốn cách đã được chứng minh mà các nhà bán lẻ sử dụng chương trình đại lý Spwig để phát triển doanh nghiệp của họ:

### Hợp tác với các nhà ảnh hưởng

Hợp tác với các nhà ảnh hưởng mạng xã hội có khán giả tích cực trong lĩnh vực của bạn. Cung cấp tỷ lệ hoa hồng cao hơn (15–20%) để thu hút các nhà ảnh hưởng chất lượng có thể mang lại lượng truy cập đáng kể. Sử dụng các liên kết theo dõi để đo lường ROI cho mỗi hợp tác.

### Đại sứ thương hiệu

Xây dựng mạng lưới các khách hàng trung thành trở thành đại sứ thương hiệu. Cung cấp tài khoản đại lý cho các khách hàng quay lại để họ có thể nhận được hoa hồng khi họ giới thiệu bạn bè và gia đình. Điều này đặc biệt hiệu quả với các sản phẩm chuyên biệt có cộng đồng đam mê.

### Nhà sáng tạo nội dung

Tuyển dụng các nhà blog, YouTuber và podcasters tạo ra các hướng dẫn mua sắm, đánh giá hoặc nội dung so sánh. Các đại lý có nội dung bền vững có thể tạo ra các giới thiệu liên tục hàng tháng.

### Mạng lưới giới thiệu

Cho phép khách hàng hiện tại tham gia chương trình và nhận được hoa hồng khi chia sẻ các sản phẩm họ yêu thích. Điều này tạo ra vòng lặp lan truyền nơi các khách hàng hài lòng trở thành người quảng bá, mang đến các khách hàng mới có thể cũng trở thành đại lý.

## Một số mẹo

- **Bắt đầu với một chương trình** — Tạo một chương trình đối tác chung với tỷ lệ hoa hồng 10% và thời gian sống cookie 30 ngày. Bạn có thể thêm các chương trình chuyên biệt sau khi hiểu rõ các đối tác nào hoạt động tốt nhất.
- **Đặt các kỳ vọng rõ ràng** — Ghi lại quy trình phê duyệt, thời gian thanh toán hoa hồng và lịch trình thanh toán trong bảng điều khiển đại lý. Sự minh bạch xây dựng lòng tin và giảm các yêu cầu hỗ trợ.
- **Theo dõi gian lận** — Kiểm tra kỹ các khoản hoa hồng để phát hiện các dấu hiệu đỏ như tự giới thiệu (đại lý mua hàng từ các liên kết của họ), tỷ lệ hoàn tiền bất thường hoặc mẫu nhấp đáng ngờ. Từ chối ngay lập tức các khoản hoa hồng gian lận.
- **Giao tiếp thường xuyên** — Gửi cập nhật hàng tháng cho các đại lý với tin tức chương trình, các điểm nổi bật trong lịch quảng bá và ghi nhận các đại lý hàng đầu. Việc giao tiếp tích cực giữ cho các đại lý gắn kết và tiếp tục quảng bá.
- **Tối ưu hóa cho di động** — Hầu hết các đại lý chia sẻ liên kết trên mạng xã hội nơi phần lớn lượt nhấp đến từ thiết bị di động. Kiểm tra quy trình thanh toán trên điện thoại để đảm bảo trải nghiệm mượt mà cho khách hàng được giới thiệu.
- **Cung cấp tài sản sáng tạo** — Làm cho việc đại lý quảng bá sản phẩm của bạn trở nên dễ dàng bằng cách cung cấp hình ảnh banner, hình ảnh sản phẩm và nội dung đã viết sẵn mà họ có thể sử dụng trong nội dung của họ.