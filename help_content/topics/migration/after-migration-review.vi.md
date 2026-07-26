---
title: Sau khi di chuyển của bạn
---

Việc di chuyển hoàn tất là điểm bắt đầu để bạn xem xét, chứ không phải là điểm kết thúc. Bước 6 của hướng dẫn sẽ cung cấp cho bạn một bản tóm tắt về những gì đã được chuyển, một công cụ để sửa các liên kết vẫn trỏ đến trang web cũ của bạn, và một báo cáo bạn có thể tải xuống để lưu trữ. Chủ đề này sẽ hướng dẫn bạn kiểm tra những điều cần kiểm tra trước khi bạn coi việc di chuyển là hoàn tất, bao gồm các công việc liên quan đến thuế, vận chuyển và việc đưa vào vận hành mà chính hướng dẫn không thực hiện cho bạn.

## Đọc kết quả của bạn

Tại đầu trang hoàn tất, bạn sẽ thấy một hàng các thẻ thống kê — một thẻ cho mỗi loại dữ liệu (Sản phẩm, Danh mục, Khách hàng, Đơn hàng, v.v.) — tiếp theo là bảng **Tóm tắt Nhập khẩu** với các cột Imported, Skipped, Failed, và Total cho từng bước đã chạy.

- **Imported** — các mục đã được tạo thành công trong Spwig.
- **Skipped** — các mục mà nền tảng nguồn của bạn có, nhưng Spwig không tạo. Điều này hầu như luôn là điều được mong đợi: với tùy chọn **Skip existing items** được bật ở bước 3, bất kỳ mục nào trùng khớp với một mục đã tồn tại trong Spwig (theo SKU, email, v.v.) sẽ được giữ nguyên thay vì bị sao chép. Một số lượng bỏ qua cao sau khi thử lại thường chỉ có nghĩa là lần thử đầu tiên đã tạo ra các bản ghi đó.
- **Failed** — các mục mà Spwig đã cố gắng tạo nhưng không thể do vấn đề dữ liệu, thiếu phụ thuộc, hoặc lỗi ở phía nguồn. Một số lượng thất bại không bằng 0 đáng để điều tra; xem [Giải quyết sự cố di chuyển](migration-troubleshooting) để biết cách đọc nhật ký và các tùy chọn dọn dẹp của bạn.

> **Lưu ý:** Nếu bất kỳ bước nào hiển thị lỗi, đừng giả định cửa hàng đã hoàn tác bất cứ thứ gì để bù đắp — nó không làm như vậy. Những gì đã được nhập trước khi xảy ra lỗi vẫn đang tồn tại trong cửa hàng của bạn cùng với mọi thứ đã thành công. Kiểm tra nó theo cùng cách bạn sẽ kiểm tra kết quả riêng phần bình thường.

## Viết lại liên kết

Sản phẩm, trang và bài viết blog được nhập từ nền tảng cũ của bạn thường chứa các liên kết quay trở lại miền gốc — một URL hình ảnh, một liên kết "sản phẩm liên quan", hoặc một tham chiếu chéo nội bộ. Nếu Spwig phát hiện bất kỳ liên kết nào trong nội dung vừa nhập, một bảng điều khiển **Viết lại liên kết** sẽ xuất hiện trên trang hoàn tất.

Mỗi liên kết được phát hiện sẽ được nhóm theo trang hoặc sản phẩm mà nó đến từ, và được hiển thị với:

- **Original URL** — liên kết chính xác như nó xuất hiện trong nội dung đã nhập.
- **Suggested URL** — URL được Spwig đề xuất là trang tương đương trên cửa hàng mới của bạn, nếu có.
- **Match** — phần trăm độ tin cậy cho đề xuất đó. Các liên kết không có đề xuất hợp lý sẽ hiển thị là **None** và không có URL đề xuất nào để phê duyệt.

Đối với mỗi liên kết, bạn có thể **Phê duyệt** đề xuất hoặc **Bỏ qua** nó, lần lượt. **Tự động phê duyệt các đề xuất có độ tin cậy cao** sẽ phê duyệt mọi đề xuất có độ tin cậy 85% trở lên chỉ với một cú nhấp chuột — tiết kiệm thời gian, nhưng vẫn đáng để kiểm tra ngẫu nhiên sau đó. Các đề xuất dưới ngưỡng đó là những liên kết đáng để bạn mở thủ công: một tỷ lệ phù hợp 50-70% có thể là sản phẩm đúng nhưng có tên sai, hoặc có thể hoàn toàn không liên quan, và chỉ có một cái nhìn nhanh của con người mới có thể xác định được.

