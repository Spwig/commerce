---
title: Thỏa mãn đơn hàng sản phẩm có thể tùy chỉnh
---

Khi khách hàng thiết kế một sản phẩm và đặt hàng, thiết kế của họ sẽ được cố định và lưu trữ cùng với đơn hàng. Hướng dẫn này giải thích cách các thiết kế tùy chỉnh di chuyển qua vòng đời đơn hàng và cách truy cập các tệp đã sẵn sàng in mà bạn cần để thực hiện đơn hàng.

## Chu trình thiết kế

Thiết kế của khách hàng trải qua nhiều giai đoạn từ lúc tạo đến khi thực hiện:

### 1. Tạo thiết kế

Khách hàng sử dụng trình chỉnh sửa trực quan trên cửa hàng để tạo thiết kế của họ. Khi họ làm việc, tiến độ của họ sẽ được lưu tự động trong trình duyệt. Khách hàng đã đăng ký cũng có thể lưu thiết kế vào tài khoản của họ để chỉnh sửa sau này.

### 2. Phiên bản thiết kế

Khi khách hàng nhấp vào **Thêm vào giỏ hàng**, trạng thái thiết kế hiện tại sẽ được lưu dưới dạng **phiên bản thiết kế**. Phiên bản bao gồm:

- Trạng thái toàn bộ khung vẽ cho mọi bề mặt (vị trí các phần tử, nội dung văn bản, hình ảnh đã tải lên, hình ảnh minh họa, kiểu dáng)
- Phân tích giá cả hiển thị tất cả các khoản phí thiết kế áp dụng
- Hình thu nhỏ xem trước cho từng bề mặt

Phiên bản được liên kết với mục giỏ hàng thông qua một mã token duy nhất. Điều này đảm bảo thiết kế chính xác mà khách hàng đã tạo được giữ nguyên ngay cả khi họ tiếp tục mua sắm trước khi thanh toán.

**Hết hạn phiên bản:** Các phiên bản thiết kế sẽ tự động hết hạn sau 7 ngày nếu khách hàng không hoàn tất đơn hàng. Điều này ngăn chặn việc tích lũy các thiết kế bị bỏ lại.

### 3. Hình ảnh thiết kế cố định

Khi khách hàng hoàn tất thanh toán và đơn hàng được đặt, phiên bản thiết kế sẽ được chuyển đổi thành **hình ảnh thiết kế không thể thay đổi**. Đây là bản ghi vĩnh viễn của thiết kế:

- Hình ảnh thiết kế không thể được khách hàng sửa đổi sau khi mua
- Nó chứa cùng dữ liệu thiết kế chính xác như phiên bản
- Nó được liên kết vĩnh viễn với mục đơn hàng cụ thể

Tính không thể thay đổi này rất quan trọng — nó đảm bảo rằng những gì khách hàng đã đặt hàng là chính xác những gì bạn sản xuất và giao hàng, không có khả năng thay đổi sau khi thanh toán.

### 4. Tạo tệp thực hiện

Sau khi đơn hàng được đặt, hệ thống sẽ tự động tạo ra **các tệp thực hiện độ phân giải cao** cho từng bề mặt của thiết kế. Đây là các hình ảnh tổng hợp kết hợp tất cả các yếu tố thiết kế (văn bản, hình ảnh, hình ảnh minh họa) thành một tệp in sẵn duy nhất ở độ DPI được cấu hình cho từng bề mặt.

Việc tạo tệp diễn ra bất đồng bộ trong nền. Với hầu hết các thiết kế, việc tạo tệp hoàn tất trong vài giây. Trạng thái **Đã tạo** của hình ảnh thiết kế cho biết các tệp thực hiện có sẵn hay không.

## Truy cập dữ liệu thiết kế trong đơn hàng

### Trang chi tiết đơn hàng

Khi bạn xem một đơn hàng chứa sản phẩm có thể tùy chỉnh trong bảng điều khiển quản trị:

1. Di chuyển đến **Đơn hàng > Tất cả đơn hàng**
2. Mở đơn hàng chứa sản phẩm đã tùy chỉnh
3. Mục đơn hàng cho sản phẩm có thể tùy chỉnh hiển thị thông tin thiết kế, bao gồm hình xem trước từng bề mặt và liên kết đến hình ảnh thiết kế cố định

