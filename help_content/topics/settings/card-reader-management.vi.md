---
title: Quản lý Thiết bị Đọc Thẻ
---

Quản lý thiết bị đọc thẻ theo dõi các thiết bị phần cứng thanh toán vật lý, gán chúng cho các máy POS và giám sát trạng thái hoạt động của chúng. Mỗi thiết bị đọc thẻ đại diện cho phần cứng thực tế (Stripe S700, WisePOS E hoặc P400) đã đăng ký với nhà cung cấp thanh toán của bạn. Các thiết bị đọc thẻ có mối quan hệ một đối một với các máy POS—mỗi máy đăng ký có thiết bị đọc thẻ riêng của nó. Theo dõi trạng thái thiết bị đọc thẻ (trực tuyến, ngoại tuyến, bận) theo thời gian thực, tùy chỉnh màn hình chờ với thương hiệu của bạn và khắc phục sự cố kết nối trước khi chúng ảnh hưởng đến trải nghiệm thanh toán của khách hàng.

Sử dụng quản lý thiết bị đọc thẻ để đảm bảo phần cứng thanh toán được cấu hình, gán và hoạt động đúng tại tất cả các địa điểm.

![Danh sách Thiết bị Đọc Thẻ](/static/core/admin/img/help/card-reader-management/reader-list.webp)

## Hiểu Về Thiết Bị Đọc Thẻ

Thiết bị đọc thẻ là các thiết bị phần cứng vật lý xử lý thanh toán thẻ tín dụng và thẻ ghi nợ:

**Các Thành Phần Phần Cứng**:
- Khe cắm chip EMV
- Anten NFC (không tiếp xúc/thanh toán bằng chạm)
- Máy đọc dải từ (cổ điển, hiếm khi được sử dụng)
- Màn hình hiển thị (hiển thị số tiền, yêu cầu mã PIN, chữ ký)
- Kết nối mạng (Wi-Fi hoặc cáp mạng, tùy theo mẫu)

**Tích Hợp Phần Mềm**:
- Thiết bị đọc thẻ kết nối với API Stripe Terminal (dựa trên đám mây, không kết nối trực tiếp với thiết bị POS)
- Thiết bị POS yêu cầu thanh toán qua API
- Stripe định tuyến yêu cầu đến thiết bị đọc thẻ đã đăng ký
- Thiết bị đọc thẻ xử lý thẻ và trả lại kết quả cho POS
- Không cần kết nối USB/Bluetooth giữa POS và thiết bị đọc thẻ

**Một Thiết Bị Đọc Thẻ Cho Mỗi Máy POS**:
- Mỗi máy POS nên có đúng một thiết bị đọc thẻ được gán
- Mối quan hệ một đối một đảm bảo trách nhiệm rõ ràng và dễ dàng khắc phục sự cố
- Nhiều máy POS không thể chia sẻ một thiết bị đọc thẻ (gây xung đột)

## Loại Thiết Bị Đọc Thẻ

Spwig POS hỗ trợ các thiết bị đọc thẻ Stripe Terminal:

**BBPOS WisePOS E** (`bbpos_wisepos_e`):
- Thiết bị Android tích hợp với màn hình cảm ứng màu 5"
- Tùy chọn in ấn nhiệt (phiếu thu)
- Tốt nhất cho: Thanh toán bán lẻ đầy đủ tính năng, nhà hàng (yêu cầu tip trên màn hình màu)
- Kết nối: Chỉ Wi-Fi
- Màn hình chờ: Màu đầy đủ 480×800 dọc

**Stripe Reader S700** (`stripe_s700`):
- Thiết bị đọc thẻ trên bàn với màn hình LCD đen trắng
- Thiết kế nhỏ gọn, chống thấm nước
- Tốt nhất cho: Bán lẻ tiêu chuẩn, quầy thanh toán nhỏ gọn
- Kết nối: Wi-Fi hoặc cáp mạng
- Màn hình chờ: Đen trắng 480×800 dọc

**Verifone P400** (`verifone_p400`):
- Thiết bị đọc thẻ trên bàn cũ (mẫu cũ hơn)
- Vẫn được hỗ trợ nhưng không khuyến khích cho triển khai mới
- Tốt nhất cho: Các triển khai hiện tại (không thay thế thiết bị phần cứng đang hoạt động)
- Kết nối: Wi-Fi hoặc cáp mạng
- Màn hình chờ: Đen trắng 480×800 dọc

**Tương thích Tương Lai**:
- Các mẫu thiết bị đọc thẻ bổ sung có thể được thêm vào khi Stripe Terminal mở rộng các lựa chọn phần cứng
- Danh sách thả xuống loại thiết bị đọc thẻ tự động cập nhật từ khả năng của nhà cung cấp

