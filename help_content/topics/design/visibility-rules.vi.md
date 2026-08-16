---
title: Quy tắc hiển thị
---

# Quy tắc hiển thị

Các quy tắc hiển thị cho phép bạn hiển thị hoặc ẩn một phần cửa hàng trực tuyến của bạn tùy thuộc vào ai đang truy cập và họ đến từ đâu. Bạn có thể khóa **các phần trang**, **các mục menu**, và **các tiện ích thanh đầu và chân trang** bằng cùng các điều kiện — thị trường hoặc khu vực của khách hàng, ngôn ngữ hoặc tiền tệ mà họ đang xem, thời gian trong ngày, hoặc các tín hiệu riêng biệt của người dùng như việc họ có đăng nhập hay không.

Mọi thứ đều được xây dựng từ **những nhóm quy tắc**: một gói có thể tái sử dụng, được đặt tên, bao gồm một hoặc nhiều điều kiện. Bạn tạo một nhóm quy tắc một lần (ví dụ: "thị trường New Zealand" hoặc "thành viên đã đăng nhập") và sau đó gắn nó với bất kỳ phần tử, mục menu hoặc tiện ích nào bạn muốn nó kiểm soát. Một mục không có nhóm quy tắc nào được gắn sẽ luôn hiển thị.

## Cách xác định tính khả dụng

Khi có nhiều hơn một nhóm quy tắc được gắn với một mục, mục đó sẽ được hiển thị nếu **bất kỳ** nhóm nào được gắn khớp (chúng kết hợp bằng OR). Trong một nhóm duy nhất, bạn chọn xem **tất cả** hay **bất kỳ** các điều kiện nào của nó phải khớp.

Các quy tắc thuộc hai gia đình, và Spwig xử lý chúng khác nhau để cửa hàng của bạn luôn nhanh và thân thiện với công cụ tìm kiếm:

- **Các quy tắc thị trường** — điều kiện dựa trên khu vực/thị trường, ngôn ngữ, tiền tệ và thời gian. Những điều này được quyết định trên máy chủ cho mỗi URL thị trường, do đó cùng một trang được giao đến mọi người dùng (và mọi công cụ tìm kiếm) tại địa chỉ đó. Điều này giữ cho các trang có thể lưu trữ được và an toàn cho SEO.
- **Các quy tắc dựa trên người dùng** — tình trạng đăng nhập, nội dung giỏ hàng, thiết bị và vị trí chính xác. Những điều này phụ thuộc vào người dùng cụ thể, do đó Spwig giải quyết chúng riêng tư cho mỗi người sau khi trang được tải. Chúng không bao giờ được nướng vào một trang được lưu trữ chung.

Nếu bạn vô hiệu hóa một nhóm quy tắc, nó sẽ đơn giản là ngừng áp dụng — mục mà nó được gắn sẽ trở lại hiển thị. Việc vô hiệu hóa một nhóm không phải là cách để ẩn thứ gì đó.

## Tạo và gắn quy tắc

Có hai cách để làm việc với các nhóm quy tắc.

### Gắn chúng ở nơi bạn thiết kế

Nơi nào bạn có thể khóa nội dung, bạn sẽ thấy một **kiểm soát khả dụng** (biểu tượng mắt):

- **Người xây dựng trang** — chọn một phần tử, mở thuộc tính của nó và sử dụng kiểm soát khả dụng.
- **Người xây dựng menu** — chọn một mục menu và mở **Tab Khả dụng**. Điều này hoạt động với **mọi** mục, bao gồm cả mục con (menu thả xuống) được lồng trong mục khác — một quy tắc trên một phần tử con chỉ ẩn riêng phần tử đó, giữ nguyên phần còn lại của menu.
- **Người xây dựng thanh đầu và chân trang** — chọn một tiện ích và mở phần **Nhóm quy tắc khả dụng** trong cài đặt của nó.

