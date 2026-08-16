---
title: Các hành động khối cho hàng tồn kho
---

Bên cạnh các điều chỉnh riêng lẻ, Spwig cung cấp cho bạn ba hành động khối trên danh sách **Các mặt hàng tồn kho** để thực hiện công việc quản lý tồn kho cho nhiều sản phẩm cùng lúc: chuyển hàng giữa các kho, ghi nhận hàng hóa bị hỏng hoặc mất, và kiểm kê lại hàng tồn sau khi đếm thực tế. Cả ba hành động này đều có trong cùng một **Dropdown Hành động**, áp dụng cùng một số lượng cho mỗi mặt hàng tồn kho bạn chọn và đều được ghi nhận đầy đủ trong lịch sử kiểm tra di chuyển hàng tồn kho.

Đến với **Sản phẩm > Các mặt hàng tồn kho** để sử dụng chúng.

## Chạy một hành động hàng tồn kho khối

1. Trên danh sách **Các mặt hàng tồn kho**, sử dụng bộ lọc hoặc tìm kiếm để tìm các mặt hàng bạn muốn cập nhật
2. Chọn ô bên cạnh mỗi mặt hàng tồn kho để bao gồm (hoặc sử dụng ô chọn ở đầu để chọn tất cả các mặt hàng trên trang)
3. Chọn một trong ba hành động từ **Dropdown Hành động**:
   - **Chuyển hàng tồn kho sang kho**
   - **Ghi nhận hàng hóa bị hỏng/mất**
   - **Kiểm kê lại hàng tồn (đếm thực tế)**
4. Nhấn **Xong**
5. Xem trang xác nhận — nó liệt kê từng mặt hàng tồn kho đã chọn cùng với số lượng **có sẵn**, **được phân bổ**, và **có thể sử dụng** hiện tại để bạn có thể kiểm tra lại xem bạn đã chọn đúng mặt hàng chưa
6. Điền vào các trường của hành động (xem bên dưới) và nhấn nút gửi để áp dụng

