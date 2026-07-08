---
title: Đăng nhập đơn (SSO) cho quản trị viên
---

Đăng nhập đơn (SSO) cho phép nhân viên của bạn đăng nhập vào bảng điều khiển quản trị bằng nhà cung cấp danh tính của tổ chức thay vì tên người dùng và mật khẩu riêng biệt. Spwig hỗ trợ bất kỳ nhà cung cấp danh tính nào sử dụng giao thức OpenID Connect (OIDC), bao gồm Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak và các nhà cung cấp khác.

## Enterprise SSO là gì?

Enterprise SSO khác với đăng nhập mạng xã hội (đăng nhập bằng tài khoản Google hoặc Facebook cá nhân). Với Enterprise SSO:

- Nhân viên xác thực thông qua **nhà cung cấp danh tính của tổ chức** — hệ thống cùng mà họ sử dụng cho email, công cụ nội bộ và các ứng dụng kinh doanh khác
- Nhóm IT của bạn kiểm soát quyền truy cập tập trung — khi ai đó rời khỏi tổ chức, việc vô hiệu hóa tài khoản của họ trong nhà cung cấp danh tính sẽ ngay lập tức thu hồi quyền truy cập Spwig của họ
- Xác thực đa yếu tố (MFA) được thực thi bởi nhà cung cấp danh tính, mang lại chính sách bảo mật nhất quán cho tất cả các ứng dụng
- Nhân viên không cần nhớ mật khẩu riêng biệt cho Spwig

## Cách hoạt động

Khi SSO được bật, trang đăng nhập quản trị sẽ hiển thị nút **Đăng nhập bằng [Nhà cung cấp]**. Quy trình xác thực hoạt động như sau:

1. Nhân viên nhấp vào nút SSO trên trang đăng nhập Spwig
2. Họ được chuyển hướng đến trang đăng nhập của nhà cung cấp danh tính (ví dụ: đăng nhập Microsoft)
3. Họ xác thực với nhà cung cấp danh tính (bao gồm bất kỳ MFA nào mà nhà cung cấp yêu cầu)
4. Nhà cung cấp danh tính chuyển hướng họ trở lại Spwig với mã ủy quyền an toàn
5. Spwig đổi mã lấy thông tin người dùng và tạo phiên
6. Nhân viên đến trang bảng điều khiển quản trị, đã được xác thực đầy đủ

Điều này sử dụng giao thức **OpenID Connect (OIDC)** tiêu chuẩn ngành, được hỗ trợ bởi hầu hết các nhà cung cấp danh tính doanh nghiệp.

## Bật SSO

SSO được cấu hình tại hai nơi:

1. **Cài đặt Website > Tab Bảo mật** — Bật hoặc tắt SSO và kiểm soát tính khả thi của đăng nhập mật khẩu
2. **Cấu hình Nhà cung cấp SSO** — Nhập chi tiết OIDC của nhà cung cấp danh tính của bạn

### Bước 1: Cấu hình nhà cung cấp danh tính

Trước khi bật SSO trong Spwig, bạn cần đăng ký Spwig là một ứng dụng trong nhà cung cấp danh tính của bạn. Xem hướng dẫn cụ thể cho nhà cung cấp:

- **Microsoft Entra ID** — xem hướng dẫn thiết lập Microsoft Entra ID
- **Google Workspace** — xem hướng dẫn thiết lập Google Workspace
- **Okta** — xem hướng dẫn thiết lập Okta
- **Các nhà cung cấp khác** — bất kỳ nhà cung cấp nào tuân thủ OIDC đều hoạt động. Đăng ký một ứng dụng web với URI chuyển hướng `https://your-store.com/oidc/callback/` và tham khảo tài liệu của nhà cung cấp để tìm URL khám phá OIDC, ID Khách hàng và Mật khẩu Khách hàng.

### Bước 2: Cấu hình Nhà cung cấp SSO trong Spwig

Di chuyển đến trang **Cấu hình Nhà cung cấp SSO** (liên kết từ tab Bảo mật hoặc truy cập tại **Enterprise SSO > Cấu hình Nhà cung cấp SSO** trong thanh bên quản trị). Nhập:

1. **Tên Nhà cung cấp** — hiển thị trên nút đăng nhập (ví dụ: "Microsoft Entra ID")
2. **URL Khám phá OIDC** — URL `.well-known/openid-configuration` của nhà cung cấp của bạn. Nhấp **Khám phá tự động** để tự động điền các trường điểm cuối.
3. **ID Khách hàng** và **Mật khẩu Khách hàng** — từ đăng ký ứng dụng của nhà cung cấp danh tính của bạn

Mật khẩu khách hàng được lưu trữ dưới dạng mã hóa và không bao giờ được hiển thị sau khi lưu.

### Bước 3: Bật SSO trong Cài đặt Website

