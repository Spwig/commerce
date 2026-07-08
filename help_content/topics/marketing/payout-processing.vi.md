---
title: Xử lý thanh toán
---

Xử lý thanh toán cho phép bạn thanh toán cho các đại lý của mình những hoa hồng đã được phê duyệt. Hướng dẫn này sẽ hướng dẫn bạn cách tạo, quản lý và xử lý thanh toán qua PayPal hoặc các nhà cung cấp chuyển khoản ngân hàng.

![Danh sách thanh toán](/static/core/admin/img/help/payout-processing/payout-list.webp)

## Tổng quan thanh toán

Một thanh toán là một lô thanh toán nhóm nhiều hoa hồng đã được phê duyệt cho một đại lý duy nhất. Hãy tưởng tượng như là viết một séc cho tất cả các khoản thu nhập còn lại.

Đặc điểm chính:
- **Bao gồm nhiều hoa hồng** — Một thanh toán có thể bao gồm hàng chục hoa hồng đã được phê duyệt
- **Yêu cầu ngưỡng tối thiểu** — Hầu hết các chương trình đều có số tiền thanh toán tối thiểu ($50-$100 phổ biến)
- **Được xử lý qua nhà cung cấp** — PayPal hoặc Airwallex xử lý việc chuyển tiền thực tế
- **Có vòng đời** — Chờ xử lý → Đang xử lý → Hoàn tất (hoặc Thất bại)

## Quy trình thanh toán

Quy trình thanh toán hoàn chỉnh bao gồm 6 bước:

1. **Đại lý kiếm được hoa hồng** — Doanh số được ghi nhận thông qua liên kết theo dõi đại lý
2. **Nhà bán hàng phê duyệt hoa hồng** — Xem xét và phê duyệt các khoản hoa hồng đang chờ xử lý
3. **Số dư đạt ngưỡng tối thiểu** — Số dư đã được phê duyệt của đại lý đạt ngưỡng chương trình
4. **Đại lý yêu cầu thanh toán** — Đại lý gửi yêu cầu thanh toán trong bảng điều khiển của họ
5. **Nhà bán hàng xử lý thanh toán** — Bạn tạo và xử lý thanh toán
6. **Thanh toán hoàn tất** — Nhà cung cấp gửi tiền, các khoản hoa hồng được đánh dấu là đã thanh toán

## Xem thanh toán

Truy cập **Chương trình đại lý > Thanh toán** để truy cập bảng điều khiển quản lý thanh toán.

Bảng thống kê hiển thị:
- **Đang chờ** — Các thanh toán đã được tạo nhưng chưa được xử lý
- **Đang xử lý** — Hiện đang được gửi đến nhà cung cấp thanh toán
- **Hoàn tất** — Đã thanh toán thành công
- **Thất bại** — Thanh toán thất bại (cần được xử lý)

Danh sách hiển thị:
- Tên và mã đại lý
- Số tiền thanh toán
- Phương thức thanh toán (PayPal hoặc Chuyển khoản ngân hàng)
- Biểu tượng trạng thái
- Ngày tạo và hoàn tất
- Nút hành động

Sử dụng bộ lọc để thu hẹp theo:
- Đại lý
- Phương thức thanh toán
- Trạng thái
- Khoảng thời gian

## Tạo thanh toán

Thực hiện theo các bước sau để tạo thanh toán mới:

1. **Truy cập** **Chương trình đại lý > Thanh toán**
2. **Nhấn** nút **+ Thêm thanh toán**
3. **Chọn đại lý** từ danh sách thả xuống
4. **Xem các khoản hoa hồng đã được phê duyệt** — Hệ thống hiển thị tất cả các khoản hoa hồng chưa thanh toán và đã được phê duyệt cho đại lý này
5. **Chọn các khoản hoa hồng để bao gồm** — Chọn các ô kiểm cho các khoản hoa hồng cần thanh toán (thường là tất cả)
6. **Kiểm tra tổng số tiền** — Hệ thống tính toán tổng số tiền tự động
7. **Chọn phương thức thanh toán** — PayPal hoặc Chuyển khoản ngân hàng (dựa trên sở thích của đại lý)
8. **Chọn tài khoản nhà cung cấp** — Chọn tài khoản PayPal/Airwallex nào để sử dụng
9. **Thêm ghi chú** (tùy chọn) — Ghi chú nội bộ để lưu trữ
10. **Nhấn Lưu** — Tạo thanh toán với trạng thái "Đang chờ"

