---
title: Hạn chế phiếu quà tặng
---

Các hạn chế phiếu quà tặng kiểm soát người dùng có thể sử dụng phiếu quà tặng, thời gian sử dụng và tần suất sử dụng. Cấu hình các cài đặt này khi tạo hoặc chỉnh sửa phiếu quà tặng tại **Marketing > Phiếu quà tặng**.

![Quy tắc hạn chế](/static/core/admin/img/help/voucher-restrictions/restriction-rules.webp)

## Giới hạn sử dụng

Đặt giới hạn toàn bộ và theo khách hàng trong phần **Giới hạn sử dụng** của biểu mẫu phiếu quà tặng.

- **Số lần sử dụng tối đa** — Số lần tối đa phiếu quà tặng này có thể được sử dụng trên tất cả khách hàng. Để trống để không giới hạn.
- **Số lần sử dụng mỗi khách hàng** — Số lần một khách hàng duy nhất có thể sử dụng phiếu quà tặng này. Đặt thành 1 cho hầu hết các chiến dịch.

| Mẫu | Tổng tối đa | Mỗi khách hàng | Trường hợp sử dụng |
|-----|-------------|----------------|------------------|
| Chiến dịch giới hạn | 100 | 1 | "100 khách hàng đầu tiên" tạo cảm giác khan hiếm |
| Mã chia sẻ không giới hạn | (trống) | 1 | Chiến dịch tiếp thị liên tục |
| Mã sử dụng nhiều lần không giới hạn | (trống) | (trống) | Giảm giá nội bộ/nhân viên |
| Mã duy nhất sử dụng một lần | 1 | 1 | Mã chiến dịch được tạo hàng loạt |

## Giá trị đơn hàng tối thiểu

Trường **Giá trị đơn hàng tối thiểu** bảo vệ lợi nhuận của bạn bằng cách yêu cầu tổng giá trị giỏ hàng trước khi áp dụng phiếu quà tặng. Ví dụ, "Giảm 10 đô la cho đơn hàng trên 50 đô la" đảm bảo bạn không bao giờ giảm giá đơn hàng nhỏ đến mức không có lợi nhuận.

| Giảm giá | Giá trị tối thiểu được đề xuất | Tỷ lệ |
|----------|-----------------------------|-------|
| Giảm 5 đô la | 30 đô la trở lên | ~6:1 |
| Giảm 10 đô la | 50 đô la trở lên | ~5:1 |
| Giảm 20 đô la | 100 đô la trở lên | ~5:1 |
| Giảm 15% | 40 đô la trở lên | Phụ thuộc vào danh mục sản phẩm |

## Giới hạn giảm giá (Giá trị giảm tối đa)

Trường **Giá trị giảm tối đa** trong **Cấu hình giảm giá** giới hạn số tiền mà phiếu quà tặng theo tỷ lệ có thể khấu trừ. Điều này chỉ áp dụng cho phiếu quà tặng theo tỷ lệ và ngăn chặn việc giảm giá quá mức trên các đơn hàng có giá trị cao.

Ví dụ: "Giảm 20%, tối đa 50 đô la"
- Giỏ hàng 200 đô la = Giảm 40 đô la (20%)
- Giỏ hàng 300 đô la = Giảm 50 đô la (bị giới hạn)
- Giỏ hàng 1.000 đô la = Vẫn giảm 50 đô la (bị giới hạn)

Thêm giới hạn giảm giá cho bất kỳ phiếu quà tặng theo tỷ lệ nào bạn chia sẻ công khai.

## Quy tắc kết hợp

Trường **Hạn chế và quy tắc** (nhấp để mở rộng) chứa các hộp kiểm kiểm soát cách phiếu quà tặng tương tác với các ưu đãi khác.

| Cài đặt | Mô tả | Khi nào nên bật |
|--------|-------|------------------|
| **Loại bỏ sản phẩm đang giảm giá** | Phiếu quà tặng bỏ qua các sản phẩm đang được giảm giá | Hầu hết các chiến dịch — bảo vệ lợi nhuận từ sản phẩm đang giảm giá |
| **Không thể kết hợp với các phiếu quà tặng khác** | Chỉ một phiếu quà tặng mỗi đơn hàng | Mặc định cho hầu hết các phiếu quà tặng |
| **Không thể kết hợp với sản phẩm đang giảm giá** | Ngăn phiếu quà tặng nếu giỏ hàng có BẤT KỲ sản phẩm đang giảm giá nào | Chiến dịch nghiêm ngặt nơi phiếu quà tặng thay thế giá giảm |
| **Chỉ dành cho khách hàng mới** | Chỉ khách hàng không có đơn hàng trước đó | Chiến dịch chào mừng/thu hút khách hàng |

