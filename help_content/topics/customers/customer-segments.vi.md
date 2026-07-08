---
title: Phân khúc khách hàng
---

Phân khúc khách hàng cho phép bạn tự động phân loại khách hàng của mình thành các nhóm có ý nghĩa dựa trên hành vi mua hàng của họ. Sau khi khách hàng được phân nhóm, bạn có thể sử dụng các nhóm này để tập trung vào nỗ lực tiếp thị của mình — ví dụ như cung cấp phần thưởng trung thành cho khách hàng VIP hoặc gửi chiến dịch thu hút lại khách hàng đã lâu không mua hàng.

Spwig đánh giá các tiêu chí phân khúc dựa trên các chỉ số của từng khách hàng và gán họ vào phân khúc có độ ưu tiên cao nhất mà họ đủ điều kiện. Điều này xảy ra tự động khi dữ liệu khách hàng được cập nhật.

## Các loại phân khúc có sẵn

Spwig đi kèm với một bộ các loại phân khúc được xây dựng sẵn. Mỗi loại phân khúc có một định danh nội bộ cố định, nhưng bạn có thể tùy chỉnh tên hiển thị, mô tả, tiêu chí và màu sắc để phù hợp với cách bạn nhìn nhận về khách hàng của mình.

| Loại Phân Khúc | Mục đích Thường Gặp |
|---|---|
| **Khách hàng Không Đăng Ký** | Khách hàng đã thanh toán mà không tạo tài khoản |
| **Khách hàng Mới** | Khách hàng đã thực hiện lần mua hàng đầu tiên gần đây |
| **Khách hàng Thường xuyên** | Khách hàng có lịch sử mua hàng ổn định |
| **Khách hàng Mua Nhiều** | Khách hàng mua hàng thường xuyên (khoảng thời gian giữa các đơn hàng ngắn) |
| **Khách hàng Giá Trị Cao** | Khách hàng có tổng chi tiêu cao |
| **Khách hàng VIP** | Khách hàng có giá trị và trung thành nhất của bạn |
| **Khách hàng Săn Sale** | Khách hàng có xu hướng mua hàng trong các đợt khuyến mãi |
| **Khách hàng Nguy Cơ** | Khách hàng đã lâu không mua hàng |
| **Khách hàng Không Hoạt Động** | Khách hàng đã vắng mặt trong một khoảng thời gian dài |

## Hiểu về tiêu chí phân khúc

Mỗi phân khúc được xác định bởi sự kết hợp của các tiêu chí. Spwig kiểm tra các tiêu chí này dựa trên các chỉ số đã lưu trữ của từng khách hàng. Tất cả các tiêu chí trong một phân khúc được kết hợp — khách hàng phải đáp ứng tất cả các điều kiện được thiết lập để đủ điều kiện.

### Tiêu chí chi tiêu

- **Tối Thiểu Tổng Chi Tiêu** — khách hàng phải chi ít nhất số tiền này trên tất cả các đơn hàng đã hoàn thành
- **Tối Đa Tổng Chi Tiêu** — khách hàng không được chi quá số tiền này

Sử dụng khoảng chi tiêu để xác định một cấp bậc cụ thể. Ví dụ, thiết lập Tối Thiểu là 500 USD và Tối Đa là 2.000 USD sẽ nhắm đến các khách hàng ở cấp trung.

### Tiêu chí số lượng đơn hàng

- **Tối Thiểu Số Đơn Hàng** — khách hàng phải có ít nhất số lượng đơn hàng hoàn thành này
- **Tối Đa Số Đơn Hàng** — khách hàng không được có nhiều hơn số lượng đơn hàng hoàn thành này

Kết hợp Tối Thiểu Số Đơn Hàng với một mức chi tiêu tối thiểu là cách đáng tin cậy để xác định khách hàng VIP: họ mua hàng thường xuyên *và* chi tiêu một cách hào phóng.

### Tiêu chí gần nhất

- **Tối Thiểu Số Ngày Từ Lần Mua Gần Nhất** — đơn hàng gần nhất của khách hàng phải ít nhất là số ngày này trước đây
- **Tối Đa Số Ngày Từ Lần Mua Gần Nhất** — đơn hàng gần nhất của khách hàng phải nằm trong khoảng số ngày này

Các tiêu chí gần nhất là rất quan trọng cho các phân khúc Nguy Cơ và Không Hoạt Động. Ví dụ, thiết lập Tối Thiểu Ngày là 90 và Tối Đa Ngày là 365 sẽ xác định các khách hàng đã im lặng nhưng chưa hoàn toàn bị mất đi.

## Ưu tiên phân khúc

Khi một khách hàng đủ điều kiện cho nhiều hơn một phân khúc, phân khúc có **giá trị ưu tiên cao nhất** sẽ được chọn. Bạn có thể thiết lập ưu tiên cho từng phân khúc trong phần **Cài Đặt Hiển Thị** của biểu mẫu phân khúc.

Phân khúc **Khách hàng Không Đăng Ký** luôn được đánh giá trước tiên, độc lập với thứ tự ưu tiên, vì trạng thái khách hàng không đăng ký được xác định bởi loại tài khoản thay vì tiêu chí mua hàng.

## Xem và quản lý phân khúc

Truy cập **Khách hàng > Phân Khúc Khách Hàng** để xem tất cả các phân khúc đã cấu hình của bạn. Danh sách hiển thị tên hiển thị của từng phân khúc, loại nội bộ, màu được gán, độ ưu tiên, số lượng khách hàng hiện tại phù hợp, và liệu phân khúc có đang hoạt động hay không.

