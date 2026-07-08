---
title: Trưng bày khuyến mãi khách hàng
---

Trưng bày khuyến mãi hiển thị trên màn hình dành cho khách hàng khi thiết bị POS không hoạt động (không có giao dịch đang diễn ra). Tạo một carousel hình ảnh để quảng bá các chương trình khuyến mãi theo mùa, sản phẩm mới ra mắt, chính sách cửa hàng, sự kiện sắp tới và lợi ích chương trình khách hàng thân thiết. Các slide có thể nhắm mục tiêu đến các cửa hàng hoặc nhóm cụ thể bằng cách gán phạm vi - chỉ chạy chương trình khuyến mãi lễ hội tại các cửa hàng ở Mỹ, hoặc chỉ hiển thị thông tin sự kiện địa phương tại các vị trí liên quan. Các slide đang hoạt động sẽ tự động chuyển đổi mỗi 5-10 giây, tạo ra bảng quảng cáo kỹ thuật số hấp dẫn giúp khách hàng được thông báo khi đang chờ đợi.

Sử dụng các slide khuyến mãi để tăng cường nhận thức về các chương trình khuyến mãi hiện tại, giáo dục khách hàng về chính sách và thúc đẩy sự tương tác với chương trình khách hàng thân thiết và các sự kiện.

![Danh sách slide khuyến mãi](/static/core/admin/img/help/customer-display-promo-slides/promoslide-list.webp)

## Hành vi hiển thị khách hàng

Khi thiết bị POS không hoạt động (không có khách hàng ở quầy thanh toán, không có giao dịch đang diễn ra), màn hình dành cho khách hàng sẽ hiển thị:

**Chế độ Carousel**:
- Chuyển đổi qua lại tất cả các slide đang hoạt động
- Mỗi slide hiển thị trong 5-10 giây (có thể cấu hình theo từng thiết bị)
- Chuyển tiếp mượt giữa các slide
- Lặp lại liên tục cho đến khi giao dịch bắt đầu

**Trong quá trình giao dịch**:
- Carousel dừng ngay lập tức
- Màn hình chuyển sang chế độ giao dịch (sản phẩm, tổng tiền đang tính, lời nhắc thanh toán)
- Carousel tiếp tục khi giao dịch hoàn tất và thiết bị trở lại trạng thái không hoạt động

**Không có slide nào được cấu hình**:
- Màn hình hiển thị thông điệp "Welcome" với thương hiệu cửa hàng
- Màn hình tĩnh (không có carousel)

**Yêu cầu kỹ thuật**:
- Màn hình hiển thị khách hàng có thể là màn hình riêng biệt hoặc cùng màn hình với nhân viên (ứng dụng POS hỗ trợ chế độ hình trong hình)
- Màn hình đồng bộ hóa qua API BroadcastChannel (giao tiếp cùng thiết bị) hoặc WebSocket (màn hình thiết bị riêng biệt)

## Nhắm mục tiêu phạm vi

Giống như mẫu hóa đơn, slide khuyến mãi hỗ trợ nhắm mục tiêu dựa trên phạm vi (ưu tiên cao nhất đến thấp nhất):

| Ưu tiên | Phạm vi | Ví dụ | Trường hợp sử dụng |
|----------|-------|---------|----------|
| **1** | Cửa hàng cụ thể | Slide của Cửa hàng Paris | Slide sự kiện lễ hội mùa hè ở Paris |
| **2** | Nhóm cửa hàng cụ thể | Slide của Nhóm Cửa hàng Châu Âu | Slide chính sách bảo mật GDPR chỉ dành cho EU |
| **3** | Tất cả cửa hàng | Slide toàn cầu | "Miễn phí vận chuyển cho đơn hàng >$50" (chương trình khuyến mãi toàn công ty) |

**Cách phạm vi hoạt động**:
- Thiết bị hiển thị các slide phù hợp với phạm vi cửa hàng của nó (slide cửa hàng cụ thể)
- Cộng thêm các slide phù hợp với phạm vi nhóm (nếu cửa hàng thuộc một nhóm)
- Cộng thêm các slide không có gán phạm vi (slide toàn cầu)
- Kết quả: Một cửa hàng có thể hiển thị 3-5 slide (kết hợp cả slide có phạm vi và toàn cầu)

**Ví dụ**:
- Slide toàn cầu: "Chương trình khách hàng thân thiết mới - Tham gia ngay hôm nay!" (không có phạm vi)
- Slide nhóm: "Khuyến mãi Ngày Kỷ niệm - Giảm 30%" (chỉ dành cho nhóm Cửa hàng Mỹ)
- Slide cửa hàng: "Lễ khai trương - Cửa hàng flagship NYC" (chỉ dành cho cửa hàng NYC)