![Danh sách Các mặt hàng tồn kho với dropdown Hành động khối mở, hiển thị Chuyển hàng tồn kho sang kho, Ghi nhận hàng hóa bị hỏng/mất và Kiểm kê lại hàng tồn (đếm thực tế) bên cạnh các hành động khác](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

Số lượng bạn nhập sẽ được áp dụng cho **mọi** mặt hàng được chọn — đây là thiết kế dành cho việc di chuyển, ghi nhận hoặc kiểm kê lại cùng một số lượng đơn vị trên nhiều SKU cùng lúc (ví dụ: chuyển 10 đơn vị của một số sản phẩm vào vị trí cửa hàng mới). Đối với một mặt hàng duy nhất với số lượng khác nhau, hãy chạy hành động đó lần nữa chỉ với mặt hàng đó được chọn, hoặc sử dụng **Điều chỉnh mức tồn kho** thay thế.

## Chuyển hàng tồn kho sang kho

Sử dụng để di chuyển hàng tồn kho có sẵn từ kho của mỗi mặt hàng được chọn sang một kho khác — ví dụ, tái nhập kho cho một địa điểm bán lẻ mới từ kho chính của bạn, hoặc cân bằng lại hàng tồn kho giữa các trung tâm xử lý khu vực.

Trên trang xác nhận, điền vào:

| Trường | Mô tả |
|-------|-------------|
| **Kho đích** | Nơi hàng hóa nên được chuyển đến. Chỉ các kho hoạt động mới xuất hiện trong danh sách này. |
| **Số lượng mỗi mặt hàng** | Đơn vị cần chuyển khỏi kho hiện tại của mỗi mặt hàng được chọn. |
| **Lý do** | Ghi chú tùy chọn, ví dụ: "Tái nhập kho cửa hàng Auckland mới". |

Nhấn **Chuyển hàng tồn kho** để áp dụng.

![Trang xác nhận Chuyển hàng tồn kho: một thẻ Selected Stock Items liệt kê ba mặt hàng với các con số có sẵn/được phân bổ/có thể sử dụng, và một biểu mẫu Chi tiết Chuyển hàng với kho đích, số lượng và lý do đã được điền](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Chỉ có hàng tồn kho chưa được phân bổ mới có thể chuyển đi.** Spwig chuyển từ *hàng tồn kho có sẵn* (hàng có sẵn trừ các đơn hàng đang mở đã được phân bổ) — các đơn vị đã được cam kết cho đơn hàng của khách hàng sẽ vẫn ở kho nguồn để đơn hàng đó vẫn có thể được giao. Nếu một mặt hàng được chọn không đủ hàng tồn kho có sẵn để bù đắp số lượng bạn nhập, mặt hàng đó sẽ bị bỏ qua và một thông báo lỗi giải thích lý do; phần còn lại của danh sách vẫn được chuyển.

Nếu một mặt hàng được chọn đã có sẵn tại kho đích bạn đã chọn, nó sẽ bị bỏ qua tự động (không có gì để chuyển sang chính nó), và bạn sẽ thấy một thông báo cho biết có bao nhiêu mặt hàng đã bị bỏ qua do lý do này.

Mỗi lần chuyển hàng ghi lại một cặp ghi nhận di chuyển vào lịch sử kiểm tra — một ghi nhận **Chuyển kho** âm tại nguồn và một ghi nhận dương tương ứng tại đích — do đó, lịch sử đầy đủ cho thấy chính xác hàng tồn kho đến từ đâu và đi đến đâu.

## Ghi nhận hàng hóa bị hỏng/mất

Sử dụng để ghi nhận các đơn vị bị hỏng, hư hỏng hoặc mất — ví dụ, sau khi phát hiện hàng hóa bị hỏng trong một lô hàng hoặc điều tra một sự chênh lệch.

Trên trang xác nhận, điền vào:

| Field | Description |
|-------|-------------|
| **Số lượng ghi giảm (theo mặt hàng)** | Đơn vị cần loại bỏ khỏi số lượng tồn kho hiện có cho mỗi mặt hàng được chọn. |
| **Lý do** | Ghi chú tùy chọn, ví dụ: "Hư hỏng do nước trong quá trình lưu trữ". |

Nhấn **Ghi nhận ghi giảm** để áp dụng.

**Số lượng tồn kho được giữ riêng không thể ghi giảm được.** Số lượng tồn kho hiện có không bao giờ được phép thấp hơn số lượng đang được phân bổ cho đơn hàng mở — Spwig sẽ chặn việc ghi giảm cho bất kỳ mặt hàng nào mà số lượng bạn nhập sẽ làm giảm số lượng đã phân bổ, do đó bạn không thể vô tình để lại một đơn hàng đã thanh toán mà không có đủ số lượng tồn kho để giao.
Nếu xảy ra với một mặt hàng, bạn sẽ thấy một thông báo chỉ ra mặt hàng đó và số lượng đơn vị không bị phân bổ thực tế mà nó thực sự có thể ghi giảm.

Mỗi lần ghi giảm sẽ được ghi nhận dưới dạng **Hư hỏng/Mất mát** cho mặt hàng tồn kho đó, với số lượng âm.

## Đếm lại số lượng tồn kho (đếm thực tế)

Sử dụng chức năng này sau khi đếm thực tế số lượng tồn kho để điều chỉnh số lượng tồn kho cho đúng với số bạn đã đếm được — cách nhanh nhất để đối chiếu nhiều mặt hàng sau khi kiểm tra kho hoặc đếm chu kỳ.

Trên trang xác nhận, điền vào:

| Field | Description |
|-------|-------------|
| **Số lượng tồn kho đã đếm (theo mặt hàng)** | Số lượng bạn đã đếm thực tế. Số lượng tồn kho sẽ được đặt chính xác bằng con số này cho mỗi mặt hàng được chọn — không được cộng hoặc trừ. |
| **Lý do** | Ghi chú tùy chọn, ví dụ: "Cuối quý 3, đếm kho". |

Nhấn **Áp dụng đếm lại** để áp dụng.

![Trang xác nhận Đếm lại số lượng tồn kho: Thẻ Các mặt hàng tồn kho đã chọn và biểu mẫu Chi tiết đếm lại với số lượng tồn kho đã đếm và lý do đã điền](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Khác với hai hành động còn lại, đếm lại có thể làm thay đổi số lượng theo cả hai hướng — tăng nếu bạn đếm được nhiều hơn số hệ thống dự kiến, giảm nếu bạn đếm được ít hơn. Nếu số bạn nhập thấp hơn số lượng đang được phân bổ cho đơn hàng mở, Spwig vẫn áp dụng (việc đếm là sự thật, không phải điều gì để tranh luận), nhưng giá trị **Có sẵn** của mặt hàng đó sẽ hiển thị là `0` trên danh sách tồn kho và biểu tượng trạng thái của nó sẽ chuyển sang Hết hàng — xem đây là tín hiệu để kiểm tra xem các đơn hàng bị ảnh hưởng có thể được giao không.

Mỗi lần đếm lại sẽ được ghi nhận dưới dạng **Đếm lại thực tế** với số lượng thể hiện sự điều chỉnh (dương hoặc âm) giữa số tồn kho cũ và mới.

## Xem lại những thay đổi nào đã xảy ra

Mọi lần chuyển kho, ghi giảm và đếm lại đều được ghi chép theo cách giống như các thay đổi tồn kho khác:

- Mở một mặt hàng tồn kho và cuộn xuống phần **Lịch sử di chuyển tồn kho** để xem lịch sử đầy đủ của nó
- Hoặc điều hướng đến **Sản phẩm > Di chuyển tồn kho** để duyệt các lần di chuyển trên tất cả các mặt hàng, có thể lọc theo loại

Mỗi mục ghi nhận loại di chuyển, số thay đổi, số tồn kho trước và sau, ai đã thực hiện thay đổi, và lý do bạn đã nhập (nếu có) — do đó, một lần chuyển kho hàng loạt hoặc ghi giảm cũng dễ theo dõi như một điều chỉnh thủ công đơn lẻ.

## Lời khuyên

- Chạy **Đếm lại số lượng tồn kho** ngay sau khi đếm thực tế trong kho, khi các con số đã đếm còn nguyên vẹn — dễ dàng phát hiện lỗi gõ trong trang xác nhận hơn là tìm ra sau này từ lịch sử di chuyển.
- Luôn điền vào **Lý do** cho các lần ghi giảm và đếm lại. Sáu tháng sau, "Hư hỏng do nước trong quá trình lưu trữ" sẽ hữu ích hơn rất nhiều trong đường dẫn kiểm toán so với một trường trống.
- Trước khi chuyển kho, kiểm tra cột **Có sẵn** trên trang xác nhận — nó đã tính đến số lượng đã phân bổ, do đó bạn sẽ biết ngay nếu một số lượng nào đó quá cao cho một trong những mặt hàng bạn chọn.
- Các hành động này áp dụng cùng một số lượng cho mọi mặt hàng được chọn. Nhóm các mặt hàng cần cùng một số lượng di chuyển, ghi giảm hoặc đếm lại, và xử lý các trường hợp ngoại lệ từng mặt hàng một.
- Nếu bạn sử dụng POS tại một cửa hàng bán lẻ, hãy nhớ rằng số tồn kho dự phòng của kho hàng không phải là "có sẵn" cho các đơn hàng trực tuyến — nhưng các lần chuyển kho hàng loạt và ghi giảm vẫn hoạt động dựa trên tổng số tồn kho thực tế của kho.
