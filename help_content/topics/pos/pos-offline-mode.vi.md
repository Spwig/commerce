---
title: Chế độ ngoại tuyến POS & Cài đặt ứng dụng
---

<!-- screenshots-needed:
- url: /pos/
  filename: pos-pwa-idle.webp
  description: POS PWA tại trạng thái nghỉ — giao diện chính chọn đăng nhập/máy tính POS hiển thị thương hiệu Spwig POS
  save-to: core/static/core/admin/img/help/pos-offline-mode/
  viewport: 1440x900
  notes: Hình ảnh Add-to-Home-Screen (iPad Safari, Android Chrome) là cụ thể cho hệ điều hành/trình duyệt
         hình ảnh tham khảo được chú thích. Phiên bản chụp màn hình nên sử dụng chế độ giả lập thiết bị
         hoặc hình ảnh tham khảo thay vì cố gắng kích hoạt lời nhắc cài đặt trình duyệt.
-->

Spwig POS là một Progressive Web App (PWA). Nó chạy hoàn toàn trong trình duyệt và có thể được cài đặt vào màn hình chính của thiết bị như một ứng dụng bản địa. Vì ứng dụng, danh mục sản phẩm của bạn và lịch sử đơn hàng gần đây được lưu trữ cục bộ trên thiết bị, máy tính tiền của bạn vẫn hoạt động trong thời gian ngắn mất kết nối mạng và kết nối chậm.

Chủ đề này giải thích chính xác những gì vẫn hoạt động khi kết nối bị ngắt, cách các giao dịch được ghi lại khi kết nối quay lại, cách cài đặt POS vào màn hình chính của thiết bị, và cách cập nhật đến các thiết bị đã cài đặt.

## Cách chế độ ngoại tuyến hoạt động

Khi bạn mở POS lần đầu tiên trên một thiết bị, trình duyệt sẽ tải xuống và lưu trữ toàn bộ ứng dụng — giao diện, hình ảnh và tất cả mã hỗ trợ. Một thành phần nền gọi là Service Worker quản lý bộ nhớ đệm này. Từ thời điểm đó, ứng dụng sẽ tải từ bộ nhớ đệm cục bộ ngay cả khi máy chủ không thể truy cập được.

Ngoài bộ nhớ đệm ứng dụng, POS duy trì một cơ sở dữ liệu cục bộ trên thiết bị (sử dụng IndexedDB lưu trữ tích hợp của trình duyệt). Cơ sở dữ liệu này lưu trữ:

- **Sản phẩm và biến thể** — được đồng bộ từ danh mục của bạn và được làm mới mỗi 5 phút khi đang online
- **Danh mục** — được đồng bộ khi khởi động và được làm mới cùng với sản phẩm
- **Mức tồn kho** — được đồng bộ mỗi 2 phút khi đang online (sử dụng chiến lược mạng đầu tiên, nếu máy chủ không phản hồi trong 3 giây thì sẽ chuyển sang dữ liệu được lưu trữ)
- **Hồ sơ khách hàng** — lên đến 1.000 khách hàng gần đây
- **Lịch sử đơn hàng** — một số lượng cấu hình được đặt trước các đơn hàng POS gần đây (mặc định: 500 đơn hàng trong 14 ngày; thiết lập theo từng máy tính tiền trong **POS > POS Terminals**)
- **Hình ảnh sản phẩm** — được lưu trữ cục bộ trong tối đa 24 giờ

Khi POS phát hiện thiết bị đã ngoại tuyến, một thanh thông báo sẽ xuất hiện ở đầu màn hình: **"Chế độ ngoại tuyến - Các giao dịch sẽ được đồng bộ khi kết nối được khôi phục."** Máy tính tiền tiếp tục hoạt động bằng dữ liệu được lưu trữ cục bộ.

## Các tính năng hoạt động khi ngoại tuyến

