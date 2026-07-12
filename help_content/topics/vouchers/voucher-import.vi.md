---
title: Nhập hàng loạt mã phiếu giảm giá
---

Chuyên gia nhập mã phiếu giảm giá cho phép bạn tạo hàng trăm mã phiếu giảm giá cùng lúc bằng cách tải lên tệp CSV hoặc XLSX. Điều này lý tưởng khi bạn có mã đã in sẵn, mã chương trình khách hàng trung thành từ hệ thống bên thứ ba, hoặc đơn giản là cần triển khai chiến dịch lớn mà không cần thêm từng mã thủ công.

![Danh sách phiếu giảm giá với nút Nhập](/static/core/admin/img/help/voucher-import/voucher-list-import-button.webp)

## Bắt đầu nhập

Truy cập **Marketing > Voucher** và nhấp vào nút **Nhập** ở góc trên bên phải của trang. Điều này mở ra trình hướng dẫn nhập ba bước.

## Bước 1: Tải tệp của bạn và đặt cài đặt theo lô

![Biểu mẫu tải lên nhập](/static/core/admin/img/help/voucher-import/import-upload.webp)

Trang đầu tiên có hai phần: tải tệp và cài đặt giảm giá theo lô.

### Chuẩn bị tệp của bạn

Tải lên tệp `.csv` hoặc `.xlsx` lên đến 5 MB. Tệp phải có hàng tiêu đề làm hàng đầu tiên. Yêu cầu tối thiểu là một cột chứa mã phiếu giảm giá — mọi cột khác là tùy chọn.

Chuyên gia nhập nhận biết tự động các tên cột phổ biến. Nếu tệp của bạn sử dụng bất kỳ tên nào dưới đây, Spwig sẽ chọn sẵn ánh xạ đúng trên trang tiếp theo mà không cần nhấp thêm:

| Tên cột của bạn | Ánh xạ đến |
|-----------------|-----------|
| `code`, `voucher_code`, `coupon_code`, `promo_code` | Mã phiếu giảm giá |
| `name`, `title`, `campaign` | Tên nội bộ |
| `description`, `details`, `note` | Mô tả dành cho khách hàng |
| `external_id`, `member_id`, `reference` | ID bên ngoài |

**Lưu ý:** Tải xuống mẫu XLSX trước (xem [Xuất phiếu giảm giá dưới dạng mẫu](#exporting-vouchers-as-a-template) bên dưới) — nó sử dụng chính xác tên cột mà chuyên gia nhập kỳ vọng, vì vậy ánh xạ cột sẽ tự động.

### Giới hạn tệp

- Kích thước tệp tối đa: **5 MB**
- Số hàng tối đa mỗi lần nhập: **5.000 mã**

### Đặt cài đặt giảm giá theo lô

Mỗi phiếu giảm giá trong lô sẽ chia sẻ cùng một cài đặt giảm giá mà bạn cấu hình trên trang này. Điền các trường như bạn sẽ làm khi tạo một phiếu giảm giá đơn lẻ:

**Phần giảm giá**

| Trường | Mô tả |
|-------|-------------|
| **Loại giảm giá** | Phần trăm, Số tiền cố định hoặc Miễn phí vận chuyển |
| **Giá trị giảm giá** | Phần trăm (0–100) hoặc số tiền cố định được khấu trừ |
| **Giá trị giảm giá tối đa** | Giới hạn tùy chọn cho các khoản giảm giá theo phần trăm (ví dụ: giới hạn giảm 20% ở mức 50 đô la) |
| **Phạm vi áp dụng** | Toàn bộ giỏ hàng, Sản phẩm cụ thể hoặc Danh mục cụ thể |

**Phần hiệu lực**

| Trường | Mô tả |
|-------|-------------|
| **Ngày bắt đầu** | Thời điểm mã trở nên hoạt động (mặc định là ngay bây giờ nếu để trống) |
| **Ngày kết thúc** | Thời điểm mã hết hạn (để trống để không có ngày hết hạn) |
| **Số ngày hiệu lực** | Một lựa chọn thay thế cho ngày kết thúc — mã hết hạn sau số ngày này kể từ khi tạo |

**Phần giới hạn sử dụng**

| Trường | Mô tả |
|-------|-------------|
| **Số lần sử dụng tối đa tổng cộng** | Tổng số lần đổi quà được phép cho tất cả khách hàng (trống = không giới hạn) |
| **Số lần sử dụng tối đa mỗi khách hàng** | Số lần một khách hàng có thể sử dụng bất kỳ mã nào từ lô này |
| **Giá trị đơn hàng tối thiểu** | Tổng giá trị giỏ hàng tối thiểu cần thiết trước khi mã được áp dụng |

**Giới hạn**

Kiểm tra bất kỳ sự kết hợp nào sau đây:
- **Không áp dụng cho sản phẩm đang giảm giá** — ngăn mã chồng lên các sản phẩm đã được giảm giá
- **Không thể kết hợp với các phiếu giảm giá khác** — ngăn khách hàng sử dụng hai mã trên cùng một đơn hàng
- **Không thể kết hợp với sản phẩm đang giảm giá** — tương tự như trên nhưng nhắm đến các sản phẩm có giá giảm
- **Chỉ dành cho khách hàng mới** — giới hạn mã chỉ dành cho khách hàng không có đơn hàng hoàn thành trước đó
- **Kích hoạt ngay lập tức** — để chọn nếu bạn muốn mã trở nên hoạt động ngay khi được nhập

Khi bạn hài lòng với các cài đặt, nhấp **Tiếp tục để xem trước**.

## Bước 2: Ánh xạ cột và xem trước

![Trang ánh xạ cột và xem trước](/static/core/admin/img/help/voucher-import/import-preview.webp)

Trang xem trước hiển thị bốn bộ đếm tổng kết ở phía trên:

- **Dòng được phân tích** — tổng số dòng dữ liệu được tìm thấy trong tệp của bạn

- **Sẽ nhập** — mã mới sẽ được tạo

- **Duplicat** — mã đã tồn tại trong danh mục của bạn

- **Sẽ bỏ qua (không hợp lệ)** — các dòng bị từ chối do lỗi xác thực (mã trống, mã quá dài, v.v.)

### Ánh xạ cột

Bảng **Ánh xạ cột** cho phép bạn chỉ định Spwig cột nào trong tệp của bạn tương ứng với từng trường voucher. Spwig tự động phát hiện tên tiêu đề phổ biến (xem bảng trên), nhưng bạn có thể thay đổi bất kỳ ánh xạ nào bằng cách sử dụng danh sách thả xuống trên mỗi dòng.

Chỉ cột **Mã voucher** là bắt buộc. Các trường khác — **Tên nội bộ**, **Mô tả dành cho khách hàng**, và **ID bên ngoài** — là tùy chọn. Nếu bạn bỏ qua chúng, Spwig sẽ sử dụng các giá trị mặc định hợp lý (tên nội bộ mặc định là "Voucher được nhập {code}").

### Chiến lược mã trùng lặp

Nếu có mã nào trong tệp của bạn đã tồn tại trong danh mục của bạn, bạn phải chọn cách xử lý chúng:

| Chiến lược | Điều gì sẽ xảy ra |

|----------|-------------|

| **Bỏ qua các mã trùng lặp** | Các mã hiện có sẽ được giữ nguyên. Chỉ có các mã mới được tạo. |

| **Ghi đè cài đặt** | Các mã hiện có sẽ được cập nhật với cài đặt giảm giá của lô này. Mã, số lần sử dụng và ngày tạo của chúng được giữ nguyên. |

| **Thất bại khi nhập** | Toàn bộ quá trình nhập sẽ bị hủy nếu tìm thấy ít nhất một mã trùng lặp. Sử dụng tùy chọn này khi bạn cần đảm bảo rằng không mã hiện có nào bị ảnh hưởng. |

Bất kỳ mã trùng lặp nào được tìm thấy sẽ được liệt kê trong một bảng điều khiển có thể mở rộng để bạn xem xét trước khi đưa ra quyết định.

### Bảng xem trước dữ liệu

Phần cuối trang hiển thị 20 dòng đầu tiên của tệp của bạn để bạn xác nhận ánh xạ cột trông chính xác trước khi xác nhận. Các dòng khớp với mã hiện có được đánh dấu nổi bật.

Khi mọi thứ trông ổn, hãy nhấp **Nhập N voucher** để xác nhận lô.

## Bước 3: Xem lại kết quả

![Trang kết quả nhập](/static/core/admin/img/help/voucher-import/import-result.webp)

Sau khi quá trình nhập hoàn tất, bạn sẽ thấy một bản tóm tắt hiển thị:

- **Đã nhập** — mã đã được tạo thành công

- **Đã bỏ qua** — mã không được tạo (mã trùng lặp hoặc dòng không hợp lệ)

- **Dòng được xử lý** — tổng số dòng từ tệp của bạn đã được đánh giá

- **Thất bại** — các dòng gặp lỗi bất ngờ

Nhấp **Xem các voucher đã nhập** để mở danh sách voucher được lọc chỉ hiển thị các mã từ lô này, giúp bạn dễ dàng kiểm tra kết quả hoặc kích hoạt hàng loạt các mã mới.

Nếu có điều gì đó trông sai — ví dụ như loại giảm giá không đúng được áp dụng — bạn có thể sử dụng chiến lược **Ghi đè cài đặt** trên lần nhập lại để sửa lô mà không cần xóa và tạo lại các mã.

Nhấp **Nhập một lô khác** để bắt đầu tải lên mới, hoặc **Quay lại danh sách voucher** để trở lại danh mục đầy đủ của bạn.

## Xuất voucher dưới dạng mẫu

Danh sách voucher hỗ trợ hành động xuất XLSX tạo ra một tệp với đúng thứ tự cột mà trình nhập kỳ vọng. Đây là cách dễ nhất để nhận được một mẫu được định dạng chính xác:

1. Di chuyển đến **Marketing > Voucher**

2. Chọn các voucher bạn muốn xuất (hoặc chọn tất cả)

3. Chọn **Xuất các voucher đã chọn thành XLSX** từ danh sách thả xuống **Hành động**

4. Nhấp **Tiến hành**

Tệp được tải xuống có tất cả 21 cột mà trình nhập hiểu, bao gồm các trường là cấp lô trong trình hướng dẫn nhập (loại giảm giá, ngày tháng, giới hạn sử dụng, v.v.). Bạn có thể sử dụng tệp này làm tài liệu tham khảo hoặc đưa các mã hiện có của bạn qua chu trình chỉnh sửa → nhập lại bằng chiến lược **Ghi đè cài đặt**.

## Mẹo

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- Tải xuống tệp XLSX xuất trước để sử dụng làm mẫu — tên cột đã được định dạng sẵn để ánh xạ tự động có thể nhận ra chúng mà không cần điều chỉnh trên trang xem trước.
- Chạy một lô nhỏ gồm 5–10 mã trước khi nhập hàng trăm mã để kiểm tra xem cài đặt ánh xạ cột và cài đặt lô của bạn có đúng không.
- Sử dụng **Days valid** thay vì ngày kết thúc cố định **End date** khi mã sẽ được phân phối theo thời gian — lúc đó ngày hết hạn của mỗi mã sẽ được tính từ thời điểm nó được nhập thay vì một ngày cụ thể trong lịch.
- Nếu bạn nhận mã từ hệ thống trung thành bên thứ ba, ánh xạ mã thành viên hoặc mã khách hàng của nhà cung cấp đến cột **External ID** để bạn có thể đối chiếu việc đổi mã sau này.
- Sau khi nhập lớn, nhấp vào **View imported vouchers** trên trang kết quả để lọc danh sách chỉ hiển thị lô mới — bạn có thể chỉnh sửa theo nhóm, kích hoạt hoặc vô hiệu hóa chúng.
- Một lần nhập thất bại (sử dụng chiến lược **Fail** cho bản sao) sẽ không làm thay đổi danh mục của bạn, vì vậy an toàn để sửa tệp và thử lại nhiều lần nếu cần.