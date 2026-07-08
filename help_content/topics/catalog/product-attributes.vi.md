---
title: Thuộc tính Sản phẩm
---

Thuộc tính sản phẩm xác định các chiều mà sản phẩm có thể thay đổi — ví dụ như Kích cỡ, Màu sắc hoặc Chất liệu. Sau khi bạn đã tạo một thuộc tính và các giá trị có thể có, bạn có thể gán nó cho bất kỳ sản phẩm nào có thể thay đổi và Spwig sẽ tạo trình chọn biến thể mà khách hàng sử dụng khi thanh toán.

Truy cập **Catalog > Product Attributes** để quản lý các thuộc tính và giá trị của chúng.

## Cách thuộc tính hoạt động

Thuộc tính có thể được sử dụng lại trên toàn bộ danh mục của bạn. Bạn tạo chúng một lần và gán chúng cho bất kỳ sản phẩm nào cần thiết. Mỗi thuộc tính có:

- Một **tên** xác định nó (ví dụ: "Kích cỡ")
- Một **loại hiển thị** kiểm soát cách trình chọn hiển thị trên trang sản phẩm
- Một hoặc nhiều **giá trị** đại diện cho các tùy chọn có sẵn (ví dụ: "Nhỏ", "Trung", "Lớn")

Khi bạn gán một thuộc tính cho một sản phẩm, bạn cũng chỉ định các giá trị nào có sẵn cho sản phẩm cụ thể đó. Điều này có nghĩa là thuộc tính "Kích cỡ" có thể có các giá trị từ S đến 3XL, nhưng một chiếc áo cụ thể có thể chỉ cung cấp S, M và L.

## Loại hiển thị thuộc tính

Trường **Loại** trên thuộc tính kiểm soát cách trình chọn hiển thị trên trang sản phẩm cửa hàng của bạn:

| Loại | Hình thức hiển thị | Phù hợp nhất với |
|---|---|---|
| **Dropdown Select** | Một danh sách thả xuống mà khách hàng mở ra để chọn giá trị | Các thuộc tính có nhiều giá trị (ví dụ: một dãy kích cỡ với 10+ kích cỡ) |
| **Color Swatch** | Các hình tròn hoặc hình vuông có màu mà khách hàng nhấp vào | Các thuộc tính màu sắc nơi việc nhận biết trực quan giúp ích |
| **Button Group** | Các nút hình viên thuốc được hiển thị theo hàng | Các thuộc tính có số lượng giá trị nhỏ (ví dụ: S, M, L, XL) |
| **Radio Buttons** | Danh sách nút radio truyền thống | Bất kỳ thuộc tính nào mà bạn muốn hiển thị danh sách rõ ràng và dễ truy cập |

Chọn loại hiển thị phù hợp với cách khách hàng của bạn nghĩ về thuộc tính đó. Đối với màu sắc, các mẫu màu gần như luôn tốt hơn so với danh sách thả xuống. Đối với kích cỡ, các nhóm nút hoạt động tốt khi có ít hơn 8 tùy chọn.

## Tạo thuộc tính

1. Truy cập **Catalog > Product Attributes**
2. Nhấp **+ Add Product Attribute**
3. Nhập **Tên** (ví dụ: `Size`, `Colour`, `Material`)
4. **Slug** được điền tự động — bạn có thể để nguyên như vậy
5. Chọn **Loại** (Dropdown, Color Swatch, Button Group, hoặc Radio Buttons)
6. Chọn **Is Required** nếu khách hàng phải chọn thuộc tính này trước khi thêm sản phẩm vào giỏ hàng — điều này phù hợp với hầu hết các thuộc tính kích cỡ và màu sắc
7. Thiết lập **Sort Order** — các thuộc tính có số nhỏ hơn sẽ xuất hiện trước trong trình chọn biến thể trên trang sản phẩm
8. Thêm các giá trị thuộc tính trực tiếp trong phần **Values** (xem bên dưới)
9. Nhấp **Save**

## Thêm giá trị thuộc tính

Các giá trị thuộc tính là các tùy chọn riêng lẻ trong một thuộc tính. Bạn có thể thêm chúng trực tiếp khi tạo hoặc chỉnh sửa một thuộc tính, sử dụng biểu mẫu giá trị trực tiếp ở cuối trang chi tiết thuộc tính.

Đối với mỗi giá trị:

