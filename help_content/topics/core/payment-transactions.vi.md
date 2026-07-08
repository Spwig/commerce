---
title: Giao dịch thanh toán
---

Giao dịch thanh toán là bản ghi đầy đủ của mọi sự kiện thanh toán được xử lý thông qua cửa hàng của bạn — các khoản thu, hoàn tiền, phê duyệt và nhiều hơn nữa. Phần này cũng bao gồm nhật ký webhook từ nhà cung cấp thanh toán của bạn và các ý định thanh toán được tạo ra trong quá trình thanh toán.

## Giao dịch thanh toán

Truy cập **Thanh toán > Giao dịch thanh toán** để xem tất cả các giao dịch mà cửa hàng của bạn đã xử lý.

### Loại giao dịch

| Loại | Ý nghĩa |
|------|--------------|
| **Thu tiền** | Một khoản thanh toán ngay lập tức — tiền được thu tại thời điểm giao dịch |
| **Phê duyệt** | Tiền được giữ trên thẻ của khách hàng nhưng chưa được thu |
| **Thu tiền** | Thu tiền từ một phê duyệt trước đó |
| **Hủy bỏ** | Hủy bỏ một phê duyệt trước khi thu tiền |
| **Hoàn tiền** | Trả lại khoản thanh toán cho khách hàng |

### Trạng thái giao dịch

| Trạng thái | Ý nghĩa |
|--------|--------------|
| **Đang chờ** | Giao dịch đã được khởi tạo nhưng chưa được xử lý |
| **Đang xử lý** | Đang được xử lý bởi nhà cung cấp thanh toán |
| **Đã phê duyệt** | Tiền được giữ — đang chờ thu |
| **Hoàn tất** | Thanh toán đã thành công |
| **Thất bại** | Thanh toán bị từ chối hoặc xảy ra lỗi |
| **Đã hủy bỏ** | Phê duyệt đã bị hủy bỏ trước khi thu tiền |
| **Đã hoàn tiền** | Một khoản hoàn tiền đầy đủ đã được thực hiện |
| **Đã hoàn tiền một phần** | Một phần của khoản thanh toán đã được hoàn lại |

### Những gì bạn có thể thấy trong bản ghi giao dịch

Mỗi giao dịch hiển thị:
- **ID giao dịch** — tham chiếu nội bộ của Spwig
- **ID giao dịch nhà cung cấp** — tham chiếu từ nhà cung cấp thanh toán của bạn (ví dụ: ID thu tiền của Stripe)
- **Số tiền** — số tiền và loại tiền tệ của giao dịch
- **Trạng thái** và **Loại**
- **Email khách hàng** và **Tên khách hàng**
- **Phương thức thanh toán** — loại (thẻ tín dụng, chuyển khoản ngân hàng, v.v.) và 4 chữ số cuối cùng
- **Đơn hàng** — đơn hàng mà giao dịch này thuộc về
- **Tài khoản nhà cung cấp** — nhà cung cấp thanh toán nào đã xử lý
- **Phản hồi nhà cung cấp** — phản hồi kỹ thuật gốc từ nhà cung cấp thanh toán
- **Thông báo lỗi** — nếu giao dịch thất bại, lý do được nhà cung cấp cung cấp
- Thời gian tạo, cập nhật cuối cùng và hoàn tất

### Lọc giao dịch

Sử dụng bộ lọc quản trị để thu hẹp giao dịch theo:
- Trạng thái (ví dụ: chỉ hiển thị các giao dịch thất bại)
- Loại (ví dụ: chỉ hiển thị các giao dịch hoàn tiền)
- Tài khoản nhà cung cấp
- Khoảng thời gian

Điều này rất hữu ích cho việc đối chiếu cuối ngày hoặc điều tra lịch sử thanh toán của một khách hàng cụ thể.

### Khi nào một giao dịch có thể được hoàn tiền?

