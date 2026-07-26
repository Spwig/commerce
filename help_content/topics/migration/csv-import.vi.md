---
title: Nhập khẩu từ Tệp CSV
---

Nhập khẩu CSV là phương pháp di chuyển dự phòng cho bất kỳ cửa hàng nào mà Spwig không kết nối trực tiếp. Nếu bạn đến từ BigCommerce, PrestaShop, Squarespace, Wix, một bảng tính bạn đã duy trì bằng tay, hoặc một hệ thống tùy chỉnh không có API mà Spwig hiểu, đây là nơi bạn sẽ đến — xuất dữ liệu của bạn thành tệp CSV và tải chúng lên tại đây thay vì kết nối trực tiếp.

Hướng dẫn này bao gồm khi nên sử dụng CSV thay vì kết nối API, những thứ mà CSV không thể chuyển, năm tệp liên quan, cách chuẩn bị chúng và cách ánh xạ cột hoạt động như thế nào.

## Khi Nên Sử Dụng CSV Thay Vì Kết Nối API

Spwig kết nối trực tiếp với WooCommerce, Shopify và Magento 2/Adobe Commerce — xem [Tổng quan Di chuyển Dữ liệu](migration-overview) cho các nền tảng này. Đối với bất kỳ nền tảng nào khác, CSV là lựa chọn duy nhất; không có tích hợp trực tiếp cho BigCommerce, PrestaShop, Squarespace hoặc Wix. Nó cũng là lựa chọn đúng nếu bạn đang hợp nhất dữ liệu từ một bảng tính, ngừng sử dụng một cửa hàng được xây dựng tùy chỉnh, hoặc muốn kiểm soát chính xác những gì được nhập bằng cách tự tạo tệp.

## Những Điều CSV Không Thể Làm Được

Trước khi chuẩn bị bất cứ thứ gì, hãy biết những thứ mà phương pháp này bỏ lại phía sau — đây là nguồn gây ngạc nhiên lớn nhất cho các nhà bán hàng sử dụng nhập khẩu CSV:

- **Không có hình ảnh sản phẩm.** Các sản phẩm được nhập khẩu không có hình ảnh đính kèm; hãy tải chúng lên sau.
- **Không có biến thể.** Mỗi sản phẩm được tạo như một sản phẩm đơn giản. Xây dựng lại cấu trúc kích thước/màu sắc/phong cách trong Spwig sau khi nhập khẩu.
- **Không có phiếu giảm giá.** Mã giảm giá và khuyến mãi không phải là phần của định dạng CSV.
- **Không có nội dung blog.** Không có tệp CSV cho các bài đăng hoặc bài viết.

Không có điều nào trong số này ngăn cản việc nhập khẩu — chỉ có nghĩa là sản phẩm cần được xử lý tiếp theo sau khi chúng đã có trong Spwig. Xem [Sau Khi Di Chuyển](after-migration-review) để có danh sách kiểm tra đầy đủ sau khi nhập khẩu.

## Năm Tệp

Bước CSV của wizard cung cấp năm đầu vào tệp, mỗi tệp đều có nút **Tải Xuống Mẫu**. Bắt đầu từ các mẫu này thay vì xây dựng tệp từ đầu — chúng đảm bảo tên cột đúng và cho phép phát hiện tự động thực hiện nhiều hơn trong bước 4.

| Tệp | Có yêu cầu không? |
|---|---|
| Sản phẩm | **Yêu cầu** |
| Danh mục | Tùy chọn |
| Khách hàng | Tùy chọn |
| Đơn hàng | Tùy chọn |
| Đánh giá | Tùy chọn |

Sản phẩm là tệp duy nhất mà Spwig yêu cầu — các tệp còn lại có thể để trống nếu bạn chưa có dữ liệu đó.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: csv-file-upload-step.webp
  description: Bước 2 với CSV được chọn, hiển thị năm đầu vào tệp và các nút Tải Xuống Mẫu của chúng
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

### Sản phẩm (Yêu cầu)

