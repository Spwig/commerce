---
title: Mua sắm AI
---

Mua sắm AI cho phép các trợ lý mua sắm AI tìm kiếm sản phẩm của bạn và, khi bạn cho phép, mua hàng từ cửa hàng của bạn thay mặt khách hàng. Tính năng này **mặc định là tắt** — việc bật nó là một lựa chọn cố ý, và cho đến khi bạn bật, cửa hàng của bạn sẽ không tiết lộ bất cứ thứ gì cho các trợ lý này.

## Bật tính năng

Mở **Cài đặt → Mua sắm AI** và bật **Kinh doanh tự động được bật**. Từ thời điểm này, các trợ lý hỗ trợ Giao dịch Thương mại Phổ quát có thể phát hiện cửa hàng của bạn và đọc danh mục sản phẩm của bạn. Không có gì thay đổi trên cửa hàng trực quan của bạn.

## Bảng điều khiển sẵn sàng

Phần đầu trang Mua sắm AI trả lời một câu hỏi trong một câu: **Hiện tại, các trợ lý AI có thể thực sự mua hàng từ cửa hàng của bạn không?**

- **"Các trợ lý AI có thể mua hàng từ cửa hàng của bạn"** — mọi thứ cần thiết để thực hiện giao dịch đều đã sẵn sàng.
- **"Các trợ lý AI có thể duyệt cửa hàng của bạn, nhưng chưa thể mua hàng"** — cửa hàng của bạn có thể được phát hiện, nhưng vẫn còn thiếu một số thứ trước khi hoàn tất giao dịch (thường là nhà cung cấp thanh toán được kết nối).
- **"Chế độ dừng khẩn cấp đang bật"** hoặc **"Kinh doanh tự động đang tắt"** — không có gì được cung cấp cho các trợ lý.

Dưới phần kết luận, bạn sẽ thấy một danh sách kiểm tra ngắn — nhà cung cấp thanh toán được kết nối, có thể báo giá vận chuyển, sản phẩm có thể được trợ lý xem — với một gợi ý bên cạnh bất cứ thứ gì vẫn cần được chú ý. Các con số hiển thị số lượng sản phẩm trợ lý có thể bán, số lượng bạn đã ẩn khỏi họ, số lượng trợ lý đã truy cập và số lượng bạn đã chặn.

Danh sách kiểm tra phản ánh cấu hình **thực tế** của bạn: kết nối một nhà cung cấp thanh toán hoặc thêm phương thức vận chuyển và kết luận sẽ được cập nhật khi bạn mở lại trang.

## Chế độ dừng khẩn cấp

**Chế độ dừng khẩn cấp** là một công tắc riêng biệt so với công tắc chính. Sử dụng nó để dừng ngay lập tức mọi hoạt động của trợ lý — ví dụ, nếu bạn thấy điều gì đó không ổn — mà không cần thay đổi cấu hình của bạn. Xóa chế độ dừng để tiếp tục. Hãy nghĩ đến công tắc chính như là **tính năng này đã được cấu hình chưa** và chế độ dừng khẩn cấp như là **ngừng mọi thứ ngay lập tức**.

## Những gì trợ lý có thể làm

Hai cấp độ truy cập, được kiểm soát riêng biệt:

- **Đọc** (phát hiện và duyệt) là cấp độ rủi ro thấp hơn. Một trợ lý có thể tìm thấy cửa hàng của bạn và đọc chi tiết sản phẩm.
- **Thanh toán** (thực sự mua hàng) là cấp độ rủi ro cao hơn và sẽ giữ đóng đối với các trợ lý chưa được xác minh trừ khi bạn cho phép.

Một cửa hàng có thể được phát hiện nhưng không thể mua — đây là cách hữu ích để bắt đầu.

## Ẩn sản phẩm cụ thể

Mỗi sản phẩm đều có cài đặt **Hiển thị cho trợ lý mua sắm AI** (mặc định là bật). Tắt nó để giữ một sản phẩm cụ thể không hiển thị cho trợ lý trong khi nó vẫn hiển thị trên cửa hàng của bạn — hữu ích cho các mặt hàng bạn muốn bán chỉ qua trang web của riêng bạn.

## Quản lý trợ lý cá nhân

Khi một trợ lý thực hiện giao dịch đầu tiên — hoặc cố gắng — Spwig ghi lại dưới mục **Mua sắm AI → Nhận dạng Trợ lý**. Mỗi mục hiển thị nơi nhà ở đã được xác minh của trợ lý (thư mục mà trợ lý ký tên) và số lượng yêu cầu mà trợ lý đã thực hiện. Tên và biểu tượng mà trợ lý hiển thị chỉ được hiển thị như **chi tiết được tuyên bố** — hãy coi đó là nhãn, không phải bằng chứng xác minh danh tính; phần nhà ở đã được xác minh là phần duy nhất có thể tin cậy.

Các trợ lý mới bắt đầu **bị giới hạn**: họ có thể thực hiện giao dịch, nhưng trong giới hạn nhất định. Để dừng một trợ lý, hãy chọn nó và chọn **Chặn trợ lý đã chọn** — các giao dịch mở sẽ kết thúc và trợ lý không còn thể mua hàng, trong khi bất kỳ khoản thanh toán nào đã được thực hiện sẽ không bị ảnh hưởng. **Mở lại trợ lý đã chọn** sẽ đưa nó trở lại trạng thái bị giới hạn (không bao giờ trực tiếp trở lại không giới hạn — việc xóa giới hạn luôn là bước riêng biệt và có ý thức).

## Nhật ký hoạt động

**Mua sắm AI → Sự kiện Trợ lý** là một bản ghi có thể phát hiện được việc can thiệp của những gì trợ lý đã làm — mọi yêu cầu đã được xác minh, mọi nỗ lực bị chặn, mọi thay đổi bạn đã thực hiện. Đây là bản ghi chỉ đọc và không thể chỉnh sửa hoặc xóa, vì vậy nó sẽ là bằng chứng của bạn nếu có tranh chấp về một giao dịch mà trợ lý đã thực hiện.

## Một lưu ý về các nền tảng trợ lý

Các công ty điều hành các trợ lý này (và các quy tắc để xuất hiện trên chúng) là mới và thay đổi thường xuyên.

Một số yêu cầu bạn phải đăng ký hoặc đáp ứng các điều kiện khu vực trước khi sản phẩm của bạn có thể được mua thông qua chúng.

Spwig làm cho cửa hàng của bạn sẵn sàng; việc một trợ lý cụ thể liệt kê bạn hay không phụ thuộc vào trợ lý đó.