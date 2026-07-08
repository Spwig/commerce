---
title: Trình tạo SEO AI
---

Trình tạo SEO AI tự động viết tiêu đề meta, mô tả meta và nội dung SEO khác cho sản phẩm của bạn bằng cách sử dụng nhà cung cấp AI. Thay vì viết nội dung SEO cho từng sản phẩm một cách thủ công, bạn có thể tạo nội dung chính xác, tối ưu hóa theo lô với một hành động duy nhất.

Cửa hàng của bạn đi kèm với trình tạo SEO tích hợp hoạt động ngay lập tức. Bạn cũng có thể cài đặt các thành phần nhà cung cấp AI bổ sung từ thị trường thành phần Spwig để truy cập các mô hình ngôn ngữ mạnh mẽ hơn.

## Cách trình tạo SEO hoạt động

Trình tạo SEO đọc tên sản phẩm, mô tả, danh mục và các thuộc tính của sản phẩm, sau đó sử dụng nhà cung cấp AI được cấu hình để viết nội dung SEO phù hợp với sản phẩm đó. Nội dung được tạo sẽ được lưu trực tiếp vào các trường SEO của sản phẩm.

Bạn có thể tạo nội dung SEO cho các sản phẩm riêng lẻ từ trang chỉnh sửa sản phẩm, hoặc chạy tạo theo lô trên nhiều sản phẩm từ danh sách sản phẩm.

## Cấu hình nhà cung cấp SEO

### Sử dụng nhà cung cấp tích hợp

Cửa hàng của bạn bao gồm một nhà cung cấp SEO tích hợp tạo nội dung SEO một cách xác định từ dữ liệu sản phẩm của bạn — không cần khóa API bên ngoài. Nó được thiết lập tự động làm nhà cung cấp chính trên các cài đặt mới.

Để xác minh rằng nó đang hoạt động:

1. Di chuyển đến **Marketing > Nhà cung cấp SEO**
2. Kiểm tra xem nhà cung cấp tích hợp xuất hiện với nhãn **CHÍNH** và trạng thái **HOẠT ĐỘNG**
3. Nếu không có nhà cung cấp nào được liệt kê, hãy nhấp vào **+ Thêm tài khoản nhà cung cấp SEO** và đặt **Khóa nhà cung cấp** thành `deterministic`

### Kết nối thành phần nhà cung cấp AI

Để có nội dung SEO phong phú và có ngữ cảnh hơn, bạn có thể cài đặt một thành phần nhà cung cấp AI (ví dụ như nhà cung cấp dựa trên OpenAI hoặc Claude) từ thị trường thành phần Spwig.

1. Cài đặt thành phần nhà cung cấp thông qua hệ thống cập nhật thành phần (hỏi quản trị viên cửa hàng của bạn)
2. Di chuyển đến **Marketing > Nhà cung cấp SEO**
3. Nhấp vào **+ Thêm tài khoản nhà cung cấp SEO**
4. Điền vào biểu mẫu:

**Phần Thông tin nhà cung cấp:**
- **Trang** — chọn cửa hàng của bạn
- **Thành phần nhà cung cấp** — chọn thành phần nhà cung cấp AI đã cài đặt
- **Khóa nhà cung cấp** — để trống khi sử dụng thành phần nhà cung cấp
- **Tên tài khoản** — tên mô tả như `Nhà cung cấp SEO OpenAI`

**Phần Cấu hình:**
- **Hoạt động** — đánh dấu để kích hoạt nhà cung cấp này
- **Chính** — đánh dấu để sử dụng nhà cung cấp này làm nhà cung cấp mặc định cho tất cả việc tạo SEO
- **Ưu tiên** — các số nhỏ hơn sẽ được thử trước trong chuỗi dự phòng
- **Cài đặt** — cài đặt cụ thể cho nhà cung cấp dưới dạng đối tượng JSON (ví dụ: tên mô hình, giọng điệu, ngôn ngữ)

5. Nhấp vào **Lưu**

Chỉ có một nhà cung cấp có thể được đặt làm chính. Nếu bạn đánh dấu một nhà cung cấp mới làm chính, nhà cung cấp chính trước đó sẽ tự động bị hạ cấp.

### Chuỗi dự phòng nhà cung cấp

Nếu nhà cung cấp chính của bạn thất bại (ví dụ do sự cố API), cửa hàng của bạn sẽ tự động chuyển sang nhà cung cấp hoạt động tiếp theo theo thứ tự ưu tiên. Điều này đảm bảo việc tạo SEO vẫn hoạt động ngay cả khi một nhà cung cấp tạm thời không khả dụng.

## Tạo nội dung SEO cho một sản phẩm

### Sản phẩm riêng lẻ

