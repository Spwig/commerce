---
title: Bán sản phẩm dưới dạng đăng ký
---

Bất kỳ sản phẩm Đơn giản, Biến đổi hoặc Số hóa nào cũng có thể được bán theo hình thức định kỳ, ngay bên cạnh — hoặc thay vì — một lần mua duy nhất. Hướng dẫn này bao gồm việc bật tính năng đăng ký cho sản phẩm, chọn các kế hoạch mà khách hàng có thể chọn, và điều mà khách hàng thực sự thấy khi mua sản phẩm.

<!-- screenshots-needed:
- url: /admin/catalog/product/{id}/change/
  filename: subscriptions-tab.webp
  description: Mẫu chỉnh sửa sản phẩm với tab Đăng ký được kích hoạt, cho thấy
    tùy chọn Bật Đăng ký được chọn, một hoặc nhiều kế hoạch được chọn trong trường Kế hoạch Đăng ký, và các tùy chọn Cho phép Mua một lần / Mặc định là Đăng ký
    hiển thị.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
- url: (storefront) trang chi tiết sản phẩm cho sản phẩm được bật đăng ký
  filename: subscribe-and-save-selector.webp
  description: Bộ chọn "Mua một lần" vs "Đăng ký và Tiết kiệm" được mở rộng, cho thấy danh sách cấp độ tần suất giao hàng với nhãn Tiết kiệm X% trên các cấp độ được giảm giá.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
  notes: Yêu cầu một sản phẩm được bật đăng ký thực tế với ít nhất một kế hoạch công khai hoạt động và các cấp độ giá, được xem từ cửa hàng (không phải admin).
-->

## Loại sản phẩm nào có thể được bán dưới dạng đăng ký

Chỉ có các loại sản phẩm sau đây mới có thể được bán dưới dạng đăng ký:

| Được phép | Không được phép |
|----------|---------------|
| Sản phẩm Đơn giản | Gói sản phẩm |
| Sản phẩm Biến đổi | Thẻ quà tặng |
| Sản phẩm Số hóa | Sản phẩm Có thể tùy chỉnh |
| | Sản phẩm Có thể cấu hình |
| | Sản phẩm Đặt chỗ |

Lý do là do giao hàng, không phải giá cả: một đăng ký sẽ tính phí khách hàng mỗi chu kỳ và giao sản phẩm thông qua một đơn hàng mới mỗi lần. Spwig biết cách giao hàng lại sản phẩm Đơn giản hoặc Biến đổi và cấp lại quyền tải xuống hoặc giấy phép cho sản phẩm Số hóa trên mỗi lần gia hạn — nhưng nó không thể an toàn chạy lại việc phát hành thẻ quà tặng, một gói nhiều thành phần, sự tùy chỉnh được lưu trữ của khách hàng, một bản xây dựng trình cấu hình, hoặc một khung thời gian đặt chỗ theo lịch trình định kỳ. Việc cho phép các loại sản phẩm này được bán dưới dạng đăng ký sẽ làm tăng rủi ro lấy tiền khách hàng ở chu kỳ 2 mà không thể giao hàng.

Lựa chọn **Bật Đăng ký** không bị ẩn hoặc mờ đi cho các loại sản phẩm không phù hợp — bạn có thể kiểm tra nó trên bất kỳ sản phẩm nào. Nếu bạn cố gắng lưu một sản phẩm Thẻ quà tặng, Gói, Có thể tùy chỉnh, Có thể cấu hình hoặc Đặt chỗ với đăng ký được bật, Spwig sẽ từ chối lưu với lỗi xác thực giải thích rằng loại sản phẩm này không thể được bán dưới dạng đăng ký. Thay đổi **Loại sản phẩm** trước (tab Thông tin cơ bản), hoặc để đăng ký tắt cho sản phẩm đó.

## Kích hoạt đăng ký cho sản phẩm

1. Truy cập **Sản phẩm > Tất cả sản phẩm** và mở sản phẩm bạn muốn bán dưới dạng đăng ký (hoặc tạo một sản phẩm mới).
2. Xác nhận **Loại sản phẩm** trên tab Thông tin cơ bản là Đơn giản, Biến đổi hoặc Số hóa.
3. Nhấp vào tab **Đăng ký**.
4. Chọn **Bật Đăng ký**.
5. Trong trường **Kế hoạch Đăng ký**, chọn một hoặc nhiều kế hoạch mà sản phẩm này nên cung cấp. Bạn chỉ có thể chọn các kế hoạch đã tồn tại — nếu bạn chưa tạo kế hoạch nào, hãy xem trước [Kế hoạch Đăng ký](/help/subscription-plans).
6. Cấu hình hai tùy chọn chế độ mua hàng (nằm dưới).
7. Nhấp vào **Lưu**.

## Gắn kế hoạch đăng ký

Một **Kế hoạch Đăng ký** là một mẫu có thể tái sử dụng — các tùy chọn chu kỳ thanh toán, giai đoạn thử, phí ban đầu, quy định hủy bỏ — mà bạn xây dựng một lần và có thể gắn với bất kỳ số lượng sản phẩm nào phù hợp. Trường **Kế hoạch Đăng ký** trên tab Đăng ký của sản phẩm là nơi bạn kết nối sản phẩm với các kế hoạch mà nó nên được bán.

Bạn có thể gắn nhiều kế hoạch hơn cho cùng một sản phẩm.

Điều này hữu ích khi, ví dụ, bạn muốn cung cấp một cấp độ "Chuẩn" và "Nâng cao" định kỳ cho cùng một mặt hàng — mỗi kế hoạch có thể mang theo các cấp độ giá, giai đoạn thử và chính sách hủy bỏ riêng.


