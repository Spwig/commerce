---
title: Ví dụ khuyến mãi
---

Hướng dẫn này hiển thị các ví dụ cụ thể về cách cấu hình các loại khuyến mãi khác nhau. Mỗi ví dụ bao gồm các giá trị trường chính xác để nhập vào trình hướng dẫn khuyến mãi, giúp bạn theo dõi hoặc điều chỉnh chúng cho cửa hàng của mình.

![Thẻ khuyến mãi](/static/core/admin/img/help/promotion-examples/promotion-card.webp)

## Ví dụ: Giảm giá theo phần trăm cho một danh mục

**Tình huống:** Giảm 30% cho tất cả giày dép trong đợt thanh lý mùa đông.

Truy cập **Marketing > Sales & Promotions** và nhấn **+ Tạo khuyến mãi**. Nhập các giá trị sau tại từng bước của trình hướng dẫn:

| Bước | Trường | Giá trị |
|------|-------|-------|
| Cơ bản | Tên | Thanh lý mùa đông — Giảm 30% giày dép |
| Cơ bản | Mô tả | Thanh lý cuối mùa cho tất cả giày dép |
| Cơ bản | Hoạt động | Đã chọn |
| Giảm giá | Loại | Giảm theo phần trăm |
| Giảm giá | Giá trị | 30 |
| Lịch trình | Ngày bắt đầu | 15 tháng 1, 2026 |
| Lịch trình | Ngày kết thúc | 28 tháng 2, 2026 |
| Sản phẩm | Áp dụng cho | Danh mục |
| Sản phẩm | Đã chọn | Giày, Giày ủng, Giày sandal |

Điều này tạo ra một đợt bán hàng giới hạn thời gian, tự động giảm giá mọi sản phẩm trong danh mục đã chọn. Một đôi giày ủng 120 đô la trở thành 84 đô la, và một đôi giày sandal 60 đô la trở thành 42 đô la.

## Ví dụ: Giảm giá cố định cho một bộ sưu tập

**Tình huống:** Giảm 15 đô la cho các mặt hàng trong bộ sưu tập Essentials mùa hè.

| Bước | Trường | Giá trị |
|------|-------|-------|
| Cơ bản | Tên | Essentials mùa hè — Giảm 15 đô la |
| Cơ bản | Hoạt động | Đã chọn |
| Giảm giá | Loại | Giảm giá cố định |
| Giảm giá | Giá trị | 15.00 |
| Lịch trình | Ngày bắt đầu | 1 tháng 6, 2026 |
| Lịch trình | Ngày kết thúc | (trống — không có ngày hết hạn) |
| Sản phẩm | Áp dụng cho | Bộ sưu tập |
| Sản phẩm | Đã chọn | Essentials mùa hè |

> **Lưu ý:** Giảm 15 đô la áp dụng cho từng sản phẩm đủ điều kiện riêng lẻ. Một sản phẩm 50 đô la trở thành 35 đô la, một sản phẩm 30 đô la trở thành 15 đô la. Để trống ngày kết thúc có nghĩa là khuyến mãi sẽ chạy vô thời hạn cho đến khi bạn tắt nó thủ công.

## Ví dụ: Đặt giá bán cố định cho đợt thanh lý

**Tình huống:** Đặt tất cả các mặt hàng thanh lý thành 9,99 đô la.

| Bước | Trường | Giá trị |
|------|-------|-------|
| Cơ bản | Tên | Thanh lý cuối cùng — Tất cả sản phẩm 9,99 đô la |
| Cơ bản | Hoạt động | Đã chọn |
| Giảm giá | Loại | Giá bán cố định |
| Giảm giá | Giá trị | 9.99 |
| Lịch trình | Ngày bắt đầu | (hôm nay) |
| Sản phẩm | Áp dụng cho | Bộ sưu tập |
| Sản phẩm | Đã chọn | Thanh lý cuối cùng |

> **Lưu ý:** Giá bán cố định thiết lập giá bán chính xác bất kể giá gốc. Một sản phẩm 75 đô la và một sản phẩm 25 đô la đều trở thành 9,99 đô la. Sử dụng điều này cho các kệ hàng thanh lý hoặc giá bán đồng nhất khi bạn muốn tất cả các mặt hàng ở cùng một mức giá.

![Khuyến mãi theo danh mục](/static/core/admin/img/help/promotion-examples/category-promotion.webp)

