---
title: Cài đặt màn hình khách hàng POS
---

screenshots-needed

core/static/core/admin/img/help/pos-customer-display-setup/

paragraph

Màn hình khách hàng là màn hình thứ hai hướng về phía khách hàng trong quá trình bán hàng. Trong khi bạn xử lý giao dịch, khách hàng sẽ thấy từng mặt hàng khi được quét, tổng số tiền đang chạy, phân tích giá và thuế, và - khi không có giao dịch nào đang diễn ra - một slide show xoay vòng nội dung khuyến mãi của bạn.

paragraph

Hướng dẫn này bao gồm phần phần cứng và ghép nối khi thiết lập màn hình khách hàng của bạn: bật tính năng trên thiết bị đầu cuối, ghép nối thiết bị riêng biệt làm màn hình hiển thị, và xử lý các tình huống thiết lập phổ biến. Để biết thông tin về các slide khuyến mãi được hiển thị trong thời gian rảnh, xem [Slide khuyến mãi màn hình khách hàng](customer-display-promo-slides).

heading

Nội dung màn hình khách hàng hiển thị

paragraph

Khi có giao dịch đang diễn ra, màn hình khách hàng sẽ hiển thị:

list

paragraph

Khi thiết bị đầu cuối không hoạt động (không có giao dịch đang diễn ra), màn hình sẽ chuyển sang slide show khuyến mãi. Bạn kiểm soát nội dung của slide show này riêng biệt - xem [Slide khuyến mãi màn hình khách hàng](customer-display-promo-slides).

heading

Các thiết lập phần cứng phổ biến

paragraph

Có ba cách thực tế để thiết lập màn hình hướng khách:

list

heading

Bật màn hình khách hàng trên thiết bị đầu cuối

paragraph

Tính năng màn hình khách hàng được bật theo từng thiết bị đầu cuối thông qua cấu hình phần cứng của thiết bị đầu cuối.

list

code-block

{'customer_display': true}

paragraph

Nếu trường đã chứa các cài đặt phần cứng khác (như cấu hình máy in hoặc máy quét), thêm "customer_display": true cùng với chúng:

code-block

{'printer': 'HP LaserJet', 'scanner': 'Datalogic', 'customer_display': true}

list

image

![Cấu hình phần cứng thiết bị đầu cuối với customer_display được bật](/static/core/admin/img/help/pos-customer-display-setup/terminal-capabilities-toggle.webp)

paragraph

Sau khi bật, ứng dụng POS trên thiết bị đầu cuối đó sẽ mở màn hình hiển thị khách hàng trong một cửa sổ trình duyệt hoặc tab thứ hai khi phiên bắt đầu.

heading

Ghép nối thiết bị riêng biệt làm màn hình hiển thị

paragraph

Nếu bạn đang sử dụng thiết bị vật lý riêng biệt cho màn hình khách hàng (một máy tính bảng, điện thoại hoặc máy tính thứ hai), bạn ghép nối nó với thiết bị đầu cuối bằng một mã 6 chữ số có thời hạn ngắn.

heading

Bước 1: Tạo mã ghép nối trên thiết bị đầu cuối chính

Mở ứng dụng POS trên thiết bị đầu cuối chính của bạn và vào phần cài đặt hiển thị hoặc phần ghép nối của giao diện thiết bị đầu cuối.

Yêu cầu mã ghép nối hiển thị mới.

Mã là một số 6 chữ số và có hiệu lực trong **5 phút**.

Khi bạn tạo mã mới, bất kỳ mã nào chưa sử dụng trước đó cho thiết bị đầu cuối này sẽ tự động bị hủy.

### Bước 2: Mở URL hiển thị trên thiết bị khách hàng

Trên thiết bị dành cho khách hàng, mở trình duyệt web và truy cập:

```
https://your-store-domain.com/pos/display/
```

Không cần đăng nhập — trang hiển thị là công khai. Điều này là cố ý: thiết bị hiển thị không cần thông tin xác thực của nhân viên, và mã ghép nối cung cấp liên kết giữa hiển thị và thiết bị đầu cuối đúng.

![Giao diện hiển thị khách hàng khi không hoạt động](/static/core/admin/img/help/pos-customer-display-setup/customer-display-view.webp)

### Bước 3: Nhập mã ghép nối

Trên thiết bị khách hàng, nhập mã 6 chữ số từ thiết bị đầu cuối chính. Hiển thị sẽ ghép nối với thiết bị đầu cuối đó và bắt đầu hiển thị dữ liệu giỏ hàng trực tiếp.

Sau khi mã được sử dụng, nó sẽ bị vô hiệu hóa ngay lập tức và không thể sử dụng lại.

## Tạo lại mã ghép nối

Nếu mã ghép nối hết hạn trước khi bạn có thể nhập nó, hoặc nếu bạn cần ghép nối lại thiết bị hiển thị (ví dụ, nếu thiết bị hiển thị bị thay thế hoặc đặt lại), hãy tạo mã mới từ ứng dụng POS trên thiết bị đầu cuối chính.

Việc tạo mã mới sẽ tự động hủy bất kỳ mã nào chưa sử dụng trước đó cho thiết bị đầu cuối đó. Mã mới có hiệu lực trong 5 phút.

Bạn không cần thay đổi bất cứ thứ gì trong phần quản trị để tạo lại mã — việc này được thực hiện hoàn toàn trong ứng dụng POS.

## Cấu hình nhiều màn hình trên một thiết bị

