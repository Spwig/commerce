---
title: Cài đặt SSL
---

SSL (Secure Sockets Layer) mã hóa kết nối giữa trình duyệt của khách hàng và cửa hàng của bạn. Khi SSL được kích hoạt, URL của cửa hàng bạn sẽ bắt đầu bằng `https://` và trình duyệt sẽ hiển thị biểu tượng khóa. SSL là yếu tố cần thiết để chấp nhận thanh toán, bảo vệ dữ liệu khách hàng và xếp hạng tốt trên công cụ tìm kiếm.

Spwig hỗ trợ nhiều chế độ SSL để phù hợp với các cấu hình lưu trữ khác nhau. Hướng dẫn này giải thích từng chế độ và giúp bạn chọn chế độ phù hợp nhất.

## Chọn chế độ SSL

| Chế độ | Phù hợp nhất | Chi phí chứng chỉ | Cập nhật |
|--------|--------------|-------------------|---------|
| **Let's Encrypt** | Hầu hết các cửa hàng | Miễn phí | Tự động |
| **Cloudflare Origin CA** | Cửa hàng sử dụng proxy Cloudflare | Miễn phí | Thủ công (tối đa 15 năm) |
| **Chứng chỉ tùy chỉnh** | Cửa hàng có chứng chỉ đã mua | Thay đổi | Thủ công |
| **Quản lý bên ngoài** | Máy cân bằng tải, Cloudflare Flexible | Không áp dụng | Không áp dụng |
| **Tự ký** | Phát triển và kiểm thử | Miễn phí | Thủ công |
| **Không (HTTP)** | Phát triển cục bộ | Không áp dụng | Không áp dụng |

Nếu bạn không chắc nên chọn chế độ nào, **Let's Encrypt** là lựa chọn tốt nhất cho hầu hết các cửa hàng. Nó miễn phí, tự động và được tin cậy bởi tất cả trình duyệt.

## Let's Encrypt

Let's Encrypt cung cấp chứng chỉ SSL miễn phí, được tin cậy và tự động gia hạn mỗi 60-90 ngày. Đây là lựa chọn được khuyến nghị cho hầu hết các nhà bán hàng.

**Yêu cầu:**
- Tên miền của bạn phải trỏ đến máy chủ của bạn (ký ghi A trong DNS)
- Cổng 80 phải có thể truy cập từ Internet (để xác minh chứng chỉ)
- Địa chỉ email để nhận thông báo khi chứng chỉ hết hạn

**Các bước thiết lập:**
1. Truy cập **Settings > Site Settings** và mở tab **Domain & SSL**
2. Nhập tên miền của bạn
3. Chọn **Let's Encrypt**
4. Nhập địa chỉ email quản trị của bạn
5. Nhấp **Apply Configuration**

Spwig sẽ tự động xử lý mọi thứ còn lại: xác minh tên miền, lấy chứng chỉ, cấu hình NGINX và thiết lập gia hạn tự động.

## Cloudflare Origin CA

Chứng chỉ Cloudflare Origin CA mã hóa kết nối giữa các máy chủ biên Cloudflare và cửa hàng của bạn. Các chứng chỉ này miễn phí và có thể kéo dài đến 15 năm, nhưng chúng **chỉ được tin cậy bởi Cloudflare** – trình duyệt kết nối trực tiếp đến máy chủ của bạn sẽ hiển thị cảnh báo chứng chỉ.

Chế độ này lý tưởng nếu bạn sử dụng Cloudflare làm proxy (mây cam được bật) cho tên miền của bạn. Cloudflare sẽ hiển thị chứng chỉ được tin cậy của riêng mình cho khách truy cập, và chứng chỉ Origin CA bảo mật kết nối giữa Cloudflare và máy chủ của bạn.

**Yêu cầu:**
- Tài khoản Cloudflare với tên miền của bạn đã được thêm
- Chứng chỉ Origin CA và khóa riêng tư được tạo từ bảng điều khiển Cloudflare
- Chế độ SSL/TLS của Cloudflare được đặt thành **Full (Strict)**

**Tạo chứng chỉ Origin CA:**
1. Đăng nhập vào bảng điều khiển Cloudflare
2. Chọn tên miền của bạn
3. Truy cập **SSL/TLS > Origin Server**
4. Nhấp **Create Certificate**
5. Chọn RSA hoặc ECC (RSA có tính tương thích cao nhất)
6. Thêm tên miền của bạn (ví dụ: `example.com` và `*.example.com`)
7. Chọn thời hạn (15 năm được khuyến nghị)
8. Nhấp **Create** và sao chép cả chứng chỉ và khóa riêng tư

**Thiết lập trong Spwig:**
1. Truy cập **Settings > Site Settings** và mở tab **Domain & SSL**
2. Nhập tên miền của bạn
3. Chọn **Cloudflare Origin CA**
4. Dán chứng chỉ vào trường **Certificate (PEM)**
5. Dán khóa riêng tư vào trường **Private Key (PEM)**
6. Nhấp **Apply Configuration**

