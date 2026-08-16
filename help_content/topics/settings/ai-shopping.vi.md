---
title: Mua sắm bằng AI
---

Mua sắm bằng AI cho phép các trợ lý mua sắm bằng AI tìm thấy sản phẩm của bạn và, khi bạn cho phép, mua hàng từ cửa hàng của bạn thay mặt người dùng. Tính năng này **tắt theo mặc định** — việc bật nó lên là một lựa chọn có chủ ý, và cho đến khi bạn thực hiện, cửa hàng của bạn sẽ không tiết lộ điều gì cho các trợ lý này.

## Bật tính năng

Mở **Cài đặt → Mua sắm bằng AI** và chuyển **Mua sắm chủ động được bật** sang chế độ bật. Từ điểm này, các trợ lý hỗ trợ Giao thức Mua sắm Tổng quát có thể phát hiện cửa hàng của bạn và đọc danh mục sản phẩm của bạn. Không điều gì về cửa hàng thông thường của bạn thay đổi.

## Bảng kiểm tra tình trạng

Phần đầu trang của trang Mua sắm bằng AI trả lời một câu hỏi bằng một câu: **Các trợ lý AI có thể mua hàng từ cửa hàng của bạn ngay bây giờ không?**

- **"Các trợ lý AI có thể mua hàng từ cửa hàng của bạn"** — mọi thứ cần thiết cho một giao dịch đã sẵn sàng.
- **"Các trợ lý AI có thể duyệt cửa hàng của bạn, nhưng chưa thể mua hàng"** — cửa hàng của bạn có thể phát hiện được, nhưng vẫn còn thiếu thứ gì đó trước khi giao dịch có thể hoàn tất (thường là nhà cung cấp thanh toán được kết nối).
- **"Chế độ dừng khẩn cấp đang bật"** hoặc **"Mua sắm chủ động bị tắt"** — không điều gì được cung cấp cho các trợ lý.

Dưới phần đánh giá, bạn sẽ thấy một danh sách kiểm tra ngắn — nhà cung cấp thanh toán đã được kết nối, chi phí vận chuyển có thể được báo giá, sản phẩm có thể nhìn thấy bởi các trợ lý — với một gợi ý bên cạnh bất kỳ thứ gì vẫn cần sự chú ý. Các số đếm cho thấy bao nhiêu sản phẩm các trợ lý có thể bán, bao nhiêu sản phẩm bạn đã ẩn khỏi chúng, bao nhiêu trợ lý đã truy cập, và bao nhiêu bạn đã chặn.

Danh sách kiểm tra phản ánh **cài đặt đang hoạt động** của bạn: kết nối nhà cung cấp thanh toán hoặc thêm phương thức vận chuyển và phần đánh giá sẽ được cập nhật lần tiếp theo bạn mở trang này.

## Chế độ dừng khẩn cấp

**Chế độ dừng khẩn cấp** là một nút chuyển riêng biệt so với nút chính. Sử dụng nó để dừng mọi hoạt động của trợ lý ngay lập tức — ví dụ, nếu điều gì đó trông có vấn đề — mà không cần thay đổi cấu hình của bạn. Xóa nó để tiếp tục. Hãy nghĩ đến nút chính là "tính năng này có được cấu hình không" và chế độ dừng khẩn cấp là "tắt mọi thứ ngay bây giờ".

## Những gì các trợ lý có thể làm

Hai cấp độ truy cập, được kiểm soát riêng biệt:

- **Đọc (phát hiện và duyệt)** là rủi ro thấp hơn. Một trợ lý có thể tìm thấy cửa hàng của bạn và đọc chi tiết sản phẩm.
- **Thanh toán (thực sự mua hàng)** là rủi ro cao hơn và sẽ bị khóa với các trợ lý chưa được xác minh trừ khi bạn cho phép chúng.

Một cửa hàng có thể có thể phát hiện được mà không cần mua hàng — đây là cách hữu ích để bắt đầu.

## Ẩn các sản phẩm cụ thể

Mỗi sản phẩm đều có **Cài đặt "Có thể nhìn thấy bởi các đại diện mua sắm bằng AI"** (mặc định là bật). Tắt nó đi để giữ một sản phẩm cụ thể khỏi các trợ lý trong khi nó vẫn ở trên cửa hàng của bạn — điều này hữu ích cho các mặt hàng bạn muốn bán chỉ thông qua trang web của riêng mình.

## Quản lý từng trợ lý riêng lẻ

Khi một trợ lý mua hàng lần đầu — hoặc cố gắng mua — Spwig ghi nhận nó dưới **Mua sắm bằng AI → Xác minh Trợ lý**. Mỗi mục hiển thị địa điểm đã xác minh của trợ lý (thư mục mà nó ký tên), cấp độ tin cậy của nó, và số lượng yêu cầu mà nó đã thực hiện. Tên và biểu tượng mà trợ lý trình bày chỉ được hiển thị dưới dạng *thông tin được tuyên bố* — hãy xem chúng như nhãn, chứ không phải bằng chứng về danh tính; phần địa điểm đã xác minh là phần có thể tin cậy được.