Thanh toán hiện đã sẵn sàng để xử lý.

## Xử lý thanh toán

Bạn có hai tùy chọn để xử lý thanh toán: thủ công hoặc dựa trên nhà cung cấp.

### Xử lý thủ công

Sử dụng xử lý thủ công khi bạn xử lý thanh toán bên ngoài hệ thống (séc, chuyển tiền, v.v.):

1. Chọn thanh toán trong danh sách
2. Nhấn hành động **Đánh dấu là đang xử lý**
3. Hoàn tất thanh toán thông qua phương thức bên ngoài của bạn
4. Trở lại thanh toán
5. Nhấn hành động **Đánh dấu là hoàn tất**
6. Các khoản hoa hồng tự động cập nhật thành trạng thái "Đã thanh toán"

Xử lý thủ công cung cấp tính linh hoạt nhưng yêu cầu nhiều công việc hành chính hơn.

### Xử lý nhà cung cấp (Khuyến nghị)

Xử lý nhà cung cấp tự động hóa thanh toán thông qua PayPal hoặc Airwallex:

1. **Chọn thanh toán (các)** trong danh sách (bạn có thể xử lý nhiều thanh toán)
2. **Nhấn** hành động **Xử lý qua nhà cung cấp**
3. **Xác nhận** trong hộp thoại
4. **Hệ thống xếp hàng công việc** — Công nhân Celery xử lý cuộc gọi API
5. **Nhà cung cấp xử lý thanh toán**:
   - **PayPal**: Gói lên đến 15.000 thanh toán mỗi yêu cầu
   - **Airwallex**: Chuyển khoản ngân hàng cá nhân
6. **Webhook cập nhật trạng thái** — Nhà cung cấp xác nhận hoàn tất
7. **Các khoản hoa hồng được đánh dấu là đã thanh toán** — Hệ thống cập nhật tất cả các khoản hoa hồng được bao gồm

Xử lý nhà cung cấp nhanh hơn, đáng tin cậy hơn và tạo ra hồ sơ kiểm toán tự động.

## Phương thức thanh toán

Spwig hỗ trợ hai phương thức thanh toán với các yêu cầu khác nhau:

| Phương thức | Nhà cung cấp | Yêu cầu | Thời gian xử lý | Phí | Tốt nhất cho |
|-------------|-------------|---------|----------------|-----|--------------|
| **PayPal** | PayPal Payouts | Đại lý phải có địa chỉ `payment_email` hợp lệ | 1-2 ngày làm việc | ~2% hoặc $0.25-$1.00 mỗi thanh toán | Hầu hết các đại lý, phạm vi toàn cầu |
| **Chuyển khoản ngân hàng** | Airwallex | Chi tiết tài khoản ngân hàng (số tài khoản, định tuyến, SWIFT) | 2-5 ngày làm việc | Thay đổi theo quốc gia | Đại lý quốc tế, số tiền lớn |

Đại lý cấu hình phương thức thanh toán và chi tiết của họ trong bảng điều khiển của họ. Hệ thống tự động chọn nhà cung cấp phù hợp dựa trên sở thích của họ.

### Logic lựa chọn phương thức thanh toán

Khi xử lý thanh toán, Spwig chọn nhà cung cấp như sau:

1. Kiểm tra phương thức thanh toán ưa thích của đại lý (PayPal hoặc Chuyển khoản ngân hàng)
2. Phối hợp với tài khoản nhà cung cấp đã cấu hình (PayPal → PayPal, Chuyển khoản → Airwallex)
3. Nếu không có sở thích, quay lại nhà cung cấp đầu tiên có sẵn
4. Hiển thị lỗi nếu không có nhà cung cấp nào được cấu hình

## Luồng trạng thái thanh toán

Hiểu rõ các trạng thái thanh toán giúp bạn theo dõi tiến trình thanh toán:

| Trạng thái | Ý nghĩa | Hành động tiếp theo |
|------------|--------|---------------------|
| **Đang chờ** | Đã tạo nhưng chưa gửi đến nhà cung cấp | Xử lý qua nhà cung cấp hoặc đánh dấu là đang xử lý |
| **Đang xử lý** | Đã gửi đến nhà cung cấp thanh toán, đang chờ xác nhận | Chờ webhook hoặc kiểm tra bảng điều khiển nhà cung cấp |
| **Hoàn tất** | Thanh toán thành công, tiền đã được gửi | Không có hành động — các khoản hoa hồng được đánh dấu là đã thanh toán |
| **Thất bại** | Thanh toán thất bại (xem chi tiết lỗi) | Xem xét lỗi, sửa vấn đề, thử lại hoặc hủy bỏ |
| **Đã hủy bỏ** | Bị hủy bỏ thủ công trước khi hoàn tất | Không có hành động — các khoản hoa hồng vẫn chưa được thanh toán |

