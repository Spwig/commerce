---
title: Tổng quan hệ thống POS
---

Hệ thống POS của Spwig biến cửa hàng của bạn thành một giải pháp bán lẻ hoàn chỉnh với các máy bán hàng hiện đại. Triển khai vô số máy bán hàng tại vô số địa điểm với phí cấp phép cố định €499/năm. Mỗi máy bán hàng là một ứng dụng Web Tiến bộ (PWA) có thể hoạt động ngoại tuyến, đồng bộ tự động và tích hợp liền mạch với kho hàng, dữ liệu khách hàng và xử lý thanh toán của bạn. Quản lý mọi thứ từ bảng điều khiển quản trị—cấu hình máy bán hàng, đối chiếu ca làm việc, tùy chỉnh biên lai và tích hợp phần cứng.

Sử dụng hệ thống POS khi bạn có các địa điểm bán lẻ vật lý, cửa hàng di động, hội chợ thương mại hoặc bất kỳ môi trường nào mà khách hàng mua hàng trực tiếp thay vì trực tuyến.

![Bảng điều khiển POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Spwig POS là gì?

Spwig POS là hệ thống điểm bán hàng được tích hợp đầy đủ dành cho các nhà bán hàng bán cả trực tuyến và tại các địa điểm vật lý. Khác với các hệ thống POS bên thứ ba yêu cầu tích hợp phức tạp, Spwig POS được xây dựng trực tiếp vào nền tảng của bạn, đảm bảo đồng bộ dữ liệu hoàn hảo trên tất cả các kênh bán hàng.

**Đặc điểm chính**:
- **Máy bán hàng không giới hạn** - Triển khai nhiều máy bán hàng cần thiết mà không phát sinh chi phí
- **Kiến trúc ưu tiên ngoại tuyến** - Tiếp tục xử lý bán hàng ngay cả khi mất kết nối internet
- **Ứng dụng Web Tiến bộ** - Không cần cài đặt từ cửa hàng ứng dụng; truy cập qua trình duyệt trên bất kỳ thiết bị nào (máy tính bảng, máy tính, máy bán hàng chuyên dụng)
- **Đồng bộ tồn kho thực tế** - Đặt hàng tồn kho (15 phút TTL) ngăn việc bán quá số lượng trên các kênh
- **Hỗ trợ thanh toán chia nhỏ** - Chấp nhận nhiều phương thức thanh toán cho mỗi giao dịch (tiền mặt + thẻ + thẻ quà tặng)
- **Tích hợp phần cứng** - Máy in nhiệt ESC/POS, máy quét mã vạch, ngăn kéo đựng tiền, màn hình khách hàng
- **Quản lý ca làm việc** - Đối chiếu tiền mặt với số lượng mở/closing và theo dõi chênh lệch
- **Sẵn sàng cho nhiều địa điểm** - Nhóm cửa hàng với cài đặt kế thừa cho quản lý nhượng quyền và khu vực

## Cấp phép và Kích hoạt

**Giá cố định**: €499 mỗi năm bao gồm vô số máy bán hàng tại vô số địa điểm. Không có phí mỗi máy bán hàng, không có phí giao dịch, không có chi phí ẩn.

**Định dạng cấp phép**: `POS-XXXX-XXXX-XXXX-XXXX` (cung cấp sau khi mua hàng)

**Kích hoạt**: Nhập khóa cấp phép của bạn tại **Cài đặt > Cấp phép POS**. Hệ thống xác minh với máy chủ cấp phép của Spwig và kích hoạt tất cả tính năng POS ngay lập tức. Cấp phép bao gồm 14 ngày ân hạn sau khi hết hạn để cho phép xử lý thanh toán chậm trễ.

**Bạn nhận được gì**:
- Đăng ký máy bán hàng không giới hạn
- Phân công nhân viên không giới hạn
- Tất cả tính năng POS (ca làm việc, quản lý tiền mặt, tùy chỉnh biên lai, màn hình khách hàng)
- Tích hợp nhà cung cấp thanh toán (Stripe Terminal và hệ thống nhà cung cấp mở rộng)
- Hỗ trợ tích hợp phần cứng
- Cập nhật và sửa lỗi trong thời gian cấp phép

Không có tính năng POS nào có thể truy cập được mà không có giấy phép hợp lệ—giao diện ghép nối máy bán hàng, quản lý ca làm việc và các trang quản trị POS đều yêu cầu kích hoạt.

## Kiến trúc Hệ thống

**Frontend** - Ứng dụng Web Tiến bộ React 18:
- Ưu tiên ngoại tuyến với lưu trữ Service Worker (hoạt động mà không cần internet)
- Hệ thống xây dựng Vite để tải nhanh
- CSS Modules + mã thiết kế (tương thích với chủ đề cửa hàng của bạn)
- IndexedDB để lưu trữ dữ liệu cục bộ
- 10 ngôn ngữ được hỗ trợ (Tiếng Anh, Tiếng Trung giản thể/đại tự, Tiếng Pháp, Tiếng Đức, Tiếng Tây Ban Nha, Tiếng Bồ Đào Nha, Tiếng Nhật, Tiếng Nga, Tiếng Ả Rập)

**Backend** - Tích hợp Backend:
- 13 mô hình POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, v.v.)
- 43+ điểm cuối REST API cho hoạt động máy bán hàng
- Hệ thống đặt hàng tồn kho với quản lý TTL
- Nhiệm vụ Celery cho đồng bộ nền sau
- Lưu trữ xác thực được mã hóa cho nhà cung cấp thanh toán

