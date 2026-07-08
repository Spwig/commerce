---
title: Chỉnh sửa khoảng cách
---

Chỉnh sửa khoảng cách trực quan cho phép bạn cấu hình khoảng cách và độ giãn bằng sơ đồ mô hình hộp trực quan. Kiểm soát khoảng cách chính xác đảm bảo bố cục nhất quán và trải nghiệm đọc thoải mái trên toàn bộ cửa hàng của bạn. Mở tab **Style** của bất kỳ phần tử nào và tìm phần **Spacing** để truy cập trình chỉnh sửa.

![Chỉnh sửa khoảng cách](/static/core/admin/img/help/spacing-editor/spacing-editor.webp)

## Sơ đồ mô hình hộp

Trình chỉnh sửa hiển thị sơ đồ mô hình hộp trực quan với ba lớp lồng nhau:

- **Margin** (vòng ngoài, thường được hiển thị bằng màu cam) — Khoảng cách bên ngoài viền phần tử, tách phần tử khỏi các phần tử lân cận
- **Padding** (vòng trong, thường được hiển thị bằng màu xanh lá) — Khoảng cách giữa viền phần tử và nội dung của nó
- **Content** (khu vực trung tâm) — Nội dung thực tế của phần tử, như văn bản hoặc hình ảnh

Mỗi cạnh của sơ đồ (trên, phải, dưới, trái) có một tay cầm kéo và một trường nhập số. Kéo tay cầm ra ngoài để tăng giá trị, hoặc kéo vào trong để giảm giá trị. Bạn cũng có thể nhấp trực tiếp vào giá trị của cạnh để nhập một số cụ thể.

## Tab Khoảng cách và Độ giãn

Hai tab ở đầu trình chỉnh sửa chuyển đổi giữa chế độ **Margin** và **Padding**. Khi chọn Margin, vòng ngoài được đánh dấu và có thể chỉnh sửa. Khi chọn Padding, vòng trong được đánh dấu và có thể chỉnh sửa. Vòng không hoạt động vẫn hiển thị để tham khảo nhưng được làm mờ.

Cả hai tab đều chia sẻ cùng một điều khiển và tùy chọn đơn vị, vì vậy quy trình làm việc giống nhau cho việc cấu hình khoảng cách và độ giãn.

## Điều khiển theo cạnh

Mỗi cạnh có một trường nhập giá trị độc lập và một trình chọn đơn vị:

| Cạnh | Mô tả |
|------|-------------|
| **Trên** | Khoảng cách phía trên phần tử (margin) hoặc phía trên nội dung (padding) |
| **Phải** | Khoảng cách bên phải của phần tử hoặc nội dung |
| **Dưới** | Khoảng cách phía dưới phần tử hoặc nội dung |
| **Trái** | Khoảng cách bên trái của phần tử hoặc nội dung |

Nhấp vào giá trị của cạnh bất kỳ trong sơ đồ để chọn nó, sau đó nhập một số hoặc sử dụng phím mũi tên lên/xuống để tăng giá trị 1 đơn vị. Giữ phím Shift khi nhấn phím mũi tên để tăng giá trị 10 đơn vị.

## Đơn vị

Trình chọn đơn vị bên cạnh mỗi trường nhập giá trị cho phép bạn chọn đơn vị đo lường:

| Đơn vị | Mô tả |
|------|-------------|
| **px** | Pixel. Kích thước cố định, nhất quán trên các thiết bị. Tốt nhất cho các giá trị khoảng cách nhỏ và chính xác. |
| **em** | Tương đối với kích thước phông chữ của phần tử. Tự động điều chỉnh khi thay đổi kiểu chữ. |
| **rem** | Tương đối với kích thước phông chữ gốc. Cung cấp quy mô nhất quán trên toàn trang. |
| **%** | Phần trăm chiều rộng của phần tử cha. Hữu ích cho bố cục linh hoạt và thích ứng. |
| **auto** | Cho phép trình duyệt tính toán giá trị tự động. Thường được sử dụng để căn chỉnh ngang bằng khoảng cách trái/phải. |