Khi một sản phẩm có nhiều hơn một kế hoạch được gắn vào, khách hàng sẽ thấy bộ chọn kế hoạch trên trang sản phẩm trước khi chọn tần suất thanh toán.

## Kiểm soát các lần mua hàng một lần so với mua theo gói đăng ký

Hai tùy chọn trên tab Đăng ký kiểm soát cách khách hàng có thể mua sản phẩm:

- **Cho phép mua hàng một lần** — Được bật mặc định. Khi được chọn, khách hàng có thể chọn giữa một lần mua hàng thông thường và đăng ký. Bỏ chọn để sản phẩm chỉ có thể mua theo gói đăng ký — mọi lần mua hàng đều trở thành đơn hàng lặp lại, và không có tùy chọn mua một lần nào cả.
- **Mặc định là đăng ký** — Chọn trước tùy chọn đăng ký (và kế hoạch/tầng mặc định) khi trang sản phẩm được tải, thay vì buộc khách hàng phải chọn chủ động. Điều này chỉ có hiệu lực khi **Cho phép mua hàng một lần** cũng được chọn — nếu mua hàng một lần bị tắt, sản phẩm sẽ chỉ có thể mua theo gói đăng ký bất kể cài đặt này.

Hãy sử dụng **Mặc định là đăng ký** cho các sản phẩm mà việc giao hàng định kỳ là kỳ vọng tự nhiên (cà phê, thực phẩm chức năng, hàng tiêu dùng) — điều này giúp loại bỏ một lần nhấp chuột và thúc đẩy khách hàng chọn lựa giữ chân họ quay lại, mà không làm mất đi khả năng mua một lần của họ.

## Những gì khách hàng nhìn thấy

### Trên trang sản phẩm

Khi sản phẩm có đăng ký được bật và có ít nhất một kế hoạch hoạt động, công cụ chọn chế độ mua hàng xuất hiện trên trang sản phẩm:

- Nếu mua hàng một lần được phép, khách hàng sẽ thấy lựa chọn **"Mua một lần"** so với **"Đăng ký & Tiết kiệm"**, mặc định là chế độ bạn đã cấu hình.
- Nếu sản phẩm có nhiều hơn một kế hoạch được gắn, bộ chọn kế hoạch sẽ xuất hiện khi chọn "Đăng ký & Tiết kiệm".
- Đối với kế hoạch được chọn, khách hàng sẽ thấy danh sách **tần suất giao hàng** được xây dựng từ các cấp độ giá của kế hoạch đó (ví dụ: Hàng tháng, Hàng quý, Hàng năm), mỗi cấp độ hiển thị giá của nó và một **biểu tượng "Tiết kiệm X%"** khi cấp độ đó có khuyến mãi.
- Thời gian dùng thử, phí thiết lập và chính sách hủy bỏ của kế hoạch (ví dụ: "Hủy bất kỳ lúc nào") sẽ được hiển thị bên cạnh danh sách cấp độ, cùng với ghi chú rằng phương thức thanh toán sẽ được thêm vào lúc thanh toán.

### Trong giỏ hàng và lúc thanh toán

Các mục hàng hóa đăng ký trong giỏ hàng sẽ có **dấu hiệu "Đăng ký"**, tần suất thanh toán (ví dụ: "Mỗi tháng"), và ghi chú dùng thử nếu có, để khách hàng dễ dàng nhận biết các mục lặp lại. Tại trang thanh toán, khách hàng chọn nhà cung cấp thanh toán như bình thường — đây là phương thức thanh toán sẽ được tính phí cho các lần gia hạn sau.

> **Hạn chế đã biết:** Việc lưu trữ thẻ của khách hàng tự động cho các lần gia hạn đăng ký tại trang thanh toán vẫn đang được kết nối cho một số nhà cung cấp thanh toán. Trong khi nhà cung cấp cụ thể không hỗ trợ điều này, các gói đăng ký được đặt thông qua nó có thể cần thêm theo dõi (ví dụ: liên hệ khách hàng để cập nhật thông tin thanh toán trước khi gia hạn) thay vì được thực hiện tự động ngay từ đầu. Hãy kiểm tra cài đặt nhà cung cấp thanh toán của bạn nếu bạn nhận thấy các lần gia hạn không được tính phí tự động cho một gói đăng ký.

## Mẹo sử dụng

- Tạo và kiểm tra kế hoạch đăng ký trước (các cấp độ giá, thời gian dùng thử, chính sách hủy), sau đó gắn nó với sản phẩm — dễ dàng hơn để cấu hình kế hoạch đúng đắn một lần hơn là sửa chữa nó trên nhiều sản phẩm sau này.
- Giữ nguyên **Cho phép mua hàng một lần** được chọn cho hầu hết các sản phẩm. Chỉ sử dụng sản phẩm chỉ có thể mua theo gói đăng ký trong trường hợp mua một lần thực sự không hợp lý với doanh nghiệp của bạn.
- Nếu bạn đang chuyển đổi một sản phẩm bán chạy thành tùy chọn đăng ký, hãy để **Mặc định là đăng ký** ở chế độ tắt ban đầu để không làm gián đoạn khách hàng quen với việc mua một lần — bật nó lên sau khi bạn đã thấy phản hồi từ người đăng ký.
- Các sản phẩm kỹ thuật số là lựa chọn lý tưởng cho các gói đăng ký (giấy phép phần mềm, thành viên nội dung) vì việc gia hạn tự động cấp lại quyền truy cập mà không cần vận chuyển.
- Nếu bạn cần một loại sản phẩm không đủ điều kiện (một gói hoặc mặt hàng có thể tùy chỉnh, ví dụ) để bán theo chu kỳ, hãy xem xét xem liệu một phiên bản đơn giản hoặc kỹ thuật số tương đương có thể mang theo gói đăng ký thay thế hay không.