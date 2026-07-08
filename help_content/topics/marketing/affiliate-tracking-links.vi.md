---
title: Theo dõi đại lý & Liên kết
---

Theo dõi đại lý là yếu tố cốt lõi của toàn bộ hệ thống hoa hồng bằng cách kết nối các đơn hàng của khách hàng với các đại lý đã giới thiệu họ. Hướng dẫn này giải thích cách các liên kết theo dõi hoạt động, dữ liệu Spwig ghi lại khi khách hàng nhấp vào các liên kết đó, và cách hệ thống gán hoa hồng dựa trên cookie.

Hiểu rõ cơ chế theo dõi giúp bạn khắc phục các vấn đề gán hoa hồng, phân tích hiệu suất liên kết và hướng dẫn đại lý của bạn cách tối đa hóa tỷ lệ chuyển đổi của họ.

## Liên kết theo dõi là gì?

Một liên kết theo dõi là một URL duy nhất chuyển hướng khách hàng đến cửa hàng của bạn trong khi ghi lại danh tính của đại lý trong cookie. Mỗi đại lý có thể tạo nhiều liên kết theo dõi dẫn đến các đích khác nhau - trang chủ, sản phẩm cụ thể, trang bộ sưu tập hoặc trang đích.

Định dạng liên kết theo dõi ví dụ:
```
https://yourstore.com/affiliate/track/a2b7f8c4d1e9/
```

Liên kết này chuyển hướng đến đích trong khi thiết lập cookie theo dõi liên kết, liên kết đó sẽ gán các đơn hàng tương lai với đại lý sở hữu mã liên kết `a2b7f8c4d1e9`.

Các đại lý tạo ra các liên kết này từ bảng điều khiển của họ. Họ sao chép toàn bộ URL và chia sẻ nó trong các bài đăng blog, mạng xã hội, email hoặc bất kỳ kênh nào mà họ tiếp cận khách hàng tiềm năng.

## Các thành phần của liên kết theo dõi

Mỗi liên kết theo dõi chứa các thành phần sau:

| Thành phần | Ví dụ | Mô tả |
|-----------|---------|-------------|
| **URL cơ bản** | `https://yourstore.com` | Miền của cửa hàng bạn |
| **Đường dẫn theo dõi** | `/affiliate/track/` | Điểm cuối theo dõi của Spwig |
| **Mã liên kết** | `a2b7f8c4d1e9` | Mã duy nhất 12 ký tự được tạo tự động |
| **Đích** | Được thiết lập khi tạo liên kết | Nơi khách hàng đến sau khi chuyển hướng (trang chủ, sản phẩm, v.v.) |

Khi một đại lý tạo liên kết, Spwig tạo mã 12 ký tự duy nhất tự động. Đại lý không bao giờ cần tạo hoặc chỉnh sửa mã này - họ chỉ cần chọn đích và Spwig xử lý phần còn lại.

### Nhãn liên kết (Tùy chọn)

Các đại lý có thể thêm nhãn cho mỗi liên kết để tổ chức của họ:
- "Liên kết tiểu sử Instagram"
- "Mô tả YouTube"
- "Chiến dịch email Black Friday"

Các nhãn giúp đại lý theo dõi các kênh quảng bá nào hiệu quả nhất. Chúng chỉ hiển thị cho đại lý và bạn - khách hàng không bao giờ nhìn thấy nhãn.

## Cách theo dõi hoạt động

Quy trình theo dõi và gán hoa hồng bao gồm năm bước từ nhấp chuột đến hoa hồng:

### 1. Khách hàng nhấp vào liên kết

Một khách hàng tiềm năng nhấp vào liên kết theo dõi của đại lý từ bất kỳ kênh quảng bá nào (bài đăng mạng xã hội, bài viết blog, bản tin email).

### 2. Ghi lại nhấp chuột