**Thiết bị tại Cửa hàng NYC** hiển thị tất cả 3 slide (cửa hàng + nhóm + toàn cầu)
**Thiết bị tại Cửa hàng London** chỉ hiển thị slide toàn cầu (không thuộc nhóm Cửa hàng Mỹ, không phải cửa hàng NYC)

## Yêu cầu về hình ảnh

Slide khuyến mãi là hình ảnh toàn màn hình được tối ưu hóa cho màn hình hiển thị khách hàng:

**Tỷ lệ khung hình**: 16:9 (màn hình rộng)

**Độ phân giải khuyến nghị**: 1920×1080 pixel (Full HD)
- Phù hợp với hầu hết các màn hình hiện đại
- Cân bằng kích thước tệp (chất lượng so với tốc độ tải)

**Độ phân giải được chấp nhận**:
- Tối thiểu: 1280×720 (HD)
- Tối ưu: 1920×1080 (Full HD)
- Tối đa: 3840×2160 (4K) - không được khuyến khích (kích thước tệp lớn, tải chậm hơn)

**Định dạng tệp**: JPG, PNG hoặc WebP
- JPG cho hình ảnh chụp
- PNG cho đồ họa có độ trong suốt (mặc dù nền được khuyến khích)
- WebP cho kích thước tệp nhỏ nhất

**Kích thước tệp**: <500KB mỗi slide
- Các tệp lớn làm chậm việc tải carousel
- Nén hình ảnh trước khi tải lên (sử dụng tính năng tối ưu hóa Thư viện Media)

**Lời khuyên thiết kế**:
- Đối lập cao để dễ đọc từ xa (khách hàng cách màn hình 2-6 feet)
- Văn bản lớn (tối thiểu 48pt cho văn bản cơ bản, 72pt+ cho tiêu đề)
- Chữ in đậm (chữ in mảnh có thể bị mờ trên một số màn hình)
- Tránh chi tiết nhỏ (không thể nhìn thấy từ góc nhìn của khách hàng)
- Bao gồm lời kêu gọi hành động (khách hàng nên làm gì: "Hỏi nhân viên để biết thêm chi tiết", "Đăng ký ngay hôm nay")

## Tạo slide khuyến mãi

Di chuyển đến **POS > Slide khuyến mãi** và nhấn **+ Thêm slide khuyến mãi**:

![Biểu mẫu thêm slide khuyến mãi](/static/core/admin/img/help/customer-display-promo-slides/promoslide-add-form.webp)

**Hình ảnh** - Tải lên hoặc chọn từ Thư viện Media:
- Nhấn **Duyệt Thư viện Media** để chọn hình ảnh hiện có
- Hoặc tải lên hình ảnh mới đáp ứng các yêu cầu trên
- Xem trước hiển thị cách hình ảnh sẽ xuất hiện trên màn hình

**Tiêu đề** (Tùy chọn) - Văn bản chồng lên phía trên slide:
- Tối đa 60 ký tự (văn bản dài hơn sẽ bị cắt ngắn)
- Hiển thị trong thanh tối màu bán trong suốt ở phía trên hình ảnh
- Sử dụng cho tiêu đề slide ("Khuyến mãi mùa hè", "Sản phẩm mới")
- Để trống nếu hình ảnh đã bao gồm văn bản tiêu đề

**Phụ đề** (Tùy chọn) - Văn bản chồng lên dưới tiêu đề:
- Tối đa 120 ký tự
- Hiển thị dưới tiêu đề trong cùng thanh bán trong suốt
- Sử dụng cho chi tiết hỗ trợ ("Lên đến 50% giảm giá", "Tặng quà khi mua hàng")
- Để trống nếu hình ảnh tự chứa nội dung

**Kích hoạt** - Bật/tắt slide:
- Chỉ các slide đang hoạt động mới xuất hiện trong carousel
- Sử dụng để kích hoạt theo mùa (tắt sau khi chương trình khuyến mãi kết thúc)
- Tắt slide sẽ giữ slide đó để kích hoạt lại sau này

**Thứ tự sắp xếp** - Điều khiển vị trí slide trong carousel:
- Số nhỏ hơn sẽ xuất hiện sớm hơn trong chuỗi xoay
- Sử dụng các bội số của 10: 10, 20, 30 (cho phép chèn slide giữa các slide hiện có)
- Ví dụ: Chương trình khuyến mãi lễ hội (thứ tự sắp xếp 10) hiển thị trước chương trình khách hàng thân thiết chung (thứ tự sắp xếp 20)

