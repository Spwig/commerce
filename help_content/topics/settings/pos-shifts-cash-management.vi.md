---
title: Ca làm việc POS và Quản lý Tiền mặt
---

Ca làm việc POS theo dõi các khoảng thời gian làm việc của nhân viên thu ngân và đảm bảo tính chính xác trong kế toán tiền mặt. Mỗi ca làm việc đại diện cho thời gian của một nhân viên thu ngân trên một máy POS—từ việc mở ngăn kéo tiền với số tiền ban đầu đến việc đóng ca với số tiền cuối cùng và đối chiếu. Hệ thống tự động tính toán số tiền dự kiến dựa trên doanh thu tiền mặt thực tế và so sánh với số tiền vật lý, làm nổi bật các sai lệch để điều tra. Các khoản chuyển động tiền mặt trong ca làm việc (thêm tiền lẻ, rút tiền mặt nhỏ) được theo dõi với lý do để có hồ sơ kiểm toán đầy đủ.

Truy cập **POS > Ca làm việc** để xem tất cả các ca làm việc, giám sát các ca đang hoạt động, xem báo cáo đối chiếu tiền mặt và kiểm toán hoạt động lịch sử.

![Danh sách ca làm việc](/static/core/admin/img/help/pos-shifts-cash-management/shift-list.webp)

## Hiểu về Ca làm việc POS

Một ca làm việc là khoảng thời gian làm việc mà trong đó một nhân viên thu ngân vận hành một máy POS. Các ca làm việc đảm bảo tính trách nhiệm về tiền mặt—mỗi nhân viên thu ngân chịu trách nhiệm về số tiền trong ngăn kéo của họ trong ca làm việc của họ.

**Chu kỳ sống của ca làm việc**:
1. **Mở ca** - Nhân viên thu ngân bắt đầu ca, đếm tiền mặt ban đầu, ghi lại số tiền
2. **Trong ca** - Xử lý các giao dịch bán hàng, chấp nhận thanh toán, cấp lại tiền hoàn tiền
3. **Đóng ca** - Nhân viên thu ngân đếm tiền mặt, ghi lại số tiền đóng ca, hệ thống tính toán sai lệch
4. **Đối chiếu** - Ca làm việc được hoàn tất và khóa để kiểm toán

**Các chỉ số chính được theo dõi**:
- **Tiền mặt ban đầu** - Số tiền ban đầu trong ngăn kéo khi bắt đầu ca
- **Tiền mặt đóng ca** - Số tiền vật lý trong ngăn kéo khi kết thúc ca
- **Tiền mặt dự kiến** - Tính toán: Tiền mặt ban đầu + doanh thu tiền mặt - hoàn tiền tiền mặt + chuyển động tiền mặt
- **Sai lệch tiền mặt** - Sai lệch: Tiền mặt đóng ca - tiền mặt dự kiến (dương = dư, âm = thiếu)
- **Tổng doanh thu** - Tổng tất cả các giao dịch bán hàng trong ca
- **Tổng hoàn tiền** - Tổng tất cả các giao dịch hoàn tiền trong ca
- **Số lượng giao dịch** - Số lượng đơn hàng được xử lý

## Trang danh sách ca làm việc

Danh sách ca làm việc hiển thị tất cả các ca làm việc với thông tin chính:

**Trạng thái ca làm việc**:
- **Mở** (biểu ngữ màu xanh lá) - Ca làm việc đang hoạt động
- **Đã đóng** (biểu ngữ màu xám) - Ca làm việc đã hoàn thành
- **Đã đối chiếu** (biểu ngữ màu xanh dương) - Hoàn tất và khóa để kiểm toán

**Máy POS** - Máy POS nào ca làm việc được thực hiện

**Nhân viên thu ngân** - Nhân viên đã làm ca

**Tiền mặt ban đầu** - Số tiền ban đầu

**Tiền mặt đóng ca** - Số tiền kết thúc (trống nếu ca vẫn đang mở)

**Tiền mặt dự kiến** - Số tiền được tính toán dựa trên các giao dịch

**Sai lệch tiền mặt** - Sai lệch (được đánh dấu đỏ nếu âm, xanh nếu dương, đen nếu bằng 0)

**Thời gian** - Độ dài ca làm việc (từ thời gian bắt đầu đến thời gian kết thúc)

**Tổng doanh thu** - Doanh thu tạo ra trong ca

