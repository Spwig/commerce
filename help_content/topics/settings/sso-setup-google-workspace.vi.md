---
title: 'SSO Setup: Google Workspace'
---

Cấu hình SSO: Google Workspace

Hướng dẫn này sẽ hướng dẫn bạn cách kết nối Spwig với Google Workspace để bật tính năng đăng nhập duy nhất (single sign-on) cho quản trị viên. Sau khi cấu hình, nhân viên của bạn có thể đăng nhập vào bảng điều khiển quản trị Spwig bằng tài khoản Google Workspace của họ.

**Lưu ý:** Google có thể cập nhật giao diện Cloud Console theo thời gian. Các hướng dẫn này được viết dựa trên giao diện như của đầu năm 2026. Nếu các bước khác với những gì bạn thấy, vui lòng tham khảo tài liệu chính thức của Google về [cấu hình OAuth 2.0](https://support.google.com/cloud/answer/6158849).

## Yêu cầu trước

- Một bản đăng ký Google Workspace (Google Workspace Business, Enterprise hoặc Education)
- Quyền quản trị trên [Google Cloud Console](https://console.cloud.google.com)
- URL cửa hàng Spwig của bạn (ví dụ: `https://your-store.com`)
- Nhân viên phải có địa chỉ email trong Spwig khớp với tài khoản Google Workspace của họ

## Bước 1: Tạo hoặc chọn một dự án Google Cloud

1. Truy cập [Google Cloud Console](https://console.cloud.google.com)
2. Nhấp vào trình chọn dự án ở thanh trên cùng
3. Nhấp **New Project** (hoặc chọn một dự án hiện có nếu bạn muốn)
4. Nhập tên dự án (ví dụ: `Spwig SSO`)
5. Chọn tổ chức của bạn
6. Nhấp **Create**

## Bước 2: Cấu hình màn hình đồng ý OAuth

1. Trong Cloud Console, điều hướng đến **APIs & Services > OAuth consent screen**
2. Chọn **Internal** làm loại người dùng — điều này giới hạn đăng nhập cho người dùng trong tổ chức Google Workspace của bạn
3. Nhấp **Create**
4. Điền các trường bắt buộc:

| Trường | Giá trị |
|-------|-------|
| **Tên ứng dụng** | `Spwig Admin` (hoặc tên cửa hàng của bạn) |
| **Email hỗ trợ người dùng** | Địa chỉ email quản trị của bạn |
| **Tài khoản được phép** | `your-store.com` (tên miền cửa hàng của bạn, không có `https://`) |
| **Email liên hệ nhà phát triển** | Địa chỉ email quản trị của bạn |

5. Nhấp **Save and Continue**
6. Trên trang **Scopes**, nhấp **Add or Remove Scopes** và thêm:
   - `openid`
   - `email`
   - `profile`
7. Nhấp **Save and Continue**
8. Xem lại tóm tắt và nhấp **Back to Dashboard**

## Bước 3: Tạo thông tin xác thực OAuth

1. Điều hướng đến **APIs & Services > Credentials**
2. Nhấp **Create Credentials > OAuth client ID**
3. Cấu hình ứng dụng:

| Trường | Giá trị |
|-------|-------|
| **Loại ứng dụng** | Web application |
| **Tên** | `Spwig SSO` |
| **URL chuyển hướng được phép** | `https://your-store.com/oidc/callback/` |

4. Nhấp **Create**
5. Một hộp thoại hiển thị **Client ID** và **Client Secret** của bạn — sao chép cả hai giá trị. Bạn cũng có thể tải chúng dưới dạng JSON để lưu trữ an toàn.

**Quan trọng:** URL chuyển hướng phải khớp chính xác với `https://your-store.com/oidc/callback/` — bao gồm cả dấu gạch chéo cuối và phương thức `https://`. Thay thế `your-store.com` bằng tên miền cửa hàng thực tế của bạn.

## Bước 4: Lấy URL khám phá (Discovery URL)

Google sử dụng một URL khám phá duy nhất và tiêu chuẩn cho tất cả các tổ chức Workspace:

```
https://accounts.google.com/.well-known/openid-configuration
```

URL này giống nhau cho mọi tổ chức Google Workspace — bạn không cần tùy chỉnh nó với một tổ chức hoặc tên miền.

## Bước 5: Cấu hình trong Spwig

1. Trong bảng điều khiển quản trị Spwig, điều hướng đến **Enterprise SSO > SSO Provider Configuration**
2. Đặt **Provider Name** thành `Google Workspace`
3. Nhập URL khám phá: `https://accounts.google.com/.well-known/openid-configuration`
4. Nhấp **Auto-Discover** — điều này tự động điền tất cả các trường điểm cuối
5. Nhập **Client ID** từ Bước 3
6. Nhập **Client Secret** từ Bước 3
7. Nhấp **Save**

### Ánh xạ yêu cầu (Claims Mapping)

Google sử dụng tên yêu cầu OIDC tiêu chuẩn, do đó cấu hình mặc định của Spwig hoạt động ngay lập tức:

| Cài đặt Spwig | Yêu cầu Google | Giá trị mặc định |
|---------------|-------------|---------------|
| Yêu cầu email | `email` | `email` |
| Yêu cầu tên đầu | `given_name` | `given_name` |
| Yêu cầu tên cuối | `family_name` | `family_name` |

Không cần thay đổi ánh xạ yêu cầu.

## Bước 6: Bật và kiểm tra

1.

Điều hướng đến **Site Settings > Security** tab
2.

Tích chọn **Enable SSO for admin login**
3.

Nhấp **Save**
4.



Mở trang đăng nhập admin trong **cửa sổ riêng tư/incognito**
5.

Bạn nên thấy nút **Đăng nhập bằng Google Workspace**
6.

Nhấn vào nó — bạn sẽ được chuyển hướng đến trang đăng nhập của Google
7.

Đăng nhập bằng tài khoản Google Workspace có địa chỉ email khớp với một tài khoản nhân viên trong Spwig
8.

Bạn sẽ được chuyển hướng trở lại trang quản trị Spwig

## Ánh xạ vai trò dựa trên nhóm

Khác với Microsoft Entra ID hoặc Okta, Google không bao gồm thành viên nhóm trong token OIDC tiêu chuẩn theo mặc định. Việc triển khai các tuyên bố nhóm với Google yêu cầu API Thư mục Google Workspace và cấu hình bổ sung ngoài OIDC cơ bản.

Đối với hầu hết các triển khai Google Workspace, chúng tôi khuyên bạn nên quản lý trạng thái nhân viên và siêu quản trị viên trực tiếp trong Spwig thay vì ánh xạ vai trò tự động:

1. Tạo tài khoản nhân viên trong Spwig với quyền truy cập phù hợp
2. Sử dụng hệ thống Vai trò Nhân viên của Spwig để kiểm soát cấp độ truy cập
3. Nhân viên đăng nhập qua SSO, và Spwig sử dụng quyền truy cập hiện có của họ

Nếu bạn cần ánh xạ vai trò dựa trên nhóm tự động, vui lòng tham khảo [Tài liệu API Thư mục Admin SDK của Google Workspace](https://developers.google.com/admin-sdk/directory) để cấu hình các tuyên bố tùy chỉnh.

## Các vấn đề phổ biến

| Vấn đề | Nguyên nhân | Giải pháp |
|---------|-------|----------|
| **Lỗi 400: redirect_uri_mismatch** | URI chuyển hướng trong Google Cloud không khớp chính xác | Kiểm tra URI chuyển hướng là `https://your-store.com/oidc/callback/` với dấu gạch chéo cuối. Kiểm tra HTTP so với HTTPS. |
| **Lỗi 403: access_denied** | Người dùng không thuộc tổ chức Google Workspace | Với loại người dùng "Internal", chỉ những người dùng trong tổ chức của bạn mới có thể đăng nhập. Kiểm tra tài khoản người dùng có thuộc miền Workspace của bạn không. |
| **Màn hình đồng ý OAuth hiển thị "Ứng dụng này chưa được xác minh"** | Bình thường cho các ứng dụng Internal | Cảnh báo này là bình thường cho các ứng dụng Internal và không ảnh hưởng đến tính năng. Người dùng trong tổ chức của bạn vẫn có thể đăng nhập. |
| **Đăng nhập thành công tại Google nhưng thất bại tại Spwig** | Không có tài khoản nhân viên khớp tại Spwig | Đảm bảo tài khoản nhân viên tồn tại tại Spwig với cùng địa chỉ email như tài khoản Google Workspace. Kiểm tra xem tùy chọn "Hạn chế chỉ cho Nhân viên" đã được cấu hình đúng chưa. |
| **"Truy cập bị chặn: Yêu cầu của ứng dụng này không hợp lệ"** | Các phạm vi không được cấu hình đúng | Kiểm tra xem các phạm vi `openid`, `email`, và `profile` đã được thêm vào màn hình đồng ý OAuth. |

## Một số mẹo

- **Sử dụng loại người dùng "Internal"** — điều này giới hạn đăng nhập cho tổ chức Google Workspace của bạn và không yêu cầu quy trình xác minh ứng dụng của Google.
- **Bí mật khách hàng Google không hết hạn** — khác với Microsoft Entra ID, các bí mật khách hàng OAuth của Google không có ngày hết hạn. Tuy nhiên, bạn có thể xoay chúng bất kỳ lúc nào từ trang Tùy chọn.
- **Một dự án cho nhiều ứng dụng** — bạn có thể tạo nhiều ID khách hàng OAuth trong cùng một dự án Google Cloud nếu bạn có nhiều cài đặt Spwig.
- **Kiểm tra bằng tài khoản không phải quản trị viên** — tạo tài khoản nhân viên kiểm tra trong Spwig và sử dụng người dùng Google Workspace bình thường (không phải siêu quản trị viên) để xác minh SSO hoạt động như mong đợi.