| Cột | Mô tả |
|---|---|
| `id` | Nhận dạng duy nhất trong dữ liệu nguồn của bạn; không hiển thị cho khách hàng. |
| `name` | Tiêu đề sản phẩm. **Quan trọng.** |
| `slug` | Phiên bản thân thiện với URL của tên; được tạo tự động từ `name` nếu trống. |
| `description` | Mô tả được hiển thị trên cửa hàng. |
| `price` | Giá bán lẻ của sản phẩm. **Quan trọng.** |
| `sku` | Đơn vị kiểm soát hàng tồn — được sử dụng để khớp khi **Bỏ qua các mục hiện có** được bật. |
| `stock_quantity` | Số lượng hiện có. |
| `category` | Tên danh mục mà sản phẩm thuộc về. Phải khớp với `name` trong tệp danh mục của bạn. |

### Danh mục

| Cột | Mô tả |
|---|---|
| `id` | Nhận dạng duy nhất trong dữ liệu nguồn của bạn. |
| `name` | Tên danh mục. **Quan trọng.** |
| `slug` | Phiên bản thân thiện với URL của tên; được tạo tự động nếu trống. |
| `description` | Văn bản mô tả danh mục. |
| `parent_id` | `id` của danh mục mẹ. Trống có nghĩa là cấp độ cao nhất. |

### Khách hàng

| Cột | Mô tả |
|---|---|
| `id` | Nhận dạng duy nhất trong dữ liệu nguồn của bạn. |
| `email` | Địa chỉ email của khách hàng. **Quan trọng** — liên kết đơn hàng và đánh giá với khách hàng đúng. |
| `first_name` | Tên riêng của khách hàng. |
| `last_name` | Họ của khách hàng. |
| `phone` | Số điện thoại của khách hàng. |

### Đơn hàng

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

| Column | Description |
|---|---|
| `id` | Unique identifier in your source data. |
| `customer_email` | Email of the customer who placed the order. **Essential** — links the order to a customer record. |
| `order_date` | The date the order was placed. |
| `status` | The order's status (e.g. completed, processing). |
| `total` | The order total. **Essential.** |
| `currency` | Currency code for the order total. |

### Reviews (Optional)

| Column | Description |
|---|---|
| `id` | Unique identifier in your source data. |
| `product_id` | The `id` of the product being reviewed, matching your products file. **Essential** — links the review to the right product. |
| `customer_email` | Email address of the reviewer. |
| `rating` | The star rating given. |
| `comment` | The review text. |
| `date` | The date the review was posted. |

## Chuẩn bị tệp của bạn

- **Lưu dưới dạng UTF-8** để tránh các ký tự có dấu bị lỗi, đặc biệt là từ một mã hóa nguồn khác.
- **Đánh dấu các trường chứa dấu phẩy** — bọc một mô tả hoặc tên chứa dấu phẩy trong dấu ngoặc kép để tránh bị hiểu sai là dấu phân cách cột.
- **Bao gồm hàng tiêu đề.** Hàng đầu tiên phải chứa tên các cột của bạn — một tệp không có hàng tiêu đề sẽ bị từ chối.
- **Xây dựng phân cấp danh mục bằng `parent_id`.** Gán cho mỗi danh mục một `id` duy nhất, sau đó đặt `parent_id` của danh mục con thành `id` của danh mục cha. Trống có nghĩa là cấp độ cao nhất.
- **Liên kết đơn hàng với khách hàng bằng `customer_email`**, khớp với cột `email` trong tệp khách hàng của bạn (hoặc tạo một bản ghi khách hàng ẩn danh), thay vì dựa vào các số ID nội bộ, vì chúng hiếm khi khớp với nhau trên các nền tảng khác nhau.
- **Liên kết đánh giá với sản phẩm bằng `product_id`**, khớp với giá trị trong cột `id` của tệp sản phẩm của bạn, hoặc đánh giá đó sẽ bị bỏ qua.

## Ánh xạ cột trong bước 4

