---
title: Di chuyển từ WooCommerce
---

Nếu cửa hàng của bạn hiện đang chạy trên WooCommerce, công cụ di chuyển của Spwig có thể nhập sản phẩm, khách hàng, đơn hàng và nội dung trực tiếp qua REST API của WooCommerce. Hướng dẫn này bao gồm việc lấy thông tin xác thực API, chạy quá trình nhập, và hai tính năng đặc biệt của WooCommerce mà bạn nên biết trước: plugin Di chuyển (Migration) Bridge tùy chọn để nhập dữ liệu liên kết, và hỗ trợ tích hợp cho một số tiện ích mở rộng phổ biến của WooCommerce.

## Trước khi bắt đầu

WooCommerce có hỗ trợ rộng nhất trong số các nền tảng nguồn trong công cụ di chuyển. Các mục sau sẽ được nhập một cách rõ ràng: danh mục (bao gồm phân cấp), sản phẩm, hình ảnh và biến thể, khách hàng và địa chỉ, đơn hàng, đánh giá, phiếu giảm giá, và bài viết blog cùng với danh mục, thẻ và hình ảnh của chúng.

Thông tin hồ sơ liên kết, bản ghi hoa hồng và lịch sử thanh toán cũng có thể được nhập, nhưng chỉ khi bạn cài đặt plugin Spwig Migration Bridge trước — xem bên dưới. Nếu không, dữ liệu đó sẽ bị bỏ qua.

Bạn cũng cần lưu ý:

- Sản phẩm từ một số tiện ích mở rộng WooCommerce (ký gửi, gói, đặt chỗ, thẻ quà tặng) sẽ được đưa vào tính năng tương ứng của Spwig, nhưng không phải mọi chi tiết đều được chuyển — xem **Hỗ trợ tiện ích mở rộng WooCommerce** bên dưới.
- Các trường tùy chỉnh trên sản phẩm, khách hàng và đơn hàng của bạn sẽ được phát hiện tự động và cần được ánh xạ trong bước sau. Xem [Ánh xạ trường di chuyển](migration-field-mapping).
- Các tùy chọn **Nhập cài đặt thuế** và **Nhập khu vực vận chuyển và phương thức** của công cụ không được áp dụng cho dữ liệu đã nhập. Bạn cần tự thiết lập tỷ lệ thuế và vận chuyển trong Spwig sau đó — xem [Sau khi di chuyển](after-migration-review).
- Tùy chọn **Điều chỉnh giá** trên cùng một bước *sẽ* có hiệu lực cho việc nhập từ WooCommerce, thay đổi giá cơ bản của mỗi sản phẩm khi nó được tạo. Chỉ để nó ở **Không** trừ khi bạn cố ý muốn thay đổi tất cả giá.

Hãy chuẩn bị sẵn thông tin đăng nhập quản trị WordPress của bạn, và biết rõ số lượng sản phẩm, khách hàng và đơn hàng bạn đang nhập để bạn có thể kiểm tra lại các con số mà công cụ hiển thị.

## Lấy thông tin xác thực REST API

Spwig kết nối với WooCommerce bằng một khóa API REST được tạo từ quản trị WordPress của bạn. Khóa này chỉ cần **Đọc** — Spwig chỉ đọc từ cửa hàng của bạn trong quá trình di chuyển, nó không bao giờ ghi lại bất cứ thứ gì.

1. Trong WordPress, đi đến **WooCommerce > Cài đặt > Nâng cao > REST API**
2. Nhấp vào **Thêm khóa**
3. Đặt tên cho nó (ví dụ, `Spwig Migration`) và đặt **Quyền** thành **Đọc**
4. Nhấp vào **Tạo khóa API**
5. Sao chép **Khóa Người tiêu dùng** (`ck_...`) và **Bí mật Người tiêu dùng** (`cs_...`) vào một nơi an toàn

> **Lưu ý quan trọng:** WooCommerce chỉ hiển thị Bí mật Người tiêu dùng một lần, vào thời điểm bạn tạo nó. Nếu bạn rời khỏi trang trước khi sao chép nó, bạn sẽ cần tạo một khóa mới.

## Kết nối cửa hàng của bạn

Đi đến **Nhập/Xuất dữ liệu > Bắt đầu di chuyển mới** trong quản trị Spwig và chọn **WooCommerce** ở bước 1. Ở bước 2, nhập:

- **URL Cửa hàng** — địa chỉ web đầy đủ của cửa hàng bạn, ví dụ `https://mystore.com`
- **Khóa Người tiêu dùng** và **Bí mật Người tiêu dùng** — các giá trị bạn vừa sao chép

