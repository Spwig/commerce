---
title: Tổng quan về Công cụ Xây dựng Biểu mẫu
---

Công cụ Xây dựng Biểu mẫu tạo các biểu mẫu tùy chỉnh để thu thập dữ liệu - biểu mẫu liên hệ, khảo sát, ứng tuyển, đăng ký và nhiều hơn nữa. Xây dựng biểu mẫu trực quan với các trường kéo thả, cấu hình quy tắc xác thực, bật quy trình làm việc nhiều bước và thu thập phản hồi với phân tích chi tiết. Các biểu mẫu tích hợp liền mạch với các phần tử của Công cụ Xây dựng Trang, có thể chèn ở bất kỳ đâu trên trang web của bạn. Tất cả các lần nộp đều được lưu trữ trong cơ sở dữ liệu với đầy đủ thông tin (địa chỉ IP, trình duyệt, thời gian hoàn thành) để phân tích và xuất dữ liệu.

Sử dụng Công cụ Xây dựng Biểu mẫu khi bạn cần thu thập dữ liệu có cấu trúc từ khách hàng, dù là thông tin liên hệ đơn giản hay các ứng dụng nhiều trang phức tạp.

## Công cụ Xây dựng Biểu mẫu là gì?

Công cụ Xây dựng Biểu mẫu là một công cụ kéo thả trực quan để tạo các biểu mẫu tùy chỉnh mà không cần lập trình:

**Các loại biểu mẫu được hỗ trợ**:
- Biểu mẫu liên hệ (tên, email, tin nhắn)
- Khảo sát khách hàng (đánh giá, phản hồi, NPS)
- Đăng ký sản phẩm (bảo hành, hỗ trợ)
- Ứng tuyển việc làm (tải lên CV, nhiều bước)
- Đăng ký sự kiện (thông tin người tham dự, sở thích)
- Yêu cầu dịch vụ (yêu cầu chi tiết)
- Đăng ký bản tin (kèm hộp kiểm sở thích)

**Tính năng chính**:
- **22 loại trường** - Văn bản, email, điện thoại, tải tệp, đánh giá, lựa chọn sản phẩm và nhiều hơn nữa
- **Biểu mẫu nhiều bước** - Chia các biểu mẫu dài thành các bước hợp lý với thanh tiến độ
- **Logic điều kiện** - Hiển thị/ẩn các trường dựa trên phản hồi của người dùng
- **Quy tắc xác thực** - Trường bắt buộc, độ dài tối thiểu/tối đa, mẫu regex tùy chỉnh
- **Bảo vệ chống spam** - Trường honeypot hoặc Google reCAPTCHA v3
- **Phân tích phản hồi** - Theo dõi thời gian hoàn thành, địa chỉ IP, trình duyệt, người giới thiệu
- **Xuất CSV** - Tải xuống tất cả các phản hồi để phân tích trong Excel/Google Sheets
- **Đa ngôn ngữ** - Dịch nhãn biểu mẫu và thông báo thành tất cả các ngôn ngữ đang hoạt động

## Tạo Biểu mẫu Đầu tiên của Bạn

Truy cập **Cài đặt > Trang > Biểu mẫu** để truy cập trình quản lý biểu mẫu:

**Bước 1: Tạo Biểu mẫu Mới**
- Nhấp **+ Tạo Biểu mẫu Mới**
- Nhập tên biểu mẫu (định danh nội bộ, không hiển thị cho khách hàng)
- Nhập tiêu đề biểu mẫu (hiển thị như tiêu đề phía trên biểu mẫu)
- Tùy chọn: Thêm mô tả (văn bản hướng dẫn hiển thị dưới tiêu đề)

**Bước 2: Thêm Trường**
- Nhấp **Chỉnh sửa Thiết kế Biểu mẫu** để mở trình xây dựng trực quan
- Kéo các loại trường từ thanh bên trái ra vùng làm việc
- Nhấp vào trường để cấu hình tại bảng bên phải
- Thiết lập nhãn, nội dung gợi ý, văn bản hướng dẫn
- Bật/tắt trạng thái bắt buộc
- Thêm quy tắc xác thực

**Bước 3: Cấu hình Cài đặt Biểu mẫu**
- Thiết lập văn bản nút gửi (mặc định: "Gửi")
- Tùy chỉnh thông báo thành công (hiển thị sau khi gửi)
- Chọn bảo vệ chống spam (khuyến nghị trường honeypot)
- Bật/tắt "Yêu cầu Đăng nhập" nếu cần
- Bật "Biểu mẫu Nhiều bước" cho các biểu mẫu phức tạp

