---
title: Chia sẻ xã hội
---

Các nút chia sẻ xã hội cho phép khách hàng chia sẻ sản phẩm, bài đăng blog và các trang của bạn trực tiếp từ cửa hàng trực tuyến của bạn. Bạn kiểm soát các nền tảng nào được hiển thị, cách các nút trông như thế nào, vị trí đặt chúng và liệu hoạt động chia sẻ có được theo dõi và đếm hay không.

## Cấu hình cài đặt chia sẻ xã hội

Tất cả hành vi chia sẻ xã hội được kiểm soát từ một trang cài đặt duy nhất. Di chuyển đến **Marketing > Cài đặt Chia sẻ Xã hội** (trang sẽ tự động chuyển hướng đến biểu mẫu cài đặt — chỉ có một bản ghi cài đặt).

### Vị trí: nơi các nút xuất hiện

Phần **Vị trí** kiểm soát các loại nội dung nào sẽ hiển thị nút chia sẻ tự động.

| Cài đặt | Mô tả |
|---------|-------------|
| **Bật trên Sản phẩm** | Hiển thị nút chia sẻ trên các trang chi tiết sản phẩm |
| **Bật trên Danh mục** | Hiển thị nút chia sẻ trên các trang danh sách danh mục |
| **Bật trên Bài đăng Blog** | Hiển thị nút chia sẻ trên các trang bài đăng blog |
| **Bật trên Trang Tùy chỉnh** | Hiển thị nút chia sẻ trên các trang cửa hàng tùy chỉnh |

Chọn các loại nội dung bạn muốn hiển thị nút. Bạn có thể bật bất kỳ sự kết hợp nào — ví dụ, chỉ sản phẩm và bài đăng blog.

**Vị trí Nút** kiểm soát nơi trên trang các nút được hiển thị:

| Tùy chọn | Mô tả |
|--------|-------------|
| **Dưới Nội dung** (mặc định) | Hiển thị sau nội dung chính |
| **Trên Nội dung** | Hiển thị trước nội dung chính |
| **Thanh bên** | Hiển thị trong thanh bên của trang |
| **Lơ lửng (cố định)** | Dính vào bên cạnh khung nhìn khi người truy cập cuộn |

### Ngoại hình: cách các nút trông như thế nào

Phần **Ngoại hình** kiểm soát các nền tảng nào được hiển thị và cách các nút được thiết kế.

**Các nền tảng được bật** — để trống để hiển thị tất cả các nền tảng được hỗ trợ, hoặc nhập một mảng JSON để giới hạn các nền tảng được hiển thị:

```json
["facebook", "twitter", "pinterest", "whatsapp", "email"]
```

Các khóa nền tảng được hỗ trợ: `facebook`, `twitter`, `linkedin`, `pinterest`, `whatsapp`, `telegram`, `email`

**Phong cách Nút**:

| Phong cách | Mô tả |
|-------|-------------|
| **Chỉ biểu tượng** (mặc định) | Chỉ hiển thị biểu tượng nền tảng |
| **Biểu tượng + Nhãn** | Hiển thị biểu tượng và tên nền tảng |
| **Chỉ nhãn** | Chỉ hiển thị tên nền tảng dưới dạng văn bản |

**Kích thước Nút** — chọn **Nhỏ**, **Trung bình** (mặc định), hoặc **Lớn** để phù hợp với thiết kế cửa hàng trực tuyến của bạn.

**Hướng Bố cục** — sắp xếp các nút **Ngang** (mặc định, hiển thị song song) hoặc **Dọc** (xếp chồng lên nhau).

**Hiển thị Tiêu đề** — khi được chọn, một tiêu đề "Chia sẻ" sẽ xuất hiện trên nhóm nút.

**Hiển thị trên thiết bị di động** kiểm soát việc hiển thị nút trên màn hình nhỏ:

| Tùy chọn | Mô tả |
|--------|-------------|
| **Luôn hiển thị** (mặc định) | Nút hiển thị trên tất cả các thiết bị |
| **Ẩn trên thiết bị di động** | Nút ẩn trên thiết bị di động |
| **Chỉ trên thiết bị di động** | Nút chỉ hiển thị trên thiết bị di động |

### Cài đặt theo dõi

**Hiển thị Số lượng Chia sẻ** — khi được chọn, một nhãn số lượng sẽ xuất hiện trên mỗi nút, hiển thị số lần nền tảng đó đã được chia sẻ. Số lượng được cập nhật theo thời gian thực khi các chia sẻ được ghi lại.

**Theo dõi Chia sẻ** — khi được chọn, mỗi lần nhấp chia sẻ sẽ được ghi lại trong phân tích chia sẻ. Tắt tính năng này sẽ dừng việc lưu trữ các bản ghi mới nhưng không xóa dữ liệu hiện có. Việc theo dõi cũng trao tặng các biểu tượng trung thành cho khách hàng chia sẻ (nếu chương trình trung thành đang hoạt động).

