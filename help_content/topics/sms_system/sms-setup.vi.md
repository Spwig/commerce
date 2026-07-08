---
title: Cài đặt nhà cung cấp SMS
---

Thông báo SMS giúp khách hàng của bạn được thông báo tại mọi bước trong đơn hàng của họ - từ xác nhận đến giao hàng. Để gửi tin nhắn SMS hoặc WhatsApp từ cửa hàng của bạn, bạn cần kết nối tài khoản nhà cung cấp SMS với thông tin xác thực của bạn. Sau khi kết nối, Spwig sẽ sử dụng tài khoản đó để gửi tất cả các tin nhắn văn bản đi.

Truy cập **Hệ thống SMS > Tài khoản nhà cung cấp SMS** để quản lý nhà cung cấp SMS của bạn.

![Danh sách tài khoản nhà cung cấp SMS](/static/core/admin/img/help/sms-setup/provider-list.webp)

## Thêm nhà cung cấp SMS

Bạn có thể thêm nhà cung cấp bằng cách sử dụng **Chỉ dẫn cài đặt** (khuyến nghị cho lần cài đặt đầu tiên) hoặc biểu mẫu thủ công.

### Sử dụng chỉ dẫn cài đặt

1. Truy cập **Hệ thống SMS > Tài khoản nhà cung cấp SMS**
2. Nhấp vào **Chỉ dẫn cài đặt** trong thanh công cụ
3. Theo dõi các bước được hướng dẫn:
   - **Bước 1**: Chọn nhà cung cấp của bạn từ danh sách các nhà cung cấp có sẵn
   - **Bước 2**: Nhập thông tin xác thực của nhà cung cấp (khóa API, SID tài khoản, v.v.)
   - **Bước 3**: Thiết lập tên hiển thị và cài đặt mặc định, sau đó lưu
4. Chỉ dẫn sẽ kiểm tra kết nối tự động trước khi lưu

### Thêm nhà cung cấp thủ công

1. Truy cập **Hệ thống SMS > Tài khoản nhà cung cấp SMS**
2. Nhấp vào **Duyệt nhà cung cấp** để khám phá các nhà cung cấp SMS có sẵn, hoặc nhấp trực tiếp vào **+ Thêm tài khoản nhà cung cấp SMS**
3. Trong trường **Nhà cung cấp**, chọn nhà cung cấp SMS của bạn từ danh sách thả xuống
4. Sau khi chọn nhà cung cấp, các trường thông tin xác thực sẽ xuất hiện tự động dựa trên những gì nhà cung cấp đó yêu cầu
5. Điền vào các trường thông tin xác thực cần thiết (các trường này thay đổi tùy theo nhà cung cấp - xem các phần dưới đây để biết các nhà cung cấp phổ biến)
6. Nhập **Tên hiển thị** để nhận biết tài khoản này (ví dụ: `Twilio - Chính`) 
7. Thiết lập **Cài đặt mặc định** (xem bên dưới)
8. Nhấp **Lưu**

## Thông tin xác thực nhà cung cấp

### Twilio

| Trường | Nơi tìm thấy |
|-------|-----------------|
| SID tài khoản | Trong Trang điều khiển Twilio → Bảng điều khiển |
| Token xác thực | Trong Trang điều khiển Twilio → Bảng điều khiển |
| Số điện thoại gửi | Số điện thoại Twilio của bạn ở định dạng E.164 (ví dụ: `+15551234567`) |

### Các nhà cung cấp khác

Các thành phần nhà cung cấp SMS đã cài đặt khác sẽ hiển thị các trường thông tin xác thực cụ thể của riêng họ khi được chọn. Tham khảo tài liệu của nhà cung cấp để biết giá trị chính xác cần thiết - thường là một khóa API hoặc mã truy cập và một định danh người gửi.

## Cài đặt mặc định

Sau khi nhập thông tin xác thực, hãy cấu hình cách tài khoản này được sử dụng:

- **Kích hoạt** - bật hoặc tắt tài khoản này. Các tài khoản không hoạt động sẽ không được sử dụng để gửi, ngay cả khi được đặt làm mặc định
- **Tài khoản SMS mặc định** - khi được chọn, tất cả thông báo SMS từ cửa hàng của bạn sẽ sử dụng tài khoản này. Chỉ có một tài khoản có thể là tài khoản SMS mặc định tại một thời điểm
- **Tài khoản WhatsApp mặc định** - nếu nhà cung cấp này hỗ trợ WhatsApp (ví dụ: Twilio qua WhatsApp Business API), hãy chọn để sử dụng nó làm tài khoản mặc định cho tin nhắn WhatsApp

## Kiểm tra kết nối

Sau khi lưu tài khoản nhà cung cấp, hãy kiểm tra xem thông tin xác thực có hoạt động không:

1. Truy cập **Hệ thống SMS > Tài khoản nhà cung cấp SMS**
2. Nhấp vào tài khoản nhà cung cấp của bạn để mở nó
3. Nhấp vào nút **Kiểm tra kết nối**
4. Spwig gửi một yêu cầu kiểm tra đến nhà cung cấp và cập nhật trường **Trạng thái kết nối**

| Trạng thái | Ý nghĩa |
|--------|---------|
| Kết nối | Thông tin xác thực hợp lệ và nhà cung cấp có thể truy cập được |
| Kết nối thất bại | Thông tin xác thực không đúng hoặc nhà cung cấp không thể truy cập được |
| Chưa kiểm tra | Kết nối chưa được kiểm tra |

Nếu kiểm tra thất bại, hãy kiểm tra lại thông tin xác thực của bạn và đảm bảo rằng tài khoản của bạn có quyền cần thiết tại bảng điều khiển nhà cung cấp.

## Cột trạng thái kết nối

Danh sách Tài khoản nhà cung cấp SMS hiển thị một nhãn **Kết nối** được mã hóa theo màu cho mỗi tài khoản:

- **Kết nối** (xanh lá) - tài khoản đang hoạt động
- **Kết nối thất bại** (đỏ) - thông tin xác thực đã thất bại - cập nhật chúng
- **Chưa kiểm tra** (xám) - tài khoản chưa được kiểm tra

## Một số mẹo

- Sử dụng Chỉ dẫn cài đặt cho nhà cung cấp đầu tiên của bạn - nó sẽ hướng dẫn bạn qua từng trường và kiểm tra kết nối trước khi lưu
- Chỉ có một tài khoản có thể là Tài khoản SMS mặc định tại một thời điểm.

Nếu bạn thêm tài khoản thứ hai và đánh dấu nó là mặc định, tài khoản mặc định trước đó sẽ tự động bị hủy bỏ
- Lưu lại thông tin xác thực API của nhà cung cấp ở nơi an toàn.

Nếu thông tin xác thực thay đổi, hãy cập nhật ngay tại đây để tránh thông báo thất bại
- Tài khoản không hoạt động vẫn sẽ hiển thị trong danh sách nhưng không được sử dụng để gửi — hữu ích để lưu trữ thông tin xác thực dự phòng mà không cần kích hoạt
- Hầu hết các nhà cung cấp tính phí theo tin nhắn được gửi — theo dõi việc sử dụng trong bảng điều khiển của nhà cung cấp để tránh hóa đơn bất ngờ