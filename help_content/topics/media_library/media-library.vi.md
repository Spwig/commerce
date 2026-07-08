---
title: Thư viện phương tiện
---

Thư viện phương tiện là trung tâm để quản lý tất cả các hình ảnh, video, mô hình 3D và tệp được sử dụng trên toàn bộ cửa hàng của bạn. Tải lên tệp bằng cách kéo và thả chúng vào, tổ chức bằng thư mục và thẻ, và để hệ thống tự động tối ưu hóa hình ảnh để tải nhanh hơn.

![Thư viện phương tiện](/static/core/admin/img/help/media-library/media-gallery.webp)

## Giao diện Thư viện

Truy cập **Thư viện phương tiện** trong thanh bên để mở thư viện. Giao diện có ba khu vực:

| Khu vực | Vị trí | Mục đích |
|---------|--------|---------|
| **Khu vực Tải lên** | Thanh bên trái, phía trên | Kéo và thả tệp để tải lên (hình ảnh, video, mô hình 3D lên đến 100MB) |
| **Thư mục & Thẻ** | Thanh bên trái, bên dưới | Duyệt thư mục, lọc theo thẻ, truy cập Thùng rác |
| **Mạng lưới phương tiện** | Khu vực chính | Tìm kiếm, lọc, duyệt và quản lý tất cả tài sản của bạn |

### Điều khiển thanh công cụ

Thanh công cụ phía trên lưới phương tiện cung cấp:

- **Tìm kiếm** — tìm tài sản theo tiêu đề, văn bản thay thế, mô tả hoặc tên thẻ
- **Lọc theo loại** — chỉ hiển thị Hình ảnh, Video hoặc Mô hình 3D
- **Lọc theo kích thước** — lọc theo kích thước tệp (Nhỏ, Trung bình, Lớn)
- **Hành động theo khối** — Chọn mục, Chỉnh sửa chi tiết, Xóa đã chọn
- **Chế độ xem** — Mạng lưới (lớn), Mạng lưới nhỏ hoặc chế độ xem danh sách (duy trì qua các phiên làm việc)

## Tải lên tệp

Kéo một hoặc nhiều tệp vào khu vực **Tải lên** ở thanh bên trái, hoặc nhấp vào khu vực để mở trình chọn tệp.

### Định dạng được hỗ trợ

| Loại | Định dạng |
|------|---------|
| **Hình ảnh** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Video** | MP4, WebM, MOV, MKV, AVI |
| **Mô hình 3D** | GLB, glTF |

### Hàng đợi tải lên

Khi tải lên nhiều tệp, một quản lý hàng đợi sẽ xuất hiện hiển thị:

- Tên tệp và thanh tiến trình tải lên cho mỗi tệp
- Các tải lên đồng thời (tối đa 2 tại một thời điểm để đảm bảo hiệu suất)
- Trạng thái xử lý khi các tệp được tối ưu hóa sau khi tải lên
- Tùy chọn hủy bỏ các tải lên riêng lẻ hoặc xóa các mục đã hoàn thành

Hàng đợi có thể kéo và thu nhỏ để bạn có thể tiếp tục làm việc trong khi các tệp tải lên hoàn tất.

## Tối ưu hóa hình ảnh tự động

Mọi hình ảnh bạn tải lên đều được tối ưu hóa tự động:

- **Chuyển đổi WebP** — một phiên bản WebP được tạo ra cùng với tệp gốc (chất lượng 85%) để tải nhanh hơn
- **Tạo ảnh thu nhỏ** — tạo nhiều phiên bản kích thước khác nhau dựa trên cài đặt hình ảnh của bạn
- **Định hướng EXIF** — hình ảnh được xoay tự động để định hướng đúng

### Cài đặt hình ảnh hệ thống

Nền tảng bao gồm 21 cài đặt có sẵn bao phủ các trường hợp sử dụng phổ biến:

| Cài đặt | Kích thước | Cắt | Mục đích |
|--------|-----------|------|---------|
| **Ảnh thu nhỏ** | 150 x 150 | Cover | Danh sách quản trị, xem trước nhanh |
| **Nhỏ** | 300 x 300 | Cover | Thẻ sản phẩm nhỏ |
| **Trung bình** | 600 x 600 | Contain | Thẻ sản phẩm, ảnh thu nhỏ blog |
| **Lớn** | 1200 x 1200 | Contain | Trang chi tiết sản phẩm |
| **Thư viện** | 800 x 800 | Contain | Thư viện hình ảnh |
| **Hình ảnh chính** | 1920 x 1080 | Cover | Các phần chính, banner trang |
| **Banner** | 1200 x 400 | Cover | Banner quảng cáo |
| **Thẻ** | 400 x 300 | Cover | Thẻ tính năng, thẻ nội dung |
| **Ảnh đại diện** | 200 x 200 | Crop | Ảnh đại diện khách hàng và nhân viên |
| **Danh sách sản phẩm** | 400 x 400 | Cover | Thẻ lưới sản phẩm |
| **Chi tiết sản phẩm** | 1200 x 1200 | Cover | Hình ảnh sản phẩm đầy đủ |
| **Ảnh thu nhỏ sản phẩm** | 100 x 100 | Cover | Chọn biến thể, giỏ hàng nhỏ |
| **Banner danh mục** | 1920 x 480 | Cover | Tiêu đề trang danh mục |
| **Ảnh thu nhỏ danh mục** | 300 x 200 | Cover | Thẻ danh mục |
| **Logo đầu trang** | 300 x 80 | Pad | Logo đầu trang |
| **Logo chân trang** | 200 x 60 | Pad | Logo chân trang |
| **Logo email** | 400 x 100 | Pad | Logo mẫu email |
| **Logo vuông** | 160 x 160 | Pad | Vị trí logo vuông |
| **Logo thương hiệu** | 200 x 100 | Pad | Logo thương hiệu/thương mại |
| **Banner thông báo** | 800 x 300 | Cover | Hình ảnh thông báo |
| **Nền thông báo** | 1200 x 800 | Cover | Nền thông báo |

Cài đặt hệ thống không thể đổi tên hoặc xóa. Bạn có thể tạo thêm các cài đặt tùy chỉnh dưới **Thư viện phương tiện > Cài đặt kích thước hình ảnh** nếu bạn cần kích thước không được bao gồm trong cài đặt mặc định.

### Chế độ cắt

| Chế độ | Hành vi |
|--------|---------|
| **Cover** | Điền đầy toàn bộ khu vực, cắt các cạnh nếu cần — phù hợp cho các thẻ và banner |
| **Contain** | Thích hợp toàn bộ hình ảnh trong khu vực, thêm không gian trong suốt nếu cần — phù hợp cho hình ảnh sản phẩm |
| **Crop** | Cắt chính xác theo kích thước |
| **Pad** | Thích hợp hình ảnh và thêm khoảng trống (trong suốt, trắng hoặc đen) — phù hợp cho logo |

## Tổ chức tệp

### Thư mục

Tạo thư mục để tổ chức phương tiện của bạn thành các nhóm logic. Thư mục có thể được lồng ghép đến bất kỳ độ sâu nào. Nhấp vào thư mục trong thanh bên trái để chỉ hiển thị các tài sản bên trong nó. Liên kết **Tất cả tệp** hiển thị mọi thứ.

### Thẻ

Thêm thẻ cho tài sản để tổ chức chéo thư mục một cách linh hoạt. Thẻ xuất hiện dưới dạng đám mây trong thanh bên trái. Nhấp vào thẻ để lọc tài sản theo thẻ đó. Tài sản có thể có nhiều thẻ.

### Tìm kiếm

Thanh tìm kiếm tìm tài sản theo tiêu đề, văn bản thay thế, mô tả hoặc tên thẻ. Kết hợp tìm kiếm với bộ lọc loại và kích thước để có kết quả chính xác hơn.

## Chi tiết tài sản

Nhấp vào tài sản để mở chế độ xem chi tiết với xem trước lớn và toàn bộ thông tin kỹ thuật.

![Chi tiết tài sản](/static/core/admin/img/help/media-library/media-detail.webp)

Chế độ xem chi tiết hiển thị:

- **Xem trước** — xem trước hình ảnh lớn với kích thước gốc
- **Thông tin tệp** — loại, kích thước, kích thước tệp, ngày tải lên
- **Tab** để chỉnh sửa:

| Tab | Các trường |
|-----|--------|
| **Tổng quát** | Tiêu đề, Văn bản thay thế, Mô tả (tất cả đều có thể dịch cho các cửa hàng đa ngôn ngữ) |
| **Kỹ thuật** | Loại MIME, hash tệp, tên tệp gốc, trạng thái phiên bản WebP |
| **Tổ chức** | Gán thư mục, thẻ, chuyển đổi công khai/riêng tư |
| **Nâng cao** | Tọa độ điểm tập trung, ID bên ngoài, JSON thông tin kỹ thuật |

### Các trường có thể dịch

Tiêu đề, văn bản thay thế và mô tả hỗ trợ dịch. Nhấp vào biểu tượng dịch bên cạnh mỗi trường để thêm dịch cho các ngôn ngữ đã bật. Điều này đảm bảo hình ảnh có văn bản thay thế và mô tả được địa phương hóa đúng cách cho SEO và tính khả dụng.