### Danh sách hình ảnh thiết kế

Bạn cũng có thể duyệt tất cả các hình ảnh thiết kế trực tiếp:

1. Di chuyển đến **Sản phẩm có thể tùy chỉnh > Hình ảnh thiết kế cố định**
2. Danh sách hiển thị tất cả các hình ảnh thiết kế liên kết với mục đơn hàng
3. Nhấp vào một hình ảnh thiết kế để xem toàn bộ dữ liệu thiết kế, hình ảnh đã tạo và tệp thực hiện

Mỗi hình ảnh thiết kế hiển thị:

| Trường | Mô tả |
|-------|-------------|
| **Mục đơn hàng** | Liên kết đến mục đơn hàng liên quan |
| **Dữ liệu thiết kế** | Trạng thái khung vẽ đầy đủ (JSON) |
| **Hình ảnh đã tạo** | Hình xem trước thu nhỏ theo từng bề mặt |
| **Tệp thực hiện** | Các tệp tổng hợp độ phân giải cao để in |
| **Đã tạo** | Cho biết việc tạo tệp có hoàn tất hay không |
| **Thời gian hoàn tất tạo** | Thời điểm các tệp được tạo |

## Tải xuống tệp thực hiện

Các tệp thực hiện là những tệp bạn gửi cho nhà cung cấp in hoặc sử dụng trong quy trình sản xuất của bạn.

**Đối với đơn hàng áo phông tùy chỉnh:**
- Tải xuống tệp bề mặt **Trước** (ví dụ: tệp PNG tổng hợp 300 DPI)
- Tải xuống tệp bề mặt **Sau**
- Tải xuống tệp bề mặt **Tay áo** (nếu đã thiết kế)
- Gửi tất cả các tệp cho nhà in màn hình hoặc máy in DTG (in trực tiếp lên quần áo)

**Đối với đơn hàng poster tùy chỉnh:**
- Tải xuống tệp **Front** duy nhất ở độ phân giải in
- Tệp bao gồm khu vực bleed nếu bleed đã được cấu hình cho bề mặt
- Gửi đến nhà in poster/card của bạn

Mỗi tệp là một hình ảnh tổng hợp duy nhất chứa tất cả các yếu tố thiết kế được hợp nhất, được hiển thị ở DPI bạn đã cấu hình cho bề mặt đó.

## Thiết kế đã lưu

Khách hàng đã đăng ký có thể lưu thiết kế của họ vào tài khoản để chỉnh sửa sau này. Là một nhà bán hàng, bạn có thể xem các thiết kế đã lưu này trong danh sách chỉ đọc:

1. Di chuyển đến **Sản phẩm có thể tùy chỉnh > Thiết kế đã lưu**
2. Danh sách hiển thị tất cả thiết kế do khách hàng lưu với tên khách hàng, sản phẩm, tên thiết kế và ngày

Thiết kế đã lưu là:
- **Thuộc khách hàng** — Chúng thuộc về tài khoản của khách hàng
- **Chỉ đọc cho nhà bán hàng** — Bạn có thể xem nhưng không thể chỉnh sửa chúng
- **Tách biệt khỏi đơn hàng** — Một thiết kế đã lưu chỉ trở thành đơn hàng khi khách hàng thêm nó vào giỏ hàng và thanh toán
- **Có thể tái sử dụng** — Khách hàng có thể tải lên thiết kế đã lưu, chỉnh sửa nó và đặt hàng nhiều lần

## Quy trình xử lý đơn hàng

### Quy trình tiêu chuẩn

1. **Nhận đơn hàng** — Đơn hàng xuất hiện trong danh sách đơn hàng của bạn với các mục được tùy chỉnh
2. **Kiểm tra việc hiển thị** — Kiểm tra xem ảnh chụp thiết kế có hiển thị **Đã hiển thị: Có** hay không. Nếu việc hiển thị chưa hoàn tất, hãy đợi một lúc và làm tươi lại
3. **Tải xuống tệp** — Tải xuống tệp xử lý cho mỗi bề mặt được thiết kế
4. **Kiểm tra chất lượng** — Mở các tệp và kiểm tra thiết kế có đáp ứng tiêu chuẩn in của bạn hay không (kiểm tra DPI, vị trí các yếu tố và khả năng đọc chữ)
5. **Gửi đến sản xuất** — Gửi các tệp đến nhà cung cấp in hoặc nhóm sản xuất của bạn
6. **Giao hàng và hoàn tất** — Sau khi sản xuất, giao sản phẩm và đánh dấu đơn hàng là đã hoàn tất