## Hạn chế khách hàng

Để nhắm mục tiêu đơn giản, hãy chọn **Chỉ dành cho khách hàng mới** trong trường **Hạn chế và quy tắc**.

Để nhắm mục tiêu nâng cao, hãy sử dụng bảng **Hạn chế phiếu quà tặng** trực tiếp ở cuối biểu mẫu. Nhấp **+ Thêm một hạn chế phiếu quà tặng khác** để thêm hàng. Mỗi hạn chế có ba trường:

- **Loại** — Danh mục hạn chế (danh sách thả xuống)
- **Giá trị** — Giá trị khớp (phân tách bằng dấu phẩy hoặc JSON)
- **Là bao gồm** — Đánh dấu = khách hàng phải khớp; không đánh dấu = khách hàng phải KHÔNG khớp

| Loại | Giá trị | Bao gồm | Hiệu ứng |
|------|--------|---------|--------|
| user_email_domain | @company.com | Có | Chỉ nhân viên công ty mới có thể sử dụng |
| shipping_country | US,CA | Có | Chỉ khách hàng ở Mỹ và Canada |
| shipping_country | RU | Không | Tất cả KHÔNG PHẢI Nga |
| day_of_week | monday,tuesday | Có | Chỉ hợp lệ vào Thứ Hai và Thứ Ba |
| payment_method | stripe | Có | Chỉ dành cho thanh toán Stripe |

Kết hợp nhiều hàng để có các hạn chế phân tầng. Tất cả các hạn chế bao gồm phải khớp, và không có hạn chế loại trừ nào có thể khớp, để phiếu quà tặng có thể áp dụng.

## Chiến lược hết hạn

Kiểm soát thời điểm phiếu quà tặng hết hạn bằng các trường ngày và tính hợp lệ.

- **Ngày kết thúc** — Ngày giới hạn cứng (ví dụ: 31/12/2026).

Phiếu quà tặng ngừng hoạt động vào nửa đêm.
- **Số ngày hợp lệ** — Tính hợp lệ di chuyển từ ngày tạo hoặc lần sử dụng đầu tiên của phiếu quà tặng.

Điều này sẽ ghi đè ngày kết thúc khi được thiết lập.

Hữu ích cho mã chào mừng: "hợp lệ trong 30 ngày sau khi bạn nhận được nó".

| Chiến lược | Ngày kết thúc | Số ngày hợp lệ | Trường hợp sử dụng |
|----------|----------|------------|----------|
| Hạn chót cứng | Đặt | (trống) | Chiến dịch theo mùa, sự kiện |
| Thời gian trượt | (trống) | 30 | Mã chào mừng, phiếu thưởng |
| Không có ngày hết hạn | (trống) | (trống) | Mã liên tục, phiếu giảm giá nhân viên |

## Ngăn chặn lạm dụng

Hãy tuân theo danh sách kiểm tra này để đảm bảo phiếu giảm giá của bạn an toàn:

- Luôn đặt **Số lần sử dụng tối đa cho mỗi khách hàng** thành 1 trừ khi có lý do cụ thể không làm như vậy.
- Đặt **Giá trị đơn hàng tối thiểu** cho tất cả các phiếu giảm giá theo số tiền cố định.
- Thêm **Giá trị giảm giá tối đa** cho các phiếu giảm giá theo tỷ lệ công khai.
- Sử dụng mã khó đoán cho các phiếu giảm giá có giá trị cao — tránh các mã dễ đoán như "DISCOUNT50".
- Theo dõi phân tích sử dụng trên mỗi thẻ phiếu giảm giá trong bảng điều khiển.
- Vô hiệu hóa phiếu giảm giá ngay lập tức nếu bạn thấy các mẫu sử dụng bất thường.
- Đối với các chiến dịch có giá trị cao, hãy sử dụng các mã duy nhất được tạo theo lô thay vì một mã chung duy nhất.

## Mẹo

- Bắt đầu với các giới hạn nghiêm ngặt và lỏng lẻo hơn nếu tỷ lệ sử dụng quá thấp — dễ dàng hơn để nới lỏng các quy tắc hơn là siết chặt chúng sau khi mã đã được phát hành.
- Kiểm tra từng phiếu giảm giá bằng thanh toán thực tế trước khi phân phối cho khách hàng.
- Kiểm tra bảng điều khiển phân tích phiếu giảm giá thường xuyên để phát hiện vấn đề sớm.
- Kết hợp nhiều giới hạn để có bảo vệ đa lớp — ví dụ, giới hạn theo khách hàng + giá trị đơn hàng tối thiểu + giới hạn giảm giá + loại trừ các mặt hàng đang giảm giá.