---
title: Di chuyển từ Magento
---

Spwig có thể nhập danh mục, khách hàng, đơn hàng, phiếu giảm giá và trang CMS trực tiếp từ cửa hàng Magento 2 hoặc Adobe Commerce đang hoạt động bằng REST API của Magento. Hướng dẫn này sẽ hướng dẫn bạn tạo các thông tin xác thực tích hợp mà Magento yêu cầu, chạy chương trình di chuyển và một điểm thiếu hụt lớn mà các nhà bán hàng chuyển từ Magento cần lên kế hoạch: đánh giá sản phẩm.

Chỉ **Magento 2 và Adobe Commerce** được hỗ trợ. Magento 1 đã hết thời gian hỗ trợ cách đây nhiều năm và không cung cấp REST API mà việc di chuyển này phụ thuộc vào — nếu bạn vẫn đang sử dụng Magento 1, hãy sử dụng [Nhập từ tập tin CSV](csv-import) thay vào đó.

## Trước khi bắt đầu

Xem [Tổng quan di chuyển dữ liệu](migration-overview) để có hướng dẫn lập kế hoạch tổng quát. Đối với Magento cụ thể:

- **Danh mục** — được nhập với cấu trúc phân cấp được giữ nguyên.
- **Sản phẩm** — được nhập, bao gồm hình ảnh.
- **Khách hàng và địa chỉ** — được nhập.
- **Đơn hàng** — được nhập.
- **Phiếu giảm giá** — được nhập dưới dạng phiếu giảm giá của Spwig, được lấy từ các quy tắc bán hàng của Magento.
- **Trang CMS** — được nhập dưới dạng trang của Spwig.
- **Đánh giá** — thường **không** được nhập. Hãy xem phần tiếp theo trước khi dựa vào điều này.
- Các biến thể được hỗ trợ cho sản phẩm cấu hình.

> **Lưu ý:** Các cuộc di chuyển Magento không chuyển tiếp các chương trình liên kết, hoa hồng hoặc thanh toán — tích hợp cầu nối liên kết của Spwig chỉ có sẵn cho các cửa hàng WooCommerce.

### Giới hạn đánh giá

Magento Community Edition không cung cấp điểm cuối REST cho đánh giá sản phẩm — tuyến đường `/reviews` đơn giản không tồn tại trên cài đặt Community tiêu chuẩn. Spwig kiểm tra xem nó có tồn tại không trước khi nhập, và nếu không có, sẽ ghi lại một thông báo và tiếp tục với phần còn lại của cuộc di chuyển thay vì làm hỏng toàn bộ công việc. Các danh mục, sản phẩm, khách hàng, đơn hàng, phiếu giảm giá và trang của bạn vẫn được chuyển; chỉ đánh giá bị bỏ qua.

Đánh giá **sẽ** được nhập nếu cửa hàng của bạn chạy **Adobe Commerce** (nơi cung cấp điểm cuối này) hoặc nếu cài đặt Magento của bạn có mô-đun tùy chỉnh thêm tuyến đường đánh giá tương thích.

Nếu bạn đang sử dụng Magento Community và cần đánh giá trong Spwig, hãy xuất chúng riêng (hầu hết các phần mở rộng đánh giá cung cấp xuất CSV) và sau đó nhập chúng bằng tệp đánh giá trong [Nhập từ tập tin CSV](csv-import), được liên kết với sản phẩm của bạn bằng `product_id`.

## Bước 1: Chọn Magento

Từ bảng điều khiển di chuyển tại **Nhập và Xuất Dữ liệu**, nhấp **Bắt đầu Di chuyển Mới** và chọn **Magento** làm nền tảng của bạn.

## Bước 2: Kết nối đến Cửa hàng của Bạn

Bạn sẽ cần URL cửa hàng Magento của bạn và một token truy cập tích hợp. Magento không cấp một khóa API đơn giản như một số nền tảng — bạn tạo một **Tích hợp**, là một thông tin xác thực có phạm vi mà Magento xử lý như một ứng dụng được kết nối.

