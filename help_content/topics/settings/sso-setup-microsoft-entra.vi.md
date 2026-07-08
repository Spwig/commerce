---
title: 'Cài đặt SSO: Microsoft Entra ID'
---

Hướng dẫn này sẽ hướng dẫn bạn cách kết nối Spwig với Microsoft Entra ID (trước đây là Azure Active Directory) để bật tính năng đăng nhập duy nhất (single sign-on) cho quản trị viên. Sau khi cấu hình, nhân viên của bạn có thể đăng nhập vào bảng điều khiển quản trị Spwig bằng tài khoản làm việc Microsoft của họ.

**Lưu ý:** Microsoft có thể cập nhật giao diện Trung tâm quản trị Entra theo thời gian. Các hướng dẫn này được viết dựa trên giao diện như của đầu năm 2026. Nếu bất kỳ bước nào khác với những gì bạn thấy, vui lòng tham khảo tài liệu chính thức của Microsoft về [đăng ký ứng dụng với nền tảng xác thực Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app).

## Yêu cầu trước

- Một tài khoản Azure có quyền truy cập vào Microsoft Entra ID
- Vai trò **Application Administrator** hoặc **Global Administrator** trong tenant Entra ID của bạn
- URL cửa hàng Spwig của bạn (ví dụ: `https://your-store.com`)
- Nhân viên phải có địa chỉ email trong Spwig khớp với tài khoản Microsoft của họ

## Bước 1: Đăng ký Ứng dụng

