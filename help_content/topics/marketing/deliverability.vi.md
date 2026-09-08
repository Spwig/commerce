---
title: Hướng dẫn vận hành khả năng giao email
---

Việc *gửi* một email là điều dễ dàng. Việc đưa email vào hộp thư đến thay vì thư mục spam mới là công việc thực sự — và các nhà cung cấp hộp thư như Gmail và Yahoo hiện đang áp dụng các yêu cầu kỹ thuật nghiêm ngặt trước khi họ thậm chí xem xét nó. Hướng dẫn này đi qua những gì cần cấu hình, theo thứ tự nào, để các xác nhận đơn hàng và chiến dịch của bạn đến đúng nơi khách hàng có thể nhìn thấy.

Không có gì ở đây là nhiệm vụ một lần. Khả năng giao email là một uy tín mà bạn xây dựng theo thời gian và có thể mất đi nhanh chóng — danh sách kiểm tra ở cuối đáng để xem xét lại bất cứ khi nào có điều gì đó trông không ổn.

## Tại sao điều này quan trọng

Mọi nhà cung cấp hộp thư lớn đều chấm điểm email đến dựa trên uy tín của người gửi trước khi quyết định có giao, gộp vào thư mục spam hay từ chối hoàn toàn. Kể từ năm 2024, Gmail và Yahoo đã chính thức hóa điều này thành các **yêu cầu người gửi hàng loạt** rõ ràng cho bất kỳ ai gửi với khối lượng đáng kể:

- **Xác thực tên miền của bạn** — các bản ghi SPF, DKIM và DMARC hợp lệ.
- **Dễ dàng hủy đăng ký** — một tùy chọn hủy đăng ký hoạt động, ít ma sát trong mọi email tiếp thị.
- **Giữ khiếu nại spam ở mức thấp** — các người gửi hàng loạt vượt qua ngưỡng khoảng 0,3% khiếu nại có nguy cơ bị từ chối email hoặc gộp vào thư mục hàng loạt; mục tiêu an toàn nhất là dưới 0,1%.

Thất bại trong những điều này không chỉ ảnh hưởng đến các chiến dịch tiếp thị — uy tín tên miền bị tổn hại có thể kéo cả email giao dịch (xác nhận đơn hàng, đặt lại mật khẩu) vào spam, vì Gmail và Yahoo ngày càng đánh giá uy tín ở cấp độ tên miền gửi, chứ không chỉ theo từng loại thông điệp. Các bước dưới đây là cách bạn đáp ứng cả ba yêu cầu.

## Bước 1: Xác thực tên miền gửi của bạn

SPF, DKIM và DMARC là các bản ghi DNS TXT chứng minh cho các máy chủ email nhận rằng email tuyên bố là từ tên miền của bạn thực sự do bạn gửi. Cách bạn thiết lập chúng phụ thuộc vào chế độ gửi mà cửa hàng của bạn sử dụng — cả ba đều được cấu hình dưới **Cấu hình Email** trong thanh bên quản trị (mở danh sách Tài khoản Email; xem [Cấu hình Email](email-configuration) để biết hướng dẫn thiết lập tài khoản đầy đủ).

