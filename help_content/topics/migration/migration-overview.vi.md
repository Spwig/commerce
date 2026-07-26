---
title: Tổng quan về di chuyển dữ liệu
---

Nếu sản phẩm, khách hàng và đơn hàng của bạn hiện đang lưu trữ trên WooCommerce, Shopify hoặc Magento — hoặc chỉ là một vài tệp CSV — công cụ di chuyển dữ liệu sẽ đưa dữ liệu đó vào cửa hàng Spwig mới của bạn, giúp bạn không cần nhập lại bằng tay. Nó xử lý các danh mục, sản phẩm, khách hàng, đơn hàng, đánh giá và phiếu giảm giá, và đối với WooCommerce, nó cũng có thể chuyển nội dung blog và, với plugin cầu nối, chương trình liên kết của bạn.

Tìm nó trong thanh bên quản trị dưới mục **Bảng điều khiển hệ thống > Nhập/xuất dữ liệu** (hiển thị cho người dùng cấp siêu quản trị trên cài đặt tự chủ; nếu bạn không thấy nó, hãy hỏi người quản lý cài đặt của bạn). Trang này có tiêu đề **Nhập và Xuất dữ liệu**, liệt kê mọi lần di chuyển bạn đã bắt đầu với các thẻ thống kê cho Tổng số lần di chuyển, Đã hoàn thành, Đang thực hiện và Thất bại, cùng với các nút **Bắt đầu di chuyển mới**, **Xem nhật ký** và **Ánh xạ trường**. Các lần di chuyển chỉ có thể được tạo thông qua hướng dẫn.

## Các nền tảng được hỗ trợ

Spwig kết nối trực tiếp với ba nền tảng, cùng với các tệp CSV thuần túy:

- **WooCommerce** — con đường đầy đủ nhất; dữ liệu mở rộng (ký gửi, gói, thẻ quà tặng, đặt chỗ) và chương trình liên kết của bạn cũng có thể được chuyển.
- **Shopify** — kết nối thông qua ứng dụng tùy chỉnh bạn tạo trong bảng điều khiển nhà phát triển Shopify của bạn.
- **Magento 2** — kết nối thông qua mã token tích hợp từ bảng điều khiển Magento của bạn.
- **Tệp CSV** — năm tệp riêng biệt (sản phẩm, danh mục, khách hàng, đơn hàng, đánh giá), cho các nền tảng khác hoặc dữ liệu được chuẩn bị thủ công.

> **Lưu ý:** BigCommerce, PrestaShop, Squarespace và Wix không được hỗ trợ kết nối trực tiếp. Nếu bạn đang di chuyển từ một trong những nền tảng này, hãy xuất danh mục và dữ liệu khách hàng của bạn thành tệp CSV và sử dụng đường dẫn CSV thay vào đó — xem [Nhập từ tệp CSV](csv-import).

## Những gì được chuyển, theo nền tảng

Mức độ bao phủ thay đổi theo nền tảng — hãy kiểm tra bảng này với cửa hàng của bạn trước khi cam kết ngày ra mắt.

| Dữ liệu | WooCommerce | Shopify | Magento 2 | CSV |
|---|---|---|---|---|
| Danh mục | Có, với cấu trúc phân cấp | Có, dưới dạng Tập hợp (phẳng) | Có | Có |
| Sản phẩm | Có | Có | Có | Có (tệp bắt buộc) |
| Hình ảnh sản phẩm | Có | Có | Có | Không |
| Biến thể | Có | Có | Có | Không |
| Khách hàng + địa chỉ | Có | Có | Có | Có |
| Đơn hàng | Có | Có, chỉ 60 ngày gần nhất trừ khi thêm phạm vi `read_all_orders` | Có | Có |
| Đánh giá | Có | Không được hỗ trợ hoàn toàn | Thường không khả dụng — Magento Community không có điểm cuối REST cho đánh giá | Có |
| Phiếu giảm giá / khuyến mãi | Có | Có | Có | Không |
| Nội dung blog / CMS | Có (bài viết, danh mục, thẻ, hình ảnh) | Có (bài viết) | Có (trang CMS) | Không |
| Liên kết, hoa hồng, thanh toán | Có, yêu cầu plugin Spwig Migration Bridge | Không | Không | Không |
| Phát hiện trường tùy chỉnh | Có | Không — các trường meta của Shopify không được đọc | Không | n/a |

Các nhà bán hàng Shopify nên lên kế hoạch nhập lại bất kỳ dữ liệu metafield nào (thông số kỹ thuật sản phẩm tùy chỉnh, trường khách hàng bổ sung) thủ công sau khi nhập, vì nó không được phát hiện hoặc chuyển. Đối với mọi thứ khác, xem [Ánh xạ trường di chuyển](migration-field-mapping) để biết cách các trường nguồn ánh xạ với các trường Spwig.

