---
title: 电子邮件配置
---

电子邮件配置控制您的商店如何发送事务性电子邮件——订单确认、发货通知、密码重置等。Spwig 内置了 SMTP 服务器，并支持外部电子邮件服务提供商以提高送达率。

![电子邮件账户](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## 可用提供商

| 提供商 | 描述 |
|----------|-------------|
| **内置 SMTP** | 随 Spwig 提供的免费自托管电子邮件服务器。自动 DKIM 签名。 |
| **Gmail API** | 使用 OAuth 认证通过您的 Gmail 或 Google Workspace 账户发送。 |
| **通用 SMTP** | 连接任何 SMTP 服务器（SendGrid、Mailgun、Amazon SES 或您自己的邮件服务器）。 |

## 设置电子邮件

导航至 **设置 > 电子邮件账户** 并点击 **添加电子邮件账户** 以启动设置向导。

### 步骤 1：选择提供商

选择您的电子邮件提供商。内置 SMTP 服务器是最简单的入门选项——它不需要外部账户。

### 步骤 2：配置凭据

输入所选提供商的凭据：

- **内置 SMTP** — 无需凭据。服务器运行在您的 Spwig 安装环境中。
- **Gmail API** — 通过 Google OAuth 进行身份验证。您将被重定向以使用您的 Google 账户登录。
- **通用 SMTP** — 输入 SMTP 服务器地址、端口、用户名和密码。

### 步骤 3：发件人配置

设置 outgoing 电子邮件的发件人身份：

- **发件人邮箱** — 显示在“发件人”字段中的电子邮件地址（例如，orders@yourstore.com）
- **发件人名称** — 电子邮件地址旁边的显示名称（例如，“您的商店名称”）
- **回复至邮箱** — 客户回复的接收地址（可以与发件人地址不同）

### 步骤 4：DNS 验证

验证您域名的电子邮件认证记录。向导将检查三个 DNS 记录：

| 记录 | 用途 |
|--------|---------|
| **SPF** | 授权您的服务器代表您的域名发送电子邮件 |
| **DKIM** | 对电子邮件进行数字签名，以证明其未被篡改 |
| **DMARC** | 告知接收服务器如何处理未通过 SPF/DKIM 检查的电子邮件 |

对于每条记录，向导将显示：
- **当前状态** — 记录是否正确配置
- **所需值** — 需要在域名注册商处添加的确切 DNS 记录
- **传播状态** — 最近的更改是否已生效（DNS 更改可能需要长达 48 小时）

内置的 SMTP 服务器会自动为您的域名生成 DKIM 密钥。

### 步骤 5：发送测试邮件

发送测试邮件以验证一切正常工作：
1. 输入收件人电子邮件地址
2. 点击 **发送测试**
3. 检查您的收件箱中的测试消息
4. 验证邮件到达时没有垃圾邮件警告

### 步骤 6：保存并激活

保存配置并将该账户设置为激活状态。如果它应该是主要电子邮件账户，请将其标记为 **默认**。

## 电子邮件模板

Spwig 包含 30 多个电子邮件模板，涵盖所有事务性事件。导航至 **设置 > 电子邮件模板** 进行管理。

### 模板类型

模板涵盖所有商店事件，包括：
- **订单生命周期** — 确认、处理中、已发货、已送达、已取消
- **支付** — 收据、退款确认、支付失败
- **客户账户** — 欢迎、密码重置、电子邮件验证
- **礼品卡** — 交付、余额通知
- **物流** — 跟踪更新、送达确认
- **数字产品** — 下载链接、许可证密钥
- **营销** — 弃购挽回、评价请求

### 自定义模板

1. 导航至模板列表
2. 点击模板进行编辑
3. 修改主题行、页眉、正文内容和页脚
4. 使用模板变量（例如 `{{ order.number }}`、`{{ customer.name }}`）实现动态内容
5. 保存前预览电子邮件

### 多语言支持

保留所有 Markdown 格式、图片路径、代码块和技术术语。

Email templates support multiple languages:
- Each template can have translations for all your store's active languages
- The system sends emails in the customer's preferred language
- **Language fallback chain** — If a translation isn't available, the system falls back to the store's default language
- Use the **AI Translation** feature to automatically translate templates into other languages

### Cloning Templates

To create a customized version of a system template:
1. Open the template you want to modify
2. Click **Clone Template**
3. Edit the cloned version
4. The clone takes priority over the original system template

## Email Queue

Monitor outgoing emails at **Settings > Email Queue**:

- **Queued** — Emails waiting to be sent
- **Sending** — Currently being transmitted
- **Sent** — Successfully delivered
- **Failed** — Could not be delivered (with error details)
- **Bounced** — Rejected by the recipient's mail server

Click any email to view its full details including recipient, subject, send time, and delivery status.

## Delivery Tracking

Track email engagement:
- **Opens** — How many recipients opened the email
- **Clicks** — Link clicks within the email
- **Bounces** — Hard and soft bounce tracking
- **Complaints** — Spam reports from recipients

## Multiple Accounts

You can configure multiple email accounts:
- **Default Account** — Used for all outgoing emails unless overridden
- **Fallback** — If the default account fails, emails queue for retry
- Use different accounts for different purposes (e.g., one for transactional emails, another for marketing)

## Email Delivery Mode

Navigate to **Settings > Store Settings** to control how your store handles outgoing emails. These settings are useful during development and testing.

| 模式 | 描述 |
|------|-------------|
| **实时** | 邮件正常发送给真实收件人 |
| **暂停** | 邮件保留在队列中，直到您切换回实时模式才会发送 |
| **仅记录** | 邮件记录在发件箱中，但永远不会发送 |

### 测试重定向邮件

设置一个**测试重定向邮件**地址，以拦截所有发出的邮件并将其重定向到单一地址。设置后，所有邮件——无论真实收件人是谁——都将发送到该地址。这对于在不意外发送给真实客户的情况下测试邮件模板非常有用。留空则向实际收件人发送邮件。

### 沙盒邮件白名单

在沙盒或开发模式下，您可以将邮件发送限制为已批准地址的白名单。仅向白名单上的地址发送邮件。所有其他邮件仅被记录，但永远不会发送。管理员邮件会自动始终包含在内。您最多可以添加 10 个地址。

## 提示

- 从**内置 SMTP** 服务器开始以快速设置，如果需要更高的发送量或更好的送达率，再切换到外部提供商。
- 始终配置 **SPF、DKIM 和 DMARC** 记录——没有它们，邮件更有可能进入垃圾邮件文件夹。
- 在任何配置更改后发送一封**测试邮件**，以验证发送是否正常工作。
- 定期监控邮件队列中的**失败**或**退信**邮件——这些表明存在送达率问题。
- 使用**专业发件人地址**（例如 orders@yourstore.com），而不是免费邮件地址，以获得更好的信任度和送达率。
- 保持模板简洁——事务性邮件应快速传递信息，而不是营销通讯。