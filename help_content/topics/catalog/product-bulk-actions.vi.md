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
4. Nhấn **Áp dụng**

Các hành động thay đổi hoặc xuất dữ liệu sẽ được thực hiện ngay; **Xóa Các Sản Phẩm Được Chọn** yêu cầu bạn xác nhận trước, vì đây là hành động duy nhất ở đây mà bạn không thể dễ dàng hủy bỏ từ danh sách bản thân nó.

## Các Hành Động Có Sẵn

| Hành Động | Điều mà nó làm | 
|--------|---------------| 
| **Đánh Dấu Là Đã Xuất Bản** | Thiết lập trạng thái của các sản phẩm được chọn thành **Đã Xuất Bản** để chúng hiển thị trên cửa hàng. | 
| **Đánh Dấu Là Bản Nháp** | Thiết lập trạng thái của các sản phẩm được chọn thành **Bản Nháp**, ẩn chúng khỏi cửa hàng khi bạn tiếp tục chỉnh sửa. | 
| **Đánh Dấu Là Sản Phẩm Nổi Bật** | Kích hoạt **Được Đặc Biệt** trên các sản phẩm được chọn. | 
| **Bỏ Đánh Dấu Là Sản Phẩm Nổi Bật** | Tắt **Được Đặc Biệt** trên các sản phẩm được chọn. | 
| **Xuất Sang CSV** | Tải xuống một tệp CSV chứa ID, tên, SKU, trạng thái, cờ nổi bật và giá của các sản phẩm được chọn. | 
| **Xuất Dữ Liệu Hải Quan (CSV)** | Tải xuống một tệp CSV chứa thông tin hải quan cho các sản phẩm được chọn. Xem bên dưới. | 
| **Kiểm Tra Tính Sẵn Sàng Vận Chuyển Quốc Tế** | Hiển thị bản tóm tắt những sản phẩm được chọn có dữ liệu hải quan cần thiết cho việc vận chuyển quốc tế không. Xem bên dưới. | 
| **Xóa Các Sản Phẩm Được Chọn** | Di chuyển các sản phẩm được chọn đến thùng rác, sau khi xác nhận. | 

## Xuất Dữ Liệu Hải Quan (CSV)

Sử dụng điều này khi bạn cần một tờ khai hải quan để giao cho người vận chuyển, công ty chuyển phát nhanh hoặc đại lý hải quan — ví dụ, trước khi gửi một lô hàng quốc tế lớn, hoặc khi thiết lập một nhà khai thác mới yêu cầu mã HS và dữ liệu nguồn gốc trước.

Chọn các sản phẩm, chọn **Xuất Dữ Liệu Hải Quan (CSV)** từ hộp thả xuống, và nhấn **Áp dụng**. Spwig tải xuống một tệp có tên `product_customs_data.csv` với một hàng cho mỗi sản phẩm và các cột sau:

| Cột | Nguồn | 
|--------|--------| 
| **SKU** | SKU của sản phẩm | 
| **Tên** | Tên sản phẩm | 
| **Mã HS** | Mã phân loại Hệ thống Tổng hợp | 
| **Quốc Gia Sản Xuất** | Nơi sản phẩm được sản xuất | 
| **Giá Đơn Vị Hải Quan** | Giá trị khai báo cho mỗi đơn vị cho hải quan | 
| **Giấy Phép Xuất Khẩu** | Số giấy phép xuất khẩu, nếu sản phẩm yêu cầu | 
| **Ngày Hết Hạn Giấy Phép** | Ngày hết hạn giấy phép xuất khẩu, nếu có | 
| **Sẵn Sàng Quốc Tế** | `Có` hoặc `Không` — xem xét xem sản phẩm có dữ liệu tối thiểu cần thiết cho vận chuyển quốc tế không (xem dưới đây) | 

Các trường này đến từ phần **Vận Chuyển Quốc Tế / Hải Quan** trong biểu mẫu sản phẩm. Nếu một sản phẩm thiếu một trong số chúng, cột tương ứng sẽ để trống trong tệp xuất — hãy điền dữ liệu còn thiếu cho sản phẩm trước khi bạn dựa vào tệp này cho một lô hàng thực tế.

