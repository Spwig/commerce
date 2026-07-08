---
title: Màu sắc
---

Bộ chọn màu nâng cao cho phép bạn chọn màu bằng nhiều phương pháp đầu vào và các cài đặt có sẵn theo chủ đề. Nó xuất hiện bất cứ nơi nào thuộc tính màu được sử dụng trên nền tảng — trong trình tạo trang, trình tạo đầu/footer, trình tạo menu và quản trị danh mục. Nhấp vào bất kỳ ô màu nào hoặc trường đầu vào màu để mở trình chọn màu.

![Màu sắc](/static/core/admin/img/help/color-picker/color-picker.webp)

## Phương pháp đầu vào màu

Bộ chọn hỗ trợ nhiều cách để xác định một màu:

| Phương pháp | Mô tả | Ví dụ |
|-----------|-------|--------|
| **Hex** | Nhập trực tiếp mã hex 6 chữ số | `#FF5733` |
| **RGB** | Điều chỉnh thanh trượt Red, Green và Blue (mỗi thanh từ 0-255) | `rgb(255, 87, 51)` |
| **HSL** | Thiết lập Hue (0-360), Saturation (0-100%) và Lightness (0-100%) | `hsl(14, 100%, 60%)` |
| **RGBA** | RGB với kênh độ trong suốt (alpha) | `rgba(255, 87, 51, 0.8)` |
| **HSLA** | HSL với kênh độ trong suốt (alpha) | `hsla(14, 100%, 60%, 0.8)` |
| **Bảng phổ màu** | Nhấp hoặc kéo trên khu vực phổ màu để chọn trực quan | Chọn bằng cách nhấp chuột |

Bạn cũng có thể nhập giá trị trực tiếp vào trường văn bản ở phía dưới của trình chọn màu.

## Bộ chọn định dạng

Một danh sách thả xuống ở phía trên của trình chọn màu cho phép bạn chuyển đổi giữa các chế độ đầu ra **HEX**, **RGB**, **RGBA**, **HSL**, và **HSLA**. Khi bạn chuyển đổi định dạng, màu hiện tại sẽ được chuyển đổi tự động — không có giá trị nào bị mất. Chọn định dạng phù hợp nhất với quy trình làm việc hoặc yêu cầu của hệ thống thiết kế của bạn.

## Màu cài sẵn

Dưới khu vực phổ màu, một hàng các ô màu truy cập nhanh cung cấp lựa chọn một lần nhấp cho các màu phổ biến. Các ô màu này **có thể nhận biết chủ đề**: chúng tự động phản ánh các màu chính, phụ, nhấn mạnh và trung tính của chủ đề đang hoạt động. Điều này giúp bạn dễ dàng duy trì tính nhất quán với thương hiệu mà không cần ghi nhớ mã hex.

Để áp dụng một cài sẵn, nhấp vào ô màu. Trình chọn màu sẽ cập nhật ngay lập tức để hiển thị màu đã chọn trong khu vực phổ và các trường đầu vào.

## Độ trong suốt / Alpha

Khi sử dụng chế độ RGBA hoặc HSLA, một thanh trượt **alpha** nằm ngang xuất hiện dưới khu vực phổ. Kéo thanh để thiết lập độ trong suốt từ 0% (hoàn toàn trong suốt) đến 100% (hoàn toàn không trong suốt). Giá trị độ trong suốt cũng có thể được chỉnh sửa như một đầu vào số bên cạnh thanh trượt để kiểm soát chính xác.

Các màu bán trong suốt rất hữu ích cho các lớp phủ, hiệu ứng hover và các phần tử thiết kế phân tầng.

## Màu hiện tại và màu mới

Ở phía dưới trình chọn màu, hai hộp hiển thị song song cho thấy **màu hiện tại** được áp dụng và **màu mới** được chọn. So sánh này giúp bạn đánh giá sự thay đổi trước khi xác nhận. Nhấp **Áp dụng** để chấp nhận màu mới, hoặc nhấp ra ngoài trình chọn để hủy bỏ và giữ nguyên giá trị hiện tại.

## Nơi hiển thị

Trình chọn màu là một công cụ chia sẻ được sử dụng trên toàn bộ giao diện quản trị:

- **Trình tạo trang** — Màu chữ, màu nền, màu viền và trạng thái hover trong tab Phong cách
- **Trình tạo đầu/footer** — Màu chữ, màu nền, màu biểu tượng và màu liên kết của widget
- **Trình tạo menu** — Màu liên kết mục menu và màu trạng thái hover/active
- **Quản trị danh mục** — Màu nhãn sản phẩm và màu nhấn mạnh danh mục

Bất kỳ trường nào chấp nhận giá trị màu đều mở trình chọn màu này, do đó trải nghiệm là nhất quán ở mọi nơi.

## Một số mẹo

- Sử dụng các ô màu cài sẵn của chủ đề để duy trì tính nhất quán thương hiệu trên các trang và thành phần.
- Chuyển sang chế độ HSL khi bạn cần tạo các biến thể sáng hơn hoặc tối hơn của cùng một tông màu — chỉ cần điều chỉnh giá trị Lightness.
- Sao chép mã hex từ trường văn bản để sử dụng lại chính xác cùng một màu trong trường khác hoặc chia sẻ với nhà thiết kế.
- Sử dụng RGBA với độ trong suốt giảm để tạo hiệu ứng lớp phủ tinh tế trên hình ảnh và phần tử hero.
- Trình chọn ghi nhớ các màu đã sử dụng gần đây trong phiên làm việc của bạn, do đó các màu tùy chỉnh được sử dụng thường xuyên vẫn dễ truy cập.
- Nếu bạn dán giá trị màu vào trường hex đầu vào ở bất kỳ định dạng nào được hỗ trợ, trình chọn sẽ nhận diện và chuyển đổi tự động.