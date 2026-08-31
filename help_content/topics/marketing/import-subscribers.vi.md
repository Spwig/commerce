---
title: Nhập người đăng ký từ tệp CSV
---

Nếu bạn đã có danh sách gửi thư rồi — một công cụ email cũ, bảng tính các cuộc đăng ký bản tin, hoặc một chồng các thẻ sự kiện — bạn không cần phải thêm từng liên hệ một vào Spwig. Chức năng nhập người đăng ký của Studio Chiến dịch đọc tệp CSV hoặc Excel và thêm mỗi liên hệ hợp lệ vào danh sách của bạn một cách nhanh chóng, sẵn sàng để gán nhãn, phân đoạn và gửi email.

## Trước khi nhập: sự đồng ý

Mỗi lần nhập đều yêu cầu bạn tích vào ô xác nhận: **"Những liên hệ này đã đồng ý nhận email tiếp thị từ tôi."** Đây không phải là một hình thức trang trọng — chỉ nhập những liên hệ đã thực sự đồng ý nhận email tiếp thị từ bạn. Điều này quan trọng vì hai lý do:

- **Đây là yêu cầu pháp lý ở hầu hết các nơi.** Gửi email tiếp thị cho những người chưa từng đồng ý nhận sẽ vi phạm luật đồng ý ở nhiều khu vực.
- **Điều này bảo vệ khả năng giao hàng của bạn.** Gửi email cho những người chưa đồng ý sẽ tạo ra các cuộc khiếu nại spam và email bị từ chối, điều mà các nhà cung cấp hộp thư sử dụng để quyết định xem *mọi* email của bạn — bao gồm cả những người đã đồng ý — có đến hộp thư hay không.

Nếu danh sách không rõ ràng đến từ các cuộc đăng ký đã đồng ý, đừng nhập nó.

## Chuẩn bị tệp của bạn

Chức năng nhập này chấp nhận tệp `.csv` hoặc `.xlsx` có hàng tiêu đề. Chỉ cần một cột duy nhất được yêu cầu:

| Cột | Có bắt buộc? | Ghi chú |
|--------|-----------|-------|
| **Email** | Có | Phải là địa chỉ email hợp lệ. |
| **Tên** | Không | Được sử dụng để cá nhân hóa email. |
| **Họ** | Không | Được sử dụng để cá nhân hóa email. |
| **Ngôn ngữ** | Không | Mã ngôn ngữ ưa thích của người đăng ký (ví dụ: `en`, `es`). |

Các cột được khớp với các trường này tự động bằng tên tiêu đề, vì vậy bạn không cần phải đổi tên chúng trước — các biến thể phổ biến như `E-mail`, `Email Address`, `First Name`, `Given Name`, `Surname`, hoặc `Locale` đều được nhận diện.

Mỗi lần nhập bị giới hạn ở **5 MB** và **5.000 hàng**. Nếu danh sách của bạn lớn hơn, hãy chia thành các tệp nhỏ hơn và nhập từng tệp một.

## Nhập liên hệ của bạn

