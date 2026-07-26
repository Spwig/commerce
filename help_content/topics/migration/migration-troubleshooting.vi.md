---
title: Giải quyết sự cố di chuyển
---

Hầu hết các lần di chuyển đều hoàn tất mà không có sự cố, nhưng kết nối có thể thất bại, việc nhập có thể hết thời gian, và đôi khi một lần chạy dừng lại giữa chừng. Chủ đề này đề cập đến việc chẩn đoán một kết nối thất bại, đọc nhật ký tiến độ trong khi đang nhập, và — quan trọng nhất — những lựa chọn thực sự của bạn khi mọi thứ đi sai hướng, bao gồm việc Retry, Cancel và Rollback thực sự làm gì.

## Lỗi kết nối tại bước 2

Ô **Test connection before proceeding** mặc định được bật và là phương pháp chẩn đoán đầu tiên — nó xác minh thông tin xác thực với nền tảng nguồn trước khi bạn cam kết với phần còn lại của wizard. Nếu nó thất bại, thông báo lỗi thường chỉ ra một trong những điều sau:

- **WooCommerce** — URL cửa hàng thiếu `https://` hoặc có phần đường dẫn cuối; khóa người tiêu dùng/ bí mật bị gõ sai hoặc được tạo lại; hoặc khóa API REST được tạo mà không có quyền **Read** tại **WooCommerce > Settings > Advanced > REST API**.
- **Shopify** — Tên miền cửa hàng không ở dạng `yourstore.myshopify.com`; ID/ bí mật khách hàng từ ứng dụng sai; hoặc, phổ biến nhất, một ứng dụng được tạo trong bảng điều khiển phát triển nhưng chưa bao giờ được **cài đặt** — việc tạo một phiên bản ứng dụng là chưa đủ, bạn cần liên kết phân phối tùy chỉnh và nhấp vào **Install**. Spwig cũng cảnh báo nếu `read_products`, `read_customers`, hoặc `read_orders` không được bao gồm trong phạm vi của ứng dụng.
- **Magento 2** — URL cửa hàng trỏ đến gian hàng thay vì gốc API, hoặc một token tích hợp được tạo nhưng chưa được kích hoạt (**Save > Activate > Allow**).
- **Vấn đề SSL** — chứng chỉ đã hết hạn, tự ký hoặc cấu hình sai sẽ làm thất bại kết nối trước khi kiểm tra thông tin xác thực, hiển thị như một lỗi chung thay vì lỗi xác thực. Nếu thông tin xác thực trông đúng, hãy kiểm tra chứng chỉ tiếp theo.

Chạy lại kiểm tra kết nối sau mỗi lần sửa chữa thay vì thay đổi nhiều thông tin xác thực cùng lúc — điều này giúp xác định thông tin nào sai.

## Đọc nhật ký trực tiếp tại bước 5

Trong khi đang nhập, bước 5 hiển thị nhật ký hoạt động khi nó xảy ra. Nhấp vào **Show Details** để mở rộng nó thành các mục riêng lẻ — cấp độ và thông báo — thay vì chỉ tóm tắt bước hiện tại. Đây là cách nhanh nhất để xem điều gì đang xảy ra nếu tiến độ trông như bị đình trệ: một loạt các mục "đã bỏ qua" cho một loại dữ liệu thường chỉ có nghĩa là tính năng "Bỏ qua các mục hiện có" đang hoạt động như dự kiến, không có nghĩa là mọi thứ bị kẹt.

Trang xem nhật ký chỉ hiển thị **500 mục gần nhất**, vì vậy trên một lần di chuyển lớn, các mục đầu tiên sẽ trượt khỏi tầm nhìn trong khi việc nhập vẫn đang chạy. Nếu bạn cần nhật ký đầy đủ sau khi một loại dữ liệu đã hoàn tất, hãy sử dụng **Download Logs** trên trang kết quả thay vào đó — nó không có giới hạn nào.

## Điều mà một lần di chuyển thất bại thực sự có nghĩa là gì

Đây là điều quan trọng nhất cần hiểu khi một lần di chuyển thất bại.