### Đường dẫn thành công

Đang chờ → Đang xử lý → Hoàn tất

Đây là đường dẫn lý tưởng. Webhook của nhà cung cấp sẽ tự động cập nhật trạng thái khi thanh toán được thực hiện.

### Đường dẫn thất bại

Đang chờ → Đang xử lý → Thất bại

Khi thanh toán thất bại, trạng thái thanh toán thay đổi thành Thất bại và bạn phải điều tra.

## Xử lý thanh toán thất bại

Các thanh toán thất bại yêu cầu can thiệp thủ công. Các nguyên nhân thất bại phổ biến:

| Nguyên nhân | Lỗi nhà cung cấp | Giải pháp |
|------------|------------------|----------|
| Tài khoản không hợp lệ | "Tài khoản người nhận không tìm thấy" | Xác minh địa chỉ email thanh toán hoặc chi tiết ngân hàng của đại lý |
| Số dư không đủ | "Tiền không đủ" | Thêm tiền vào tài khoản nhà cung cấp của bạn |
| Lỗi chi tiết ngân hàng | "Số định tuyến không hợp lệ" | Yêu cầu đại lý cập nhật thông tin ngân hàng |
| Tài khoản bị hạn chế | "Người nhận không thể nhận thanh toán" | Liên hệ đại lý để giải quyết tình trạng tài khoản của họ |
| Vấn đề nhà cung cấp | "Dịch vụ tạm thời không khả dụng" | Chờ và thử lại sau vài giờ |

### Cách thử lại thanh toán thất bại

1. **Xem thanh toán thất bại** — Nhấn vào thanh toán trong danh sách
2. **Đọc thông báo lỗi** — Kiểm tra trường **Phản hồi nhà cung cấp** để xem chi tiết
3. **Sửa vấn đề gốc** — Cập nhật chi tiết đại lý, thêm tiền vào tài khoản nhà cung cấp, v.v.
4. **Đặt lại trạng thái** — Thay đổi trạng thái trở lại **Đang chờ** (bảng biểu chỉnh sửa)
5. **Xử lý lại** — Sử dụng hành động **Xử lý qua nhà cung cấp**

### Cách hủy bỏ và tạo lại

Nếu việc thử lại không hoạt động:

1. **Mở thanh toán thất bại**
2. **Thay đổi trạng thái thành Đã hủy bỏ**
3. **Lưu thanh toán**
4. **Tạo thanh toán mới** — Thực hiện lại các bước tạo thanh toán
5. **Xử lý thanh toán mới**

Các thanh toán bị hủy bỏ không đánh dấu các khoản hoa hồng là đã thanh toán, do đó chúng vẫn đủ điều kiện để tạo thanh toán mới.

## Tích hợp nhà cung cấp thanh toán

Xử lý thanh toán yêu cầu tài khoản nhà cung cấp thanh toán được cấu hình. Spwig tích hợp với:

- **API thanh toán PayPal** — Cho các thanh toán PayPal
- **Airwallex** — Cho các chuyển khoản ngân hàng quốc tế

### Yêu cầu thiết lập

Trước khi xử lý thanh toán:
1. Cấu hình ít nhất một nhà cung cấp trong **Cài đặt > Nhà cung cấp thanh toán**
2. Thêm thông tin xác thực API (Client ID, Secret, API Key)
3. Đặt chế độ sản xuất (sandbox để kiểm tra)
4. Cấu hình URL webhook trong bảng điều khiển nhà cung cấp
5. Kiểm tra kết nối bằng cách sử dụng thanh toán thử nghiệm

