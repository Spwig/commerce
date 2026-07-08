---
title: Cấu hình Thuế
---

Cấu hình các quy tắc thuế cho cửa hàng của bạn để các loại thuế đúng được áp dụng tự động cho các đơn hàng dựa trên vị trí của khách hàng. Bạn có thể tải các cài đặt thuế khu vực với một cú nhấp chuột hoặc tạo các quy tắc tùy chỉnh cho bất kỳ quốc gia, bang, thành phố hoặc mã bưu chính nào.

![Bảng điều khiển Thuế](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Bảng điều khiển Thuế

Truy cập **Đơn hàng > Giao hàng > Mức thuế** để mở bảng điều khiển thuế. Trang hiển thị:

- **Bảng thống kê** — bốn thẻ hiển thị Tổng số Quy tắc, Quy tắc Hoạt động, Các Quốc gia Bao phủ và Loại Thuế đang sử dụng
- **Lọc** — tìm kiếm theo tên, quốc gia hoặc bang, và lọc theo quốc gia, loại thuế (Thuế bán hàng, VAT, GST, Tùy chỉnh) hoặc trạng thái (Hoạt động/Không hoạt động)
- **Thẻ quy tắc thuế** — mỗi thẻ hiển thị cờ quốc gia, tên quy tắc, vị trí, tỷ lệ phần trăm, nhãn loại thuế, nhãn trạng thái, độ ưu tiên và số lượng miễn trừ

## Tải cài đặt thuế mặc định

Nhấp vào **Tải cài đặt** để mở cửa sổ cài đặt. Các cài đặt là tập hợp các mức thuế tiêu chuẩn cho một khu vực, sẵn sàng để tải vào cửa hàng của bạn chỉ với một cú nhấp chuột.

![Tải cài đặt](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

Các cài đặt được tổ chức theo khu vực thế giới:

| Khu vực | Nhóm cài đặt |
|--------|--------------|
| **Châu Phi** | VAT Châu Phi (25 mức thuế) |
| **Châu Á - Thái Bình Dương** | VAT/GST Châu Á - Thái Bình Dương (24 mức thuế), VAT Trung Á (6 mức thuế) |
| **Châu Âu** | Mức thuế VAT EU, VAT Anh, VAT châu Âu khác |
| **Châu Mỹ Latinh** | VAT Châu Mỹ Latinh |
| **Trung Đông** | VAT Trung Đông |
| **Châu Mỹ Bắc** | Thuế bán hàng theo bang Hoa Kỳ, GST/HST Canada |
| **Oceania** | GST/VAT Oceania |

### Cách cài đặt hoạt động

1. Nhấp vào **Tải** trên nhóm cài đặt bạn muốn
2. Hệ thống tạo các quy tắc thuế cho mọi quốc gia hoặc bang trong nhóm đó
3. Các quy tắc hiện có với cùng quốc gia, bang và loại thuế sẽ tự động bị bỏ qua để tránh trùng lặp
4. Sau khi tải, mỗi quy tắc có thể chỉnh sửa đầy đủ — điều chỉnh tỷ lệ, thêm miễn trừ hoặc ngừng kích hoạt các quy tắc bạn không cần

Bạn có thể tải nhiều nhóm cài đặt. Ví dụ, tải cả VAT EU và VAT Anh nếu bạn bán hàng cho khách hàng ở nhiều nơi tại châu Âu.

## Tạo quy tắc thuế thủ công

Nhấp vào **Thêm Mức Thuế** để tạo quy tắc tùy chỉnh. Biểu mẫu có bốn phần:

![Biểu mẫu Mức Thuế](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Thông tin cơ bản

| Trường | Mô tả |
|-------|-------------|
| **Tên** | Tên hiển thị cho quy tắc (ví dụ: "Thuế bán hàng California") |
| **Hoạt động** | Chuyển đổi để kích hoạt hoặc tắt quy tắc |
| **Loại thuế** | Thuế bán hàng, VAT, GST hoặc Thuế tùy chỉnh |
| **Tỷ lệ (%)** | Mức thuế dưới dạng phần trăm (ví dụ: nhập 8.25 cho 8.25%) |
| **Ưu tiên** | Số cao hơn sẽ được ưu tiên hơn khi nhiều quy tắc khớp với cùng một vị trí |

### Phạm vi địa lý

| Trường | Mô tả |
|-------|-------------|
| **Quốc gia** | Mã ISO 3166-1 alpha-2 (ví dụ: US, GB, DE) |
| **Bang** | Bang hoặc tỉnh (trống để áp dụng cho toàn bộ quốc gia) |
| **Thành phố** | Tên thành phố (tùy chọn, cho quy tắc thuế cấp thành phố) |
| **Mã bưu chính** | Danh sách các mã bưu chính cụ thể (tùy chọn, cho quy tắc thuế cấp mã bưu chính) |

Các quy tắc được khớp từ cụ thể nhất đến ít cụ thể nhất. Một quy tắc cho mã bưu chính cụ thể sẽ được ưu tiên hơn quy tắc cho cùng bang, quy tắc này lại được ưu tiên hơn quy tắc áp dụng cho toàn quốc.

### Quy tắc áp dụng

| Trường | Mô tả |
|-------|-------------|
| **Áp dụng cho giao hàng** | Khi được chọn, thuế này cũng áp dụng cho chi phí giao hàng |
| **Thuế kết hợp** | Khi được chọn, thuế này được tính trên các thuế khác (số tiền cơ bản cộng các thuế đã áp dụng trước đó) |

### Miễn trừ sản phẩm

| Trường | Mô tả |
|-------|-------------|
| **Loại sản phẩm miễn trừ** | Các loại sản phẩm miễn trừ thuế này (ví dụ: số, dịch vụ) |
| **Danh mục miễn trừ** | Các danh mục sản phẩm cụ thể miễn trừ thuế này |

## Loại thuế

| Loại | Được sử dụng cho | Ví dụ |
|------|----------|---------|
| **Thuế bán hàng** | Hoa Kỳ, Canada | Thuế bán hàng cấp bang và tỉnh |
| **VAT** | Châu Âu, Vương quốc Anh, phần lớn châu Á và châu Phi | Thuế giá trị gia tăng |
| **GST** | Úc, New Zealand, Ấn Độ, Singapore | Thuế hàng hóa và dịch vụ |
| **Thuế tùy chỉnh** | Các trường hợp đặc biệt | Thuế bổ sung địa phương, thuế môi trường, thuế xa hoa |

## Cách tính thuế hoạt động

Khi khách hàng đến thanh toán, hệ thống tự động tính thuế dựa trên địa chỉ giao hàng của họ:

1. **Phối hợp địa lý** — tìm tất cả các quy tắc đang hoạt động khớp với quốc gia của khách hàng, sau đó thu hẹp theo bang, thành phố và mã bưu chính
2. **Đánh giá mức độ cụ thể** — các quy tắc cụ thể hơn (mã bưu chính > thành phố > bang > quốc gia) được xếp hạng cao hơn
3. **Sắp xếp theo độ ưu tiên** — trong cùng một mức độ cụ thể, các quy tắc có độ ưu tiên cao hơn được ưu tiên hơn
4. **Miễn trừ sản phẩm** — các sản phẩm miễn trừ được loại bỏ khỏi mỗi quy tắc áp dụng
5. **Thuế không kết hợp** — được tính trước trên giá cơ bản của từng mặt hàng
6. **Thuế kết hợp** — được tính trên giá cơ bản cộng tất cả các thuế không kết hợp đã áp dụng
7. **Thuế giao hàng** — nếu quy tắc có tùy chọn "Áp dụng cho giao hàng" được kích hoạt, chi phí giao hàng được tính vào số tiền chịu thuế

Phân tích thuế được lưu trữ cùng với đơn hàng để bạn có thể xem chính xác các quy tắc nào đã được áp dụng và mỗi quy tắc đã đóng góp bao nhiêu.

## Cấu hình phổ biến

### Cửa hàng EU

1. Nhấp vào **Tải cài đặt** và tải nhóm **Mức thuế VAT EU**
2. Điều này tạo ra các quy tắc VAT cho tất cả các quốc gia thành viên EU với tỷ lệ tiêu chuẩn hiện tại của họ
3. Tùy chọn tải **VAT Anh** nếu bạn cũng bán hàng cho Vương quốc Anh

### Cửa hàng Mỹ

1. Nhấp vào **Tải cài đặt** và tải nhóm **Thuế bán hàng theo bang Mỹ**
2. Điều này tạo ra các quy tắc thuế bán hàng cho tất cả các bang tại Mỹ thu thuế bán hàng
3. Đối với thuế cấp thành phố, thêm quy tắc thủ công với trường thành phố được điền và độ ưu tiên cao hơn

### Cửa hàng đa khu vực

1. Tải nhiều nhóm cài đặt cho mỗi thị trường bạn bán hàng
2. Hệ thống áp dụng thuế đúng dựa trên vị trí của từng khách hàng
3. Điều chỉnh các quy tắc cá nhân theo nhu cầu cụ thể của doanh nghiệp bạn

## Mẹo

- **Bắt đầu với cài đặt** — tải các nhóm cài đặt cho thị trường mục tiêu của bạn, sau đó tùy chỉnh các tỷ lệ cụ thể thay vì tạo mọi quy tắc từ đầu.
- **Sử dụng độ ưu tiên một cách khôn ngoan** — đặt giá trị độ ưu tiên cao hơn cho các quy tắc địa phương cụ thể để chúng đúng cách ghi đè lên các quy tắc khu vực rộng hơn.
- **Kiểm tra kỹ thuế kết hợp** — thuế kết hợp hiếm gặp. Hầu hết các khu vực pháp lý sử dụng thuế đơn giản (không kết hợp). Chỉ kích hoạt thuế kết hợp khi quy định địa phương cụ thể yêu cầu tính thuế trên thuế.
- **Giữ quy tắc hoạt động/không hoạt động** — thay vì xóa các quy tắc thuế cho các thay đổi theo mùa hoặc tạm thời, hãy chuyển chúng sang chế độ không hoạt động và kích hoạt lại khi cần.
- **Kiểm tra trước khi đưa vào vận hành** — sau khi thiết lập các quy tắc thuế, đặt một đơn hàng kiểm tra từ các địa chỉ khác nhau để xác minh các loại thuế đúng được áp dụng.