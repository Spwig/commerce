---
title: Bộ Sưu Tập Sản Phẩm
---

Các bộ sưu tập cho phép bạn nhóm các sản phẩm lại với nhau để hiển thị trên cửa hàng trực tuyến của bạn. Khác với các danh mục — được dùng để tổ chức toàn bộ danh mục sản phẩm theo một cấu trúc phân cấp cố định — các bộ sưu tập linh hoạt hơn, là các nhóm được lựa chọn kỹ lưỡng mà bạn tạo ra với một mục đích cụ thể. Một bộ sưu tập có thể làm nổi bật các sản phẩm mới, trưng bày các mặt hàng cho chiến dịch theo mùa, hoặc trình bày một lựa chọn tinh tế các sản phẩm bán chạy.

Truy cập **Catalog > Collections** để quản lý các bộ sưu tập của bạn.

## Bộ sưu tập vs danh mục

Cả danh mục và bộ sưu tập đều nhóm các sản phẩm, nhưng chúng phục vụ các mục đích khác nhau:

| | Danh mục | Bộ sưu tập |
|---|---|---|
| **Mục đích** | Cấu trúc danh mục cố định | Nhóm linh hoạt, được lựa chọn kỹ lưỡng |
| **Cấu trúc phân cấp** | Có — cấu trúc phụ thuộc/cha | Không — nhóm phẳng |
| **Số sản phẩm mỗi nhóm** | Mỗi sản phẩm thuộc về một danh mục | Một sản phẩm có thể xuất hiện trong nhiều bộ sưu tập |
| **Sử dụng điển hình** | Menu điều hướng cửa hàng, duyệt theo bộ phận | Trang đích, chiến dịch, bộ sưu tập nổi bật |

Sử dụng danh mục cho "cách cửa hàng của bạn được tổ chức" và bộ sưu tập cho "những thứ bạn muốn làm nổi bật vào lúc này".

## Loại bộ sưu tập

Khi tạo một bộ sưu tập, hãy chọn một loại phù hợp với cách bạn muốn quản lý danh sách sản phẩm:

| Loại | Cách thêm sản phẩm |
|---|---|
| **Chọn thủ công** | Bạn chọn chính xác những sản phẩm nào sẽ xuất hiện, một cách riêng lẻ |
| **Quy tắc tự động** | Các sản phẩm được thêm tự động dựa trên các tiêu chí bạn xác định |
| **Sản phẩm nổi bật** | Một lựa chọn được biên tập kỹ lưỡng, được quản lý thủ công |
| **Theo mùa** | Một lựa chọn theo thời gian, thường được quản lý thủ công cho các chiến dịch |

Loại Chọn thủ công và Sản phẩm nổi bật cho phép bạn kiểm soát chính xác. Các bộ sưu tập tự động có thể phát triển cùng với danh mục của bạn mà không cần bảo trì liên tục.

## Tạo một bộ sưu tập

1. Truy cập **Catalog > Collections**
2. Nhấp **+ Add Collection**
3. Điền vào phần **Basic Information**:
   - **Name** — tên bộ sưu tập như sẽ hiển thị trên cửa hàng trực tuyến của bạn
   - **Slug** — đường dẫn URL cho trang bộ sưu tập (tự động điền từ tên; bạn có thể tùy chỉnh nó)
   - **Description** — mô tả được hiển thị trên trang cửa hàng trực tuyến của bộ sưu tập
4. Chọn **Loại Bộ Sưu Tập**
5. Thêm sản phẩm:
   - Đối với loại **Chọn thủ công** và **Sản phẩm nổi bật**: sử dụng trường **Products** để tìm kiếm và thêm sản phẩm
   - Đối với loại **Tự động**: xác định tiêu chí trong trường **Auto Criteria**
6. Tải lên hình ảnh:
   - **Image** — hình ảnh chính của bộ sưu tập được sử dụng trên các trang danh sách và ảnh thu nhỏ
   - **Banner Image** — hình ảnh banner rộng được hiển thị ở đầu trang bộ sưu tập
7. Cấu hình các trường **SEO** (khuyến khích nhưng không bắt buộc):
   - **Meta Title** — tiêu đề trang được hiển thị trong kết quả tìm kiếm
   - **Meta Description** — mô tả được hiển thị dưới tiêu đề trong kết quả tìm kiếm
