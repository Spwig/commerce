---
title: Cài đặt nhiều loại tiền tệ
---

Cài đặt nhiều loại tiền tệ cho phép khách hàng của bạn duyệt sản phẩm và hoàn tất thanh toán bằng loại tiền tệ ưa thích của họ. Giá cả sẽ được chuyển đổi tự động từ loại tiền tệ cơ bản của bạn bằng tỷ giá từ nhà cung cấp được kết nối hoặc tỷ giá được xác định thủ công.

## Trước khi bắt đầu

Trước khi bật tính năng nhiều loại tiền tệ, bạn cần:

1. **Một nhà cung cấp tỷ giá hoạt động** - Truy cập **Settings > Tab Multi-Currency > Exchange Rates Dashboard** và kết nối ít nhất một nhà cung cấp (ví dụ như Open Exchange Rates, Fixer.io, hoặc ExchangeRate-API). Nhà cung cấp phải đang hoạt động và đồng bộ tỷ giá.
2. **Ít nhất hai loại tiền tệ** - Loại tiền tệ cơ bản của bạn cộng với một hoặc nhiều loại tiền tệ bổ sung mà bạn muốn hỗ trợ.

## Bật tính năng nhiều loại tiền tệ

Truy cập **Settings > Multi-Currency** và đánh dấu **Enable Multi-Currency**. Sau khi bật, hãy cấu hình các tùy chọn sau:

| Cài đặt | Mô tả |
|---------|-------------|
| **Chế độ chọn tiền tệ** | Cách khách hàng chọn loại tiền tệ của họ. *Tự động* phát hiện từ vị trí của họ, *Thủ công* cho phép họ chọn từ trình chuyển đổi, *Cả hai* kết hợp cả hai phương pháp. |
| **Hiển thị trình chuyển đổi tiền tệ** | Hiển thị trình chọn tiền tệ trên cửa hàng của bạn để khách hàng có thể thay đổi tiền tệ thủ công. |
| **Vị trí trình chuyển đổi** | Vị trí trình chuyển đổi tiền tệ xuất hiện (đầu trang, chân trang hoặc thanh bên). |
| **Hiển thị thông tin tỷ giá** | Hiển thị thông báo cho khách hàng rằng giá cả là ước tính từ loại tiền tệ cơ bản của bạn. |
| **Bật định dạng theo khu vực** | Định dạng số và ký hiệu tiền tệ theo khu vực của từng khách hàng (ví dụ: 1.234,56 cho định dạng châu Âu). |

## Chế độ thanh toán

Chọn cách nhiều loại tiền tệ hoạt động tại thời điểm thanh toán:

| Chế độ | Mô tả |
|------|-------------|
| **Full Multi-Currency** | Khách hàng duyệt, thêm vào giỏ hàng và thanh toán bằng loại tiền tệ đã chọn của họ. Tỷ giá sẽ được khóa tại thời điểm thanh toán và ghi lại với đơn hàng. Đây là chế độ mặc định. |
| **Chỉ hiển thị** | Giá cả được hiển thị bằng loại tiền tệ của khách hàng để thuận tiện, nhưng giỏ hàng và thanh toán luôn được xử lý bằng loại tiền tệ cơ bản của bạn. Tại thời điểm thanh toán, khách hàng sẽ thấy một thông báo hiển thị số tiền ước tính chuyển đổi cùng với số tiền thực tế được tính bằng loại tiền tệ cơ bản của bạn. |

**Chỉ hiển thị** hữu ích khi nhà cung cấp thanh toán của bạn chỉ hỗ trợ loại tiền tệ cơ bản, hoặc khi bạn muốn tránh hoàn toàn rủi ro tỷ giá. Khách hàng vẫn có thể thấy giá theo khu vực khi duyệt, giúp họ có cảm giác về chi phí theo loại tiền tệ của họ.

## Khoảng thời gian đồng bộ tỷ giá

Kiểm soát tần suất cửa hàng của bạn lấy tỷ giá mới từ nhà cung cấp đã kết nối:

| Khoảng thời gian | Mô tả |
|----------|-------------|
| **Thực thời** | Mỗi 15 phút. Tốt nhất cho các cửa hàng có lượng bán hàng quốc tế cao. |
| **Theo giờ** | Một lần mỗi giờ. Cân bằng tốt giữa độ mới và việc sử dụng API. |
| **Theo ngày** | Một lần mỗi ngày. Phù hợp với hầu hết các cửa hàng. Đây là chế độ mặc định. |
| **Theo tuần** | Một lần mỗi tuần. Dành cho các cửa hàng có giá ổn định. |
| **Theo tháng / quý** | Cập nhật ít thường xuyên hơn cho các cửa hàng hiếm khi thay đổi tỷ giá. |
| **Chỉ thủ công** | Tỷ giá không bao giờ được lấy tự động. Bạn quản lý tất cả tỷ giá thủ công. |