### Theo dõi việc sử dụng

Hệ thống theo dõi nơi mỗi tài sản được sử dụng trên toàn nền tảng. Phần **Sử dụng phương tiện** ở phía dưới hiển thị mọi mô hình và trường tham chiếu đến tài sản này, giúp bạn hiểu rõ tác động trước khi thực hiện thay đổi hoặc xóa.

## Hỗ trợ video

Các video được tải lên vào thư viện phương tiện sẽ được phân tích tự động:

- **Trích xuất thông tin kỹ thuật** — thời lượng, độ phân giải, tốc độ khung hình, bitrate và codec được thu thập
- **Hình ảnh bìa** — một ảnh thu nhỏ được tạo từ video để xem trước
- **Phát trực tiếp** — video hỗ trợ yêu cầu phạm vi để tìm kiếm mà không cần tải xuống toàn bộ tệp
- **Chuyển đổi tùy chọn** — video có thể được chuyển đổi thành định dạng WebM/AV1 tối ưu để phân phối nhanh hơn

## Thùng rác

Xóa một tài sản sẽ chuyển nó vào **Thùng rác** thay vì xóa vĩnh viễn. Điều này bảo vệ khỏi việc xóa nhầm.

| Hành động | Điều gì nó làm |
|----------|---------------|
| **Xóa** | Chuyển tài sản vào Thùng rác (xóa mềm) |
| **Khôi phục** | Trả lại tài sản đã xóa về vị trí ban đầu |
| **Xóa vĩnh viễn** | Loại bỏ tài sản và tất cả ảnh thu nhỏ của nó khỏi lưu trữ vĩnh viễn |
| **Xóa trống Thùng rác** | Xóa vĩnh viễn tất cả mục trong Thùng rác |

Nhấp vào **Thùng rác** trong thanh bên trái để xem và quản lý các tài sản đã xóa.

## Thư viện phương tiện được sử dụng ở đâu

Thư viện phương tiện được tích hợp trên toàn bộ nền tảng:

| Tính năng | Cách sử dụng phương tiện |
|----------|----------------------|
| **Thư viện sản phẩm** | Hình ảnh sản phẩm, hình ảnh biến thể, banner danh mục |
| **Blog** | Hình ảnh nổi bật, hình ảnh trong nội dung thông qua CKEditor |
| **Trình tạo trang** | Phần tử hình ảnh, nền hình ảnh chính, thành phần thư viện |
| **Trình tạo đầu/trang chân** | Hình ảnh logo, hình nền |
| **Cài đặt trang web** | Logo trang web và favicon |
| **Thông báo** | Hình ảnh thông báo và nền |
| **CKEditor** | Tất cả việc tải lên hình ảnh trong văn bản giàu có đều định tuyến qua thư viện phương tiện |
| **Chương trình khách hàng thân thiết** | Hình ảnh phần thưởng và cấp độ |

Khi bạn chọn một hình ảnh trong bất kỳ tính năng nào, thư viện phương tiện sẽ mở ra như một cửa sổ bật lên để duyệt và chọn dễ dàng.

## Một số mẹo

- **Sử dụng tiêu đề và văn bản thay thế mô tả** — thông tin kỹ thuật tốt cải thiện SEO và tính khả dụng. Hệ thống sử dụng văn bản thay thế trong thẻ hình ảnh trên toàn bộ cửa hàng.
- **Tạo thư mục tổ chức sớm** — tạo cấu trúc thư mục (ví dụ: Sản phẩm, Blog, Banner, Logo) trước khi tải lên nhiều tệp. Việc tổ chức khi tải lên sẽ dễ dàng hơn nhiều so với việc tổ chức lại sau này.
- **Sử dụng thẻ cho các danh mục xuyên suốt** — các thẻ như 'mùa vụ', 'khuyến mãi' hoặc 'lối sống' giúp bạn tìm thấy các tài sản xuyên suốt nhiều thư mục.
- **Kiểm tra việc sử dụng trước khi xóa** — phần theo dõi việc sử dụng hiển thị nơi tài sản được tham chiếu. Xóa tài sản được sử dụng có thể để lại hình ảnh bị hỏng trên cửa hàng của bạn.
- **Để WebP thực hiện công việc** — việc chuyển đổi WebP tự động thường làm giảm kích thước tệp từ 25-35% so với JPEG mà không làm mất chất lượng rõ rệt. Bạn không cần chuyển đổi hình ảnh thủ công trước khi tải lên.
- **Tạo cài đặt tùy chỉnh** — nếu bạn có bố cục độc đáo cần kích thước hình ảnh cụ thể, hãy tạo cài đặt tùy chỉnh thay vì thay đổi kích thước hình ảnh thủ công.