---
title: Khu vực bán hàng
---

Khu vực bán hàng cho phép bạn xác định các thị trường địa lý cho cửa hàng của mình và kiểm soát sản phẩm nào có sẵn trong mỗi khu vực. Điều này rất hữu ích khi bạn bán hàng ở nhiều quốc gia hoặc khu vực khác nhau và cần có các danh mục sản phẩm, tiền tệ khu vực hoặc tình trạng tồn kho khác nhau theo từng địa điểm.

## Khu vực bán hàng là gì?

Một khu vực bán hàng là một khu vực địa lý có tên, bao gồm một hoặc nhiều quốc gia. Mỗi khu vực có một loại tiền tệ mặc định, một độ ưu tiên và có thể được liên kết với một hoặc nhiều kho hàng. Khi khách hàng duyệt cửa hàng của bạn, Spwig xác định khu vực của họ dựa trên vị trí và áp dụng các quy tắc tiền tệ và hiển thị sản phẩm phù hợp.

Một số trường hợp sử dụng phổ biến:
- Chỉ hiển thị các sản phẩm có sẵn tại mỗi quốc gia cho khách hàng ở đó
- Gán loại tiền tệ mặc định theo khu vực (ví dụ: NZD cho khách hàng New Zealand)
- Kiểm soát kho hàng nào sẽ xử lý đơn hàng cho từng khu vực
- Ẩn các sản phẩm chưa có sẵn tại một số thị trường nhất định

## Tạo khu vực bán hàng

1. Di chuyển đến **Catalog > Sales Regions**
2. Nhấp **+ Add Sales Region**
3. Điền thông tin khu vực:

| Field | Description | Example |
|-------|-------------|---------|
| **Region Name** | Tên hiển thị cho khu vực này | `Asia-Pacific` |
| **Region Code** | Mã định danh duy nhất ngắn gọn | `APAC` |
| **Countries** | Các mã quốc gia ISO được bao gồm trong khu vực này | `["NZ", "AU", "SG", "FJ"]` |
| **Default Currency** | Mã tiền tệ ISO cho khu vực này | `NZD` |
| **Priority** | Các khu vực có độ ưu tiên cao hơn sẽ được khớp trước | `10` |
| **Active** | Khu vực này có đang được sử dụng không | Checked |

4. Nhấp **Save**

### Mã quốc gia

Nhập các quốc gia dưới dạng danh sách JSON gồm các mã ISO hai chữ. Ví dụ:
- New Zealand và Australia: `["NZ", "AU"]`
- Singapore: `["SG"]`
- Toàn bộ châu Âu: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Độ ưu tiên

Nếu quốc gia của khách hàng khớp với nhiều hơn một khu vực, khu vực có số ưu tiên cao nhất sẽ được sử dụng. Đặt độ ưu tiên cao hơn cho các khu vực cụ thể hơn (ví dụ: đặt độ ưu tiên cho `NZ` là 20 và `APAC` là 10 để khách hàng New Zealand được khớp với khu vực `NZ` trước).

## Kiểm soát hiển thị sản phẩm theo khu vực

Mặc định, mọi sản phẩm đều hiển thị ở tất cả các khu vực. Để giới hạn sản phẩm cho các khu vực cụ thể, hãy sử dụng **Product Region Visibility**.

### Giới hạn sản phẩm cho các khu vực cụ thể

1. Di chuyển đến **Catalog > Product Region Visibility**
2. Nhấp **+ Add Product Region Visibility**
3. Chọn **Product**
4. Chọn **Region**
5. Thiết lập **Visible** thành bật hoặc tắt theo nhu cầu
6. Nhấp **Save**

Khi có bất kỳ bản ghi hiển thị nào cho sản phẩm, Spwig sẽ áp dụng các quy tắc. Các sản phẩm không có bản ghi hiển thị sẽ vẫn hiển thị ở mọi nơi.

### Mô hình phổ biến

**Giới hạn chỉ một khu vực duy nhất**

Thêm một bản ghi hiển thị cho mỗi khu vực bạn muốn hỗ trợ, thiết lập **Visible** thành `Yes` cho các khu vực được phép. Khách hàng ở các khu vực khác sẽ không nhìn thấy sản phẩm.

**Loại bỏ khỏi một khu vực**

Thêm một bản ghi hiển thị cho khu vực bạn muốn loại bỏ và thiết lập **Visible** thành `No`. Sản phẩm sẽ vẫn hiển thị ở tất cả các khu vực khác.

### Chỉnh sửa hiển thị từ trang sản phẩm

Bạn cũng có thể quản lý hiển thị theo khu vực trực tiếp từ biểu mẫu chỉnh sửa sản phẩm. Trên phần **Region Visibility** của sản phẩm, bạn sẽ tìm thấy một bảng hiển thị inline liệt kê tất cả các khu vực và cài đặt hiển thị cho sản phẩm đó.

## Tiền tệ theo khu vực

Mỗi khu vực có một loại tiền tệ mặc định. Khách hàng duyệt cửa hàng từ khu vực đó sẽ thấy giá được hiển thị bằng tiền tệ của khu vực. Loại tiền tệ được sử dụng được xác định tại bước thanh toán.

Để thiết lập giá ở nhiều loại tiền tệ, hãy cấu hình tỷ giá hối đoái dưới **Settings > Exchange Rates**. Giá có thể được chuyển đổi tự động hoặc thiết lập thủ công theo từng loại tiền tệ.

## Liên kết kho hàng với khu vực

Kho hàng được liên kết với khu vực khi bạn tạo hoặc chỉnh sửa kho hàng dưới **Catalog > Warehouses**. Mỗi kho hàng thuộc về một khu vực, điều này kiểm soát kho hàng nào sẽ được sử dụng để xử lý đơn hàng.

Để biết thêm chi tiết về kho hàng, vui lòng xem chủ đề trợ giúp **Inventory and Warehouses**.

## Tips

- Giữ mã vùng ngắn gọn và mô tả (`NZ`, `APAC`, `EU`, `US`) — chúng được sử dụng bên trong và trong nhật ký.
- Sử dụng số độ ưu tiên cao hơn cho các khu vực nhỏ và cụ thể hơn để chúng có quyền ưu tiên hơn các khu vực rộng và chung.
- Nếu bạn chỉ bán ở một quốc gia, bạn hoàn toàn không cần cấu hình các khu vực — Spwig hoạt động tốt với một danh mục toàn cầu duy nhất.
- Kiểm tra tính hiển thị theo khu vực bằng cách xem trước cửa hàng của bạn trong khi lọc theo một khu vực cụ thể trong phần quản trị.
- Các bản ghi hiển thị sản phẩm chỉ cần được tạo khi bạn muốn giới hạn sản phẩm. Để lại một sản phẩm không có bản ghi hiển thị sẽ làm cho nó có sẵn cho tất cả mọi người.
- Kiểm tra lại các quy tắc hiển thị của bạn mỗi khi bạn thêm một khu vực mới để đảm bảo các giới hạn sản phẩm hiện tại là chính xác.