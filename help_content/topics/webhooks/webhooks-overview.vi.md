---
title: Tổng quan về Webhooks
---

Webhooks cho phép cửa hàng của bạn tự động thông báo cho các hệ thống bên ngoài — như các công cụ quản lý tồn kho, hệ thống ERP, dịch vụ giao hàng hoặc ứng dụng tùy chỉnh — khi có sự kiện xảy ra trong cửa hàng của bạn. Thay vì các hệ thống đó liên tục hỏi "có gì thay đổi không?", cửa hàng của bạn sẽ gửi một thông báo ngay khi sự kiện xảy ra.

## Webhooks làm gì

Khi một sự kiện xảy ra trong cửa hàng của bạn (một đơn hàng được đặt, một khoản thanh toán được nhận, một sản phẩm hết hàng), Spwig sẽ gửi một yêu cầu HTTP POST chứa dữ liệu sự kiện đến URL mà bạn cấu hình. Hệ thống nhận có thể xử lý dữ liệu đó ngay lập tức — ví dụ, cập nhật tồn kho, kích hoạt nhãn vận chuyển hoặc gửi thông báo tùy chỉnh.

Một số ứng dụng phổ biến của webhooks bao gồm:

- Đồng bộ đơn hàng theo thời gian thực với đối tác giao hàng
- Cập nhật tồn kho trong hệ thống ERP khi tồn kho thay đổi
- Kích hoạt tin nhắn SMS hoặc thông báo đẩy khi trạng thái đơn hàng thay đổi
- Ghi lại các sự kiện vào kho dữ liệu để báo cáo
- Kết nối với các công cụ tự động như Zapier hoặc Make

## Xem và quản lý các điểm cuối

Truy cập **Tích hợp > Webhooks** để xem tất cả các điểm cuối webhook đã cấu hình của bạn.