- **Value** — nhãn hiển thị (ví dụ: `Small`, `Red`, `Cotton`)
- **Slug** — được điền tự động từ giá trị; được sử dụng trong URL và định danh biến thể
- **Color Hex** — chỉ liên quan đến các thuộc tính loại **Color Swatch**. Nhập mã màu hex (ví dụ: `#FF0000` cho màu đỏ) để mẫu màu hiển thị đúng màu.
- **Sort Order** — kiểm soát thứ tự các giá trị hiển thị trong trình chọn. Gán các số nhỏ hơn cho các giá trị bạn muốn hiển thị trước.

### Sắp xếp giá trị một cách hợp lý

Đối với các thuộc tính kích cỡ, hãy thiết lập thứ tự sắp xếp sao cho kích cỡ tăng dần từ nhỏ đến lớn:

| Giá trị | Thứ tự sắp xếp |
|---|---|
| XS | 1 |
| S | 2 |
| M | 3 |
| L | 4 |
| XL | 5 |
| 2XL | 6 |

Đối với các thuộc tính màu sắc, bạn có thể sắp xếp theo thứ tự bảng chữ cái hoặc nhóm các màu sắc tương tự lại với nhau — bất kỳ cách nào phù hợp nhất với khách hàng của bạn.

## Quản lý giá trị thuộc tính riêng biệt

Bạn cũng có thể quản lý các giá trị thuộc tính độc lập tại **Catalog > Attribute Values**. Danh sách này hữu ích khi bạn cần tìm hoặc cập nhật một giá trị cụ thể trên toàn danh mục mà không cần mở từng thuộc tính riêng lẻ. Danh sách có thể được lọc theo tên thuộc tính.

## Gán thuộc tính cho sản phẩm

Các thuộc tính được gán ở cấp sản phẩm, không phải toàn cầu.

Để thêm thuộc tính cho sản phẩm:

1. Truy cập **Catalog > Products** và mở sản phẩm biến thể
2. Trong tab **Variations**, tìm phần **Attributes**
3. Chọn thuộc tính bạn muốn thêm
4. Chọn các giá trị của thuộc tính này có sẵn cho sản phẩm
5. Lưu sản phẩm — Spwig sẽ tạo các tổ hợp biến thể tương ứng

Để biết hướng dẫn chi tiết về cách thiết lập biến thể sản phẩm, xem chủ đề trợ giúp **Product Variants**.

## Practical examples

### Ví dụ: Thuộc tính kích cỡ quần áo

| Field | Value |
|---|---|
| Name | Size |
| Type | Button Group |
| Is Required | Yes |
| Sort Order | 1 |
| Values | XS (1), S (2), M (3), L (4), XL (5), 2XL (6) |

### Ví dụ: Thuộc tính mẫu màu sắc

| Field | Value |
|---|---|
| Name | Colour |
| Type | Color Swatch |
| Is Required | Yes |
| Sort Order | 2 |
| Values | Black (#000000), White (#FFFFFF), Navy (#001F5B), Red (#CC0000) |

### Ví dụ: Thuộc tính chất liệu

| Field | Value |
|---|---|
| Name | Material |
| Type | Dropdown Select |
| Is Required | No |
| Sort Order | 3 |
| Values | 100% Cotton, Cotton/Polyester Blend, Merino Wool, Linen |

## Tips

- Tạo các thuộc tính đại diện cho quyết định mua hàng thực tế mà khách hàng thực hiện — nếu khách hàng không cần chọn nó, có thể không cần thiết phải là thuộc tính
- Sử dụng tên gọi nhất quán trên toàn bộ danh mục của bạn: nếu một số sản phẩm sử dụng "Colour" và những sản phẩm khác sử dụng "Color", khách hàng và nhóm của bạn sẽ cảm thấy sự không nhất quán này gây bối rối
- Thứ tự sắp xếp cho cả thuộc tính và giá trị đều quan trọng — hãy đặt thuộc tính quan trọng nhất ở đầu (thường là Size hoặc Colour) và sắp xếp giá trị theo trình tự hợp lý
- Loại Color Swatch yêu cầu mã hex chính xác; hãy kiểm tra các màu trong trình chọn màu của trình duyệt trước khi lưu để đảm bảo mẫu màu khớp với màu thực tế của sản phẩm
- Nếu bạn cần đổi tên thuộc tính (ví dụ, từ "Color" sang "Colour"), hãy cập nhật trường **Name** thay vì tạo thuộc tính mới — việc thay đổi tên không ảnh hưởng đến các gán sản phẩm hiện có