Mỗi trợ lý đều ở một trong ba cấp độ tin cậy:

| Cấp độ tin cậy | Điều đó có nghĩa là gì | 
|---|---| 
| **Hạn chế (đã xác minh, giới hạn)** | Mức mặc định cho một trợ lý mới. Spwig đã ghi nhận danh tính của nó, và nó mang theo các giới hạn giá trị đơn hàng, giới hạn chi tiêu hàng ngày, và các hạn chế thanh toán được đặt trên chính sách của nó (xem bên dưới). | 
| **Đã xác minh (giới hạn bị xóa)** | Một quyết định có chủ ý của bạn để tin tưởng trợ lý này một cách hoàn toàn. Giới hạn giá trị đơn hàng và chi tiêu hàng ngày của nó bị xóa. | 
| **Bị chặn** | Trợ lý đó không còn có thể mua hàng từ cửa hàng của bạn. Các giao dịch đang mở sẽ bị kết thúc, dù bất kỳ khoản thanh toán nào đã được thực hiện đều được giữ nguyên.

Để dừng một trợ lý, chọn nó trong danh sách và chọn **Chặn các trợ lý được chọn**. **Bỏ chặn các trợ lý được chọn** luôn luôn đưa nó trở lại **Hạn chế** — không bao giờ trực tiếp sang **Đã xác minh** — vì việc xóa giới hạn là một bước riêng biệt, có chủ ý.

Để xóa toàn bộ giới hạn của một trợ lý, chọn nó và chọn **Nâng cấp lên đã xác minh (xóa giới hạn)**.

Điều này xóa giá trị đơn hàng cao nhất và giới hạn chi tiêu hàng ngày của nó, đồng thời chuyển trợ lý sang trạng thái đã xác minh.

Một trợ lý bị chặn sẽ bị bỏ qua — hãy mở khóa trước, sau đó nâng cấp lên.

Hãy xem đây là một quyết định tin cậy thực sự: chỉ nâng cấp trợ lý mà bạn chắc chắn về nó, vì việc xác minh sẽ xóa bỏ các rào chặn ban đầu mà một trợ lý mới có thể có.

## Thiết lập giới hạn cho trợ lý

Mở trang chi tiết của trợ lý và sử dụng phần **Chính sách (giới hạn và các loại tiền thưởng được phép)** để thiết lập những gì trợ lý được phép thực hiện:

| Trường | Điều mà nó kiểm soát |
|---|---|
| **Giá trị đơn hàng tối đa** | Đơn hàng lớn nhất mà trợ lý này có thể đặt. Để trống nếu không có giới hạn. |
| **Giới hạn chi tiêu hàng ngày** | Số tiền nhiều nhất mà trợ lý này có thể chi cho tất cả các đơn hàng trong một ngày. Để trống nếu không có giới hạn. |
| **Cho phép mã giảm giá** | Liệu trợ lý có thể áp dụng mã giảm giá khi thanh toán không? |
| **Cho phép thẻ quà tặng** | Liệu trợ lý có thể sử dụng thẻ quà tặng không? |
| **Cho phép hàng hóa số** | Liệu trợ lý có thể mua hàng hóa số không? |
| **Tỷ lệ giới hạn (một phút)** | Số lượng yêu cầu mà trợ lý có thể gửi đến cửa hàng của bạn mỗi phút. |

Một trợ lý mới sẽ bị giới hạn với giá trị đơn hàng cụ thể và giới hạn chi tiêu, đồng thời các tùy chọn mã giảm giá, thẻ quà tặng và hàng hóa số đều bị tắt — đây là mặc định một cách bảo thủ. Thay đổi bất kỳ trường nào và lưu lại; mọi thay đổi đều được ghi vào **Sự kiện Trợ lý** với các giá trị trước và sau, do đó bạn luôn có bản ghi về ai đã thay đổi điều gì và khi nào. Việc nâng cấp trợ lý lên trạng thái đã xác minh sẽ xóa giá trị đơn hàng tối đa và giới hạn chi tiêu hàng ngày của nó cho bạn — bạn không cần phải xóa chúng thủ công trước.

## Bản ghi hoạt động

**AI Shopping → Sự kiện Trợ lý** là một bản ghi không thể thay đổi được những gì các trợ lý đã làm — mọi yêu cầu được xác minh, mọi nỗ lực bị chặn, mọi thay đổi bạn thực hiện. Đây là bản ghi chỉ đọc và không thể chỉnh sửa hoặc xóa, do đó nó sẽ trở thành bằng chứng của bạn nếu một giao dịch do trợ lý nào đó thực hiện bị tranh cãi.

## Một lưu ý về các nền tảng trợ lý

Các công ty đang chạy các trợ lý này (và các quy tắc để xuất hiện trong đó) là mới và thường xuyên thay đổi. Một số yêu cầu bạn phải nộp hồ sơ hoặc đáp ứng điều kiện khu vực trước khi sản phẩm của bạn có thể được mua thông qua chúng. Spwig giúp cửa hàng của bạn sẵn sàng; việc một trợ lý nhất định có liệt kê bạn hay không là do chính trợ lý đó quyết định.

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật.