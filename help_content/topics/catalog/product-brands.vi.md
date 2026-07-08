---
title: Thương Hiệu Sản Phẩm
---

Các thương hiệu cho phép bạn liên kết sản phẩm với nhà sản xuất hoặc nhãn hiệu và cung cấp cho khách hàng cách duyệt cửa hàng theo thương hiệu. Mỗi thương hiệu sẽ có riêng một trang trên cửa hàng của bạn, nơi khách hàng có thể khám phá tất cả sản phẩm từ thương hiệu đó, đọc câu chuyện thương hiệu và theo dõi liên kết đến trang web của thương hiệu.

Truy cập **Catalog > Brands** để quản lý thương hiệu của bạn.

## Tại sao nên sử dụng thương hiệu

Thương hiệu có hai mục đích trong Spwig:

1. **Tổ chức** — sản phẩm được gắn nhãn với thương hiệu, giúp khách hàng trung thành với nhãn hiệu dễ dàng tìm thấy những gì họ đang tìm kiếm
2. **Quản lý hàng hóa** — các trang thương hiệu là không gian riêng để trình bày câu chuyện thương hiệu, logo và toàn bộ danh mục sản phẩm, điều này có thể cải thiện tỷ lệ chuyển đổi cho những khách hàng quan tâm đến thương hiệu

Thương hiệu cũng hoạt động cùng với hệ thống khuyến mãi — bạn có thể chạy một chương trình giảm giá áp dụng cho tất cả sản phẩm từ một thương hiệu cụ thể mà không cần chọn từng sản phẩm riêng lẻ.

## Tạo thương hiệu

1. Truy cập **Catalog > Brands**
2. Nhấp **+ Add Brand**
3. Điền vào phần **Basic Information**:
   - **Name** — tên thương hiệu như sẽ hiển thị trên cửa hàng của bạn (phải duy nhất)
   - **Slug** — đường dẫn URL cho trang thương hiệu (tự động điền từ tên; bạn có thể tùy chỉnh)
   - **Description** — mô tả ngắn về thương hiệu được hiển thị trên trang thương hiệu
   - **Website** — URL trang web chính thức của thương hiệu (tùy chọn — hiển thị dưới dạng liên kết trên trang thương hiệu)
4. Thêm tài sản thương hiệu:
   - **Logo** — hình ảnh logo thương hiệu, được sử dụng trong danh sách thương hiệu và trên trang thương hiệu
   - **Banner Image** — hình ảnh banner rộng được hiển thị ở đầu trang thương hiệu
5. Viết **Brand Story** (tùy chọn) — một bài viết dài hơn về lịch sử, giá trị hoặc điều làm nên sự đặc biệt của thương hiệu. Nội dung này xuất hiện trên trang thương hiệu và có thể là cách hiệu quả để kể câu chuyện thương hiệu cho khách hàng quan tâm.
6. Cấu hình các trường **SEO**:
   - **Meta Title** — tiêu đề trang hiển thị trong kết quả tìm kiếm của công cụ tìm kiếm
   - **Meta Description** — mô tả ngắn hiển thị bên dưới tiêu đề trong kết quả tìm kiếm
7. Thiết lập tùy chọn hiển thị:
   - **Show Brand Page** — kiểm soát xem trang thương hiệu có thể truy cập công khai hay không. Tắt tùy chọn này để ẩn thương hiệu khỏi cửa hàng nhưng vẫn giữ lại trong hệ thống.
   - **Is Active** — kiểm soát xem thương hiệu có thể được gán cho sản phẩm và hiển thị trong cửa hàng hay không
   - **Is Featured** — đánh dấu thương hiệu để hiển thị nổi bật trong chủ đề của bạn (ví dụ: một hàng logo thương hiệu trên trang chủ)
8. Nhấp **Save**

## Gán sản phẩm cho một thương hiệu

Các thương hiệu được gán trên từng bản ghi sản phẩm, không phải từ trang quản lý thương hiệu. Để gán một thương hiệu cho sản phẩm:

