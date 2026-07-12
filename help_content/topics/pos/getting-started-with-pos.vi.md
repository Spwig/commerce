---
title: Bắt đầu với POS
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: getting-started-dashboard.webp
  description: POS dashboard as it appears on a fresh install with no terminals registered
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/pos/terminal-provider/wizard/step1/
  filename: getting-started-provider-wizard-step1.webp
  description: Payment provider wizard first step showing available provider options
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/catalog/warehouse/
  filename: getting-started-store-location.webp
  description: Warehouse list showing a store location with the POS toggle enabled
  save-to: core/static/core/admin/img/help/pos/
-->

Spwig POS biến bất kỳ máy tính bảng hoặc trình duyệt nào thành một quầy thanh toán đầy đủ trong cửa hàng — được kết nối với danh mục sản phẩm, kho hàng và lịch sử đơn hàng của bạn. Danh sách kiểm tra này sẽ hướng dẫn bạn từ việc cài đặt mới đến việc hoàn tất giao dịch bán hàng đầu tiên của bạn. Mỗi bước đều có liên kết đến chủ đề riêng nếu bạn muốn xem chi tiết đầy đủ.

![Bảng điều khiển POS](/static/core/admin/img/help/pos/getting-started-dashboard.webp)

## Bước 1: Kích hoạt POS cho một địa điểm cửa hàng

Các thiết bị POS được liên kết với một địa điểm cửa hàng vật lý. Trong Spwig, các địa điểm cửa hàng là kho hàng được đánh dấu là địa điểm bán lẻ.

1. Di chuyển đến **Catalog > Warehouses** trong thanh bên quản trị của bạn.
2. Mở kho hàng bạn muốn sử dụng làm cửa hàng, hoặc tạo một kho hàng mới.
3. Chọn **Retail location** và nhập tên hiển thị **POS** (ví dụ: "High Street Store"). Tên này sẽ xuất hiện trên hóa đơn và trình chọn thiết bị.
4. Lưu kho hàng.

Nếu bạn có nhiều cửa hàng hoặc muốn nhóm chúng lại để báo cáo theo khu vực, hãy tạo **Store Group** trước tại **POS > Store Groups**, sau đó gán mỗi kho hàng vào nhóm đó. Các nhóm cửa hàng cho phép bạn thiết lập tiền tệ, múi giờ và mẫu hóa đơn chung mà tất cả các địa điểm trong nhóm kế thừa.

## Bước 2: Tạo hoặc xác minh ít nhất một tài khoản nhân viên có quyền truy cập POS

Nhân viên của bạn đăng nhập vào POS bằng cùng một thông tin xác thực mà họ sử dụng cho quản trị Spwig. Bất kỳ tài khoản nhân viên nào có trạng thái **Active** và ít nhất quyền `pos_admin` đều có thể truy cập POS.

Để kiểm tra hoặc cấp quyền truy cập, hãy đi đến **Settings > Staff Management**, mở tài khoản nhân viên và xác nhận rằng họ đã được gán vai trò POS phù hợp. Không cần tài khoản POS riêng biệt.

## Bước 3: Đăng ký thiết bị POS đầu tiên của bạn

Một thiết bị đại diện cho một quầy thanh toán hoặc thiết bị duy nhất. Bạn đăng ký nó trong quản trị, sau đó ghép nối thiết bị vật lý với nó bằng mã ghép nối một lần.

1. Di chuyển đến **POS > POS Terminals** và nhấp vào **+ Add POS Terminal**.
2. Đặt tên cho thiết bị (ví dụ: "Front Register") và gán nó cho địa điểm cửa hàng bạn đã kích hoạt ở Bước 1.
3. Lưu thiết bị. Spwig tạo ra **mã ghép nối 8 ký tự** — bạn sẽ thấy nó trên trang chi tiết thiết bị.
4. Trên thiết bị bạn muốn sử dụng làm quầy thanh toán, mở trình duyệt và đi đến `/pos/`.
5. Nhập mã ghép nối khi được yêu cầu. Thiết bị hiện đã được liên kết với thiết bị này.

