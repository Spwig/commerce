---
title: Chế độ bảo trì
---

Chế độ bảo trì tạm thời đưa cửa hàng của bạn offline và hiển thị cho khách hàng một thông báo "chúng tôi sẽ quay lại sớm". Trong khi đang ở chế độ bảo trì, phần backend quản trị vẫn hoàn toàn truy cập được — bạn có thể tiếp tục làm việc trong khi khách hàng bị giữ lại trên trang bảo trì.

Sử dụng chế độ bảo trì trước khi thực hiện các thay đổi có thể gây ra trạng thái không nhất quán tạm thời, ví dụ như chạy một lần nhập hàng sản phẩm lớn, áp dụng một thiết kế chủ đề lớn, hoặc chờ đợi một thao tác khôi phục hoàn tất.

![Chuyển đổi chế độ bảo trì trên bảng điều khiển hệ thống](/static/core/admin/img/help/maintenance-mode/system-dashboard-maintenance.webp)

## Kích hoạt chế độ bảo trì

1. Di chuyển đến **Quản lý > Chỉ số hệ thống**
2. Nhấp vào **Bảng điều khiển hệ thống** từ thanh công cụ
3. Trong bảng **Trạng thái cửa hàng**, nhấp vào **Kích hoạt chế độ bảo trì**
4. Tùy chọn nhập một **Lý do** — đây là thông tin tham khảo cho riêng bạn và không hiển thị cho khách hàng (ví dụ: `Cập nhật danh mục sản phẩm đang diễn ra`)
5. Xác nhận bằng cách nhấp vào **Kích hoạt**

Cửa hàng của bạn sẽ lập tức bắt đầu hiển thị trang bảo trì cho tất cả các khách truy cập. Phần backend quản trị không bị ảnh hưởng và bạn có thể tiếp tục làm việc bình thường.

## Điều khách hàng nhìn thấy

Khi chế độ bảo trì đang hoạt động, mọi trang của cửa hàng của bạn (cửa hàng, trang sản phẩm, thanh toán, và các trang tài khoản) sẽ hiển thị một thông báo bảo trì được thương hiệu hóa. Thông báo cho khách hàng biết cửa hàng tạm thời không khả dụng và khuyến khích họ quay lại sớm.

Những khách hàng đang trong phiên làm việc hoặc đang thanh toán khi chế độ bảo trì được kích hoạt cũng sẽ thấy trang bảo trì khi họ gửi yêu cầu tiếp theo. Không có đơn hàng đang xử lý nào bị mất — dữ liệu vẫn còn khi bạn tắt chế độ bảo trì.

## Tắt chế độ bảo trì

1. Di chuyển đến **Quản lý > Chỉ số hệ thống**
2. Nhấp vào **Bảng điều khiển hệ thống**
3. Trong bảng **Trạng thái cửa hàng**, bạn sẽ thấy một thông báo xác nhận chế độ bảo trì đang hoạt động
4. Nhấp vào **Tắt chế độ bảo trì**
5. Xác nhận khi được nhắc

Cửa hàng sẽ trở lại hoạt động ngay lập tức. Khách hàng có thể duyệt và mua hàng như bình thường.

## Khi Spwig kích hoạt chế độ bảo trì tự động

Một số thao tác hệ thống sẽ kích hoạt chế độ bảo trì tự động và bật lại cửa hàng khi chúng hoàn tất:

- **Cập nhật nền tảng** — quá trình cập nhật sẽ kích hoạt chế độ bảo trì trước khi áp dụng các thay đổi và tắt nó khi cập nhật hoàn tất
- **Thao tác khôi phục** — khôi phục từ bản sao lưu sẽ đặt cửa hàng vào chế độ bảo trì trong suốt quá trình khôi phục

Nếu một thao tác tự động kết thúc bất ngờ, chế độ bảo trì có thể vẫn còn hoạt động. Trong trường hợp này, hãy làm theo các bước trên để tắt nó thủ công.

## Một số mẹo

- Luôn thông báo cho nhóm của bạn trước khi kích hoạt chế độ bảo trì — nó ảnh hưởng đến tất cả các khách truy cập vào cửa hàng của bạn
- Giữ thời gian bảo trì càng ngắn càng tốt; ngay cả vài phút offline cũng có thể ảnh hưởng đến lòng tin của khách hàng
- Sử dụng trường lý do như một lời nhắc cho chính bạn về lý do tại sao chế độ bảo trì được bật — nó xuất hiện trong nhật ký hệ thống
- Nếu bạn nhận thấy chế độ bảo trì đang hoạt động nhưng không phải bạn kích hoạt, hãy kiểm tra nhật ký hệ thống để xem các thao tác tự động nào có thể đã kích hoạt nó
- Lên kế hoạch thời gian bảo trì vào các khung giờ ít lưu lượng (tối hoặc sáng sớm) để giảm thiểu ảnh hưởng đến doanh số