Khi một lần di chuyển thất bại, trang hoàn tất sẽ rõ ràng cho bạn biết điều gì đã xảy ra: các mục đã được nhập trước lỗi vẫn còn trong cửa hàng của bạn, không có gì bị xóa tự động, và việc sửa lỗi và chạy lại việc nhập sẽ bỏ qua những gì đã được đưa vào lần đầu. Hãy chấp nhận điều này như đúng như nó là. Không bước nào trong việc nhập chạy bên trong một giao dịch cơ sở dữ liệu có thể được quay lại như một đơn vị — bất cứ thứ gì đã được nhập thành công trước điểm thất bại, sản phẩm, danh mục, khách hàng, đơn hàng, bất kể công việc đã đạt được, vẫn tồn tại trong cửa hàng của bạn đúng như nó được tạo ra. Một lần di chuyển thất bại là một lần di chuyển **bán thành công**, không phải là một lần di chuyển bị hủy bỏ.

Sự thất bại cũng đánh dấu công việc là không còn có thể hoàn tác được nữa, vì vậy nút **Rollback** sẽ không khả dụng trên một **lần nhập** thất bại — nó chỉ xuất hiện khi một lần di chuyển đã hoàn tất, hoặc nếu việc hoàn tác của một lần di chuyển đã hoàn tất tự nó thất bại giữa chừng, trong trường hợp đó Spwig sẽ cung cấp lại nút này để bạn có thể thử lại. Tình huống duy nhất mà bạn sẽ muốn một sự hoàn tác tự động nhất — một lần nhập thất bại — vẫn chính xác là tình huống mà nút này không được cung cấp.

Vì vậy, khi một lần di chuyển thất bại:


1. **Xem xét những gì đã được nhập**, sử dụng các con số Imported/Skipped/Failed và các nhật ký đã tải xuống để xây dựng một bức tranh về những gì có trong cửa hàng của bạn và những gì không thể nhập được.

2. **Quyết định cách dọn dẹp.** Đối với một lượng dữ liệu không hoàn chỉnh nhỏ, hãy xem xét nó một cách thủ công và xóa những gì bạn không muốn thông qua các danh sách quản trị bình thường.

Đối với một lượng dữ liệu không hoàn chỉnh lớn hơn hoặc lộn xộn hơn, thường nhanh hơn để tự xóa dữ liệu đã nhập trước khi bắt đầu lại từ đầu thay vì đối chiếu từng mục một.

3. **Chạy lại với tùy chọn Skip existing items được bật**, bất kể bạn chọn con đường dọn dẹp nào — đây là cách ngăn dữ liệu đã tồn tại bị sao chép trong lần thử tiếp theo.

## Retry

**Retry** khởi động lại toàn bộ quá trình nhập từ đầu. Nó xóa các đếm và nhật ký của công việc trước đó và nhập lại mọi thứ từ đầu — nó **không** tiếp tục từ điểm mà lần thử thất bại đã dừng lại. Hãy giữ tùy chọn **Skip existing items** được bật để các mục đã được nhập lần đầu không bị sao chép trong lần chạy thứ hai.

Nếu một cuộc di chuyển dừng lại vì đã đạt đến **giới hạn 4 giờ**, thông báo bạn sẽ thấy là chính xác: việc chạy lại toàn bộ sẽ bắt đầu từ đầu và bỏ qua các mục đã được nhập, không phải là tiếp tục từ điểm dừng trước đó. Đối với một cửa hàng đủ lớn để đạt đến giới hạn thời gian, việc chạy lại toàn bộ nhiều lần hiếm khi hoàn tất; thay vào đó, hãy giảm phạm vi của mỗi lần chạy bằng cách chọn ít loại dữ liệu hơn trong bước 3 (sản phẩm trong một lần chạy, đơn hàng trong lần khác) và thực hiện nhiều lần chạy nhỏ hơn.

## Cancel