Chọn một đơn vị phù hợp với mục đích của bạn — sử dụng `px` cho khoảng cách cố định, `rem` cho khoảng cách có thể mở rộng tuân theo các token kiểu chữ của chủ đề, và `%` cho bố cục cần điều chỉnh theo chiều rộng của container.

## Liên kết cạnh

Biểu tượng **liên kết** ở trung tâm sơ đồ chuyển đổi giữa chế độ liên kết:

- **Liên kết** (biểu tượng chuỗi được kết nối) — Thay đổi giá trị của bất kỳ cạnh nào sẽ cập nhật tất cả bốn cạnh thành cùng một giá trị. Hữu ích cho khoảng cách đồng nhất.
- **Không liên kết** (biểu tượng chuỗi bị đứt) — Mỗi cạnh được kiểm soát độc lập. Sử dụng khi bạn cần các giá trị khác nhau cho trên/dưới và trái/phải.

Nhấp vào biểu tượng liên kết để chuyển đổi giữa các chế độ. Khi bạn chuyển từ chế độ không liên kết sang chế độ liên kết, tất cả bốn cạnh sẽ được đặt thành giá trị của cạnh được chỉnh sửa gần nhất.

## Cài đặt nhanh

Một hàng các nút cài đặt mặc định dưới sơ đồ cung cấp cấu hình khoảng cách một cú nhấp chuột:

| Cài đặt | Giá trị |
|--------|--------|
| **Không** | 0 trên tất cả các cạnh |
| **Nhỏ** | Khoảng cách nhỏ gọn phù hợp cho bố cục chật và các phần tử inline |
| **Trung bình** | Khoảng cách cân bằng cho mục đích chung trên các thẻ và phần |
| **Lớn** | Khoảng cách rộng rãi cho các khu vực hero và phần có trọng tâm cao |
| **XL** | Khoảng cách rộng hơn cho các banner toàn màn hình và các phần cấp cao của trang |

Cài đặt áp dụng cho tab đang hoạt động (Margin hoặc Padding) và thiết lập tất cả bốn cạnh cùng lúc. Sau khi áp dụng cài đặt, bạn có thể điều chỉnh các cạnh riêng lẻ nếu cần.

## Nơi xuất hiện

Trình chỉnh sửa khoảng cách có sẵn cho mọi phần tử hỗ trợ khoảng cách bố cục:

- **Trình xây dựng trang** — Tab Style, phần Spacing trên các phần, container, cột và các phần tử riêng lẻ
- **Trình xây dựng tiêu đề/chân trang** — Điều khiển khoảng cách hàng và widget cho khoảng cách dọc và ngang
- **Trình xây dựng menu** — Thiết lập độ giãn của mục menu và khoảng cách container

Giao diện trình chỉnh sửa giống nhau ở mọi nơi, đảm bảo trải nghiệm nhất quán trên các trình xây dựng.

## Mẹo

- Sử dụng các giá trị khoảng cách nhất quán trên các trang của bạn — chọn 2-3 kích cỡ tiêu chuẩn và giữ nguyên chúng để có bố cục sạch sẽ và chuyên nghiệp.
- Thiết lập margin thành **auto** cho trái và phải để căn chỉnh ngang một phần tử có độ rộng cố định bên trong phần tử cha.
- Ưu tiên sử dụng đơn vị `rem` cho khoảng cách nếu chủ đề của bạn sử dụng kiểu chữ thích ứng, để khoảng cách mở rộng tỷ lệ với kích thước văn bản.
- Sử dụng chế độ liên kết để thiết lập độ giãn đồng nhất nhanh chóng, sau đó ngắt liên kết và tinh chỉnh từng cạnh nếu nội dung cần khoảng cách không đối xứng.
- Tránh độ giãn quá mức trên thiết bị di động — kiểm tra khoảng cách của bạn ở độ rộng viewport hẹp để đảm bảo nội dung không bị chèn ép hoặc có độ giãn quá mức.