---
title: Tổng quan hệ thống POS
---

Hệ thống POS của Spwig biến cửa hàng của bạn thành một giải pháp bán lẻ hoàn chỉnh với các máy quầy thanh toán hiện đại. Nó được bao gồm trong mọi phiên bản — Cộng đồng, Chuyên nghiệp và Doanh nghiệp — với số lượng không giới hạn các máy quầy tại các địa điểm không giới hạn mà không có chi phí bổ sung. Mỗi máy quầy là một ứng dụng Web Tiến bộ (PWA) có thể hoạt động ngoại tuyến, đồng bộ tự động và tích hợp liền mạch với kho hàng, dữ liệu khách hàng và xử lý thanh toán. Quản lý mọi thứ từ bảng điều khiển quản trị — cấu hình máy quầy, đối chiếu ca làm, tùy chỉnh hóa hóa đơn và tích hợp phần cứng.

Sử dụng hệ thống POS khi bạn có các địa điểm bán lẻ vật lý, cửa hàng di động, hội chợ thương mại hoặc bất kỳ môi trường nào mà khách hàng mua hàng trực tiếp thay vì trực tuyến.

![Bảng điều khiển POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Spwig POS là gì?

Spwig POS là hệ thống điểm bán hàng được tích hợp đầy đủ, được thiết kế cho các nhà bán hàng bán hàng cả trực tuyến và tại các địa điểm vật lý. Khác với các hệ thống POS bên thứ ba yêu cầu tích hợp phức tạp, Spwig POS được xây dựng trực tiếp vào nền tảng của bạn, đảm bảo đồng bộ dữ liệu hoàn hảo trên tất cả các kênh bán hàng.

**Đặc điểm chính**:
- **Không giới hạn máy quầy** - triển khai bất kỳ số lượng máy quầy nào cần thiết mà không có chi phí bổ sung
- **Kiến trúc ưu tiên ngoại tuyến** - tiếp tục xử lý giao dịch ngay cả khi kết nối internet bị mất
- **Ứng dụng Web Tiến bộ** - không cần cài đặt từ cửa hàng ứng dụng; truy cập qua trình duyệt trên bất kỳ thiết bị nào (máy tính bảng, máy tính, máy quầy chuyên dụng)
- **Đồng bộ tồn kho thực tế** - đặt hàng tồn (15 phút TTL) ngăn chặn việc bán quá số lượng trên các kênh
- **Hỗ trợ thanh toán chia nhỏ** - chấp nhận nhiều phương thức thanh toán cho mỗi giao dịch (tiền mặt + thẻ + thẻ quà tặng)
- **Tích hợp phần cứng** - máy in nhiệt ESC/POS, máy quét mã vạch, ngăn tiền, màn hình khách hàng
- **Quản lý ca làm** - đối chiếu tiền mặt với số lượng mở/closing và theo dõi chênh lệch
- **Sẵn sàng cho nhiều địa điểm** - nhóm cửa hàng với cài đặt kế thừa cho quản lý nhượng quyền và khu vực

## Các phiên bản

POS được bao gồm trong mọi phiên bản Spwig — Cộng đồng, Chuyên nghiệp và Doanh nghiệp — kể từ Spwig 1.5.8. Không có giấy phép POS riêng biệt, không bước kích hoạt và không phí theo máy quầy.

**Được bao gồm trong mọi phiên bản**:
- Đăng ký máy quầy không giới hạn
- Phân công nhân viên không giới hạn
- Tất cả các tính năng POS (ca làm, quản lý tiền mặt, tùy chỉnh hóa hóa đơn, màn hình khách hàng)
- Tích hợp nhà cung cấp thanh toán (Stripe Terminal và các nhà cung cấp được hỗ trợ khác)
- Hỗ trợ tích hợp phần cứng

Các nhà bán hàng đang chạy cửa hàng được lưu trữ bởi Spwig hoặc đang trả phí cho giấy phép Chuyên nghiệp/Doanh nghiệp sẽ có giới hạn cao hơn cho các dịch vụ được lưu trữ bởi Spwig (GeoIP, geocoder, thông báo đẩy) và hỗ trợ ưu tiên, nhưng bộ tính năng POS chính bản thân nó là giống nhau trên tất cả các phiên bản.

## Kiến trúc hệ thống

**Giao diện người dùng** - Ứng dụng Web Tiến bộ React 18:
- Ưu tiên ngoại tuyến với lưu trữ Service Worker (hoạt động mà không cần internet)
- Hệ thống xây dựng Vite để tải nhanh
- CSS Modules + token thiết kế (tương thích với chủ đề cửa hàng của bạn)
- IndexedDB để lưu trữ dữ liệu cục bộ
- 10 ngôn ngữ được hỗ trợ (Tiếng Anh, Tiếng Trung giản thể/đại tự, Tiếng Pháp, Tiếng Đức, Tiếng Tây Ban Nha, Tiếng Bồ Đào Nha, Tiếng Nhật, Tiếng Nga, Tiếng Ả Rập)

**Backend** - Tích hợp Backend:
- 13 mô hình POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, v.v.)
- Hơn 43 điểm cuối REST API cho hoạt động máy quầy
- Hệ thống đặt hàng tồn với quản lý TTL
- Nhiệm vụ Celery cho đồng bộ hóa nền sau
- Lưu trữ thông tin xác thực được mã hóa cho nhà cung cấp thanh toán