Điểm cuối theo dõi của Spwig ghi lại chi tiết nhấp chuột:
- Địa chỉ IP
- User agent (trình duyệt và thiết bị)
- HTTP referrer (nơi nhấp chuột đến từ)
- Thời gian ghi lại
- Mã phiên

Dữ liệu này xuất hiện tại **Clicks** trong bảng quản trị tại **Affiliate > Clicks** để phân tích và phát hiện gian lận.

### 3. Thiết lập cookie

Hệ thống theo dõi thiết lập cookie trong trình duyệt của khách hàng trước khi chuyển hướng họ. Cookie chứa:
- ID đại lý (đại lý nào sẽ nhận được hoa hồng)
- ID chương trình (cấu trúc hoa hồng nào áp dụng)
- Mã liên kết (liên kết cụ thể nào đã được nhấp chuột)

### 4. Khách hàng mua hàng

Khách hàng duyệt cửa hàng của bạn và hoàn tất đơn hàng. Điều này có thể xảy ra ngay lập tức hoặc sau vài ngày/tuần, miễn là họ mua hàng trong khoảng thời gian cookie còn hiệu lực.

### 5. Tạo hoa hồng

Tại thanh toán, Spwig kiểm tra cookie đại lý. Nếu tìm thấy và vẫn còn hiệu lực (trong khoảng thời gian cookie), hệ thống tạo bản ghi hoa hồng với trạng thái **Pending** liên quan đến đại lý, chương trình và đơn hàng.

## Gán hoa hồng dựa trên cookie

Cookie theo dõi là cơ chế cốt lõi liên kết các đơn hàng với đại lý. Hiểu cách cookie hoạt động giúp bạn thiết lập khoảng thời gian gán hoa hồng tối ưu và khắc phục các vấn đề theo dõi.

### Cấu trúc cookie

| Thuộc tính | Giá trị |
|----------|-------|
| **Tên** | `aff_{program_id}` (ví dụ: `aff_7` cho ID chương trình 7) |
| **Giá trị** | JSON chứa ID đại lý, mã liên kết, thời gian ghi lại |
| **Miền** | Miền của cửa hàng bạn |
| **Đường dẫn** | `/` (truy cập toàn bộ trang web) |
| **Thời gian tồn tại** | Thời gian sống cookie của chương trình (1–365 ngày) |
| **HttpOnly** | `true` (ngăn chặn truy cập JavaScript để bảo mật) |
| **SameSite** | `Lax` (cho phép theo dõi từ các trang web bên ngoài) |
| **Secure** | `true` trên các trang web HTTPS (khuyến nghị) |

### Khoảng thời gian sống cookie

Khoảng thời gian sống cookie xác định thời gian khách hàng có thể mua hàng sau khi nhấp vào liên kết đại lý. Khoảng thời gian này được thiết lập theo chương trình tại **Marketing > Affiliate Programs** khi bạn tạo hoặc chỉnh sửa chương trình.

Khoảng thời gian sống cookie theo tiêu chuẩn ngành:
- **7 ngày**: Sản phẩm ra quyết định nhanh (thực phẩm, vé sự kiện)
- **30 ngày**: Thương mại điện tử tiêu chuẩn (cài đặt phổ biến nhất)
- **60–90 ngày**: Sản phẩm cần cân nhắc (nội thất, điện tử, sản phẩm B2B)
- **365 ngày**: Chu kỳ bán hàng dài (hàng xa xỉ, dịch vụ cao cấp)

Nếu khách hàng nhấp vào liên kết đại lý vào ngày 1 tháng 1 và khoảng thời gian sống cookie của bạn là 30 ngày, bất kỳ đơn hàng nào họ thực hiện đến ngày 30 tháng 1 sẽ được ghi nhận cho đại lý đó. Đơn hàng vào ngày 31 tháng 1 hoặc sau đó sẽ không tạo ra hoa hồng vì cookie đã hết hạn.

### Mô hình gán hoa hồng theo nhấp chuột cuối cùng