![Danh sách các điểm cuối webhook](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

Danh sách hiển thị tên, URL, trạng thái hoạt động, số lượng sự kiện mà điểm cuối đó đăng ký, trạng thái sức khỏe và thời gian cuối cùng nhận được giao hàng.

### Chỉ số sức khỏe

Cột **Sức khỏe** hiển thị một cách nhanh chóng mức độ hoạt động của từng điểm cuối:

- **Khỏe mạnh** — Tất cả các lần giao hàng gần đây đều thành công
- **Giảm sút** — Một số lỗi gần đây nhưng điểm cuối vẫn đang hoạt động
- **Không khỏe / Vô hiệu hóa** — Điểm cuối đã bị vô hiệu hóa tự động sau quá nhiều lần thất bại liên tiếp (mặc định là 10). Bạn phải kích hoạt lại thủ công sau khi khắc phục nguyên nhân gốc rễ.

## Tạo điểm cuối webhook

Nhấp vào **+ Thêm điểm cuối webhook** để mở trình hướng dẫn thiết lập. Trình hướng dẫn sẽ hướng dẫn bạn qua bốn bước.

### Bước 1: Thông tin cơ bản

- **Tên** — Nhãn thân thiện để nhận diện điểm cuối này (ví dụ: `Dịch vụ Giao hàng Đơn hàng` hoặc `Đồng bộ Tồn kho`).
- **URL** — URL đầy đủ của máy chủ sẽ nhận các yêu cầu POST webhook. Điều này phải có thể truy cập được từ bên ngoài (không phải là URL localhost).
- **Mô tả** — Ghi chú tùy chọn về mục đích sử dụng của điểm cuối này.
- **Hoạt động** — Xác định điểm cuối này có nhận giao hàng hay không. Tắt để tạm dừng mà không xóa điểm cuối.

### Bước 2: Đăng ký sự kiện

Chọn các sự kiện nào sẽ kích hoạt giao hàng đến điểm cuối này. Các sự kiện được phân nhóm theo danh mục:

### Sự kiện đơn hàng

| Sự kiện | Khi nào xảy ra |
|--------|----------------|
| `order.created` | Một đơn hàng mới được đặt |
| `order.paid` | Thanh toán cho đơn hàng được xác nhận |
| `order.cancelled` | Một đơn hàng bị hủy |
| `order.fulfilled` | Tất cả các mặt hàng trong đơn hàng được giao |
| `order.partially_fulfilled` | Một số mặt hàng trong đơn hàng được giao |
| `order.status_changed` | Trạng thái đơn hàng thay đổi |
| `order.note_added` | Một ghi chú được thêm vào đơn hàng |

### Sự kiện thanh toán

| Sự kiện | Khi nào xảy ra |
|--------|----------------|
| `payment.received` | Một khoản thanh toán được nhận |
| `payment.failed` | Một lần thanh toán thất bại |
| `payment.pending` | Một khoản thanh toán đang chờ xác nhận |

### Sự kiện giao hàng

| Sự kiện | Khi nào xảy ra |
|--------|----------------|
| `shipment.created` | Một lô hàng được tạo |
| `shipment.shipped` | Một lô hàng được gửi |
| `shipment.delivered` | Một lô hàng được giao |
| `shipment.returned` | Một lô hàng được trả lại |
| `shipment.tracking_updated` | Thông tin theo dõi được cập nhật |

### Sự kiện tồn kho

| Sự kiện | Khi nào xảy ra |
|--------|----------------|
| `inventory.low_stock` | Tồn kho giảm xuống dưới ngưỡng |
| `inventory.out_of_stock` | Một sản phẩm hết hàng |
| `inventory.restocked` | Một sản phẩm được bổ sung hàng |
| `inventory.adjusted` | Tồn kho được điều chỉnh thủ công |

### Sự kiện sản phẩm

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

### Sự kiện khách hàng

`customer.created`, `customer.updated`, `customer.deleted`

#### Các sự kiện đăng ký

`subscription.created`, `subscription.activated`, `subscription.renewed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `subscription.resumed`, `subscription.payment_failed`

#### Các sự kiện khác

`refund.created`, `refund.completed`, `refund.failed`, `cart.abandoned`, `cart.recovered`, `translation.job_completed`, `translation.job_failed`

Để nhận tất cả các sự kiện, hãy đăng ký với `*` (ký tự đại diện). Điều này hữu ích cho các điểm cuối mục đích chung nhưng tạo ra nhiều lưu lượng hơn — chỉ đăng ký các sự kiện bạn thực sự cần cho các tích hợp sản xuất.

### Bước 3: Cấu hình

- **Số lần thử lại tối đa** — Số lần Spwig nên thử lại việc giao hàng thất bại trước khi từ bỏ (mặc định: 5). Mỗi lần thử lại sử dụng khoảng thời gian tăng dần theo cấp số nhân.
- **Thời gian chờ (giây)** — Thời gian chờ để máy chủ nhận biết phản hồi trước khi đánh dấu giao hàng là thất bại (mặc định: 30 giây). Chỉ tăng giá trị này nếu máy chủ của bạn được biết là chậm.

### Bước 4: Bảo mật

Mỗi điểm cuối webhook đều có một **khóa bí mật ký tên** được tạo tự động — một khóa ngẫu nhiên 64 ký tự. Spwig sử dụng khóa bí mật này để ký tên mỗi tải trọng webhook bằng chữ ký HMAC-SHA256.

Chữ ký được bao gồm trong tiêu đề yêu cầu `X-Webhook-Signature`. Máy chủ nhận của bạn nên xác minh chữ ký này để xác nhận rằng yêu cầu thực sự đến từ cửa hàng của bạn và không bị sửa đổi.

Khóa bí mật được hiển thị bị che giấu trong bảng điều khiển. Để xem hoặc xoay khóa bí mật, hãy sử dụng API của Spwig. Hãy xoay khóa bí mật ngay lập tức nếu bạn nghi ngờ nó đã bị rò rỉ.

## Kích hoạt và tắt các điểm cuối

Để nhanh chóng kích hoạt hoặc tắt một hoặc nhiều điểm cuối mà không cần mở từng điểm cuối:

1. Chọn các hộp kiểm bên cạnh các điểm cuối bạn muốn thay đổi
2. Sử dụng danh sách thả xuống **Hành động** để chọn **Kích hoạt các điểm cuối đã chọn** hoặc **Tắt các điểm cuối đã chọn**
3. Nhấp **Tiến hành**

Để kích hoạt lại một điểm cuối đã bị tắt tự động do lỗi, hãy chọn nó và sử dụng hành động **Đặt lại đếm lỗi**, sau đó kích hoạt lại. Hãy sửa lỗi gây ra các lần giao hàng thất bại trước, nếu không nó sẽ bị tắt lại nhanh chóng.

## Một số mẹo

- Chỉ đăng ký các sự kiện bạn thực sự cần — các sự kiện không cần thiết tạo ra tiếng ồn trong nhật ký của bạn và làm tăng tải giao hàng.
- Luôn xác minh chữ ký webhook trên máy chủ nhận của bạn trước khi xử lý tải trọng. Điều này bảo vệ bạn khỏi các yêu cầu giả mạo.
- Sử dụng trường **Mô tả** để ghi lại hệ thống hoặc tích hợp mà điểm cuối này kết nối. Điều này giúp khi khắc phục sự cố sau nhiều tháng.
- Đặt **Thời gian chờ** cao hơn một chút so với thời gian phản hồi trung bình của máy chủ bạn. Một thời gian chờ 10–15 giây là đủ cho hầu hết các tích hợp.
- Nếu một điểm cuối chuyển sang **Không khỏe mạnh**, hãy kiểm tra nhật ký giao hàng trước (xem **Giao hàng Webhook**) để hiểu mô hình lỗi trước khi kích hoạt lại nó.
- Để kiểm tra, hãy hướng webhook đến một công cụ như [webhook.site](https://webhook.site) để kiểm tra các tải trọng thô mà không cần máy chủ trực tiếp.