**Gán phạm vi** (Tùy chọn):
- **Kho** - Chọn để chỉ hiển thị tại cửa hàng cụ thể
- **Nhóm cửa hàng** - Chọn để chỉ hiển thị tại các cửa hàng trong nhóm
- **Để cả hai trống** - Hiển thị tại tất cả các cửa hàng (slide toàn cầu)

## Thứ tự sắp xếp và luồng carousel

**Ví dụ carousel** (thiết bị tại Cửa hàng NYC):
- Slide 1 (thứ tự sắp xếp 10): "Lễ khai trương - Cửa hàng flagship NYC" (cửa hàng cụ thể)
- Slide 2 (thứ tự sắp xếp 15): "Khuyến mãi Ngày Kỷ niệm - Giảm 30%" (nhóm Cửa hàng Mỹ)
- Slide 3 (thứ tự sắp xếp 20): "Chương trình khách hàng thân thiết mới - Tham gia ngay hôm nay!" (toàn cầu)
- Slide 4 (thứ tự sắp xếp 30): "Theo dõi chúng tôi @yourstore" (toàn cầu)

Carousel lặp lại: 1 → 2 → 3 → 4 → 1 → 2 → ...

**Thiết bị tại Cửa hàng London** (không thuộc nhóm Cửa hàng Mỹ, cửa hàng khác):
- Slide 1 (thứ tự sắp xếp 20): "Chương trình khách hàng thân thiết mới - Tham gia ngay hôm nay!" (toàn cầu)
- Slide 2 (thứ tự sắp xếp 30): "Theo dõi chúng tôi @yourstore" (toàn cầu)

Carousel lặp lại: 1 → 2 → 1 → 2 → ...

Sử dụng thứ tự sắp xếp để ưu tiên nội dung quan trọng nhất đầu tiên trong chuỗi xoay.

## Chiến lược kích hoạt theo mùa

**Vấn đề**: Tạo hoặc xóa slide cho mỗi chương trình khuyến mãi theo mùa là rất phiền phức.

**Giải pháp**: Tạo slide một lần, kích hoạt/tắt theo mùa:

1. **Tạo slide cho các sự kiện lớn**:
   - "Khuyến mãi mùa hè" (Kích hoạt: Không, tạo trước)
   - "Quay lại trường học" (Kích hoạt: Không, tạo trước)
   - "Ngày Black Friday" (Kích hoạt: Không, tạo trước)
   - "Khuyến mãi lễ hội" (Kích hoạt: Không, tạo trước)

2. **Kích hoạt khi cần thiết**:
   - 1 tháng 6: Đặt "Khuyến mãi mùa hè" → Kích hoạt: Có
   - 15 tháng 8: Đặt "Khuyến mãi mùa hè" → Kích hoạt: Không, đặt "Quay lại trường học" → Kích hoạt: Có
   - 20 tháng 11: Đặt "Ngày Black Friday" → Kích hoạt: Có
   - 1 tháng 12: Đặt "Ngày Black Friday" → Kích hoạt: Không, đặt "Khuyến mãi lễ hội" → Kích hoạt: Có

3. **Tắt sau sự kiện**:
   - Giữ thư viện slide được tổ chức
   - Tái sử dụng slide hàng năm (cập nhật hình ảnh nếu cần, giữ cấu hình)

## Ví dụ về trường hợp sử dụng

**Trường hợp sử dụng 1: Khuyến mãi theo mùa**
- Hình ảnh: Nền đỏ với văn bản trắng "SUMMER SALE - UP TO 60% OFF"
- Tiêu đề: "Khuyến mãi mùa hè"
- Phụ đề: "Giảm 50-60% cho các mặt hàng chọn lọc. Hỏi nhân viên để biết thêm chi tiết."
- Phạm vi: Tất cả cửa hàng (toàn cầu)
- Thứ tự sắp xếp: 10 (ưu tiên cao nhất trong mùa hè)
- Kích hoạt: Chỉ trong tháng 6 đến tháng 8

**Trường hợp sử dụng 2: Chính sách cửa hàng**
- Hình ảnh: Infographic hiển thị các bước chính sách hoàn tiền
- Tiêu đề: "Trả hàng dễ dàng"
- Phụ đề: "30 ngày với hóa đơn. Không có câu hỏi nào."
- Phạm vi: Tất cả cửa hàng (toàn cầu)
- Thứ tự sắp xếp: 40 (ưu tiên thấp hơn khuyến mãi)
- Kích hoạt: Toàn năm

