---
title: Tối ưu hóa hiệu suất tìm kiếm
---

Hiệu suất tìm kiếm ảnh hưởng trực tiếp đến trải nghiệm khách hàng và tỷ lệ chuyển đổi. Các lần tìm kiếm chậm làm phiền khách hàng và làm tăng tỷ lệ thoát. Hướng dẫn toàn diện này xác định các điểm nghẽn hiệu suất phổ biến trong hệ thống tìm kiếm tích hợp cơ sở dữ liệu của Spwig, cung cấp chiến lược tối ưu hóa và thiết lập mục tiêu hiệu suất. Sử dụng hướng dẫn này khi thời gian phản hồi tìm kiếm vượt quá ngưỡng chấp nhận được hoặc bạn đang lên kế hoạch mở rộng danh mục sản phẩm.

Thời gian phản hồi mục tiêu: <200ms tự động hoàn tất, <500ms tìm kiếm đầy đủ. Thực hiện danh sách kiểm tra tối ưu hóa dưới đây để đạt được các mục tiêu này.

## Hiểu các chỉ số hiệu suất

Theo dõi các chỉ số này trong **Tìm kiếm > Phân tích tìm kiếm**:

**Thời gian phản hồi** - Miligiây để thực thi truy vấn tìm kiếm (chỉ phía máy chủ, không bao gồm độ trễ mạng)

**Tỷ lệ trúng cache** - Phần trăm các lần tìm kiếm được phục vụ từ cache thay vì cơ sở dữ liệu

**Số lượng truy vấn** - Số lượng truy vấn cơ sở dữ liệu mỗi lần tìm kiếm (càng ít càng tốt)

**Thời gian truy vấn cơ sở dữ liệu** - Thời gian dành cho cơ sở dữ liệu so với mã ứng dụng

## Mục tiêu hiệu suất

| Loại truy vấn | Mục tiêu | Chấp nhận được | Cần tối ưu hóa |
|---------------|---------|----------------|------------------|
| Tự động hoàn tất | <200ms | 200-300ms | >300ms liên tục |
| Tìm kiếm đầy đủ | <500ms | 500-800ms | >800ms liên tục |
| Tìm kiếm quản trị | <1000ms | 1000-1500ms | >1500ms liên tục |

Nếu thời gian phản hồi trung bình của bạn vượt quá ngưỡng "Cần tối ưu hóa", hãy triển khai các chiến lược dưới đây.

## Theo dõi hiệu suất

**Thời gian phản hồi trung bình của bảng điều khiển phân tích**

Truy cập **Tìm kiếm > Phân tích tìm kiếm** để xem thời gian phản hồi trung bình trên tất cả các lần tìm kiếm. Đây là chỉ số theo dõi hiệu suất chính của bạn.

**Khi nào cần điều tra**: Thời gian phản hồi trung bình >300ms cho tự động hoàn tất hoặc >800ms cho tìm kiếm đầy đủ liên tục trong nhiều ngày.

**Theo dõi hàng tuần**: Xem xét phân tích mỗi thứ Hai để phát hiện sự suy giảm hiệu suất sớm.

## Các điểm nghẽn hiệu suất đã biết

Hệ thống tìm kiếm tích hợp cơ sở dữ liệu của Spwig có một số điểm nghẽn được ghi lại để tránh:

### Tính toán tỷ lệ nhấp N+1 truy vấn

**Đây là gì**: Tỷ lệ nhấp thông qua trong Dịch vụ Phân tích thực thi các truy vấn riêng biệt cho từng mục kết quả được tổng hợp.

**Tác động**: Rất nghiêm trọng đối với các cửa hàng có lưu lượng truy cập cao với nhiều truy vấn được theo dõi.

**Vị trí mã**: `search/services/analytics_service.py` - phương thức `get_click_through_rate()`

