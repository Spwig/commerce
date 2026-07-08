---
title: Translation Jobs
---

Translation Jobs tự động hóa việc dịch thuật khối lượng lớn nội dung. Thay vì dịch từng sản phẩm một cách thủ công, hãy tạo một công việc để dịch toàn bộ danh mục sản phẩm của bạn - hoặc các tập con cụ thể - ở phía sau. Các công việc chạy bất đồng bộ, vì vậy bạn có thể tiếp tục làm việc trong khi hàng trăm hoặc hàng nghìn trường được dịch tự động.

Sử dụng công việc dịch thuật khi kích hoạt ngôn ngữ mới, nhập sản phẩm mới hoặc bắt kịp nội dung chưa dịch.

## Những gì là Translation Jobs?

Một công việc dịch thuật là một nhiệm vụ nền tảng thực hiện các chức năng sau:

1. **Quét nội dung** để tìm các trường có thể dịch (sản phẩm, trang, bài đăng blog, v.v.)
2. **Xác định các trường chưa dịch hoặc lỗi thời** dựa trên phạm vi công việc của bạn
3. **Gửi các trường đến bộ máy dịch** (mô hình AI cục bộ hoặc nhà cung cấp bên ngoài)
4. **Lưu trữ các bản dịch** trở lại nội dung của bạn
5. **Báo cáo hoàn thành** với các thống kê về các trường đã dịch

Các công việc chạy thông qua hàng đợi tác vụ Celery, vì vậy chúng không làm chậm giao diện quản trị của bạn.

## Khi nào nên sử dụng Translation Jobs

**Khởi động ngôn ngữ mới**:
- Kích hoạt tiếng Đức là ngôn ngữ mới
- Tạo công việc: Dịch tất cả sản phẩm từ tiếng Anh sang tiếng Đức
- Kết quả: Toàn bộ danh mục có sẵn bằng tiếng Đức trong vài phút/giờ (tùy thuộc vào kích thước)

**Nhập sản phẩm mới**:
- Nhập 500 sản phẩm mới bằng tiếng Anh
- Tạo công việc: Dịch sản phẩm mới sang tất cả các ngôn ngữ đang hoạt động
- Kết quả: Kho hàng mới ngay lập tức có sẵn tại tất cả các thị trường

**Bắt kịp các khoảng trống**:
- Báo cáo phạm vi cho thấy Sản phẩm chỉ được dịch 60% sang tiếng Pháp
- Tạo công việc: Dịch các trường sản phẩm thiếu tiếng Pháp
- Kết quả: Mức độ phủ sóng tiếng Pháp tăng lên ~100%

**Cập nhật các bản dịch lỗi thời**:
- Mô hình dịch thuật đã được cải thiện hoặc có nhà cung cấp mới
- Tạo công việc: Dịch lại tất cả sản phẩm sang tiếng Tây Ban Nha
- Kết quả: Chất lượng bản dịch tiếng Tây Ban Nha cao hơn trong toàn bộ danh mục

## Tạo một công việc dịch thuật

Di chuyển đến **Settings > Translation Jobs** và nhấn **+ Create Job**.

### Cấu hình công việc

**Tên công việc** - Nhãn mô tả (ví dụ: "Dịch sản phẩm sang tiếng Đức", "Bài đăng blog mới - tất cả ngôn ngữ")

**Loại nội dung** - Nội dung cần dịch:
- Sản phẩm
- Danh mục sản phẩm
- Trang
- Bài đăng blog
- SEO metadata
- Mẫu email
- Tất cả loại nội dung

**Ngôn ngữ nguồn** - Ngôn ngữ bạn đang dịch từ (thường là ngôn ngữ mặc định của bạn)

**Ngôn ngữ đích** - Một hoặc nhiều ngôn ngữ để dịch sang (chọn nhiều để dịch song ngữ)

**Phạm vi** - Tập con nội dung nào:
- **Tất cả mục** - Dịch mọi thứ bất kể bản dịch hiện tại
- **Chỉ chưa dịch** - Bỏ qua các trường đã có bản dịch
- **Tạo/đã cập nhật từ ngày** - Chỉ nội dung mới hoặc đã thay đổi gần đây
- **Mục cụ thể** - Chọn các sản phẩm/trang cụ thể (lọc nâng cao)

