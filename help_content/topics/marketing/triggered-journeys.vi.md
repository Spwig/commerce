---
title: Hành trình được kích hoạt
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/{journey_id}/report/
  filename: journey-report.webp
  description: The Journey report page for a journey with meaningful enrollment history — the enrollment funnel cards (Enrolled/Active now/Completed/Exited) and Attributed revenue card both showing non-zero numbers, plus the "Revenue by step" table (Step/Revenue/Orders/Sent/Opens/Clicks) with at least one plain step and one A/B step, both showing real Sent/Opens/Clicks counts.
  save-to: core/static/core/admin/img/help/triggered-journeys/
  viewport: 1440x900
-->

**Journeys** (Hành trình) trong Campaign Studio là các chuỗi email tự động, nhiều bước, được khởi động một cách tự động bất cứ khi nào khách hàng thực hiện một hành động cụ thể — đăng ký, đặt hàng, bỏ sản phẩm trong giỏ hàng, im lặng trong một thời gian, hoặc đơn hàng được giao. Thay vì phải nhớ gửi email chào mừng, nhắc nhở khôi phục giỏ hàng hoặc yêu cầu đánh giá thủ công, bạn chỉ cần xây dựng chuỗi một lần và Spwig sẽ thực hiện cho mọi khách hàng đủ điều kiện, trong suốt thời gian hành trình còn hoạt động.

## Ba cách gửi email

Campaign Studio hiện bao phủ ba mẫu gửi riêng biệt:

| Loại | Hành vi |
|------|-----------|
| **Broadcast** (Phát sóng) | Gửi một lần — ngay lập tức hoặc vào một ngày và giờ đã lên lịch. Dùng cho thông báo hoặc khuyến mãi một lần. |
| **Recurring** (Định kỳ) | Một mẫu được gửi theo lịch lặp lại (xem [Recurring Campaigns](/help/recurring-campaigns)). |
| **Journey** (Hành trình) | Một chuỗi nhiều bước được khởi động tự động cho một khách hàng khi một sự kiện vòng đời xảy ra, sau đó triển khai các bước của nó trong vài giờ hoặc vài ngày. |

Một hành trình không có nút "gửi" riêng và không có lịch để cấu hình — nó phản ứng với các sự kiện thay vì đồng hồ.

## Các bộ kích hoạt (Triggers)

Mỗi hành trình lắng nghe đúng một sự kiện, được đặt làm **Trigger** (Bộ kích hoạt) của hành trình:

| Trigger | Kích hoạt khi |
|---------|-----------|
| **Customer signs up** (Khách hàng đăng ký) | Một tài khoản khách hàng mới được tạo. |
| **Order is placed** (Đặt hàng) | Bất kỳ đơn hàng nào được đặt, bởi khách hàng mới hoặc quay lại. |
| **First order is placed** (Đặt đơn hàng đầu tiên) | Cụ thể là đơn hàng đầu tiên của một khách hàng. |
| **Cart abandoned** (Bỏ giỏ hàng) | Một người mua thêm thứ gì đó vào giỏ hàng, sau đó ngừng hoạt động mà không thanh toán. |
| **Customer lapsed (win-back)** (Khách hàng ngừng mua (thu hút lại)) | Một khách hàng đã không đặt hàng trong một thời gian. |
| **Order delivered** (Đơn hàng được giao) | Trạng thái của đơn hàng thay đổi thành Đã giao. |
| **Product back in stock** (Sản phẩm có lại hàng) | Một sản phẩm mà khách hàng đã yêu cầu được thông báo lại có sẵn.

## Chi tiết về các bộ kích hoạt khôi phục và thu hút lại

**Order delivered** (Đơn hàng được giao) và **Product back in stock** (Sản phẩm có lại hàng) được kích hoạt ngay lập tức, giống cách **Order is placed** (Đặt hàng) hoạt động. **Cart abandoned** (Bỏ giỏ hàng) và **Customer lapsed (win-back)** (Khách hàng ngừng mua (thu hút lại)) hoạt động khác: thay vì phản ứng với một khoảnh khắc duy nhất, Spwig định kỳ kiểm tra các người mua và khách hàng phù hợp, do đó có thể có một độ trễ ngắn giữa việc giỏ hàng ngừng hoạt động (hoặc khách hàng ngừng mua) và việc ghi danh.