Khoảng thời gian đồng bộ ảnh hưởng đến tần suất nhiệm vụ nền tảng lấy tỷ giá từ nhà cung cấp của bạn. Giữa các lần đồng bộ, tỷ giá được lưu trữ sẽ được sử dụng. Nếu bạn cần đồng bộ ngay lập tức, hãy sử dụng nút **Sync Now** trên bảng điều khiển tỷ giá hoặc **Sync from Provider** trên trang tỷ giá thủ công.

## Tỷ giá thủ công

Tỷ giá thủ công cho phép bạn thiết lập tỷ giá chuyển đổi chính xác cho các cặp tiền tệ cụ thể. Chúng có quyền ưu tiên cao hơn tỷ giá được lấy từ nhà cung cấp, mang lại cho bạn quyền kiểm soát đầy đủ đối với giá cả.

Truy cập **Exchange Rates > Manual Exchange Rates** để quản lý chúng.

### Thiết lập tỷ giá thủ công

Nhấp vào **Add Rate** để tạo tỷ giá cho một cặp tiền tệ. Chỉ định loại tiền tệ cơ bản, loại tiền tệ mục tiêu và tỷ giá. Ví dụ, thiết lập USD/EUR thành 0,92 có nghĩa là 1 USD = 0,92 EUR.

### Đồng bộ từ nhà cung cấp

Nhấp vào **Sync from Provider** để tự động điền tỷ giá thủ công từ tỷ giá mới nhất của nhà cung cấp đã kết nối.

Điều này tạo ra các tỷ lệ thủ công cho tất cả các loại tiền tệ được hỗ trợ, cung cấp cho bạn điểm bắt đầu để tinh chỉnh thêm.

Các tỷ lệ bị khóa sẽ bị bỏ qua trong quá trình đồng bộ, do đó bất kỳ tỷ lệ nào bạn đã điều chỉnh thủ công sẽ không bị ghi đè.

### Khóa tỷ lệ

Nhấp vào biểu tượng khóa trên bất kỳ tỷ lệ nào để ngăn nó bị ghi đè trong quá trình đồng bộ nhà cung cấp. Điều này rất hữu ích khi bạn đã đàm phán một tỷ lệ cụ thể hoặc muốn duy trì tỷ lệ cố định bất kể biến động thị trường.

- Các tỷ lệ **đã khóa** hiển thị biểu tượng khóa và bị loại khỏi đồng bộ tự động.
- Các tỷ lệ **chưa khóa** có thể được cập nhật khi bạn nhấp vào **Đồng bộ từ nhà cung cấp**.

### So sánh nhà cung cấp

Mỗi tỷ lệ thủ công hiển thị tỷ lệ hiện tại của nhà cung cấp bên cạnh nó, kèm theo phần trăm chênh lệch. Điều này giúp bạn dễ dàng nhìn thấy tỷ lệ thủ công của bạn so với tỷ lệ thị trường:

- Phần trăm **xanh lá** có nghĩa là tỷ lệ của bạn cao hơn tỷ lệ nhà cung cấp.
- Phần trăm **đỏ** có nghĩa là tỷ lệ của bạn thấp hơn tỷ lệ nhà cung cấp.

## Markup tỷ lệ trao đổi

Bạn có thể thêm phần trăm markup vào tỷ lệ trao đổi để bù đắp phí chuyển đổi tiền tệ và bảo vệ khỏi sự biến động tỷ giá giữa lúc khách hàng đặt hàng và khi bạn nhận được thanh toán.

Ví dụ, markup 2% trên tỷ lệ USD/EUR 1.18 sẽ điều chỉnh nó lên khoảng 1.20 USD/EUR. Khoảng chênh lệch nhỏ này giúp đảm bảo bạn không bị lỗ tiền trong các giao dịch chuyển đổi.

## Chiến lược chọn tỷ lệ

Khi bạn có nhiều nhà cung cấp tỷ lệ trao đổi được kết nối, bạn có thể chọn cách tỷ lệ được chọn:

- **Nhà cung cấp chính** - Luôn sử dụng tỷ lệ từ nhà cung cấp chính được chỉ định của bạn. Điều này đảm bảo giá cả nhất quán trên toàn bộ cửa hàng. Nếu nhà cung cấp chính không có dữ liệu cho một cặp tiền tệ, nó sẽ chuyển sang tỷ lệ mới nhất có sẵn từ bất kỳ nhà cung cấp nào.
- **Mới nhất có sẵn** - Sử dụng tỷ lệ mới nhất được đồng bộ từ bất kỳ nhà cung cấp hoạt động nào. Điều này mang lại dữ liệu mới nhất nhưng tỷ lệ có thể thay đổi nhẹ giữa các nhà cung cấp.

