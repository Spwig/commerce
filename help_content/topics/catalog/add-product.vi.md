---
title: Thêm sản phẩm
---

Hướng dẫn này sẽ hướng dẫn bạn tạo sản phẩm mới trong cửa hàng của bạn. Các sản phẩm được tổ chức qua nhiều tab — Thông tin cơ bản, Hình ảnh, Giá cả, Kho hàng và SEO — để bạn có thể điền đầy đủ mọi thứ một lần hoặc quay lại hoàn thành các phần sau này.

## Getting Started

Từ thanh bên, truy cập **Products > All Products** để xem danh mục sản phẩm của bạn. Nhấp vào nút **+ Add Product** ở góc trên bên phải để mở biểu mẫu tạo sản phẩm.

![Product list page](/static/core/admin/img/help/add-product/product-list-page.webp)

## Basic Info Tab

Tab **Basic Info** là nơi bạn xác định các chi tiết cốt lõi của sản phẩm.

![Add product form](/static/core/admin/img/help/add-product/add-product-form.webp)

### Required Fields

- **Name** — Tên sản phẩm được hiển thị cho khách hàng. Nhấp vào biểu tượng quả địa cầu để thêm bản dịch cho các ngôn ngữ khác.
- **Slug** — Phiên bản thân thiện với URL của tên (tự động tạo). Tắt chế độ "Auto" để tùy chỉnh nó.
- **SKU** — Mã đơn vị quản lý hàng tồn kho nội bộ của bạn.
- **Product Type** — Chọn từ: Simple, Variable, Digital, Bundle, Gift Card, Customizable, hoặc Configurable.
- **Status** — Đặt thành Draft khi đang làm việc, sau đó thay đổi thành Published khi đã sẵn sàng.

### Optional Fields

- **Category** — Gán sản phẩm vào danh mục để tổ chức và điều hướng cửa hàng.
- **Brand** — Liên kết với thương hiệu nếu phù hợp.
- **Is Featured** — Chọn để làm nổi bật sản phẩm này trên cửa hàng.
- **Is Digital Product** — Chọn nếu sản phẩm này bao gồm các tải xuống kỹ thuật số (tệp, giấy phép).
- **Hide from Storefront** — Ẩn sản phẩm khỏi danh sách cửa hàng nhưng vẫn giữ khả năng sử dụng như tùy chọn cấu hình hoặc thành phần gói.

### Product Descriptions

- **Short Description** — Hiển thị trong danh sách sản phẩm và các thẻ. Giữ ngắn gọn và hấp dẫn.
- **Full Description** — Mô tả chi tiết sản phẩm được hiển thị trên trang chi tiết sản phẩm. Sử dụng trình chỉnh sửa văn bản phong phú để thêm định dạng, hình ảnh, video và bảng.

Cả hai trường mô tả đều hỗ trợ tính năng bản dịch — nhấp vào biểu tượng quả địa cầu để cung cấp nội dung cho các ngôn ngữ khác.

## Media Tab

Tab **Media** cho phép bạn quản lý hình ảnh sản phẩm bằng Thư viện Media tích hợp.

![Media tab](/static/core/admin/img/help/add-product/media-tab.webp)

1. Nhấp **+ Add Images from Media Library** để mở trình chọn media.
2. Chọn hình ảnh hiện có hoặc tải lên hình ảnh mới trực tiếp.
3. Kéo hình ảnh để sắp xếp lại — hình ảnh **đầu tiên** sẽ trở thành hình ảnh chính của sản phẩm được hiển thị trong danh sách và các thẻ.
4. Chọn **Gallery Type** để kiểm soát cách hiển thị hình ảnh trên trang sản phẩm: Standard Gallery, Carousel, Grid Layout, Zoom Gallery, hoặc 360° View.

## Pricing Tab

Thiết lập giá sản phẩm và cấu hình khuyến mãi.