**Bảo mật**:
- Cặp máy quầy thông qua mã 8 ký tự (được tạo trên máy chủ, hết hạn sau khi sử dụng)
- Kiểm soát phân công nhân viên xác định người dùng nào có thể truy cập máy quầy nào
- Khả năng khóa/mở khóa từ xa cho các tình huống khẩn cấp của quản trị viên
- Thông tin xác thực nhà cung cấp thanh toán được mã hóa
- Xác thực dựa trên phiên với hỗ trợ mở khóa sinh trắc học (phụ thuộc vào trình duyệt)

## Quy trình bắt đầu

Thực hiện theo 4 bước sau để triển khai máy quầy POS đầu tiên của bạn.

Để xem danh sách kiểm tra từng bước đầy đủ bao gồm thiết lập nhân viên, nhà cung cấp thanh toán và chạy giao dịch đầu tiên, vui lòng xem [Getting Started with POS](getting-started-with-pos).

**Bước 1: Tạo Kho hàng**
- Di chuyển đến **Catalog > Warehouses**
- Tạo kho hàng đại diện cho địa điểm bán lẻ của bạn
- Cấu hình địa chỉ và thông tin liên hệ
- Kho hàng này sẽ theo dõi hàng tồn kho vật lý cho các giao dịch POS

**Bước 2: Đăng ký Thiết bị**
- Di chuyển đến **POS > Terminals**
- Nhấp vào **+ Add Terminal**
- Đặt tên thiết bị (ví dụ: "Main Register", "Checkout 1")
- Gán kho hàng từ Bước 2
- Cấu hình cài đặt phần cứng (máy in, máy quét, ngăn kéo tiền)
- Lưu để tạo mã ghép nối 8 ký tự

**Bước 3: Gán Nhân viên**
- Trong cài đặt thiết bị, cuộn xuống **Assigned Users**
- Chọn các nhân viên được ủy quyền sử dụng thiết bị này
- Chỉ các người dùng được gán mới có thể đăng nhập vào thiết bị
- Người dùng phải có quyền POS phù hợp trong vai trò nhân viên của họ

**Bước 4: Ghép nối Thiết bị**
- Trên thiết bị của bạn (máy tính bảng/máy tính), di chuyển đến URL `/pos/`
- Nhập mã ghép nối 8 ký tự từ Bước 3
- Thiết bị tải xuống cài đặt và đồng bộ dữ liệu ban đầu
- Đăng nhập bằng thông tin nhân viên được gán
- Thiết bị đã sẵn sàng để bán hàng