**Cart abandoned** (Bỏ giỏ hàng) — ghi danh một người mua đã thêm thứ gì đó vào giỏ hàng và sau đó ngừng hoạt động mà không hoàn tất thanh toán. Mặc định, điều này xảy ra sau khoảng một giờ không hoạt động; cửa sổ thời gian không hoạt động chính xác (và Spwig sẽ tìm kiếm ngược lại bao xa) là một ngưỡng mà chủ nhà có thể điều chỉnh cho cửa hàng của bạn. Nó hoạt động cho cả người mua đã đăng nhập và khách vãng lai — đối với khách vãng lai, Spwig sử dụng địa chỉ email được thu thập tại bước thanh toán. Nếu người mua quay lại và hoàn tất đơn hàng, họ sẽ tự động được loại khỏi hành trình, vì vậy một giao dịch hoàn thành sẽ không bao giờ nhận được email "bạn quên thứ gì đó?". Thêm một khối nội dung **Abandoned Cart** (Giỏ hàng bị bỏ) vào email khôi phục để hiển thị chính xác những gì đã bị bỏ lại, với giá cả trực tiếp, hình ảnh và liên kết quay lại giỏ hàng — hoặc sử dụng khối **Featured Product** (Sản phẩm nổi bật) để làm nổi bật một mặt hàng thay thế.

**Customer lapsed (win-back)** (Khách hàng ngừng mua (thu hút lại)) — ghi danh một khách hàng đã không đặt hàng trong một thời gian, để cho họ một lý do để quay lại.

Mặc định, đó là 90 ngày không mua hàng (cũng là một ngưỡng có thể điều chỉnh bởi chủ nhà).

Một khách hàng chỉ được nhập vào hành trình phục hồi một lần duy nhất trong khoảng thời gian đó, vì vậy một người từng ngừng hoạt động sẽ không được ghi danh lại ngay lập tức.

**Đơn hàng đã giao** — ghi danh khách hàng một lần khi trạng thái đơn hàng thay đổi thành **Đã giao**, đây là thời điểm tự nhiên để yêu cầu đánh giá sau vài ngày. Sự kiện này chỉ xảy ra một lần cho mỗi đơn hàng, khi chuyển đổi sang trạng thái Đã giao — các chỉnh sửa sau này cho đơn hàng đã giao sẽ không kích hoạt lại sự kiện này. Lưu ý rằng hành động **Ghi nhận các đơn hàng đã chọn là Đã giao** trong danh sách đơn hàng cập nhật trực tiếp đơn hàng và không kích hoạt sự kiện này (hoặc email xác nhận giao hàng); hãy cập nhật từng đơn hàng một, hoặc thông qua ứng dụng di động Spwig, để sự kiện này được kích hoạt.

**Sản phẩm trở lại tồn kho** — khi một sản phẩm mà khách hàng đã yêu cầu được thông báo trở lại tồn kho, Spwig kiểm tra xem bạn có một hành trình đang hoạt động để lắng nghe sự kiện này không. Nếu có, khách hàng sẽ được ghi danh vào hành trình đó thay vì thông báo một lần duy nhất — vì vậy bạn có thể thêm khoảng thời gian chờ, một khối **Sản phẩm Nổi bật** hiển thị sản phẩm đã hết hàng, hoặc một email theo dõi. Nếu không có hành trình trở lại tồn kho nào đang hoạt động, khách hàng vẫn nhận được email thông báo một lần duy nhất như trước đây, do đó việc kích hoạt một hành trình cho sự kiện này là hoàn toàn tùy chọn.

## Xây dựng một hành trình

Đi tới **Studio Chiến dịch > Hành trình** và nhấn **Thêm Hành trình**.

