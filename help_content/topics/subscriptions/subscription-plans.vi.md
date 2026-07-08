---
title: Kế hoạch đăng ký
---

Các kế hoạch đăng ký cho phép bạn cung cấp thanh toán định kỳ cho sản phẩm của mình — lý tưởng cho các sản phẩm tiêu hao, dịch vụ, hộp quà được lựa chọn kỹ lưỡng hoặc bất kỳ sản phẩm nào mà khách hàng mua lặp lại. Hướng dẫn này giải thích cách tạo và cấu hình các kế hoạch, thiết lập các cấp giá, thêm giai đoạn dùng thử và gắn các tùy chọn bổ sung (add-ons) không bắt buộc.

## Bắt đầu

Truy cập **Subscriptions > Subscription Plans** trong thanh bên quản trị. Danh sách kế hoạch hiển thị tất cả các kế hoạch của bạn với mô hình định giá, số lượng người đăng ký đang hoạt động và trạng thái hiển thị.

Để tạo kế hoạch mới, nhấp vào nút **+ Add Subscription Plan** — điều này sẽ mở ra trình hướng dẫn tạo kế hoạch, hướng dẫn bạn từng bước thiết lập.

![Danh sách kế hoạch đăng ký](/static/core/admin/img/help/subscription-plans/plan-list.webp)

## Thông tin kế hoạch

Phần đầu tiên thu thập bản sắc cốt lõi của kế hoạch của bạn.

- **Tên kế hoạch** — Tên khách hàng nhìn thấy khi đăng ký. Nhấp vào biểu tượng quả địa cầu để thêm bản dịch cho các ngôn ngữ cửa hàng khác.
- **Slug** — Một định danh thân thiện với URL được tạo tự động từ tên (ví dụ: `premium-plan`). Điều này được sử dụng bên trong và trong các tích hợp.
- **Mô tả** — Văn bản tùy chọn mô tả những gì kế hoạch bao gồm. Hỗ trợ bản dịch.

## Mô hình định giá

Chọn cách cấu trúc định giá cho kế hoạch này:

| Mô hình định giá | Phù hợp nhất với |
|------------------|------------------|
| **Định giá theo cấp** | Cung cấp các tùy chọn cam kết hàng tháng, quý và hàng năm với giảm giá cho các kỳ dài hơn |
| **Theo số lượng** | Định giá theo chỗ ngồi hoặc người dùng, tổng số tăng theo số lượng (ví dụ: giấy phép nhóm) |
| **Giá cố định** | Một giá cố định duy nhất không có sự thay đổi |

Đối với các kế hoạch **Theo số lượng**, hãy đặt **Số lượng tối thiểu** (số chỗ ngồi tối thiểu cần thiết) và tùy chọn **Số lượng tối đa** để giới hạn số chỗ ngồi mà người đăng ký có thể mua.

## Cấp giá

Các cấp giá xác định tần suất thanh toán và các tùy chọn giảm giá có sẵn cho khách hàng trên kế hoạch này. Thêm chúng vào phần **Pricing Tiers** bên dưới biểu mẫu chính.

Mỗi cấp có các trường sau:

- **Tên cấp** — Nhãn hiển thị cho khách hàng (ví dụ: `Monthly`, `Annual — Save 20%`). Hỗ trợ bản dịch.
- **Chu kỳ thanh toán** — Tần suất khách hàng được tính phí: Hàng ngày, Hàng tuần, Hàng tháng, Quý, Nửa năm hoặc Hàng năm.
- **Khoảng thời gian thanh toán** — Hệ số nhân cho chu kỳ thanh toán. Đặt thành `2` với Monthly để tính phí mỗi 2 tháng.
- **Tỷ lệ giảm giá** — Tỷ lệ giảm giá được áp dụng cho giá sản phẩm cho cấp này. Đặt thành `0` để tính giá đầy đủ, hoặc `20` để giảm 20%. Tỷ lệ giảm này được cộng dồn trên bất kỳ giá bán nào của sản phẩm.
- **Cấp mặc định** — Đánh dấu một cấp là mặc định để tự động chọn nó cho khách hàng khi họ xem các tùy chọn đăng ký.

### Ví dụ: kế hoạch theo cấp với ba tùy chọn

Đối với kế hoạch đăng ký "Coffee Club":

| Tên cấp | Chu kỳ thanh toán | Giảm giá |
|----------|------------------|----------|
| Monthly | Monthly | 0% |
| Quarterly — Save 10% | Quarterly | 10% |
| Annual — Save 20% | Annual | 20% |

## Giai đoạn dùng thử

Giai đoạn dùng thử cho phép khách hàng thử đăng ký của bạn trước khi thanh toán lần đầu. Cấu hình điều này trong phần **Trial Period**:

- **Trial Period (Days)** — Số ngày dùng thử miễn phí. Đặt thành `0` để tắt dùng thử. Tối đa là 365 ngày.
- **Trial Price** — Giá giảm tùy chọn trong giai đoạn dùng thử (ví dụ: $1 cho tháng đầu tiên). Để trống để có giai đoạn dùng thử hoàn toàn miễn phí.

## Chính sách hủy

Kiểm soát cách khách hàng có thể hủy đăng ký của họ trong phần **Cancellation Policy**:

| Chính sách | Mô tả |
|------------|--------|
| **Cancel Anytime** | Khách hàng có thể hủy ngay lập tức bất kỳ lúc nào |
| **Cancel at Period End** | Hủy sẽ có hiệu lực vào cuối giai đoạn đã thanh toán — khách hàng vẫn giữ quyền truy cập cho đến hết hạn |
| **Minimum Commitment Required** | Khách hàng phải hoàn thành một số lượng tối thiểu các chu kỳ thanh toán trước khi hủy |

Cài đặt bổ sung:

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- **Cam kết tối thiểu (chu kỳ)** — Khi sử dụng chính sách cam kết, hãy đặt số chu kỳ thanh toán bắt buộc (ví dụ, `3` cho cam kết tối thiểu 3 tháng).
- **Thời gian ân hạn (ngày)** — Số ngày tiếp tục truy cập sau khi thanh toán thất bại trước khi đăng ký bị tạm dừng.

Đặt thành `0` để tạm dừng ngay lập tức.
- **Thời gian kích hoạt lại (ngày)** — Số ngày sau khi hủy đăng ký trong đó khách hàng có thể kích hoạt lại đăng ký mà không cần đăng ký lại từ đầu.

## Hành vi thay đổi gói

Khi khách hàng nâng cấp hoặc hạ cấp giữa các gói, bạn có thể kiểm soát thời điểm thay đổi có hiệu lực:

- **Hành vi nâng cấp** — Chọn **Ngay lập tức** (thanh toán số tiền được tính theo tỷ lệ ngay bây giờ) hoặc **Tại thời điểm gia hạn** (chuyển đổi tại ngày thanh toán tiếp theo).
- **Hành vi hạ cấp** — Chọn **Ngay lập tức** (áp dụng số tiền hoàn lại cho hóa đơn tiếp theo) hoặc **Tại thời điểm gia hạn** (chuyển đổi tại ngày thanh toán tiếp theo).

## Giới hạn và hạn chế

- **Số chu kỳ thanh toán tối đa** — Tổng số chu kỳ thanh toán trước khi đăng ký tự động kết thúc. Để trống để có thanh toán định kỳ không giới hạn. Hữu ích cho các gói trả góp hoặc đăng ký có thời hạn.
- **Phí thiết lập** — Một khoản phí một lần được thu khi đăng ký được tạo lần đầu (ví dụ, phí thiết lập hoặc phí kích hoạt). Đặt thành `0.00` nếu không có phí thiết lập.

## Các tùy chọn bổ sung cho gói

Các tùy chọn bổ sung là các tiện ích bổ sung tùy chọn mà người đăng ký có thể thêm vào gói của họ. Thêm chúng vào phần **Tùy chọn bổ sung cho gói**:

- **Tên tùy chọn bổ sung** — Tên hiển thị cho khách hàng. Hỗ trợ dịch thuật.
- **Mô tả** — Tùy chọn bổ sung cung cấp gì.
- **Giá** — Chi phí của tùy chọn bổ sung.
- **Tần suất thanh toán** — Xác định tùy chọn bổ sung được tính **Theo chu kỳ thanh toán** (lặp lại) hoặc **Một lần** tại thời điểm bắt đầu đăng ký.
- **Cho phép số lượng** — Kích hoạt để cho phép khách hàng mua nhiều đơn vị của tùy chọn bổ sung.
- **Bắt buộc** — Chọn để tự động thêm tùy chọn bổ sung vào tất cả các đăng ký mới. Các tùy chọn bổ sung bắt buộc không thể bị khách hàng xóa.

## Tính năng hiển thị và trạng thái

- **Hoạt động** — Tắt để ngừng kích hoạt gói, không có đăng ký mới nào có thể được tạo. Các đăng ký hiện tại không bị ảnh hưởng.
- **Công khai** — Tắt để ẩn gói khỏi các trang dành cho khách hàng (hữu ích cho các gói nội bộ hoặc cũ mà các khách hàng hiện tại vẫn đang sử dụng).
- **Thứ tự hiển thị** — Điều khiển thứ tự hiển thị trên các trang chọn đăng ký. Số nhỏ hơn sẽ hiển thị trước.

## Một số mẹo

- Sử dụng **giai đoạn dùng thử** để giảm bớt sự do dự — ngay cả một giai đoạn dùng thử ngắn 7 ngày cũng có thể cải thiện đáng kể tỷ lệ chuyển đổi cho sản phẩm đăng ký.
- Thiết lập **ba cấp giá** (tháng, quý, năm) với mức giảm giá tăng dần để khuyến khích cam kết hàng năm và cải thiện dòng tiền của bạn.
- Đối với các đăng ký dựa trên dịch vụ, hãy đặt **Chính sách hủy** thành **Hủy tại cuối kỳ** để khách hàng vẫn giữ quyền truy cập trong thời gian đã thanh toán — điều này cảm thấy công bằng và giảm thiểu việc hoàn tiền.
- Giữ **thời gian ân hạn** ở mức 3–7 ngày cho các lần thanh toán thất bại. Điều này cho phép khách hàng thời gian để cập nhật phương thức thanh toán trước khi mất quyền truy cập.
- Sử dụng cờ **Bắt buộc** trên các tùy chọn bổ sung một cách tiết kiệm — chỉ sử dụng nó cho những thứ thực sự bắt buộc (ví dụ, một thỏa thuận dịch vụ), chứ không phải là cách để tăng giá.
- Tắt các gói không còn có người đăng ký thay vì xóa chúng — điều này giữ lại dữ liệu lịch sử cho bất kỳ khách hàng nào từng đăng ký trước đây.