---
title: Kết hợp khuyến mãi
---

Nền tảng cung cấp bốn loại khuyến mãi có thể hoạt động cùng nhau: giảm giá sản phẩm, khuyến mãi, mã phiếu mua hàng và thẻ quà tặng. Hiểu cách chúng tương tác giúp bạn chạy chiến dịch hiệu quả mà không có kết quả bất ngờ hoặc giảm giá kép không mong muốn.

> **Thẻ quà tặng hiện chưa thể áp dụng tại thanh toán trực tuyến.** Thiết kế được mô tả dưới đây — áp dụng thẻ quà tặng cuối cùng, sau tất cả các khuyến mãi khác — là cách nó sẽ hoạt động khi tính năng được triển khai. Hiện tại, một thẻ quà tặng chỉ có thể được sử dụng tại **Quầy thanh toán**, vì vậy các tương tác được mô tả cho cửa hàng trực tuyến hiện chưa áp dụng cụ thể cho thẻ quà tặng. Xem chủ đề **Thẻ quà tặng** để biết trạng thái hiện tại.

## Bốn lớp khuyến mãi

Mỗi loại khuyến mãi hoạt động ở cấp độ khác nhau và được khách hàng nhìn thấy theo những cách khác nhau.

| Lớp | Nơi thiết lập | Cách áp dụng | Khách hàng có thể nhìn thấy |
|-----|-------------|-------------|--------------------------|
| **Giảm giá sản phẩm** | Biểu mẫu chỉnh sửa sản phẩm > Phần Giảm giá | Tự động thay đổi giá hiển thị | Có — hiển thị dưới dạng giá gốc bị gạch bỏ |
| **Khuyến mãi** | Marketing > Bán hàng và Khuyến mãi | Tự động áp dụng cho các sản phẩm phù hợp | Có — hiển thị dưới dạng giá khuyến mãi trên các thẻ sản phẩm |
| **Mã phiếu mua hàng** | Marketing > Phiếu mua hàng | Khách hàng nhập mã tại thanh toán | Chỉ tại thanh toán sau khi nhập mã |
| **Thẻ quà tặng** | Được sử dụng đối với số dư thẻ quà tặng | Giảm tổng số tiền thanh toán | Chỉ tại Quầy thanh toán cho đến nay (xem chú thích trên) |

## Cách thức ưu tiên hoạt động

Khuyến mãi có trường **Ưu tiên** chấp nhận các giá trị từ 0 trở lên. Số càng cao thì mức độ ưu tiên càng cao.

Khi nhiều khuyến mãi phù hợp với cùng một sản phẩm, khuyến mãi có **ưu tiên cao nhất sẽ thắng**. Chúng không chồng chéo — chỉ có một khuyến mãi áp dụng cho mỗi sản phẩm.

**Ví dụ:** "Khuyến mãi flash giảm 50%" (ưu tiên 10) và "Khuyến mãi mùa hè giảm 20%" (ưu tiên 5) đều nhắm đến tất cả sản phẩm. Khách hàng nhìn thấy giá khuyến mãi flash 50%, không phải 70% kết hợp.

Trong cùng một cấp độ ưu tiên, hệ thống chọn khuyến mãi mang lại mức giảm lớn nhất cho khách hàng.

## Quy tắc chồng chéo

Bảng dưới đây cho thấy các tổ hợp khuyến mãi được phép và cách kiểm soát chúng.

| Tổ hợp | Được phép? | Cách kiểm soát |
|--------|-----------|----------------|
| Giảm giá sản phẩm + Khuyến mãi | Chỉ nếu được bật | Kiểm tra **"Kết hợp với giảm giá sản phẩm"** trong Cài đặt nâng cao của khuyến mãi |
| Khuyến mãi + Khuyến mãi | Không — khuyến mãi có ưu tiên cao nhất sẽ thắng | Thiết lập giá trị ưu tiên để kiểm soát khuyến mãi nào được áp dụng |
| Khuyến mãi + Mã phiếu mua hàng | Có | Khuyến mãi giảm giá sản phẩm, mã phiếu mua hàng giảm tổng giỏ hàng riêng biệt |
| Mã phiếu + Mã phiếu | Có thể cấu hình | Cờ **"Không thể kết hợp với các mã phiếu khác"** của mã phiếu kiểm soát điều này (mặc định được bật) |
| Mã phiếu + Sản phẩm giảm giá | Có thể cấu hình | Cờ **"Loại bỏ sản phẩm giảm giá"** của mã phiếu kiểm soát điều này |
| Thẻ quà tặng + Bất kỳ khuyến mãi nào | Có — luôn được phép | Thẻ quà tặng được áp dụng cuối cùng, giảm tổng số tiền thanh toán sau tất cả các khuyến mãi khác. Hiện tại chỉ có thể thực hiện tại Quầy thanh toán — xem chú thích trên |

