---
title: Chỉnh sửa viền
---

Chỉnh sửa viền cung cấp kiểm soát tinh tế đối với viền của các phần tử, bao gồm kiểu, màu sắc, độ rộng theo từng cạnh và bán kính góc theo từng góc. Nó mở ra dưới dạng một bảng điều khiển nổi với chế độ xem trực tiếp và hai tab cho cài đặt cơ bản và nâng cao.

![Chỉnh sửa viền](/static/core/admin/img/help/border-editor/border-editor.webp)

## Chế độ xem trực tiếp

Một hộp xem trước ở phía trên của trình chỉnh sửa hiển thị các thay đổi viền của bạn theo thời gian thực. Hộp hiển thị từ khóa "Preview" bên trong một hình chữ nhật có viền được cập nhật ngay lập tức khi bạn điều chỉnh các giá trị kiểu, màu sắc, độ rộng và bán kính.

## Chế độ Cơ bản vs Nâng cao

Trình chỉnh sửa được tổ chức thành hai tab:

| Tab | Nội dung chứa |
|-----|-----------------|
| **Cơ bản** | Kiểu viền, màu sắc, độ rộng (với điều khiển theo từng cạnh), và bán kính viền (với điều khiển theo từng góc) |
| **Nâng cao** | Tinh chỉnh bán kính góc riêng lẻ và thuộc tính Hình dạng Góc thử nghiệm |

Hầu hết công việc viền được thực hiện hoàn toàn trong tab Cơ bản. Tab Nâng cao hữu ích khi bạn cần kiểm soát chính xác từng góc hoặc muốn thử nghiệm với các tính năng CSS mới hơn.

## Kiểu viền

Một danh sách thả xuống với chín tùy chọn kiểm soát kiểu đường viền:

| Kiểu | Mô tả |
|-------|-------------|
| **Không** | Không có viền (loại bỏ bất kỳ viền nào hiện có) |
| **Đậm** | Một đường liên tục (mặc định) |
| **Đứt đoạn** | Một chuỗi các đoạn ngắn |
| **Chấm** | Một chuỗi các chấm tròn |
| **Kép** | Hai đường liên tục song song |
| **Lõm** | Một viền được chạm khắc, hiệu ứng 3D trông như bị nhấn vào bề mặt |
| **Nổi** | Một viền được nâng lên, hiệu ứng 3D (ngược lại với lõm) |
| **Làm lõm** | Làm cho phần tử trông như được chôn hoặc nhấn vào |
| **Làm nổi** | Làm cho phần tử trông như được nâng lên hoặc nổi bật |

Thiết lập kiểu thành Không sẽ loại bỏ hoàn toàn viền, bất kể cài đặt độ rộng hoặc màu sắc.

## Màu viền

Một trường đầu vào văn bản đi kèm với nút chọn màu. Nhập giá trị hex trực tiếp (ví dụ: `#3b82f6`) hoặc nhấp vào ô màu để mở trình chọn màu đầy đủ với các chế độ đầu vào hex, RGB và HSL cùng với một khu vực màu trực quan. Màu mặc định là đen (`#000000`).

## Độ rộng viền

Kiểm soát độ dày của viền theo pixel. Tab Cơ bản hiển thị bốn đầu vào riêng lẻ cho từng cạnh:

| Cạnh | Đầu vào |
|------|-------|
| **Trên** | Đầu vào số, tối thiểu 0 |
| **Phải** | Đầu vào số, tối thiểu 0 |
| **Dưới** | Đầu vào số, tối thiểu 0 |
| **Trái** | Đầu vào số, tối thiểu 0 |

Một **nút chuyển đổi liên kết** (biểu tượng chuỗi) bên cạnh nhãn kiểm soát xem liệu cả bốn cạnh có được liên kết hay không:

- **Liên kết** (mặc định) — thay đổi bất kỳ giá trị nào sẽ cập nhật tất cả bốn cạnh cùng lúc
- **Không liên kết** — mỗi cạnh có thể có độ rộng khác nhau, hữu ích cho hiệu ứng như viền chỉ ở dưới hoặc viền nhấn mạnh bên trái

