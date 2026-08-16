---
title: Bán sản phẩm dưới dạng đăng ký
---

Bất kỳ sản phẩm Đơn giản, Sản phẩm biến đổi hoặc Sản phẩm số nào cũng có thể được bán theo hình thức thanh toán định kỳ, ngay bên cạnh — hoặc thay vì — một lần mua duy nhất. Hướng dẫn này bao gồm việc bật tính năng đăng ký cho sản phẩm, chọn các kế hoạch mà khách hàng có thể chọn, và điều mà khách hàng thực sự thấy khi mua sản phẩm.

## Loại sản phẩm nào có thể được bán dưới dạng đăng ký

Chỉ có các loại sản phẩm sau đây mới có sẵn tính năng đăng ký:

| Được phép | Không được phép |
|----------|---------------|
| Sản phẩm Đơn giản | Gói sản phẩm |
| Sản phẩm Biến đổi | Thẻ quà tặng |
| Sản phẩm Số | Sản phẩm tùy chỉnh |
| | Sản phẩm Có thể cấu hình |
| | Sản phẩm Đặt chỗ |

Lý do là do quy trình giao hàng, không phải giá cả: một đăng ký sẽ tính phí khách hàng mỗi chu kỳ và giao sản phẩm thông qua một đơn hàng mới mỗi lần. Spwig biết cách giao hàng lại sản phẩm Đơn giản hoặc Sản phẩm Biến đổi và cấp lại quyền tải xuống hoặc giấy phép cho sản phẩm Số trên mỗi lần gia hạn — nhưng nó không thể an toàn chạy lại việc phát hành thẻ quà tặng, một gói nhiều thành phần, sự tùy chỉnh đã lưu của khách hàng, một bản xây dựng từ bộ tùy chọn, hoặc một khung thời gian đặt chỗ theo chu kỳ. Việc cho phép các loại sản phẩm này được bán dưới dạng đăng ký sẽ làm tăng rủi ro lấy tiền khách hàng ở chu kỳ 2 mà không thể giao hàng.

Hộp kiểm **Bật Đăng ký** không bị ẩn hoặc mờ đi cho các loại sản phẩm không đủ điều kiện — bạn có thể kiểm tra nó trên bất kỳ sản phẩm nào. Nếu bạn cố gắng lưu một sản phẩm Thẻ quà tặng, Gói sản phẩm, Tùy chỉnh, Có thể cấu hình hoặc Đặt chỗ với tính năng đăng ký được bật, Spwig sẽ từ chối lưu với lỗi xác thực giải thích rằng loại sản phẩm này không thể được bán dưới dạng đăng ký. Thay đổi **Loại sản phẩm** trước (thẻ Thông tin Cơ bản), hoặc để trống tính năng đăng ký cho sản phẩm đó.

## Bật tính năng đăng ký cho sản phẩm

1. Truy cập **Sản phẩm > Tất cả sản phẩm** và mở sản phẩm bạn muốn bán dưới dạng đăng ký (hoặc tạo một sản phẩm mới).
2. Xác nhận **Loại sản phẩm** trên tab Thông tin Cơ bản là Đơn giản, Biến đổi hoặc Số.
3. Nhấp vào tab **Đăng ký**.
4. Chọn **Bật Đăng ký**.
5. Trong trường **Kế hoạch Đăng ký**, chọn một hoặc nhiều kế hoạch mà sản phẩm này nên cung cấp. Bạn chỉ có thể chọn các kế hoạch đã tồn tại — nếu bạn chưa tạo kế hoạch nào cả, hãy xem trước [Kế hoạch Đăng ký](/help/subscription-plans).
6. Cấu hình hai tùy chọn kiểm tra chế độ mua hàng (nằm dưới đây).
7. Nhấp vào **Lưu**.

![Tab Đăng ký của biểu mẫu chỉnh sửa sản phẩm: hộp kiểm Bật Đăng ký được chọn, một kế hoạch được chọn trong danh sách Kế hoạch Đăng ký, và các tùy chọn Cho phép Mua một lần và Mặc định là Đăng ký](/static/core/admin/img/help/selling-products-as-subscriptions/subscriptions-tab.webp)

## Gắn kế hoạch đăng ký

Một **Kế hoạch Đăng ký** là một mẫu có thể sử dụng lại — các tùy chọn chu kỳ thanh toán, giai đoạn thử, phí ban đầu, quy tắc hủy bỏ — mà bạn xây dựng một lần và có thể gắn vào bất kỳ số lượng sản phẩm nào đủ điều kiện. Trường **Kế hoạch Đăng ký** trên tab Đăng ký của sản phẩm là nơi kết nối sản phẩm với các kế hoạch mà nó nên được bán.

Bạn có thể gắn nhiều hơn một kế hoạch cho cùng một sản phẩm. Điều này hữu ích khi, ví dụ, bạn muốn cung cấp một cấp độ "Chuẩn" và "Nâng cao" định kỳ cho cùng một mặt hàng — mỗi kế hoạch có thể mang theo chính sách giá, giai đoạn thử và chính sách hủy bỏ riêng. Khi một sản phẩm có nhiều hơn một kế hoạch được gắn, khách hàng sẽ thấy trình chọn kế hoạch trên trang sản phẩm trước khi chọn tần suất thanh toán.

## Kiểm soát giữa mua một lần và mua theo đăng ký

Hai tùy chọn kiểm tra trên tab Đăng ký kiểm soát cách khách hàng có thể mua sản phẩm:

- **Cho phép Mua một lần** — Được bật mặc định.

Khi được chọn, khách hàng chọn giữa việc mua một lần và đăng ký.

