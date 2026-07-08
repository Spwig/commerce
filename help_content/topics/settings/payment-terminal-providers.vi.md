---
title: Các nhà cung cấp máy đầu cuối thanh toán
---

Các nhà cung cấp máy đầu cuối thanh toán cho phép chấp nhận thẻ tín dụng và thẻ ghi nợ tại các đầu cuối POS của bạn. Stripe Terminal là nhà cung cấp được hỗ trợ chính, cung cấp các thiết bị đọc thẻ hiện đại (S700, WisePOS E, P400), tỷ lệ xử lý cạnh tranh và tích hợp liền mạch. Cấu hình tài khoản nhà cung cấp với thông tin API, theo dõi trạng thái kết nối theo thời gian thực và quản lý nhiều nhà cung cấp nếu bạn đang hoạt động tại các khu vực khác nhau. Hệ thống nhà cung cấp có thể mở rộng—các nhà xử lý thanh toán bổ sung có thể được tích hợp thông qua khung nhà cung cấp nếu Stripe Terminal không hoạt động tại thị trường của bạn.

Sử dụng nhà cung cấp thanh toán để chấp nhận thanh toán thẻ an toàn, theo dõi trạng thái xử lý thanh toán và quản lý việc phân bổ thiết bị đọc thẻ trên các đầu cuối.

![Danh sách nhà cung cấp thanh toán](/static/core/admin/img/help/payment-terminal-providers/provider-list.webp)

## Tổng quan về nhà cung cấp thanh toán

Các nhà cung cấp thanh toán là các dịch vụ bên thứ ba xử lý thanh toán thẻ thay mặt cho doanh nghiệp của bạn:

**Trách nhiệm của nhà cung cấp**:
- Xác thực giao dịch thẻ theo thời gian thực
- Giao tiếp với thiết bị đọc thẻ vật lý
- Xử lý bảo mật thanh toán (tuân thủ PCI, mã hóa)
- Chuyển tiền vào tài khoản ngân hàng của bạn (thanh toán)
- Cung cấp báo cáo giao dịch và quản lý tranh chấp

**Vai trò của Spwig**:
- Chuyển hướng yêu cầu thanh toán đến nhà cung cấp đã cấu hình
- Lưu trữ thông tin xác thực nhà cung cấp được mã hóa
- Theo dõi trạng thái kết nối
- Liên kết thiết bị đọc với đầu cuối
- Ghi lại kết quả thanh toán trong đơn hàng

## Stripe Terminal (Nhà cung cấp chính)

Stripe Terminal là nhà cung cấp thanh toán được khuyến nghị cho hầu hết các nhà bán lẻ:

**Tính năng**:
- Thiết bị đọc thẻ chip EMV hiện đại
- Hỗ trợ thanh toán không tiếp xúc (NFC) (Apple Pay, Google Pay, thẻ gõ để thanh toán)
- Quản lý tranh chấp tích hợp
- Xác thực theo thời gian thực
- API thân thiện với lập trình viên
- Có sẵn tại 40+ quốc gia

**Giá cả** (tính đến năm 2024, vui lòng kiểm tra mức giá hiện tại):
- Phí giao dịch: 2,7% + $0,05 cho mỗi giao dịch trực tiếp (Mỹ)
- Không có phí hàng tháng, không có phí thiết lập, không có phí tuân thủ PCI
- Thiết bị đọc thẻ phần cứng: Mua một lần ($59-$299 tùy theo mẫu)

**Khu vực được hỗ trợ**:
- Hoa Kỳ, Canada, Vương quốc Anh, Liên minh châu Âu, Úc, Singapore và nhiều nơi khác
- Kiểm tra tính khả dụng của Stripe: https://stripe.com/terminal

**Thiết bị đọc được hỗ trợ**:
- BBPOS WisePOS E (thiết bị Android tích hợp đầy đủ)
- Stripe Reader S700 (thiết bị đọc trên bàn)
- Verifone P400 (thiết bị cũ, vẫn được hỗ trợ)

## Cấu hình Stripe Terminal

**Bước 1: Tạo tài khoản Stripe**
- Đăng ký tại stripe.com
- Hoàn tất xác minh doanh nghiệp (tài khoản ngân hàng, mã số thuế)
- Kích hoạt thanh toán