8. Thiết lập **Display Options**:
   - **Is Active** — kiểm soát việc bộ sưu tập có hiển thị trên cửa hàng trực tuyến của bạn hay không
   - **Is Featured** — đánh dấu bộ sưu tập để hiển thị nổi bật trong chủ đề của bạn
   - **Sort Order** — kiểm soát thứ tự mà các bộ sưu tập xuất hiện trên các trang danh sách (số nhỏ hơn sẽ xuất hiện trước)
9. Nhấp **Save**

## Thêm sản phẩm vào bộ sưu tập

Đối với các bộ sưu tập thủ công, sử dụng trường **Products** tự động hoàn tất để tìm kiếm danh mục của bạn và chọn các mục. Bạn có thể thêm bất kỳ số lượng sản phẩm nào bạn cần — không có giới hạn.

Các sản phẩm có thể thuộc về nhiều bộ sưu tập cùng lúc. Ví dụ, một sản phẩm có thể nằm trong cả bộ sưu tập "Summer Sale" và bộ sưu tập "Bestsellers" của bạn mà không gây xung đột.

## Hiển thị bộ sưu tập trên cửa hàng trực tuyến

Mỗi bộ sưu tập sẽ tự động có một trang riêng tại `/collection/{slug}/`. Bạn có thể liên kết đến các trang bộ sưu tập từ menu điều hướng của bạn, trình tạo trang, hoặc các banner quảng cáo.

Cờ **Is Featured** được chủ đề của bạn sử dụng để xác định các bộ sưu tập nào sẽ hiển thị ở các vị trí nổi bật — ví dụ, một lưới các bộ sưu tập nổi bật trên trang chủ. Kiểm tra tài liệu của chủ đề bạn để hiểu chính xác cách các bộ sưu tập nổi bật được hiển thị.

## Quản lý tính năng hiển thị của bộ sưu tập

- **Tình trạng hoạt động** kiểm soát việc trang danh mục có thể truy cập công khai hay không.

Một danh mục không hoạt động sẽ bị ẩn khỏi khách hàng nhưng vẫn được lưu trữ trong phần quản trị để bạn có thể kích hoạt lại sau này.
- **Thứ tự sắp xếp** xác định thứ tự mà các danh mục hiển thị trên các trang danh sách.

Gán các số nhỏ hơn cho các danh mục bạn muốn hiển thị trước.

## SEO cho danh mục

Mỗi danh mục có riêng **Tiêu đề Meta** và **Mô tả Meta**. Những trường này kiểm soát nội dung hiển thị trên kết quả tìm kiếm của công cụ tìm kiếm khi ai đó tìm thấy trang danh mục của bạn. Nếu bạn để trống các trường này, chủ đề của bạn sẽ thường tự động chuyển sang sử dụng tên và mô tả của danh mục.

Các tiêu đề SEO danh mục tốt là mô tả và cụ thể:
- "Summer Dresses 2026 — Floral & Lightweight Styles" hoạt động tốt hơn "Summer Collection"
- "Men's Running Shoes — Lightweight & Breathable" hoạt động tốt hơn "Running Shoes"

## Mẹo

- Giữ tên danh mục ngắn gọn và rõ ràng — chúng sẽ xuất hiện như tiêu đề trang và văn bản liên kết trong thanh điều hướng cửa hàng của bạn
- Sử dụng các danh mục theo mùa hoặc chiến dịch có kế hoạch bắt đầu và kết thúc: tạo danh mục, kích hoạt nó khi chiến dịch bắt đầu, và ngừng kích hoạt (thay vì xóa) khi chiến dịch kết thúc để bạn có thể tham khảo lại sau này
- Trường **Thứ tự sắp xếp** đáng để thiết lập một cách có ý thức — mặc định là 0 cho tất cả các danh mục, điều này có nghĩa là chúng sẽ được sắp xếp theo thứ tự chữ cái. Gán các số cụ thể để kiểm soát danh mục nào sẽ được hiển thị nổi bật hơn
- Một danh mục không có sản phẩm sẽ hiển thị một trang trống cho khách hàng — hoặc thêm sản phẩm trước khi kích hoạt, hoặc giữ danh mục không hoạt động cho đến khi nó sẵn sàng
- Chỉ đánh dấu **Là danh mục nổi bật** cho các danh mục bạn thực sự muốn nổi bật; hầu hết các chủ đề dành các vị trí nổi bật cho một số lượng nhỏ danh mục và hiển thị có thể trở nên lộn xộn nếu quá nhiều danh mục được đánh dấu