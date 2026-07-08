---
title: Chương trình đại lý
---

Chương trình đại lý cho phép bạn tuyển dụng các đối tác quảng bá sản phẩm của bạn và kiếm hoa hồng từ các đơn hàng mà họ tạo ra. Các đại lý chia sẻ các liên kết giới thiệu duy nhất, và Spwig tự động theo dõi lượt nhấp, gán đơn hàng và tính toán hoa hồng.

![Chương trình đại lý](/static/core/admin/img/help/affiliate-program/program-list.webp)

## Cách hoạt động

1. Bạn tạo một hoặc nhiều **chương trình đại lý** với tỷ lệ hoa hồng và quy tắc
2. Các đại lý **đăng ký** thông qua cổng thông tin công khai hoặc được thêm vào thủ công
3. Mỗi đại lý nhận được một **liên kết giới thiệu duy nhất** kèm mã theo dõi
4. Khi khách hàng nhấp vào liên kết và thực hiện mua hàng, một **hoa hồng** sẽ được ghi nhận
5. Bạn xem xét và phê duyệt các khoản hoa hồng, sau đó xử lý **các khoản thanh toán**

## Tạo chương trình

Truy cập **Marketing > Chương trình đại lý** và nhấp **Thêm chương trình**.

### Cài đặt chương trình

| Cài đặt | Mô tả |
|---------|-------------|
| **Tên** | Tên chương trình hiển thị cho các đại lý (ví dụ: "Chương trình Đối tác") |
| **Loại hoa hồng** | **Tỷ lệ phần trăm** của tổng đơn hàng hoặc **Cố định** số tiền cho mỗi lần bán hàng |
| **Tỷ lệ hoa hồng** | Phần trăm hoặc số tiền cố định mà các đại lý kiếm được |
| **Thời gian sống cookie** | Số ngày cookie theo dõi giới thiệu tồn tại (mặc định: 30 ngày) |
| **Mức thanh toán tối thiểu** | Mức thu nhập tối thiểu trước khi đại lý có thể yêu cầu thanh toán |
| **Tự động phê duyệt đại lý** | Tự động chấp nhận các ứng dụng đại lý mới, hoặc yêu cầu phê duyệt thủ công |
| **Trạng thái** | Hoạt động, tạm dừng hoặc đóng |

### Loại hoa hồng

- **Tỷ lệ phần trăm** — Các đại lý kiếm được tỷ lệ phần trăm của tổng số tiền mỗi đơn hàng được giới thiệu (ví dụ: 10% của đơn hàng 100 đô la = 10 đô la hoa hồng)
- **Cố định** — Các đại lý kiếm được một khoản cố định cho mỗi lần bán hàng, bất kể giá trị đơn hàng (ví dụ: 5 đô la cho mỗi lần bán hàng)

## Quản lý đại lý

Truy cập **Marketing > Đại lý** để xem và quản lý tài khoản đại lý.

### Chi tiết đại lý

Mỗi đại lý có:
- **Mã đại lý** — Mã duy nhất được sử dụng trong các liên kết giới thiệu (tự động tạo hoặc tùy chỉnh)
- **Liên kết giới thiệu** — Liên kết theo dõi đầy đủ mà đại lý chia sẻ (ví dụ: `yourstore.com/?ref=CODE`)
- **Trạng thái** — Chờ xử lý, đã phê duyệt hoặc bị từ chối
- **Phương thức thanh toán** — Cách đại lý nhận các khoản thanh toán (PayPal hoặc chuyển khoản ngân hàng)
- **Thành viên chương trình** — Chương trình mà đại lý thuộc về

### Thêm đại lý thủ công

1. Nhấp **Thêm đại lý**
2. Chọn tài khoản khách hàng hiện có hoặc tạo một tài khoản mới
3. Gán đại lý cho một hoặc nhiều chương trình
4. Thiết lập mã đại lý (hoặc để trống để tự động tạo)

### Cổng thông tin đại lý

Các đại lý truy cập cổng thông tin công khai nơi họ có thể:
- Xem bảng điều khiển của họ với các khoản thu nhập và thống kê lượt nhấp
- Sao chép các liên kết giới thiệu của họ
- Theo dõi lịch sử hoa hồng
- Yêu cầu thanh toán

URL cổng thông tin được cung cấp tự động tại `/affiliate/` trên cửa hàng của bạn.

## Theo dõi và Hoa hồng

### Cách theo dõi hoạt động

1. Một khách hàng nhấp vào liên kết giới thiệu của đại lý
2. Một cookie theo dõi được thiết lập trong trình duyệt của khách hàng (tồn tại trong thời gian sống cookie được cấu hình)
3. Nếu khách hàng đặt hàng trong thời gian sống cookie, đơn hàng sẽ được gán cho đại lý
4. Một bản ghi hoa hồng được tạo với trạng thái **Chờ xử lý**

