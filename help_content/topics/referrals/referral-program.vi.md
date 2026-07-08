---
title: Chương trình giới thiệu
---

Chương trình giới thiệu cho phép khách hàng hiện tại của bạn chia sẻ liên kết giới thiệu duy nhất của họ với bạn bè và gia đình. Khi một người bạn được giới thiệu thực hiện lần mua hàng đầu tiên đủ điều kiện, cả người giới thiệu và khách hàng mới đều có thể nhận được phần thưởng — thúc đẩy việc thu hút khách hàng mới thông qua lời giới thiệu.

## Cách chương trình giới thiệu hoạt động

1. Một khách hàng chia sẻ liên kết giới thiệu (hoặc mã) của họ với một người bạn.
2. Người bạn nhấp vào liên kết và được theo dõi thông qua cookie trong vòng 30 ngày (có thể cấu hình).
3. Người bạn đăng ký và đặt đơn hàng đầu tiên đủ điều kiện.
4. Hệ thống tạo bản ghi thuộc tính giới thiệu và thực hiện kiểm tra gian lận và tính đủ điều kiện.
5. Nếu thuộc tính được phê duyệt, phần thưởng sẽ được cấp cho cả hai bên.

Cửa hàng của bạn có một cấu hình chương trình giới thiệu duy nhất. Di chuyển đến **Marketing > Chương trình giới thiệu** để thiết lập.

## Thiết lập chương trình giới thiệu của bạn

### Trạng thái chương trình

Chương trình có ba trạng thái:

- **Draft** — Chương trình đang được cấu hình nhưng chưa được kích hoạt. Liên kết giới thiệu không hoạt động.
- **Active** — Chương trình đang hoạt động. Khách hàng có thể chia sẻ liên kết và nhận phần thưởng.
- **Paused** — Chương trình tạm dừng. Các thuộc tính hiện có vẫn được xử lý, nhưng không theo dõi các giới thiệu mới.

Đặt **Status** thành **Active** khi bạn sẵn sàng ra mắt. Bạn có thể tạm dừng nó bất kỳ lúc nào.

### Cấu hình phần thưởng

Định nghĩa các phần thưởng được cấp khi một giới thiệu chuyển đổi. Chương trình hỗ trợ **phần thưởng hai bên** — nghĩa là bạn có thể thưởng cả người giới thiệu (khách hàng chia sẻ liên kết) và người được giới thiệu (khách hàng mới sử dụng liên kết).

Cấu hình phần thưởng cho từng người nhận trong trường **Reward Configuration**. Các loại phần thưởng có sẵn là:

| Reward Kind | Description |
|-------------|-------------|
| **Store Credit** | Thêm tiền vào ví của khách hàng, có thể sử dụng cho các đơn hàng tương lai |
| **Coupon Code** | Tạo mã phiếu giảm giá duy nhất |
| **Percentage Discount** | Cấp phần trăm giảm giá để sử dụng tại thanh toán |
| **Exclusive Perk** | Một quyền lợi đặc biệt (ví dụ: món quà miễn phí, quyền truy cập ưu tiên) — được mô tả trong trường mô tả của phần thưởng |

**Ví dụ cấu hình** — 10 đô la tiền thưởng cho người giới thiệu và 10 đô la giảm giá cho khách hàng mới:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Đặt "double_sided": false nếu bạn chỉ muốn thưởng cho người giới thiệu.

### Quy tắc đủ điều kiện

Quy tắc đủ điều kiện xác định các giới thiệu nào đủ điều kiện nhận phần thưởng. Cấu hình chúng trong trường **Eligibility Rules**:

| Rule | What it does |
|------|--------------|
| `new_customer_only` | Nếu `true`, người bạn được giới thiệu phải là khách hàng mới hoàn toàn (không có đơn hàng trước đó) |
| `min_order_value` | Số tiền đơn hàng tối thiểu (theo loại tiền tệ của cửa hàng bạn) mà người bạn được giới thiệu phải chi tiêu |
| `exclude_discounts` | Nếu `true`, các đơn hàng mà khách hàng được giới thiệu sử dụng phiếu giảm giá sẽ không đủ điều kiện |
| `exclude_staff` | Nếu `true`, tài khoản nhân viên không thể là người giới thiệu hoặc người được giới thiệu |

**Ví dụ** — chỉ khách hàng mới, đơn hàng tối thiểu 40 đô la, loại trừ nhân viên:

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Cấu hình thời gian

Trường **Timing Configuration** kiểm soát thời điểm cấp phần thưởng sau khi đặt hàng đủ điều kiện:

| Setting | What it does |
|---------|--------------|
| `issue_on` | Khi cấp phần thưởng: `signup` (ngay khi đăng ký), `first_purchase` (ngay sau khi đặt hàng), hoặc `post_refund` (sau khi thời gian hoàn tiền kết thúc) |
| `refund_window_days` | Số ngày cần chờ trước khi cấp phần thưởng khi sử dụng `post_refund` (mặc định: 14 ngày) |

Sử dụng `post_refund` là phương pháp thận trọng nhất — nó đợi đến khi thời gian hoàn trả đã qua mới cấp phần thưởng, giảm rủi ro cấp phần thưởng cho các đơn hàng sau đó bị hoàn tiền.

### Giới hạn và mức trần

Ngăn chặn một người giới thiệu duy nhất từ việc nhận vô số phần thưởng bằng cách đặt giới hạn trong trường **Caps & Limits**:

| Cài đặt | Mô tả chức năng |
|---------|--------------|
| `monthly_per_referrer` | Số lượng tối đa các lần giới thiệu thành công được thưởng mỗi tháng, tính cho mỗi người giới thiệu |
| `lifetime_per_referrer` | Tổng số lượng tối đa các lần giới thiệu thành công được thưởng trong suốt thời gian, tính cho mỗi người giới thiệu |
| `max_reward_per_order` | Giá trị thưởng tối đa (theo loại tiền tệ của cửa hàng) được cấp cho một lần chuyển đổi giới thiệu |

**Ví dụ** — 20 lần giới thiệu mỗi tháng, 200 lần trong suốt thời gian, 50 USD tối đa cho mỗi lần chuyển đổi:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Cấu hình theo dõi

Cấu hình cách theo dõi các liên kết giới thiệu trong trường **Cấu hình theo dõi**:

| Cài đặt | Mô tả chức năng |
|---------|--------------|
| `cookie_ttl_days` | Số ngày mà cookie theo dõi giới thiệu vẫn còn hiệu lực sau khi người bạn nhấp vào liên kết (mặc định: 30) |
| `attribution` | Phương pháp gán điểm — hiện tại là `last_touch` (lần nhấp vào liên kết giới thiệu gần nhất được ghi nhận) |

### Chính sách gian lận

Hệ thống phát hiện gian lận sẽ tự động đánh giá điểm rủi ro cho mỗi lần gán điểm giới thiệu trước khi phê duyệt. Cấu hình chính sách trong trường **Chính sách gian lận**:

| Cài đặt | Mô tả chức năng |
|---------|--------------|
| `policy` | Mức độ nghiêm ngặt tổng thể: `strict`, `balanced`, hoặc `lenient` |
| `auto_reject_threshold` | Điểm rủi ro (0–100) trên mức nào các lần gán điểm sẽ bị từ chối tự động (mặc định: 80) |
| `auto_approve_threshold` | Điểm rủi ro dưới mức nào các lần gán điểm sẽ được phê duyệt tự động (mặc định: 30) |
| `check_ip` | Nếu `true`, kiểm tra xem người giới thiệu và người được giới thiệu có cùng địa chỉ IP hay không |
| `check_device` | Nếu `true`, kiểm tra xem có chia sẻ dấu vân tay thiết bị giữa người giới thiệu và người được giới thiệu hay không |
| `check_velocity` | Nếu `true`, giám sát các tỷ lệ giới thiệu bất thường cao từ một nguồn |
| `velocity_window_hours` | Khoảng thời gian (tính bằng giờ) để kiểm tra tốc độ |
| `max_referrals_per_window` | Số lượng giới thiệu tối đa được phép từ một nguồn trong khoảng thời gian tốc độ |

Các lần gán điểm có điểm rủi ro nằm giữa ngưỡng từ chối tự động và phê duyệt tự động sẽ rơi vào trạng thái **Đang chờ** và yêu cầu xem xét thủ công.

### Điều khoản và điều kiện

Nhập bất kỳ điều khoản và điều kiện pháp lý nào cho chương trình trong trường **Điều khoản và điều kiện**. Văn bản này sẽ được hiển thị cho khách hàng khi họ xem chương trình giới thiệu. Hỗ trợ định dạng Markdown.

## Xem các lần gán điểm giới thiệu

Di chuyển đến **Marketing > Referral Attributions** để xem tất cả các trường hợp giới thiệu — mối liên hệ giữa người giới thiệu và khách hàng được giới thiệu.

![Danh sách các lần gán điểm giới thiệu](/static/core/admin/img/help/referral-program/attribution-list.webp)

Mỗi lần gán điểm sẽ hiển thị người giới thiệu, khách hàng được giới thiệu, đơn hàng đầu tiên mà họ đặt, trạng thái hiện tại và điểm rủi ro.

### Trạng thái gán điểm