## Lên kế hoạch di chuyển của bạn

- **Di chuyển trước khi ra mắt**, trên một cài đặt Spwig chưa xử lý lưu lượng truy cập thực tế, trước khi hướng dẫn tên miền của bạn đến nó — như vậy bạn có thể xem xét và sửa chữa mọi thứ mà không có khách hàng nhìn thấy một danh mục chưa hoàn chỉnh.
- **Giữ cửa hàng cũ hoạt động, chỉ đọc**, cho đến khi bạn xác nhận bản sao Spwig là chính xác.
- **Dự trù thời gian cho thiết lập thuế và vận chuyển sau đó** — các cài đặt của hướng dẫn cho điều này trông giống như chúng sẽ nhập các mức giá và khu vực của bạn, nhưng chúng không được áp dụng (xem [Ánh xạ trường di chuyển](migration-field-mapping)). Cấu hình **Cài đặt > Thuế và Tiền tệ** và **Cài đặt > Vận chuyển** bằng tay.
- **Kiểm tra ngẫu nhiên thay vì lướt qua** — dữ liệu mở rộng được nhập theo cách tốt nhất có thể; một sản phẩm mà dữ liệu mở rộng của nó không thể được đọc vẫn được tạo, chỉ không có dữ liệu mở rộng đó. Xem [Sau khi di chuyển](after-migration-review) trước khi công bố bất cứ điều gì cho khách hàng.

- **Truy cập quản trị đến nền tảng nguồn của bạn** để tạo thông tin xác thực API — một khóa API REST trong WooCommerce, một ứng dụng tùy chỉnh trong Shopify, hoặc một token tích hợp trong Magento.

Không cần cho CSV.
- **Phạm vi chỉ đọc** ở mọi nơi nền tảng nguồn cung cấp — Spwig chỉ đọc từ cửa hàng cũ của bạn, không bao giờ ghi lại vào nó.
- **Ngân sách thời gian** — mỗi lần chạy có giới hạn cứng 4 giờ.

Đối với một cửa hàng lớn, hãy lập kế hoạch theo từng giai đoạn (loại sản phẩm và sản phẩm trước, đơn hàng sau) thay vì một lần chạy duy nhất.

> **Quan trọng:** Spwig không mã hóa thông tin xác thực API mà bạn nhập vào wizard. Sau khi xác nhận quá trình di chuyển đã hoàn tất, hãy hủy hoặc xóa thông tin xác thực trên nền tảng nguồn.

## Wizard di chuyển, từng bước

Wizard có sáu bước, với tiến trình được lưu giữa các bước:

1. **Nền tảng** — chọn WooCommerce, Shopify, Magento hoặc Nhập khẩu CSV.
2. **Kết nối** — nhập thông tin xác thực, với tùy chọn (mặc định bật) để kiểm tra kết nối trước. Các hướng dẫn cụ thể cho nền tảng sẽ hướng dẫn bạn chính xác điều cần tạo.
3. **Xem trước** — số liệu sống từ cửa hàng nguồn của bạn, một mẫu của 5 sản phẩm đầu tiên, và các hộp kiểm chọn loại dữ liệu nào cần bao gồm cùng các tùy chọn như kích thước lô.
4. **Ánh xạ** — cách các trường nguồn ánh xạ lên các trường Spwig, bất kỳ trường tùy chỉnh nào trong WooCommerce và các danh mục không có sự khớp rõ ràng. Chi tiết đầy đủ trong [Ánh xạ Trường Di chuyển](migration-field-mapping).
5. **Nhập** — chạy trong nền sau lưng; bạn có thể đóng tab và nó vẫn tiếp tục, với nhật ký trực tiếp.
6. **Hoàn tất** — tóm tắt kết quả, công cụ đổi liên kết cho nội dung tham chiếu đến miền cũ của bạn, và tải xuống báo cáo PDF/CSV.

## Sau khi di chuyển của bạn

Một lần nhập thành công không phải là vạch đích — xem [Sau khi Di chuyển](after-migration-review) để có danh sách kiểm tra đầy đủ bao gồm xác minh dữ liệu, sửa các liên kết nội bộ vẫn trỏ đến miền cũ của bạn, và cấu hình thuế và vận chuyển mà wizard không xử lý cho bạn.

## Quay lại không phải là tấm lưới an toàn

Hiểu điều này trước khi bạn bắt đầu, không phải sau khi điều gì đó đi sai. Quay lại tồn tại, nhưng nó không phải là nút hủy bỏ như có thể nghe:

