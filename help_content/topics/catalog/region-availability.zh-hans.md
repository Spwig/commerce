---
title: 地区可用性
---

地区可用性控制产品可以在哪些销售区域销售，以及这些区域外的客户如何体验您的目录。当产品仅限某些国家销售时，当库存保留给本地市场时，或者当您按地区逐步推出新产品时，可以使用此功能。

这建立在**销售区域**之上，它将国家分组为命名市场（请参阅销售区域指南以了解如何设置这些区域）。一旦您的区域存在，您可以将单个产品限制为这些区域，并决定受限产品在无法购买它们的客户面前如何显示。

## 将产品限制为特定区域

每个产品在其编辑页面上都有一个**地区可用性**设置。打开**产品 > 所有产品**，选择一个产品，并在**状态**部分找到它，旁边有**状态**、**特色**和**从商店前台隐藏**。

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-field.webp
  description: 产品编辑页面滚动到状态部分，区域可用性下拉菜单可见且设置为“仅在选定区域”
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: 如果可能，请使用至少已选择2个区域的产品，以便在第二张截图中内联表格有可见行。
-->

| 选项 | 它意味着什么 |
|--------|---------------|
| **在所有区域都可用** | 没有限制。产品在所有地方都可销售。这是每个产品的默认设置。 |
| **仅在选定区域** | 允许列表。产品仅在您在下方选择的区域销售 —— 其他所有地方，它都被视为不可用。 |
| **所有区域，除了选定区域** | 拒绝列表。产品在所有区域销售，*除了*您在下方选择的区域。 |

### 选择区域

在状态部分下方，一个标题为**区域可用性（选定区域）**的表格列出了上述模式适用的区域。

1.

将 **区域可用性** 设置为 **仅在选定区域** 或 **除选定区域外的所有区域**。
2.

在 **区域可用性（选定区域）** 表中，点击 **添加另一个区域** 并选择一个销售区域。
3.

为每个要添加的区域重复此操作。
4.

点击 **保存**。

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-inline.webp
  description: "'区域可用性（选定区域）' 内联表格，已添加两个或三个区域行"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

如果 **区域可用性** 设置为 **在所有区域都可用**，则此表中的任何内容都将被忽略 —— 如果要移除限制而无需删除行，请先清除模式下拉菜单。

若要查看所有产品的区域规则列表（当同时审核多个产品时非常有用），请访问 `/admin/catalog/productregionvisibility/` 处的 **产品区域可见性**。

## 显示产品不可配送的地区

当顾客的区域与产品的可用性规则不匹配时，您可以在 **库存显示设置** 中控制他们看到的内容，该设置位于 **区域可用性** 部分。此页面目前尚无侧边栏快捷方式 —— 请直接访问 `/admin/catalog/stockdisplaysettings/` 打开它。

<!-- screenshots-needed:
- url: /en/admin/catalog/stockdisplaysettings/1/change/
  filename: stock-display-region-availability.webp
  description: "滚动到 '区域可用性' 字段集的库存显示设置更改表单，显示区域限制的显示下拉菜单"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

| Option | What shoppers see |
|--------|-------------------|
| **Show, marked as unavailable** (default) | The product still appears in listings, with an "Unavailable" badge and a "Does not ship to [region]" notice in place of the Add to Cart button. A banner also appears at the top of listing pages ("Some products don't ship to [destination]") with a link to filter down to only the items that do ship there. |
| **Hide from listings** | The product is removed from listing and search results entirely for shoppers in that region. |

<!-- screenshots-needed:
- url: /en/products/
  filename: storefront-region-restricted-listing.webp
  description: Storefront product listing with the region banner at the top and at least one product card showing the "Unavailable" badge and "Does not ship to [region]" notice
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Requires a live ship-to selection (or GeoIP detection) that resolves to a region a demo product is restricted from.
-->

A restricted product's own page always shows a "This product doesn't ship to [region]" notice when a shopper reaches it directly (for example, from a shared link or search engine result) — this applies regardless of which listing option you choose above, since a direct link bypasses the listing entirely.

## Letting shoppers pick or discover their region

Spwig can detect a shopper's region automatically and offer a switch, and you can add a selector so shoppers can change it themselves at any time.

### Before you begin

You need two things configured for region detection and switching to work correctly:

1. **Sales Regions** — the countries in each region and each region's default currency.

