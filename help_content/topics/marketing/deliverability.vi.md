---
title: Hướng dẫn vận hành khả năng giao email
---

<!-- screenshots-needed:
- url: /admin/email_system/emailaccount/add/
  filename: wizard-dns-step.webp
  description: Step 4 (DNS Configuration) of the email account setup wizard for the built-in SMTP provider, showing the SPF/DKIM/DMARC validation one-liners and the DNS provider tabs (Cloudflare/GoDaddy/Namecheap/Route 53/Other) with at least one record's "Details" panel expanded so a copyable TXT record is visible.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/email_system/emailaccount/{account_id}/change/
  filename: dkim-dns-record.webp
  description: An existing built-in SMTP EmailAccount's change form scrolled to the "DKIM keys configured" panel, showing the DNS TXT record Name/Value and the Copy DNS Record button.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: suppressed-addresses-card.webp
  description: The Campaign Studio dashboard's Suppressed addresses stat card, for the "monitor" section of this runbook.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
-->

Việc *gửi* một email là điều dễ dàng. Nhưng để email đến hộp thư đến thay vì thư mục spam mới là công việc thực sự — và các nhà cung cấp hộp thư như Gmail và Yahoo hiện đang áp dụng các yêu cầu kỹ thuật nghiêm ngặt trước khi họ thậm chí xem xét nó. Hướng dẫn này sẽ hướng dẫn bạn cần cấu hình những gì, theo thứ tự nào, để các xác nhận đơn hàng và chiến dịch của bạn đến đúng nơi khách hàng có thể nhìn thấy.

Không có gì ở đây là nhiệm vụ một lần. Khả năng giao email là một uy tín mà bạn xây dựng theo thời gian và có thể mất đi nhanh chóng — danh sách kiểm tra ở cuối tài liệu đáng để xem lại bất cứ khi nào có điều gì đó trông không ổn.

## Tại sao điều này quan trọng

Mọi nhà cung cấp hộp thư lớn đều chấm điểm email đến dựa trên uy tín của người gửi trước khi quyết định có giao, xếp vào thư mục spam hay từ chối hoàn toàn. Kể từ năm 2024, Gmail và Yahoo đã chính thức hóa điều này thành các **yêu cầu đối với người gửi hàng loạt** cho bất kỳ ai gửi với khối lượng đáng kể:

- **Xác thực tên miền của bạn** — các bản ghi SPF, DKIM và DMARC hợp lệ.
- **Dễ dàng hủy đăng ký** — một tùy chọn hủy đăng ký hoạt động, ít ma sát trong mọi email tiếp thị.
- **Giữ tỷ lệ khiếu nại spam thấp** — các người gửi hàng loạt vượt qua khoảng 0,3% khiếu nại có nguy cơ bị từ chối email hoặc xếp vào thư mục hàng loạt; mục tiêu an toàn nhất là dưới 0,1%.

Nếu không đáp ứng được những điều này, không chỉ các chiến dịch tiếp thị bị ảnh hưởng — uy tín tên miền bị tổn hại có thể kéo cả email giao dịch (xác nhận đơn hàng, đặt lại mật khẩu) vào thư mục spam, vì Gmail và Yahoo ngày càng đánh giá uy tín ở cấp độ tên miền gửi, chứ không chỉ theo từng loại thông điệp. Các bước dưới đây là cách bạn đáp ứng cả ba yêu cầu.

## Bước 1: Xác thực tên miền gửi

SPF, DKIM và DMARC là các bản ghi DNS TXT chứng minh cho các máy chủ email nhận rằng email tự nhận là từ tên miền của bạn thực sự do bạn gửi. Cách bạn thiết lập chúng phụ thuộc vào chế độ gửi mà cửa hàng của bạn sử dụng — cả ba đều được cấu hình dưới **Email Configuration** trong thanh bên quản trị (mở danh sách Email Accounts; xem [Email Configuration](email-configuration) để có hướng dẫn đầy đủ về thiết lập tài khoản).