## Quy Trình Đăng Ký Thiết Bị Đọc Thẻ

**Bước 1: Mua và Nhận Thiết Bị**
- Đặt mua thiết bị đọc thẻ từ Stripe (stripe.com/terminal) hoặc nhà phân phối được ủy quyền
- Mở hộp và bật thiết bị đọc thẻ
- Kết nối với mạng Wi-Fi (theo hướng dẫn cài đặt trên màn hình thiết bị)

**Bước 2: Đăng Ký Trên Bảng Điều Khiển Stripe**
- Truy cập **Bảng điều khiển Stripe > Terminal > Readers**
- Nhấp vào **Đăng ký Thiết bị Đọc Thẻ Mới**
- Theo dõi quy trình ghép nối trên màn hình (thiết bị đọc thẻ hiển thị mã đăng ký)
- Gán thiết bị đọc thẻ đến Vị trí Stripe (phải khớp với vị trí trong cấu hình nhà cung cấp thanh toán)
- Ghi lại **ID Thiết Bị Đọc Thẻ** (dạng `tmr_ABC123...`)

**Bước 3: Đồng Bộ Với Spwig (Tự động)**
- Spwig tự động phát hiện các thiết bị đọc thẻ đã đăng ký tại vị trí Stripe của bạn
- Nhiệm vụ nền tảng đồng bộ mỗi 30 phút
- Thiết bị đọc thẻ mới sẽ xuất hiện trong danh sách **POS > Thiết bị Đọc Thẻ** trong vòng 30 phút

**Bước 4: Gán Đến Máy POS (Tự động)**
- Truy cập **POS > Thiết bị Đọc Thẻ**
- Tìm thiết bị đọc thẻ mới được phát hiện trong danh sách
- Nhấp để chỉnh sửa
- Chọn **Máy POS** để gán thiết bị đọc thẻ
- Lưu lại

**Bước 5: Kiểm Tra Thanh Toán**
- Tại máy POS, thực hiện giao dịch kiểm tra
- Chọn phương thức thanh toán bằng thẻ
- POS nên phát hiện thiết bị đọc thẻ đã gán
- Sử dụng thẻ kiểm tra Stripe (4242 4242 4242 4242) để hoàn tất kiểm tra
- Xác nhận thanh toán hoàn tất thành công

Nếu thiết bị đọc thẻ không xuất hiện trong kiểm tra, hãy kiểm tra việc gán máy POS và trạng thái thiết bị đọc thẻ.

## Theo Dõi Trạng Thái Thiết Bị Đọc Thẻ

Các thiết bị đọc thẻ báo cáo trạng thái đến API Stripe Terminal, Spwig đồng bộ mỗi 5 phút:

**Trực tuyến** (xanh lá) - Thiết bị đọc thẻ đã bật, kết nối mạng và sẵn sàng nhận thanh toán

**Ngoại tuyến** (đỏ) - Thiết bị đọc thẻ đã tắt, ngắt kết nối mạng hoặc không thể truy cập

**Bận** (vàng) - Thiết bị đọc thẻ đang xử lý giao dịch thanh toán

**Lần cuối thấy** - Thời gian dấu ấn của lần kiểm-in gần nhất của thiết bị đọc thẻ với API Stripe
- Cập nhật mỗi ~2 phút khi thiết bị đọc thẻ trực tuyến
- Hữu ích để chẩn đoán vấn đề kết nối ("thiết bị đọc thẻ ngoại tuyến 3 giờ trước" = vấn đề nguồn hoặc mạng trong giờ làm việc)

**Trường Hợp Sử Dụng Trạng Thái**:
- **Kiểm tra trước mở cửa**: Xác nhận tất cả thiết bị đọc thẻ trong cửa hàng đều trực tuyến trước khi mở cửa
- **Khắc phục sự cố**: "Máy 3 không nhận thẻ" → Kiểm tra trạng thái thiết bị đọc thẻ → Hiển thị ngoại tuyến → Kiểm tra nguồn/mạng
- **Kiểm toán**: "Các giao dịch có được xử lý tại Máy 5 hôm qua không?" → Kiểm tra thời gian lần cuối thấy

## Gán Máy POS

Các thiết bị đọc thẻ sử dụng **mối quan hệ một đối một** với các máy POS:

**Tại Sao Việc Gán Là Quan Trọng**:
- Trong quá trình thanh toán, POS cần biết thiết bị đọc thẻ nào để giao tiếp
- Nhiều máy POS chia sẻ một thiết bị đọc thẻ gây xung đột (hai nhân viên không thể sử dụng cùng một thiết bị đọc thẻ cùng lúc)
- Thiết bị đọc thẻ chưa được gán sẽ không được sử dụng (thiết bị phần cứng bị bỏ sót)

**Quy Tắc Gán**:
- Mỗi máy POS có thể có **đúng một** thiết bị đọc thẻ được gán
- Mỗi thiết bị đọc thẻ có thể được gán đến **đúng một** máy POS
- Việc gán thiết bị đọc thẻ đến Máy A sẽ tự động gỡ gán khỏi máy POS trước đó

**Thay Đổi Gán**:
- Chỉnh sửa hồ sơ thiết bị đọc thẻ
- Thay đổi trường **Máy POS** thành máy POS mới
- Lưu lại
- Máy POS trước đó sẽ mất gán thiết bị đọc thẻ (sẽ hiển thị lỗi "Không có thiết bị đọc thẻ được gán" trong quá trình thanh toán)

**Thiết Bị Đọc Thẻ Chưa Được Gán**:
- Thiết bị đọc thẻ mới phát hiện sẽ bắt đầu chưa được gán
- Thiết bị đọc thẻ chưa được gán sẽ xuất hiện trong danh sách nhưng không thể sử dụng
- Gán đến máy POS để kích hoạt

## Tùy Chỉnh Màn Hình Chờ

Màn hình chờ thiết bị đọc thẻ hiển thị thương hiệu trên màn hình hướng đến khách hàng khi không hoạt động:

**Màn Hình Chờ Là Gì?**
- Hình ảnh hiển thị trên màn hình thiết bị đọc thẻ khi không xử lý thanh toán
- Thay thế biểu tượng Stripe mặc định bằng thương hiệu của bạn
- Hiển thị cho khách hàng khi chờ đợi tại quầy thanh toán

**Tự động Tạo vs Tùy Chỉnh**:

**Tự động Tạo** (mặc định):
- Spwig tạo màn hình chờ từ logo cửa hàng của bạn (nếu logo được cấu hình trong cài đặt cửa hàng)
- Tự động điều chỉnh kích thước theo yêu cầu thiết bị đọc thẻ (480×800 dọc)
- Đen trắng cho S700/P400, màu sắc cho WisePOS E
- Không cần cấu hình

**Màn Hình Chờ Tùy Chỉnh** (nâng cao):
- Tải lên hình ảnh màn hình chờ được thiết kế riêng của bạn
- Kiểm soát hoàn toàn thiết kế và thương hiệu
- Phải đáp ứng yêu cầu hình ảnh (xem bên dưới)

**Yêu Cầu Màn Hình Chờ Tùy Chỉnh**:
- **Độ phân giải**: Chính xác 480×800 pixel (hướng dọc)
- **Định dạng**: PNG hoặc JPG
- **S700/P400**: Chỉ đen trắng (đen và trắng, không xám)
- **WisePOS E**: Hỗ trợ màu sắc đầy đủ
- **Kích thước tệp**: <200KB

**Thiết Lập Màn Hình Chờ Tùy Chỉnh**:
1. Chỉnh sửa hồ sơ thiết bị đọc thẻ
2. Tải lên hình ảnh đến trường **Hình Ảnh Thay Thế Màn Hình Chờ** (hoặc chọn từ Thư Viện Truyền Thông)
3. Lưu lại
4. Màn hình chờ sẽ đồng bộ đến thiết bị đọc thẻ trong vòng 5 phút

**Xóa Màn Hình Chờ Tùy Chỉnh**:
- Xóa trường **Hình Ảnh Thay Thế Màn Hình Chờ**
- Lưu lại
- Thiết bị đọc thẻ sẽ quay lại màn hình chờ tự động tạo (hoặc mặc định Stripe nếu không có logo cửa hàng)

**Kiểm Tra Màn Hình Chờ**:
- Sau khi tải lên, chờ 5 phút để đồng bộ
- Truy cập thiết bị đọc thẻ
- Xác nhận màn hình chờ xuất hiện trên màn hình không hoạt động
- Kiểm tra chất lượng hình ảnh, vị trí trung tâm và độ tương phản

## Cấu Hình Màn Hình Chờ Stripe

Phía sau, Spwig quản lý cấu hình màn hình chờ Stripe Terminal:

**stripe_splash_file_id** - ID nội bộ của Stripe cho tệp hình ảnh màn hình chờ đã tải lên
- Được thiết lập tự động khi màn hình chờ được tải lên
- Được sử dụng để tham chiếu màn hình chờ trong API Stripe

