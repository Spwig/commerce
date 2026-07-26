---
title: Ví khách hàng
---

Ví khách hàng là sổ cái tín dụng cửa hàng theo dõi số dư đang chạy cho từng khách hàng. Tín dụng cửa hàng có thể được thêm vào do hoàn tiền, phần thưởng giới thiệu, chiến dịch khuyến mãi hoặc các điều chỉnh thủ công do nhóm của bạn thực hiện.

> **Số dư ví có thể sử dụng tại bước thanh toán.** Một khách hàng đã đăng nhập với tín dụng cửa hàng sẽ thấy nó tại bước thanh toán và có thể áp dụng chỉ với một cú nhấp chuột. Tín dụng sẽ được trừ khỏi hóa đơn cuối cùng — sau thuế và giao hàng — và phần còn lại sẽ được thanh toán bằng thẻ của họ như thường lệ. Nếu tín dụng đủ để thanh toán toàn bộ đơn hàng, không cần thẻ nào cả. Tín dụng được giữ lại khi áp dụng và chỉ thực sự được trừ khi thanh toán được xác nhận, do đó, việc bỏ qua thanh toán sẽ không làm mất bất cứ thứ gì cho khách hàng.

Truy cập **Customers > Customer Wallets** để xem và quản lý các ví.

## Hiểu về số dư ví

Mỗi ví khách hàng hiển thị bốn con số số dư:

| Balance | Description |
|---|---|
| **Available Balance** | Số dư hiện tại và có thể sử dụng của khách hàng — đây sẽ là số tiền có thể chi tiêu tại bước thanh toán khi tính năng này được triển khai |
| **Pending Balance** | Các khoản tín dụng chưa được đưa vào số dư có sẵn — ví dụ, một khoản hoàn tiền vẫn còn trong khoảng thời gian xác nhận |
| **Lifetime Credited** | Tổng số tiền từng được ghi vào ví này, bao gồm tất cả các khoản tín dụng trước đây |
| **Lifetime Used** | Tổng số tiền từng được trừ khỏi ví này |

Số dư có sẵn là con số sẽ quan trọng khi tính năng chi tiêu tại bước thanh toán được triển khai. Các khoản tín dụng đang chờ sẽ chuyển vào khi thời gian chờ kết thúc.

## Xem ví của khách hàng

1. Truy cập **Customers > Customer Wallets**
2. Sử dụng trường tìm kiếm để tìm khách hàng theo tên hoặc email
3. Nhấp vào mục ví để mở chế độ xem chi tiết

Chế độ xem chi tiết hiển thị các số dư hiện tại ở trên cùng và lịch sử giao dịch đầy đủ bên dưới. Các nhãn **Last Credited At** và **Last Used At** cho bạn biết thời điểm cuối cùng ví được sử dụng.

### Lọc danh sách ví

Sử dụng bộ lọc **Active** để phân tách các ví đang hoạt động và các ví bị đóng băng. Một ví được đánh dấu là không hoạt động sẽ bị đóng băng — không có khoản tín dụng hoặc giao dịch nào có thể được ghi vào, mặc dù số dư của nó vẫn được giữ nguyên.

## Đọc lịch sử giao dịch

Mọi thay đổi về số dư ví đều được ghi lại dưới dạng một giao dịch riêng biệt. Lịch sử giao dịch là sổ cái đầy đủ và vĩnh viễn — các giao dịch không bao giờ được chỉnh sửa hoặc xóa. Nếu cần sửa lỗi, sẽ thêm một giao dịch bù đắp mới thay vì vậy.

Mỗi giao dịch hiển thị:

| Field | Description |
|---|---|
| **Type** | Tín dụng, Giao dịch, Hoàn tiền, Điều chỉnh, hoặc Hủy bỏ |
| **Amount** | Giá trị của giao dịch này (luôn được hiển thị dưới dạng số dương) |
| **Balance After** | Số dư ví ngay sau khi giao dịch này được áp dụng |
| **Source** | Nơi mà khoản tín dụng hoặc giao dịch bắt nguồn |
| **Status** | Hoàn thành, Chờ xử lý, hoặc Hủy bỏ |
| **Description** | Một lời giải thích ngắn gọn về giao dịch |
| **Reference ID** | Liên kết đến bản ghi gốc (ví dụ, số đơn hàng hoặc ID phần thưởng) |
| **Created At** | Thời điểm giao dịch được ghi lại |

### Giải thích các loại giao dịch

- **Tín dụng** — tiền được thêm vào ví (từ hoàn tiền, khuyến mãi, hoặc điều chỉnh thủ công)
- **Giao dịch** — tiền được trừ khỏi ví. Khi tính năng chi tiêu tại bước thanh toán được triển khai, điều này sẽ có nghĩa là "đã chi tiêu cho một đơn hàng" — hiện tại, cách duy nhất để xảy ra giao dịch là điều chỉnh thủ công
- **Hoàn tiền** — tín dụng được thêm vào cụ thể do đơn hàng được hoàn tiền hoặc hủy bỏ
- **Điều chỉnh** — một sự điều chỉnh thủ công được thực hiện bởi nhóm của bạn
- **Hủy bỏ** — một giao dịch hủy bỏ một mục nhập trước đó

