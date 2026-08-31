---
title: Các hành động khối cho hàng tồn kho
---

Bên cạnh các điều chỉnh riêng lẻ, Spwig cung cấp cho bạn ba hành động khối trên danh sách **Các mặt hàng tồn kho** để thực hiện công việc quản lý tồn kho cho nhiều sản phẩm cùng lúc: chuyển kho giữa các nhà kho, ghi nhận hàng hóa bị hỏng hoặc mất, và kiểm kê lại tồn kho sau khi đếm thực tế. Cả ba hành động này đều có sẵn trong cùng một **Menu Hành động**, áp dụng cùng một số lượng cho mỗi mặt hàng tồn kho bạn chọn và đều được ghi nhận đầy đủ trong lịch sử kiểm tra di chuyển hàng tồn kho.

Đến với **Sản phẩm > Các mặt hàng tồn kho** để sử dụng chúng.

## Chạy một hành động tồn kho khối

1. Trên danh sách **Các mặt hàng tồn kho**, sử dụng bộ lọc hoặc tìm kiếm để tìm các mặt hàng bạn muốn cập nhật
2. Chọn ô bên cạnh mỗi mặt hàng tồn kho để bao gồm (hoặc sử dụng ô chọn ở tiêu đề để chọn tất cả các mặt hàng trên trang)
3. Chọn một trong ba hành động từ **Menu Hành động**:
   - **Chuyển hàng tồn kho sang kho mới**
   - **Ghi nhận hàng hóa bị hỏng/mất**
   - **Kiểm kê lại hàng tồn kho (đếm thực tế)**
4. Nhấn **Xong**
5. Xem trang xác nhận — nó liệt kê từng mặt hàng tồn kho đã chọn cùng với số lượng **có sẵn**, **đã phân bổ**, và **có thể sử dụng** hiện tại để bạn có thể kiểm tra lại xem bạn đã chọn đúng mặt hàng chưa
6. Điền vào các trường cho hành động đó (xem bên dưới) và nhấn nút gửi để áp dụng