**Cancel** có sẵn trên một cuộc di chuyển đang chạy, và nó đánh dấu công việc là thất bại ngay lập tức trên bảng điều khiển. Nó **không** dừng lại nhiệm vụ nhập nền sau, nhiệm vụ này vẫn tiếp tục chạy và ghi dữ liệu cho đến khi đạt đến điểm dừng tự nhiên. Dự kiến số lượng đã nhập sẽ tiếp tục tăng trong một thời gian sau khi bạn hủy bỏ — hãy để chúng ổn định trước khi quyết định cách dọn dẹp, thay vì hành động dựa trên các con số được ghi lại ngay lúc bạn nhấn Cancel.

## There is no pause or resume

Spwig không hỗ trợ việc tạm dừng một cuộc di chuyển đang diễn ra và tiếp tục sau này. Nút **Resume** trên bảng điều khiển dành cho một trường hợp khác: một cuộc di chuyển được cấu hình thông qua hướng dẫn nhưng chưa bao giờ bắt đầu. Nó mở lại hướng dẫn tại điểm bạn đã dừng lại khi cấu hình — không liên quan đến một cuộc chạy đang diễn ra.

## Hoàn tác

> **Cảnh báo:** Hoàn tác là một hành động vĩnh viễn và mang tính phá hủy. Hãy đọc kỹ toàn bộ phần này trước khi sử dụng.

Hoàn tác được cung cấp trên một lần di chuyển **đã hoàn tất**, và cũng được cung cấp lại trên một lần mà chính việc hoàn tác của nó trước đó đã thất bại giữa chừng (trạng thái **Hoàn tác thất bại**), để một lần hoàn tác bị đình trệ có thể được thử lại. Nó chỉ xóa những gì chính lần nhập đã tạo ra, và giữ lại bất cứ điều gì cửa hàng của bạn hiện đang phụ thuộc vào:

- Một khách hàng đã di chuyển đã đặt một đơn hàng thực sự kể từ khi nhập sẽ được **giữ lại** — tài khoản, địa chỉ, lịch sử trung thành và tín dụng cửa hàng của họ vẫn thuộc về họ, và đơn hàng thực đó được giữ nguyên không bị động đến. Chỉ những đơn hàng do lần nhập tạo ra mới bị xóa.
- Một sản phẩm đã di chuyển vẫn được tham chiếu bởi bất kỳ đơn hàng, gói hàng, thẻ quà tặng hoặc vị trí cấu hình nào sẽ được **giữ lại**. Các đơn hàng thuộc về khách hàng khác không bao giờ bị sửa đổi — hoàn tác không còn có thể loại bỏ các mục hàng khỏi một đơn hàng không liên quan hoặc khiến nó có tổng số tiền sai.
- Bất cứ thứ gì được giữ lại đều được báo cáo lại cho bạn theo tên và số lượng, kèm theo lý do — ví dụ "Đã giữ lại 1 Sản phẩm, vẫn được tham chiếu bởi một mục đơn hàng" — để bạn biết chính xác điều gì vẫn còn ở đó và tại sao.
- Các đại lý, hoa hồng và khoản thanh toán mà lần nhập đã tạo ra **sẽ bị** xóa, cùng với bất kỳ tài khoản đại lý nào mà lần nhập đã tạo ra. Một đại lý gắn với một khách hàng đã tồn tại từ trước vẫn giữ được tài khoản của họ; chỉ bản ghi đại lý bị xóa.
- Lịch sử trung thành và tín dụng cửa hàng đi theo khách hàng: bị xóa nếu khách hàng bị xóa, được giữ lại nếu khách hàng được giữ lại.

Nó vẫn **không** xóa các gói đăng ký, mức giá hoặc tài nguyên đặt chỗ do các tiện ích mở rộng của cửa hàng tạo ra — những thứ này vẫn tồn tại sau khi hoàn tác và cần được dọn dẹp thủ công nếu bạn không muốn giữ chúng.

Trước khi bạn xác nhận, trang xác nhận sẽ hiển thị bản xem trước chính xác những gì sẽ bị xóa và những gì sẽ được giữ lại, được tính toán dựa trên dữ liệu trực tiếp của bạn — hãy đọc kỹ trước khi nhấp vào **Có, Hoàn tác Di chuyển**. Sau đó, việc hoàn tác sẽ chạy trong nền thay vì trong trình duyệt của bạn, vì vậy bạn có thể đóng tab một cách an toàn; hãy kiểm tra trạng thái của lần di chuyển để xem báo cáo về những gì thực sự đã bị xóa và được giữ lại khi nó hoàn tất.