### Giải thích nguồn giao dịch

- **Hoàn tiền đơn hàng** — tín dụng được cấp khi đơn hàng được hoàn tiền lại vào ví
- **Phần thưởng giới thiệu** — tín dụng được kiếm thông qua chương trình giới thiệu
- **Khuyến mãi** — tín dụng được cấp như một phần của chiến dịch marketing
- **Điều chỉnh thủ công** — tín dụng được thêm hoặc trừ trực tiếp bởi nhân viên
- **Thanh toán đơn hàng** — tiền được chi tiêu tại bước thanh toán để thanh toán cho một đơn hàng. Hiện chưa được sử dụng — dành cho khi tính năng chi tiêu ví tại bước thanh toán được triển khai

## Điều chỉnh ví thủ công

Bạn không thể thêm hoặc rút tiền từ bảng điều khiển quản trị — các giao dịch ví chỉ được tạo bởi các quy trình sở hữu chúng: hoàn tiền đơn hàng, phần thưởng trung thành và phần thưởng giới thiệu. Điều này là cố ý. Mỗi lần di chuyển đều có một tham chiếu trở lại nguyên nhân gây ra nó, và một kiểm tra hàng đêm sẽ xác minh số dư ví của mỗi người dùng dựa trên lịch sử của họ; các hàng được nhập thủ công là điều làm gián đoạn chuỗi này.

Đối với một khoản tín dụng thiện chí — ví dụ như khiếu nại dịch vụ, một hành động sau khi xảy ra vấn đề — hãy phát hành **thẻ quà tặng** thủ công thay vào đó (xem chủ đề trợ giúp **Thẻ quà tặng**). Một thẻ quà tặng được thiết kế chính xác cho mục đích này: bạn kiểm soát giá trị, khách hàng sẽ nhận được mã qua email, và nó được sử dụng tại bước thanh toán giống như tiền tín dụng cửa hàng.

## Khóa ví

Nếu bạn cần ngăn khách hàng sử dụng số dư ví của họ — ví dụ, trong quá trình điều tra gian lận — bạn có thể ngừng hoạt động ví mà không cần xóa hoặc rút số dư.

1. Mở view chi tiết ví của khách hàng
2. Bỏ chọn nút **Hoạt động**
3. Nhấp **Lưu**

Số dư được giữ lại và ví có thể được kích hoạt lại bất kỳ lúc nào. Khi bị khóa, không có giao dịch tín dụng hoặc ghi nợ mới — thủ công hoặc khác — có thể được ghi lại vào ví.

## Xem tất cả giao dịch

Để có cái nhìn toàn bộ về hoạt động ví, hãy di chuyển đến **Khách hàng > Giao dịch Ví**. Danh sách này hiển thị mọi giao dịch trên tất cả ví khách hàng, với các bộ lọc sau:

- **Loại giao dịch** — bộ lọc theo tín dụng, ghi nợ, điều chỉnh, v.v.
- **Nguồn** — bộ lọc theo nơi các giao dịch bắt đầu
- **Trạng thái** — bộ lọc theo hoàn tất, đang chờ hoặc hoàn tiền
- **Ngày** — sử dụng phân cấp ngày ở đầu để xem chi tiết một ngày cụ thể, tháng hoặc năm

Danh sách giao dịch chỉ đọc — các giao dịch không thể được chỉnh sửa hoặc xóa từ view này.

## Một số mẹo

- Kiểm tra **Tổng số tiền đã được tín dụng** so với **Tổng số tiền đã sử dụng** để hiểu rõ mức độ khách hàng sử dụng tiền tín dụng cửa hàng của họ — một số dư lớn chưa sử dụng có thể cho thấy khách hàng đã quên rằng nó tồn tại
- Nếu khách hàng báo cáo số dư của họ trông sai, hãy xem lại toàn bộ lịch sử giao dịch để theo dõi chính xác cách số dư thay đổi theo thời gian; cột **Số dư sau** trên mỗi mục giúp điều này trở nên dễ dàng
- Một số dư lớn chưa sử dụng đáng để nhắc nhở — khách hàng có thể thấy tiền tín dụng cửa hàng của họ trên bảng điều khiển tài khoản và tại bước thanh toán khi mua hàng, nhưng một email ngắn nhắc đến điều này thường chuyển đổi nó thành một đơn hàng
- Các ví bị khóa giữ số dư vĩnh viễn; không có thời hạn — nếu bạn tạm thời ngừng hoạt động một ví, hãy nhớ kích hoạt lại khi vấn đề được giải quyết
- **Mã tham chiếu** trên mỗi giao dịch liên kết trở lại bản ghi gốc, giúp dễ dàng xác minh lý do tại sao một khoản tín dụng hoặc ghi nợ được áp dụng mà không cần phải tìm kiếm ở nơi khác