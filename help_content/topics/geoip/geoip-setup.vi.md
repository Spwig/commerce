---
title: Cài đặt GeoIP
---

GeoIP cho phép cửa hàng của bạn tự động xác định vị trí của từng khách truy cập dựa trên địa chỉ IP của họ. Điều này hỗ trợ các tính năng dựa trên vị trí trong toàn bộ cửa hàng — từ việc hiển thị tiền tệ mặc định phù hợp, đến việc chạy các quy tắc kinh doanh theo khu vực, đến việc xem các phân tích theo cấp độ quốc gia.

Cửa hàng của bạn đã được cấu hình sẵn với dịch vụ GeoIP của Spwig, vì vậy việc xác định vị trí theo khu vực sẽ hoạt động ngay lập tức. Bạn cũng có thể kết nối thêm các nhà cung cấp để tăng độ chính xác, sử dụng cơ sở dữ liệu bạn tải xuống, hoặc dựa vào tiêu đề từ CDN để có các tra cứu không độ trễ.

## Cách các nhà cung cấp hoạt động

Truy cập **Customers > GeoIP Providers** để xem các nhà cung cấp đã được cấu hình cho cửa hàng của bạn. Mỗi nhà cung cấp xử lý tra cứu IP đến vị trí bằng phương pháp khác nhau. Khi một khách truy cập đến, cửa hàng của bạn sẽ truy vấn các nhà cung cấp đang hoạt động theo thứ tự ưu tiên và sử dụng kết quả thành công đầu tiên.

Có thể có nhiều nhà cung cấp hoạt động cùng lúc — các nhà cung cấp có số ưu tiên thấp hơn sẽ được thử trước. Nếu nhà cung cấp có độ ưu tiên cao nhất thất bại hoặc không trả về dữ liệu, nhà cung cấp tiếp theo sẽ được thử tự động.

### Các loại nhà cung cấp có sẵn

| Nhà cung cấp | Mô tả |
|----------|-------------|
| **Spwig GeoIP** | Tra cứu dựa trên đám mây mặc định thông qua dịch vụ của Spwig. Không yêu cầu thiết lập. |
| **MaxMind GeoLite2** | Cơ sở dữ liệu ngoại tuyến từ MaxMind. Độ chính xác cao. Yêu cầu khóa cấp phép miễn phí. |
| **DB-IP Lite** | Cơ sở dữ liệu ngoại tuyến từ DB-IP. Tải xuống từ trang web của họ. |
| **IP2Location LITE** | Cơ sở dữ liệu ngoại tuyến từ IP2Location. Yêu cầu đăng ký miễn phí. |
| **CDN Edge Headers** | Đọc tiêu đề vị trí được chèn bởi CDN của bạn (ví dụ: Cloudflare). Không độ trễ. |
| **Browser Hints** | Sử dụng múi giờ/ngôn ngữ do trình duyệt cung cấp như một tín hiệu vị trí mềm. |
| **Custom Provider** | Một thành phần nhà cung cấp được cài đặt từ thị trường thành phần của Spwig. |

## Thêm một nhà cung cấp

### Sử dụng dịch vụ GeoIP của Spwig (mặc định)

Nhà cung cấp GeoIP của Spwig được thêm tự động khi cài đặt mới. Kiểm tra xem nó có xuất hiện trong danh sách và **Is Active** được đánh dấu. Không cần cấu hình bổ sung.

### Thêm cơ sở dữ liệu MaxMind GeoLite2

MaxMind cung cấp một cơ sở dữ liệu ngoại tuyến miễn phí cho kết quả chính xác mà không cần gửi tra cứu đến dịch vụ bên ngoài.

1. Đăng ký tài khoản miễn phí tại maxmind.com và tạo khóa cấp phép
2. Truy cập **Customers > GeoIP Providers** và nhấn **+ Add GeoIP Provider**
3. Điền vào biểu mẫu:
   - **Name**: `MaxMind GeoLite2` (hoặc bất kỳ tên mô tả nào)
   - **Provider Type**: MaxMind GeoLite2
   - **Is Active**: được đánh dấu
   - **Priority**: `1` (thấp hơn mặc định của Spwig để thử trước, hoặc cao hơn để sử dụng làm phương án dự phòng)
   - **License Key**: dán khóa cấp phép MaxMind của bạn
   - **Database URL**: URL tải xuống từ bảng điều khiển tài khoản MaxMind của bạn
4. Nhấn **Save**

Sau khi lưu, chọn nhà cung cấp trong danh sách và sử dụng hành động **Update selected provider databases** để xác minh URL cơ sở dữ liệu có thể truy cập được.

### Thêm tiêu đề CDN edge

Nếu cửa hàng của bạn nằm sau CDN chèn tiêu đề định vị (ví dụ: `CF-IPCountry` của Cloudflare), bạn có thể sử dụng các tiêu đề đó để phát hiện quốc gia tức thì, không độ trễ.