| chế độ gửi | Cách xác thực hoạt động |
|---|---|
| **SMTP tích hợp sẵn** (máy chủ email của riêng Spwig) | Spwig tạo cặp khóa DKIM cho tên miền của bạn một cách tự động. Thêm tài khoản email, và **Bước 4** của trình hướng dẫn cài đặt hiển thị trạng thái SPF, DKIM và DMARC của bạn cũng như bản ghi chính xác để thêm, với tính năng sao chép vào clipboard và hướng dẫn cụ thể cho nhà cung cấp như Cloudflare, GoDaddy, Namecheap và AWS Route 53. Bản ghi DKIM DNS tương tự cũng được hiển thị trên trang quản trị riêng của tài khoản sau này, dưới **Các khóa DKIM đã được cấu hình**, nếu bạn cần tìm lại. |
| **SMTP tổng quát** (một nhà cung cấp do bạn tự cài đặt như SendGrid, Mailgun, Amazon SES hoặc Google Workspace, kết nối thông qua thông tin đăng nhập SMTP) | Việc xác thực xảy ra một phần trong dashboard riêng của nhà cung cấp đó. Bước DNS trong trình hướng dẫn cài đặt bao gồm hướng dẫn có tab riêng cho Gmail, Outlook, SendGrid, Mailgun và Amazon SES cụ thể — mỗi cái đều giải thích điều gì cần cấu hình trong console của nhà cung cấp (ví dụ: xác minh tên miền gửi trong SendGrid) và bản ghi DNS nào cần thêm tại nhà cung cấp DNS của bạn. |
| **Cổng email do Spwig cung cấp** | Có sẵn trên các kế hoạch do Spwig cung cấp như một tùy chọn gửi được quản lý. Nó ký email gửi đi bằng DKIM tự động và mặc định gửi từ địa chỉ trên tên miền đã xác minh của riêng Spwig, vì vậy nó hoạt động với việc cài đặt không cần thiết. Nếu bạn muốn gửi từ tên miền của riêng mình thông qua cổng này, hãy nói chuyện với nhà cung cấp dịch vụ lưu trữ của bạn về việc xác minh nó — đây là một dịch vụ được quản lý, không phải là quy trình DNS tự phục vụ. |

Dù bạn sử dụng chế độ nào, **việc thêm bản ghi DNS itself luôn là bước bên ngoài** — bạn thực hiện tại nhà đăng ký tên miền hoặc nhà cung cấp DNS (Cloudflare, GoDaddy, Namecheap, Route 53, hoặc bất kỳ nơi nào tên miền của bạn trỏ đến), không phải bên trong Spwig. Spwig có thể nói cho bạn biết chính xác điều bạn cần thêm và xác minh rằng nó đang hoạt động, nhưng nó không thể truy cập vào nhà đăng ký của bạn và thêm nó cho bạn.

Một số điều đáng biết trước khi bắt đầu:

- **Các thay đổi DNS không xảy ra tức thì.** Quá trình phân phối có thể mất từ vài phút đến 48 giờ. Bước kiểm tra xác minh trong trình hướng dẫn sẽ hiển thị bản ghi là thất bại hoặc thiếu nếu nó chưa thực sự phân phối — điều này là bình thường, không phải dấu hiệu cho thấy điều gì đó đang gặp sự cố.
- **Chỉ được phép có một bản ghi SPF cho mỗi tên miền.** Nếu bạn đã có một bản ghi rồi (từ Google Workspace, một máy gửi khác, v.v.), hãy thêm người gửi mới của bạn vào bản ghi hiện tại bằng `include:` thay vì tạo bản ghi TXT SPF thứ hai — hai bản ghi SPF sẽ làm hỏng xác thực cho tất cả mọi người.
- **DMARC cần SPF hoặc DKIM đã hoạt động.** Hãy thiết lập cuối cùng, khi SPF và DKIM đều đã được xác minh.

## Bước 2: Sử dụng danh tính gửi thực tế

Một khi tên miền của bạn đã được xác thực, hãy đảm bảo điều mà người nhận thực sự thấy hỗ trợ cho điều đó:

- **Địa chỉ người gửi** — sử dụng địa chỉ trên tên miền được xác thực của bạn (`orders@yourstore.com`), không bao giờ là địa chỉ của nhà cung cấp miễn phí (`yourstore@gmail.com`). Một địa chỉ người gửi từ nhà cung cấp miễn phí không thể được xác thực bởi các bản ghi SPF/DKIM/DMARC của bạn, và các nhà cung cấp hộp thư sẽ xem đây là tín hiệu spam mạnh từ một cửa hàng.
- **Tên người gửi** — sử dụng tên nhận diện cửa hàng của bạn, không phải nhãn chung như "Thông báo" hoặc "Không phản hồi".
- **Trả lời** — thiết lập một địa chỉ được giám sát. Một địa chỉ `noreply@` không được giám sát mà bị chặn hoặc tự động xóa các phản hồi là chính nó là tín hiệu đánh giá nhẹ, và nó chặn kênh duy nhất mà khách hàng có thể báo cho bạn biết điều gì đó đã sai.

Thiết lập cả ba dưới **Cài đặt Email > (tài khoản của bạn) > Cấu hình Người gửi** — xem [Cài đặt Email](email-configuration) để hướng dẫn chi tiết các trường.

## Bước 3: Làm quen trước khi mở rộng

Một tên miền hoặc IP không có lịch sử gửi hàng có nghĩa là không có danh tiếng nào cả — tốt hay xấu — và các nhà cung cấp hộp thư rất cẩn trọng với điều chưa biết. Việc gửi một đợt đầu tiên lớn từ một tên miền mới có vẻ giống hệt với một kẻ spam bắt đầu chiến dịch mới, và nó có thể bị đưa vào thư mục hàng loạt ngay cả khi mọi hộp kỹ thuật đều được kiểm tra.

- Bắt đầu nhỏ hơn.

Gửi vài chiến dịch đầu tiên của bạn đến đối tượng khán giả tương tác nhiều nhất, có khả năng mở email cao nhất, thay vì gửi cho toàn bộ danh sách ngay lập tức — xem [Audiences](audiences) để xây dựng phân khúc khởi đầu có mục tiêu.
- Tăng dần khối lượng trong vài tuần đầu tiên thay vì nhảy thẳng vào việc gửi cho toàn bộ danh sách.
- Nếu bạn đang chuyển đổi một danh sách hiện có từ nền tảng khác, hãy coi đó là ngày đầu tiên cho mục đích uy tín — lịch sử gửi email của nền tảng cũ không được chuyển sang cùng với tên miền.

## Bước 4: Giữ danh sách sạch

Mỗi khiếu nại spam hoặc email bị trả về (bounce) đều làm giảm uy tín của bạn, và cả hai phần lớn phụ thuộc vào ai có trong danh sách của bạn và họ đến đó bằng cách nào:

- **Chỉ gửi email cho những người đã đồng ý.** Các liên hệ được nhập, danh sách mua lại và địa chỉ được thu thập tự động là cách nhanh nhất để làm tăng khiếu nại spam và email bị trả về cứng (hard bounces).
- **Sử dụng xác nhận hai bước (double opt-in).** Quy trình đồng ý tiếp thị của Spwig xác minh địa chỉ email của người đăng ký trước khi gửi email tiếp thị cho họ — xem [Communication Preferences](communication-preferences) để biết cách cấu hình này.
- **Để tính năng tự động chặn (suppression) của Spwig thực hiện công việc của nó.** Spwig theo dõi các email bị trả về cứng, khiếu nại spam và các email bị trả về mềm (soft bounces) lặp đi lặp lại, sau đó tự động ngừng gửi email đến các địa chỉ đó mà không cần thiết lập — xem [List Hygiene and Suppressions](list-hygiene) để biết chính xác cách hoạt động này và khi nào (hiếm khi) cần ghi đè.
- **Loại bỏ các người đăng ký không hoạt động định kỳ** thay vì gửi email cho cùng một địa chỉ không tương tác vô thời hạn — một danh sách nhỏ dần nhưng mở và nhấp chuột có giá trị hơn cho uy tín của bạn so với một danh sách lớn nhưng không tương tác.

