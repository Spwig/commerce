---
title: Hiểu về Hoa Hồng
---

Hoa hồng là bản ghi thu nhập được tạo ra khi một đại lý thành công trong việc thúc đẩy một đơn hàng đến cửa hàng của bạn. Mỗi hoa hồng gắn với một đơn hàng cụ thể, đại lý và chương trình, và di chuyển qua vòng đời từ đang chờ đến đã thanh toán. Hướng dẫn này giải thích cách hoa hồng hoạt động, cách chúng được tính toán và cách quản lý chúng hiệu quả.

## Hoa Hồng Là Gì?

Một hoa hồng đại diện cho số tiền mà một đại lý được hưởng khi giới thiệu một khách hàng đã hoàn tất mua hàng. Khi khách hàng nhấp vào liên kết giới thiệu của đại lý và đặt hàng trong khoảng thời gian cookie, Spwig sẽ tự động tạo bản ghi hoa hồng.

Mỗi hoa hồng chứa:
- **Đại lý** — Đối tác đã giới thiệu khách hàng
- **Chương trình** — Chương trình đại lý xác định các quy tắc hoa hồng
- **Đơn hàng** — Đơn hàng tạo ra hoa hồng
- **Số tiền** — Giá trị hoa hồng được tính toán
- **Trạng thái** — Giai đoạn hiện tại trong vòng đời của hoa hồng
- **Ngày tháng** — Ngày tạo, ngày duyệt/chối và ngày thanh toán

## Tính Toán Hoa Hồng

Hoa hồng được tính toán tự động dựa trên loại hoa hồng và tỷ lệ của chương trình.

| Loại Hoa Hồng | Tính Toán | Ví Dụ |
|----------------|-----------|--------|
| **Tỷ lệ phần trăm** | Tổng đơn hàng × % hoa hồng ÷ 100 | Đơn hàng: $200, Tỷ lệ: 10% → **$20 hoa hồng** |
| **Cố định** | Số tiền cố định cho mỗi đơn hàng | Tỷ lệ: $15 → **$15 hoa hồng** (bất kể giá trị đơn hàng) |

### Ví Dụ Tính Toán

**Hoa Hồng Tỷ Lệ (10%)**:
- Khách hàng đặt đơn hàng $50 → $5 hoa hồng
- Khách hàng đặt đơn hàng $150 → $15 hoa hồng
- Khách hàng đặt đơn hàng $300 → $30 hoa hồng

**Hoa Hồng Cố Định ($20)**:
- Khách hàng đặt đơn hàng $50 → $20 hoa hồng
- Khách hàng đặt đơn hàng $150 → $20 hoa hồng
- Khách hàng đặt đơn hàng $300 → $20 hoa hồng

Hoa hồng được tính toán trên **tổng số tiền đơn hàng** (trước khi tính phí vận chuyển và thuế) và được tạo ngay lập tức khi đơn hàng được đặt.

## Vòng Đời Hoa Hồng

Mỗi hoa hồng di chuyển qua một loạt các trạng thái từ lúc tạo đến thanh toán:

```
Đang chờ → Được duyệt → Đã thanh toán
   ↓
Bị từ chối
```

### Định Nghĩa Trạng Thái

| Trạng Thái | Mô Tả | Điều Gì Xảy Ra |
|------------|-------|------------------|
| **Đang chờ** | Đơn hàng được đặt, hoa hồng đang chờ xem xét | Hoa hồng được tạo nhưng chưa được xác nhận. Đại lý có thể thấy nó nhưng không thể rút tiền. |
| **Được duyệt** | Nhà bán hàng xác nhận giao dịch là hợp lệ | Hoa hồng được xác minh và được thêm vào số dư có thể sử dụng của đại lý. Có thể nhận thanh toán. |
| **Bị từ chối** | Nhà bán hàng từ chối hoa hồng | Hoa hồng bị từ chối (ví dụ: đơn hàng được hoàn tiền, gian lận hoặc vi phạm điều khoản). Không đủ điều kiện để thanh toán. |
| **Đã thanh toán** | Hoa hồng được bao gồm trong thanh toán đã hoàn tất | Đại lý đã được thanh toán. Hoa hồng được xác nhận cuối cùng và không thể chỉnh sửa. |

![Danh Sách Hoa Hồng](/static/core/admin/img/help/commission-management/commission-list.webp)

## Khi Nào Hoa Hồng Được Tạo

Hoa hồng được tạo tự động theo trình tự sau:

1. **Khách hàng nhấp vào liên kết đại lý** — URL giới thiệu chứa mã theo dõi duy nhất của đại lý (ví dụ: `?ref=JOHNSMITH`)
2. **Cookie được thiết lập** — Một cookie theo dõi được lưu trữ trong trình duyệt của khách hàng với mã đại lý
3. **Mua hàng trong thời gian cookie** — Khách hàng hoàn tất đơn hàng trước khi cookie hết hạn (mặc định: 30 ngày)
4. **Hệ thống gán đơn hàng** — Spwig kiểm tra cookie theo dõi đang hoạt động và xác định đại lý giới thiệu
5. **Hoa hồng được tạo tự động** — Một bản ghi hoa hồng được tạo với trạng thái **Đang chờ**

Hoa hồng được tạo **ngay lập tức** khi đơn hàng được đặt, ngay cả trước khi xác nhận thanh toán. Điều này cho phép các nhà bán hàng xem xét các hoa hồng trong khi đơn hàng đang được xử lý.

