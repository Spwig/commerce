---
title: Background Editor
---

Chỉnh sửa nền

Chỉnh sửa nền cho phép bạn kiểm soát hoàn toàn nền của các phần tử với bốn loại: màu rắn, gradient, hình ảnh và video. Nó cũng hỗ trợ trạng thái Normal và Hover riêng biệt, giúp bạn tạo hiệu ứng thị giác tương tác. Mở tab **Style** của bất kỳ phần tử nào và tìm phần **Background** để truy cập trình chỉnh sửa.

![Chỉnh sửa nền](/static/core/admin/img/help/background-editor/background-editor.webp)

## Trạng thái Normal và Hover

Ở đầu trình chỉnh sửa nền, một nút chuyển đổi giữa các trạng thái **Normal** và **Hover**. Mỗi trạng thái có cấu hình nền độc lập:

- **Normal** — nền mặc định được hiển thị khi trang được tải
- **Hover** — nền được áp dụng khi người truy cập di chuột qua phần tử

Hai khối xem trước nhỏ bên cạnh nút chuyển đổi hiển thị nền Normal và Hover song song, giúp bạn dễ dàng so sánh sự khác biệt. Cấu hình trạng thái Normal trước, sau đó chuyển sang Hover để thêm hiệu ứng tương tác nếu cần.

## Loại nền

Chọn một loại nền từ hàng biểu tượng ở đầu bảng điều khiển chỉnh sửa:

| Loại | Mô tả |
|------|-------------|
| **Màu sắc** | Điền đầy bằng một giá trị màu đơn. Dễ áp dụng và nhẹ nhàng. |
| **Gradient** | Sự pha trộn mượt giữa hai hoặc nhiều màu, có thể là tuyến tính hoặc radial. Bao gồm các cài đặt mặc định như Ocean, Sunset, Forest, và Berry. Để chỉnh sửa gradient nâng cao, xem chủ đề [Gradient Creator](gradient-creator). |
| **Hình ảnh** | Hình ảnh được tải lên hoặc chọn từ thư viện phương tiện. Hỗ trợ điều khiển vị trí, kích thước và lặp lại. |
| **Video** | URL video nền với hình ảnh poster tùy chọn hiển thị khi video đang tải hoặc trên thiết bị di động. |

Chỉ có một loại có thể hoạt động tại một thời điểm cho mỗi trạng thái. Chuyển đổi loại không xóa cấu hình trước đó — bạn có thể chuyển đổi trở lại và cài đặt sẽ được giữ nguyên.

## Nền màu sắc

Khi chọn **Màu sắc**:

- **Nhập mã hex** — Nhập trực tiếp mã hex (ví dụ: `#1A1A2E`)
- **Màu mẫu** — Nhấp vào mẫu màu cài đặt sẵn để chọn nhanh. Các mẫu màu nhận biết chủ đề và phản ánh bảng màu của chủ đề đang hoạt động.
- **Nút chỉnh sửa** — Mở trình chọn màu đầy đủ với phổ màu, thanh trượt và tùy chọn định dạng (xem chủ đề [Color Picker](color-picker))

Các nền màu sắc được hiển thị ngay lập tức và không ảnh hưởng đến hiệu suất, khiến chúng lý tưởng cho các phần, thẻ và hộp chứa.

## Nền gradient

Khi chọn **Gradient**:

- **Gradient mặc định** — Chọn từ các gradient có sẵn: Ocean, Sunset, Forest, Berry và các gradient khác
- **Gradient tùy chỉnh** — Nhấp **Edit** để mở trình tạo gradient, nơi bạn có thể thiết lập hướng, loại (tuyến tính hoặc radial) và điểm màu
- **Thanh trượt góc** — Điều chỉnh hướng gradient cho gradient tuyến tính (0-360 độ)

Gradient thêm chiều sâu thị giác mà không cần tài nguyên hình ảnh và mở rộng hoàn hảo cho mọi kích thước màn hình.

## Nền hình ảnh

Khi chọn **Hình ảnh**:

- **Tải lên hoặc thư viện phương tiện** — Nhấp vào vị trí hình ảnh để tải lên hình ảnh mới hoặc chọn từ thư viện phương tiện của bạn
- **Kích thước** — Chọn **Cover** (lấp đầy phần tử, có thể cắt), **Contain** (phù hợp bên trong phần tử), hoặc kích thước tùy chỉnh
- **Vị trí** — Thiết lập điểm tập trung bằng lưới 9 điểm (trên trái, giữa, dưới phải, v.v.) hoặc nhập phần trăm X/Y tùy chỉnh
- **Lặp lại** — Bật/tắt lặp lại. Hữu ích cho các mô hình lặp lại
- **Lớp phủ** — Thêm lớp phủ màu trên hình ảnh với độ trong suốt có thể điều chỉnh, hữu ích để đảm bảo tính đọc được của văn bản

Luôn tối ưu hóa hình ảnh trước khi tải lên. Các hình ảnh lớn chưa nén làm chậm thời gian tải trang.

## Nền video

Khi chọn **Video**:

- **URL video** — Nhập URL trực tiếp đến tệp video MP4 hoặc WebM
- **Hình ảnh poster** — Tải lên hình ảnh dự phòng được hiển thị khi video đang tải và trên các thiết bị không tự động phát video
- **Tự động phát / Lặp / Tĩnh âm** — Nền video tự động phát, lặp và được tắt âm mặc định để tuân thủ chính sách trình duyệt

Giữ các video nền ngắn (10-30 giây), nén và tinh tế về mặt thị giác.

Chúng nên cải thiện phần này mà không làm phân tâm nội dung.

## Nơi xuất hiện

Trình chỉnh sửa nền có sẵn cho mọi phần tử hỗ trợ nền:

- **Page Builder** — Các phần, container, cột và các phần tử riêng lẻ đều có phần Nền trong tab Phong cách
- **Header/Footer Builder** — Nền hàng và nền của từng widget riêng lẻ
- **Menu Builder** — Nền container menu và nền bảng thả xuống

Giao diện chỉnh sửa giống nhau ở mọi nơi, do đó quy trình làm việc của bạn sẽ nhất quán trên tất cả các trình xây dựng.

## Mẹo

- Sử dụng lớp phủ màu bán trong suốt trên nền hình ảnh để đảm bảo văn bản vẫn dễ đọc bất kể nội dung hình ảnh.
- Các cài đặt gradient là cách nhanh chóng để thêm sự hấp dẫn thị giác — áp dụng một cài đặt, sau đó tùy chỉnh góc hoặc màu sắc để phù hợp với thương hiệu của bạn.
- Thiết lập cả nền Normal và Hover cho các thẻ tương tác để cung cấp phản hồi thị giác rõ ràng khi khách truy cập khám phá nội dung của bạn.
- Đối với nền hình ảnh, luôn thiết lập điểm tập trung để phần quan trọng nhất của hình ảnh vẫn hiển thị trên mọi kích thước màn hình.
- Ưu tiên nền màu sắc hoặc gradient thay vì hình ảnh cho các phần mà tốc độ tải là yếu tố quan trọng, chẳng hạn như nội dung trên gập (above-the-fold content).
- Kiểm tra nền video trên thiết bị di động — hầu hết trình duyệt di động sẽ hiển thị hình ảnh đại diện thay vì phát video.