### Trạng thái hoa hồng

| Trạng thái | Mô tả |
|--------|-------------|
| **Chờ xử lý** | Hoa hồng được ghi nhận, đang chờ xem xét |
| **Đã phê duyệt** | Đã xác minh và sẵn sàng để thanh toán |
| **Bị từ chối** | Hoa hồng bị từ chối (ví dụ: đơn hàng gian lận hoặc hàng hóa được hoàn trả) |
| **Đã thanh toán** | Hoa hồng được bao gồm trong khoản thanh toán đã hoàn thành |

### Xem xét hoa hồng

Truy cập **Marketing > Hoa hồng** để xem các khoản hoa hồng đang chờ xử lý:

1. Kiểm tra chi tiết đơn hàng để xác minh giao dịch là hợp lệ
2. Nhấp **Phê duyệt** để xác nhận, hoặc **Từ chối** với lý do
3. Các khoản hoa hồng đã được phê duyệt tích lũy vào số dư thanh toán của đại lý

## Thanh toán

Khi số dư hoa hồng đã được phê duyệt của đại lý đạt đến ngưỡng thanh toán tối thiểu, bạn có thể xử lý khoản thanh toán.

### Xử lý khoản thanh toán

1. Truy cập **Marketing > Thanh toán**
2. Chọn các đại lý có số dư khả dụng
3. Chọn phương thức thanh toán:
   - **PayPal** — Gửi tiền trực tiếp đến email PayPal của đại lý
   - **Chuyển khoản ngân hàng** — Ghi lại chuyển khoản ngân hàng thủ công
4. Xác nhận và xử lý khoản thanh toán
5. Trạng thái thanh toán được cập nhật thành **Hoàn tất** và các khoản hoa hồng được đánh dấu là **Đã thanh toán**

### Nhà cung cấp thanh toán

Spwig tích hợp với các nhà cung cấp thanh toán để thực hiện thanh toán tự động:
- **PayPal** — Thanh toán hàng loạt tự động thông qua API PayPal
- **Airwallex** — Thanh toán quốc tế với tỷ giá cạnh tranh
- **Thủ công** — Ghi lại các khoản thanh toán được xử lý bên ngoài Spwig

## Liên kết giới thiệu

Mỗi liên kết giới thiệu của đại lý tuân theo mẫu này:

```
https://yourstore.com/?ref=AFFILIATE_CODE
```

Các đại lý cũng có thể tạo liên kết đến các sản phẩm hoặc danh mục cụ thể:

```
https://yourstore.com/products/shoe-name/?ref=AFFILIATE_CODE
```

Tham số `ref` hoạt động trên bất kỳ trang nào — cookie theo dõi được thiết lập bất kể trang đích là gì.

## Phân tích chương trình

Bảng điều khiển chương trình đại lý hiển thị:
- **Tổng lượt nhấp** — Số lần các liên kết giới thiệu đã được nhấp
- **Tổng đơn hàng** — Các đơn hàng được gán cho các đại lý
- **Tổng hoa hồng** — Tổng số tất cả các khoản hoa hồng (chờ xử lý, đã phê duyệt và đã thanh toán)
- **Đại lý đang hoạt động** — Số lượng đại lý đã được phê duyệt hiện đang tạo các liên kết giới thiệu

## Một số mẹo

- Bắt đầu với **hoa hồng theo tỷ lệ phần trăm** (5–15%) — nó mở rộng tự nhiên theo giá trị đơn hàng và dễ hiểu cho các đại lý.
- Thiết lập **thời gian sống cookie 30 ngày** làm cơ sở — điều này cho phép khách hàng có thời gian quay lại và hoàn thành mua hàng trong khi vẫn gán doanh số cho đại lý.
- Kích hoạt **tự động phê duyệt** cho các chương trình công khai để giảm bớt sự cản trở, hoặc sử dụng phê duyệt thủ công cho các chương trình mời riêng nơi bạn muốn kiểm tra từng đại lý.
- Thiết lập một **mức thanh toán tối thiểu** hợp lý (ví dụ: 25–50 đô la) để tránh xử lý nhiều giao dịch nhỏ.
- Cá nhân hóa **cổng thông tin đại lý** để phù hợp với thương hiệu của bạn — các đại lý có xu hướng quảng bá cửa hàng của bạn khi trải nghiệm cảm thấy chuyên nghiệp.
- Theo dõi thường xuyên các khoản hoa hồng cho **các mô hình gian lận** như tự giới thiệu, tỷ lệ hoàn trả cao bất thường hoặc khối lượng nhấp đáng ngờ.