## Theo Dõi & Gán Trách Nhiệm

Spwig sử dụng **mô hình gán trách nhiệm theo lượt nhấp cuối cùng** để xác định đại lý nào nên nhận được tín dụng cho một giao dịch.

### Cách Gán Trách Nhiệm Hoạt Động

- **Mô hình lượt nhấp cuối cùng** — Liên kết đại lý cuối cùng được nhấp sẽ được ghi nhận (ngay cả khi nhiều đại lý đã giới thiệu khách hàng)
- **Theo dõi dựa trên cookie** — Một cookie lưu trữ mã đại lý trong trình duyệt của khách hàng
- **Thời gian sống của cookie** — Xác định khoảng thời gian mà một giao dịch có thể được gán trách nhiệm (được cấu hình theo chương trình, thường là 30 ngày)
- **Theo dõi IP và phiên** — Dữ liệu bổ sung giúp xác định các mô hình gian lận

### Ví Dụ Gán Trách Nhiệm

- Ngày 1: Khách hàng nhấp vào liên kết của Đại lý A → Cookie được thiết lập cho Đại lý A
- Ngày 5: Khách hàng nhấp vào liên kết của Đại lý B → Cookie **được cập nhật** thành Đại lý B (lượt nhấp cuối cùng thắng)
- Ngày 7: Khách hàng đặt đơn hàng → Hoa hồng thuộc về **Đại lý B**

Nếu khách hàng quay lại vào Ngày 35 (sau khi cookie hết hạn 30 ngày) và đặt đơn hàng, **không có hoa hồng** nào được tạo vì cửa sổ theo dõi đã đóng.

## Chi Tiết Hoa Hồng

Truy cập **Marketing > Hoa Hồng** để xem tất cả bản ghi hoa hồng.

### Các Trường Hoa Hồng

Mỗi hoa hồng hiển thị:

| Trường | Mô Tả |
|--------|--------|
| **Đại lý** | Tên và mã đại lý |
| **Chương trình** | Tên chương trình đại lý |
| **Đơn hàng** | Số đơn hàng (liên kết nhấp để xem chi tiết đơn hàng đầy đủ) |
| **Số tiền** | Giá trị hoa hồng được tính toán |
| **Trạng thái** | Giai đoạn hiện tại (Đang chờ, Được duyệt, Bị từ chối, Đã thanh toán) |
| **Tạo** | Thời điểm hoa hồng được tạo |
| **Ngày duyệt/chối** | Thời điểm trạng thái được cập nhật |
| **Ngày thanh toán** | Thời điểm thanh toán được xử lý |
| **Ghi chú** | Ghi chú nội bộ về hoa hồng |

### Xem Chi Tiết Đơn Hàng

Nhấp vào **số đơn hàng** trong bản ghi hoa hồng để xem đơn hàng gốc. Điều này cho phép bạn kiểm tra:
- Tổng đơn hàng và các mặt hàng đã mua
- Thông tin khách hàng
- Trạng thái thanh toán
- Trạng thái vận chuyển
- Bất kỳ hoàn tiền hoặc hoàn đổi nào

Bối cảnh này giúp bạn quyết định xem có nên duyệt hoặc từ chối hoa hồng hay không.

## Quản Lý Hoa Hồng

Mặc dù hướng dẫn này tập trung vào việc hiểu về hoa hồng, các bước thực tế để duyệt, từ chối và thanh toán hoa hồng được đề cập chi tiết trong chủ đề giúp đỡ **Quản lý Hoa Hồng**.

### Tổng Quan Nhanh

- **Duyệt** — Xác minh đơn hàng là hợp lệ và xác nhận hoa hồng là hợp lệ
- **Từ chối** — Từ chối các hoa hồng cho các đơn hàng gian lận, hoàn tiền hoặc vi phạm chính sách
- **Thêm ghi chú** — Ghi lại lý do duyệt hoặc từ chối để tham khảo sau này
- **Xử lý thanh toán** — Nhóm các hoa hồng đã duyệt thành các thanh toán theo lô

Xem các chủ đề giúp đỡ liên quan để có hướng dẫn từng bước cho mỗi nhiệm vụ quản lý.

## Mẹo

- Xem xét các hoa hồng đang chờ **hàng ngày** trong tháng đầu tiên của bạn để thiết lập một thói quen và phát hiện sớm bất kỳ vấn đề theo dõi nào
- Thiết lập **thông báo qua email** để được thông báo khi có hoa hồng mới được tạo, để bạn có thể xem xét chúng khi chi tiết đơn hàng vẫn còn mới
- Duyệt hoa hồng **sau khi giao hàng** (không ngay lập tức khi đơn hàng được đặt) để tính đến việc hủy bỏ và hoàn đổi
- Sử dụng **trường ghi chú** để ghi lại quyết định, đặc biệt là đối với các hoa hồng bị từ chối, để bạn có hồ sơ nếu đại lý đặt câu hỏi
- Tìm kiếm **mẫu từ chối** — nếu một đại lý có nhiều hoa hồng bị từ chối, điều này có thể cho thấy gian lận hoặc hiểu sai điều khoản chương trình
- Cân nhắc tạo **chính sách duyệt hoa hồng** (ví dụ: "được duyệt sau 14 ngày cửa sổ hoàn đổi") và thông báo cho các đại lý để thiết lập kỳ vọng rõ ràng

Lưu ý: Bảo tồn toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật chính xác như được hiển thị trong các quy tắc bảo tồn.