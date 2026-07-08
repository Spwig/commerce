---
title: Quản lý máy POS
---

Quản lý máy POS là nền tảng của hoạt động bán lẻ của bạn. Mỗi máy đại diện cho một thiết bị vật lý (máy tính bảng, máy tính hoặc phần cứng POS chuyên dụng) nơi nhân viên xử lý các giao dịch. Cấu hình máy với việc gán kho, ủy quyền nhân viên, tích hợp phần cứng và cài đặt đồng bộ ngoại tuyến. Theo dõi tình trạng máy với việc theo dõi tín hiệu nhịp tim thời gian thực và mở khóa máy từ xa khi có sự cố. Việc quản lý máy đúng cách đảm bảo hoạt động trơn tru trong cửa hàng và ngăn chặn xung đột cấu hình giữa các địa điểm.

Truy cập **POS > Máy** để đăng ký máy mới, xem trạng thái trực tuyến/đang ngoại tuyến và quản lý tất cả cài đặt máy.

![Danh sách máy](/static/core/admin/img/help/managing-pos-terminals/terminal-list.webp)

## Danh sách máy

Danh sách máy hiển thị tất cả các máy đã đăng ký với thông tin trạng thái chính:

**Tên máy** - Nhãn mô tả cho máy (ví dụ: "Thanh toán 1", "Quầy chính", "Máy di động")

**UUID** - Nhận dạng duy nhất được tạo tự động khi tạo (dùng nội bộ để nhận dạng thiết bị)

**Kho** - Vị trí vật lý được gán cho máy này (xác định tính khả dụng của hàng tồn kho và gán đơn hàng)

**Trạng thái trực tuyến** - Chỉ báo trực tiếp cho thấy máy hiện đang được kết nối:
- **Điểm xanh** - Trực tuyến (nhận được tín hiệu nhịp tim trong vòng 5 phút gần đây)
- **Điểm đỏ** - Ngoại tuyến (không có tín hiệu nhịp tim hơn 5 phút)
- **Điểm xám** - Chưa từng ghép nối (máy được tạo nhưng thiết bị chưa bao giờ kết nối)

**Tín hiệu nhịp tim cuối cùng** - Thời gian dấu thời gian của tín hiệu gần nhất từ máy (cập nhật mỗi 5 phút khi trực tuyến)

**Mã ghép nối** - Mã chữ số 8 ký tự được sử dụng cho ghép nối thiết bị ban đầu (ẩn sau lần sử dụng đầu tiên)

**Người dùng được gán** - Số lượng nhân viên được ủy quyền sử dụng máy này

## Tạo máy mới

Nhấn **+ Thêm máy** để đăng ký thiết bị POS mới:

![Biểu mẫu thêm máy](/static/core/admin/img/help/managing-pos-terminals/terminal-add-form.webp)

### Cấu hình cơ bản

**Tên máy** - Chọn tên mô tả cho thấy:
- Vị trí vật lý: "Quầy đầu ra phía Bắc"
- Chức năng: "Quầy hoàn tiền"
- Thứ tự: "Thanh toán 1", "Thanh toán 2", "Thanh toán 3"

Tên giúp nhân viên xác định máy trong quá trình phân công ca và khắc phục sự cố. Sử dụng quy tắc đặt tên nhất quán trên tất cả các địa điểm.

**Kho** - **YÊU CẦU** - Chọn kho mà máy này hoạt động:
- Xác định kho nào có hàng tồn kho sẵn sàng để bán
- Các đơn hàng được đặt trên máy này được gán cho kho này
- Kiểm tra tính khả dụng hàng tồn kho trong kho được gán
- **Không thể xử lý giao dịch nếu không gán kho**

Nếu bạn có nhiều địa điểm bán lẻ, hãy tạo kho riêng biệt cho mỗi địa điểm và gán máy theo cách tương ứng.

**Trạng thái hoạt động** - Bật/tắt máy mà không xóa cấu hình:
- Máy không hoạt động không thể ghép nối
- Các phiên làm việc hiện tại trên máy không hoạt động sẽ hết hạn ngay lập tức
- Sử dụng để tạm thời tắt máy bị đánh cắp hoặc hư hỏng

### Gán nhân viên