| Chế độ gửi | Cách xác thực hoạt động |
|---|---|
| **SMTP tích hợp** (máy chủ email riêng của Spwig) | Spwig tự động tạo cặp khóa DKIM cho tên miền của bạn. Thêm một tài khoản email, và **Bước 4** của trình hướng dẫn thiết lập sẽ hiển thị trạng thái SPF, DKIM và DMARC của bạn cùng bản ghi chính xác cần thêm, với tính năng sao chép vào clipboard và hướng dẫn cụ thể cho nhà cung cấp cho Cloudflare, GoDaddy, Namecheap và AWS Route 53. Bản ghi DNS DKIM tương tự cũng được hiển thị trên trang quản trị riêng của tài khoản sau đó, dưới **Các khóa DKIM đã cấu hình**, nếu bạn cần tìm lại nó. |
| **SMTP chung** (một nhà cung cấp tự mang theo như SendGrid, Mailgun, Amazon SES hoặc Google Workspace, kết nối thông qua thông tin xác thực SMTP) | Xác thực diễn ra một phần trong bảng điều khiển riêng của nhà cung cấp đó. Bước DNS của trình hướng dẫn thiết lập bao gồm các hướng dẫn dạng tab dành riêng cho Gmail, Outlook, SendGrid, Mailgun và Amazon SES — mỗi hướng dẫn giải thích những gì cần cấu hình trong console của nhà cung cấp (ví dụ: xác thực tên miền gửi trong SendGrid) và các bản ghi DNS kết quả nào cần thêm tại nhà cung cấp DNS của bạn. |
| **Cổng email do Spwig lưu trữ** | Có sẵn trong các gói lưu trữ của Spwig như một tùy chọn gửi được quản lý. Nó ký email đi bằng DKIM tự động và mặc định gửi từ một địa chỉ trên tên miền đã xác thực của chính Spwig, vì vậy nó hoạt động với cấu hình bằng không. Nếu bạn muốn gửi từ tên miền của mình thông qua cổng, hãy nói chuyện với nhà cung cấp lưu trữ của bạn về việc xác thực nó — đây là một dịch vụ được quản lý, không phải là luồng DNS tự phục vụ. |

![Bước 4 của trình hướng dẫn thiết lập tài khoản email, hiển thị xác thực SPF/DKIM/DMARC, các tab nhà cung cấp DNS và một bản ghi DKIM đã mở sẵn sàng để sao chép](/static/core/admin/img/help/deliverability/wizard-dns-step.webp)

![Bảng các khóa DKIM đã cấu hình của một tài khoản email SMTP tích hợp hiện có, với bản ghi DNS TXT và nút Sao chép Bản ghi DNS](/static/core/admin/img/help/deliverability/dkim-dns-record.webp)

Dù bạn sử dụng chế độ nào, **việc thêm bản ghi DNS luôn là một bước bên ngoài** — bạn thực hiện điều này tại nhà đăng ký tên miền hoặc nhà cung cấp DNS (Cloudflare, GoDaddy, Namecheap, Route 53, hoặc bất kỳ nơi nào mà nameserver của tên miền bạn trỏ đến), chứ không phải bên trong Spwig.

Spwig có thể cho bạn biết chính xác cần thêm gì và xác minh rằng bản ghi đã hoạt động, nhưng nó không thể truy cập vào nhà đăng ký của bạn để thêm thay cho bạn.

Một vài điều đáng biết trước khi bắt đầu:

- **Thay đổi DNS không diễn ra ngay lập tức.** Quá trình lan truyền có thể mất từ vài phút đến 48 giờ. Bước xác minh của trình hướng dẫn sẽ hiển thị bản ghi là thất bại hoặc thiếu cho đến khi nó thực sự lan truyền — điều này là bình thường, không phải dấu hiệu có gì sai sót.
- **Mỗi tên miền chỉ được phép có một bản ghi SPF.** Nếu bạn đã có một bản ghi (từ Google Workspace, một trình gửi thư khác, v.v.), hãy thêm người gửi mới của bạn vào bản ghi hiện có bằng `include:` thay vì tạo một bản ghi TXT SPF thứ hai — hai bản ghi SPF sẽ làm hỏng xác thực cho tất cả mọi người.
- **DMARC cần SPF hoặc DKIM đã vượt qua trước đó.** Hãy thiết lập nó cuối cùng, sau khi cả SPF và DKIM đều đã được xác minh.

## Bước 2: Sử dụng danh tính gửi thực

Sau khi tên miền của bạn được xác thực, hãy đảm bảo những gì người nhận thực sự thấy phù hợp với điều đó:

- **Địa chỉ From** — sử dụng một địa chỉ trên tên miền đã được xác thực của riêng bạn (`orders@yourstore.com`), không bao giờ sử dụng địa chỉ của nhà cung cấp miễn phí (`yourstore@gmail.com`). Địa chỉ From của nhà cung cấp miễn phí không thể được xác thực bởi các bản ghi SPF/DKIM/DMARC của bạn, và các nhà cung cấp hộp thư đến coi đó là một tín hiệu spam mạnh từ một cửa hàng.
- **Tên From** — sử dụng tên dễ nhận biết của cửa hàng bạn, không phải một nhãn chung chung như "Thông báo" hoặc "Không trả lời".
- **Reply-to** — thiết lập một địa chỉ được giám sát. Một địa chỉ `noreply@` không được giám sát mà bị trả lại hoặc âm thầm loại bỏ các phản hồi chính nó là một tín hiệu danh tiếng nhẹ, và nó chặn kênh duy nhất mà khách hàng có thể dùng để báo cho bạn biết có điều gì đó không ổn.

Thiết lập cả ba dưới **Email Configuration > (tài khoản của bạn) > Sender Configuration** — xem [Email Configuration](email-configuration) để có hướng dẫn chi tiết từng trường.

## Bước 3: Làm nóng trước khi mở rộng

Một tên miền hoặc IP không có lịch sử gửi thư chưa có danh tiếng — tốt hay xấu — và các nhà cung cấp hộp thư đến thận trọng với những gì không rõ ràng. Gửi một đợt lớn đầu tiên từ một tên miền mới hoàn toàn trông giống hệt về mặt thống kê với một kẻ spam bắt đầu chiến dịch mới, và nó có thể bị chuyển vào thư mục spam hàng loạt ngay cả khi mọi hộp kỹ thuật đều được kiểm tra.

- Bắt đầu nhỏ hơn. Gửi vài chiến dịch đầu tiên của bạn cho đối tượng tương tác nhiều nhất, có khả năng mở cao nhất thay vì toàn bộ danh sách cùng một lúc — xem [Audiences](audiences) để xây dựng một phân khúc khởi đầu có mục tiêu.
- Tăng dần khối lượng trong vài tuần đầu tiên thay vì nhảy thẳng vào việc gửi cho toàn bộ danh sách.
- Nếu bạn đang di chuyển một danh sách hiện có từ một nền tảng khác, hãy coi đó là ngày đầu tiên về mặt danh tiếng — lịch sử gửi thư của nền tảng cũ của bạn không được chuyển sang cùng với tên miền.

## Bước 4: Giữ danh sách của bạn sạch sẽ

Mỗi khiếu nại hoặc email bị trả lại đều làm giảm danh tiếng của bạn, và cả hai phần lớn là chức năng của ai đó trong danh sách của bạn và cách họ đến đó:

- **Chỉ gửi email cho những người đã đồng ý.** Các liên hệ được nhập, danh sách mua và địa chỉ cào là cách nhanh nhất để làm tăng khiếu nại spam và email bị trả lại cứng.
- **Sử dụng xác nhận hai bước (double opt-in).** Luồng đồng ý tiếp thị của Spwig xác minh địa chỉ email của người đăng ký trước khi gửi cho họ email tiếp thị — xem [Communication Preferences](communication-preferences) để biết cách cấu hình này.
- **Để chế độ ức chế tự động của Spwig làm việc.** Spwig theo dõi các email bị trả lại cứng, khiếu nại spam và các email bị trả lại mềm lặp đi lặp lại và tự động ngừng gửi email cho các địa chỉ đó, không cần thiết lập — xem [List Hygiene and Suppressions](list-hygiene) để biết chính xác cách hoạt động này và khi nào (hiếm khi) cần ghi đè.
- **Loại bỏ các người đăng ký không hoạt động định kỳ** thay vì gửi email cho cùng các địa chỉ không tương tác vô thời hạn — một danh sách thu nhỏ nhưng mở và nhấp chuột có giá trị hơn cho danh tiếng của bạn so với một danh sách lớn nhưng không làm vậy.

## Bước 5: Giám sát

Các vấn đề về khả năng giao thư sẽ thể hiện qua các con số trước khi khách hàng báo cho bạn rằng email không đến được.

