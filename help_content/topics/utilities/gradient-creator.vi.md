---
title: Tạo Gradient
---

Tạo Gradient cho phép bạn xây dựng các chuyển tiếp màu sắc mượt mà cho nền của các phần tử. Nó được truy cập thông qua tab Gradient trong trình chỉnh sửa nền và hiển thị dưới dạng bảng điều khiển nổi lên với thanh gradient trực quan, các điều khiển điểm màu và tùy chọn mặc định.

![Tạo Gradient](/static/core/admin/img/help/gradient-creator/gradient-creator.webp)

## Truy cập Tạo Gradient

1. Chọn một phần tử trong Trình tạo Trang hoặc Trình tạo Header/Footer
2. Mở tab **Style** trong bảng thuộc tính
3. Nhấn vào phần **Background** để mở Trình chỉnh sửa nền
4. Chuyển sang tab **Gradient**
5. Bảng điều khiển Tạo Gradient mở ra với bản xem trước trực tiếp và các điều khiển chỉnh sửa

## Bản xem trước trực tiếp

Phần trên cùng của bảng điều khiển hiển thị so sánh song song:

| Hộp | Mục đích |
|-----|---------|
| **Hiện tại** | Gradient hiện tại (hoặc trong suốt nếu chưa được thiết lập) |
| **Mới** | Cập nhật theo thời gian thực khi bạn thực hiện các thay đổi |

Một mũi tên giữa hai hộp chỉ ra hướng thay đổi.

## Loại Gradient

Ba loại gradient có sẵn, có thể chọn thông qua các tab ở phía trên của trình chỉnh sửa:

| Loại | Mô tả | Điều khiển |
|------|-------------|----------|
| **Linear** | Chuyển tiếp màu dọc theo một đường thẳng | Thanh trượt góc (0-360 độ) với các nút hướng mặc định (lên, chéo, phải, xuống, v.v.) |
| **Radial** | Chuyển tiếp màu lan tỏa từ một điểm trung tâm | Trình chọn hình dạng (hình tròn hoặc elip) và trình chọn vị trí (trung tâm, trên, dưới, góc) |
| **Conic** | Chuyển tiếp màu xoay quanh một điểm trung tâm | Thanh trượt góc bắt đầu (0-360 độ) và trình chọn vị trí |

### Điều khiển hướng Linear

Đối với gradient tuyến tính, bạn có thể thiết lập góc theo ba cách:
- **Thanh trượt góc** — kéo từ 0 đến 360 độ
- **Trường nhập góc** — nhập giá trị độ chính xác
- **Nút hướng mặc định** — nhấn các biểu tượng mũi tên để chọn các hướng phổ biến (lên, lên phải, phải, xuống phải, xuống, xuống trái, trái, lên trái)

## Điểm màu

Thanh gradient hiển thị các điểm màu hiện tại của bạn dưới dạng các dấu mốc kéo được. Mỗi điểm xác định một màu sắc tại một vị trí cụ thể dọc theo gradient.

**Thêm điểm** — Nhấn nút **+** trong phần Điểm màu để thêm điểm mới. Không có giới hạn cứng về số lượng điểm.

**Chỉnh sửa điểm** — Mỗi điểm trong danh sách hiển thị:
- Một mẫu màu mở trình chọn màu khi được nhấn
- Một giá trị vị trí (0% đến 100%) mà bạn có thể nhập hoặc điều chỉnh
- Một điều khiển độ trong suốt (0 đến 1)
- Một nút xóa để loại bỏ điểm

**Sắp xếp lại** — Kéo các điểm dọc theo thanh gradient để sắp xếp lại chúng trực quan.

## Gradient mặc định

Sáu preset mặc định có sẵn để bắt đầu nhanh chóng. Nhấn vào bất kỳ preset nào để áp dụng ngay lập tức:

| Preset | Màu sắc | Góc |
|--------|--------|-------|
| **Ocean** | Xanh nhạt đến xanh dương | 120 độ |
| **Sunset** | Cam ấm đến hồng cam (3 điểm) | 45 độ |
| **Forest** | Indigo đến xanh lá ngọc | 135 độ |
| **Berry** | Hồng đến tím xanh | 90 độ |
| **Flame** | Đỏ đến vàng kim | 45 độ |
| **Night** | Đen xám đến xanh dương đại dương | 180 độ |

Các preset là điểm bắt đầu. Sau khi áp dụng một preset, bạn có thể chỉnh sửa màu sắc, thêm hoặc xóa điểm và thay đổi góc để tạo ra biến thể của riêng bạn.

## Hành động Footer

| Nút | Hành động |
|--------|--------|
| **Xóa** | Loại bỏ hoàn toàn gradient, đặt lại thành trong suốt |
| **Áp dụng** | Lưu gradient và đóng trình chỉnh sửa |

Đóng trình chỉnh sửa mà không nhấn Áp dụng sẽ hủy bỏ các thay đổi của bạn.

## Nơi nó xuất hiện

Tạo Gradient được sử dụng trong:

- **Trình tạo Trang** — thông qua tab Gradient trong trình chỉnh sửa nền trên bất kỳ phần tử nào
- **Trình tạo Header/Footer** — cho nền gradient trên các phần header, thanh điều hướng và khu vực footer

Nó hoạt động cùng với trình chỉnh sửa nền, cũng cung cấp các tùy chọn nền màu rắn, hình ảnh và video.

## Mẹo

- **Bắt đầu với một preset** — áp dụng một preset gần với điều bạn muốn, sau đó điều chỉnh màu sắc và góc thay vì xây dựng từ đầu.
- **Sử dụng hai hoặc ba điểm** — các gradient đơn giản với hai điểm trông sạch sẽ và chuyên nghiệp. Nhiều điểm hơn có thể hữu ích cho hiệu ứng phức tạp nhưng có thể nhanh chóng trở nên quá tải.
- **Tương thích với màu thương hiệu** — sử dụng trình chọn màu để nhập giá trị hex chính xác từ bảng màu thương hiệu của bạn để có gradient nhất quán và đúng thương hiệu.
- **Kiểm tra với nội dung** — các gradient trông ấn tượng khi đứng một mình có thể làm giảm khả năng đọc của văn bản. Luôn kiểm tra xem văn bản trên nền gradient có độ tương phản đủ để đọc.
- **Thử radial cho hiệu ứng spotlight** — gradient radial hoạt động tốt khi thu hút sự chú ý đến một khu vực trung tâm, ví dụ như điểm nhấn của phần hero.
