---
title: Báo cáo chiến dịch
---

<!-- screenshots-needed:
- url: /admin/campaigns/{campaign_id}/report/
  filename: engagement-over-time-chart.webp
  description: The report page scrolled to the "Engagement over time" chart card, with a campaign that has several days of send history so all three lines (Sent, Opened, Clicked) show a realistic shape.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: top-links-table.webp
  description: The report page's "Top links" card, with a campaign whose email contains at least 3 distinct links and a realistic spread of Clicks/Unique/CTR values.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipients-list.webp
  description: The Recipients page with the filters panel open and a mixed list of rows (some opened, some clicked, some bounced) so the engagement states are visibly distinct.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipient-activity-modal.webp
  description: The Recipients page with the "Recipient activity" modal open for a recipient who has multiple event types (delivered, opened, at least one clicked entry naming a link).
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: attributed-revenue-card.webp
  description: A close-up of the report page's "Attributed revenue" stat card, for a campaign with a logged Spend so the orders/AOV/revenue-per-email/ROAS sub-line is fully populated.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: dashboard-attributed-revenue-kpi.webp
  description: The Campaign Studio dashboard's stat card grid, scrolled/cropped to show the "Attributed revenue (30d)" tile alongside its neighboring cards, with a non-zero revenue figure.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: report-stat-cards.webp
  description: 'RECAPTURE NEEDED: the existing report-stat-cards.webp only shows 6 cards (Recipients, Delivered, Open rate, Click rate, Bounce rate, Spam complaints). The stat grid now has a 7th "Attributed revenue" card — recapture this shot with a campaign that has both attribution data and a logged Spend so all 7 cards are visible in a realistic state.'
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
-->

Mỗi chiến dịch bạn gửi qua Campaign Studio đều có một trang **Báo cáo** riêng — một trang tóm tắt cho biết chiến dịch đã tiếp cận bao nhiêu người, bao nhiêu email thực sự được giao thành công và người nhận đã phản hồi như thế nào. Hãy sử dụng trang này để kiểm tra xem việc gửi email có diễn ra suôn sẻ không, phát hiện sớm các vấn đề về khả năng giao email, hoặc so sánh hiệu suất của các chiến dịch khác nhau theo thời gian.

## Mở báo cáo

Từ **Campaign Studio > Campaigns**, tìm chiến dịch bạn muốn kiểm tra và nhấp vào biểu tượng biểu đồ (**Report**) trên thẻ của chiến dịch đó.

![Lưới thẻ thống kê trên trang báo cáo chiến dịch, hiển thị số người nhận, số email đã giao, tỷ lệ mở, tỷ lệ nhấp, tỷ lệ trả lại và khiếu nại spam](/static/core/admin/img/help/campaign-reports/report-stat-cards.webp)

Báo cáo chỉ hiển thị số liệu khi chiến dịch đã thực sự được gửi — một chiến dịch vẫn ở trạng thái **Draft** sẽ hiển thị mọi chỉ số bằng số không, vì chưa có gì để đo lường.

## Các thẻ thống kê

