---
title: Các Gói Đăng Ký
---

Các gói đăng ký cho phép bạn cung cấp thanh toán định kỳ cho sản phẩm của bạn — lý tưởng cho hàng tiêu dùng, dịch vụ, hộp được tuyển chọn, hoặc bất kỳ sản phẩm nào mà khách hàng mua lặp lại. Hướng dẫn này giải thích cách tạo và cấu hình các gói, thiết lập các cấp độ giá, thêm thời gian dùng thử, và gắn các tùy chọn bổ sung tùy chọn.

## Bắt đầu

Đi đến **Phân khúc > Các gói đăng ký** trong thanh điều hướng quản trị. Danh sách gói hiển thị tất cả các gói của bạn với mô hình giá, số lượng người đăng ký đang hoạt động, và trạng thái hiển thị.

![Danh sách các gói đăng ký](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Để tạo một gói mới, nhấn nút **Tạo bằng Trình hướng dẫn** — điều này mở trình hướng dẫn tạo gói, giúp bạn thiết lập từng bước một. Nút **+ Thêm Gói** bên cạnh nó mở ra một biểu mẫu trống cho các chủ cửa hàng muốn cấu hình mọi thứ bằng tay thay vì sử dụng trình hướng dẫn.

Một gói riêng lẻ không thể mua được — đó là một mẫu. Một khi bạn đã xây dựng nó ở đây, hãy gắn nó với một hoặc nhiều sản phẩm từ tab **Đăng ký** của sản phẩm (chỉ dành cho sản phẩm Đơn giản, Biến đổi và Số hóa) để khách hàng thực sự có thể đăng ký. Xem [Bán Sản phẩm dưới dạng Đăng ký](/help/selling-products-as-subscriptions) cho bước đó.

## Trình chỉnh sửa gói

Mở một gói hiện có (nhấn vào tên của nó, hoặc biểu tượng bút chì, từ danh sách) sẽ đưa bạn đến trình chỉnh sửa gói. Phần đầu hiển thị tên gói, mô hình giá, các thẻ trạng thái **Đang hoạt động**/**Không hoạt động** và **Công khai**/**Riêng tư**, cũng như ngày tháng được tạo. Hai nút ở góc trên bên phải của phần đầu lưu trữ thay đổi của bạn — biểu tượng đồng hồ kiểm tra lưu trữ và quay lại danh sách, biểu tượng đồng hồ kiểm tra đơn giản lưu trữ và giữ bạn trên trang để tiếp tục chỉnh sửa.

Dưới phần đầu, một dải thống kê tóm tắt gói một cách nhanh chóng: **Đăng ký Đang hoạt động**, **Cấp độ Giá**, **Tùy chọn bổ sung**, và **Doanh thu Tổng cộng**.

Phần còn lại của biểu mẫu được tổ chức thành năm tab:

| Tab | Những gì nó chứa |
|-----|-------------------|
| **Tổng quan** | Thông tin Gói (tên, slug, mô tả) và Trạng thái (hoạt động/công khai) |
| **Giá** | Cấu hình Giá, Thời gian Thử nghiệm, và Giới hạn & Hạn chế |
| **Cấp độ & Tùy chọn bổ sung** | Người chỉnh sửa Cấp độ Giá và Tùy chọn bổ sung |
| **Quy trình** | Chính sách Hủy bỏ và Hành vi Thay đổi Gói |
| **Nâng cao** | Tích hợp Nhà cung cấp và Thống kê |

Các phần dưới đây đi dọc theo các cài đặt của từng tab. Khi bạn tạo một gói mới trực tiếp từ **+ Thêm Gói** (thay vì trình hướng dẫn), các trường giống nhau xuất hiện trong một biểu mẫu cuộn duy nhất thay vì các tab — lưu gói một lần và mở lại để có trình chỉnh sửa có tab đầy đủ.

## Thông tin gói (Tab Tổng quan)

Thẻ **Thông tin Gói** ghi nhận bản chất cốt lõi của gói của bạn.

- **Tên Gói** — Tên mà khách hàng nhìn thấy khi đăng ký. Nhấn vào biểu tượng hành tinh để thêm bản dịch cho các ngôn ngữ cửa hàng khác.
- **Slug** — Một định danh URL được tạo tự động từ tên (ví dụ: `premium-plan`). Điều này được sử dụng bên trong và trong các tích hợp.
- **Mô tả** — Văn bản tùy chọn mô tả những gì gói bao gồm. Hỗ trợ dịch thuật.

Thẻ **Trạng thái** trên cùng một tab kiểm soát các nút **Đang hoạt động** và **Công khai** — xem [Hiển thị và Trạng thái](#visibility-and-status) bên dưới.

![Tab Tổng quan của trình chỉnh sửa gói](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Mô hình Giá (Tab Giá)

Thẻ **Cấu hình Giá** kiểm soát cách cấu trúc giá cho gói này:

| Mô hình Giá | Tốt nhất cho |
|---------------|----------|
| **Giá theo cấp độ** | Cung cấp các tùy chọn cam kết hàng tháng, hàng quý và hàng năm với chiết khấu cho các khoản thời gian dài hơn |
| **Dựa trên Số lượng** | Giá theo người dùng hoặc người dùng, nơi tổng cộng thay đổi theo số lượng (ví dụ: giấy phép nhóm) |
| **Cố định** | Một mức giá cố định duy nhất mà không có sự thay đổi |

Đối với các gói **Dựa trên Số lượng**, hãy kiểm tra **Cho phép Số lượng** và đặt **Số lượng Tối thiểu** (số ghế tối thiểu được yêu cầu) và tùy chọn **Số lượng Tối đa** để giới hạn số ghế mà người đăng ký có thể mua.

[![](https://d35f7a71u2y0ne.cloudfront.net/9d4d611f-5f8c-46c0-9f7c-5a0f5c6d6d6d/subscription-plans/edit-form-pricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Các cấp độ giá (Thẻ Cấp độ & Phụ kiện)

Các cấp độ giá xác định tần suất thanh toán và các tùy chọn giảm giá có sẵn cho khách hàng trên kế hoạch này. Thêm chúng vào thẻ **Cấp độ giá** trên tab **Cấp độ & Phụ kiện**, bên cạnh trình soạn thảo Phụ kiện.

Mỗi cấp độ có các trường sau:

- **Tên cấp độ** — Nhãn được hiển thị cho khách hàng (ví dụ: `Hàng tháng`, `Hàng năm — Tiết kiệm 20%`). Hỗ trợ dịch thuật.
- **Chu kỳ thanh toán** — Tần suất mà khách hàng bị tính phí: Hàng ngày, Hàng tuần, Hàng tháng, Hàng quý, Nửa năm, hoặc Hàng năm.
- **Khoảng cách thanh toán** — Hệ số nhân cho chu kỳ thanh toán. Thiết lập thành `2` với Hàng tháng để tính phí mỗi 2 tháng.
- **Phần trăm giảm giá** — Mức giảm giá được áp dụng cho giá sản phẩm cho cấp độ này. Thiết lập thành `0` để giá đầy đủ, hoặc `20` để giảm 20%. Giảm giá này được cộng dồn với bất kỳ giá bán nào trên chính sản phẩm.
- **Cấp độ mặc định** — Đánh dấu một cấp độ là mặc định để chọn trước cho khách hàng khi họ xem các tùy chọn đăng ký.

Giảm giá được áp dụng bắt đầu từ chu kỳ thanh toán đầu tiên của khách hàng, không chỉ ở các lần gia hạn — một cấp độ có giảm giá 20% sẽ tính 20% giảm giá từ ngày đầu tiên (hoặc từ lần thanh toán đầu tiên sau khi thử, nếu kế hoạch có một).

### Ví dụ: Kế hoạch phân cấp với ba tùy chọn

Với kế hoạch đăng ký "Câu lạc bộ Cà phê":

| Tên cấp độ | Chu kỳ thanh toán | Giảm giá |
|-----------|-------------------|----------|
| Hàng tháng | Hàng tháng | 0% |
| Hàng quý — Tiết kiệm 10% | Hàng quý | 10% |
| Hàng năm — Tiết kiệm 20% | Hàng năm | 20% |

## Phụ kiện cho kế hoạch (Thẻ Cấp độ & Phụ kiện)

Phụ kiện là các tùy chọn bổ sung có thể chọn cho kế hoạch đăng ký. Thêm chúng vào thẻ **Phụ kiện**, ngay dưới Cấp độ giá trên cùng một tab:

- **Tên phụ kiện** — Tên được hiển thị cho khách hàng. Hỗ trợ dịch thuật.
- **Mô tả** — Những gì phụ kiện cung cấp.
- **Giá** — Chi phí của phụ kiện.
- **Tần suất thanh toán** — Phụ kiện được tính **Mỗi chu kỳ thanh toán** (lặp lại) hoặc **Một lần** khi bắt đầu đăng ký.
- **Cho phép số lượng** — Bật để cho phép khách hàng mua nhiều đơn vị của phụ kiện.
- **Bắt buộc** — Chọn để bao gồm phụ kiện này trên tất cả các đăng ký mới. Các phụ kiện bắt buộc không thể bị xóa bởi khách hàng.

[![](https://d35f7a71u2y0ne.cloudfront.net/9d4d611f-5f8c-46c0-9f7c-5a0f5c6d6d6d/subscription-plans/edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Thời gian dùng thử (Thẻ Giá)

Thời gian dùng thử cho phép khách hàng thử nghiệm đăng ký của bạn trước khi thanh toán đầu tiên. Cài đặt điều này trong thẻ **Thời gian dùng thử**, bên dưới Cấu hình Giá:

- **Thời gian dùng thử (Ngày)** — Số ngày dùng thử miễn phí. Thiết lập thành `0` để vô hiệu hóa dùng thử. Giới hạn tối đa là 365 ngày.
- **Giá dùng thử** — Giá giảm tùy chọn trong thời gian dùng thử (ví dụ: $1 cho tháng đầu tiên). Để trống để dùng thử hoàn toàn miễn phí.

## Giới hạn và hạn chế (Thẻ Giá)

Thẻ **Giới hạn & Hạn chế**, cũng trên Thẻ Giá, chứa:

- **Số chu kỳ thanh toán tối đa** — Tổng số chu kỳ thanh toán trước khi đăng ký tự động kết thúc. Để trống để không giới hạn thanh toán lặp lại. Ích lợi cho các kế hoạch trả góp hoặc đăng ký có thời hạn.

**Phí thiết lập** và **Thứ tự sắp xếp** không phải là một phần của thẻ này — chúng được thiết lập một lần, khi bạn tạo kế hoạch đầu tiên thông qua luồng **Tạo bằng Wizard**, và không thể thay đổi từ màn hình chỉnh sửa sau đó. Nếu bạn cần điều chỉnh giá trị nào, hãy vô hiệu hóa kế hoạch và tạo lại bằng wizard thay vì chỉnh sửa kế hoạch hiện tại. Lưu ý rằng phí thiết lập chưa được tính tự động tại thời điểm thanh toán trong phiên bản này — xem trường này là dành cho cập nhật tương lai thay vì một khoản phí hoạt động.

## Chính sách hủy bỏ (Thẻ Chu kỳ)

Kiểm soát cách khách hàng có thể hủy bỏ đăng ký của họ trong thẻ **Chính sách Hủy bỏ**:

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật.

| Chính sách | Mô tả |
|--------|-------------|
| **Hủy bất kỳ lúc nào** | Khách hàng có thể hủy ngay lập tức vào bất kỳ thời điểm nào |
| **Hủy vào cuối kỳ** | Việc hủy có hiệu lực vào cuối kỳ thanh toán — khách hàng giữ quyền truy cập cho đến khi hết hạn |
| **Yêu cầu cam kết tối thiểu** | Khách hàng phải hoàn tất một số chu kỳ thanh toán tối thiểu trước khi hủy |

Các cài đặt bổ sung:

- **Cam kết tối thiểu (chu kỳ)** — Khi sử dụng chính sách cam kết, hãy đặt số chu kỳ thanh toán tối thiểu (ví dụ: `3` cho cam kết 3 tháng).
- **Thời gian chờ (ngày)** — Số ngày truy cập tiếp tục sau khi thanh toán thất bại trước khi đăng ký bị tạm dừng. Đặt thành `0` để tạm dừng ngay lập tức.
- **Thời gian tái kích hoạt (ngày)** — Số ngày sau khi hủy mà khách hàng có thể kích hoạt lại đăng ký của họ mà không cần đăng ký lại từ đầu.

## Hành vi thay đổi gói (Thẻ Cuộc đời)

Thẻ **Hành vi thay đổi gói**, bên dưới Chính sách Hủy bỏ, kiểm soát điều gì xảy ra khi khách hàng nâng cấp hoặc hạ cấp giữa các gói:

- **Hành vi nâng cấp** — Đặt thành **Ngay lập tức** (tính phí theo tỷ lệ ngay) hoặc **Vào thời điểm gia hạn** (chuyển đổi vào ngày thanh toán tiếp theo).
- **Hành vi hạ cấp** — Đặt thành **Ngay lập tức** (áp dụng tín dụng cho hóa đơn tiếp theo) hoặc **Vào thời điểm gia hạn** (chuyển đổi vào ngày thanh toán tiếp theo).

![Thẻ Cuộc đời của trình chỉnh sửa gói](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

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
- Sử dụng cờ **Bắt buộc** trên các tùy chọn bổ sung một cách có chọn lọc — chỉ sử dụng cho những thứ thực sự bắt buộc (ví dụ: một thỏa thuận dịch vụ), chứ không phải là cách để tăng giá.
- Vô hiệu hóa các gói không có người đăng ký thay vì xóa chúng — điều này giữ nguyên dữ liệu lịch sử cho bất kỳ khách hàng nào từng đăng ký trước đó.