---
title: Khả dụng theo khu vực
---

Khả dụng theo khu vực kiểm soát những khu vực bán hàng nào mà sản phẩm của bạn có thể bán được, cũng như cách người mua bên ngoài những khu vực đó trải nghiệm danh mục của bạn. Sử dụng tính năng này khi sản phẩm chỉ được cấp phép cho một số quốc gia nhất định, khi hàng hóa được dành riêng cho thị trường địa phương, hoặc khi bạn đang triển khai sản phẩm mới theo từng khu vực.

Tính năng này dựa trên **Khu vực bán hàng**, nơi nhóm các quốc gia thành các thị trường được đặt tên (xem hướng dẫn Khu vực bán hàng để thiết lập chúng). Khi các khu vực của bạn đã tồn tại, bạn có thể giới hạn từng sản phẩm cho chúng và quyết định cách sản phẩm bị giới hạn xuất hiện với người mua không thể mua chúng.

## Giới hạn sản phẩm cho các khu vực cụ thể

Mỗi sản phẩm đều có cài đặt **Khả dụng theo khu vực** trên trang chỉnh sửa của nó. Mở **Sản phẩm > Tất cả sản phẩm**, chọn một sản phẩm và tìm nó ở phần **Trạng thái** bên cạnh **Trạng thái**, **Nổi bật**, và **Ẩn khỏi cửa hàng**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-field.webp
  description: Product edit page scrolled to the Status section, with the Region availability dropdown visible and set to "Only in selected regions"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Use a product with at least 2 regions already selected below, if possible, so the inline table has visible rows in the second screenshot.
-->

| Tùy chọn | Điều đó có nghĩa là gì |
|--------|---------------|
| **Có sẵn ở tất cả các khu vực** | Không có giới hạn nào. Sản phẩm được bán ở mọi nơi. Đây là cài đặt mặc định cho mọi sản phẩm. |
| **Chỉ ở các khu vực đã chọn** | Danh sách cho phép. Sản phẩm chỉ được bán ở các khu vực bạn chọn dưới đây — ở mọi nơi khác, nó sẽ được xem là không có sẵn. |
| **Tất cả các khu vực trừ các khu vực đã chọn** | Danh sách chặn. Sản phẩm được bán ở mọi nơi *trừ* các khu vực bạn chọn dưới đây. |

### Chọn các khu vực

Dưới phần Trạng thái, một bảng có tiêu đề **Khả dụng theo khu vực (các khu vực đã chọn)** liệt kê các khu vực mà chế độ trên áp dụng.

1. Thiết lập **Khả dụng theo khu vực** thành **Chỉ ở các khu vực đã chọn** hoặc **Tất cả các khu vực trừ các khu vực đã chọn**.
2. Trong bảng **Khả dụng theo khu vực (các khu vực đã chọn)**, nhấp vào **Thêm khu vực khác** và chọn một **Khu vực bán hàng**.
3. Lặp lại cho mỗi khu vực bạn muốn thêm.
4. Nhấp vào **Lưu**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-inline.webp
  description: The "Region availability (selected regions)" inline table with two or three region rows added
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Nếu **Khả dụng theo khu vực** được đặt thành **Có sẵn ở tất cả các khu vực**, mọi thứ trong bảng này sẽ bị bỏ qua — xóa chế độ dropdown trước nếu bạn muốn gỡ bỏ giới hạn mà không xóa các hàng đã chọn.

Để xem toàn bộ danh mục về các quy tắc khu vực của mỗi sản phẩm trong một danh sách (thoải mái khi kiểm tra nhiều sản phẩm cùng lúc), hãy truy cập **Vùng hiển thị sản phẩm** tại `/admin/catalog/productregionvisibility/`.

## Hiển thị cho người mua biết sản phẩm không giao đến khu vực của họ

Khi khu vực của người mua không khớp với các quy tắc khả dụng của sản phẩm, bạn kiểm soát điều mà họ thấy trong **Cài đặt hiển thị hàng tồn**, dưới phần **Khả dụng theo khu vực**. Trang này vẫn chưa có phím tắt thanh bên — hãy mở trực tiếp tại `/admin/catalog/stockdisplaysettings/`.

<!-- screenshots-needed:
- url: /en/admin/catalog/stockdisplaysettings/1/change/
  filename: stock-display-region-availability.webp
  description: Stock Display Settings change form scrolled to the "Region Availability" fieldset, showing the Region-restricted display dropdown
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật.

