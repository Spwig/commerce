---
title: Dịch vụ lưu trữ của Spwig
---

Spwig bao gồm ba dịch vụ đám mây tùy chọn mà cửa hàng của bạn có thể sử dụng mà không cần bạn cấu hình hoặc lưu trữ bất cứ thứ gì: **GeoIP** xác định vị trí của khách truy cập, **Geocoder** chuyển đổi địa chỉ khách hàng thành tọa độ bản đồ, và **Push** gửi thông báo tức thì đến ứng dụng quản trị di động Spwig của bạn. Trên phiên bản Community (miễn phí), mỗi dịch vụ đi kèm với mức giới hạn hàng tháng khá lớn. Khi bất kỳ dịch vụ nào tiếp cận giới hạn của nó, Spwig sẽ cảnh báo bạn trong phần quản trị để bạn có thể quyết định có nên nâng cấp hay không trước khi khách hàng nhận thấy điều gì đó.

## Ba dịch vụ lưu trữ

### GeoIP — phát hiện quốc gia của khách truy cập

GeoIP tra cứu quốc gia của mỗi khách truy cập dựa trên địa chỉ IP của họ. Cửa hàng của bạn sử dụng thông tin này để tự động hiển thị tiền tệ phù hợp khi khách hàng truy cập, và điền trước trường quốc gia trong quá trình thanh toán. Ví dụ, một khách truy cập từ Đức sẽ thấy giá cả bằng euro, và một khách truy cập từ Nhật Bản sẽ thấy giá cả bằng yên — mà không cần chọn thủ công.

Mỗi lần tải trang mà GeoIP thực hiện tra cứu sẽ tính vào hạn mức hàng tháng của bạn. Các lần truy cập lặp lại từ cùng một phiên trình duyệt sẽ không tiêu tốn một lần tra cứu; kết quả được lưu trữ trong phiên. Các tra cứu GeoIP chỉ xảy ra trên cửa hàng, không phải trong bảng điều khiển quản trị của bạn.

### Geocoder — địa chỉ đến tọa độ

Geocoder chuyển đổi địa chỉ được khách hàng nhập vào thành tọa độ địa lý (vĩ độ và kinh độ). Cửa hàng của bạn sử dụng các tọa độ này cho hai mục đích: tính toán chi phí vận chuyển dựa trên khoảng cách khi bạn có điểm nhận hàng hoặc quy tắc vận chuyển dựa trên bán kính, và cung cấp đề xuất tự động hoàn thành địa chỉ trên trang thanh toán để khách hàng có thể tìm địa chỉ của họ nhanh chóng.

Một tra cứu Geocoder được kích hoạt khi khách hàng chọn hoặc xác nhận địa chỉ trong quá trình thanh toán. Tương tự như GeoIP, kết quả được lưu trữ để cùng một địa chỉ chỉ được tra cứu một lần mỗi phiên.

### Push — thông báo ứng dụng quản trị

Push gửi thông báo thời gian thực đến ứng dụng di động thương nhân Spwig của bạn. Khi có đơn hàng mới, khi tồn kho giảm xuống dưới ngưỡng, hoặc khi khách hàng gửi tin nhắn, Push sẽ gửi thông báo tức thì đến thiết bị của bạn để bạn có thể phản hồi mà không cần phải giữ bảng điều khiển quản trị mở.

Mỗi thông báo được gửi đến thiết bị của bạn được tính là một yêu cầu đẩy trong hạn mức hàng tháng của bạn.

## Phiên bản miễn phí Community

Trên phiên bản Community của Spwig, mỗi dịch vụ được cung cấp miễn phí lên đến giới hạn yêu cầu hàng tháng. Giới hạn chính xác được thiết lập bởi Spwig và có thể thay đổi; bảng điều khiển quản trị của bạn luôn hiển thị các con số hiện tại cho cài đặt của bạn. Các gói trả phí (Starter, Growth, Pro, Pro Plus) và các cài đặt tự lưu trữ với giấy phép trả phí có giới hạn cao hơn cho mỗi dịch vụ.

Khi một dịch vụ đạt 100% giới hạn Community, các yêu cầu đến dịch vụ đó sẽ dừng lại cho đến khi tháng lịch tiếp theo đặt lại bộ đếm. Tác động đến cửa hàng của bạn phụ thuộc vào dịch vụ nào bị ảnh hưởng:

| Dịch vụ | Điều gì xảy ra khi đạt 100% |
|---------|----------------------|
| GeoIP | Phát hiện tiền tệ tự động sẽ quay về tiền tệ mặc định của cửa hàng. Khách hàng vẫn có thể thay đổi tiền tệ thủ công. |
| Geocoder | Tự động hoàn thành địa chỉ ngừng cung cấp đề xuất. Khách hàng vẫn có thể nhập địa chỉ thủ công. Tính toán chi phí vận chuyển tiếp tục sử dụng tọa độ cuối cùng được biết. |
| Push | Các thông báo mới cho ứng dụng quản trị sẽ được xếp hàng nhưng không được gửi cho đến tháng sau hoặc nâng cấp. |