1. Truy cập **Catalog > Products** và mở sản phẩm
2. Trong biểu mẫu sản phẩm, tìm trường **Brand**
3. Tìm kiếm và chọn thương hiệu phù hợp
4. Lưu sản phẩm

Sau khi gán thương hiệu, sản phẩm sẽ tự động xuất hiện trên trang cửa hàng của thương hiệu đó.

## Trang thương hiệu trên cửa hàng của bạn

Mỗi thương hiệu có **Show Brand Page** được bật sẽ có riêng một trang tại `/brand/{slug}/`. Trang hiển thị:

- Logo thương hiệu và hình ảnh banner
- Tên thương hiệu và mô tả
- Câu chuyện thương hiệu (nếu có)
- Liên kết đến trang web của thương hiệu (nếu có)
- Tất cả sản phẩm đang hoạt động được gán cho thương hiệu đó

Khách hàng có thể truy cập các trang thương hiệu bằng cách nhấp vào tên thương hiệu trên trang sản phẩm, hoặc thông qua các liên kết bạn tạo trong thanh điều hướng hoặc trình tạo trang.

## SEO cho trang thương hiệu

Việc điền các trường **Meta Title** và **Meta Description** cho từng thương hiệu giúp các trang thương hiệu hiển thị tốt trong kết quả tìm kiếm. Các tiêu đề SEO hiệu quả cho thương hiệu thường kết hợp tên thương hiệu với những gì thương hiệu bán:

| Brand | Good Meta Title |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

Nếu bạn để trống các trường SEO, chủ đề của bạn sẽ tự động sử dụng tên thương hiệu.

### Tạo SEO tự động

Nếu **SEO Tự động tạo** được bật cho một thương hiệu, Spwig sẽ tự động tạo nội dung tiêu đề và mô tả meta khi lưu thương hiệu.

Điều này rất tiện lợi cho các cửa hàng có nhiều thương hiệu nhưng sẽ cung cấp ít kiểm soát hơn về từ ngữ cụ thể.

Bạn luôn có thể ghi đè nội dung được tạo tự động bằng cách nhập trực tiếp vào các trường và tắt nút chuyển đổi tự động.

## Thương hiệu nổi bật

Cờ **Is Featured** được các chủ đề sử dụng để hiển thị một hàng hoặc lưới các logo thương hiệu được chọn lọc — thường trên trang chủ. Chỉ nên chọn một số nhỏ thương hiệu để nổi bật tại một thời điểm; hãy tham khảo tài liệu chủ đề của bạn để hiểu rõ số lượng thương hiệu nổi bật hiển thị tối ưu là bao nhiêu.

## Mẹo

- Tải lên logo thương hiệu dưới dạng PNG hoặc WebP có nền trong suốt — nó sẽ hiển thị rõ ràng trên bất kỳ màu nền nào trong chủ đề của bạn
- Viết một câu chuyện thương hiệu hấp dẫn ngay cả đối với các thương hiệu ít được biết đến; khách hàng không quen thuộc với thương hiệu sẽ đánh giá cao bối cảnh giúp họ quyết định xem sản phẩm có phù hợp với họ hay không
- Nếu bạn chạy các chương trình khuyến mãi nhắm đến các thương hiệu cụ thể, hãy đảm bảo tên thương hiệu trong Spwig khớp hoàn toàn — các chương trình khuyến mãi sử dụng mối quan hệ thương hiệu trên sản phẩm để xác định tính đủ điều kiện
- Khi bạn ngừng cung cấp sản phẩm của thương hiệu, hãy tắt thương hiệu thay vì xóa nó — việc xóa sẽ loại bỏ tham chiếu thương hiệu khỏi tất cả sản phẩm liên quan, trong khi việc tắt giữ lại lịch sử
- Sử dụng cờ **Is Featured** một cách tiết kiệm; một trang chủ hiển thị 20 logo thương hiệu sẽ mất đi tác động so với 6–8 logo được chọn cẩn thận