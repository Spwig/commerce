---
title: Cài đặt nhà cung cấp thanh toán
---

Cài đặt nhà cung cấp thanh toán cho phép bạn cấu hình PayPal và Airwallex để thực hiện thanh toán đại lý tự động. Hướng dẫn này sẽ hướng dẫn bạn cách kết nối tài khoản nhà cung cấp thanh toán, cấu hình webhook và kiểm tra tích hợp của bạn.

## Các nhà cung cấp thanh toán được hỗ trợ

Spwig tích hợp với hai nhà cung cấp thanh toán để tự động hóa thanh toán đại lý:

| Nhà cung cấp | Phương thức thanh toán | Xử lý | Hỗ trợ theo lô | Tốt nhất cho |
|----------------|----------------------|--------|----------------|------------|
| **PayPal** | Chuyển khoản qua tài khoản PayPal | Dựa trên API | Có (tối đa 15.000) | Hầu hết các đại lý, phạm vi toàn cầu |
| **Airwallex** | Chuyển khoản ngân hàng quốc tế | Dựa trên API | Không (cá nhân) | Chuyển khoản ngân hàng, thanh toán quốc tế |

### Sự khác biệt chính

**PayPal Payouts**:
- Yêu cầu đại lý phải có tài khoản PayPal (email thanh toán)
- Xử lý các lô lên đến 15.000 khoản thanh toán cùng lúc
- Xử lý nhanh hơn (1-2 ngày làm việc)
- Độ phức tạp thiết lập thấp hơn
- Phí: ~2% hoặc $0.25-$1.00 mỗi khoản thanh toán
- Một webhook cho toàn bộ lô

**Airwallex**:
- Hỗ trợ chuyển khoản ngân hàng trực tiếp
- Xử lý các khoản thanh toán cá nhân một cách riêng lẻ
- Thời gian xử lý dài hơn (2-5 ngày làm việc)
- Hỗ trợ nhiều loại tiền tệ và quốc gia
- Phí thay đổi tùy theo quốc gia đích
- Webhook cá nhân cho mỗi khoản thanh toán

Bạn có thể cấu hình cả hai nhà cung cấp và để đại lý chọn phương thức thanh toán ưa thích của họ.

## Tại sao nên sử dụng nhà cung cấp thanh toán?

Việc tích hợp nhà cung cấp thanh toán mang lại nhiều lợi ích hơn so với thanh toán thủ công:

- **Xử lý tự động** — Không cần nhập dữ liệu hoặc thực hiện thanh toán thủ công
- **Hiệu quả theo lô** — Xử lý hàng chục hoặc hàng trăm khoản thanh toán chỉ với một cú nhấp chuột
- **Xác nhận webhook** — Cập nhật trạng thái tự động khi thanh toán hoàn tất
- **Giảm lỗi** — Hệ thống xác minh chi tiết tài khoản trước khi xử lý
- **Lịch sử kiểm toán** — Ghi lại đầy đủ các giao dịch và phản hồi từ nhà cung cấp
- **Thanh toán nhanh hơn** — Đại lý nhận được tiền nhanh hơn
- **Khả năng mở rộng** — Xử lý các chương trình đại lý đang phát triển mà không cần tăng lượng công việc quản trị tương ứng

Không có tích hợp nhà cung cấp, bạn phải xử lý từng khoản thanh toán thủ công thông qua bảng điều khiển ngân hàng hoặc PayPal của bạn, sau đó quay lại Spwig để đánh dấu các khoản thanh toán đã hoàn tất.

## Cài đặt PayPal

Thực hiện theo các bước sau để cấu hình PayPal Payouts cho thanh toán đại lý tự động.

### Yêu cầu trước

Trước khi bắt đầu, bạn cần:
- Tài khoản PayPal Business (tài khoản cá nhân không thể sử dụng API Payouts)
- Truy cập bảng điều khiển nhà phát triển PayPal
- Phê duyệt sử dụng API Payouts (sau khi kiểm tra trong môi trường Sandbox)

### Bước 1: Tạo ứng dụng PayPal