**Người dùng được gán** - Chọn nhân viên nào có thể truy cập máy này:
- Chỉ các người dùng được gán mới có thể đăng nhập vào máy
- Người dùng cũng phải có quyền POS trong vai trò nhân viên của họ
- Gán không người dùng sẽ khóa máy hiệu quả
- Mẫu phổ biến: Gán tất cả nhân viên cửa hàng cho tất cả máy trong cửa hàng

**Ví dụ về trường hợp sử dụng**:
- **Cửa hàng tổng hợp**: Gán tất cả nhân viên cho tất cả máy (bất kỳ nhân viên thu ngân nào cũng có thể làm việc tại bất kỳ quầy nào)
- **Cửa hàng theo bộ phận**: Gán nhân viên theo bộ phận cho máy của bộ phận
- **Nhiều địa điểm**: Gán nhân viên theo địa điểm cho máy của địa điểm
- **Quản lý**: Gán quản lý cho tất cả máy để truy cập giám sát

Người dùng không được gán máy sẽ thấy thông báo lỗi "Không được ủy quyền cho máy này" khi cố gắng đăng nhập.

### Cấu hình phần cứng

Trường **Cấu hình phần cứng** là một cấu trúc JSON xác định các thiết bị ngoại vi:

**Máy in nhiệt**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  }
}
```

**Máy quét mã vạch USB**:
```json
{
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  }
}
```

**Két tiền** (kết nối với máy in):
```json
{
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

**Ví dụ đầy đủ**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  },
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  },
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

Để trống nếu máy không có thiết bị ngoại vi (phù hợp cho máy di động hoặc máy tính bảng không có máy in/máy quét).

### Cài đặt bộ đệm ngoại tuyến

Cấu hình lượng dữ liệu máy bộ đệm cho hoạt động ngoại tuyến:

**Số ngày đồng bộ hóa đơn hàng** (7-30 ngày, mặc định: 14):
- Số ngày đơn hàng gần đây được bộ đệm cục bộ
- Giá trị cao hơn = có nhiều dữ liệu lịch sử hơn có sẵn ngoại tuyến
- Giá trị thấp hơn = đồng bộ hóa nhanh hơn, sử dụng ít bộ nhớ hơn
- **Khuyến nghị**: 7 ngày cho máy cao cấp, 14 ngày cho sử dụng bình thường, 30 ngày cho hoạt động kiểm toán nhiều

**Giới hạn đồng bộ hóa đơn hàng** (200-1000 đơn hàng, mặc định: 500):
- Số lượng đơn hàng tối đa được bộ đệm bất kể khoảng thời gian
- Ngăn chặn việc sử dụng bộ nhớ quá mức trên các máy cao cấp
- **Khuyến nghị**: 200 cho máy tính bảng có bộ nhớ hạn chế, 500 cho máy tiêu chuẩn, 1000 cho thiết bị POS chuyên dụng

**Điều chỉnh**:
- **Cài đặt cao hơn**: Truy cập ngoại tuyến tốt hơn đến dữ liệu lịch sử, đồng bộ hóa ban đầu chậm hơn, sử dụng nhiều bộ nhớ hơn
- **Cài đặt thấp hơn**: Đồng bộ hóa nhanh hơn, ít bộ nhớ hơn, lịch sử ngoại tuyến bị giới hạn

Máy tải xuống X đơn hàng gần đây nhất (trong Y ngày) trong mỗi chu kỳ đồng bộ hóa. Nếu máy xử lý 50 đơn hàng/ngày và sync_days là 14, kỳ vọng ~700 đơn hàng được bộ đệm (có thể đạt giới hạn đồng bộ hóa).

## Quy trình ghép nối máy

Sau khi tạo máy, ghép nối thiết bị vật lý:

1. **Tạo mã ghép nối** - Được tạo tự động khi bạn lưu máy (8 ký tự chữ số)

2. **Ghi chú mã** - Hiển thị trong danh sách máy và xem chi tiết (hết hạn sau lần ghép nối đầu tiên thành công)

3. **Di chuyển đến thiết bị máy** - Trên thiết bị vật lý (máy tính bảng/máy tính), mở trình duyệt và đi đến: `https://yourstore.com/pos/`

4. **Nhập mã ghép nối** - Nhập mã 8 ký tự khi được nhắc

5. **Máy tải xuống cấu hình** - Thiết bị nhận được:
   - Gán kho
   - Cấu hình phần cứng (máy in, máy quét, két tiền)
   - Cài đặt bộ đệm ngoại tuyến
   - Danh sách người dùng được gán
   - Đồng bộ hóa danh mục sản phẩm ban đầu