**Giảm thiểu**: Tránh gọi tính toán tỷ lệ nhấp trong môi trường sản xuất. Đây chủ yếu là tính năng phân tích quản trị nên được tính toán bất đồng bộ, không phải trong các yêu cầu hướng đến khách hàng.

### Tổng hợp tồn kho

**Đây là gì**: `with_stock_totals()` tính toán số lượng tồn kho trên tất cả kho hàng theo sản phẩm.

**Tác động**: Tốn kém trên các danh mục >1.000 sản phẩm. Được gọi khi bộ lọc `in_stock` được sử dụng hoặc trạng thái tồn kho được hiển thị trong tự động hoàn tất.

**Kích hoạt**: **Cài đặt tìm kiếm > Tự động hoàn tất** - tùy chọn "Hiển thị trạng thái tồn kho"

**Khuyến nghị**: KHÔNG BAO GIỜ bật trạng thái tồn kho trong tự động hoàn tất trên các danh mục lớn. Thêm 200-500ms mỗi yêu cầu.

### Kết nối biến thể

**Đây là gì**: Các truy vấn SKU kích hoạt JOIN trên bảng biến thể để tìm SKU biến thể.

**Tác động**: Chậm hơn 2-3 lần đối với các sản phẩm có nhiều biến thể (10+ biến thể mỗi sản phẩm).

**Giảm thiểu**: Sử dụng `.distinct()` để tránh trùng lặp, điều này làm tăng chi phí. Cần thiết cho chức năng SKU - không tắt trừ khi không sử dụng SKU.

### Số lượng sản phẩm trong tự động hoàn tất

**Đây là gì**: Kết quả tự động hoàn tất theo danh mục/Thương hiệu hiển thị số lượng sản phẩm ("Điện tử (234)")

**Tác động**: Mỗi loại nội dung với số lượng được bật thêm 2 truy vấn. Các truy vấn bao gồm các kết nối và tổng hợp.

**Kích hoạt**: **Cài đặt tìm kiếm > Tự động hoàn tất** - "Hiển thị số lượng sản phẩm" cho danh mục/thương hiệu

**Khuyến nghị**: Tắt số lượng sản phẩm. Tiết kiệm 2-4 truy vấn mỗi yêu cầu tự động hoàn tất. Chiến lược tối ưu hóa tự động hoàn tất lớn nhất.

### Chỉ mục tài liệu

**Đây là gì**: Trích xuất văn bản từ các tệp PDF/DOCX/XLSX trong quá trình truy vấn tìm kiếm.

**Tác động**: Rất tốn kém (I/O tệp + trích xuất văn bản). Các hoạt động chặn đồng bộ.

**Kích hoạt**: **Cài đặt tìm kiếm > Chỉ mục sâu** - "Chỉ mục tài liệu"

**Khuyến nghị**: Gần như không bao giờ đáng để chi trả chi phí hiệu suất. CHỈ bật khi bạn có danh mục sản phẩm kỹ thuật số nhỏ (<500 sản phẩm) sau khi kiểm tra kỹ lưỡng.

## Cấu hình cache

Caching là phương pháp tối ưu hiệu suất hiệu quả nhất.

**Cache tự động hoàn tất** - Mặc định: 60s
- **Khoảng khuyến nghị**: 45-90s
- **TTL cao hơn (90-120s)**: Hiệu suất tốt hơn nếu thay đổi tồn kho ít thường xuyên
- **TTL thấp hơn (30-45s)**: Kết quả mới hơn nếu bạn thêm sản phẩm mỗi giờ

**Cache kết quả** - Mặc định: 300s (5 phút)
- **Khoảng khuyến nghị**: 180-600s
- **TTL cao hơn (600s/10 phút)**: Cải thiện hiệu suất đáng kể cho danh mục tĩnh
- **TTL thấp hơn (180s)**: Mới hơn nếu thường xuyên cập nhật dữ liệu sản phẩm