| Option | Điều mà người mua hàng nhìn thấy |
|--------|-------------------|
| **Hiện, được đánh dấu là không khả dụng** (mặc định) | Sản phẩm vẫn xuất hiện trong danh sách, với nhãn "Không khả dụng" và thông báo "Không giao hàng đến [vùng miền]" thay cho nút "Thêm vào giỏ". Một banner cũng xuất hiện ở đầu trang danh sách ("Một số sản phẩm không giao hàng đến [đích đến]") với liên kết để lọc xuống các mặt hàng chỉ giao đến đó. |
| **Ẩn khỏi danh sách** | Sản phẩm bị xóa khỏi danh sách và kết quả tìm kiếm hoàn toàn cho người mua hàng ở vùng đó. |

<!-- screenshots-needed:
- url: /en/products/
  filename: storefront-region-restricted-listing.webp
  description: Danh sách sản phẩm cửa hàng với banner vùng ở đầu và ít nhất một thẻ sản phẩm hiển thị nhãn "Không khả dụng" và thông báo "Không giao hàng đến [vùng miền]"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Yêu cầu một lựa chọn giao hàng đến (hoặc phát hiện GeoIP) đang hoạt động, xác định đến một vùng mà sản phẩm mẫu bị hạn chế.
-->

Một trang sản phẩm bị hạn chế luôn hiển thị thông báo "Sản phẩm này không giao hàng đến [vùng miền]" khi người mua truy cập trực tiếp (ví dụ: từ liên kết chia sẻ hoặc kết quả của công cụ tìm kiếm) — điều này áp dụng bất kể bạn chọn tùy chọn nào ở trên, vì một liên kết trực tiếp sẽ bỏ qua danh sách hoàn toàn.

## Cho phép người mua hàng chọn hoặc phát hiện vùng của họ

Spwig có thể phát hiện vùng của người mua hàng tự động và cung cấp tùy chọn thay đổi, bạn có thể thêm một bộ chọn để người mua hàng thay đổi vùng của họ bất cứ lúc nào.

### Trước khi bắt đầu

Bạn cần hai thứ được cấu hình đúng để phát hiện và chuyển đổi vùng hoạt động chính xác:

1. **Vùng bán hàng** — các quốc gia trong mỗi vùng và đồng tiền mặc định của mỗi vùng. Nếu bạn không thấy **Vùng bán hàng** dưới **Kho hàng** trong thanh bên, hãy bật **Kích hoạt Kho hàng đa địa điểm** dưới **Cài đặt > Cài đặt Cửa hàng > Thương mại điện tử** để hiển thị liên kết menu (bạn không cần phải sử dụng kho hàng đa địa điểm — cài đặt này chỉ mở khóa liên kết menu). Bạn cũng có thể truy cập trực tiếp vào `/admin/catalog/salesregion/`.
2. **Quốc gia giao hàng** — các quốc gia mà cửa hàng của bạn thực sự giao hàng. Những quốc gia này thường đã được thiết lập: mọi quốc gia bạn thêm vào một Khu vực giao hàng sẽ được thêm tự động vào đây. Để xem lại hoặc điều chỉnh thủ công danh sách, hãy mở trực tiếp `/admin/shipping/shippingcountry/` (nó cũng chưa có liên kết thanh bên).

### Xác nhận vùng tự động

Spwig phát hiện vùng của người mua hàng từ vị trí của họ và áp dụng nó một cách tự động. Khi điều này đặt họ vào một vùng *khác* so với thị trường chính (thị trường mặc định) của cửa hàng của bạn — và bạn có hai hoặc nhiều **Vùng bán hàng** đang hoạt động — Spwig hiển thị một xác nhận trên lần truy cập đầu tiên của họ để họ biết họ đang ở vùng nào và có thể thay đổi nó:

> **Chúng tôi đã đặt vùng của bạn là [Vùng]**
> Chúng tôi đã chọn dựa trên vị trí của bạn để bạn xem các sản phẩm và giá cả phù hợp. Không đúng? Chọn quốc gia của bạn.
> Giao đến: [bộ chọn quốc gia]  **[Tiếp tục mua sắm]**

<!-- screenshots-needed:
- url: /en/
  filename: region-confirmation-modal.webp
  description: Màn hình xác nhận "Chúng tôi đã đặt vùng của bạn là [Vùng]" trên trang chủ cửa hàng, với bộ chọn quốc gia và nút "Tiếp tục mua sắm"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Yêu cầu GeoIP xác định đến một vùng không phải là vùng mặc định và ít nhất 2 Vùng bán hàng đang hoạt động để kích hoạt. Trong nước, đặt cookie "geo_country" đến một quốc gia không phải là vùng mặc định để mô phỏng.
-->

Việc chọn quốc gia khác trong bộ chọn sẽ chuyển đổi vùng của họ ngay lập tức. Việc đóng khung xác nhận hoặc nhấp vào **Tiếp tục mua sắm** sẽ giữ nguyên vùng hiện tại của họ, và họ sẽ không bị hỏi lại trên trình duyệt đó. Những người truy cập đang ở trong vùng mặc định của bạn sẽ không bao giờ được hiển thị xác nhận này.

