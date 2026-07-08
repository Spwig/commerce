---
title: Quản lý blog
---

Blog cho phép bạn xuất bản các bài viết, hướng dẫn và tin tức để thu hút lưu lượng truy cập và tương tác với khán giả của bạn. Blog của Spwig bao gồm trình chỉnh sửa văn bản phong phú, xuất bản có lịch trình, thông báo cho người đăng ký, chia sẻ tự động trên mạng xã hội và công cụ SEO.

![Bài đăng blog](/static/core/admin/img/help/blog-management/blog-post-list.webp)

## Tạo bài đăng blog

Truy cập **Marketing > Blog Posts** và nhấp vào **Add Post**.

### Nội dung bài đăng

Viết bài đăng của bạn bằng trình chỉnh sửa văn bản phong phú **CKEditor 5**, hỗ trợ:
- Định dạng văn bản (tiêu đề, in đậm, in nghiêng, danh sách, trích dẫn)
- Hình ảnh và phương tiện (tải lên qua thư viện phương tiện)
- Video được nhúng (YouTube, Vimeo)
- Bảng và khối mã
- Liên kết đến sản phẩm, danh mục và URL bên ngoài

Để bố cục phức tạp hơn, hãy bật tùy chọn **Page Builder** để sử dụng trình xây dựng trang kéo thả thay vì trình chỉnh sửa văn bản.

### Cài đặt bài đăng

| Cài đặt | Mô tả |
|---------|-------------|
| **Tiêu đề** | Tiêu đề được hiển thị trên blog và trong kết quả tìm kiếm |
| **Slug** | Nhận dạng thân thiện với URL (tự động được tạo từ tiêu đề, có thể chỉnh sửa) |
| **Tóm tắt** | Tóm tắt ngắn được hiển thị trên các thẻ bài đăng và nguồn cấp dữ liệu RSS |
| **Hình ảnh nổi bật** | Hình ảnh chính được hiển thị ở đầu bài đăng và trên các thẻ bài đăng |
| **Danh mục** | Danh mục chính cho bài đăng |
| **Thẻ** | Từ khóa để lọc và nội dung liên quan |
| **Tác giả** | Nhân viên được ghi nhận là tác giả |
| **Trạng thái** | Nháp, Lên lịch, Đã xuất bản hoặc Đã lưu trữ |
| **Nổi bật** | Đính bài đăng lên đầu danh sách blog |

### Cài đặt SEO

Mỗi bài đăng bao gồm các trường SEO:
- **Tiêu đề meta** — Tiêu đề tùy chỉnh cho kết quả tìm kiếm (mặc định là tiêu đề bài đăng)
- **Mô tả meta** — Tóm tắt được hiển thị trong kết quả tìm kiếm
- **Hình ảnh Open Graph** — Hình ảnh được sử dụng khi bài đăng được chia sẻ trên mạng xã hội

## Trạng thái bài đăng

| Trạng thái | Mô tả |
|--------|-------------|
| **Nháp** | Đang được thực hiện, không hiển thị cho công chúng |
| **Lên lịch** | Sẽ được xuất bản tự động vào ngày và giờ đã đặt |
| **Đã xuất bản** | Đang hoạt động và hiển thị cho khách truy cập |
| **Đã lưu trữ** | Ẩn khỏi danh sách blog nhưng vẫn có thể truy cập qua URL trực tiếp |

### Lên lịch bài đăng

Để lên lịch bài đăng để xuất bản trong tương lai:
1. Đặt trạng thái thành **Lên lịch**
2. Chọn **ngày và giờ xuất bản**
3. Lưu bài đăng

Một tác vụ nền tự động xuất bản bài đăng vào thời gian đã lên lịch và kích hoạt thông báo cho người đăng ký.

## Danh mục

Truy cập **Marketing > Blog Categories** để tổ chức nội dung của bạn.

Danh mục hỗ trợ:
- **Cấp bậc** — Tạo danh mục cha và con (ví dụ: "Hướng dẫn" > "Getting Started")
- **URL tùy chỉnh** — Mỗi danh mục có slug riêng để có URL sạch
- **Mô tả** — Thêm mô tả danh mục được hiển thị trên trang lưu trữ danh mục
- **Thứ tự** — Kiểm soát thứ tự hiển thị của danh mục trong điều hướng

## Thẻ

Thẻ cung cấp cách phân loại nội dung thứ cấp. Khác với danh mục (có cấp bậc), thẻ là nhãn phẳng. Người truy cập có thể nhấp vào thẻ để xem tất cả các bài đăng có thẻ đó.

## Người đăng ký

Truy cập **Marketing > Blog Subscribers** để quản lý danh sách người đăng ký của bạn.

### Cách hoạt động của đăng ký

