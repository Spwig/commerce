---
title: Cấu hình Tự động hoàn thành
---

Tự động hoàn thành, còn được gọi là tìm kiếm dự đoán hoặc tìm kiếm khi đang nhập, hiển thị kết quả khi khách hàng nhập các truy vấn của họ. Điều này cải thiện đáng kể trải nghiệm người dùng bằng cách giúp khách hàng tìm thấy sản phẩm nhanh hơn và giảm các truy vấn không có kết quả. Hướng dẫn này giải thích cách cấu hình hành vi tự động hoàn thành, cài đặt hiển thị và các sự đánh đổi về hiệu suất.

Tự động hoàn thành được kích hoạt mặc định với các cài đặt hợp lý. Chỉ điều chỉnh nếu bạn có lo ngại cụ thể về hiệu suất hoặc sở thích hiển thị.

![Cài đặt Tự động hoàn thành](/static/core/admin/img/help/configuring-autocomplete/autocomplete-settings-main.webp)

## Kích hoạt Tự động hoàn thành

Đi đến **Tìm kiếm > Cài đặt Tìm kiếm** và nhấp vào tab **Tự động hoàn thành**.

**Kích hoạt Tự động hoàn thành** - Công tắc chính cho tìm kiếm dự đoán. Khi được kích hoạt, các trường tìm kiếm sẽ hiển thị danh sách kết quả khi khách hàng nhập.

**Số lượng Kết quả Tối đa theo Loại** - Mặc định: 8 mục. Số lượng kết quả hiển thị cho mỗi loại nội dung (sản phẩm, danh mục, thương hiệu, bài viết blog). Giá trị thấp hơn (5-6) làm giảm kích thước tải dữ liệu API và hiển thị nhanh hơn. Giá trị cao hơn (10-12) cung cấp cho khách hàng nhiều tùy chọn hơn nhưng làm chậm phản hồi.

## Thời gian Chờ (Debounce Timing)

⚠️ **CẢNH BÁO VỀ HIỆU NĂNG** - Thời gian chờ (debounce timing) ảnh hưởng đáng kể đến tải trên máy chủ.

**Thời gian Chờ (Debounce Delay)** - Mặc định: 300ms. Thời gian chờ sau phím cuối cùng trước khi kích hoạt yêu cầu tự động hoàn thành.

Cài đặt này cân bằng giữa tính phản hồi và tải trên máy chủ:

| Delay | Trải nghiệm Người dùng | Tác động Máy chủ |
|-------|----------------|---------------|
| **100ms** | Rất phản hồi | 3 lần gọi API hơn 300ms - tải cao |
| **200ms** | Phản hồi | 1.5 lần gọi API hơn 300ms |
| **300ms** | Cân bằng tốt (khuyến nghị) | Mức cơ sở |
| **400ms** | Chậm một chút | Ít gọi API hơn - tải thấp hơn |
| **500ms** | Trễ rõ rệt | Ít hơn 50% gọi nhưng cảm giác chậm |

**Khuyến nghị**: Giữ trong khoảng 250-350ms. Chỉ tăng trên 350ms nếu máy chủ của bạn đang gặp khó khăn với tải tự động hoàn thành. Không bao giờ giảm dưới 200ms trừ khi bạn có máy chủ rất nhanh và danh mục nhỏ.

## Cài đặt Hiển thị cho Sản phẩm

Các công tắc này kiểm soát thông tin nào hiển thị trong kết quả tự động hoàn thành sản phẩm:

**Hiển thị Hình thu nhỏ** - Mặc định: BẬT. Hiển thị hình ảnh sản phẩm bên cạnh kết quả. **Tác động hiệu năng**: Thêm truy vấn hình ảnh và tăng kích thước payload JSON. Tắt để có tự động hoàn thành nhanh hơn trên kết nối chậm.

**Hiển thị Mô tả** - Mặc định: TẮT. Hiển thị mô tả ngắn của sản phẩm. **Tác động hiệu năng**: Thêm xử lý văn bản và làm tăng đáng kể kích thước payload. Giữ ở chế độ tắt trừ khi mô tả là điều kiện thiết yếu để chọn sản phẩm.

**Hiển thị Giá** - Mặc định: BẬT. Hiển thị giá sản phẩm. **Tác động hiệu năng**: Thấp - dữ liệu giá đã được tải cùng với sản phẩm. An toàn để giữ ở chế độ bật.

**Hiển thị SKU** - Mặc định: BẬT. Hiển thị SKU sản phẩm. **Tác động hiệu năng**: Thấp - SKU đã được chỉ mục. Quan trọng cho các cửa hàng B2B.

**Hiển thị Tình trạng Kho** - Mặc định: TẮT. ⚠️ **CẢNH BÁO HIỆU NĂNG MẠNH**

Hiển thị nhãn "Còn hàng", "Hết hàng", hoặc "Hết hàng". ⚠️ **KHÔNG BAO GIỜ kích hoạt điều này trên danh mục lớn**.

Tình trạng kho yêu cầu `with_stock_totals()` aggregation - tính toán số lượng hàng tồn kho trên tất cả kho cho mỗi sản phẩm trong kết quả tự động hoàn thành. Điều này thêm vào:
- Tải cơ sở dữ liệu đáng kể (truy vấn aggregation)
- 200-500ms độ trễ bổ sung trên danh mục >1.000 sản phẩm
- Có thể gây thời gian chờ trên danh mục >10.000 sản phẩm

Chỉ kích hoạt nếu thực sự cần thiết và bạn có ít hơn 500 sản phẩm.

## Cài đặt Hiển thị cho Bài viết Blog