Sử dụng bộ lọc để xem:
- Chỉ các ca đang mở (giám sát các máy POS đang hoạt động)
- Các ca có sai lệch (sai lệch tiền mặt ≠ 0)
- Các ca theo khoảng thời gian (báo cáo đối chiếu hàng ngày)
- Các ca theo nhân viên thu ngân (kiểm toán hiệu suất)

## Mở ca làm việc

Nhân viên thu ngân mở ca làm việc trực tiếp từ máy POS (không thể mở từ trang quản trị). Quy trình trên máy:

1. **Nhân viên đăng nhập** - Nhập thông tin xác thực để truy cập máy

2. **Đếm tiền mặt ban đầu** - Đếm vật lý tất cả tiền trong ngăn kéo (giấy bạc và xu)

3. **Nhập số tiền ban đầu** - Ghi lại số tiền đã đếm trong ứng dụng POS

4. **Ca làm việc bắt đầu** - Máy sẵn sàng để xử lý các giao dịch bán hàng

**Hướng dẫn tiền mặt ban đầu**:
- Tiền mặt ban đầu (tiền lẻ) thường là $100-$300 tùy theo quy mô cửa hàng
- Đếm hai lần để đảm bảo tính chính xác—sai sót khi mở sẽ lan truyền thành sai lệch khi đóng
- Nếu ngăn kéo trống, tiền mặt ban đầu là $0.00 (tiền lẻ được thêm vào thông qua chuyển động tiền mặt)
- Ghi lại các tờ tiền lớn (>$50) riêng để theo dõi chuyển động của chúng

![Biểu mẫu thêm ca làm việc](/static/core/admin/img/help/pos-shifts-cash-management/shift-add-form.webp)

## Trong ca làm việc

Khi ca làm việc đang mở, hệ thống tự động theo dõi:

**Bán hàng bằng tiền mặt** - Bất kỳ giao dịch nào mà khách hàng thanh toán bằng tiền mặt (thêm vào tiền mặt dự kiến)

**Hoàn tiền bằng tiền mặt** - Bất kỳ hoàn tiền nào được phát hành bằng tiền mặt (trừ đi từ tiền mặt dự kiến)

**Bán hàng bằng thẻ** - Giao dịch thẻ tín dụng/thẻ ghi nợ (không ảnh hưởng đến tiền mặt)

**Chia sẻ thanh toán** - Một phần tiền mặt + một phần thẻ (chỉ phần tiền mặt ảnh hưởng đến tiền mặt dự kiến)

**Thẻ quà tặng & Voucher** - Các phương thức thanh toán không dùng tiền mặt (không ảnh hưởng đến tiền mặt)

Nhân viên thu ngân tiếp tục xử lý các giao dịch bình thường. Hệ thống duy trì một tính toán liên tục về tiền mặt dự kiến phía sau hậu trường.

## Chuyển động tiền mặt

Chuyển động tiền mặt là các điều chỉnh trong ngăn kéo tiền trong ca làm việc:

**Thêm tiền lẻ** - Thêm tiền vào ngăn kéo:
- Lý do: "Thêm tiền lẻ để đổi tờ tiền lớn"
- Số tiền: +$100.00
- Tiền mặt dự kiến tăng lên $100.00

**Rút tiền mặt nhỏ** - Loại bỏ tiền mặt cho các khoản chi phí:
- Lý do: "Mua văn phòng phẩm"
- Số tiền: -$25.00
- Tiền mặt dự kiến giảm đi $25.00

**Giao nộp tiền mặt** - Loại bỏ tiền mặt dư thừa để đảm bảo an toàn:
- Lý do: "Giao nộp an toàn - hơn $500 trong ngăn kéo"
- Số tiền: -$300.00
- Tiền mặt dự kiến giảm đi $300.00

**Ghi lại chuyển động tiền mặt trên máy**:
1. Nhấn **Menu** > **Chuyển động tiền mặt**
2. Chọn loại: Thêm hoặc Loại bỏ
3. Nhập số tiền
4. Nhập lý do (yêu cầu cho hồ sơ kiểm toán)
5. Xác nhận

Tất cả chuyển động tiền mặt sẽ xuất hiện trong báo cáo chi tiết ca làm việc với thời gian, số tiền và lý do.

## Đóng ca làm việc

Khi nhân viên thu ngân hoàn thành khoảng thời gian làm việc của họ, họ đóng ca làm việc:

1. **Nhấn Đóng ca** - Trên menu máy

2. **Xử lý các giao dịch còn lại** - Hoàn thành các giỏ hàng đã tạm dừng hoặc các giao dịch đang chờ