### Tạo Token Truy cập Tích hợp

1. Trong Magento admin, đi đến **Hệ thống > Tích hợp**.
2. Nhấp **Thêm Tích hợp Mới**.
3. Đặt tên là `Spwig Migration` để dễ dàng nhận biết sau này.
4. Mở tab **API** và đặt **Truy cập Tài nguyên** thành **Tất cả**.
5. Nhấp **Lưu**, sau đó nhấp **Kích hoạt**.
6. Xác nhận bằng cách nhấp **Cho phép** trên hộp thoại liệt kê các quyền được cấp.
7. Sao chép token truy cập được hiển thị sau khi kích hoạt — Magento chỉ hiển thị nó một lần.

> **Lưu ý:** Truy cập Tài nguyên được đặt thành **Tất cả** vì cây tài nguyên của Magento rất chi tiết — hàng trăm quyền riêng lẻ bao gồm danh mục, bán hàng, khách hàng và CMS — không có nút bật/tắt "đọc tất cả" nào ngoại trừ việc chọn tất cả chúng. Cuộc di chuyển chỉ bao giờ đọc từ cửa hàng của bạn; nó không bao giờ ghi lại, và bạn có thể hủy tích hợp sau khi xác nhận cuộc di chuyển của bạn (được đề cập ở cuối hướng dẫn này).

Quay lại chương trình hướng dẫn của Spwig, nhập **URL Cửa hàng** và **Token Truy cập** bạn đã sao chép. Giữ tùy chọn **Kiểm tra kết nối trước khi tiếp tục** được chọn (mặc định bật) để Spwig xác minh nó có thể kết nối và xác thực với cửa hàng của bạn trước khi bạn tiếp tục. Nếu kiểm tra thất bại, hãy kiểm tra lại URL và đảm bảo tích hợp vẫn đang **Hoạt động** trong Magento. Nhấp **Tiếp theo**.

screenshots-needed

heading

## Bước 3: Xem trước nội dung sẽ được nhập

paragraph

Spwig truy vấn cửa hàng Magento của bạn và hiển thị các con số trực tiếp cho từng loại dữ liệu mà nó tìm thấy: danh mục, sản phẩm, khách hàng, đơn hàng, phiếu giảm giá (được lấy từ quy tắc bán hàng), và trang CMS. Mỗi loại có một ô kiểm, được đánh dấu tự động khi Spwig tìm thấy các mục để nhập và bị vô hiệu hóa khi con số là 0.

paragraph

Bạn cũng sẽ thấy một mẫu của năm sản phẩm đầu tiên để bạn kiểm tra tính hợp lý rằng các tiêu đề, giá cả và hình ảnh trông đúng trước khi cam kết thực hiện nhập toàn bộ.

paragraph

Dưới các con số, **Tùy chọn nhập** cho phép bạn kiểm soát cách nhập hoạt động:

list

paragraph

Nếu bạn cần thay đổi cách ánh xạ các trường cụ thể — thuộc tính tùy chỉnh, khớp danh mục, xử lý thuế hoặc vận chuyển — điều này được thực hiện ở bước 4, được đề cập trong [Ánh xạ trường di chuyển](migration-field-mapping). Nhấp **Tiếp theo** để tiếp tục đến bước ánh xạ, sau đó nhấp **Bắt đầu Di chuyển** sau khi bạn đã xem xét.

heading

## Thực hiện nhập

paragraph

Quá trình nhập được thực hiện ở phía sau — bạn có thể đóng cửa sổ và nó sẽ tiếp tục. Trang tiến độ hiển thị trạng thái trực tiếp cho từng loại dữ liệu (danh mục, sản phẩm, khách hàng, đơn hàng, đánh giá, phiếu giảm giá) với một nhật ký bạn có thể mở rộng để xem chi tiết.

paragraph