Spwig sử dụng mô hình **gán hoa hồng theo nhấp chuột cuối cùng**: đại lý có liên kết nhấp chuột cuối cùng sẽ nhận được hoa hồng. Dưới đây là cách hoạt động:

**Tình huống**: Một khách hàng nhấp vào liên kết đại lý A vào thứ Hai, sau đó nhấp vào liên kết đại lý B vào thứ Năm, và mua hàng vào thứ Sáu.

**Kết quả**: Đại lý B nhận được hoa hồng vì liên kết của họ là nhấp chuột cuối cùng.

Cookie nhấp chuột cuối cùng sẽ ghi đè lên cookie đại lý trước đó. Mô hình này dễ hiểu và ngăn chặn việc ghi nhận hoa hồng kép, mặc dù điều này có nghĩa là chỉ một đại lý nhận được tín dụng cho mỗi đơn hàng (đại lý cuối cùng trước khi mua hàng).

## Ghi lại nhấp chuột

Spwig ghi lại mọi nhấp chuột trên mọi liên kết đại lý để cung cấp phân tích cho cả bạn và đại lý. Dữ liệu nhấp chuột giúp đo lường hiệu suất liên kết, phát hiện gian lận và tối ưu hóa chiến lược quảng bá.

### Dữ liệu được ghi lại cho mỗi nhấp chuột

Truy cập **Affiliate > Clicks** để xem tất cả các nhấp chuột đã được ghi lại. Mỗi mục chứa:

| Trường | Mô tả |
|-------|-------------|
| **Liên kết** | Liên kết theo dõi nào đã được nhấp chuột |
| **Đại lý** | Người sở hữu liên kết |
| **Địa chỉ IP** | Địa chỉ IP của khách hàng (phát hiện gian lận) |
| **User Agent** | Thông tin trình duyệt và thiết bị |
| **Nguồn** | Trang web mà khách hàng nhấp vào liên kết (ví dụ: "https://instagram.com") |
| **Mã phiên** | Mã nhận dạng duy nhất cho phiên duyệt web này |
| **Thời gian ghi lại** | Ngày và giờ chính xác của nhấp chuột |

### Giới hạn tốc độ

Để ngăn chặn gian lận nhấp chuột và lạm dụng bot, Spwig giới hạn nhấp chuột ở **100 mỗi phút mỗi địa chỉ IP**. Nếu cùng một IP vượt quá ngưỡng này, các nhấp chuột bổ sung sẽ bị bỏ qua và không làm tăng đếm nhấp chuột.

Bảo vệ này ngăn chặn các hành vi xấu làm tăng số liệu nhấp chuột mà không chặn lưu lượng hợp lệ. Khách hàng thực tế hầu như không bao giờ vượt quá 100 nhấp chuột mỗi phút.

### Xét đến quyền riêng tư

Dữ liệu nhấp chuột chứa địa chỉ IP và user agent để phát hiện gian lận. Đảm bảo chính sách quyền riêng tư của bạn tiết lộ rằng bạn theo dõi các lần giới thiệu đại lý và chia sẻ dữ liệu hiệu suất đã được ẩn danh với các đại lý.

## Xem các liên kết đại lý

Tất cả các liên kết theo dõi do đại lý tạo ra sẽ xuất hiện trong bảng điều khiển quản trị của bạn để giám sát và quản lý.

### Truy cập danh sách liên kết

Truy cập **Affiliate > Links** để xem tất cả các liên kết theo dõi cho tất cả các đại lý và chương trình. Danh sách hiển thị:

- **Mã liên kết**: Nhận dạng duy nhất 12 ký tự
- **Đại lý**: Người tạo liên kết
- **Chương trình**: Cấu trúc hoa hồng nào áp dụng
- **Nhãn**: Mô tả tùy chọn do đại lý cung cấp
- **Đích**: Nơi liên kết chuyển hướng khách hàng
- **Tổng số nhấp chuột**: Số lượng nhấp chuột theo thời gian
- **Trạng thái hoạt động**: Liên kết hiện đang theo dõi hay không

