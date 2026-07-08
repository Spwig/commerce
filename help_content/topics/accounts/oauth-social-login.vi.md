---
title: Cài đặt xác thực OAuth và Đăng nhập xã hội
---

OAuth và đăng nhập xã hội cho phép khách hàng đăng nhập vào cửa hàng của bạn bằng tài khoản Google, Apple hoặc Microsoft hiện có — không cần tạo và ghi nhớ mật khẩu khác nữa.

![Cài đặt OAuth](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## OAuth / Đăng nhập xã hội là gì?

OAuth là tiêu chuẩn xác thực an toàn cho phép khách hàng đăng nhập bằng thông tin xác thực từ các nhà cung cấp đáng tin cậy như Google, Apple hoặc Microsoft.

### Lợi ích

- **Thanh toán nhanh hơn** — Khách hàng bỏ qua biểu mẫu đăng ký và đăng nhập bằng một cú nhấp chuột
- **Giảm ma sát** — Không cần tạo mật khẩu, email xác nhận hoặc quy trình quên mật khẩu
- **Chuyển đổi tốt hơn** — Các nghiên cứu cho thấy đăng nhập xã hội có thể tăng tỷ lệ chuyển đổi lên 20-40%
- **An ninh được cải thiện** — Thông tin xác thực không đi qua cửa hàng của bạn; xác thực được xử lý bởi nhà cung cấp
- **Tăng độ tin cậy của khách hàng** — Khách hàng tin tưởng các nhà cung cấp đã thiết lập với thông tin xác thực của họ

### Cách hoạt động

1. Khách hàng nhấp vào "Đăng nhập bằng Google" (hoặc Apple/Microsoft) trên trang đăng nhập của bạn
2. Họ được chuyển hướng đến trang đăng nhập an toàn của nhà cung cấp
3. Khách hàng xác thực bằng thông tin xác thực của nhà cung cấp
4. Nhà cung cấp gửi thông tin danh tính đã xác minh trở lại cửa hàng của bạn
5. Khách hàng được đăng nhập tự động

Trên lần đăng nhập đầu tiên, một tài khoản khách hàng mới sẽ được tạo tự động bằng email và thông tin hồ sơ từ nhà cung cấp.

## Nhà cung cấp được hỗ trợ

Spwig hỗ trợ ba nhà cung cấp OAuth chính:

| Nhà cung cấp | Trường hợp sử dụng | Yêu cầu thông tin xác thực |
|----------|----------|------------------------|
| **Google** | Phổ biến nhất, dễ thiết lập nhất | Client ID, Client Secret |
| **Apple** | Yêu cầu cho ứng dụng iOS, tập trung vào quyền riêng tư | Client ID, Team ID, Key ID, Private Key |
| **Microsoft** | Khách hàng doanh nghiệp, người dùng Office 365 | Client ID, Client Secret, Tenant ID |

Bạn có thể bật một, hai hoặc cả ba nhà cung cấp. Mỗi nhà cung cấp hoạt động độc lập.

## Cài đặt OAuth Google

OAuth Google là lựa chọn phổ biến nhất và dễ cấu hình nhất.

### Yêu cầu trước

- Tài khoản Google
- Truy cập vào Google Cloud Console

### Cài đặt từng bước

1. **Di chuyển đến Cài đặt OAuth**
   - Đi đến **Cài đặt > Cài đặt Cửa hàng** trong bảng điều khiển quản trị của bạn
   - Cuộn xuống phần **Nhà cung cấp OAuth**
   - Nhấp vào **Cấu hình Google**

2. **Tạo dự án Google Cloud**
   - Truy cập [Google Cloud Console](https://console.cloud.google.com/)
   - Nhấp vào **Tạo Dự án**
   - Nhập tên dự án (ví dụ: "OAuth Cửa hàng của tôi")
   - Nhấp vào **Tạo**

3. **Kích hoạt API Google+**
   - Trong thanh bên trái, đi đến **APIs & Services > Thư viện**
   - Tìm kiếm "Google+ API"
   - Nhấp vào **Kích hoạt**

4. **Tạo thông tin xác thực OAuth**
   - Đi đến **APIs & Services > Thông tin xác thực**
   - Nhấp vào **Tạo thông tin xác thực > OAuth client ID**
   - Chọn loại ứng dụng: **Ứng dụng Web**
   - Nhập tên (ví dụ: "Đăng nhập Cửa hàng")

5. **Cấu hình URI chuyển hướng**
   - Dưới **URI chuyển hướng được phép**, thêm:
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - Thay thế `yourdomain.com` bằng tên miền thực tế của bạn
   - Nhấp vào **Tạo**

6. **Sao chép thông tin xác thực**
   - Sao chép **Client ID** và **Client Secret** từ hộp thoại bật lên

7. **Nhập thông tin xác thực vào Spwig**
   - Trở lại cài đặt OAuth trong bảng điều khiển quản trị Spwig
   - Dán Client ID và Client Secret
   - Nhấp vào **Lưu**
   - Bật **Kích hoạt OAuth Google** để kích hoạt

### Kiểm tra

- Truy cập trang đăng nhập cửa hàng của bạn
- Tìm nút "Đăng nhập bằng Google"
- Nhấp vào và xác thực bằng tài khoản Google của bạn
- Bạn nên được đăng nhập và chuyển hướng đến bảng điều khiển khách hàng của bạn

## Cài đặt OAuth Apple

OAuth Apple phức tạp hơn Google do hệ thống xác thực dựa trên khóa.

### Yêu cầu trước

- Tài khoản Nhà phát triển Apple (yêu cầu thành viên trả phí)
- Truy cập vào cổng thông tin Nhà phát triển Apple

### Cài đặt từng bước

1. **Di chuyển đến Cài đặt OAuth**
   - Đi đến **Cài đặt > Cài đặt Cửa hàng > Nhà cung cấp OAuth**
   - Nhấp vào **Cấu hình Apple**

2. **Tạo ID Dịch vụ**
   - Đăng nhập vào [Apple Developer](https://developer.apple.com/account/)
   - Đi đến **Chứng chỉ, ID và hồ sơ**
   - Nhấp vào **ID** và sau đó là nút **+**
   - Chọn **ID Dịch vụ** và nhấp **Tiếp tục**
   - Nhập mô tả (ví dụ: "Đăng nhập Cửa hàng")
   - Nhập ID dịch vụ (ví dụ: `com.yourstore.login`)
   - Nhấp **Tiếp tục** và sau đó **Đăng ký**

3. **Cấu hình ID Dịch vụ**
   - Nhấp vào ID Dịch vụ mới tạo
   - Chọn **Đăng nhập bằng Apple**
   - Nhấp **Cấu hình**
   - Thêm tên miền và URL trả về:
     - **Tên miền**: `yourdomain.com`
     - **URL trả về**: `https://yourdomain.com/accounts/apple/login/callback/`
   - Nhấp **Lưu** và sau đó **Tiếp tục** và **Lưu** thêm lần nữa

4. **Tạo Khóa**
   - Trong thanh bên trái, nhấp vào **Khóa** và sau đó là nút **+**
   - Nhập tên khóa (ví dụ: "Khóa OAuth Cửa hàng")
   - Chọn **Đăng nhập bằng Apple**
   - Nhấp **Cấu hình** và chọn ID ứng dụng chính của bạn
   - Nhấp **Lưu**, sau đó **Tiếp tục** và **Đăng ký**
   - **Tải xuống tệp khóa** (.p8) — bạn không thể tải xuống nó lần nữa

5. **Thu thập thông tin cần thiết**
   Bạn cần:
   - **Client ID** (ID Dịch vụ): ID bạn đã tạo (ví dụ: `com.yourstore.login`)
   - **Team ID**: Được tìm thấy ở góc trên bên phải của cổng thông tin Nhà phát triển Apple
   - **Key ID**: Hiển thị khi bạn tạo khóa
   - **Private Key**: Nội dung của tệp .p8 bạn đã tải xuống

6. **Nhập thông tin xác thực vào Spwig**
   - Trở lại cài đặt OAuth trong Spwig
   - Dán Client ID, Team ID và Key ID
   - Mở tệp .p8 trong trình soạn thảo văn bản và sao chép nội dung của nó
   - Dán toàn bộ khóa (bao gồm tiêu đề) vào trường Private Key
   - Nhấp **Lưu**
   - Bật **Kích hoạt OAuth Apple** để kích hoạt

### Kiểm tra

- Truy cập trang đăng nhập cửa hàng của bạn trên thiết bị có ID Apple
- Nhấp vào "Đăng nhập bằng Apple"
- Xác thực bằng ID Apple của bạn
- Bạn nên được đăng nhập thành công

## Cài đặt OAuth Microsoft

OAuth Microsoft lý tưởng cho các cửa hàng nhắm đến khách hàng doanh nghiệp sử dụng Office 365 hoặc Azure AD.

### Yêu cầu trước

- Tài khoản Microsoft
- Truy cập vào Azure Portal

### Cài đặt từng bước

1. **Di chuyển đến Cài đặt OAuth**
   - Đi đến **Cài đặt > Cài đặt Cửa hàng > Nhà cung cấp OAuth**
   - Nhấp vào **Cấu hình Microsoft**

2. **Đăng ký Ứng dụng trong Azure**
   - Truy cập [Azure Portal](https://portal.azure.com/)
   - Đi đến **Azure Active Directory > Đăng ký ứng dụng**
   - Nhấp vào **Đăng ký mới**
   - Nhập tên (ví dụ: "OAuth Cửa hàng")
   - Chọn **Tài khoản trong bất kỳ thư mục tổ chức nào và tài khoản Microsoft cá nhân**
   - Dưới **URI chuyển hướng**, chọn **Web** và nhập:
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - Nhấp vào **Đăng ký**

3. **Sao chép ID Ứng dụng**
   - Trên trang tổng quan ứng dụng, sao chép **ID Ứng dụng (client) ID**

4. **Tạo Khóa bí mật Client**
   - Trong thanh bên trái, nhấp vào **Chứng chỉ & bí mật**
   - Nhấp vào **Tạo bí mật client mới**
   - Nhập mô tả (ví dụ: "Bí mật OAuth")
   - Chọn thời gian hết hạn (khuyến nghị: 24 tháng)
   - Nhấp vào **Thêm**
   - **Sao chép giá trị bí mật ngay lập tức** — nó sẽ không được hiển thị lại

5. **Nhập thông tin xác thực vào Spwig**
   - Trở lại cài đặt OAuth trong Spwig
   - Dán ID Ứng dụng (client) ID làm Client ID
   - Dán giá trị bí mật làm Client Secret
   - Tùy chọn nhập ID Tenant (cho ứng dụng đơn thư mục; để trống cho ứng dụng đa thư mục)
   - Nhấp **Lưu**
   - Bật **Kích hoạt OAuth Microsoft** để kích hoạt

### Kiểm tra

- Truy cập trang đăng nhập cửa hàng của bạn
- Nhấp vào "Đăng nhập bằng Microsoft"
- Xác thực bằng tài khoản Microsoft của bạn
- Bạn nên được đăng nhập thành công

## Quản lý kết nối OAuth

### Quan điểm của khách hàng

Khách hàng có thể xem và quản lý các nhà cung cấp OAuth đã kết nối từ bảng điều khiển tài khoản của họ:

- Di chuyển đến **Tài khoản của tôi > Tài khoản đã kết nối**
- Xem các nhà cung cấp nào được liên kết (Google, Apple, Microsoft)
- Ngắt kết nối nhà cung cấp bằng cách nhấp vào **Ngắt kết nối**
- Kết nối lại bằng cách đăng nhập bằng nhà cung cấp đó lần nữa

### Nhiều nhà cung cấp

Một tài khoản khách hàng có thể được liên kết với nhiều nhà cung cấp OAuth. Ví dụ, một khách hàng có thể kết nối cả Google và Apple với cùng một tài khoản.

Nếu một khách hàng cố gắng đăng nhập bằng nhà cung cấp OAuth khác nhau bằng cùng một địa chỉ email, Spwig tự động liên kết nó với tài khoản hiện có của họ.

### Quản lý của quản trị viên

Làm quản trị viên, bạn có thể xem kết nối OAuth của khách hàng:

- Đi đến **Khách hàng > Khách hàng**
- Mở hồ sơ khách hàng
- Cuộn xuống phần **Tài khoản đã kết nối**
- Xem các nhà cung cấp nào được liên kết và thời gian họ được liên kết

Bạn không thể ngắt kết nối nhà cung cấp thay mặt khách hàng — họ phải tự thực hiện để đảm bảo an ninh.

## Khắc phục sự cố

### Mismatch URI chuyển hướng

**Lỗi**: "Mismatch URI chuyển hướng" hoặc "URI chuyển hướng không hợp lệ"

**Giải pháp**:
- Đảm bảo URI chuyển hướng trong cài đặt nhà cung cấp của bạn khớp chính xác với URI trong Spwig
- Kiểm tra xem có dấu gạch chéo cuối hay không — chúng phải khớp
- Xác nhận bạn đang sử dụng `https://` (không phải `http://`)
- Xóa bộ nhớ cache trình duyệt và thử lại

### Thông tin xác thực không hợp lệ

**Lỗi**: "Client ID không hợp lệ" hoặc "Xác thực thất bại"

**Giải pháp**:
- Kiểm tra lại xem bạn đã sao chép Client ID và Client Secret chính xác chưa
- Đảm bảo không có khoảng trắng hoặc dòng mới thừa
- Xác nhận thông tin xác thực đến từ dự án/app đúng
- Đối với Apple, đảm bảo Private Key bao gồm toàn bộ nội dung tệp .p8

### API nhà cung cấp không được kích hoạt

**Lỗi**: "API không được kích hoạt" hoặc "Không được cấu hình truy cập"

**Giải pháp**:
- Đối với Google: Đảm bảo bạn đã kích hoạt API Google+ trong dự án Google Cloud của bạn
- Đối với Microsoft: Xác nhận việc đăng ký ứng dụng của bạn đã được phê duyệt và đang hoạt động
- Đối với Apple: Kiểm tra xem "Đăng nhập bằng Apple" đã được kích hoạt cho ID Dịch vụ của bạn

### Yêu cầu SSL

**Lỗi**: "OAuth yêu cầu HTTPS" hoặc "URI chuyển hướng không an toàn"

**Giải pháp**:
- Các nhà cung cấp OAuth yêu cầu SSL/TLS (HTTPS) để an ninh
- Đảm bảo cửa hàng của bạn có cài đặt chứng chỉ SSL hợp lệ
- Cập nhật URI chuyển hướng của bạn để sử dụng `https://` thay vì `http://`
- Nếu đang kiểm tra cục bộ, sử dụng dịch vụ như ngrok để tạo đường hầm HTTPS

### Nút không hiển thị

**Vấn đề**: Nút "Đăng nhập bằng Google/Apple/Microsoft" không hiển thị trên trang đăng nhập

**Giải pháp**:
- Xác nhận nhà cung cấp đã được bật trong cài đặt OAuth
- Xóa bộ nhớ cache trình duyệt và làm tươi trang
- Kiểm tra xem chủ đề của bạn có bao gồm mẫu đăng nhập xã hội không
- Xem lại bảng điều khiển trình duyệt để tìm lỗi JavaScript

## Mẹo và Thực hành Tốt nhất

### An ninh

- **Thay đổi mật khẩu định kỳ** — Cập nhật Client Secrets mỗi 12-24 tháng
- **Theo dõi lần đăng nhập thất bại** — Theo dõi các mẫu xác thực bất thường
- **Sử dụng thông tin xác thực riêng biệt cho từng môi trường** — Thông tin xác thực khác nhau cho môi trường staging và production
- **Hạn chế URI chuyển hướng** — Chỉ thêm URI chính xác bạn cần

### Trải nghiệm người dùng

- **Bật cả ba nhà cung cấp** — Cho phép khách hàng lựa chọn; các nhóm dân số khác nhau ưa thích các nhà cung cấp khác nhau
- **Đặt nút nổi bật** — Nút đăng nhập xã hội nên được đặt trên biểu mẫu email/mật khẩu
- **Sử dụng thương hiệu dễ nhận biết** — Giữ nguyên kiểu dáng nút Google/Apple/Microsoft tiêu chuẩn
- **Kiểm tra trên thiết bị di động** — Các quy trình OAuth hoạt động khác nhau trên trình duyệt di động

### Tuân thủ

- **Chính sách bảo mật** — Công khai rằng bạn sử dụng nhà cung cấp OAuth và dữ liệu bạn nhận được
- **Điều khoản dịch vụ** — Tuân thủ điều khoản nhà cung cấp (Google, Apple, Microsoft mỗi nhà cung cấp đều có yêu cầu)
- **Giảm thiểu dữ liệu** — Chỉ yêu cầu thông tin hồ sơ bạn thực sự cần

### Danh sách kiểm tra kiểm tra

Trước khi đưa vào hoạt động, hãy kiểm tra:

- [ ] Đăng nhập bằng từng nhà cung cấp trên máy tính để bàn
- [ ] Đăng nhập bằng từng nhà cung cấp trên thiết bị di động
- [ ] Đăng nhập lần đầu (tạo tài khoản)
- [ ] Đăng nhập lần sau (liên kết tài khoản)
- [ ] Đăng nhập bằng cùng một email qua các nhà cung cấp khác nhau
- [ ] Ngắt kết nối và liên kết lại một nhà cung cấp
- [ ] Quy trình đặt lại mật khẩu vẫn hoạt động cho người dùng không dùng OAuth

