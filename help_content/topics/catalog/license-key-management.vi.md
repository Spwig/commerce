---
title: Quản lý Khóa License
---

Quản lý khóa license cho phép bạn kiểm soát cách các khóa license phần mềm được tạo, lưu trữ và gửi đến khách hàng khi họ mua sản phẩm số. Spwig hỗ trợ tạo khóa nội bộ, nhóm khóa đã tải trước và tích hợp với các dịch vụ quản lý license bên ngoài.

## Tổng quan

Có ba cách để quản lý khóa license trong Spwig:

| Phương pháp | Phù hợp nhất với |
|--------|---------|
| **Mẫu khóa license** | Tự động tạo các khóa duy nhất theo định dạng tùy chỉnh tại thời điểm mua hàng |
| **Nhóm khóa** | Tạo sẵn một lô khóa trước để phân phối theo lô |
| **Cung cấp bên ngoài** | Giao việc tạo và quản lý khóa cho một dịch vụ bên thứ ba như Keygen.sh |

Các phương pháp này có thể được kết hợp — ví dụ, một nhóm khóa có thể sử dụng mẫu tùy chỉnh để xác định định dạng khóa và có thể đồng bộ hóa các khóa đã tạo với một nhà cung cấp bên ngoài.

## Mẫu khóa license

Một mẫu khóa license xác định *định dạng* của các khóa được tạo. Các mẫu sử dụng một mẫu có các chỗ trống mà Spwig điền vào khi tạo khóa.

### Tạo mẫu

1. Di chuyển đến **Catalog > License Key Templates**
2. Nhấp **+ Add License Key Template**
3. Nhập **Tên** (ví dụ: `Standard App License`)
4. Cấu hình **Mẫu** bằng các chỗ trống (xem bên dưới)
5. Thiết lập **Tiền tố** và **Sau tố** nếu cần (ví dụ, tiền tố `MYAPP` sẽ thêm `MYAPP-` vào mỗi khóa)
6. Chọn **Ký tự phân tách** (mặc định: `-`)
7. Thiết lập **Bộ ký tự** — các ký tự được sử dụng cho các đoạn ngẫu nhiên. Mặc định loại bỏ các ký tự dễ nhầm lẫn như `0` và `O`, `1` và `I`
8. Thiết lập **Chiều dài tối thiểu/tối đa** để xác minh
9. Nhấp **Lưu**

### Các chỗ trống trong mẫu

| Chỗ trống | Mô tả | Ví dụ đầu ra |
|-------------|-------------|---------------|
| `{RANDOM:N}` | N ký tự ngẫu nhiên từ bộ ký tự | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | Mã kiểm tra N chữ số để xác minh | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | Giá trị tiền tố của mẫu | `MYAPP` |
| `{SUFFIX}` | Giá trị sau tố của mẫu | `PRO` |
| `{ORDER_ID}` | Số đơn hàng | `10045` |
| `{PRODUCT_SKU}` | Mã SKU của sản phẩm | `SOFTPRO` |
| `{DATE:FORMAT}` | Ngày được định dạng | `{DATE:YYMMDD}` → `260318` |