**Chiến lược tối ưu hóa**: Nếu tìm kiếm chậm, hãy tăng gấp đôi TTL cache trước khi tắt các tính năng. Chuyển từ 60s → 120s cache tự động hoàn tất giảm tải cơ sở dữ liệu một nửa.

## Danh sách kiểm tra tối ưu hóa tự động hoàn tất

Áp dụng các thay đổi này cho cài đặt tự động hoàn tất để đạt hiệu suất tối đa:

**1. Tăng thời gian chờ lên 300-400ms**
- Vị trí: **Cài đặt tìm kiếm > Tự động hoàn tất** - "Thời gian chờ"
- Tác động: Giảm các cuộc gọi API bằng cách chờ lâu hơn giữa các phím nhấn
- Đổi lấy: Ít phản hồi hơn (khó nhận ra đối với hầu hết người dùng)

**2. Giảm số lượng kết quả tối đa từ 8 xuống 5-6**
- Vị trí: **Cài đặt tìm kiếm > Tự động hoàn tất** - "Số lượng tối đa mỗi loại"
- Tác động: Bộ kết quả nhỏ hơn = truy vấn nhanh hơn và payload JSON nhỏ hơn
- Đổi lấy: Ít tùy chọn hơn được hiển thị (thường là đủ)

**3. Tắt số lượng sản phẩm (THẮNG LỚN NHẤT)**
- Vị trí: **Cài đặt tìm kiếm > Tự động hoàn tất** - Bỏ chọn "Hiển thị số lượng sản phẩm" cho danh mục/thương hiệu
- Tác động: Tiết kiệm 2-4 truy vấn mỗi yêu cầu tự động hoàn tất
- Đổi lấy: Không có số lượng sản phẩm trong dropdown (hiếm khi cần)

**4. Tắt trạng thái tồn kho**
- Vị trí: **Cài đặt tìm kiếm > Tự động hoàn tất** - Bỏ chọn "Hiển thị trạng thái tồn kho"
- Tác động: Loại bỏ tổng hợp tồn kho tốn kém
- Đổi lấy: Không có nhãn tồn kho (không cần thiết trong ngữ cảnh tự động hoàn tất)

**5. Tắt mô tả sản phẩm**
- Vị trí: **Cài đặt tìm kiếm > Tự động hoàn tất** - Bỏ chọn "Hiển thị mô tả"
- Tác động: Giảm xử lý văn bản và kích thước payload
- Đổi lấy: Ít văn bản xem trước hơn (tên sản phẩm thường là đủ)

**6. Tăng TTL cache lên 90s**
- Vị trí: **Cài đặt tìm kiếm > Caching** - "TTL cache tự động hoàn tất"
- Tác động: Nhiều yêu cầu hơn được phục vụ từ cache
- Đổi lấy: Kết quả có thể lỗi thời đến 90 giây (chấp nhận được cho hầu hết các cửa hàng)

**Cải tiến dự kiến**: Áp dụng tất cả 6 tối ưu hóa thường làm giảm thời gian phản hồi tự động hoàn tất 50-70%.

## Tối ưu hóa chỉ mục sâu

Mỗi tùy chọn chỉ mục sâu thêm chi phí. Tắt tùy chọn dựa trên kích thước danh mục:

| Kích thước danh mục | Chỉ mục sâu được khuyến nghị |
|---------------------|-----------------------------|
| **<1.000 sản phẩm** | Tất cả BẬT (tác động tối thiểu) |
| **1.000-10.000** | Giữ SKU, Thuộc tính, Trường tùy chỉnh BẬT; Tắt Đánh giá |
| **10.000-20.000** | Giữ SKU, Thuộc tính BẬT; Tắt Trường tùy chỉnh, Đánh giá |
| **20.000-50.000** | Chỉ giữ SKU BẬT; Tắt tất cả các tùy chọn khác |
| **>50.000** | Giữ SKU BẬT; Xem xét di chuyển sang Elasticsearch |