| Tính năng | Khả dụng ngoại tuyến |
|---------|---------------------|
| Tìm kiếm và duyệt sản phẩm | Có sẵn — sử dụng danh mục được lưu trữ cục bộ |
| Quét mã vạch | Có sẵn — quét tìm sản phẩm trong bộ nhớ đệm cục bộ |
| Thêm mặt hàng vào giỏ hàng | Có sẵn |
| Áp dụng giảm giá thủ công | Có sẵn |
| Áp dụng mã phiếu quà tặng | Không có sẵn — kiểm tra số dư yêu cầu kết nối trực tiếp |
| Thanh toán tiền mặt | Có sẵn — được ghi lại cục bộ và xếp hàng để đồng bộ |
| Thanh toán thẻ (Nhập thủ công) | Có sẵn — nhân viên xử lý trên một máy tính tiền khác và nhập tham chiếu; được ghi lại cục bộ và xếp hàng để đồng bộ |
| Thanh toán thẻ (đọc thẻ tích hợp — Stripe Terminal, v.v.) | Không có sẵn — thiết bị đọc thẻ tích hợp giao tiếp với mạng thanh toán theo thời gian thực |
| Thanh toán thẻ quà tặng | Không có sẵn — kiểm tra số dư yêu cầu kết nối trực tiếp |
| Thanh toán chia nhỏ kết hợp tiền mặt và thẻ thủ công | Có sẵn |
| In hóa đơn đến máy in mạng | Có sẵn nếu máy in trên cùng mạng cục bộ với thiết bị — in không cần truy cập internet, chỉ cần kết nối mạng cục bộ |
| Hóa đơn số (email/SMS/WhatsApp) | Không có sẵn — gửi yêu cầu kết nối trực tiếp |
| Duyệt lịch sử đơn hàng | Có sẵn — hiển thị các đơn hàng được lưu trữ với thanh thông báo cho biết bạn đang xem dữ liệu ngoại tuyến |
| Hoàn tiền và hủy bỏ | Không có sẵn — yêu cầu kết nối trực tiếp |
| Tra cứu điểm khách hàng thân thiết | Không có sẵn |
| Mở và đóng ca làm việc | Có sẵn — trạng thái ca được lưu trữ cục bộ |

## Các giao dịch được xếp hàng và đồng bộ khi kết nối quay lại

Các giao dịch ngoại tuyến không bị mất.


Khi thiết bị không thể kết nối đến máy chủ, mỗi giao dịch hoàn tất sẽ được ghi vào hàng đợi cục bộ (cơ sở dữ liệu cục bộ của thiết bị gọi là `pendingTransactions`).

Giao dịch bao gồm tất cả các mục trong giỏ hàng, số lượng, giá cả, phương thức thanh toán và thời gian hoàn tất.

Khi kết nối internet được khôi phục, POS sẽ tự động:

1. Phát hiện việc kết nối lại thông qua sự kiện `online` của trình duyệt
2. Hiển thị một thông báo: **"Đang đồng bộ N giao dịch đang chờ..."**
3. Gửi các giao dịch đã được xếp hàng đến backend theo thứ tự, sử dụng lịch trình thử lại theo cấp số nhân nếu lần thử đầu tiên thất bại (tối đa 10 lần thử trong khoảng thời gian tối đa 5 phút cho mỗi lần thử)
4. Đánh dấu mỗi giao dịch là đã đồng bộ khi backend xác nhận

**Bảo vệ chống giao dịch trùng lặp** — mỗi giao dịch được xếp hàng sẽ được gán một ID cục bộ duy nhất trước khi rời khỏi thiết bị. Backend sẽ kiểm tra ID này trước khi tạo đơn hàng. Nếu cùng một giao dịch được gửi hai lần (ví dụ, do một lần thử lại trùng với lần thử đầu tiên thành công), backend sẽ bỏ qua giao dịch trùng lặp. Bạn sẽ không bao giờ gặp tình trạng giao dịch bị tính hai lần.

**Phát hiện xung đột** — trong một số trường hợp hiếm, backend có thể đánh dấu giao dịch được xếp hàng là xung đột (ví dụ, nếu một sản phẩm đã bị xóa ở phía máy chủ trong khi thiết bị đang ngoại tuyến). Các giao dịch xung đột sẽ xuất hiện trong **POS > Cài đặt > Giao dịch đang chờ** để bạn có thể xem xét và giải quyết thủ công.