Bước 4 hiển thị bảng ánh xạ cột CSV. Spwig quét các tiêu đề và tự động phát hiện các khớp có thể với danh sách các biệt danh phổ biến — ví dụ, trường `sku` cũng khớp với `barcode`, `part_number`, hoặc `item_number`. Các tiêu đề được xuất trực tiếp từ nền tảng khác thường ánh xạ chính xác mà không cần làm việc thủ công.

Đối với mỗi cột, bạn có thể chấp nhận dự đoán tự động, ghi đè bằng cách chọn một trường đích khác, hoặc chọn "— Bỏ qua cột này —" để loại bỏ nó. Các ánh xạ được lưu và sử dụng lại trong các lần di chuyển CSV tiếp theo. Xem [Ánh xạ trường di chuyển](migration-field-mapping) để có cái nhìn toàn diện về bước 4, bao gồm ánh xạ trường tự động, ánh xạ danh mục và các tùy chọn thuế/vận chuyển.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: Step 4 CSV Column Mapping panel showing auto-detected mappings with override dropdowns
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Các lỗi phổ biến và ý nghĩa của chúng

| Lỗi | Ý nghĩa |
|---|---|
| `Products CSV is required.` | Bạn đã cố gắng tiếp tục mà không tải lên tệp sản phẩm. Đây là tệp duy nhất mà Spwig yêu cầu — tải lên một tệp để tiếp tục. |
| `{Type} CSV has no headers.` | Hàng đầu tiên của tệp có tên không có nội dung hoặc bị thiếu. Thêm hàng tiêu đề chứa tên các cột và tải lên lại. |
| `{Type} CSV could not be read: ...` | Spwig không thể phân tích tệp có tên — thường là tệp bị hỏng, mã hóa sai, hoặc tệp không thực sự là CSV mặc dù có phần mở rộng. Tải lại sau khi xuất lại và xác nhận tệp mở được một cách rõ ràng. |

## Chạy quá trình nhập

Sau khi xác nhận ánh xạ, bắt đầu di chuyển từ bước 5. Nó chạy ở chế độ nền, vì vậy bạn có thể đóng cửa sổ — tiến độ và nhật ký trực tiếp có sẵn nếu bạn kiểm tra lại trước khi hoàn tất. Xem [Sau khi di chuyển](after-migration-review) để kiểm tra kết quả.

Hãy nhớ rằng việc nhập CSV cụ thể để lại **hình ảnh sản phẩm** và **biến thể** cho bạn hoàn thành bằng tay — cả hai đều không được chuyển tự động, bất kể tệp của bạn hoàn chỉnh đến đâu.

## Một số mẹo

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- **Bắt đầu từ nút Tải xuống Mẫu cho từng tệp** — điều này giúp bạn tránh được lỗi chính tả tên cột mà nếu không, chúng sẽ bị bỏ sót và phải ánh xạ thủ công.
- **Sửa lỗi không khớp `product_id` trước khi tải lên đánh giá** — một đánh giá có `product_id` không khớp với bất kỳ `id` nào của sản phẩm sẽ không có gì để gắn vào và sẽ bị bỏ qua.
- **Đừng đổi tên các tiêu đề từ tệp xuất của nền tảng khác** — việc phát hiện tự động thường nhận ra chúng như là, thông qua các biệt danh, vì vậy có thể không cần ánh xạ thủ công gì cả.
- **Dành thời gian cho hình ảnh và biến thể ngay sau khi nhập** — đây là hai thứ mà CSV không thể chuyển qua, và rất dễ quên đến khi khách hàng nhận thấy một trang sản phẩm trống.
- **Sử dụng `parent_id` để mô hình hóa các danh mục nhiều cấp** — chỉ định `parent_id` của một danh mục con đến `id` của danh mục cha để lồng nó vào; để trống nếu là cấp cao nhất.
- **Xuất lại và kiểm tra lại khi gặp lỗi "could not be read"** — hầu như luôn là lỗi mã hóa hoặc hỏng tệp nguồn, chứ không phải điều gì cần sửa trong Spwig.