**Bước 4: Kích hoạt Biểu mẫu**
- Bật trạng thái **Kích hoạt**
- Chỉ các biểu mẫu đang hoạt động mới chấp nhận các lần nộp
- Lưu biểu mẫu

**Bước 5: Sử dụng trong Công cụ Xây dựng Trang**
- Thêm phần tử **Biểu mẫu** vào bất kỳ trang nào
- Chọn biểu mẫu của bạn từ danh sách thả xuống
- Biểu mẫu kế thừa phong cách trang
- Các lần nộp được gửi đến phía sau tự động

## Biểu mẫu Một Trang vs Nhiều Bước

**Biểu mẫu Một Trang** (mặc định):
- Tất cả các trường được hiển thị cùng lúc
- Cuộn để xem tất cả các trường
- Nút gửi ở phía dưới
- Phù hợp nhất: Biểu mẫu liên hệ, khảo sát ngắn, thu thập dữ liệu đơn giản

**Biểu mẫu Nhiều Bước**:
- Các trường được tổ chức thành các bước được đánh số
- Thanh tiến độ hiển thị bước hiện tại
- Nút điều hướng Quay lại/Tiếp theo
- Chỉ gửi ở bước cuối cùng
- Tùy chọn: Lưu các phản hồi một phần (chế độ nháp)
- Phù hợp nhất: Ứng tuyển việc làm, đăng ký, khảo sát phức tạp, quy trình thanh toán

**Bật Biểu mẫu Nhiều Bước**:
1. Bật "Biểu mẫu Nhiều bước" trong cài đặt biểu mẫu
2. Nhấp vào tab **Bước** trong bảng bên phải
3. Thêm bước (ví dụ: "Thông tin cá nhân", "Chi tiết liên hệ", "Sở thích")
4. Gán trường cho các bước bằng cách sử dụng danh sách thả xuống bước khi chỉnh sửa trường
5. Sắp xếp lại các bước bằng cách kéo
6. Thiết lập thuộc tính bước: tiêu đề, mô tả, có thể bỏ qua

**Lợi ích của Biểu mẫu Nhiều Bước**:
- Giảm tỷ lệ từ bỏ biểu mẫu (tâm lý: "chỉ có 3 câu hỏi trên trang này")
- Nhóm logic cải thiện trải nghiệm người dùng
- Chỉ số tiến độ khuyến khích hoàn thành
- Lưu nháp tùy chọn cho các biểu mẫu dài

## Giải thích Cài đặt Biểu mẫu

**Cài đặt Cơ bản**:
- **Tên Nội bộ** - Cách bạn nhận biết biểu mẫu trong quản trị (không hiển thị cho khách hàng)
- **Slug** - Nhận dạng URL (tự động tạo, được sử dụng trong điểm cuối API)
- **Tiêu đề Biểu mẫu** - Tiêu đề hiển thị phía trên biểu mẫu
- **Mô tả** - Văn bản hướng dẫn tùy chọn hiển thị dưới tiêu đề
- **Văn bản Nút Gửi** - Tùy chỉnh nhãn nút (ví dụ: "Gửi Tin Nhắn", "Ứng Tuyển Ngay")

**Thông báo**:
- **Thông báo Thành công** - Hiển thị sau khi gửi thành công (mặc định: "Cảm ơn bạn đã gửi biểu mẫu!")
- **Thông báo Lỗi** - Hiển thị nếu gửi thất bại (mặc định: "Đã xảy ra lỗi. Vui lòng thử lại.")

**Bảo mật & Truy cập**:
- **Kích hoạt** - Chỉ các biểu mẫu đang hoạt động mới chấp nhận các lần nộp (biểu mẫu không hoạt động hiển thị "Biểu mẫu không khả dụng")
- **Yêu cầu Đăng nhập** - Chỉ dành cho người dùng đã xác thực (người dùng không xác thực sẽ thấy lời nhắc đăng nhập)

**Bảo vệ chống spam**:
- **Không có** - Không có bảo vệ (không được khuyến nghị, bot sẽ gửi spam)
- **Trường Honeypot** - Trường không nhìn thấy được bắt bot (khuyến nghị cho hầu hết các nhà bán hàng)
- **Google reCAPTCHA v3** - Yêu cầu khóa trang web và khóa bí mật từ Google (bảo vệ mạnh nhất)

**Tính năng Nâng cao**:
- **Biểu mẫu Nhiều bước** - Bật quy trình làm việc từng bước
- **Lưu Phản hồi Một phần** - Cho phép người dùng lưu tiến độ và tiếp tục sau này (chỉ dành cho biểu mẫu nhiều bước)

## Tùy chọn Bảo vệ chống spam

**Trường Honeypot (Khuyến nghị)**:
- Trường không nhìn thấy được được thêm vào biểu mẫu
- Bot điền vào nó (người dùng không thể nhìn thấy)
- Các lần nộp có trường honeypot được điền sẽ bị từ chối
- Không cần cấu hình
- Không có sự phiền toái của CAPTCHA cho người dùng
- Hiệu quả chống lại hơn 95% bot spam

**Google reCAPTCHA v3**:
- Điểm nền tảng ẩn (0.0-1.0)
- Không có thử thách "nhấn đèn giao thông"
- Yêu cầu thiết lập:
  1. Tạo tài khoản tại google.com/recaptcha/admin
  2. Tạo khóa trang web và khóa bí mật
  3. Nhập khóa vào cài đặt Công cụ Xây dựng Biểu mẫu
- Robust hơn honeypot
- Sử dụng khi honeypot không đủ

**Không có**:
- Không có bảo vệ chống spam
- Chỉ sử dụng cho các biểu mẫu nội bộ hoặc kiểm tra
- Các biểu mẫu công khai sẽ bị spam nặng

## Quản lý Phản hồi Biểu mẫu

Xem tất cả các lần nộp tại **Cài đặt > Trang > Biểu mẫu > [Tên Biểu mẫu] > Phản hồi**:

**Lịch sử Phản hồi**:
- Trạng thái: nháp, đã gửi, đã hoàn thành
- Người gửi: email (nếu đã đăng nhập) hoặc "Ẩn danh"
- Địa chỉ IP và vị trí (nếu đã bật GeoIP)
- Ngày giờ gửi
- Thời gian hoàn thành (giây)

**Chi tiết Phản hồi**:
- Tất cả các giá trị trường với nhãn
- Thông tin bổ sung: trình duyệt, người giới thiệu, ngôn ngữ
- Theo dõi tiến độ (biểu mẫu nhiều bước): bước hiện tại, bước đã hoàn thành
- Kết quả hành động (nếu biểu mẫu kích hoạt hành động)

**Lọc Phản hồi**:
- Lọc theo biểu mẫu, trạng thái, khoảng thời gian
- Tìm kiếm theo email người gửi hoặc địa chỉ IP
- Sắp xếp theo ngày gửi, thời gian hoàn thành

**Xuất Phản hồi**:
- Nhấp vào nút **Xuất thành CSV**
- Tải xuống `{form-slug}_responses_{date}.csv`
- Hàng tiêu đề: Submitted At, User, IP, Status, [Field Labels]
- Một lần nộp mỗi hàng
- Mở trong Excel, Google Sheets hoặc các công cụ phân tích dữ liệu

## Sử dụng Biểu mẫu trong Trang

**Chèn Biểu mẫu**:
1. Mở trang trong Công cụ Xây dựng Trang
2. Thêm phần tử **Biểu mẫu** từ bảng điều khiển phần tử
3. Chọn biểu mẫu từ danh sách thả xuống
4. Tùy chỉnh phong cách hộp chứa biểu mẫu (nền, khoảng cách, viền)
5. Lưu và xuất bản trang

**Biểu mẫu được hiển thị cùng với**:
- Tiêu đề và mô tả biểu mẫu (từ cài đặt biểu mẫu)
- Tất cả các trường theo thứ tự (biểu mẫu một trang) hoặc bước hiện tại (biểu mẫu nhiều bước)
- Nút gửi với văn bản tùy chỉnh
- Thông báo thành công/lỗi sau khi gửi

**Kế thừa Phong cách**:
- Biểu mẫu kế thừa phong cách chủ đề trang
- Nút sử dụng phong cách nút chủ đề
- Trường đầu vào sử dụng phong cách đầu vào chủ đề
- Có thể thêm lớp CSS tùy chỉnh cho các trường để thiết kế cụ thể

## Giao Diện Công cụ Xây dựng Biểu mẫu

