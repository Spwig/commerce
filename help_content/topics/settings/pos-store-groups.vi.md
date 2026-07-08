---
title: Nhóm Cửa Hàng POS
---

Các nhóm cửa hàng tổ chức nhiều địa điểm bán lẻ với cấu hình chia sẻ. Thay vì cấu hình từng máy POS riêng lẻ, hãy nhóm các máy POS theo khu vực, nhượng quyền hoặc loại địa điểm và áp dụng cài đặt ở cấp độ nhóm. Các nhóm hỗ trợ kế thừa cài đặt - tiền tệ, ngôn ngữ, múi giờ, mẫu biên lai và nội dung khuyến mãi được truyền từ nhóm xuống từng cửa hàng riêng lẻ. Điều này đơn giản hóa việc quản lý cho các nhà bán hàng có nhiều địa điểm trong khi vẫn giữ tính linh hoạt để ghi đè cài đặt cụ thể khi cần.

Sử dụng nhóm cửa hàng khi bạn vận hành nhiều địa điểm bán lẻ, nhượng quyền hoặc thị trường khu vực với các yêu cầu vận hành khác nhau.

![Danh sách nhóm cửa hàng](/static/core/admin/img/help/pos-store-groups/storegroup-list.webp)

## Nhóm cửa hàng là gì?

Các nhóm cửa hàng là các hộp chứa tổ chức cho kho hàng và máy POS chia sẻ các đặc điểm chung:

**Chiến lược nhóm phổ biến**:
- **Địa lý**: Khu vực Bắc, Khu vực Nam, Bờ Tây, Bờ Đông
- **Nhượng quyền**: Cửa hàng của Nhà nhượng quyền A, Cửa hàng của Nhà nhượng quyền B, Cửa hàng của Tổng công ty
- **Định dạng**: Vị trí trong trung tâm thương mại, Cửa hàng độc lập, Cửa hàng kiểu Pop-Up
- **Thị trường**: Cửa hàng nội địa, Cửa hàng châu Âu, Cửa hàng châu Á - Thái Bình Dương

Các nhóm không thay đổi hoạt động vật lý của máy POS - chúng cung cấp một lớp cấu hình giúp đơn giản hóa việc quản lý ở quy mô lớn.

## Khi nào nên sử dụng nhóm cửa hàng

**Một địa điểm** - Không cần nhóm. Cấu hình máy POS trực tiếp.

**2-3 địa điểm với cài đặt giống nhau** - Nhóm có thể không cần thiết. Có thể dễ hơn để cấu hình máy POS trực tiếp.

**4+ địa điểm** - Nhóm được khuyến khích mạnh mẽ. Cấu hình tập trung tiết kiệm thời gian.

**Vận hành đa quốc gia** - Nhóm là cần thiết. Các loại tiền tệ, ngôn ngữ và múi giờ khác nhau yêu cầu ghi đè ở cấp độ nhóm.

**Vận hành nhượng quyền** - Nhóm là rất quan trọng. Mỗi nhà nhượng quyền cần cài đặt độc lập trong khi duy trì tính nhất quán thương hiệu.

## Cấp độ kế thừa cài đặt

POS Spwig sử dụng 4 cấp độ truyền cài đặt (ưu tiên cao nhất đến thấp nhất):

| Cấp độ | Ưu tiên | Ví dụ | Trường hợp sử dụng |
|--------|---------|-------|------------------|
| **Máy POS** | 1 (Cao nhất) | Máy POS 5 ghi đè chiều rộng giấy in thành 58mm | Một máy POS duy nhất có thiết bị in đặc biệt |
| **Cửa hàng** | 2 | Cửa hàng 2 ghi đè tiền tệ thành GBP | Vị trí Anh trong môi trường chủ yếu là cửa hàng Mỹ |
| **Nhóm** | 3 | Nhóm châu Âu đặt múi giờ thành CET | Tính nhất quán khu vực qua nhiều cửa hàng |
| **Trang web** | 4 (Thấp nhất) | Mặc định toàn cầu: USD, Tiếng Anh, UTC | Cài đặt dự phòng cho tất cả các cài đặt chưa được cấu hình |

**Cách hoạt động**:
- Hệ thống kiểm tra cài đặt máy POS trước
- Nếu không được thiết lập, kiểm tra cài đặt cửa hàng
- Nếu không được thiết lập, kiểm tra cài đặt nhóm
- Nếu không được thiết lập, sử dụng cài đặt mặc định của trang web