**Ví dụ mẫu**: `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

Điều này tạo ra các khóa như: `MYAPP-K7JXQ-M3TPR-9BWKN-47`

### Xem trước khóa

Sau khi lưu mẫu, hành động **Generate Sample Key** sẽ có sẵn trong danh sách mẫu. Sử dụng điều này để kiểm tra mẫu của bạn tạo ra các khóa theo định dạng mong muốn trước khi gán mẫu cho sản phẩm.

## Nhóm khóa

Một nhóm khóa là một lô khóa được tạo sẵn cho một sản phẩm. Các nhóm rất hữu ích khi:
- Bạn cần khóa cho bao bì vật lý (hộp bán lẻ, thẻ in)
- Bạn làm việc với các nhà phân phối cần lô khóa
- Bạn muốn tạo khóa trước thay vì theo yêu cầu

### Tạo nhóm khóa

1. Di chuyển đến **Catalog > License Pools**
2. Nhấp **+ Add License Pool**
3. Điền chi tiết nhóm:

| Trường | Mô tả |
|-------|-------------|
| **Tên** | Tên mô tả (ví dụ: `Retail Pack Q1 2026`) |
| **Sản phẩm** | Sản phẩm mà các khóa này dành cho |
| **Mẫu khóa** | Mẫu định dạng khóa (mặc định là mẫu của sản phẩm) |
| **Tổng số khóa** | Số lượng khóa cần tạo |
| **Loại khóa** | Vĩnh viễn, đăng ký hoặc dùng thử |
| **Số lần kích hoạt tối đa** | Số lượng thiết bị mà mỗi khóa có thể kích hoạt |
| **Hết hạn sau (ngày)** | Số ngày trước khi giấy phép hết hạn sau lần kích hoạt đầu tiên (trống để không hết hạn) |
| **Hết hạn nhóm tại** | Ngày sau đó các khóa chưa sử dụng trong nhóm này trở nên không hợp lệ |
| **Đồng bộ với nhà cung cấp** | Tùy chọn đồng bộ khóa đã tạo với nhà cung cấp giấy phép bên ngoài |

4. Nhấp **Lưu** — Spwig bắt đầu tạo khóa trong nền

### Trạng thái nhóm

| Trạng thái | Ý nghĩa |
|--------|---------|
| **Đang tạo** | Các khóa đang được tạo ở phía sau |
| **Sẵn sàng** | Tất cả khóa đã được tạo và sẵn sàng để phân phối |
| **Hết hạn** | Tất cả khóa đã được gán cho các đơn hàng |
| **Hết hạn** | Ngày hết hạn của nhóm khóa đã qua |

### Theo dõi nhóm khóa

Danh sách nhóm khóa hiển thị số lượng khóa đã phân phối so với tổng số khóa đã tạo. Mở một nhóm khóa để xem danh sách đầy đủ các khóa và trạng thái cụ thể của từng khóa.

## Các nhà cung cấp giấy phép bên ngoài

Các nhà cung cấp bên ngoài là các dịch vụ quản lý giấy phép bên thứ ba xử lý việc tạo khóa và theo dõi việc kích hoạt. Khi khách hàng hoàn tất mua hàng, Spwig sẽ giao tiếp với nhà cung cấp để tạo và đăng ký khóa.

### Các nhà cung cấp được hỗ trợ

| Nhà cung cấp | Loại |
|----------|------|
| **Máy chủ giấy phép tích hợp của Spwig** | Tích hợp sẵn — không cần tài khoản bên ngoài |
| **Keygen.sh** | API quản lý giấy phép dựa trên đám mây |
| **LicenseSpring** | Quản lý giấy phép doanh nghiệp |
| **Cryptlex** | Quản lý giấy phép với hỗ trợ ngoại tuyến |
| **API tùy chỉnh** | Bất kỳ hệ thống giấy phép dựa trên REST nào |

### Kết nối với nhà cung cấp

1. Di chuyển đến **Catalog > License Providers**
2. Nhấp **+ Add License Provider**
3. Điền thông tin nhà cung cấp:

| Trường | Mô tả |
|-------|-------------|
| **Tên** | Nhãn cho kết nối này (ví dụ: `Keygen Production`) |
| **Loại nhà cung cấp** | Chọn từ các nhà cung cấp được hỗ trợ |
| **Điểm cuối API** | URL cơ sở API của nhà cung cấp |
| **Khóa API** | Khóa xác thực cho nhà cung cấp |
| **Bí mật API** | Nếu nhà cung cấp yêu cầu |

4. Cấu hình hành vi đồng bộ:
   - **Đồng bộ khi đặt hàng** — Đồng bộ tự động khi khách hàng hoàn tất mua hàng
   - **Đồng bộ khi kích hoạt** — Báo cáo việc kích hoạt thiết bị cho nhà cung cấp
   - **Đồng bộ khi hủy kích hoạt** — Báo cáo việc hủy kích hoạt (hữu ích cho việc chuyển nhượng giấy phép và hoàn tiền)
   - **Đồng bộ hai chiều** — Cho phép nhà cung cấp cập nhật các bản ghi của Spwig thông qua webhook

5. Nhấp **Lưu**, sau đó nhấp **Test Connection** để xác minh các thông tin xác thực hoạt động

### Trạng thái kết nối

Mỗi nhà cung cấp hiển thị một trong ba trạng thái kết nối:

| Trạng thái | Ý nghĩa |
|--------|---------|
| **Chưa kiểm tra** | Kết nối chưa được xác minh |
| **Kết nối thành công** | Kiểm tra lần cuối thành công |
| **Lỗi** | Kiểm tra kết nối thất bại — kiểm tra thông báo lỗi |

### Đồng bộ giấy phép hiện có

Để đẩy các khóa giấy phép hiện có đến nhà cung cấp (cho thiết lập ban đầu hoặc sau khi đồng bộ thất bại), hãy sử dụng hành động **Sync Now** từ danh sách nhà cung cấp.

## Theo dõi hoạt động đồng bộ

Di chuyển đến **Catalog > External License Syncs** để xem nhật ký đồng bộ. Mỗi bản ghi hiển thị:
- Khóa giấy phép đã được đồng bộ
- Nhà cung cấp đã gửi đến
- Hướng (Spwig → Nhà cung cấp hoặc Nhà cung cấp → Spwig)
- Trạng thái (Đang chờ, Thành công, Thất bại)
- Chi tiết lỗi cho các đồng bộ thất bại

Các đồng bộ thất bại sẽ được thử lại tự động. Bạn cũng có thể buộc thử lại bằng cách chỉnh sửa bản ghi và xóa lỗi.

## Một số mẹo

- Sử dụng bộ ký tự mặc định (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`) để tránh các ký tự dễ nhầm lẫn mà khách hàng thường đọc sai — nó loại bỏ `0`, `O`, `1`, và `I`.
- Thêm đoạn `{CHECKSUM}` vào mẫu mẫu của bạn để khách hàng và nhóm hỗ trợ của bạn có thể nhanh chóng phát hiện các khóa được nhập sai.
- Đối với các sản phẩm có khối lượng lớn, hãy sử dụng nhóm thay vì tạo theo yêu cầu để đảm bảo các khóa được giao ngay lập tức tại thời điểm thanh toán.
- Thiết lập **Pool Expires At** cho các lô khóa theo mùa hoặc có thời hạn để các khóa cũ không được sử dụng tự động bị vô hiệu hóa.
- Luôn kiểm tra kết nối nhà cung cấp sau khi thiết lập và sau bất kỳ thay đổi thông tin xác thực nào — một kết nối bị hỏng có nghĩa là khách hàng không nhận được khóa của họ.
- Nếu sử dụng đồng bộ hai chiều, hãy cấu hình URL webhook của nhà cung cấp để chỉ đến điểm cuối webhook giấy phép của cửa hàng của bạn.