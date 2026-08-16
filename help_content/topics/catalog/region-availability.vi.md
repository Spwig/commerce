---
title: Khả dụng theo khu vực
---

Khả dụng theo khu vực kiểm soát những khu vực bán hàng nào mà sản phẩm của bạn có thể bán được, cũng như cách người mua bên ngoài những khu vực đó trải nghiệm danh mục của bạn. Sử dụng tính năng này khi sản phẩm chỉ được cấp phép cho một số quốc gia nhất định, khi hàng hóa được dành riêng cho thị trường địa phương, hoặc khi bạn đang triển khai sản phẩm mới theo từng khu vực.

Điều này dựa trên **Khu vực bán hàng**, nơi nhóm các quốc gia thành các thị trường được đặt tên (xem hướng dẫn Khu vực bán hàng để thiết lập chúng). Khi các khu vực của bạn đã tồn tại, bạn có thể giới hạn từng sản phẩm cho chúng và quyết định cách sản phẩm bị giới hạn xuất hiện với người mua không thể mua chúng.

## Giới hạn sản phẩm cho các khu vực cụ thể

Mỗi sản phẩm đều có cài đặt **Khả dụng theo khu vực** trên trang chỉnh sửa của nó. Mở **Sản phẩm > Tất cả sản phẩm**, chọn một sản phẩm và tìm nó ở phần **Trạng thái** bên cạnh **Trạng thái**, **Nổi bật**, và **Ẩn khỏi cửa hàng**.