1. Mở **Studio Chiến dịch > Người đăng ký** và nhấn **Nhập CSV**.
2. Chọn tệp `.csv` hoặc `.xlsx` của bạn.
3. Chọn điều gì sẽ **xảy ra với những người đã có trong danh sách của bạn** — xem [Xử lý trùng lặp](#xu-ly-trung-lap) bên dưới.
4. Tùy chọn chọn một thẻ dưới **Gán thẻ cho người đăng ký đã nhập** để đánh dấu tất cả mọi người trong lần nhập này (ví dụ: `Sự kiện 2026`) — xem [Thẻ người đăng ký](/help/subscriber-tags) để biết thêm thông tin về các thẻ.
5. Đánh dấu **Những liên hệ này đã đồng ý nhận email tiếp thị từ tôi**.
6. Nhấn **Tiếp tục**.

![Mẫu tải lên nhập với tệp đã chọn, thẻ đã chọn và sự đồng ý được xác nhận](/static/core/admin/img/help/import-subscribers/import-upload-form.webp)

Spwig sau đó hiển thị cho bạn một bản xem trước trước khi bất kỳ thứ gì được nhập thực sự:

![Màn hình xem trước nhập với số lượng người mới, người đã có và đã bỏ qua hợp lệ cùng lý do](/static/core/admin/img/help/import-subscribers/import-preview.webp)

- **Người đăng ký mới** — các hàng sẽ tạo ra một người đăng ký mới.
- **Đã có trong danh sách của bạn** — các hàng có địa chỉ email trùng với người đăng ký hiện có.
- **Bị bỏ qua (không hợp lệ)** — các hàng không thể đọc được, mỗi hàng được liệt kê cùng số hàng và lý do (định dạng email không hợp lệ, ô email trống, hoặc trùng lặp với hàng trước đó trong cùng tệp).

Kiểm tra các con số này, sau đó nhấn **Nhập ngay** để thực hiện việc nhập, hoặc **Hủy** để quay lại mà không thay đổi gì cả.

## Xử lý trùng lặp

Một hàng được coi là trùng lặp khi địa chỉ email của nó trùng với một người đăng ký bạn đã có. Bạn chọn cách Spwig xử lý những hàng này trên mẫu tải lên:

| Tùy chọn | Điều xảy ra |
|--------|--------------|
| **Giữ nguyên** *(mặc định)* | Tên và ngôn ngữ của người đăng ký hiện có được giữ nguyên. |
| **Cập nhật tên / ngôn ngữ** | Tên, họ và ngôn ngữ của người đăng ký hiện có được cập nhật từ tệp (chỉ cho các trường mà tệp thực sự cung cấp). |

Thẻ bạn chọn cho lần nhập được áp dụng cho **tất cả mọi người trong tệp** — cả người mới và người đã có — bất kể tùy chọn trùng lặp nào bạn chọn.


Việc nhập 'danh sách VIP' với thẻ **VIP** sẽ đánh dấu những người bạn đã có rồi nữa.

Tùy chọn trùng lặp chỉ kiểm soát việc tên và ngôn ngữ của người liên hệ đã có có được ghi đè hay không.

## Sau khi nhập

Mọi liên hệ được tạo bởi quá trình nhập sẽ được ghi nhận với nguồn **Nhập**, và được đánh dấu là đã đồng ý vào thời điểm bạn chạy quá trình nhập (không phải ngày nào họ có thể đã đồng ý ở nơi khác). Tên đệm và tên của họ — nếu tệp cung cấp — sẽ được lưu trên hồ sơ người đăng ký của họ, điều này có nghĩa là các trường ghi chú `[[first_name]]` và `[[last_name]]` trong chiến dịch của bạn hiện tại sẽ cá nhân hóa chính xác cho họ nữa, ngay cả khi họ chưa từng tạo tài khoản Spwig.

## Mẹo

- Xuất danh sách nguồn của bạn thành một tệp CSV hoặc `.xlsx` trên cùng một trang với hàng tiêu đề sạch sẽ trước khi tải lên — các trang phụ, ô được gộp hoặc hàng tóm tắt có thể làm rối column matching.
- Sử dụng **Gán thẻ cho người liên hệ đã nhập** để tạo ngay lập tức đối tượng chính xác bạn sẽ muốn nhắm đến sau này — xem [Subscriber Tags](/help/subscriber-tags) để xây dựng một phân đoạn từ nó.
- Luôn đọc **Lý do đã bỏ qua (không hợp lệ)** trước khi cho rằng quá trình nhập đã bị lỗi — một vài hàng bị bỏ qua với lý do rõ ràng là điều bình thường đối với hầu hết các danh sách thực tế.
- Chạy lại cùng một tệp là an toàn: những người liên hệ bạn đã nhập trước đó sẽ được xem là trùng lặp lần thứ hai, không được tạo lại.
- Nếu bạn đang tổng hợp một số danh sách nhỏ, hãy gán thẻ mỗi lần nhập khác nhau (ví dụ: `Nhập: Sự kiện Tháng 1`, `Nhập: Hội chợ Thương mại`) để bạn có thể phân biệt chúng sau này ngay cả khi chúng đã được trộn vào danh sách chính của bạn.
- Đối với các danh sách có hơn 5.000 hàng, hãy chia theo một ranh giới rõ ràng (theo thứ tự chữ cái, theo nguồn, hoặc theo ngày thu thập) thay vì một ranh giới tùy ý, để mỗi lô vẫn dễ nhận biết sau này.