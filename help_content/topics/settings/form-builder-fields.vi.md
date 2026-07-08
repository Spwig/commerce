---
title: Các trường và quy tắc xác thực của Trình tạo biểu mẫu
---

Các trường biểu mẫu là các khối xây dựng của biểu mẫu của bạn—mỗi trường thu thập một mảnh dữ liệu từ người dùng. Trình tạo biểu mẫu cung cấp 22 loại trường từ các trường nhập văn bản đơn giản đến các thang đánh giá nâng cao và trình chọn sản phẩm. Cấu hình mỗi trường với nhãn, quy tắc xác thực, văn bản hướng dẫn và logic điều kiện để tạo các biểu mẫu động thích ứng dựa trên phản hồi của người dùng. Các trường có thể là bắt buộc hoặc tùy chọn, được xác thực bằng các mẫu regex và được thiết kế với các lớp CSS tùy chỉnh.

Sử dụng hướng dẫn này để hiểu tất cả các loại trường có sẵn, khi nào nên sử dụng từng loại và cách cấu hình xác thực và logic điều kiện.

## Cơ bản cấu hình trường

Mỗi trường chia sẻ các cài đặt chung sau:

**Định danh**:
- **Tên trường** - Tên máy tính để lưu trữ dữ liệu (không có khoảng trắng, sử dụng dấu gạch dưới: `email_address`)
- **Loại trường** - Xác định hành vi nhập và hiển thị
- **Bước gán** - Bước nào trường thuộc về (chỉ dành cho biểu mẫu nhiều bước)

**Hiển thị**:
- **Nhãn** - Câu hỏi hoặc hướng dẫn hiển thị cho người dùng (ví dụ: "Bạn có địa chỉ email là gì?")
- **Dấu nhắc** - Văn bản gợi ý bên trong trường nhập (ví dụ: "you@example.com")
- **Văn bản hướng dẫn** - Hướng dẫn bổ sung dưới trường (ví dụ: "Chúng tôi sẽ không bao giờ chia sẻ email của bạn")
- **Giá trị mặc định** - Giá trị được điền sẵn (người dùng có thể thay đổi nó)

**Bố cục**:
- **Chiều rộng** - Toàn bộ (100%), Một nửa (50%) hoặc Một phần ba (33%) chiều rộng biểu mẫu
- **Lớp CSS** - Các lớp thiết kế bổ sung cho thiết kế tùy chỉnh
- **Thứ tự** - Vị trí trong bước (kéo để sắp xếp lại)

**Xác thực**:
- **Bắt buộc** - Bật/tắt trạng thái bắt buộc (dấu sao đỏ xuất hiện trên nhãn)
- **Chiều dài tối thiểu/tối đa** - Giới hạn ký tự (trường văn bản)
- **Giá trị tối thiểu/tối đa** - Giới hạn số (trường số)
- **Mẫu xác thực** - Mẫu regex tùy chỉnh cho xác thực phức tạp
- **Thông báo lỗi** - Văn bản tùy chỉnh hiển thị khi xác thực thất bại

## Các trường nhập văn bản

**Văn bản đơn dòng** (`text`):
- Nhập văn bản cơ bản cho các phản hồi ngắn
- Xác thực: chiều dài tối thiểu/tối đa, mẫu regex
- Trường hợp sử dụng: Tên, địa chỉ, mã sản phẩm, câu trả lời ngắn
- Ví dụ: "Họ và tên đầy đủ", "Địa chỉ đường phố", "Tên công ty"

**Văn bản nhiều dòng** (`textarea`):
- Khu vực văn bản có thể mở rộng cho nội dung dài hơn (3-10 hàng)
- Xác thực: chiều dài tối thiểu/tối đa
- Trường hợp sử dụng: Nhận xét, phản hồi, mô tả chi tiết, tin nhắn
- Ví dụ: "Hãy cho chúng tôi biết về trải nghiệm của bạn", "Ghi chú bổ sung"

**Địa chỉ email** (`email`):
- Xác thực email cụ thể (yêu cầu @ và tên miền)
- Bàn phím di động hiển thị phím @ nổi bật
- Trường hợp sử dụng: Email liên hệ, đăng ký bản tin, tạo tài khoản
- Ví dụ: "Địa chỉ email", "Email làm việc"

**Số điện thoại** (`phone`):
- Tự động định dạng số điện thoại
- Bàn phím di động hiển thị bố cục số
- Xác thực: mẫu cấu hình được (hỗ trợ định dạng quốc tế)
- Trường hợp sử dụng: Số điện thoại liên hệ, số điện thoại khẩn cấp, lịch hẹn
- Ví dụ: "Số điện thoại", "Di động", "Số liên hệ"

