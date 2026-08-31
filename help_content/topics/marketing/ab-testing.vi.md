---
title: Kiểm tra A/B
---

Tính năng **kiểm tra A/B** của Studio Chiến dịch cho phép bạn thử nghiệm 2 đến 4 **phiên bản** — các phiên bản khác nhau của cùng một chiến dịch — trên một phần của đối tượng người dùng của bạn trước khi gửi đầy đủ. Chỉ thay đổi tiêu đề email, hoặc tạo nội dung hoàn toàn khác nhau cho mỗi phiên bản. Spwig chia đều một mẫu danh sách của bạn cho các phiên bản, theo dõi cách mỗi phiên bản hoạt động và tự động gửi phiên bản hiệu quả nhất đến những người dùng không xem thử nghiệm.

## Thiết lập một thử nghiệm

Xây dựng chiến dịch của bạn như bình thường trong trình xây dựng trực quan của Studio Chiến dịch trước — viết tiêu đề, thiết kế nội dung của bạn và chọn **Phân khúc** mà bạn muốn tiếp cận. Chiến dịch này trở thành **khối chứa** của thử nghiệm. Khi bạn gắn thử nghiệm A/B với nó, khối chứa sẽ không bao giờ được gửi trực tiếp — nhiệm vụ của nó là lưu trữ cài đặt, và đối tượng mà nó được thiết lập để tiếp cận chính xác là nhóm đối tượng mà thử nghiệm chạy trên đó.

Hai vị trí mở trình hướng dẫn kiểm tra A/B:

- Nút **Kiểm tra A/B** trong thanh công cụ của trình xây dựng trực quan.
- Biểu tượng **Kiểm tra A/B** trên thẻ chiến dịch trong **Studio Chiến dịch > Chiến dịch**.

Một khi một thử nghiệm tồn tại trên chiến dịch, nút đó sẽ đưa bạn trực tiếp đến kết quả của nó thay vì trình hướng dẫn, và thẻ chiến dịch sẽ có một nhãn nhỏ **A/B** để bạn có thể nhận ra nó trong danh sách một cách nhanh chóng.

## Điều gì cần kiểm tra

Bước đầu tiên của trình hướng dẫn hỏi điều gì sẽ khác nhau giữa các phiên bản:

| Tùy chọn | Điều gì thay đổi | Được đo lường bởi |
|--------|--------------|-------------|
| **Tiêu đề email** | Mỗi phiên bản gửi cùng nội dung — chỉ có tiêu đề email khác nhau. Thử nghiệm phổ biến nhất. | Tỷ lệ mở email |
| **Nội dung** | Mỗi phiên bản là một thiết kế riêng biệt mà bạn tự xây dựng trong trình xây dựng trực quan. | Tỷ lệ nhấp chuột |

![Bước "Bạn muốn kiểm tra điều gì?", với tiêu đề email được chọn](/static/core/admin/img/help/ab-testing/ab-test-what-to-test.webp)

## Chọn các phiên bản của bạn

Những gì bạn nhập tiếp theo phụ thuộc vào điều bạn đã chọn:

- **Tiêu đề email** — nhập tiêu đề cho mỗi phiên bản (2–4). Hai hàng được hiển thị ban đầu; nhấn **Thêm tiêu đề khác** để có phiên bản thứ ba hoặc thứ tư.
- **Nội dung** — chỉ cần chọn số phiên bản bạn muốn (2–4). Mỗi phiên bản ban đầu là bản sao chính xác của thiết kế hiện tại của khối chứa, vì vậy bạn chỉ cần thay đổi những gì bạn đang kiểm tra.

Bất kể cách nào, Spwig đánh dấu các phiên bản là **A**, **B**, **C** và **D** theo thứ tự bạn nhập — bạn sẽ thấy chúng là "Phiên bản A", "Phiên bản B", v.v. từ đây.

![Bước Các phiên bản với ba tiêu đề được nhập cho các phiên bản A, B và C](/static/core/admin/img/help/ab-testing/ab-test-variants.webp)

Đối với thử nghiệm nội dung, bạn không thiết kế các phiên bản trong chính trình hướng dẫn — sau khi bạn tạo thử nghiệm, mỗi thẻ phiên bản trên trung tâm kết quả sẽ có một biểu tượng bút chì nhỏ mở nó trong cùng trình xây dựng trực quan mà bạn đã sử dụng cho khối chứa. Điều này chỉ khả dụng khi thử nghiệm vẫn ở trạng thái **Draft**; một khi bạn bắt đầu thử nghiệm, các thiết kế sẽ bị khóa lại để nội dung bạn đang đo lường không thay đổi trong quá trình thử nghiệm.

## Cài đặt thử nghiệm

Bước cuối cùng của trình hướng dẫn nói về cách thử nghiệm được thực hiện và quyết định:

