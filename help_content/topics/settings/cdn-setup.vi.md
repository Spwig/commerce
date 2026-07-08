---
title: Cài đặt CDN
---

Một mạng lưới phân phối nội dung (CDN) lưu trữ các bản sao của hình ảnh, bảng phong cách và các tập lệnh của cửa hàng bạn trên các máy chủ ở nhiều nơi trên thế giới. Khi một khách hàng truy cập cửa hàng của bạn, các tệp này sẽ được cung cấp từ máy chủ gần họ nhất thay vì từ máy chủ lưu trữ chính của bạn. Điều này làm giảm thời gian tải trang, đặc biệt là đối với các khách hàng ở xa nơi cửa hàng của bạn được lưu trữ.

Spwig đã tối ưu hóa việc phân phối tài nguyên tĩnh ngay từ ban đầu với việc nén trước bằng Brotli và gzip, lưu trữ tài nguyên được đánh dấu vân tay với tiêu đề không thay đổi trong 1 năm, và đàm phán nội dung đúng cách. Việc thêm CDN là tùy chọn, nhưng nó có thể cải thiện tốc độ thêm nữa cho các cửa hàng có cơ sở khách hàng quốc tế.

## Cửa hàng của bạn có cần CDN không?

Không phải cửa hàng nào cũng đều hưởng lợi như nhau từ CDN. Sử dụng các hướng dẫn sau để quyết định:

**Khuyến nghị sử dụng CDN nếu**:
- Khách hàng của bạn phân tán ở nhiều quốc gia hoặc lục địa
- Cửa hàng của bạn có nhiều hình ảnh sản phẩm hoặc các trang nặng về phương tiện
- Bạn muốn thời gian tải trang nhanh nhất có thể trên toàn cầu
- Bạn bán hàng cho các khu vực xa máy chủ lưu trữ của bạn (ví dụ: máy chủ ở châu Âu, khách hàng ở châu Á)

**Có khả năng không cần CDN nếu**:
- Khách hàng của bạn chủ yếu là địa phương hoặc ở cùng quốc gia với máy chủ của bạn
- Cửa hàng của bạn có danh mục nhỏ với ít hình ảnh
- Nhà cung cấp lưu trữ của bạn đã bao gồm CDN tích hợp

Khi còn nghi ngờ, CDN không làm giảm hiệu suất. Các dịch vụ như Cloudflare cung cấp cấp miễn phí, vì vậy không có chi phí để thử.

## Spwig hoạt động như thế nào với CDN

Spwig sẵn sàng cho CDN theo mặc định. Bạn không cần thay đổi bất kỳ mã hoặc cài đặt nào trong bảng điều khiển quản trị Spwig của bạn. Dưới đây là những gì Spwig đã làm cho bạn:

- **Tệp tĩnh được đánh dấu vân tay** -- Mỗi tệp CSS, JavaScript và hình ảnh đều có một mã băm phiên bản duy nhất trong tên tệp của nó. Điều này có nghĩa là CDN có thể an toàn lưu trữ các tệp này trong một thời gian dài mà không cần cung cấp nội dung lỗi thời.
- **Tiêu đề lưu trữ dài hạn** -- Các tài nguyên tĩnh được cung cấp với tiêu đề lưu trữ không thay đổi trong 1 năm, hướng dẫn CDN và trình duyệt lưu trữ chúng một cách tích cực.
- **Tệp được nén trước** -- Spwig nén trước các tài nguyên bằng Brotli và gzip, vì vậy CDN của bạn có thể cung cấp các tệp nhỏ hơn mà không cần xử lý bổ sung.
- **Đàm phán nội dung đúng cách** -- Spwig gửi các tiêu đề loại nội dung và mã hóa đúng cách mà CDN dựa vào để lưu trữ đúng cách.

Tất cả những gì bạn cần làm là chỉ định máy chủ tên miền (DNS) của bạn đến nhà cung cấp CDN, và mọi thứ sẽ hoạt động tự động.

## Cài đặt Cloudflare

Cloudflare là CDN phổ biến nhất và cung cấp cấp miễn phí hoạt động tốt cho hầu hết các cửa hàng. Làm theo các bước sau:

**Bước 1: Tạo tài khoản Cloudflare**
- Truy cập cloudflare.com và đăng ký tài khoản miễn phí

**Bước 2: Thêm tên miền của bạn**
- Nhấp vào **Thêm một trang web** và nhập tên miền cửa hàng của bạn
- Chọn gói **Miễn phí** (đủ cho hầu hết các cửa hàng)

**Bước 3: Cập nhật máy chủ tên miền (DNS)**
- Cloudflare sẽ hiển thị cho bạn hai máy chủ tên miền (ví dụ: `anna.ns.cloudflare.com`)
- Đăng nhập vào nhà cung cấp tên miền của bạn (nơi bạn mua tên miền)
- Thay thế máy chủ tên miền hiện tại của bạn bằng máy chủ tên miền của Cloudflare
- Thay đổi DNS có thể mất đến 24 giờ để có hiệu lực