**Bộ máy dịch** - Dịch vụ nào sẽ được sử dụng:
- Mô hình AI cục bộ (mặc định, không có chi phí API)
- Nhà cung cấp bên ngoài cụ thể (DeepL, Google, Azure, AWS)
- Tự động chọn (sử dụng tùy chọn đã cấu hình)

**Khóa bản dịch** - Liệu các trường đã dịch có bị khóa để không bị ghi đè tự động trong tương lai (hữu ích cho các bản dịch đã được xem xét)

### Tùy chọn nâng cao

**Bỏ qua các trường đã khóa** - Nếu được bật, tôn trọng các bản dịch đã khóa trước đó (khuyến nghị)

**Ghi đè hiện có** - Dịch lại ngay cả khi bản dịch đã tồn tại (sử dụng để cải thiện chất lượng)

**Lọc trường** - Chỉ dịch các trường cụ thể (ví dụ: tên và mô tả sản phẩm, bỏ qua thuộc tính)

**Kích thước lô** - Số lượng mục để xử lý cùng lúc (mặc định: 50, tăng lên nếu máy chủ có thể xử lý để tăng tốc độ)

**Ưu tiên** - Các công việc ưu tiên cao sẽ chạy trước các công việc ưu tiên bình thường (sử dụng thận trọng)

## Chu kỳ sống và trạng thái công việc

Các công việc tiến triển qua các trạng thái sau:

**Đợi xử lý** - Công việc đã được tạo, đang chờ công nhân lấy nó

**Đang xử lý** - Công nhân đang tích cực dịch nội dung

**Hoàn thành** - Tất cả bản dịch đã hoàn tất thành công

**Thất bại** - Công việc gặp lỗi (kiểm tra nhật ký lỗi)

**Hủy bỏ** - Bị dừng lại thủ công bởi quản trị viên

**Tạm dừng** - Tạm dừng tạm thời (có thể tiếp tục)

## Theo dõi tiến độ công việc

Trang chi tiết công việc hiển thị:

**Thanh tiến độ** - Phần trăm hoàn thành

**Thống kê**:
- Tổng số mục cần dịch
- Số mục đã hoàn thành
- Số mục còn lại
- Thời gian ước tính còn lại

**Nhật ký thời gian thực** - Luồng hoạt động dịch thuật (hữu ích để khắc phục sự cố)

**Số lượng lỗi** - Số lượng trường không thể dịch (với lý do)

## Kết quả và thống kê công việc

Khi một công việc hoàn thành, trang kết quả hiển thị:

**Tóm tắt**:
- Tổng số trường đã xử lý
- Bản dịch thành công
- Bản dịch thất bại
- Bỏ qua (đã dịch, khóa hoặc bị loại bởi bộ lọc)

**Phân tích theo từng mục**:
- Những sản phẩm/trang nào đã được dịch
- Số trường mỗi mục
- Bất kỳ lỗi nào đã gặp phải

**Chỉ số hiệu suất**:
- Tổng thời gian trôi qua
- Trung bình bản dịch mỗi giây
- Bộ máy dịch đã sử dụng

## Xử lý bản dịch thất bại

Nếu một số bản dịch thất bại:

**Xem nhật ký lỗi** - Xác định các trường nào đã thất bại và lý do

**Nguyên nhân thất bại phổ biến**:
- Đã đạt giới hạn tỷ lệ API (nhà cung cấp bên ngoài)
- Bộ máy dịch hết thời gian (văn bản rất dài)
- Định dạng trường không hợp lệ (lỗi phân tích JSON)
- Mô hình không hỗ trợ cặp ngôn ngữ

**Lựa chọn thử lại**:
- Sửa vấn đề gốc
- Tạo công việc mới chỉ cho các mục đã thất bại
- Sử dụng bộ máy dịch khác

## Hủy bỏ và tạm dừng công việc

**Hủy bỏ** - Dừng công việc ngay lập tức, loại bỏ bất kỳ bản dịch đang thực hiện nào (bản dịch đã hoàn thành được lưu giữ)

**Tạm dừng** - Dừng công việc tạm thời, có thể tiếp tục sau này từ điểm dừng lại

