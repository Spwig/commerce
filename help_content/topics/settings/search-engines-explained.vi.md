---
title: Search Engines Explained
---

Giải thích về Máy tìm kiếm

Các máy tìm kiếm trong Spwig không phải là các dịch vụ bên ngoài như Elasticsearch hoặc Algolia - chúng là các bối cảnh cấu hình trong hệ thống tìm kiếm gốc của cửa hàng bạn. Mỗi máy tìm kiếm xác định nội dung nào cần tìm, nội dung nào cần loại bỏ và cách xếp hạng kết quả. Hướng dẫn này giải thích máy tìm kiếm là gì, khi nào nên tạo nhiều máy tìm kiếm và cách cấu hình chúng.

Hầu hết các nhà bán hàng sử dụng một máy tìm kiếm mặc định là "shop". Chỉ tạo nhiều máy tìm kiếm khi bạn cần các hỗn hợp nội dung hoặc các loại bỏ khác nhau cho các trường hợp sử dụng khác nhau.

![Danh sách Máy tìm kiếm](/static/core/admin/img/help/search-engines-explained/search-engines-list.webp)

## Máy tìm kiếm là gì?

Một máy tìm kiếm trong Spwig là một cấu hình có tên chỉ định:

- **Loại nội dung cần tìm** (sản phẩm, danh mục, thương hiệu, bài viết blog)
- **Nội dung cần loại bỏ** (các danh mục hoặc thương hiệu cụ thể bạn muốn ẩn khỏi tìm kiếm)
- **Trọng số liên quan tùy chỉnh** (trọng số tùy chỉnh theo từng máy tìm kiếm, tùy chọn)
- **Trạng thái hoạt động** (các máy tìm kiếm có thể tạm thời bị tắt)

Mỗi máy tìm kiếm có một slug duy nhất được sử dụng trong các cuộc gọi API và mã phía trước để chỉ định máy tìm kiếm nào nên xử lý yêu cầu tìm kiếm.

## Khi nào nên tạo nhiều máy tìm kiếm

Hầu hết các cửa hàng chỉ cần một máy tìm kiếm. Tạo thêm các máy tìm kiếm cho các trường hợp sau:

| Trường hợp sử dụng | Ví dụ |
|------------------|-------|
| **Hỗn hợp nội dung khác nhau** | Máy tìm kiếm cửa hàng chỉ tìm sản phẩm; Máy tìm kiếm blog chỉ tìm bài viết blog |
| **Loại bỏ chọn lọc** | Máy tìm kiếm cửa hàng chính ẩn danh mục giảm giá; Máy tìm kiếm giảm giá chỉ hiển thị các mặt hàng giảm giá |
| **Tìm kiếm theo bộ phận** | Máy tìm kiếm điện tử loại bỏ danh mục thời trang; Máy tìm kiếm thời trang loại bỏ điện tử |
| **Phân tách B2B và B2C** | Máy tìm kiếm sỉ chỉ hiển thị sản phẩm số lượng lớn; Máy tìm kiếm lẻ hiển thị sản phẩm tiêu dùng |

Nếu bạn không chắc liệu mình có cần nhiều máy tìm kiếm hay không, hãy giữ lại một máy. Việc thêm các máy tìm kiếm tạo ra sự phức tạp mà không có lợi ích trừ khi bạn có một trường hợp sử dụng cụ thể.

## Hướng dẫn 4 bước

![Bước 1 - Thông tin cơ bản](/static/core/admin/img/help/search-engines-explained/wizard-step1-basic.webp)

Truy cập **Tìm kiếm > Hướng dẫn thiết lập** để tạo một máy tìm kiếm mới thông qua quy trình 4 bước được hướng dẫn:

### Bước 1: Thông tin cơ bản

**Tên máy tìm kiếm** - Tên hiển thị thân thiện (ví dụ: "Tìm kiếm cửa hàng", "Tìm kiếm blog"). Chỉ được sử dụng trong giao diện quản trị.

**Slug** - Nhận dạng an toàn cho URL (ví dụ: "shop-search", "blog-search"). Được sử dụng trong các cuộc gọi API và mã phía trước. Được tạo tự động từ tên nếu để trống.

**Hoạt động** - Chỉ định máy tìm kiếm này có sẵn cho các cuộc tìm kiếm hay không. Các máy tìm kiếm không hoạt động sẽ không trả về kết quả nào.

### Bước 2: Loại nội dung

Chọn các loại nội dung mà máy tìm kiếm này sẽ tìm kiếm:

- Sản phẩm (bao gồm tất cả các loại sản phẩm: vật lý, kỹ thuật số, đăng ký)
- Danh mục
- Thương hiệu
- Bài viết blog

**Lưu ý**: Chỉ chọn các loại nội dung liên quan đến mục đích của máy tìm kiếm này. Một máy tìm kiếm tập trung vào blog không cần bật tìm kiếm sản phẩm.

### Bước 3: Trọng số (tùy chọn)