### Ví dụ xử lý áo phông

1. Đơn hàng nhận được: "Áo phông nhóm tùy chỉnh" với thiết kế ở mặt trước và mặt sau
2. Mở đơn hàng → xem ảnh chụp thiết kế
3. Tải xuống `front.png` (300 DPI, 300x400mm) và `back.png` (300 DPI, 300x400mm)
4. Gửi cả hai tệp đến máy in DTG của bạn cùng với màu áo và kích cỡ từ lựa chọn biến thể trong đơn hàng
5. Sau khi in và kiểm tra chất lượng, giao hàng cho khách hàng

### Ví dụ xử lý poster

1. Đơn hàng nhận được: "Poster A4 tùy chỉnh" với một bề mặt được thiết kế
2. Mở đơn hàng → xem ảnh chụp thiết kế
3. Tải xuống `front.png` (300 DPI, 210x297mm với 3mm bleed)
4. Gửi đến dịch vụ in poster của bạn
5. Sau khi in và cắt, giao hàng cho khách hàng

## Khắc phục sự cố

**Vấn đề:** Ảnh chụp thiết kế hiển thị "Đã hiển thị: Không" và việc hiển thị chưa hoàn tất

- **Nguyên nhân:** Nhiệm vụ hiển thị nền có thể đã thất bại hoặc vẫn đang xử lý
- **Giải pháp:** Chờ một vài phút. Nếu việc hiển thị không hoàn tất, hãy kiểm tra nhật ký nhiệm vụ nền. Bạn cũng có thể xem dữ liệu thiết kế trực tiếp trong ảnh chụp để xác nhận thiết kế của khách hàng vẫn được bảo tồn

**Vấn đề:** Tệp xử lý xuất hiện có chất lượng kém hơn mong đợi

- **Nguyên nhân:** Khách hàng có thể đã tải lên hình ảnh độ phân giải thấp
- **Giải pháp:** Kiểm tra cài đặt DPI của bề mặt. Nếu đã cấu hình cảnh báo DPI tối thiểu, khách hàng sẽ được cảnh báo trong quá trình thiết kế. Đối với sản phẩm trong tương lai, hãy cân nhắc tăng yêu cầu DPI tối thiểu

**Vấn đề:** Khách hàng yêu cầu thay đổi thiết kế sau khi đặt hàng

- **Giải pháp:** Ảnh chụp thiết kế là bất biến theo thiết kế. Nếu khách hàng cần thay đổi, họ nên đặt một đơn hàng mới với thiết kế đã cập nhật. Nếu bạn đồng ý tạo ngoại lệ, khách hàng có thể sử dụng thiết kế đã lưu của họ (nếu họ đã lưu) làm điểm bắt đầu cho đơn hàng mới

## Một số mẹo

- Luôn kiểm tra xem việc hiển thị đã hoàn tất trước khi bắt đầu sản xuất.

Kiểm tra trường **Đã hiển thị** trên ảnh chụp thiết kế.
- Luôn giữ cài đặt DPI phù hợp với phương pháp in của bạn.

DPI cao hơn tạo ra chất lượng tốt hơn nhưng kích thước tệp lớn hơn. 300 DPI là tiêu chuẩn cho hầu hết các sản phẩm in chuyên nghiệp.
- Khuyến khích khách hàng lưu thiết kế của họ trước khi đặt hàng.

Bảo tồn tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

Nếu có sự cố trong quá trình sản xuất và đơn hàng cần được làm lại, thiết kế đã lưu sẽ giúp việc đặt lại đơn hàng trở nên dễ dàng hơn.
- Hãy xây dựng một khoảng thời gian dự phòng trong lịch trình sản xuất của bạn cho các sản phẩm có thể tùy chỉnh.

Khác với các sản phẩm tiêu chuẩn, mỗi mặt hàng đều yêu cầu xử lý tệp riêng lẻ.
- Nếu bạn xử lý số lượng lớn đơn hàng tùy chỉnh, hãy cân nhắc tự động hóa bước tải xuống tệp bằng cách tích hợp với API của nhà cung cấp in ấn của bạn.