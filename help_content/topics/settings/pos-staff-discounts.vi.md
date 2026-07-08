---
title: Giảm giá nhân viên POS và An ninh Thiết bị
---

Cài đặt giảm giá nhân viên POS cho phép bạn kiểm soát mức giảm giá mà mỗi nhân viên có thể áp dụng tại điểm bán hàng. Các sự kiện khóa thiết bị cung cấp hồ sơ kiểm toán cho mỗi lần thiết bị được khóa hoặc mở khóa — giúp bạn theo dõi ai đã truy cập thiết bị và có hay không có bất kỳ lần đăng nhập thất bại nào xảy ra.

## Giới hạn giảm giá nhân viên

Mỗi nhân viên sử dụng POS có thể có quyền hạn giảm giá riêng. Mặc định, nhân viên có thể áp dụng giảm giá lên đến 10% cho từng mặt hàng hoặc toàn bộ giỏ hàng. Bạn có thể tăng hoặc giảm giới hạn này theo từng người, hoặc chỉ định nhân viên là quản lý có thể phê duyệt các khoản giảm giá vượt quá giới hạn tiêu chuẩn.

### Cấu hình giới hạn giảm giá cho nhân viên

1. Di chuyển đến **POS > Giảm giá Nhân viên**
2. Nhấp **+ Thêm Giảm giá Nhân viên POS** hoặc nhấp vào nhân viên hiện có để chỉnh sửa
3. Chọn **Nhân viên** từ danh sách
4. Thiết lập giới hạn giảm giá:

| Trường | Mô tả |
|-------|-------------|
| **Tối đa % Giảm giá** | Tỷ lệ phần trăm giảm giá tối đa mà người này có thể áp dụng (ví dụ: `10` cho 10%) |
| **Tối đa Số tiền Giảm giá** | Số tiền cố định tối đa cho mỗi giao dịch (trống để không có giới hạn cố định) |
| **Có thể Áp dụng Giảm giá Mặt hàng** | Cho phép giảm giá từng mục hàng |
| **Có thể Áp dụng Giảm giá Toàn bộ Giỏ hàng** | Cho phép giảm giá tổng số tiền toàn bộ giỏ hàng |
| **Yêu cầu Lý do** | Khi được chọn, nhân viên phải nhập lý do trước khi áp dụng bất kỳ khoản giảm giá nào |

5. Nhấp **Lưu**

### Cách giới hạn giảm giá hoạt động tại POS

Khi nhân viên thu ngân cố gắng áp dụng giảm giá:
- Nếu giảm giá nằm trong giới hạn của họ, nó sẽ được áp dụng ngay lập tức
- Nếu giảm giá vượt quá giới hạn của họ, thiết bị sẽ yêu cầu **phê duyệt từ quản lý**
- Một quản lý nhập mã PIN của họ để phê duyệt việc ghi đè, và khoản giảm giá sẽ được áp dụng

Quy trình này ngăn chặn các khoản giảm giá có giá trị cao không được ủy quyền, đồng thời cho phép linh hoạt khi các khoản giảm giá thực sự cần thiết.

## Vai trò quản lý

Nhân viên có cờ **Là Quản lý** có thể phê duyệt các khoản giảm giá vượt quá giới hạn của nhân viên khác. Các quản lý được xác định tại thiết bị thông qua mã PIN mà họ nhập khi yêu cầu phê duyệt.

### Thiết lập quản lý

1. Mở hồ sơ giảm giá của nhân viên
2. Chọn **Là Quản lý**
3. Nhập **Mã PIN Quản lý** (4-6 chữ số) — mã này được mã hóa an toàn khi lưu
4. Nhấp **Lưu**

Mã PIN quản lý là riêng biệt với mã PIN thu ngân được sử dụng để khóa/mở khóa thiết bị. Một quản lý có thể có cả mã PIN quản lý (dùng để phê duyệt giảm giá) và mã PIN thu ngân (dùng để truy cập thiết bị).

### An ninh mã PIN quản lý

Khi bạn nhập mã PIN trong biểu mẫu quản trị và lưu, Spwig sẽ tự động mã hóa nó — mã PIN gốc sẽ không bao giờ được lưu trữ. Trường mã PIN gốc sẽ xóa sau khi lưu, điều này là hành vi mong muốn.

## Mã PIN thu ngân và truy cập thẻ

Mỗi nhân viên cũng có thể có **Mã PIN Thu ngân** để khóa và mở khóa thiết bị:

- **Mã PIN Thu ngân** — mã PIN 4-6 chữ số được sử dụng để mở khóa thiết bị sau khi thiết bị tự động khóa hoặc được khóa thủ công
- **Mã Nhận dạng Thẻ** — Một thẻ đã đăng ký (thẻ quẹt hoặc NFC) cũng có thể được sử dụng để mở khóa thiết bị