**Bước 2: Kích hoạt Stripe Terminal**
- Trong Bảng điều khiển Stripe, truy cập **Sản phẩm > Terminal**
- Nhấp vào **Bắt đầu**
- Chấp nhận điều khoản dịch vụ của Terminal

**Bước 3: Tạo vị trí**
- Stripe Terminal yêu cầu một "Vị trí" đại diện cho địa điểm bán lẻ vật lý của bạn
- Truy cập **Terminal > Vị trí**
- Nhấp vào **Tạo Vị trí**
- Nhập địa chỉ cửa hàng và chi tiết
- Lưu ID vị trí (dạng `tml_1ABC123...`)

**Bước 4: Tạo khóa API**
- Truy cập **Nhà phát triển > Khóa API**
- Tìm thấy **Khóa bí mật** của bạn (bắt đầu bằng `sk_live_...` cho môi trường sản xuất, `sk_test_...` cho kiểm tra)
- Sao chép khóa bí mật (không chia sẻ công khai)

**Bước 5: Cấu hình trong Spwig**
- Truy cập **POS > Nhà cung cấp thanh toán**
- Nhấp vào **+ Thêm nhà cung cấp thanh toán**
- Chọn **Nhà cung cấp**: "Stripe Terminal"
- Nhập **Khóa bí mật API** (từ Bước 4)
- Nhập **ID Vị trí** (từ Bước 3)
- Lưu

**Bước 6: Kiểm tra kết nối**
- Sau khi lưu, trạng thái nhà cung cấp nên thay đổi thành "Kết nối" (màu xanh)
- Nếu trạng thái hiển thị "Lỗi" (màu đỏ), hãy xác minh khóa API và ID vị trí
- Kiểm tra thông báo lỗi trong chi tiết nhà cung cấp

![Biểu mẫu thêm nhà cung cấp thanh toán](/static/core/admin/img/help/payment-terminal-providers/provider-add-form.webp)

## Các trường cấu hình nhà cung cấp

**Khóa nhà cung cấp** - Chọn nhà xử lý thanh toán:
- **stripe_terminal** - Stripe Terminal (khuyến nghị)
- **manual** - Nhập thanh toán thủ công (chỉ dùng để kiểm tra, không xử lý thực tế)
- Các nhà cung cấp bổ sung có thể xuất hiện nếu được cài đặt qua hệ thống thành phần

**Thông tin xác thực (được mã hóa)** - Cấu trúc JSON chứa thông tin xác thực API:
- Được mã hóa tự động trước khi lưu trữ
- Không bao giờ hiển thị dưới dạng văn bản rõ sau khi lưu
- Ví dụ cấu trúc (Stripe Terminal):
```json
{
  "api_key": "sk_live_ABC123...",
  "location_id": "tml_1ABC123..."
}
```

**Cài đặt nhà cung cấp** - Cấu hình bổ sung (tùy thuộc vào nhà cung cấp):
- Mô tả hóa đơn (hiển thị trên sao kê thẻ tín dụng của khách hàng)
- Thu giữ tự động (thu giữ ngay các giao dịch đã được xác thực thay vì thu giữ thủ công)
- Ghi đè tiền tệ (nếu tài khoản nhà cung cấp sử dụng tiền tệ khác với cửa hàng)

**Trạng thái kết nối** - Chỉ báo trạng thái theo thời gian thực:
- **Kết nối** (xanh) - Nhà cung cấp có thể truy cập và được cấu hình đúng
- **Lỗi** (đỏ) - Kết nối thất bại hoặc thông tin xác thực không hợp lệ
- **Không xác định** (xám) - Chưa được kiểm tra (ngay sau khi tạo)

**Lần kiểm tra cuối cùng** - Thời gian dấu thời gian của lần kiểm tra kết nối gần nhất
- Cập nhật tự động khi xử lý giao dịch
- Kích hoạt kiểm tra thủ công thông qua hành động quản trị **Kiểm tra kết nối**

## Giám sát trạng thái kết nối

Hệ thống giám sát kết nối nhà cung cấp để cảnh báo bạn về các vấn đề trước khi khách hàng cố gắng thanh toán:

**Kiểm tra tự động**:
- Mỗi giao dịch thanh toán kích hoạt kiểm tra kết nối (theo yêu cầu)
- Công việc nền kiểm tra kết nối mỗi 6 giờ (giám sát phòng ngừa)

**Ý nghĩa trạng thái**:

**Kết nối** - API nhà cung cấp có thể truy cập, thông tin xác thực hợp lệ, sẵn sàng xử lý thanh toán

**Lỗi** - Nguyên nhân phổ biến:
- Khóa API không hợp lệ (đã hủy, hết hạn hoặc sai)
- ID vị trí không hợp lệ (vị trí đã xóa trong Stripe, ID nhập sai)
- Vấn đề kết nối mạng (tường lửa chặn API Stripe)
- Sự cố dịch vụ Stripe (hiếm)

**Không xác định** - Nhà cung cấp chưa được kiểm tra (tài khoản mới được tạo, đang chờ giao dịch đầu tiên)

**Giải quyết trạng thái lỗi**:
1. Kiểm tra thông báo lỗi trong chi tiết nhà cung cấp (giải thích vấn đề cụ thể)
2. Xác minh khóa API vẫn hợp lệ trong Bảng điều khiển Stripe
3. Xác minh ID vị trí vẫn tồn tại trong Bảng điều khiển Stripe
4. Kiểm tra kết nối thủ công thông qua hành động quản trị **Kiểm tra kết nối**
5. Cập nhật thông tin xác thực nếu cần

![Chi tiết nhà cung cấp thanh toán](/static/core/admin/img/help/payment-terminal-providers/provider-detail.webp)

## So sánh thiết bị đọc thẻ được hỗ trợ

Stripe Terminal cung cấp nhiều tùy chọn phần cứng thiết bị đọc:

| Mô hình | Loại | Phương thức thanh toán | Màn hình | Tốt nhất cho | Giá |
|-------|------|-----------------|---------|----------|-------|
| **WisePOS E** | Tất cả trong một | Chip EMV, NFC, quẹt thẻ | Màn hình cảm ứng màu 5" | Điểm bán hàng bán lẻ đầy đủ tính năng | ~$299 |
| **S700** | Trên bàn | Chip EMV, NFC, quẹt thẻ | Màn hình LCD màu đen | Thanh toán bán lẻ tiêu chuẩn | ~$249 |
| **P400** | Trên bàn | Chip EMV, NFC, quẹt thẻ | Màn hình LCD màu đen | Triển khai cũ | ~$299 |

**Ưu điểm của WisePOS E**:
- Dựa trên Android (chạy ứng dụng, có thể hiển thị nội dung tùy chỉnh)
- Màn hình cảm ứng màu (UX tốt hơn cho việc nhắc nhở tip, ký tên)
- Máy in hóa đơn tích hợp (tùy chọn)
- Tốc độ giao dịch nhanh nhất

**Ưu điểm của S700**:
- Chi phí thấp hơn WisePOS E
- Kích thước nhỏ gọn
- Thiết kế chống thấm nước

**P400** (mô hình cũ):
- Vẫn được hỗ trợ nhưng không khuyến nghị cho triển khai mới
- Xử lý thẻ chip chậm hơn S700/WisePOS E

Tất cả thiết bị đọc kết nối với POS Spwig thông qua API Stripe Terminal (không cần kết nối trực tiếp USB/Bluetooth với thiết bị POS).

## Xét về bảo mật

**Mã hóa thông tin xác thực**:
- Tất cả thông tin xác thực nhà cung cấp được mã hóa khi lưu trữ trong cơ sở dữ liệu
- Mã hóa sử dụng khóa bí mật ứng dụng (được định nghĩa trong cài đặt ứng dụng)
- Thông tin xác thực không bao giờ xuất hiện trong nhật ký hoặc thông báo lỗi

**Quyền truy cập khóa API**:
- Sử dụng **khóa API bị giới hạn** trong môi trường sản xuất (hạn chế quyền truy cập chỉ đến Terminal)
- Không sử dụng khóa bí mật không bị giới hạn (quyền truy cập rộng hơn cần thiết = rủi ro bảo mật)
- Trong Bảng điều khiển Stripe, tạo khóa bị giới hạn chỉ có **quyền Terminal**

**Tuân thủ PCI**:
- Stripe Terminal xử lý tuân thủ PCI (dữ liệu thẻ không bao giờ tiếp xúc với máy chủ Spwig)
- Số thẻ được xử lý hoàn toàn trên phần cứng thiết bị đọc → máy chủ Stripe → mạng thẻ
- Spwig chỉ lưu trữ kết quả thanh toán (được chấp nhận/từ chối), không bao giờ lưu trữ chi tiết thẻ