**Trường hợp sử dụng 3: Ra mắt sản phẩm mới**
- Hình ảnh: Hình ảnh sản phẩm chính của sản phẩm mới
- Tiêu đề: "MỚI: Tai nghe không dây Pro"
- Phụ đề: "Hiện có tại cửa hàng và trực tuyến. $199.99"
- Phạm vi: Tất cả cửa hàng (toàn cầu)
- Thứ tự sắp xếp: 5 (ưu tiên cao nhất trong tuần ra mắt)
- Kích hoạt: Chỉ trong tuần ra mắt, sau đó tắt

**Trường hợp sử dụng 4: Sự kiện địa phương**
- Hình ảnh: Poster chạy từ thiện địa phương
- Tiêu đề: "Hỗ trợ địa phương"
- Phụ đề: "Hãy tham gia cùng chúng tôi tại cuộc đua 5K cộng đồng vào ngày 15 tháng 6!"
- Phạm vi: Cửa hàng cụ thể (chỉ Cửa hàng NYC)
- Thứ tự sắp xếp: 8 (ưu tiên cho cửa hàng này)
- Kích hoạt: 2 tuần trước sự kiện

**Trường hợp sử dụng 5: Chương trình khách hàng thân thiết**
- Hình ảnh: Hình ảnh thẻ khách hàng thân thiết với ví dụ điểm
- Tiêu đề: "Tích lũy điểm thưởng"
- Phụ đề: "Tham gia chương trình khách hàng thân thiết của chúng tôi và tích lũy 1 điểm cho mỗi $1 chi tiêu"
- Phạm vi: Tất cả cửa hàng (toàn cầu)
- Thứ tự sắp xếp: 30 (nội dung luôn luôn cần thiết)
- Kích hoạt: Toàn năm

## Quản lý slide

**Xem danh sách slide**:
- Hiển thị tất cả các slide với hình ảnh xem trước, tiêu đề, phạm vi, trạng thái
- Lọc theo kích hoạt/không kích hoạt
- Lọc theo phạm vi (xem tất cả slide toàn cầu, tất cả slide nhóm, v.v.)

**Kích hoạt/deaktivate hàng loạt**:
- Chọn nhiều slide trong danh sách
- Sử dụng hành động quản trị để kích hoạt hoặc tắt tất cả cùng lúc
- Hữu ích cho chuyển đổi theo mùa (tắt tất cả slide mùa hè, kích hoạt tất cả slide mùa thu)

**Kiểm tra slide**:
- Sau khi tạo hoặc cập nhật slide, di chuyển đến thiết bị POS
- Để thiết bị trở lại trạng thái không hoạt động (không có giao dịch)
- Kiểm tra slide xuất hiện trong carousel
- Kiểm tra chất lượng hình ảnh, khả năng đọc văn bản chồng, thời gian hiển thị

**Cập nhật slide đang hoạt động**:
- Các thay đổi sẽ có hiệu lực khi carousel được làm mới lần tiếp theo (thường <30 giây)
- Không cần khởi động lại các thiết bị

## Một số mẹo

- **Thiết kế cho khoảng cách** - Khách hàng xem màn hình từ 2-6 feet; sử dụng văn bản lớn và độ tương phản cao
- **Giữ thông điệp đơn giản** - Slide hiển thị trong <10 giây; một thông điệp rõ ràng mỗi slide
- **Sử dụng kích hoạt theo mùa** - Tạo một lần, bật/tắt hàng năm thay vì tạo lại
- **Ưu tiên bằng thứ tự sắp xếp** - Các chương trình khuyến mãi quan trọng nhất nên có thứ tự sắp xếp thấp nhất (xuất hiện trước)
- **Kiểm tra trên thiết bị thực tế** - Cân bằng màu sắc màn hình khác nhau; xác nhận slide trông tốt trên màn hình cụ thể của bạn
- **Hạn chế số lượng slide đang hoạt động** - 3-5 slide đang hoạt động mỗi cửa hàng là tối ưu; 10+ slide có nghĩa là mỗi slide xuất hiện ít lần
- **Bao gồm lời kêu gọi hành động** - Nói cho khách hàng biết họ nên làm gì ("Hỏi nhân viên", "Truy cập trang web", "Quét mã QR trên hóa đơn")
- **Cập nhật thường xuyên** - Các chương trình khuyến mãi cũ (giảm giá đã hết hạn, sự kiện đã qua) làm giảm lòng tin của khách hàng
- **Sử dụng phạm vi một cách chiến lược** - Các chương trình khuyến mãi khu vực (phạm vi nhóm) và sự kiện địa phương (phạm vi cửa hàng) sẽ cảm thấy liên quan hơn so với nội dung toàn cầu liên tục