Cửa hàng của bạn vẫn hoạt động bình thường trong mọi trường hợp — không có đơn hàng nào bị mất và khách hàng vẫn có thể thanh toán. Các tác động này chỉ giới hạn ở các tính năng tiện lợi.

## Đọc bảng điều khiển

Bảng **Sử dụng dịch vụ Spwig** xuất hiện trên trang chủ bảng điều khiển quản trị của bạn. Nó hiển thị thanh tiến trình cho mỗi trong ba dịch vụ.

Mỗi hàng trong bảng điều khiển tuân theo cùng một bố cục:

- **Tên dịch vụ** (trái) — GeoIP, Tra cứu địa chỉ (Geocoder), hoặc Thông báo đẩy.
- **Thanh tiến trình** (giữa) — được lấp đầy từ trái sang phải khi mức sử dụng tăng lên.

Màu sắc của thanh thay đổi khi tiến gần đến giới hạn:
  - **Xanh lá** — mức sử dụng dưới 80%.

Tất cả đang hoạt động bình thường.

  - **Amber** — tỷ lệ sử dụng nằm giữa 80% và 99%.

Dịch vụ vẫn đang chạy nhưng đang dần tiến gần đến giới hạn.

  - **Red** — tỷ lệ sử dụng đã đạt 100%.

Dịch vụ hiện đang bị giới hạn trong tháng này.

- **Usage counts** (phía phải) — con số chính xác của các yêu cầu đã sử dụng so với tổng số được phép, ví dụ `3,241 / 10,000`.

Nhãn trong ngoặc đơn hiển thị khoảng thời gian, thường là `(tháng này)`.

Nếu tile không thể kết nối đến máy chủ cập nhật của Spwig để lấy thông tin sử dụng hiện tại của bạn (ví dụ, nếu máy chủ của bạn không có quyền truy cập internet ra ngoài), cột số liệu sẽ hiển thị dấu gạch ngang (`—`) cho dịch vụ đó. Điều này không có nghĩa là dịch vụ bị hỏng; nó chỉ có nghĩa là hiển thị số liệu sử dụng tạm thời không khả dụng.

### Nút **Upgrade**

Khi bất kỳ dịch vụ nào đạt đến 80% hoặc cao hơn, nút **Upgrade** sẽ xuất hiện ở góc trên bên phải của tile. Nhấp vào nút này sẽ mở trang nâng cấp của Spwig, nơi bạn có thể so sánh các gói và nâng cao giới hạn dịch vụ của mình. Nút sẽ biến mất khi tỷ lệ sử dụng giảm xuống dưới 80% vào đầu tháng tới.

## Thông báo cảnh báo giới hạn

Ngoài tile trên bảng điều khiển, một thông báo sẽ xuất hiện ở đầu mỗi trang quản trị khi bất kỳ dịch vụ nào vượt quá ngưỡng 80%. Thông báo chỉ hiển thị trên các cài đặt Community.

**Amber banner — đang tiến gần đến giới hạn (80–99%)**

> **Đang tiến gần đến giới hạn dịch vụ được lưu trữ:** Một trong các dịch vụ Spwig của bạn đã vượt quá 80% hạn mức của cấp Community. Nâng cấp để tăng giới hạn trước khi đạt đến giới hạn.

Thông báo này là một cảnh báo sớm. Các dịch vụ của bạn vẫn đang chạy, và bạn vẫn còn thời gian để quyết định có nên nâng cấp trước khi kết thúc tháng.

**Red banner — giới hạn đã đạt (100%)**

> **Giới hạn dịch vụ Spwig đã đạt:** Một trong các dịch vụ được lưu trữ của bạn đã đạt đến hạn mức cấp Community. Nâng cấp để duy trì hoạt động mà không bị gián đoạn.

Thông báo này xuất hiện khi ít nhất một dịch vụ đạt đến 100% và hiện đang bị giới hạn. Nhấp vào **Upgrade** trên bất kỳ thông báo nào sẽ mở cùng một trang nâng cấp như nút trên tile.

Thông báo sẽ tự động biến mất vào đầu tháng kế tiếp khi các chỉ số được đặt lại, hoặc ngay lập tức sau khi bạn nâng cấp lên gói trả phí.

## Cảnh báo qua email tại 90%