### Lọc liên kết

Sử dụng bộ lọc quản trị để thu hẹp danh sách:
- **Theo đại lý**: Xem tất cả các liên kết cho một đối tác cụ thể
- **Theo chương trình**: Xem các liên kết quảng bá cấu trúc hoa hồng cụ thể
- **Theo trạng thái hoạt động**: Tìm các liên kết đã bị vô hiệu hóa

Việc lọc này giúp bạn phân tích sự phân bố liên kết trong mạng lưới đại lý của bạn và xác định các liên kết hiệu quả nhất.

## Thống kê liên kết

Mỗi liên kết theo dõi tích lũy các chỉ số hiệu suất giúp đại lý tối ưu hóa chiến lược quảng bá của họ và giúp bạn xác định các đối tác hiệu quả nhất.

### Nhấp vào bản ghi liên kết để xem thống kê chi tiết:

| Chỉ số | Mô tả | Tính toán |
|--------|-------------|-------------|
| **Tổng số nhấp chuột** | Tất cả các nhấp chuột được ghi lại kể từ khi tạo liên kết | Số lượng bản ghi nhấp chuột |
| **Nhấp chuột (7 ngày)** | Chỉ số hoạt động gần đây | Số nhấp chuột trong 7 ngày qua |
| **Chuyển đổi** | Số đơn hàng được gán cho liên kết này | Số lượng hoa hồng từ mã liên kết này |
| **Tỷ lệ chuyển đổi** | Phần trăm nhấp chuột dẫn đến mua hàng | (Chuyển đổi ÷ Tổng số nhấp chuột) × 100 |
| **Tổng doanh thu** | Tổng giá trị tất cả đơn hàng từ liên kết này | Tổng giá trị đơn hàng cho các nhấp chuột đã chuyển đổi |

### Sử dụng thống kê để tối ưu hóa

**Đối với đại lý**: Những con số này cho thấy kênh quảng bá nào hiệu quả nhất. Nếu một liên kết tiểu sử Instagram có tỷ lệ chuyển đổi 5% nhưng một liên kết bài viết blog có 15%, đại lý nên tập trung nhiều hơn vào nội dung blog.

**Đối với người bán hàng**: Thống kê liên kết tiết lộ đại lý nào mang lại lưu lượng chất lượng. Số nhấp chuột cao nhưng tỷ lệ chuyển đổi thấp cho thấy đối tượng khách hàng của đại lý không phù hợp với sản phẩm của bạn.

## Quản lý liên kết

Bạn có thể quản lý các liên kết đại lý từ bảng điều khiển quản trị để bảo trì và khắc phục sự cố.

### Vô hiệu hóa liên kết

Để ngăn một liên kết cụ thể theo dõi các nhấp chuột mới trong khi vẫn giữ lại dữ liệu lịch sử:

1. Truy cập **Affiliate > Links**
2. Nhấp vào liên kết bạn muốn vô hiệu hóa
3. Bỏ chọn **Active**
4. Nhấp **Save**

Các liên kết đã vô hiệu hóa vẫn chuyển hướng khách hàng đến đích, nhưng không thiết lập cookie theo dõi hoặc ghi lại các nhấp chuột. Điều này hữu ích khi đại lý đang chạy chiến dịch tạm thời hoặc bạn cần vô hiệu hóa một kênh quảng bá cụ thể.

### Chỉnh sửa chi tiết liên kết

Bạn có thể chỉnh sửa:
- **Nhãn**: Cập nhật mô tả do đại lý cung cấp
- **Đích**: Thay đổi nơi liên kết chuyển hướng (hữu ích nếu bạn di chuyển trang sản phẩm)
- **Trạng thái hoạt động**: Bật hoặc tắt theo dõi