Sau khi ghép nối, các thiết bị sẽ tự động đồng bộ mỗi 5 phút (có thể cấu hình). Chế độ ngoại tuyến cho phép tiếp tục hoạt động khi không có kết nối internet — các giao dịch sẽ tự động đồng bộ khi kết nối quay lại.

## Các Tính Năng Chính của POS

**Xử lý Bán hàng**:
- Tìm kiếm sản phẩm theo tên, SKU hoặc mã vạch
- Phân chia thanh toán (nhiều phương thức thanh toán cho một đơn hàng)
- Giỏ hàng tạm dừng (lưu các giao dịch chưa hoàn tất)
- Hoàn tiền và hủy giao dịch với theo dõi lý do
- Áp dụng khuyến mãi (phiếu mua hàng, thẻ quà tặng, chương trình khuyến mãi)
- Tra cứu khách hàng và đổi điểm thành viên

**Quản lý Tiền mặt**:
- Mở ca với số tiền mặt ban đầu
- Đóng ca với đối chiếu số tiền dự kiến và thực tế
- Các khoản chuyển tiền mặt (thêm tiền mặt, rút tiền lẻ với lý do)
- Tính toán tự động số tiền mặt dự kiến dựa trên doanh thu tiền mặt
- Theo dõi và báo cáo chênh lệch

**Tích hợp Thiết bị**:
- Máy in hóa đơn nhiệt ESC/POS (mạng hoặc cổng nối tiếp)
- Máy quét mã vạch USB
- Kích hoạt ngăn kéo tiền qua xung máy in
- Màn hình hướng đến khách hàng (trình di chuyển khuyến mãi khi không hoạt động)
- Thiết bị đọc thẻ Stripe Terminal (S700, WisePOS E, P400)

**Khả năng Hoạt động Ngoại tuyến**:
- Service Worker lưu trữ tất cả tài sản thiết bị
- IndexedDB lưu trữ các đơn hàng gần đây (có thể cấu hình: 7-30 ngày, 200-1000 đơn hàng)
- Đặt hàng tồn kho với TTL 15 phút ngăn việc bán quá mức
- Đợi đồng bộ khi kết nối quay lại
- Phát hiện kết nối lại tự động

## Các Trang Quản trị POS

Truy cập các trang quản trị này để quản lý mọi khía cạnh triển khai POS của bạn:

**Bảng điều khiển POS** (`/admin/pos/`)
- Tổng quan hệ thống và thống kê nhanh
- Hoạt động thiết bị gần đây
- Tóm tắt ca đang hoạt động
- Các mô-đun sử dụng dịch vụ lưu trữ (GeoIP, geocoder, push — xem [Spwig Hosted Services](hosted-services))

**Quản lý Thiết bị** (`/admin/pos_app/posterminal/`)
- Đăng ký và cấu hình thiết bị
- Gán nhân viên và kho hàng
- Theo dõi trạng thái trực tuyến/đang ngoại tuyến (theo dõi nhịp tim)
- Mở khóa thiết bị từ xa
- [Tìm hiểu thêm: Managing POS Terminals](managing-pos-terminals)

**Quản lý Ca làm việc** (`/admin/pos_app/posshift/`)
- Xem tất cả các ca (đang mở, đã đóng, lịch sử)
- Xem báo cáo đối chiếu tiền mặt
- Theo dõi các khoản chuyển tiền mặt và chênh lệch
- Kiểm toán hoạt động ca
- [Tìm hiểu thêm: POS Shifts and Cash Management](pos-shifts-cash-management)

**Nhóm Cửa hàng** (`/admin/pos_app/storegroup/`)
- Phân loại thiết bị theo vị trí/khu vực
- Cấu hình cài đặt cấp nhóm (tiền tệ, ngôn ngữ, múi giờ)
- Triển khai phân cấp cài đặt
- [Tìm hiểu thêm: POS Store Groups](pos-store-groups)

**Mẫu biên lai** (`/admin/pos_app/receipttemplate/`)
- Tùy chỉnh biên lai in ra (chiều rộng giấy, logo, tiêu đề/chân trang)
- Cấu hình các trường tuân thủ (số thuế, giấy phép kinh doanh)
- Thêm mã QR cho khuyến mãi
- Áp dụng mẫu cho các cửa hàng hoặc nhóm cụ thể
- [Tìm hiểu thêm: Tùy chỉnh mẫu biên lai](receipt-template-customization)