1. Đặt cho hành trình một **Tên** — đây là để bạn tham khảo; khách hàng sẽ không bao giờ nhìn thấy nó.
2. Chọn sự kiện **Kích hoạt**.
3. Tùy chọn đặt **Chỉ cho đoạn** thành một đoạn — khi được đặt, chỉ những người đăng ký thuộc đoạn đó mới được ghi danh. Để trống để ghi danh mọi người đăng ký đủ điều kiện.
4. Đặt **Một lần cho mỗi người đăng ký** và **Khoảng thời gian chờ trước khi ghi danh lại (ngày)** — xem [Bảo vệ chống ghi danh quá nhiều](#guarding-against-over-enrollment) bên dưới.
5. Đặt **Trạng thái** thành **Đang hoạt động** để kích hoạt hành trình. Giữ nguyên ở **Bản nháp** khi bạn vẫn đang thiết kế, hoặc đặt thành **Tạm dừng** để dừng ghi danh mới mà không làm mất thiết lập của bạn.
6. Nhấn **Lưu** — Spwig sẽ đưa bạn trực tiếp vào [Journey Builder](/help/journey-builder), bảng canvas trực quan nơi bạn thiết kế chuỗi thực tế: email nào được gửi, khoảng thời gian chờ giữa chúng là bao lâu, và liệu các người đăng ký khác nhau có theo các con đường khác nhau hay không.

Một chuỗi chào mừng ba bước đơn giản, sau khi được thiết kế trên bảng vẽ, có thể trông như sau:

| Bước | Thời gian chờ | Gửi | 
|------|-------|-------| 
| 1 | Ngay lập tức | Email Chào mừng | 
| 2 | Sau 3 ngày | Mẹo Bắt đầu | 
| 3 | Sau 7 ngày | Khuyến mãi Giảm giá Đơn hàng Đầu tiên | 

Các email chính là các chiến dịch thông thường bạn thiết kế trong cùng một trình xây dựng trực quan mà bạn sẽ dùng cho một cuộc phát sóng — tiêu đề email, khối nội dung, mọi thứ. Không cần phải lên lịch hoặc gửi email của riêng bạn; để nguyên ở trạng thái **Bản nháp** và chỉ chọn từ danh sách thả xuống trong bước đó trong trình xây dựng. Hành trình sẽ gửi email đó cho bạn, một lần cho mỗi người đăng ký đạt đến bước đó.

Xem [Journey Builder](/help/journey-builder) để hướng dẫn đầy đủ về cách thiết kế các bước trên bảng vẽ, nhánh một hành trình với điều kiện **Có/Không**, và bắt đầu từ một mẫu có sẵn thay vì bảng vẽ trống.

## Thử nghiệm A/B cho một bước

Bước **Gửi email** nào cũng có thể được chuyển thành thử nghiệm A/B, để hành trình tự động phát hiện — và sau đó tiếp tục sử dụng — email có hiệu suất tốt nhất. Vì hành trình chạy liên tục (người đăng ký đến theo thời gian), Spwig không kiểm tra một nhóm cố định và dừng lại; thay vào đó nó **chia đều người tham gia vào các biến thể khi họ chảy vào, quan sát hiệu suất của mỗi biến thể, và một khi một biến thể rõ ràng là người chiến thắng thống kê, nó sẽ khóa biến thể đó cho mọi người tham gia sau.** Người đăng ký đã ở giữa chừng sẽ giữ phiên bản mà họ đã được gửi lần đầu.

Mở một bước **Gửi email** trong [Journey Builder](/help/journey-builder) và đặt **Loại bước**:

- **Một email duy nhất** — hành vi thông thường: tất cả mọi người nhận được một email duy nhất mà bạn đã chọn.
- **A/B: các email khác nhau** — chọn **hai đến bốn** email (thiết kế, ưu đãi hoặc bố cục khác nhau); mỗi người đăng ký nhận được một email.
- **A/B: các tiêu đề khác nhau** — chọn một email và nhập **hai đến bốn** tiêu đề; mỗi người đăng ký nhận được email đó với một tiêu đề khác nhau.

Sau đó, chọn **Chọn người chiến thắng bằng** — **Tỷ lệ mở** (thường tốt nhất cho một bài kiểm tra tiêu đề) hoặc **Tỷ lệ nhấp** — và bạn đã hoàn tất. Đặt hành trình ở trạng thái **Hoạt động** và các người đăng ký bắt đầu được phân bổ giữa các biến thể.

Bảng điều khiển của bước này hiển thị một **bảng điểm trực tiếp** khi dữ liệu được ghi nhận — số người nhận, tỷ lệ mở và tỷ lệ nhấp của mỗi biến thể, cùng với mức độ tin cậy của Spwig đối với người dẫn đầu ("Dẫn đầu với độ tin cậy 92%"). Người chiến thắng chỉ được khóa khi Spwig có độ tin cậy ít nhất **95%** *và* có đủ dữ liệu để tin tưởng, vì vậy một hành trình có lưu lượng thấp sẽ không vội vàng đưa ra kết luận. Một khi đã được khóa, bước này hiển thị **"Người chiến thắng đã khóa: Biến thể B"** và mọi người đăng ký mới sẽ nhận được biến thể đó; trên canvas, thẻ hiển thị **"A/B · N email"** trong khi đang kiểm tra, sau đó hiển thị **"A/B người chiến thắng: B"** khi đã quyết định.

Một số điều cần biết:

- **Cung cấp lưu lượng.** Độ tin cậy phụ thuộc vào khối lượng — một bước mà chỉ một số ít người tiếp cận có thể ở trạng thái "Chưa đủ dữ liệu" trong một thời gian. Kiểm tra A/B phát huy hiệu quả trên các hành trình có đăng ký ổn định.
- **Sửa đổi các biến thể hoặc chỉ số người chiến thắng sẽ bắt đầu một bài kiểm tra mới** — người chiến thắng đã được khóa trước đó sẽ bị xóa để bộ cài đặt mới có thể đạt được kết quả riêng của nó.
- Một bước A/B có ít hơn hai biến thể **sẽ chặn hành trình chuyển sang trạng thái Hoạt động** cho đến khi bạn hoàn thành nó (hoặc chuyển đổi nó trở lại một email duy nhất).

Xem [Kiểm tra A/B](ab-testing) để biết thêm về cách Spwig đọc độ tin cậy và mức ý nghĩa.

## Cách đăng ký hoạt động

Khi sự kiện kích hoạt xảy ra cho một khách hàng, Spwig kiểm tra mọi hành trình hoạt động đang lắng nghe sự kiện đó và, đối với mỗi hành trình mà khách hàng đủ điều kiện, **đăng ký** họ tại điểm bắt đầu của luồng. Từ đó, Spwig di chuyển người đăng ký tiến lên qua những gì bạn đã thiết kế trên canvas — chờ đợi mỗi bước **Chờ**, gửi email của mỗi bước **Gửi email**, và đi theo đường **Có**/**Không** đúng tại bất kỳ **Nhánh** nào — cho đến khi họ đạt đến một bước **Thoát**, tại thời điểm đó hành trình được đánh dấu là **Hoàn thành** cho người đăng ký đó.

**Sự đồng ý luôn được tôn trọng.** Một người đăng ký chưa đăng ký nhận email tiếp thị, hoặc đã hủy đăng ký kể từ đó, sẽ đơn giản bị bỏ qua — hành trình không dừng lại cho các người đăng ký khác, và việc hủy đăng ký giữa hành trình sẽ tự động dừng các email còn lại của người đăng ký đó. Bạn không bao giờ cần phải lọc các hành trình của mình theo trạng thái đồng ý một cách thủ công.

## Ngăn ngừa đăng ký quá mức

Hai cài đặt trên hành trình kiểm soát tần suất một người đăng ký có thể đi qua nó:

| Cài đặt | Nó làm gì | Sử dụng điển hình |
|---------|--------------|-------------|
| **Một lần mỗi người đăng ký** *(bật theo mặc định)* | Mỗi người đăng ký được đăng ký tối đa một lần, mãi mãi, bất kể sự kiện kích hoạt xảy ra lại bao nhiêu lần cho họ. | Một chuỗi chào mừng — một khách hàng chỉ nên nhận được nó một lần. |
| **Thời gian làm mát đăng ký lại (ngày)** | Khi **Một lần mỗi người đăng ký** bị tắt, thiết lập số ngày tối thiểu phải trôi qua kể từ lần đăng ký cuối cùng của người đăng ký trước khi họ có thể được đăng ký lại. Đặt thành `0` để không có thời gian làm mát. | Một chuỗi được kích hoạt bởi đơn hàng nên chạy lại cho một đơn hàng mới, nhưng không kích hoạt lại cho mọi đơn hàng được đặt trong cùng một tuần. |

Tắt **Một lần mỗi người đăng ký** cho một hành trình mà bạn muốn chạy theo từng đơn hàng (như lời cảm ơn sau mua hàng), và kết hợp nó với một thời gian làm mát để một khách hàng đặt hàng hai lần trong cùng một ngày chỉ được đăng ký một lần. Một người đăng ký đang tích cực thực hiện một hành trình sẽ không bao giờ được đăng ký vào một lần chạy thứ hai, chồng chéo của cùng một hành trình đó bất kể các cài đặt này.

## Giám sát các hành trình


Danh sách **Campaign Studio > Journeys** hiển thị **Trigger**, **Status**, số lượng **Emails** được gửi, và tổng số **Enrolled** / **Completed** đang chạy, giúp bạn nhìn nhanh xem hành trình có thực sự tiếp cận được khách hàng hay không.

![Danh sách Journeys hiển thị hai hành trình đang hoạt động với số lượng đăng ký và hoàn thành](/static/core/admin/img/help/triggered-journeys/journey-list.webp)

Để xem từng người đăng ký thay vì tổng số, hãy mở danh sách **Journey Enrollments** tại `/admin/email_marketing/journeyenrollment/`. Mỗi dòng hiển thị tiến trình của một người đăng ký trong một hành trình: **Journey** họ đang tham gia, **Current step** (bước hiện tại), **Status** (Active, Completed, hoặc Cancelled), và thời điểm **Next step** (bước tiếp theo) đến hạn. Sử dụng bộ lọc để thu hẹp phạm vi xuống một hành trình hoặc một trạng thái — ví dụ, lọc theo **Active** sẽ hiển thị tất cả những người đang ở giữa chuỗi.

![Danh sách Journey Enrollments hiển thị tiến trình của người đăng ký qua hai hành trình](/static/core/admin/img/help/triggered-journeys/journey-enrollments.webp)

## Báo cáo hành trình

Mỗi hành trình có trang **Report** riêng, được mở bằng cách nhấp vào nút **Report** trên thẻ hành trình trong **Campaign Studio > Journeys**, hoặc trên trang cài đặt của chính hành trình đó. Đây là bản tóm tắt một trang về mức độ tiến triển của người đăng ký trong chuỗi và, nếu email của bạn chứa các liên kết được theo dõi, doanh thu mà hành trình đã tạo ra.

![Trang báo cáo Journey hiển thị phễu đăng ký, thẻ doanh thu được quy kết và bảng doanh thu theo bước](/static/core/admin/img/help/triggered-journeys/journey-report.webp)

### Phễu đăng ký

Bốn thẻ hiển thị vị trí hiện tại của người đăng ký:

| Thẻ | Nội dung hiển thị |
|------|---------------|
| **Enrolled** | Tổng số người đăng ký đã từng tham gia hành trình này. |
| **Active now** | Người đăng ký đang ở giữa chuỗi, đang chờ hoặc thực hiện bước tiếp theo. |
| **Completed** | Người đăng ký đã đạt đến bước **Exit** của hành trình. |
| **Exited** | Người đăng ký bị loại khỏi hành trình trước khi hoàn thành — ví dụ, một người mua hàng đã hoàn tất thanh toán giữa chừng trong chuỗi bỏ giỏ hàng, hoặc một người đăng ký đã hủy đăng ký. |

Nếu hành trình chưa có đăng ký nào, cả bốn thẻ đều hiển thị số 0 và một ghi chú nhắc bạn rằng các chỉ số sẽ xuất hiện khi khách hàng bắt đầu tham gia hành trình.

### Doanh thu được quy kết

Thẻ **Attributed revenue** hoạt động giống như [báo cáo chiến dịch](campaign-reports) — Spwig truy vết đơn hàng ngược lại các lần nhấp vào liên kết trong email của hành trình, cùng với quy kết dựa trên nhấp chuột và đồng ý được mô tả trong [Attributed revenue](campaign-reports#attributed-revenue) trên trang đó. Các lưu ý tương tự cũng áp dụng ở đây: quy kết chỉ dựa trên nhấp chuột (chỉ mở email không bao giờ quy kết doanh thu), nó tuân theo mô hình quy kết và cửa sổ nhìn lại đang hoạt động của cửa hàng bạn, nó tôn trọng sự đồng ý phân tích, và nó không có hiệu lực hồi tố — một hành trình chỉ hiển thị doanh thu từ các email được gửi sau khi theo dõi quy kết được bật cho cửa hàng của bạn.

Dòng phụ của thẻ phân tách tổng số thành:

- **Orders** — số lượng đơn hàng được ghi nhận cho hành trình này, gộp từ email của tất cả các bước.
- **AOV** — giá trị đơn hàng trung bình của những đơn hàng đó.
- **Revenue per enrollee** — doanh thu được quy kết chia cho tổng số **Enrolled**. Một hành trình không có một khoản "chi tiêu" duy nhất như một chiến dịch — nó chạy liên tục thay vì tốn một lần chi phí — vì vậy không có chỉ số ROAS ở đây. **Revenue per enrollee** là tương đương gần nhất: một thước đo ổn định, có thể so sánh về hiệu quả chuyển đổi đăng ký thành đơn hàng của hành trình, mà bạn có thể theo dõi theo thời gian hoặc so sánh với một hành trình khác.

### Doanh thu theo bước

Khi hành trình có ít nhất một bước **Send email**, bảng **Revenue by step** sẽ phân tách tổng số chi tiết hơn, mỗi dòng cho một bước, để bạn có thể thấy email nào trong chuỗi thực sự tạo ra doanh thu:

| Cột | Nội dung hiển thị |
|--------|---------------|
| **Bước** | Email của bước đó, kèm nhãn **A/B** nếu bước này đang chạy [thử nghiệm A/B](ab-testing). |
| **Doanh thu** | Doanh thu được ghi nhận từ các đơn hàng được truy vết ngược lại email của bước đó. |
| **Đơn hàng** | Số lượng đơn hàng tạo ra mức doanh thu đó. |
| **Đã gửi** | Số lần email của bước này đã được gửi đi. |
| **Mở** / **Nhấp** | Số lượng email đã được mở và số lượng đã được nhấp. Spwig theo dõi lượt mở và nhấp cho mọi lần gửi của từng bước, bao gồm cả email thông thường và A/B. |

Sử dụng bảng này để phát hiện điểm yếu trong một hành trình tổng thể đang hoạt động tốt — ví dụ, một chuỗi email chào mừng mà email đầu tiên tạo ra phần lớn doanh thu trong khi một bước sau đó đóng góp rất ít có thể là ứng viên cho một ưu đãi mạnh hơn hoặc một bản viết lại, thay vì giả định rằng toàn bộ chuỗi cần được xem xét lại.

## Mẹo

- Cách nhanh nhất để bắt đầu một hành trình bỏ giỏ hàng, thu hút khách hàng cũ, đánh giá sau giao hàng hoặc thông báo có hàng trở lại là sử dụng mẫu khởi động — khi bạn lưu một hành trình mới với một trong những kích hoạt này, trình chọn **Mẫu** trong [Trình tạo hành trình](/help/journey-builder) sẽ cung cấp một luồng có sẵn (**Phục hồi giỏ hàng bị bỏ**, **Thu hút khách hàng đã ngừng mua**, **Yêu cầu đánh giá sau giao hàng**, hoặc **Thông báo có hàng trở lại**) để bạn điều chỉnh thay vì xây dựng từ đầu.
- Bắt đầu mọi hành trình ở trạng thái **Nháp** trong khi bạn xây dựng các bước, sau đó chuyển **Trạng thái** sang **Hoạt động** khi bạn đã kiểm tra email và thời gian chờ — không có người đăng ký nào được ghi danh cho đến khi hành trình ở trạng thái Hoạt động.
- Giữ bật **Mỗi người đăng ký một lần** cho bất kỳ điều gì liên quan đến một cột mốc một lần (đăng ký, đơn hàng đầu tiên); tắt nó đi với thời gian làm mát hợp lý cho bất kỳ điều gì nên lặp lại, như một chuỗi email sau mua hàng.
- Sử dụng **Chỉ cho phân khúc** để chạy một chuỗi email chào mừng khác nhau cho một đối tượng cụ thể — ví dụ, một phân khúc VIP nhận được một chuỗi phong phú hơn so với mọi người khác.
- Đặt thời gian chờ của bước đầu tiên thành `0` nếu bạn muốn email đầu tiên được gửi ngay lập tức sau khi kích hoạt được thực hiện, thay vì chờ đợi.
- Kiểm tra danh sách **Ghi danh hành trình** sau khi kích hoạt một hành trình mới để xác nhận rằng người đăng ký thực sự đang được ghi danh và tiến qua các bước của họ như mong đợi.
- Tạm dừng một hành trình (**Trạng thái: Tạm dừng**) sẽ ngăn các lượt ghi danh mới nhưng không hủy bỏ những người đăng ký đã ở giữa hành trình — họ vẫn tiếp tục nhận các bước còn lại.