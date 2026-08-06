---
title: Các khu vực bán hàng
---

Các khu vực bán hàng cho phép bạn xác định các thị trường địa lý cho cửa hàng của bạn và kiểm soát sản phẩm nào có sẵn ở mỗi khu vực. Điều này hữu ích khi bạn bán hàng ở nhiều quốc gia hoặc lãnh thổ khác nhau và cần các danh mục sản phẩm riêng biệt, tiền tệ khu vực, hoặc tình trạng tồn kho theo từng địa điểm.

## Khu vực bán hàng là gì?

Một khu vực bán hàng là một khu vực địa lý được đặt tên bao gồm một hoặc nhiều quốc gia. Mỗi khu vực có một tiền tệ mặc định, mức độ ưu tiên và có thể được liên kết với một hoặc nhiều kho hàng. Khi khách hàng duyệt cửa hàng của bạn, Spwig xác định khu vực của họ dựa trên vị trí của họ và áp dụng tiền tệ phù hợp và các quy tắc hiển thị sản phẩm.

Các trường hợp sử dụng phổ biến:
- Hiển thị sản phẩm chỉ có sẵn tại địa phương cho khách hàng ở mỗi quốc gia
- Gán tiền tệ mặc định riêng cho khu vực (ví dụ: NZD cho khách hàng New Zealand)
- Kiểm soát kho hàng nào giao hàng cho mỗi khu vực
- Ẩn các sản phẩm chưa có sẵn ở một số thị trường nhất định

## Tạo khu vực bán hàng

1. Truy cập **Kho hàng > Khu vực bán hàng**. Nếu bạn không thấy nó, hãy bật **Kích hoạt Kho hàng đa địa điểm** dưới **Cài đặt > Cài đặt Cửa hàng > Thương mại điện tử** để hiển thị mục menu — bạn không cần phải sử dụng thực sự nhiều kho hàng cho điều này, chỉ cần mở khóa liên kết. Bạn cũng có thể truy cập trực tiếp vào `/admin/catalog/salesregion/`.
2. Nhấn **+ Thêm Khu vực Bán hàng**
3. Điền thông tin khu vực:

| Trường | Mô tả | Ví dụ |
|-------|-------------|---------|
| **Tên Khu vực** | Tên hiển thị cho khu vực này | `Châu Á - Thái Bình Dương` |
| **Mã Khu vực** | Mã định danh duy nhất ngắn | `APAC` |
| **Quốc gia** | Các mã quốc gia ISO bao gồm trong khu vực này | `["NZ", "AU", "SG", "FJ"]` |
| **Tiền tệ Mặc định** | Mã tiền tệ ISO cho khu vực này | `NZD` |
| **Mức độ Ưu tiên** | Các khu vực có mức độ ưu tiên cao hơn sẽ được khớp trước | `10` |
| **Đang hoạt động** | Liệu khu vực này có đang được sử dụng không | Đã chọn |

4. Nhấn **Lưu**

### Mã quốc gia

Nhập các quốc gia dưới dạng danh sách JSON các mã hai chữ ISO. Ví dụ:
- New Zealand và Úc: `["NZ", "AU"]`
- Chỉ có Singapore: `["SG"]`
- Tất cả châu Âu: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Mức độ Ưu tiên

Nếu quốc gia của khách hàng khớp với nhiều hơn một khu vực, khu vực có số mức độ ưu tiên cao nhất sẽ được sử dụng. Đặt mức độ ưu tiên cao hơn cho các khu vực cụ thể hơn (ví dụ: gán cho `NZ` mức độ ưu tiên là 20 và `APAC` là 10 để khách hàng New Zealand được khớp với khu vực `NZ` trước).

## Kiểm soát tính khả dụng của sản phẩm theo khu vực

Mặc định, mọi sản phẩm đều có sẵn ở tất cả các khu vực. Để giới hạn sản phẩm, mở nó dưới **Sản phẩm > Tất cả Sản phẩm** và đặt trường **Tình trạng Khu vực** (trong phần Trạng thái) để cho phép sản phẩm chỉ ở các khu vực nhất định hoặc ở tất cả các khu vực ngoại trừ các khu vực nhất định, sau đó chọn các khu vực trong bảng dưới đây.

Điều này cũng xác định điều gì người mua ngoài khu vực có sẵn của sản phẩm thấy — liệu sản phẩm có bị ẩn khỏi danh sách hoàn toàn hay không, hoặc có thể hiện thị với thông báo "Không giao đến [khu vực]". Xem hướng dẫn **Tình trạng Khu vực** để biết hướng dẫn đầy đủ, bao gồm cài đặt hiển thị đó và Bộ chọn Giao hàng đến.

## Tiền tệ khu vực

Mỗi khu vực có một tiền tệ mặc định. Nếu cửa hàng của bạn hỗ trợ rõ ràng hơn một tiền tệ (**Cài đặt > Nhiều Tiền tệ**), tiền tệ được hiển thị của khách hàng sẽ chuyển sang tiền tệ mặc định của khu vực mỗi khi khu vực của họ thay đổi — có thể do trình hướng dẫn khu vực tự động hoặc Bộ chọn Giao hàng đến. Các cửa hàng chỉ có một tiền tệ, hoặc chưa chủ ý bật nhiều tiền tệ, luôn hiển thị tiền tệ duy nhất đó bất kể khu vực nào.

Để thiết lập giá theo nhiều tiền tệ, cấu hình tỷ giá hối đoái dưới **Cài đặt > Tỷ giá Hối đoái**. Giá có thể được chuyển đổi tự động hoặc được đặt thủ công theo từng tiền tệ.

## Liên kết kho hàng với khu vực

Kho hàng được liên kết với khu vực khi bạn tạo hoặc chỉnh sửa kho hàng dưới **Danh mục > Kho hàng**. Mỗi kho hàng thuộc về một khu vực, điều này kiểm soát hàng tồn kho của khu vực nào được sử dụng để giao hàng.

Giữ nguyên định dạng markdown, đường dẫn hình ảnh, khối mã, và các thuật ngữ kỹ thuật.

Để biết thêm chi tiết về kho hàng, xem chủ đề **Inventory and Warehouses** (Kho hàng và Kho lưu trữ) trong phần trợ giúp.

## Mẹo

- Giữ mã khu vực ngắn và mô tả (`NZ`, `APAC`, `EU`, `US`) — chúng được sử dụng bên trong và trong nhật ký.
- Sử dụng số thứ tự cao hơn cho các khu vực nhỏ và cụ thể hơn để chúng có ưu tiên hơn các khu vực tổng quát.
- Nếu bạn chỉ bán cho một quốc gia, bạn không cần phải cấu hình khu vực — Spwig hoạt động tốt với một danh mục toàn cầu duy nhất.
- Chỉ đặt **Tình trạng khu vực** của sản phẩm khác với **Có sẵn ở tất cả các khu vực** khi bạn thực sự cần giới hạn — mặc định sẽ giữ sản phẩm có sẵn ở mọi nơi mà không cần bảo trì.
- Kiểm tra lại các quy tắc khu vực của mỗi sản phẩm mỗi khi bạn thêm một **Khu vực bán hàng** mới, để đảm bảo các hạn chế vẫn phù hợp với mục đích của bạn.
- Thêm **Bộ chọn giao hàng đến** vào thanh đầu trang của bạn (xem hướng dẫn **Tình trạng khu vực**) để bạn có thể chuyển đổi khu vực và kiểm tra xem sản phẩm bị giới hạn có hoạt động đúng như mong đợi hay không.