## Bước 5: Giám sát

Các vấn đề về khả năng giao hàng (deliverability) xuất hiện trong các con số trước khi khách hàng báo cho bạn rằng email không đến.

Mở [Report](campaign-reports) của một chiến dịch sau mỗi lần gửi và theo dõi:

| Chỉ số | Cần chú ý điều gì |
|---|---|
| **Tỷ lệ bounce** | Chủ yếu là soft bounces là bình thường; tỷ lệ **hard bounce** tăng lên có nghĩa là danh sách của bạn đang tích lũy các địa chỉ cũ hoặc không hợp lệ. |
| **Khiếu nại spam** | Nên ở mức gần bằng không trong mỗi lần gửi. Giữ nó dưới ngưỡng khoảng 0,3% kích hoạt thực thi đối với người gửi hàng loạt tại Gmail và Yahoo — coi ngay cả một sự tăng vọt nhỏ cũng đáng để điều tra ngay lập tức. |
| **Tỷ lệ mở / tỷ lệ nhấp so với mở** | Một sự sụt giảm đột ngột, không giải thích được qua các lần gửi đến cùng một danh sách (không chỉ một chiến dịch) có thể là dấu hiệu sớm rằng email đang rơi vào thư mục spam thay vì hộp thư đến, ngay cả trước khi các con số về bounce hoặc khiếu nại thay đổi. |

Kiểm tra định kỳ thẻ **Suppressed addresses** trên bảng điều khiển Campaign Studio — một dòng chảy ổn định là sự suy giảm danh sách bình thường, nhưng một sự tăng vọt đột ngột đáng để điều tra trước lần gửi tiếp theo của bạn (xem [List Hygiene](list-hygiene)).

Nếu có điều gì đó tăng vọt: tạm dừng và kiểm tra xem các bản ghi DNS của bạn có còn hợp lệ không trước tiên (việc gia hạn tên miền hết hạn hoặc thay đổi DNS vô tình có thể làm hỏng SPF/DKIM một cách im lặng), sau đó xem xét điều gì đã thay đổi về nội dung hoặc đối tượng của lần gửi đã kích hoạt nó.

## Bước 6: Vệ sinh nội dung

Xác thực và chất lượng danh sách giúp bạn vào cửa; nội dung vẫn ảnh hưởng đến cách bạn được đối xử một khi đã ở đó.

- **Tránh các mẫu gây kích hoạt spam** trong tiêu đề — CHỮ IN HOA, dấu câu quá mức ("!!!"), và các cụm từ như "hành động ngay" hoặc "tiền miễn phí" vẫn gây bất lợi cho bạn với bộ lọc spam, ngay cả từ một tên miền đã được xác thực.
- **Đừng gửi email chỉ chứa hình ảnh.** Một email là một hình ảnh đơn lẻ không có văn bản thực sự là một mẫu spam điển hình; giữ một lượng văn bản nội dung thực sự có ý nghĩa bên cạnh bất kỳ hình ảnh nào.
- **Xem trước trước khi gửi.** Kiểm tra cách email thực sự hiển thị — bao gồm trên thiết bị di động — trước khi nó được gửi đến toàn bộ danh sách của bạn.
- **Liên kết hủy đăng ký đã được xử lý.** Spwig tự động thêm một liên kết hủy đăng ký hoạt động, không cần đăng nhập vào chân trang của mọi email tiếp thị — bạn không cần phải thêm liên kết của riêng mình (xem [Communication Preferences](communication-preferences) để biết chính xác quy trình đó hoạt động như thế nào). Đừng xóa hoặc ẩn nó; một liên kết hủy đăng ký bị thiếu hoặc hỏng chính nó là một vi phạm chính sách với các quy tắc người gửi hàng loạt của Gmail và Yahoo, bất kể các con số khác của bạn.