**Các điều chỉnh tồn kho ngoại tuyến** được xử lý theo cùng cách: các thay đổi tồn kho được thực hiện khi ngoại tuyến sẽ được xếp hàng và phát lại khi kết nối quay lại. Các con số tồn kho cục bộ trên thiết bị sẽ được cập nhật ngay lập tức để nhân viên thu ngân có thể thấy con số chính xác (ước tính).

## Cài đặt POS lên màn hình chính thiết bị

Cài đặt POS lên màn hình chính sẽ mang lại trải nghiệm toàn màn hình không có thanh địa chỉ trình duyệt, biểu tượng tắt nhanh trên thiết bị và thời gian khởi động nhanh hơn.

### iPad (Safari)

1. Mở Safari và truy cập URL POS của cửa hàng bạn: `https://yourstore.com/pos/`
2. Đăng nhập và hoàn tất việc ghép nối nếu đây là thiết bị mới.
3. Nhấn nút **Chia sẻ** (hình vuông với mũi tên hướng lên) trong thanh công cụ của Safari.
4. Cuộn xuống trong bảng chia sẻ và nhấn **Thêm vào Màn hình chính**.
5. Chỉnh sửa tên nếu bạn muốn (mặc định là "Spwig POS") và nhấn **Thêm**.

Biểu tượng POS hiện đã xuất hiện trên màn hình chính của iPad. Nhấn vào đó sẽ mở ứng dụng toàn màn hình mà không có thanh trình duyệt của Safari.

> **Lưu ý:** Tùy chọn "Thêm vào Màn hình chính" yêu cầu Safari trên iPad. Các trình duyệt thứ ba trên iOS (Chrome, Firefox) không hỗ trợ cài đặt PWA cho đến giữa năm 2025.

### Android (Chrome)

1. Mở Chrome và truy cập URL POS của cửa hàng bạn: `https://yourstore.com/pos/`
2. Đăng nhập và hoàn tất ghép nối nếu cần.
3. Nhấn vào **menu ba dấu chấm** (góc trên bên phải) và nhấn **Cài đặt ứng dụng** (hoặc **Thêm vào Màn hình chính** trên các phiên bản Chrome cũ hơn).
4. Xác nhận bằng cách nhấn **Cài đặt**.

Biểu tượng POS xuất hiện trên màn hình chính và trong ngăn ứng dụng. Mở từ biểu tượng sẽ mở ứng dụng ở chế độ độc lập.

### Máy tính để bàn (Chrome hoặc Edge)

1. Truy cập URL POS của cửa hàng bạn trong Chrome hoặc Edge.
2. Tìm **biểu tượng cài đặt** trong thanh địa chỉ trình duyệt (một màn hình máy tính với mũi tên hướng xuống hoặc biểu tượng "+" tùy theo phiên bản).
3. Hoặc mở **menu ba dấu chấm** và chọn **Cài đặt Spwig POS** (Chrome) hoặc **Ứng dụng > Cài đặt trang web này thành ứng dụng** (Edge).
4. Xác nhận việc cài đặt.

POS mở ra như một cửa sổ độc lập không có tab trình duyệt hoặc thanh địa chỉ. Nó xuất hiện trong danh sách ứng dụng của hệ thống và có thể được gắn vào thanh tác vụ.

## Cách ứng dụng cập nhật

POS quản lý các bản cập nhật của riêng nó thông qua Service Worker. Bạn không cần phải truy cập cửa hàng ứng dụng hoặc tải xuống bất cứ thứ gì thủ công.

**Chu kỳ cập nhật:**

1.

Mỗi lần bạn mở POS (hoặc tab trở lại hoạt động sau khi ở nền), Service Worker sẽ kiểm tra máy chủ để xem có phiên bản mới nào không.
2.

Nếu có phiên bản mới, Service Worker sẽ tải về trong nền khi bạn tiếp tục làm việc — phiên bản hiện tại của bạn sẽ không bị gián đoạn.
3.

