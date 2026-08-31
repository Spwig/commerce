---
title: 订阅计划
---

订阅计划允许您为产品提供周期性计费——非常适合消耗品、服务、精选礼盒或任何客户会重复购买的产品。本指南将介绍如何创建和配置计划、设置价格层级、添加试用期以及附加可选的附加服务。

## 快速入门

在管理侧边栏中导航至 **Subscriptions > Subscription Plans**。计划列表将显示您所有的计划，包括其定价模式、活跃订阅者数量和可见性状态。

![订阅计划列表](/static/core/admin/img/help/subscription-plans/plan-list.webp)

要创建新计划，请点击 **Create with Wizard** 按钮——这将打开计划创建向导，引导您逐步完成设置。旁边的 **+ Add Plan** 按钮则会打开一个空白表单，供偏好手动配置所有设置的商家使用。

单独的计划本身是不可购买的——它是一个模板。在此处构建完成后，您需要从产品的 **Subscriptions** 选项卡（仅限简单产品、可变产品和数字产品）将其附加到一个或多个产品上，这样客户才能实际进行订阅。有关该步骤，请参阅 [Selling Products as Subscriptions](/help/selling-products-as-subscriptions)。

## 计划编辑器

打开现有计划（从列表中点击其名称或铅笔图标）将带您进入计划编辑器。页眉显示计划名称、其定价模式、**Active**/**Inactive** 和 **Public**/**Private** 状态徽章，以及创建日期。页眉右上角的两个按钮用于保存您的更改——带圆圈的勾选图标保存并返回列表，普通勾选图标保存并保留在当前页面，以便您继续编辑。

页眉下方，一个统计条以一目了然的方式总结计划：**Active Subscriptions**、**Pricing Tiers**、**Add-ons** 和 **Total Revenue**。

表单的其余部分组织为五个选项卡：