6. **Màn hình đăng nhập xuất hiện** - Máy hiển thị màn hình đăng nhập cho người dùng được gán

7. **Nhân viên đăng nhập** - Nhập thông tin xác thực cho người dùng được gán cho máy này

8. **Đồng bộ hóa ban đầu hoàn tất** - Máy tải xuống:
   - Các đơn hàng gần đây (theo sync_days và sync_limit)
   - Danh mục sản phẩm đầy đủ cho kho được gán
   - Cơ sở dữ liệu khách hàng
   - Cấu hình khuyến mãi

9. **Máy sẵn sàng** - Màn hình "Sẵn sàng để bán" xuất hiện với thanh tìm kiếm

10. **Mã ghép nối đã sử dụng** - Mã bị xóa khỏi quản trị; tạo mã mới nếu cần ghép nối lại

**Tạo lại mã ghép nối**: Nếu bạn cần ghép nối lại máy (đặt lại thiết bị, xóa bộ nhớ trình duyệt, phần cứng mới), sử dụng hành động quản trị **Tạo lại mã ghép nối**. Điều này vô hiệu hóa mã cũ và tạo mã mới.

## Theo dõi trạng thái máy

### Hệ thống nhịp tim

Máy ping máy chủ mỗi **5 phút** với tín hiệu nhịp tim chứa:
- UUID máy
- Thời gian hiện tại
- Số lượng người dùng trực tuyến
- Thời gian đồng bộ hóa cuối cùng
- Trạng thái công nhân dịch vụ

**Chỉ báo trạng thái trực tuyến**:
- **Xanh** - Nhận được tín hiệu nhịp tim trong vòng 5 phút gần đây (máy trực tuyến và hoạt động)
- **Đỏ** - Không có tín hiệu nhịp tim hơn 5 phút (máy ngoại tuyến hoặc ngắt kết nối)
- **Xám** - Máy chưa từng ghép nối (không bao giờ nhận được tín hiệu nhịp tim)

**Trường hợp sử dụng**:
- **Mở cửa hàng hàng ngày**: Kiểm tra tất cả máy đều trực tuyến trước khi mở cửa hàng
- **Khắc phục sự cố**: Xác định máy nào đang gặp vấn đề kết nối
- **Kiểm toán**: Xác minh máy đang hoạt động trong giờ làm việc

### Thời gian dấu thời gian nhịp tim cuối cùng

Hiển thị thời gian và ngày cụ thể của tín hiệu nhịp tim gần nhất. Sử dụng để:
- Xác định máy đã ngoại tuyến bao lâu
- Nhận biết các mô hình (ví dụ: máy ngoại tuyến mỗi đêm khi đóng cửa)
- Xác minh tần suất đồng bộ hóa (nên cập nhật mỗi ~5 phút khi trực tuyến)

## Tính năng Mở khóa từ xa

Khi máy trở nên không phản hồi hoặc bị kẹt trên màn hình (crash phần mềm, vấn đề hết phiên, trình duyệt bị treo), sử dụng hành động quản trị **Mở khóa từ xa**:

**Cách hoạt động**:
1. Chọn máy gặp sự cố trong danh sách quản trị
2. Chọn **Mở khóa từ xa** từ danh sách hành động quản trị
3. Xác nhận hành động
4. Máy chủ gửi tín hiệu mở khóa qua phản hồi nhịp tim
5. Máy nhận tín hiệu trong chu kỳ nhịp tim tiếp theo (<5 phút)
6. Máy buộc đăng xuất người dùng hiện tại và trở lại màn hình đăng nhập

**Khi sử dụng**:
- Máy bị kẹt trên màn hình giao dịch
- Nhân viên không thể đăng xuất (nút đăng xuất không phản hồi)
- Phiên làm việc vẫn hoạt động nhưng máy không phản hồi
- Trình duyệt bị treo nhưng cookie phiên vẫn tồn tại

**Lưu ý quan trọng**: Mở khóa từ xa **không khởi động lại thiết bị hoặc trình duyệt**—nó chỉ buộc đăng xuất và xóa phiên. Nếu máy hoàn toàn bị treo, nhân viên có thể cần khởi động lại trình duyệt hoặc thiết bị thủ công.