- Không có việc quay lại tự động nếu việc nhập thất bại một phần. Những gì đã được nhập trước khi xảy ra sự cố sẽ vẫn tồn tại trong cửa hàng của bạn, và một lần nhập thất bại không thể được quay lại từ bảng điều khiển — bạn sẽ cần xem xét và dọn dẹp dữ liệu không đầy đủ bằng tay.
- Một lần di chuyển đã hoàn tất có thể được quay lại, và việc quay lại chỉ xóa những gì chính lần nhập đã tạo ra — không bao giờ nhiều hơn. Một khách hàng đã di chuyển và đã đặt một đơn hàng thực sự kể từ khi nhập vẫn giữ được tài khoản, địa chỉ, lịch sử tích điểm và tín dụng cửa hàng của họ, và đơn hàng thực đó được giữ nguyên không bị động đến; chỉ những đơn hàng do lần nhập tạo ra mới bị xóa. Một sản phẩm đã di chuyển vẫn được tham chiếu bởi bất kỳ đơn hàng, gói, thẻ quà tặng hoặc vị trí cấu hình nào cũng được giữ lại, và các đơn hàng thuộc về khách hàng khác không bao giờ bị thay đổi.
- Các liên kết, hoa hồng và khoản thanh toán do lần nhập tạo ra sẽ bị xóa, cùng với bất kỳ tài khoản liên kết nào mà lần nhập đã tạo ra — một liên kết gắn với một khách hàng đã tồn tại từ trước vẫn giữ được tài khoản của họ, và chỉ bản ghi liên kết bị xóa. Các gói đăng ký, mức giá và tài nguyên đặt chỗ do các tiện ích mở rộng của cửa hàng tạo ra vẫn không bị xóa — hãy tự dọn dẹp những thứ này bằng tay.
- Trước khi bạn xác nhận, Spwig sẽ hiển thị bản xem trước chính xác những gì sẽ bị xóa và những gì sẽ được giữ lại, theo tên và số lượng, kèm theo lý do — được tính toán dựa trên dữ liệu trực tiếp của bạn. Hãy đọc kỹ trước khi xác nhận. Sau đó, việc quay lại sẽ chạy trong nền, vì vậy bạn có thể đóng tab một cách an toàn; hãy kiểm tra tóm tắt của lần di chuyển để xem báo cáo khi nó hoàn tất.
- Việc quay lại vẫn là một hành động vĩnh viễn, mang tính phá hủy đối với các bản ghi mà nó thực sự xóa, vì vậy hãy sử dụng nó một cách có chủ đích — và tự dọn dẹp bằng tay bất cứ thứ gì Spwig giữ lại mà bạn thực sự không muốn. Nhưng vì nó không còn vượt ra ngoài những gì lần nhập đã tạo ra, nó không còn là một công cụ chỉ dùng trong ngày như trước đây.
- Nút Quay lại vẫn khả dụng trên tóm tắt của một lần di chuyển đã hoàn tất miễn là bản ghi công việc còn tồn tại, và nó sẽ được cung cấp lại nếu chính một lần thử quay lại thất bại giữa chừng, để bạn có thể thử lại. Các bản ghi không bị xóa theo bất kỳ lịch trình nào, vì vậy điều này không tự hết hạn.

Nếu bạn gặp phải lần di chuyển thất bại hoặc bị kẹt, [Giải quyết Vấn đề Di chuyển](migration-troubleshooting) bao gồm việc thử lại, hủy bỏ và đọc nhật ký.

## Tips

- **Bắt đầu bằng một lần chạy thử nhỏ** — các danh mục cộng với một vài sản phẩm sẽ xác nhận việc ánh xạ trường trông đúng trước khi thực hiện toàn bộ danh mục.
- **Đọc hướng dẫn riêng cho nền tảng trước** — [Migrating from WooCommerce](migrate-from-woocommerce), [Migrating from Shopify](migrate-from-shopify), và [Migrating from Magento](migrate-from-magento) sẽ đề cập chính xác các thông tin xác thực và phạm vi mà bạn cần.
- **Đừng bỏ qua bảng ma trận khả năng ở trên** — việc biết trước về các đánh giá Shopify hoặc các biến thể CSV sẽ giúp bạn tránh bất ngờ sau khi đã chuyển đổi DNS.
- **Giữ giao diện quản trị nền tảng nguồn mở trong một tab khác** để tạo hoặc sao chép thông tin xác thực khi cần.
- **Xử lý các hộp kiểm của wizard một cách nghiêm túc** — nếu một cài đặt không được mô tả là hoạt động ở đây, hãy cấu hình nó trực tiếp trên Spwig thay vì tin tưởng vào wizard.