{"| Tab | What it contains |\n|-----|-------------------|\n| **General** | Plan Information (name, slug, description) and Status (active/public) |\n| **Pricing** | Pricing Configuration, Trial Period, and Limits & Restrictions |\n| **Tiers & Add-ons** | The Pricing Tiers and Add-ons editors |\n| **Lifecycle** | Cancellation Policy and Plan Change Behavior |\n| **Advanced** | Provider Integration and Statistics |\n\nThe sections below walk through each tab's settings. When you create a brand-new plan directly from **+ Add Plan** (rather than the wizard), the same fields appear in a single scrollable form instead of tabs — save the plan once and reopen it to get the full tabbed editor.\n\n## Plan information (General tab)\n\nThe **Plan Information** card captures the core identity of your plan.\n\n- **Plan Name** — The name customers see when subscribing. Click the globe icon to add translations for other store languages.\n- **Slug** — A URL-friendly identifier auto-generated from the name (e.g., `premium-plan`). This is used internally and in integrations.\n- **Description** — Optional text describing what the plan includes. Supports translations.\n\nThe **Status** card on the same tab controls the **Active** and **Public** toggles — see [Visibility and status](#visibility-and-status) below.\n\n![General tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)\n\n## Pricing model (Pricing tab)\n\nThe **Pricing Configuration** card controls how pricing is structured for this plan:\n\n| Pricing Model | Best For |\n|---------------|----------|\n| **Tiered Pricing** | Offering monthly, quarterly, and annual commitment options with discounts for longer terms |\n| **Quantity-Based** | Per-seat or per-user pricing where the total scales with quantity (e.g., team licenses) |\n| **Flat Rate** | A single fixed price with no variations |}

对于**基于数量**的计划，请勾选**允许数量**，并设置**最小数量**（所需的最少席位）以及可选的**最大数量**，以限制订阅者可以购买的席位数量。

![计划编辑器的定价选项卡](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## 定价层级（层级与附加项选项卡）

定价层级定义了该计划中客户可用的计费频率和折扣选项。请在**层级与附加项**选项卡的**定价层级**卡片中添加它们，与附加项编辑器并列。

每个层级包含以下字段：

- **层级名称** — 向客户显示的标签（例如：`每月`、`每年 — 节省 20%`）。支持翻译。
- **计费周期** — 向客户收费的频率：每日、每周、每月、每季度、每半年或每年。
- **计费间隔** — 计费周期的倍数。设置为 `2` 并选择每月，则每 2 个月计费一次。
- **折扣百分比** — 应用于该层级产品价格的折扣。设置为 `0` 表示全价，或设置为 `20` 表示打八折。此折扣叠加在产品本身的促销价格之上。
- **默认层级** — 将其中一个层级标记为默认，以便客户查看订阅选项时预先选中它。

折扣从客户的第一个计费周期开始生效，而不仅仅是在续费时——具有 20% 折扣的层级从第一天起就收取 20% 的折扣价（如果计划包含试用期，则从试用期后的首次收费开始）。

### 示例：具有三个选项的层级计划

对于一个“咖啡俱乐部”订阅计划：

| 层级名称 | 计费周期 | 折扣 |
|-----------|---------------|----------|
| 每月 | 每月 | 0% |
| 每季度 — 节省 10% | 每季度 | 10% |
| 每年 — 节省 20% | 每年 | 20% |

## 计划附加项（层级与附加项选项卡）

附加项是订阅者可以附加到其计划上的可选额外内容。请在同一选项卡上定价层级正下方的**附加项**卡片中添加它们：

- **附加项名称** — 向客户显示的名称。

支持翻译。
- **描述** — 该附加功能提供的内容。
- **价格** — 附加功能的费用。
- **计费频率** — 附加功能是在订阅开始时按**每个计费周期**（周期性）收费，还是**一次性**收费。
- **允许数量** — 启用后，允许客户购买多个该附加功能的单位。
- **必需** — 勾选此项可自动在所有新订阅中包含该附加功能。

客户无法移除必需的附加功能。

![计划编辑器中的层级与附加功能选项卡](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## 试用期（定价选项卡）

试用期让客户在首次全额扣款之前试用您的订阅服务。请在定价配置下方的**试用期**卡片中进行配置：

- **试用期（天数）** — 免费试用天数。设置为 `0` 可禁用试用。最大值为 365 天。
- **试用价格** — 试用期间的可选优惠价格（例如，首月 1 美元）。留空表示完全免费试用。

## 限制与约束（定价选项卡）

**限制与约束**卡片同样位于定价选项卡中，包含以下内容：

- **最大计费周期数** — 订阅自动结束前的总计费周期数。留空表示无限期循环计费。适用于分期付款计划或限时订阅。

**安装费**和**排序顺序**不属于此卡片 — 它们仅在您首次通过**向导创建**流程创建计划时设置一次，之后无法从编辑屏幕更改。如果需要调整任一值，请停用该计划并使用向导重新创建，而不是编辑现有计划。请注意，在此版本中，安装费尚未在结账时自动收取 — 请将该字段视为为未来更新保留，而非当前可用的收费项。

## 取消政策（生命周期选项卡）

在**取消政策**卡片中控制客户如何取消订阅：

| 策略 | 描述 |
|--------|-------------|
| **随时取消** | 客户可以随时立即取消 |
| **在周期结束时取消** | 取消将在付费周期结束时生效 —— 客户将在到期前保持访问权限 |
| **需要最低承诺周期** | 客户必须完成一定数量的计费周期后才能取消 |

附加设置：

- **最低承诺周期** —— 使用承诺策略时，设置所需的计费周期数量（例如，`3` 表示 3 个月的最低要求）。
- **宽限期（天）** —— 在支付失败后，继续访问的天数，之后订阅将被暂停。设置为 `0` 表示立即暂停。
- **重新激活周期（天）** —— 取消后，客户可以在多少天内重新激活其订阅而无需从头开始重新订阅。

## 计划变更行为（生命周期选项卡）

在取消策略下方的 **计划变更行为** 卡片，控制客户在不同计划之间升级或降级时会发生什么：

- **升级行为** —— 设置为 **立即**（现在收取按比例计算的金额）或 **在续订时**（在下一个计费日期切换）。
- **降级行为** —— 设置为 **立即**（将信用额度应用到下一张账单）或 **在续订时**（在下一个计费日期切换）。

![计划编辑器的生命周期选项卡](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## 高级选项卡

**高级** 选项卡包含您日常使用中很少需要的设置：

- **提供者集成** —— 将此计划映射到您支付提供者的计划/价格 ID（例如，`{"stripe": "price_xxx", "paypal": "P-xxx"}`），适用于通过提供者本机管理订阅的商店，而不是通过 Spwig 自己的计费引擎。
- **统计信息** —— 只读数据：**活跃订阅**、**总收入** 和该计划的 **创建时间** / **更新时间** 时间戳。这些数据与页面顶部的统计信息条相匹配。

[Advanced tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## 可见性和状态（常规选项卡）

- **已激活** — 取消勾选以停用该计划，这样将无法再创建新的订阅。现有的订阅不受影响。
- **公开** — 取消勾选以将该计划从客户页面中隐藏（对于内部或旧计划很有用，现有订阅者仍可继续使用）。

## 提示

- 使用 **免费试用期** 以减少犹豫 —— 即使是短短7天的免费试用期，也能显著提高订阅产品的转化率。
- 设置 **三个定价层级**（每月、每季度、每年）并提供递增的折扣，以鼓励客户签订年度协议并改善现金流。
- 对于基于服务的订阅，将 **取消政策** 设置为 **在周期结束时取消**，这样客户在付费周期内仍可访问服务 —— 这样感觉更公平并减少退款请求。
- 将 **宽限期** 设置为3–7天，以应对支付失败的情况。这为客户提供了更新支付方式的时间，以免失去访问权限。
- 对附加服务使用 **必需** 标志时要谨慎 —— 仅在某些东西真正必需时使用（例如服务协议），而不是用来人为提高价格。
- 停用没有订阅者的计划，而不是删除它们 —— 这样可以保留历史数据，以便之前订阅的客户仍可访问。