**Bảo mật**:
- Ghép nối máy bán hàng qua mã 8 ký tự (tạo trên máy chủ, hết hạn sau khi sử dụng)
- Kiểm soát phân công nhân viên xác định người dùng nào có thể truy cập máy bán hàng nào
- Khả năng khóa/giải khóa từ xa cho các tình huống khẩn cấp của quản trị
- Xác thực dựa trên phiên với hỗ trợ mở khóa sinh trắc học (phụ thuộc vào trình duyệt)

## Quy trình Bắt đầu

Thực hiện theo 5 bước sau để triển khai máy bán hàng POS đầu tiên của bạn:

**Bước 1: Kích hoạt giấy phép POS**
- Di chuyển đến **Cài đặt > Cấp phép POS**
- Nhập khóa cấp phép của bạn (`POS-XXXX-XXXX-XXXX-XXXX`)
- Xác minh giấy phép (yêu cầu kết nối internet)
- Xác nhận kích hoạt

**Bước 2: Tạo kho hàng**
- Di chuyển đến **Bảng mục > Kho hàng**
- Tạo kho hàng đại diện cho địa điểm bán lẻ của bạn
- Cấu hình địa chỉ và thông tin liên hệ
- Kho hàng này sẽ theo dõi tồn kho vật lý cho các giao dịch bán hàng POS

**Bước 3: Đăng ký máy bán hàng**
- Di chuyển đến **POS > Máy bán hàng**
- Nhấp vào **+ Thêm Máy bán hàng**
- Đặt tên máy bán hàng (ví dụ: "Bàn thu ngân chính", "Thanh toán 1")
- Gán kho hàng từ Bước 2
- Cấu hình cài đặt phần cứng (máy in, máy quét, ngăn kéo tiền)
- Lưu để tạo mã ghép nối 8 ký tự

**Bước 4: Phân công nhân viên**
- Trong cài đặt máy bán hàng, cuộn xuống **Người dùng được chỉ định**
- Chọn nhân viên được ủy quyền sử dụng máy bán hàng này
- Chỉ những người dùng được chỉ định mới có thể đăng nhập vào máy bán hàng
- Người dùng phải có quyền POS phù hợp trong vai trò nhân viên của họ

**Bước 5: Ghép nối thiết bị**
- Trên thiết bị máy bán hàng của bạn (máy tính bảng/máy tính), di chuyển đến URL `/pos/`
- Nhập mã ghép nối 8 ký tự từ Bước 3
- Máy bán hàng tải xuống cấu hình và đồng bộ dữ liệu ban đầu
- Đăng nhập bằng thông tin xác thực nhân viên được chỉ định
- Máy bán hàng sẵn sàng để bán hàng