Việc phê duyệt hoặc bỏ qua chỉ đánh dấu một liên kết — không có gì trong nội dung của bạn thay đổi cho đến khi bạn nhấp vào **Áp dụng các liên kết đã phê duyệt**, điều này sẽ viết lại tất cả các liên kết đã được phê duyệt cùng lúc. Điều này có nghĩa là bạn có thể an toàn làm việc qua danh sách trong nhiều lần ngồi khác nhau trước khi cam kết thực hiện.

> **Lời khuyên:** Nếu bạn không chắc chắn về bất kỳ liên kết nào, hãy để nó ở trạng thái **Bỏ qua** thay vì phê duyệt một giả định. Bạn luôn có thể sửa liên kết miền cũ còn sót lại bằng tay sau này; việc viết lại sai cho hàng chục sản phẩm sẽ tốn nhiều công để đảo ngược hơn.

## Kiểm tra dữ liệu của bạn

Xem các thẻ thống kê như một điểm bắt đầu, chứ không phải bằng chứng cho thấy mọi thứ đều đúng. Hãy dành vài phút kiểm tra ngẫu nhiên:

- **Sản phẩm** — Mở một vài sản phẩm, đặc biệt là những sản phẩm có biến thể (kích cỡ, màu sắc, v.v.), và xác nhận các tùy chọn biến thể và giá đã được chuyển đúng, và hình ảnh được đính kèm và hiển thị trên cửa hàng, không chỉ trong phần quản trị.
- **Danh mục** — Xác nhận cấu trúc danh mục trông đúng, đặc biệt nếu bạn đã di chuyển từ Shopify, nơi các bộ sưu tập được nhập dưới dạng danh sách phẳng thay vì cây phân cấp.
- **Tài khoản khách hàng** — Kiểm tra ngẫu nhiên email và địa chỉ trên một vài bản ghi.

Khách hàng đã di chuyển không mang theo mật khẩu cũ của họ — Spwig không thể đọc mật khẩu đó từ nền tảng nguồn — vì vậy **khách hàng sẽ cần đặt lại mật khẩu** lần đầu tiên họ đăng nhập.

Hãy cân nhắc gửi một email thông báo trước khi bạn chính thức đi vào hoạt động.
- **Đơn hàng** — Kiểm tra xem tổng số, trạng thái và các mục hàng hóa trên một mẫu đơn hàng có khớp với những gì bạn đã thấy trên nền tảng cũ không.
- **Sản phẩm được mở rộng** — Nếu bạn di chuyển từ WooCommerce với các phần mở rộng như Subscriptions, Bundles, Gift Cards, Composite Products hoặc Bookings, hãy kiểm tra nhanh các sản phẩm đã sử dụng chúng.

Dữ liệu mở rộng không thể đọc được sẽ không cản trở việc nhập sản phẩm — nó vẫn được chuyển qua, chỉ thiếu cấu hình bổ sung — vì vậy những sản phẩm này có khả năng cao nhất cần được chỉnh sửa thủ công.

## Cấu hình thuế và vận chuyển

Các tùy chọn nhập thuế và khu vực vận chuyển trong bước 4 của chương trình hướng dẫn ghi lại sở thích của bạn, nhưng chúng không được áp dụng cho việc nhập — không có tỷ lệ thuế hoặc khu vực vận chuyển nào được tạo ra từ chúng. Điều này là bình thường: **cấu hình thuế và vận chuyển là bước bình thường, riêng biệt mà bạn thực hiện trực tiếp trong Spwig** sau khi hoàn tất việc nhập dữ liệu, giống như khi bạn thiết lập một cửa hàng mới.

**Kiểm soát Điều chỉnh giá** trên cùng bước này là một ngoại lệ — nó có hiệu lực cho các lần nhập từ WooCommerce, CSV và Shopify, dịch chuyển giá cơ bản của mỗi sản phẩm khi nó được tạo. Nếu bạn đã thiết lập một giá và giá của bạn trông sai, đó là nơi thay đổi đến từ. Xem [Ánh xạ trường di chuyển](migration-field-mapping) để biết chi tiết.

Trước khi bạn đi vào hoạt động, hãy cấu hình:

- Tỷ lệ thuế của bạn — xem [Cấu hình thuế](tax-configuration) để thiết lập tỷ lệ theo quốc gia, tỉnh hoặc khu vực, bao gồm bất kỳ miễn trừ nào mà sản phẩm của bạn cần.
- Khu vực và phương thức vận chuyển của bạn — xem [Thiết lập vận chuyển](setup-shipping) để tái tạo các tùy chọn vận chuyển mà khách hàng của bạn đã có trên nền tảng cũ của bạn.

Hãy thực hiện điều này trước khi kiểm tra thanh toán, để đơn hàng kiểm tra của bạn phản ánh tổng số thực tế.

## Tải xuống báo cáo của bạn

Trang hoàn tất cung cấp ba tùy chọn tải xuống:

