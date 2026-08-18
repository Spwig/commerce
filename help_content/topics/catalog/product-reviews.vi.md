---
title: Đánh giá sản phẩm
---

Các đánh giá sản phẩm cho phép khách hàng đánh giá và viết về trải nghiệm của họ với sản phẩm. Các đánh giá mà bạn duyệt sẽ xuất hiện trên trang sản phẩm trong cửa hàng của bạn, nơi chúng giúp các khách hàng khác quyết định điều gì nên mua. Spwig cung cấp cho bạn toàn quyền kiểm soát các đánh giá được đăng — không điều gì được công bố cho đến khi bạn duyệt chúng.

Các đánh giá nằm dưới **Sản phẩm > Đánh giá** trong thanh bên, được mở dưới dạng một nhóm: liên kết trên cùng sẽ đưa bạn đến **Bảng điều khiển Đánh giá**, và **Duyệt Đánh giá** sẽ đưa bạn trực tiếp đến danh sách đánh giá.

## Bảng điều khiển Đánh giá

Truy cập **Sản phẩm > Đánh giá** để mở bảng điều khiển — một cái nhìn tổng quan trên cùng một màn hình về cách các đánh giá đang hoạt động trên cửa hàng của bạn.

![Bảng điều khiển Đánh giá](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

Ở đầu trang, sáu thẻ KPI tóm tắt hoạt động đánh giá của bạn:

| Thẻ | Điều nó hiển thị |
|---|---|
| **Tổng số đánh giá** | Tất cả các đánh giá từng được gửi, đã được duyệt hoặc không |
| **Điểm đánh giá trung bình** | Điểm trung bình sao trên mọi đánh giá |
| **Đánh giá đang chờ duyệt** | Các đánh giá đang chờ duyệt hoặc từ chối của bạn |
| **Tỷ lệ duyệt** | Tỷ lệ các đánh giá bạn đã duyệt |
| **Mua hàng đã xác minh** | Tỷ lệ các đánh giá do khách hàng có đơn hàng xác nhận cho sản phẩm đó |
| **Mới (30 ngày)** | Các đánh giá được gửi trong 30 ngày gần đây |

Dưới các KPI, ba biểu đồ cung cấp thêm chi tiết:

- **Phân phối Điểm đánh giá** — biểu đồ thanh cho thấy số lượng đánh giá thuộc mỗi mức điểm đánh giá (1–5). Một cụm đánh giá 1 sao ở đây cần được xem xét ngay lập tức.
- **Số lượng Đánh giá (12 tuần)** — biểu đồ đường của số lượng đánh giá theo tuần, vì vậy bạn có thể phát hiện các điểm tăng đột biến sau một chiến dịch hoặc sự suy giảm cần chú ý.
- **Kênh Mua hàng của Người đánh giá** — biểu đồ hình donut về kênh tiếp thị (trực tiếp, email, tìm kiếm trả phí, mạng xã hội hữu cơ, v.v.) đã mang lại **mua hàng** đằng sau mỗi đánh giá. Điều này tái sử dụng dữ liệu phân bổ của bạn và thực sự hữu ích để xem kênh nào mang lại khách hàng đi kèm với việc để lại đánh giá — nhưng nó **không** phải là ghi chép về cách khách hàng tìm thấy biểu mẫu đánh giá đó. Spwig không theo dõi điều này riêng biệt; xem "Điều chuyến đi có thể làm và không thể làm" ở phần tiếp theo của hướng dẫn này.

Hai danh sách làm tròn bảng điều khiển:

- **Sản phẩm được đánh giá nhiều nhất** — các sản phẩm được đánh giá nhiều nhất của bạn, mỗi sản phẩm đều có số lượng đánh giá và điểm trung bình, liên kết trực tiếp đến sản phẩm.
- **Đang chờ duyệt** — các đánh giá mới nhất đang chờ duyệt của bạn, để bạn có thể nhanh chóng đưa ra quyết định mà không cần rời bảng điều khiển.

## Danh sách đánh giá

Nhấp vào **Duyệt Đánh giá** (hoặc **Sản phẩm > Đánh giá > Duyệt Đánh giá**) để xem mọi đánh giá dưới dạng thẻ, với các bộ lọc ở trên danh sách.

![Danh sách Đánh giá Sản phẩm với các bộ lọc và thẻ đánh giá đang chờ](/static/core/admin/img/help/product-reviews/review-list.webp)

Mỗi thẻ hiển thị hình ảnh sản phẩm, tiêu đề đánh giá, mức điểm đánh giá, nhãn **Đã duyệt**/**Đang chờ**, nhãn **Mua hàng đã xác minh** khi có liên quan, phần xem trước bình luận, và ai đã viết nó cũng như thời gian viết.

### Lọc đánh giá

Sử dụng bảng lọc để thu hẹp danh sách:

- **Tìm kiếm** — khớp với tên sản phẩm, tên người dùng khách hàng, hoặc tiêu đề đánh giá
- **Điểm đánh giá** — chỉ hiển thị các đánh giá có mức điểm sao cụ thể (rất hữu ích để điều tra các khiếu nại điểm 1 sao)
- **Duyệt** — nhanh chóng tách biệt giữa các đánh giá đã duyệt và đang chờ duyệt
- **Đã xác minh** — lọc các đánh giá từ khách hàng có đơn hàng xác nhận cho sản phẩm đó

Việc lọc diễn ra ngay lập tức mà không cần tải lại trang.

## Duyệt và từ chối đánh giá

Các đánh giá sẽ không xuất hiện trên cửa hàng của bạn cho đến khi bạn duyệt chúng. Bạn có thể duyệt hoặc từ chối các đánh giá riêng lẻ hoặc theo lô.

### Hành động theo lô

1. Trong danh sách đánh giá, chọn các ô bên cạnh các đánh giá bạn muốn thực hiện
2. Chọn **Duyệt các đánh giá được chọn** hoặc **Từ chối các đánh giá được chọn** từ danh sách thả xuống hành động
3. Nhấp vào **Go**

Đây là cách nhanh nhất để xử lý một lô các đánh giá mới.

### Đánh giá riêng lẻ

1.

Nhấp vào biểu tượng chỉnh sửa trên thẻ đánh giá, hoặc tiêu đề của nó, để mở đánh giá
2.

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật.

Trên tab **Đánh giá**, chọn hoặc bỏ chọn **Đã được phê duyệt**
3.

Nhấp vào nút dấu kiểm trong tiêu đề để lưu

## Trang chỉnh sửa đánh giá

Việc mở một đánh giá sẽ mang lại cho bạn một giao diện kiểu bảng điều khiển được xây dựng xung quanh chính đánh giá đó — một tiêu đề với tên sản phẩm, xếp hạng sao, nhãn **Đã được phê duyệt**/**Đang chờ**, nhãn **Mua hàng đã xác minh** khi có liên quan, ai đã viết đánh giá và thời gian, cùng một hàng thống kê (**Xếp hạng**, **Lượt bình chọn hữu ích**, **Đơn hàng khách hàng**, **Tổng chi tiêu trong suốt thời gian**) . Dưới đó, phần chi tiết được tổ chức thành bốn tab.

![Trang chỉnh sửa đánh giá — Tab Đánh giá với bộ sưu tập hình ảnh](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Tab Đánh giá

Đây là nơi bạn kiểm duyệt bản thân đánh giá:

- **Hình ảnh đánh giá** — nếu khách hàng đính kèm hình ảnh, chúng sẽ xuất hiện ở đây dưới dạng bộ sưu tập hình thu nhỏ; nhấp vào bất kỳ hình thu nhỏ nào để mở hình ảnh đầy đủ trong tab mới. Các đánh giá có hình ảnh là tín hiệu tin cậy mạnh cho người mua, vì vậy đây là điều worth một cái nhìn trước khi bạn phê duyệt.
- **Xếp hạng**, **Tiêu đề**, **Bình luận** — nội dung mà khách hàng đã gửi
- **Đã được phê duyệt** — kiểm soát xem đánh giá có hiển thị trên cửa hàng của bạn hay không
- **Mua hàng đã xác minh** — đánh dấu đánh giá là đến từ người mua được xác nhận; Spwig thiết lập điều này tự động khi có tồn tại đơn hàng đã hoàn tất cho sản phẩm (xem tab **Mua hàng**), nhưng bạn có thể ghi đè nó ở đây nếu cần
- **Hình ảnh** — danh sách các URL hình ảnh nền phía sau bộ sưu tập trên; bạn thường không cần phải chỉnh sửa điều này, nhưng nó vẫn có thể chỉnh sửa được cho các trường hợp đặc biệt (ví dụ: xóa bỏ một hình ảnh khỏi đánh giá có nhiều hình ảnh)

Bạn không thể chỉnh sửa từ ngữ của đánh giá — việc phê duyệt hoặc từ chối, và quản lý hình ảnh là phạm vi kiểm soát của bạn ở đây.

### Tab Khách hàng & Hành trình

![Trang chỉnh sửa đánh giá — Tab Khách hàng & Hành trình](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

Tab này cung cấp thông tin về ai đã để lại đánh giá: tổng số đơn hàng, số lượng đánh giá mà họ đã viết, xếp hạng trung bình mà họ đưa ra, thời gian họ đã là khách hàng, và thông tin liên lạc của họ, với một liên kết để mở hồ sơ khách hàng đầy đủ của họ.

Dưới đó là **hành trình nguồn truy cập** — các kênh, chiến dịch và người giới thiệu đã mang khách hàng đến cửa hàng của bạn, được lấy từ dữ liệu phân biệt và hiển thị dưới dạng một chuỗi thời gian.

#### Điều mà "hành trình" làm và không làm

Đọc chuỗi thời gian này như là **hành trình đến và mua hàng** của khách hàng — cách họ ban đầu tìm thấy cửa hàng của bạn và sau đó mua hàng. Nó **không phải** là ghi chép về lần truy cập mà họ đã để lại đánh giá này. Spwig không theo dõi nơi khách hàng đang ở, hoặc thiết bị hoặc phiên nào họ sử dụng, vào thời điểm họ gửi đánh giá. Nếu chuỗi thời gian hiển thị "Email > chăm sóc da mùa hè" ba tuần trước ngày đánh giá, điều đó cho bạn biết chiến dịch email có thể đã thúc đẩy việc *mua hàng* — nó không nói lên điều gì về việc khách hàng có quay lại từ kết quả tìm kiếm, một dấu trang, hay một email theo dõi để thực sự để lại đánh giá hay không. Xem xét tab này như là bối cảnh tiếp thị hữu ích, chứ không phải là một dấu vết chính xác của việc gửi đánh giá.

### Tab Mua hàng

![Trang chỉnh sửa đánh giá — Tab Mua hàng](/static/core/admin/img/help/product-reviews/review-edit-purchase-tab.webp)

Tab này liệt kê mọi đơn hàng mà khách hàng đã mua sản phẩm được đánh giá — số đơn hàng, ngày, tổng số, trạng thái, và kênh mua hàng cho đơn hàng đó. Nếu bất kỳ đơn hàng nào trong số đó đã đạt trạng thái đã hoàn tất (giao hàng hoặc giao xong), bạn sẽ thấy một ghi chú xác nhận rằng đây là một lần mua hàng đã xác minh — cùng một tín hiệu mà thiết lập **Mua hàng đã xác minh** tự động trên tab Đánh giá.

Nếu không có đơn hàng nào khớp xuất hiện ở đây, người đánh giá có thể đã mua sản phẩm trước khi cửa hàng của bạn theo dõi đơn hàng trong Spwig, hoặc họ chưa bao giờ thực sự mua sản phẩm đó — điều worth biết trước khi bạn quyết định xem đánh giá đó có đáng được cân nhắc nhiều hay không.

### Tab Nâng cao

Thông tin mô tả bạn hiếm khi cần chạm vào: **Số lần được cho là hữu ích** (số lượng khách hàng đã đánh dấu đánh giá là hữu ích), nguồn gốc nhập liệu nếu đánh giá được di dời từ nền tảng khác, và các mốc thời gian được tạo/mới cập nhật.

## Lời khuyên

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật.

- Kiểm tra danh sách **Đang chờ kiểm duyệt** trên bảng điều khiển ngay từ đầu — đây là cách nhanh nhất để xem điều gì cần đưa ra quyết định mà không cần mở danh sách đánh giá đầy đủ
- Một nhóm các đánh giá 1 sao trên cùng một sản phẩm trong biểu đồ **Phân phối đánh giá** là dấu hiệu rõ ràng để kiểm tra bao bì, chất lượng sản phẩm hoặc nội dung mô tả sản phẩm của bạn
- Sử dụng bộ lọc **Đã xác minh** khi quyết định cách xử lý các đánh giá biên giới — phản hồi từ khách hàng đã xác nhận đơn hàng mang nhiều trọng lượng hơn trong bất kỳ tranh chấp nào
- Duyệt các đánh giá một cách nhanh chóng, bao gồm cả những đánh giá tiêu cực — một đánh giá tiêu cực hiển thị cùng với không có phản hồi nào có thể tệ hơn so với một khiếu nại đã được xử lý, và các đánh giá xuất hiện chậm sẽ làm giảm động lực của khách hàng để lại phản hồi trong tương lai
- Đừng đọc quá kỹ **Hành trình nguồn truy cập** hoặc biểu đồ **Kênh mua hàng của người đánh giá** trên bảng điều khiển — cả hai đều mô tả cách khách hàng đến và mua hàng, chứ không phải cách họ đến để viết đánh giá
- Các đánh giá có hình ảnh cần được xem xét kỹ hơn trước khi duyệt; các hình ảnh sản phẩm từ khách hàng thực sự là nội dung thuyết phục nhất trên cửa hàng của bạn