**Tiếp tục** - Tiếp tục công việc đã tạm dừng

Sử dụng tạm dừng/tiếp tục khi bạn cần giải phóng tài nguyên máy chủ tạm thời.

## Chiến lược công việc theo khối lượng

**Chiến lược 1: Theo ngôn ngữ**:
- Tạo các công việc riêng biệt cho mỗi ngôn ngữ đích
- Dễ theo dõi tiến độ theo từng ngôn ngữ
- Có thể ưu tiên các ngôn ngữ quan trọng
- Phân tán khối lượng theo thời gian

**Chiến lược 2: Tất cả cùng lúc**:
- Một công việc dịch sang tất cả các ngôn ngữ đang hoạt động
- Hoàn thành nhanh hơn tổng thể
- Tải lượng máy chủ cao hơn trong quá trình xử lý
- Quản lý công việc đơn giản hơn

**Chiến lược 3: Theo loại nội dung**:
- Dịch sản phẩm trước (ưu tiên cao nhất)
- Sau đó là danh mục, trang, bài đăng blog
- Cho phép triển khai từng bước
- Dễ kiểm tra và xác minh bản dịch

Chọn dựa trên khả năng máy chủ của bạn, tính khẩn cấp và kích thước danh mục.

## Lịch trình công việc

Lịch trình các công việc lặp lại để xử lý nội dung mới tự động:

**Công việc hàng ngày** - Dịch bất kỳ sản phẩm nào được tạo/cập nhật trong 24 giờ qua

**Công việc hàng tuần** - Bắt kịp bất kỳ khoảng trống dịch thuật hàng tuần

**Sau khi nhập** - Khởi động công việc tự động sau khi nhập sản phẩm theo khối lượng

**Khi kích hoạt ngôn ngữ** - Tự động tạo công việc khi bạn kích hoạt ngôn ngữ mới

Các công việc được lên lịch giữ cho bản dịch luôn cập nhật mà không cần can thiệp thủ công.

## Xét nghiệm hiệu năng

**Mô hình AI cục bộ**:
- ~100-500 bản dịch/giây (tùy thuộc vào máy chủ)
- Tiêu tốn CPU trong quá trình xử lý
- Không có giới hạn tỷ lệ API
- Miễn phí (không có chi phí theo bản dịch)

**Nhà cung cấp bên ngoài**:
- Giới hạn tỷ lệ thay đổi (DeepL: 500k ký tự/tháng trên bản miễn phí)
- Độ trễ API làm tăng chi phí
- Chất lượng tốt hơn nhưng tốn tiền
- Giới hạn yêu cầu đồng thời

**Công việc lớn** (>10.000 trường):
- Chạy vào giờ thấp điểm
- Theo dõi tài nguyên máy chủ
- Xem xét chia nhỏ thành các lô nhỏ hơn
- Thử nghiệm với một phần trước

## Một số mẹo

- **Bắt đầu nhỏ** - Thử nghiệm công việc trên một phần (ví dụ: 10 sản phẩm) trước khi chạy dịch toàn danh mục
- **Sử dụng phạm vi "Chỉ chưa dịch"** - Nhanh hơn và tránh dịch lại nội dung đã tốt
- **Theo dõi công việc đầu tiên chặt chẽ** - Theo dõi lỗi hoặc vấn đề chất lượng trước khi triển khai các công việc lớn hơn
- **Lên lịch công việc trong thời gian ít lưu lượng** - Dịch thuật là tiêu tốn CPU/API
- **Khóa các bản dịch đã xem xét** - Ngăn chặn các công việc theo khối lượng ghi đè các chỉnh sửa thủ công của bạn
- **Giữ công việc tập trung** - Các công việc nhỏ, có mục tiêu rõ ràng dễ khắc phục hơn các công việc "dịch mọi thứ" lớn
- **Kiểm tra mẫu sau khi hoàn thành** - Kiểm tra ngẫu nhiên các bản dịch để đảm bảo chất lượng trước khi coi công việc là thành công
- **Xuất/khởi tạo sao lưu trước các công việc lớn** - Trong trường hợp bạn cần đảo ngược các thay đổi theo khối lượng

Nhớ rằng: Giữ nguyên toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật như đã hiển thị trong các quy tắc bảo tồn.