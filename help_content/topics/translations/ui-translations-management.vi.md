---
title: Quản lý bản dịch UI
---

Trang Quản lý Bản dịch UI cho phép bạn tùy chỉnh cách hiển thị các chuỗi giao diện phía trước—những nút, nhãn, thông báo lỗi và các văn bản giao diện khác—trong mỗi ngôn ngữ. Khác với bản dịch nội dung sản phẩm hoặc trang, đây là các phần tử giao diện cố định mà khách hàng nhìn thấy trên toàn bộ cửa hàng của bạn. Tùy chỉnh chúng để phù hợp với giọng điệu thương hiệu của bạn hoặc cải thiện tính rõ ràng cho đối tượng cụ thể của bạn.

Trang này hiển thị tất cả các chuỗi UI có thể dịch và cho phép bạn ghi đè các bản dịch mặc định do Spwig cung cấp.

## Hiểu về Bản dịch UI

Bản dịch UI là các chuỗi văn bản tạo nên giao diện cửa hàng của bạn:

**Các ví dụ về chuỗi UI**:
- Nút: "Thêm vào giỏ hàng", "Thanh toán", "Tìm kiếm"
- Nhãn: "Giá", "Số lượng", "Địa chỉ giao hàng"
- Thông báo: "Sản phẩm đã được thêm vào giỏ hàng", "Đơn hàng đã xác nhận", "Địa chỉ email không hợp lệ"
- Điều hướng: "Trang chủ", "Cửa hàng", "Liên hệ"
- Trường biểu mẫu: "Email", "Mật khẩu", "Tên"

Spwig bao gồm các bản dịch mặc định cho khoảng 300 chuỗi UI trong tất cả các ngôn ngữ được hỗ trợ. Trang Quản lý Bản dịch UI cho phép bạn ghi đè bất kỳ bản dịch mặc định nào bằng các bản dịch tùy chỉnh của riêng bạn.

## Tại sao cần tùy chỉnh bản dịch UI?

**Giọng điệu thương hiệu**: Thay đổi "Thêm vào giỏ hàng" thành "Mua ngay" hoặc "Đặt ngay" để phù hợp với cá tính thương hiệu của bạn

**Biến thể khu vực**: Điều chỉnh bản dịch cho các thị trường cụ thể (Tiếng Anh Anh vs Tiếng Anh Mỹ, Tiếng Tây Ban Nha châu Âu vs Tiếng Tây Ban Nha châu Mỹ Latinh)

**Tính rõ ràng**: Nếu bản dịch mặc định không phù hợp với sản phẩm hoặc đối tượng của bạn, thay thế nó bằng văn bản rõ ràng hơn

**Thuật ngữ theo ngành**: Sử dụng thuật ngữ mà khách hàng của bạn mong đợi (ví dụ: "Đặt lịch hẹn" thay vì "Thêm vào giỏ hàng" cho các cửa hàng dựa trên dịch vụ)

## Tìm kiếm chuỗi

Sử dụng hộp tìm kiếm để tìm các chuỗi UI cụ thể:

**Tìm kiếm theo văn bản tiếng Anh**: Nhập "add to cart" để tìm bản dịch của nút đó

**Tìm kiếm theo bản dịch**: Nhập văn bản bằng bất kỳ ngôn ngữ nào để tìm các bản dịch tương ứng

**Tìm kiếm theo khóa**: Nếu bạn biết khóa bản dịch (ví dụ: `cart.add_item`), hãy tìm trực tiếp bằng khóa đó

Trang sẽ cập nhật ngay lập tức khi bạn gõ, chỉ hiển thị các chuỗi khớp.

## Xem chi tiết bản dịch

Mỗi chuỗi UI hiển thị:

**Văn bản nguồn tiếng Anh** - Phiên bản tiếng Anh mặc định (điểm tham chiếu của bạn)

**Khóa bản dịch** - Nhận dạng nội bộ được sử dụng trong mã (ví dụ: `cart.add_to_cart`)

**Cột ngôn ngữ** - Bản dịch hiện tại cho mỗi ngôn ngữ đang hoạt động

**Trạng thái ghi đè** - Liệu bạn có đã tùy chỉnh bản dịch hay không (được đánh dấu nổi bật nếu đã ghi đè)

## Tạo ghi đè bản dịch

Để tùy chỉnh bản dịch của một chuỗi UI:

1. **Tìm chuỗi** bằng cách tìm kiếm (ví dụ: tìm kiếm "add to cart")
2. **Nhấp vào ô ngôn ngữ** bạn muốn tùy chỉnh
3. **Nhập bản dịch tùy chỉnh** của bạn trong trình chỉnh sửa bật lên
4. **Lưu** - Ghi đè của bạn sẽ có hiệu lực ngay lập tức

Bản dịch mặc định ban đầu được giữ nguyên - bạn đang tạo một ghi đè có độ ưu tiên cao hơn.

## Quay lại bản dịch mặc định

Để xóa ghi đè tùy chỉnh và khôi phục bản dịch mặc định:

1. **Nhấp vào bản dịch đã ghi đè** (những bản dịch này được đánh dấu nổi bật)
2. **Nhấp vào "Quay lại bản dịch mặc định"** trong trình chỉnh sửa
3. **Xác nhận** - Bản dịch mặc định sẽ được khôi phục ngay lập tức

Bạn có thể quay lại các ghi đè ngôn ngữ riêng lẻ mà không ảnh hưởng đến các ghi đè khác trong các ngôn ngữ khác.

## Lọc theo trạng thái ghi đè

Sử dụng menu thả xuống để xem:

**Tất cả chuỗi** - Tất cả các chuỗi UI trong hệ thống (~300 tổng số)

**Chỉ chuỗi đã ghi đè** - Các chuỗi mà bạn đã tạo bản dịch tùy chỉnh

**Chỉ chuỗi mặc định** - Các chuỗi vẫn đang sử dụng bản dịch mặc định của Spwig

Điều này giúp bạn xem xét các chuỗi đã được tùy chỉnh và xác định các khoảng trống.

## Các ví dụ tùy chỉnh phổ biến

| Bản dịch tiếng Anh mặc định | Ghi đè tùy chỉnh | Trường hợp sử dụng |
|----------------|----------------|----------|
| Add to Cart | Buy Now | Gọi hành động trực tiếp hơn |
| Checkout | Secure Checkout | Nhấn mạnh tính bảo mật |
| Search | Find Products | Phù hợp hơn với thương mại điện tử |
| Contact Us | Get in Touch | Tông giọng thân thiện hơn |
| Subscribe | Join Our Newsletter | Đề xuất giá trị rõ ràng hơn |

## Kiểm tra tính hợp lệ của bản dịch

Khi nhập các bản dịch tùy chỉnh, hãy kiểm tra:

**Độ dài phù hợp với không gian UI** - Bản dịch có thể dài hơn hoặc ngắn hơn so với tiếng Anh (ví dụ, các từ tiếng Đức thường dài hơn)

**Giữ nguyên ý nghĩa** - Đừng thay đổi chức năng trong bản dịch (nút "Hủy" không nên nói "Xóa")

**Thuật ngữ nhất quán** - Sử dụng cùng một bản dịch cho các thuật ngữ lặp lại trên toàn bộ giao diện

**Mức độ trang trọng phù hợp** - Phù hợp với tông giọng của thị trường mục tiêu (trang trọng vs thân mật)

## Tính nhất quán đa ngôn ngữ

Khi tùy chỉnh một chuỗi cho nhiều ngôn ngữ:

1. **Bắt đầu bằng ngôn ngữ mặc định của bạn** - Thiết lập nền tảng

2. **Tùy chỉnh các ngôn ngữ khác** để phù hợp với cùng ý định

3. **Kiểm tra trên mỗi ngôn ngữ** để xác minh bố cục và ý nghĩa

4. **Sử dụng người bản xứ khi có thể** để xem xét các tùy chỉnh không phải tiếng Anh

Các tùy chỉnh không nhất quán trên các ngôn ngữ tạo ra trải nghiệm khách hàng gây nhầm lẫn.

## Xuất/Nhập hàng loạt

Đối với các tùy chỉnh lớn, hãy xem xét quy trình xuất/nhập:

1. **Xuất** các bản dịch hiện tại dưới dạng JSON hoặc CSV

2. **Chỉnh sửa trong bảng tính** hoặc trình soạn thảo văn bản (dễ dàng hơn cho các thay đổi hàng loạt)

3. **Nhập** lại các bản dịch đã cập nhật trở lại hệ thống

Quy trình này có sẵn qua trang Công việc Bản dịch để quản lý các dự án bản dịch quy mô lớn.

## Một số mẹo

- **Tìm kiếm trước khi tùy chỉnh** - Đảm bảo bạn đang chỉnh sửa chuỗi đúng; một số chuỗi tương tự có thể phục vụ các mục đích khác nhau

- **Kiểm tra trên giao diện phía trước sau khi lưu** - Xác minh bản dịch tùy chỉnh của bạn hiển thị đúng trong giao diện thực tế

- **Giữ bản dịch ngắn gọn** - Ngắn gọn thường tốt hơn cho các nút và nhãn

- **Ghi chú lại các ghi đè của bạn** - Lưu lại lý do bạn tùy chỉnh các chuỗi cụ thể để tham khảo sau này

- **Sử dụng thuật ngữ nhất quán** - Nếu bạn tùy chỉnh "Giỏ hàng" thành "Giỏ", hãy thực hiện điều này nhất quán trên tất cả các chuỗi liên quan

- **Cân nhắc bố cục di động** - Các bản dịch dài có thể bị gãy hoặc cắt trên màn hình nhỏ

- **Xem xét lại sau khi cập nhật ngôn ngữ** - Khi Spwig thêm các bản dịch mặc định mới, hãy xem xét và tùy chỉnh chúng để duy trì tính nhất quán

Hãy nhớ: Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật chính xác như được hiển thị trong các quy tắc bảo tồn.