| Card | What it shows |
|------|---------------|
| **Người nhận** | Số lượng người đăng ký mà chiến dịch này nhắm đến, kèm theo dòng phụ ghi nhận số lượng đã bị bỏ qua và, trong số đó, số lượng bị bỏ qua do địa chỉ nằm trong danh sách [loại bỏ](list-hygiene). Việc bỏ qua không phải lúc nào cũng là loại bỏ — Spwig cũng bỏ qua một người đăng ký nếu không có địa chỉ email hợp lệ, ví dụ — vì vậy hai số liệu này được hiển thị riêng biệt. |
| **Đã gửi** | Số lượng email thực sự được máy chủ thư nhận và không bao giờ bị trả lại, kèm theo **tỷ lệ gửi thành công** — số đã gửi tính theo tỷ lệ mỗi lần gửi mà Spwig *thử* (được máy chủ hoặc nhà cung cấp của bạn chấp nhận, bất kể sau đó có bị trả lại hay không). |
| **Tỷ lệ mở** | Tỷ lệ *email đã gửi* được mở, kèm theo số **mở** nguyên bản. |
| **Tỷ lệ nhấp chuột** | Tỷ lệ *email đã gửi* được nhấp chuột, kèm theo số **nhấp chuột** nguyên bản và **tỷ lệ nhấp chuột so với mở** — số nhấp chuột tính theo tỷ lệ mở, một chỉ số phản ánh mức độ hấp dẫn nội dung của bạn với những người đã mở email. |
| **Tỷ lệ trả lời** | Tỷ lệ *lượt gửi đã thử* bị trả lại, được phân chia thành **lượt trả lời cố định** và **lượt trả lời tạm thời**. |
| **Phản hồi spam** | Số lượng người nhận đã đánh dấu email là spam hoặc thư rác, kèm theo **tỷ lệ phản hồi** — số phản hồi tính theo tỷ lệ *email đã gửi*. |
| **Doanh thu được ghi nhận** | Doanh thu từ các đơn hàng mà Spwig có thể truy xuất về chiến dịch này, kèm theo số lượng đơn hàng, giá trị trung bình mỗi đơn hàng (**AOV**), doanh thu trên mỗi email đã gửi, và — một khi bạn đã ghi nhận chi phí của chiến dịch — **ROAS** của nó. Xem [Doanh thu được ghi nhận](#attributed-revenue) bên dưới. |

## Tại sao các tỷ lệ sử dụng mẫu số khác nhau

Tỷ lệ mở, tỷ lệ nhấp chuột và tỷ lệ phản hồi đều được đo dựa trên email *đã gửi* — những người nhận có thể xem được email — trong khi tỷ lệ gửi thành công và tỷ lệ trả lời được đo dựa trên *lượt gửi đã thử*. Đây là cách tiêu chuẩn trong ngành email, và đây là lý do tại sao không có tỷ lệ nào có thể vượt quá 100%: một email bị trả lại không bao giờ được gửi đi, vì vậy nó không thể tính vào tỷ lệ mở hoặc tỷ lệ nhấp chuột, và một email chưa từng được gửi đi (bị bỏ qua) không tính vào bất kỳ tỷ lệ nào cả.

## Lượt trả lời cố định so với lượt trả lời tạm thời

- **Lượt trả lời cố định** — địa chỉ không thể gửi đến được mãi mãi. Nó không tồn tại, hoặc tên miền từ chối nhận thư cho địa chỉ đó.
- **Lượt trả lời tạm thời** — vấn đề tạm thời: hộp thư đầy, máy chủ nhận tạm thời không khả dụng, và các tình huống tương tự. Lượt trả lời tạm thời thường tự động được giải quyết.

Hãy theo dõi sự phân chia, không chỉ tổng số. Số lượng **lượt trả lời cố định** tăng lên thường cho thấy danh sách của bạn có địa chỉ lỗi thời hoặc bị gõ sai; số lượng **lượt trả lời tạm thời** tăng lên thường là do sự cố nhất thời ở phía người nhận. Bất kỳ lượt trả lời cố định nào, bất kỳ phản hồi spam nào, và một địa chỉ nào đó có số lượt trả lời tạm thời tăng lên đều làm cho danh sách [loại bỏ](list-hygiene) tự động của Spwig — bạn không cần phải hành động riêng, nhưng báo cáo là nơi bạn sẽ phát hiện đầu tiên về một sự cố đáng kể.

## Doanh thu được ghi nhận

Vì cửa hàng của bạn và Studio Chiến dịch cùng tồn tại trong cùng một hệ thống, Spwig không cần nền tảng phân tích bên thứ ba hoặc pixel theo dõi để biết xem chiến dịch thực sự có thúc đẩy doanh số hay không. Khi một khách hàng nhấp vào liên kết trong email của chiến dịch này và đến cửa hàng của bạn, Spwig có thể theo dõi hành trình đó đến khi thanh toán và ghi nhận doanh thu của đơn hàng đó về chiến dịch — đó là điều mà thẻ **Doanh thu được ghi nhận** thể hiện.

Dòng phụ của thẻ này phân tích kỹ hơn số liệu:

- **Đơn hàng** — số lượng đơn hàng được ghi nhận cho chiến dịch này.
- **AOV** — giá trị trung bình mỗi đơn hàng trên các đơn hàng đó.
- **Doanh thu trên mỗi email** — doanh thu được ghi nhận chia cho số lượng email *đã gửi*, cùng mẫu số mà báo cáo sử dụng cho tỷ lệ mở và tỷ lệ nhấp chuột.
- **ROAS** — tỷ lệ lợi nhuận trên chi phí quảng cáo, được hiển thị chỉ khi bạn đã nhập **Chi phí** cho chính chiến dịch.

Nó được tính bằng doanh thu được ghi nhận chia cho chi phí.

Nếu chi phí được ghi nhận bằng loại tiền tệ khác với tiền tệ mặc định của cửa hàng bạn, Spwig sẽ ẩn ROAS thay vì hiển thị một con số không thể so sánh trực tiếp — hãy nhập chi phí bằng tiền tệ cơ sở của cửa hàng bạn để xem kết quả.

Một số điều cần biết về cách con số này được tính toán:

- **Đây là số liệu dựa trên lần nhấp chuột, không phải dựa trên lần mở email.** Người dùng phải nhấp vào liên kết được theo dõi trong email và đến được cửa hàng của bạn — việc mở email một mình sẽ không bao giờ ghi nhận doanh thu. Đây là điều có chủ đích: việc theo dõi mở email đang ngày càng không chính xác do các dịch vụ như Bảo vệ Quyền riêng tư của Apple tải trước hình ảnh cho gần như mọi tin nhắn, làm tăng số lần mở email bất kể ai có thực sự đọc email hay không.
- **Nó tuân theo mô hình phân bổ doanh thu của cửa hàng bạn.** Mặc định đó là **lần chạm cuối không phải trực tiếp** với khoảng thời gian xem lại 90 ngày — cùng một lần nhấp chuột phải dẫn đến đơn hàng trong khoảng thời gian này để được tính, và một lần ghé thăm trực tiếp sau đó sẽ không xóa bỏ quyền lợi đã được ghi nhận bởi lần nhấp chuột của chiến dịch này.
- **Nó tôn trọng sự đồng ý của người dùng về phân tích.** Chỉ có những khách hàng đã đồng ý với chính sách phân tích trong thanh cookie của cửa hàng bạn mới được theo dõi (nếu bạn không chạy thanh đồng ý, việc theo dõi sẽ tuân theo chính sách mặc định của cửa hàng bạn). Một khách hàng đã từ chối sự đồng ý vẫn có thể mua hàng — đơn hàng của họ sẽ không được ghi nhận cho bất kỳ kênh nào, bao gồm cả kênh này.
- **Nó không có hiệu lực ngược.** Việc theo dõi doanh thu chỉ bao gồm các chiến dịch được gửi sau khi theo dõi phân bổ được kích hoạt cho cửa hàng của bạn. Một chiến dịch được gửi trước đó sẽ hiển thị không có doanh thu được ghi nhận ở đây ngay cả khi nó đã tạo ra doanh số thực tế, đơn giản là Spwig không có dữ liệu nhấp chuột được ghi nhận cho chiến dịch đó.
- **Các cuộc thử nghiệm A/B và chiến dịch định kỳ cũng tổng hợp doanh thu được ghi nhận** — xem [Báo cáo về một cuộc thử nghiệm A/B](#reports-on-an-ab-test) bên dưới.

Bạn cũng sẽ tìm thấy một thẻ **Doanh thu được ghi nhận (30 ngày)** trên bảng điều khiển Studio Chiến dịch, tổng hợp doanh thu được ghi nhận từ email trên mọi chiến dịch trong vòng 30 ngày qua — một kiểm tra nhanh mà không cần mở báo cáo riêng lẻ. Đối với cái nhìn tổng thể của toàn bộ cửa hàng bao gồm mọi kênh, không chỉ có email — tìm thấy [Phân tích Doanh thu](/help/revenue-attribution) dưới mục **Nhận diện**.

## Sự tương tác theo thời gian

Dưới các thẻ thống kê, biểu đồ **Tương tác theo thời gian** vẽ ba đường — **Đã gửi**, **Đã mở**, và **Đã nhấp** — mỗi ngày một điểm, bao gồm 30 ngày trước ngày hôm nay (hoặc ít hơn nếu chiến dịch chưa gửi được lâu như vậy — biểu đồ không bao giờ bắt đầu sớm hơn ngày đầu tiên gửi chiến dịch).

Một số điều cần biết về cách các đường được đếm:

- **Đã mở** và **Đã nhấp** đếm mỗi người nhận một lần — ngày mà *lần mở đầu tiên* hoặc *lần nhấp đầu tiên* của họ — không phải mỗi lần họ mở lại email hoặc nhấp vào liên kết lần nữa. Điều này giúp biểu đồ không bị lệch do một số ít người mở email cùng một lần nhiều lần.
- Các con số đằng sau biểu đồ này khớp với các thẻ thống kê phía trên: **Đã gửi** phản ánh số email mà Spwig đã cố gắng giao, trong khi **Đã mở** và **Đã nhấp** đều được đo dựa trên email đã được giao, giống như các thẻ **Tỷ lệ mở** và **Tỷ lệ nhấp**.
- Biểu đồ chỉ xuất hiện khi chiến dịch có ít nhất một lần gửi được ghi nhận — một chiến dịch vẫn ở trạng thái **Bản nháp** sẽ hiển thị thông báo "Chưa có lần gửi nào" thay vì biểu đồ, giống như các thẻ thống kê.

Hãy sử dụng biểu đồ này để xem *hình dạng* của một lần gửi, chứ không chỉ các con số cuối cùng — một chiến dịch được gửi đến danh sách lớn thường cho thấy sự gia tăng đột ngột về số lần mở vào ngày đầu tiên hoặc ngày thứ hai, sau đó giảm dần. Một đợt gia tăng thứ hai vài ngày sau có thể chỉ ra rằng máy chủ email của người nhận đang xếp hàng tin nhắn của bạn, hoặc tiêu đề email của bạn được chú ý muộn hơn bình thường.

## Các liên kết hàng đầu

Nếu email của bạn chứa các liên kết và ít nhất một người nhận đã nhấp vào một liên kết nào đó, một bảng **Các liên kết hàng đầu** sẽ xuất hiện dưới biểu đồ, liệt kê mọi liên kết được theo dõi theo thứ tự phổ biến.

| Cột | Nội dung hiển thị |
|--------|---------------|
| **Liên kết** | URL đích như đã xuất hiện trong email của bạn. |
| **Số lần nhấp** | Tổng số lần liên kết đó được nhấp, bao gồm cả các lần nhấp lặp lại từ cùng một người nhận. |
| **Độc lập** | Số lượng người nhận khác nhau đã nhấp vào liên kết cụ thể đó ít nhất một lần. |
| **CTR** | **Tỷ lệ nhấp** của liên kết đó — tỷ lệ giữa số lượng **Độc lập** và số email đã được giao thành công. Chỉ số này sử dụng cùng một mẫu số với thẻ **Tỷ lệ nhấp** tiêu đề của báo cáo, cho phép bạn so sánh sức hút của một liên kết riêng lẻ trực tiếp với hiệu suất nhấp chung của chiến dịch. |

Nếu email của bạn liên kết đến nhiều sản phẩm hoặc một tổ hợp các nút kêu gọi hành động, bảng này là cách nhanh nhất để xem liên kết nào thực sự tạo ra lượt nhấp — hữu ích cho việc quyết định nên làm nổi bật yếu tố nào hơn vào lần tới.

## Người nhận

Nhấp vào **Người nhận** ở đầu báo cáo để mở danh sách đầy đủ, có thể tìm kiếm, của tất cả những người mà chiến dịch này đã được gửi, kèm theo kết quả giao và mức độ tương tác của từng người.

Hai cách để thu hẹp danh sách:

- **Tìm kiếm** — lọc theo địa chỉ email (khớp một phần cũng được, vì vậy chỉ cần nhập một phần tên miền hoặc tên là đủ).
- **Tương tác** — lọc theo một trạng thái tại một thời điểm: **Đã mở**, **Đã nhấp**, **Đã giao, chưa mở**, hoặc **Bị trả lại**. Để ở **Tất cả** để xem danh sách đầy đủ.

Danh sách hiển thị 100 người nhận khớp gần nhất mỗi lần, mới nhất trước — số đếm phía trên danh sách luôn phản ánh tổng số thực sự khớp với bộ lọc hiện tại của bạn, ngay cả khi nó lớn hơn những gì được hiển thị. Đối với một lần gửi lớn, hãy thu hẹp danh sách bằng Tìm kiếm hoặc Tương tác trước thay vì cuộn qua tất cả mọi người.

### Xem dòng thời gian hoạt động của người nhận

Nhấp vào biểu tượng hoạt động trên dòng của bất kỳ người nhận nào để mở dòng thời gian **Hoạt động của người nhận** — mọi sự kiện được theo dõi đối với bản sao email của người đó, theo thứ tự: đã giao, đã mở, đã nhấp (ghi rõ liên kết nào), bị trả lại (kèm lý do trả lại), được đánh dấu là spam, hoặc đã hủy đăng ký, mỗi sự kiện đều có mốc thời gian riêng.

Đây là cách nhanh nhất để trả lời một câu hỏi cụ thể về một khách hàng — ví dụ, xác nhận xem một người đăng ký cụ thể có thực sự nhận được chiến dịch trước khi liên hệ lại với họ bằng kênh khác, hoặc kiểm tra liên kết nào khách hàng đã nhấp trước khi họ đặt hàng.

## Báo cáo về một bài kiểm tra A/B

Nếu chiến dịch bạn đang xem là nơi chứa một [bài kiểm tra A/B](ab-testing), báo cáo của nó sẽ tổng hợp trên **mọi biến thể** — toàn bộ bài kiểm tra, gộp lại, bao gồm cả **Doanh thu được ghi nhận** — thay vì hiển thị một biến thể riêng lẻ. Để xem hiệu suất của từng biến thể riêng lẻ, hãy mở trang kết quả của chính bài kiểm tra thay vì báo cáo. Một [chiến dịch định kỳ](recurring-campaigns) hoạt động theo cách tương tự: báo cáo của nó gộp lại mọi lần gửi đã thực hiện.

## Thế nào là tốt

Không có một con số khỏe mạnh duy nhất phù hợp với mọi cửa hàng hoặc danh sách — đối tượng, ngành và nội dung đều làm thay đổi mức cơ sở — nhưng một vài mẫu hình đáng chú ý trên bất kỳ chiến dịch nào:

- **Tỷ lệ trả lại** chủ yếu là trả lại mềm, với trả lại cứng hiếm gặp, cho thấy một danh sách sạch, được bảo trì tốt. Một sự tăng đột biến trong trả lại cứng đáng được điều tra trước lần gửi tiếp theo của bạn.
- **Khiếu nại spam** gần bằng không là mục tiêu trong mọi lần gửi. Khiếu nại làm tổn hại danh tiếng người gửi của bạn hơn hầu hết mọi thứ khác — xem [Vệ sinh danh sách](list-hygiene) để biết tại sao chúng quan trọng vượt ra ngoài chiến dịch này.
- **Tỷ lệ nhấp trên mở** khỏe mạnh so với tỷ lệ mở của bạn cho thấy những người đã mở đã tìm thấy nội dung đáng để hành động — một tỷ lệ nhấp trên mở thấp cùng với tỷ lệ mở mạnh thường cho thấy tiêu đề hoạt động tốt hơn nội dung bên trong.

## Mẹo



- Kiểm tra báo cáo một chút sau khi gửi, không phải ngay lập tức — các chỉ số như lượt mở và lượt nhấp chuột (cùng một số báo cáo về việc bị từ chối) có thể mất thời gian để cập nhật từ nhà cung cấp dịch vụ email của bạn.
- Nếu **Đã gửi** nhìn chung thấp hơn mong đợi, hãy kiểm tra phần **Người nhận** và phân tích số lượng người bị bỏ qua trước — một loạt các trường hợp bị từ chối do bị cấm thường là nguyên nhân chính, chứ không phải vấn đề về việc gửi.
- Sử dụng báo cáo này để so sánh chiến dịch của bạn với các lần gửi trước của chính bạn, thay vì so sánh với một con số chung của ngành — danh sách, nội dung và đối tượng người dùng của bạn chính là yếu tố xác định cơ sở thực tế cho chiến dịch của bạn.
- Một sự gia tăng về số lượng khiếu nại trong một lần gửi cụ thể nào đó cần được xem xét kỹ hơn về nội dung hoặc đối tượng nhắm đến của chiến dịch đó, thay vì chỉ ghi nhận và chuyển sang chiến dịch tiếp theo.
- Với chiến dịch được kiểm tra A/B, hãy đọc báo cáo này để biết kết quả tổng thể và truy cập trang [Kết quả kiểm tra A/B](ab-testing) để biết phiên bản nào thực sự đã chiến thắng và mức độ chiến thắng là bao nhiêu.
- Sử dụng bảng **Các liên kết hàng đầu** để tìm ra liên kết được nhấp nhiều nhất, sau đó kiểm tra xem nó có khớp với điều bạn *muốn* người nhận nhấp chuột hay không — nếu một liên kết phụ vượt qua nút gọi hành động chính của bạn, có thể bạn nên đặt nó cao hơn trong email lần sau.
- Các bộ lọc **Đã mở** và **Đã nhấp** trên trang **Người nhận** là cách nhanh để xây dựng một nhóm đối tượng phản hồi — ví dụ, kiểm tra xem ai đã mở nhưng không nhấp chuột trước khi lên kế hoạch gửi nhắc nhở cho phần còn lại của danh sách.
- Nếu bạn chi trả cho một chiến dịch quảng bá xung quanh một lần gửi — một bài đăng mạng xã hội được tăng tốc, một lời giới thiệu từ người nổi tiếng, hoặc thuê danh sách — hãy ghi nhận nó dưới mục **Chi phí** của chiến dịch để mở khóa **ROAS** trên báo cáo.

Đây là cách nhanh nhất để xem loại chiến dịch nào thực sự đáng để lặp lại.