**Ví dụ**:
- Mặc định trang web: Tiền tệ = USD, Ngôn ngữ = Tiếng Anh
- Nhóm "Cửa hàng châu Âu": Tiền tệ = EUR, Ngôn ngữ = không được thiết lập
- Cửa hàng "Cửa hàng flagship Paris": Tiền tệ = không được thiết lập, Ngôn ngữ = Tiếng Pháp
- Máy POS "Quầy 1 Paris": Tiền tệ = không được thiết lập, Ngôn ngữ = không được thiết lập

**Kết quả cho Quầy 1 Paris**:
- Tiền tệ: EUR (di truyền từ nhóm)
- Ngôn ngữ: Tiếng Pháp (di truyền từ cửa hàng)

Cấp độ này cho phép cài đặt mặc định rộng rãi với các ghi đè chính xác khi cần.

## Tạo nhóm cửa hàng

Truy cập **POS > Nhóm cửa hàng** và nhấn **+ Thêm nhóm cửa hàng**:

![Biểu mẫu thêm nhóm cửa hàng](/static/core/admin/img/help/pos-store-groups/storegroup-add-form.webp)

### Cấu hình cơ bản

**Tên nhóm** - Nhãn mô tả (ví dụ: "Cửa hàng Bờ Tây", "Nhượng quyền châu Âu", "Vị trí trong trung tâm thương mại")

**Mã** - Mã định danh ngắn gọn (ví dụ: "WEST", "EUR", "MALL"):
- Được sử dụng nội bộ để tham chiếu
- Phải duy nhất trong tất cả các nhóm
- 2-10 ký tự, chữ số và chữ cái
- Khuyến khích viết in hoa để đảm bảo tính nhất quán

**Thứ tự sắp xếp** - Điều khiển thứ tự hiển thị trong danh sách quản trị (số nhỏ hơn sẽ hiển thị trước):
- Sử dụng bội số của 10: 10, 20, 30 (cho phép chèn các nhóm mới giữa các nhóm hiện có)
- Giúp tổ chức các nhóm một cách hợp lý (theo thứ tự địa lý, thứ tự kích thước, v.v.)

### Ghi đè khu vực

**Ghi đè tiền tệ** - Thiết lập tiền tệ cấp nhóm khác với mặc định trang web:
- Ví dụ: Nhóm châu Âu sử dụng EUR, nhóm châu Á - Thái Bình Dương sử dụng JPY
- Tất cả máy POS trong nhóm này mặc định sử dụng tiền tệ này
- Ảnh hưởng đến hiển thị giá, đối chiếu tiền mặt, báo cáo

**Ghi đè ngôn ngữ** - Thiết lập ngôn ngữ cấp nhóm khác với mặc định trang web:
- Ví dụ: Cửa hàng tiếng Pháp sử dụng tiếng Pháp, cửa hàng tiếng Đức sử dụng tiếng Đức
- Ảnh hưởng đến ngôn ngữ giao diện POS, ngôn ngữ biên lai (nếu mẫu hỗ trợ)
- Nhân viên sẽ thấy giao diện POS bằng ngôn ngữ này khi đăng nhập vào máy POS thuộc nhóm

**Ghi đè múi giờ** - Thiết lập múi giờ cấp nhóm khác với mặc định trang web:
- Ví dụ: Cửa hàng bờ tây sử dụng America/Los_Angeles, cửa hàng châu Âu sử dụng Europe/Paris
- Ảnh hưởng đến thời gian ca, lịch trình báo cáo, lịch trình trượt quảng cáo
- Đảm bảo báo cáo ca phù hợp với giờ làm việc địa phương

**Khi nào nên ghi đè**:
- **Tiền tệ**: Luôn ghi đè cho các vị trí quốc tế (tiền tệ thanh toán khác nhau)
- **Ngôn ngữ**: Ghi đè cho các thị trường không nói tiếng Anh (nội dung hướng đến khách hàng)
- **Múi giờ**: Ghi đè cho các vị trí hơn 2 giờ so với mặc định trang web (thời gian địa phương chính xác)

## Liên kết kho hàng với nhóm

Sau khi tạo nhóm, hãy gán kho hàng cho nó:

1. Truy cập **Bảng điều khiển > Kho hàng**
2. Chỉnh sửa kho hàng đại diện cho một vị trí cửa hàng
3. Thiết lập trường **Nhóm cửa hàng** thành nhóm bạn đã tạo
4. Lưu lại

Tất cả máy POS được gán với kho hàng này giờ đây sẽ kế thừa cài đặt của nhóm.