Mở [Báo cáo](campaign-reports) của chiến dịch sau mỗi lần gửi và theo dõi:

| Chỉ số | Cần chú ý điều gì |
|---|---|
| **Tỷ lệ trả thư (Bounce rate)** | Chủ yếu là trả thư mềm (soft bounces) là bình thường; tỷ lệ **trả thư cứng (hard bounce)** tăng lên có nghĩa là danh sách của bạn đang tích lũy các địa chỉ cũ hoặc không hợp lệ. |
| **Khiếu nại spam** | Nên duy trì ở mức gần bằng 0 sau mỗi lần gửi. Giữ mức này thấp hơn đáng kể so với ngưỡng khoảng 0,3% kích hoạt cơ chế thực thi cho người gửi hàng loạt tại Gmail và Yahoo — coi ngay cả một sự tăng vọt nhỏ cũng cần được điều tra ngay lập tức. |
| **Tỷ lệ mở / Tỷ lệ nhấp vào sau khi mở** | Sự sụt giảm đột ngột, không rõ nguyên nhân qua các lần gửi đến cùng một danh sách (không chỉ một chiến dịch) có thể là dấu hiệu sớm cho thấy email đang rơi vào thư mục spam thay vì hộp thư đến, ngay cả trước khi các con số về trả thư hoặc khiếu nại thay đổi. |

Định kỳ kiểm tra thẻ **Địa chỉ bị chặn (Suppressed addresses)** trên bảng điều khiển Campaign Studio — một dòng chảy ổn định là sự suy giảm tự nhiên của danh sách, nhưng một sự tăng vọt đột ngột đáng để điều tra trước lần gửi tiếp theo của bạn (xem [Vệ sinh danh sách](list-hygiene)).

![Thẻ thống kê Địa chỉ bị chặn trên bảng điều khiển Campaign Studio](/static/core/admin/img/help/deliverability/suppressed-addresses-card.webp)

Nếu có chỉ số nào tăng vọt: hãy tạm dừng và kiểm tra xem các bản ghi DNS của bạn có còn hợp lệ không trước tiên (việc gia hạn tên miền hết hạn hoặc thay đổi DNS vô tình có thể làm hỏng SPF/DKIM một cách âm thầm), sau đó xem xét điều gì đã thay đổi về nội dung hoặc đối tượng của lần gửi đã gây ra vấn đề.

## Bước 6: Vệ sinh nội dung

Xác thực và chất lượng danh sách giúp bạn bước qua cánh cửa; nội dung vẫn ảnh hưởng đến cách bạn được đối xử một khi đã ở bên trong.

- **Tránh các mẫu hình kích hoạt spam** trong dòng tiêu đề — CHỮ IN HOA, dấu câu quá mức ("!!!"), và các cụm từ như "hành động ngay" hoặc "tiền miễn phí" vẫn gây bất lợi cho bạn với các bộ lọc spam, ngay cả khi gửi từ một tên miền đã được xác thực.
- **Đừng gửi email chỉ chứa hình ảnh.** Một email chỉ là một hình ảnh duy nhất mà không có văn bản thực sự là một mẫu hình spam điển hình; hãy giữ một lượng nội dung văn bản thực sự có ý nghĩa bên cạnh bất kỳ hình ảnh nào.
- **Xem trước trước khi gửi.** Kiểm tra cách email thực sự hiển thị — bao gồm cả trên thiết bị di động — trước khi nó được gửi đến toàn bộ danh sách của bạn.
- **Liên kết hủy đăng ký đã được xử lý sẵn.** Spwig tự động thêm một liên kết hủy đăng ký hoạt động, không yêu cầu đăng nhập vào phần chân trang của mọi email marketing — bạn không cần phải thêm liên kết của riêng mình (xem [Tùy chọn liên lạc](communication-preferences) để biết chính xác quy trình đó hoạt động như thế nào). Đừng xóa hoặc ẩn nó; một liên kết hủy đăng ký bị thiếu hoặc hỏng bản thân nó là một vi phạm chính sách với các quy tắc người gửi hàng loạt của Gmail và Yahoo, bất kể các chỉ số khác của bạn.