如果在侧边栏的 **库存** 下没有看到 **销售区域**，请转到 **设置 > 商店设置 > 电商业务** 下打开 **启用多仓库** 以显示菜单链接（您不需要实际使用多个仓库 —— 此设置仅用于解锁菜单项）。

您也可以直接访问 `/admin/catalog/salesregion/`。
2. **运输国家** —— 您的商店实际运输到的国家。

这些通常已经设置好了：您添加到运输区域的每个国家也会自动添加到这里。

要查看或手动调整列表，请直接打开 `/admin/shipping/shippingcountry/`（它目前还没有侧边栏链接）。

### 自动区域确认

Spwig 会从顾客的位置检测其区域并自动应用。当该区域与您商店的默认（主）市场不同时 —— 并且您有 2 个或更多活动的销售区域 —— Spwig 会在他们第一次访问时显示一个确认信息，让他们知道他们所在的区域并可以更改它：

> **我们已将您的区域设置为 [区域]**
> 我们从您的位置中选择了这个区域，以便您看到正确的商品和价格。不正确吗？选择您的国家。
> 运输到：[国家选择器]  **[继续浏览]**

<!-- screenshots-needed:
- url: /en/
  filename: region-confirmation-modal.webp
  description: 在商店前台首页的 "We've set your region to [Region]" 确认模态框，包含国家选择器和 Keep browsing 按钮
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: 需要 GeoIP 解析到非默认区域且至少有 2 个活动的销售区域才能触发。在本地，将 "geo_country" cookie 设置为非默认国家以进行模拟。
-->

在选择器中选择不同的国家会立即切换他们的区域。关闭它或点击 **继续浏览** 会保留他们的当前区域，并且他们在该浏览器上不会再被询问。已经在默认区域的访客根本不会看到确认信息。

### 在你的网站头部或页脚中添加配送地址选择器

如果你希望购物者可以随时自行更改地区（而不是仅依赖自动提示），请将 **配送地址选择器** 小部件添加到你的网站头部或页脚。

1. 导航到 **设计 > 头部构建器**（或 **页脚构建器**）。
2. 从小部件库中拖动 **配送地址选择器** 小部件到一个行中。
3. 点击 **保存**。

<!-- screenshots-needed:
- url: /en/theme/header/builder/
  filename: ship-to-selector-widget-library.webp
  description: 头部构建器，小部件库侧边栏已打开，显示/突出显示配送地址选择器小部件
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

该小部件无需任何设置 —— 它会自动列出你当前有效的配送国家，并显示购物者的当前选择（或通过GeoIP检测的国家，如果他们尚未选择）。

选择不同的国家会立即更新他们的地区并重新加载页面的产品可用性和价格。

配送地址选择器目前还没有专用的设置表单。如果你想要更改其按钮样式（轮廓、实心或透明）或隐藏“配送至”标签，请在构建器中打开小部件的设置，并直接编辑 **自定义配置（JSON）** 字段，使用 `button_style` 和 `show_label`。

### 货币跟随地区

如果你的商店支持多种货币（在 **设置 > 多种货币** 中设置），通过提示或配送地址选择器切换地区时，也会切换到该地区的默认货币。如果你的商店只有一种货币，或者尚未明确启用第二种货币，当购物者更改地区时货币不会改变。

## 提示

保留所有markdown格式、图片路径、代码块和术语。

- 保留 **区域可用性** 为 **所有区域均可**，除非您有特定原因要限制产品——这是最简单的选项，且在以后添加区域时无需维护。
- 对于小范围的允许列表（例如，产品首先在某个国家推出），请使用 **仅在选定区域**，而对于小范围的阻止列表（例如，除了某个未获得许可的国家外的所有区域），请使用 **所有区域除外选定** —— 选择设置所需行数较少的那个。
- 如果购物者报告某个应显示的产品缺失，请检查产品的 **区域可用性** 设置，以及他们的国家是否被一个活动的 **销售区域** 和一个活动的 **运输国家** 覆盖。
- **从列表中隐藏** 可以让您的目录在无法购买某些商品的购物者面前保持整洁，但这也意味着在这些区域，商品推广和搜索结果会显得更少——如果希望购物者即使在无法结账的区域也能浏览完整目录，通常 **显示，标记为不可用** 更好。
- 通过在页眉中添加 **运送至选择器** 并在依赖 GeoIP 检测进行发布前自行在国家之间切换，测试区域行为。
- 明确设置您的区域的优先级值（在销售区域页面上）——最高优先级的活动区域是购物者所在国家无法检测或与任何区域不匹配时的默认选项。