1. Truy cập **Customers > GeoIP Providers** và nhấn **+ Add GeoIP Provider**
2. Thiết lập **Provider Type** thành **CDN Edge Headers**
3. Thiết lập **Priority** thành `0` (ưu tiên cao nhất, vì tiêu đề là nguồn nhanh nhất)
4. Trong trường **Config**, chỉ định tiêu đề CDN bạn sử dụng:
   ```json
   {
     "header_name": "CF-IPCountry"
   }
   ```
5. Nhấn **Save**

## Kiểm tra một nhà cung cấp

Sau khi thêm một nhà cung cấp, bạn có thể xác minh nó đang hoạt động đúng cách:

1. Trong danh sách GeoIP Providers, chọn nhà cung cấp bằng cách đánh dấu ô kiểm của nó
2. Mở dropdown **Action** và chọn **Test selected providers**
3. Nhấn **Go**

Spwig sẽ gửi một tra cứu kiểm tra cho một địa chỉ IP đã biết (DNS công khai của Google, `8.8.8.8`) và hiển thị kết quả cho bạn. Một bài kiểm tra thành công sẽ hiển thị quốc gia được trả về và thời gian phản hồi tính bằng miligiây.

## Thiết lập độ ưu tiên nhà cung cấp

Khi có nhiều nhà cung cấp đang hoạt động, trường **Priority** (Ưu tiên) sẽ xác định nhà cung cấp nào được thử trước.

Số nhỏ hơn có nghĩa là mức độ ưu tiên cao hơn.

Ví dụ, để sử dụng tiêu đề CDN trước (nhanh nhất) và sau đó chuyển sang Spwig GeoIP:

| Provider | Priority |
|----------|----------|
| CDN Edge Headers | 0 |
| Spwig GeoIP | 10 |

Bạn có thể chỉnh sửa độ ưu tiên trực tiếp trong chế độ xem danh sách — cột **Priority** (Ưu tiên) có thể chỉnh sửa trực tiếp.

## Giám sát hiệu suất nhà cung cấp

Mỗi bản ghi nhà cung cấp theo dõi riêng các thống kê độ chính xác của nó:

- **Total Lookups** — tổng số lần tra cứu IP đã thực hiện
- **Successful Lookups** — các lần tra cứu trả về kết quả
- **Failed Lookups** — các lần tra cứu không trả về dữ liệu hoặc xảy ra lỗi
- **Average Response (ms)** — thời gian phản hồi trung bình tính bằng miligiây
- **Accuracy** — tỷ lệ phần trăm các lần tra cứu thành công

Nếu một nhà cung cấp hiển thị tỷ lệ độ chính xác thấp hoặc thời gian phản hồi cao, hãy cân nhắc điều chỉnh độ ưu tiên hoặc tắt nó để chuyển sang tùy chọn hiệu suất tốt hơn.

## Ánh xạ quốc gia

Truy cập **Customers > Country Mappings** để cấu hình mặc định theo quốc gia cho tiền tệ, ngôn ngữ, thuế và vận chuyển. Mỗi mục quốc gia kiểm soát:

- **Default Currency** — tiền tệ được chọn mặc định cho khách truy cập từ quốc gia đó
- **Default Language** — ngôn ngữ hiển thị cho khách truy cập từ quốc gia đó
- **Tax Rate** — tỷ lệ thuế mặc định được áp dụng cho quốc gia đó
- **Is EU Member** / **Requires VAT** — được sử dụng cho logic tuân thủ thuế EU
- **Shipping Zone** — liên kết quốc gia với một khu vực vận chuyển
- **Supports COD** — bật thanh toán tiền mặt tại thời điểm giao hàng cho quốc gia đó

Bạn có thể chỉnh sửa các trường **Is Active**, **Default Currency**, và **Default Language** trực tiếp trong danh sách mà không cần mở từng bản ghi.

## Một số mẹo

- Nhà cung cấp Spwig GeoIP hoạt động ngay lập tức mà không cần cấu hình — chỉ thêm các nhà cung cấp bổ sung nếu bạn cần độ chính xác cao hơn hoặc hoạt động ngoại tuyến
- Nếu bạn sử dụng Cloudflare, nhà cung cấp CDN Edge Headers là lựa chọn tốt nhất: nó không làm chậm thêm và không tính vào định额 API
- Chỉ giữ các nhà cung cấp bạn thực sự cần hoạt động — việc có nhiều nhà cung cấp hoạt động không cải thiện độ chính xác nếu nhà cung cấp đầu tiên đã thành công
- Kiểm tra thống kê độ chính xác hàng tuần và tắt bất kỳ nhà cung cấp nào có tỷ lệ thành công dưới 80%
- Ánh xạ quốc gia được sử dụng làm mặc định; khách hàng luôn có thể thay đổi tiền tệ và ngôn ngữ của họ thủ công trong cửa hàng