1. Di chuyển đến **Sản phẩm > Sản phẩm** và mở bất kỳ sản phẩm nào
2. Cuộn xuống phần **SEO** của biểu mẫu sản phẩm
3. Nhấp vào nút **Tạo SEO**
4. Nhà cung cấp AI tạo tiêu đề meta và mô tả meta dựa trên chi tiết sản phẩm
5. Xem lại nội dung được tạo và chỉnh sửa nếu cần
6. Nhấp vào **Lưu** để áp dụng các thay đổi

### Tạo theo lô

Để tạo hoặc cập nhật nội dung SEO cho nhiều sản phẩm cùng lúc:

1. Di chuyển đến **Sản phẩm > Sản phẩm**
2. Chọn các sản phẩm bạn muốn cập nhật bằng cách sử dụng các ô kiểm, hoặc chọn tất cả
3. Mở danh sách thả xuống **Hành động**
4. Chọn **Tạo nội dung SEO** (hoặc tên hành động tương tự — kiểm tra danh sách thả xuống để có nhãn chính xác)
5. Nhấp vào **Tiến hành**

Spwig xếp hàng các nhiệm vụ tạo và xử lý chúng ở phía sau. Làm tươi danh sách sản phẩm sau một hoặc hai phút để xem các trường SEO đã được cập nhật.

## Xem xét phạm vi SEO

Trình tạo SEO theo dõi các sản phẩm đã có nội dung SEO. Để xác định các sản phẩm vẫn cần SEO:

1.

Di chuyển đến **Sản phẩm > Sản phẩm**
2.


Sử dụng bộ lọc **Trạng thái SEO** (nếu có sẵn) để hiển thị các sản phẩm thiếu tiêu đề meta hoặc mô tả
3.

Chọn những sản phẩm đó và thực hiện hành động tạo hàng loạt

## Cài đặt nhà cung cấp

Trường **Cài đặt** trên tài khoản nhà cung cấp SEO chấp nhận một đối tượng JSON với cấu hình cụ thể cho nhà cung cấp. Các tùy chọn phổ biến bao gồm:

```json
{
  "language": "en",
  "tone": "professional",
  "max_title_length": 60,
  "max_description_length": 160
}
```

Các cài đặt này thay đổi tùy theo thành phần nhà cung cấp. Vui lòng tham khảo tài liệu của nhà cung cấp để biết danh sách đầy đủ các tùy chọn có sẵn.

## Quản lý nhiều nhà cung cấp

Nếu bạn có nhiều hơn một tài khoản nhà cung cấp SEO được cấu hình, danh sách nhà cung cấp sẽ hiển thị trạng thái của chúng một cách tổng quát:

- **Biểu tượng PRIMARY** — nhà cung cấp này được sử dụng cho tất cả việc tạo nội dung SEO theo mặc định
- **Biểu tượng ACTIVE** — nhà cung cấp đang được bật
- **Biểu tượng INACTIVE** — nhà cung cấp đang bị tắt và sẽ không được sử dụng

Để thay đổi nhà cung cấp nào là nhà cung cấp chính, hãy mở tài khoản nhà cung cấp bạn muốn nâng cấp, đánh dấu hộp **Là nhà cung cấp chính**, và lưu lại. Hệ thống tự động đảm bảo chỉ có một nhà cung cấp duy nhất giữ cờ chính tại bất kỳ thời điểm nào.

## Một số mẹo

- Tạo nội dung SEO cho các sản phẩm mới ngay sau khi tạo chúng — chỉ mất vài giây và giúp các công cụ tìm kiếm có nội dung hữu ích để lập chỉ mục ngay lập tức
- Kiểm tra lại các mô tả meta do AI tạo ra trước khi xuất bản nếu sản phẩm của bạn có tên không bình thường hoặc kỹ thuật; trình tạo hoạt động tốt nhất với tên sản phẩm rõ ràng và mô tả
- Thiết lập "max_title_length": 60 và "max_description_length": 160 trong cài đặt nhà cung cấp để giữ nội dung được tạo trong giới hạn ký tự được Google khuyến nghị
- Thực hiện tạo SEO hàng loạt sau khi nhập một danh mục sản phẩm lớn để nhanh chóng điền đầy các trường SEO
- Nếu bạn cập nhật mô tả sản phẩm một cách đáng kể, hãy tạo lại nội dung SEO của nó để giữ cho các thẻ meta phù hợp với nội dung mới
- Nhà cung cấp xác định sẵn có thể là điểm bắt đầu tốt; nâng cấp lên thành phần được hỗ trợ bởi AI khi danh mục của bạn đã được thiết lập và bạn muốn nội dung SEO phong phú hơn, tự nhiên hơn