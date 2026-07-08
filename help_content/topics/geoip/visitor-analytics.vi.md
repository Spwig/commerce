---
title: Phân tích người truy cập
---

Phân tích người truy cập cung cấp cho bạn cái nhìn rõ ràng về cách khách hàng di chuyển qua cửa hàng của bạn. Bạn có thể thấy được trang nào thu hút nhiều lượt truy cập nhất, xu hướng lưu lượng truy cập tổng thể theo thời gian, thiết bị mà khách hàng của bạn sử dụng, và cách so sánh giữa người truy cập mới và người quay lại — tất cả mà không cần bất kỳ công cụ phân tích bên ngoài nào.

## Tổng quan về các màn hình phân tích

Cửa hàng của bạn sẽ theo dõi hoạt động người truy cập tự động một khi hệ thống GeoIP được kích hoạt. Dữ liệu được tổ chức thành ba cách xem, mỗi cách xem cung cấp cho bạn một cấp độ chi tiết khác nhau.

### Tổng览 lưu lượng hàng ngày

Truy cập vào **Khách hàng > Thống kê lưu lượng hàng ngày** để xem lưu lượng tổng thể của cửa hàng bạn cho mỗi ngày. Mỗi hàng đại diện cho một ngày dương lịch và hiển thị:

| Cột | Nó cho bạn biết điều gì |
|-----|----------------------|
| **Ngày** | Ngày lưu lượng được ghi nhận |
| **Tổng lượt xem** | Tất cả các lượt xem trang, bao gồm cả bot |
| **Người truy cập duy nhất** | Người truy cập khác nhau (theo phiên) |
| **Lượt xem từ bot** | Lượt xem từ các công cụ bò và tự động |
| **Người truy cập mới** | Các phiên không có lịch sử trước đó |
| **Người truy cập quay lại** | Các phiên từ người truy cập đã từng thấy trước đây |
| **Lượt xem máy tính để bàn** | Lượt xem từ trình duyệt máy tính để bàn |
| **Lượt xem di động** | Lượt xem từ thiết bị di động |
| **Lượt xem máy tính bảng** | Lượt xem từ thiết bị máy tính bảng |

Sử dụng thanh điều hướng phân cấp ngày ở đầu danh sách để nhanh chóng nhảy đến một tháng hoặc năm cụ thể. Tổng số được cập nhật mỗi ngày thông qua một quy trình nền tự động, vì vậy các con số cho ngày hiện tại sẽ xuất hiện vào sáng hôm sau.

### Thống kê theo trang

Truy cập vào **Khách hàng > Thống kê trang hàng ngày** để xem lưu lượng được phân chia theo từng trang cụ thể. Mỗi hàng hiển thị một đường dẫn URL trên một ngày, vì vậy bạn có thể so sánh hiệu suất của các trang cụ thể theo thời gian.

| Cột | Nó cho bạn biết điều gì |
|-----|----------------------|
| **Ngày** | Ngày mà các thống kê này áp dụng |
| **Đường dẫn URL** | Đường dẫn trang được chuẩn hóa (ví dụ: `/products/blue-widget`) |
| **Lượt xem** | Tổng số lượt xem cho trang đó trong ngày đó |
| **Người truy cập duy nhất** | Người truy cập khác nhau đã xem trang đó |
| **Lượt xem từ bot** | Lượt xem từ bot trên trang đó |
| **Lượt truy cập** | Số lượng phiên bắt đầu từ trang này (nó là trang đích của họ) |

Sử dụng hộp tìm kiếm **Đường dẫn URL** để tìm thống kê cho một trang cụ thể. Ví dụ, tìm kiếm `/products/` để xem tất cả lưu lượng trang sản phẩm, hoặc tìm kiếm một slug sản phẩm cụ thể để tập trung vào một mặt hàng.

### Sự kiện xem trang cá nhân

Truy cập vào **Khách hàng > Xem trang** để có nhật ký thô của mọi lần điều hướng trang được theo dõi. Đây là bản ghi chỉ đọc — bạn không thể thêm hoặc chỉnh sửa các mục. Sử dụng nó để điều tra các phiên cụ thể hoặc xác minh rằng việc theo dõi đang được ghi lại đúng cách.

Mỗi bản ghi hiển thị:
- **Đường dẫn URL** — trang đã được truy cập
- **Phiên** — một mã nhận diện ngắn cho phiên của người truy cập
- **Nguồn** — liệu lần truy cập có đến từ frontend không đầu hay từ cửa hàng tiêu chuẩn
- **Là bot** — liệu người truy cập có được xác định là lưu lượng tự động
- **Là trang đích** — liệu đây có phải là trang đầu tiên trong phiên của họ
- **Thời gian** — thời gian chính xác của lần truy cập

Bạn có thể lọc theo **Là bot**, **Nguồn**, và **Là trang đích** bằng cách sử dụng thanh bộ lọc bên cạnh, và điều hướng theo ngày bằng cách sử dụng thanh phân cấp ngày ở đầu.