| Cài đặt | Mô tả |
|---------|--------------|
| **Mẫu thử nghiệm** | Phần trăm đối tượng người dùng được sử dụng cho thử nghiệm, chia đều cho các phiên bản: 20%, 30%, 50%, hoặc 100%. Phần còn lại — **nhóm giữ lại** — nhận được người chiến thắng sau đó. Việc chọn 100% kiểm tra toàn bộ danh sách của bạn cùng một lúc, do đó không còn nhóm giữ lại nào để gửi người chiến thắng. |
| **Người chiến thắng được quyết định bởi** | **Tỷ lệ mở email** hoặc **Tỷ lệ nhấp chuột**. Mặc định là tỷ lệ mở email cho thử nghiệm tiêu đề email và tỷ lệ nhấp chuột cho thử nghiệm nội dung, vì đó là điều mỗi thử nghiệm thực sự đo lường — nhưng bạn có thể thay đổi bất kỳ cách nào. |
| **Khoảng thời gian thử nghiệm (giờ)** | Thời gian để thu thập các lần mở email và nhấp chuột trước khi chọn người chiến thắng, từ 1 đến 168 giờ (một tuần đầy). |
| **Tự động gửi người chiến thắng đến phần còn lại của đối tượng** | Được bật theo mặc định. Khi được chọn, Spwig gửi email phiên bản chiến thắng đến nhóm giữ lại ngay khi khoảng thời gian kết thúc, không cần hành động nào từ bạn. |

Một thẻ xem xét ngắn ở cuối tổng hợp các lựa chọn của bạn trước khi bạn xác nhận.

[![]( /static/core/admin/img/help/ab-testing/ab-test-settings.webp )]

## Bắt đầu thử nghiệm

Nhấp vào **Tạo thử nghiệm** để lưu thiết lập — điều này không gửi bất kỳ thứ gì cả. Bạn sẽ đến trang tổng quan kết quả của thử nghiệm ở trạng thái **Soạn thảo**, hiển thị mỗi biến thể với số người nhận bằng 0 cho đến nay và hai nút: **Bắt đầu thử nghiệm** và **Hủy bỏ thử nghiệm**.

[![]( /static/core/admin/img/help/ab-testing/ab-test-draft.webp )]

Nhấp vào **Bắt đầu thử nghiệm** khi bạn sẵn sàng. Spwig chia đều mẫu thử nghiệm cho các biến thể và gửi email ngay lập tức — bạn không cần phải làm gì thêm; một công việc nền sẽ kiểm tra một lần khi khoảng thời gian thử nghiệm đã qua và quyết định người chiến thắng tự động. Trạng thái của chiến dịch chính sẽ vẫn ở trạng thái **Soạn thảo** trong suốt quá trình này — đây là điều kỳ vọng, vì các biến thể (và sau này là người chiến thắng) mới thực sự được gửi đi, chứ không phải container.

Đội ngũ người dùng của bạn cần phải đủ lớn để mỗi biến thể nhận được số lượng người nhận xứng đáng. Spwig chặn việc bắt đầu một thử nghiệm nếu bất kỳ biến thể nào cũng có thể kết thúc với 0 người, nhưng một thử nghiệm thực sự đáng đọc cần nhiều hơn mức tối thiểu — hãy hướng đến vài trăm người nhận hoặc nhiều hơn trước khi dựa vào kết quả.

## Trong khi thử nghiệm đang chạy

Sau khi bắt đầu, bảng điều khiển chuyển sang trạng thái **Đang chạy** và hiển thị "Thử nghiệm đang chạy — người chiến thắng sẽ được quyết định tự động vào" ngày và giờ khoảng thời gian kết thúc. Số lượng người nhận và tỷ lệ mở/xem, tỷ lệ nhấp chuột được cập nhật mỗi lần truy cập, cùng với biểu đồ thanh so sánh tỷ lệ mở và tỷ lệ nhấp chuột của mỗi biến thể — không chỉ là chỉ số bạn đã chọn để quyết định người chiến thắng.

[![]( /static/core/admin/img/help/ab-testing/ab-test-running.webp )]

Bạn cũng có thể theo dõi mọi thử nghiệm từ **bảng điều khiển Studio Chiến dịch**: phần *Thử nghiệm A/B gần đây* liệt kê các thử nghiệm đang chạy và đã được quyết định gần đây — mỗi thử nghiệm đều hiển thị mức độ tin cậy ngay lập tức — và liên kết trực tiếp đến kết quả, cùng với các thẻ đếm số lượng thử nghiệm đang chạy và số lượng đã được quyết định trong 30 ngày qua.

## Đọc kết quả

Khi khoảng thời gian thử nghiệm kết thúc, Spwig chọn biến thể có tỷ lệ cao nhất trên chỉ số bạn đã chọn, đánh dấu thử nghiệm ở trạng thái **Hoàn tất**, và — nếu **Gửi tự động người chiến thắng** được chọn và có một nhóm người không tham gia để gửi — gửi biến thể đó đến tất cả những người không tham gia thử nghiệm. Thẻ của biến thể chiến thắng được viền và mang theo nhãn **Người chiến thắng**; biểu đồ so sánh vẫn giữ nguyên để bạn có thể xem cách các biến thể so sánh với nhau.

[![]( /static/core/admin/img/help/ab-testing/ab-test-complete.webp )]

