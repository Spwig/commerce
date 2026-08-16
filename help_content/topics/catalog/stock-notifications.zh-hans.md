---
title: 库存通知
---

库存通知允许客户注册以在缺货商品重新有货时收到电子邮件通知。库存显示设置控制客户在商品页面上看到的内容—例如库存状态标签、低库存警告，以及商品售完时会发生什么。

## 库存显示设置

库存显示设置是适用于所有商品的全局默认设置，除非在分类或商品级别被覆盖。

导航至 **目录 > 库存显示设置** 来配置这些选项。您商店有一个设置记录—点击它进行编辑。

### 库存状态显示

| 设置 | 描述 |
|---------|-------------|
| **显示库存状态** | 在商品页面上显示“有库存”或“缺货”标签 |
| **显示低库存警告** | 当库存不足时显示“仅剩X件”信息 |
| **低库存阈值** | 低于该数量时会显示低库存警告（默认：5） |
| **显示确切数量** | 显示剩余的确切数字（例如，“仅剩3件！”）而不是通用警告 |

### 缺货行为

**缺货行为** 设置决定了当商品无库存时客户看到的内容：

| 行动 | 客户看到的内容 |
|--------|-------------------|
| **从列表中隐藏** | 该商品将从分类页面和搜索结果中移除 |
| **显示为不可用** | 商品可见但无法加入购物车 |
| **显示“通知我”按钮** | 客户可以注册他们的电子邮件以在库存恢复时收到通知 |
| **允许缺货订单** | 客户可以在库存为零时购买该商品 |

设置 **缺货信息** 以自定义商品不可用时显示的文本（默认：`缺货`）。

设置 **缺货订单信息** 以自定义缺货订单商品的显示文本（默认：`可缺货订购`）。

### 发货和配送显示

| 设置 | 说明 |
|---------|-------------|
| **显示“发货地”信息** | 在商品页面显示仓库名称 |
| **显示预计送达时间** | 显示从仓库位置计算的预计送达日期 |

### 允许 backorders（全局设置）

勾选 **允许缺货订单** 以允许客户默认购买任何缺货商品。个别商品和分类可以覆盖此设置。

## 库存补货通知

当您将缺货操作设置为 **显示“通知我”按钮** 时，客户可以在商品页面输入他们的电子邮件地址，以便在商品补货时收到电子邮件通知。

### 查看补货通知请求

导航至 **目录 > 库存通知** 以查看所有客户补货通知请求。每个记录显示：
- 客户 电子邮件地址
- 商品和变体（如果适用）
- 所选区域偏好的仓库（如果客户选择了区域偏好）
- 请求创建时间
- 通知发送时间（如果尚未发送则为空）

### 通知发送时间

当商品库存水平上升到零以上时，Spwig 会自动发送补货电子邮件。**通知时间** 字段记录了电子邮件发送的时间。

客户只会收到一封通知邮件。一旦通知后，如果商品再次缺货，客户需要重新注册。

### 过滤通知请求

使用管理界面的筛选器来查找：
- 某个特定商品的请求
- 已经通知过的请求（查看已联系过的客户）
- 仍处于等待状态的请求（客户等待补货）

## 商品级别的覆盖设置

全局库存显示设置可以按商品或分类覆盖。在商品编辑表单中，查找 **库存** 部分，您可以设置特定于商品的 **缺货操作**，这与全局默认设置不同。

This is useful when you want most products to allow backorders but keep a few products set to "Notify Me" — or when a specific product should be hidden when out of stock.

## Tips

- Set **Low Stock Threshold** to the reorder point you typically use, so customers are warned about limited availability before you run out entirely.
- Use the **Show "Notify Me" button** option instead of hiding out-of-stock products — customers who sign up represent real demand that can justify a restock order.
- Enable **Show Exact Quantity** sparingly. For most stores, showing "Only 3 left!" works better than showing the exact number, as it creates urgency without revealing your full inventory picture.
- Check the stock notifications list before placing a new order — the number of pending notification requests tells you how much demand exists for that product.
- If you use backorders, update your **Backorder Message** to set accurate expectations (e.g., "Ships in 2-3 weeks — order now to reserve your place").
- Combine out-of-stock notifications with email marketing: when you restock a popular product, send a campaign to everyone who signed up, not just the automatic notification email.