3. **Đếm tiền mặt đóng ca** - Đếm vật lý tất cả tiền trong ngăn kéo
   - Đếm tiền giấy theo mệnh giá ($100s, $50s, $20s, $10s, $5s, $1s)
   - Đếm xu theo loại (quarter, dime, nickel, penny)
   - Tổng = số tiền đóng ca

4. **Nhập số tiền đóng ca** - Ghi lại tổng số tiền đã đếm

5. **Hệ thống tính toán sai lệch**:
   - Tiền mặt dự kiến = Tiền mặt ban đầu + doanh thu tiền mặt - hoàn tiền tiền mặt + chuyển động tiền mặt
   - Sai lệch tiền mặt = Tiền mặt đóng ca - tiền mặt dự kiến
   - Ví dụ: Tiền mặt đóng $485.00 - Dự kiến $480.00 = +$5.00 dư

6. **Xem xét sai lệch** - Máy hiển thị sự khác biệt:
   - **Chính xác ($0.00)** - Đối chiếu hoàn hảo
   - **Dư nhỏ (+$1 đến +$5)** - Chấp nhận làm tròn hoặc tiền tip khách hàng
   - **Thiếu nhỏ (-$1 đến -$5)** - Lỗi đếm nhỏ, chấp nhận được
   - **Sai lệch lớn (>$5)** - Yêu cầu đếm lại

7. **Đếm lại nếu cần** - Nếu sai lệch lớn (>$10), nhân viên thu ngân nên đếm lại tiền mặt trước khi hoàn tất

8. **Hoàn tất ca làm việc** - Xác nhận số tiền đóng ca, trạng thái ca làm việc thay đổi thành "Đã đóng"

9. **In báo cáo ca làm việc** - Máy in biên lai đối chiếu tiền mặt cho hồ sơ của nhân viên thu ngân

![Chi tiết ca làm việc](/static/core/admin/img/help/pos-shifts-cash-management/shift-detail.webp)

## Công thức đối chiếu tiền mặt

Hệ thống tính toán tiền mặt dự kiến bằng công thức này:

```
Tiền mặt dự kiến = Tiền mặt ban đầu
                + Doanh thu tiền mặt
                - Hoàn tiền tiền mặt
                + Thêm tiền mặt (chuyển động)
                - Loại bỏ tiền mặt (chuyển động)
```

**Ví dụ**:
- Tiền mặt ban đầu: $200.00
- Doanh thu tiền mặt: $450.00 (từ 15 giao dịch)
- Hoàn tiền tiền mặt: -$30.00 (1 hoàn tiền)
- Thêm tiền mặt: +$100.00 (thêm tiền lẻ giữa ca)
- Loại bỏ tiền mặt: -$50.00 (rút tiền mặt nhỏ)
- **Tiền mặt dự kiến: $200 + $450 - $30 + $100 - $50 = $670.00**

Nếu nhân viên thu ngân đếm $675.00 khi đóng ca:
- Sai lệch tiền mặt: $675.00 - $670.00 = **+$5.00 dư**

## Báo cáo và kiểm toán ca làm việc

Báo cáo ca làm việc cung cấp thông tin đối chiếu chi tiết:

**Phần tổng quát**:
- Tiền mặt ban đầu và đóng ca
- Tính toán tiền mặt dự kiến
- Sai lệch tiền mặt (dư/thiếu)
- Tổng doanh thu và hoàn tiền
- Số lượng giao dịch
- Thời gian ca làm việc

**Chi tiết giao dịch**:
- Tất cả các giao dịch bán hàng trong ca (mã đơn hàng, số tiền, phương thức thanh toán)
- Tất cả các hoàn tiền được phát hành
- Thời gian ghi lại của từng giao dịch

**Lịch sử chuyển động tiền mặt**:
- Tất cả các lần thêm và loại bỏ
- Lý do được cung cấp
- Thời gian ghi lại

**Các trường hợp sử dụng**:
- **Đối chiếu hàng ngày** - Xem xét tất cả các ca làm việc vào cuối ngày kinh doanh
- **Hiệu suất nhân viên thu ngân** - Nhận biết các mô hình sai lệch theo từng nhân viên
- **Phát hiện trộm cắp** - Thiếu hụt lớn và nhất quán có thể chỉ ra trộm cắp
- **Yêu cầu đào tạo** - Những sai lệch nhỏ thường xuyên cho thấy vấn đề về độ chính xác khi đếm
- **Hồ sơ kiểm toán** - Ghi chép đầy đủ cho mục đích kế toán và thuế

## Quản lý tiền mặt cho nhiều máy POS

