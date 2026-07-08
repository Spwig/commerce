---
title: 'Cấu hình SSO: Okta'
---

Hướng dẫn này sẽ hướng dẫn bạn cách kết nối Spwig với Okta để bật tính năng đăng nhập duy nhất (single sign-on) cho quản trị viên. Sau khi cấu hình, nhân viên của bạn có thể đăng nhập vào bảng điều khiển quản trị Spwig bằng tài khoản Okta của họ.

**Lưu ý:** Okta có thể cập nhật giao diện bảng điều khiển quản trị theo thời gian. Các hướng dẫn này được viết dựa trên bảng điều khiển quản trị Okta vào đầu năm 2026. Nếu các bước có sự khác biệt so với những gì bạn thấy, vui lòng tham khảo tài liệu chính thức của Okta tại [tạo tích hợp ứng dụng OIDC](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/).

## Yêu cầu trước

- Một tổ chức Okta (bất kỳ cấp độ nào — tài khoản phát triển miễn phí có thể dùng để kiểm tra)
- Vai trò **Super Administrator** hoặc **Application Administrator** trong Okta
- URL cửa hàng Spwig của bạn (ví dụ: `https://your-store.com`)
- Nhân viên phải có địa chỉ email trong Spwig khớp với tài khoản Okta của họ

## Bước 1: Tạo Ứng dụng

