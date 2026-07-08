---
title: Hiểu về Cài đặt Tìm kiếm
---

Giao diện SearchSettings kiểm soát tất cả hành vi tìm kiếm toàn cầu trong cửa hàng Spwig của bạn. Trang cấu hình duy nhất này sử dụng giao diện 8 tab để tổ chức các tùy chọn tìm kiếm, từ việc bật/tắt cơ bản đến tối ưu hóa hiệu suất nâng cao. Các thay đổi ở đây áp dụng cho tất cả các công cụ tìm kiếm trừ khi bị ghi đè ở cấp độ công cụ.

Hướng dẫn này sẽ đi qua từng tab, giải thích chức năng của từng cài đặt và khi nào nên điều chỉnh nó.

![Tab Cài đặt Tìm kiếm Tổng quát](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## Giao diện 8 tab

SearchSettings là một mô hình singleton - chỉ có một bản ghi cấu hình duy nhất (pk=1) cho toàn bộ cửa hàng của bạn. Giao diện được chia thành tám tab:

| Tab | Mục đích |
|-----|---------|
| **Tổng quát** | Bật/tắt tìm kiếm, thiết lập các tham số cơ bản |
| **Tự động hoàn thành** | Cấu hình hành vi dropdown tìm kiếm dự đoán |
| **Loại nội dung** | Chọn các loại nội dung có thể được tìm kiếm |
| **Chỉ mục sâu** | Kiểm soát dữ liệu sản phẩm nào được chỉ mục (ảnh hưởng đến hiệu suất) |
| **So khớp mờ** | Độ dung sai lỗi chính tả và ngưỡng tương đồng |
| **Trọng số** | Các hệ số xếp hạng độ liên quan của kết quả |
| **Bộ nhớ đệm** | Quyết định giữa thời gian phản hồi và độ mới của kết quả |
| **Phân tích** | Theo dõi truy vấn và cài đặt bảo mật |

Mỗi tab tập trung vào một khía cạnh cụ thể của cấu hình tìm kiếm.

## Tab Tổng quát

Tab Tổng quát chứa các cài đặt cốt lõi ảnh hưởng đến tất cả các cuộc tìm kiếm:

**Bật Tìm kiếm** - Công tắc chính cho hệ thống tìm kiếm. Khi bị tắt, tất cả các tính năng tìm kiếm sẽ không hoạt động trên toàn bộ cửa hàng của bạn, bao gồm cả tự động hoàn thành và trang kết quả tìm kiếm.

**Chiều dài truy vấn tối thiểu** - Mặc định: 2 ký tự. Các cuộc tìm kiếm ngắn hơn sẽ bị từ chối. Việc thiết lập thành 1 cho phép tìm kiếm với một ký tự (ví dụ: "A") nhưng làm tăng tải cho máy chủ.

**Số kết quả mỗi trang** - Mặc định: 20 mục. Điều khiển phân trang cho các trang kết quả tìm kiếm. Các giá trị cao hơn (30-50) làm giảm số lần nhấp phân trang nhưng làm tăng thời gian tải trang.

## Tab Loại nội dung

![Cài đặt Loại nội dung](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

Bật/tắt các loại nội dung xuất hiện trong kết quả tìm kiếm:

- **Sản phẩm** - Sản phẩm vật lý, kỹ thuật số và đăng ký
- **Danh mục** - Danh mục sản phẩm
- **Thương hiệu** - Thương hiệu sản phẩm
- **Bài viết blog** - Nội dung blog

**Lưu ý hiệu suất**: Số lượng loại nội dung ít hơn = tìm kiếm nhanh hơn. Mỗi loại được bật sẽ thêm các truy vấn cơ sở dữ liệu bổ sung. Nếu bạn không có blog, hãy tắt Bài viết blog để cải thiện thời gian phản hồi.

## Tab Chỉ mục sâu

⚠️ **CẢNH BÁO HIỆU SUẤT** - Các cài đặt này có ảnh hưởng lớn đến hiệu suất.

![Cài đặt Chỉ mục sâu](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Chỉ mục sâu kiểm soát dữ liệu liên quan đến sản phẩm nào được bao gồm trong tìm kiếm:

**Chỉ mục SKU** - Mặc định: BẬT, Ảnh hưởng thấp. Bao gồm SKU sản phẩm và biến thể trong tìm kiếm. Quan trọng cho các cửa hàng B2B nơi khách hàng tìm kiếm theo mã sản phẩm.

**Chỉ mục Thuộc tính** - Mặc định: BẬT, Ảnh hưởng trung bình. Bao gồm các thuộc tính sản phẩm (màu sắc, kích thước, chất liệu) trong tìm kiếm. Thêm JOIN vào bảng thuộc tính. Quan trọng cho các sản phẩm thời trang và có thể cấu hình.

**Chỉ mục Trường tùy chỉnh** - Mặc định: BẬT, Ảnh hưởng trung bình. Bao gồm các trường tùy chỉnh do người bán định nghĩa trong kết quả tìm kiếm. Yêu cầu truy cập JSONField.

**Chỉ mục Đánh giá** - Mặc định: BẬT, Ảnh hưởng trung bình - cao ⚠️

Chỉ mục đánh giá trích xuất văn bản từ các tệp PDF, DOCX và XLSX đính kèm với sản phẩm kỹ thuật số. Tính năng này:

- Yêu cầu chỉ mục ban đầu rất đắt đỏ
- Thêm chi phí truy vấn đáng kể trên mỗi cuộc tìm kiếm
- Có thể gây ra thời gian chờ trên các tệp lớn
- **Chỉ nên được bật cho các cửa hàng sản phẩm kỹ thuật số có tài liệu có thể tìm kiếm**
- **Không bao giờ bật một cách tùy tiện** - kiểm tra kỹ ảnh hưởng hiệu suất

## Tab So khớp mờ

![Cài đặt So khớp mờ](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

So khớp mờ sử dụng khoảng cách Levenshtein để xử lý lỗi chính tả:

**Bật So khớp mờ** - Cho phép tìm kiếm khớp các từ tương tự (ví dụ: "laptop" khớp với "labtop")

**Ngưỡng Tương đồng** - Mặc định: 0.80 (80% tương đồng). Phạm vi: 0.0-1.0. Giá trị cao hơn yêu cầu khớp gần hơn và chạy nhanh hơn. Giá trị thấp hơn bắt được nhiều lỗi chính tả hơn nhưng có thể trả về các kết quả không liên quan.

**Khoảng cách chỉnh sửa tối đa** - Mặc định: 2 thay đổi ký tự. Số lượng tối đa các phép chèn, xóa hoặc thay thế được phép. Giá trị thấp hơn (1) cải thiện hiệu suất nhưng bắt được ít lỗi chính tả hơn.

## Tab Trọng số

Trọng số kiểm soát điểm số liên quan - cách các kết quả được xếp hạng. Tab Trọng số hiển thị các hệ số mặc định cho từng trường có thể tìm kiếm:

- weight_name: 1.50 (tên sản phẩm quan trọng nhất)
- weight_sku: 1.20
- weight_description: 0.80
- weight_categories: 0.80
- weight_attributes: 0.70
- weight_brands: 0.70
- weight_blog_posts: 0.60
- weight_reviews: 0.50

Các giá trị mặc định này hoạt động tốt cho hầu hết các cửa hàng thương mại điện tử. Để biết thông tin chi tiết về việc điều chỉnh trọng số và hiểu rõ tác động của chúng, xem chủ đề [Trọng số Liên quan và Chỉ mục sâu](/en/admin/help/relevance-weights-deep-indexing/).

## Tab Bộ nhớ đệm

![Cài đặt Bộ nhớ đệm](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

Bộ nhớ đệm cải thiện đáng kể hiệu suất tìm kiếm bằng cách lưu trữ các kết quả gần đây:

**Thời gian sống Bộ nhớ đệm Tự động hoàn thành** - Mặc định: 60 giây. Thời gian bộ nhớ đệm lưu trữ kết quả tự động hoàn thành. Thời gian sống ngắn hơn (30-45s) = kết quả mới hơn nhưng nhiều truy vấn cơ sở dữ liệu hơn. Thời gian sống dài hơn (90-120s) = nhanh hơn nhưng có thể có kết quả lỗi thời.

**Thời gian sống Bộ nhớ đệm Kết quả** - Mặc định: 300 giây (5 phút). Thời gian bộ nhớ đệm lưu trữ trang kết quả tìm kiếm đầy đủ. Thời gian sống dài hơn cải thiện hiệu suất đáng kể nhưng làm chậm việc hiển thị sản phẩm mới.

**Điều chỉnh**: Bộ nhớ đệm là phương pháp tối ưu hiệu suất hiệu quả nhất. Nếu tìm kiếm chậm, hãy tăng các giá trị này trước khi tắt các tính năng.

## Tab Phân tích

![Cài đặt Phân tích](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Theo dõi Truy vấn Tìm kiếm** - Kích hoạt bảng điều khiển phân tích tìm kiếm. Ghi lại văn bản truy vấn, số lượng kết quả, thời gian phản hồi và thời gian dấu thời gian.

**Theo dõi Thông tin Người dùng** - Liên kết các cuộc tìm kiếm với người dùng đã đăng nhập. Tắt tính năng này để tuân thủ quyền riêng tư (GDPR, CCPA).

**Theo dõi Thông tin Phiên** - Sử dụng ID phiên để theo dõi các cuộc tìm kiếm của người dùng ẩn danh. Hữu ích để xác định các mẫu tìm kiếm mà không cần dữ liệu cá nhân.

## Mô hình Singleton

SearchSettings sử dụng mô hình singleton - chỉ có một bản ghi cài đặt duy nhất trong cơ sở dữ liệu của bạn (pk=1). Khi bạn truy cập Cài đặt Tìm kiếm trong quản trị, bạn luôn đang chỉnh sửa cùng một bản ghi.

Không có tùy chọn "Thêm" hoặc "Xóa" - chỉ có "Thay đổi". Tất cả các công cụ tìm kiếm kế thừa các cài đặt này trừ khi chúng chỉ định ghi đè theo từng công cụ (hiếm).

## Một số mẹo

- **Giữ nguyên các cài đặt mặc định trừ khi bạn có nhu cầu cụ thể** - Các cài đặt mặc định được tối ưu hóa cho các cửa hàng thương mại điện tử điển hình
- **KHÔNG bao giờ bật chỉ mục tài liệu một cách tùy tiện** - Chỉ dành cho các cửa hàng sản phẩm kỹ thuật số có tài liệu có thể tìm kiếm, và kiểm tra ảnh hưởng hiệu suất trước
- **Theo dõi thời gian phản hồi trong phân tích** - Mục tiêu <200ms cho tự động hoàn thành, <500ms cho tìm kiếm đầy đủ
- **Tăng thời gian sống bộ nhớ đệm nếu hiệu suất chậm** - Bộ nhớ đệm là cách tối ưu hiệu suất dễ dàng nhất
- **Xem xét lại các truy vấn không có kết quả hàng tuần** - Chúng tiết lộ các sản phẩm bị thiếu hoặc các từ đồng nghĩa cần thiết
- **Tắt các loại nội dung không sử dụng** - Nếu bạn không có blog, hãy tắt Bài viết blog để tăng tốc độ tìm kiếm

Lưu ý: Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật chính xác như được hiển thị trong các quy tắc bảo tồn.