**Sau khi thiết lập:**
- Trong Cloudflare, đặt chế độ SSL/TLS thành **Full (Strict)**
- Kích hoạt proxy Cloudflare (mây cam) cho bản ghi DNS của tên miền
- Cửa hàng của bạn sẽ có thể truy cập qua HTTPS với chứng chỉ được tin cậy của Cloudflare

## Chứng chỉ tùy chỉnh

Sử dụng chế độ này nếu bạn đã mua chứng chỉ SSL từ một nhà cung cấp chứng chỉ (CA) như DigiCert, Sectigo hoặc GoDaddy, hoặc nếu nhà cung cấp lưu trữ của bạn đã cấp cho bạn một chứng chỉ.

**Các bước thiết lập:**
1.

Truy cập **Settings > Site Settings** và mở tab **Domain & SSL**
2.

Nhập tên miền của bạn
3.

Chọn **Custom Certificate**
4.

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

Dán chuỗi chứng chỉ của bạn (bao gồm các chứng chỉ trung gian) vào trường **Certificate (PEM)**
5.

Dán khóa riêng tư của bạn vào trường **Private Key (PEM)**
6.

Nhấn **Apply Configuration**

Chứng chỉ của bạn phải bao gồm toàn bộ chuỗi: chứng chỉ miền của bạn, sau đó là bất kỳ chứng chỉ trung gian nào. Khóa riêng tư phải ở định dạng PEM (bắt đầu với `-----BEGIN PRIVATE KEY-----` hoặc `-----BEGIN RSA PRIVATE KEY-----`).

## Managed Externally

Chọn chế độ này khi SSL được chấm dứt bởi một dịch vụ bên ngoài trước khi lưu lượng truy cập đến máy chủ của bạn. Trong thiết lập này, máy chủ của bạn chỉ nhận lưu lượng HTTP thuần túy - không có chứng chỉ nào được cài đặt trên máy chủ.

**Các tình huống phổ biến:**
- **Cloudflare Flexible SSL** -- Cloudflare mã hóa lưu lượng từ trình duyệt đến Cloudflare, nhưng gửi HTTP đến máy chủ của bạn
- **Bộ cân bằng tải đám mây** -- AWS ALB, Google Cloud Load Balancer hoặc DigitalOcean Load Balancer chấm dứt SSL và chuyển tiếp HTTP
- **Proxy ngược** -- Một máy chủ khác phía trước Spwig xử lý SSL

**Các bước thiết lập:**
1. Đi đến **Settings > Site Settings** và mở tab **Domain & SSL**
2. Nhập tên miền của bạn
3. Chọn **Managed Externally**
4. Nhấn **Apply Configuration**

Spwig sẽ cấu hình NGINX để chỉ phục vụ HTTP và tin tưởng tiêu đề `X-Forwarded-Proto` từ proxy của bạn để xác định chính xác các truy cập HTTPS.

## Self-Signed Certificate

Các chứng chỉ tự ký mã hóa kết nối nhưng không được trình duyệt tin cậy. Người truy cập sẽ thấy cảnh báo bảo mật mà họ phải bỏ qua thủ công. Chế độ này chỉ phù hợp cho các máy chủ phát triển và kiểm tra nội bộ.

**Các bước thiết lập:**
1. Đi đến **Settings > Site Settings** và mở tab **Domain & SSL**
2. Nhập tên miền của bạn
3. Chọn **Self-Signed**
4. Nhấn **Apply Configuration**

Spwig sẽ tạo tự động một chứng chỉ tự ký. Đừng sử dụng chế độ này cho cửa hàng sản xuất.

## Troubleshooting

**Chứng chỉ không hoạt động sau khi cấu hình:**
- Kiểm tra bản ghi A của tên miền có trỏ đến địa chỉ IP của máy chủ của bạn không
- Đảm bảo các cổng 80 và 443 đã được mở trong tường lửa của bạn
- Chờ vài phút để các thay đổi DNS được lan truyền

**Let's Encrypt không thể cấp chứng chỉ:**
- Kiểm tra xem tên miền của bạn có giải quyết đến địa chỉ IP của máy chủ này không
- Đảm bảo cổng 80 không bị chặn bởi tường lửa
- Nếu bạn đang sử dụng Cloudflare, tạm thời đặt DNS thành "DNS only" (mây xám) trong quá trình cấp chứng chỉ

**Cloudflare hiển thị "Error 526" (Chứng chỉ SSL không hợp lệ):**
- Đảm bảo bạn đã chọn chế độ **Cloudflare Origin CA** (không phải Managed Externally)
- Kiểm tra xem chế độ SSL/TLS của Cloudflare có được đặt thành **Full (Strict)** không
- Kiểm tra xem chứng chỉ Origin CA có hết hạn chưa

**Trình duyệt hiển thị "Not Secure" mặc dù đã có SSL:**
- Một số trang có thể tải hình ảnh hoặc kịch bản qua HTTP (nội dung hỗn hợp). Kiểm tra bảng điều khiển nhà phát triển của trình duyệt để xem cảnh báo nội dung hỗn hợp.
- Đảm bảo URL trang web của bạn trong Cài đặt sử dụng `https://`