Các quy tắc dựa trên người dùng cụ thể — xem xét xem họ có đăng nhập hay không, nội dung giỏ hàng của họ, hoặc thiết bị của họ — được giải quyết cho mỗi người mua sắm mà không làm chậm cửa hàng của bạn hoặc ảnh hưởng đến công cụ tìm kiếm. Cửa hàng trực tuyến của bạn vẫn nhanh và có thể lưu trữ được, và mỗi người dùng vẫn chỉ thấy phần điều hướng dành cho họ.

Trong trình chỉnh sửa khả dụng, bạn có thể:

- **Gắn** bất kỳ nhóm quy tắc nào bạn đã có bằng cách đánh dấu chúng.
- **Quy tắc nhanh** — tạo một nhóm quy tắc đơn giản ngay tại chỗ (ví dụ: "chỉ thành viên", một thị trường duy nhất, một loại tiền tệ, một thiết bị hoặc giá trị giỏ hàng tối thiểu) và gắn chúng trong một bước.
- **Quản lý nhóm quy tắc** — chuyển đến trình xây dựng đầy đủ để tạo các quy tắc nâng cao.

Nhấn **Áp dụng** và mục đó sẽ được khóa ngay lập tức.

### Xây dựng quy tắc nâng cao

Đối với bất kỳ điều gì phức tạp hơn — kết hợp một số điều kiện, lồng nhóm hoặc các toán tử chi tiết — hãy đến **Thiết kế → Quy tắc Hiển thị** (nhóm quy tắc). Ở đó, bạn có thể xây dựng các quy tắc với logic AND/OR và tái sử dụng chúng trên toàn bộ cửa hàng của bạn.

## Các điều kiện phổ biến

| Condition | Use it to… |
|-----------|------------|
| **Khu vực / thị trường** | Hiển thị một khối chỉ dành cho những người truy cập đến từ một thị trường cụ thể (ví dụ: New Zealand) |
| **Tiền tệ đã chọn** | Hiển thị ghi chú giá hoặc ưu đãi chỉ khi một loại tiền tệ nhất định đang được sử dụng |
| **Ngôn ngữ đã chọn** | Hiển thị nội dung chỉ bằng ngôn ngữ nhất định |
| **Ngày / thời gian / thứ / giờ kinh doanh** | Hiển thị banner trong khoảng thời gian khuyến mãi hoặc chỉ trong giờ làm việc |
| **Trạng thái đã đăng nhập** | Hiển thị nội dung dành riêng cho thành viên, hoặc lời mời đăng ký cho khách vãng lai |
| **Loại thiết bị** | Hiển thị hoặc ẩn một thứ gì đó trên điện thoại di động, máy tính bảng hoặc máy tính để bàn |
| **Giá trị / số lượng giỏ hàng** | Hiển thị lời nhắc miễn phí vận chuyển khi giỏ hàng vượt qua một mức nhất định |

## Xem trước

Trong chế độ xem trước của Page Builder, bạn có thể **xem như một thị trường** và **xem như một người dùng** (đã đăng nhập hoặc là khách, với một giỏ hàng mẫu) để xem chính xác điều gì mà mỗi đối tượng người dùng sẽ thấy — bao gồm các quy tắc riêng tư mà thường thì chỉ có người dùng đó mới nhìn thấy được.

## Mẹo

- Xây dựng một tập hợp nhỏ các nhóm quy tắc được đặt tên rõ ràng ('Thị trường NZ', 'Thành viên', 'Chỉ dành cho điện thoại') và sử dụng chúng ở mọi nơi — dễ quản lý hơn so với các quy tắc riêng lẻ.
- Các quy tắc thị trường là lựa chọn an toàn cho bất kỳ điều gì bạn muốn được lập chỉ mục bởi các công cụ tìm kiếm, vì kết quả sẽ giống nhau cho mọi người ở một URL thị trường nhất định.
- Nếu một mục nào đó biến mất một cách bất ngờ, hãy kiểm tra các nhóm quy tắc được gắn với nó — một mục sẽ bị ẩn chỉ khi nó có một nhóm đang hoạt động và không có nhóm nào trong số các nhóm của nó phù hợp với người dùng hiện tại.