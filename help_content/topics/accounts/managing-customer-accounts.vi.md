---
title: Quản lý Tài khoản Khách hàng
---

Tài khoản khách hàng cho phép các nhà bán hàng theo dõi thông tin khách hàng, lịch sử đặt hàng và sở thích. Di chuyển đến **Customers > All Customers** trong thanh bên trái của trang quản trị để quản lý tài khoản khách hàng.

![Add Customer](/static/core/admin/img/help/managing-customer-accounts/add-customer.webp)

## Hiểu về Tài khoản Khách hàng và Hồ sơ Khách hàng

**Tài khoản Khách hàng** là thông tin đăng nhập (email/mật khẩu) được lưu trữ trong mô hình Người dùng. **Hồ sơ Khách hàng** lưu trữ thông tin bổ sung như số điện thoại, ngày sinh, sở thích và phân tích. Mỗi tài khoản khách hàng đều có một hồ sơ tương ứng lưu trữ dữ liệu mở rộng này.

Khi bạn quản lý khách hàng trong trang quản trị, bạn đang làm việc với Hồ sơ Khách hàng liên kết với tài khoản Người dùng phía sau.

## Xem Tất cả Khách hàng

Danh sách khách hàng hiển thị tất cả khách hàng đã đăng ký cùng với các chỉ số chính:

| Cột | Mô tả |
|--------|-------------|
| **Người dùng** | Tên khách hàng và địa chỉ email |
| **Trạng thái Đại lý** | Khách hàng có phải là đối tác đại lý hay không |
| **Giá trị Khách hàng** | Tổng số tiền khách hàng đã chi (màu sắc được đánh dấu) |
| **Phân khúc Khách hàng** | Phân khúc RFM (Champion, Loyal, At Risk, v.v.) |
| **Tổng số đơn hàng** | Số lượng đơn hàng đã hoàn thành |
| **Số ngày kể từ đơn hàng cuối cùng** | Độ mới của lần mua gần nhất |
| **Khách hàng VIP** | Biểu tượng nếu khách hàng được đánh dấu là VIP |

### Lọc Khách hàng

Sử dụng thanh lọc bên trái để thu hẹp danh sách:

- **Trạng thái Đại lý** — Là Đại lý, Không phải Đại lý, Đại lý Đang chờ, Hoạt động, Tạm dừng, Bị từ chối
- **Bố cục Trang chủ** — Bố cục trang chủ ưa thích của khách hàng
- **Đăng ký Bản tin** — Khách hàng có đăng ký nhận bản tin hay không
- **Email Quảng cáo** — Khách hàng có đăng ký nhận email quảng cáo hay không
- **Tạo ngày** — Lọc theo ngày đăng ký

### Tìm kiếm Khách hàng

Sử dụng thanh tìm kiếm để tìm khách hàng theo:
- Tên người dùng
- Địa chỉ email
- Tên đầu
- Tên cuối
- Số điện thoại

## Xem Chi tiết Khách hàng

Nhấp vào tên khách hàng để xem hồ sơ đầy đủ của họ. Trang chi tiết khách hàng hiển thị:

![Customer Detail](/static/core/admin/img/help/managing-customer-accounts/customer-detail.webp)

### Phần Thông tin Khách hàng

Thông tin liên lạc cơ bản và trạng thái tài khoản:
- **Người dùng** — Liên kết đến tài khoản Người dùng cơ bản
- **Điện thoại** — Số điện thoại của khách hàng
- **Ngày sinh** — Để xác minh độ tuổi và chiến dịch sinh nhật

### Ưa chuộng Trang chủ

Cách khách hàng đã tùy chỉnh trang dashboard tài khoản của họ:
- **Bố cục Trang chủ** — Lưới, danh sách hoặc bố cục gọn
- **Hiển thị Lịch sử Đơn hàng** — Lịch sử đơn hàng xuất hiện trên trang dashboard hay không
- **Hiển thị Danh sách Yêu thích** — Danh sách yêu thích xuất hiện trên trang dashboard hay không
- **Hiển thị Sản phẩm Mới** — Sản phẩm đã xem gần đây xuất hiện hay không
- **Hiển thị Gợi ý** — Gợi ý sản phẩm xuất hiện hay không

### Ưa chuộng Giao tiếp