Cập nhật sẽ có hiệu lực lần tới bạn mở POS.


Nếu ứng dụng đã mở và đang chờ đồng bộ, POS sẽ đợi hàng đợi trống trước khi thông báo rằng việc tải lại đã sẵn sàng, để tránh làm gián đoạn ca làm việc hiện tại với các giao dịch chưa đồng bộ.

**Ý nghĩa của "tải lại" khi có giao dịch đang chờ** — nếu bạn thấy thông báo yêu cầu tải lại để cập nhật và có các giao dịch ngoại tuyến đang chờ, hãy kết thúc ca làm việc hiện tại một cách rõ ràng (hoặc đợi đến khi thông báo đồng bộ biến mất) trước khi tải lại. Tải lại khi có giao dịch đang chờ sẽ không xóa chúng — chúng vẫn tồn tại trong cơ sở dữ liệu cục bộ — nhưng an toàn hơn là đồng bộ trước để xác nhận chúng đã được nhận.

**Kiểm tra phiên bản đã cài đặt** — mở POS, nhấn vào **biểu tượng menu** (ba đường ngang), và đi đến **Cài đặt**. Phiên bản hiện tại được hiển thị ở cuối bảng cài đặt.

## Lưu trữ và xóa cài đặt

POS lưu trữ nhiều loại dữ liệu cục bộ:

| Nội dung | Kích thước điển hình |
|--------|---------------------|
| Giao diện ứng dụng (HTML, CSS, JS, biểu tượng) | ~3–5 MB |
| Danh mục sản phẩm (văn bản và siêu dữ liệu) | 1–10 MB tùy theo kích thước danh mục |
| Hình ảnh sản phẩm (được lưu đệm) | 5–50 MB tùy theo kích thước danh mục |
| Lịch sử đơn hàng | 1–5 MB (500 đơn hàng) |
| Hồ sơ khách hàng | 1–3 MB (1.000 khách hàng) |
| Hàng đợi giao dịch đang chờ | Ít; được xóa khi đồng bộ |

**Nếu thiết bị thiếu không gian lưu trữ** — trình duyệt sẽ áp dụng áp lực lên bộ nhớ đệm khi thiết bị đầy. POS thiết lập bộ nhớ đệm của nó là bền vững ở nơi trình duyệt cho phép, nhưng trên các thiết bị đầy bộ nhớ, trình duyệt có thể xóa hình ảnh sản phẩm trước. Nếu hình ảnh ngừng tải, POS sẽ tải lại chúng vào lần đồng bộ tiếp theo. Các giao dịch đã đồng bộ và giao diện ứng dụng không bị ảnh hưởng.

**Khởi động lại cài đặt** — nếu POS hoạt động bất thường (bị kẹt ở phiên bản cũ, danh mục không làm mới, đồng bộ bị kẹt vĩnh viễn), bạn có thể thực hiện khởi động lại sạch sẽ:

1. **Gỡ cài đặt ứng dụng** — trên điện thoại, nhấn và giữ biểu tượng POS và chọn **Xóa** hoặc **Gỡ cài đặt**. Trên máy tính, nhấp chuột phải vào thanh tiêu đề cửa sổ ứng dụng và chọn **Gỡ cài đặt**.
2. Mở trực tiếp URL POS trong trình duyệt và đăng nhập lại.
3. Thiết bị sẽ yêu cầu mã ghép nối 8 ký tự của máy POS. Bạn có thể tìm hoặc tạo lại mã này trong quản trị tại **POS > Máy POS** — mở máy POS và nhấn **Tạo lại mã ghép nối**.
4. Mã ghép nối mới sẽ buộc POS đồng bộ lại toàn bộ dữ liệu được lưu đệm.

> **Sau khi khởi động lại**: bất kỳ giao dịch ngoại tuyến nào đã được xếp hàng nhưng chưa đồng bộ trước khi khởi động lại sẽ bị mất, vì cơ sở dữ liệu cục bộ đã được xóa. Luôn đảm bảo kết nối đã được khôi phục và thông báo đồng bộ biến mất trước khi khởi động lại cài đặt.

