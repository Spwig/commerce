---
title: Cài đặt Cửa hàng
---

Cài đặt Cửa hàng là nơi trung tâm để cấu hình danh tính, địa phương hóa, thương hiệu và các tùy chọn vận hành của cửa hàng bạn. Điều hướng đến **Cài đặt > Cài đặt Cửa hàng** để bắt đầu.

![Tab Cài đặt Cửa hàng](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Tab Tổng quan

Tab **Tổng quan** chứa các cài đặt chính về danh tính cửa hàng của bạn.

### Danh tính Cửa hàng

- **Tên Cửa hàng** — Tên hiển thị được hiển thị trong tiêu đề trang, email và thanh đầu trang của bảng điều khiển.
- **Dòng tiêu đề** — Mô tả ngắn về cửa hàng của bạn, được sử dụng trong SEO và chia sẻ trên mạng xã hội.
- **URL Trang web** — Địa chỉ web công khai của cửa hàng. Điều này được sử dụng trong email, tạo sitemap và xây dựng liên kết.

### Thông tin Liên hệ

- **Email Liên hệ** — Nhận thông báo đơn hàng và được hiển thị trong giao tiếp với khách hàng.
- **Số Điện thoại** — Số điện thoại hỗ trợ tùy chọn được hiển thị trong chân trang và email.

### Địa chỉ Doanh nghiệp

Nhập địa chỉ đầy đủ của bạn (đường, thành phố, tiểu bang, mã bưu điện, quốc gia). Điều này được sử dụng cho:
- Tính toán điểm xuất phát giao hàng
- Tính toán thuế
- Yêu cầu pháp lý và hóa đơn

## Thương hiệu

### Logo

Tải lên logo cửa hàng của bạn (PNG hoặc SVG được khuyến khích, ~200x50px với nền trong suốt). Logo xuất hiện ở:
- Thanh đầu trang cửa hàng
- Mẫu email
- Bảng điều khiển quản trị

### Favicon

Tải lên favicon hình vuông (ICO hoặc PNG, 32x32px). Nó xuất hiện như:
- Biểu tượng tab trình duyệt
- Biểu tượng thư mục đánh dấu
- Biểu tượng màn hình chính di động

## Địa phương hóa

### Ngôn ngữ Mặc định

Chọn ngôn ngữ chính cho cửa hàng của bạn từ 10 tùy chọn được hỗ trợ:

| Ngôn ngữ | Mã |
|----------|------|
| Tiếng Anh | en |
| Tiếng Tây Ban Nha | es |
| Tiếng Pháp | fr |
| Tiếng Đức | de |
| Tiếng Bồ Đào Nha | pt |
| Tiếng Nhật | ja |
| Tiếng Trung Quốc đơn giản | zh-hans |
| Tiếng Trung Quốc truyền thống | zh-hant |
| Tiếng Nga | ru |
| Tiếng Ả Rập | ar |

Ngôn ngữ mặc định kiểm soát ngôn ngữ giao diện bảng điều khiển và sự thay thế cho nội dung cửa hàng.

### Múi giờ

Chọn múi giờ cho cửa hàng của bạn để đảm bảo thời gian đơn hàng chính xác, khuyến mãi được lên kế hoạch và báo cáo.

### Tiền tệ

- **Tiền tệ Mặc định** — Tiền tệ chính cho giá cả và kế toán.
- **Nhiều Tiền tệ** — Kích hoạt để cho phép khách hàng xem giá theo tiền tệ ưa thích của họ với chuyển đổi tự động bằng tỷ giá hối đoái thời gian thực.

Cấu hình tiền tệ bổ sung trong **Cài đặt > Cài đặt Cửa hàng > Tiền tệ**.

## Cài đặt Thương mại điện tử

### Thanh toán Không cần Tài khoản

Cho phép mua hàng mà không cần tạo tài khoản:
- Quy trình thanh toán nhanh hơn
- Giảm bớt sự phức tạp cho người mua lần đầu
- Thu thập ít dữ liệu khách hàng hơn

### Thời điểm Tạo Tài khoản

Kiểm soát thời điểm khách hàng được yêu cầu tạo tài khoản:

| Tùy chọn | Mô tả |
|--------|-------------|
| **Sau Khi Mua (Được khuyến khích)** | Yêu cầu tạo tài khoản sau khi đơn hàng thành công — tận dụng lòng tốt sau mua hàng để chuyển đổi tốt nhất |
| **Trong Quy trình Thanh toán** | Tạo tài khoản trước khi thanh toán được xử lý |
| **Trước Khi Thanh toán** | Yêu cầu tài khoản trước khi mua sắm (không được khuyến khích — làm giảm tỷ lệ chuyển đổi) |

Bạn cũng có thể đặt tùy chỉnh **Thông điệp Tạo Tài khoản** để giải thích lợi ích của việc đăng ký.

### Cài đặt Kho hàng

- **Theo dõi Kho hàng** — Kích hoạt theo dõi tồn kho toàn cục
- **Ngưỡng Kho hàng Thấp** — Mức tồn kho tại đó thông báo hết hàng được gửi đến email quản trị (mặc định: 10 đơn vị)

## Thông minh Kho hàng

![Thẻ Thông minh Kho hàng hiển thị các trường Default Reorder Lead Time, Safety Stock Multiplier, Velocity Calculation Window, Allow Backorders by Default, và Low Stock Alert Frequency](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Những cài đặt này điều chỉnh các tính toán tự động về đặt hàng lại, hàng tồn kho an toàn và tốc độ bán hàng, đồng thời kiểm soát cách xử lý các tình huống hết hàng và tồn kho thấp.

- **Thời gian Giao hàng Mặc định (Ngày)** — Số ngày trung bình bạn mất để nhận hàng tồn kho từ nhà cung cấp của bạn một khi bạn đặt hàng (mặc định: 14).

Việc dự báo sử dụng điều này để đánh dấu các sản phẩm cần được đặt hàng lại *ngay lập tức* để tránh hết hàng trước khi hàng hóa mới đến.
- **Hệ số an toàn** — Một lớp đệm được áp dụng trên nhu cầu dự kiến để hấp thụ các đợt tăng doanh số hoặc chậm trễ từ nhà cung cấp.

Ví dụ, một hệ số là `1.5` sẽ tạo ra một lớp đệm 50% trên hệ số an toàn đã tính toán của bạn; `2.0` sẽ nhân đôi nó.

Tăng giá trị này cho các sản phẩm mà việc hết hàng là tốn kém (sản phẩm bán chạy, hàng mùa vụ); giảm giá trị này cho hàng tồn kho chậm bán mà bạn không muốn đặt hàng quá nhiều.
- **Khoảng thời gian tính tốc độ (ngày)** — Khoảng thời gian xem lại mà Spwig sử dụng để tính tốc độ bán hàng của mỗi sản phẩm, từ đó đưa ra gợi ý đặt hàng và số ngày tồn kho (mặc định: 30).

Khoảng thời gian ngắn phản hồi nhanh hơn với các thay đổi nhu cầu gần đây; khoảng thời gian dài làm mịn các đợt tăng trưởng theo mùa để một tuần bận rộn duy nhất không làm lệch dự báo.
- **Cho phép đặt hàng trước theo mặc định** — Cài đặt đặt hàng trước được áp dụng cho các sản phẩm được tạo mới (tắt theo mặc định).

Mỗi sản phẩm vẫn có thể ghi đè nó riêng trên trang sản phẩm của nó, và các sản phẩm hiện có giữ nguyên cài đặt mà chúng đã có — việc thay đổi này chỉ thay đổi cài đặt mặc định mà các sản phẩm mới bắt đầu với, nó không cập nhật lại danh mục của bạn theo chiều ngược lại.
- **Tần suất thông báo hàng tồn kho thấp** — Tần suất mà ứng dụng di động Spwig được thông báo về hàng tồn kho thấp: **Thời gian thực** gửi thông báo đẩy ngay khi một sản phẩm vượt qua ngưỡng hàng tồn kho thấp; **Tin tức hàng ngày** và **Tóm tắt hàng tuần** thay vào đó gửi một thông báo đẩy tổng hợp tất cả các sản phẩm tồn kho thấp hiện tại theo lịch trình đó.

Cài đặt này chỉ có hiệu lực khi **Thông báo hàng tồn kho** (Cài đặt Email, bên dưới) được bật — với thông báo tắt, không có thông báo nào được gửi ở bất kỳ tần suất nào.

### Tài liệu & Hóa đơn

![Thẻ Tài liệu & Hóa đơn hiển thị các trường Mã số Thuế / Số VAT, Văn bản Chân hóa đơn, Văn bản Chân phiếu đóng gói, và Kích thước Logo Tài liệu được điền bằng các giá trị ví dụ](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Các trường này điền vào hóa đơn và phiếu đóng gói mà Spwig tạo ra cho các đơn hàng — ví dụ khi một người bán tải xuống hoặc gửi email hóa đơn PDF, hoặc in phiếu đóng gói cho một đơn hàng.

- **Mã số Thuế / Số VAT** — Số nhận dạng thuế doanh nghiệp của bạn. Được in trên hóa đơn được tạo ra để chúng đáp ứng các yêu cầu tài liệu thuế địa phương.
- **Văn bản Chân hóa đơn** — Văn bản tự do được hiển thị ở cuối mỗi hóa đơn được tạo ra. Các mục phổ biến: điều khoản thanh toán ("Thanh toán trong vòng 30 ngày"), lời cảm ơn, hoặc chi tiết chuyển khoản ngân hàng.
- **Văn bản Chân phiếu đóng gói** — Văn bản tự do được hiển thị ở cuối mỗi phiếu đóng gói được tạo ra. Các mục phổ biến: hướng dẫn trả lại hoặc ghi chú cho đội ngũ kho/fulfillment.
- **Kích thước Logo Tài liệu (px)** — Kích thước logo cửa hàng của bạn khi xuất hiện trên hóa đơn và phiếu đóng gói PDF (mặc định: 200px). Chiều cao được điều chỉnh tự động để phù hợp, vì vậy tỷ lệ logo của bạn được giữ nguyên. Hình ảnh logo của bạn đến từ **Logo** (Thương hiệu, phía trên) — các logo SVG không được vẽ trên tài liệu PDF, vì vậy hãy tải lên phiên bản PNG hoặc JPG của logo nếu bạn sử dụng nghệ thuật vector trên trang web.

## Cài đặt Email

Thiết lập các cài đặt giao tiếp email trong **Cài đặt > Tài khoản Email** và **Cài đặt > Mẫu Email**. Xem [Cấu hình Email](/help/email-configuration) để biết chi tiết đầy đủ.

Các cài đặt email chính có sẵn trong Cài đặt Cửa hàng:

- **Email xác nhận đơn hàng** — Bật email xác nhận tự động trên hoặc tắt
- **Email thông báo vận chuyển** — Bật thông báo cập nhật vận chuyển trên hoặc tắt
- **Thông báo hàng tồn kho thấp** — Gửi thông báo đến email quản trị khi hàng tồn kho giảm dưới ngưỡng
- **Chế độ Giao hàng Email** — Sống (giao hàng bình thường), Tạm dừng (giữ tất cả email), hoặc Ghi lại (ghi nhận nhưng không bao giờ gửi)
- **Email chuyển hướng kiểm tra** — Chuyển tất cả email đầu ra đến một địa chỉ duy nhất để kiểm tra

## Cài đặt Bảo mật

### Xác thực Hai yếu tố (2FA)

Kiểm soát xem nhân viên có bắt buộc sử dụng xác thực hai yếu tố hay không:

{
  "Setting": "Mô tả",
  "---------": "-------------",
  "**Tùy chọn**": "Nhân viên có thể chọn bật 2FA nhưng không bắt buộc",
  "**Được khuyến khích**": "Nhân viên sẽ thấy thông báo khuyến khích họ thiết lập 2FA",
  "**Bắt buộc**": "Nhân viên không thể truy cập admin cho đến khi 2FA được bật",
  
  "- **Thời gian chờ (ngày)**" : "Số ngày nhân viên có để thiết lập 2FA sau khi việc áp dụng được kích hoạt",
  "- **Cho phép thiết bị đáng tin cậy**" : "Cho phép nhân viên bỏ qua xác minh 2FA trên các thiết bị được nhận diện trong một số ngày nhất định",
  
  "## Đồng ý cookie",
  "Cấu hình thanh đồng ý cookie được hiển thị cho khách truy cập cửa hàng:",
  "- **Đồng ý cookie đã bật**" : "Hiển thị hoặc ẩn thanh đồng ý cookie",
  "- **Vị trí thanh**" : "Nơi thanh xuất hiện trên màn hình (thanh dưới, hộp thoại góc, v.v.)",
  "- **Chế độ đồng ý**" : "Thông báo đơn giản, chọn tham gia hoặc chọn không tham gia",
  "- **Tiêu đề và nội dung thanh**" : "Tiêu đề và mô tả có thể tùy chỉnh được hiển thị cho khách truy cập",
  "- **Mô tả danh mục**" : "Mô tả riêng cho cookie phân tích, quảng cáo và chức năng",
  
  "Tất cả các trường văn bản thanh đồng ý đều hỗ trợ dịch thuật cho các cửa hàng đa ngôn ngữ."
  
  "## Giao tiếp",
  "Thẻ **Giao tiếp** điều khiển cách cửa hàng của bạn nhận, xác nhận và cho phép khách hàng quản lý sự đồng ý cho email và SMS tiếp thị. Các cài đặt này xác định tư thế tuân thủ pháp lý của bạn (GDPR cho email, TCPA cho SMS), vì vậy hãy xem xét chúng với luật sư của riêng bạn trước khi ra mắt — Spwig cung cấp các công cụ, không phải lời khuyên.",
  
  "![Thẻ Giao tiếp hiển thị các thẻ Email Tiếp thị, Lựa chọn và Hủy đăng ký, và SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)"
  
  "### Đồng ý Email Tiếp thị",
  "- **Bật xác nhận kép cho email tiếp thị**" : "Khi bật, một khách hàng đăng ký email tiếp thị sẽ nhận được email xác nhận và phải nhấp vào liên kết trong đó trước khi Spwig gửi bất kỳ thông báo tiếp thị nào cho họ. Khi tắt, việc chọn ô đăng ký tiếp thị là đủ. Mặc định được bật, theo hướng dẫn tốt nhất của GDPR.",
  "- **Trạng thái đăng ký tiếp thị mặc định**" : "Trạng thái đăng ký tiếp thị ban đầu được áp dụng cho các tài khoản khách hàng mới. Mặc định tắt (GDPR chọn không tham gia), do đó khách hàng mới bắt đầu ở trạng thái không đăng ký email tiếp thị cho đến khi họ chủ động đăng ký.",
  
  "Khi xác nhận kép được bật, việc đăng ký sẽ kích hoạt email xác nhận với liên kết xác minh. Cho đến khi khách hàng nhấp vào nó, họ được ghi nhận là đã đăng ký nhưng chưa xác minh, và các cuộc gửi tiếp thị sẽ bỏ qua họ — email giao dịch (xác nhận đơn hàng, cập nhật vận chuyển, khôi phục mật khẩu) bao giờ cũng không bị ảnh hưởng bởi cài đặt này.",
  
  "### Lựa chọn và Hủy đăng ký",
  "- **Bật Trung tâm Lựa chọn của Khách hàng**" : "Khi bật, khách hàng có thể quản lý lựa chọn email và SMS của họ từ trang tự phục vụ được liên kết từ bảng điều khiển tài khoản của họ. Khi tắt, trang đó và API hỗ trợ của nó sẽ trả về không khả dụng và liên kết bảng điều khiển bị ẩn. Liên kết hủy đăng ký một bước trong email của bạn vẫn hoạt động trong mọi trường hợp — lối thoát này là bắt buộc cho việc tuân thủ và không bị ảnh hưởng bởi nút chuyển đổi này.",
  "- **Thu thập lý do hủy đăng ký**" : "Khi bật, trang hủy đăng ký một bước hỏi khách hàng một lý do ngắn trước khi xác nhận: 'Tôi nhận được quá nhiều email', 'Nội dung không liên quan đến tôi', 'Tôi chưa đăng ký', 'Tôi không còn quan tâm', hoặc 'Khác'. Lý do khách hàng chọn được ghi nhận vào nhật ký kiểm toán đồng ý để bạn có thể xem xét các mô hình hủy đăng ký theo thời gian.",
  
  "### Đồng ý SMS",
  "- **Yêu cầu xác minh SMS**" : "Khi bật (mặc định), khách hàng phải xác minh số điện thoại của họ bằng mã một lần trước khi Spwig gửi bất kỳ tin nhắn SMS nào, bao gồm cả tin nhắn tiếp thị. Khi tắt, việc chọn ô đăng ký SMS là đủ để bắt đầu gửi. Mặc định đã được thay đổi thành **bật** cho an toàn TCPA — chỉ tắt nếu bạn có bước xác minh khác trong quy trình đăng ký của mình.",
  
  "## Chế độ Bảo trì",
  "Kích hoạt chế độ bảo trì để đưa cửa hàng của bạn tạm thời offline:"
  "- Hiển thị thông báo bảo trì tùy chỉnh cho khách truy cập",
  "- Bạn có thể liên kết một **Trang Bảo trì** được xây dựng bằng Trình xây dựng Trang để có trải nghiệm thương hiệu đầy đủ",
  "- Hạn chế truy cập chỉ cho người dùng admin",
  "- Ích lợi trong các lần cập nhật lớn hoặc di dời",
  
  "Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật."
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
- **Từ khóa Meta** — Từ khóa phân tách bằng dấu phẩy mặc định

## Cài đặt Thuế

Cấu hình việc thu thập thuế tại **Cài đặt > Cài đặt Thuế**:

1. **Phương pháp Tính toán** — Theo địa chỉ giao hàng, địa chỉ thanh toán hoặc vị trí cửa hàng
2. **Tỷ lệ Thuế** — Xác định tỷ lệ theo khu vực và lớp thuế sản phẩm
3. **Hiển thị Thuế** — Hiển thị giá cả có thuế, không có thuế, hoặc cả hai

## Lời khuyên

- Đặt múi giờ chính xác trước khi xử lý đơn hàng nào — điều này ảnh hưởng đến tất cả thời điểm và báo cáo.
- Bật chế độ thanh toán không cần tài khoản để cải thiện tỷ lệ chuyển đổi.
- Điền địa chỉ doanh nghiệp của bạn để tính toán vận chuyển và thuế chính xác.
- Tải lên cả logo và favicon để có trải nghiệm chuyên nghiệp, mang tính thương hiệu.
- Sử dụng thời điểm **Tạo tài khoản Sau khi Mua hàng** để đạt được tỷ lệ đăng ký tốt nhất.
- Bật chế độ **Yêu cầu Xác thực Hai yếu tố** cho nhân viên để bảo vệ cửa hàng admin của bạn.
- Kiểm tra luồng email bằng cài đặt **Email Chuyển tiếp Thử nghiệm** trước khi phát hành.
- Thiết lập **Thời gian Giai đoạn Dự báo Đặt hàng Lại** để phù hợp với nhà cung cấp chậm nhất của bạn — dự báo đặt hàng áp dụng giá trị này cho toàn bộ danh mục sản phẩm của bạn, vì vậy hãy chọn giá trị có thời gian giao hàng dài nhất.
- Ngắn gọn **Khoảng thời gian Tính toán Tốc độ** nếu bạn chạy các chương trình khuyến mãi hoặc nhập hàng thường xuyên và muốn dự báo phản ứng nhanh với doanh số trong vài ngày gần đây; kéo dài nó để có cái nhìn ổn định, ít bị gián đoạn hơn về nhu cầu.
- Nếu bạn bật **Cho phép Đặt hàng trước theo Mặc định**, hãy nhớ rằng nó chỉ đặt điểm bắt đầu cho các sản phẩm được tạo *sau* khi thay đổi — quay lại các sản phẩm hiện có nếu bạn muốn đặt hàng trước được bật trên danh mục hiện tại của bạn nữa.
- Đồng bộ **Tần suất Cảnh báo Hết hàng** với cách bạn quản lý hàng tồn kho: **Thời gian thực** cho danh mục di chuyển nhanh nơi mà mọi rủi ro hết hàng đều cần sự chú ý ngay lập tức, **Bản tóm tắt Hàng ngày** hoặc **Tóm tắt Hàng tuần** để tránh kiệt sức thông báo trên danh mục lớn.
- Điền vào **Mã số Thuế / Số VAT** và văn bản chân trang trước khi hóa đơn đầu tiên của bạn gửi cho khách hàng — cả hai trường đều trống theo mặc định.
- Nếu **Logo** của bạn là SVG, hãy tải lên phiên bản PNG hoặc JPG nữa — **Chiều rộng Logo Tài liệu** không ảnh hưởng đến PDF vì Spwig không thể vẽ nghệ thuật SVG trên hóa đơn và phiếu đóng gói được tạo ra.
- Giữ nguyên **Bật Xác minh Hai bước cho Email Tiếp thị** trừ khi bạn có lý do cụ thể để tắt nó — đó là cài đặt mặc định an toàn cho GDPR và nó bảo vệ danh tính người gửi của bạn bằng cách giữ các địa chỉ chưa xác minh khỏi việc gửi email tiếp thị.
- Giữ nguyên **Trạng thái Tùy chọn Tiếp thị Mặc định** ở chế độ tắt. Việc chọn trước tùy chọn đồng ý tiếp thị cho tài khoản mới làm suy yếu yêu cầu đồng ý GDPR ngay cả khi khách hàng có thể gỡ bỏ nó.
- Không tắt **Bật Trung tâm Ưu tiên Khách hàng** chỉ để đơn giản hóa bảng điều khiển tài khoản của bạn — mà không có nó, khách hàng vẫn có thể hủy đăng ký một loại thông báo cụ thể, nhưng họ mất khả năng tùy chỉnh ưu tiên (ví dụ: giữ cập nhật vận chuyển nhưng bỏ qua tin tức).
- Giữ nguyên **Yêu cầu Xác minh SMS** ở chế độ bật trừ khi quy trình đăng ký của bạn đã xác minh số điện thoại theo cách khác (ví dụ: đăng nhập dựa trên SMS) — cài đặt này tồn tại đặc biệt để giữ bạn trong các quy định TCPA.

## Xử lý sự cố

**Các thay đổi không xuất hiện trên cửa hàng trực tuyến:**
- Xóa bộ nhớ cache trình duyệt của bạn
- Chạy lệnh xóa bộ nhớ cache từ bảng điều khiển quản trị
- Kiểm tra xem chế độ bảo trì có được bật tình cờ hay không

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