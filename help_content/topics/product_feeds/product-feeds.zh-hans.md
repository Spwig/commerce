---
title: 产品数据源
---

产品数据源可让您将商品目录导出到购物平台，如Google Shopping和Facebook Catalog。一旦连接，您的产品数据将按照预定计划自动同步，以确保广告始终反映您当前的价格、库存和产品详情。

您的商店使用了一个提供程序组件系统来管理数据源。每个数据源提供程序（如Google、Facebook或其他）都作为组件安装，然后通过提供程序账户进行连接。您可以同时运行多个数据源提供程序——例如，一个用于Google Shopping的数据源，另一个用于Facebook。

## 连接数据源提供程序

在同步您的商品目录之前，您需要安装并连接至少一个数据源提供程序组件。

### 安装提供程序组件

提供程序组件可在Spwig组件市场中找到。您的商店管理员通过组件更新系统安装它们。一旦安装了提供程序组件，它就会在创建数据源提供程序账户时显示为一个选项。

### 创建数据源提供程序账户

1. 导航到 **营销 > 数据源提供程序**
2. 点击 **+ 添加数据源提供程序账户**
3. 填写表单：

**提供程序信息部分：**
- **站点** — 选择您的商店（只有一个）
- **提供程序组件** — 选择已安装的数据源提供程序（例如，Google Shopping、Facebook Catalog）
- **账户名称** — 一个描述性名称，如 `Google Shopping — 主账户` 或 `Facebook Catalog — 美国`

**配置部分：**
- **是否启用** — 勾选以启用数据源生成和同步
- **是否为主账户** — 如果这是您此平台类型的主数据源提供程序，请勾选
- **优先级** — 控制列表中的排序顺序（数字较小的会优先显示）
- **配置** — 提供程序特定的设置（见下文）

4. 点击 **保存**

### 数据源配置选项

**配置** 字段接受一个包含以下选项的JSON对象：

保留所有Markdown格式、图片路径、代码块和专业术语。

table

heading

#### Example configuration for daily XML feed targeting the US:

code_block

{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}

heading

## Filtering which products appear in the feed

paragraph

You can control exactly which products are included by adding a `product_filter` section to the config:

code_block

{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}

table

paragraph

You can also exclude specific products by their IDs using `exclude_products`:

code_block

{
  "exclude_products": [42, 87, 103]
}

heading

## Monitoring sync status

paragraph

The feed provider accounts list shows the sync status of each connected feed at a glance:

list

paragraph

The list also shows the number of products in the current feed and when the last sync ran.

heading

## Viewing generated feeds

转到 **营销 > 产品提要** 以查看生成的提要文件。

每条记录代表一个生成的提要快照，并显示：

- **提供商账户** — 此提要属于哪个账户
- **格式** — XML、CSV 或 JSON
- **产品数量** — 包含的产品数量
- **大小** — 生成的提要文件大小
- **生成时间** — 创建时间
- **过期时间** — 此缓存版本的过期时间
- **状态** — 提要是否仍然有效或已过期
- **下载次数** — 此提要已被下载的次数

在管理后台中，提要文件是只读的 — 它们由同步过程自动生成。

## 查看同步历史记录

转到 **营销 > 提要同步日志** 以查看所有提要账户的完整同步尝试历史记录。每个日志条目记录：

- 被同步的提供商账户
- 同步类型（完整、增量、手动或计划）
- 状态（成功、部分成功、失败等）
- 同步、失败和跳过的产品数量
- 同步持续时间
- 任何错误信息

页面顶部的同步日志仪表板显示总体统计信息：总同步次数、成功率和平均同步持续时间。使用 **账户** 和 **同步类型** 过滤器缩小到特定提要。

### 当同步失败时该怎么做

1. 转到 **营销 > 提要同步日志** 并找到失败的条目
2. 点击日志条目以查看完整的 **错误信息** 和 **错误详情**
3. 常见原因包括：
   - 缺少必需的产品字段（标题、价格、图片）
   - 无效或过期的 API 凭据 — 重新安装提供商组件以刷新凭据
   - 连接到提供商 API 的网络错误
4. 一旦问题解决，下一次计划的同步将自动运行，或者您可以从提供商账户触发手动同步

## 小贴士

保留所有 markdown 格式、图片路径、代码块和专业术语。

- 将 `"sync_interval": "daily"` 用于大多数情况 — 除非你面临极高的价格波动，否则 Google 和 Facebook 不需要更频繁的更新
- 始终在你的产品筛选器中包含 `"in_stock_only": true`，以避免推广客户无法购买的产品
- 使用包含平台和目标市场的描述性账户名称（例如，`Google Shopping — UK`），以便于管理多个数据源
- 提供商账户上的 **Products in Feed** 数量可立即告诉你是否有少于预期的产品被包含 — 如果数量看起来偏低，请检查你的产品筛选器设置
- 为每种提供商类型标记一个账户作为 **Primary Feed**；某些报告工具会使用此标记来识别你的主要数据源
- 在对产品目录进行批量更改后，查看同步日志以确认更新的数据是否已正确获取