Trạng thái đăng ký của khách hàng cho các hình thức giao tiếp khác nhau:
- **Đăng ký Bản tin** — Đăng ký nhận bản tin chung
- **Email Quảng cáo** — Đăng ký nhận email quảng cáo
- **Thông báo Đơn hàng** — Đăng ký nhận cập nhật trạng thái đơn hàng

### Phân tích Khách hàng

Tóm tắt chỉ đọc về hành vi và giá trị của khách hàng:
- **Tóm tắt Phân tích Khách hàng** — Điểm số RFM, phân khúc, giá trị suốt đời
- **Tóm tắt Hành vi Mua hàng** — Tần suất đặt hàng, giá trị trung bình của đơn hàng, danh mục ưa thích
- **Tóm tắt Tương tác** — Lần đăng nhập cuối cùng, tỷ lệ mở email, hoạt động trên trang web

Các trường phân tích này được tính toán tự động và không thể chỉnh sửa thủ công. Xem [Hiểu về Phân tích Khách hàng](customer-analytics.md) để biết thêm chi tiết.

## Tạo Tài khoản Khách hàng

Nhà bán hàng có thể tạo tài khoản khách hàng thủ công cho các đơn hàng qua điện thoại, đặt hàng tại cửa hàng, hoặc để đăng ký trước các khách hàng buôn bán.

1. Nhấp vào **+ Thêm Hồ sơ Khách hàng** ở góc trên bên phải
2. Điền các trường bắt buộc và không bắt buộc:

| Trường | Bắt buộc | Mô tả |
|-------|----------|-------------|
| **Người dùng** | Có | Chọn tài khoản Người dùng hiện có hoặc tạo mới |
| **Điện thoại** | Không | Số điện thoại của khách hàng |
| **Ngày sinh** | Không | Để xác minh độ tuổi và chiến dịch sinh nhật |
| **Đăng ký Bản tin** | Không | Đăng ký khách hàng vào bản tin |
| **Email Quảng cáo** | Không | Đăng ký khách hàng vào email quảng cáo |

### Tạo Tài khoản Người dùng Mới Khi Thêm Hồ sơ

Nếu khách hàng chưa có tài khoản Người dùng:
1. Nhấp vào biểu tượng **+** bên cạnh trường Người dùng
2. Nhập **địa chỉ email** của khách hàng (đây sẽ là tên người dùng của họ)
3. Tùy chọn nhập **tên đầu** và **tên cuối**
4. Tùy chọn đặt **mật khẩu**
5. Chọn **Gửi email đặt lại mật khẩu** nếu bạn chưa đặt mật khẩu
6. Lưu tài khoản Người dùng
7. Hoàn tất các trường Hồ sơ Khách hàng
8. Nhấp **Lưu**

### Email Chào mừng

Sau khi tạo tài khoản khách hàng:
- Nếu bạn đã đặt mật khẩu, khách hàng có thể đăng nhập ngay lập tức với mật khẩu đó
- Nếu bạn chưa đặt mật khẩu, hệ thống sẽ gửi email đặt lại mật khẩu để khách hàng tự đặt mật khẩu của họ
- Bạn có thể kích hoạt thủ công email chào mừng qua hệ thống email tại **Marketing > Chiến dịch Email**

## Chỉnh sửa Thông tin Khách hàng

Để cập nhật thông tin khách hàng:
1. Di chuyển đến **Customers > All Customers**
2. Nhấp vào tên khách hàng
3. Chỉnh sửa các trường bạn muốn cập nhật
4. Nhấp **Lưu**

### Những Điều Bạn Có Thể Chỉnh sửa

**Thông tin Liên lạc:**
- Tên (qua tài khoản Người dùng)
- Địa chỉ email (qua tài khoản Người dùng)
- Số điện thoại
- Ngày sinh

**Ưa chuộng:**
- Trạng thái đăng ký bản tin
- Đăng ký email quảng cáo
- Ưa chuộng thông báo đơn hàng
- Bố cục trang chủ và cài đặt hiển thị

### Những Điều Bạn Không Thể Chỉnh sửa

Các trường này được tính toán tự động dựa trên hành vi của khách hàng:
- Tổng chi tiêu / Giá trị khách hàng
- Số lượng đơn hàng
- Phân khúc khách hàng (Champion, Loyal, At Risk, v.v.)
- Điểm số RFM
- Dự đoán giá trị suốt đời
- Ngày đơn hàng cuối cùng
- Tóm tắt phân tích

