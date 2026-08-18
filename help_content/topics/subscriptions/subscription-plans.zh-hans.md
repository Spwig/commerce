---
title: 订阅计划
---

订阅计划让您能够为您的产品提供定期收费服务 —— 适用于消耗品、服务、精选礼盒或任何客户会反复购买的产品。本指南将解释如何创建和配置计划，设置定价层级，添加试用期，并附加可选的附加服务。

## 入门

在管理后台侧边栏中导航至 **订阅 > 订阅计划**。计划列表显示了所有您的计划及其定价模型、活跃订阅者数量和可见性状态。

![订阅计划列表](/static/core/admin/img/help/subscription-plans/plan-list.webp)

要创建新计划，请点击 **使用向导创建** 按钮 —— 这将打开计划创建向导，逐步引导您完成设置。旁边的 **+ 添加计划** 按钮会打开一个空白表单，供希望手动配置所有内容的商家使用。

一个单独的计划是无法购买的 —— 它只是一个模板。在此处构建完成后，从产品的 **订阅** 选项卡（仅限普通商品、变体商品和数字商品）将其附加到一个或多个产品上，这样客户才能实际订阅。请参阅 [将产品作为订阅销售](/help/selling-products-as-subscriptions) 完成此步骤。

## 计划编辑器

打开现有计划（从列表中点击其名称或铅笔图标）会进入计划编辑器。标题显示计划名称、其定价模型、**激活**/**停用** 和 **公开**/**私有** 状态徽章，以及创建日期。标题右上角的两个按钮保存您的更改 —— 对勾图标保存并返回列表，普通对勾图标保存并保持在页面上以便继续编辑。

在标题下方，一个统计栏快速总结了计划的概况：**激活的订阅**、**定价层级**、**附加服务** 和 **总收入**。

其余表单分为五个选项卡：