Một giao dịch có thể được hoàn tiền khi:
- Trạng thái của nó là **Hoàn tất**
- Loại của nó là **Thu tiền** hoặc **Thu tiền**

Để thực hiện hoàn tiền, hãy sử dụng hành động **Hoàn tiền** từ trang chi tiết đơn hàng. Các khoản hoàn tiền được xử lý thông qua đơn hàng sẽ tạo ra một bản ghi giao dịch mới có loại **Hoàn tiền**.

### Luồng phê duyệt và thu tiền

Một số phương thức thanh toán (và một số nhà cung cấp thanh toán) hỗ trợ phê duyệt và thu tiền riêng biệt. Điều này rất hữu ích nếu bạn muốn xác minh thanh toán trước khi giao hàng:

1. **Phê duyệt** — Tiền được giữ trên thẻ của khách hàng (trạng thái: `Đã phê duyệt`)
2. **Thu tiền** — Được kích hoạt khi đơn hàng được giao hoặc được thực hiện
3. Nếu không được thu tiền trong khoảng thời gian phê duyệt, việc giữ tiền sẽ **hết hạn** tự động

Trường **Hết hạn lúc** trên giao dịch hiển thị thời điểm phê duyệt sẽ hết hạn.

## Webhook thanh toán

Nhà cung cấp thanh toán gửi các sự kiện webhook để thông báo cho cửa hàng của bạn về các thay đổi trạng thái thanh toán — ví dụ, khi thanh toán thành công, thất bại hoặc có tranh chấp. Spwig ghi lại tất cả các webhook đến.

Truy cập **Thanh toán > Webhook thanh toán** để xem nhật ký.

### Những gì bản ghi webhook hiển thị

| Trường | Mô tả |
|-------|-------------|
| **Nhà cung cấp** | Nhà cung cấp thanh toán nào đã gửi webhook |
| **ID sự kiện** | ID sự kiện duy nhất của nhà cung cấp |
| **Loại sự kiện** | Loại sự kiện (ví dụ: `payment_intent.succeeded`, `charge.refunded`) |
| **Đã xử lý** | Spwig có xử lý webhook này không |
| **Kiểm tra chữ ký** | Chữ ký bảo mật của webhook có hợp lệ không |
| **Nội dung** | Toàn bộ dữ liệu được gửi bởi nhà cung cấp |
| **Kết quả xử lý** | Điều Spwig đã thực hiện trong phản hồi |
| **Lỗi xử lý** | Bất kỳ lỗi nào xảy ra trong quá trình xử lý |
| **Thời gian nhận** | Thời điểm webhook được nhận |

### Sử dụng nhật ký webhook để khắc phục sự cố

Nếu thanh toán bị kẹt hoặc trạng thái đơn hàng không được cập nhật sau khi thanh toán:

1. Di chuyển đến **Thanh toán > Webhook Thanh toán**
2. Lọc theo nhà cung cấp và tìm các sự kiện gần đây
3. Kiểm tra cột **Đã xử lý** — webhook chưa được xử lý có thể cho thấy vấn đề về giao tiếp
4. Kiểm tra **Kiểm tra chữ ký** — chữ ký thất bại có thể có nghĩa là bí mật webhook của bạn được cấu hình sai
5. Xem xét **Lỗi xử lý** để biết bất kỳ thông báo lỗi nào

Các sự kiện trùng lặp được xử lý tự động — sự kết hợp `ID sự kiện` và nhà cung cấp là duy nhất, vì vậy webhook giống nhau không thể được xử lý hai lần.

## Ý định thanh toán

Một ý định thanh toán theo dõi vòng đời của thanh toán tại điểm bán hàng từ thời điểm khách hàng bắt đầu quy trình thanh toán đến kết quả cuối cùng. Các ý định thanh toán được tạo tự động khi khách hàng đến bước thanh toán tại điểm bán hàng.

Di chuyển đến **Thanh toán > Ý định thanh toán** để xem danh sách.

