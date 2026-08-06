---
title: API Tokens
---

API tokens là các khóa an toàn cho phép các dịch vụ bên ngoài và tích hợp giao tiếp với cửa hàng của bạn. Khi một dịch vụ bên thứ ba hoặc công cụ cần truy cập dữ liệu cửa hàng của bạn hoặc kích hoạt các hành động, nó sẽ gửi một API token cùng với mỗi yêu cầu để cửa hàng của bạn có thể xác minh yêu cầu đó được ủy quyền. Bạn tạo và quản lý tất cả các token, bao gồm cả các phần cụ thể của cửa hàng mà chúng có thể truy cập, từ phần API Tokens trong bảng điều khiển quản trị của bạn.

## Khi bạn cần một API token

Bạn thường sẽ cần tạo một API token khi:

- Kết nối một dịch vụ bên ngoài hoặc công cụ tự động hóa cần đọc từ hoặc ghi vào cửa hàng của bạn
- Thiết lập một trình nhận webhook cần xác thực các cuộc gọi đến
- Cấu hình Hệ thống Hỗ trợ Spwig cho cài đặt của bạn
- Xây dựng một tích hợp tùy chỉnh sử dụng API của Spwig
- Đồng bộ dữ liệu giữa cửa hàng Spwig của bạn và hệ thống khác

Mỗi tích hợp nên có riêng một token để bạn có thể thu hồi quyền truy cập cho một dịch vụ mà không ảnh hưởng đến các dịch vụ khác.

## Loại token

Khi tạo một token, bạn chọn một loại để mô tả mục đích của nó. Loại này dành cho tham khảo của bạn và giúp bạn theo dõi được mỗi token làm gì.

| Loại | Mục đích |
|------|---------|
| **Hệ thống Hỗ trợ** | Được sử dụng bởi hệ thống tài liệu hỗ trợ Spwig |
| **Tích hợp bên ngoài** | Các dịch vụ bên thứ ba, công cụ tự động hóa (ví dụ: Zapier), hoặc công cụ đồng bộ dữ liệu |
| **Webhook** | Xác thực cho trình nhận webhook hoặc điểm cuối |
| **Tùy chỉnh** | Bất kỳ mục đích nào không phù hợp với các danh mục trên |
| **Đồng bộ Cài đặt** | Đồng bộ giữa các cài đặt Spwig hoặc dịch vụ Spwig bên ngoài |

## API scopes: kiểm soát những phần mà token có thể truy cập

Mỗi token cũng có một phần **API Scopes** quyết định chính xác những phần nào trong cửa hàng của bạn nó được phép gọi. Thay vì một token có quyền truy cập toàn diện vào mọi thứ, bạn cấp quyền truy cập từng khu vực một lần — và ở cấp độ mà tích hợp thực sự cần.

**Một token không chọn bất kỳ scope nào sẽ không thể truy cập bất kỳ API nào**, ngay cả khi nó vẫn hoạt động và hợp lệ. Đây là cài đặt mặc định cho một token mới, vì vậy tích hợp sẽ không hoạt động cho đến khi bạn cố ý cấp quyền truy cập cho nó.

Đối với mỗi scope, bạn chọn một trong ba cấp độ truy cập:

| Cấp độ truy cập | Điều mà nó cho phép |
|------------------|---------------------|
| **Không có quyền truy cập** | Token không thể gọi bất kỳ điểm cuối nào trong khu vực này |
| **Đọc** | Token có thể truy xuất dữ liệu từ khu vực này, nhưng không thể thay đổi bất cứ thứ gì |
| **Đọc & Ghi** | Token có thể truy xuất dữ liệu và cũng có thể tạo, cập nhật hoặc xóa nó |

Các scope được nhóm lại để phù hợp với các khu vực trong bảng điều khiển quản trị của bạn:

| Nhóm | Scope | Đọc & Ghi có sẵn? | Cấp quyền truy cập cho |
|-------|-------|:---:|-------------------|
| Phân tích | **Phân tích Doanh số** | Chỉ đọc | Bảng điều khiển doanh số, chỉ số KPI, phân tích sản phẩm/khách hàng/danh mục, so sánh và xuất dữ liệu |
| Phân tích | **Phân tích Web** | Chỉ đọc | Phân tích người truy cập và lưu lượng: tổng quan, xu hướng, các trang hàng đầu, địa lý và nguồn truy cập |
| Danh mục | **Sản phẩm** | Có | Sản phẩm, biến thể, hình ảnh, điều chỉnh tồn kho và gán thuộc tính |
| Danh mục | **Danh mục** | Có | Danh mục sản phẩm, bao gồm hình ảnh và banner |
| Danh mục | **Thương hiệu** | Có | Thương hiệu sản phẩm |
| Danh mục | **Thuộc tính** | Có | Định nghĩa thuộc tính sản phẩm |
| Danh mục | **Tồn kho** | Có | Bảng điều khiển tồn kho, tốc độ tồn kho, các chuyển động, đề xuất đặt lại và cài đặt tồn kho |
| Đơn hàng | **Đơn hàng** | Có | Đơn hàng, ghi chú đơn hàng, cập nhật trạng thái/theo dõi, hủy bỏ, hoàn tiền và tài liệu đơn hàng |
| Khách hàng | **Thông điệp Khách hàng** | Có | Thông điệp khách hàng từ các biểu mẫu liên hệ và ghi chú đơn hàng, bao gồm cập nhật trạng thái và phản hồi |
| Cửa hàng & Cài đặt | **Cài đặt Cửa hàng** | Có | Cài đặt cửa hàng, ngôn ngữ có sẵn và thương hiệu (tên, màu sắc, logo) |
| Người dùng & Truy cập | **Nhân viên & Vai trò** | Có | Tài khoản nhân viên, lời mời, vai trò và danh mục quyền |

Hai scope **Phân tích** luôn chỉ đọc — dữ liệu báo cáo không có khái niệm "ghi", vì vậy trình chọn chỉ cung cấp **Không có quyền truy cập** hoặc **Đọc** cho chúng.

