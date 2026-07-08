---
title: Trọng số liên quan và chỉ số hóa sâu
---

Trọng số liên quan và chỉ số hóa sâu kiểm soát cách kết quả tìm kiếm được xếp hạng và dữ liệu sản phẩm nào được tìm kiếm. Trọng số là các hệ số quan trọng - trọng số 2.0 có nghĩa là các kết quả trùng khớp trong trường đó quan trọng gấp đôi so với trọng số 1.0. Chỉ số hóa sâu xác định liệu tìm kiếm có đi sâu hơn vào tên sản phẩm cơ bản để vào SKU, thuộc tính, đánh giá, và thậm chí nội dung tài liệu. Hướng dẫn này giải thích cả hai hệ thống, khi nào nên điều chỉnh chúng và các hệ quả quan trọng về hiệu suất.

Các giá trị mặc định hoạt động tốt cho hầu hết các cửa hàng thương mại điện tử. Chỉ điều chỉnh nếu bạn có nhu cầu xếp hạng hoặc chỉ số hóa cụ thể.

![Tab Trọng số](/static/core/admin/img/help/search-settings-overview/search-settings-weights.webp)

## Hiểu về Trọng số

Trọng số là các hệ số (thang điểm 0.0-2.0) được áp dụng khi có sự trùng khớp văn bản trong các trường khác nhau. Trọng số cao hơn có nghĩa là các trùng khớp trong trường đó sẽ được xếp hạng cao hơn trong kết quả.

**Ví dụ**: Nếu một sản phẩm có từ "laptop" trong cả tên (trọng số 1.50) và mô tả (trọng số 0.80):
- Trùng khớp tên đóng góp 1.50 vào điểm liên quan
- Trùng khớp mô tả đóng góp 0.80
- Điểm tổng hợp xác định thứ hạng so với các sản phẩm khác

Trọng số cho phép bạn ưu tiên các trường nhất định hơn các trường khác khi xếp hạng kết quả tìm kiếm.

## Các loại Trọng số và Giá trị Mặc định

Truy cập **Cài đặt Tìm kiếm > Tab Trọng số** để xem tất cả cài đặt trọng số:

| Trường | Trọng số Mặc định | Lý do |
|-------|---------------|-----------|
| **weight_name** | 1.50 | Tên sản phẩm quan trọng nhất - khách hàng mong đợi các kết quả trùng khớp tên chính xác ở đầu |
| **weight_sku** | 1.20 | SKU là các mã nhận dạng cụ thể - quan trọng cho B2B và khách hàng quay lại |
| **weight_description** | 0.80 | Mô tả cung cấp bối cảnh nhưng ít quan trọng hơn các kết quả trùng khớp tên chính xác |
| **weight_categories** | 0.80 | Các kết quả trùng khớp danh mục hữu ích cho việc duyệt nhưng không cụ thể bằng tên/SKU |
| **weight_attributes** | 0.70 | Tìm kiếm theo màu sắc, kích cỡ, chất liệu - hữu ích nhưng là thông tin hỗ trợ |
| **weight_brands** | 0.70 | Lọc theo thương hiệu quan trọng nhưng không phải tiêu chí tìm kiếm chính cho hầu hết cửa hàng |
| **weight_blog_posts** | 0.60 | Nội dung blog ít quan trọng trong tìm kiếm tập trung vào thương mại điện tử (ưu tiên thấp nhất) |
| **weight_reviews** | 0.50 | Nội dung do người dùng tạo ít kiểm soát hơn - trọng số thấp nhất |

Các giá trị mặc định giả định một cửa hàng thương mại điện tử điển hình nơi việc khám phá sản phẩm là mục tiêu tìm kiếm chính.

## Khi nào nên Điều chỉnh Trọng số

Điều chỉnh trọng số khi ưu tiên của cửa hàng bạn khác với các mô hình thương mại điện tử điển hình:

**Cửa hàng nặng về SKU (B2B, Bán buôn)** - Tăng `weight_sku` lên 1.8-2.0 để tìm kiếm theo mã sản phẩm chi phối kết quả. Khách hàng B2B thường tìm kiếm theo mã SKU chính xác.