Để thiết lập mã PIN thu ngân, hãy nhập mã PIN vào trường **Mã PIN Thu ngân** và lưu. Tương tự như mã PIN quản lý, nó sẽ được mã hóa tự động khi lưu.

## Sự kiện khóa thiết bị

Mỗi lần thiết bị được khóa hoặc mở khóa, Spwig sẽ ghi lại một sự kiện khóa thiết bị. Điều này tạo ra hồ sơ kiểm toán an ninh đầy đủ.

### Xem các sự kiện khóa

Di chuyển đến **POS > Sự kiện Khóa Thiết bị** để xem toàn bộ lịch sử. Bạn có thể lọc các sự kiện theo:
- Thiết bị
- Loại sự kiện
- Khoảng thời gian

### Loại sự kiện

| Sự kiện | Ý nghĩa |
|-------|---------|
| **Khóa thủ công** | Một nhân viên đã cố ý khóa thiết bị |
| **Khóa tự động (Hết thời gian không hoạt động)** | Thiết bị được khóa tự động do không có hoạt động |
| **Mở khóa bởi nhân viên thu ngân** | Nhân viên thu ngân xác thực và mở khóa thiết bị |
| **Mở khóa bởi quản lý** | Một quản lý đã sử dụng thông tin xác thực của họ để mở khóa |
| **Mở khóa bởi thẻ** | Thiết bị được mở khóa bằng thẻ đã đăng ký |
| **Mở khóa bằng sinh trắc học** | Thiết bị được mở khóa bằng vân tay hoặc nhận diện khuôn mặt |
| **Thử mở khóa thất bại** | Một lần thử mở khóa được thực hiện bằng thông tin xác thực không đúng |
| **Khóa tạm thời (3+ lần thất bại)** | Thiết bị bị khóa sau nhiều lần thất bại liên tiếp |

### Những gì các bản ghi sự kiện khóa chứa

Mỗi sự kiện ghi lại:
- Thiết bị **Terminal** liên quan
- **Loại sự kiện**
- Người thực hiện hành động (**Performed By**) và người đã đăng nhập khi sự kiện khóa xảy ra (**Locked By**)
- Liệu có sử dụng **Quyền ưu tiên của quản lý** hay không
- **Phương pháp mở khóa** (Mã PIN, thẻ hoặc sinh trắc học)
- **Số lần thử mở khóa thất bại** trước sự kiện này (hữu ích để phát hiện các mẫu brute-force)
- **Tổng giá trị giỏ hàng** và số lượng mặt hàng tại thời điểm sự kiện
- Địa chỉ IP của yêu cầu

### Khảo sát một vấn đề bảo mật

Nếu bạn nghi ngờ có truy cập trái phép vào thiết bị:

1. Di chuyển đến **POS > Terminal Lock Events**
2. Lọc theo thiết bị cần kiểm tra
3. Tìm các sự kiện loại **Thử mở khóa thất bại** hoặc **Khóa tạm thời** — những sự kiện này cho thấy nhiều lần truy cập thất bại
4. Kiểm tra trường **Performed By** trên các lần mở khóa thành công để xem ai đã truy cập
5. Đối chiếu với bản ghi ca làm việc (**POS > Shifts**) để xác minh nhân viên thu ngân được giao nhiệm vụ

## Mẹo

- Thiết lập giới hạn giảm giá dựa trên cấp bậc nhân viên — nhân viên mới có thể bắt đầu ở 5%, nhân viên có kinh nghiệm ở 10-15%, và quản lý có thể phê duyệt bất kỳ mức nào cao hơn.
- Kích hoạt **Yêu cầu lý do** cho bất kỳ nhân viên nào có giới hạn giảm giá cao hơn. Việc ghi lại lý do giúp bạn phân tích xu hướng giảm giá và phát hiện bất kỳ việc lạm dụng nào.
- Kiểm tra các sự kiện khóa thiết bị hàng tuần nếu cửa hàng của bạn có nhiều nhân viên hoặc tỷ lệ nhân viên thay đổi cao — các mẫu truy cập bất thường dễ dàng được phát hiện trước khi chúng trở thành vấn đề.
- Nếu một nhân viên rời đi, hãy lập tức xóa mã PIN và định danh thẻ của họ để ngăn chặn quyền truy cập thiết bị.
- Sử dụng sự kiện khóa tạm thời để xác định các thiết bị có thể cần điều chỉnh thời gian khóa tự động — nếu khách hàng thường xuyên kích hoạt khóa không cố ý, thời gian không hoạt động có thể được đặt quá ngắn.
- Mã PIN của quản lý nên được thay đổi định kỳ. Cập nhật chúng trong bản ghi giảm giá nhân viên — mã PIN mới sẽ được mã hóa khi lưu.