### Thêm bộ chọn Giao đến vào đầu trang hoặc chân trang

Nếu bạn muốn người mua hàng thay đổi vùng của họ bất cứ lúc nào (thay vì chỉ dựa vào vào màn hình xác nhận tự động), hãy thêm **Bộ chọn Giao đến** vào đầu trang hoặc chân trang của bạn.

1.

Chuyển đến **Thiết kế > Người xây dựng Header** (hoặc **Người xây dựng Footer**).
2.

Kéo **Widget Ship-To Selector** từ Thư viện Widget vào một hàng.
3.

Nhấp vào **Lưu**.

<!-- screenshots-needed:
- url: /en/theme/header/builder/
  filename: ship-to-selector-widget-library.webp
  description: Header Builder với thanh bên Thư viện Widget mở và widget Ship-To Selector được hiển thị/nổi bật
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Widget này không cần thiết lập — nó liệt kê các Quốc gia Giao hàng đang hoạt động của bạn tự động, và hiển thị lựa chọn hiện tại của người mua (hoặc quốc gia được phát hiện bởi GeoIP, nếu họ chưa chọn bất kỳ quốc gia nào). Việc chọn quốc gia khác sẽ cập nhật khu vực của họ ngay lập tức và làm mới khả năng có sẵn và giá sản phẩm của trang web.

Widget Ship-To Selector hiện tại chưa có biểu mẫu cài đặt riêng. Nếu bạn muốn thay đổi kiểu nút (dáng viền, dáng đầy, hoặc dáng mờ), hoặc ẩn nhãn "Ship đến", hãy mở cài đặt của widget trong người xây dựng và chỉnh sửa trường **Cấu hình tùy chỉnh (JSON)** trực tiếp, sử dụng `button_style` và `show_label`.

### Tiền tệ theo khu vực

Nếu cửa hàng của bạn hỗ trợ hơn một loại tiền tệ (được thiết lập dưới **Cài đặt > Nhiều loại tiền tệ**), việc chuyển đổi khu vực — thông qua lời nhắc hoặc widget Ship-To Selector — cũng sẽ chuyển đổi tiền tệ được hiển thị thành tiền tệ mặc định của khu vực đó. Nếu cửa hàng của bạn chỉ có một loại tiền tệ, hoặc chưa bật rõ loại thứ hai, tiền tệ sẽ không thay đổi khi người mua thay đổi khu vực.

## Mẹo

- Giữ nguyên **Tình trạng khu vực** ở **Có sẵn ở tất cả các khu vực** trừ khi bạn có lý do cụ thể để giới hạn một sản phẩm — đó là tùy chọn đơn giản nhất và không cần bảo trì khi bạn thêm các khu vực sau này.
- Sử dụng **Chỉ có sẵn ở các khu vực đã chọn** cho một danh sách cho phép nhỏ (ví dụ: một sản phẩm ra mắt ở một quốc gia đầu tiên) và **Tất cả các khu vực trừ các khu vực đã chọn** cho một danh sách chặn nhỏ (ví dụ: mọi nơi trừ một quốc gia nơi mặt hàng không được cấp phép) — hãy chọn tùy chọn nào cần ít hàng hơn để thiết lập.
- Nếu người mua báo cáo rằng sản phẩm bị thiếu mà nên hiển thị, hãy kiểm tra cả cài đặt **Tình trạng khu vực** của sản phẩm và xem quốc gia của họ có được bao phủ bởi **Khu vực Bán hàng** đang hoạt động và **Quốc gia Giao hàng** đang hoạt động hay không.
- **Ẩn khỏi danh sách** giữ cho danh mục của bạn trông sạch sẽ cho người mua không thể mua một số mặt hàng, nhưng điều đó cũng có nghĩa là thương mại và tìm kiếm sẽ trông mỏng hơn ở các khu vực đó — **Hiển thị, được đánh dấu là không có sẵn** thường tốt hơn nếu bạn vẫn muốn người mua duyệt danh mục đầy đủ của bạn ngay cả khi họ không thể thanh toán.
- Kiểm tra hành vi khu vực bằng cách thêm widget Ship-To Selector vào header và chuyển đổi giữa các quốc gia của chính bạn trước khi dựa vào phát hiện GeoIP trong lần ra mắt.
- Thiết lập giá trị ưu tiên của các khu vực của bạn một cách có chủ đích — khu vực có ưu tiên cao nhất đang hoạt động là lựa chọn dự phòng cho những người mua mà quốc gia của họ không thể phát hiện hoặc không khớp với bất kỳ khu vực nào.