**Số** (`number`):
- Nhập số với các điều khiển tăng/giảm
- Xác thực: giá trị tối thiểu/tối đa, bước tăng
- Trả về số (không phải chuỗi) trong phản hồi
- Trường hợp sử dụng: Số lượng, độ tuổi, năm kinh nghiệm, số tiền ngân sách
- Ví dụ: "Bạn có bao nhiêu nhân viên?", "Tuổi của bạn", "Năm kinh nghiệm"

**URL** (`url`):
- Xác thực URL (yêu cầu http:// hoặc https://)
- Bàn phím di động hiển thị phím .com
- Trường hợp sử dụng: Trang web, hồ sơ LinkedIn, liên kết danh mục đầu tư
- Ví dụ: "Trang web công ty", "Liên kết danh mục đầu tư"

## Các trường lựa chọn

**Chọn từ danh sách thả xuống** (`select`):
- Chọn một tùy chọn từ danh sách thả xuống
- Cấu hình: mảng {value, label} tùy chọn
- Hỗ trợ chọn mặc định
- Trường hợp sử dụng: Danh mục, các bang/quốc gia, lựa chọn trạng thái
- Ví dụ: "Chọn quốc gia của bạn", "Bộ phận", "Bạn biết đến chúng tôi qua đâu?"
- Tốt nhất cho: 5+ tùy chọn (ít hơn tùy chọn sử dụng nút bấm thay thế)

**Nút bấm** (`radio`):
- Chọn một tùy chọn từ các tùy chọn hiển thị (tất cả tùy chọn được hiển thị)
- Cấu hình: mảng {value, label} tùy chọn
- Trải nghiệm người dùng tốt hơn select cho 2-4 tùy chọn
- Trường hợp sử dụng: Câu hỏi có/không, giới tính, sở thích với ít lựa chọn
- Ví dụ: "Bạn có thể giới thiệu chúng tôi không?", "Phương thức liên hệ ưa thích"

**Hộp kiểm** (`checkbox`):
- Hộp kiểm bật/tắt đơn (bật/tắt)
- Trả về true/false trong phản hồi
- Trường hợp sử dụng: Chấp nhận điều khoản, thỏa thuận, sở thích đơn
- Ví dụ: "Tôi đồng ý với các điều khoản và điều kiện", "Đăng ký nhận bản tin"

**Nhóm hộp kiểm** (`checkbox_group`):
- Nhiều lựa chọn từ các tùy chọn (người dùng có thể chọn 0, 1 hoặc nhiều)
- Cấu hình: mảng {value, label} tùy chọn
- Trả về mảng các giá trị được chọn
- Trường hợp sử dụng: Lựa chọn đa, sở thích, tính năng cần thiết
- Ví dụ: "Những chủ đề nào quan tâm đến bạn?", "Chọn tất cả các mục áp dụng"

## Các trường đánh giá

**Đánh giá sao** (`rating_stars`):
- Thang đánh giá sao trực quan (thường là 1-5 sao)
- Cấu hình:
  - `max_stars`: 3-10 sao (mặc định: 5)
  - `allow_half`: true/false cho đánh giá bán sao
  - `icon`: fa-star (mặc định) hoặc fa-heart
  - `color`: mã màu hex (mặc định: #FFD700 vàng)
- Trường hợp sử dụng: Đánh giá sản phẩm, chất lượng dịch vụ, điểm hài lòng
- Ví dụ: "Đánh giá trải nghiệm của bạn", "Dịch vụ của chúng tôi như thế nào?"

**Thang đánh giá Likert** (`rating_likert`):
- Thang đánh giá câu phát biểu: không đồng ý mạnh → đồng ý mạnh
- Cấu hình:
  - `scale_type`: 5_point (1-5) hoặc 7_point (1-7)
  - `labels`: tùy chỉnh văn bản đầu cuối (trái: "Không đồng ý mạnh", phải: "Đồng ý mạnh")
- Trả về giá trị số (1-5 hoặc 1-7)
- Trường hợp sử dụng: Câu hỏi khảo sát, thang đánh giá sự đồng ý, đo lường tâm lý
- Ví dụ: "Sản phẩm đáp ứng nhu cầu của tôi", "Dịch vụ khách hàng hữu ích"

**Điểm NPS (Điểm Người Giới Thiệu)** (`rating_nps`):
- Thang 0-10: "Không có khả năng gì" đến "Rất có khả năng"
- Cấu hình:
  - `low_label`: văn bản đầu cuối bên trái (mặc định: "Không có khả năng gì")
  - `high_label`: văn bản đầu cuối bên phải (mặc định: "Rất có khả năng")
- Trả về giá trị 0-10 (0-6 = người làm giảm, 7-8 = người trung lập, 9-10 = người làm tăng)
- Trường hợp sử dụng: Khảo sát NPS, khả năng giới thiệu, đo lường lòng trung thành
- Ví dụ: "Bạn có khả năng giới thiệu chúng tôi cho bạn bè không?"

## Các trường nâng cao

**Tải lên tệp** (`file`):
- Tải lên một hoặc nhiều tệp
- Cấu hình:
  - `max_size_mb`: giới hạn kích thước tệp mỗi tệp (mặc định: 5MB)
  - `allowed_types`: mảng các phần mở rộng (ví dụ: ["pdf", "doc", "docx", "jpg", "png"])
  - `max_files`: số lượng tệp tối đa (1 cho một tệp, 2+ cho nhiều tệp)
- Trả về đường dẫn tệp (s) trong phản hồi
- Tệp được lưu trữ tại `/media/form_uploads/{form-slug}/`
- Trường hợp sử dụng: Tải lên CV, nộp tài liệu, đính kèm hình ảnh
- Ví dụ: "Tải lên CV của bạn", "Đính kèm tài liệu hỗ trợ"

**Trình chọn sản phẩm** (`product_select`):
- Chọn nhiều sản phẩm từ danh mục sản phẩm của bạn
- Cấu hình:
  - `category_filters`: giới hạn đến các danh mục cụ thể (mảng các ID danh mục)
  - `max_selections`: 1 cho một sản phẩm, 2+ cho nhiều sản phẩm
  - `display_mode`: "list" (mặc định) hoặc "grid" (với hình thu nhỏ)
- Trả về ID/SKU sản phẩm trong phản hồi
- Trường hợp sử dụng: Khuyến nghị sản phẩm, danh sách yêu thích, khảo sát phản hồi, bộ sản phẩm
- Ví dụ: "Bạn quan tâm đến sản phẩm nào?", "Chọn các mặt hàng yêu thích của bạn"

**Ngày** (`date`):
- Giao diện chọn ngày (hộp thoại lịch)
- Trả về định dạng ISO (YYYY-MM-DD)
- Xác thực: ngày tối thiểu/tối đa
- Trường hợp sử dụng: Ngày sinh, ngày sự kiện, lịch hẹn, hạn chót
- Ví dụ: "Ngày sinh", "Ngày lịch hẹn ưa thích"

**Thời gian** (`time`):
- Chọn thời gian (giờ và phút)
- Trả về định dạng thời gian ISO (HH:MM)
- Trường hợp sử dụng: Thời gian lịch hẹn, cửa sổ khả dụng
- Ví dụ: "Thời gian ưa thích", "Sau thời gian này"

**Ngày và giờ** (`datetime`):
- Chọn ngày và giờ kết hợp
- Trả về định dạng datetime ISO đầy đủ
- Trường hợp sử dụng: Lên lịch sự kiện, đặt lịch hẹn
- Ví dụ: "Thời gian bắt đầu sự kiện", "Cửa sổ giao hàng"

## Các trường bố cục (không phải trường nhập)

**Tiêu đề phần** (`heading`):
- Văn bản tiêu đề để tổ chức các phần biểu mẫu
- Cấu hình: cấp độ tiêu đề (h2, h3, h4)
- Không thu thập dữ liệu
- Trường hợp sử dụng: Chia biểu mẫu dài thành các phần hợp lý
- Ví dụ: "Thông tin cá nhân", "Chi tiết liên hệ", "Sở thích"

**Đoạn văn mô tả** (`paragraph`):
- Khối văn bản phong phú cho hướng dẫn hoặc thông tin
- Không thu thập dữ liệu
- Hỗ trợ định dạng cơ bản (in đậm, in nghiêng, liên kết)
- Trường hợp sử dụng: Hướng dẫn từng bước, tuyên bố pháp lý, giải thích
- Ví dụ: Thông báo chính sách bảo mật, giải thích sự đồng ý GDPR

**Đường phân cách** (`divider`):
- Đường phân cách ngang trực quan
- Không thu thập dữ liệu
- Trường hợp sử dụng: Tổ chức trực quan giữa các phần

**Trường ẩn** (`hidden`):
- Trường ẩn với giá trị được lập trình
- Cấu hình: `default_value` (bắt buộc)
- Không hiển thị nhãn hoặc văn bản hướng dẫn cho người dùng
- Trường hợp sử dụng: Tham số UTM, dữ liệu theo dõi, ID phiên, mã giới thiệu
- Ví dụ: Trường ẩn có giá trị từ tham số URL

## Quy tắc xác thực trường

**Trường bắt buộc**:
- Bật hộp kiểm "Bắt buộc" trong cài đặt trường
- Dấu sao đỏ (*) xuất hiện bên cạnh nhãn
- Biểu mẫu không thể gửi nếu các trường bắt buộc trống
- Thông báo tùy chỉnh: "Trường này là bắt buộc" (hoặc thông báo tùy chỉnh)

**Chiều dài tối thiểu/tối đa** (trường văn bản):
- Đặt số lượng ký tự tối thiểu: ngăn phản hồi quá ngắn
- Đặt số lượng ký tự tối đa: ngăn đầu vào quá dài
- Ví dụ: Trường thông báo yêu cầu tối thiểu 10 ký tự (ngăn phản hồi "ok")

**Giá trị tối thiểu/tối đa** (trường số):
- Đặt giá trị số tối thiểu: ngăn độ tuổi âm, số lượng
- Đặt giá trị số tối đa: giới hạn đầu vào trong phạm vi hợp lý
- Ví dụ: Trường độ tuổi yêu cầu tối thiểu 18, tối đa 120

**Mẫu xác thực** (regex):
- Biểu thức chính quy tùy chỉnh cho xác thực phức tạp
- Các mẫu phổ biến:
  - Mã bưu điện: `^{5}(-{4})?$` (định dạng Mỹ)
  - Điện thoại: `^{3}{3}-{4}$` (định dạng Mỹ)
  - Mã sản phẩm: `^[A-Z]{2}{4}$` (2 chữ cái, 4 chữ số)
- Yêu cầu thông báo lỗi tùy chỉnh khi sử dụng mẫu

**Xác thực tệp**:
- Kích thước tệp tối đa: ngăn tải lên lớn (mặc định 5MB)
- Loại tệp được phép: danh sách trắng các phần mở rộng cụ thể (an ninh)
- Ví dụ: Trường CV cho phép ["pdf", "doc", "docx"], tối đa 2MB

## Logic điều kiện

Tạo các biểu mẫu động nơi các trường xuất hiện/thoạt ra dựa trên phản hồi của người dùng:

**Cách quy tắc điều kiện hoạt động**:
1. Người dùng trả lời "trường nguồn" (triggers)
2. Hệ thống đánh giá quy tắc: toán tử + giá trị so sánh
3. Nếu điều kiện đúng, hành động được thực thi (hiển thị/ẩn trường hoặc bước)
4. Nhiều quy tắc có thể được nối tiếp (quy tắc A kích hoạt quy tắc B)

**Các toán tử có sẵn**:
- **Bằng** (`equals`): khớp chính xác (ví dụ: quốc gia bằng "US")
- **Không bằng** (`not_equals`): bất kỳ thứ gì ngoại trừ giá trị
- **Chứa** (`contains`): văn bản bao gồm chuỗi con (không phân biệt hoa thường)
- **Lớn hơn** (`greater_than`): so sánh số (ví dụ: tuổi > 18)
- **Nhỏ hơn** (`less_than`): so sánh số (ví dụ: điểm đánh giá < 3)
- **Trống** (`is_empty`): trường không có giá trị
- **Không trống** (`is_not_empty`): trường có bất kỳ giá trị nào
- **Trong danh sách** (`in_list`): giá trị là một trong ["Tùy chọn 1", "Tùy chọn 2"]

**Các hành động có sẵn**:
- **Hiển thị trường** - Hiển thị trường ẩn
- **Ẩn trường** - Ẩn trường (xóa giá trị nếu ẩn)
- **Yêu cầu trường** - Làm trường bắt buộc
- **Không yêu cầu trường** - Làm trường tùy chọn
- **Đặt giá trị** - Điền giá trị vào trường
- **Hiển thị bước** - Hiển thị bước ẩn (chỉ dành cho biểu mẫu nhiều bước)
- **Ẩn bước** - Ẩn bước (chỉ dành cho biểu mẫu nhiều bước)
- **Bỏ qua đến bước** - Nhảy đến bước cụ thể (chỉ dành cho biểu mẫu nhiều bước)

**Ví dụ quy tắc**:
- NẾU `contact_method` BẰNG "phone" THÌ hiển thị trường `phone_number`
- NẾU `rating` NHỎ HƠN "3" THÌ yêu cầu trường `improvement_feedback`
- NẾU `country` TRONG DANH SÁCH ["US", "CA"] THÌ hiển thị bước `shipping_details`
- NẾU `budget` LỚN HƠN "10000" THÌ hiển thị trường `enterprise_features`

**Tạo quy tắc điều kiện**:
1. Nhấp vào tab "Quy tắc điều kiện" trong bảng điều khiển bên phải
2. Nhấp vào "Thêm quy tắc"
3. Chọn trường nguồn (trigger)
4. Chọn toán tử (cách so sánh)
5. Nhập giá trị so sánh (so sánh với giá trị nào)
6. Chọn hành động (làm gì)
7. Chọn mục tiêu (trường hoặc bước bị ảnh hưởng)
8. Tùy chọn: Đặt độ ưu tiên (các quy tắc có độ ưu tiên cao hơn được đánh giá trước)
9. Lưu quy tắc

**Ưu tiên quy tắc**:
- Số cao hơn được đánh giá trước (ưu tiên 100 trước ưu tiên 10)
- Sử dụng ưu tiên khi các quy tắc xung đột hoặc nối tiếp
- Ví dụ: Quy tắc A (ưu tiên 100) hiển thị trường, Quy tắc B (ưu tiên 50) yêu cầu nó (A được thực thi trước, sau đó là B)

## Các mẫu trường phổ biến

**Biểu mẫu liên hệ**:
- Họ và tên đầy đủ (text, bắt buộc)
- Email (email, bắt buộc)
- Điện thoại (phone)
- Chủ đề (select với các tùy chọn: "Bán hàng", "Hỗ trợ", "Hợp tác")
- Thông báo (textarea, bắt buộc, tối thiểu 10 ký tự)

**Phản hồi sản phẩm**:
- Sản phẩm (product_select, chọn một)
- Đánh giá tổng thể (rating_stars, 5 sao)
- Điều kiện: NẾU đánh giá < 3 THÌ yêu cầu "Chúng tôi có thể cải thiện điều gì?" (textarea)
- Điểm NPS (rating_nps)

**Ứng tuyển việc làm**:
- Bước 1: Cá nhân (tên, email, điện thoại)
- Bước 2: CV (tải lên tệp, cho phép ["pdf", "doc"], tối đa 2MB)
- Bước 3: Khả năng (ngày bắt đầu, checkbox_group cho các ngày làm việc)
- Điều kiện: NẾU "years_experience" > 5 THÌ hiển thị trường "trải nghiệm lãnh đạo"

## Một số mẹo

- **Sử dụng loại trường phù hợp** - Trường email cho email (không phải text), cung cấp xác thực và bàn phím di động tốt hơn
- **Giữ nhãn ngắn gọn** - Sử dụng văn bản hướng dẫn cho chi tiết, không phải nhãn
- **Nhóm các trường liên quan** - Sử dụng tiêu đề và đường phân cách để tổ chức trực quan
- **Kiểm tra xác thực** - Xem trước biểu mẫu và thử gửi với dữ liệu không hợp lệ
- **Giới hạn kích thước tải lên tệp** - Tối đa 5MB ngăn quá tải máy chủ từ các tệp lớn
- **Sử dụng logic điều kiện một cách tiết kiệm** - Quá nhiều quy tắc làm người dùng bối rối; giữ biểu mẫu đơn giản
- **Đặt giá trị tối đa thực tế** - Tuổi tối đa 120, số lượng tối đa 100 (ngăn lỗi gõ như 1000)
- **Cung cấp ví dụ mẫu** - Nếu sử dụng xác thực regex, hãy hiển thị ví dụ trong văn bản hướng dẫn
- **Làm rõ các trường bắt buộc** - Tên và email cho biểu mẫu liên hệ, luôn bắt buộc
- **Sử dụng nút bấm cho 2-4 tùy chọn** - Danh sách thả xuống cho 5+ tùy chọn (cải thiện trải nghiệm người dùng)
- **Trường nhập nửa chiều rộng cho đầu vào ngắn** - Điện thoại và mã bưu điện có thể là nửa chiều rộng, tiết kiệm không gian dọc
- **Trình chọn sản phẩm cho danh sách yêu thích** - Cho phép khách hàng chọn nhiều sản phẩm để khuyến nghị

