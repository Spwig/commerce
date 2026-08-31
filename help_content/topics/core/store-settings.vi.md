---
title: Cấu hình Cài đặt Cửa hàng
---

Cài đặt Cửa hàng là nơi trung tâm để cấu hình danh tính, địa phương hóa, thương hiệu và các tùy chọn vận hành của cửa hàng bạn. Điều hướng đến **Cài đặt > Cài đặt Cửa hàng** để bắt đầu.

![Tab chung của cài đặt cửa hàng](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Tab Chung

Tab **Chung** chứa các cài đặt danh tính cốt lõi của cửa hàng bạn.

### Danh tính Cửa hàng

- **Tên Cửa hàng** — Tên hiển thị được thể hiện trong tiêu đề trang, email và tiêu đề quản trị.
- **Khẩu hiệu** — Mô tả ngắn về cửa hàng của bạn, được sử dụng trong SEO và chia sẻ trên mạng xã hội.
- **URL Trang web** — Địa chỉ web công khai của cửa hàng bạn. Điều này được sử dụng trong email, tạo sitemap và xây dựng liên kết.

### Thông tin Liên hệ

- **Email Liên hệ** — Nhận thông báo đơn hàng và được hiển thị trong các giao tiếp với khách hàng.
- **Số Điện thoại** — Số điện thoại hỗ trợ tùy chọn được hiển thị trong phần chân trang và email.

### Địa chỉ Kinh doanh

Nhập địa chỉ đầy đủ của bạn (đường, thành phố, bang, mã bưu chính, quốc gia). Điều này được sử dụng cho:
- Tính toán điểm xuất phát vận chuyển
- Tính toán thuế
- Yêu cầu pháp lý và hóa đơn

## Thương hiệu

### Logo

Tải lên logo cửa hàng của bạn (khuyến nghị PNG hoặc SVG, ~200x50px với nền trong suốt). Logo xuất hiện trong:
- Tiêu đề cửa hàng
- Mẫu email
- Bảng điều khiển quản trị

### Favicon

Tải lên favicon hình vuông (ICO hoặc PNG, 32x32px). Nó xuất hiện dưới dạng:
- Biểu tượng tab trình duyệt
- Biểu tượng đánh dấu trang
- Biểu tượng màn hình chính trên thiết bị di động

## Địa phương hóa

### Ngôn ngữ Mặc định

Chọn ngôn ngữ chính của cửa hàng bạn từ 10 tùy chọn được hỗ trợ:

| Ngôn ngữ | Mã |
|----------|------|
| Tiếng Anh | en |
| Tiếng Tây Ban Nha | es |
| Tiếng Pháp | fr |
| Tiếng Đức | de |
| Tiếng Bồ Đào Nha | pt |
| Tiếng Nhật | ja |
| Tiếng Trung Giản thể | zh-hans |
| Tiếng Trung Truyền thống | zh-hant |
| Tiếng Nga | ru |
| Tiếng Ả Rập | ar |

Ngôn ngữ mặc định kiểm soát ngôn ngữ của giao diện quản trị và ngôn ngữ dự phòng cho nội dung cửa hàng.

### Múi giờ

Chọn múi giờ của cửa hàng bạn để có dấu thời gian đơn hàng chính xác, các khuyến mãi được lên lịch và báo cáo.

### Tiền tệ

- **Tiền tệ Mặc định** — Tiền tệ chính cho định giá và kế toán.
- **Đa Tiền tệ** — Bật để cho phép khách hàng xem giá bằng tiền tệ ưa thích của họ với chuyển đổi tự động sử dụng tỷ giá hối đoái thời gian thực.

Cấu hình các loại tiền tệ bổ sung trong **Cài đặt > Cài đặt Cửa hàng > Tiền tệ**.

## Cài đặt Thương mại Điện tử

### Thanh toán Khách vãng lai

Cho phép mua hàng mà không cần tạo tài khoản:
- Quy trình thanh toán nhanh hơn
- Giảm ma sát cho người mua lần đầu
- Thu thập ít dữ liệu khách hàng hơn

### Thời điểm Tạo Tài khoản

Kiểm soát thời điểm khách hàng được nhắc tạo tài khoản:

| Tùy chọn | Mô tả |
|--------|-------------|
| **Sau khi Mua hàng (Khuyến nghị)** | Nhắc tạo tài khoản sau khi đặt hàng thành công — tận dụng thiện chí sau mua hàng để đạt tỷ lệ chuyển đổi tốt nhất |
| **Trong khi Thanh toán** | Tạo tài khoản trước khi xử lý thanh toán |
| **Trước khi Thanh toán** | Yêu cầu tài khoản trước khi mua sắm (không khuyến nghị — giảm tỷ lệ chuyển đổi) |

Bạn cũng có thể đặt một **Thông báo Tạo Tài khoản** tùy chỉnh để giải thích lợi ích của việc đăng ký.

### Mặc định Kho hàng

- **Theo dõi Kho hàng** — Bật theo dõi tồn kho toàn cục
- **Ngưỡng Tồn kho Thấp** — Mức tồn kho mà tại đó các cảnh báo tồn kho thấp được gửi đến email quản trị (mặc định: 10 đơn vị)

### Trí tuệ Kho hàng

![Thẻ Trí tuệ Kho hàng hiển thị các trường Thời gian Đặt lại hàng Mặc định, Hệ số Tồn kho An toàn, Cửa sổ Tính toán Tốc độ Bán, Cho phép Đặt hàng Trả sau Mặc định và Tần suất Cảnh báo Tồn kho Thấp](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Các cài đặt này điều chỉnh các tính toán đặt lại hàng tự động, tồn kho an toàn và tốc độ bán hàng, và kiểm soát cách xử lý các tình trạng hết hàng và tồn kho thấp.

- **Thời gian Đặt lại hàng Mặc định (Ngày)** — Số ngày thường mất để nhận hàng bổ sung từ nhà cung cấp của bạn sau khi bạn đặt hàng (mặc định: 14).

Dự báo sử dụng thông số này để đánh dấu các sản phẩm cần đặt lại hàng *ngay bây giờ* để tránh tình trạng hết hàng trước khi lô hàng mới đến.
- **Hệ số An toàn** — Một lớp đệm được áp dụng trên top nhu cầu dự kiến để hấp thụ các đợt tăng đột biến về doanh số hoặc sự chậm trễ từ nhà cung cấp.

Ví dụ, hệ số `1.5` tạo ra một lớp đệm 50% trên mức tồn kho an toàn đã tính toán; `2.0` nhân đôi mức đó.

Tăng hệ số này cho các sản phẩm mà việc hết hàng gây thiệt hại lớn (sản phẩm bán chạy, hàng theo mùa); giảm nó cho hàng bán chậm mà bạn không muốn đặt quá nhiều.
- **Cửa sổ Tính toán Tốc độ Bán (Ngày)** — Cửa sổ nhìn lại mà Spwig sử dụng để tính toán tốc độ bán của từng sản phẩm, từ đó tạo ra các gợi ý đặt lại hàng và số ngày cung cấp (mặc định: 30).

Cửa sổ ngắn hơn phản ứng nhanh hơn với những thay đổi nhu cầu gần đây; cửa sổ dài hơn làm mượt các đỉnh theo mùa để một tuần bận rộn duy nhất không làm lệch dự báo.
- **Cho phép Đặt trước Mặc định** — Cài đặt đặt trước ban đầu được áp dụng cho các sản phẩm mới được tạo (mặc định là tắt).

Mỗi sản phẩm vẫn có thể ghi đè cài đặt này riêng lẻ trên trang sản phẩm của nó, và các sản phẩm hiện có giữ nguyên cài đặt mà chúng đã có — việc thay đổi này chỉ thay đổi cài đặt mặc định mà các sản phẩm mới bắt đầu với, nó không cập nhật ngược lại danh mục của bạn.
- **Tần suất Cảnh báo Hết hàng** — Tần suất ứng dụng di động Spwig của bạn được thông báo về tình trạng hết hàng: **Thời gian thực** gửi một thông báo đẩy ngay khi một sản phẩm vượt qua ngưỡng hết hàng; **Tóm tắt Hàng ngày** và **Tóm tắt Hàng tuần** thay vào đó gửi một thông báo đẩy duy nhất tóm tắt tất cả các sản phẩm đang hết hàng theo lịch đó.

Cài đặt này chỉ có hiệu lực khi **Cảnh báo Hết hàng** (Cài đặt Email, bên dưới) được bật — với cảnh báo tắt, không có thông báo nào được gửi ở bất kỳ tần suất nào.

### Tài liệu & Hóa đơn

![Thẻ Tài liệu & Hóa đơn hiển thị các trường Mã số Thuế / Mã số VAT, Chân trang Hóa đơn, Chân trang Phiếu đóng gói và Độ rộng Logo Tài liệu được điền với các giá trị ví dụ](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Các trường này điền vào các hóa đơn và phiếu đóng gói mà Spwig tạo cho các đơn hàng — ví dụ khi một thương nhân tải xuống hoặc gửi email một hóa đơn PDF, hoặc in một phiếu đóng gói cho một lô hàng.

- **Mã số Thuế / Mã số VAT** — Mã số định danh thuế doanh nghiệp của bạn. Được in trên các hóa đơn được tạo để đáp ứng các yêu cầu về tài liệu thuế địa phương.
- **Chân trang Hóa đơn** — Văn bản tự do hiển thị ở cuối mỗi hóa đơn được tạo. Các mục sử dụng phổ biến: điều khoản thanh toán ("Thanh toán trong vòng 30 ngày"), một lời cảm ơn, hoặc chi tiết chuyển khoản ngân hàng.
- **Chân trang Phiếu đóng gói** — Văn bản tự do hiển thị ở cuối mỗi phiếu đóng gói được tạo. Các mục sử dụng phổ biến: hướng dẫn trả hàng hoặc một ghi chú cho đội ngũ kho/bàn giao.
- **Độ rộng Logo Tài liệu (px)** — Độ rộng của logo cửa hàng của bạn như nó xuất hiện trên các hóa đơn PDF và phiếu đóng gói được tạo (mặc định: 200px). Chiều cao tự động điều chỉnh để phù hợp, do đó tỷ lệ logo của bạn được giữ nguyên. Bản thân hình ảnh logo đến từ **Logo** (Thương hiệu, bên trên) — các logo SVG không được vẽ trên các tài liệu PDF, vì vậy hãy tải lên một phiên bản PNG hoặc JPG của logo nếu bạn sử dụng đồ họa vector trên cửa hàng.

## Cài đặt Email

Cấu hình các cài đặt gửi email trong **Cài đặt > Tài khoản Email** và **Cài đặt > Mẫu Email**. Xem [Cấu hình Email](/help/email-configuration) để biết chi tiết đầy đủ.

Các cài đặt email chính có sẵn trong Cài đặt Cửa hàng:

- **Email Xác nhận Đơn hàng** — Bật hoặc tắt email xác nhận tự động
- **Email Thông báo Vận chuyển** — Bật hoặc tắt các thông báo cập nhật vận chuyển
- **Cảnh báo Hết hàng** — Gửi cảnh báo đến email quản trị khi tồn kho giảm xuống dưới ngưỡng
- **Chế độ Gửi Email** — Trực tiếp (gửi bình thường), Tạm dừng (giữ tất cả email), hoặc Chỉ ghi log (ghi lại nhưng không bao giờ gửi)
- **Email Chuyển hướng Kiểm thử** — Chuyển hướng tất cả email gửi đi đến một địa chỉ duy nhất để kiểm thử

## Cài đặt Bảo mật

### Xác thực Hai yếu tố (2FA)

Kiểm soát xem nhân viên có bắt buộc phải sử dụng xác thực hai yếu tố hay không:


{
  "Setting": "Mục",
  "Description": "Mô tả",
  "\*\*Optional\*\*": "Nhân viên có thể chọn bật 2FA nhưng không bắt buộc",
  "\*\*Recommended\*\*": "Nhân viên sẽ thấy thông báo khuyến khích họ thiết lập 2FA",
  "\*\*Required\*\*": "Nhân viên không thể truy cập admin cho đến khi 2FA được bật",
  "\*\*Grace Period (Days)\*\*": "Số ngày nhân viên có thể thiết lập 2FA sau khi bật chế độ bắt buộc",
  "\*\*Allow Trusted Devices\*\*": "Cho phép nhân viên bỏ qua xác minh 2FA trên các thiết bị được nhận diện trong một khoảng thời gian nhất định",
  "\n## Cookie Consent\n\n": "Cấu hình thanh thông báo đồng ý cookie được hiển thị cho khách hàng mua sắm:",
  "\*\*Cookie Consent Enabled\*\*": "Hiển thị hoặc ẩn thanh thông báo cookie",
  "\*\*Banner Position\*\*": "Vị trí thanh banner xuất hiện trên màn hình (dải dưới, cửa sổ bật lên góc, v.v.)",
  "\*\*Consent Mode\*\*": "Thông báo đơn giản, chọn tham gia hoặc chọn không tham gia",
  "\*\*Banner Title and Text\*\*": "Tiêu đề và mô tả có thể tùy chỉnh được hiển thị cho khách hàng",
  "\*\*Category Descriptions\*\*": "Mô tả riêng biệt cho cookie phân tích, quảng cáo và chức năng",
  "\nAll banner text fields support translations for multilingual stores.\n\n": "Tất cả các trường văn bản thanh đều hỗ trợ dịch cho các cửa hàng đa ngôn ngữ.\n\n",
  "\n## Communications\n\n": "\n## Thông báo\n\n",
  "The \*\*Communications\*\* tab controls how your store obtains, confirms, and lets customers manage consent for marketing email and SMS. These settings shape your legal compliance posture (GDPR for email, TCPA for SMS), so review them with your own legal counsel before launch — Spwig provides the controls, not the advice.\n\n": "Mục \*\*Thông báo\*\* điều khiển cách cửa hàng của bạn nhận, xác nhận và cho phép khách hàng quản lý sự đồng ý cho email và SMS tiếp thị. Các cài đặt này xác định vị thế tuân thủ pháp lý của bạn (GDPR cho email, TCPA cho SMS), vì vậy hãy xem xét chúng với luật sư của riêng bạn trước khi ra mắt — Spwig cung cấp các công cụ, không phải lời khuyên.",
  "\n![Communications tab showing Email Marketing Consent, Preferences & Unsubscribe, and SMS Consent cards](/static/core/admin/img/help/store-settings/communications-tab.webp)\n\n": "\n![Mục Thông báo hiển thị Thẻ Đồng ý Email Tiếp thị, Ưu đãi & Hủy đăng ký, và Thẻ Đồng ý SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)\n\n",
  "\n### Email Marketing Consent\n\n": "\n### Đồng ý Email Tiếp thị\n\n",
  "\*\*Enable Double Opt-In for Marketing Emails\*\*": "Khi bật, khách hàng đăng ký email tiếp thị sẽ nhận được email xác nhận và phải nhấp vào liên kết trong đó trước khi Spwig gửi bất kỳ thông điệp tiếp thị nào cho họ. Khi tắt, việc tích vào ô đăng ký tiếp thị là đủ. Mặc định được bật, theo đúng thực hành tốt nhất của GDPR.",
  "\*\*Default Marketing Opt-In State\*\*": "Trạng thái đăng ký tiếp thị ban đầu được áp dụng cho tài khoản khách hàng mới. Mặc định là tắt (GDPR chọn không tham gia), do đó khách hàng mới bắt đầu ở trạng thái không đăng ký tiếp thị cho đến khi họ chủ động đăng ký.",
  "\nWhen double opt-in is on, opting in triggers a confirmation email with a verification link. Until the customer clicks it, they're recorded as opted in but unconfirmed, and marketing sends skip them — transactional email (order confirmations, shipping updates, password resets) is never affected by this setting.\n\n": "\nKhi bật double opt-in, việc đăng ký sẽ kích hoạt email xác nhận với liên kết xác minh. Cho đến khi khách hàng nhấp vào liên kết đó, họ sẽ được ghi nhận là đã đăng ký nhưng chưa xác nhận, và các cuộc gửi email tiếp thị sẽ bỏ qua chúng — email giao dịch (xác nhận đơn hàng, cập nhật vận chuyển, khôi phục mật khẩu) không bao giờ bị ảnh hưởng bởi cài đặt này.\n\n",
  "\n### Preferences & Unsubscribe\n\n": "\n### Ưu đãi & Hủy đăng ký\n\n",
  "\*\*Enable Customer Preference Center\*\*": "Khi bật, khách hàng có thể quản lý email và SMS của họ từ trang truy cập tự phục vụ được liên kết từ bảng điều khiển tài khoản của họ. Khi tắt, trang đó và API hỗ trợ sẽ không khả dụng và liên kết bảng điều khiển sẽ bị ẩn. Các liên kết hủy đăng ký một bước trong email của bạn sẽ hoạt động trong mọi trường hợp — lối thoát này là bắt buộc cho việc tuân thủ và không bị ảnh hưởng bởi nút chuyển đổi này.",
  "\*\*Collect Unsubscribe Reasons\*\*": "Khi bật, trang hủy đăng ký một bước sẽ hỏi khách hàng lý do ngắn gọn trước khi xác nhận: 'Tôi nhận được quá nhiều email', 'Nội dung không liên quan đến tôi', 'Tôi chưa từng đăng ký', 'Tôi không còn quan tâm', hoặc 'Khác'. Lý do khách hàng chọn sẽ được ghi nhận vào nhật ký đồng ý để bạn có thể xem xét các mô hình hủy đăng ký theo thời gian.",
  "\n### SMS Consent\n\n": "\n### Đồng ý SMS\n\n",
  "\*\*Require SMS Verification\*\*": "Khi bật (mặc định), khách hàng phải xác minh số điện thoại của họ bằng mã một lần trước khi Spwig gửi bất kỳ tin nhắn SMS nào, bao gồm cả tin nhắn tiếp thị. Khi tắt, việc tích vào ô đăng ký SMS là đủ để bắt đầu gửi. Mặc định đã được thay đổi thành 'Bật' để an toàn cho TCPA — chỉ tắt nếu bạn có bước xác minh khác trong quy trình đăng ký của mình.",
  "\n## Maintenance Mode\n\n": "\n## Chế độ Bảo trì\n\n",
  "Enable maintenance mode to take your store offline temporarily:\n- Displays a custom maintenance message to visitors\n- You can link a \*\*Maintenance Page\*\* built in the Page Builder for a fully branded maintenance experience\n- Restricts access to admin users only\n- Useful during major updates or migrations\n\n": "Bật chế độ bảo trì để đưa cửa hàng của bạn về chế độ không hoạt động trong thời gian ngắn:
- Hiển thị một thông báo bảo trì tùy chỉnh cho khách truy cập
- Bạn có thể liên kết một \*\*Trang Bảo trì\*\* được xây dựng trong Page Builder để có trải nghiệm bảo trì được thương hiệu hóa hoàn toàn
- Giới hạn truy cập chỉ cho người dùng admin
- Hữu ích trong các lần cập nhật hoặc di dời lớn"
}

## Mạng xã hội

Kết nối các hồ sơ mạng xã hội của cửa hàng. Chúng xuất hiện ở chân trang và mẫu email:

- **URL Facebook**
- **URL Twitter**
- **URL Instagram**
- **URL LinkedIn**

## Cài đặt SEO mặc định

Thiết lập các thẻ meta mặc định khi trang không có cài đặt SEO riêng:

- **Tiêu đề Meta** — Tên trang mặc định (tối đa 60 ký tự)
- **Mô tả Meta** — Mô tả mặc định hiển thị trong kết quả tìm kiếm (tối đa 160 ký tự)
- **Từ khóa Meta** — Từ khóa phân cách bằng dấu phẩy mặc định

## Cài đặt Thuế

Cấu hình việc thu thập thuế tại **Cài đặt > Cài đặt Thuế**:

1. **Phương pháp Tính toán** — Theo địa chỉ giao hàng, địa chỉ thanh toán hoặc vị trí cửa hàng
2. **Tỷ lệ Thuế** — Xác định tỷ lệ theo khu vực và lớp thuế sản phẩm
3. **Hiển thị Thuế** — Hiển thị giá tiền bao gồm thuế, không bao gồm thuế, hoặc cả hai

## Lời khuyên

- Đặt múi giờ chính xác trước khi xử lý đơn hàng nào — điều này ảnh hưởng đến tất cả thời điểm và báo cáo.
- Bật chế độ thanh toán không cần tài khoản để cải thiện tỷ lệ chuyển đổi.
- Điền địa chỉ doanh nghiệp của bạn để tính toán vận chuyển và thuế chính xác.
- Tải lên cả logo và favicon để có trải nghiệm chuyên nghiệp, mang tính thương hiệu.
- Sử dụng **Thời điểm tạo tài khoản Sau khi mua hàng** để đạt tỷ lệ đăng ký tốt nhất.
- Bật chế độ **Yêu cầu Xác minh Hai bước** cho nhân viên để bảo vệ cửa hàng admin của bạn.
- Kiểm tra luồng email bằng **Cài đặt Email Chuyển tiếp Thử nghiệm** trước khi phát hành chính thức.
- Thiết lập **Thời gian dẫn đầu Mặc định** để phù hợp với nhà cung cấp chậm nhất của bạn — dự báo đặt hàng áp dụng giá trị duy nhất này trên toàn bộ danh mục sản phẩm của bạn, vì vậy hãy chọn giá trị có thời gian dẫn đầu dài nhất.
- Ngắn gọn **Khoảng thời gian Tính toán Tốc độ** nếu bạn chạy các chương trình khuyến mãi hoặc nhập hàng thường xuyên và muốn dự báo phản ứng nhanh với doanh số trong vài ngày gần đây; kéo dài nó để có cái nhìn ổn định, ít bị gián đoạn hơn về nhu cầu.
- Nếu bạn bật **Cho phép Đặt hàng trước Mặc định**, hãy nhớ rằng nó chỉ đặt điểm bắt đầu cho các sản phẩm được tạo *sau* khi thay đổi — quay lại các sản phẩm hiện có nếu bạn muốn đặt hàng trước được bật trên danh mục hiện tại của bạn nữa.
- Tương ứng **Tần suất Cảnh báo Hết hàng** với cách bạn quản lý hàng tồn kho: **Thời gian thực** cho danh mục di chuyển nhanh nơi mà mọi rủi ro hết hàng đều cần sự chú ý ngay lập tức, **Tóm tắt Hàng ngày** hoặc **Tóm tắt Hàng tuần** để tránh kiệt sức thông báo trên danh mục lớn.
- Điền vào **Mã số Thuế / Số VAT** và văn bản chân trang trước khi hóa đơn đầu tiên thực sự được gửi cho khách hàng — cả hai trường đều trống theo mặc định.
- Nếu **Logo** của bạn là SVG, hãy tải lên phiên bản PNG hoặc JPG nữa — **Chiều rộng Logo Tài liệu** không ảnh hưởng đến PDF vì Spwig không thể vẽ nghệ thuật SVG trên hóa đơn và phiếu đóng gói được tạo ra.
- Giữ nguyên **Bật Xác minh Hai bước cho Email Tiếp thị** trừ khi bạn có lý do cụ thể để tắt nó — đó là cài đặt mặc định an toàn cho GDPR và nó bảo vệ danh tính người gửi của bạn bằng cách giữ các địa chỉ chưa xác minh khỏi các email tiếp thị của bạn.
- Giữ nguyên **Trạng thái Tùy chọn Tiếp thị Mặc định** ở chế độ tắt. Việc chọn trước tùy chọn đồng ý tiếp thị cho tài khoản mới làm suy yếu yêu cầu đồng ý GDPR ngay cả khi khách hàng có thể gỡ bỏ tùy chọn đó.
- Không tắt **Bật Trung tâm Ưa thích Khách hàng** chỉ để đơn giản hóa bảng điều khiển tài khoản của bạn — mà không có nó, khách hàng vẫn có thể hủy đăng ký một loại thông báo cụ thể, nhưng họ mất khả năng tùy chỉnh các ưu tiên (ví dụ: giữ cập nhật vận chuyển nhưng bỏ qua tin tức).
- Giữ nguyên **Yêu cầu Xác minh SMS** ở chế độ bật trừ khi quy trình đăng ký của bạn đã xác minh số điện thoại theo cách khác (ví dụ: đăng nhập dựa trên SMS) — cài đặt này tồn tại đặc biệt để giữ bạn trong các quy định TCPA.

## Xử lý sự cố

**Các thay đổi không xuất hiện trên cửa hàng trực tuyến:**
- Xóa bộ nhớ đệm trình duyệt của bạn
- Chạy lệnh xóa bộ nhớ đệm từ bảng điều khiển quản trị
- Kiểm tra xem chế độ bảo trì có được bật tình cờ hay không hay không

**Email không gửi được:**
- Xác minh cài đặt nhà cung cấp email của bạn trong Cấu hình Email
- Kiểm tra xem **Chế độ Gửi Email** có được đặt thành **Thực tế** hay không
- Đảm bảo **Email Chuyển tiếp Thử nghiệm** trống nếu bạn muốn email được gửi đến người nhận thực sự

**Chuyển đổi tiền tệ không hoạt động:**
- Kiểm tra xem nhà cung cấp tỷ giá hối đoái của bạn đã được kết nối chưa
- Kiểm tra thông tin đăng nhập API trong cài đặt tỷ giá hối đoái
- Thử cập nhật tỷ giá thủ công

**Email tiếp thị không đến được khách hàng đã đăng ký nhận:**
- Kiểm tra xem **Kích hoạt xác nhận hai lần cho email tiếp thị** có được bật không — nếu có, khách hàng phải nhấp vào liên kết xác nhận trong email xác minh trước khi email tiếp thị được gửi lại
- Yêu cầu khách hàng kiểm tra hộp thư rác/email rác cho email xác minh
- Xác nhận xem tùy chọn nhận email tiếp thị của khách hàng vẫn được bật trong phần tùy chỉnh của họ không — việc nhấp vào nút hủy đăng ký sẽ làm tắt tùy chọn đó

**Khách hàng nói họ không thể tìm thấy trung tâm tùy chỉnh:**
- Kiểm tra xem **Kích hoạt Trung tâm Tùy chỉnh của Khách hàng** có được bật không — khi tắt, liên kết bảng điều khiển sẽ bị ẩn và trang này không thể truy cập được theo thiết kế
- Liên kết hủy đăng ký trong bất kỳ email tiếp thị nào cũng luôn hoạt động bất kể cài đặt này, vì vậy hãy chỉ cho khách hàng truy cập vào đó như một giải pháp thay thế