**Chỉ mục tài liệu**: LUÔN TẮT trừ khi cần thiết (sản phẩm kỹ thuật số với tài liệu có thể tìm kiếm và <500 sản phẩm tổng cộng).

## Tối ưu hóa loại nội dung

Tắt các loại nội dung không sử dụng trong **Cài đặt tìm kiếm > Loại nội dung**:

- **Không có blog?** Tắt "Bài viết blog" - tiết kiệm truy vấn
- **Không có bộ lọc thương hiệu?** Tắt "Thương hiệu" - tiết kiệm truy vấn
- **Cửa hàng chỉ bán hàng?** Tắt "Danh mục" và "Bài viết blog"

Mỗi loại nội dung bị tắt sẽ loại bỏ các truy vấn cơ sở dữ liệu khỏi mọi lần tìm kiếm.

## Tối ưu hóa cơ sở dữ liệu

Spwig tạo các chỉ mục cần thiết thông qua các lần di chuyển. Tin tưởng vào chúng - không tạo thêm chỉ mục nào mà không phân tích.

**Bảo trì PostgreSQL** (nếu đang sử dụng PostgreSQL):
- Chạy `VACUUM ANALYZE` hàng tuần để cập nhật thống kê của trình lập kế hoạch truy vấn
- Các danh mục lớn có lợi từ `VACUUM FULL` hàng tháng (yêu cầu thời gian ngừng hoạt động)

**Theo dõi thời gian truy vấn cơ sở dữ liệu**: Trong quá trình phát triển, xác định các truy vấn chậm bằng các công cụ phân tích. Hầu hết tối ưu hóa truy vấn đã được triển khai:
- `.select_related('brand', 'category')` trên sản phẩm
- `.prefetch_related('images')` cho hình thu nhỏ
- `.distinct()` cho tìm kiếm biến thể

## Hiệu suất so khớp mờ

Khoảng cách Levenshtein tốn nhiều chi phí tính toán (độ phức tạp O(m*n)):

**Tối ưu hóa ngưỡng**:
- **Ngưỡng cao hơn (0,85 so với 0,80)**: Nhanh hơn nhưng bắt được ít lỗi chính tả hơn
- **Ngưỡng thấp hơn (0,75 so với 0,80)**: Chậm hơn nhưng dễ dàng hơn

**Tối ưu hóa số chỉnh sửa tối đa**:
- **Số chỉnh sửa tối đa thấp hơn (1 so với 2)**: Nhanh hơn nhưng bỏ sót nhiều lỗi chính tả hơn
- **Số chỉnh sửa tối đa cao hơn (2 so với 3)**: Chậm hơn nhưng bắt được nhiều lỗi chính tả hơn

**Hiệu suất thư viện**: Spwig sử dụng `rapidfuzz` nếu có sẵn (nhanh hơn 10 lần so với Python thuần). Đảm bảo nó được cài đặt: `pip install rapidfuzz`

## Hiệu suất từ đồng nghĩa và chuyển hướng

**Mở rộng truy vấn đồng nghĩa**: Mỗi đồng nghĩa thêm các điều kiện OR vào truy vấn tìm kiếm. Giới hạn tối đa 10-20 đồng nghĩa mỗi thuật ngữ.

**Loại khớp chính quy**: Chuyển hướng chính quy chậm hơn so với khớp chính xác/chứa/bắt đầu với. Tránh các mẫu phức tạp.

**Khuyến nghị**: Sử dụng loại khớp đơn giản khi có thể. Dự trữ chính quy cho các trường hợp mà các loại khớp khác không hoạt động.

## Tối ưu hóa danh mục lớn (>10.000 sản phẩm)

Chiến lược cụ thể cho danh mục lớn:

**1. Caching mạnh mẽ**
- Tự động hoàn tất: TTL 90-120s
- Kết quả: TTL 600s (10 phút)
- Chấp nhận sự lỗi thời để đạt hiệu suất