Đối với các cửa hàng có nhiều máy POS chạy các ca làm việc song song:

**Ngăn kéo riêng biệt**: Mỗi máy POS có riêng một ngăn kéo tiền—các ca làm việc là độc lập. Nhân viên A trên Máy 1 và Nhân viên B trên Máy 2 chạy các ca làm việc riêng biệt với đối chiếu riêng biệt.

**Chia sẻ ngăn kéo**: Một số cửa hàng chia sẻ một ngăn kéo tiền qua nhiều máy POS (không được khuyến khích). Nếu thực hiện điều này:
- Chỉ một ca làm việc có thể mở tại một thời điểm cho mỗi ngăn kéo chia sẻ
- Nhân viên thu ngân phải đóng ca làm việc khi chuyển giao cho nhân viên thu ngân tiếp theo
- Các chuyển động tiền mặt theo dõi tất cả các lần thêm/loại bỏ trong quá trình chuyển giao
- Sai lệch khó xác định cụ thể cho từng nhân viên thu ngân

**Thực hành tốt nhất**: Một ngăn kéo tiền cho mỗi máy POS, một ca làm việc cho mỗi nhân viên thu ngân mỗi phiên. Điều này đảm bảo trách nhiệm rõ ràng và đối chiếu đơn giản.

## Xử lý sai lệch

Khi số tiền đóng ca không khớp với số tiền dự kiến:

**Sai lệch nhỏ (<$5)**:
- Chấp nhận được do làm tròn, lỗi đếm hoặc tiền tip khách hàng
- Ghi chú trong ghi chú ca làm việc
- Không cần hành động thêm trừ khi xu hướng xuất hiện

**Sai lệch trung bình ($5-$20)**:
- Đếm lại tiền mặt trước khi hoàn tất ca làm việc
- Kiểm tra lại nhật ký giao dịch để tìm lỗi (tiền thối sai, giao dịch hủy không được xử lý)
- Ghi chú tình huống trong ghi chú ca làm việc
- Khuyến khích xem xét bởi quản lý

**Sai lệch lớn (>$20)**:
- Đếm lại bắt buộc
- Yêu cầu phê duyệt của quản lý để đóng ca làm việc
- Kiểm tra lại tất cả các giao dịch và chuyển động tiền mặt
- Điều tra các nguyên nhân tiềm năng (trộm cắp, nhấn máy rút tiền, số tiền mở ca sai)
- Có thể yêu cầu hành động kỷ luật tùy theo tình huống

**Thiếu hụt nhất quán**:
- Xu hướng thiếu hụt âm từ cùng một nhân viên thu ngân = vấn đề đào tạo hoặc trộm cắp
- Thực hiện giám sát bổ sung (quản lý kiểm tra ngẫu nhiên trong ca làm việc)
- Kiểm tra lại quy trình đào tạo POS
- Xem xét cập nhật chính sách quản lý tiền mặt

## Một số mẹo

- **Đếm tiền mặt ban đầu hai lần** - Lỗi khi mở sẽ lan truyền thành sai lệch khi đóng; độ chính xác ở đầu ngăn chặn vấn đề ở cuối
- **Ghi lại chuyển động tiền mặt ngay lập tức** - Đừng chờ đến khi đóng ca để ghi lại việc thêm tiền lẻ hoặc rút tiền mặt nhỏ
- **Luôn cung cấp lý do cho chuyển động** - "Thêm $100" không hữu ích cho kiểm toán; "Thêm $100 để đổi tiền (thiếu tờ $5)") là hành động có thể thực hiện được
- **Đếm lại nếu sai lệch >$10** - Đừng hoàn tất ca làm việc với sai lệch lớn mà không đếm lại
- **In báo cáo ca làm việc hàng ngày** - Gắn vào giấy tờ đối chiếu hàng ngày cho kế toán
- **Xem xét xu hướng, không phải từng sai lệch** - Một thiếu hụt -$3.00 là chấp nhận được; năm thiếu hụt -$3.00 liên tiếp là vấn đề
- **Đóng ca làm việc vào cuối ngày** - Đừng để ca làm việc mở qua đêm; sai lệch dễ điều tra hơn khi mới
- **Đào tạo nhân viên thu ngân cách đếm theo mệnh giá** - Hầu hết lỗi đến từ việc đếm sai mệnh giá (nghĩ rằng tờ $5 là $10)
- **Sử dụng túi đựng xu** - Các đồng xu được đóng gói sẵn giúp giảm lỗi đếm và tăng tốc độ đối chiếu