1. **Di chuyển** đến [Bảng điều khiển nhà phát triển PayPal](https://developer.paypal.com/dashboard/)
2. **Đăng nhập** bằng tài khoản PayPal Business của bạn
3. **Nhấp** vào **My Apps & Credentials** trong thanh bên trái
4. **Chọn** tab **Live** (hoặc Sandbox để kiểm tra)
5. **Nhấp** vào **Create App**
6. **Nhập tên ứng dụng** (ví dụ: "Spwig Affiliate Payouts")
7. **Chọn loại ứng dụng**: Merchant
8. **Nhấp** vào **Create App**

PayPal tạo các thông tin xác thực của bạn.

### Bước 2: Lấy thông tin xác thực API

Sau khi tạo ứng dụng:

1. **Sao chép Client ID** — Chuỗi chữ số và chữ cái dài
2. **Nhấp** vào **Show** dưới mục Secret
3. **Sao chép Client Secret** — Giữ bí mật thông tin này
4. **Ghi chú chế độ** — Sandbox hoặc Live

### Bước 3: Kích hoạt tính năng Payouts

Ứng dụng PayPal yêu cầu quyền xác thực để sử dụng Payouts:

1. **Cuộn xuống** phần **Features** trong ứng dụng của bạn
2. **Tìm** tính năng **Payouts**
3. **Nhấp** vào **Add** nếu chưa kích hoạt
4. **Gửi yêu cầu phê duyệt** nếu sử dụng chế độ Live (phê duyệt mất 1-2 ngày làm việc)

### Bước 4: Thêm nhà cung cấp trong Spwig

Bây giờ thêm tài khoản PayPal vào Spwig:

1. **Di chuyển** đến **Settings > Payout Providers**
2. **Nhấp** vào **+ Add PayPal Account**
3. **Điền vào biểu mẫu**:
   - **Tên tài khoản**: Nhãn mô tả (ví dụ: "Main PayPal Account")
   - **Client ID**: Dán từ Bảng điều khiển nhà phát triển PayPal
   - **Client Secret**: Dán từ Bảng điều khiển nhà phát triển PayPal
   - **Chế độ**: Chọn Sandbox (kiểm tra) hoặc Production (sản phẩm)
   - **Is Active**: Chọn để kích hoạt
4. **Nhấp Save**

Spwig xác minh thông tin xác thực bằng cách yêu cầu một token truy cập. Nếu xác minh thất bại, hãy kiểm tra lại Client ID và Secret của bạn.

### Bước 5: Kiểm tra kết nối

Kiểm tra tích hợp PayPal của bạn:

1. Tạo khoản thanh toán kiểm tra trong **Affiliate Program > Payouts**
2. Sử dụng email PayPal của riêng bạn làm người nhận
3. Đặt số tiền là $0.01 (nếu đang ở chế độ Production) hoặc bất kỳ số tiền nào (nếu Sandbox)
4. Xử lý bằng nhà cung cấp
5. Kiểm tra tài khoản PayPal để xem khoản thanh toán đến
6. Xác nhận webhook cập nhật trạng thái khoản thanh toán trong Spwig

Nếu đang sử dụng chế độ Sandbox, tạo tài khoản PayPal kiểm tra tại [PayPal Sandbox](https://developer.paypal.com/dashboard/accounts) để nhận các khoản thanh toán kiểm tra.

## Cài đặt Airwallex

Airwallex hỗ trợ chuyển khoản ngân hàng quốc tế cho các đại lý ưa thích chuyển khoản trực tiếp.

### Yêu cầu trước

Trước khi bắt đầu, bạn cần:
- Tài khoản Airwallex (tạo tại [airwallex.com](https://www.airwallex.com))
- Trạng thái tài khoản doanh nghiệp đã được xác minh
- Bật quyền truy cập API (liên hệ hỗ trợ Airwallex nếu cần)
- Số dư đủ trong tài khoản Airwallex của bạn

### Bước 1: Tạo thông tin xác thực API

1. **Đăng nhập** vào [Bảng điều khiển Airwallex](https://www.airwallex.com/app/)
2. **Di chuyển** đến **Settings > API Keys**
3. **Nhấp** vào **Create API Key**
4. **Nhập mô tả**: "Spwig Affiliate Payouts"
5. **Chọn quyền truy cập**: Bật **Payouts** (đọc và ghi)
6. **Nhấp** vào **Generate**
7. **Sao chép API Key** — Chỉ hiển thị một lần
8. **Sao chép Client ID** — Hiển thị cùng với khóa

### Bước 2: Ghi chú môi trường của bạn

Airwallex cung cấp hai môi trường:

- **Demo**: Để kiểm tra với các giao dịch giả
- **Production**: Để chuyển khoản thật tiền

Đảm bảo bạn biết môi trường nào mà khóa API của bạn thuộc về.

### Bước 3: Thêm nhà cung cấp trong Spwig

Thêm tài khoản Airwallex vào Spwig:

1. **Di chuyển** đến **Settings > Payout Providers**
2. **Nhấp** vào **+ Add Airwallex Account**
3. **Điền vào biểu mẫu**:
   - **Tên tài khoản**: Nhãn mô tả (ví dụ: "Airwallex EUR Account")
   - **API Key**: Dán từ bảng điều khiển Airwallex
   - **Client ID**: Dán từ bảng điều khiển Airwallex
   - **Môi trường**: Chọn Demo hoặc Production
   - **Is Active**: Chọn để kích hoạt
4. **Nhấp Save**

Spwig xác minh thông tin xác thực bằng cách truy vấn số dư tài khoản của bạn.

### Bước 4: Xác nhận các quốc gia được hỗ trợ

Airwallex hỗ trợ chuyển khoản đến nhiều quốc gia nhưng không phải tất cả. Kiểm tra trang [Airwallex coverage](https://www.airwallex.com/global-business-account/global-transfers) để xác nhận các quốc gia đại lý của bạn được hỗ trợ.

Các quốc gia được hỗ trợ phổ biến bao gồm:
- Hoa Kỳ
- Vương quốc Anh
- Các nước thuộc Liên minh châu Âu
- Úc
- Canada
- Singapore
- Hồng Kông

### Bước 5: Kiểm tra chuyển khoản ngân hàng

Kiểm tra tích hợp Airwallex của bạn:

1. Tạo khoản thanh toán kiểm tra cho đại lý có thông tin ngân hàng
2. Sử dụng một số tiền nhỏ ($1-$5) nếu đang ở chế độ Production
3. Xử lý bằng nhà cung cấp
4. Kiểm tra bảng điều khiển Airwallex để xem giao dịch
5. Chờ xác nhận webhook
6. Xác nhận khoản thanh toán hoàn tất trong Spwig

Chế độ Demo xử lý ngay lập tức. Chế độ Production mất 2-5 ngày làm việc.

## Logic lựa chọn nhà cung cấp

Khi bạn xử lý khoản thanh toán, Spwig tự động chọn nhà cung cấp phù hợp dựa trên phương thức thanh toán của đại lý.

### Luồng lựa chọn

1. **Kiểm tra phương thức thanh toán đại lý**:
   - Nếu `payment_email` được thiết lập → Đại lý ưa thích PayPal
   - Nếu thông tin ngân hàng được thiết lập → Đại lý ưa thích chuyển khoản ngân hàng
2. **Đối sánh với nhà cung cấp**:
   - Email PayPal → Sử dụng tài khoản nhà cung cấp PayPal đang hoạt động
   - Thông tin ngân hàng → Sử dụng tài khoản nhà cung cấp Airwallex đang hoạt động
3. **Chuyển sang nhà cung cấp đầu tiên có sẵn** nếu nhà cung cấp được ưa thích không được cấu hình
4. **Hiển thị lỗi** nếu không có nhà cung cấp nào phù hợp

### Nhiều tài khoản nhà cung cấp

Bạn có thể cấu hình nhiều tài khoản cho cùng một nhà cung cấp (ví dụ: hai tài khoản PayPal cho các khu vực khác nhau). Spwig chọn tài khoản đang hoạt động đầu tiên phù hợp với phương thức thanh toán. Để kiểm soát tài khoản nào được sử dụng, hãy sắp xếp lại chúng trong danh sách quản trị hoặc chỉ thiết lập một tài khoản là đang hoạt động.

## Kiểm tra tích hợp thanh toán

Luôn kiểm tra tích hợp nhà cung cấp của bạn trước khi xử lý các khoản thanh toán thực tế cho đại lý.

### Kiểm tra chế độ Sandbox/Demo

1. **Chuyển nhà cung cấp sang chế độ Sandbox** (PayPal Sandbox hoặc Airwallex Demo)
2. **Tạo đại lý kiểm tra** với thông tin thanh toán kiểm tra
3. **Tạo hoa hồng kiểm tra** và phê duyệt chúng
4. **Tạo khoản thanh toán kiểm tra** bao gồm các hoa hồng đó
5. **Xử lý bằng nhà cung cấp** sử dụng menu hành động
6. **Theo dõi nhật ký Celery** cho các yêu cầu API
7. **Kiểm tra bảng điều khiển nhà cung cấp** cho giao dịch
8. **Chờ webhook** để cập nhật trạng thái khoản thanh toán
9. **Xác nhận hoa hồng được đánh dấu là đã thanh toán**

### Kiểm tra chế độ Production

Trước khi chuyển sang chế độ sản xuất:

1. **Chuyển sang chế độ sản xuất** trong cài đặt nhà cung cấp
2. **Tạo khoản thanh toán kiểm tra nhỏ** cho chính bạn ($0.01-$1.00)
3. **Xử lý nó** và chờ hoàn tất
4. **Xác nhận tiền đã nhận** trong tài khoản của bạn
5. **Kiểm tra webhook đã được kích hoạt** và cập nhật trạng thái
6. **Xem lại phí giao dịch của nhà cung cấp**

### Các vấn đề kiểm tra phổ biến

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|------------|----------|
| "Thông tin xác thực không hợp lệ" | Khóa API sai hoặc không khớp chế độ | Kiểm tra lại thông tin xác thực, xác nhận sandbox vs sản xuất |
| Webhook không bao giờ kích hoạt | URL không được cấu hình trong nhà cung cấp | Thêm URL webhook trong bảng điều khiển nhà cung cấp |
| Khoản thanh toán vẫn ở trạng thái Xử lý | Ký tên webhook thất bại | Kiểm tra xem khóa bí mật webhook có khớp không |
| Không có nhà cung cấp nào có sẵn | Không có nhà cung cấp đang hoạt động cho phương thức thanh toán | Kích hoạt ít nhất một tài khoản nhà cung cấp |

## Xử lý theo lô (PayPal)

PayPal hỗ trợ xử lý theo lô để tăng hiệu quả và tiết kiệm chi phí.

### Cách xử lý theo lô hoạt động

Khi bạn chọn nhiều khoản thanh toán và nhấp **Process with Provider**:

1. Spwig nhóm tất cả các khoản thanh toán PayPal thành một lô duy nhất
2. Hệ thống gửi một yêu cầu API duy nhất với tất cả chi tiết thanh toán (tối đa 15.000)
3. PayPal xử lý toàn bộ lô như một giao dịch duy nhất
4. Webhook trả về với kết quả theo lô
5. Spwig cập nhật tất cả các khoản thanh toán dựa trên phản hồi theo lô

### Lợi ích của xử lý theo lô

- **Giảm số lần gọi API** — Một yêu cầu cho hàng trăm khoản thanh toán
- **Giảm phí** — Một số cấu trúc phí PayPal ưu tiên xử lý theo lô
- **Xử lý nhanh hơn** — Thực thi song song cho toàn bộ lô
- **Webhook duy nhất** — Dễ dàng giám sát và ghi nhật ký

### Giới hạn theo lô

PayPal áp dụng các giới hạn sau:
- Tối đa 15.000 người nhận mỗi lô
- Tối đa $100.000 tổng cộng mỗi lô
- Thời gian xử lý thường hoàn tất trong vài phút

Nếu bạn vượt quá 15.000 khoản thanh toán, Spwig tự động chia thành nhiều lô.

## Xử lý từng khoản (Airwallex)

Airwallex xử lý các khoản thanh toán một cách riêng lẻ, điều này mang lại các ưu nhược điểm khác nhau.

### Cách xử lý từng khoản hoạt động

Khi bạn xử lý các khoản thanh toán Airwallex:

1. Hệ thống gửi yêu cầu API riêng biệt cho mỗi khoản thanh toán
2. Airwallex xếp hàng các chuyển khoản riêng lẻ
3. Mỗi chuyển khoản hoàn tất độc lập (2-5 ngày)
4. Webhook cá nhân kích hoạt khi mỗi chuyển khoản hoàn tất
5. Spwig cập nhật các khoản thanh toán khi webhook đến

### Lợi ích của xử lý từng khoản

- **Phân tách lỗi tốt hơn** — Một lỗi không làm chặn các khoản khác
- **Theo dõi từng khoản thanh toán** — ID giao dịch từng khoản
- **Thông tin thanh toán chi tiết hơn** — Thông tin cụ thể cho mỗi chuyển khoản
- **Thời gian linh hoạt** — Các chuyển khoản hoàn tất ở các tốc độ khác nhau

### Thời gian xử lý

Khác với việc xử lý theo lô tức thời của PayPal, các chuyển khoản Airwallex mất nhiều thời gian hơn:
- Chuyển khoản trong nước: 1-2 ngày làm việc
- Chuyển khoản quốc tế: 3-5 ngày làm việc
- Một số quốc gia: Đến 7 ngày làm việc

Hãy thiết lập kỳ vọng của đại lý phù hợp trong điều khoản chương trình của bạn.

## Cấu hình Webhook

Webhook cho phép cập nhật trạng thái khoản thanh toán tự động khi nhà cung cấp hoàn tất giao dịch.

### Định dạng URL Webhook

Cấu hình URL này trong bảng điều khiển nhà cung cấp của bạn:

```
https://yourdomain.com/api/payout-providers/{provider}/webhook/
```

Thay thế `{provider}` bằng:
- `paypal` cho webhook PayPal
- `airwallex` cho webhook Airwallex

Ví dụ:
- `https://shop.example.com/api/payout-providers/paypal/webhook/`
- `https://shop.example.com/api/payout-providers/airwallex/webhook/`

### Cấu hình Webhook PayPal

1. **Di chuyển** đến [Bảng điều khiển nhà phát triển PayPal](https://developer.paypal.com/dashboard/)
2. **Nhấp** vào tên ứng dụng của bạn
3. **Cuộn xuống** phần **Webhooks**
4. **Nhấp** vào **Add Webhook**
5. **Nhập URL webhook** (định dạng trên)
6. **Chọn sự kiện**:
   - `PAYMENT.PAYOUTSBATCH.SUCCESS`
   - `PAYMENT.PAYOUTSBATCH.DENIED`
   - `PAYMENT.PAYOUTS-ITEM.SUCCEEDED`
   - `PAYMENT.PAYOUTS-ITEM.FAILED`
7. **Nhấp Save**

PayPal cung cấp khóa ký webhook. Spwig sử dụng khóa này để xác minh tính xác thực của webhook.

### Cấu hình Webhook Airwallex

1. **Di chuyển** đến [Bảng điều khiển Airwallex](https://www.airwallex.com/app/)
2. **Di chuyển đến** **Settings > Webhooks**
3. **Nhấp** vào **Create Webhook**
4. **Nhập URL webhook** (định dạng trên)
5. **Chọn sự kiện**:
   - `transfer.created`
   - `transfer.completed`
   - `transfer.failed`
6. **Nhấp Create**

Airwallex ký webhook bằng khóa bí mật API của bạn.

### Bảo mật Webhook

Webhook được xác minh bằng các cơ chế sau:

- **Kiểm tra chữ ký** — Nhà cung cấp ký payload webhook bằng khóa bí mật
- **Kiểm tra thời gian** — Từ chối webhook cũ (ngăn chặn cuộc tấn công lặp lại)
- **Danh sách IP cho phép (tùy chọn)** — Giới hạn chỉ đến các dải IP của nhà cung cấp
- **Yêu cầu HTTPS** — Webhook chỉ hoạt động qua SSL

Không bao giờ tắt kiểm tra chữ ký trong môi trường sản xuất.

### Kiểm tra Webhook

Hầu hết nhà cung cấp cung cấp công cụ kiểm tra webhook:

**PayPal**: Sử dụng công cụ "Simulator" trong Bảng điều khiển nhà phát triển để kích hoạt webhook kiểm tra

**Airwallex**: Tạo chuyển khoản kiểm tra trong chế độ Demo và theo dõi webhook

Bạn cũng có thể kiểm tra nhật ký webhook trong Spwig tại **Settings > System Logs** (nếu đã bật nhật ký).

## Khắc phục sự cố

### Lỗi thông tin xác thực không hợp lệ

**Triệu chứng**: "Đăng nhập thất bại" khi lưu tài khoản nhà cung cấp

**Nguyên nhân**:
- Client ID hoặc Secret sai
- Sử dụng thông tin xác thực Sandbox trong chế độ Production (hoặc ngược lại)
- Khóa API đã hết hạn hoặc bị hủy bỏ
- Tài khoản chưa được xác minh

**Giải pháp**:
- Sao chép lại thông tin xác thực từ bảng điều khiển nhà cung cấp
- Xác minh chế độ khớp (sandbox vs sản xuất)
- Tạo lại khóa API
- Liên hệ hỗ trợ nhà cung cấp để xác minh trạng thái tài khoản

### Không nhận được webhook

**Triệu chứng**: Khoản thanh toán bị kẹt ở trạng thái "Processing" mãi mãi

**Nguyên nhân**:
- URL webhook chưa được cấu hình trong bảng điều khiển nhà cung cấp
- Chứng chỉ HTTPS không hợp lệ
- Tường lửa chặn IP của nhà cung cấp
- Kiểm tra chữ ký webhook không thành công

**Giải pháp**:
- Kiểm tra lại URL webhook trong cài đặt nhà cung cấp
- Xác minh chứng chỉ SSL hợp lệ
- Cho phép IP của nhà cung cấp trong tường lửa
- Kiểm tra nhật ký Celery để tìm lỗi chữ ký
- Kiểm tra webhook bằng công cụ mô phỏng của nhà cung cấp

### Khoản thanh toán thất bại

**Triệu chứng**: Trạng thái khoản thanh toán thay đổi thành "Failed" kèm theo thông báo lỗi

**Nguyên nhân**:
- Thông tin thanh toán đại lý không hợp lệ (email hoặc tài khoản ngân hàng sai)
- Số dư không đủ trong tài khoản nhà cung cấp
- Tài khoản người nhận không thể nhận thanh toán
- Quốc gia không được hỗ trợ (Airwallex)
- Khoản thanh toán vượt quá giới hạn của nhà cung cấp

**Giải pháp**:
- Xem lại lỗi trong trường **Provider Response**
- Xác minh thông tin thanh toán đại lý là chính xác
- Nạp thêm tiền vào tài khoản nhà cung cấp
- Yêu cầu đại lý kiểm tra trạng thái tài khoản của họ
- Kiểm tra hỗ trợ quốc gia và tiền tệ của nhà cung cấp
- Chia nhỏ các khoản thanh toán lớn nếu vượt quá giới hạn

### Mismatch chế độ

**Triệu chứng**: Các khoản thanh toán kiểm tra hoạt động nhưng các khoản thanh toán sản xuất thất bại

**Nguyên nhân**:
- Nhà cung cấp được đặt ở chế độ Sandbox nhưng sử dụng tài khoản đại lý sản xuất
- Khóa API đến từ môi trường sai

**Giải pháp**:
- Chuyển chế độ nhà cung cấp sang Production
- Tạo lại khóa API sản xuất
- Xác minh URL webhook trỏ đến miền sản xuất

## Các thực hành bảo mật tốt nhất

Bảo vệ tích hợp thanh toán của bạn bằng các biện pháp bảo mật sau:

### Lưu trữ thông tin xác thực

- **Không bao giờ lưu trữ thông tin xác thực vào kiểm soát phiên bản** — Sử dụng biến môi trường hoặc lưu trữ an toàn
- **Làm mới khóa API mỗi quý** — Tạo khóa mới mỗi 3 tháng
- **Sử dụng khóa riêng biệt cho Sandbox và Production** — Không bao giờ trộn lẫn môi trường
- **Hạn chế quyền API** — Chỉ cấp quyền Payouts, không cấp quyền kiểm soát toàn bộ tài khoản

Spwig lưu trữ thông tin xác thực nhà cung cấp được mã hóa trong cơ sở dữ liệu. Đảm bảo sao lưu cơ sở dữ liệu của bạn an toàn.

### Bảo mật Webhook

- **Luôn xác minh chữ ký** — Không bao giờ bỏ qua xác minh chữ ký
- **Sử dụng HTTPS duy nhất** — Không hỗ trợ webhook HTTP
- **Thực hiện danh sách IP cho phép** — Giới hạn webhook chỉ đến các dải IP của nhà cung cấp
- **Ghi lại tất cả webhook** — Giám sát để phát hiện hoạt động đáng ngờ
- **Giới hạn tốc độ webhook** — Ngăn chặn việc lạm dụng

### Kiểm soát truy cập

- **Hạn chế quyền truy cập của nhân viên** — Chỉ những nhân viên tin cậy mới nên xử lý các khoản thanh toán
- **Sử dụng xác thực hai yếu tố** — Yêu cầu xác thực 2FA cho tài khoản nhân viên
- **Kiểm toán các hành động thanh toán** — Xem xét ai đã xử lý khoản thanh toán nào
- **Phân chia nhiệm vụ** — Nhân viên khác nhau xử lý việc phê duyệt và xử lý

### Giám sát

- **Kiểm tra các khoản thanh toán thất bại hàng ngày** — Giải quyết vấn đề kịp thời
- **Giám sát số dư tài khoản nhà cung cấp** — Đảm bảo có đủ tiền
- **Xem xét nhật ký giao dịch hàng tuần** — Phát hiện bất thường sớm
- **Thiết lập cảnh báo** — Thông báo qua email cho các khoản thanh toán lớn hoặc thất bại

## Một số mẹo

- Luôn kiểm tra tích hợp của bạn kỹ lưỡng trong chế độ Sandbox trước khi chuyển sang Production — phát hiện vấn đề với tiền giả.
- Cấu hình cả PayPal và Airwallex để cho đại lý lựa chọn phương thức thanh toán — các đại lý khác nhau ưa thích các phương thức khác nhau.
- Thiết lập URL webhook trong quá trình cài đặt ban đầu và xác nhận chúng kích hoạt đúng — webhook rất quan trọng cho tự động hóa.
- Luôn đảm bảo số dư tài khoản nhà cung cấp được nạp đầy để tránh các khoản thanh toán thất bại trong quá trình xử lý theo lô.
- Sử dụng tên tài khoản mô tả nếu bạn cấu hình nhiều nhà cung cấp (ví dụ: "PayPal USD", "PayPal EUR").
- Làm mới khóa xác thực API mỗi quý theo thực hành bảo mật.
- Ghi lại URL webhook và thông tin xác thực trong một quản lý mật khẩu an toàn chia sẻ với nhóm của bạn.
- Giám sát các khoản thanh toán thất bại ngay lập tức — sự chậm trễ làm phiền đại lý và làm tổn hại đến danh tiếng chương trình.
- Luôn sử dụng HTTPS cho cài đặt Spwig của bạn — webhook yêu cầu chứng chỉ SSL.
- Liên hệ hỗ trợ nhà cung cấp nếu bạn gặp phải lỗi liên tục — họ có thể xác minh trạng thái tài khoản và quyền của bạn.