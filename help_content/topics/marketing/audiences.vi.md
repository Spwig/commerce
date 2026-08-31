---
title: Đối tượng
---

Một **Đối tượng** là một danh sách đối tượng đã lưu mà bạn có thể chỉ định cho một chiến dịch, một hành trình, hoặc một bài kiểm tra A/B — danh sách Đối tượng riêng của Công cụ Chiến dịch gọi chúng là 'Đối tượng được nhắm mục tiêu', và hướng dẫn này sử dụng cả hai từ cho cùng một thứ việc. Mỗi đối tượng có thể là **động**, được xác định bởi các quy tắc mà Spwig đánh giá lại mỗi lần nó được sử dụng, hoặc **tĩnh**, một danh sách cụ thể các người đăng ký bạn chọn thủ công.

Hướng dẫn này nói về cách xây dựng các quy tắc của đối tượng động — bao gồm các trường mới hơn nhằm nhắm mục tiêu các bucket giá trị khách hàng của chính cửa hàng bạn, chương trình trung thành, và các đối tác liên kết — và nút **Thêm đối tượng ban đầu** một cách nhanh chóng giúp tạo ra một tập hợp các đối tượng có sẵn từ dữ liệu mà cửa hàng bạn đã có.

## Đối tượng động và đối tượng tĩnh

| Loại | Cách hoạt động | Dành cho | 
|---|---|---| 
| **Đối tượng động (quy tắc)** | Bạn xác định các điều kiện — ví dụ: "Tổng số tiền đã chi ít nhất là $500." Spwig tính toán lại ai phù hợp mỗi khi đối tượng được sử dụng, do đó thành viên thay đổi tự động khi người đăng ký của bạn thay đổi. | Các đối tượng liên tục nên luôn cập nhật, ví dụ: "Khách hàng VIP" hoặc "Chưa mua hàng trong 90 ngày." | 
| **Đối tượng tĩnh (danh sách cố định)** | Một danh sách cụ thể các người đăng ký bạn thêm hoặc xóa thủ công. Thành viên sẽ không bao giờ thay đổi trừ khi bạn thay đổi chúng. | Một danh sách duy nhất — tất cả mọi người từ một sự kiện cụ thể, hoặc một nhóm được chọn thủ công cho một lần gửi duy nhất. | 

Chọn loại với trường **Loại** khi bạn tạo một đối tượng. Phần còn lại của hướng dẫn này nói về các đối tượng động — các đối tượng tĩnh chỉ đơn giản là một danh sách thành viên mà không có quy tắc nào để cấu hình.

## Xây dựng một đối tượng động

Mở **Công cụ Chiến dịch > Đối tượng**, sau đó nhấp vào **+ Tạo Đối tượng Mới** (hoặc mở một đối tượng động hiện có) để truy cập **Trình xây dựng Quy tắc Đối tượng**. Nhấp vào **+ Thêm điều kiện** để thêm một quy tắc, chọn điều bạn muốn kiểm tra và cách, và thiết lập xem người đăng ký phải đáp ứng **tất cả** hay **một số** trong các điều kiện của bạn. Một con số trực tiếp ở góc trên bên phải — ví dụ: "8 người đăng ký phù hợp" — sẽ được cập nhật ngay sau mỗi lần thay đổi, vì vậy bạn có thể xem chính xác ai đủ điều kiện trước khi lưu.