Bạn không thể chỉnh sửa mã liên kết - nó vĩnh viễn và liên kết với tất cả dữ liệu nhấp chuột và hoa hồng lịch sử.

### Xóa các liên kết không hoạt động

Xóa các liên kết không còn được sử dụng và không có nhấp chuột hoặc chuyển đổi lịch sử. Điều này giữ danh sách liên kết của bạn sạch sẽ mà không làm mất dữ liệu phân tích quý giá.

**Cảnh báo**: Xóa liên kết sẽ xóa tất cả các bản ghi nhấp chuột liên quan. Chỉ xóa liên kết có số nhấp chuột bằng 0 hoặc khi bạn chắc chắn rằng bạn không cần dữ liệu lịch sử.

## Mô hình gán hoa hồng

Hiểu logic gán hoa hồng của Spwig giúp bạn thiết lập kỳ vọng với đại lý và khắc phục tranh chấp về hoa hồng.

### Gán hoa hồng theo nhấp chuột cuối cùng

Như đã đề cập trước đây, Spwig sử dụng mô hình gán hoa hồng theo nhấp chuột cuối cùng: nếu khách hàng nhấp vào nhiều liên kết đại lý trước khi mua hàng, chỉ đại lý có nhấp chuột cuối cùng mới nhận được hoa hồng.

**Ưu điểm**:
- Dễ hiểu và giải thích
- Ngăn chặn việc ghi nhận hoa hồng kép
- Ghi nhận đại lý đóng vai trò kết thúc giao dịch

**Nhược điểm**:
- Đại lý giới thiệu khách hàng không nhận được tín dụng
- Không phản ánh hành trình khách hàng đa chạm
- Có thể khuyến khích hành vi "hijacking liên kết" (đại lý nhắm đến khách hàng có ý định cao đã được giới thiệu bởi người khác)

### Thời gian sống cookie xác định tính đủ điều kiện

Chỉ các đơn hàng trong khoảng thời gian sống cookie mới tạo ra hoa hồng. Nếu cookie hết hạn trước khi thanh toán, không có hoa hồng nào được tạo ra, ngay cả khi khách hàng quay lại thông qua bookmark.

**Ví dụ**: Thời gian sống cookie 30 ngày
- Khách hàng nhấp vào liên kết ngày 1 tháng 1 → Cookie được thiết lập, hết hạn ngày 31 tháng 1
- Khách hàng mua hàng ngày 25 tháng 1 → Hoa hồng được tạo
- Khách hàng mua hàng ngày 5 tháng 2 → Không có hoa hồng (cookie đã hết hạn)

### Theo dõi phiên

Ngoài cookie, Spwig theo dõi mã phiên cho mỗi nhấp chuột. Điều này cho phép gán hoa hồng cho nhiều lần truy cập trong cùng một phiên, ngay cả khi cookie bị chặn hoặc xóa.

Nếu khách hàng nhấp vào liên kết, duyệt cửa hàng của bạn kích hoạt nhiều lần tải trang, và sau đó họ mua hàng - tất cả trong cùng một phiên - đại lý sẽ nhận được tín dụng ngay cả khi không có cookie bền vững.

## Khắc phục sự cố

Các vấn đề theo dõi phổ biến và cách khắc phục chúng:

### Liên kết không theo dõi nhấp chuột

**Triệu chứng**: Số nhấp chuột vẫn ở mức 0 mặc dù đại lý báo cáo đã chia sẻ liên kết.

**Nguyên nhân và cách khắc phục**:
1. **Liên kết bị vô hiệu hóa**: Kiểm tra trạng thái **Active** trong trang chi tiết liên kết
2. **Chương trình bị vô hiệu hóa**: Truy cập **Affiliate > Programs** và xác nhận trạng thái chương trình là **Active**
3. **Tài khoản đại lý bị vô hiệu hóa**: Kiểm tra trạng thái tài khoản đại lý tại **Affiliate > Affiliates**
4. **Giới hạn tốc độ**: Kiểm tra xem cùng một IP có tạo ra nhiều nhấp chuột quá mức (lưu lượng bot) không