{"| Tab | What it contains |\n|-----|-------------------|\n| **General** | Plan Information (name, slug, description) and Status (active/public) |\n| **Pricing** | Pricing Configuration, Trial Period, and Limits & Restrictions |\n| **Tiers & Add-ons** | The Pricing Tiers and Add-ons editors |\n| **Lifecycle** | Cancellation Policy and Plan Change Behavior |\n| **Advanced** | Provider Integration and Statistics |\n\nThe sections below walk through each tab's settings. When you create a brand-new plan directly from **+ Add Plan** (rather than the wizard), the same fields appear in a single scrollable form instead of tabs — save the plan once and reopen it to get the full tabbed editor.\n\n## Plan information (General tab)\n\nThe **Plan Information** card captures the core identity of your plan.\n\n- **Plan Name** — The name customers see when subscribing. Click the globe icon to add translations for other store languages.\n- **Slug** — A URL-friendly identifier auto-generated from the name (e.g., `premium-plan`). This is used internally and in integrations.\n- **Description** — Optional text describing what the plan includes. Supports translations.\n\nThe **Status** card on the same tab controls the **Active** and **Public** toggles — see [Visibility and status](#visibility-and-status) below.\n\n![General tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)\n\n## Pricing model (Pricing tab)\n\nThe **Pricing Configuration** card controls how pricing is structured for this plan:\n\n| Pricing Model | Best For |\n|---------------|----------|\n| **Tiered Pricing** | Offering monthly, quarterly, and annual commitment options with discounts for longer terms |\n| **Quantity-Based** | Per-seat or per-user pricing where the total scales with quantity (e.g., team licenses) |\n| **Flat Rate** | A single fixed price with no variations |}

对于**基于数量**的计划，请勾选**允许数量**，并设置**最小数量**（所需的最小席位数），并可选地设置**最大数量**以限制订阅者可以购买的席位数。

![计划编辑器的定价选项卡](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## 定价层级（层级与附加选项选项卡）

定价层级定义了客户在此计划上可使用的计费频率和折扣选项。在**定价层级**卡片中添加它们，同时在**层级与附加选项**选项卡中添加附加选项编辑器。

每个层级包含以下字段：

- **层级名称** — 显示给客户的标签（例如，`Monthly`, `Annual — Save 20%`）。支持翻译。
- **计费周期** — 客户被计费的频率：每日、每周、每月、每季度、每半年或每年。
- **计费间隔** — 计费周期的乘数。设置为`2`，每月计费则每2个月计费一次。
- **折扣百分比** — 该层级对产品价格应用的折扣。设置为`0`表示全价，或设置为`20`表示打8折。此折扣会叠加在产品本身的促销定价之上。
- **默认层级** — 将一个层级标记为默认层级，以便在客户查看订阅选项时预选它。

折扣从客户的第一个计费周期开始适用，而不仅仅是续订时 —— 一个有20%折扣的层级从第一天开始就打8折（或从试用期后的第一次收费开始，如果该计划有试用期的话）。

### 示例：带有三个选项的层级计划

对于“Coffee Club”订阅计划：

| 层级名称 | 计费周期 | 折扣 |
|-----------|---------------|----------|
| 每月 | 每月 | 0% |
| 每季度 — 节省10% | 每季度 | 10% |
| 每年 — 节省20% | 每年 | 20% |

## 试用期

试用期允许客户在第一次完整收费前试用您的订阅。在**试用期**部分中配置此功能：

- **试用期（天数）** — 免费试用天数。

设置为`0`以禁用试用期。

最大为365天。
- **试用价格** — 试用期间的可选折扣价格（例如，第一个月$1）。

留空以提供完全免费的试用。

## 取消政策

在 **取消政策** 部分控制客户如何取消订阅:

| 政策 | 描述 |
|--------|-------------|
| **随时取消** | 客户可以在任何时候立即取消 |
| **在周期结束时取消** | 取消将在付费周期结束时生效 — 客户将在到期前保持访问权限 |
| **需要最低承诺** | 客户必须完成一定数量的计费周期后才能取消 |

其他设置:

- **最低承诺（周期）** — 使用承诺政策时，设置所需的计费周期数量（例如，3 表示 3 个月的最低要求）。
- **宽限期（天数）** — 在支付失败后继续访问的天数，订阅将被暂停。设置为 0 表示立即暂停。
- **重新激活期限（天数）** — 取消后，客户可以在该期限内重新激活其订阅而无需从头开始重新订阅。

## 计划变更行为

当客户在不同计划之间升级或降级时，您可以控制变更何时生效:

- **升级行为** — 设置为 **立即**（现在收取按比例计算的金额）或 **在续订时**（在下一个计费日期切换）。
- **降级行为** — 设置为 **立即**（对下一张账单应用信用）或 **在续订时**（在下一个计费日期切换）。

## 限制和限制

- **最大计费周期** — 订阅自动结束前的总计费周期数。留空以无限期续订。适用于分期付款计划或限时订阅。
- **设置费用** — 订阅首次创建时收取的一次性费用（例如，入门或激活费用）。设置为 0.00 表示无设置费用。

## 计划附加项

附加项是订阅者可以附加到其计划的可选额外内容。

保留所有 markdown 格式、图片路径、代码块和术语。

在 **计划附加功能** 部分中添加它们：

- **附加功能名称** — 显示给客户的名称。支持翻译。
- **描述** — 附加功能提供什么。
- **价格** — 附加功能的成本。
- **计费频率** — 附加功能是按 **计费周期**（定期收费）还是在订阅开始时 **一次性** 收费。
- **允许数量** — 启用以允许客户购买多个附加功能单位。
- **必需** — 勾选此选项以在所有新订阅中自动包含该附加功能。必需的附加功能不能被客户删除。

## 可见性和状态

- **活动** — 取消勾选以停用一个计划，这样就不能再创建新订阅。现有订阅不受影响。
- **公开** — 取消勾选以从客户页面中隐藏该计划（对于内部或旧计划有用，现有订阅者仍可继续）。
- **排序顺序** — 控制订阅选择页面上的显示顺序。较小的数字会先显示。

## 提示

- 使用 **免费试用期** 来减少犹豫 —— 即使是短至7天的免费试用期也能显著提高订阅产品的转化率。
- 设置 **三个定价层级**（每月、每季度、每年），并随着折扣增加来鼓励年度承诺并改善现金流。
- 对于基于服务的订阅，将 **取消政策** 设置为 **在周期结束时取消**，以便客户在付费期间保持访问权限 —— 这样感觉公平并减少退款。
- 将 **宽限期** 设置为3–7天，以应对支付失败。这给了客户更新支付方式的时间，以免失去访问权限。
- 对附加功能的 **必需** 标志要谨慎使用 —— 仅用于真正必需的东西（例如，服务协议），而不是用来夸大价格。
- 停用没有订阅者的计划，而不是删除它们 —— 这样可以为之前订阅的任何客户保留历史数据。

保留所有markdown格式、图片路径、代码块和术语。