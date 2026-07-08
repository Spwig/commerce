---
title: Quy tắc định giá hấp dẫn
---

Định giá hấp dẫn (còn gọi là định giá tâm lý) tự động điều chỉnh giá sản phẩm của bạn để kết thúc bằng các chữ số cụ thể mà khách hàng cảm thấy hấp dẫn hơn. Ví dụ, thay vì hiển thị giá $20.00, định giá hấp dẫn có thể hiển thị $19.99 — một kỹ thuật được sử dụng rộng rãi giúp giá trông thấp hơn khi nhìn thoáng qua.

Spwig áp dụng quy tắc định giá hấp dẫn tự động trên toàn bộ cửa hàng của bạn, theo từng loại tiền tệ, vì vậy bạn chỉ cần thiết lập mỗi quy tắc một lần.

## Cách định giá hấp dẫn hoạt động

Khi giá sản phẩm được tính toán (bao gồm cả sau khi áp dụng khuyến mãi hoặc giảm giá), Spwig sẽ kiểm tra xem có quy tắc định giá hấp dẫn nào đang hoạt động cho loại tiền tệ đó hay không. Nếu có, giá sẽ được điều chỉnh trước khi hiển thị cho khách hàng. Việc điều chỉnh này áp dụng cho các giá cao hơn ngưỡng tối thiểu mà bạn chọn.

Bạn có thể cấu hình các quy tắc riêng biệt cho từng loại tiền tệ mà cửa hàng của bạn chấp nhận. Ví dụ, bạn có thể sử dụng kết thúc bằng `.99` cho USD nhưng làm tròn đến `¥10` cho JPY.

## Tạo quy tắc định giá hấp dẫn

1. Di chuyển đến **Catalog > Price Charming Rules**
2. Nhấp **+ Add Price Charming Rule**
3. Chọn **Currency** mà quy tắc này áp dụng (ví dụ: `USD`, `EUR`, `NZD`)
4. Chọn **Rule Type** (xem bảng dưới đây)
5. Tùy chọn thiết lập **Minimum Price Threshold** để loại bỏ các giá rất thấp
6. Chọn **Apply to Sale Prices** nếu bạn cũng muốn áp dụng định giá hấp dẫn khi sản phẩm đang được bán giảm giá
7. Đảm bảo **Active** được chọn
8. Nhấp **Save**

Chỉ có thể tồn tại một quy tắc cho mỗi loại tiền tệ. Nếu bạn cần thay đổi quy tắc, hãy chỉnh sửa quy tắc hiện có.

## Loại quy tắc

| Loại Quy tắc | Ví dụ | Phù hợp nhất |
|---------------|--------|---------------|
| **Charm .99 ending** | $20.50 → $19.99 | Hầu hết các sản phẩm bán lẻ — giá tâm lý cổ điển |
| **Charm .95 ending** | $20.50 → $19.95 | Một lựa chọn nhẹ nhàng hơn một chút so với .99 |
| **Charm .90 ending** | $20.50 → $19.90 | Làm tròn nhưng vẫn dưới một đô la |
| **Round Down** | $19.50 → $19.00 | Các cửa hàng ưa thích các con số nguyên |
| **Round Up** | $19.50 → $20.00 | Làm tròn nhẹ để hiển thị rõ ràng |
| **Round to nearest 5** | $23.00 → $25.00 | Bán lẻ và thị trường có lưu lượng cao |
| **Round to nearest 10** | $23.00 → $20.00 | Các mặt hàng có giá cao hơn như thiết bị gia dụng |
| **Round to nearest 100** | $1,234 → $1,200 | Các mặt hàng có giá trị cao như nội thất hoặc điện tử |
| **Custom ending** | Bất kỳ — chỉ định bên dưới | Khi thương hiệu của bạn sử dụng một kết thúc cụ thể như `.88` |

### Kết thúc tùy chỉnh

Nếu bạn chọn **Custom ending**, hãy nhập giá trị kết thúc trong trường **Custom Ending**. Ví dụ, nhập `0.88` để làm cho tất cả các giá kết thúc bằng `.88` (thường thấy ở một số thị trường châu Á).

## Ngưỡng giá tối thiểu

Sử dụng trường **Minimum Price Threshold** để bỏ qua định giá hấp dẫn cho các mặt hàng có giá rất thấp, nơi việc điều chỉnh sẽ trông kỳ lạ. Ví dụ, việc thiết lập ngưỡng là `5.00` có nghĩa là các sản phẩm có giá dưới $5 sẽ được hiển thị với giá tính toán thực tế mà không áp dụng định giá hấp dẫn.

Giữ nguyên ở `0` để áp dụng định giá hấp dẫn cho tất cả các giá.

## Giá bán giảm

Mặc định, định giá hấp dẫn được áp dụng cho cả giá bán lẻ và giá bán giảm. Nếu bạn muốn giá bán giảm hiển thị giá trị tính toán chính xác (có ích cho các chương trình khuyến mãi giới hạn thời gian nơi các con số cụ thể quan trọng), hãy bỏ chọn **Apply to Sale Prices**.

## Tạm dừng quy tắc

Để tạm dừng định giá hấp dẫn mà không xóa quy tắc, hãy bỏ chọn **Active** và lưu lại. Quy tắc được bảo lưu và có thể được kích hoạt lại bất kỳ lúc nào.

## Một số mẹo

Bảo tồn toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- Bắt đầu với các giá kết thúc bằng `.99` nếu bạn không chắc — đây là kỹ thuật định giá tâm lý được công nhận rộng rãi nhất và hoạt động tốt với hầu hết các loại sản phẩm.
- Thiết lập ngưỡng tối thiểu nếu bạn bán các mặt hàng có giá thấp (dưới $5) để tránh trường hợp một sản phẩm $3.50 giảm xuống $2.99.
- Kiểm tra giá của bạn sau khi kích hoạt quy tắc mới bằng cách xem sản phẩm trên cửa hàng — giá được định dạng sẽ hiển thị thời gian thực.
- Đồng Yên Nhật Bản và các loại tiền tệ theo số nguyên tương tự hoạt động tốt nhất với **Làm tròn đến 10 gần nhất** hoặc **Làm tròn đến 100 gần nhất**, vì các kết thúc thập phân trông không tự nhiên.
- Việc định dạng giá sẽ được áp dụng sau tất cả các khuyến mãi và chương trình giảm giá, do đó giá bán hàng của bạn cũng sẽ được định dạng trừ khi bạn bỏ chọn **Áp dụng cho Giá bán hàng**.
- Bạn có thể sử dụng các loại quy tắc khác nhau cho các loại tiền tệ khác nhau, điều này rất hữu ích nếu bạn bán hàng cho nhiều thị trường với các quy ước định giá khác nhau.