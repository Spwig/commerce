---
title: Đăng nhập của Nhân viên POS & Đăng nhập bằng Nhận dạng Sinh trắc học
---

Mọi người cần phục vụ khách hàng tại quầy POS đều cần có tài khoản nhân viên với quyền truy cập phù hợp. Chủ đề này giải thích cách tạo tài khoản đó, gán nhân viên với máy POS, và sau đó thiết lập đăng nhập bằng sinh trắc học để họ có thể mở quầy bằng vân tay, quét khuôn mặt hoặc khóa phần cứng thay vì nhập mật khẩu mỗi lần.

Để biết thông tin về mã PIN, giới hạn chiết khấu và cài đặt khóa máy, xem [Chiết khấu Nhân viên POS & An ninh Máy POS](pos-staff-discounts).

## Những gì nhân viên cần để sử dụng máy POS

Để đăng nhập vào máy POS, người dùng cần:

1. Một **tài khoản nhân viên** — một người dùng Spwig với cờ **Trạng thái Nhân viên** được bật.
2. Một **vai trò bao gồm quyền truy cập POS** — vai trò kiểm soát những gì nhân viên có thể làm bên trong trang quản trị. Một vai trò có quyền truy cập POS là cần thiết để truy cập quầy.
3. **Gán với máy** — máy phải liệt kê họ là nhân viên được gán, hoặc họ phải được gán tại cấp độ địa điểm cửa hàng.

## Tạo tài khoản nhân viên đủ điều kiện POS

Truy cập **Nhân viên & Tài khoản > Nhân viên** (hoặc đi đến `/admin/accounts/staffmember/`).

1. Nhấp **+ Thêm Nhân viên**.
2. Điền **tên**, **họ** và **địa chỉ email** của nhân viên.
3. Thiết lập mật khẩu tạm thời và yêu cầu nhân viên thay đổi mật khẩu khi đăng nhập lần đầu.
4. Đảm bảo **Trạng thái Nhân viên** được đánh dấu — đây là điều cho phép họ đăng nhập vào trang quản trị và ứng dụng POS.
5. Nhấp **Lưu**.

> **Lưu ý:** Không đánh dấu **Trạng thái Superuser** cho nhân viên thu ngân hoặc giám sát bình thường. Trạng thái Superuser bỏ qua tất cả kiểm tra quyền và nên được dành riêng cho chủ cửa hàng.

### Gán vai trò có quyền truy cập POS

Tài khoản nhân viên riêng biệt không có quyền — vai trò cấp quyền cụ thể. Sau khi tạo tài khoản, mở hồ sơ nhân viên và đi đến phần **Vai trò**. Gán một vai trò bao gồm quyền truy cập POS.

Để có giải thích đầy đủ về cách vai trò hoạt động và quyền cần bao gồm, xem [Vai trò Nhân viên](staff-roles).

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: staff-user-list.webp
  description: Danh sách nhân viên hiển thị người dùng đủ điều kiện POS với nhãn vai trò của họ
-->

![Danh sách nhân viên](/static/core/admin/img/help/pos-staff-login/staff-user-list.webp)

## Gán nhân viên cho máy POS

Cài đặt tuân theo quy tắc phân tầng: **Mặc định trang web → Nhóm cửa hàng → Địa điểm cửa hàng → Máy riêng lẻ**. Đối với hầu hết các cửa hàng, nơi đúng để gán nhân viên là tại cấp độ máy.

1. Truy cập **POS > Máy POS** (hoặc đi đến `/admin/pos_app/posterminal/`).
2. Mở máy bạn muốn cấu hình.
3. Đi đến tab **Gán Nhân viên**.
4. Trong trường **Nhân viên được gán**, tìm kiếm và thêm nhân viên.
5. Nhấp **Lưu**.

Những nhân viên xuất hiện trong danh sách **Nhân viên được gán** cho một máy có thể chọn tên của họ trên màn hình đăng nhập của máy đó. Nhân viên không được gán cho bất kỳ máy nào vẫn có thể đăng nhập bằng cách nhập email của họ trực tiếp.

> **Lưu ý:** Nếu cửa hàng của bạn có nhiều nhân viên luân chuyển giữa các máy, hãy gán họ tại cấp độ địa điểm (kho) thay vì từng máy. Bất kỳ nhân viên nào được gán cho địa điểm sẽ tự động có quyền truy cập tất cả các máy tại địa điểm đó.

## Đăng nhập tại quầy POS

Khi nhân viên mở ứng dụng POS (`/pos/`) trên máy, họ sẽ thấy màn hình chọn nhân viên. Quy trình đăng nhập hoạt động như sau:

1. Nhân viên chạm hoặc nhấp tên của họ trong danh sách (hoặc nhập email của họ nếu không được liệt kê).
2. Họ nhập mật khẩu của mình.
3. Họ được đăng nhập và quầy mở ra cho ca làm việc của họ.

Để biết thông tin về mở khóa bằng mã PIN (sau khi máy bị khóa trong ca làm việc), xem [Chiết khấu Nhân viên POS & An ninh Máy POS](pos-staff-discounts).