Sau khi ghép nối, máy bán hàng sẽ tự động đồng bộ mỗi 5 phút (có thể cấu hình). Chế độ ngoại tuyến cho phép hoạt động tiếp tục khi không có kết nối internet—các giao dịch sẽ đồng bộ tự động khi kết nối quay lại.

## Tính năng POS Chính

**Xử lý bán hàng**:
- Tìm kiếm sản phẩm theo tên, SKU hoặc mã vạch
- Thanh toán chia nhỏ (nhiều phương thức thanh toán cho mỗi đơn hàng)
- Giỏ hàng tạm dừng (lưu các giao dịch chưa hoàn tất)
- Hoàn tiền và hủy bỏ với theo dõi lý do
- Áp dụng khuyến mãi (phiếu mua hàng, thẻ quà tặng, khuyến mãi)
- Tra cứu khách hàng và đổi điểm thành viên

**Quản lý tiền mặt**:
- Mở ca làm việc với số tiền mặt ban đầu
- Đóng ca làm việc với đối chiếu dự kiến và thực tế
- Các khoản chuyển tiền mặt (thêm tiền mặt, rút tiền lẻ với lý do)
- Tính toán tự động số tiền mặt dự kiến dựa trên doanh thu tiền mặt
- Theo dõi và báo cáo chênh lệch

**Tích hợp phần cứng**:
- Máy in biên lai nhiệt ESC/POS (mạng hoặc cổng nối tiếp)
- Máy quét mã vạch USB
- Kích hoạt ngăn kéo tiền qua xung máy in
- Màn hình hướng đến khách hàng (cuộn khuyến mãi khi không hoạt động)
- Máy đọc thẻ Stripe Terminal (S700, WisePOS E, P400)

**Khả năng ngoại tuyến**:
- Service Worker lưu trữ tất cả tài sản máy bán hàng
- IndexedDB lưu trữ các đơn hàng gần đây (có thể cấu hình: 7-30 ngày, 200-1000 đơn hàng)
- Đặt hàng tồn kho với TTL 15 phút ngăn việc bán quá số lượng
- Đợi bán hàng để đồng bộ khi kết nối quay lại
- Phát hiện kết nối lại tự động

## Trang quản trị POS

Truy cập các trang quản trị này để quản lý mọi khía cạnh triển khai POS của bạn:

**Bảng điều khiển POS** (`/admin/pos/`)
- Tổng quan hệ thống và thống kê nhanh
- Hoạt động máy bán hàng gần đây
- Tóm tắt ca làm việc đang hoạt động
- Trạng thái cấp phép và ngày hết hạn

**Quản lý máy bán hàng** (`/admin/pos_app/posterminal/`)
- Đăng ký và cấu hình máy bán hàng
- Gán nhân viên và kho hàng
- Theo dõi trạng thái trực tuyến/đang ngoại tuyến (theo dõi nhịp tim)
- Mở khóa máy bán hàng từ xa
- [Tìm hiểu thêm: Quản lý máy bán hàng POS](managing-pos-terminals)

**Quản lý ca làm việc** (`/admin/pos_app/posshift/`)
- Xem tất cả các ca làm việc (đang mở, đã đóng, lịch sử)
- Xem báo cáo đối chiếu tiền mặt
- Theo dõi các khoản chuyển tiền mặt và chênh lệch
- Kiểm toán hoạt động ca làm việc
- [Tìm hiểu thêm: Ca làm việc POS và Quản lý tiền mặt](pos-shifts-cash-management)

**Nhóm cửa hàng** (`/admin/pos_app/storegroup/`)
- Phân loại máy bán hàng theo vị trí/khu vực
- Cấu hình cài đặt cấp nhóm (tiền tệ, ngôn ngữ, múi giờ)
- Triển khai phân cấp cài đặt
- [Tìm hiểu thêm: Nhóm cửa hàng POS](pos-store-groups)

