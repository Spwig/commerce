---
title: Kho hàng và Kho lưu trữ
---

Hệ thống kho cho phép bạn quản lý hàng tồn kho ở nhiều địa điểm khác nhau, thiết lập thứ tự thực hiện đơn hàng, và theo dõi mức hàng tồn kho theo thời gian thực. Truy cập **Sản phẩm > Kho** trong thanh điều hướng quản trị để quản lý các địa điểm kho của bạn.

![Danh sách kho](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Kho

### Danh sách kho

Trang kho hiển thị tất cả các địa điểm hàng hóa của bạn dưới dạng thẻ với:

- **Tên và mã** — Mã định danh kho (ví dụ: "Kho chính", mã "CHINH-WH")
- **Vùng bán hàng** — Phân vùng địa lý
- **Biểu tượng trạng thái** — Đang hoạt động/dừng hoạt động, cửa hàng bán lẻ
- **Thống kê** — Số sản phẩm tồn kho, thứ tự thực hiện đơn hàng, tỷ lệ hàng tồn kho dự phòng
- **Vị trí** — Thành phố và quốc gia
- **Cập nhật lần cuối** — Thời điểm mức hàng tồn kho cuối cùng được thay đổi

### Tạo kho

1. Nhấn **+ Thêm Kho**
2. Điền thông tin **Cơ bản**:
   - **Tên** — Nhãn mô tả (ví dụ: "Kho Đông Hoa Kỳ")
   - **Mã** — Mã định danh ngắn duy nhất (ví dụ: "ĐÔNG-HOA") — phải duy nhất trên toàn bộ các kho
   - **Vùng bán hàng** — Gán cho một khu vực địa lý để định tuyến thực hiện đơn hàng
   - **Đang hoạt động** — Kích hoạt để bao gồm trong quá trình thực hiện đơn hàng
3. Điền phần **Địa chỉ** với địa chỉ đầy đủ của kho
4. Cấu hình **Cài đặt Thực hiện đơn hàng**:
   - **Thứ tự thực hiện** — Số lớn hơn = thứ tự cao hơn cho việc thực hiện đơn hàng
   - **Tỷ lệ hàng tồn kho dự phòng** — Phần trăm hàng tồn kho được giữ lại làm hàng dự phòng (0–100)
   - **Vị trí giao hàng** — Liên kết tùy chọn đến địa điểm lấy hàng nếu kho này hỗ trợ khách hàng lấy hàng
5. Cấu hình **Hiển thị cho Người dùng** (tùy chọn):
   - **Tên hiển thị** — Nhãn cho người dùng (ví dụ: "Giao hàng từ Úc"). Để trống để sử dụng tên kho.
   - **Hiển thị trên Trang chủ** — Hiển thị nguồn hàng của kho này cho người dùng trên trang sản phẩm
6. Cấu hình **Cửa hàng POS / Bán lẻ** (tùy chọn):
   - **Cửa hàng bán lẻ** — Kiểm tra nếu kho này đồng thời là cửa hàng vật lý có máy POS
   - **Tên hiển thị POS** — Tên ngắn được hiển thị trong giao diện POS
   - **Nhóm Cửa hàng** — Gán vào nhóm cửa hàng POS để kế thừa cài đặt
7. Thêm **Thông tin Liên hệ** nếu cần (tên, email, số điện thoại)
8. Nhấn **Lưu**

### Thứ tự Thực hiện

Khi có đơn hàng đến, hệ thống chọn kho tốt nhất dựa trên:

1. **Giá trị thứ tự** — Kho có thứ tự cao hơn được ưa tiên
2. **Sự sẵn có của hàng tồn kho** — Phải có đủ hàng tồn kho
3. **Phù hợp khu vực** — Kho ở khu vực khách hàng được ưa tiên

Ví dụ, nếu bạn có kho Hoa Kỳ (thứ tự 100) và kho châu Âu (thứ tự 60), đơn hàng Hoa Kỳ sẽ được thực hiện từ kho Hoa Kỳ trước.

### Tỷ lệ Hàng tồn kho Dự phòng

Tỷ lệ hàng tồn kho dự phòng giữ lại một phần hàng tồn kho không được bán trực tuyến. Điều này hữu ích cho:

- Các cửa hàng bán lẻ vật lý cần hàng trưng bày
- Hàng tồn kho an toàn để tránh bán quá mức
- Hàng tồn kho được giữ riêng cho đơn hàng bán buôn

Một tỷ lệ 10% trên 100 đơn vị có nghĩa là chỉ có 90 đơn vị có sẵn cho đơn hàng trực tuyến.

## Mặt hàng Hàng tồn kho

Các mặt hàng hàng tồn kho đại diện cho hàng tồn kho thực tế của một sản phẩm cụ thể tại một kho cụ thể.

### Xem Mức hàng tồn kho

1. Nhấn vào **biểu tượng hàng tồn kho** trên thẻ kho để xem các mặt hàng hàng tồn kho của nó
2. Hoặc truy cập tab **Hàng tồn kho** của sản phẩm để xem hàng tồn kho trên tất cả các kho

Mỗi mặt hàng hàng tồn kho hiển thị:

- **Tên sản phẩm** và biến thể (nếu có)
- **Số lượng hiện có** — Tổng hàng tồn kho vật lý
- **Đã phân bổ** — Số lượng được giữ cho các đơn hàng đang chờ
- **Còn lại** — Số lượng hiện có trừ đi đã phân bổ (điều mà có thể bán được)

### Thêm hàng tồn kho

1. Truy cập **Sản phẩm > Mặt hàng Hàng tồn kho** và nhấn **+ Thêm Mặt hàng Hàng tồn kho**, hoặc
2. Mở biểu mẫu chỉnh sửa sản phẩm và sử dụng phần **Mặt hàng Hàng tồn kho** ở cuối
3. Chọn **sản phẩm** và **kho** (và tùy chọn **biến thể** cho sản phẩm có biến thể)
4. Nhập **số lượng hiện có**
5. Thiết lập **ngưỡng hàng tồn kho thấp** — ngưỡng này cho từng mặt hàng kích hoạt thông báo hàng tồn kho thấp
6. Lưu

### Các chuyển động Hàng tồn kho

Mọi thay đổi về hàng tồn kho đều được ghi nhận dưới dạng **chuyển động hàng tồn kho**:

| Loại Di Chuyển | Mô Tả |
|--------------|-------------|
| **Nhập Kho** | Hàng hóa mới được nhận từ nhà cung cấp |
| **Bán Hàng** | Số lượng hàng hóa bị trừ cho đơn hàng đã hoàn tất |
| **Trả Lại** | Hàng hóa được trả lại từ khách hàng |
| **Điều Chỉnh** | Sửa đổi thủ công (sai lệch số lượng kiểm kê) |
| **Chuyển Kho** | Được di chuyển giữa các kho hàng |
| **Duy Trì** | Được giữ tạm thời cho giỏ hàng đang hoạt động |
| **Hư Hại** | Được ghi nhận là hư hỏng hoặc mất mát |
| **Đếm Lại** | Được điều chỉnh để khớp với số lượng kiểm kê thực tế |

Các chuyển động hàng hóa cung cấp một bản ghi kiểm toán đầy đủ về các thay đổi trong hàng tồn kho. Ngoài hành động **Điều Chỉnh Mức Hàng Tồn Kho**, Spwig còn cung cấp các hành động khối trên danh sách Hàng Hóa để chuyển kho, ghi nhận hàng hóa hư hại và đếm lại số lượng hàng hóa trên nhiều mặt hàng cùng lúc — xem [Hành Động Kiểm Kê Đa Dạng](/help/stock-bulk-actions).

## Theo Dõi Hàng Hóa Trên Sản Phẩm

### Kích Hoạt Theo Dõi Hàng Hóa

Trên phần **Hàng Hóa** của sản phẩm:

1. Chuyển đổi **Theo Dõi Hàng Hóa** để kích hoạt quản lý số lượng hàng hóa cho sản phẩm này
2. Thiết lập **Ngưỡng Hàng Hóa Dưới Mức** — kích hoạt thông báo bảng điều khiển khi số lượng hàng hóa tại bất kỳ kho nào đều dưới mức này
3. Cấu hình **Cho phép Đặt Hàng Khi Hết Hàng** nếu bạn muốn chấp nhận đơn hàng khi hết hàng
4. Thiết lập tùy chọn **Hành Động Hết Hàng** để ghi đè hành vi chung của trang web hoặc danh mục cho sản phẩm cụ thể này

Sau khi kích hoạt theo dõi, quản lý số lượng hàng hóa thực tế bằng phần **Hàng Hóa** ngay dưới dạng biểu mẫu sản phẩm, hoặc thông qua **Sản Phẩm > Hàng Hóa**.

### Hàng Hóa Nhiều Kho

Khi theo dõi hàng hóa được kích hoạt, tab Hàng Hóa hiển thị số lượng hàng hóa tại tất cả các kho trong bảng tổng quan:

- Tổng số lượng hàng hóa có sẵn tại tất cả địa điểm
- Phân bổ theo kho
- Số lượng có sẵn sau khi giữ chỗ và phân bổ

## Cảnh Báo Hàng Hóa Dưới Mức

Hệ thống tự động theo dõi mức hàng hóa và cảnh báo cho bạn khi:
- Một sản phẩm giảm dưới **ngưỡng hàng hóa dưới mức**
- Một sản phẩm đạt **mức hàng hóa bằng không**

Cảnh báo hàng hóa dưới mức xuất hiện tại:
- **Bảng Điều Khiển Cửa Hàng** trong phần Các Hành Động Cần Thiết
- Danh sách sản phẩm với biểu tượng trực quan

## Lời Khuyên

- Bắt đầu với một kho duy nhất và thêm nhiều kho hơn khi doanh nghiệp phát triển.
- Thiết lập thứ tự thực hiện dựa trên tốc độ và chi phí giao hàng đến từng khu vực.
- Sử dụng các biện pháp dự phòng hàng hóa cho các cửa hàng bán lẻ để đảm bảo có hàng tồn kho trên sàn.
- Đánh giá các chuyển động hàng hóa định kỳ để phát hiện sự hao hụt hoặc sai lệch.
- Thiết lập ngưỡng hàng hóa dưới mức dựa trên thời gian đặt hàng của bạn — nếu thời gian restock là 2 tuần, hãy thiết lập ngưỡng để bao gồm 2 tuần doanh số.
- Kích hoạt theo dõi hàng hóa trước khi ra mắt để tránh bán quá số lượng.