Nếu các trường này hiển thị không chính xác, hãy kiểm tra dữ liệu đơn hàng cơ bản hoặc kích hoạt tính toán lại thủ công tại **Customers > Analytics** → **Tính toán lại Chỉ số**.

## Ghi chú Khách hàng

Thêm ghi chú nội bộ về khách hàng để theo dõi các vấn đề hỗ trợ, yêu cầu VIP hoặc các nhiệm vụ theo dõi.

### Thêm Ghi chú

1. Mở hồ sơ khách hàng
2. Cuộn xuống phần **Ghi chú Khách hàng** (có thể là tab riêng biệt)
3. Nhấp **+ Thêm Ghi chú**
4. Điền chi tiết ghi chú:

| Trường | Mô tả |
|-------|-------------|
| **Loại Ghi chú** | Tổng quát, Vấn đề Hỗ trợ, Khiếu nại, Khen ngợi, Dịch vụ VIP, Cần theo dõi, Vấn đề thanh toán, Vấn đề giao hàng |
| **Tiêu đề** | Tóm tắt ngắn gọn của ghi chú |
| **Nội dung** | Nội dung chi tiết của ghi chú |
| **Cần theo dõi** | Đánh dấu nếu cần hành động |
| **Ngày theo dõi** | Ngày cần theo dõi |
| **Hoàn thành** | Đánh dấu khi theo dõi đã hoàn thành |

### Loại Ghi chú

| Loại | Trường hợp sử dụng |
|------|----------|
| **Ghi chú Tổng quát** | Bất kỳ quan sát nào về khách hàng |
| **Vấn đề Hỗ trợ** | Ghi lại vé hỗ trợ hoặc vấn đề |
| **Khiếu nại** | Khiếu nại của khách hàng để theo dõi và giải quyết |
| **Khen ngợi** | Phản hồi tích cực về khách hàng hoặc phản hồi của họ |
| **Dịch vụ VIP** | Yêu cầu xử lý đặc biệt cho khách hàng VIP |
| **Cần theo dõi** | Nhiệm vụ cần hành động trước một ngày cụ thể |
| **Vấn đề thanh toán** | Ghi chú về các vấn đề thanh toán hoặc tranh chấp |
| **Vấn đề giao hàng** | Ghi chú về các vấn đề giao hàng hoặc yêu cầu giao hàng đặc biệt |

### Xem Lịch sử Ghi chú

Tất cả ghi chú sẽ xuất hiện theo thứ tự thời gian trên hồ sơ khách hàng. Mỗi ghi chú hiển thị:
- Ngày và giờ tạo
- Người tạo (tên nhân viên)
- Biểu tượng loại ghi chú
- Tiêu đề và nội dung
- Trạng thái theo dõi nếu có

### Ghi chú Nội bộ và Ghi chú Khách hàng Có thể Xem

Tất cả ghi chú khách hàng đều là **nội bộ** theo mặc định — khách hàng sẽ không bao giờ nhìn thấy các ghi chú này. Chúng chỉ dành cho giao tiếp nội bộ trong đội ngũ bán hàng.

Nếu bạn cần giao tiếp với khách hàng, hãy sử dụng hệ thống email tại **Marketing > Chiến dịch Email** hoặc thêm ghi chú vào đơn hàng cụ thể.

## Chuyển đổi Khách hàng Vãng lai thành Khách hàng Đăng ký

Khách hàng vãng lai được tạo tự động khi ai đó hoàn tất thanh toán mà không tạo tài khoản. Tên người dùng của họ theo mẫu `guest_10374` với số là ID duy nhất.

Để chuyển đổi khách hàng vãng lai thành khách hàng đăng ký:

1. Di chuyển đến **Customers > All Customers**
2. Tìm kiếm khách hàng vãng lai theo địa chỉ email đơn hàng của họ
3. Nhấp vào hồ sơ khách hàng vãng lai
4. Nhấp vào liên kết **Người dùng** để chỉnh sửa tài khoản Người dùng cơ bản
5. Thay đổi **tên người dùng** từ `guest_10374` thành địa chỉ email thực tế của khách hàng
6. Thay đổi **email** để khớp với địa chỉ email
7. Tùy chọn thêm **tên đầu** và **tên cuối**
8. Chọn **Gửi email đặt lại mật khẩu** để khách hàng có thể đặt mật khẩu
9. Nhấp **Lưu**

