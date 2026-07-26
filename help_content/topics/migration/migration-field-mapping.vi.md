---
title: Ánh xạ Trường Di chuyển
---

Mỗi nền tảng đều đặt tên cho các thứ một chút khác nhau — `regular_price` của WooCommerce không phải là `price` của Shopify, và một cột CSV được gọi là `barcode` có thể chính xác là cùng một thứ mà Spwig kỳ vọng thấy được dán nhãn là `sku`. Bước 4 của hướng dẫn di chuyển, **Cấu hình Ánh xạ Trường**, là nơi bạn kiểm tra cách dữ liệu nguồn của bạn sẽ được đưa vào Spwig trước khi thực sự chạy quá trình nhập. Chủ đề này bao gồm mọi khối trên trang đó và áp dụng cho các di chuyển WooCommerce, Shopify, Magento và CSV, với sự khác biệt theo nền tảng được nêu ra khi cần thiết. Để biết thông tin về tài khoản và các bước hướng dẫn trước đó, xem [Di chuyển từ WooCommerce](migrate-from-woocommerce) hoặc hướng dẫn tương ứng cho nền tảng của bạn.

## Ánh xạ Tự động

Khối này hiển thị, cho mỗi loại dữ liệu bạn đã chọn ở bước 3, một danh sách chỉ đọc của các trường nguồn và trường Spwig mà mỗi trường đó sẽ được đưa vào — ví dụ như trường `name` của sản phẩm ánh xạ đến tiêu đề sản phẩm của Spwig, hoặc trường `email` của khách hàng ánh xạ đến email tài khoản. Chỉ các loại dữ liệu mà bạn đang thực sự nhập sẽ xuất hiện ở đây; nếu bạn không chọn Đánh giá ở bước 3, sẽ không có phần Đánh giá trên trang này.

Vì các hàng này là chỉ đọc, không có gì để cấu hình — chúng tồn tại để bạn kiểm tra lại ánh xạ trước khi cam kết thực hiện nhập. Nếu một ánh xạ trông không đúng với dữ liệu của bạn, không có cách nào để ghi đè nó từ màn hình này; tùy chọn của bạn là sửa dữ liệu nguồn trước khi di chuyển, hoặc sửa các bản ghi bị ảnh hưởng trong Spwig sau khi nhập hoàn tất.

## Ánh xạ Cột CSV

Khối này chỉ xuất hiện cho các di chuyển CSV, với một bảng cho mỗi tệp bạn đã tải lên. Spwig tự động phát hiện các khớp có khả năng cao từ các tiêu đề cột của bạn — ví dụ, ánh xạ `sku` cũng nhận ra các tiêu đề như `barcode`, `part_number`, hoặc `item_number` — vì vậy trong hầu hết các trường hợp, bạn sẽ không cần phải thay đổi bất cứ thứ gì ở đây.

Mỗi cột CSV sẽ có một danh sách thả xuống liệt kê các trường mà Spwig kỳ vọng cho loại tệp đó:

- **products** — `id, name, slug, description, price, sku, stock_quantity, category`
- **categories** — `id, name, slug, description, parent_id`
- **customers** — `id, email, first_name, last_name, phone`
- **orders** — `id, customer_email, order_date, status, total, currency`
- **reviews** — `id, product_id, customer_email, rating, comment, date`

Mỗi danh sách thả xuống cũng bao gồm **— Bỏ qua cột này —**, điều này sẽ loại bỏ cột đó khỏi quá trình nhập hoàn toàn. Ghi đè ánh xạ tự phát hiện khi tiêu đề của bạn sử dụng quy tắc đặt tên mà Spwig không nhận ra, hoặc khi một cột thực sự không tương ứng với bất cứ thứ gì Spwig nhập (ví dụ như một trường ghi chú nội bộ) — hãy chọn Bỏ qua thay vì ép nó vào trường gần nhất có sẵn.

## Trường Tùy chỉnh

Khối này chỉ dành riêng cho WooCommerce. Spwig lấy mẫu 10 sản phẩm, khách hàng và đơn hàng từ cửa hàng của bạn và liệt kê bất kỳ trường meta tùy chỉnh nào mà nó phát hiện ra ngoài các trường WooCommerce tiêu chuẩn, cùng với loại được phát hiện và một giá trị ví dụ.

Đối với mỗi trường, hãy chọn nơi nó nên được đưa vào:

- **Ánh xạ đến** — Trường Tùy chỉnh 1, 2 hoặc 3 cho sản phẩm (Trường Tùy chỉnh 1 hoặc 2 cho khách hàng và đơn hàng), hoặc **Meta Data (JSON)** như một lựa chọn tổng hợp nếu bạn có nhiều trường tùy chỉnh hơn các vị trí được đánh số, hoặc để nguyên là **— Bỏ qua trường này —**.
- **Chuyển đổi** — cách giá trị nên được chuyển đổi khi nhập: Là Văn bản, Là Số (Nguyên), Là Thập phân, Là Đúng/Sai (Boolean), Là JSON, Là Ngày, Là URL, hoặc Là Email.

> **Lưu ý:** Các trường meta của Shopify hoàn toàn không được phát hiện bởi tính năng này — các di chuyển Shopify sẽ không bao giờ hiển thị khối Trường Tùy chỉnh, bất kể lượng dữ liệu metafield cửa hàng của bạn là bao nhiêu. Nếu bạn phụ thuộc vào các trường metafield của Shopify cho thông số sản phẩm, thuộc tính khách hàng hoặc tương tự, hãy lên kế hoạch nhập lại dữ liệu đó thủ công trong Spwig sau khi nhập.