**stripe_splash_config_id** - ID nội bộ của Stripe cho cấu hình màn hình chờ
- Liên kết tệp màn hình chờ với thiết bị đọc thẻ
- Được quản lý tự động khi gán màn hình chờ đến thiết bị đọc thẻ

Các trường này là chỉ đọc và được quản lý tự động—you không cần tương tác trực tiếp với chúng.

## Khắc Phục Các Vấn Đề Thường Gặp

**Vấn đề 1: Thiết bị đọc thẻ hiển thị ngoại tuyến nhưng đã bật nguồn**
- **Nguyên nhân**: Vấn đề kết nối mạng, mật khẩu Wi-Fi đã thay đổi, thiết bị đọc thẻ ngoài phạm vi
- **Giải pháp**: Kiểm tra cài đặt mạng của thiết bị đọc thẻ, kết nối lại với Wi-Fi, xác nhận API Stripe có thể truy cập từ mạng

**Vấn đề 2: POS hiển thị "Không có thiết bị đọc thẻ được gán" trong quá trình thanh toán**
- **Nguyên nhân**: Thiết bị đọc thẻ chưa được gán đến máy POS hoặc gán chưa hoàn tất
- **Giải pháp**: Chỉnh sửa thiết bị đọc thẻ, gán đến máy POS, lưu lại, kiểm tra thanh toán lại

**Vấn đề 3: Thiết bị đọc thẻ bận mãi (bị kẹt trên màn hình thanh toán)**
- **Nguyên nhân**: Giao dịch hết thời gian hoặc bị lỗi, trạng thái thiết bị đọc thẻ không được đặt lại
- **Giải pháp**: Khởi động lại thiết bị đọc thẻ (tắt nguồn và bật lại), liên hệ hỗ trợ Stripe nếu vẫn tiếp diễn

**Vấn đề 4: Màn hình chờ tùy chỉnh không xuất hiện**
- **Nguyên nhân**: Hình ảnh có độ phân giải sai, chưa đồng bộ, không đáp ứng yêu cầu đen trắng (S700/P400)
- **Giải pháp**: Xác nhận hình ảnh chính xác 480×800, chờ 5 phút để đồng bộ, đảm bảo đen trắng cho thiết bị đọc thẻ không màu

**Vấn đề 5: Thiết bị đọc thẻ đã đăng ký trên Stripe nhưng không xuất hiện trong Spwig**
- **Nguyên nhân**: Thiết bị đọc thẻ được đăng ký đến vị trí Stripe khác với ID vị trí cấu hình nhà cung cấp
- **Giải pháp**: Trong Bảng điều khiển Stripe, xác nhận vị trí thiết bị đọc thẻ khớp với ID vị trí nhà cung cấp

## Mẹo

- **Một thiết bị đọc thẻ cho mỗi máy POS** - Đừng chia sẻ thiết bị đọc thẻ giữa các máy POS; ngăn xung đột và đơn giản hóa trách nhiệm
- **Đăng ký thiết bị đọc thẻ trước khi triển khai** - Hoàn tất đăng ký Stripe và gán Spwig trước khi đặt thiết bị đọc thẻ tại quầy thanh toán
- **Kiểm tra màn hình chờ trong cửa hàng** - Độ tương phản thay đổi theo mẫu thiết bị đọc thẻ và ánh sáng; xác nhận màn hình chờ trông tốt trong môi trường thực tế
- **Theo dõi trạng thái trước mở cửa** - Kiểm tra danh sách thiết bị đọc thẻ mỗi sáng để đảm bảo tất cả thiết bị đọc thẻ trực tuyến trước khi cửa hàng mở
- **Gắn nhãn phần cứng vật lý** - Sử dụng máy in nhãn để đánh dấu thiết bị đọc thẻ với tên máy POS ("Máy POS 1 Reader") để dễ dàng xác định trong quá trình khắc phục sự cố
- **Giữ thiết bị đọc thẻ trên nguồn không gián đoạn** - Sự cố mất điện giữa giao dịch có thể làm hỏng trạng thái thiết bị đọc thẻ; khuyến khích sử dụng UPS
- **Ghi lại số serial thiết bị đọc thẻ** - Lưu trữ hồ sơ số serial cho bảo hành và hỗ trợ (tìm thấy trên nhãn phần cứng thiết bị đọc thẻ)
- **Cập nhật firmware thiết bị đọc thẻ** - Stripe tự động đẩy các bản cập nhật firmware, nhưng xác nhận thiết bị đọc thẻ đang ở phiên bản mới nhất định kỳ (kiểm tra Bảng điều khiển Stripe)
