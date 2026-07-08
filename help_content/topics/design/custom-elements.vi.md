---
title: Phần tử tùy chỉnh
---

Các phần tử tùy chỉnh cho phép bạn xây dựng các khối xây dựng trang có thể tái sử dụng, được thiết kế riêng cho nhu cầu của cửa hàng bạn. Bạn thiết kế một phần tử bằng cách trực quan sử dụng các công cụ hiện có của trình xây dựng trang, sau đó có thể kết nối nó với dữ liệu cửa hàng đang hoạt động - như tên sản phẩm, giá cả hoặc hình ảnh - để phần tử tự động điền nội dung thực tế khi được đặt trên một trang. Sau khi tạo, các phần tử tùy chỉnh của bạn sẽ xuất hiện trong thư viện phần tử của trình xây dựng trang cùng với các khối có sẵn.

![Thư viện phần tử tùy chỉnh](/static/core/admin/img/help/custom-elements/custom-elements-list.webp)

## Khi nào nên sử dụng phần tử tùy chỉnh

Các phần tử tùy chỉnh có giá trị nhất khi bạn liên tục xây dựng cùng một bố cục. Thay vì tạo lại một "thẻ sản phẩm nổi bật" từ đầu trên mọi trang, bạn xây dựng nó một lần dưới dạng phần tử tùy chỉnh và thả nó ở bất cứ đâu bạn cần. Nếu phần tử được liên kết dữ liệu, nó sẽ tự động lấy thông tin sản phẩm hiện tại - không cần cập nhật thủ công khi giá cả hoặc tên thay đổi.

Một số ứng dụng phổ biến:

- Các thẻ nổi bật sản phẩm hiển thị tên, giá và hình ảnh chính
- Các khối khuyến mãi danh mục có banner, tiêu đề và liên kết
- Các bảng trưng bày thương hiệu có logo và mô tả
- Các bản tóm tắt bài viết blog có hình ảnh nổi bật, tiêu đề và đoạn trích

## Tạo phần tử tùy chỉnh mới

1. Di chuyển đến **Thiết kế > Phần tử tùy chỉnh**
2. Nhấp **+ Thêm phần tử tùy chỉnh**
3. Spwig lập tức tạo một phần tử nháp và mở **Trình xây dựng trực quan** - bạn không cần điền vào một biểu mẫu trước
4. Trong Trình xây dựng trực quan, xây dựng bố cục phần tử của bạn bằng các công cụ trình xây dựng trang hiện có
5. Khi bạn hài lòng với thiết kế, cấu hình cài đặt phần tử (tên, liên kết dữ liệu, biểu tượng) trong thanh bên
6. Bật **Hoạt động** khi bạn sẵn sàng xuất bản phần tử vào thư viện
7. Lưu phần tử

Phần tử hiện đã có sẵn trong bảng phần tử của trình xây dựng trang dưới danh mục bạn đã chỉ định.

## Trình xây dựng trực quan

Trình xây dựng trực quan là một bảng vẽ chuyên dụng để thiết kế phần tử của bạn. Nó hoạt động giống như trình xây dựng trang tiêu chuẩn nhưng tập trung vào một phần tử thay vì toàn bộ trang. Bạn có thể:

- Thêm và sắp xếp các phần tử con (khối văn bản, hình ảnh, hộp chứa, v.v.)
- Thiết lập kiểu dáng, khoảng cách và bố cục cho từng phần tử con
- Xem trước cách phần tử sẽ trông như thế nào với dữ liệu mẫu

Các thay đổi trong Trình xây dựng trực quan được lưu trực tiếp vào định nghĩa phần tử. Không có bước xuất bản riêng biệt - việc lưu trong trình xây dựng sẽ cập nhật phần tử ngay lập tức cho bất kỳ trang nào đã sử dụng nó.

## Cấu hình cài đặt phần tử

Mỗi phần tử tùy chỉnh có các cài đặt sau:

| Trường | Mô tả |
|-------|-------------|
| **Tên** | Tên hiển thị được hiển thị trong thư viện phần tử |
| **Slug** | Nhận dạng an toàn URL, được tạo tự động từ tên |
| **Mô tả** | Ghi chú tùy chọn về mục đích của phần tử này |
| **Mô hình mục tiêu** | Mô hình cửa hàng để liên kết dữ liệu từ (xem bên dưới) |
| **Biểu tượng** | Biểu tượng được hiển thị trong thư viện phần tử |
| **Danh mục** | Nhóm các phần tử liên quan lại với nhau trong thư viện |
| **Hoạt động** | Phần tử có sẵn trong trình xây dựng trang hay không |

## Liên kết dữ liệu

Liên kết dữ liệu kết nối các phần của bố cục phần tử của bạn với dữ liệu cửa hàng đang hoạt động. Khi một nhà biên tập trang đặt phần tử được liên kết dữ liệu trên một trang, họ chọn một bản ghi cụ thể (ví dụ, một sản phẩm), và tất cả các trường được liên kết sẽ tự động điền từ bản ghi đó.

### Chọn mô hình mục tiêu

Cài đặt **Mô hình mục tiêu** xác định loại dữ liệu cửa hàng mà phần tử có thể hiển thị. Các mô hình có sẵn là:

| Mô hình | Nó cung cấp gì |
|-------|-----------------|
| **Sản phẩm** | Tên, giá, trạng thái tồn kho, hình ảnh, mô tả, SKU, danh mục, thương hiệu và nhiều hơn nữa |
| **Danh mục** | Tên, mô tả, hình ảnh, banner, số lượng sản phẩm và URL |
| **Thương hiệu** | Tên, logo, mô tả, câu chuyện thương hiệu và URL |
| **Bài viết blog** | Tiêu đề, đoạn trích, hình ảnh nổi bật, tác giả, ngày xuất bản và URL |

Để trống **Mô hình mục tiêu** để tạo một phần tử tĩnh không có dữ liệu động. Các phần tử tĩnh hữu ích cho các thành phần thiết kế cố định như banner trang trí hoặc các khoảng cách bố cục.

### Cách hoạt động của các liên kết


Trong trình xây dựng trực quan (Visual Builder), bạn có thể đánh dấu các phần tử con riêng lẻ là có liên kết dữ liệu bằng cách chọn trường mô hình mà chúng nên hiển thị.

Ví dụ:
- Một phần tử con **text** có thể được liên kết với **Product Name**, để hiển thị tên sản phẩm đã chọn
- Một phần tử con **image** có thể được liên kết với **Main Image**, để hiển thị ảnh chính của sản phẩm
- Một phần tử con **text** có thể được liên kết với **Price**, để luôn phản ánh giá hiện tại

Mỗi liên kết ánh xạ một trường nội dung của phần tử đến một trường mô hình. Bạn có thể thêm nhiều liên kết cho một phần tử tùy chỉnh — ví dụ, liên kết một khối văn bản với **Product Name** và một khối hình ảnh riêng biệt với **Main Image** cùng lúc.

### Các cài đặt ảnh thu nhỏ

Đối với các liên kết ảnh, bạn có thể chọn tùy chọn **Thumbnail Preset** (ví dụ như `thumbnail` hoặc `medium`). Điều này kiểm soát kích thước ảnh được tải, giúp trang tải nhanh hơn bằng cách cung cấp ảnh có kích thước phù hợp với bố cục phần tử.

## Tắt và bật lại các phần tử

Tắt một phần tử sẽ xóa nó khỏi thư viện phần tử, khiến nó không thể được thêm vào các trang mới. Các trang hiện tại đã sử dụng phần tử đó sẽ không bị ảnh hưởng — phần tử vẫn tiếp tục hiển thị trên các trang đó.

Để tắt:
1. Di chuyển đến **Design > Custom Elements**
2. Nhấp vào tên phần tử
3. Bỏ chọn **Active**
4. Lưu

Để bật lại, thực hiện các bước tương tự và chọn lại **Active**.

## Lọc thư viện phần tử

Danh sách phần tử hỗ trợ lọc theo:
- **Active / Inactive** — chỉ hiển thị các phần tử đã xuất bản hoặc chỉ các phần tử nháp
- **Target Model** — lọc theo mô hình mà phần tử được liên kết
- **Category** — lọc theo danh mục phần tử
- **Search** — tìm kiếm theo tên, slug hoặc mô tả

Điều này rất hữu ích khi bạn có nhiều phần tử tùy chỉnh và cần tìm một phần tử cụ thể nhanh chóng.

## Ví dụ: thẻ nổi bật sản phẩm

**Mục tiêu:** Một phần tử thẻ hiển thị ảnh chính, tên và giá của sản phẩm.

| Cài đặt | Giá trị |
|---------|-------|
| Name | Product Highlight Card |
| Target Model | Product |
| Category | Products |
| Icon | fas fa-box |

Trong trình xây dựng trực quan, thêm:
- Một phần tử **Image** được liên kết với **Main Image** với cài đặt thu nhỏ `medium`
- Một phần tử **Text** được liên kết với **Product Name**
- Một phần tử **Text** được liên kết với **Price**

Sau khi lưu và kích hoạt, phần tử sẽ xuất hiện trong trình xây dựng trang dưới danh mục Products. Khi một biên tập viên trang thêm nó vào trang, họ sẽ chọn sản phẩm cần nổi bật và thẻ sẽ tự động điền thông tin.

## Một số mẹo

- Đặt tên các phần tử mô tả rõ mục đích và loại dữ liệu của chúng — ví dụ, "Product Highlight Card" thay vì "Card 1" — để thư viện dễ điều hướng hơn khi số lượng phần tử tăng lên
- Sử dụng trường **Category** để nhóm các phần tử liên quan (Products, Blog, Promotions) — điều này giúp thư viện phần tử luôn được tổ chức cho các biên tập viên trang của bạn
- Kiểm tra các phần tử liên kết dữ liệu bằng cách thêm chúng vào một trang nháp và chọn một bản ghi thực tế trước khi xuất bản, để xác nhận liên kết đang lấy đúng thông tin
- Tắt các phần tử lỗi thời thay vì xóa chúng — điều này giữ nguyên các trang vẫn tham chiếu đến chúng và cho phép bạn kích hoạt lại sau này
- Các phần tử tĩnh (không có mô hình mục tiêu) lý tưởng cho các mẫu bố cục bạn sử dụng lại trên toàn trang web, như các thanh phân cách, bảng gọi hành động (CTA) hoặc khoảng trống thương hiệu