Mã ghép nối chỉ sử dụng được một lần. Nếu bạn cần ghép nối lại thiết bị, hãy mở thiết bị trong quản trị và nhấp vào **Regenerate pairing code**.

Để biết các tùy chọn cấu hình phần cứng (máy in hóa đơn, máy quét mã vạch, ngăn đựng tiền), xem [Cấu hình thiết bị POS](pos-terminal-setup).

## Bước 4: Cấu hình nhà cung cấp thanh toán

Nhà cung cấp thanh toán kết nối máy đọc thẻ của bạn với mạng thanh toán như Stripe Terminal hoặc Square. Sử dụng hướng dẫn thiết lập 5 bước để nhập thông tin xác thực của bạn.

1. Di chuyển đến **POS > Payment Providers** và nhấp vào **Configure provider**.
2. Hướng dẫn sẽ mở tại `/admin/pos/terminal-provider/wizard/step1/`.

![Hướng dẫn nhà cung cấp thanh toán](/static/core/admin/img/help/pos/getting-started-provider-wizard-step1.webp)

3. Chọn nhà cung cấp của bạn (ví dụ: **Stripe Terminal**) và làm theo hướng dẫn trên màn hình qua tất cả năm bước: chọn nhà cung cấp → hướng dẫn thiết lập → nhập thông tin xác thực → kiểm tra kết nối → cấu hình địa điểm.
4. Biểu tượng **Connected** màu xanh lá cây xác nhận tích hợp đang hoạt động.


Nếu bạn chỉ cần thanh toán tiền mặt và nhập thẻ thủ công, hãy chọn **Manual** làm nhà cung cấp — không yêu cầu thông tin xác thực.

Để xem các trường thông tin xác thực chi tiết cho từng nhà cung cấp được hỗ trợ, vui lòng xem [Cài đặt nhà cung cấp thanh toán POS](pos-payment-provider-setup).

## Bước 5: Kết nối thiết bị đọc thẻ

Với nhà cung cấp thanh toán đã được kết nối, bạn có thể ghép một thiết bị đọc thẻ vật lý với một trong các máy tính của bạn bằng hướng dẫn 3 bước của thiết bị đọc thẻ.

1. Truy cập **POS > Card Readers** và nhấn **Add reader**.
2. Hướng dẫn thiết bị bắt đầu tại `/admin/pos/reader/wizard/step1/`.
3. Chọn nhà cung cấp của bạn, sau đó chọn **Register new device** (nhập mã được hiển thị trên màn hình thiết bị) hoặc **Discover existing** (Spwig sẽ truy xuất các thiết bị đã được đăng ký với nhà cung cấp).
4. Trên bước cuối cùng, gán thiết bị đọc thẻ với máy tính bạn đã tạo ở Bước 3.

Mỗi máy tính chỉ hỗ trợ một thiết bị đọc thẻ được gán. Bạn có thể gán lại thiết bị đọc thẻ bất kỳ lúc nào từ danh sách Card Readers.

## Bước 6: Thiết kế hóa đơn (tùy chọn cho ngày đầu tiên)

Spwig tạo ra mẫu hóa đơn mặc định tự động. Bạn có thể bắt đầu bán hàng ngay lập tức mà không cần chỉnh sửa — mẫu mặc định sẽ in tên cửa hàng, địa chỉ, chi tiết bán hàng, phương thức thanh toán và chân trang "Cảm ơn bạn đã mua hàng!".

Khi bạn đã sẵn sàng tùy chỉnh, hãy truy cập **POS > Receipt Templates**. Các tùy chọn bao gồm logo của bạn, số thuế, mã QR quảng cáo, chính sách hoàn tiền và chiều rộng giấy in (58mm hoặc 80mm cho máy in nhiệt). Bạn có thể tạo mẫu riêng cho từng cửa hàng hoặc nhóm cửa hàng.

## Bước 7: Mở ca bán hàng đầu tiên của bạn