**Hiển thị Hình ảnh Đặc trưng** - Mặc định: BẬT. Hình ảnh thu nhỏ của bài viết blog trong kết quả tự động hoàn thành.

**Hiển thị Tóm tắt** - Mặc định: BẬT. Văn bản xem trước ngắn từ nội dung bài viết.

**Chiều dài Tóm tắt** - Mặc định: 60 ký tự. Số lượng văn bản xem trước để hiển thị.

Các cài đặt này có tác động hiệu năng tối thiểu vì số lượng bài viết blog thường ít hơn so với sản phẩm.

## Cài đặt Hiển thị cho Danh mục và Thương hiệu

**Hiển thị Hình ảnh/Logo** - Mặc định: BẬT. Hình ảnh danh mục hoặc thương hiệu trong kết quả.

**Hiển thị Số lượng Sản phẩm** - Mặc định: TẮT. ⚠️ **CẢNH BÁO HIỆU NĂNG**

Hiển thị số lượng sản phẩm trong mỗi danh mục hoặc thương hiệu (ví dụ: "Điện tử (234)").

⚠️ **KHÔNG BAO GIỜ kích hoạt điều này trên danh mục lớn**. Số lượng sản phẩm được tính lại trên mỗi yêu cầu tự động hoàn thành:
- Mỗi loại nội dung với số lượng được kích hoạt thêm 2 truy vấn bổ sung
- Các truy vấn bao gồm các phép nối và aggregation
- 100-300ms độ trễ bổ sung điển hình
- Tăng tuyến tính theo số lượng danh mục/thương hiệu

Chỉ kích hoạt nếu bạn có ít hơn 50 danh mục/thương hiệu và tổng số sản phẩm dưới 1.000.

## Lưu trữ (Caching)

**Thời gian sống (TTL) của bộ nhớ đệm Tự động hoàn thành** - Mặc định: 60 giây (được thiết lập trong tab Caching).

Kết quả tự động hoàn thành được lưu trữ để cải thiện hiệu suất. TTL 60 giây có nghĩa là:
- Khách hàng đầu tiên tìm kiếm "laptop" sẽ kích hoạt truy vấn cơ sở dữ liệu
- Trong 59 giây tiếp theo, tất cả các tìm kiếm "laptop" sẽ trả về kết quả được lưu trữ
- Sau 60 giây, bộ nhớ đệm hết hạn và tìm kiếm tiếp theo sẽ làm tươi dữ liệu

**Khuyến nghị cho TTL**:
- **45-60s**: Cân bằng tốt cho hầu hết các cửa hàng (mặc định)
- **90-120s**: Hiệu suất tốt hơn nếu tồn kho sản phẩm thay đổi hiếm khi
- **30s**: Kết quả mới hơn nếu bạn thường xuyên thêm sản phẩm mới

Tăng TTL bộ nhớ đệm là cách dễ nhất để cải thiện hiệu suất tự động hoàn thành.

## Tự động hoàn thành đa ngôn ngữ

Nếu bạn đã cấu hình nhiều ngôn ngữ, tự động hoàn thành sẽ tự động tìm kiếm nội dung đã dịch được lưu trữ trong trường JSONField dịch vụ.

**Cách hoạt động**:
- Khách hàng tìm kiếm bằng tiếng Tây Ban Nha: "zapatos"
- Hệ thống tìm kiếm các bản dịch tên sản phẩm tiếng Tây Ban Nha
- Kết quả hiển thị tên sản phẩm tiếng Tây Ban Nha từ dữ liệu JSONField
- Quay lại ngôn ngữ cơ bản nếu bản dịch tiếng Tây Ban Nha không tồn tại

**Hiệu năng**: Chi phí phụ thêm tối thiểu cho 1-3 ngôn ngữ. Với 5+ ngôn ngữ, tăng nhẹ độ phức tạp của truy vấn.

## Kiểm tra Tự động hoàn thành

Sau khi cấu hình cài đặt, hãy kiểm tra trải nghiệm tự động hoàn thành:

1. **Mở trang chủ cửa hàng** của bạn trong một cửa sổ ẩn danh
2. **Nhấp vào hộp tìm kiếm** để tập trung vào nó
3. **Nhập tên sản phẩm phổ biến** một cách chậm rãi (ví dụ: "laptop")
4. **Quan sát**:
   - Tốc độ kết quả xuất hiện sau khi bạn dừng nhập (thời gian chờ có hoạt động không?)
   - Thông tin nào được hiển thị (hình thu nhỏ, giá cả, SKU như đã cấu hình)
   - Kết quả có liên quan không (kiểm tra trọng số liên quan nếu không)
5. **Kiểm tra trên thiết bị di động** - Đảm bảo danh sách thả xuống dễ chạm và đọc được

## Một số mẹo

- **Tắt mô tả sản phẩm để tăng tốc độ** - Mô tả làm tăng đáng kể kích thước payload với giá trị tối thiểu trong ngữ cảnh tự động hoàn thành
- **KHÔNG BAO GIỜ kích hoạt tình trạng kho trên danh mục lớn** - Tính toán kho làm giảm hiệu suất tự động hoàn thành
- **Kiểm tra trên thiết bị di động với mục tiêu chạm** - Kết quả tự động hoàn thành phải dễ chạm trên điện thoại
- **Theo dõi thời gian phản hồi hàng tuần** - Mục tiêu dưới 200ms cho các yêu cầu tự động hoàn thành
- **Tăng TTL bộ nhớ đệm nếu chậm** - Dễ nhất để tối ưu hiệu năng
- **Số lượng sản phẩm là tốn kém - tắt trừ khi cần thiết** - Mỗi số lượng danh mục/thương hiệu thêm 2 truy vấn cho mỗi yêu cầu tự động hoàn thành