**Mẫu biên lai** (`/admin/pos_app/receipttemplate/`)
- Tùy chỉnh biên lai in (chiều rộng giấy, logo, tiêu đề/chân trang)
- Cấu hình trường tuân thủ (Mã số thuế, đăng ký kinh doanh)
- Thêm mã QR cho khuyến mãi
- Áp dụng mẫu cho cửa hàng hoặc nhóm cụ thể
- [Tìm hiểu thêm: Tùy chỉnh mẫu biên lai](receipt-template-customization)

**Trượt khuyến mãi** (`/admin/pos_app/promoslide/`)
- Tạo nội dung cuộn màn hình khách hàng
- Gắn trượt cho cửa hàng hoặc nhóm cụ thể
- Lên lịch khuyến mãi theo mùa
- [Tìm hiểu thêm: Trượt khuyến mãi hiển thị khách hàng](customer-display-promo-slides)

**Nhà cung cấp thanh toán** (`/admin/pos_app/posterminalprovider/`)
- Cấu hình tích hợp Stripe Terminal
- Quản lý thông tin xác thực nhà cung cấp thanh toán
- Theo dõi trạng thái kết nối
- [Tìm hiểu thêm: Nhà cung cấp thiết bị thanh toán](payment-terminal-providers)

**Máy đọc thẻ** (`/admin/pos_app/posterminalreader/`)
- Đăng ký máy đọc thẻ vật lý
- Gán máy đọc thẻ cho máy bán hàng
- Tùy chỉnh màn hình khởi động (thương hiệu màn hình hướng đến khách hàng)
- Theo dõi trạng thái máy đọc thẻ (trực tuyến/đang ngoại tuyến/bận)
- [Tìm hiểu thêm: Quản lý máy đọc thẻ](card-reader-management)

## Triển khai Nhiều Địa điểm

Đối với các nhà bán hàng có nhiều địa điểm bán lẻ, Spwig POS hỗ trợ kế thừa cài đặt theo cấp bậc:

**Cấp bậc cài đặt** (ưu tiên cao nhất đến thấp nhất):
1. Cài đặt cụ thể máy bán hàng (ghi đè tất cả)
2. Cài đặt cụ thể cửa hàng (ghi đè nhóm và trang web)
3. Cài đặt nhóm (ghi đè cài đặt trang web mặc định)
4. Cài đặt trang web mặc định (lựa chọn thay thế cho tất cả)

Cấu hình cài đặt chia sẻ tại cấp độ nhóm (ví dụ: tiền tệ khu vực, ngôn ngữ) và ghi đè khi cần cho cửa hàng hoặc máy bán hàng cụ thể. Xem [Nhóm cửa hàng POS](pos-store-groups) để có hướng dẫn cấu hình chi tiết.

## Mẹo

- **Bắt đầu với một máy bán hàng** - Kiểm tra thiết lập POS và quy trình làm việc với một máy bán hàng trước khi triển khai toàn bộ
- **Gán kho hàng trước khi ghép nối** - Máy bán hàng không thể xử lý bán hàng mà không có giao tiếp kho hàng
- **Cấu hình mẫu biên lai sớm** - Các trường tuân thủ (Mã số thuế) thay đổi theo khu vực; thiết lập trước khi đi vào hoạt động
- **Kiểm tra chế độ ngoại tuyến** - Ngắt kết nối internet và xác minh bán hàng tiếp tục; xác nhận đồng bộ khi kết nối lại
- **Sử dụng nhóm cửa hàng cho nhiều địa điểm** - Đơn giản hóa quản lý cấu hình cho triển khai nhượng quyền hoặc khu vực
- **Theo dõi trạng thái nhịp tim** - Máy bán hàng ping máy chủ mỗi 5 phút; máy bán hàng ngoại tuyến hiển thị trong bảng điều khiển quản trị
- **Cấu hình giới hạn đồng bộ để tối ưu hiệu suất** - Máy bán hàng có kết nối chậm có lợi từ cài đặt sync_days/sync_limit thấp hơn
- **Sao lưu cấu hình phần cứng** - Ghi lại địa chỉ IP máy in, cài đặt máy quét, cấu hình ngăn kéo tiền cho phục hồi thảm họa