Nếu Spwig không phát hiện bất kỳ trường tùy chỉnh nào trong mẫu của bạn, bạn sẽ thấy một thông báo xác nhận thay vì khối này, và không có gì cần cấu hình thêm.

Khi một số danh mục nguồn của bạn không có sự khớp nối rõ ràng trong Spwig, khối này cung cấp ba lựa chọn: **Tạo danh mục mới**, **Gán vào danh mục mặc định** (một danh mục 'Chưa phân loại' tổng hợp), hoặc **Bỏ qua các mục có danh mục chưa được ánh xạ**.

> **Lưu ý:** Dù bạn chọn tùy chọn nào ở đây, Spwig hiện tại sẽ tự động tạo danh mục khớp nối cho bất kỳ sản phẩm nào có dữ liệu danh mục nguồn, và chỉ rơi vào 'Chưa phân loại' cho các sản phẩm hoàn toàn không có thông tin danh mục. Bạn không cần phải lo lắng quá nhiều về lựa chọn này — nếu bạn cuối cùng có các danh mục bạn không muốn, sẽ nhanh hơn để hợp nhất hoặc xóa chúng trong **Catalog > Categories** sau khi nhập dữ liệu thay vì dựa vào cài đặt này.

## Cài đặt thuế, vận chuyển và giá

Khối cuối cùng, **Cài đặt Thuế & Vận chuyển**, có ba tùy chọn: **Nhập cài đặt thuế**, **Nhập khu vực và phương thức vận chuyển**, và một loại **Điều chỉnh giá** và giá trị.

Hai ô kiểm không ảnh hưởng đến việc nhập dữ liệu — không có tỷ lệ thuế hay khu vực vận chuyển nào được chuyển từ nền tảng cũ của bạn, bất kể cách bạn thiết lập chúng. Cấu hình cả hai trực tiếp trong Spwig sau khi hoàn tất việc nhập dữ liệu: tỷ lệ thuế dưới **Settings > Tax & Currency**, khu vực và phương thức vận chuyển dưới **Settings > Shipping**.

**Điều chỉnh giá** hoạt động khác nhau tùy thuộc vào nền tảng nguồn của bạn:

- **Di chuyển từ WooCommerce, CSV và Shopify** — tùy chọn này hoạt động như mô tả. Chọn **Tỷ lệ phần trăm** hoặc **Số tiền cố định**, nhập giá trị (ví dụ `10` để tăng 10%, hoặc `-5` để giảm $5), và giá cơ bản của mỗi sản phẩm sẽ được điều chỉnh theo số lượng đó khi nhập. Nó chỉ áp dụng cho giá cơ bản — giá khuyến mãi/giá so sánh sẽ được chuyển mà không điều chỉnh.
- **Di chuyển từ Magento** — tùy chọn này cũng hiển thị trên trang, nhưng không có tác dụng; giá của Magento được nhập không thay đổi bất kể bạn nhập gì. Nếu bạn cần thay đổi giá chung cho di chuyển từ Magento, hãy áp dụng nó sau bằng các công cụ điều chỉnh giá hàng loạt trong danh mục của Spwig thay vì trường này.

> **Cảnh báo:** Nếu bạn đang di chuyển từ WooCommerce, CSV hoặc Shopify và không muốn thay đổi giá, hãy để **Điều chỉnh giá** được đặt thành **Không**. Đây là điều khiển duy nhất trên trang này thực sự thay đổi dữ liệu của bạn, và rất dễ giả định sai rằng nó hoạt động giống như các ô kiểm thuế và vận chuyển ngay phía trên.

## Các ánh xạ được lưu để sử dụng lần sau

Bất kể bạn cấu hình gì trên trang này, nó sẽ được lưu cùng với công việc di chuyển, và Spwig sẽ sử dụng lại nó làm điểm bắt đầu cho các lần di chuyển tương lai từ cùng một nền tảng — rất hữu ích nếu bạn thực hiện di chuyển theo giai đoạn (danh mục và sản phẩm trước, đơn hàng sau) hoặc cần nhập lại sau khi sửa lỗi dữ liệu. Bạn cũng có thể quay lại và điều chỉnh các ánh xạ đã lưu sau khi hoàn tất di chuyển từ nút **Field Mappings** trên bảng điều khiển di chuyển, mà không cần chạy lại toàn bộ hướng dẫn.

## Một số mẹo

- **Kiểm tra khối Ánh xạ Tự động ngay cả khi bạn không thể chỉnh sửa nó** — việc phát hiện một ánh xạ sai trước khi nhấp vào **Bắt đầu nhập** sẽ rẻ hơn rất nhiều so với việc sửa hàng trăm bản ghi đã nhập sau đó.
- **Đổi tên các tiêu đề CSV mơ hồ trước khi tải lên** nếu việc phát hiện tự động không nhận ra chúng, thay vì cố gắng ép một trường không khớp thông qua danh sách thả xuống.
- **Sử dụng Meta Data (JSON) làm nơi chứa các trường tùy chỉnh của bạn** — đây là mục tiêu ánh xạ duy nhất không bị giới hạn sau hai hoặc ba trường.
- **Đừng dựa vào trang này cho thuế, vận chuyển hoặc (trên Magento) giá** — hãy coi những thứ này là nhiệm vụ thiết lập thủ công ngay sau khi nhập, chứ không phải là điều mà hướng dẫn xử lý cho bạn.
- **Để Điều chỉnh giá ở chế độ Không trong lần chạy đầu tiên của một lần di chuyển mới**, sau đó sử dụng một lô hàng kiểm tra nhỏ để xác nhận toán học trước khi áp dụng nó cho toàn bộ danh mục của bạn.