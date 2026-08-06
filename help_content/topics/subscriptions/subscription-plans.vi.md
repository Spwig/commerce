---
title: Các gói đăng ký
---

Các gói đăng ký cho phép bạn cung cấp thanh toán định kỳ cho sản phẩm của bạn — lý tưởng cho hàng tiêu dùng, dịch vụ, hộp được chọn lọc, hoặc bất kỳ sản phẩm nào mà khách hàng mua lặp lại. Hướng dẫn này giải thích cách tạo và cấu hình các gói, thiết lập các cấp độ giá, thêm thời gian dùng thử và gắn các tùy chọn bổ sung tùy chọn.

## Bắt đầu

Đi đến **Đăng ký > Các gói đăng ký** trong thanh điều hướng quản trị. Danh sách gói hiển thị tất cả các gói của bạn với mô hình giá, số lượng người đăng ký đang hoạt động, và trạng thái hiển thị.

Để tạo một gói mới, nhấn nút **+ Thêm gói đăng ký** — điều này mở trình hướng dẫn tạo gói, giúp bạn thiết lập từng bước một.

![Danh sách các gói đăng ký](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Một gói riêng lẻ không thể mua được — đó là mẫu. Một khi bạn đã xây dựng nó ở đây, hãy gắn nó với một hoặc nhiều sản phẩm từ tab **Đăng ký** của sản phẩm (chỉ các sản phẩm Đơn giản, Đa dạng và Số hóa) để khách hàng thực sự có thể đăng ký. Xem [Bán sản phẩm dưới dạng đăng ký](/help/selling-products-as-subscriptions) cho bước đó.

## Thông tin gói

Phần đầu tiên ghi nhận bản chất cốt lõi của gói của bạn.

- **Tên gói** — Tên mà khách hàng nhìn thấy khi đăng ký. Nhấn vào biểu tượng quả địa cầu để thêm bản dịch cho các ngôn ngữ cửa hàng khác.
- **Slug** — Một định danh URL được tạo tự động từ tên (ví dụ: `premium-plan`). Điều này được sử dụng bên trong và trong các tích hợp.
- **Mô tả** — Văn bản tùy chọn mô tả những gì gói bao gồm. Hỗ trợ dịch thuật.

## Mô hình giá

Chọn cách cấu trúc giá cho gói này:

| Mô hình giá | Tốt nhất cho |
|---------------|----------|
| **Giá theo cấp độ** | Cung cấp các tùy chọn cam kết hàng tháng, hàng quý và hàng năm với chiết khấu cho các khoản thời gian dài hơn |
| **Dựa trên số lượng** | Giá theo người dùng hoặc người dùng, tổng số thay đổi theo số lượng (ví dụ: giấy phép nhóm) |
| **Giá cố định** | Một mức giá cố định duy nhất mà không có sự thay đổi |

Đối với các gói **Dựa trên số lượng**, hãy đặt **Số lượng tối thiểu** (số ghế tối thiểu cần thiết) và tùy chọn **Số lượng tối đa** để giới hạn số ghế mà người đăng ký có thể mua.

## Các cấp độ giá

Các cấp độ giá xác định tần suất thanh toán và các tùy chọn chiết khấu có sẵn cho khách hàng trên gói này. Thêm chúng ở phần **Các cấp độ giá** bên dưới biểu mẫu chính.

Mỗi cấp độ có các trường sau:

- **Tên cấp độ** — Nhãn được hiển thị cho khách hàng (ví dụ: `Hàng tháng`, `Hàng năm — Tiết kiệm 20%`). Hỗ trợ dịch thuật.
- **Chu kỳ thanh toán** — Tần suất mà khách hàng bị tính phí: Hàng ngày, Hàng tuần, Hàng tháng, Hàng quý, Nửa năm, hoặc Hàng năm.
- **Khoảng cách thanh toán** — Hệ số nhân cho chu kỳ thanh toán. Đặt thành `2` với Hàng tháng để tính phí mỗi 2 tháng.
- **Phần trăm giảm giá** — Chiết khấu được áp dụng cho giá sản phẩm cho cấp độ này. Đặt thành `0` để giá đầy đủ, hoặc `20` để giảm 20%. Chiết khấu này được cộng thêm vào bất kỳ giá khuyến mãi nào trên chính sản phẩm.
- **Cấp độ mặc định** — Đánh dấu một cấp độ là mặc định để chọn trước cho khách hàng khi họ xem các tùy chọn đăng ký.

Chiết khấu áp dụng bắt đầu từ chu kỳ thanh toán đầu tiên của khách hàng, không chỉ trên các lần gia hạn — một cấp độ có chiết khấu 20% sẽ tính 20% giảm giá từ ngày đầu tiên (hoặc từ lần thanh toán đầu tiên sau khi thử, nếu gói có một).

### Ví dụ: gói cấp độ với ba tùy chọn

Đối với gói đăng ký "Coffee Club":

| Tên cấp độ | Chu kỳ thanh toán | Giảm giá |
|-----------|---------------|----------|
| Hàng tháng | Hàng tháng | 0% |
| Hàng quý — Tiết kiệm 10% | Hàng quý | 10% |
| Hàng năm — Tiết kiệm 20% | Hàng năm | 20% |

## Thời gian dùng thử

Một thời gian dùng thử cho phép khách hàng thử nghiệm đăng ký của bạn trước khi thanh toán đầu tiên đầy đủ. Cài đặt điều này trong phần **Thời gian dùng thử**:

- **Thời gian dùng thử (ngày)** — Số ngày dùng thử miễn phí. Đặt thành `0` để vô hiệu hóa thời gian dùng thử. Giới hạn tối đa là 365 ngày.
- **Giá trong thời gian dùng thử** — Giá giảm tùy chọn trong thời gian dùng thử (ví dụ: $1 cho tháng đầu tiên). Để trống để dùng thử hoàn toàn miễn phí.

## Chính sách hủy bỏ

Kiểm soát cách khách hàng có thể hủy bỏ đăng ký của họ trong phần **Chính sách hủy bỏ**:

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật.

| Chính sách | Mô tả |
|--------|-------------|
| **Hủy bất kỳ lúc nào** | Khách hàng có thể hủy ngay lập tức vào bất kỳ thời điểm nào |
| **Hủy vào cuối kỳ** | Việc hủy sẽ có hiệu lực vào cuối kỳ thanh toán — khách hàng được truy cập cho đến khi hết hạn |
| **Yêu cầu cam kết tối thiểu** | Khách hàng phải hoàn tất một số chu kỳ thanh toán tối thiểu trước khi hủy |

Các cài đặt bổ sung:

- **Cam kết tối thiểu (chu kỳ)** — Khi sử dụng chính sách cam kết, hãy đặt số chu kỳ thanh toán tối thiểu (ví dụ: `3` cho cam kết 3 tháng).
- **Thời gian chờ (ngày)** — Số ngày tiếp cận sau khi thanh toán thất bại trước khi đăng ký bị tạm dừng. Đặt thành `0` để dừng ngay lập tức.
- **Thời gian tái kích hoạt (ngày)** — Số ngày sau khi hủy trong đó khách hàng có thể kích hoạt lại đăng ký mà không cần đăng ký lại từ đầu.

## Hành vi thay đổi gói

Khi khách hàng nâng cấp hoặc hạ cấp giữa các gói, bạn có thể kiểm soát thời điểm thay đổi xảy ra:

- **Hành vi nâng cấp** — Đặt thành **Liền mạch** (tính phí theo tỷ lệ ngay) hoặc **Vào thời điểm gia hạn** (chuyển đổi vào ngày thanh toán tiếp theo).
- **Hành vi hạ cấp** — Đặt thành **Liền mạch** (áp dụng tiền tín dụng cho hóa đơn tiếp theo) hoặc **Vào thời điểm gia hạn** (chuyển đổi vào ngày thanh toán tiếp theo).

## Giới hạn và hạn chế

- **Số chu kỳ thanh toán tối đa** — Tổng số chu kỳ thanh toán trước khi đăng ký tự động kết thúc. Để trống để thanh toán lặp lại không giới hạn. Ích lợi cho các kế hoạch trả góp hoặc đăng ký có thời hạn.
- **Phí thiết lập** — Một khoản phí một lần được thu khi đăng ký được tạo lần đầu (ví dụ: phí hướng dẫn hoặc kích hoạt). Đặt thành `0.00` để không có phí thiết lập.

## Phụ kiện bổ sung cho gói

Phụ kiện là các tùy chọn bổ sung có thể được khách hàng gắn vào gói của họ. Thêm chúng vào phần **Phụ kiện bổ sung**:

- **Tên phụ kiện** — Tên được hiển thị cho khách hàng. Hỗ trợ dịch thuật.
- **Mô tả** — Phụ kiện cung cấp điều gì.
- **Giá** — Chi phí của phụ kiện.
- **Tần suất thanh toán** — Phụ kiện được tính **Theo chu kỳ thanh toán** (lặp lại) hoặc **Một lần** khi bắt đầu đăng ký.
- **Cho phép số lượng** — Bật để cho phép khách hàng mua nhiều đơn vị của phụ kiện.
- **Bắt buộc** — Chọn để bao gồm phụ kiện này trên tất cả các đăng ký mới. Các phụ kiện bắt buộc không thể bị khách hàng xóa.

## Tính khả kiến và trạng thái

- **Đang hoạt động** — Bỏ chọn để vô hiệu hóa một gói để không có đăng ký mới nào được tạo. Các đăng ký hiện tại sẽ không bị ảnh hưởng.
- **Công khai** — Bỏ chọn để ẩn gói khỏi các trang dành cho khách hàng (dùng cho các gói nội bộ hoặc di sản mà người đăng ký hiện tại vẫn ở lại).
- **Thứ tự sắp xếp** — Kiểm soát thứ tự hiển thị trên các trang chọn đăng ký. Số nhỏ hơn xuất hiện trước.

## Lời khuyên

- Sử dụng **thời gian dùng thử** để giảm sự do dự — ngay cả một thời gian dùng thử miễn phí 7 ngày ngắn gọn cũng có thể cải thiện đáng kể tỷ lệ chuyển đổi trên các sản phẩm đăng ký.
- Thiết lập **ba cấp độ giá** (hàng tháng, hàng quý, hàng năm) với các khoản giảm giá tăng dần để khuyến khích cam kết hàng năm và cải thiện dòng tiền của bạn.
- Đối với các đăng ký dịch vụ, đặt **Chính sách hủy** thành **Hủy vào cuối kỳ** để khách hàng giữ quyền truy cập trong suốt kỳ thanh toán của họ — điều này sẽ cảm thấy công bằng và giảm thiểu các cuộc tranh chấp.
- Giữ **Thời gian chờ** ở mức 3–7 ngày cho các sự cố thanh toán. Điều này cho khách hàng thời gian để cập nhật phương thức thanh toán của họ trước khi mất quyền truy cập.
- Sử dụng cờ **Bắt buộc** trên các phụ kiện một cách hợp lý — chỉ sử dụng cho những thứ thực sự bắt buộc (ví dụ: thỏa thuận dịch vụ), không phải là cách để tăng giá.
- Vô hiệu hóa các gói không có người đăng ký thay vì xóa chúng — điều này giữ nguyên dữ liệu lịch sử cho bất kỳ khách hàng nào từng đăng ký nào.

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật.