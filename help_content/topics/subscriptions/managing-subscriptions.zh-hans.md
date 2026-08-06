---
title: 管理客户订阅
---

客户订阅部分让您全面了解商店中所有活动、暂停和取消的定期订阅。在这里您可以监控账单健康状况，查看单个订阅详情，并在出现问题时采取行动。

## 查看客户订阅

导航至 **订阅 > 客户订阅** 以查看所有客户的订阅列表。

![客户订阅列表](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

列表显示每个订阅的客户、计划名称、当前状态、下次计费日期以及已完成的计费周期数。

### 筛选和搜索

使用右侧的筛选面板按以下条件缩小订阅范围：

- **状态** — 按活动、试用、逾期、暂停、取消或过期筛选
- **计划** — 查看特定计划的订阅
- **提供者模式** — 原生（Stripe/PayPal管理）或回退（内部计费）

使用搜索栏通过客户电子邮件地址查找订阅。

## 订阅状态

了解每种状态有助于您识别需要关注的订阅：

| 状态 | 含义 |
|--------|---------------|
| **试用** | 客户处于免费或折扣价格的试用期 |
| **活动** | 订阅正常 — 计费及时且访问权限有效 |
| **逾期** | 付款尝试失败 — 系统正在重试。在宽限期客户仍可访问 |
| **暂停** | 订阅暂时中止 — 不计费，无访问 |
| **取消** | 已请求取消。客户可能在周期结束日期前仍可访问 |
| **过期** | 订阅已完全结束 — 试用期已过，达到最大计费周期或取消期已过 |

需要最多关注的是 **逾期** 订阅 — 如果付款继续失败且宽限期用尽，订阅将被暂停。

## 查看订阅详情

点击任何订阅以打开详细视图。

这显示了：

### 当前计费周期

- **当前周期开始/结束** — 活动计费窗口的日期
- **下次计费日期** — 下一次尝试收费的日期
- **上次计费日期** 和 **上次计费状态** — 最近一次计费尝试的结果
- **计费周期数** — 已完成的成功的计费周期数量

### 订阅信息

- **计划** 和 **定价层级** — 客户所使用的计划和计费频率
- **产品/变体** — 与该订阅关联的目录产品（如果适用）
- **数量** — 数量型计划的席位或单位数量
- **支付令牌** — 用于定期计费的存储支付方式

### 试用详情

如果订阅处于试用期，**试用结束日期** 显示客户试用期结束的日期以及开始全面计费的日期。

### 取消详情

对于已取消的订阅，您可以查看：

- **取消类型** — 取消是立即生效、在周期结束时生效，还是计划中的
- **取消时间** — 取消请求的时间
- **取消原因** — 关于客户取消原因的备注（如果已记录）
- **重新激活截止日期** — 客户可以在不从头开始重新订阅的情况下重新激活的最后日期

### 宽限期和承诺

- **宽限期结束日期** — 如果支付失败，此日期显示在访问被暂停前的最后期限
- **最低承诺结束日期** — 对于有最低承诺的计划，最早可以取消的日期

## 暂停订阅

暂停的订阅会暂时停止计费，同时暂停访问。这对于希望暂时休息而无需完全取消的客户很有用。

要查看暂停的订阅，请按 **状态: 暂停** 过滤。详细视图显示：

- **Paused At** — 当暂停开始的时间
- **Pause Reason** — 暂停的原因说明
- **Auto Resume Date** — 如果设置，订阅将自动恢复计费和访问的日期

订阅在自动恢复日期恢复，或者在客户手动重新激活时恢复。

## 计费周期日志

每次计费尝试——无论成功还是失败——都会记录在计费周期日志中。导航至 **订阅 > 计费周期日志** 以查看此历史记录。

![计费周期日志列表](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### 阅读计费周期日志条目

每个日志条目记录以下信息：

- **订阅** — 该计费尝试所属的客户订阅
- **周期编号** — 顺序计费周期（周期 1 = 试用后的首次扣费）
- **计费日期** — 扣费尝试的日期
- **状态** — 待处理、处理中、成功、失败或重试中
- **金额明细**：
  - **基础金额** — 在任何调整之前的计划价格
  - **数量金额** — 对于席位/单位数量的额外费用
  - **附加费用金额** — 活动附加服务的总成本
  - **折扣金额** — 应用的总折扣
  - **总金额** — 最终扣费金额（或尝试扣费）
- **支付方式** — 使用的卡或支付方式
- **提供商交易 ID** — 支付提供商的参考编号（对于退款查询有用）
- **失败原因** — 如果计费失败，失败的原因（例如，卡被拒、资金不足）

### 诊断支付失败

如果客户联系您关于计费问题，请找到他们的订阅并检查计费周期日志。**失败原因** 字段会解释哪里出错了。常见的失败原因包括：

- **Card declined** — The customer's card was rejected by their bank
- **Insufficient funds** — The account balance was too low at billing time
- **Card expired** — The saved payment method has expired
- **Network error** — A temporary connection issue with the payment provider — usually resolves on retry

For persistent failures, direct the customer to update their payment method in their account settings.

## How renewals are fulfilled

Every successful renewal charge creates a brand-new paid order for that billing cycle — it isn't just a payment record. That order flows through your normal fulfilment process exactly like an order placed at checkout:

- **Physical products** — The renewal order enters your regular fulfilment queue for picking, packing, and shipping. It is not automatically stock-allocated the instant the card is charged, so a temporary stock shortfall never blocks a charge that already succeeded — you'll still see the order and can fulfil it as stock allows.
- **Digital products** — Access (download links, license keys) is re-granted automatically the moment the renewal order is created, the same way it would be for a first-time purchase.

Renewal orders copy the shipping and billing details from the order that started the subscription, so you don't need to re-enter anything. They don't carry a special badge in your **Orders** list, but you can always trace a specific cycle back to its order: open **Subscriptions > Billing Cycle Logs**, click the log entry for that cycle, and the **Order** field links straight to it.

## Automatic subscription emails

Spwig sends subscription lifecycle emails automatically — you don't need to trigger these manually. The ones merchants ask about most:

| 电子邮件 | 何时发送 |
|-------|----------------|
| **续订提醒** | 在即将产生续订费用之前 |
| **试用期结束** | 在免费或折扣试用期转换为完整计费之前 |
| **支付失败** | 在续订费用失败后立即发送，并在宽限期即将结束时作为最终通知再次发送（催缴） |
| **取消确认** | 当订阅被取消时 |

Spwig还会在订阅生命周期的相应阶段发送欢迎邮件、支付成功、暂停/恢复、过期、重新激活、计划更改和支付方式过期邮件。所有这些都是普通电子邮件模板——请参阅[电子邮件模板](/help/email-templates)以查看或自定义其内容并确认它们已启用。

## 客户自助服务

客户不需要联系您进行常规的订阅更改——他们可以从他们的账户中管理自己的订阅：查看详细信息和账单历史，暂停、恢复、取消，并更新已保存的支付方式。这涵盖了原本会进入您支持队列的大部分内容，因此当客户联系您关于他们的订阅时，首先检查他们是否已经在他们的账户页面上尝试过，然后再在后台为您他们进行更改。

## 提示

- 每周检查**逾期**筛选器以捕捉有流失风险的订阅。

给客户发送一封快速邮件通常可以在宽限期结束前解决支付问题。
- 计费周期日志是只读的——它们会自动创建，无法修改。

这确保了可靠的审计跟踪。
- 如果客户的订阅显示**逾期**，但他们已经更新了支付方式，下一次自动重试将使用新卡。

重试遵循计划中配置的宽限期时间表。
- **已过期**的订阅不会被删除——它们仍会显示以便于报告。

保留所有markdown格式、图片路径、代码块和术语。

使用日期筛选器来聚焦当前有效的订阅。
- 对于处于**试用**状态的订阅，请查看**试用结束日期**以预判即将进行的首次收费，并主动解决任何支付方式问题。
- 如果客户说一个实体续订"还没有发货"，请检查您的常规配送队列，而不是订阅记录——续订订单的配送方式与其他订单相同，不会跳过队列。