- **Tải xuống PDF** — một bản tóm tắt được định dạng với thông tin công việc, số lượng theo từng bước và danh sách lỗi, giới hạn ở **20 lỗi đầu tiên**.
- **Tải xuống CSV** — cùng bản tóm tắt dưới dạng bảng tính, giới hạn ở **50 lỗi đầu tiên**.
- **Tải xuống Nhật ký** — mọi mục nhật ký cho công việc, không có giới hạn.

Nếu số lượng lỗi của bạn nhỏ, PDF hoặc CSV là đủ. Đối với một lần di chuyển có số lượng lỗi lớn, hãy tải xuống nhật ký thay vì — đây là duy nhất trong ba lựa chọn có bản ghi đầy đủ thay vì mẫu bị cắt ngắn.

> **Lưu ý:** Các bản ghi công việc di chuyển — bao gồm nhật ký và báo cáo của chúng — sẽ được lưu trữ trong Spwig vĩnh viễn; không có gì xóa chúng theo lịch trình. Tuy nhiên, hãy tải xuống bản sao bất kể nếu bạn muốn lưu trữ ngoại tuyến hoặc chia sẻ với người không có quyền truy cập quản trị, nhưng không có đếm ngược nào ép buộc bạn phải làm điều đó hôm nay.

## Đi vào hoạt động

Khi bạn hài lòng với dữ liệu, cài đặt thuế và vận chuyển của mình:

1. **Kiểm tra thanh toán từ đầu đến cuối.** Thêm một sản phẩm vào giỏ hàng, hoàn tất thanh toán và xác nhận thuế, vận chuyển và thanh toán đều được tính toán và xử lý đúng, lý tưởng là với phương thức thanh toán thực tế trong chế độ kiểm tra.
2. **Cập nhật DNS** của bạn để chỉ định tên miền của bạn chỉ đến Spwig sau khi kiểm tra đó thành công. Đừng chuyển đổi DNS trước và sau đó điều chỉnh — khách hàng có thể gặp phải thanh toán bị hỏng trong thời gian đó.
3. **Giữ cửa hàng cũ của bạn khả dụng, ở trạng thái chỉ đọc hoặc "đóng"**, cho đến khi bạn tự tin rằng cửa hàng mới xử lý đơn hàng đúng cách. Điều này cho phép bạn có một phương án dự phòng mà không làm tăng nguy cơ đơn hàng được đặt trên nền tảng cũ sau khi chuyển đổi.

## Hủy quyền truy cập nền tảng nguồn

Sau khi bạn đã xác nhận việc di chuyển hoàn tất và không dự kiến sẽ chạy lại, hãy quay lại nền tảng nguồn và hủy hoặc xóa khóa API, ứng dụng hoặc tích hợp bạn đã tạo cho nó (xem [Di chuyển từ WooCommerce](migrate-from-woocommerce) hoặc hướng dẫn nền tảng tương ứng để biết nơi lưu trữ thông tin xác thực đó).

Spwig không cần quyền truy cập liên tục đến cửa hàng cũ của bạn sau khi quá trình nhập dữ liệu kết thúc, vì vậy việc xóa nó sẽ loại bỏ một tài khoản xác thực bạn không còn sử dụng nữa.

## Tips

- **Skipped is usually fine, failed is not** — một số lượng skipped lớn sau khi thử lại với tùy chọn Skip existing items on là điều được mong đợi; một số lượng failed khác 0 xứng đáng để bạn xem xét lại nhật ký.
- **Đừng vội Apply Approved Links** — việc phê duyệt và bỏ qua có thể thay đổi bất kỳ lúc nào trước khi bạn nhấn Apply, vì vậy hãy dành thời gian xem xét các mục có độ tin cậy thấp.
- **Cấu hình thuế và vận chuyển trước khi bán hàng đầu tiên trực tiếp**, không phải sau — quá trình nhập dữ liệu không thực hiện điều này cho bạn, và một tỷ lệ thuế chưa được cấu hình dễ bị bỏ sót cho đến khi khách hàng phàn nàn.
- **Thông báo cho khách hàng về việc đặt lại mật khẩu** nếu bạn đang gửi email cho danh sách khách hàng về việc chuyển đổi, để lần đăng nhập đầu tiên không gây bất ngờ.
- **Tải xuống báo cáo của bạn trước thời điểm 90 ngày** nếu bạn cần nó cho hồ sơ kế toán hoặc tuân thủ.
- **Giữ lại cửa hàng cũ, chỉ đọc, trong một thời gian** — nó tốn ít chi phí và cung cấp cho bạn một mạng lưới an toàn trong những ngày đầu tiên hoạt động trên Spwig.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-results-summary.webp
  description: Migration completion page showing the stat cards and Imported/Skipped/Failed/Total summary table
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-link-rewriting.webp
  description: Link Rewriting panel with grouped suggestions, confidence percentages, and the Approve/Skip/Apply Approved Links controls
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
-->