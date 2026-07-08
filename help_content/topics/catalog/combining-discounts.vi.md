---
title: Kết hợp khuyến mãi
---

Nền tảng cung cấp bốn loại khuyến mãi có thể hoạt động cùng nhau: giảm giá sản phẩm, khuyến mãi, mã phiếu mua hàng và thẻ quà tặng. Hiểu cách chúng tương tác giúp bạn chạy chiến dịch hiệu quả mà không có kết quả bất ngờ hoặc giảm giá kép không mong muốn.

## Bốn lớp khuyến mãi

Mỗi loại khuyến mãi hoạt động ở cấp độ khác nhau và được khách hàng nhìn thấy theo những cách khác nhau.

| Lớp | Nơi thiết lập | Cách áp dụng | Khách hàng có thể nhìn thấy |
|-------|---------------|-----------------|-------------------|
| **Giảm giá sản phẩm** | Biểu mẫu chỉnh sửa sản phẩm > Phần giảm giá | Tự động thay đổi giá hiển thị | Có — hiển thị dưới dạng giá gốc bị gạch bỏ |
| **Khuyến mãi** | Marketing > Khuyến mãi và giảm giá | Tự động áp dụng cho các sản phẩm phù hợp | Có — hiển thị dưới dạng giá khuyến mãi trên các thẻ sản phẩm |
| **Mã phiếu mua hàng** | Marketing > Mã phiếu mua hàng | Khách hàng nhập mã tại thanh toán | Chỉ tại thanh toán sau khi nhập mã |
| **Thẻ quà tặng** | Áp dụng tại thanh toán từ số dư thẻ quà tặng | Giảm tổng số tiền thanh toán | Chỉ tại thanh toán |

## Cách hoạt động của độ ưu tiên

Khuyến mãi có trường **Độ ưu tiên** chấp nhận các giá trị từ 0 trở lên. Số càng lớn thì độ ưu tiên càng cao.

Khi nhiều khuyến mãi cùng áp dụng cho một sản phẩm, khuyến mãi có **độ ưu tiên cao nhất sẽ thắng**. Chúng không chồng chéo — chỉ có một khuyến mãi áp dụng cho mỗi sản phẩm.

**Ví dụ:** "Khuyến mãi flash giảm 50%" (ưu tiên 10) và "Khuyến mãi mùa hè giảm 20%" (ưu tiên 5) đều nhắm đến tất cả sản phẩm. Khách hàng nhìn thấy giá khuyến mãi flash 50%, không phải 70% kết hợp.

Trong cùng một cấp độ ưu tiên, hệ thống chọn khuyến mãi mang lại mức giảm lớn nhất cho khách hàng.

## Quy tắc chồng chéo

Bảng dưới đây cho thấy các tổ hợp khuyến mãi nào được phép và cách kiểm soát chúng.

| Tổ hợp | Được phép? | Cách kiểm soát |
|-------------|----------|-------------------|
| Giảm giá sản phẩm + Khuyến mãi | Chỉ khi được bật | Kiểm tra **"Có thể chồng chéo với giảm giá sản phẩm"** trong Cài đặt nâng cao của khuyến mãi |
| Khuyến mãi + Khuyến mãi | Không — khuyến mãi có độ ưu tiên cao nhất thắng | Thiết lập giá trị độ ưu tiên để kiểm soát khuyến mãi nào được áp dụng |
| Khuyến mãi + Mã phiếu mua hàng | Có | Khuyến mãi giảm giá sản phẩm, mã phiếu mua hàng giảm tổng giỏ hàng riêng biệt |
| Mã phiếu + Mã phiếu | Có thể cấu hình | Cờ **"Không thể kết hợp với các mã phiếu khác"** của mã phiếu kiểm soát điều này (mặc định được bật) |
| Mã phiếu + Sản phẩm giảm giá | Có thể cấu hình | Cờ **"Loại bỏ sản phẩm giảm giá"** của mã phiếu kiểm soát điều này |
| Thẻ quà tặng + Bất kỳ khuyến mãi nào | Có — luôn được phép | Thẻ quà tặng được áp dụng cuối cùng, giảm số tiền thanh toán cuối cùng sau tất cả các khuyến mãi khác |

## Tình huống phổ biến

### Tình huống A: Khuyến mãi toàn trang web + mã phiếu mua hàng