**Cửa hàng tập trung vào Thương hiệu** - Tăng `weight_brands` lên 1.2-1.5 khi khách hàng chủ yếu mua hàng theo thương hiệu (thời trang thiết kế, hàng xa xỉ).

**Cửa hàng nặng về Nội dung** - Tăng `weight_blog_posts` lên 0.9-1.2 nếu bạn là nhà xuất bản nội dung hoặc nhà bán lẻ giáo dục nơi nội dung blog quan trọng bằng sản phẩm.

**Cửa hàng nặng về Thuộc tính (Thời trang)** - Tăng `weight_attributes` lên 1.0-1.2 khi khách hàng thường xuyên tìm kiếm theo thuộc tính màu sắc, kích cỡ, phong cách.

## Ví dụ Điều chỉnh Trọng số

| Loại Cửa hàng | Các điều chỉnh được đề xuất |
|-----------|------------------------|
| **Bán buôn B2B** | weight_sku: 2.0, weight_name: 1.3, weight_description: 0.6 - Ưu tiên mã sản phẩm |
| **Cửa hàng Thời trang** | weight_attributes: 1.2, weight_brands: 1.2, weight_name: 1.4 - Màu sắc/phong cách/thương hiệu quan trọng |
| **Nhà xuất bản Nội dung** | weight_blog_posts: 1.2, weight_name: 1.3, weight_reviews: 0.7 - Nội dung quan trọng bằng sản phẩm |
| **Thương mại điện tử Tổng quát** | Sử dụng giá trị mặc định - Cân bằng cho các cửa hàng trực tuyến điển hình |

Điều chỉnh một trọng số tại một thời điểm và kiểm tra trước khi thực hiện các thay đổi bổ sung.

## Tổng quan Chỉ số hóa Sâu

⚠️ **CẢNH BÁO VỀ HIỆN THỰC** - Mỗi tùy chọn chỉ số hóa sâu thêm vào độ phức tạp và chi phí truy vấn.

Chỉ số hóa sâu mở rộng tìm kiếm vượt ra ngoài tên và mô tả sản phẩm cơ bản vào dữ liệu bổ sung:

![Tab Chỉ số hóa Sâu](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Truy cập **Cài đặt Tìm kiếm > Tab Chỉ số hóa Sâu** để cấu hình.

## Chỉ số hóa SKU

**Mặc định**: BẬT, **Ảnh hưởng đến hiệu suất**: Thấp

Bao gồm SKU sản phẩm và SKU biến thể trong chỉ số tìm kiếm. Gây ra JOIN biến thể (chi phí nhỏ).

**Khi nên giữ BẬT**: Quan trọng cho các cửa hàng B2B nơi khách hàng biết mã sản phẩm. Cũng hữu ích cho khách hàng quay lại nhớ SKU từ đơn hàng trước.

**Khi nên tắt**: Không bao giờ, trừ khi bạn thực sự không có SKU nào được chỉ định. Ảnh hưởng đến hiệu suất là không đáng kể.

## Chỉ số hóa Thuộc tính

**Mặc định**: BẬT, **Ảnh hưởng đến hiệu suất**: Trung bình

Bao gồm thuộc tính sản phẩm (màu sắc, kích cỡ, chất liệu, thuộc tính tùy chỉnh) trong chỉ số tìm kiếm. Gắn kết với bảng thuộc tính.

**Khi nên giữ BẬT**: Quan trọng cho thời trang, sản phẩm có thể cấu hình, hoặc bất kỳ cửa hàng nào nơi khách hàng tìm kiếm theo đặc điểm sản phẩm ("áo váy đỏ", "áo phông cỡ lớn").

**Khi nên tắt**: Các danh mục >20,000 sản phẩm với nhiều thuộc tính mỗi sản phẩm có thể thấy 50-100ms chi phí. Chỉ tắt nếu hiệu suất là điều quan trọng và khách hàng không tìm kiếm theo thuộc tính.

## Chỉ số hóa Trường Tùy chỉnh

**Mặc định**: BẬT, **Ảnh hưởng đến hiệu suất**: Trung bình

Bao gồm các trường tùy chỉnh do người bán định nghĩa từ JSONField trong chỉ số tìm kiếm. Yêu cầu truy cập JSONField.

**Khi nên giữ BẬT**: Nếu bạn sử dụng các trường tùy chỉnh cho dữ liệu sản phẩm có thể tìm kiếm (thông tin bảo hành, thông số kỹ thuật, chi tiết tương thích).

**Khi nên tắt**: Nếu bạn không sử dụng các trường tùy chỉnh, hoặc các trường tùy chỉnh chứa dữ liệu không thể tìm kiếm (ghi chú nội bộ, mã kế toán). Tắt sẽ tiết kiệm chi phí xử lý JSONField.

## Chỉ số hóa Đánh giá

**Mặc định**: BẬT, **Ảnh hưởng đến hiệu suất**: Trung bình-Cao

Bao gồm tiêu đề và bình luận đánh giá đã được phê duyệt trong tìm kiếm. Gắn kết với bảng đánh giá và thêm chi phí tìm kiếm văn bản.

**Khi nên giữ BẬT**: Các danh mục đánh giá nhiều nơi khách hàng tìm kiếm sản phẩm dựa trên nội dung đánh giá ("túi đựng laptop chống nước" có thể xuất hiện trong văn bản đánh giá).

**Khi nên tắt**: Các danh mục >20,000 sản phẩm hoặc cửa hàng có nhiều đánh giá mỗi sản phẩm. Thêm 100-200ms chi phí trên các danh mục lớn.

## Chỉ số hóa Tài liệu

**Mặc định**: TẮT, **Ảnh hưởng đến hiệu suất**: RẤT CAO 🚨

**KHÔNG BẬT NGẪU NHIÊN** - Tính năng tìm kiếm đắt đỏ nhất.

Chỉ số hóa tài liệu trích xuất văn bản từ các tệp PDF, DOCX và XLSX đính kèm với sản phẩm kỹ thuật số, làm cho nội dung tệp có thể tìm kiếm được.

**Chi tiết kỹ thuật**:
- Sử dụng thư viện PyPDF2, python-docx và openpyxl
- I/O tệp đồng bộ và trích xuất văn bản trên tìm kiếm
- Theo dõi tệp qua checksum MD5 (chỉ chỉ số hóa lại khi tệp thay đổi)
- Có thể xảy ra thời gian chờ trên các tệp lớn (>10MB PDF)

**Ảnh hưởng đến hiệu suất**:
- Chi phí chỉ số hóa ban đầu rất cao (từ phút đến giờ cho thư viện lớn)
- Chi phí truy vấn đáng kể (thêm 100-500ms độ trễ)
- Tiêu tốn bộ nhớ cho các tài liệu lớn

**Chỉ bật nếu**:
- Bạn bán các sản phẩm kỹ thuật số có tài liệu có thể tìm kiếm (sách điện tử, báo cáo, hướng dẫn sử dụng)
- Danh mục nhỏ (<500 sản phẩm kỹ thuật số)
- Máy chủ có đủ tài nguyên
- Bạn đã kiểm tra kỹ ảnh hưởng

**Đối với các cửa hàng sản phẩm kỹ thuật số**: Hãy cân nhắc xem khách hàng thực sự cần tìm kiếm nội dung tài liệu hay việc tìm kiếm tên sản phẩm/mô tả là đủ.

## Bảng Ảnh hưởng đến Hiệu suất

| Tính năng | Mặc định | Ảnh hưởng | Sử dụng khi |
|---------|---------|--------|----------|
| Chỉ số hóa SKU | BẬT | Thấp | Luôn bật (quyết định cho B2B) |
| Chỉ số hóa Thuộc tính | BẬT | Trung bình | Sản phẩm có thể cấu hình |
| Chỉ số hóa Trường Tùy chỉnh | BẬT | Trung bình | Sử dụng trường tùy chỉnh |
| Chỉ số hóa Đánh giá | BẬT | Trung bình-Cao | Cửa hàng đánh giá nhiều |
| Chỉ số hóa Tài liệu | TẮT | Rất cao | Chỉ dành cho sản phẩm kỹ thuật số (kiểm tra trước) |

Ảnh hưởng giả định các danh mục điển hình. Các danh mục lớn (>50,000 sản phẩm) trải qua chi phí cao hơn theo tỷ lệ.

## Kiểm tra Thay đổi Trọng số

Khi điều chỉnh trọng số, hãy tuân theo quy trình kiểm tra sau:

1. **Thay đổi một trọng số tại một thời điểm** - Đừng điều chỉnh nhiều trọng số cùng lúc; bạn sẽ không biết thay đổi nào gây ra kết quả
2. **Tăng giảm nhỏ** - Điều chỉnh từng bước ±0.2 (ví dụ, 1.0 → 1.2, không phải 1.0 → 1.8)
3. **Kiểm tra với các truy vấn thực tế** - Sử dụng các từ khóa tìm kiếm thực tế từ phân tích, không phải kiểm tra ngẫu nhiên
4. **Theo dõi phân tích** - So sánh tính liên quan của kết quả trước và sau khi sử dụng các truy vấn hàng đầu
5. **Chờ 1-2 tuần** - Cho phép khách hàng thời gian tương tác với thứ hạng mới
6. **Đo lường tỷ lệ nhấp** - Khách hàng có nhấp vào kết quả nhiều hơn hay ít hơn so với trước đây không?

## Giao dịch giữa Hiệu suất và Độ chính xác

Chỉ số hóa nhiều hơn = kết quả tìm kiếm tốt hơn nhưng hiệu suất chậm hơn:

**Tình huống: Danh mục Nhỏ (<1,000 sản phẩm)**
- Bật tất cả tùy chọn chỉ số hóa (SKU, thuộc tính, trường tùy chỉnh, đánh giá)
- Ảnh hưởng đến hiệu suất tối thiểu
- Khả năng tìm kiếm toàn diện

**Tình huống: Danh mục Trung bình (1,000-10,000 sản phẩm)**
- Giữ SKU, thuộc tính, trường tùy chỉnh BẬT
- Xem xét tắt đánh giá nếu trung bình mỗi sản phẩm có >10 đánh giá
- Theo dõi thời gian phản hồi

**Tình huống: Danh mục Lớn (>10,000 sản phẩm)**
- Giữ SKU BẬT (ảnh hưởng thấp)
- Tắt chỉ số hóa đánh giá (ảnh hưởng cao)
- Tắt trường tùy chỉnh nếu không sử dụng
- KHÔNG BAO GIỜ bật chỉ số hóa tài liệu
- Xem xét Elasticsearch khi có >50,000 sản phẩm

Cân bằng dựa trên kích thước danh mục và tài nguyên máy chủ của bạn.

## Ghi đè Trọng số Đặc thù của Máy Chủ

Khi tạo một bộ máy tìm kiếm thông qua hướng dẫn (Bước 3), bạn có thể ghi đè các trọng số toàn cục cho bộ máy đó cụ thể.

**Trường hợp sử dụng**: Bộ máy tập trung vào blog
- Tạo bộ máy "blog"
- Ghi đè `weight_blog_posts` lên 1.5 (thay vì toàn cục 0.60)
- Nội dung blog giờ đây sẽ được xếp hạng cao hơn trong tìm kiếm bộ máy blog

Hầu hết các bộ máy nên KHÔNG ghi đè trọng số - để trống để kế thừa cài đặt toàn cục.

## Một số Lời khuyên

- **KHÔNG bao giờ bật chỉ số hóa tài liệu trừ khi thực sự cần thiết** - Tính năng tìm kiếm có chi phí hiệu suất cao nhất
- **Cửa hàng B2B: Tăng weight_sku lên 2.0** - Mã sản phẩm là phương pháp tìm kiếm chính
- **Kiểm tra thay đổi trọng số trong giờ thấp điểm** - Quan sát ảnh hưởng hiệu suất trước giờ cao điểm
- **Theo dõi thời gian phản hồi sau khi bật chỉ số hóa** - Kiểm tra bảng điều khiển phân tích để phát hiện chậm lại
- **Tắt chỉ số hóa đánh giá trên danh mục >20K sản phẩm** - Ảnh hưởng hiệu suất đáng kể
- **Thay đổi một trọng số tại một thời điểm để kiểm tra** - Không thể xác định nguyên nhân/kết quả với các thay đổi đồng thời
- **Trích xuất tài liệu yêu cầu PyPDF2/docx/openpyxl** - Kiểm tra xem các thư viện này đã được cài đặt trước khi bật chỉ số hóa tài liệu

Hãy nhớ: Giữ nguyên toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật như đã hiển thị trong các quy tắc bảo tồn.