[![The API Scopes picker, with an access note above the Analytics and Catalog scope groups](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)](https://example.com)

Dưới phần chọn phạm vi, một phần **"This token can access:"** chỉ đọc sẽ liệt kê tất cả phạm vi bạn đã cấp và cấp độ của nó, để bạn có thể kiểm tra lại quyền truy cập của token một cách nhanh chóng mà không cần giải mã phần chọn.

![The "This token can access" summary listing each granted scope and its Read or Read & Write level](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)

### Whose permissions a token actually uses

Các phạm vi của token mô tả *giới hạn* những gì nó có thể làm — nhưng token cũng kế thừa quyền truy cập thực tế của nhân viên đã tạo ra nó:

- Token không bao giờ có thể hành động với quyền **superuser**, ngay cả khi nhân viên tạo token là một superuser.
- **Read & Write** trên một phạm vi chỉ hoạt động nếu vai trò của nhân viên tạo token cũng cho phép truy cập ghi vào khu vực đó. Nếu vai trò của họ chỉ có thể xem, ví dụ như Sản phẩm, một token họ tạo với "Sản phẩm: Read & Write" vẫn chỉ có thể đọc — vai trò đóng vai trò như một cổng thứ hai trên phạm vi.
- Nếu nhân viên tạo token bị xóa hoặc tài khoản của họ bị vô hiệu hóa, token sẽ lập tức mất quyền truy cập API, bất kể phạm vi của nó — không còn có người dùng được phép để nó hành động.

Điều này có nghĩa là cách an toàn nhất để giới hạn phạm vi của token là tạo nó khi đang đăng nhập dưới tư cách của một nhân viên có vai trò đã khớp với quyền truy cập mà bạn muốn token có.

## Creating an API token

1. Navigate to **Settings > API Tokens**
2. Click **+ Add API Token**
3. Enter a **Name** that clearly describes what the token is for (e.g., `Zapier Product Sync` or `Help System API`)
4. Select the appropriate **Token Type**
5. Optionally add a **Description** with more detail about the integration
6. In **API Scopes**, choose **No access**, **Read**, or **Read & Write** for each area the integration needs — leave every other scope at **No access**
7. Configure the **Active** status, **Expiry Date**, and **Allowed IPs** as needed (see below)
8. Click **Save**

After saving, the full token value is displayed on the detail page. **Copy it immediately** — the token is masked in the list view for security and cannot be retrieved in full again after you leave this page.

![API Token Detail](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Token value security

Spwig chỉ hiển thị giá trị đầy đủ của token một lần: ngay sau khi bạn lưu token mới. Sau đó, danh sách hiển thị chỉ phiên bản được che giấu (ví dụ: `spw_••••••••••••••••••••3f8a`).

Nếu bạn mất giá trị token, bạn không thể khôi phục nó. Bạn sẽ cần xóa token cũ và tạo một token mới, sau đó cập nhật tích hợp đang sử dụng nó.

**Không bao giờ chia sẻ giá trị token qua email, tin nhắn chat hoặc mã nguồn.** Xử lý chúng như mật khẩu.

## Setting an expiry date

Trường **Expires At** đặt ngày và giờ sau đó token sẽ ngừng hoạt động tự động. Để trống nếu token không nên hết hạn.

Các ngày hết hạn hữu ích cho:

- Các tích hợp tạm thời với ngày kết thúc cố định
- Các token được cấp cho bên thứ ba mà bạn muốn tự động xóa quyền truy cập
- Thêm một lớp bảo mật bổ sung cho các tích hợp có quyền cao

Khi token hết hạn, các yêu cầu sử dụng nó sẽ bị từ chối. Bạn có thể mở rộng quyền truy cập bằng cách cập nhật ngày **Expires At** hoặc tạo một token thay thế.

## Restricting to specific IP addresses

Trường **Allowed IPs** chấp nhận danh sách địa chỉ IP. Khi danh sách không trống, token chỉ hoạt động khi yêu cầu đến từ một trong những địa chỉ đó.

Ví dụ, nếu công cụ phân tích của bạn chạy trên máy chủ tại `203.0.113.42`, việc thêm địa chỉ IP này có nghĩa là token không thể bị lạm dụng từ bất kỳ vị trí nào khác, ngay cả khi nó bị rò rỉ.

Để trống **Allowed IPs** để cho phép yêu cầu đến từ bất kỳ địa chỉ IP nào.

**Hạn sử dụng và hạn chế IP được kiểm tra độc lập với phạm vi (scopes).** Một token đã hết hạn hoặc không nằm trong danh sách IP được phép sẽ bị từ chối trước khi phạm vi của nó được xem xét, và một token có phạm vi rộng cũng sẽ bị từ chối ngay khi hết hạn hoặc được gọi từ một IP không được liệt kê.

## Gọi API bằng token

Các tích hợp xác thực với API quản trị của Spwig bằng cách gửi token trong tiêu đề `Authorization`:

```
Authorization: Bearer <your-token-value>
```

Tất cả các điểm cuối (endpoints) của API quản trị đều nằm dưới `/api/admin/...`. Nhà phát triển xây dựng tích hợp của bạn sẽ quyết định các điểm cuối cần gọi — nhiệm vụ của bạn là người bán hàng là đảm bảo token có **Phạm vi API** bao phủ các điểm cuối đó. Nếu yêu cầu bị từ chối với lỗi quyền truy cập, điều đầu tiên cần kiểm tra là token có được cấp phạm vi đúng hay không.

### Ví dụ: đọc dữ liệu phân tích lưu lượng truy cập web

Spwig cung cấp điểm cuối `GET /api/admin/analytics/traffic/` trả về phân tích lưu lượng truy cập và người truy cập cho cửa hàng của bạn — tổng quan về lượt truy cập và người truy cập duy nhất, xu hướng theo thời gian, các trang hàng đầu, vị trí địa lý của người truy cập và nguồn truy cập. Để cho phép công cụ báo cáo hoặc bảng điều khiển đọc dữ liệu này:

1. Tạo một token (hoặc chỉnh sửa token hiện có) cho tích hợp đó
2. Trong **Phạm vi API**, đặt **Phân tích Web** thành **Đọc (Read)**
3. Lưu token và cung cấp nó cho tích hợp

Vì **Phân tích Web** là phạm vi chỉ đọc, không có tùy chọn **Đọc & Viết (Read & Write)** để chọn — tích hợp chỉ có thể truy xuất dữ liệu phân tích, không bao giờ thay đổi cấu hình cửa hàng của bạn.

## Theo dõi việc sử dụng token

Danh sách token hiển thị:

- **Số lần sử dụng** — tổng số lần token đã được sử dụng
- **Lần sử dụng cuối cùng** — thời điểm token được sử dụng lần cuối để thực hiện yêu cầu

Những trường này giúp bạn xác định các token không được sử dụng (ứng viên cho việc thu hồi) và phát hiện hoạt động bất thường. Một sự gia tăng đột biến trong số lần sử dụng có thể cho thấy token đang được sử dụng bởi một bên khác ngoài tích hợp được chỉ định.

## Thu hồi token

Để ngay lập tức dừng token hoạt động mà không xóa nó:

1. Nhấp vào tên token
2. Bỏ chọn **Hoạt động (Active)**
3. Lưu

Token vẫn tồn tại trong danh sách của bạn để tham khảo nhưng sẽ bị từ chối trong mọi yêu cầu tiếp theo. Điều này hữu ích khi bạn cần tạm dừng tích hợp trong khi điều tra một vấn đề.

Để xóa token vĩnh viễn:

1. Chọn hộp kiểm của nó trong danh sách
2. Chọn **Xóa các token API đã chọn** từ menu hành động
3. Xác nhận xóa

Sau khi xóa, token không thể phục hồi. Nếu tích hợp vẫn cần truy cập, hãy tạo token mới và cập nhật cấu hình tích hợp.

## Ví dụ: thiết lập tích hợp Zapier

**Tình huống:** Bạn muốn kết nối cửa hàng của mình với Zapier để tự động hóa thông báo đơn hàng.

| Trường | Giá trị |
|-------|-------|
| Tên | `Zapier Order Automation` |
| Loại token | Tích hợp bên ngoài |
| Mô tả | Được Zapier sử dụng để đọc đơn hàng mới và kích hoạt thông báo |
| Phạm vi API | **Đơn hàng (Orders)**: Đọc & Viết |
| Hoạt động | Có |
| Hết hạn vào | *(trống)* |
| IP được phép | *(trống — Zapier sử dụng IP động)* |

Chỉ phạm vi **Đơn hàng (Orders)** được cấp, vì vậy ngay cả khi token này từng bị rò rỉ, nó cũng không thể ảnh hưởng đến sản phẩm, tin nhắn khách hàng, tài khoản nhân viên hoặc bất kỳ phần nào khác của cửa hàng của bạn. Sau khi lưu, sao chép giá trị token đầy đủ và dán vào cài đặt tích hợp Spwig của Zapier.

## Một số lưu ý

Giữ nguyên toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- Gán cho mỗi token một tên rõ ràng và cụ thể - `Shopify Sync v2` hữu ích hơn nhiều so với `Token 3` khi bạn đang khắc phục sự cố sau nhiều tháng
- Tạo một token cho mỗi tích hợp - nếu một tích hợp bị xâm nhập, bạn có thể thu hồi chỉ token đó mà không làm gián đoạn các token khác
- **Chỉ cấp các phạm vi mà tích hợp thực sự cần** - một công cụ báo cáo chỉ cần quyền đọc trên Phân tích Doanh số hoặc Phân tích Web, chứ không cần quyền đọc và ghi trên Sản phẩm hoặc Nhân viên & Vai trò
- Kiểm tra phần tóm tắt **"This token can access:"** trên biểu mẫu thay đổi trước khi trao token cho bên thứ ba - đây là cách nhanh nhất để xác nhận bạn không đã cấp quyền vượt quá mong muốn
- Nhớ rằng quyền ghi cũng phụ thuộc vào vai trò của nhân viên tạo token - nếu một phạm vi hiển thị là Đọc & Ghi nhưng việc ghi vẫn thất bại, hãy kiểm tra quyền của người dùng đó nữa
- Đặt ngày hết hạn cho các token được sử dụng trong các dự án một lần hoặc tích hợp tạm thời - điều này làm giảm nguy cơ các token bị quên vẫn còn hoạt động vô thời hạn
- Xem lại danh sách token của bạn mỗi vài tháng và ngừng sử dụng bất kỳ token nào có ngày **Last Used** bất thường cũ, vì những token này có thể thuộc về các tích hợp không còn đang chạy
- Nếu bạn nghi ngờ một token đã bị tiết lộ, hãy ngừng sử dụng nó ngay lập tức, tạo một token thay thế, và cập nhật tích hợp bị ảnh hưởng trước khi bật lại quyền truy cập