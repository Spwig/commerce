---
title: Di chuyển từ Shopify
---

Nếu cửa hàng của bạn hiện đang chạy trên Shopify, công cụ di chuyển của Spwig có thể nhập sản phẩm, khách hàng, đơn hàng và nội dung của bạn bằng cách kết nối với một ứng dụng tùy chỉnh nhỏ mà bạn tạo trong bảng điều khiển Shopify Partners. Nền tảng Shopify có nhiều hạn chế hơn so với hầu hết, vì vậy phần lớn hướng dẫn này tập trung vào việc tạo ứng dụng đó một cách chính xác — việc kết nối chính chỉ là bước 5 phút sau khi ứng dụng được tạo.

## Trước khi bắt đầu

Hai giới hạn cụ thể của Shopify đủ quan trọng để cần được đề cập ở đây, không chỉ là trong bảng dưới đây:

> **Lưu ý quan trọng:** Shopify không có API đánh giá, vì vậy **không có đánh giá khách hàng nào được di chuyển**, bất kể bạn cấp những phạm vi ứng dụng nào. Nếu bạn cần đánh giá của mình, hãy xuất chúng riêng từ ứng dụng đánh giá bạn đang sử dụng (Judge.me, Yotpo, Loox, v.v.) và nhập chúng vào Spwig bằng tay.

> **Lưu ý quan trọng:** Mặc định, Spwig chỉ có thể đọc **đơn hàng trong 60 ngày gần nhất**. Để chuyển toàn bộ lịch sử đơn hàng của bạn, bạn phải thêm phạm vi `read_all_orders` khi tạo ứng dụng của mình — xem danh sách phạm vi bên dưới. Điều này rất dễ bị bỏ sót vì ứng dụng vẫn có thể kết nối và nhập thành công mà không có nó; nó chỉ lặng lẽ giới hạn mức độ xa bạn có thể quay lại trong lịch sử đơn hàng.

Tất cả các thứ khác đều chuyển đổi tốt: các danh mục (dưới dạng Bộ sưu tập — xem bên dưới), sản phẩm, hình ảnh, biến thể, khách hàng và địa chỉ, phiếu giảm giá, và nội dung blog. Các trường tùy chỉnh là khoảng trống đáng chú ý khác — xem **Metafields của Shopify** gần cuối hướng dẫn này.

Hãy nhớ thêm:

- Các tùy chọn **Import tax settings** và **Import shipping zones and methods** của wizard không được áp dụng cho dữ liệu đã nhập. Bạn cần tự thiết lập thuế và vận chuyển trong Spwig sau đó — xem [Sau khi di chuyển](after-migration-review).
- Tùy chọn **Price adjustment** trên cùng một bước *thực sự* có hiệu lực cho việc nhập từ Shopify, thay đổi giá cơ bản của mỗi sản phẩm khi nó được tạo. Hãy để nó ở chế độ **None** trừ khi bạn cố ý muốn thay đổi tất cả giá.
- Bạn sẽ cần quyền truy cập vào tài khoản Shopify Partners để tạo ứng dụng. Nếu bạn chưa có tài khoản, Shopify cho phép bạn tạo một tài khoản miễn phí tại partners.shopify.com.

## Tạo ứng dụng Shopify

Spwig kết nối với Shopify thông qua một ứng dụng tùy chỉnh mà bạn tạo và cài đặt trên cửa hàng của riêng bạn. Điều này tương tự như modal **Shopify API Setup Guide** trong sản phẩm (mở bằng **Open Setup Guide** ở bước 2 của wizard), vì vậy các bước dưới đây khớp hoàn toàn với những gì bạn sẽ thấy ở đó — bạn có thể theo dõi bất kỳ hướng dẫn nào.

### Bước 1: Tạo ứng dụng