## Chỉnh sửa cấu hình máy

Nhấn vào máy trong danh sách để chỉnh sửa cấu hình của nó:

![Biểu mẫu chỉnh sửa máy](/static/core/admin/img/help/managing-pos-terminals/terminal-edit-form.webp)

**An toàn để thay đổi khi máy đang trực tuyến**:
- Tên máy
- Người dùng được gán
- Cấu hình phần cứng (có hiệu lực sau khi máy khởi động lại ứng dụng)
- Cài đặt bộ đệm ngoại tuyến (có hiệu lực trên chu kỳ đồng bộ hóa tiếp theo)

**Yêu cầu ghép nối lại**:
- Gán kho (thay đổi kho yêu cầu ghép nối lại để đồng bộ hóa hàng tồn kho mới)

**Không thể thay đổi**:
- UUID (nhận dạng duy nhất không thể thay đổi)

Các thay đổi đối với hầu hết các cài đặt áp dụng trên chu kỳ nhịp tim/sync tiếp theo. Thay đổi cấu hình phần cứng yêu cầu nhân viên đóng và mở lại ứng dụng POS (hoặc làm mới trình duyệt).

## Khắc phục sự cố các vấn đề phổ biến

**Máy hiển thị "Không được ủy quyền" khi đăng nhập**:
- Kiểm tra người dùng có trong danh sách **Người dùng được gán** cho máy này không
- Kiểm tra người dùng có quyền POS trong **Nhân viên & Quyền > Vai trò** không
- Kiểm tra máy được đánh dấu **Trạng thái hoạt động**

**Máy không thể ghép nối (mã không hợp lệ)**:
- Mã ghép nối hết hạn sau lần sử dụng đầu tiên—tạo lại nếu cần
- Mã nhạy cảm với chữ hoa/chữ thường—kiểm tra chữ hoa
- Kiểm tra máy được đánh dấu **Trạng thái hoạt động**

**Máy hiển thị ngoại tuyến (điểm đỏ)**:
- Kiểm tra thiết bị có kết nối internet không
- Kiểm tra máy thực sự đang chạy (trình duyệt mở đến URL /pos/)
- Đảm bảo tường lửa không chặn yêu cầu nhịp tim
- Chờ 5 phút cho chu kỳ nhịp tim tiếp theo

**Máy đồng bộ hóa chậm**:
- Giảm **Số ngày đồng bộ hóa đơn hàng** từ 30 xuống 7
- Giảm **Giới hạn đồng bộ hóa đơn hàng** từ 1000 xuống 200
- Kiểm tra tốc độ mạng tại vị trí máy
- Xác minh máy chủ không đang quá tải

**Máy in không hoạt động**:
- Kiểm tra IP và cổng máy in trong **Cấu hình phần cứng**
- Kiểm tra kết nối máy in từ máy (ping địa chỉ IP)
- Kiểm tra máy in có tương thích ESC/POS không
- Kiểm tra máy in đã bật và trực tuyến

## Một số mẹo

- **Quy tắc đặt tên quan trọng** - Sử dụng quy tắc đặt tên nhất quán (vị trí + số) để đơn giản hóa quản lý quy mô
- **Luôn gán kho trước khi ghép nối** - Máy không thể xử lý giao dịch nếu không gán kho
- **Kiểm tra cấu hình phần cứng trước khi triển khai** - In hóa đơn kiểm tra để xác minh tích hợp máy in/két tiền
- **Theo dõi nhịp tim hàng ngày** - Thiết lập thói quen kiểm tra tất cả máy đều trực tuyến khi cửa hàng mở
- **Giảm giới hạn đồng bộ cho máy di động** - Máy tính bảng và điện thoại có lợi khi sync_days: 7, sync_limit: 200
- **Sử dụng mở khóa từ xa một cách tiết kiệm** - Đăng xuất cưỡng chế làm gián đoạn các giao dịch đang diễn ra; xác nhận máy thực sự bị kẹt trước tiên
- **Ghi lại mã ghép nối** - Viết mã trước khi triển khai máy xuống sàn bán lẻ (trong trường hợp thiết lập mất nhiều thời gian hơn mong đợi)
- **Gán quản lý cho tất cả máy** - Đảm bảo giám sát có thể truy cập bất kỳ quầy nào để hủy bỏ, hoàn tiền và khắc phục sự cố