Xem hướng dẫn [Thiết lập nhà cung cấp thanh toán](#) để biết các hướng dẫn cấu hình chi tiết.

### Lựa chọn nhà cung cấp bởi đại lý

Đại lý chọn phương thức thanh toán ưa thích của họ trong bảng điều khiển:
- PayPal: Nhập `payment_email`
- Chuyển khoản ngân hàng: Nhập chi tiết tài khoản ngân hàng

Hệ thống tự động định tuyến thanh toán đến nhà cung cấp phù hợp.

## Kế hoạch thanh toán tốt nhất

Thiết lập lịch thanh toán định kỳ để xây dựng lòng tin với đại lý:

| Kế hoạch | Tần suất | Mức độ công việc | Mức độ hài lòng của đại lý | Khuyến nghị cho |
|----------|-----------|------------------|---------------------------|------------------|
| Tuần lễ | Mỗi thứ Sáu | Cao | Tuyệt vời | Chương trình mới, khối lượng cao |
| Hai tuần một lần | Ngày 1 và 15 | Trung bình | Tốt | Chương trình khối lượng trung bình |
| Tháng | Ngày 1 của tháng | Thấp | Chấp nhận được | Chương trình đã thiết lập |
| Quý | Mỗi 3 tháng | Rất thấp | Kém | Không khuyến nghị |

Hãy cân nhắc quy mô chương trình và khả năng hành chính của bạn khi chọn kế hoạch.

## Hướng dẫn xử lý tốt nhất

Theo dõi các hướng dẫn sau để đảm bảo hoạt động thanh toán diễn ra suôn sẻ:

- **Nhóm thanh toán theo lịch trình** — Xử lý tất cả các thanh toán đủ điều kiện cùng ngày mỗi tuần/tháng
- **Kiểm tra lại thông tin trước khi xử lý** — Kiểm tra lại thông tin thanh toán của đại lý, đặc biệt là với các khoản lớn
- **Theo dõi số dư nhà cung cấp** — Đảm bảo số dư đủ trong tài khoản PayPal/Airwallex của bạn
- **Thiết lập ngưỡng tối thiểu rõ ràng** — Truyền đạt số tiền thanh toán tối thiểu trong điều khoản chương trình ($50-$100 phổ biến)
- **Ghi lại lịch trình thanh toán** — Thêm lịch trình thanh toán vào điều khoản đại lý và cài đặt cổng thông tin
- **Sử dụng xử lý nhà cung cấp** — Tránh xử lý thủ công trừ khi thực sự cần thiết
- **Kiểm tra các thanh toán thất bại ngay lập tức** — Xử lý các lỗi trong vòng 24 giờ
- **Giữ các webhook nhà cung cấp được cấu hình** — Webhook cho phép cập nhật trạng thái tự động
- **Xuất báo cáo thanh toán định kỳ** — Tải xuống báo cáo hàng tháng cho kế toán

## hồ sơ thanh toán và báo cáo

Mỗi thanh toán tạo ra một bản ghi không thể thay đổi với:
- Thông tin đại lý
- Các ID hoa hồng được bao gồm
- Tổng số tiền
- Phương thức và nhà cung cấp thanh toán
- Thời gian tạo và hoàn tất
- ID giao dịch nhà cung cấp (sau khi xử lý)
- Dữ liệu phản hồi nhà cung cấp (để gỡ lỗi)
- Ghi chú nội bộ

Truy cập dữ liệu này bằng cách nhấn vào bất kỳ thanh toán nào trong danh sách. Sử dụng tính năng xuất dữ liệu từ giao diện quản trị để tải xuống báo cáo thanh toán cho mục đích kế toán hoặc thuế.

## Một số mẹo

- Xử lý thanh toán theo lịch trình cố định (ví dụ: thứ Sáu hàng tuần lúc 2 giờ chiều) để đại lý biết khi nào họ có thể mong đợi thanh toán.
- Luôn sử dụng xử lý nhà cung cấp thay vì xử lý thủ công — nó nhanh hơn, đáng tin cậy hơn và tạo hồ sơ kiểm toán tốt hơn.
- Thiết lập ngưỡng thanh toán tối thiểu trong chương trình của bạn để giảm bớt công việc hành chính — $50 hoặc $100 là tiêu chuẩn.
- Theo dõi số dư tài khoản nhà cung cấp trước khi xử lý các lô lớn để tránh thất bại.
- Kiểm tra tích hợp thanh toán của bạn trong chế độ sandbox trước khi chuyển sang thanh toán thực tế.
- Thêm ghi chú cho mỗi thanh toán để giải thích giai đoạn mà nó bao phủ (ví dụ: "Hoa hồng cho tháng 1 năm 2026").
- Kiểm tra các thanh toán thất bại ngay lập tức — sự chậm trễ làm phiền đại lý và làm tổn hại lòng tin.
- Truyền đạt sự chậm trễ một cách chủ động — nếu bạn không thể xử lý đúng hạn, hãy thông báo cho các đại lý bị ảnh hưởng trước.