Bỏ chọn để sản phẩm chỉ bán theo đăng ký — mọi lần mua đều trở thành đơn hàng định kỳ, và không có tùy chọn mua một lần nào được hiển thị cả.
- **Mặc định là Đăng ký** — chọn tùy chọn đăng ký (và kế hoạch/tầng mặc định) khi trang sản phẩm được tải, thay vì buộc khách hàng phải chọn nó một cách chủ động.

Điều này chỉ có hiệu lực khi **Cho phép mua một lần** cũng được chọn — nếu mua một lần bị tắt, sản phẩm chỉ có thể đăng ký bất kể cài đặt này.

Sử dụng **Mặc định là Đăng ký** cho các sản phẩm mà việc giao hàng định kỳ là điều kỳ vọng tự nhiên (cà phê, thực phẩm chức năng, hàng tiêu dùng) — điều này giúp giảm bớt một thao tác nhấp chuột và tạo động lực cho khách hàng chọn lựa giữ chân họ quay lại, đồng thời không làm mất đi khả năng mua một lần của họ.

## Điều khách hàng nhìn thấy

### Trên trang sản phẩm

Khi một sản phẩm có đăng ký được bật và có ít nhất một kế hoạch hoạt động, công khai được gắn kèm, một bộ chọn chế độ mua hàng xuất hiện trên trang sản phẩm:

![Bộ chọn mua hàng của cửa hàng với "Đăng ký & Tiết kiệm" được chọn: nút chuyển đổi "Mua một lần" so với "Đăng ký & Tiết kiệm" ở trên danh sách tần suất giao hàng hiển thị các cấp độ Hàng năm (Tiết kiệm 20%), Hàng tháng và Hàng quý (Tiết kiệm 10%) với giá cả, cùng với ghi chú về thử thách, phí thiết lập và chính sách hủy bỏ](/static/core/admin/img/help/selling-products-as-subscriptions/subscribe-and-save-selector.webp)

- Nếu mua một lần được phép, khách hàng sẽ thấy lựa chọn **"Mua một lần"** so với **"Đăng ký & Tiết kiệm"**, mặc định là chế độ bạn đã cấu hình.
- Nếu sản phẩm có nhiều hơn một kế hoạch được gắn, một bộ chọn kế hoạch sẽ xuất hiện khi "Đăng ký & Tiết kiệm" được chọn.
- Đối với kế hoạch được chọn, khách hàng sẽ thấy danh sách **tần suất giao hàng** được xây dựng từ các cấp độ giá của kế hoạch đó (ví dụ: Hàng tháng, Hàng quý, Hàng năm), mỗi cấp độ hiển thị giá của nó và một **"Tiết kiệm X%"** badge khi cấp độ đó có khuyến mãi.
- Thời gian dùng thử, phí thiết lập và chính sách hủy bỏ của kế hoạch (ví dụ: "Hủy bất kỳ lúc nào") sẽ được hiển thị bên cạnh danh sách cấp độ, cùng với ghi chú rằng phương thức thanh toán sẽ được thêm vào lúc thanh toán.

### Trong giỏ hàng và lúc thanh toán

Các mục hàng hóa đăng ký trong giỏ hàng mang theo **dấu hiệu Đăng ký**, tần suất thanh toán (ví dụ: "Mỗi tháng"), và ghi chú dùng thử nếu có, để khách hàng rõ ràng biết được những mục nào là lặp lại. Tại thanh toán, khách hàng chọn nhà cung cấp thanh toán như bình thường — đây là phương thức thanh toán sẽ được tính phí cho các lần gia hạn sau.

> **Hạn chế đã biết:** Việc tự động lưu thẻ của khách hàng để gia hạn đăng ký trong tương lai tại trang thanh toán vẫn đang được kết nối cho một số nhà cung cấp thanh toán. Trong khi một nhà cung cấp cụ thể không hỗ trợ điều này, các đăng ký được đặt thông qua nó có thể cần thêm theo dõi (ví dụ: liên hệ khách hàng để cập nhật thông tin thanh toán trước khi gia hạn) thay vì được thực hiện một cách tự động ngay từ đầu. Kiểm tra cài đặt nhà cung cấp thanh toán của bạn nếu bạn nhận thấy các lần gia hạn không được tính phí tự động cho một đăng ký.

## Mẹo

- Tạo và kiểm tra kế hoạch đăng ký trước (các cấp độ giá, thời gian dùng thử, chính sách hủy), sau đó gắn nó với sản phẩm — dễ dàng hơn để có được kế hoạch chính xác một lần so với việc sửa chữa nó trên nhiều sản phẩm sau này.
- Giữ nguyên **Cho phép mua một lần** được chọn cho hầu hết các sản phẩm. Dành các sản phẩm chỉ đăng ký cho các trường hợp mà việc mua một lần thực sự không phù hợp với doanh nghiệp của bạn.
- Nếu bạn đang chuyển đổi một sản phẩm bán chạy thành tùy chọn đăng ký, hãy để **Mặc định là Đăng ký** bị tắt ban đầu để không làm gián đoạn khách hàng quen mua nó một lần — bật nó lên sau khi bạn đã thấy cách người đăng ký phản hồi.
- Sản phẩm kỹ thuật số là lựa chọn lý tưởng cho các đăng ký (giấy phép phần mềm, thành viên nội dung) vì việc gia hạn tự động cấp lại quyền truy cập mà không cần vận chuyển.
- Nếu bạn cần một loại sản phẩm không đủ điều kiện (một gói hoặc mặt hàng có thể tùy chỉnh, ví dụ) để bán theo chu kỳ, hãy xem xét xem liệu một phiên bản đơn giản hoặc kỹ thuật số tương đương có thể mang theo đăng ký thay thế hay không.