![Bước 3 - Trọng số](/static/core/admin/img/help/search-engines-explained/wizard-step3-weights.webp)

Tùy chọn tùy chỉnh trọng số liên quan cho máy tìm kiếm cụ thể này. Nếu bỏ qua, máy tìm kiếm sẽ kế thừa trọng số toàn cục từ SearchSettings.

Hầu hết các máy tìm kiếm nên bỏ qua bước này và sử dụng trọng số mặc định toàn cục. Chỉ tùy chỉnh trọng số nếu máy tìm kiếm này có nhu cầu xếp hạng đặc biệt (ví dụ: một máy tìm kiếm blog có thể tăng weight_blog_posts lên 1.2).

### Bước 4: Xem lại và tạo

Xem lại cấu hình của bạn và nhấp **Tạo máy tìm kiếm** để lưu.

## Các trường cấu hình máy tìm kiếm

Nếu bạn chỉnh sửa một máy tìm kiếm trực tiếp (bỏ qua hướng dẫn), bạn sẽ thấy các trường sau:

**Tên và Slug** - Tên hiển thị và nhận dạng URL

**Trạng thái hoạt động** - Chuyển đổi để bật/tắt

**Loại nội dung** - Mảng JSON như `['product', 'category']`

**Trọng số thay thế** - Đối tượng JSON như `{'weight_name': 1.8}` (trống nếu sử dụng trọng số toàn cục)

**Danh mục bị loại bỏ** - Mối quan hệ M2M với mô hình Category. Các sản phẩm trong các danh mục này sẽ không xuất hiện trong kết quả tìm kiếm.

**Thương hiệu bị loại bỏ** - Mối quan hệ M2M với mô hình Brand.

Sản phẩm có các thương hiệu này sẽ không hiển thị trong kết quả tìm kiếm.

## Sử dụng Loại trừ

Loại trừ sẽ ẩn nội dung cụ thể khỏi kết quả tìm kiếm của động cơ này:

**Ví dụ: Ẩn sản phẩm giảm giá**

1. Tạo động cơ "Main Shop"
2. Trong trường Danh mục bị loại trừ, chọn danh mục "Clearance" của bạn
3. Trong trường Thương hiệu bị loại trừ, chọn bất kỳ thương hiệu giá rẻ nào bạn muốn ẩn
4. Lưu

Bây giờ các cuộc tìm kiếm thông qua động cơ "Main Shop" sẽ không trả về sản phẩm giảm giá, mặc dù chúng vẫn hiển thị trên trang web của bạn. Bạn có thể tạo một động cơ "Clearance" riêng biệt để chỉ tìm kiếm các sản phẩm giảm giá.

## Sử dụng Động cơ trên Giao diện Người dùng

Mã前端 của bạn chỉ định động cơ nào được sử dụng thông qua các cuộc gọi API:

```javascript
// Sử dụng động cơ "shop" (thường gặp nhất)
fetch('/api/search/?q=laptop&engine=shop')

// Sử dụng động cơ "blog"
fetch('/api/search/?q=ecommerce tips&engine=blog')

// Động cơ mặc định nếu không chỉ định tham số engine
fetch('/api/search/?q=laptop')
```

Slug động cơ trở thành tham số truy vấn. Nếu không chỉ định động cơ, Spwig sẽ sử dụng động cơ hoạt động đầu tiên theo thứ tự bảng chữ cái.

## Đồng nghĩa và Chuyển hướng Đặc thù Động cơ

Cả hai mô hình Synonym và SearchRedirect đều có một khóa ngoại tùy chọn là `engine`. Nếu được thiết lập, đồng nghĩa hoặc chuyển hướng đó chỉ áp dụng cho các cuộc tìm kiếm thông qua động cơ cụ thể đó.

**Ví dụ**: Một động cơ blog có thể có các đồng nghĩa như "tutorial" → "guide" mà không áp dụng cho các cuộc tìm kiếm sản phẩm.

Hầu hết các đồng nghĩa và chuyển hướng nên KHÔNG đặc thù cho động cơ - hãy để trường engine trống để áp dụng chúng toàn cục.

## Một số mẹo

- **Bắt đầu với một động cơ** - Tạo động cơ mặc định "shop" và sử dụng nó cho mọi thứ cho đến khi bạn có nhu cầu rõ ràng cho nhiều động cơ
- **Sử dụng slug mô tả** - Chọn các slug như "shop", "blog", "wholesale" để rõ ràng chỉ ra mục đích của động cơ
- **Kiểm tra động cơ trước khi kích hoạt** - Tạo động cơ ở trạng thái không hoạt động, kiểm tra qua API, sau đó kích hoạt
- **Không tạo động cơ trừ khi cần thiết** - Nhiều động cơ sẽ làm tăng độ phức tạp cấu hình mà không mang lại lợi ích nếu chúng đều thực hiện cùng một việc
- **Xem lại phân tích theo động cơ** - Bảng điều khiển Phân tích Tìm kiếm có thể lọc theo động cơ để xem động cơ nào được sử dụng nhiều nhất