Nhấp **Lưu** ở cuối biểu mẫu để áp dụng các thay đổi của bạn. Cài đặt có hiệu lực ngay lập tức.

## Xem hoạt động chia sẻ

### Các sự kiện chia sẻ cá nhân

Di chuyển đến **Marketing > Chia sẻ Xã hội** để xem nhật ký của mọi sự kiện chia sẻ được ghi lại. Mỗi mục hiển thị:

- **Nền tảng** — nền tảng mạng xã hội nào được sử dụng (hiển thị dưới dạng nhãn được tô màu)
- **Nội dung được chia sẻ** — loại và tên nội dung được chia sẻ (ví dụ, `product: Blue Widget`)
- **Người dùng** — khách hàng đã chia sẻ, hoặc "Ẩn danh" cho những người truy cập không đăng nhập
- **Loại thiết bị** — máy tính để bàn, di động hoặc máy tính bảng
- **Thời gian chia sẻ** — ngày và giờ chia sẻ

Bản ghi chia sẻ là chỉ đọc — các mục được tạo tự động khi khách hàng nhấp vào các nút chia sẻ.

Sử dụng bộ lọc **Platform** và **Device Type** để khám phá các mô hình chia sẻ, và phân cấp ngày để xem xét các khoảng thời gian cụ thể.

### Số lượng chia sẻ theo nội dung

Truy cập **Marketing > Share Counts** để xem tổng số chia sẻ được nhóm theo từng mục nội dung và nền tảng. Trang này giúp bạn dễ dàng xác định các sản phẩm và bài đăng được chia sẻ nhiều nhất.

Mỗi mục hiển thị:
- **Content** — loại và tên của mục (ví dụ: `product: Blue Widget`)
- **Platform** — mạng xã hội
- **Share Count** — tổng số lần chia sẻ được ghi nhận trên nền tảng đó
- **Last Updated** — thời điểm số lượng được tính lại lần cuối

Danh sách được sắp xếp theo số lượng chia sẻ giảm dần, do đó nội dung phổ biến nhất sẽ xuất hiện ở trên cùng. Số lượng chia sẻ được cập nhật tự động mỗi khi có sự kiện chia sẻ mới được ghi nhận — không cần phải làm tươi chúng thủ công.

## Hiểu cách theo dõi chia sẻ

Khi khách hàng nhấn vào nút chia sẻ, Spwig ghi lại:

1. Nền tảng họ đã chia sẻ
2. Nội dung được chia sẻ (sản phẩm, bài viết blog, trang, v.v.)
3. Họ có đăng nhập hay không (nếu có, lượt chia sẻ sẽ được liên kết với tài khoản của họ để tích hợp chương trình trung thành)
4. Loại thiết bị
5. URL được chia sẻ

Số lượng chia sẻ cho nền tảng và mục nội dung đó sẽ được tăng lên tự động. Nếu **Show Share Counts** được bật, số lượng đã cập nhật sẽ hiển thị trên nút khi trang được tải lại lần tiếp theo.

## Tích hợp chương trình trung thành

Nếu chương trình trung thành của bạn đang hoạt động và **Track Shares** được bật, khách hàng đã đăng nhập sẽ nhận được biểu tượng trung thành khi chia sẻ nội dung. Biểu tượng chia sẻ xã hội là một phần trong các quy tắc dựa trên hành động của chương trình trung thành.

Để cấu hình việc cấp điểm khi chia sẻ, truy cập **Customers > Loyalty Rules** và tìm các quy tắc có loại **Action-Based** và loại hành động **Social Share**.

## Một số mẹo

- Bật chia sẻ trên sản phẩm và bài viết blog trước — đây là các loại nội dung mà khách hàng có xu hướng chia sẻ một cách tự nhiên nhất
- Pinterest đặc biệt hữu ích cho các danh mục sản phẩm có tính thị giác như thời trang, nội thất và ẩm thực — hãy ưu tiên bật nó trong danh sách `enabled_platforms` cho các cửa hàng đó
- Việc chia sẻ qua WhatsApp thúc đẩy chuyển đổi mạnh từ các lời giới thiệu ấm, đặc biệt là trên thiết bị di động; hãy cân nhắc sử dụng chế độ hiển thị **Mobile Only** cho WhatsApp trong khi giữ các nền tảng khác hiển thị trên tất cả thiết bị
- Nếu bạn nhận thấy số lượng chia sẻ bị phình to, hãy kiểm tra xem lưu lượng thử nghiệm (từ phiên admin) có được tính trước khi cờ **Is Admin Traffic** hoạt động đầy đủ hay không — bạn có thể đặt lại số lượng bằng cách xóa các mục từ phân tích chia sẻ
- Kiểm tra danh sách Share Counts hàng tháng để xác định các sản phẩm được chia sẻ nhiều nhất và hiển thị chúng nổi bật hơn trên trang chủ hoặc trong các email marketing