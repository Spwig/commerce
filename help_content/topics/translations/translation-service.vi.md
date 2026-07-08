---
title: Dịch thuật
---

Dịch thuật cung cấp các bản dịch được hỗ trợ bởi AI cho mô tả sản phẩm, nội dung trang, bài đăng blog, trường SEO và nội dung khác của cửa hàng của bạn. Các bản dịch được thực hiện cục bộ trên máy chủ của bạn hoặc thông qua các nhà cung cấp bên ngoài, vì vậy nội dung của bạn vẫn được bảo mật và bản dịch được thực hiện trong vài giây.

![Quản lý ngôn ngữ](/static/core/admin/img/help/translation-service/language-management.webp)

## Cách hoạt động

1. Bạn **kích hoạt ngôn ngữ** cho cửa hàng của mình (ví dụ: tiếng Anh, tiếng Đức, tiếng Nhật)
2. Khi bạn tạo hoặc chỉnh sửa nội dung (sản phẩm, trang, bài đăng blog), bạn viết bằng ngôn ngữ mặc định của mình
3. Nhấp vào **Dịch thuật** trên bất kỳ trường có thể dịch để tạo bản dịch AI sang các ngôn ngữ đang hoạt động của bạn
4. Các bản dịch được lưu trữ cùng với nội dung gốc và được cung cấp tự động dựa trên ngôn ngữ của người truy cập

## Quản lý ngôn ngữ

Di chuyển đến **Cài đặt > Ngôn ngữ** để quản lý ngôn ngữ của cửa hàng của bạn.

### Bảng điều khiển ngôn ngữ

Bảng điều khiển hiển thị:
- **Tổng số ngôn ngữ** — Tất cả các ngôn ngữ có sẵn trong hệ thống (100+)
- **Ngôn ngữ đang hoạt động** — Các ngôn ngữ hiện đang được kích hoạt cho cửa hàng của bạn
- **Bao phủ mô hình** — Số lượng ngôn ngữ mà mô hình dịch thuật đã cài đặt hỗ trợ

### Kích hoạt ngôn ngữ

1. Tìm ngôn ngữ trong cột **Ngôn ngữ có sẵn**
2. Nhấp vào ngôn ngữ để di chuyển nó đến cột **Ngôn ngữ đang hoạt động**
3. Ngôn ngữ sẽ ngay lập tức sẵn sàng cho việc dịch thuật và hiển thị trong trình chuyển đổi ngôn ngữ của cửa hàng của bạn

### Ngôn ngữ mặc định

Một ngôn ngữ được đánh dấu là **mặc định**. Đây là:
- Ngôn ngữ bạn viết nội dung
- Ngôn ngữ dự phòng khi bản dịch không tồn tại
- Ngôn ngữ được hiển thị khi khách truy cập chưa chọn sở thích

## Mô hình dịch thuật

Spwig bao gồm một động cơ dịch thuật AI cục bộ chạy hoàn toàn trên máy chủ của bạn — không dữ liệu nào được gửi đến các dịch vụ bên ngoài.

### Mô hình có sẵn

| Mô hình | Ngôn ngữ | Tốc độ | Chất lượng |
|---------|----------|--------|-----------|
| **M2M100-418M** | 100 | Nhanh | Tốt cho các cặp ngôn ngữ phổ biến |
| **M2M100-1.2B** | 100 | Trung bình | Chất lượng tốt hơn, sử dụng tài nguyên cao hơn |
| **NLLB-200** | 200+ | Trung bình | Bao phủ tốt nhất, bao gồm các ngôn ngữ hiếm |

### Chọn mô hình

Trang quản lý ngôn ngữ hiển thị mô hình nào được cài đặt và phạm vi ngôn ngữ của nó. Mô hình chạy như một dịch vụ cục bộ sử dụng CTranslate2 để suy luận hiệu quả.

## Nhà cung cấp bên ngoài

Đối với các cửa hàng ưa thích dịch thuật dựa trên đám mây hoặc cần chất lượng ngôn ngữ cụ thể, Spwig hỗ trợ các nhà cung cấp dịch thuật bên ngoài.

| Nhà cung cấp | Mô tả |
|--------------|--------|
| **DeepL** | Chất lượng dịch thuật cao cấp cho các ngôn ngữ châu Âu và châu Á |
| **Google Translate** | Phạm vi ngôn ngữ rộng với dịch thuật máy học thần kinh |
| **Azure Translator** | Dịch vụ dịch thuật thần kinh của Microsoft |
| **AWS Translate** | Dịch thuật máy của Amazon với hỗ trợ thuật ngữ tùy chỉnh |

### Kết nối nhà cung cấp

1. Di chuyển đến **Cài đặt > Nhà cung cấp dịch thuật**
2. Chọn nhà cung cấp và nhập khóa API của bạn
3. Thiết lập nhà cung cấp là động cơ dịch thuật được ưa chuộng
4. Các bản dịch sẽ sử dụng nhà cung cấp bên ngoài thay vì mô hình cục bộ

Bạn có thể sử dụng các nhà cung cấp bên ngoài cùng với mô hình cục bộ — ví dụ, sử dụng DeepL cho các ngôn ngữ châu Âu và mô hình cục bộ cho mọi thứ khác.

## Dịch thuật nội dung

### Dịch thuật cấp trường

Các trường có thể dịch (tên sản phẩm, mô tả, tiêu đề SEO, v.v.) hiển thị một **nút dịch** bên cạnh trường. Nhấp vào nó để:

1. **Dịch sang tất cả các ngôn ngữ đang hoạt động** — Tạo bản dịch cho mọi ngôn ngữ đang hoạt động cùng lúc
2. **Dịch sang một ngôn ngữ cụ thể** — Chọn các ngôn ngữ riêng lẻ để dịch

Các bản dịch sẽ xuất hiện trong tab ngôn ngữ của trình chỉnh sửa. Bạn có thể xem lại và chỉnh sửa thủ công bất kỳ bản dịch do máy tạo ra nào.

### Nhiệm vụ dịch thuật theo lô

Đối với lượng nội dung lớn, hãy sử dụng **nhiệm vụ dịch thuật theo lô**:

1. Di chuyển đến **Cài đặt > Nhiệm vụ dịch thuật**
2. Tạo một công việc mới bằng cách chọn:
   - **Loại nội dung** — Sản phẩm, trang, bài đăng blog, danh mục, v.v.
   - **Ngôn ngữ nguồn** — Ngôn ngữ để dịch từ
   - **Ngôn ngữ đích** — Một hoặc nhiều ngôn ngữ để dịch sang
   - **Phạm vi** — Tất cả nội dung, hoặc chỉ các trường chưa dịch
3. Gửi công việc — nó được thực hiện trong nền qua hàng đợi tác vụ
4. Theo dõi tiến độ trong danh sách công việc (đang chờ → đang xử lý → hoàn thành)

Các nhiệm vụ theo lô rất hữu ích khi bạn kích hoạt một ngôn ngữ mới và muốn dịch toàn bộ danh mục của bạn một lần.

## Quản lý dịch thuật

### Xem lại dịch thuật

Mỗi trường dịch thuật theo dõi:
- **Trạng thái dịch thuật** — Trường đó đã được dịch tự động, chỉnh sửa thủ công, hoặc đang thiếu
- **Trạng thái khóa** — Các bản dịch được khóa sẽ không bị ghi đè bởi các bản dịch tự động trong tương lai
- **Dịch thuật lần cuối** — Khi bản dịch được tạo hoặc chỉnh sửa lần cuối

### Khóa dịch thuật

Nếu bạn chỉnh sửa thủ công bản dịch do máy tạo ra để cải thiện nó, **khóa** trường đó để ngăn nó bị ghi đè khi lần dịch theo lô tiếp theo được thực hiện. Các trường được khóa sẽ bị bỏ qua trong quá trình dịch tự động.

### Bao phủ dịch thuật

Bảng theo dõi bao phủ hiển thị tỷ lệ phần trăm nội dung của bạn đã được dịch cho mỗi ngôn ngữ. Di chuyển đến **Cài đặt > Ngôn ngữ** để xem:
- Phần trăm hoàn thành theo ngôn ngữ
- Các loại nội dung nào có khoảng trống
- Các trường vẫn cần dịch

## Ghi đè dịch thuật giao diện người dùng

Ngoài nội dung sản phẩm và trang, bạn có thể tùy chỉnh các bản dịch của **chuỗi giao diện người dùng phía trước** — các nút, nhãn, thông báo và văn bản giao diện khác được hiển thị cho khách truy cập.

Di chuyển đến **Cài đặt > Ghi đè giao diện người dùng** để:
1. Tìm kiếm một chuỗi cụ thể (ví dụ: "Thêm vào giỏ hàng")
2. Nhập bản dịch ưa thích của bạn cho mỗi ngôn ngữ
3. Lưu — ghi đè sẽ có hiệu lực ngay lập tức

Có khoảng 300 chuỗi giao diện phía trước có sẵn để tùy chỉnh. Ghi đè có quyền ưu tiên cao hơn so với bản dịch mặc định.

## Mẹo

- Bắt đầu bằng cách chỉ kích hoạt các ngôn ngữ mà khách hàng của bạn thực sự sử dụng — bạn luôn có thể thêm nhiều hơn sau này.
- Sử dụng **mô hình AI cục bộ** cho các bản dịch hàng ngày — nó nhanh, riêng tư và không có chi phí cho mỗi bản dịch.
- Xem xét **DeepL** nếu bạn cần chất lượng cao nhất cho các ngôn ngữ châu Âu quan trọng — nó liên tục tạo ra các bản dịch tự nhiên hơn so với các mô hình chung.
- Luôn **xem lại các bản dịch do máy tạo ra** cho tên sản phẩm, thuật ngữ thương hiệu và nội dung quảng cáo — AI xử lý nội dung kỹ thuật tốt nhưng có thể bỏ qua sự tinh tế trong văn bản sáng tạo.
- **Khóa** bất kỳ bản dịch nào bạn đã chỉnh sửa thủ công để bảo vệ chúng khỏi bị ghi đè trong các lần dịch theo lô tiếp theo.
- Sử dụng **các nhiệm vụ dịch thuật theo lô** khi kích hoạt một ngôn ngữ mới để dịch toàn bộ danh mục của bạn trong một lần thay vì dịch từng sản phẩm một.
- Tùy chỉnh **ghi đè giao diện người dùng** để phù hợp với giọng điệu thương hiệu của bạn — ví dụ, thay đổi "Thêm vào giỏ hàng" thành "Mua ngay" nếu điều đó phù hợp hơn với cửa hàng của bạn.

Hãy nhớ: Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và thuật ngữ kỹ thuật chính xác như được hiển thị trong các quy tắc bảo tồn.