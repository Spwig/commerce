---
title: Thẻ quà tặng đa tiền tệ
---

Nếu bạn bán hàng cho khách hàng ở nhiều quốc gia, bạn có thể phát hành thẻ quà tặng ở các loại tiền tệ cụ thể. Ví dụ, một khách hàng ở New Zealand có thể mua thẻ quà tặng 50 đô la New Zealand (NZD) và người nhận có thể quy đổi nó bằng tiền NZD — giá trị danh nghĩa vẫn giữ nguyên bất kể biến động tỷ giá hối đoái.

Tính năng này yêu cầu phải bật chế độ đa tiền tệ với ít nhất một nhà cung cấp tỷ giá đã được cấu hình.

## Cách hoạt động

Khi bạn thiết lập **Tiền tệ Thẻ Quà Tặng** cho một sản phẩm thẻ quà tặng, hệ thống sẽ chuyển đổi giá sản phẩm thành tiền tệ mục tiêu tại thời điểm mua hàng bằng tỷ giá hiện hành. Thẻ quà tặng được phát hành với giá trị bằng tiền tệ đó và chỉ có thể được quy đổi bởi khách hàng đang mua sắm bằng cùng loại tiền tệ.

| Bước | Điều gì xảy ra |
|------|-------------|
| **Thiết lập sản phẩm** | Bạn thiết lập giá sản phẩm thẻ quà tặng bằng tiền tệ cơ bản của bạn và chọn một tiền tệ mục tiêu (ví dụ: NZD) |
| **Mua hàng** | Một khách hàng mua thẻ quà tặng. Giá cơ bản được chuyển đổi thành NZD theo tỷ giá hiện hành |
| **Thẻ quà tặng được tạo** | Thẻ quà tặng được phát hành với giá trị bằng NZD (ví dụ: NZ$78.50) |
| **Quy đổi** | Người nhận áp dụng mã tại thanh toán khi đang mua sắm bằng NZD. Số dư NZD sẽ bị trừ |

## Yêu cầu trước

Trước khi thiết lập thẻ quà tặng đa tiền tệ, hãy đảm bảo bạn đã có:

1. **Đa tiền tệ được bật** — Truy cập **Settings > Store Settings** và bật hỗ trợ đa tiền tệ
2. **Tiền tệ được hỗ trợ được cấu hình** — Thêm các tiền tệ bạn muốn cung cấp (ví dụ: NZD, SGD, EUR)
3. **Nhà cung cấp tỷ giá được kết nối** — Truy cập **Settings > Exchange Rates** và cấu hình nhà cung cấp để tỷ giá trực tiếp có sẵn

## Thiết lập sản phẩm thẻ quà tặng đa tiền tệ

### Bước 1: Tạo hoặc chỉnh sửa sản phẩm thẻ quà tặng

1. Truy cập **Products > All Products**
2. Nhấp **+ Add Product** hoặc mở một sản phẩm thẻ quà tặng hiện có
3. Thiết lập **Product Type** thành **Gift Card**

### Bước 2: Thiết lập tiền tệ thẻ quà tặng

1. Nhấp vào tab **Gift Card**
2. Cấu hình cài đặt mệnh giá như thường lệ (mệnh giá cố định, mệnh giá tùy chỉnh, hoặc cả hai)
3. Ở cuối tab Gift Card, tìm dropdown **Gift Card Currency**
4. Chọn tiền tệ mục tiêu (ví dụ: **NZD - New Zealand Dollar**)
5. Lưu sản phẩm

Dropdown hiển thị tất cả các tiền tệ đã được bật trong cài đặt cửa hàng của bạn. Việc chọn **Store base currency (default)** có nghĩa là thẻ quà tặng sẽ được phát hành bằng tiền tệ cơ bản của bạn — đây là hành vi mặc định.

### Bước 3: Thiết lập giá cả

Thiết lập giá sản phẩm bằng tiền tệ cơ bản của bạn như bình thường. Khi khách hàng mua thẻ quà tặng này, giá sẽ tự động được chuyển đổi thành tiền tệ mục tiêu bằng tỷ giá hiện hành.

**Ví dụ:** Tiền tệ cơ bản của bạn là USD. Bạn tạo một sản phẩm thẻ quà tặng có giá 50 USD với **Gift Card Currency** được thiết lập thành NZD. Nếu tỷ giá là 1 USD = 1.57 NZD, thẻ quà tặng kết quả sẽ có giá trị là NZ$78.50.

## Phù hợp tiền tệ và quy đổi

Thẻ quà tặng đa tiền tệ sử dụng **quy đổi cùng tiền tệ** — tiền tệ mua sắm đang hoạt động của khách hàng phải khớp với tiền tệ của thẻ quà tặng.

### Trải nghiệm của khách hàng

- Một khách hàng đang mua sắm bằng **NZD** có thể áp dụng thẻ quà tặng NZD tại thanh toán
- Một khách hàng đang mua sắm bằng **USD** không thể áp dụng thẻ quà tặng NZD — họ sẽ thấy một thông báo giải thích sự không khớp tiền tệ
- Khách hàng có thể chuyển đổi tiền tệ mua sắm của họ bằng trình chọn tiền tệ trên cửa hàng của bạn trước khi áp dụng thẻ quà tặng

### Cách hoạt động của số dư

Số dư thẻ quà tặng luôn được theo dõi bằng tiền tệ gốc của nó:

- Một thẻ quà tặng NZ$78.50 bắt đầu với số dư NZ$78.50
- Nếu một khách hàng thực hiện mua sắm trị giá NZ$30, số dư còn lại là NZ$48.50
- Số dư không thay đổi theo tỷ giá — giá trị danh nghĩa là cố định