![Danh sách phân khúc khách hàng](/static/core/admin/img/help/customer-segments/segments-list.webp)

### Tạo hoặc chỉnh sửa phân khúc

1.

Truy cập **Khách hàng > Phân Khúc Khách Hàng**
2.

Nhấp vào phân khúc hiện có để chỉnh sửa, hoặc nhấp **+ Thêm Phân Khúc Khách Hàng** để tạo một phân khúc mới
3.

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

Điền vào tab **Thông tin phân khúc**:
   - **Tên** — chọn loại phân khúc nội bộ từ danh sách thả xuống
   - **Tên hiển thị** — tên dễ hiểu được hiển thị trong trang quản trị (ví dụ: "Khách hàng VIP")
   - **Mô tả** — ghi chú ngắn gọn bên trong giải thích phân khúc này đại diện cho điều gì
4.

Đặt tiêu chí trên các tab liên quan:
   - **Tiêu chí - Chi tiêu** — chi tiêu tối thiểu và tối đa tổng cộng
   - **Tiêu chí - Đơn hàng** — số lượng đơn hàng tối thiểu và tối đa
   - **Tiêu chí - Tính gần nhất** — số ngày tối thiểu và tối đa kể từ lần mua hàng cuối cùng
5.

Cấu hình **Cài đặt hiển thị**:
   - **Màu sắc** — mã màu hex được sử dụng để nhận biết phân khúc này trực quan trong danh sách
   - **Ưu tiên** — số càng cao thì phân khúc này được đánh giá trước
   - **Kích hoạt** — bỏ chọn để vô hiệu hóa phân khúc mà không xóa nó
6.

Nhấp vào **Lưu** để áp dụng các thay đổi

### Ví dụ: Cấu hình phân khúc VIP

Đây là ví dụ thực tế cho một phân khúc VIP cao giá:

| Trường | Giá trị |
|---|---|
| Tên | `vip` |
| Tên hiển thị | Khách hàng VIP |
| Chi tiêu tối thiểu | $1,000 |
| Số đơn hàng tối thiểu | 5 |
| Số ngày tối đa kể từ lần mua hàng cuối cùng | 180 |
| Ưu tiên | 90 |
| Màu sắc | `#FFD700` |

Điều này có nghĩa là: một khách hàng đủ điều kiện là VIP nếu họ đã chi ít nhất $1,000, đặt ít nhất 5 đơn hàng và mua hàng trong vòng 6 tháng qua.

### Ví dụ: Cấu hình phân khúc Nguy cơ cao

| Trường | Giá trị |
|---|---|
| Tên | `at_risk` |
| Tên hiển thị | Nguy cơ cao |
| Số ngày tối thiểu kể từ lần mua hàng cuối cùng | 60 |
| Số ngày tối đa kể từ lần mua hàng cuối cùng | 180 |
| Ưu tiên | 30 |
| Màu sắc | `#FF6B35` |

## Sử dụng phân khúc cho tiếp thị nhắm mục tiêu

Các phân khúc được hiển thị trên hồ sơ khách hàng trong toàn bộ trang quản trị, vì vậy nhóm của bạn sẽ biết ngay lập tức khách hàng thuộc cấp nào. Sử dụng thông tin này để:

- **Chạy chiến dịch phiếu giảm giá nhắm mục tiêu** — tạo phiếu giảm giá chỉ dành cho khách hàng trong phân khúc cụ thể, sau đó sử dụng hệ thống email của bạn để gửi chúng chỉ cho nhóm đó
- **Ưu tiên hỗ trợ** — đánh dấu khách hàng VIP hoặc có giá trị cao để nhóm của bạn có thể cung cấp dịch vụ ưu tiên
- **Lên kế hoạch tái tiếp cận** — xem xét định kỳ các phân khúc Nguy cơ cao và Không hoạt động để xác định khách hàng cần email phục hồi hoặc ưu đãi đặc biệt
- **Điều chỉnh chi phí tiếp thị** — tập trung ngân sách thu hút vào các kênh mang lại khách hàng có giá trị cao bằng cách phân tích các nhóm nào mà các phân khúc chuyển đổi

## Một số mẹo

- Bắt đầu với các loại phân khúc có sẵn trước khi tạo tiêu chí tùy chỉnh — chúng đáp ứng nhu cầu phân khúc phổ biến nhất ngay từ đầu
- Kiểm tra định kỳ số lượng khách hàng trên mỗi phân khúc; một phân khúc VIP không có khách hàng hoặc phân khúc Nguy cơ cao đang tăng nhanh đều đáng để điều tra
- Sử dụng cẩn thận trường **Ưu tiên** — nếu tiêu chí của bạn chồng chéo giữa các phân khúc (ví dụ: một khách hàng đủ điều kiện cho cả Người mua hàng thường xuyên và Người có giá trị cao), phân khúc có độ ưu tiên cao hơn sẽ được áp dụng
- Vô hiệu hóa các phân khúc bạn không đang sử dụng thay vì xóa chúng — bạn có thể kích hoạt lại chúng sau này mà không cần cấu hình lại tiêu chí
- Tiêu chí phân khúc được kiểm tra với các chỉ số khách hàng đã lưu trữ, các chỉ số này được tính toán lại tự động. Nếu số lượng phân khúc trông cũ kỹ, bạn có thể tính toán lại chỉ số từ phần **Chỉ số khách hàng** trong trang quản trị