---
title: Quy tắc kinh doanh dựa trên vị trí
---

Các quy tắc kinh doanh dựa trên vị trí cho phép bạn tự động thực hiện các hành động khi một khách truy cập đến từ một quốc gia, khu vực hoặc loại thiết bị cụ thể. Bạn có thể sử dụng các quy tắc để đặt tiền tệ cho khách hàng đến từ một khu vực cụ thể, chuyển hướng khách truy cập đến một trang được địa phương hóa, hiển thị một banner khuyến mãi hoặc hạn chế truy cập vào nội dung nhất định.

Các quy tắc được đánh giá theo thứ tự ưu tiên mỗi lần một phiên khách truy cập được thiết lập. Khi một quy tắc khớp, các hành động được cấu hình sẽ được thực hiện ngay lập tức.

## Cách quy tắc kinh doanh hoạt động

Mỗi quy tắc bao gồm hai phần:

- **Điều kiện** — tiêu chí phải được đáp ứng để quy tắc được kích hoạt (ví dụ: "khách truy cập đến từ Đức")
- **Hành động** — điều gì xảy ra khi tất cả điều kiện khớp (ví dụ: "đặt tiền tệ thành EUR")

Điều kiện và hành động được lưu trữ dưới dạng đối tượng JSON trong biểu mẫu quy tắc. Spwig đánh giá tất cả các quy tắc đang hoạt động theo thứ tự ưu tiên (số nhỏ nhất trước) và áp dụng bất kỳ quy tắc nào khớp.

## Điều hướng đến quy tắc kinh doanh

Đi đến **Customers > Business Rules** để xem tất cả các quy tắc đã cấu hình của bạn. Danh sách hiển thị tên, trạng thái, ưu tiên, số lần đã kích hoạt và thời gian cuối cùng kích hoạt của mỗi quy tắc.

Click vào bất kỳ quy tắc nào để xem hoặc chỉnh sửa nó, hoặc click **+ Add Business Rule** để tạo một quy tắc mới.

## Tạo quy tắc kinh doanh

### Bước 1: thông tin cơ bản

Nhập các chi tiết nhận dạng quy tắc:

- **Tên** — tên rõ ràng và mô tả (ví dụ: `Set EUR for Eurozone`)
- **Mô tả** — ghi chú tùy chọn giải thích mục đích của quy tắc
- **Is Active** — đánh dấu để kích hoạt quy tắc; bỏ đánh dấu để tạm dừng mà không xóa nó
- **Ưu tiên** — số nhỏ hơn chạy trước; sử dụng `10`, `20`, `30` để dành không gian cho các quy tắc trong tương lai

### Bước 2: xác định điều kiện

Trong trường **Điều kiện**, nhập một đối tượng JSON mô tả khi quy tắc nên được kích hoạt. Tất cả điều kiện trong đối tượng phải đúng để quy tắc khớp.

#### Các khóa điều kiện có sẵn

| Điều kiện | Định dạng | Ví dụ |
|-----------|--------|---------|
| `country_in` | Mảng các mã quốc gia ISO | `["DE", "FR", "IT"]` |
| `country_not_in` | Mảng các mã quốc gia ISO | `["US", "CA"]` |
| `region_in` | Mảng các tên khu vực | `["Bavaria", "Catalonia"]` |
| `region_not_in` | Mảng các tên khu vực | `["Quebec"]` |
| `is_mobile` | Boolean | `true` |
| `is_vpn` | Boolean | `false` |

#### Ví dụ điều kiện

Khách truy cập đến từ Đức, Pháp hoặc Ý:
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Khách truy cập đến từ Hoa Kỳ và đang sử dụng thiết bị di động:
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Khách truy cập đến từ bên ngoài Liên minh châu Âu:
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Bước 3: xác định hành động

Trong trường **Hành động**, nhập một đối tượng JSON mô tả điều gì nên xảy ra khi quy tắc được kích hoạt.

#### Các khóa hành động có sẵn

| Hành động | Định dạng | Mô tả |
|--------|--------|-------------|
| `set_currency` | Chuỗi mã tiền tệ | Chọn tiền tệ mặc định cho khách truy cập |
| `set_language` | Chuỗi mã ngôn ngữ | Thiết lập ngôn ngữ hiển thị |
| `show_banner` | Boolean | Kích hoạt banner khuyến mãi |
| `redirect_to` | Chuỗi đường dẫn URL | Chuyển hướng khách truy cập đến URL khác |

