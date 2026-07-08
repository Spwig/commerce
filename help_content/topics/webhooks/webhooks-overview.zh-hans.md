---
title: Webhooks 概述
---

Webhooks 可让您的商店在发生某些事件时自动通知外部系统（如库存工具、ERP、履行服务或自定义应用程序）。这些系统无需反复询问“是否有变化？”，您的商店会在事件发生时立即推送通知。

## Webhooks 的作用

当商店中发生事件（如下单、收到付款、商品缺货）时，Spwig 会向您配置的 URL 发送包含事件数据的 HTTP POST 请求。接收系统可以立即处理这些数据，例如更新库存、触发运单或发送自定义通知。

Webhooks 的常见用途包括：

- 与履行合作伙伴实时同步订单
- 在库存变化时更新 ERP 中的库存
- 在订单状态变化时触发短信或推送通知
- 在数据仓库中记录事件以供报告
- 连接到自动化工具，如 Zapier 或 Make

## 查看和管理端点

导航到 **集成 > Webhooks** 以查看所有配置的 Webhook 端点。

![Webhook 端点列表](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

列表显示每个端点的名称、URL、激活状态、它订阅的事件数量、其健康状态以及它最后一次接收交付的时间。

### 健康状态指示器

**健康状态** 列可让您一目了然地了解每个端点的性能：

- **健康** — 所有最近的交付都已成功
- **降级** — 有一些最近的失败，但端点仍处于活动状态
- **不健康 / 已禁用** — 在连续失败太多次（默认为 10 次）后，该端点会自动禁用。您必须在底层问题解决后手动重新启用它。

## 创建 Webhook 端点

点击 **+ 添加 Webhook 端点** 以打开设置向导。向导将引导您完成四个步骤。

### 第 1 步：基本信息

- **名称** — 用于标识此端点的友好标签（例如，`Order Fulfilment Service` 或 `Inventory Sync`）。
- **URL** — 将接收 webhook POST 请求的服务器的完整 URL。

此 URL 必须是公开可访问的（不能是 localhost URL）。
- **描述** — 关于此端点用途的可选说明。
- **启用** — 此端点是否应接收通知。

取消勾选可临时暂停通知，而无需删除该端点。

### 第 2 步：事件订阅

选择哪些事件应触发向此端点的通知。事件按类别分组：

#### 订单事件

| 事件 | 触发时机 |
|-------|---------------|
| `order.created` | 创建新订单时 |
| `order.paid` | 订单付款确认时 |
| `order.cancelled` | 订单被取消时 |
| `order.fulfilled` | 订单中的所有商品已发货 |
| `order.partially_fulfilled` | 订单中的部分商品已发货 |
| `order.status_changed` | 订单状态发生变化时 |
| `order.note_added` | 向订单添加备注时 |

#### 支付事件

| 事件 | 触发时机 |
|-------|---------------|
| `payment.received` | 收到付款时 |
| `payment.failed` | 付款尝试失败时 |
| `payment.pending` | 付款等待确认时 |

#### 发货事件

| 事件 | 触发时机 |
|-------|---------------|
| `shipment.created` | 创建发货时 |
| `shipment.shipped` | 发货已发出 |
| `shipment.delivered` | 发货已送达 |
| `shipment.returned` | 发货已退回 |
| `shipment.tracking_updated` | 跟踪信息已更新 |

#### 库存事件

| 事件 | 触发时机 |
|-------|---------------|
| `inventory.low_stock` | 库存低于阈值时 |
| `inventory.out_of_stock` | 商品缺货时 |
| `inventory.restocked` | 商品已补货 |
| `inventory.adjusted` | 库存被手动调整时 |

#### 商品事件

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

#### 客户事件

`customer.created`, `customer.updated`, `customer.deleted`

#### 订阅事件

`subscription.created`, `subscription.activated`, `subscription.renewed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `subscription.resumed`, `subscription.payment_failed`

#### 其他事件

`refund.created`, `refund.completed`, `refund.failed`, `cart.abandoned`, `cart.recovered`, `translation.job_completed`, `translation.job_failed`

要接收所有事件，请订阅 `*`（通配符）。这对于通用日志记录端点很有用，但会产生更多流量 —— 仅在生产集成中实际需要的事件上进行订阅。

### 第 3 步：配置

- **最大重试次数** —— Spwig 在放弃之前应重试失败交付的次数（默认值：5）。每次重试使用指数退避间隔。
- **超时（秒）** —— 等待接收服务器响应的时间，超时后将标记交付失败（默认值：30 秒）。仅当您的服务器已知较慢时才增加此值。

### 第 4 步：安全性

每个 Webhook 端点都会自动生成一个 **签名密钥** —— 一个 64 个字符的随机密钥。Spwig 使用此密钥对每个 Webhook 负载使用 HMAC-SHA256 签名进行签名。

签名包含在 `X-Webhook-Signature` 请求头中。您的接收服务器应验证此签名，以确认请求确实来自您的商店且未被篡改。

密钥在管理界面中以遮蔽形式显示。要查看或轮换密钥，请使用 Spwig API。如果您怀疑密钥已被泄露，请立即轮换密钥。

## 启用和禁用端点

要快速启用或禁用一个或多个端点而无需逐一打开：

1.

勾选您要更改的端点旁边的复选框
2.


使用 **Action** 下拉菜单选择 **启用所选端点** 或 **禁用所选端点**
3.

点击 **Go**

若要重新启用因故障而被自动禁用的端点，请选择该端点，使用 **重置故障计数** 操作，然后重新启用。请先修复导致故障的原因，否则它会很快再次被禁用。

## Tips

- 仅订阅你实际需要的事件 —— 不必要的事件会在日志中产生噪音并增加交付负载。
- 在接收服务器上处理负载之前，始终验证 webhook 的签名。这可以保护你免受伪造请求的影响。
- 使用 **Description** 字段记录此端点连接的系统或集成。这有助于在数月后进行故障排除。
- 将 **Timeout** 设置为略高于服务器的典型响应时间。对于大多数集成来说，10–15 秒的超时时间就足够了。
- 如果端点变为 **Unhealthy**，请首先检查交付日志（参见 **Webhook Deliveries**），以了解故障模式，然后再重新启用它。
- 对于测试，可以将 webhook 指向像 [webhook.site](https://webhook.site) 这样的工具，以检查原始负载，而无需使用实际服务器。