## Đọc xu hướng lưu lượng

Tổng览 lưu lượng hàng ngày là công cụ tốt nhất của bạn để phát hiện xu hướng. Tìm kiếm các mô hình như:

- **Sự gia tăng lưu lượng** sau khi chạy một chương trình khuyến mãi hoặc gửi email marketing
- **Tăng trưởng dần** trong vài tuần và vài tháng khi cửa hàng của bạn tăng cường độ phủ sóng tự nhiên
- **Mô hình cuối tuần so với ngày làm việc** để hiểu khi khách hàng của bạn hoạt động nhiều nhất
- **Phân chia di động so với máy tính để bàn** để quyết định xem có nên ưu tiên thay đổi thiết kế tối ưu cho di động không

Các cột **Người truy cập mới** và **Người truy cập quay lại** cùng nhau cho bạn biết bạn đang giữ chân khách hàng tốt đến đâu. Một cửa hàng khỏe mạnh thường thấy sự kết hợp của cả hai — tỷ lệ người truy cập mới cao cho thấy việc thu hút khách hàng mạnh, trong khi tỷ lệ người quay lại cao hơn cho thấy lòng trung thành của khách hàng đang được xây dựng.

Trang xem thống kê theo trang, được sắp xếp theo lượt xem theo thứ tự giảm dần (mặc định), sẽ hiển thị ngay lập tức những trang nào tạo ra lượng truy cập lớn nhất trong ngày cụ thể.

Tìm kiếm:

- **Trang có nhiều lượt truy cập nhưng ít lượt xem** — những trang thu hút người truy cập từ công cụ tìm kiếm hoặc quảng cáo nhưng có thể không giữ chân người dùng
- **Trang có nhiều lượt xem và nhiều lượt truy cập duy nhất** — những trang phổ biến đáng để duy trì nội dung mới
- **Trang sản phẩm có xu hướng tăng lượt xem** — sản phẩm có thể đang tăng khả năng hiển thị trên công cụ tìm kiếm

### Ví dụ: Tìm lượng truy cập của một sản phẩm

Để kiểm tra lượng truy cập mà sản phẩm bán chạy nhất của bạn đã nhận được trong tuần trước:

1. Di chuyển đến **Customers > Daily Page Stats**
2. Sử dụng phân cấp ngày để chọn tuần phù hợp
3. Trong hộp tìm kiếm, nhập slug URL của sản phẩm (ví dụ: `/blue-widget`)
4. Xem **Views**, **Unique Visitors**, và **Entries** trong các ngày được hiển thị

## Dữ liệu vị trí người truy cập

Di chuyển đến **Customers > Visitor Locations** để xem một góc nhìn ở cấp độ phiên truy cập về nơi mà người truy cập của bạn đang ở. Mỗi bản ghi đại diện cho một phiên truy cập và bao gồm:

- Quốc gia và thành phố (được xác định tự động bởi hệ thống GeoIP)
- Loại thiết bị (máy tính để bàn, điện thoại di động, máy tính bảng)
- Tiền tệ và ngôn ngữ mà người truy cập đã chọn
- Thuộc tính chiến dịch UTM (nguồn, phương tiện, tên chiến dịch)
- Cờ hiệu cho lưu lượng bot và truy cập quản trị

Bạn có thể lọc người truy cập theo quốc gia, loại thiết bị, nguồn UTM, và xem họ có phải là bot hoặc nhân viên quản trị hay không. Sử dụng bộ lọc **Is Bot** đặt thành false để tập trung vào lưu lượng truy cập khách hàng thực sự, và bộ lọc **Is Admin Traffic** để loại bỏ các phiên kiểm tra của bạn khỏi phân tích.

## Một số mẹo

- Các lượt xem của bot được theo dõi riêng biệt và tự động bị loại khỏi số lượng người truy cập duy nhất — các con số lưu lượng truy cập của bạn phản ánh hoạt động thực sự của khách hàng
- Cột **Entries** trong thống kê theo trang cho bạn biết những trang nào đóng vai trò như cửa trước của cửa hàng từ công cụ tìm kiếm và quảng cáo; tối ưu hóa các trang này sẽ tạo tác động lớn nhất
- Lọc vị trí người truy cập theo **UTM Source** để đo lường lượng truy cập mà một kênh marketing cụ thể (ví dụ: một bản tin email hoặc quảng cáo Google) đang thực sự gửi đến
- Thống kê hàng ngày được tổng hợp vào ban đêm — nếu bạn cần kiểm tra lưu lượng cùng ngày, hãy sử dụng trực tiếp nhật ký Trang xem
- Phân tích thiết bị trong tóm tắt hàng ngày giúp bạn xác định ưu tiên cho công việc thiết kế; nếu hơn một nửa lượt truy cập của bạn là từ thiết bị di động, hãy đảm bảo các trang sản phẩm và quy trình thanh toán của bạn trông tuyệt vời trên màn hình nhỏ