| Trạng thái | Ý nghĩa |
|--------|---------------|
| **Đang chờ** | Đang chờ xem xét — điểm rủi ro nằm trong khoảng cần xem xét thủ công |
| **Đã phê duyệt** | Lần giới thiệu hợp lệ — phần thưởng đã hoặc sẽ được cấp |
| **Đã từ chối** | Lần giới thiệu không đạt yêu cầu hoặc bị đánh dấu là gian lận |
| **Đã hết hạn** | Lần giới thiệu không được chuyển đổi trong khoảng thời gian theo dõi |

### Phê duyệt hoặc từ chối gán điểm thủ công

Đối với các lần gán điểm có trạng thái **Đang chờ**, bạn có thể phê duyệt hoặc từ chối chúng bằng cách mở hồ sơ gán điểm và sử dụng các nút hành động. Khi từ chối, hãy chọn **Lý do từ chối**:

- Tự giới thiệu
- Không phải khách hàng mới
- Dưới giá trị đơn hàng tối thiểu
- Email tạm thời
- Đã đạt giới hạn
- Rủi ro gian lận
- Đơn hàng được hoàn tiền hoặc hủy
- Từ chối thủ công

Bạn cũng có thể thêm **Ghi chú từ chối** cho hồ sơ của riêng bạn.

### Lọc theo cấp độ rủi ro

Sử dụng bộ lọc **Cấp độ rủi ro** trong thanh bên để tập trung vào các lần gán điểm có rủi ro cao cần xem xét:

- Rủi ro thấp (điểm 0–30) — Được phê duyệt tự động
- Rủi ro trung bình (điểm 31–70) — Xem xét thủ công
- Rủi ro cao (điểm 71–89) — Xem xét thủ công, cần thận trọng
- Rủi ro rất cao (điểm 90+) — Bị từ chối tự động

## Xem các phần thưởng đã cấp


Truy cập vào **Marketing > Phần thưởng đã cấp** để xem tất cả các phần thưởng đã được cấp như kết quả của các thuộc tính đã được phê duyệt.

Mỗi mục phần thưởng hiển thị khách hàng, xem họ là người giới thiệu hay người được giới thiệu, loại và số lượng phần thưởng, cũng như trạng thái đổi thưởng hiện tại.

### Trạng thái phần thưởng

| Trạng thái | Ý nghĩa của nó |
|------------|----------------|
| **Đang chờ** | Phần thưởng đã được tạo nhưng chưa được giao cho khách hàng |
| **Đã cấp** | Phần thưởng đang hoạt động và sẵn sàng cho khách hàng sử dụng |
| **Đã sử dụng** | Khách hàng đã sử dụng phần thưởng |
| **Hết hạn** | Phần thưởng đã hết hạn mà không được sử dụng |
| **Đã hủy** | Phần thưởng đã bị hủy bỏ thủ công (ví dụ, nếu đơn hàng ban đầu được hoàn tiền sau khi phần thưởng đã được cấp) |

### Hủy bỏ phần thưởng

Nếu cần hủy bỏ phần thưởng — ví dụ, đơn hàng đủ điều kiện được hoàn trả — hãy mở hồ sơ phần thưởng và sử dụng hành động **Hủy bỏ**. Thêm chú thích giải thích lý do hủy bỏ để lưu vào hồ sơ của bạn.

## Mẹo

- Bắt đầu với cài đặt thời gian `post_refund`. Chờ đến khi thời gian hoàn trả hết hạn trước khi cấp phần thưởng sẽ giúp tránh việc cấp phần thưởng cho các đơn hàng cuối cùng bị hoàn trả.
- Chính sách gian lận `balanced` là lựa chọn mặc định tốt cho hầu hết các cửa hàng. Chuyển sang `strict` nếu bạn nhận thấy sự gia tăng bất thường trong số lượng giới thiệu từ một số tài khoản nhỏ.
- Đặt giới hạn hàng tháng và suốt đời hợp lý. Nếu giá trị phần thưởng của bạn cao, giới hạn 10–20 mỗi tháng mỗi người giới thiệu là hợp lý để ngăn chặn việc lạm dụng.
- Kiểm tra các thuộc tính **Đang chờ** hàng tuần. Việc để chúng không được xem xét trong thời gian quá dài có thể làm bực bội các người giới thiệu hợp lệ đang chờ phần thưởng của họ.
- Sử dụng bộ lọc **Mức độ rủi ro** để ưu tiên hàng đợi xem xét thủ công của bạn — bắt đầu với các thuộc tính có mức rủi ro rất cao trước khi chuyển sang mức rủi ro trung bình.
- Giữ Điều khoản và Điều kiện ngắn gọn và sử dụng ngôn ngữ đơn giản. Khách hàng có xu hướng tham gia nhiều hơn khi họ hiểu rõ các quy tắc.