## Kiểm Tra Tính Sẵn Sàng Vận Chuyển Quốc Tế

Sử dụng điều này để kiểm tra một lô sản phẩm trước khi bạn bắt đầu vận chuyển chúng quốc tế, mà không cần mở từng sản phẩm một hoặc chờ đợi một tệp CSV đầy đủ.

Chọn các sản phẩm, chọn **Kiểm Tra Tính Sẵn Sàng Vận Chuyển Quốc Tế**, và nhấn **Áp dụng**. Spwig kiểm tra mỗi sản phẩm được chọn dựa trên ba trường được yêu cầu — **Mã HS**, **Quốc Gia Sản Xuất**, và **Giá Đơn Vị Hải Quan** — và hiển thị một thông báo tóm tắt kết quả:

- Nếu mọi sản phẩm được chọn đều có đầy đủ ba trường thông tin, bạn sẽ thấy một thông báo cho biết tất cả đều sẵn sàng.
- Nếu một số sản phẩm thiếu dữ liệu, thông báo sẽ báo cáo số lượng sản phẩm đã sẵn sàng và số lượng không sẵn sàng, đồng thời liệt kê từng sản phẩm không sẵn sàng cùng các trường mà chúng thiếu (ví dụ: "Cup gốm xanh (thiếu: hs_code, country_of_origin)").

Nếu có hơn 10 sản phẩm thiếu dữ liệu, thông báo sẽ liệt kê 10 sản phẩm đầu tiên và cho biết số lượng còn lại.

Hành động này chỉ đọc dữ liệu — nó không thay đổi bất kỳ thứ gì trên sản phẩm, vì vậy bạn có thể chạy nó thường xuyên bất cứ khi nào bạn muốn trong quá trình điền thông tin hải quan cho danh mục sản phẩm của mình.

**Số hiệu giấy phép xuất khẩu** và **Ngày hết hạn giấy phép xuất khẩu** không phải là một phần của quá trình kiểm tra tính sẵn sàng. Chúng chỉ áp dụng cho các mặt hàng bị kiểm soát hoặc bị hạn chế, do đó một sản phẩm có thể "sẵn sàng" để giao hàng quốc tế mà không cần chúng.

## Mẹo

- Chạy **Kiểm tra Tính sẵn sàng Giao hàng Quốc tế** trên toàn bộ danh mục sản phẩm (hoặc từng danh mục một) trước đơn hàng quốc tế đầu tiên — nó nhanh hơn rất nhiều so với việc phát hiện mã HS bị thiếu khi lô hàng đã ở biên giới.
- Duy trì **Dữ liệu Hải quan Xuất khẩu (CSV)** để giao cho các đại lý và nhà vận chuyển, và **Kiểm tra Tính sẵn sàng Giao hàng Quốc tế** cho danh sách kiểm tra nội bộ của bạn — CSV là một tài liệu, việc kiểm tra tính sẵn sàng là danh sách việc cần làm.
- Điền mã HS, quốc gia xuất xứ và giá đơn vị hải quan trên biểu mẫu sản phẩm (dưới mục **Giao hàng Quốc tế / Hải quan**) khi bạn thêm sản phẩm mới, để bạn không phải thực hiện việc này theo lô sau này.
- Bảng sản phẩm tải thêm sản phẩm tự động khi bạn cuộn (cuộn vô hạn), và các lựa chọn hộp kiểm của bạn được giữ nguyên khi các sản phẩm mới được tải — vì vậy bạn có thể cuộn để xây dựng một danh sách lớn trước khi áp dụng một hành động. Tuy nhiên, thay đổi bộ lọc hoặc tải lại trang sẽ xóa bỏ lựa chọn của bạn, vì vậy hãy áp dụng hành động trước khi điều chỉnh bộ lọc.
- **Đánh dấu là bản nháp** là cách nhanh để rút nhiều sản phẩm khỏi cửa hàng cùng lúc — ví dụ, trước khi kiểm kê hàng tồn — mà không làm thay đổi bất kỳ điều gì khác về chúng.