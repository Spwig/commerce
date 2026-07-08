---
title: Product Feeds
---

Product feeds let you export your catalog to shopping platforms such as Google Shopping and Facebook Catalog. Once connected, your product data is automatically synchronized on a schedule so your ads always reflect your current prices, stock, and product details.

Your store uses a provider component system for feeds. Each feed provider (Google, Facebook, or others) is installed as a component and then connected through a provider account. You can run multiple feed providers at the same time — for example, one feed for Google Shopping and a separate one for Facebook.

## Connecting a feed provider

Before you can sync your catalog, you need to install and connect at least one feed provider component.

### Installing a provider component

Provider components are available in the Spwig component marketplace. Your store administrator installs them through the component update system. Once a provider component is installed, it appears as an option when creating a feed provider account.

### Creating a feed provider account

1. Navigate to **Marketing > Feed Providers**
2. Click **+ Add Feed Provider Account**
3. Fill in the form:

**Provider Information section:**
- **Site** — select your store (there is only one)
- **Provider Component** — choose the installed feed provider (e.g., Google Shopping, Facebook Catalog)
- **Account Name** — a descriptive name such as `Google Shopping — Main` or `Facebook Catalog — US`

**Configuration section:**
- **Is Active** — check to enable feed generation and syncing
- **Is Primary** — check if this is your main feed provider for this platform type
- **Priority** — controls the sort order in the list (lower numbers appear first)
- **Config** — provider-specific settings (see below)

4. Click **Save**

### Feed configuration options

The **Config** field accepts a JSON object with the following options:

| Option | Values | Description |
|--------|--------|-------------|
| `sync_interval` | `hourly`, `daily`, `weekly`, `manual` | How often the feed is automatically regenerated |
| `format_preference` | `xml`, `csv`, `json` | Output format (most platforms prefer XML) |
| `include_variants` | `true` / `false` | Include product variants as separate feed entries |
| `target_country` | Country code e.g. "US" | Target country for the feed |
| `content_language` | Language code e.g. "en" | Language of the product data |

#### Example configuration for daily XML feed targeting the US:

```json
{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}
```

## Filtering which products appear in the feed

You can control exactly which products are included by adding a `product_filter` section to the config:

```json
{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}
```

| Filter option | Description |
|---------------|-------------|
| `status` | Only include products with these statuses. Use `["published"]` for live products only. |
| `in_stock_only` | Set to `true` to exclude out-of-stock products |
| `categories` | Limit to specific category IDs |
| `brands` | Limit to specific brand IDs |

You can also exclude specific products by their IDs using `exclude_products`:

```json
{
  "exclude_products": [42, 87, 103]
}
```

## Monitoring sync status

The feed provider accounts list shows the sync status of each connected feed at a glance:

- **PENDING** — no sync has run yet, or the feed is waiting to be generated
- **SYNCING** — a sync is currently in progress
- **SUCCESS** — the last sync completed without errors
- **ERROR** — the last sync failed; the error message is shown on the account detail page

The list also shows the number of products in the current feed and when the last sync ran.

## Viewing generated feeds

Navigate to **Marketing > Product Feeds** to see the generated feed files. Each entry represents one generated feed snapshot and shows:

- **Tài khoản nhà cung cấp** — tài khoản mà feed này thuộc về
- **Định dạng** — XML, CSV hoặc JSON
- **Số lượng sản phẩm** — số lượng sản phẩm được bao gồm
- **Kích thước** — kích thước tệp của feed được tạo
- **Thời gian tạo** — thời điểm feed được tạo
- **Hết hạn** — thời điểm phiên bản được lưu trữ này hết hạn
- **Trạng thái** — feed vẫn còn hợp lệ hay đã hết hạn
- **Số lần tải xuống** — số lần feed này đã được tải xuống

Feeds là chỉ đọc trong phần quản trị — chúng được tạo tự động bởi quy trình đồng bộ.

## Xem lịch sử đồng bộ

Chuyển đến **Marketing > Feed Sync Logs** để xem toàn bộ lịch sử của mọi lần đồng bộ cho tất cả tài khoản feed của bạn. Mỗi mục nhật ký ghi lại:

- Tài khoản nhà cung cấp đã được đồng bộ
- Loại đồng bộ (Toàn bộ, Tăng thêm, Thủ công hoặc Theo lịch trình)
- Trạng thái (Thành công, Thành công một phần, Thất bại, v.v.)
- Số lượng sản phẩm đã đồng bộ, thất bại và bỏ qua
- Thời gian đồng bộ
- Các thông báo lỗi (nếu có)

Bảng điều khiển nhật ký đồng bộ ở đầu trang hiển thị thống kê tổng thể: tổng số lần đồng bộ, tỷ lệ thành công và thời gian đồng bộ trung bình. Sử dụng bộ lọc **Tài khoản** và **Loại đồng bộ** để thu hẹp lại một feed cụ thể.

### Điều gì nên làm khi đồng bộ thất bại

1. Chuyển đến **Marketing > Feed Sync Logs** và tìm mục đã thất bại
2. Nhấp vào mục nhật ký để xem toàn bộ **Thông báo lỗi** và **Chi tiết lỗi**
3. Các nguyên nhân phổ biến bao gồm:
   - Thiếu các trường sản phẩm bắt buộc (tiêu đề, giá, hình ảnh)
   - Thông tin xác thực API không hợp lệ hoặc đã hết hạn — cài đặt lại thành phần nhà cung cấp để làm mới thông tin xác thực
   - Lỗi mạng khi kết nối với API của nhà cung cấp
4. Khi vấn đề đã được khắc phục, lần đồng bộ theo lịch trình tiếp theo sẽ chạy tự động, hoặc bạn có thể kích hoạt đồng bộ thủ công từ tài khoản nhà cung cấp

## Một số mẹo

- Đặt `"sync_interval": "daily"` cho hầu hết các trường hợp sử dụng — Google và Facebook không yêu cầu cập nhật thường xuyên hơn trừ khi bạn có sự biến động giá rất cao
- Luôn bao gồm `"in_stock_only": true` trong bộ lọc sản phẩm của bạn để tránh quảng cáo các sản phẩm mà khách hàng không thể mua
- Sử dụng tên tài khoản mô tả bao gồm nền tảng và thị trường mục tiêu (ví dụ: `Google Shopping — UK`) để dễ dàng quản lý nhiều feed
- Số lượng **Sản phẩm trong Feed** trên tài khoản nhà cung cấp cho bạn biết ngay lập tức nếu có ít sản phẩm hơn dự kiến được bao gồm — kiểm tra lại cài đặt bộ lọc sản phẩm của bạn nếu con số dường như thấp
- Đánh dấu một tài khoản là **Feed chính** cho mỗi loại nhà cung cấp; một số công cụ báo cáo sử dụng điều này để xác định feed chính của bạn
- Kiểm tra nhật ký đồng bộ sau bất kỳ thay đổi hàng loạt nào trong danh mục sản phẩm của bạn để xác nhận dữ liệu đã được cập nhật đúng cách