**Bước 4: Cấu hình SSL/TLS**
- Trong bảng điều khiển Cloudflare, đi đến **SSL/TLS**
- Đặt chế độ mã hóa thành **Full (strict)**
- Điều này đảm bảo tất cả lưu lượng giữa Cloudflare và máy chủ của bạn vẫn được mã hóa

**Bước 5: Kiểm tra xem nó có hoạt động không**
- Sau khi DNS được cập nhật, hãy truy cập cửa hàng của bạn và kiểm tra tiêu đề `cf-cache-status` trong trình duyệt của bạn (xem Xác minh CDN của bạn bên dưới)

## Cài đặt AWS CloudFront

Nếu bạn đã sử dụng Amazon Web Services, CloudFront tích hợp tự nhiên với cơ sở hạ tầng của bạn:

1. Mở **CloudFront** trong bảng điều khiển AWS của bạn
2. Tạo một **Phân phối** mới với tên miền cửa hàng của bạn làm nguồn gốc
3. Đặt **Chính sách Giao thức Nguồn** thành "HTTPS Only"
4. Dưới **Hành vi Lưu trữ**, đặt **Chính sách Lưu trữ** thành "CachingOptimized" cho các tài nguyên tĩnh
5. Thêm tên miền cửa hàng của bạn làm **Tên miền Thay thế (CNAME)**
6. Gắn một chứng chỉ SSL từ AWS Certificate Manager
7. Cập nhật DNS của tên miền bạn để chỉ đến URL phân phối CloudFront



Giá CloudFront phụ thuộc vào mức sử dụng.

Đối với hầu hết các cửa hàng, chi phí là tối thiểu vì các tài sản được đánh dấu vân tay của Spwig được lưu trữ trong thời gian dài.

## Cài đặt CDN được khuyến nghị

Để đạt kết quả tốt nhất, hãy cấu hình CDN của bạn để lưu trữ nội dung phù hợp và bỏ qua phần còn lại.