Giữ tùy chọn **Kiểm tra kết nối trước khi tiếp tục** được chọn (mặc định là bật) để Spwig xác nhận rằng nó có thể kết nối với cửa hàng và xác thực trước khi bạn tiếp tục — điều này giúp phát hiện lỗi chính tả và vấn đề quyền truy cập ngay lập tức thay vì ở giữa quá trình nhập. Nhấp **Tiếp theo** một lần khi nó thành công.

## Xem xét và chọn dữ liệu

Bước 3 sẽ lấy các con số sống từ cửa hàng của bạn — danh mục, sản phẩm, khách hàng, đơn hàng, đánh giá và phiếu giảm giá — cùng với một mẫu của năm sản phẩm đầu tiên để bạn có thể xác nhận rằng nó đang đọc từ trang web đúng. Mỗi hộp kiểm của loại dữ liệu sẽ được chọn tự động khi con số của nó lớn hơn 0, và bị vô hiệu hóa khi bằng 0.

**Tùy chọn nhập**:

- **Bỏ qua các mục hiện có** (bật) — so sánh các bản ghi mới với những gì đã có trong Spwig (SKU cho sản phẩm, email cho khách hàng) và bỏ qua các bản sao.



Hãy để nó bật trừ khi bạn đang bắt đầu từ một cửa hàng trống.
- **Nhập hình ảnh sản phẩm** (bật) — chậm hơn, nhưng đáng giá.
- **Giữ nguyên ID gốc khi có thể** (tắt) — công cụ hướng dẫn tự động ghi chú rằng điều này "không được khuyến khích". Hãy để nó tắt trừ khi bạn có lý do kỹ thuật cụ thể để giữ các ID số của WooCommerce.
- **Kích thước lô** — 10, 25 (mặc định), 50 hoặc 100 bản ghi tại một thời điểm.

Các lô nhỏ phù hợp với kết nối không ổn định; các lô lớn hoàn tất nhanh hơn trên kết nối ổn định.

## Plugin Cầu nối Di chuyển Spwig

WooCommerce không có khái niệm tích hợp sẵn về chương trình đại lý, vì vậy nếu bạn đang chạy một chương trình đại lý thông qua một phần mở rộng WooCommerce, dữ liệu đó nằm trong các bảng mà API REST tiêu chuẩn không thể nhìn thấy. Plugin **Cầu nối Di chuyển Spwig** là một plugin phụ trợ nhỏ mà bạn cài đặt trên trang WordPress của mình để mở rộng tính năng này.

Plugin Cầu nối mở khóa:

- **Hồ sơ đại lý** — chi tiết đại lý và mã giới thiệu của họ
- **Lịch sử hoa hồng** — lịch sử hoa hồng liên quan đến từng đại lý
- **Lịch sử thanh toán** — các khoản thanh toán đã thực hiện cho các đại lý

Đây hoàn toàn là tùy chọn — bỏ qua nó nếu bạn không chạy chương trình đại lý hoặc không cần lịch sử đó trong Spwig.

> **Lưu ý:** Dữ liệu đại lý chỉ có thể được nhập nếu đơn hàng và khách hàng cũng được nhập trong cùng một lần di chuyển, vì các khoản hoa hồng và thanh toán liên quan đến các đơn hàng và khách hàng cụ thể.

Để cài đặt nó:

1. Ở bước 3, nếu plugin chưa được phát hiện trên trang web của bạn, bạn sẽ thấy nút **Tải xuống Plugin Cầu nối** cùng với hướng dẫn cài đặt
2. Tải xuống plugin ZIP
3. Trong WordPress, vào **Plugins > Add New > Upload Plugin**, chọn ZIP, nhấp **Install Now**, sau đó **Activate**
4. Trở lại hướng dẫn Spwig và làm tươi trang — một ô kiểm **Affiliates** và một khối **Affiliate Program Data** sẽ xuất hiện, hiển thị số lượng được tìm thấy

Bạn có thể gỡ cài đặt và xóa plugin Cầu nối khỏi WordPress sau khi hoàn tất di chuyển.

## Hỗ trợ phần mở rộng WooCommerce

Nếu cửa hàng của bạn sử dụng các phần mở rộng phổ biến nhất, các sản phẩm mà chúng tạo ra được nhận diện trong quá trình nhập và được ánh xạ vào tính năng Spwig tương ứng thay vì được nhập như các sản phẩm bình thường:

| Phần mở rộng WooCommerce | Đến nơi nào |
|---|---|
| Subscriptions | Kế hoạch đăng ký Spwig |
| Product Add-Ons | Phụ kiện sản phẩm Spwig |
| Product Bundles | Gói sản phẩm Spwig |
| Thẻ quà tặng (WooCommerce, YITH và PW) | Thẻ quà tặng Spwig |
| Composite Products | Sản phẩm tổng hợp Spwig |
| Bookings and Accommodation Bookings | Đặt chỗ Spwig |