![Phần Trạng thái của biểu mẫu chỉnh sửa sản phẩm, với bảng chọn Khả dụng theo khu vực được đặt thành "Chỉ ở các khu vực đã chọn" bên cạnh Nổi bật và Ẩn khỏi cửa hàng](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| Lựa chọn | Ý nghĩa của nó |
|--------|---------------|
| **Có sẵn ở tất cả các khu vực** | Không có giới hạn nào. Sản phẩm được bán ở mọi nơi. Đây là cài đặt mặc định cho mọi sản phẩm. |
| **Chỉ ở các khu vực đã chọn** | Danh sách cho phép. Sản phẩm chỉ được bán ở các khu vực bạn chọn dưới đây — ở mọi nơi khác, nó sẽ được xem là không có sẵn. |
| **Tất cả các khu vực trừ các khu vực đã chọn** | Danh sách chặn. Sản phẩm được bán ở mọi nơi *trừ* các khu vực bạn chọn dưới đây. |

### Chọn các khu vực

Dưới phần Trạng thái, một bảng có tiêu đề **Khả dụng theo khu vực (các khu vực đã chọn)** liệt kê các khu vực mà chế độ trên áp dụng.

1. Thiết lập **Khả dụng theo khu vực** thành **Chỉ ở các khu vực đã chọn** hoặc **Tất cả các khu vực trừ các khu vực đã chọn**.
2. Trong bảng **Khả dụng theo khu vực (các khu vực đã chọn)**, nhấp vào **Thêm Khu vực khác** và chọn một Khu vực bán hàng.
3. Lặp lại cho mỗi khu vực bạn muốn thêm.
4. Nhấp vào **Lưu**.

![Bảng dọc "Khả dụng theo khu vực (các khu vực đã chọn)" với các hàng Bắc Mỹ và châu Âu được thêm vào](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

Nếu **Khả dụng theo khu vực** được đặt thành **Có sẵn ở tất cả các khu vực**, mọi thứ trong bảng này sẽ bị bỏ qua — xóa chế độ bảng chọn trước nếu bạn muốn gỡ bỏ giới hạn mà không xóa các hàng đã chọn.

Để xem toàn bộ danh mục các quy tắc khu vực của mỗi sản phẩm trong một danh sách (thoải mái khi kiểm tra nhiều sản phẩm cùng lúc), hãy truy cập **Vị trí hiển thị sản phẩm theo khu vực** tại `/admin/catalog/productregionvisibility/`.

## Hiển thị cho người mua biết sản phẩm không giao đến khu vực của họ

Khi khu vực của người mua không khớp với các quy tắc khả dụng của sản phẩm, bạn kiểm soát điều mà họ thấy trong **Cài đặt hiển thị hàng tồn**, ở phần **Khả dụng theo khu vực**. Trang này vẫn chưa có phím tắt thanh bên — hãy mở trực tiếp tại `/admin/catalog/stockdisplaysettings/`.

![Cài đặt hiển thị hàng tồn, phần **Khả dụng theo khu vực** — bảng chọn **Hiển thị theo khu vực**, được đặt thành "Hiển thị, được đánh dấu là không có sẵn"](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| Lựa chọn | Người mua thấy gì |
|--------|-------------------|
| **Hiển thị, được đánh dấu là không có sẵn** (mặc định) | Sản phẩm vẫn xuất hiện trong danh sách, với nhãn "Không có sẵn" và thông báo "Không giao đến [khu vực]" thay cho nút "Thêm vào giỏ hàng". Một banner cũng xuất hiện ở đầu trang danh sách("Một số sản phẩm không giao đến [đích đến]") với liên kết để lọc chỉ những mặt hàng có thể giao đến đó. |
| **Ẩn khỏi danh sách** | Sản phẩm bị xóa khỏi danh sách và kết quả tìm kiếm hoàn toàn cho người mua ở khu vực đó. |

![Trang danh sách sản phẩm cửa hàng, giao hàng đến châu Âu — banner "Một số sản phẩm không giao đến châu Âu" ở trên lưới, và một thẻ sản phẩm được đánh dấu là "Không có sẵn" với thông báo "Không giao đến châu Âu"](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

Trang của một sản phẩm bị giới hạn luôn hiển thị thông báo 'Sản phẩm này không giao đến [vùng]' khi người mua truy cập trực tiếp (ví dụ: từ một liên kết chia sẻ hoặc kết quả của công cụ tìm kiếm) — điều này áp dụng bất kể bạn chọn tùy chọn danh sách nào ở trên, vì một liên kết trực tiếp sẽ bỏ qua danh sách hoàn toàn.

## Cho phép người mua chọn hoặc phát hiện vùng của họ

Spwig có thể phát hiện vùng của người mua một cách tự động và cung cấp tùy chọn chuyển đổi, bạn có thể thêm một trình chọn để người mua có thể thay đổi vùng của họ bất cứ lúc nào.

### Trước khi bắt đầu

Bạn cần hai thứ được cấu hình đúng để phát hiện và chuyển đổi vùng hoạt động chính xác:

1. **Vùng bán hàng** — các quốc gia trong mỗi vùng và đồng tiền mặc định của mỗi vùng. Nếu bạn không thấy **Vùng bán hàng** dưới **Kho hàng** trong thanh điều hướng, hãy bật **Kích hoạt Kho hàng đa địa điểm** dưới **Cài đặt > Cài đặt Cửa hàng > Thương mại điện tử** để hiển thị liên kết menu (bạn không cần phải sử dụng kho hàng đa địa điểm — cài đặt này chỉ kích hoạt liên kết menu). Bạn cũng có thể truy cập trực tiếp vào `/admin/catalog/salesregion/`.
2. **Quốc gia vận chuyển** — các quốc gia mà cửa hàng của bạn thực sự giao hàng. Những quốc gia này thường đã được thiết lập: mọi quốc gia bạn thêm vào một Khu vực vận chuyển sẽ được thêm vào đây tự động. Để xem lại hoặc điều chỉnh thủ công danh sách, hãy mở trực tiếp `/admin/shipping/shippingcountry/` (nó cũng chưa có liên kết thanh điều hướng).

### Xác nhận vùng tự động

Spwig phát hiện vùng của người mua dựa trên vị trí của họ và áp dụng nó một cách tự động. Khi điều này khiến họ ở trong một vùng *khác* so với thị trường chính (thị trường mặc định) của cửa hàng bạn — và bạn có hai hoặc nhiều Vùng bán hàng hoạt động — Spwig sẽ hiển thị một thông báo xác nhận trên lần truy cập đầu tiên của họ để họ biết họ đang ở vùng nào và có thể thay đổi được:

> **Chúng tôi đã đặt vùng của bạn là [Vùng]**
> Chúng tôi đã chọn dựa trên vị trí của bạn để bạn xem được sản phẩm và giá cả phù hợp. Không đúng? Chọn quốc gia của bạn.
> Giao đến: [trình chọn quốc gia]  **[Tiếp tục mua sắm]**

![Thông báo 'Chúng tôi đã đặt vùng của bạn là Bắc Mỹ' trên giao diện cửa hàng, với trình chọn quốc gia 'Giao đến' và nút 'Tiếp tục mua sắm'](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Việc chọn quốc gia khác trong trình chọn sẽ chuyển đổi vùng của họ ngay lập tức. Việc đóng thông báo hoặc nhấp vào **Tiếp tục mua sắm** sẽ giữ nguyên vùng hiện tại của họ, và họ sẽ không bị hỏi lại trên trình duyệt này. Những người truy cập đang ở trong vùng mặc định của cửa hàng sẽ không bao giờ được hiển thị thông báo này.

### Thêm trình chọn Giao đến vào tiêu đề hoặc chân trang

Nếu bạn muốn người mua thay đổi vùng của họ bất cứ lúc nào (thay vì chỉ dựa vào thông báo tự động), hãy thêm **Trình chọn Giao đến** vào tiêu đề hoặc chân trang của bạn.

1. Điều hướng đến **Thiết kế > Người xây dựng Tiêu đề** (hoặc **Người xây dựng Chân trang**).
2. Kéo **Trình chọn Giao đến** từ Thư viện Widget vào một hàng.
3. Nhấp vào **Lưu**.

![Thư viện widget Người xây dựng Tiêu đề với nhóm Shop được chọn, hiển thị trình chọn Giao đến cùng với Giỏ hàng, Menu Tài khoản và Trình chọn Ngôn ngữ](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

Trình chọn này không cần cài đặt — nó liệt kê tự động các Quốc gia vận chuyển đang hoạt động của bạn, và hiển thị lựa chọn hiện tại của người mua (hoặc quốc gia được phát hiện bởi GeoIP, nếu họ chưa chọn). Việc chọn quốc gia khác sẽ cập nhật vùng của họ ngay lập tức và làm mới khả năng có sẵn và giá sản phẩm của trang.

Trình chọn Giao đến chưa có biểu mẫu cài đặt riêng. Nếu bạn muốn thay đổi kiểu nút (viền, đầy đủ hoặc mờ) hoặc ẩn nhãn 'Giao đến', hãy mở cài đặt của trình chọn trong người xây dựng và chỉnh sửa trường **Cấu hình tùy chỉnh (JSON)** trực tiếp, sử dụng `button_style` và `show_label`.

### Đồng tiền theo vùng

Nếu cửa hàng của bạn hỗ trợ hơn một đồng tiền (được thiết lập dưới **Cài đặt > Đa đồng tiền**), việc chuyển đổi vùng — thông qua thông báo hoặc trình chọn Giao đến — cũng sẽ chuyển đổi đồng tiền được hiển thị thành đồng tiền mặc định của vùng đó.

Nếu cửa hàng của bạn chỉ có một loại tiền tệ, hoặc chưa bật rõ ràng loại thứ hai, tiền tệ sẽ không bị thay đổi khi người mua thay đổi khu vực.

## Mẹo

- Giữ **Tình trạng khu vực** ở **Có sẵn ở tất cả các khu vực** trừ khi bạn có lý do cụ thể để giới hạn sản phẩm — đây là tùy chọn đơn giản nhất và không cần bảo trì khi bạn thêm các khu vực sau này.
- Sử dụng **Chỉ ở một số khu vực** cho danh sách cho phép nhỏ (ví dụ: một sản phẩm ra mắt ở một quốc gia đầu tiên) và **Tất cả các khu vực trừ đã chọn** cho danh sách chặn nhỏ (ví dụ: mọi nơi trừ một quốc gia mà mặt hàng không được cấp phép) — hãy chọn tùy chọn nào cần ít hàng hơn để thiết lập.
- Nếu người mua báo cáo rằng sản phẩm bị thiếu nhưng nên hiển thị, hãy kiểm tra cả cài đặt **Tình trạng khu vực** của sản phẩm và xem quốc gia của họ có được bao phủ bởi **Khu vực bán hàng** đang hoạt động và **Quốc gia giao hàng** đang hoạt động hay không.
- **Ẩn khỏi danh sách** giúp danh mục của bạn trông sạch sẽ hơn cho người mua không thể mua một số mặt hàng, nhưng điều đó cũng có nghĩa là thương mại và tìm kiếm sẽ trông thưa thớt hơn ở những khu vực đó — **Hiển thị, được đánh dấu là không khả dụng** thường tốt hơn nếu bạn vẫn muốn người mua duyệt đầy đủ danh mục của bạn ngay cả khi họ không thể thanh toán.
- Kiểm tra hành vi khu vực bằng cách thêm **Người chọn giao hàng** vào header và chuyển đổi giữa các quốc gia của chính bạn trước khi dựa vào phát hiện GeoIP trong quá trình ra mắt.
- Thiết lập giá trị ưu tiên cho các khu vực của bạn một cách có chủ đích — khu vực có ưu tiên cao nhất đang hoạt động là lựa chọn thay thế cho người mua mà quốc gia của họ không thể phát hiện hoặc không khớp với bất kỳ khu vực nào.