## "Email của tôi đang rơi vào thư mục spam" — danh sách kiểm tra khắc phục sự cố

Thực hiện theo các bước này theo thứ tự:

1. **Kiểm tra lại các bản ghi DNS của bạn.** Mở bước DNS của trình hướng dẫn thiết lập tài khoản (hoặc bảng DKIM trên trang quản trị của tài khoản cho SMTP tích hợp) và xác nhận rằng SPF, DKIM và DMARC đều vẫn hiển thị là đạt.

Việc gia hạn tên miền, di chuyển nhà cung cấp DNS, hoặc một thay đổi không liên quan đến tệp zone của bạn có thể làm hỏng một trong những thứ này một cách âm thầm.
2. **Kiểm tra các con số về trả thư và khiếu nại trong báo cáo chiến dịch** cho các lần gửi bị ảnh hưởng — xem [Báo cáo chiến dịch](campaign-reports).


Một sự gia tăng về điểm số cho thấy vấn đề về chất lượng danh sách hoặc nội dung, chứ không phải vấn đề về xác thực.
3. **Kiểm tra danh sách các địa chỉ bị từ chối** ([Làm sạch danh sách](list-hygiene)) để phát hiện sự gia tăng đột ngột — nếu một lượng lớn danh sách của bạn đã bị lỗi trong một thời gian dài, khả năng giao hàng cho phần còn lại cũng sẽ bị suy giảm.
4. **Xác minh địa chỉ 'Từ' của bạn nằm trong miền đã xác thực**, chứ không phải là địa chỉ của nhà cung cấp miễn phí hoặc một miền không khớp với những gì SPF/DKIM/DMARC đã được thiết lập.
5. **Gửi một email thử đến địa chỉ Gmail và Yahoo/Outlook mà bạn kiểm soát** và kiểm tra xem nó có rơi vào thư mục thực sự nào không, thay vì chỉ kiểm tra xem nó có đến được hay không.
6. **Nếu bạn vừa thay đổi khối lượng gửi hoặc đối tượng người nhận một cách đột ngột**, hãy xem đây là quá trình làm quen lại — giảm khối lượng gửi xuống và tăng dần dần hơn.
7. **Nếu tất cả các điều trên đều kiểm tra được và vấn đề vẫn còn tồn tại**, có thể đây là sự giới hạn tốc độ do nhà cung cấp gây ra, chứ không phải do lỗi trong thiết lập của bạn — điều này có thể mất một khoảng thời gian để tự giải quyết khi nguyên nhân cơ bản (thường là khiếu nại hoặc lỗi giao hàng) đã được khắc phục.

## Mẹo

- Sửa lỗi xác thực DNS trước khi sửa lỗi nào khác — mọi yếu tố giao hàng khác (nội dung, làm sạch danh sách, quá trình làm quen) sẽ ít quan trọng hơn nếu SPF/DKIM/DMARC không đạt.
- Xem xét kiểm tra DNS trong trình hướng dẫn thiết lập như một kiểm tra điểm thời điểm, chứ không phải là một lần duy nhất — chạy lại bất cứ khi nào bạn chuyển đổi nhà cung cấp DNS hoặc gia hạn miền thông qua nhà đăng ký khác.
- Một danh sách sạch sẽ có thể mở và nhấp vào nhiều hơn so với danh sách lớn hơn nhưng không có hiệu quả — hãy kiềm chế việc nhập danh sách cũ, chưa được xác minh 'chỉ vì sợ.'
- Theo dõi các con số của bạn so với các lần gửi trước của bạn, thay vì một chỉ số ngành chung — lịch sử của chính bạn là tín hiệu đáng tin cậy nhất cho một vấn đề thực sự.
- Nếu bạn đang ở trên gói được Spwig cung cấp, việc ký số DKIM và quản lý uy tín của cổng thư được Spwig thực hiện thay cho bạn — trách nhiệm còn lại của bạn là chất lượng danh sách và nội dung, chứ không phải DNS.