## Khắc phục sự cố

### POS bị kẹt ở phiên bản cũ

Worker Dịch vụ có thể chưa kích hoạt phiên bản mới. Hãy thử đóng tất cả các tab trình duyệt đang mở POS, sau đó mở lại. Nếu vấn đề vẫn tồn tại, hãy khởi động lại cài đặt như đã mô tả ở trên.

### Thông báo "Không có kết nối" không biến mất

Kiểm tra xem thiết bị có truy cập internet bên ngoài POS (thử tải một trang web khác). Nếu thiết bị đang online nhưng thông báo vẫn tồn tại:

- Máy chủ POS có thể tạm thời không thể truy cập — đợi một phút và POS sẽ tự động thử lại.
- Nếu bạn đang sử dụng mạng yêu cầu trang đăng nhập (captive portal), mở một tab trình duyệt mới, hoàn tất đăng nhập, sau đó quay lại POS.

### Một sản phẩm không xuất hiện trên POS dù tồn tại trong quản trị

POS đồng bộ sản phẩm mỗi 5 phút khi đang online. Nếu bạn vừa thêm sản phẩm trong quản trị, nhấn vào **biểu tượng menu** và đi đến **Cài đặt > Đồng bộ ngay** để kích hoạt đồng bộ tức thì. Nếu sản phẩm vẫn không xuất hiện, hãy xác nhận rằng nó được đánh dấu là **Hoạt động** và không bị loại khỏi khả năng sử dụng trên POS trong cài đặt sản phẩm.

### Giao dịch đang chờ bị kẹt ở trạng thái "Xung đột"

Đi đến **POS > Cài đặt** (trong ứng dụng POS chính) và kiểm tra bảng **Giao dịch đang chờ**.

Các giao dịch xung đột thường do sản phẩm hoặc giá đã thay đổi giữa lúc giao dịch được thực hiện ngoại tuyến và lúc nó được đồng bộ.

Bạn có thể xem chi tiết đơn hàng và, nếu đơn hàng đã được nhận đúng, đánh dấu nó là đã xem.

## Tips

- Chạy POS trên một thiết bị riêng biệt được kết nối với mạng Wi-Fi cục bộ của bạn. Các gián đoạn Wi-Fi ngắn sẽ được xử lý tự động, nhưng thiết bị dành nhiều thời gian ngoại tuyến sẽ cần nhiều thời gian hơn để đồng bộ lại khi kết nối lại.
- Khoảng thời gian đồng bộ là theo thiết bị. Nếu bạn có nhiều đầu cuối, mỗi đầu cuối sẽ đồng bộ độc lập. Một đơn hàng trên một đầu cuối sẽ xuất hiện ngay lập tức trong phần quản trị khi đồng bộ, nhưng bộ đệm đơn hàng cục bộ của đầu cuối khác chỉ được làm mới khi chu kỳ đồng bộ của nó diễn ra.
- Trước khi có sự cố internet dự kiến (ví dụ, di chuyển đến một sự kiện không có Wi-Fi), hãy mở POS khi vẫn còn kết nối để dữ liệu danh mục và tồn kho được cập nhật đầy đủ. Các giao dịch tiền mặt sẽ được xếp hàng đáng tin cậy; chỉ cần tránh các giao dịch thẻ tích hợp cho đến khi bạn quay lại online.
- Nếu bạn chỉ cần các giao dịch tiền mặt tại một sự kiện, phương thức thanh toán thẻ thủ công (nhân viên xử lý trên máy tính độc lập và nhập một tham chiếu) cũng hoạt động ngoại tuyến cho các giao dịch thẻ.
- Giữ thiết bị được cắm sạc trong ca làm việc dài — cơ sở dữ liệu cục bộ và quy trình đồng bộ không ảnh hưởng đáng kể đến pin so với màn hình, nhưng thiết bị được sạc đầy luôn an toàn hơn cho giao dịch.