Khi thẻ quà tặng được áp dụng tại thanh toán, hệ thống sẽ chuyển đổi khoản giảm giá thành tiền tệ cơ bản của bạn nội bộ để tính toán đơn hàng, nhưng số dư thẻ quà tặng luôn được khấu trừ bằng tiền tệ gốc của nó.

## Quản lý thẻ quà tặng đa tiền tệ

Truy cập **Products > Gift Cards** để xem tất cả các thẻ quà tặng đã được phát hành. Các thẻ quà tặng đa tiền tệ được hiển thị với tiền tệ gốc của chúng:

- **Số dư** hiển thị bằng tiền tệ của thẻ quà tặng (ví dụ: NZ$48.50)
- **Giao dịch** ghi lại các khoản tiền bằng tiền tệ của thẻ quà tặng
- **Giá trị ban đầu** hiển thị số tiền đã chuyển đổi tại thời điểm mua hàng

### Kiểm tra chi tiết tỷ giá

Mỗi giao dịch thẻ quà tặng ghi lại tỷ giá được sử dụng tại thời điểm giao dịch. Điều này cung cấp một hồ sơ kiểm toán đầy đủ cho mục đích kế toán.

## Ví dụ

### Ví dụ 1: Thẻ quà tặng dành cho khu vực New Zealand

**Tình huống:** Bạn hoạt động từ Mỹ nhưng có khách hàng ở New Zealand. Bạn muốn bán thẻ quà tặng được tính bằng NZD.

| Thiết lập | Giá trị |
|---------|-------|
| Tên sản phẩm | NZ Gift Card |
| Loại sản phẩm | Thẻ quà tặng |
| Giá | $50.00 (USD — tiền tệ cơ bản của bạn) |
| Loại mệnh giá | Mệnh giá cố định |
| Mệnh giá cố định | 25, 50, 100, 200 |
| Tiền tệ Thẻ Quà Tặng | NZD - New Zealand Dollar |
| Hạn sử dụng | 365 ngày |

Khi khách hàng chọn mệnh giá $50:
- Hệ thống chuyển đổi $50 USD thành NZD theo tỷ giá hiện hành
- Một thẻ quà tặng được tạo với giá trị tương đương NZD (ví dụ: NZ$78.50)
- Người nhận có thể quy đổi nó khi đang mua sắm bằng NZD

### Ví dụ 2: Thẻ quà tặng nhiều tiền tệ

**Tình huống:** Bạn bán hàng cho khách hàng ở Singapore, Úc và Vương quốc Anh. Tạo ba sản phẩm thẻ quà tặng:

1. **SG Gift Card** — Tiền tệ Thẻ Quà Tặng: SGD
2. **AU Gift Card** — Tiền tệ Thẻ Quà Tặng: AUD
3. **UK Gift Card** — Tiền tệ Thẻ Quà Tặng: GBP

Mỗi sản phẩm chuyển đổi giá tiền tệ cơ bản của bạn thành tiền tệ mục tiêu tại thời điểm mua hàng. Khách hàng ở mỗi khu vực có thể quy đổi thẻ quà tặng bằng tiền tệ địa phương của họ.

### Ví dụ 3: Cung cấp thẻ quà tặng hỗn hợp

**Tình huống:** Bạn muốn cung cấp cả thẻ quà tặng bằng tiền tệ cơ bản và thẻ quà tặng theo khu vực.

- **Store Gift Card** — Tiền tệ Thẻ Quà Tặng: *Tiền tệ cơ bản của cửa hàng (mặc định)* — có thể quy đổi bằng tiền tệ cơ bản của bạn
- **NZ Gift Card** — Tiền tệ Thẻ Quà Tặng: NZD — chỉ có thể quy đổi bằng NZD

Cả hai sản phẩm có thể đồng tồn tại trong danh mục của bạn. Khách hàng sẽ thấy tiền tệ mà thẻ quà tặng được tính khi kiểm tra số dư.

## Một số mẹo

- Bắt đầu với một loại tiền tệ khu vực và kiểm tra toàn bộ quy trình (mua hàng, giao hàng, quy đổi) trước khi thêm nhiều tiền tệ hơn.
- Tỷ giá tại thời điểm mua hàng xác định giá trị thẻ quà tặng. Nếu tỷ giá thay đổi đáng kể, giá trị thẻ quà tặng vẫn giữ nguyên — điều này bảo vệ cả bạn và khách hàng.
- Làm rõ tiền tệ trong tên sản phẩm (ví dụ: "NZ Gift Card" hoặc "Gift Card (NZD)") để khách hàng biết họ đang mua gì.
- Các thẻ quà tặng không có tiền tệ được thiết lập sẽ tiếp tục hoạt động chính xác như trước đây bằng tiền tệ cơ bản của bạn — các sản phẩm hiện có không bị ảnh hưởng.
- Theo dõi nhà cung cấp tỷ giá của bạn để đảm bảo tỷ giá luôn cập nhật. Tỷ giá lỗi thời có thể dẫn đến thẻ quà tặng được định giá quá cao hoặc quá thấp.
- Hãy cân nhắc kỹ các mệnh giá của bạn. Một mệnh giá 25 USD sẽ chuyển đổi thành khoảng NZ$39 — các mệnh giá tròn trong tiền tệ mục tiêu có thể trông đẹp hơn. Bạn có thể tạo các sản phẩm riêng biệt với các mệnh giá là số tròn trong tiền tệ mục tiêu.