**Ví dụ thiết lập**:
- Tạo nhóm: "Cửa hàng châu Âu" (Tiền tệ: EUR, Ngôn ngữ: không được thiết lập, Múi giờ: CET)
- Tạo kho hàng: "Cửa hàng Paris", "Cửa hàng Berlin", "Cửa hàng Rome"
- Gán tất cả 3 kho hàng vào nhóm "Cửa hàng châu Âu"
- Tạo máy POS: "Quầy 1 Paris", "Quầy 1 Berlin", "Quầy 1 Rome"
- Mỗi máy POS kế thừa tiền tệ EUR và múi giờ CET từ nhóm
- Ghi đè ngôn ngữ ở cấp cửa hàng: Paris=Tiếng Pháp, Berlin=Tiếng Đức, Rome=Tiếng Ý

## Cài đặt được kiểm soát bởi nhóm

Các nhóm có thể ghi đè các cài đặt sau:

**Cài đặt vận hành**:
- Tiền tệ (ảnh hưởng đến hiển thị giá và đối chiếu tiền mặt)
- Ngôn ngữ (ảnh hưởng đến ngôn ngữ giao diện POS)
- Múi giờ (ảnh hưởng đến thời gian và lịch trình)

**Cài đặt nội dung** (qua các mô hình có phạm vi):
- Mẫu biên lai (tạo thiết kế biên lai cụ thể cho nhóm)
- Trượt quảng cáo (nhắm quảng cáo đến các nhóm cụ thể)

**Không được kiểm soát bởi nhóm**:
- Cấu hình phần cứng máy POS (được cấu hình theo từng máy POS)
- Phân công nhân viên (được cấu hình theo từng máy POS)
- Mức tồn kho kho hàng (được cấu hình theo từng kho hàng)
- Tài khoản nhà cung cấp thanh toán (được cấu hình toàn trang web hoặc theo từng nhà cung cấp)

## Ví dụ thực tế

### Ví dụ 1: Nhà bán lẻ thời trang quốc tế

**Thiết lập**:
- 50 cửa hàng ở 5 quốc gia
- Mỗi quốc gia có tiền tệ, ngôn ngữ và yêu cầu thuế khác nhau

**Cấu trúc nhóm**:
- Nhóm: "Cửa hàng Mỹ" (USD, Tiếng Anh, America/New_York)
  - 20 kho hàng (New York, Los Angeles, Chicago, v.v.)
  - 60 máy POS
- Nhóm: "Cửa hàng Anh" (GBP, Tiếng Anh, Europe/London)
  - 10 kho hàng (London, Manchester, v.v.)
  - 30 máy POS
- Nhóm: "Cửa hàng EU" (EUR, không được thiết lập, Europe/Paris)
  - 15 kho hàng (Paris, Berlin, Rome, v.v.)
  - 45 máy POS
  - Ghi đè ngôn ngữ ở cấp cửa hàng (Paris=Tiếng Pháp, Berlin=Tiếng Đức, Rome=Tiếng Ý)
- Nhóm: "Cửa hàng Nhật Bản" (JPY, Tiếng Nhật, Asia/Tokyo)
  - 5 kho hàng (Tokyo, Osaka, v.v.)
  - 15 máy POS

**Lợi ích**:
- Một cấu hình nhóm áp dụng cho tất cả các cửa hàng trong mỗi thị trường
- Mẫu biên lai được phân vùng theo nhóm (định dạng VAT cho EU, thuế bán hàng cho Mỹ)
- Trượt quảng cáo nhắm theo khu vực (Mỹ: Khuyến mãi Ngày Kỷ niệm, EU: Khuyến mãi Ngày lễ Hè)

### Ví dụ 2: Chuỗi cà phê

**Thiết lập**:
- 30 địa điểm, tất cả cùng một quốc gia, nhưng có định dạng khác nhau

**Cấu trúc nhóm**:
- Nhóm: "Cửa hàng trong trung tâm thương mại" (không được thiết lập, không được thiết lập, không được thiết lập)
  - 10 cửa hàng trong trung tâm thương mại
  - Trượt quảng cáo giờ mở rộng (mở đến 9 giờ tối)
  - Mẫu biên lai với mã QR xác minh bãi đỗ xe trung tâm thương mại
- Nhóm: "Cửa hàng độc lập" (không được thiết lập, không được thiết lập, không được thiết lập)
  - 15 cửa hàng mặt đường
  - Trượt quảng cáo giờ tiêu chuẩn
  - Mẫu biên lai tiêu chuẩn
- Nhóm: "Cửa hàng sân bay" (không được thiết lập, không được thiết lập, không được thiết lập)
  - 5 cửa hàng sân bay
  - Trượt quảng cáo 24 giờ
  - Mẫu biên lai tích hợp mã QR thông tin chuyến bay