## Các tình huống phổ biến

### Tình huống A: Khuyến mãi toàn trang web + mã phiếu mua hàng

- **Thiết lập:** Giảm 20% cho tất cả sản phẩm (khuyến mãi) + khách hàng có mã phiếu mua hàng 10 USD
- **Kết quả:** Một sản phẩm 100 USD trở thành 80 USD (khuyến mãi), sau đó mã phiếu mua hàng 10 USD được áp dụng cho tổng giỏ hàng. Khách hàng thanh toán **70 USD**.

### Tình huống B: Sản phẩm đang giảm giá + khuyến mãi toàn trang web

- **Thiết lập:** Sản phẩm có giảm giá 30% theo cấp độ sản phẩm + khuyến mãi toàn trang web 20% tồn tại
- **Kết quả (không bật chồng chéo):** Chỉ áp dụng giảm giá sản phẩm. Khách hàng thanh toán **70 USD**.
- **Kết quả (bật chồng chéo):** Cả hai đều áp dụng. Giảm 30% trước = 70 USD, sau đó giảm 20% = **56 USD**.

### Tình huống C: Hai khuyến mãi cùng một sản phẩm

- **Thiết lập:** "Khuyến mãi flash giảm 40%" (ưu tiên 10) + "Khuyến mãi mùa hè giảm 20%" (ưu tiên 5), cả hai nhắm đến tất cả sản phẩm
- **Kết quả:** Khuyến mãi flash thắng vì có ưu tiên cao hơn. Khách hàng thanh toán **60 USD** cho một sản phẩm 100 USD.

### Tình huống D: Mã phiếu mua hàng cho sản phẩm đang giảm giá

- **Thiết lập:** Sản phẩm đang được giảm giá 25%.

Khách hàng nhập mã phiếu giảm giá 10% có tùy chọn "Loại trừ sản phẩm khuyến mãi" được bật.
- **Kết quả:** Phiếu giảm giá không áp dụng cho sản phẩm đó.

Nếu giỏ hàng có các sản phẩm không phải là sản phẩm khuyến mãi, phiếu giảm giá chỉ áp dụng cho những sản phẩm đó.

## Loại Giảm Giá Nào Nên Sử Dụng

| Mục tiêu | Phương pháp được khuyến nghị | Lý do |
|---------|--------------------------|------|
| Xử lý hàng tồn kho theo mùa | **Khuyến mãi** (mục tiêu theo danh mục hoặc bộ sưu tập) | Tự động, không cần hành động của khách hàng, hiển thị trên các thẻ sản phẩm |
| Thưởng cho khách hàng cụ thể | **Mã phiếu giảm giá** (sử dụng một lần, giới hạn theo khách hàng) | Nhắm mục tiêu, có thể theo dõi, cảm giác cá nhân |
| Giao dịch nhanh cho một sản phẩm | **Khuyến mãi sản phẩm** (trên biểu mẫu chỉnh sửa sản phẩm) | Nhanh nhất để thiết lập, không cần hướng dẫn thiết lập khuyến mãi |
| Tiền thưởng hoặc quà tặng | **Thẻ quà tặng** | Dựa trên số dư; hiện tại chỉ có thể sử dụng tại quầy thanh toán |
| Sự kiện toàn trang web | **Khuyến mãi** (mục tiêu tất cả sản phẩm) | Phạm vi lớn nhất, một lần thiết lập bao phủ tất cả |
| Chiến dịch thu hút khách hàng quay lại | **Mã phiếu giảm giá** (hạn chế khách hàng mới hoặc khách hàng quay lại) | Có thể nhắm mục tiêu các nhóm khách hàng cụ thể |

## Mẹo

- **Thử nghiệm với một giỏ hàng thực tế** — sau khi thiết lập khuyến mãi và mã phiếu giảm giá, thêm sản phẩm vào giỏ hàng và đi qua quy trình thanh toán để kiểm tra xem các ưu đãi có áp dụng như mong đợi không.
- **Kiểm tra số lượng sản phẩm bị ảnh hưởng** — trong bước xem xét khuyến mãi, xác nhận số lượng sản phẩm bị ảnh hưởng khớp với mục tiêu của bạn.
- **Sử dụng độ ưu tiên một cách có ý thức** — nếu bạn chạy nhiều khuyến mãi cùng lúc, luôn đặt các giá trị độ ưu tiên khác nhau để bạn kiểm soát khuyến mãi nào sẽ được áp dụng.
- **Giữ chế độ chồng chéo tắt mặc định** — chỉ bật "Chồng chéo với khuyến mãi sản phẩm" khi bạn đặc biệt muốn có hai mức giảm giá.
- **Ghi lại chiến lược của bạn** — sử dụng trường Mô tả của khuyến mãi để ghi chú lý do khuyến mãi tồn tại và cách nó liên quan đến các khuyến mãi đang hoạt động khác.