Đối với hầu hết các cửa hàng, **Nhà cung cấp chính** là lựa chọn được khuyến nghị vì nó cung cấp giá cả dự đoán nhất.

## Tiền tệ được hỗ trợ

Sử dụng công cụ quản lý kéo thả tiền tệ để chọn các loại tiền tệ mà cửa hàng của bạn hỗ trợ:

1. **Tiền tệ có sẵn** (cột bên trái) hiển thị tất cả các loại tiền tệ bạn có thể kích hoạt.
2. **Tiền tệ đang hoạt động** (cột bên phải) hiển thị các loại tiền tệ hiện đang được kích hoạt trên cửa hàng của bạn.
3. Kéo các loại tiền tệ giữa các cột để kích hoạt hoặc tắt chúng.
4. Kéo bên trong cột đang hoạt động để sắp xếp lại thứ tự hiển thị của các loại tiền tệ trong trình chuyển đổi.
5. Nhấp vào **Lưu cấu hình tiền tệ** để áp dụng các thay đổi của bạn.

Tiền tệ cơ sở của bạn luôn được kích hoạt và không thể xóa.

## Cách giải quyết tỷ lệ trao đổi

Khi một giá cần được chuyển đổi, hệ thống kiểm tra tỷ lệ theo thứ tự sau:

1. **Tỷ lệ trao đổi thủ công** - Nếu tồn tại tỷ lệ thủ công đang hoạt động cho cặp tiền tệ, nó luôn được sử dụng trước.
2. **Tỷ lệ nhà cung cấp** - Nếu không có tỷ lệ thủ công, tỷ lệ mới nhất từ nhà cung cấp đã kết nối của bạn sẽ được sử dụng.

Điều này có nghĩa là bạn có thể sử dụng nhà cung cấp cho hầu hết các loại tiền tệ và ghi đè các cặp cụ thể bằng tỷ lệ thủ công khi bạn cần kiểm soát chính xác.

## Lưu ý quan trọng: Cài đặt này là vĩnh viễn

Khi chức năng đa tiền tệ được kích hoạt và khách hàng đặt hàng bằng tiền tệ nước ngoài, cài đặt này **không thể bị tắt**. Lý do là:

- Các đơn hàng lưu trữ vĩnh viễn tiền tệ được khách hàng chọn và tỷ lệ trao đổi được sử dụng tại thời điểm mua hàng.
- Báo cáo tài chính và tính toán hoàn tiền phụ thuộc vào dữ liệu tiền tệ lịch sử này.
- Tắt chức năng đa tiền tệ sẽ để lại các đơn hàng đa tiền tệ hiện có ở trạng thái không nhất quán.

Nếu chưa có đơn hàng nào được đặt bằng tiền tệ nước ngoài, bạn vẫn có thể tắt chức năng đa tiền tệ.

## Một số mẹo

Bảo tồn toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- **Thử nghiệm với đơn hàng nhỏ trước** - Đặt một đơn hàng kiểm tra bằng ngoại tệ để kiểm tra quy trình thanh toán và đảm bảo tỷ giá được áp dụng chính xác.
- **Theo dõi tỷ giá hối đoái thường xuyên** - Kiểm tra bảng điều khiển Tỷ giá hối đoái định kỳ để đảm bảo nhà cung cấp của bạn đang đồng bộ tỷ giá và chúng trông hợp lý.
- **Xem xét markup cho các loại tiền tệ biến động** - Nếu bạn hỗ trợ các loại tiền tệ có độ biến động cao, markup cao hơn một chút (2-3%) có thể bảo vệ lợi nhuận của bạn.
- **Bắt đầu với các loại tiền tệ chính** - Bắt đầu với các loại tiền tệ phổ biến (EUR, GBP, JPY, CAD, AUD) và mở rộng dựa trên nhu cầu của khách hàng.
- **Kiểm tra tính tương thích với nhà cung cấp thanh toán** - Không phải tất cả nhà cung cấp thanh toán đều hỗ trợ tất cả các loại tiền tệ.

Kiểm tra tài liệu của nhà cung cấp thanh toán của bạn để xác nhận các loại tiền tệ mà họ xử lý.
- **Sử dụng chế độ Hiển thị Chỉ đọc nếu không chắc chắn** - Nếu bạn không chắc nhà cung cấp thanh toán của mình có hỗ trợ thanh toán đa tiền tệ hay không, hãy bắt đầu với chế độ Hiển thị Chỉ đọc.

Bạn có thể chuyển sang Chế độ Đa tiền tệ đầy đủ sau này.
- **Khóa tỷ giá trước các giai đoạn khuyến mãi** - Nếu bạn đang chạy một chương trình khuyến mãi, hãy khóa tỷ giá hối đoái của bạn trước để đảm bảo giá cả nhất quán trong suốt chiến dịch.