---
title: Các Hành Động Đa Sản Phẩm
---

Danh sách **Sản phẩm** cho phép bạn thực hiện các hành động trên nhiều sản phẩm cùng lúc thay vì mở từng sản phẩm một. Từ **Các Hành Động Đa** trong thanh công cụ phía trên lưới sản phẩm, bạn có thể xuất bản hoặc hủy xuất bản sản phẩm, làm nổi bật hoặc bỏ nổi bật chúng, xuất dữ liệu dưới dạng CSV, kiểm tra xem những sản phẩm nào đã sẵn sàng cho vận chuyển quốc tế, hoặc xóa chúng — tất cả trong một bước duy nhất.

Đến với **Sản phẩm > Tất cả sản phẩm** để sử dụng các hành động này.

![Thanh công cụ danh sách Sản phẩm với ba thẻ sản phẩm được chọn và hộp thả xuống Các Hành Động Đa hiển thị mọi tùy chọn, bao gồm Xuất Dữ Liệu Hải Quan (CSV) và Kiểm Tra Tính Sẵn Sàng Vận Chuyển Quốc Tế](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Thực Hiện Một Hành Động Đa

1. Sử dụng bảng lọc hoặc ô **Tìm kiếm** để thu hẹp danh sách sản phẩm bạn muốn, nếu cần
2. Chọn ô ở góc trên cùng bên trái của mỗi thẻ sản phẩm bạn muốn bao gồm — thanh **Các Hành Động Đa** sẽ hiển thị số lượng sản phẩm được chọn
3. Chọn một hành động từ hộp thả xuống **Các Hành Động Đa**
4. Nhấn **Áp Dụng**

Các hành động thay đổi hoặc xuất dữ liệu sẽ được thực hiện ngay; **Xóa Các Sản Phẩm Được Chọn** yêu cầu bạn xác nhận trước, vì đây là hành động duy nhất ở đây mà bạn không thể dễ dàng hủy bỏ từ danh sách bản thân nó.

## Các Hành Động Có Sẵn

| Hành Động | Mô tả | 
|--------|---------------| 
| **Đánh Dấu Là Đã Xuất Bản** | Thiết lập trạng thái của các sản phẩm được chọn thành **Đã Xuất Bản** để chúng hiển thị trên cửa hàng. | 
| **Đánh Dấu Là Bản Nháp** | Thiết lập trạng thái của các sản phẩm được chọn thành **Bản Nháp**, ẩn chúng khỏi cửa hàng khi bạn tiếp tục chỉnh sửa. | 
| **Đánh Dấu Là Sản Phẩm Nổi Bật** | Kích hoạt **Là Sản Phẩm Nổi Bật** trên các sản phẩm được chọn. | 
| **Bỏ Đánh Dấu Nổi Bật** | Tắt **Là Sản Phẩm Nổi Bật** trên các sản phẩm được chọn. | 
| **Xuất Sang CSV** | Tải xuống tệp CSV chứa ID, tên, SKU, trạng thái, cờ nổi bật và giá của các sản phẩm được chọn. | 
| **Xuất Dữ Liệu Hải Quan (CSV)** | Tải xuống tệp CSV chứa thông tin hải quan cho các sản phẩm được chọn. Xem dưới đây. | 
| **Kiểm Tra Tính Sẵn Sàng Vận Chuyển Quốc Tế** | Hiển thị bản tóm tắt những sản phẩm được chọn có dữ liệu hải quan cần thiết cho vận chuyển quốc tế hay không. Xem dưới đây. | 
| **Xóa Các Sản Phẩm Được Chọn** | Di chuyển các sản phẩm được chọn đến thùng rác, sau khi xác nhận. | 

## Xuất Dữ Liệu Hải Quan (CSV)

Sử dụng chức năng này khi bạn cần một tờ khai hải quan để giao cho người vận chuyển, công ty chuyển phát nhanh hoặc đại lý hải quan — ví dụ, trước khi gửi một lô hàng quốc tế lớn, hoặc khi thiết lập một nhà khai thác mới yêu cầu mã HS và dữ liệu nguồn gốc trước.

Chọn các sản phẩm, chọn **Xuất Dữ Liệu Hải Quan (CSV)** từ hộp thả xuống, và nhấn **Áp Dụng**. Spwig tải xuống tệp có tên `product_customs_data.csv` với mỗi hàng tương ứng với một sản phẩm và các cột sau:

| Cột | Nguồn | 
|--------|--------| 
| **SKU** | SKU của sản phẩm | 
| **Tên** | Tên sản phẩm | 
| **Mã HS** | Mã phân loại Hệ thống Tổng hợp | 
| **Quốc Gia Nguồn Gốc** | Nơi sản phẩm được sản xuất | 
| **Giá Đơn Vị Hải Quan** | Giá trị khai báo cho mỗi đơn vị cho hải quan | 
| **Giấy Phép Xuất Khẩu** | Số giấy phép xuất khẩu, nếu sản phẩm yêu cầu giấy phép | 
| **Ngày Hết Hạn Giấy Phép** | Ngày hết hạn giấy phép xuất khẩu, nếu có | 
| **Sẵn Sàng Vận Chuyển Quốc Tế** | `Có` hoặc `Không` — xem liệu sản phẩm có dữ liệu tối thiểu cần thiết cho vận chuyển quốc tế hay không (xem dưới đây) | 

Các trường này đến từ phần **Vận Chuyển Quốc Tế / Hải Quan** trong biểu mẫu sản phẩm. Nếu một sản phẩm thiếu một trong số chúng, cột tương ứng sẽ để trống trong tệp xuất — hãy điền đầy đủ dữ liệu cho sản phẩm trước khi bạn dựa vào tệp này cho một lô hàng thực tế.

## Kiểm Tra Tính Sẵn Sàng Vận Chuyển Quốc Tế

Sử dụng chức năng này để kiểm tra một loạt sản phẩm trước khi bạn bắt đầu vận chuyển chúng quốc tế, mà không cần mở từng sản phẩm một hoặc đợi đầy đủ tệp CSV xuất.

Chọn các sản phẩm, chọn **Kiểm Tra Tính Sẵn Sàng Vận Chuyển Quốc Tế**, và nhấn **Áp Dụng**. Spwig kiểm tra mỗi sản phẩm được chọn dựa trên ba trường được yêu cầu — **Mã HS**, **Quốc Gia Nguồn Gốc**, và **Giá Đơn Vị Hải Quan** — và hiển thị một thông báo tóm tắt kết quả:

- Nếu tất cả các sản phẩm đã chọn đều có đủ ba trường, bạn sẽ thấy thông báo xác nhận rằng tất cả đều sẵn sàng.
- Nếu một số sản phẩm thiếu dữ liệu, thông báo sẽ báo cáo số lượng sản phẩm đã sẵn sàng và số lượng chưa sẵn sàng, đồng thời liệt kê từng sản phẩm chưa sẵn sàng cùng với các trường bị thiếu (ví dụ: "Ly Gốm Xanh (thiếu: hs_code, country_of_origin)").

Nếu hơn 10 sản phẩm thiếu dữ liệu, thông báo sẽ liệt kê 10 sản phẩm đầu tiên và cho biết còn bao nhiêu sản phẩm khác.

Hành động này chỉ đọc dữ liệu — nó không thay đổi bất kỳ điều gì trên các sản phẩm, vì vậy bạn có thể chạy nó thường xuyên tùy ý trong khi đang điền thông tin hải quan cho toàn bộ danh mục của mình.

**Số Giấy Phép Xuất Khẩu** và **Ngày Hết Hạn Giấy Phép Xuất Khẩu** không phải là một phần của kiểm tra độ sẵn sàng. Chúng chỉ áp dụng cho các mặt hàng được kiểm soát hoặc hạn chế, vì vậy một sản phẩm có thể "sẵn sàng" cho việc vận chuyển quốc tế mà không cần chúng.

## Mẹo

- Chạy **Kiểm Tra Độ Sẵn Sàng Vận Chuyển Quốc Tế** trên toàn bộ danh mục (hoặc từng danh mục một) trước đơn hàng quốc tế đầu tiên của bạn — nó nhanh hơn nhiều so với việc phát hiện mã HS bị thiếu khi lô hàng đã ở biên giới.
- Giữ **Dữ Liệu Hải Quan Xuất Khẩu (CSV)** để cung cấp cho các đại lý và nhà vận chuyển, và **Kiểm Tra Độ Sẵn Sàng Vận Chuyển Quốc Tế** cho danh sách kiểm tra nội bộ của bạn — CSV là một bản ghi, còn kiểm tra độ sẵn sàng là một danh sách việc cần làm.
- Điền **Mã HS**, **Quốc Gia Xuất Xứ** và **Đơn Giá Hải Quan** trên biểu mẫu sản phẩm (dưới **Vận Chuyển Quốc Tế / Hải Quan**) khi bạn thêm các sản phẩm mới, để bạn không phải làm việc hàng loạt sau này.
- Lưới sản phẩm tự động tải thêm sản phẩm khi bạn cuộn xuống (cuộn vô hạn), và các lựa chọn hộp kiểm của bạn được giữ nguyên khi các sản phẩm mới được tải vào — vì vậy bạn có thể cuộn để xây dựng một lựa chọn lớn trước khi áp dụng một hành động. Tuy nhiên, việc thay đổi bộ lọc hoặc tải lại trang sẽ xóa lựa chọn của bạn, vì vậy hãy áp dụng hành động trước khi điều chỉnh bộ lọc.
- **Đánh Dấu Là Bản Nháp** là một cách nhanh chóng để gỡ nhiều sản phẩm khỏi cửa hàng trực tuyến cùng một lúc — ví dụ, trước khi kiểm kê lại hàng tồn kho — mà không thay đổi bất kỳ điều gì khác về chúng.