1. Người truy cập đăng ký thông qua biểu mẫu trên blog (yêu cầu địa chỉ email)
2. Gửi email xác nhận **double opt-in**
3. Sau khi xác nhận, người đăng ký nhận được thông báo khi có bài đăng mới được xuất bản

### Tần suất thông báo

Người đăng ký chọn tần suất nhận thông báo:

| Tần suất | Mô tả |
|-----------|-------------|
| **Ngay lập tức** | Gửi email ngay khi có bài đăng mới được xuất bản |
| **Tóm tắt hàng tuần** | Một bản tóm tắt hàng tuần của tất cả các bài đăng mới |
| **Tóm tắt hàng tháng** | Một bản tóm tắt hàng tháng của tất cả các bài đăng mới |

Các tác vụ nền xử lý việc biên soạn và gửi tóm tắt tự động.

### Quản lý người đăng ký

- Xem số lượng người đăng ký, trạng thái xác nhận và ngày đăng ký
- Xuất danh sách người đăng ký để sử dụng trong các công cụ tiếp thị email bên ngoài
- Xóa hoặc hủy đăng ký địa chỉ cụ thể
- Mỗi email thông báo bao gồm một liên kết **hủy đăng ký** một lần nhấn

## Chia sẻ tự động trên mạng xã hội

Spwig có thể tự động chia sẻ các bài đăng mới đến tài khoản mạng xã hội của bạn khi chúng được xuất bản.

### Kết nối tài khoản mạng xã hội

Truy cập **Marketing > Social Connectors** để kết nối tài khoản của bạn:

| Nền tảng | Xác thực |
|----------|---------------|
| **Facebook** | OAuth — kết nối trang Facebook của bạn |
| **Instagram** | OAuth — kết nối tài khoản doanh nghiệp của bạn |
| **LinkedIn** | OAuth — kết nối trang công ty của bạn |

### Cách chia sẻ tự động hoạt động

1. Kết nối một hoặc nhiều tài khoản mạng xã hội
2. Khi tạo bài đăng, bật **Auto Share** cho mỗi tài khoản đã kết nối
3. Tùy chỉnh thông báo chia sẻ (mặc định là tiêu đề và tóm tắt bài đăng)
4. Khi bài đăng được xuất bản (hoặc đạt đến thời gian lên lịch), nó sẽ được chia sẻ tự động

Chia sẻ tự động cũng hoạt động với các bài đăng đã lên lịch — thông báo mạng xã hội được gửi cùng lúc bài đăng được đăng lên.

## Feeds RSS

Blog tự động tạo một feed RSS tại `/blog/feed/`. Điều này cho phép người truy cập và các công cụ tổng hợp đăng ký nội dung của bạn. Feed bao gồm:
- Tiêu đề và tóm tắt bài đăng
- Ngày xuất bản
- Thông tin tác giả
- Liên kết trực tiếp đến bài đăng đầy đủ

## Cài đặt blog

Truy cập **Marketing > Blog Settings** để cấu hình các tùy chọn blog toàn cầu:

- **Posts Per Page** — Số lượng bài đăng hiển thị trên mỗi trang trong danh sách
- **Allow Comments** — Bật hoặc tắt bình luận cho các bài đăng
- **Default Category** — Danh mục dự phòng cho các bài đăng không có danh mục được chỉ định
- **Social Sharing Buttons** — Hiển thị nút chia sẻ trên các trang bài đăng riêng lẻ

## Một số mẹo

- Viết bài đăng với **SEO trong tâm trí** — sử dụng tiêu đề mô tả, điền mô tả meta và bao gồm các từ khóa liên quan một cách tự nhiên trong nội dung.
- Sử dụng **xuất bản có lịch trình** để duy trì nhịp độ đăng bài đều đặn mà không cần nỗ lực thủ công.
- Bật **chia sẻ tự động** để tối đa hóa phạm vi tiếp cận — các bài đăng được chia sẻ trên mạng xã hội ngay sau khi xuất bản thu hút tương tác nhiều nhất.
- Khuyến khích người truy cập **đăng ký** bằng cách đặt biểu mẫu đăng ký nổi bật trên blog của bạn và sử dụng lời kêu gọi hành động hấp dẫn.
- Sử dụng **danh mục** cho các nhóm nội dung rộng và **thẻ** cho các chủ đề cụ thể — điều này giúp người truy cập tìm thấy nội dung liên quan.
- Thêm **hình ảnh nổi bật** cho mỗi bài đăng — các bài đăng có hình ảnh hoạt động tốt hơn trong kết quả tìm kiếm và chia sẻ mạng xã hội.
- Sử dụng tùy chọn **tóm tắt hàng tuần hoặc hàng tháng** cho các người đăng ký không muốn nhận email thường xuyên — điều này làm giảm tỷ lệ hủy đăng ký.