- **Thiết lập:** Giảm 20% cho tất cả sản phẩm (khuyến mãi) + khách hàng có mã phiếu mua hàng 10 đô la
- **Kết quả:** Một sản phẩm 100 đô la trở thành 80 đô la (khuyến mãi), sau đó mã phiếu mua hàng 10 đô la áp dụng cho tổng giỏ hàng. Khách hàng thanh toán **70 đô la**.

### Tình huống B: Sản phẩm đang giảm giá + khuyến mãi toàn trang web

- **Thiết lập:** Sản phẩm có chương trình giảm giá 30% cấp sản phẩm + khuyến mãi toàn trang web 20% tồn tại
- **Kết quả (không chồng chéo):** Chỉ chương trình giảm giá sản phẩm được áp dụng. Khách hàng thanh toán **70 đô la**.
- **Kết quả (cho phép chồng chéo):** Cả hai đều được áp dụng. Giảm 30% trước = 70 đô la, sau đó giảm 20% = **56 đô la**.

### Tình huống C: Hai khuyến mãi cùng áp dụng cho một sản phẩm

- **Thiết lập:** "Khuyến mãi flash giảm 40%" (ưu tiên 10) + "Khuyến mãi mùa hè giảm 20%" (ưu tiên 5), cả hai nhắm đến tất cả sản phẩm
- **Kết quả:** Khuyến mãi flash thắng vì có độ ưu tiên cao hơn. Khách hàng thanh toán **60 đô la** cho sản phẩm 100 đô la.

### Tình huống D: Mã phiếu mua hàng áp dụng cho sản phẩm đang giảm giá

- **Thiết lập:** Sản phẩm đang được giảm giá 25%. Khách hàng nhập mã phiếu mua hàng 10% có tùy chọn "Loại bỏ sản phẩm giảm giá" được bật.
- **Kết quả:** Mã phiếu mua hàng không áp dụng cho sản phẩm này. Nếu giỏ hàng có các sản phẩm không giảm giá, mã phiếu mua hàng chỉ áp dụng cho những sản phẩm đó.

## Loại khuyến mãi nào nên sử dụng

| Mục tiêu | Phương pháp được đề xuất | Lý do |
|------|---------------------|-----|
| Xử lý hàng tồn kho theo mùa | **Khuyến mãi** (nhắm đến danh mục hoặc bộ sưu tập) | Tự động, không cần hành động của khách hàng, hiển thị trên thẻ sản phẩm |
| Thưởng cho khách hàng cụ thể | **Mã phiếu mua hàng** (sử dụng một lần, giới hạn theo khách hàng) | Nhắm mục tiêu, có thể theo dõi, cảm giác cá nhân hóa |
| Giao dịch nhanh cho một sản phẩm | **Giảm giá sản phẩm** (trên biểu mẫu chỉnh sửa sản phẩm) | Nhanh nhất để thiết lập, không cần hướng dẫn khuyến mãi |
| Tín dụng cửa hàng hoặc quà tặng | **Thẻ quà tặng** | Dựa trên số dư, khách hàng tự quản lý tín dụng của họ |
| Sự kiện toàn trang web | **Khuyến mãi** (nhắm đến tất cả sản phẩm) | Phạm vi lớn nhất, một lần thiết lập bao phủ tất cả |
| Chiến dịch thu hút khách hàng quay lại | **Mã phiếu mua hàng** (hạn chế cho khách hàng mới hoặc quay lại) | Có thể nhắm mục tiêu các nhóm khách hàng cụ thể |

## Một số mẹo

- **Thử nghiệm với một giỏ hàng thực tế** — sau khi thiết lập khuyến mãi và mã phiếu mua hàng, thêm sản phẩm vào giỏ hàng và đi qua quy trình thanh toán để kiểm tra các khuyến mãi có được áp dụng như mong đợi không.
- **Kiểm tra số lượng sản phẩm bị ảnh hưởng** — trong bước xem xét khuyến mãi, xác nhận số lượng sản phẩm bị ảnh hưởng khớp với mục tiêu của bạn.
- **Sử dụng độ ưu tiên một cách có ý thức** — nếu bạn chạy nhiều khuyến mãi cùng lúc, luôn thiết lập các giá trị độ ưu tiên khác nhau để bạn kiểm soát khuyến mãi nào thắng.
- **Giữ chế độ chồng chéo tắt mặc định** — chỉ bật "Có thể chồng chéo với giảm giá sản phẩm" khi bạn đặc biệt muốn có giảm giá kép.
- **Ghi lại chiến lược của bạn** — sử dụng trường Mô tả khuyến mãi để ghi chú lý do khuyến mãi tồn tại và cách nó liên quan đến các khuyến mãi đang hoạt động khác.