## Đăng nhập bằng sinh trắc học

Đăng nhập bằng sinh trắc học cho phép nhân viên chạm vào cảm biến vân tay, nhìn vào máy quét khuôn mặt hoặc chạm vào khóa phần cứng thay vì nhập mật khẩu. Trên quầy bận rộn, điều này tiết kiệm vài giây mỗi ca và tránh sai sót trong giờ cao điểm.

Spwig sử dụng tiêu chuẩn trình duyệt **WebAuthn** để đăng nhập bằng sinh trắc học.

Một "WebAuthn credential" là một cặp khóa gắn với thiết bị: khóa riêng được lưu trữ trong phần cứng an toàn của thiết bị và không bao giờ rời khỏi thiết bị đó.

Ứng dụng POS giao tiếp với phần cứng đó thông qua trình duyệt.

### Thiết bị và trình duyệt hỗ trợ đăng nhập sinh trắc học

WebAuthn được hỗ trợ bởi tất cả các trình duyệt hiện đại — Chrome, Edge, Firefox và Safari — trên các thiết bị có phần cứng tương thích. Các cấu hình phổ biến hoạt động tốt:

| Thiết bị | Authenticator |
|--------|---------------|
| iPad (Touch ID) | Vân tay qua Safari hoặc Chrome |
| Máy tính bảng Android | Vân tay hoặc khuôn mặt qua Chrome |
| Máy tính bảng hoặc máy tính Windows | Windows Hello (vân tay, khuôn mặt hoặc mã PIN) |
| Bất kỳ thiết bị nào + khóa bảo mật | Khóa FIDO2 qua USB, NFC hoặc Bluetooth (ví dụ: YubiKey) |
| iPhone (Face ID) | Khuôn mặt qua Safari |

Ứng dụng POS chỉ hiển thị tùy chọn đăng nhập sinh trắc học khi trình duyệt đã xác nhận rằng một credential đã được đăng ký cho người dùng hiện tại trên thiết bị đó.

### Cách đăng ký hoạt động

Đăng ký xảy ra tại máy POS, không phải trong phần quản trị. Nhân viên phải hoàn thành đăng nhập bằng mật khẩu bình thường trước, sau đó chọn thiết lập đăng nhập sinh trắc học từ bên trong ứng dụng POS. Trình duyệt sau đó sẽ yêu cầu họ xác minh danh tính bằng cảm biến sinh trắc học của thiết bị (hoặc passkey được lưu trữ trong tài khoản của họ trên iOS/macOS/Windows). Sau khi xác nhận, credential được lưu trữ và đăng nhập sinh trắc học sẽ có sẵn cho các ca làm việc tiếp theo trên thiết bị đó.

Một nhân viên có thể đăng ký trên nhiều thiết bị — ví dụ, một máy tính bảng cá nhân và một máy quầy chia sẻ — và mỗi thiết bị lưu trữ credential của riêng nó.

> **Lưu ý:** Từ ngữ cụ thể trong lời nhắc đăng ký ("Đăng ký sinh trắc học", "Thiết lập đăng nhập vân tay", v.v.) đến từ ứng dụng POS và có thể thay đổi tùy theo trình duyệt và thiết bị.

### Đăng nhập bằng sinh trắc học

Sau khi đã đăng ký, tên nhân viên trên màn hình đăng nhập sẽ hiển thị nút đăng nhập sinh trắc học (biểu tượng vân tay hoặc tương tự). Nhân viên:

1. Nhấn vào tên của họ trên màn hình đăng nhập của máy tính.
2. Nhấn **Đăng nhập bằng vân tay** (hoặc tương đương).
3. Đặt tay lên cảm biến hoặc nhìn vào camera.
4. Máy tính sẽ mở khóa ngay lập tức.

Nếu xác minh sinh trắc học thất bại (vân tay không được nhận diện, khuôn mặt bị che), nhân viên sẽ quay lại nhập mật khẩu của họ.

### Hủy bỏ một credential

Nếu thiết bị bị mất, bị trộm hoặc nhân viên rời đi, bạn nên xóa ngay credential sinh trắc học của họ.

1. Di chuyển đến **Nhân viên & Tài khoản > Nhân viên**.
2. Mở hồ sơ của nhân viên.
3. Cuộn xuống phần **Cài đặt POS**.
4. Trong hàng **Mở khóa sinh trắc học**, nhấp vào **Xóa tất cả**.
5. Xác nhận hành động.

Điều này xóa tất cả các credential WebAuthn đã đăng ký cho nhân viên đó trên mọi thiết bị. Lần tới họ cố gắng sử dụng đăng nhập sinh trắc học trên bất kỳ máy tính nào, họ sẽ phải đăng nhập bằng mật khẩu thay thế.

> **Quan trọng:** Xóa credential ở đây không chặn nhân viên đăng nhập bằng mật khẩu của họ. Để hủy quyền truy cập hoàn toàn, cũng hãy vô hiệu hóa tài khoản nhân viên hoặc xóa họ khỏi danh sách nhân viên được chỉ định trên máy tính.

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: Biểu mẫu thay đổi nhân viên hiển thị phần Cài đặt POS với số lượng credential sinh trắc học và nút Xóa tất cả
-->