## "Email của tôi bị vào hộp thư rác" — danh sách kiểm tra khắc phục sự cố

Thực hiện theo thứ tự sau:

1. **Kiểm tra lại các bản ghi DNS của bạn.** Mở bước DNS trong trình hướng dẫn thiết lập của tài khoản (hoặc bảng DKIM trên trang quản trị của tài khoản cho SMTP tích hợp) và xác nhận rằng SPF, DKIM và DMARC đều vẫn hiển thị là đạt. Việc gia hạn tên miền, di chuyển nhà cung cấp DNS, hoặc một thay đổi không liên quan đến tệp zone của bạn có thể vô tình làm hỏng một trong những cấu hình này.
2. **Kiểm tra số lượng email bị trả lại (bounce) và khiếu nại trong báo cáo chiến dịch** cho các lần gửi bị ảnh hưởng — xem [Báo cáo chiến dịch](campaign-reports). Sự gia tăng đột biến ở bất kỳ chỉ số nào cho thấy vấn đề về chất lượng danh sách hoặc nội dung, chứ không phải vấn đề xác thực.
3. **Kiểm tra danh sách Ức chế** ([Vệ sinh danh sách](list-hygiene)) xem có sự tăng đột biến nào không — nếu một phần lớn danh sách của bạn đã gặp sự cố trong một thời gian, khả năng giao thành công cho phần còn lại cũng sẽ giảm.
4. **Xác nhận địa chỉ From của bạn nằm trên tên miền đã được xác thực**, không phải là địa chỉ của nhà cung cấp miễn phí hoặc tên miền không khớp với cấu hình SPF/DKIM/DMARC.
5. **Gửi một email thử nghiệm đến một địa chỉ Gmail và một địa chỉ Yahoo/Outlook do bạn kiểm soát** và kiểm tra thư mục thực tế mà email được đưa vào, chứ không chỉ là việc nó có đến hay không.
6. **Nếu bạn gần đây đã thay đổi đột ngột khối lượng gửi hoặc đối tượng nhận,** hãy coi đó như một quá trình làm nóng (warm-up) mới — giảm khối lượng xuống và tăng dần từ từ hơn.
7. **Nếu tất cả các mục trên đều ổn và vấn đề vẫn tiếp diễn,** có thể đó là do việc giới hạn lưu lượng (throttling) cụ thể của nhà cung cấp thay vì lỗi trong cấu hình của bạn — điều này có thể mất một thời gian để tự khắc phục sau khi nguyên nhân gốc (thường là khiếu nại hoặc email bị trả lại) đã được xử lý.

## Mẹo

- Sửa xác thực DNS trước khi sửa bất kỳ thứ gì khác — mọi công cụ giao thành công khác (nội dung, vệ sinh danh sách, làm nóng) đều kém quan trọng hơn nếu SPF/DKIM/DMARC không đạt.
- Coi việc xác thực DNS của trình hướng dẫn thiết lập là một kiểm tra tại một thời điểm cụ thể, không phải là kiểm tra một lần duy nhất — chạy lại bất cứ khi nào bạn di chuyển nhà cung cấp DNS hoặc gia hạn tên miền thông qua một nhà đăng ký khác.
- Một danh sách sạch sẽ, có tỷ lệ mở và nhấp cao luôn hiệu quả hơn một danh sách lớn nhưng không tương tác — hãy kìm chế mong muốn nhập một danh sách cũ, chưa được xác thực "chỉ để phòng trường hợp".
- Theo dõi các chỉ số của bạn so với lịch sử gửi trước đó của chính bạn, chứ không phải một tiêu chuẩn ngành chung chung — lịch sử của chính bạn là tín hiệu đáng tin cậy nhất về một vấn đề thực sự.
- Nếu bạn đang sử dụng gói dịch vụ do Spwig lưu trữ, việc ký DKIM và quản lý danh tiếng của cổng email lưu trữ sẽ được xử lý thay cho bạn — trách nhiệm còn lại của bạn là chất lượng danh sách và nội dung, chứ không phải DNS.