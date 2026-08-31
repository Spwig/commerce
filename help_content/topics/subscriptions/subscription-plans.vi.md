---
title: Gói đăng ký
---

Gói đăng ký cho phép bạn cung cấp thanh toán định kỳ cho sản phẩm của mình — lý tưởng cho hàng tiêu dùng, dịch vụ, hộp quà tặng chọn lọc, hoặc bất kỳ sản phẩm nào mà khách hàng mua đi mua lại. Hướng dẫn này giải thích cách tạo và cấu hình các gói, thiết lập các mức giá, thêm thời gian dùng thử và gắn các tiện ích bổ sung tùy chọn.

## Bắt đầu

Điều hướng đến **Subscriptions > Subscription Plans** trong thanh bên quản trị. Danh sách các gói hiển thị tất cả các gói của bạn cùng với mô hình định giá, số lượng người đăng ký hoạt động và trạng thái hiển thị.

![Danh sách các gói đăng ký](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Để tạo một gói mới, nhấp vào nút **Create with Wizard** — điều này sẽ mở trình hướng dẫn tạo gói, giúp bạn thực hiện các bước thiết lập lần lượt. Nút **+ Add Plan** bên cạnh mở một biểu mẫu trống dành cho các nhà bán hàng muốn tự cấu hình mọi thứ thay vì sử dụng trình hướng dẫn.

Một gói đơn lẻ không thể mua được — nó là một mẫu. Sau khi bạn đã xây dựng nó ở đây, hãy gắn nó vào một hoặc nhiều sản phẩm từ tab **Subscriptions** của sản phẩm (chỉ dành cho sản phẩm Simple, Variable và Digital) để khách hàng thực sự có thể đăng ký. Xem [Selling Products as Subscriptions](/help/selling-products-as-subscriptions) cho bước đó.

## Trình chỉnh sửa gói

Mở một gói hiện có (nhấp vào tên của nó, hoặc biểu tượng bút chì, từ danh sách) sẽ đưa bạn đến trình chỉnh sửa gói. Phần tiêu đề hiển thị tên gói, mô hình định giá, các huy hiệu trạng thái **Active**/**Inactive** và **Public**/**Private**, cùng với ngày tạo. Hai nút ở góc trên bên phải của phần tiêu đề lưu các thay đổi của bạn — biểu tượng vòng tròn có dấu kiểm lưu và quay lại danh sách, biểu tượng kiểm đơn giản lưu và giữ bạn ở trên trang để tiếp tục chỉnh sửa.

Bên dưới phần tiêu đề, một dải thống kê tóm tắt gói một cách khái quát: **Active Subscriptions**, **Pricing Tiers**, **Add-ons** và **Total Revenue**.

Phần còn lại của biểu mẫu được tổ chức thành năm tab:

| Tab | Nội dung chứa |
|-----|-------------------|
| **General** | Thông tin gói (tên, slug, mô tả) và Trạng thái (hoạt động/công khai) |
| **Pricing** | Cấu hình định giá, Thời gian dùng thử và Giới hạn & Hạn chế |
| **Tiers & Add-ons** | Trình chỉnh sửa các Mức giá và Tiện ích bổ sung |
| **Lifecycle** | Chính sách hủy và Hành vi thay đổi gói |
| **Advanced** | Tích hợp nhà cung cấp và Thống kê |

Các phần bên dưới sẽ hướng dẫn qua cài đặt của từng tab. Khi bạn tạo một gói hoàn toàn mới trực tiếp từ **+ Add Plan** (thay vì trình hướng dẫn), các trường tương tự sẽ xuất hiện trong một biểu mẫu cuộn duy nhất thay vì các tab — hãy lưu gói một lần và mở lại nó để có trình chỉnh sửa đầy đủ với các tab.

## Thông tin gói (Tab General)

Thẻ **Plan Information** nắm bắt danh tính cốt lõi của gói của bạn.

- **Plan Name** — Tên mà khách hàng thấy khi đăng ký. Nhấp vào biểu tượng quả địa cầu để thêm bản dịch cho các ngôn ngữ cửa hàng khác.
- **Slug** — Một định danh thân thiện với URL được tạo tự động từ tên (ví dụ: `premium-plan`). Điều này được sử dụng nội bộ và trong các tích hợp.
- **Description** — Văn bản tùy chọn mô tả những gì gói bao gồm. Hỗ trợ bản dịch.

Thẻ **Status** trên cùng một tab kiểm soát các công tắc **Active** và **Public** — xem [Visibility and status](#visibility-and-status) bên dưới.

![Tab General của trình chỉnh sửa gói](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Mô hình định giá (Tab Pricing)

Thẻ **Pricing Configuration** kiểm soát cách cấu trúc định giá cho gói này:

| Mô hình định giá | Phù hợp nhất cho |
|---------------|----------|
| **Tiered Pricing** | Cung cấp các tùy chọn cam kết hàng tháng, hàng quý và hàng năm với chiết khấu cho các kỳ hạn dài hơn |
| **Quantity-Based** | Định giá theo chỗ hoặc theo người dùng, trong đó tổng số tiền tăng theo số lượng (ví dụ: giấy phép nhóm) |
| **Flat Rate** | Một giá cố định duy nhất không có biến thể |

Đối với các gói **Quantity-Based**, hãy đánh dấu **Allow Quantity** và đặt **Minimum Quantity** (số chỗ tối thiểu yêu cầu) và tùy chọn **Maximum Quantity** để giới hạn số chỗ mà người đăng ký có thể mua.

[![](https://d35f7a71u2y0ne.cloudfront.net/9/20230823103452/subscription-plans-edit-form-pricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Các cấp độ giá (Thẻ Cấp độ & Phụ kiện)

Các cấp độ giá xác định tần suất thanh toán và tùy chọn giảm giá mà khách hàng có được trên kế hoạch này. Thêm chúng vào thẻ **Cấp độ giá** trên tab **Cấp độ & Phụ kiện**, bên cạnh trình soạn thảo Phụ kiện.

Mỗi cấp độ có các trường sau:

- **Tên cấp độ** — Nhãn được hiển thị cho khách hàng (ví dụ: `Hàng tháng`, `Hàng năm — Tiết kiệm 20%`). Hỗ trợ dịch thuật.
- **Chu kỳ thanh toán** — Tần suất mà khách hàng bị tính phí: Hàng ngày, Hàng tuần, Hàng tháng, Hàng quý, Nửa năm, hoặc Hàng năm.
- **Khoảng cách thanh toán** — Hệ số nhân cho chu kỳ thanh toán. Đặt thành `2` với Hàng tháng để tính phí mỗi 2 tháng.
- **Phần trăm giảm giá** — Mức giảm giá được áp dụng cho giá sản phẩm cho cấp độ này. Đặt thành `0` để giá đầy đủ, hoặc `20` để giảm 20%. Giảm giá này được cộng dồn với bất kỳ giá bán nào trên chính sản phẩm.
- **Cấp độ mặc định** — Đánh dấu một cấp độ là mặc định để chọn trước cho khách hàng khi họ xem các tùy chọn đăng ký.

Giảm giá được áp dụng bắt đầu từ chu kỳ thanh toán đầu tiên của khách hàng, không chỉ ở các lần gia hạn — một cấp độ có giảm giá 20% sẽ tính 20% giảm ngay từ ngày đầu tiên (hoặc từ lần thanh toán đầu tiên sau khi thử, nếu kế hoạch có một).

### Ví dụ: Kế hoạch cấp độ với ba tùy chọn

Với kế hoạch đăng ký "Câu lạc bộ Cà phê":

| Tên cấp độ | Chu kỳ thanh toán | Giảm giá |
|-----------|-------------------|----------|
| Hàng tháng | Hàng tháng | 0% |
| Hàng quý — Tiết kiệm 10% | Hàng quý | 10% |
| Hàng năm — Tiết kiệm 20% | Hàng năm | 20% |

## Phụ kiện cho kế hoạch (Thẻ Cấp độ & Phụ kiện)

Phụ kiện là các tùy chọn bổ sung có thể thêm vào kế hoạch của người đăng ký. Thêm chúng vào thẻ **Phụ kiện**, ngay dưới Cấp độ giá trên cùng một tab:

- **Tên phụ kiện** — Tên được hiển thị cho khách hàng. Hỗ trợ dịch thuật.
- **Mô tả** — Những gì phụ kiện cung cấp.
- **Giá** — Chi phí của phụ kiện.
- **Tần suất thanh toán** — Phụ kiện được tính phí **Theo chu kỳ thanh toán** (lặp lại) hoặc **Một lần** khi bắt đầu đăng ký.
- **Cho phép số lượng** — Bật để cho phép khách hàng mua nhiều đơn vị của phụ kiện.
- **Bắt buộc** — Chọn để bao gồm phụ kiện này trên tất cả các đăng ký mới. Các phụ kiện bắt buộc không thể bị xóa bởi khách hàng.

[![](https://d35f7a71u2y0ne.cloudfront.net/9/20230823103452/subscription-plans-edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Thời gian dùng thử (Thẻ Giá)

Thời gian dùng thử cho phép khách hàng thử nghiệm đăng ký của bạn trước khi thanh toán đầu tiên. Cài đặt điều này trong thẻ **Thời gian dùng thử**, dưới Cấu hình Giá:

- **Thời gian dùng thử (ngày)** — Số ngày dùng thử miễn phí. Đặt thành `0` để vô hiệu hóa dùng thử. Giới hạn tối đa là 365 ngày.
- **Giá dùng thử** — Giá giảm tùy chọn trong thời gian dùng thử (ví dụ: $1 cho tháng đầu tiên). Để trống để dùng thử hoàn toàn miễn phí.

## Giới hạn và hạn chế (Thẻ Giá)

Thẻ **Giới hạn & Hạn chế**, cũng trên Thẻ Giá, chứa:

- **Số chu kỳ thanh toán tối đa** — Tổng số chu kỳ thanh toán trước khi đăng ký tự động kết thúc. Để trống để không giới hạn thanh toán lặp lại. Ích lợi cho các kế hoạch trả góp hoặc đăng ký có thời hạn.

**Phí thiết lập** và **Thứ tự sắp xếp** không phải là một phần của thẻ này — chúng được thiết lập một lần, khi bạn tạo kế hoạch lần đầu thông qua quy trình **Tạo bằng Wizard**, và không thể thay đổi từ màn hình chỉnh sửa sau đó. Nếu bạn cần điều chỉnh bất kỳ giá trị nào, hãy vô hiệu hóa kế hoạch và tạo lại bằng wizard thay vì chỉnh sửa kế hoạch hiện có. Lưu ý rằng phí thiết lập không được tính tự động tại thời điểm thanh toán trong phiên bản này — xem trường này là dành cho cập nhật tương lai thay vì một khoản phí hoạt động.

## Chính sách hủy bỏ (Thẻ Chu kỳ)

Kiểm soát cách khách hàng có thể hủy bỏ đăng ký của họ trong thẻ **Chính sách hủy bỏ**:

| Chính sách | Mô tả |
|--------|-------------|
| **Hủy bất kỳ lúc nào** | Khách hàng có thể hủy ngay lập tức vào bất kỳ thời điểm nào |
| **Hủy vào cuối kỳ** | Việc hủy có hiệu lực vào cuối kỳ thanh toán — khách hàng giữ quyền truy cập cho đến khi hết hạn |
| **Yêu cầu cam kết tối thiểu** | Khách hàng phải hoàn tất một số chu kỳ thanh toán tối thiểu trước khi hủy |

Các cài đặt bổ sung:

- **Cam kết tối thiểu (chu kỳ)** — Khi sử dụng chính sách cam kết, hãy đặt số chu kỳ thanh toán tối thiểu (ví dụ: `3` cho cam kết 3 tháng).
- **Thời gian chờ (ngày)** — Số ngày truy cập tiếp tục sau khi thanh toán thất bại trước khi đăng ký bị tạm dừng. Đặt thành `0` để tạm dừng ngay lập tức.
- **Thời gian tái kích hoạt (ngày)** — Số ngày sau khi hủy trong đó khách hàng có thể kích hoạt lại đăng ký của họ mà không cần đăng ký lại từ đầu.

## Hành vi thay đổi gói (Thẻ Cuộc sống)

Thẻ **Hành vi thay đổi gói**, bên dưới Chính sách Hủy bỏ, kiểm soát điều gì xảy ra khi khách hàng nâng cấp hoặc hạ cấp giữa các gói:

- **Hành vi nâng cấp** — Đặt thành **Ngay lập tức** (tính phí theo tỷ lệ ngay) hoặc **Vào thời điểm gia hạn** (chuyển đổi vào ngày thanh toán tiếp theo).
- **Hành vi hạ cấp** — Đặt thành **Ngay lập tức** (áp dụng tín dụng cho hóa đơn tiếp theo) hoặc **Vào thời điểm gia hạn** (chuyển đổi vào ngày thanh toán tiếp theo).

![Thẻ Cuộc sống của trình chỉnh sửa gói](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## Thẻ Nâng cao

Thẻ **Nâng cao** chứa các cài đặt bạn sẽ hiếm khi cần đến mỗi ngày:

- **Tích hợp nhà cung cấp** — Gán gói này với các ID gói/định giá từ các nhà cung cấp thanh toán của bạn (ví dụ: `"stripe": "price_xxx", "paypal": "P-xxx"`), dành cho các cửa hàng quản lý đăng ký trực tiếp thông qua nhà cung cấp thay vì động cơ thanh toán của Spwig.
- **Thống kê** — Các con số đọc-only: **Đăng ký đang hoạt động**, **Doanh thu tổng cộng**, và các mốc thời gian **Được tạo lúc** / **Cập nhật lúc** của gói. Những con số này phản ánh các chỉ số ở đầu trang.

![Thẻ Nâng cao của trình chỉnh sửa gói](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## Tính khả kiến và trạng thái (Thẻ Tổng quan)

- **Đang hoạt động** — Bỏ chọn để vô hiệu hóa một gói để không có đăng ký mới nào được tạo. Các đăng ký hiện tại sẽ không bị ảnh hưởng.
- **Công khai** — Bỏ chọn để ẩn gói khỏi các trang dành cho khách hàng (rất hữu ích cho các gói nội bộ hoặc cũ kỹ mà người đăng ký hiện tại vẫn ở trên).

## Mẹo

- Sử dụng **thời gian dùng thử** để giảm bớt sự do dự — ngay cả một thời gian dùng thử miễn phí 7 ngày ngắn gọn cũng có thể cải thiện đáng kể tỷ lệ chuyển đổi trên sản phẩm đăng ký.
- Thiết lập **ba cấp độ giá** (hàng tháng, hàng quý, hàng năm) với các khoản giảm giá tăng dần để khuyến khích cam kết hàng năm và cải thiện dòng tiền của bạn.
- Đối với các đăng ký dịch vụ, đặt **Chính sách Hủy bỏ** thành **Hủy vào cuối kỳ** để khách hàng giữ quyền truy cập trong suốt kỳ thanh toán của họ — điều này sẽ cảm thấy công bằng và giảm thiểu các cuộc tranh chấp.
- Giữ **Thời gian chờ** ở mức 3–7 ngày cho các sự cố thanh toán. Điều này cho khách hàng thời gian để cập nhật phương thức thanh toán của họ trước khi mất quyền truy cập.
- Sử dụng cờ **Bắt buộc** trên các tùy chọn bổ sung một cách có chọn lọc — chỉ sử dụng nó cho những thứ thực sự bắt buộc (ví dụ: một thỏa thuận dịch vụ), chứ không phải là cách để tăng giá.
- Vô hiệu hóa các gói không có người đăng ký thay vì xóa chúng — điều này giữ nguyên dữ liệu lịch sử cho bất kỳ khách hàng nào từng đăng ký trước đó.