## Ghi chú bảo mật

- **Các credential được gắn với phần cứng.** Khóa riêng không bao giờ rời khỏi phần tử an toàn của thiết bị.

Nếu một thiết bị bị đánh cắp, đối tượng tấn công không thể trích xuất khóa sinh trắc học — họ vẫn cần phải vượt qua màn hình khóa của thiết bị trước khi trình duyệt sẽ giải phóng khóa.
- **Mất thiết bị không làm rò rỉ mật khẩu.** WebAuthn thay thế mật khẩu cho thiết bị đó; mật khẩu của nhân viên là riêng biệt và không bị ảnh hưởng.
- **Hủy bỏ ngay khi nhân viên rời đi.** Xóa các thông tin sinh trắc học và vô hiệu hóa tài khoản nhân viên trong cùng một phiên khi chấm dứt hợp đồng với nhân viên.
- **Thông tin sinh trắc học không bao giờ được truyền đi.** Vết dấu vân tay hoặc quét khuôn mặt được xử lý hoàn toàn bởi phần cứng thiết bị.

Spwig chỉ nhận được phản hồi thách thức đã được ký, không có bất kỳ dữ liệu sinh trắc học nào.

## Khắc phục sự cố

### Nút **Đăng nhập bằng vân tay** không hiển thị

Tùy chọn sinh trắc học chỉ xuất hiện khi:
- Nhân viên đã đăng ký thông tin trên thiết bị cụ thể này.
- Trình duyệt hỗ trợ WebAuthn (tất cả trình duyệt hiện đại đều hỗ trợ — cập nhật nếu đang dùng phiên bản cũ hơn).

Nếu nút không hiển thị, nhân viên chưa đăng ký trên thiết bị này. Họ nên đăng nhập bằng mật khẩu của mình và thiết lập đăng nhập sinh trắc học thông qua ứng dụng POS.

### Đăng ký thất bại

Nguyên nhân phổ biến:
- **Quyền truy cập trình duyệt bị từ chối.** Trình duyệt yêu cầu quyền truy cập thiết bị xác thực và nhân viên đã từ chối. Họ cần thử lại và nhấn **Cho phép** khi được nhắc.
- **Không tìm thấy thiết bị xác thực tương thích.** Thiết bị không có cảm biến vân tay, máy ảnh khuôn mặt hoặc khóa bảo mật gắn kèm. Kiểm tra phần cứng thiết bị.
- **Thông tin xác thực trùng lặp.** Nhân viên có thể đã đăng ký trên thiết bị này. Các thông tin xác thực hiện tại sẽ bị loại bỏ trong quá trình đăng ký lại để tránh trùng lặp.

### Sinh trắc học hoạt động trên một thiết bị nhưng không hoạt động trên thiết bị khác

Mỗi thiết bị lưu trữ thông tin xác thực riêng của nó. Đăng ký trên một iPad không tự động hoạt động trên iPad thứ hai. Nhân viên phải hoàn tất quy trình đăng ký riêng biệt trên mỗi thiết bị họ sẽ sử dụng.

### Khóa truy cập đa thiết bị

Một số hệ điều hành (iOS 16+, macOS Ventura+, Windows 11 với tài khoản Microsoft) có thể đồng bộ khóa truy cập qua iCloud Keychain hoặc Windows Hello. Nếu nhân viên đã đăng ký bằng khóa truy cập được đồng bộ, nó có thể hoạt động tự động trên nhiều thiết bị. Hành vi phụ thuộc vào hệ điều hành và trình duyệt, không phải Spwig.

## Một số mẹo

- Thiết lập đăng nhập sinh trắc học trên các máy tính bán hàng chia sẻ trước khi nhân viên đến làm ca của họ — quy trình đăng ký 2 phút sẽ mượt hơn nhiều khi thực hiện mà không có khách hàng đang chờ.
- Gán vai trò có quyền POS hạn chế cho nhân viên thu ngân và vai trò quản lý riêng biệt cho giám sát. Giữ tài khoản của họ tách biệt khỏi tài khoản chủ cửa hàng.
- Khi nhân viên thay đổi thiết bị (máy tính bảng mới, điện thoại mới), hãy yêu cầu họ đăng ký trên thiết bị mới trước, sau đó hủy bỏ thông tin xác thực cũ từ trang quản trị nếu thiết bị không còn được sử dụng.
- Đối với các cửa hàng có tỷ lệ nhân viên thay đổi cao, hãy xem danh sách **Nhân viên được chỉ định** trên mỗi máy tính bán hàng định kỳ và xóa nhân viên không còn làm việc tại địa điểm đó.
- Nếu bạn sử dụng khóa bảo mật phần cứng (YubiKey hoặc tương tự), một khóa có thể được đăng ký trên nhiều máy tính bán hàng mà không cần thay đổi gì ở trang quản trị — chỉ cần cắm khóa vào và hoàn tất quy trình đăng ký trên mỗi máy tính bán hàng.