**Trang trình chiếu khuyến mãi** (`/admin/pos_app/promoslide/`)
- Tạo nội dung carousel hiển thị cho khách hàng
- Định hướng trang trình chiếu cho các cửa hàng hoặc nhóm cụ thể
- Lên lịch khuyến mãi theo mùa
- [Tìm hiểu thêm: Trang trình chiếu khuyến mãi hiển thị cho khách hàng](customer-display-promo-slides)

**Nhà cung cấp thanh toán** (`/admin/pos_app/posterminalprovider/`)
- Cấu hình tích hợp Stripe Terminal
- Quản lý thông tin xác thực nhà cung cấp thanh toán
- Theo dõi trạng thái kết nối
- [Tìm hiểu thêm: Nhà cung cấp thiết bị thanh toán](payment-terminal-providers)

**Đọc thẻ** (`/admin/pos_app/posterminalreader/`)
- Đăng ký thiết bị đọc thẻ vật lý
- Gán thiết bị đọc thẻ cho các đầu cuối
- Tùy chỉnh màn hình khởi động (thương hiệu hiển thị cho khách hàng)
- Theo dõi trạng thái thiết bị đọc thẻ (trực tuyến/đang ngoại tuyến/đang bận)
- [Tìm hiểu thêm: Quản lý thiết bị đọc thẻ](card-reader-management)

## Triển khai đa địa điểm

Đối với các nhà bán lẻ có nhiều địa điểm, Spwig POS hỗ trợ kế thừa cài đặt theo cấp bậc:

**Cấp bậc cài đặt** (ưu tiên cao nhất đến thấp nhất):
1. Cài đặt cụ thể cho đầu cuối (ghi đè tất cả)
2. Cài đặt cụ thể cho cửa hàng (ghi đè nhóm và trang web)
3. Cài đặt nhóm (ghi đè cài đặt mặc định của trang web)
4. Cài đặt mặc định của trang web (lựa chọn dự phòng cho tất cả)

Cấu hình cài đặt chia sẻ ở cấp độ nhóm (ví dụ: tiền tệ khu vực, ngôn ngữ) và ghi đè khi cần cho các cửa hàng hoặc đầu cuối cụ thể. Xem [Nhóm cửa hàng POS](pos-store-groups) để biết hướng dẫn cấu hình chi tiết.

## Một số mẹo

- **Bắt đầu với một đầu cuối** - Kiểm tra thiết lập và quy trình POS với một đầu cuối trước khi triển khai trên toàn bộ đội ngũ
- **Gán kho hàng trước khi ghép nối** - Các đầu cuối không thể xử lý giao dịch nếu chưa được gán kho hàng
- **Cấu hình mẫu biên lai sớm** - Các trường tuân thủ (số thuế) thay đổi theo khu vực; hãy thiết lập trước khi chính thức vận hành
- **Kiểm tra chế độ ngoại tuyến** - Ngắt kết nối internet và xác nhận giao dịch vẫn tiếp tục; xác nhận đồng bộ khi kết nối lại
- **Sử dụng nhóm cửa hàng cho nhiều địa điểm** - Đơn giản hóa quản lý cấu hình cho triển khai nhượng quyền hoặc khu vực
- **Theo dõi trạng thái "heartbeat"** - Các đầu cuối ping máy chủ mỗi 5 phút; các đầu cuối ngoại tuyến sẽ hiển thị trên bảng điều khiển quản trị
- **Cấu hình giới hạn đồng bộ để tối ưu hiệu suất** - Các đầu cuối có kết nối chậm sẽ có lợi từ cài đặt sync_days/sync_limit thấp hơn
- **Sao lưu cấu hình phần cứng** - Ghi lại địa chỉ IP máy in, cài đặt máy quét, cấu hình ngăn kéo tiền để phục hồi thảm họa