Bây giờ khách hàng có thể đăng nhập bằng địa chỉ email của họ và sẽ thấy các đơn hàng vãng lai trước đây trong lịch sử đơn hàng của họ.

### Tại Sao Nên Chuyển đổi Khách hàng Vãng lai?

- Các đơn hàng vãng lai không được tính vào phân tích khách hàng hoặc phân khúc
- Khách hàng vãng lai không thể theo dõi đơn hàng hoặc truy cập lịch sử đơn hàng
- Việc chuyển đổi khách hàng vãng lai tăng số lượng khách hàng đăng ký và cải thiện độ chính xác của phân tích
- Khách hàng đăng ký có khả năng cao hơn để mua lại

## Tạm khóa vs Xóa Tài khoản

### Tạm khóa Tài khoản Khách hàng

Tạm khóa ngăn đăng nhập nhưng vẫn giữ nguyên tất cả dữ liệu:

1. Mở hồ sơ khách hàng
2. Nhấp vào liên kết **Người dùng** để chỉnh sửa tài khoản Người dùng
3. **Bỏ chọn "Hoạt động"**
4. Nhấp **Lưu**

**Điều gì xảy ra:**
- Khách hàng không thể đăng nhập
- Lịch sử đơn hàng được giữ nguyên
- Khách hàng có thể được kích hoạt lại sau này bằng cách chọn "Hoạt động" lại
- Phân tích và chỉ số vẫn giữ nguyên

**Sử dụng tạm khóa cho:**
- Tạm dừng tài khoản do tranh chấp thanh toán
- Chặn khách hàng gây khó chịu
- Khách hàng yêu cầu dừng nhận quyền truy cập nhưng không xóa dữ liệu

### Xóa Tài khoản Khách hàng

Xóa tài khoản sẽ loại bỏ tài khoản và có thể làm mất liên kết lịch sử đơn hàng:

1. Mở hồ sơ khách hàng
2. Cuộn xuống dưới và nhấp **Xóa**
3. Xác nhận xóa

**Điều gì xảy ra:**
- Tài khoản khách hàng bị xóa vĩnh viễn
- Hồ sơ khách hàng bị xóa
- Lịch sử đơn hàng có thể bị mất (đơn hàng tồn tại nhưng không liên kết với khách hàng)
- Không thể hoàn tác

**Sử dụng xóa cho:**
- Yêu cầu xóa dữ liệu theo GDPR/CCPA (xuất dữ liệu trước)
- Tài khoản kiểm tra mà không nên tồn tại
- Tài khoản trùng lặp được tạo nhầm

### Tuân thủ GDPR

Trước khi xóa tài khoản khách hàng theo yêu cầu GDPR:

1. Di chuyển đến **Customers > All Customers**
2. Chọn khách hàng
3. Sử dụng hành động **Xuất Dữ liệu** để tạo bản xuất dữ liệu đầy đủ
4. Gửi bản xuất cho khách hàng nếu họ yêu cầu
5. Sau đó thực hiện xóa

Bản xuất bao gồm: hồ sơ khách hàng, lịch sử đơn hàng, địa chỉ, ghi chú và dữ liệu phân tích.

## Mẹo

- **Sử dụng bộ lọc để xác định khách hàng cao giá trị** — Lọc theo Giá trị Khách hàng để tìm Champions và VIP
- **Kiểm tra ghi chú khách hàng thường xuyên** — Kiểm tra các nhiệm vụ theo dõi mở ít nhất hàng tuần
- **Không chỉnh sửa phân tích thủ công** — Để hệ thống tính toán điểm số RFM và phân khúc tự động
- **Chuyển đổi khách hàng vãng lai chủ động** — Sau khi khách hàng vãng lai thực hiện lần mua hàng thứ hai, hãy liên hệ và đề nghị tạo tài khoản chính thức
- **Sử dụng tạm khóa thay vì xóa** — Tạm khóa giữ nguyên dữ liệu và có thể đảo ngược nếu cần
- **Thêm ghi chú trong cuộc gọi hỗ trợ** — Ghi lại các tương tác hỗ trợ để các thành viên nhóm khác có bối cảnh
- **Đặt ngày theo dõi** — Sử dụng hệ thống nhiệm vụ theo dõi trong ghi chú để đảm bảo không bỏ sót bất kỳ điều gì
- **Tôn trọng ước muốn giao tiếp** — Không gửi email quảng cáo cho khách hàng đã từ chối nhận