#### Ví dụ hành động

Đặt tiền tệ thành Euro:
```json
{
  "set_currency": "EUR"
}
```

Chuyển hướng đến trang đích được địa phương hóa:
```json
{
  "redirect_to": "/de/"
}
```

Đặt cả tiền tệ và ngôn ngữ cùng lúc:
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Các ví dụ thực tế

### Ví dụ: Quy tắc tiền tệ khu vực Euro

**Tình huống:** Tự động hiển thị giá bằng Euro cho khách truy cập đến từ các quốc gia thuộc khu vực Euro.

| Trường | Giá trị |
|-------|-------|
| Tên | `Eurozone — Set EUR` |
| Ưu tiên | `10` |
| Is Active | Đã đánh dấu |
| Điều kiện | `{"country_in": ["AT","BE","DE","ES","FI","FR","GR","IE","IT","LU","NL","PT"]}` |
| Hành động | `{"set_currency": "EUR"}` |

### Ví dụ: Quy tắc giá cho Vương quốc Anh

**Tình huống:** Hiển thị giá bằng GBP cho khách truy cập đến từ Vương quốc Anh.

| Trường | Giá trị |
|-------|-------|
| Tên | `UK — Đặt GBP` |
| Ưu tiên | `20` |
| Hoạt động | Đã chọn |
| Điều kiện | `"{\"country_in\": [\"GB\"]}"` |
| Hành động | `"{\"set_currency\": \"GBP\"}"` |

### Ví dụ: chuyển hướng đến phần cửa hàng địa phương

**Tình huống:** Gửi khách truy cập từ Úc đến trang Úc riêng biệt.

| Trường | Giá trị |
|-------|-------|
| Tên | `Australia — Redirect` |
| Ưu tiên | `30` |
| Hoạt động | Đã chọn |
| Điều kiện | `"{\"country_in\": [\"AU\"]}"` |
| Hành động | `"{\"redirect_to\": \/au\/}"` |

## Kiểm tra quy tắc

Bạn có thể xác minh rằng một quy tắc phù hợp với hồ sơ người truy cập mong muốn mà không cần chờ lưu lượng truy cập thực tế:

1. Trong danh sách Quy tắc Kinh doanh, chọn quy tắc bằng cách sử dụng ô kiểm
2. Mở dropdown **Hành động** và chọn **Kiểm tra quy tắc đã chọn**
3. Nhấp **Tiến hành**

Spwig sẽ đánh giá quy tắc dựa trên hồ sơ người truy cập giả định từ Mỹ và báo cáo xem nó có khớp không và các hành động nào sẽ được kích hoạt.

## Theo dõi hoạt động quy tắc

Cột **Đã kích hoạt** trong danh sách quy tắc hiển thị số lần mỗi quy tắc đã được kích hoạt. Nhấp vào quy tắc để xem **Thời gian kích hoạt cuối cùng** trong phần Thống kê.

Sử dụng hành động **Đặt lại thống kê** để đặt lại số lần kích hoạt về 0 nếu bạn muốn bắt đầu đo đếm từ một ngày cụ thể sau khi thay đổi quy tắc.

## Một số lưu ý

- Thiết lập ưu tiên với khoảng cách (10, 20, 30) thay vì các số liên tiếp (1, 2, 3) để bạn có thể chèn quy tắc mới sau này mà không cần phải đổi lại tất cả các số
- Các quy tắc được kích hoạt theo thứ tự ưu tiên và tất cả các quy tắc khớp sẽ được áp dụng — nếu hai quy tắc đều đặt tiền tệ, hành động của quy tắc có độ ưu tiên thấp hơn (số lớn hơn) sẽ được áp dụng cuối cùng
- Sử dụng nút **Hoạt động** để tạm dừng quy tắc trong thời gian khuyến mãi mà không cần xóa cấu hình
- Luôn kiểm tra quy tắc mới trước khi kích hoạt nó trong môi trường trực tuyến để đảm bảo điều kiện là chính xác
- Phát hiện VPN (`"is_vpn": true`) có sẵn nếu bạn muốn áp dụng xử lý khác cho các khách truy cập che giấu vị trí của họ, nhưng lưu ý rằng một số khách hàng hợp lệ sử dụng VPN để bảo vệ quyền riêng tư