**Lợi ích**:
- Nội dung quảng cáo khác nhau cho các định dạng khác nhau
- Tùy chỉnh biên lai theo vị trí
- Quản lý đơn giản hơn (cập nhật một nhóm thay vì cập nhật 10 cửa hàng riêng lẻ)

### Ví dụ 3: Vận hành nhượng quyền

**Thiết lập**:
- 100 cửa hàng, 20 nhà nhượng quyền khác nhau

**Cấu trúc nhóm**:
- Nhóm: "Nhà nhượng quyền A" (không được thiết lập, không được thiết lập, không được thiết lập)
  - 10 cửa hàng do Nhà nhượng quyền A vận hành
  - Thông tin liên hệ của Nhà nhượng quyền A trên biên lai (qua mẫu biên lai nhóm)
  - Nội dung quảng cáo của Nhà nhượng quyền A (sự kiện địa phương, khuyến mãi)
- Nhóm: "Nhà nhượng quyền B" (không được thiết lập, không được thiết lập, không được thiết lập)
  - 8 cửa hàng do Nhà nhượng quyền B vận hành
  - Thông tin liên hệ của Nhà nhượng quyền B trên biên lai
  - Nội dung quảng cáo của Nhà nhượng quyền B
- (Lặp lại cho tất cả các nhà nhượng quyền)
- Nhóm: "Cửa hàng do công ty sở hữu" (không được thiết lập, không được thiết lập, không được thiết lập)
  - 5 cửa hàng do công ty sở hữu
  - Thương hiệu công ty và quảng cáo

**Lợi ích**:
- Mỗi nhà nhượng quyền quản lý cài đặt nhóm của riêng họ
- Tính nhất quán thương hiệu được duy trì thông qua cài đặt mặc định trang web
- Tính độc lập của nhà nhượng quyền thông qua ghi đè nhóm

## Quản lý cài đặt nhóm

**Thay đổi cài đặt nhóm** ảnh hưởng đến tất cả máy POS trong nhóm đó:
- Thay đổi tiền tệ: Tất cả máy POS trong nhóm sẽ chuyển sang tiền tệ mới khi đồng bộ lần sau
- Thay đổi ngôn ngữ: Tất cả máy POS trong nhóm sẽ chuyển sang ngôn ngữ mới khi đồng bộ lần sau
- Thay đổi múi giờ: Tất cả máy POS trong nhóm sẽ tính toán lại thời gian khi đồng bộ lần sau

**Xem xét tác động**:
- Thử nghiệm thay đổi trên một máy POS trước khi áp dụng cho toàn bộ nhóm
- Thông báo cho nhân viên về các thay đổi sắp tới (ví dụ: chuyển đổi ngôn ngữ)
- Lên lịch thay đổi vào giờ thấp điểm để giảm thiểu gián đoạn

**Xóa một nhóm**:
- Gán lại tất cả kho hàng cho nhóm khác hoặc xóa giao tiếp nhóm
- Máy POS sẽ mất cài đặt cấp nhóm và quay về cài đặt mặc định trang web
- Không thể xóa nhóm khi kho hàng vẫn được gán

## Một số mẹo

- **Sử dụng mã có ý nghĩa** - "WEST" rõ ràng hơn "GRP1" khi xem xét cấu hình
- **Lên kế hoạch phân cấp trước khi tạo nhóm** - Hãy suy nghĩ kỹ về cấu trúc tổ chức của bạn trước; việc cấu trúc lại sau này rất phiền phức
- **Thử nghiệm cài đặt nhóm với một máy POS** - Trước khi gán 50 kho hàng vào một nhóm, hãy thử nghiệm cài đặt nhóm với một máy POS
- **Ghi đè ít ở cấp cửa hàng** - Quá nhiều ghi đè cấp cửa hàng sẽ làm mất đi mục đích của các nhóm
- **Ghi chú mục đích nhóm** - Ghi chú trong tên nhóm điều gì làm cho nhóm này khác biệt (địa lý, định dạng, nhà nhượng quyền)
- **Sử dụng thứ tự sắp xếp một cách chiến lược** - Sắp xếp nhóm theo mức độ quan trọng (Cửa hàng công ty trước) hoặc theo địa lý (từ Tây sang Đông) để dễ dàng điều hướng hơn
- **Giữ số lượng nhóm hợp lý** - 20+ nhóm cho thấy sự phân đoạn quá mức; hãy cân nhắc hợp nhất
- **Ghi đè tiền tệ là vĩnh viễn** - Chuyển đổi tiền tệ của nhóm trong quá trình vận hành làm phức tạp hóa kế toán; hãy lên kế hoạch cẩn thận

Hãy nhớ: Bảo tồn toàn bộ định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật chính xác như được hiển thị trong các quy tắc bảo tồn.