**Thay đổi khóa**:
- Thay đổi khóa API hàng năm theo thực hành bảo mật tốt nhất
- Khi thay đổi, cập nhật thông tin xác thực trong cấu hình nhà cung cấp
- Khóa cũ có thể bị hủy trong Bảng điều khiển Stripe sau khi xác nhận khóa mới hoạt động

## Nhiều nhà cung cấp

Một số nhà bán lẻ cần nhiều tài khoản nhà cung cấp:

**Vận hành đa tiền tệ**:
- Cửa hàng Mỹ sử dụng tài khoản Stripe Mỹ (xử lý USD)
- Cửa hàng châu Âu sử dụng tài khoản Stripe EU (xử lý EUR)
- Cấu hình nhà cung cấp riêng cho mỗi loại tiền tệ

**Nhà cung cấp dự phòng**:
- Nhà cung cấp chính (Stripe Terminal)
- Nhà cung cấp dự phòng (nhập thủ công) khi thiết bị đọc gặp sự cố
- Nhân viên chọn nhà cung cấp khi bắt đầu thanh toán

**Kiểm tra vs. Sản xuất**:
- Nhà cung cấp kiểm tra với khóa API `sk_test_...`
- Nhà cung cấp sản xuất với khóa API `sk_live_...`
- Chuyển đổi nhà cung cấp sau giai đoạn kiểm tra

## Giải quyết các vấn đề phổ biến

**Vấn đề 1: Trạng thái hiển thị "Lỗi" với thông báo "Khóa API không hợp lệ"**
- **Nguyên nhân**: Khóa API bị hủy hoặc sao chép sai
- **Giải pháp**: Tạo khóa API mới trong Bảng điều khiển Stripe, cập nhật thông tin xác thực nhà cung cấp, kiểm tra kết nối

**Vấn đề 2: Thiết bị đọc không được phát hiện trong quá trình thanh toán**
- **Nguyên nhân**: Thiết bị đọc chưa được đăng ký với vị trí nhà cung cấp
- **Giải pháp**: Trong Bảng điều khiển Stripe, xác minh thiết bị đọc đã được đăng ký với cùng ID vị trí được sử dụng trong cấu hình nhà cung cấp

**Vấn đề 3: Thanh toán bị từ chối mặc dù thẻ hợp lệ**
- **Nguyên nhân**: Tài khoản Stripe chưa được kích hoạt đầy đủ (đang chờ xác minh)
- **Giải pháp**: Hoàn tất xác minh doanh nghiệp trong Bảng điều khiển Stripe (tài khoản ngân hàng, mã số thuế)

**Vấn đề 4: Trạng thái kết nối hiển thị "Không xác định" và không bao giờ cập nhật**
- **Nguyên nhân**: Nhà cung cấp chưa được kiểm tra (không có giao dịch nào được thực hiện)
- **Giải pháp**: Sử dụng hành động quản trị **Kiểm tra kết nối** để kích hoạt kiểm tra kết nối thủ công

## Một số mẹo

- **Kiểm tra trước khi sản xuất** - Sử dụng khóa API kiểm tra của Stripe (`sk_test_...`) cho việc thiết lập ban đầu và kiểm tra
- **Một nhà cung cấp cho mỗi loại tiền tệ** - Đừng cố gắng xử lý EUR bằng tài khoản Stripe dựa trên USD; tạo nhà cung cấp riêng biệt
- **Theo dõi trạng thái kết nối hàng tuần** - Giám sát chủ động giúp ngăn chặn sự cố thanh toán tại quầy thanh toán
- **Hạn chế quyền truy cập khóa API** - Giới hạn khóa API Stripe chỉ đến quyền Terminal (nguyên tắc quyền tối thiểu)
- **Ghi lại ID vị trí** - Lưu trữ bản ghi ID Stripe nào tương ứng với cửa hàng vật lý nào
- **Kiểm tra việc phân bổ thiết bị đọc** - Sau khi thiết lập nhà cung cấp, kiểm tra thanh toán bằng thiết bị đọc thực tế để xác minh luồng end-to-end
- **Cập nhật thông tin liên hệ Stripe** - Đảm bảo thông tin liên hệ doanh nghiệp trong Stripe khớp với hiện tại (quan trọng cho tranh chấp, tuân thủ)