Hãy lưu ý rằng các con số trên trang này luôn dành cho mẫu thử nghiệm, chứ không phải toàn bộ danh sách của bạn — với mẫu 20%, bạn đang đọc cách một phần năm trong số người dùng của bạn phản hồi, chứ không phải tất cả.

## Kết quả có độ tin cậy cao đến mức nào?

Tỷ lệ mở hoặc nhấp chuột cao hơn không luôn có nghĩa là biến thể đó thực sự tốt hơn — với đội ngũ người dùng nhỏ, một biến thể có thể vượt trội chỉ do may mắn. Vì vậy, bên cạnh người chiến thắng, Spwig hiển thị **mức độ tin cậy mà nó có được rằng kết quả là chính xác**, dựa trên kích thước của khoảng cách và số lượng người nhận. Bạn sẽ thấy một trong ba kết quả:

- **Kết quả rõ ràng** — Spwig tin cậy ít nhất 95% rằng biến thể dẫn đầu thực sự vượt trội hơn các biến thể khác. Đây là kết quả bạn có thể hành động.
- **Quá gần để đưa ra kết luận** — vẫn có người dẫn đầu, nhưng khoảng cách nhỏ đến mức có thể do may rủi. Con số được hiển thị là mức độ tin cậy mà Spwig có được, dưới mức 95%. Hãy cân nhắc chạy lại với đội ngũ người dùng lớn hơn hoặc khoảng thời gian thử nghiệm dài hơn trước khi đưa ra kết luận.
- **Chưa đủ dữ liệu** — số người nhận quá ít (hoặc số lần mở và nhấp chuột quá ít) để phân biệt các biến thể. Điều này thường xảy ra với danh sách nhỏ; hãy mở rộng đội ngũ người dùng hoặc để thử nghiệm chạy lâu hơn.

![Một bài kiểm tra hoàn tất cho thấy kết quả rõ ràng — biến thể chiến thắng có huy hiệu độ tin cậy và phần tóm tắt ghi "rõ ràng về mặt thống kê"](/static/core/admin/img/help/ab-testing/ab-test-confidence.webp)

Cùng một cách đọc này xuất hiện trong khi bài kiểm tra vẫn đang chạy, vì vậy bạn có thể theo dõi kết quả trở nên chắc chắn — hoặc không — trước khi cửa sổ thời gian đóng lại. Vì độ tin cậy phụ thuộc rất nhiều vào kích thước đối tượng, đây là lý do thực tế để nhắm tới vài trăm hoặc nhiều hơn người nhận cho mỗi bài kiểm tra: trên một danh sách rất nhỏ, ngay cả một sự khác biệt trông có vẻ lớn thường vẫn sẽ được đọc là "quá sát để phân định".

Lưu ý rằng khi tự động gửi được bật, Spwig vẫn gửi biến thể có tỷ lệ cao nhất cho phần còn lại của đối tượng của bạn ngay cả khi kết quả không rõ ràng — cách đọc độ tin cậy ở đó để cho bạn biết mức độ tin tưởng vào kết quả, chứ không phải để trì hoãn việc gửi.

## Hủy bỏ một bài kiểm tra

**Hủy bài kiểm tra** có sẵn trong khi một bài kiểm tra ở trạng thái **Nháp** hoặc **Đang kiểm tra**, và dừng nó mà không bao giờ gửi người chiến thắng. Tính năng này dành cho khi bạn đã đổi ý hoặc mắc lỗi trong thiết lập — không phải thứ nên dùng một cách nhẹ nhàng, vì một khi bài kiểm tra bị hủy (hoặc đã hoàn thành bình thường), không có nút nào để thiết lập một bài kiểm tra mới trên chiến dịch đó. Nếu bạn muốn chạy một cuộc so sánh khác sau đó, hãy xây dựng một chiến dịch mới cho nó.

## Mẹo

- Hãy thử một bài kiểm tra **Tiêu đề** trước — nó đơn giản nhất để thiết lập và là lý do phổ biến nhất để A/B test.
- Sử dụng bài kiểm tra **Nội dung** khi bạn muốn so sánh các thiết kế hoặc ưu đãi thực sự khác nhau, chứ không chỉ là cách diễn đạt trong tiêu đề.
- Hoàn thành thiết kế mọi biến thể của một bài kiểm tra nội dung — sử dụng biểu tượng bút chì trên mỗi thẻ — trước khi nhấp vào **Bắt đầu kiểm tra**. Bạn không thể chỉnh sửa thiết kế của một biến thể một khi bài kiểm tra đang chạy.
- Để **Mẫu kiểm tra** dưới 100% nếu bạn muốn Spwig tự động gửi email người chiến thắng cho phần còn lại của danh sách của bạn sau đó — ở 100% sẽ không còn phần giữ lại nào để nó tiếp cận.

- Cho cửa sổ kiểm tra đủ thời gian để bao phủ thói quen đọc bình thường của người đăng ký của bạn (24 giờ thoải mái bao phủ một ngày đầy đủ của các múi giờ và hộp thư) thay vì quyết định người chiến thắng chỉ dựa trên một hoặc hai giờ đầu tiên.