**2. Chỉ mục sâu tối thiểu**
- Chỉ SKU (tắt thuộc tính, trường tùy chỉnh, đánh giá)
- Kiểm tra hiệu suất có và không có thuộc tính

**3. Giảm số lượng kết quả tự động hoàn tất**
- Tối đa 5 kết quả mỗi loại (giảm từ 8)
- Giảm chi phí truy vấn

**4. Tắt trạng thái tồn kho ở mọi nơi**
- Trong tự động hoàn tất
- Trong kết quả tìm kiếm nếu được hiển thị

**5. Xem xét Elasticsearch khi có >50.000 sản phẩm**
- Tìm kiếm tích hợp cơ sở dữ liệu phù hợp đến ~50.000 sản phẩm
- Vượt quá đó, Elasticsearch được khuyến nghị cho:
  - Tìm kiếm có mặt hàng phức tạp
  - Tải lượng tìm kiếm đồng thời cao (>100 tìm kiếm/giây)
  - Thời gian phản hồi >500ms liên tục ngay cả sau khi tối ưu hóa

## Hiệu suất đa ngôn ngữ

Chỉ mục JSONField JSONB (PostgreSQL) làm cho đa ngôn ngữ hiệu quả:

- **1-3 ngôn ngữ**: Chi phí tối thiểu (5-10ms)
- **5+ ngôn ngữ**: Tăng nhẹ độ phức tạp truy vấn (20-40ms)
- **10+ ngôn ngữ**: Tăng đáng kể (50-100ms)

Chi phí tăng tuyến tính theo số lượng ngôn ngữ.

## Sửa lỗi hiệu suất khẩn cấp

Nếu tìm kiếm rất chậm (>2s thời gian phản hồi), áp dụng các sửa lỗi khẩn cấp này theo thứ tự:

**Khẩn cấp** (áp dụng ngay):
1. Tắt chỉ mục tài liệu
2. Tắt số lượng sản phẩm trong tự động hoàn tất
3. Tăng TTL cache lên 120s tự động hoàn tất / 600s kết quả

**Nhanh** (áp dụng trong vòng 24 giờ):
4. Tắt trạng thái tồn kho trong tự động hoàn tất
5. Giảm số lượng kết quả tối đa tự động hoàn tất xuống 5
6. Tắt mô tả sản phẩm trong tự động hoàn tất

**Trung bình** (áp dụng trong vòng một tuần):
7. Tắt chỉ mục đánh giá nếu >20K sản phẩm
8. Xem xét và tắt các loại nội dung không sử dụng
9. Tăng thời gian chờ lên 400ms

**Cải tiến dự kiến**: 9 sửa lỗi này thường làm giảm thời gian phản hồi 60-80% trên các danh mục lớn.

## Một số mẹo

- **Theo dõi thời gian phản hồi hàng tuần** - Phát hiện sự suy giảm hiệu suất sớm
- **Tăng TTL cache là tối ưu hóa đầu tiên** - Nhân đôi TTL cache là chiến thắng dễ nhất
- **Số lượng sản phẩm trong tự động hoàn tất = tốn kém** - Kẻ giết hiệu suất tự động hoàn tất lớn nhất
- **Chỉ mục tài liệu gần như không bao giờ đáng** - Chi phí hiệu suất hiếm khi xứng đáng với lợi ích
- **Kiểm tra từng thay đổi một lần** - Không thể xác định nguyên nhân/kết quả với các thay đổi đồng thời
- **Đánh giá với khối lượng dữ liệu thực tế** - Kiểm tra với danh mục có kích thước sản xuất
- **Tổng hợp tồn kho làm giảm hiệu suất trên danh mục lớn** - Tránh hiển thị tồn kho trong tự động hoàn tất
- **Xem xét Elasticsearch khi có >50.000 sản phẩm** - Tìm kiếm tích hợp cơ sở dữ liệu có giới hạn