Vì việc hoàn tác không còn vượt ra ngoài những gì lần nhập đã tạo ra, nó không còn là một công cụ chỉ dùng trong ngày — các đơn hàng thực của một khách hàng đã di chuyển và doanh số thực của một sản phẩm đã di chuyển được bảo vệ dù đã bao lâu trôi qua kể từ lần di chuyển. Nó vẫn là một hành động vĩnh viễn, mang tính phá hủy đối với các bản ghi mà nó thực sự xóa, vì vậy hãy sử dụng nó một cách có chủ đích chứ không tùy tiện, và tự dọn dẹp bằng tay bất cứ thứ gì Spwig giữ lại mà bạn thực sự không muốn.

Về tính khả dụng: nút Hoàn tác sẽ hiển thị trên tóm tắt của một lần di chuyển đã hoàn tất cho đến khi bản ghi công việc còn tồn tại — đối với hầu hết các nền tảng không có hạn chót cố định. Magento là ngoại lệ và mất tính khả dụng hoàn tác sau một khoảng thời gian nhất định, vì vậy hãy quyết định nhanh nếu bạn đang sử dụng Magento. Bản ghi công việc không bị xóa theo bất kỳ lịch trình nào, vì vậy một lần di chuyển vẫn có thể hoàn tác vô thời hạn trừ khi bạn tự xóa bản ghi đó.

## Chiến lược cho cửa hàng lớn và các lần nhập chậm

Đối với một cửa hàng đủ lớn đến mức một lần chạy duy nhất có nguy cơ vượt quá giới hạn 4 giờ:

- **Tăng kích thước lô** trong bước 3 (tối đa 100) — các lô lớn hơn thường có nghĩa là ít chuyến đi hơn và tốc độ truyền dữ liệu nhanh hơn.
- **Chia nhỏ việc di chuyển thành nhiều lần chạy theo loại dữ liệu** — các danh mục và sản phẩm trong một lần chạy, khách hàng và đơn hàng trong lần chạy tiếp theo, thay vì tất cả cùng lúc.
- **Giữ tùy chọn Bỏ qua các mục đã tồn tại bật** cho mọi lần chạy sau lần đầu tiên, để các lần chạy lặp lại không sao chép những gì đã thành công.
- **Tắt tùy chọn Nhập hình ảnh sản phẩm.** Việc tải xuống và xử lý từng hình ảnh thường là yếu tố lớn nhất làm chậm lần chạy. Bạn có thể thêm hình ảnh vào sản phẩm riêng lẻ hoặc thông qua một lần nhập CSV riêng biệt sau khi phần còn lại của dữ liệu đã được đưa vào.

## Một số mẹo

- **Kiểm tra kết nối sau mỗi lần thay đổi thông tin xác thực**, chứ không phải chỉ một lần ở cuối — điều này giúp xác định giá trị nào đang sai.
- **Không bao giờ giả định rằng một công việc thất bại đã tự dọn dẹp** — hãy kiểm tra xem thực sự có gì trong cửa hàng của bạn trước khi quyết định dọn dẹp hoặc thử lại.
- **Tùy chọn Bỏ qua các mục đã tồn tại nên được giữ bật cho mọi lần thử lại** — đây là yếu tố duy nhất ngăn chặn việc trùng lặp trong lần chạy thứ hai.
- **Đừng cố gắng vượt qua giới hạn 4 giờ bằng cách tăng số lần thử lại** — hãy chia nhỏ theo loại dữ liệu thay vào đó.
- **Đọc bản xem trước hoàn tác trước khi xác nhận** — nó liệt kê chính xác những gì sẽ bị xóa và những gì sẽ được giữ lại, được tính toán dựa trên dữ liệu trực tiếp của bạn, vì vậy sẽ không có bất ngờ nào xảy ra.