Khi bất kỳ dịch vụ nào vượt quá 90% hạn mức, Spwig cũng sẽ gửi một email cảnh báo một lần đến địa chỉ được cấu hình trong cài đặt cửa hàng của bạn (**Settings > Store Settings > Contact > Admin Email**). Email được gửi tối đa một lần mỗi dịch vụ mỗi tháng, vì vậy bạn sẽ không bị ngập tràn các thông báo. Không có email được gửi khi đạt đến 100% vì lúc đó thông báo trong trang quản trị đã làm rõ tình hình.

Nếu bạn không nhận được email, hãy kiểm tra xem địa chỉ email quản trị của bạn đã được thiết lập đúng dưới **Settings > Store Settings**.

## Nâng cấp gói của bạn

Khi bạn nâng cấp từ gói Community lên bất kỳ gói trả phí nào, các giới hạn cao hơn sẽ có hiệu lực ngay lập tức — không cần khởi động lại cửa hàng hoặc thay đổi cấu hình. Tile trên bảng điều khiển sẽ hiển thị giới hạn mới, cao hơn vào lần làm mới tiếp theo (trong vòng năm phút).

Để nâng cấp, hãy nhấp vào nút **Upgrade** trên tile bảng điều khiển hoặc thông báo giới hạn, hoặc truy cập trực tiếp trang nâng cấp của Spwig. Các gói trả phí bao gồm ba dịch vụ được lưu trữ giống nhau (GeoIP, Geocoder, Push) với giới hạn hàng tháng cao hơn, cùng với quyền truy cập vào dịch vụ gửi email do Spwig cung cấp và hỗ trợ ưu tiên.

## Tự lưu trữ và giấy phép Pro

Nếu bạn chạy cài đặt Spwig tự lưu trữ với giấy phép trả phí, cấp giấy phép của bạn sẽ xác định giới hạn dịch vụ, giống như gói được lưu trữ tương ứng. Cửa hàng của bạn vẫn cần quyền truy cập internet ra ngoài để đến `updates.spwig.com` để nền tảng có thể tải và xác minh cấu hình cấp của bạn. Các chỉ số sử dụng được hiển thị trên tile bảng điều khiển được lấy từ các điểm cuối dịch vụ được lưu trữ tại `geoip.spwig.com`, `geocoder.spwig.com`, và `push.spwig.com`.

Hiện tại không có tùy chọn nào để thay thế GeoIP, Geocoder hoặc Push bằng các giải pháp tự lưu trữ — các dịch vụ này chỉ được cung cấp bởi hạ tầng của Spwig và được bao gồm trong tất cả các phiên bản.

## Mẹo

Giữ nguyên toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- **Kiểm tra tile thường xuyên vào cuối các tháng bận rộn** — một sự kiện bán hàng hoặc khuyến mãi có thể làm tăng đáng kể các truy vấn GeoIP và Geocoder.

Tile sẽ thông báo cho bạn trước khi khách hàng bị ảnh hưởng.
- **Việc chuyển đổi tiền tệ là điều mà hầu hết khách hàng không nhận ra** — nếu GeoIP đạt giới hạn, khách hàng sẽ thấy tiền tệ mặc định của cửa hàng bạn.

Điều này hiếm khi là vấn đề nghiêm trọng đối với các cửa hàng chủ yếu phục vụ một thị trường; nó quan trọng hơn đối với các cửa hàng thực sự quốc tế.
- **Tự động điền địa chỉ là sự tiện lợi, không phải là rào cản** — khi Geocoder bị giới hạn, khách hàng vẫn có thể nhập và gửi địa chỉ của họ bình thường.

Nếu bạn thường xuyên chạy các chương trình khuyến mãi thu hút lượng giao dịch cao, hãy cân nhắc nâng cấp trước các thời điểm bận rộn.
- **Việc giới hạn gửi thông báo không làm mất thông báo vĩnh viễn** — các thông báo được xếp hàng trong thời gian bị giới hạn sẽ không được gửi lại khi tháng mới bắt đầu hoặc sau khi nâng cấp.

Nếu bạn phụ thuộc nhiều vào thông báo đẩy cho các cảnh báo đơn hàng khẩn cấp, việc nâng cấp trước khi đạt giới hạn đảm bảo bạn không bỏ lỡ bất cứ điều gì.
- **Kích thước bộ nhớ cache 5 phút có nghĩa là tile không hoàn toàn theo thời gian thực** — các con số sử dụng được làm mới khoảng mỗi 5 phút ở nền sau.

Trong các giai đoạn lưu lượng truy cập bất thường cao, lượng sử dụng thực tế có thể hơi vượt trước những gì tile hiển thị.
- **Thiết lập địa chỉ email quản trị viên** — email cảnh báo 90% chỉ hoạt động nếu **Settings > Store Settings > Admin Email** được điền đầy đủ.

Hãy kiểm tra lại xem địa chỉ này đã được thiết lập đúng để bạn nhận được thông báo trước khi xảy ra vấn đề.