## Chọn loại giảm giá phù hợp

| Loại | Cách hoạt động | Phù hợp nhất | Ví dụ |
|------|-------------|----------|---------|
| **Giảm theo phần trăm** | Giảm giá theo tỷ lệ phần trăm | Các đợt giảm giá lớn khi sản phẩm có giá khác nhau | 20% giảm — 100 đô la trở thành 80 đô la, 50 đô la trở thành 40 đô la |
| **Giảm giá cố định** | Trừ một khoản tiền cố định | Các chương trình khuyến mãi với thông điệp tiết kiệm cụ thể theo đô la | 15 đô la giảm — 100 đô la trở thành 85 đô la, 50 đô la trở thành 35 đô la |
| **Giá bán cố định** | Thiết lập giá bán chính xác | Thanh lý, giá đồng nhất, "tất cả ở X đô la" | 9,99 đô la — tất cả các mặt hàng trở thành 9,99 đô la bất kể giá gốc |

## Chọn mục tiêu phù hợp

| Mục tiêu | Cách hoạt động | Phù hợp nhất |
|--------|-------------|----------|
| **Tất cả sản phẩm** | Áp dụng cho tất cả sản phẩm trong cửa hàng | Các đợt giảm giá toàn trang web, sự kiện toàn cửa hàng |
| **Danh mục** | Áp dụng cho tất cả sản phẩm trong danh mục đã chọn | Các đợt bán hàng theo phòng ban, thanh lý theo mùa theo loại |
| **Thương hiệu** | Áp dụng cho tất cả sản phẩm từ thương hiệu đã chọn | Hợp tác thương hiệu, sự kiện thương hiệu cụ thể |
| **Bộ sưu tập** | Áp dụng cho tất cả sản phẩm trong bộ sưu tập đã chọn | Các chương trình khuyến mãi được chọn lọc, bán hàng theo chủ đề |
| **Sản phẩm** | Áp dụng cho các sản phẩm được chọn riêng lẻ | Các chương trình khuyến mãi được chọn tay, lựa chọn giới hạn |

## Mẫu lịch trình

Ba mẫu phổ biến để thiết lập lịch trình khuyến mãi:

| Mẫu | Ngày bắt đầu | Ngày kết thúc | Trường hợp sử dụng |
|---------|-----------|----------|----------|
| **Ngay lập tức, liên tục** | Hôm nay | (trống) | Giảm giá vĩnh viễn, bán hàng dài hạn |
| **Khoảng thời gian** | Ngày trong tương lai | Ngày trong tương lai | Các sự kiện theo mùa, bán hàng lễ hội |
| **Bắt đầu trong tương lai, không có ngày kết thúc** | Ngày trong tương lai | (trống) | Giá bán vĩnh viễn mới bắt đầu vào một ngày cụ thể |

Việc thiết lập Ngày bắt đầu trong tương lai tạo ra một chương trình khuyến mãi được lên lịch. Nó sẽ xuất hiện trong tab **Đã lên lịch** trên bảng điều khiển khuyến mãi và kích hoạt tự động khi ngày đến. Để trống Ngày kết thúc có nghĩa là chương trình khuyến mãi vẫn hoạt động cho đến khi bạn tắt nó thủ công.

## Mẹo

- **Sử dụng tên mô tả** — Bao gồm giá trị giảm giá và mục tiêu trong tên (ví dụ: "Mùa hè 20% giảm giày") để bạn có thể nhanh chóng nhận biết các chương trình khuyến mãi trên bảng điều khiển.
- **Kiểm tra số lượng sản phẩm bị ảnh hưởng** — Bước Xem xét hiển thị số lượng sản phẩm sẽ được giảm giá. Nếu con số trông không đúng, quay lại và kiểm tra lại mục tiêu của bạn.
- **Bắt đầu nhỏ** — Nếu bạn không chắc chắn về một chương trình giảm giá, hãy bắt đầu với tỷ lệ phần trăm nhỏ hơn và tăng lên nếu cần.
- **Sử dụng Giảm giá cố định cho quảng bá** — "15 đô la giảm" là khoản tiết kiệm cụ thể dễ truyền đạt trong quảng cáo và chiến dịch email.
- **Sử dụng Giảm theo phần trăm cho tính công bằng** — Một khoản giảm theo phần trăm tỷ lệ với giá, mang lại khoản tiết kiệm tỷ lệ cho các mức giá khác nhau.