### Tỷ lệ chuyển đổi thấp

**Triệu chứng**: Số nhấp chuột cao nhưng rất ít đơn hàng được gán.

**Nguyên nhân và cách khắc phục**:
1. **Thời gian sống cookie quá ngắn**: Tăng thời gian sống cookie của chương trình nếu sản phẩm của bạn yêu cầu nghiên cứu và cân nhắc
2. **Chất lượng trang đích**: Kiểm tra trang đích - có thân thiện với thiết bị di động không? Tải trang nhanh không? Sản phẩm có tồn kho không?
3. **MISMATCH đối tượng**: Đối tượng của đại lý có thể không phù hợp với sản phẩm của bạn
4. **Trình duyệt chặn cookie**: Một số công cụ bảo vệ quyền riêng tư chặn cookie bên thứ ba, mặc dù Spwig sử dụng cookie bên thứ nhất, ít có khả năng bị chặn hơn

### Bản ghi nhấp chuột trùng lặp

**Triệu chứng**: Cùng một khách hàng tạo ra nhiều bản ghi nhấp chuột liên tiếp.

**Nguyên nhân**: Điều này là hành vi bình thường. Mỗi lần tải trang của liên kết theo dõi tạo ra một bản ghi nhấp chuột. Nếu khách hàng nhấp vào, trang tải chậm và họ nhấp lại, bạn sẽ thấy nhiều bản ghi.

**Cách khắc phục**: Không cần hành động. Bộ giới hạn tốc độ ngăn chặn việc lạm dụng (100 nhấp chuột/phút/IP), và các nhấp chuột trùng lặp từ cùng một phiên không ảnh hưởng đến việc gán hoa hồng - chỉ một cookie được thiết lập.

## Một số mẹo

- **Kiểm tra theo dõi trước khi ra mắt** - Tạo một tài khoản đại lý thử nghiệm, tạo liên kết theo dõi, nhấp vào nó trong trình duyệt ẩn danh và hoàn tất một đơn hàng thử nghiệm. Xác nhận hoa hồng xuất hiện với gán đại lý đúng.
- **Giáo dục đại lý về thời gian sống cookie** - Đảm bảo đại lý hiểu rằng họ chỉ nhận được hoa hồng cho các đơn hàng trong khoảng thời gian cookie. Điều này giúp họ thiết lập kỳ vọng thực tế và tập trung vào lưu lượng có ý định cao.
- **Theo dõi mẫu nhấp chuột để phát hiện gian lận** - Số lượng nhấp chuột bất thường cao từ một IP duy nhất hoặc các nhấp chuột không có chuỗi user agent có thể chỉ ra lưu lượng bot. Kiểm tra kỹ các đại lý này trước khi phê duyệt hoa hồng.
- **Sử dụng nhãn liên kết một cách nhất quán** - Khuyến khích đại lý gắn nhãn liên kết theo kênh (Instagram, Blog, Email) để bạn có thể cùng nhau phân tích kênh quảng bá nào mang lại chuyển đổi tốt nhất.
- **Xem xét thời gian sống cookie dài hơn cho sản phẩm cao cấp** - Nếu giá trị đơn hàng trung bình của bạn cao và khách hàng thường nghiên cứu trước khi mua, hãy kéo dài thời gian sống cookie lên 60–90 ngày để thu thập các chuyển đổi bị chậm lại.
- **Kiểm tra dữ liệu nguồn để có cái nhìn về kênh** - Trường nguồn cho thấy nơi nhấp chuột đến từ. Nếu bạn thấy nhiều nhấp chuột từ "instagram.com" hoặc "youtube.com", bạn biết các đại lý của bạn đang sử dụng các nền tảng mạng xã hội nào hiệu quả nhất.