![Trình xây dựng Quy tắc Đối tượng với các điều kiện Khách hàng, Cấp độ Trung thành, Giá trị Trọn đời, và Đối tác được đặt, cùng với số lượng người đăng ký phù hợp trực tiếp](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

Một điều kiện với kiểm tra **is true**-style cố định — **Đã mua hàng**, **Đã đồng ý với quảng cáo**, **Thành viên Trung thành**, **Đối tác** — chỉ cần chọn chính trường đó; không có toán tử hay giá trị nào để thiết lập.

## Những gì bạn có thể nhắm mục tiêu

| Trường | Nó kiểm tra | 
|---|---| 
| **Tổng số tiền đã chi** | Tổng đơn hàng theo thời gian. | 
| **Số lượng đơn hàng** | Số lượng đơn hàng đã hoàn tất. | 
| **Giá trị trọn đời** | Giá trị trọn đời được tính toán của khách hàng. | 
| **Giá trị đơn hàng trung bình** | Số tiền trung bình cho mỗi đơn hàng đã hoàn tất. | 
| **Ngày kể từ lần mua cuối cùng** | Khoảng thời gian kể từ lần mua gần đây nhất của khách hàng — nhắm mục tiêu 90+ ngày để tạo đối tượng khách hàng quay lại. | 
| **Đã mua hàng** | Xem khách hàng có ít nhất một đơn hàng hoàn tất hay không. | 
| **Đã đồng ý với quảng cáo** | Xem người đăng ký có đồng ý với email quảng cáo hay không. | 
| **Ngôn ngữ** | Ngôn ngữ được lưu trữ của người đăng ký. | 
| **Nguồn** | Cách người đăng ký tham gia — Đăng ký Cửa hàng, Nhập, Đơn hàng, Được thêm thủ công, hoặc API. | 
| **Tham gia sau** | Người đăng ký đã tham gia vào hoặc sau ngày được chọn. | 
| **Có thẻ** | Xem người đăng ký có mang theo [thẻ](/help/subscriber-tags) bạn đã tạo hay không. | 
| **Nhóm khách hàng** | Xem khách hàng có thuộc một trong những nhóm khách hàng được đặt tên riêng của cửa hàng bạn — Khách hàng Vắng mặt, Khách hàng Mới, Khách hàng Thường xuyên, Người mua Nhiều, Khách hàng Có Giá trị Cao, Khách hàng VIP, Người tìm kiếm Giá rẻ, Khách hàng Nguy cơ, hoặc Khách hàng Không hoạt động hay không. | 
| **Thành viên Trung thành** | Xem khách hàng có phải là thành viên hoạt động của chương trình trung thành của bạn hay không. | 
| **Điểm Trung thành** | Số điểm hiện có của thành viên. | 
| **Cấp độ Trung thành** | Cấp độ trung thành mà thành viên hiện đang giữ. | 
| **Đối tác** | Xem khách hàng có phải là đối tác liên kết hoạt động của bạn hay không. |

**Customer segment**, hai trường **Loyalty** (Lợi ích), **Loyalty tier** (Cấp độ Lợi ích), và **Affiliate** (Đối tác) là những tính năng mới, và mỗi tính năng chỉ xuất hiện trong trình chọn điều kiện khi cửa hàng của bạn thực sự có loại dữ liệu đó: các trường Lợi ích xuất hiện khi chương trình Lợi ích của bạn có thành viên và ít nhất một cấp độ đang hoạt động, **Affiliate** xuất hiện khi bạn có ít nhất một đối tác, và **Customer segment** xuất hiện khi bạn có ít nhất một đoạn khách hàng đang hoạt động được cấu hình sẵn.

Bạn sẽ không thấy một tùy chọn nào trên cửa hàng mới toanh mà không thể phù hợp với bất kỳ ai.

Một hạn chế hiện tại đáng chú ý: đối với bất kỳ điều kiện nào có danh sách thả xuống các lựa chọn — **Language** (Ngôn ngữ), **Source** (Nguồn), **Has tag** (Có thẻ), **Customer segment** (Đoạn khách hàng), **Loyalty tier** (Cấp độ Lợi ích) — toán tử **is any of** (là một trong các) vẫn chỉ cho phép bạn chọn một giá trị tại một thời điểm. Nếu bạn muốn khớp nhiều (ví dụ, khách hàng thuộc đoạn VIP hoặc Giá trị Cao), hãy thêm một điều kiện cho mỗi giá trị và đặt **Match** (Match) thành **any** (một trong các).

## Thêm các đoạn khách hàng ban đầu

Việc tạo một quy tắc từ đầu cho mỗi đoạn khách hàng rõ ràng — những khách hàng VIP của bạn, những thành viên chương trình Lợi ích, mọi người đã im lặng — là điều mất thời gian khi Spwig đã có thể nhìn thấy ai đủ điều kiện. Trên danh sách Các đoạn khách hàng, hãy nhấn **Add starter audiences** (Thêm các đoạn khách hàng ban đầu) và Spwig tạo ra một tập hợp các đoạn khách hàng có sẵn, có thể chỉnh sửa từ dữ liệu khách hàng, chương trình Lợi ích và đối tác mà cửa hàng bạn đã có.

![Danh sách Các đoạn khách hàng với các nút Thêm đoạn khách hàng mới và Thêm các đoạn khách hàng ban đầu](/static/core/admin/img/help/audiences/segments-changelist.webp)

| Starter | Đối tượng | Cần | 
|---|---|---| 
| **Khách hàng VIP** | Đoạn khách hàng VIP của bạn | Một đoạn khách hàng VIP đang hoạt động | 
| **Khách hàng có giá trị cao** | Đoạn khách hàng VIP và Giá trị Cao của bạn | Một đoạn khách hàng VIP hoặc Giá trị Cao đang hoạt động | 
| **Khách hàng mua lại** | Đoạn khách hàng Mua lại thường xuyên và Khách hàng Thường xuyên của bạn | Một đoạn khách hàng Mua lại thường xuyên hoặc Khách hàng Thường xuyên đang hoạt động | 
| **Khách hàng mới** | Đoạn khách hàng Mới của bạn | Một đoạn khách hàng Mới đang hoạt động | 
| **Khách hàng ngừng hoạt động** | Những khách hàng đã mua hàng trước đó nhưng không mua trong 90 ngày gần đây | Bất kỳ lịch sử mua hàng nào của khách hàng | 
| **Thành viên chương trình Lợi ích** | Tất cả mọi người đang hoạt động trong chương trình Lợi ích của bạn | Một chương trình Lợi ích đang hoạt động với thành viên | 
| **Cấp độ Lợi ích cao nhất** | Những thành viên ở cấp độ Lợi ích được xếp hạng cao nhất của bạn | Ít nhất một cấp độ Lợi ích đang hoạt động | 
| **Đối tác** | Các đối tác liên kết đang hoạt động của bạn | Ít nhất một đối tác | 

Spwig chỉ tạo các đoạn khách hàng ban đầu mà nó thực sự có dữ liệu — một cửa hàng chưa có chương trình Lợi ích nào sẽ không bao giờ nhận được một đoạn **Loyalty members** (Thành viên Lợi ích), mà thay vào đó là một đoạn trống mà không bao giờ có thể khớp được ai. Spwig xác nhận chính xác những gì nó đã thêm, ví dụ: "Đã thêm 7 đoạn khách hàng ban đầu: Khách hàng có giá trị cao, Khách hàng mua lại, Khách hàng mới, Khách hàng ngừng hoạt động, Thành viên Lợi ích, Cấp độ Lợi ích cao nhất, Đối tác."

![Thông báo thành công xác nhận các đoạn khách hàng ban đầu vừa được thêm](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

An tâm khi nhấn **Add starter audiences** (Thêm các đoạn khách hàng ban đầu) nhiều lần. Spwig không bao giờ tạo ra một đoạn khách hàng ban đầu trùng lặp nếu nó đã tồn tại, vì vậy việc nhấn lại sau khi thiết lập (ví dụ) chương trình Lợi ích của bạn lần đầu chỉ thêm những gì mới có sẵn — nếu mọi thứ đã được thiết lập sẵn, nó sẽ chỉ đơn giản là nói vậy.

![Thông báo thông tin được hiển thị khi mọi đoạn khách hàng ban đầu đều đã tồn tại](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

Nếu bạn xóa một đoạn khách hàng ban đầu không muốn, việc nhấn **Add starter audiences** (Thêm các đoạn khách hàng ban đầu) lần nữa sẽ không làm cho nó xuất hiện lại — Spwig xem đây là một đoạn khách hàng bạn đã xóa cố ý, chứ không phải là đoạn khách hàng cần được tạo lại.

Một khi đã được tạo, một đoạn khách hàng ban đầu sẽ trở thành một đoạn khách hàng động thông thường: mở nó từ danh sách để xem lại hoặc điều chỉnh quy tắc của nó, đổi tên, hoặc xóa nó, giống như bất kỳ đoạn khách hàng nào bạn tự tạo.

## Những đoạn khách hàng này thực sự tiếp cận được ai

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật.

Các điều kiện về khách hàng, khách hàng thân thiết và đối tác liên kết ở trên chỉ khớp với những người đăng ký có email được liên kết với tài khoản khách hàng — một đăng ký bản tin ẩn danh sẽ không khớp với điều kiện **Khách hàng thân thiết** hoặc **VIP**, ngay cả khi điều đó là chính xác, vì Spwig không có lịch sử đơn hàng hay khách hàng thân thiết để đối chiếu.

Nếu nhiều khách hàng của bạn có tài khoản nhưng chưa đăng ký, hãy yêu cầu người quản lý cài đặt Spwig của bạn chạy đồng bộ hóa người đăng ký — thao tác này tạo một bản ghi Người đăng ký cho mọi tài khoản khách hàng hiện có chỉ trong một bước, để các đối tượng này có những người thực sự để khớp.

Dù một phân khúc đếm được bao nhiêu người đăng ký, con số đó mô tả những người *có thể* nhận chiến dịch, chứ không phải những người sẽ nhận. Mọi lần gửi vẫn kiểm tra sự đồng ý tiếp thị của từng người đăng ký trước tiên, vì vậy một phân khúc không bao giờ là cách để bỏ qua điều đó.

## Mẹo

- Bắt đầu từ một đối tượng khởi đầu và điều chỉnh nó thay vì xây dựng cùng một quy tắc thủ công — một khi đã được tạo, một đối tượng khởi đầu không khác gì bất kỳ phân khúc nào bạn tự xây dựng.
- Các điều kiện Boolean như **Khách hàng thân thiết**, **Đối tác liên kết** và **Đã đặt hàng** không cần toán tử hoặc giá trị — chỉ cần thêm điều kiện và bạn đã hoàn tất.
- Kết hợp các trường mới hơn với các trường gốc để nhắm mục tiêu chặt chẽ hơn, ví dụ **Khách hàng thân thiết** cộng với **Đã đồng ý tiếp thị**, thay vì chỉ dựa vào một điều kiện duy nhất.
- Nếu các quy tắc của một phân khúc tham chiếu đến thứ gì đó đã bị xóa — một phân khúc khách hàng đã bị xóa, một thẻ đã bị làm trống, v.v. — Spwig coi nó như không khớp với ai thay vì quay lại danh sách người đăng ký toàn bộ của bạn. Nhắm mục tiêu bị hỏng sẽ gửi ít hơn; nó không bao giờ gửi cho tất cả mọi người một cách vô tình.
- Nếu số lượng thành viên của một phân khúc trông có vẻ cũ, hãy mở nó và lưu lại, hoặc sử dụng hành động hàng loạt **Xây dựng lại số lượng thành viên** từ danh sách Phân khúc, để tính lại ngay lập tức.
- Theo dõi số lượng "người đăng ký khớp" trực tiếp trong khi bạn xây dựng một quy tắc — đó là cách nhanh nhất để phát hiện một điều kiện hẹp hơn (hoặc rộng hơn) so với ý định của bạn trước khi bạn lưu.