> **Lưu ý:** Việc nhập dữ liệu phần mở rộng sẽ không bao giờ chặn việc tạo sản phẩm cơ bản. Nếu dữ liệu cụ thể của phần mở rộng không thể đọc được, sản phẩm vẫn sẽ được nhập — chỉ như một sản phẩm bình thường, không có cài đặt đăng ký, gói, đặt chỗ hoặc thẻ quà tặng.

Kiểm tra ngẫu nhiên các sản phẩm đăng ký, gói, đặt chỗ và thẻ quà tặng của bạn sau khi nhập để xác nhận các cài đặt cụ thể của phần mở rộng đã được chuyển, thay vì giả định rằng một lần nhập thành công đã mang theo mọi chi tiết.

## Các trường tùy chỉnh

Nếu bạn đã thêm các trường meta tùy chỉnh vào sản phẩm, khách hàng hoặc đơn hàng WooCommerce của mình, Spwig sẽ lấy mẫu khoảng mười bản ghi của mỗi loại để phát hiện các trường nào tồn tại. Bạn sẽ ánh xạ từng trường đó đến một vị trí trường tùy chỉnh của Spwig hoặc một trường Meta Data chung ở bước 4. Xem [Ánh xạ trường di chuyển](migration-field-mapping) để có hướng dẫn đầy đủ, bao gồm cách lưu ánh xạ cho các lần di chuyển trong tương lai.

## Chạy quá trình nhập

Sau khi bạn đã xem xét bước 3 và xác nhận ánh xạ của bạn ở bước 4, hãy bắt đầu nhập. Nó chạy ở chế độ nền — bạn có thể đóng cửa sổ trình duyệt và nó vẫn tiếp tục. Bước 5 hiển thị tiến trình trực tiếp với một hàng cho mỗi loại dữ liệu (danh mục, sản phẩm, khách hàng, đơn hàng, đánh giá, phiếu giảm giá, bài viết blog và đại lý/hoa hồng/thanh toán nếu plugin Cầu nối được sử dụng) cùng với nhật ký hoạt động có thể mở rộng.

Bước 6 hiển thị kết quả của bạn: những gì đã được nhập, bỏ qua hoặc thất bại, cùng với công cụ **Viết lại Liên kết** nếu các liên kết nội bộ đến miền WooCommerce cũ của bạn được tìm thấy trong nội dung đã nhập.

Kiểm tra kỹ tóm tắt, sau đó làm theo danh sách kiểm tra trong [Sau khi Di chuyển](after-migration-review) — nó bao gồm việc xác minh dữ liệu của bạn, thiết lập thuế và vận chuyển (điều mà trình hướng dẫn không cấu hình cho bạn), và viết lại các liên kết nội bộ.

## Hủy Giao quyền Khóa API

Sau khi bạn đã xác nhận việc di chuyển hoàn tất thành công, quay lại **WooCommerce > Settings > Advanced > REST API** trong WordPress và hủy hoặc xóa khóa bạn đã tạo cho Spwig. Không có lý do gì để để lại một khóa API hoạt động trên cửa hàng cũ của bạn sau khi bạn đã hoàn tất.

## Mẹo

- **Tạo khóa API ngay trước khi bạn cần nó** — vì mật khẩu Người tiêu dùng chỉ được hiển thị một lần, hãy tạo nó ngay trước khi bắt đầu bước 2 thay vì tạo trước.
- **Chỉ đọc là đủ** — không bao giờ cấp quyền Viết hoặc Đọc/Viết; Spwig chỉ bao giờ đọc từ cửa hàng WooCommerce của bạn.
- **Cài đặt plugin Bridge trước khi bắt đầu nhập** — bạn sẽ cần thêm nó và làm mới trình hướng dẫn trước khi nhập, vì vậy hãy kiểm tra xem có nó không trước khi bắt đầu thay vì trong quá trình thực hiện.
- **Kiểm tra sơ bộ các sản phẩm được hỗ trợ bởi tiện ích mở rộng** — các sản phẩm đăng ký, gói, đặt chỗ và thẻ quà tặng là những sản phẩm có khả năng cần kiểm tra thủ công sau khi nhập.
- **Một lần nhập một phần không được làm sạch tự động** — xem [Giải quyết Vấn đề Di chuyển](migration-troubleshooting) trước khi thử lại lần nhập đã thất bại.
- **Hủy khóa API khi bạn đã xong** — đừng để các tích hợp cũ hoạt động trên một cửa hàng bạn đã di chuyển khỏi.