## Bán kính viền

Kiểm soát độ tròn của từng góc. Tab Cơ bản hiển thị bốn đầu vào góc:

| Góc | Nhãn |
|--------|-------|
| **Trên trái** | TL |
| **Trên phải** | TR |
| **Dưới trái** | BL |
| **Dưới phải** | BR |

Một **nút chuyển đổi liên kết** hoạt động theo cùng cách như độ rộng viền:

- **Liên kết** (mặc định) — tất cả bốn góc chia sẻ cùng một giá trị bán kính
- **Không liên kết** — mỗi góc có thể có bán kính khác nhau

Các giá trị bán kính phổ biến:

| Giá trị | Hiệu ứng |
|-------|--------|
| 0px | Góc vuông sắc nét |
| 4-8px | Độ tròn tinh tế, phù hợp cho các thẻ và nút |
| 12-16px | Độ tròn rõ rệt, kiểu hiện đại và mềm mại |
| 50% | Hình tròn hoặc hình viên thuốc (tùy thuộc vào kích thước phần tử) |

Trình chọn đơn vị hỗ trợ px, em, rem và % cho cả giá trị độ rộng và bán kính.

## Hình dạng góc (Nâng cao)

Tab Nâng cao bao gồm thuộc tính **Hình dạng góc** thử nghiệm. Tính năng CSS này kiểm soát liệu các góc tròn sử dụng hình dạng tròn tiêu chuẩn hay hình dạng góc sắc hơn "scoop". Hỗ trợ trình duyệt bị giới hạn, và trình chỉnh sửa hiển thị cảnh báo tương thích khi trình duyệt hiện tại không hỗ trợ thuộc tính này.

## Hành động chân trang

| Nút | Hành động |
|--------|--------|
| **Khôi phục** | Quay lại tất cả giá trị về trạng thái khi trình chỉnh sửa được mở |
| **Hủy bỏ** | Đóng trình chỉnh sửa mà không áp dụng thay đổi |
| **Áp dụng** | Lưu cài đặt viền và đóng trình chỉnh sửa |

## Nơi xuất hiện

Trình chỉnh sửa viền có sẵn trên nhiều trình xây dựng:

- **Trình xây dựng Trang** — chọn bất kỳ phần tử nào, mở tab Phong cách, và nhấp vào phần Viền
- **Trình xây dựng Tiêu đề/Chân trang** — thêm viền cho các phần tiêu đề, hộp chứa điều hướng và khu vực chân trang
- **Trình xây dựng Menu** — thiết lập viền cho các mục menu và hộp chứa dropdown

Trình chỉnh sửa đọc các kiểu viền được tính toán hiện tại từ phần tử sống trên khung vẽ, vì vậy nó luôn mở với các giá trị hiện có đúng.

## Mẹo

- **Sử dụng viền một cách tiết kiệm** — các viền mỏng 1px màu xám nhạt tạo sự tách biệt rõ ràng giữa các phần mà không làm tăng trọng lượng thị giác.
- **Kết hợp bán kính với bóng đổ** — các góc tròn đi kèm với bóng đổ mềm mại (qua trình chỉnh sửa Bóng đổ) tạo hiệu ứng thẻ tinh tế.
- **Thử viền một cạnh** — ngắt liên kết các cạnh và chỉ đặt viền dưới hoặc bên trái để tạo đường viền nhấn mạnh, đường phân tách phần hoặc chỉ báo thanh bên.
- **Sử dụng bán kính phần trăm cho hình viên thuốc** — đặt tất cả các góc thành 50% trên nút hoặc nhãn để tạo hình viên thuốc thích ứng với bất kỳ kích thước nội dung nào.
- **Kiểm tra chế độ xem trước** — hộp xem trước trực tiếp được cập nhật ngay lập tức, vì vậy hãy thoải mái thử nghiệm trước khi áp dụng.