Sau khi hoàn tất, bạn sẽ đến trang tổng kết kết quả. Hãy xem qua [Sau khi di chuyển](after-migration-review) để kiểm tra những gì đã được chuyển, xử lý bất kỳ việc thay đổi liên kết nào cho nội dung tham chiếu đến các URL Magento cũ của bạn, và đảm bảo các cài đặt thuế và vận chuyển mà trình hướng dẫn thu thập nhưng không áp dụng tự động.

screenshots-needed

heading

## Hạn chót hoàn tác

paragraph

Magento là nền tảng duy nhất có giới hạn thời gian cho việc hoàn tác. Một khi quá trình di chuyển của bạn hoàn tất, nút **Hoàn tác** sẽ xuất hiện trên trang tổng kết công việc — nhưng đối với Magento cụ thể, nút này có thể ngừng được cung cấp sau một khoảng thời gian kể từ khi hoàn tất. Các loại di chuyển khác (WooCommerce, Shopify, CSV) không có hạn chót này, nhưng Magento thì có, vì vậy đừng để việc kiểm tra đến sau.

blockquote

> **Cảnh báo:** Hoàn tác xóa nhiều hơn những gì quá trình di chuyển đã tạo ra — bao gồm các đơn hàng được đặt bởi khách hàng đã di chuyển *sau* quá trình di chuyển, và các mục đơn hàng tham chiếu đến các sản phẩm đã di chuyển, ngay cả trên các đơn hàng từ những khách hàng bạn không di chuyển. Chỉ an toàn để sử dụng ngay sau khi di chuyển, trước khi có bất kỳ giao dịch thực tế nào xảy ra trên cửa hàng. Xem [Giải quyết sự cố di chuyển](migration-troubleshooting) để có cái nhìn toàn diện về những gì hoàn tác có thể và không thể đảo ngược.

paragraph

Kiểm tra dữ liệu đã nhập của bạn kịp thời, trong khi vẫn còn có thể hoàn tác, trong trường hợp bạn cần sử dụng nó.

heading

## Hủy tích hợp

paragraph

Sau khi bạn đã xác nhận dữ liệu của mình trong Spwig — sản phẩm, giá cả, hình ảnh, khách hàng, đơn hàng, phiếu giảm giá và các trang đều trông đúng — hãy quay lại **Hệ thống > Tích hợp** trong Magento, tìm `Spwig Migration`, và ngừng hoạt động hoặc xóa nó.

Token sẽ không cần thiết nữa trừ khi bạn có kế hoạch chạy lại migration, và việc xóa nó sẽ đóng lại một chứng nhận truy cập đọc mở mà bạn không còn cần nữa.

## Tips

- **Các đánh giá là điều bất ngờ lớn nhất đối với các nhà bán hàng Magento** — hãy lập kế hoạch xuất/nhập riêng nếu bạn đang dùng phiên bản Community và đánh giá quan trọng đối với cửa hàng của bạn.
- **Sao chép token truy cập ngay lập tức** — Magento chỉ hiển thị nó một lần khi bạn kích hoạt tích hợp; nếu bạn mất nó, bạn sẽ cần phải hủy kích hoạt và tạo lại tích hợp.
- **Đừng trì hoãn xác minh** — nút Rollback chỉ có sẵn trong thời gian giới hạn đối với Magento, khác với các nền tảng khác.
- **Sử dụng bản xem trước mẫu trong bước 3** để phát hiện các vấn đề ánh xạ rõ ràng (giá sai, thiếu hình ảnh) trước khi chạy toàn bộ import.
- **Các phiếu giảm giá đến từ các quy tắc bán hàng** — nếu phiếu giảm giá Magento phụ thuộc vào các điều kiện phức tạp, hãy kiểm tra nó trong Spwig sau đó vì không phải mọi loại quy tắc đều có tương đương trực tiếp.
- **Cấu hình thuế và khu vực vận chuyển trong Spwig sau khi import** — các tùy chọn thuế và vận chuyển của wizard được lưu lại nhưng không tự động áp dụng cho cửa hàng của bạn.