Các ca bán hàng theo dõi người đã xử lý các giao dịch và số tiền mặt nên có trong ngăn kéo. Nhân viên thu ngân mở và đóng ca bán hàng trực tiếp trên giao diện POS.

1. Trên thiết bị đã ghép, truy cập `/pos/` và đăng nhập bằng thông tin xác thực của nhân viên.
2. Chọn máy tính và vị trí cửa hàng.
3. Spwig sẽ nhắc bạn **đếm số dư mở đầu** — nhập số tiền mặt hiện có trong ngăn kéo (nhập `0` nếu ngăn kéo trống).
4. Nhấn **Open Shift**. Bây giờ ngăn kéo đã sẵn sàng để bán hàng.

Để biết giải thích đầy đủ về các ca bán hàng, các khoản chuyển tiền mặt và báo cáo đối chiếu, vui lòng xem [Quản lý ca bán hàng POS](pos-shifts).

## Bước 8: Hoàn tất giao dịch đầu tiên của bạn

Khi một ca bán hàng đã được mở, việc bán hàng trở nên đơn giản:

1. Tìm kiếm sản phẩm theo tên, quét mã vạch hoặc duyệt qua các danh mục để thêm các mặt hàng vào giỏ hàng.
2. Áp dụng giảm giá hoặc mã khuyến mãi nếu cần.
3. Nhấn **Charge** để bắt đầu thanh toán. Chọn phương thức thanh toán (tiền mặt, thẻ qua thiết bị đọc thẻ hoặc thanh toán chia nhỏ).
4. Với thanh toán bằng thẻ, thiết bị đọc thẻ sẽ nhắc khách hàng chạm hoặc chèn thẻ của họ.
5. Hóa đơn được in tự động (hoặc hiển thị tùy chọn hóa đơn số). Đơn hàng được lưu vào lịch sử đơn hàng của bạn theo thời gian thực.

## Bước 9: Đóng ca bán hàng vào cuối ngày

Đóng ca bán hàng sẽ khóa ngăn kéo và tạo báo cáo đối chiếu.

1. Từ menu POS, nhấn **Close Shift**.
2. Đếm số tiền mặt trong ngăn kéo và nhập tổng số khi được nhắc.
3. Spwig tính toán số tiền mặt dự kiến dựa trên số dư mở đầu, doanh thu tiền mặt và bất kỳ khoản chuyển tiền mặt nào trong ca, và hiển thị sự chênh lệch.
4. Xác nhận để đóng ca. Báo cáo ca sẽ được lưu và hiển thị trong **POS > Shifts** trong bảng điều khiển của bạn.

Ghi lại bất kỳ khoản tiền mặt nào được rút ra hoặc thêm vào ngăn kéo trong ngày như **cash movements** (qua menu ca) thay vì điều chỉnh số lượng đóng ca — điều này giúp giữ cho báo cáo đối chiếu của bạn chính xác.

## Một số lưu ý

- Hoàn thành các bước 1 đến 5 trước ngày kinh doanh đầu tiên của bạn.

Các bước 6 đến 9 có thể được thực hiện vào ngày kinh doanh.
- Sử dụng mật khẩu nhân viên mạnh nhưng dễ nhớ — nhân viên POS sẽ nhập thông tin xác thực tại quầy, vì vậy mật khẩu quá phức tạp sẽ làm chậm họ lại.
- Nếu thiết bị đọc thẻ không hiển thị trực tuyến, nhấn **Sync readers** trên trang Card Readers để tải trạng thái mới nhất từ nhà cung cấp của bạn.
- Thử toàn bộ quy trình (mở ca → bán hàng → hóa đơn → đóng ca) với giao dịch kiểm tra 0,01 đô la trước giai đoạn kinh doanh bận rộn của bạn.
- POS hoạt động ngoại tuyến cho các giao dịch tiền mặt cơ bản.

Thanh toán qua máy đọc thẻ yêu cầu kết nối internet để xác thực.
- Bạn có thể có nhiều máy đọc thẻ tại một địa điểm cửa hàng — thêm một bản ghi máy đọc thẻ mới trong trang quản trị và ghép nối nó với thiết bị khác.