### Trạng thái ý định thanh toán

| Trạng thái | Ý nghĩa |
|--------|---------|
| **Đã tạo** | Ý định đã được tạo, đang chờ phương thức thanh toán |
| **Yêu cầu phương thức thanh toán** | Đang chờ khách hàng nhập thông tin thẻ của họ |
| **Yêu cầu xác nhận** | Thông tin thanh toán đã được nhập, đang chờ xác nhận |
| **Yêu cầu hành động** | Khách hàng cần hoàn thành một hành động (ví dụ: xác thực 3D Secure) |
| **Đang xử lý** | Thanh toán đang được xử lý |
| **Thành công** | Thanh toán hoàn tất thành công |
| **Hủy bỏ** | Thanh toán bị bỏ qua hoặc hủy bỏ |
| **Thất bại** | Lần thử thanh toán thất bại |

### Luồng ý định thanh toán đến đơn hàng

1. Khách hàng đến bước thanh toán tại điểm bán hàng → Spwig tạo **Ý định thanh toán** và một **Đơn hàng nháp** (chưa thanh toán)
2. Khách hàng nhập thông tin thanh toán và xác nhận
3. Nhà cung cấp thanh toán xử lý thanh toán
4. Trên thành công, đơn hàng được cập nhật thành **Đã thanh toán** và ý định thanh toán chuyển sang **Thành công**
5. Một **Giao dịch thanh toán** được tạo với chi tiết khoản thanh toán cuối cùng

Ý định thanh toán kết nối phiên điểm bán hàng, tài khoản nhà cung cấp và đơn hàng — cung cấp cho bạn một bức tranh đầy đủ về hành trình thanh toán của khách hàng.

### Sử dụng ý định thanh toán cho hỗ trợ

Nếu khách hàng báo cáo rằng họ đã thanh toán nhưng đơn hàng vẫn hiển thị là chưa thanh toán:

1. Tìm đơn hàng của khách hàng trong **Đơn hàng**
2. Di chuyển đến **Thanh toán > Ý định thanh toán** và tìm kiếm các ý định liên kết với đơn hàng đó
3. Kiểm tra trạng thái ý định — nếu nó là **Thành công**, hãy kiểm tra giao dịch liên kết
4. Nếu ý định là **Yêu cầu hành động**, khách hàng có thể chưa hoàn thành xác thực 3D Secure
5. Nếu ý định là **Thất bại**, chi tiết lỗi sẽ giải thích lý do thanh toán bị từ chối

## Một số lưu ý

- Kiểm tra các giao dịch thất bại hàng ngày — các mẫu thất bại (ví dụ: một phương thức thanh toán cụ thể hoặc quốc gia) có thể cho thấy vấn đề cấu hình hoặc nỗ lực lừa đảo.
- Nhật ký webhook rất hữu ích khi điều tra các sự khác biệt thanh toán.

Nếu đơn hàng đã được thanh toán nhưng không được xác nhận, nhật ký webhook thường sẽ cho bạn biết điều gì đã đi sai.
- Các khoản giữ chỗ xác nhận tự động hết hạn — nếu bạn sử dụng phương pháp xác nhận rồi thu tiền, hãy đảm bảo quy trình giao hàng của bạn thu tiền trước khi cửa sổ hết hạn đóng lại (thường là 7 ngày cho hầu hết các nhà cung cấp).
- Trường **Phản hồi nhà cung cấp** trên giao dịch chứa dữ liệu thô từ nhà cung cấp thanh toán.

Chia sẻ điều này với nhóm hỗ trợ của nhà cung cấp nếu bạn cần sự giúp đỡ để giải quyết một vấn đề giao dịch cụ thể.
- Các lỗi xác thực chữ ký trên webhook nên được điều tra ngay lập tức — chúng có thể cho thấy webhook secret được cấu hình sai hoặc một nỗ lực gửi các sự kiện webhook gian lận đến cửa hàng của bạn.