Nếu thiết bị đầu cuối chính của bạn là một laptop hoặc máy tính để bàn có hai màn hình:

1. Kết nối màn hình thứ hai và đặt nó ở chế độ **mở rộng màn hình** trong cài đặt hiển thị của hệ điều hành (không phải chế độ phản chiếu).
2. Mở ứng dụng POS trên màn hình chính như bình thường.
3. Ứng dụng POS sẽ mở hiển thị khách hàng trong một cửa sổ thứ hai. Kéo cửa sổ đó sang màn hình thứ hai.
4. Tối đa hóa hoặc chuyển sang chế độ toàn màn hình trên màn hình thứ hai.

Không cần mã ghép nối vì cả hai cửa sổ đều chạy trên cùng một thiết bị và giao tiếp trực tiếp.

## Hành vi khi không hoạt động

Khi không có giao dịch nào đang diễn ra, màn hình khách hàng sẽ hiển thị một slideshow xoay vòng của các hình ảnh quảng cáo. Bạn tạo và quản lý các slide này riêng biệt dưới mục **POS > Promo Slides**.

Để biết chi tiết về cách tạo slide, nhắm mục tiêu chúng đến các cửa hàng cụ thể và quản lý nội dung theo mùa, xem [Customer Display Promo Slides](customer-display-promo-slides).

Nếu không có slide nào được cấu hình, màn hình sẽ hiển thị một màn hình chào mừng đơn giản với tên cửa hàng của bạn.

## Khắc phục sự cố

**Màn hình hiển thị trở nên tối hoặc ngừng cập nhật**

Màn hình hiển thị giao tiếp với thiết bị đầu cuối chính theo thời gian thực. Nếu kết nối bị gián đoạn, màn hình có thể trở nên tối hoặc hiển thị dữ liệu lỗi thời. Làm mới trình duyệt trên thiết bị khách hàng. Nếu điều này không giúp được, hãy tạo mã ghép nối mới và ghép nối lại.

**Màn hình hiển thị đang hiển thị giỏ hàng của thiết bị đầu cuối sai**

Mỗi màn hình hiển thị được ghép nối với một thiết bị đầu cuối cụ thể. Nếu bạn có nhiều thiết bị đầu cuối, hãy đảm bảo rằng bạn đã tạo mã ghép nối trên thiết bị đầu cuối đúng và nhập mã đó trên màn hình hiển thị. Để khắc phục sự không khớp, hãy tạo mã mới trên thiết bị đầu cuối đúng và ghép nối lại thiết bị hiển thị.

**Mã ghép nối đã hết hạn trước khi tôi có thể nhập nó**

Các mã có hiệu lực trong 5 phút. Tạo mã mới từ ứng dụng POS và nhập mã đó trên thiết bị hiển thị ngay lập tức. Giữ hai thiết bị gần nhau trong quá trình ghép nối.

**Mã ghép nối đã được nhập nhưng màn hình hiển thị không kết nối**

Kiểm tra xem thiết bị khách hàng có thể truy cập được tên miền cửa hàng của bạn (nó cần quyền truy cập mạng). Ngoài ra, hãy xác nhận rằng `"customer_display": true` được đặt trong cấu hình phần cứng của thiết bị đầu cuối và thiết bị đầu cuối đã được lưu.

**URL hiển thị trả về lỗi**

Đảm bảo bạn đang điều hướng đến `/pos/display/` trên tên miền cửa hàng của bạn, không phải URL quản trị. Trang xem hiển thị không yêu cầu đăng nhập — nếu bạn được yêu cầu đăng nhập, hãy kiểm tra lại URL.

## Mẹo

Bảo tồn toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- **Giữ phiên ghép nối ngắn** — hãy để thiết bị của khách hàng sẵn sàng và mở trình duyệt đến `/pos/display/` trước khi tạo mã ghép nối.

Bạn có 5 phút, nhưng hoàn thành trong vòng một phút sẽ tránh được việc hết thời gian.
- **Kiểm tra trước khi mở** — thực hiện một giao dịch kiểm tra với màn hình hiển thị được kết nối để đảm bảo khách hàng sẽ thấy các mặt hàng và tổng số tiền chính xác trước giao dịch thực tế đầu tiên của bạn.
- **Đánh dấu URL hiển thị** — thiết lập trình duyệt trên thiết bị khách hàng để mở `/pos/display/` khi khởi động để luôn sẵn sàng.
- **Sử dụng màn hình mở rộng để đơn giản hóa** — nếu máy tính của bạn có cổng HDMI dự phòng và màn hình có sẵn, phương pháp màn hình mở rộng không yêu cầu ghép nối liên tục và không bao giờ hết hạn.
- **Thêm slide khuyến mãi trước khi mở** — một màn hình hiển thị chỉ hiển thị màn hình chào mừng trống là bỏ lỡ cơ hội.

Cài đặt ít nhất vài slide khuyến mãi để màn hình hiển thị hữu ích ngay cả khi không có giao dịch nào đang diễn ra.

Xem [Slide khuyến mãi hiển thị khách hàng](customer-display-promo-slides).
- **Bảo vệ thiết bị hiển thị** — URL hiển thị được thiết kế để truy cập công khai, nhưng nó chỉ hiển thị dữ liệu giỏ hàng trực tiếp khi được ghép nối với máy tính đầu cuối đang hoạt động.

Tuy nhiên, hãy xem xét chế độ trình duyệt kiosk trên thiết bị khách hàng để ngăn khách hàng truy cập các trang khác.