1. Truy cập [bảng điều khiển phát triển Shopify Partners](https://dev.shopify.com/dashboard) của bạn và mở **Apps**
2. Nhấp **Create app**
3. Chọn **Start from Dev Dashboard**
4. Nhập tên ứng dụng: `Spwig Migration`
5. Nhấp **Create**

![Tạo ứng dụng Spwig Migration trong bảng điều khiển phát triển Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### Bước 2: Thiết lập URL ứng dụng và phạm vi

Trên trang cấu hình của ứng dụng mới, dưới **Versions**, hãy thiết lập:

- **App URL**: `https://shopify.dev/apps/default-app-home`
- **Scopes**: `read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![Thiết lập URL ứng dụng và phạm vi cần thiết](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| Phạm vi | Cho phép Spwig truy cập |
|---|---|
| `read_products` | Sản phẩm, biến thể, hình ảnh, bộ sưu tập |
| `read_customers` | Tên khách hàng, email, địa chỉ |
| `read_orders` | Đơn hàng trong 60 ngày gần nhất |
| `read_content` | Bài viết blog và trang |
| `read_discounts` | Mã giảm giá và quy tắc |
| `read_files` | Các tệp phương tiện đã tải lên |

> **Lưu ý:** Bạn muốn có toàn bộ lịch sử đơn hàng thay vì chỉ trong 60 ngày gần nhất? Thêm `read_all_orders` vào danh sách phạm vi trên.

### Bước 3: Sao chép Client ID và Secret của bạn

Đi đến **Settings > Credentials** và sao chép **Client ID** và **Secret** được hiển thị ở đó — bạn sẽ dán chúng vào wizard Spwig trong vài giây tới.

![Sao chép Client ID và Secret từ trang Cài đặt của ứng dụng](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### Bước 4: Tạo liên kết phân phối tùy chỉnh

1.

Đi đến **Phân phối** và chọn **Phân phối tùy chỉnh**
2.

Nhập tên miền cửa hàng của bạn (ví dụ, `yourstore.myshopify.com`)
3.

Nhấp vào **Tạo liên kết**, sau đó **Sao chép** liên kết cài đặt được tạo ra

![Sao chép liên kết cài đặt phân phối tùy chỉnh được tạo](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### Bước 5: Cài đặt ứng dụng trên cửa hàng của bạn

Mở liên kết cài đặt bạn vừa sao chép trong trình duyệt của bạn (đảm bảo bạn đã đăng nhập vào trang quản trị Shopify của mình), xem xét các quyền mà nó yêu cầu, và nhấp vào **Cài đặt**.

![Cài đặt ứng dụng trên cửa hàng Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **Lưu ý quan trọng:** Bước cuối cùng này dễ bị bỏ sót. Việc tạo liên kết cài đặt không cài đặt ứng dụng — bạn phải thực sự mở liên kết và nhấp vào Cài đặt, nếu không Spwig sẽ không thể kết nối. Nếu kiểm tra kết nối thất bại trong phần tiếp theo, đây là điều đầu tiên bạn cần kiểm tra.

## Sao chép Thông tin Đăng nhập vào Spwig

Trong trang quản trị Spwig, đi đến **Nhập và Xuất Dữ liệu > Bắt đầu Di chuyển Mới**, chọn **Shopify** ở bước 1, và ở bước 2 nhập:

- **Tên miền Cửa hàng** — `yourstore.myshopify.com`
- **Client ID** — từ **Cài đặt > Thông tin Đăng nhập**
- **Client Secret** — từ **Cài đặt > Thông tin Đăng nhập**

Nếu bạn muốn theo dõi hướng dẫn trong sản phẩm thay vì hướng dẫn này, nhấp vào **Mở Hướng dẫn Thiết lập** ở bước này — nó bao gồm cùng năm bước như trên với cùng các hình ảnh chụp màn hình, và mất khoảng 10 phút để hoàn thành từ đầu đến cuối.

Giữ tùy chọn **Kiểm tra kết nối trước khi tiếp tục** được chọn. Nếu `read_products`, `read_customers` hoặc `read_orders` bị thiếu khỏi phạm vi của ứng dụng, Spwig sẽ cảnh báo bạn trước khi bạn tiếp tục — quay lại trang **Phiên bản** của ứng dụng trong bảng điều khiển Shopify, thêm phạm vi bị thiếu, lưu phiên bản mới và thử lại.

## Xem xét và Chọn Dữ liệu

Bước 3 sẽ trích xuất các con số sống từ cửa hàng của bạn và hiển thị một mẫu của năm sản phẩm đầu tiên. Một vài thứ trông khác so với các nền tảng khác:

- **Bộ sưu tập, không phải danh mục** — Shopify tổ chức sản phẩm thành Bộ sưu tập thay vì danh mục, và Bộ sưu tập không hỗ trợ lồng ghép, vì vậy cấu trúc phân cấp sẽ được nhập theo cách phẳng. Nếu cửa hàng Shopify của bạn đã sử dụng bộ sưu tập để đại diện cho cây danh mục, hãy lên kế hoạch xây dựng lại cấu trúc đó trong trình quản lý danh mục của Spwig sau khi nhập.
- **Giảm giá, không phải phiếu giảm giá** — Mã giảm giá và quy tắc giảm giá của Shopify được nhập dưới dạng giảm giá của Spwig.
- **Không có hàng Đánh giá** — vì Shopify không có API đánh giá, loại dữ liệu này không xuất hiện trên bước này chút nào, khác với WooCommerce hoặc nhập từ tệp CSV.

**Tùy chọn Nhập** hoạt động giống như trên các nền tảng khác: **Bỏ qua các mục hiện có** (bật) khớp theo SKU và email để tránh trùng lặp; **Nhập hình ảnh sản phẩm** (bật) chậm hơn nhưng được khuyến nghị; **Giữ nguyên ID ban đầu nếu có thể** (tắt) nên giữ nguyên trừ khi bạn có lý do cụ thể để thay đổi; **Kích thước lô** mặc định là 25.

## Metafields của Shopify

Nếu bạn sử dụng metafields của Shopify để lưu trữ dữ liệu bổ sung trên sản phẩm, khách hàng hoặc đơn hàng, hãy lưu ý rằng Spwig không phát hiện hoặc đọc chúng — khác với WooCommerce, không có bước ánh xạ trường tùy chỉnh cho việc nhập Shopify. Bất kỳ dữ liệu nào bạn đã lưu trữ trong metafields sẽ cần được nhập lại thủ công trong Spwig bằng [trường tùy chỉnh](migration-field-mapping) sau khi di chuyển, vì vậy đáng để xuất danh sách metafields và giá trị của bạn từ Shopify trước khi bắt đầu.

## Chạy Quá trình Nhập

Sau khi bạn đã xem xét bước 3, hãy bắt đầu quá trình nhập. Nó chạy ở chế độ nền — bạn có thể đóng cửa sổ trình duyệt và nó vẫn tiếp tục. Bước 5 hiển thị tiến trình trực tiếp với một hàng cho mỗi loại dữ liệu và nhật ký hoạt động có thể mở rộng.

Bước 6 hiển thị kết quả của bạn: những gì đã được nhập, bỏ qua hoặc thất bại, cùng với công cụ **Chuyển đổi Liên kết** nếu các liên kết nội bộ đến tên miền cũ `myshopify.com` của bạn được tìm thấy trong nội dung đã nhập.

Kiểm tra kỹ tóm tắt, sau đó làm theo danh sách kiểm tra trong [Sau khi Di chuyển](after-migration-review) — nó bao gồm việc xác minh dữ liệu của bạn, xây dựng lại bất kỳ cấu trúc bộ sưu tập nào, thiết lập thuế và vận chuyển (điều mà chương trình hướng dẫn không cấu hình cho bạn), và nhập lại bất kỳ thứ gì đã được lưu trữ trong các trường meta.

## Xóa ứng dụng khỏi Shopify

Sau khi bạn đã xác nhận việc di chuyển hoàn tất thành công, quay lại trang **Apps** trong Shopify admin của bạn, hoặc bảng điều khiển Partners, và xóa ứng dụng Di chuyển Spwig (hoặc ít nhất là gỡ cài đặt nó khỏi cửa hàng của bạn). Không có lý do gì để giữ quyền truy cập đọc dữ liệu cửa hàng của bạn hoạt động sau khi di chuyển đã hoàn tất.

## Mẹo

- **Lịch sử đơn hàng mặc định bị giới hạn** — nếu bạn cần nhiều hơn 60 ngày đơn hàng gần đây, hãy thêm `read_all_orders` vào danh sách phạm vi trước khi tạo liên kết cài đặt của bạn, chứ không phải sau.
- **Đánh giá cần xuất riêng** — hãy lập kế hoạch cho điều này trước khi di chuyển, vì không có cách nào để chuyển đánh giá qua chương trình hướng dẫn.
- **Tạo liên kết không giống với việc cài đặt ứng dụng** — luôn hoàn thành Bước 5 và nhấp vào Cài đặt, nếu không kiểm tra kết nối trong Spwig sẽ thất bại.
- **Bộ sưu tập đến dưới dạng phẳng** — nếu cấu trúc danh mục của bạn quan trọng cho điều hướng hoặc SEO, hãy dành thời gian để xây dựng lại cấu trúc phân cấp trong Spwig sau khi nhập.
- **Xuất các trường meta trước** — Spwig không thể đọc chúng, vì vậy hãy thu thập dữ liệu đó từ Shopify trước khi bắt đầu nếu bạn cần nó sau này.
- **Xóa ứng dụng sau khi đã xác nhận** — đừng để tích hợp đang hoạt động chỉ đến cửa hàng cũ của bạn sau khi bạn đã chuyển sang.