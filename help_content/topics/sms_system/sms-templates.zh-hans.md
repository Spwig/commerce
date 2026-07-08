---
title: 短信模板
---

短信模板控制您的商店通过短信向客户发送的每条通知的文本。每个模板对应一个特定的事件——例如订单确认或发货更新——并使用占位符变量，当消息发送时，Spwig会用实际的订单详细信息替换这些变量。

导航到 **短信系统 > 短信模板** 查看和编辑您的模板。

![短信模板列表](/static/core/admin/img/help/sms-templates/templates-list.webp)

## 可用的模板类型

Spwig 包含以下内置的模板类型：

| 模板类型 | 发送时机 |
|---------------|-----------------|
| 订单确认 | 当客户下单时 |
| 发货更新 | 当订单的跟踪状态发生变化时 |
| 配送通知 | 当订单标记为已送达时 |
| 重置密码 | 当客户请求重置密码时 |
| 验证码 | 当需要一次性验证码进行账户验证时 |
| POS 收据 | 当在销售终端处理销售时 |
| 营销 | 用于促销活动（需要单独的同意） |
| 自定义 | 用于您创建的任何其他通知 |

## 编辑模板

1. 导航到 **短信系统 > 短信模板**
2. 点击您要编辑的模板
3. 在 **消息** 字段中更新您想要的文本
4. 使用 `{variable}` 占位符来包含订单特定的信息（请参阅下方的变量）
5. 勾选 **启用** 以启用模板——未启用的模板不会被发送
6. 点击 **保存**

![编辑短信模板](/static/core/admin/img/help/sms-templates/template-edit.webp)

## 使用变量

变量是以花括号书写的占位符——例如，`{name}` 或 `{order_number}`。当 Spwig 发送消息时，它会将每个占位符替换为该客户或订单的实际值。

### 常见变量

保留所有 markdown 格式、图片路径、代码块和专业术语。

| Variable | Replaced with |
|----------|---------------|
| `{name}` | The customer's first name |
| `{order_number}` | The order reference number |
| `{total}` | The order total amount |
| `{tracking_number}` | The shipment tracking number |
| `{store_name}` | Your store's name |
| `{code}` | A verification or reset code |

**Example message:**

```
Hi {name}, your order #{order_number} has been confirmed. Total: {total}. We'll update you when it ships. - {store_name}
```

When sent, this becomes:

```
Hi Sarah, your order #10045 has been confirmed. Total: $89.00. We'll update you when it ships. - The Garden Shop
```

> Only include variables that are available for a given template type. For example, `{tracking_number}` is available in a Shipping Update template but not in a Password Reset template. If you use an unavailable variable, it will appear as-is (unreplaced) in the message.

## Character limits and message length

Standard SMS messages are limited to **160 characters** for a single segment. Longer messages are split into multiple segments and sent as one (concatenated SMS), but carriers count each segment separately for billing purposes.

**Tips for staying within the limit:**
- Keep messages concise — one purpose per message
- Abbreviate common phrases where natural (e.g., "Ord" instead of "Order")
- Avoid unnecessary filler words

Spwig does not enforce a hard character limit in the editor, so count your characters (including variable values) before saving.

## Activating and deactivating templates

The **Active** toggle on each template controls whether that notification type is sent. If a template is inactive, Spwig skips sending that notification entirely — the message will appear as **Skipped** in the SMS Outbox with the reason `template_inactive`.

To activate a template:
1. Open the template
2. Check the **Active** checkbox
3. Save

To deactivate (stop sending a notification type without deleting the template):
1.

Open the template
2.

取消勾选 **启用**
3.

保存

## 小贴士

- 以与您的品牌一致的语气撰写信息 —— 短信是一种直接且个人化的渠道，因此友好的语气效果很好
- 消息中始终包含您的店铺名称，以便顾客知道是谁在给他们发短信
- 保持订单确认信息简洁：订单号、总金额以及下一步操作的说明就足够了
- 通过在您自己的店铺上放置一个测试订单（使用您控制的电话号码）来测试信息，以查看顾客实际收到的内容
- 如果某个通知引发了混淆或投诉，请停用该模板并进行修改，而不是直接删除它 —— 这样在更新后可以重新启用
- 营销模板只能发送给已明确同意接收短信营销的客户，这是大多数国家电信法规的要求