![Danh sách Các mặt hàng tồn kho với dropdown Hành động khối đang mở, hiển thị Chuyển hàng tồn kho sang kho mới, Ghi nhận hàng hóa bị hỏng/mất và Kiểm kê lại hàng tồn kho (đếm thực tế) bên cạnh các hành động khác](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

Số lượng bạn nhập sẽ được áp dụng cho **mọi** mặt hàng được chọn — đây là thiết kế dành cho việc di chuyển, ghi nhận hoặc kiểm kê lại cùng một số lượng đơn vị trên nhiều SKU cùng lúc (ví dụ: chuyển 10 đơn vị của một số sản phẩm vào vị trí cửa hàng mới). Đối với một mặt hàng duy nhất với số lượng khác nhau, hãy chạy hành động đó lần nữa chỉ với mặt hàng đó được chọn, hoặc sử dụng **Điều chỉnh mức tồn kho** thay thế.

## Chuyển hàng tồn kho sang kho mới

Sử dụng để di chuyển hàng tồn kho có sẵn từ kho của mỗi mặt hàng được chọn sang một kho khác — ví dụ, tái nhập kho cho một địa điểm bán lẻ mới từ kho chính của bạn, hoặc cân bằng lại hàng hóa giữa các trung tâm xử lý khu vực.

Trên trang xác nhận, điền vào:

| Trường | Mô tả |
|-------|-------------|
| **Kho đích** | Nơi hàng hóa sẽ được chuyển đến. Chỉ có các kho hoạt động mới xuất hiện trong danh sách này. |
| **Số lượng mỗi mặt hàng** | Đơn vị cần chuyển khỏi kho hiện tại của mỗi mặt hàng được chọn. |
| **Lý do** | Ghi chú tùy chọn, ví dụ: "Tái nhập kho cửa hàng Auckland mới". |

Nhấn **Chuyển hàng tồn kho** để áp dụng.

![Trang xác nhận Chuyển hàng tồn kho: một thẻ Selected Stock Items liệt kê ba mặt hàng với các con số về số lượng có sẵn, đã phân bổ và có thể sử dụng, cùng với một biểu mẫu Chi tiết Chuyển hàng với kho đích, số lượng và lý do đã được điền](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Chỉ có hàng tồn kho chưa được phân bổ mới có thể chuyển đi.** Spwig chuyển từ *hàng tồn kho có sẵn* (số lượng có sẵn trừ đi các đơn hàng đang mở đã phân bổ) — các đơn vị đã cam kết cho đơn hàng của khách hàng sẽ vẫn ở kho nguồn để đơn hàng đó có thể được giao. Nếu một mặt hàng được chọn không đủ hàng tồn kho có sẵn để bù đắp số lượng bạn nhập, mặt hàng đó sẽ bị bỏ qua và một thông báo lỗi giải thích lý do; phần còn lại của danh sách vẫn được chuyển đi.

Nếu một mặt hàng được chọn đã có sẵn tại kho đích bạn đã chọn, nó sẽ bị bỏ qua tự động (không có gì để chuyển sang chính nó), và bạn sẽ thấy một thông báo cho biết có bao nhiêu mặt hàng bị bỏ qua do lý do này.

Mỗi lần chuyển hàng ghi nhận một cặp hoạt động vào lịch sử kiểm tra — một mục **Chuyển kho** âm tại kho nguồn và một mục dương tương ứng tại kho đích — do đó, lịch sử đầy đủ cho thấy chính xác hàng tồn kho đến từ đâu và đi đến đâu.

## Ghi nhận hàng hóa bị hỏng/mất

Sử dụng để ghi nhận các đơn vị bị hỏng, hư hỏng hoặc mất — ví dụ, sau khi phát hiện hàng hóa bị hỏng trong một lô hàng hoặc điều tra một sự chênh lệch.

Trên trang xác nhận, điền vào:

| Trường | Mô tả |
|-------|-------------|
| **Số lượng cần hủy (mỗi mặt hàng)** | Số đơn vị cần loại bỏ khỏi tồn kho thực tế cho mỗi mặt hàng được chọn. |
| **Lý do** | Ghi chú tùy chọn, ví dụ: "Hư hỏng do nước trong quá trình lưu kho". |

Nhấp vào **Ghi nhận hủy** để áp dụng.

**Tồn kho đã đặt chỗ không thể bị hủy.** Tồn kho thực tế không bao giờ được phép giảm xuống dưới số lượng hiện đang được phân bổ cho các đơn hàng mở — Spwig sẽ chặn việc hủy đối với bất kỳ mặt hàng nào mà số lượng bạn nhập vào sẽ xâm phạm vào kho đã phân bổ, để bạn không vô tình để lại một đơn hàng đã thanh toán mà không có đủ hàng để giao. Nếu điều này xảy ra với một mặt hàng, bạn sẽ thấy một thông báo lỗi nêu rõ tên mặt hàng và số đơn vị chưa đặt chỗ thực sự có sẵn để hủy.

Mỗi lần hủy được ghi nhận là một chuyển động **Hư hỏng/Mất** trên mặt hàng tồn kho đó, với số lượng âm.

## Kiểm kê lại tồn kho (đếm vật lý)

Sử dụng tính năng này sau khi kiểm kê vật lý để chỉnh sửa số lượng tồn kho thực tế cho khớp với số lượng bạn thực sự đếm được — cách nhanh nhất để đối soát nhiều mặt hàng sau một cuộc kiểm toán kho hoặc kiểm kê chu kỳ.

Trang xác nhận, hãy điền:

| Trường | Mô tả |
|-------|-------------|
| **Số lượng tồn kho thực tế đã đếm (mỗi mặt hàng)** | Số lượng bạn đã đếm vật lý. Tồn kho thực tế sẽ được đặt chính xác bằng con số này cho mọi mặt hàng được chọn — không cộng hay trừ. |
| **Lý do** | Ghi chú tùy chọn, ví dụ: "Kiểm kê kho quý 3". |

Nhấp vào **Áp dụng kiểm kê lại** để áp dụng.

![Trang xác nhận Kiểm kê lại tồn kho: thẻ Các mặt hàng tồn kho được chọn và biểu mẫu Chi tiết kiểm kê lại với số lượng tồn kho thực tế đã đếm và lý do được điền](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Khác với hai hành động còn lại, kiểm kê lại có thể điều chỉnh tồn kho theo cả hai hướng — tăng nếu bạn đếm được nhiều hơn hệ thống dự kiến, giảm nếu bạn đếm được ít hơn. Nếu số lượng bạn nhập thấp hơn số lượng hiện đang được phân bổ cho các đơn hàng mở, Spwig vẫn sẽ áp dụng (một con số kiểm kê là sự thật, không phải thứ để tranh cãi), nhưng chỉ số **Có sẵn** của mặt hàng đó sẽ hiển thị là `0` trong danh sách tồn kho và biểu tượng trạng thái sẽ chuyển sang Hết hàng — hãy coi đó là tín hiệu để kiểm tra xem các đơn hàng bị ảnh hưởng có thể được giao tiếp hay không.

Mỗi lần kiểm kê lại được ghi nhận là một chuyển động **Kiểm kê lại vật lý**, với số lượng hiển thị mức điều chỉnh (dương hoặc âm) giữa số tồn kho thực tế cũ và mới.

## Xem xét những gì đã thay đổi

Mọi chuyển kho, hủy và kiểm kê lại đều được ghi log theo cách giống như bất kỳ thay đổi tồn kho nào khác:

- Mở một mặt hàng tồn kho và cuộn xuống phần **Chuyển động tồn kho** để xem lịch sử đầy đủ của nó
- Hoặc điều hướng đến **Sản phẩm > Chuyển động tồn kho** để xem chuyển động của tất cả các mặt hàng, có thể lọc theo loại

Mỗi mục ghi nhận loại chuyển động, sự thay đổi số lượng, số tồn kho thực tế trước và sau, người thực hiện thay đổi, và lý do bạn đã nhập (nếu có) — vì vậy một chuyển kho hoặc hủy hàng loạt cũng dễ truy vết như một điều chỉnh thủ công đơn lẻ.

## Mẹo

- Chạy **Kiểm kê lại tồn kho** ngay sau khi kiểm kê vật lý khi các con số đếm được còn mới — dễ dàng phát hiện lỗi đánh máy trên trang xác nhận hơn là gỡ rối nó sau đó từ lịch sử chuyển động.

- Luôn điền **Lý do** cho các lần hủy và kiểm kê lại. Sáu tháng sau, "Hư hỏng do nước trong quá trình lưu kho" hữu ích hơn nhiều trong hồ sơ kiểm toán so với một trường trống.

- Trước khi chuyển kho, kiểm tra cột **Có sẵn** trên trang xác nhận — nó đã tính đến các đơn vị đã phân bổ, vì vậy bạn sẽ biết ngay lập tức nếu một số lượng quá cao cho một trong các mặt hàng bạn đã chọn.

- Các hành động này áp dụng cùng một số lượng cho mọi mặt hàng được chọn. Nhóm lựa chọn của bạn theo các mặt hàng thực sự cần cùng một số lượng được chuyển, hủy hoặc kiểm kê lại, và xử lý các trường hợp ngoại lệ từng mặt hàng một.

- Nếu bạn sử dụng POS tại một địa điểm bán lẻ, hãy nhớ rằng bộ đệm tồn kho của kho không phải là một phần của "có sẵn" cho các đơn hàng trực tuyến — nhưng các chuyển kho và hủy hàng loạt vẫn hoạt động dựa trên tổng tồn kho thực tế thực sự của kho.