1. Đăng nhập vào [Okta Admin Console](https://your-org-admin.okta.com)
2. Di chuyển đến **Applications > Applications**
3. Nhấp **Create App Integration**
4. Chọn:

| Field | Value |
|-------|-------|
| **Sign-in method** | OIDC - OpenID Connect |
| **Application type** | Web Application |

5. Nhấp **Next**

## Bước 2: Cấu hình Ứng dụng

Điền các cài đặt ứng dụng:

| Field | Value |
|-------|-------|
| **App integration name** | `Spwig Admin SSO` (hoặc bất kỳ tên nào bạn ưa thích) |
| **Grant type** | Authorization Code (nên được chọn mặc định) |
| **Sign-in redirect URIs** | `https://your-store.com/oidc/callback/` |
| **Sign-out redirect URIs** | `https://your-store.com/en/admin/login/` |
| **Controlled access** | Chọn dựa trên nhu cầu của bạn (xem bên dưới) |

Đối với **Controlled access**, chọn một trong các tùy chọn sau:

- **Cho phép tất cả người dùng trong tổ chức của bạn truy cập** — tất cả người dùng Okta có thể đăng nhập (bạn vẫn có thể kiểm soát quyền truy cập Spwig bằng cài đặt Restrict to Staff)
- **Hạn chế quyền truy cập đến các nhóm đã chọn** — chỉ người dùng trong các nhóm Okta cụ thể mới có thể đăng nhập
- **Bỏ qua việc gán nhóm cho lúc này** — bạn sẽ gán người dùng hoặc nhóm thủ công sau này

Nhấp **Save**.

**Quan trọng:** URI chuyển hướng đăng nhập phải khớp chính xác với `https://your-store.com/oidc/callback/` — bao gồm cả dấu gạch chéo ở cuối.

## Bước 3: Lấy Thông tin Khách hàng

Sau khi lưu, tab **General** của ứng dụng sẽ hiển thị thông tin xác thực của bạn:

| Value | Where to Find It |
|-------|-----------------|
| **Client ID** | Tab General, phần Client Credentials |
| **Client Secret** | Tab General, phần Client Credentials (nhấp vào biểu tượng mắt để hiển thị) |

Sao chép cả hai giá trị — bạn sẽ cần chúng cho Spwig.

## Bước 4: Xây dựng URL Khám phá

URL Khám phá phụ thuộc vào tổ chức Okta và máy chủ ủy quyền của bạn:

**Máy chủ ủy quyền mặc định (thường gặp nhất):**

Click **Thêm yêu cầu**
5.

Cấu hình yêu cầu:

| Trường | Giá trị |
|-------|-------|
| **Tên** | `groups` |
| **Bao gồm trong loại token** | ID Token, Luôn |
| **Loại giá trị** | Groups |
| **Lọc** | Phù hợp với regex: `.*` (để bao gồm tất cả các nhóm) |
| **Bao gồm trong** | Bất kỳ phạm vi nào (hoặc `openid` nếu bạn muốn giới hạn) |

6. Click **Tạo**

**Lưu ý:** Khác với Microsoft Entra ID gửi Object IDs, Okta gửi **tên nhóm** theo mặc định. Điều này làm cho ánh xạ vai trò trở nên trực quan hơn — bạn có thể sử dụng tên hiển thị của nhóm Okta của bạn trực tiếp trong các trường Nhóm Nhân viên và Nhóm Superuser của Spwig.

### Lọc Nhóm

Nếu người dùng của bạn thuộc nhiều nhóm Okta và bạn chỉ muốn bao gồm một số cụ thể trong token:

- Thay đổi bộ lọc từ `.*` thành regex cụ thể hơn, ví dụ `^Spwig.*` để chỉ bao gồm các nhóm bắt đầu bằng "Spwig"
- Hoặc sử dụng bộ lọc **Bắt đầu bằng**, **Bằng**, hoặc **Chứa** thay vì regex

## Bước 7: Cấu hình trong Spwig

1. Trong trang quản trị Spwig, chuyển đến **Enterprise SSO > Cấu hình Cung cấp SSO**
2. Đặt **Tên Cung cấp** thành `Okta`
3. Nhập URL Khám phá từ Bước 4
4. Click **Khám phá tự động** — điều này tự động điền tất cả các trường điểm cuối
5. Nhập **Client ID** từ Bước 3
6. Nhập **Client Secret** từ Bước 3
7. Nếu bạn đã cấu hình yêu cầu nhóm trong Bước 6:
   - Đặt **Yêu cầu Nhóm** thành `groups`
   - Trong **Nhóm Nhân viên**, nhập tên các nhóm Okta mà thành viên nên là nhân viên (phân tách bằng dấu phẩy)
   - Trong **Nhóm Superuser**, nhập tên các nhóm Okta mà thành viên nên là superuser (phân tách bằng dấu phẩy)
8. Click **Lưu**

## Bước 8: Kích hoạt và kiểm tra

1. Chuyển đến **Cài đặt Trang > Tab An ninh**
2. Chọn **Kích hoạt SSO cho đăng nhập quản trị**
3. Click **Lưu**
4. Mở trang đăng nhập quản trị trong **cửa sổ riêng tư/incognito**
5. Bạn nên thấy nút **Đăng nhập bằng Okta**
6. Click vào nó — bạn sẽ được chuyển hướng đến trang đăng nhập của Okta
7. Đăng nhập bằng tài khoản Okta được gán với ứng dụng và email khớp với người dùng nhân viên trong Spwig
8. Bạn sẽ được chuyển hướng trở lại trang quản trị Spwig

## Các vấn đề phổ biến

| Vấn đề | Nguyên nhân | Giải pháp |
|---------|-------|----------|
| **URI chuyển hướng không được phép** | URI chuyển hướng không khớp với cấu hình ứng dụng | Kiểm tra URI chuyển hướng đăng nhập chính xác là `https://your-store.com/oidc/callback/` với dấu gạch chéo cuối |
| **Người dùng không được gán cho ứng dụng client** | Người dùng không được gán cho ứng dụng Okta | Gán người dùng hoặc nhóm của họ cho ứng dụng trong tab Gán |
| **Đăng nhập thành công tại Okta nhưng thất bại tại Spwig** | Không có người dùng khớp tại Spwig | Đảm bảo tài khoản nhân viên tồn tại tại Spwig với cùng email. Kiểm tra cài đặt Giới hạn cho Nhân viên. |
| **Yêu cầu nhóm trống** | Yêu cầu nhóm không được cấu hình trên máy chủ ủy quyền | Làm theo Bước 6 để thêm yêu cầu nhóm. Đảm bảo bạn đang thêm nó vào máy chủ ủy quyền đúng. |
| **Máy chủ ủy quyền sai** | URL khám phá sử dụng máy chủ ủy quyền khác với nơi yêu cầu nhóm được cấu hình | Kiểm tra URL khám phá khớp với máy chủ ủy quyền nơi bạn đã cấu hình yêu cầu nhóm |
| **"Client_id được cung cấp không hợp lệ"** | Client ID không khớp hoặc ứng dụng không hoạt động | Kiểm tra Client ID có chính xác và ứng dụng có trạng thái Hoạt động tại Okta |

## Một số lưu ý

- **Okta gửi tên nhóm, không phải ID** — điều này làm cho ánh xạ vai trò trở nên dễ dàng.

Nhập tên hiển thị nhóm chính xác (ví dụ: `Spwig Admins`) vào trường Nhóm Nhân viên hoặc Nhóm Superuser của Spwig.
- **Sử dụng gán nhóm để kiểm soát truy cập** — gán các nhóm Okta cụ thể cho ứng dụng Spwig thay vì cho phép tất cả người dùng.

# Cấu hình xác thực SSO

Điều này đảm bảo chỉ nhân viên được chỉ định mới có thể đăng nhập.
- **Okta client secrets không hết hạn mặc định** — tuy nhiên, bạn có thể xoay vòng chúng bất kỳ lúc nào từ tab Tổng quan của ứng dụng để tuân thủ tốt nhất về bảo mật.
- **Thử nghiệm với tài khoản không phải admin** — sử dụng người dùng Okta bình thường (không phải siêu quản trị viên) được gán với ứng dụng để kiểm tra SSO hoạt động như mong đợi.
- **MFA trong Okta** — cấu hình chính sách phiên toàn cầu của Okta hoặc chính sách xác thực để yêu cầu MFA.

Điều này sẽ áp dụng cho tất cả các lần đăng nhập SSO vào Spwig mà không cần cấu hình MFA riêng trong Spwig.