![Pricing tab](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Regular Pricing

- **Regular Price** — Giá bán lẻ tiêu chuẩn mà khách hàng sẽ nhìn thấy.
- **Currency** — Chọn loại tiền tệ (loại tiền tệ mặc định của cửa hàng bạn đã được chọn trước).
- **Cost** — Chi phí hàng hóa của bạn, được sử dụng để tính toán lợi nhuận. Điều này sẽ không bao giờ được hiển thị cho khách hàng.

### Sale Settings

Cấu hình các giảm giá tạm thời:

- **Sale Type** — Chọn từ: No Sale, Fixed Sale Price, Amount Off, hoặc Percentage Off.
- **Sale Value** — Số tiền giảm giá hoặc tỷ lệ phần trăm.
- **Start/End Dates** — Lên lịch thời gian khuyến mãi bắt đầu và kết thúc. Để trống nếu muốn bắt đầu ngay hoặc không có ngày kết thúc.

## Inventory Tab

Quản lý mức tồn kho và các thuộc tính sản phẩm vật lý.

![Inventory tab](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Stock Management

- **Track Inventory** — Kích hoạt để theo dõi số lượng tồn kho (mặc định là đã kích hoạt).
- **Low Stock Threshold** — Nhận thông báo khi tồn kho giảm xuống dưới con số này (mặc định: 5).
- **Stock Quantity** — Tổng số lượng đơn vị có sẵn.
- **Allow Backorders** — Kích hoạt để chấp nhận đơn hàng ngay cả khi hết hàng.

### Physical Attributes

Nhập trọng lượng (kg) và kích thước (chiều dài, chiều rộng, chiều cao tính bằng cm) của sản phẩm để tính toán giao hàng chính xác.

### Product Identifiers

Mã sản phẩm tiêu chuẩn cho danh sách thị trường và hệ thống tồn kho:

- **GTIN** — Global Trade Item Number
- **EAN** — European Article Number
- **UPC** — Universal Product Code (US)
- **ISBN** — Cho sách
- **ASIN** — Mã định danh của Amazon
- **MPN** — Số phần tử của nhà sản xuất

### International Shipping / Customs

Yêu cầu cho các đơn hàng quốc tế:

- **HS Code** — Mã phân loại hệ thống hài hòa
- **Country of Origin** — Nơi sản phẩm được sản xuất
- **Customs Unit Price** — Giá trị khai báo cho mỗi đơn vị để hải quan

## SEO Tab

Tối ưu khả năng hiển thị của sản phẩm trên công cụ tìm kiếm.

![SEO tab](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Meta Title** — Tiêu đề được hiển thị trong kết quả tìm kiếm của công cụ tìm kiếm. Nhấp vào biểu tượng quả địa cầu để bản dịch.
- **Meta Description** — Mô tả ngắn cho kết quả tìm kiếm (tối đa 160 ký tự). Nhấp vào biểu tượng quả địa cầu để bản dịch.
- **Auto-generate SEO** — Chọn để tự động tạo nội dung SEO khi sản phẩm được lưu.

**Kết quả tìm kiếm trực tiếp** hiển thị chính xác cách sản phẩm của bạn sẽ xuất hiện trong kết quả tìm kiếm Google.

## Saving Your Product

Khi bạn đã sẵn sàng, sử dụng các nút lưu ở góc trên bên phải:

- **Save** (biểu tượng checkmark) — Lưu và giữ ở trang sản phẩm.
- **Save and continue editing** — Lưu và tiếp tục ở biểu mẫu để tiếp tục làm việc.

Sản phẩm của bạn sẽ hiển thị trên cửa hàng khi trạng thái của nó được đặt thành **Published**.

## Tips

- Bắt đầu với trạng thái **Draft** để bạn có thể hoàn thiện sản phẩm trước khi khách hàng nhìn thấy nó.
- Tải lên nhiều hình ảnh — sản phẩm với nhiều hình ảnh sẽ chuyển đổi tốt hơn.
- Điền đầy đủ các trường **SEO** để cải thiện khả năng phát hiện trên công cụ tìm kiếm.
- Sử dụng **Categories** và **Brands** để giúp khách hàng điều hướng danh mục của bạn.
- Đối với các sản phẩm biến thể (ví dụ, kích cỡ hoặc màu sắc khác nhau), chọn loại **Variable Product** và thêm các biến thể sau khi lưu.