**Thanh bên trái - Thư viện Trường**:
- Được tổ chức theo danh mục (Văn bản, Lựa chọn, Đánh giá, Nâng cao)
- Kéo trường ra vùng làm việc hoặc nhấp để thêm
- Tìm kiếm để nhanh chóng tìm thấy loại trường

**Vùng làm việc chính - Trình chỉnh sửa Trường**:
- Tay kéo (≡) để sắp xếp lại các trường
- Nhấp vào trường để chọn và chỉnh sửa
- Nút xóa (×) trên mỗi trường
- Xem trước trực quan của trường như đã cấu hình
- Trạng thái trống với hướng dẫn khu vực kéo

**Thanh bên phải - Bảng thuộc tính**:
- **Tab Cài đặt Biểu mẫu** - Thông tin cơ bản, thông báo, bảo vệ chống spam
- **Tab Cài đặt Trường** - Cấu hình trường được chọn (nhãn, xác thực, v.v.)
- **Tab Bước** - Quản lý bước (chỉ dành cho biểu mẫu nhiều bước)
- **Tab Quy tắc Điều kiện** - Thêm logic hiển thị/ẩn dựa trên phản hồi

**Tính năng Thanh công cụ**:
- **Hủy bỏ/Làm lại** - Lịch sử chỉnh sửa đầy đủ
- **Xem trước** - Kiểm tra chức năng biểu mẫu
- **Lưu** - Tự động lưu mỗi 3 giây khi đang chỉnh sửa
- **Dịch** - Dịch văn bản biểu mẫu sang các ngôn ngữ khác

## Ví dụ Biểu mẫu Thường gặp

**Biểu mẫu Liên hệ**:
- Trường: Họ tên đầy đủ (bắt buộc), Email (bắt buộc), Điện thoại, Tin nhắn (bắt buộc)
- Nút gửi: "Gửi Tin Nhắn"
- Thành công: "Cảm ơn bạn đã liên hệ với chúng tôi! Chúng tôi sẽ trả lời trong vòng 24 giờ." 

**Khảo sát Phản hồi Sản phẩm**:
- Bước 1: Đánh giá sao, thang đo sự đồng thuận Likert
- Bước 2: Điểm NPS, đề xuất cải tiến
- Điều kiện: Nếu điểm đánh giá < 3, yêu cầu phản hồi cải tiến

**Ứng tuyển Việc làm**:
- Bước 1: Thông tin cá nhân (tên, email, điện thoại)
- Bước 2: Kinh nghiệm (tải lên CV, năm kinh nghiệm, thư giới thiệu)
- Bước 3: Khả năng có mặt (ngày bắt đầu, kỳ vọng về lương)
- Bật lưu nháp một phần (ứng viên có thể tiếp tục sau này)

**Đăng ký Bản tin với Sở thích**:
- Email (bắt buộc)
- Nhóm hộp kiểm: Sở thích (Sản phẩm, Khuyến mãi, Cập nhật blog)
- Bật reCAPTCHA (ngăn chặn đăng ký giả mạo)

## Một số Lời Khuyên

- **Bắt đầu với biểu mẫu một trang** - Chỉ thêm biểu mẫu nhiều bước nếu biểu mẫu có hơn 10 trường
- **Sử dụng honeypot trước** - Chỉ nâng cấp lên reCAPTCHA nếu spam vẫn tiếp diễn
- **Kiểm tra trước khi xuất bản** - Sử dụng chế độ xem trước để xác minh xác thực và quy trình
- **Xuất định kỳ** - Tải xuống tệp CSV phản hồi hàng tuần để sao lưu
- **Theo dõi thời gian hoàn thành** - Nếu trung bình >5 phút, biểu mẫu có thể quá dài
- **Sử dụng logic điều kiện** - Ẩn các trường không liên quan để giảm cảm giác độ dài biểu mẫu
- **Bật lưu nháp một phần cho biểu mẫu dài** - Giảm tỷ lệ từ bỏ trên các biểu mẫu nhiều bước
- **Dịch nhãn biểu mẫu** - Sử dụng hệ thống dịch nội bộ cho các trang web đa ngôn ngữ
- **Yêu cầu đăng nhập cho dữ liệu nhạy cảm** - Ngăn chặn spam không xác thực, liên kết các lần nộp với tài khoản người dùng
- **Giữ thông báo thành công cụ thể** - "Chúng tôi sẽ trả lời trong vòng 24 giờ" tốt hơn "Cảm ơn bạn"