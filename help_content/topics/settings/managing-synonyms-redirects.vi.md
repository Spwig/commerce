---
title: Quản lý Từ đồng nghĩa và Chuyển hướng
---

Từ đồng nghĩa và chuyển hướng giúp cải thiện khả năng tìm kiếm bằng cách xử lý các thuật ngữ tương đương và định tuyến các truy vấn cụ thể đến các trang mục tiêu. Từ đồng nghĩa mở rộng tìm kiếm để bao gồm các thuật ngữ liên quan ("laptop" cũng tìm thấy "notebook"), trong khi chuyển hướng gửi các truy vấn như "sale" trực tiếp đến trang bán hàng của bạn. Hướng dẫn này giải thích cách tạo và quản lý cả hai tính năng này để cải thiện tính liên quan của tìm kiếm và trải nghiệm khách hàng.

Sử dụng từ đồng nghĩa cho tính tương đương của thuật ngữ và chuyển hướng cho các đường tắt điều hướng.

![Danh sách từ đồng nghĩa](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## Hiểu về Từ đồng nghĩa

Từ đồng nghĩa cho hệ thống tìm kiếm biết rằng một số thuật ngữ nên được coi là tương đương. Khi khách hàng tìm kiếm một thuật ngữ, hệ thống tự động bao gồm các kết quả phù hợp với các thuật ngữ đồng nghĩa.

**Ví dụ**: Tạo bản ánh xạ từ đồng nghĩa "laptop" → "notebook", "portable computer". Bây giờ khi ai đó tìm kiếm "laptop", họ cũng sẽ nhận được kết quả cho các sản phẩm chứa "notebook" hoặc "portable computer" trong tên hoặc mô tả của chúng.

Từ đồng nghĩa đặc biệt hữu ích cho:
- Tiếng Anh Anh vs Tiếng Anh Mỹ (jumper/sweater, trainers/sneakers)
- Thuật ngữ thương hiệu vs thuật ngữ chung (tissues/Kleenex)
- Các lỗi chính tả phổ biến (accommodate/accomodate)
- Thuật ngữ ngành vs ngôn ngữ phổ thông (CPU/processor)

## Tạo Từ đồng nghĩa

Di chuyển đến **Tìm kiếm > Từ đồng nghĩa** và nhấp vào **+ Thêm Từ đồng nghĩa**.

![Biểu mẫu Thêm Từ đồng nghĩa](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Thuật ngữ** - Thuật ngữ tìm kiếm gốc kích hoạt mở rộng từ đồng nghĩa

**Từ đồng nghĩa** - Mảng JSON của các thuật ngữ tương đương, ví dụ: `['sweater', 'pullover', 'jumper']`

**Hai chiều** - Mặc định: Được chọn. Khi được bật, mối quan hệ từ đồng nghĩa hoạt động cả hai chiều:
- Tìm kiếm "laptop" tìm thấy sản phẩm "notebook"
- Tìm kiếm "notebook" tìm thấy sản phẩm "laptop"

Bỏ chọn để có bản ánh xạ một chiều (xem bên dưới).

**Ngôn ngữ** - Tùy chọn. Giới hạn từ đồng nghĩa này cho các tìm kiếm trong ngôn ngữ cụ thể. Để trống để áp dụng cho tất cả ngôn ngữ.

**Động cơ** - Tùy chọn. Giới hạn từ đồng nghĩa này cho một động cơ tìm kiếm cụ thể. Để trống để áp dụng toàn cục.

**Hoạt động** - Liệu từ đồng nghĩa này có đang được sử dụng hay không. Bỏ chọn để tạm thời vô hiệu hóa mà không xóa.

## Ví dụ Hai chiều

Hầu hết từ đồng nghĩa nên là hai chiều - các tương đương thực sự hoạt động theo cả hai hướng:

| Thuật ngữ | Từ đồng nghĩa | Trường hợp sử dụng |
|----------|----------------|---------------------|
| laptop | notebook, portable computer | Tiếng Anh Mỹ/Tiếng Anh Anh + thuật ngữ chung |
| sofa | couch, settee | Biến thể khu vực |
| trainers | sneakers, running shoes | Tiếng Anh UK/Tiếng Anh Mỹ |
| mobile | cell phone, cellular | Biến thể quốc tế |

Khi bật hai chiều, tất cả các thuật ngữ này sẽ tìm thấy cùng một sản phẩm bất kể khách hàng sử dụng thuật ngữ nào.

## Ví dụ Một chiều

Bỏ chọn "Hai chiều" cho các mối quan hệ một chiều:

**Các trường hợp sử dụng phổ biến**:
- **Lỗi chính tả**: Thuật ngữ: "acco
mmodate" → Từ đồng nghĩa: `['accommodate']` (một chiều nên tìm kiếm chính xác không tìm thấy lỗi chính tả)
- **Cụ thể → Chung**: Thuật ngữ: "MacBook" → Từ đồng nghĩa: `['laptop']` (MacBooks là laptop, nhưng không phải tất cả laptop đều là MacBook)
- **Viết tắt**: Thuật ngữ: "CPU" → Từ đồng nghĩa: `['processor']` (CPU tìm thấy sản phẩm processor, nhưng tìm kiếm processor không nên luôn bao gồm CPU)

## Từ đồng nghĩa theo ngôn ngữ

Sử dụng trường Ngôn ngữ để tạo các từ đồng nghĩa phù hợp với khu vực:

**Ví dụ**: Cửa hàng Tiếng Anh Anh
- Thuật ngữ: "jumper", Từ đồng nghĩa: `['sweater', 'pullover']`, Ngôn ngữ: English (UK)
- Thuật ngữ: "trainers", Từ đồng nghĩa: `['sneakers']`, Ngôn ngữ: English (UK)

**Ví dụ**: Cửa hàng đa ngôn ngữ
- Thuật ngữ: "ordinateur portable", Từ đồng nghĩa: `['laptop', 'notebook']`, Ngôn ngữ: French
- Thuật ngữ: "zapatos", Từ đồng nghĩa: `['shoes']`, Ngôn ngữ: Spanish

Từ đồng nghĩa theo ngôn ngữ chỉ áp dụng khi khách hàng đang duyệt bằng ngôn ngữ đó.

## Từ đồng nghĩa theo động cơ

Hầu hết từ đồng nghĩa nên áp dụng toàn cục (để trống trường Động cơ). Chỉ sử dụng từ đồng nghĩa theo động cơ khi các bối cảnh tìm kiếm khác nhau cần các ánh xạ thuật ngữ khác nhau:


**Ví dụ**: Bạn có các "shop" và "blog" riêng biệt
- Từ đồng nghĩa blog: Từ: "tutorial" → Đồng nghĩa: `['guide', 'how-to']`, Engine: blog
- Từ đồng nghĩa này chỉ áp dụng cho tìm kiếm blog, không phải tìm kiếm sản phẩm

## Hiểu về Redirects

Redirects tìm kiếm sẽ chuyển các truy vấn cụ thể trực tiếp đến các trang được chỉ định, bỏ qua kết quả tìm kiếm bình thường. Sử dụng redirect khi bạn biết rõ khách hàng nên đến đâu.

**Ví dụ**: Tạo redirect cho "sale" → "/products/sale/". Bây giờ khi ai đó tìm kiếm "sale", họ sẽ bỏ qua kết quả tìm kiếm và trực tiếp đến trang bán hàng của bạn.

Redirects lý tưởng cho:
- Các đường tắt điều hướng phổ biến ("returns" → trang chính sách hoàn trả)
- Các chương trình khuyến mãi theo mùa ("summer sale" → bộ sưu tập mùa hè)
- Các danh mục phổ biến ("laptops" → trang danh mục laptop)
- Các trang chính sách ("shipping" → thông tin vận chuyển)

![Danh sách Redirects](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## Loại Phù Hợp

Redirects hỗ trợ bốn loại phù hợp kiểm soát cách nghiêm ngặt truy vấn tìm kiếm phải khớp:

**Exact** - Khớp chính xác không phân biệt chữ hoa chữ thường. Truy vấn phải khớp chính xác với từ (bỏ qua chữ hoa). 
- Từ: "sale"
- Khớp: "sale", "SALE", "Sale"
- Không khớp: "summer sale", "on sale"

**Contains** - Truy vấn chứa từ ở bất kỳ đâu.
- Từ: "sizing"
- Khớp: "sizing guide", "help with sizing", "what sizing"
- Không khớp: "size chart" (từ khác)

**Starts With** - Truy vấn bắt đầu bằng từ.
- Từ: "return"
- Khớp: "returns", "return policy", "returning items"
- Không khớp: "how to return" (không bắt đầu bằng từ)

**Regex** - Phù hợp mẫu sử dụng biểu thức chính quy. **⚠️ Lưu ý hiệu suất** - các mẫu regex phức tạp làm chậm tìm kiếm. Sử dụng thận trọng.
- Mẫu: `^(laptop|notebook)s?$`
- Khớp: "laptop", "laptops", "notebook", "notebooks"
- Chỉ sử dụng nếu các loại phù hợp khác không hoạt động

## Tạo Redirects

Đi đến **Search > Redirects** và nhấn **+ Add Redirect**.

![Biểu mẫu Thêm Redirect](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Term** - Truy vấn tìm kiếm cần khớp

**Match Type** - Exact, Contains, Starts With, hoặc Regex (xem trên)

**Redirect URL** - Chuyển hướng khách hàng đến đâu. Có thể là tương đối (`/products/sale/`) hoặc tuyệt đối (`https://example.com/page/`)

**Redirect Type** - Mã trạng thái HTTP:
- **302 (Tạm thời)**: Được khuyến khích. Trình duyệt không lưu cache, bạn có thể thay đổi đích sau này
- **301 (Vĩnh viễn)**: Trình duyệt và công cụ tìm kiếm lưu cache. Chỉ sử dụng cho các redirect vĩnh viễn

**Engine** - Tùy chọn. Giới hạn cho engine tìm kiếm cụ thể

**Hit Count** - Tự tăng mỗi lần redirect này được sử dụng. Giúp xác định các đường tắt phổ biến.

**Active** - Bật/tắt redirect này

## Ví dụ Redirect

| Term | Match Type | URL | Use Case |
|------|-----------|-----|----------|
| sale | Exact | "/products/sale/" | Chuyển trực tiếp các truy vấn "sale" đến trang bán hàng |
| clearance | Exact | "/clearance/" | Bỏ qua tìm kiếm các mặt hàng giảm giá |
| sizing | Contains | "/pages/size-guide/" | Mọi truy vấn liên quan đến kích cỡ sẽ đến hướng dẫn |
| return | Starts With | "/pages/returns/" | Các truy vấn liên quan đến hoàn trả sẽ đến trang chính sách |

Tất cả sử dụng redirect 302 (tạm thời) để có tính linh hoạt.

## Loại Redirect: 302 vs 301

**302 (Tạm thời)** - Được khuyến khích cho hầu hết các redirect
- Trình duyệt thực hiện yêu cầu mới mỗi lần
- Bạn có thể thay đổi URL đích bất kỳ lúc nào
- Lựa chọn an toàn hơn nếu bạn không chắc chắn

**301 (Vĩnh viễn)** - Sử dụng thận trọng
- Trình duyệt lưu cache redirect
- Công cụ tìm kiếm cập nhật chỉ mục của họ
- Khó thay đổi sau này

**Khuyến nghị**: Sử dụng 302 trừ khi bạn hoàn toàn chắc chắn rằng redirect sẽ không bao giờ thay đổi.

## Phân tích Hit Count

Trường Hit Count tự tăng mỗi lần redirect được kích hoạt. Sử dụng để:
- Xác định các đường tắt điều hướng được sử dụng nhiều nhất
- Tìm các redirect không bao giờ được sử dụng (xem xét xóa)
- Phát hiện các mẫu tìm kiếm phổ biến

Xem xét hit counts hàng tháng để tối ưu chiến lược redirect của bạn.

## Tìm Cơ Hội Đồng Nghĩa


**Sử dụng các truy vấn không có kết quả**: Di chuyển đến **Tìm kiếm > Phân tích tìm kiếm** và lọc theo các truy vấn không có kết quả.

Những điều này tiết lộ:
- Các từ khóa khách hàng sử dụng không khớp với mô tả sản phẩm của bạn
- Các biến thể khu vực bạn chưa xem xét
- Các lỗi chính tả phổ biến

**Quy trình làm việc**:
1. Xem xét các truy vấn không có kết quả hàng tuần
2. Nhận diện các mô hình (các từ khóa xuất hiện lặp lại)
3. Thêm các từ đồng nghĩa để ánh xạ ngôn ngữ khách hàng với tên sản phẩm của bạn
4. Theo dõi xem số lượng truy vấn không có kết quả có giảm không

## Mẹo

- **Theo dõi các truy vấn không có kết quả hàng tuần để tìm ý tưởng từ đồng nghĩa** - Chúng tiết lộ khoảng cách giữa ngôn ngữ khách hàng và mô tả sản phẩm của bạn
- **Bắt đầu với các từ đồng nghĩa phổ biến, mở rộng dựa trên dữ liệu** - Bắt đầu với các biến thể khu vực rõ ràng, sau đó thêm dựa trên hành vi tìm kiếm thực tế
- **Sử dụng từ đồng nghĩa hai chiều để có sự tương đương thực sự** - Hầu hết các từ đồng nghĩa nên hoạt động cả hai chiều (laptop ↔ notebook)
- **Tránh các mẫu regex phức tạp** - Việc khớp regex chậm hơn các loại khớp khác; chỉ sử dụng khi thực sự cần thiết
- **Sử dụng 302 redirects (tạm thời) làm mặc định** - Cho phép bạn linh hoạt thay đổi đích sau này
- **Kiểm tra từ đồng nghĩa với các truy vấn thực tế** - Tìm kiếm các từ đồng nghĩa để xác minh chúng trả về kết quả mong muốn
- **Từ đồng nghĩa theo ngôn ngữ cho các cửa hàng đa ngôn ngữ** - Tạo ánh xạ các từ ngữ phù hợp với từng khu vực cho mỗi ngôn ngữ bạn hỗ trợ