Di chuyển đến **Cài đặt Website > Tab Bảo mật** và đánh dấu **Bật SSO cho đăng nhập quản trị**. Nút SSO sẽ ngay lập tức xuất hiện trên trang đăng nhập quản trị.

## Cài đặt SSO

| Cài đặt | Mô tả |
|---------|-------------|
| **Bật SSO cho đăng nhập quản trị** | Hiển thị nút SSO trên trang đăng nhập quản trị. Không ảnh hưởng đến đăng nhập mật khẩu thông thường trừ khi bạn cũng tắt nó. |
| **Cho phép đăng nhập mật khẩu trên trang quản trị** | Khi không được chọn, biểu mẫu mật khẩu được ẩn sau một nút gập. Nhân viên chỉ thấy nút SSO mặc định. Biểu mẫu mật khẩu vẫn có thể được truy cập bằng cách nhấp vào "Đăng nhập bằng tài khoản cục bộ" hoặc bằng cách thêm `?password=1` vào URL đăng nhập. |

### Hành vi trang đăng nhập

| SSO Enabled | Password Login | Result |
|-------------|---------------|--------|
| Off | On | Trang đăng nhập tiêu chuẩn chỉ có biểu mẫu tên người dùng/mật khẩu |
| On | On | Nút SSO ở trên cùng, "hoặc" phân tách, sau đó là biểu mẫu mật khẩu bên dưới |
| On | Off | Chỉ có nút SSO. Biểu mẫu mật khẩu được ẩn sau một chuyển đổi "Đăng nhập bằng tài khoản cục bộ" |
| Off | Off | Không thể — đăng nhập bằng mật khẩu sẽ được kích hoạt lại tự động nếu SSO bị tắt hoặc không được cấu hình |

## User Matching

Khi một nhân viên đăng nhập qua SSO, Spwig sẽ khớp họ với tài khoản người dùng hiện có bằng **địa chỉ email** (không phân biệt chữ hoa chữ thường). Địa chỉ email từ các tuyên bố của nhà cung cấp danh tính phải khớp với địa chỉ email trên tài khoản Spwig của nhân viên.

Nếu không tìm thấy người dùng khớp:

- **Tự động tạo người dùng bị tắt** (mặc định) — đăng nhập bị từ chối. Bạn phải tạo tài khoản nhân viên trong Spwig trước với địa chỉ email khớp.
- **Tự động tạo người dùng được bật** — một tài khoản người dùng mới được tạo tự động với tên và email từ các tuyên bố của nhà cung cấp danh tính.

Cài đặt **Hạn chế chỉ dành cho Nhân viên** (mặc định được bật) thêm một kiểm tra bổ sung: ngay cả khi tài khoản người dùng tồn tại, đăng nhập sẽ bị từ chối trừ khi người dùng có trạng thái nhân viên. Điều này ngăn chặn các tài khoản không phải nhân viên truy cập bảng điều khiển quản trị qua SSO.

## Role Mapping

Nếu nhà cung cấp danh tính của bạn gửi thông tin thành viên nhóm trong các tuyên bố OIDC, Spwig có thể tự động thiết lập trạng thái nhân viên và siêu người dùng dựa trên thành viên nhóm.

Để cấu hình ánh xạ vai trò:

1. Trong Cấu hình Nhà cung cấp SSO, đặt trường **Tuyên bố Nhóm** thành tên tuyên bố mà nhà cung cấp của bạn sử dụng (mặc định: `groups`)
2. Trong **Nhóm Nhân viên**, nhập tên hoặc ID nhóm được phân tách bằng dấu phẩy. Người dùng trong bất kỳ nhóm nào cũng sẽ được cấp trạng thái nhân viên.
3. Trong **Nhóm Siêu người dùng**, nhập tên hoặc ID nhóm được phân tách bằng dấu phẩy. Người dùng trong bất kỳ nhóm nào cũng sẽ được cấp trạng thái siêu người dùng.

Ánh xạ vai trò được đánh giá mỗi lần người dùng đăng nhập qua SSO. Nếu người dùng bị loại khỏi nhóm trong nhà cung cấp danh tính, trạng thái nhân viên hoặc siêu người dùng của họ sẽ được cập nhật khi họ đăng nhập SSO lần tiếp theo.

**Lưu ý:** Microsoft Entra ID gửi **ID Đối tượng** (UUID) của nhóm theo mặc định, không phải tên nhóm. Sao chép ID Đối tượng từ Azure portal khi cấu hình ánh xạ vai trò. Các nhà cung cấp khác như Okta thường gửi tên nhóm.

## Claims Mapping

Spwig đọc thông tin người dùng từ các tuyên bố OIDC tiêu chuẩn. Các giá trị mặc định hoạt động với hầu hết các nhà cung cấp, nhưng bạn có thể tùy chỉnh tên trường tuyên bố trong Cấu hình Nhà cung cấp SSO:

| Setting | Default | Description |
|---------|---------|-------------|
| **Email Claim** | `email` | Tuyên bố chứa địa chỉ email của người dùng |
| **First Name Claim** | `given_name` | Tuyên bố chứa tên đầu của người dùng |
| **Last Name Claim** | `family_name` | Tuyên bố chứa họ của người dùng |
| **Groups Claim** | `groups` | Tuyên bố chứa thành viên nhóm (trống để tắt ánh xạ vai trò) |

## MFA Behavior

Khi một nhân viên đăng nhập qua SSO, yêu cầu xác thực hai yếu tố (2FA) tích hợp của Spwig sẽ được bỏ qua tự động. Điều này là vì nhà cung cấp danh tính chịu trách nhiệm thực thi MFA làm phần của quy trình đăng nhập SSO.

Nếu tổ chức của bạn yêu cầu MFA, hãy cấu hình nó trong chính sách truy cập điều kiện của nhà cung cấp danh tính thay vì trong cài đặt 2FA của Spwig. Điều này cho phép bạn quản lý MFA tập trung tại tất cả các ứng dụng của bạn.

## Recovery Access

Nếu nhà cung cấp danh tính của bạn gặp sự cố hoặc cấu hình sai, bạn vẫn có thể truy cập biểu mẫu đăng nhập quản trị:

- **Nhấn vào chuyển đổi** — Nếu đăng nhập bằng mật khẩu bị tắt, nhấn "Đăng nhập bằng tài khoản cục bộ" trên trang đăng nhập để hiển thị biểu mẫu mật khẩu
- **Tham số URL** — Thêm `?password=1` vào URL đăng nhập quản trị (ví dụ: `https://your-store.com/en/admin/login/?password=1`) để hiển thị biểu mẫu mật khẩu trực tiếp
- **Đăng nhập bằng mật khẩu luôn có sẵn** — Ngay cả khi bị ẩn khỏi giao diện người dùng, nền tảng xác thực mật khẩu vẫn hoạt động. Chỉ tính năng hiển thị biểu mẫu bị ảnh hưởng.

Spwig cũng ngăn không cho bạn tắt đăng nhập bằng mật khẩu trừ khi SSO đã được bật và cấu hình đúng — bạn không thể vô tình khóa chính mình ra ngoài.

## Các nhà cung cấp được hỗ trợ

Spwig hoạt động với bất kỳ nhà cung cấp danh tính nào hỗ trợ giao thức OpenID Connect (OIDC). Các hướng dẫn cài đặt chi tiết có sẵn cho:

- **Microsoft Entra ID** (trước đây là Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

Đối với các nhà cung cấp tuân thủ OIDC khác (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud, v.v.), các bước cấu hình của Spwig là giống nhau — bạn cần URL khám phá OIDC của nhà cung cấp, Client ID và Client Secret. Tham khảo tài liệu của nhà cung cấp để biết cách đăng ký ứng dụng web và nhận các thông tin xác thực này. URI chuyển hướng cần sử dụng luôn là `https://your-store.com/oidc/callback/`.

## Mẹo

- **Bắt đầu bằng cách bật đăng nhập bằng mật khẩu** — Bật SSO cùng với đăng nhập bằng mật khẩu. Sau khi bạn đã xác nhận SSO hoạt động cho nhóm của mình, bạn có thể chọn tắt đăng nhập bằng mật khẩu.
- **Thử nghiệm trong cửa sổ ẩn danh** — Sử dụng cửa sổ trình duyệt riêng tư/ẩn danh để kiểm tra SSO mà không bị ảnh hưởng bởi phiên quản trị hiện tại của bạn.
- **Tạo tài khoản nhân viên trước** — Trừ khi bạn bật Tự động tạo người dùng, nhân viên cần có tài khoản Spwig hiện có với địa chỉ email khớp trước khi họ có thể đăng nhập qua SSO.
- **Sử dụng nút Tự động khám phá** — Nhập URL khám phá OIDC của nhà cung cấp và nhấn Tự động khám phá để tự động điền tất cả các trường điểm cuối. Điều này nhanh hơn và ít sai sót hơn so với việc nhập các điểm cuối thủ công.
- **Giữ một tài khoản quản trị cục bộ** — Luôn duy trì ít nhất một tài khoản quản trị cục bộ có mật khẩu làm phương án phục hồi trong trường hợp xảy ra sự cố với nhà cung cấp danh tính.
- **Theo dõi thời hạn hết hạn của client secret** — Một số nhà cung cấp (đặc biệt là Microsoft Entra ID) cấp client secret có ngày hết hạn. Đặt lời nhắc lịch để xoay đổi mật khẩu trước khi nó hết hạn.