**Nên lưu trữ** (tài nguyên tĩnh):
- `/static/` -- Tất cả các bảng phong cách, kịch bản, font chữ và tài nguyên chủ đề
- `/media/` -- Hình ảnh sản phẩm và tệp phương tiện đã tải lên
- Các tệp hình ảnh (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- Các tệp font chữ (`.woff`, `.woff2`)

**Không nên lưu trữ** (trang động):
- `/admin/` -- Bảng điều khiển quản trị phải luôn cung cấp nội dung mới
- `/cart/` -- Các trang giỏ hàng chứa dữ liệu phiên
- `/checkout/` -- Các trang thanh toán không bao giờ được lưu trữ vì lý do bảo mật
- `/accounts/` -- Các trang tài khoản khách hàng chứa dữ liệu riêng tư
- Bất kỳ trang nào yêu cầu đăng nhập hoặc hiển thị nội dung cá nhân

**Quy tắc lưu trữ chung**:
- **Tôn trọng tiêu đề cache của nguồn gốc** -- Spwig gửi các tiêu đề cache-control đúng cho từng loại nội dung. Cấu hình CDN của bạn để tôn trọng các tiêu đề này thay vì ghi đè lên chúng.
- **Kích hoạt nén Brotli** -- Cả Cloudflare và CloudFront đều hỗ trợ Brotli. Kích hoạt nó để tận dụng các tài nguyên đã được nén trước của Spwig.
- **Đặt TTL lưu trữ trình duyệt thành "Tôn trọng Tiêu đề Hiện có"** -- Điều này cho phép chính sách lưu trữ tích hợp của Spwig xác định hành vi.

## Xác minh CDN của bạn

Sau khi thiết lập, hãy xác nhận rằng CDN đang cung cấp nội dung của bạn đúng cách:

**Bước 1: Mở Công cụ Phát triển Trình duyệt**
- Trong Chrome hoặc Firefox, nhấn **F12** để mở công cụ phát triển
- Nhấp vào tab **Mạng**

**Bước 2: Tải trang cửa hàng của bạn**
- Truy cập trang chủ cửa hàng của bạn với công cụ phát triển mở
- Nhấp vào bất kỳ yêu cầu tệp tĩnh nào (ví dụ: một tệp `.css` hoặc `.js`)

**Bước 3: Kiểm tra Tiêu đề Phản hồi**
- **Cloudflare**: Tìm tiêu đề `cf-cache-status`. Giá trị là `HIT` có nghĩa là tệp được cung cấp từ bộ nhớ đệm CDN. `MISS` có nghĩa là nó được lấy từ máy chủ của bạn (chỉ lần yêu cầu đầu tiên).
- **CloudFront**: Tìm tiêu đề `x-cache`. Giá trị là `Hit from cloudfront` xác nhận việc giao hàng qua CDN.

**Bước 4: Kiểm tra từ vị trí khác**
- Sử dụng công cụ miễn phí như gtmetrix.com hoặc webpagetest.org để kiểm tra cửa hàng của bạn từ các vị trí địa lý khác nhau
- So sánh thời gian tải trước và sau khi thiết lập CDN

## Các vấn đề phổ biến

### Nội dung lỗi thời sau khi thay đổi chủ đề

**Vấn đề**: Sau khi cập nhật chủ đề hoặc thực hiện thay đổi thiết kế, khách hàng vẫn thấy phiên bản cũ.

**Giải pháp**: Xóa bộ nhớ đệm CDN. Trong Cloudflare, đi đến **Caching > Configuration > Purge Everything**. Trong CloudFront, tạo **Invalidation** cho `/*`. Lưu ý rằng các tài nguyên được đánh dấu vân tay của Spwig thường ngăn vấn đề này xảy ra vì các tệp được cập nhật sẽ có tên tệp mới tự động. Vấn đề này thường xảy ra nhất với các tài nguyên không được đánh dấu vân tay như các tệp tải lên tùy chỉnh.

---

### Cảnh báo nội dung hỗn hợp

**Vấn đề**: Trình duyệt của bạn hiển thị cảnh báo bảo mật về "nội dung hỗn hợp" sau khi kích hoạt CDN.

**Giải pháp**: Đảm bảo chế độ SSL của CDN được đặt thành **Full (strict)**, không phải "Flexible". Chế độ Flexible có thể khiến máy chủ của bạn nhận được yêu cầu HTTP thay vì HTTPS, dẫn đến cảnh báo nội dung hỗn hợp. Trong Cloudflare, kiểm tra **SSL/TLS > Overview** và xác nhận chế độ.

---

### Bảng điều khiển quản trị chạy chậm

**Vấn đề**: Bảng điều khiển quản trị cảm thấy chậm hơn sau khi thêm CDN.

**Giải pháp**: CDN không nên lưu trữ các trang quản trị. Tạo **Quy tắc Trang** (Cloudflare) hoặc **Hành vi Lưu trữ** (CloudFront) đặt chế độ lưu trữ thành "Bypass" cho bất kỳ URL nào khớp với `/admin/*`. Điều này đảm bảo các yêu cầu quản trị sẽ trực tiếp đến máy chủ của bạn mà không có chi phí CDN.

---

### Hình ảnh không tải được

**Vấn đề**: Hình ảnh sản phẩm hoặc tệp phương tiện trả về lỗi sau khi thiết lập CDN.

**Giải pháp**: Kiểm tra xem CDN của bạn đã được cấu hình với giao thức đúng (HTTPS) và cổng. Ngoài ra, kiểm tra xem tường lửa máy chủ của bạn có cho phép kết nối từ các dải IP của CDN không.

## Mẹo

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và thuật ngữ kỹ thuật.

- **Bắt đầu với cấp miễn phí của Cloudflare** -- Nó đáp ứng nhu cầu của hầu hết các cửa hàng và chỉ mất vài phút để thiết lập
- **Luôn sử dụng chế độ SSL đầy đủ (khắt khe)** -- Chế độ linh hoạt tạo ra lỗ hổng bảo mật và có thể làm hỏng quy trình thanh toán
- **Xóa bộ nhớ đệm CDN sau khi cập nhật chủ đề lớn** -- Mặc dù các tệp được đánh dấu bằng Spwig xử lý hầu hết các trường hợp, việc xóa bộ nhớ đệm hoàn toàn đảm bảo không có nội dung lỗi thời nào còn tồn tại
- **Không lưu cache các trang thanh toán hoặc giỏ hàng** -- Việc lưu cache các trang này có thể làm lộ thông tin của khách hàng này cho khách hàng khác
- **Kiểm tra từ vị trí của khách hàng** -- Sử dụng các công cụ miễn phí như webpagetest.org để đo lường hiệu suất thực tế từ các khu vực mà khách hàng của bạn mua sắm
- **Theo dõi phân tích CDN** -- Cả Cloudflare và CloudFront đều cung cấp bảng điều khiển hiển thị tỷ lệ truy cập cache, băng thông được tiết kiệm và lưu lượng theo quốc gia
- **Giữ TTL DNS thấp trong quá trình thiết lập** -- Đặt TTL DNS thành 300 giây (5 phút) khi chuyển đổi sang CDN, sau đó tăng lên sau khi mọi thứ đã được xác nhận hoạt động
- **Một CDN không thay thế việc lưu trữ tốt** -- Máy chủ gốc của bạn vẫn quan trọng đối với các trang động như thanh toán, giỏ hàng và quản trị.

Chọn dịch vụ lưu trữ chất lượng cùng với CDN