1. Đăng nhập vào [Trung tâm quản trị Microsoft Entra](https://entra.microsoft.com)
2. Di chuyển đến **Identity > Applications > App registrations**
3. Nhấp **New registration**
4. Cấu hình đăng ký:

| Field | Value |
|-------|-------|
| **Name** | `Spwig Admin SSO` (hoặc bất kỳ tên nào bạn ưa thích) |
| **Supported account types** | **Accounts in this organizational directory only** (Single tenant) |
| **Redirect URI** | Platform: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. Nhấp **Register**

**Quan trọng:** URI chuyển hướng phải khớp chính xác với `https://your-store.com/oidc/callback/` — bao gồm cả dấu gạch chéo ở cuối. Thay thế `your-store.com` bằng tên miền cửa hàng thực tế của bạn.

## Bước 2: Ghi lại Các ID Ứng dụng

Sau khi đăng ký, bạn sẽ thấy trang **Overview** của ứng dụng. Ghi lại hai giá trị này — bạn sẽ cần chúng sau:

| Value | Where to Find It | What It's For |
|-------|-----------------|---------------|
| **Application (client) ID** | Trang Overview, phần đầu | Nhập vào trường **Client ID** trong Spwig |
| **Directory (tenant) ID** | Trang Overview, phần đầu | Dùng để xây dựng URL Discovery |

## Bước 3: Tạo Khóa Bí mật Khách hàng

1. Trong đăng ký ứng dụng, di chuyển đến **Certificates & secrets**
2. Nhấp **New client secret**
3. Nhập mô tả (ví dụ: `Spwig SSO`) và chọn thời hạn sử dụng
4. Nhấp **Add**
5. **Sao chép giá trị ngay lập tức** — nó chỉ được hiển thị một lần. Đây là khóa bí mật khách hàng bạn sẽ nhập vào Spwig.

**Đừng sao chép ID Khóa Bí mật** — bạn cần cột **Value**, không phải cột ID.

**Đặt lời nhắc** để xoay khóa trước khi hết hạn. Khi khóa hết hạn, SSO sẽ ngừng hoạt động cho đến khi bạn tạo khóa mới và cập nhật trong Spwig.

## Bước 4: Cấu hình Quyền API

1. Di chuyển đến **API permissions**
2. Kiểm tra xem **Microsoft Graph > User.Read** (delegated) có được liệt kê hay không. Giá trị này được thêm mặc định.
3. Nếu các quyền `openid`, `email`, và `profile` không được liệt kê, nhấp **Add a permission > Microsoft Graph > Delegated permissions** và thêm chúng.
4. Nhấp **Grant admin consent for [your organization]** nếu được nhắc đến.

## Bước 5: Xây dựng URL Discovery

URL Discovery OIDC có định dạng như sau:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

Thay thế `{tenant-id}` bằng **Directory (tenant) ID** từ Bước 2.

Ví dụ: nếu ID tenant của bạn là `a1b2c3d4-e5f6-7890-abcd-ef1234567890`, URL Discovery sẽ là:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## Bước 6: Cấu hình Khai báo Nhóm (Tùy chọn)

Nếu bạn muốn Spwig tự động gán trạng thái nhân viên hoặc siêu quản trị viên dựa trên thành viên nhóm Entra ID:

1. Trong đăng ký ứng dụng, di chuyển đến **Token configuration**
2. Nhấp **Add groups claim**
3. Chọn loại nhóm cần bao gồm (thường là **Security groups**)
4. Dưới **Customize token properties by type**, đối với **ID** token, chọn **Group ID**
5. Nhấp **Add**

**Quan trọng:** Entra ID gửi **Object IDs** (UUID như `a1b2c3d4-...`), không phải tên hiển thị của nhóm.

Khi cấu hình ánh xạ vai trò trong Spwig, bạn phải sử dụng các Object ID này.

Để tìm Object ID của một nhóm:
1. Trong trung tâm quản trị Entra, đi đến **Identity > Groups > All groups**
2. Nhấp vào nhóm
3. Sao chép **Object ID** từ trang tổng quan của nhóm

### Giới hạn nhóm

Microsoft Entra ID chỉ bao gồm tối đa **200 nhóm** trong token. Nếu người dùng thuộc về nhiều hơn 200 nhóm, tuyên bố nhóm sẽ được thay thế bằng liên kết đến Microsoft Graph API. Đối với các tổ chức có nhiều nhóm, hãy xem xét tạo một nhóm bảo mật riêng dành cho truy cập Spwig và sử dụng [lọc nhóm](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) để giới hạn các nhóm được bao gồm.

## Bước 7: Cấu hình trong Spwig

1. Trong trang quản trị Spwig, điều hướng đến **Enterprise SSO > SSO Provider Configuration**
2. Đặt **Provider Name** thành `Microsoft Entra ID`
3. Dán URL Khám phá từ Bước 5 vào **OIDC Discovery URL**
4. Nhấp **Auto-Discover** — điều này tự động điền tất cả các trường điểm cuối
5. Nhập **Client ID** từ Bước 2
6. Nhập **Client Secret** (Giá trị) từ Bước 3
7. Nếu bạn đã cấu hình tuyên bố nhóm trong Bước 6:
   - Đặt **Groups Claim** thành `groups`
   - Trong **Staff Groups**, nhập các Object ID của các nhóm mà các thành viên nên là nhân viên (phân tách bằng dấu phẩy)
   - Trong **Superuser Groups**, nhập các Object ID của các nhóm mà các thành viên nên là siêu người dùng (phân tách bằng dấu phẩy)
8. Nhấp **Save**

## Bước 8: Kích hoạt và kiểm tra

1. Điều hướng đến **Site Settings > Security** tab
2. Chọn **Enable SSO for admin login**
3. Nhấp **Save**
4. Mở trang đăng nhập quản trị trong **cửa sổ riêng tư/incognito**
5. Bạn nên thấy nút **Sign in with Microsoft Entra ID**
6. Nhấp vào nó — bạn nên được chuyển hướng đến trang đăng nhập của Microsoft
7. Đăng nhập bằng tài khoản Microsoft có địa chỉ email khớp với tài khoản nhân viên trong Spwig
8. Bạn nên được chuyển hướng trở lại trang quản trị Spwig

## Các vấn đề phổ biến

| Vấn đề | Nguyên nhân | Giải pháp |
|---------|-------|----------|
| **AADSTS50011: URI chuyển hướng không khớp** | URI chuyển hướng trong Entra không khớp chính xác | Kiểm tra URI chuyển hướng là `https://your-store.com/oidc/callback/` với dấu gạch chéo cuối. Kiểm tra sự không khớp giữa HTTP và HTTPS. |
| **AADSTS700016: Ứng dụng không được tìm thấy** | Client ID sai hoặc thuê bao | Kiểm tra lại Client ID và đảm bảo URL Khám phá sử dụng ID thuê bao đúng |
| **Đăng nhập thành công tại Microsoft nhưng thất bại tại Spwig** | Không có tài khoản khớp trong Spwig | Đảm bảo tài khoản nhân viên tồn tại trong Spwig với cùng địa chỉ email như tài khoản Microsoft. Kiểm tra rằng người dùng có trạng thái nhân viên nếu tùy chọn "Restrict to Staff" được bật. |
| **Tuyên bố nhóm trống** | Tuyên bố nhóm không được cấu hình | Làm theo Bước 6 để thêm tuyên bố nhóm vào cấu hình token |
| **Tuyên bố nhóm trả về URL thay vì ID** | Người dùng thuộc về hơn 200 nhóm | Sử dụng lọc nhóm để giới hạn các nhóm trong token, hoặc chỉ định các nhóm cụ thể |
| **SSO ngừng hoạt động sau vài tháng** | Client secret đã hết hạn | Tạo client secret mới trong Entra và cập nhật nó trong Cấu hình nhà cung cấp SSO của Spwig |

## Một số mẹo

- **Sử dụng nhóm bảo mật** cho ánh xạ vai trò, thay vì nhóm Microsoft 365 hoặc danh sách phân phối.

Nhóm bảo mật được thiết kế cho kiểm soát truy cập và hoạt động đáng tin cậy nhất với các tuyên bố OIDC.
- **Khuyến khích sử dụng một thuê bao** — chọn "Tài khoản trong thư mục tổ chức này chỉ" để giới hạn SSO cho người dùng trong tổ chức của bạn.

Các cấu hình đa thuê bao yêu cầu xác thực bổ sung.
- **Thiết lập thời hạn mật khẩu dài** — chọn 24 tháng khi tạo client secret, và thiết lập lời nhắc lịch tại 22 tháng để xoay đổi nó.
- **Truy cập có điều kiện** — bạn có thể tạo các chính sách truy cập có điều kiện trong Entra ID áp dụng cụ thể cho ứng dụng đăng ký Spwig.


Ví dụ: yêu cầu xác thực đa yếu tố (MFA), chặn đăng nhập từ các vị trí không đáng tin cậy hoặc yêu cầu thiết bị tuân thủ.
- **Thử nghiệm với tài khoản không phải là quản trị viên** — tạo một tài khoản nhân viên thử nghiệm trong Spwig để kiểm tra SSO hoạt động trước khi triển khai cho toàn bộ đội ngũ của bạn.