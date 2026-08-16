---
title: 配置商店设置
---

商店设置是配置商店身份、本地化、品牌和操作首选项的中心位置。导航到 **设置 > 商店设置** 开始。

![商店设置常规选项卡](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## 常规选项卡

**常规** 选项卡包含商店的核心身份设置。

### 商店身份

- **商店名称** — 在页面标题、电子邮件和管理面板标题栏中显示的名称。
- **标语** — 商店的简短描述，用于SEO和社交分享。
- **网站URL** — 商店的公共网址。这在电子邮件、站点地图生成和链接建设中使用。

### 联系信息

- **联系电子邮件** — 接收订单通知，并在客户沟通中显示。
- **电话号码** — 可选的支持电话号码，在页脚和电子邮件中显示。

### 业务地址

输入完整的地址（街道、城市、州、邮政编码、国家）。这将用于：
- 运费起点计算
- 税务计算
- 法律要求和发票

## 品牌

### 标志

上传商店标志（推荐PNG或SVG，~200x50像素，透明背景）。标志将出现在：
- 商店前台标题栏
- 电子邮件模板
- 管理面板

### Favicon

上传正方形favicon（ICO或PNG，32x32像素）。它将显示为：
- 浏览器标签图标
- 书签图标
- 移动主屏幕图标

## 本地化

### 默认语言

从10个支持的选项中选择商店的主要语言：

| 语言 | 代码 |
|----------|------|
| 英语 | en |
| 西班牙语 | es |
| 法语 | fr |
| 德语 | de |
| 葡萄牙语 | pt |
| 日语 | ja |
| 简体中文 | zh-hans |
| 繁体中文 | zh-hant |
| 俄语 | ru |
| 阿拉伯语 | ar |

默认语言控制管理界面语言和前台内容的回退语言。

### 时区

选择商店的时区以获得准确的订单时间戳、计划促销和报告。

### 货币

- **Default Currency** — The primary currency for pricing and accounting.
- **Multi-Currency** — Enable to let customers view prices in their preferred currency with automatic conversion using real-time exchange rates.

Configure additional currencies in **Settings > Store Settings > Currency**.

## E-Commerce Settings

### Guest Checkout

Allow purchases without creating an account:
- Faster checkout flow
- Lower friction for first-time buyers
- Captures less customer data

### Account Creation Timing

Control when customers are prompted to create an account:

| Option | Description |
|--------|-------------|
| **After Purchase (Recommended)** | Prompt for account creation after a successful order — leverages post-purchase goodwill for best conversion |
| **During Checkout** | Create an account before payment is processed |
| **Before Checkout** | Require an account before shopping (not recommended — reduces conversion) |

You can also set a custom **Account Creation Message** to explain the benefits of registering.

### Inventory Defaults

- **Track Inventory** — Enable stock tracking globally
- **Low Stock Threshold** — Stock level at which low-stock alerts are sent to the admin email (default: 10 units)

### Inventory Intelligence

![Inventory Intelligence card showing Default Reorder Lead Time and Safety Stock Multiplier fields](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

These settings tune the automatic reorder, safety-stock, and sales-velocity calculations, and control how out-of-stock and low-stock situations are handled.

- **Default Reorder Lead Time (Days)** — How many days it typically takes to receive restock from your supplier once you place an order (default: 14).

Forecasting uses this to flag products that need reordering *now* to avoid a stockout before the new stock arrives.
- **Safety Stock Multiplier** — A buffer applied on top of expected demand to absorb sales spikes or supplier delays.

例如，乘数 `1.5` 会在您计算的安全库存基础上增加 50% 的缓冲；`2.0` 会将其翻倍。

对于缺货成本较高的产品（畅销品、季节性商品）应提高此值；对于周转缓慢的库存，应降低此值。
- **速度计算窗口（天）** —— Spwig 用于计算每个产品销售速度的回顾窗口，这反过来决定了补货建议和库存天数（默认：30）。

较短的窗口能更快响应最近的需求变化；较长的窗口能平滑季节性峰值，因此单个繁忙周不会影响预测。
- **默认允许缺货** —— 新创建产品默认的缺货设置（默认关闭）。

每个产品仍可以在其产品页面上单独覆盖此设置，现有产品会保留其当前设置 —— 更改此设置仅会影响新产品的默认设置，不会对您的商品目录进行回溯更新。
- **低库存警报频率** —— Spwig 移动应用通知低库存的频率：**实时** 在产品库存低于低库存阈值时立即发送推送通知；**每日摘要** 和 **每周总结** 则在该时间点汇总所有当前低库存产品并发送一次推送通知。

此设置仅在 **低库存警报**（下方的电子邮件设置）启用时生效 —— 当警报关闭时，任何频率都不会发送通知。

### 文档与发票

![显示税务ID/增值税号、发票页脚文本和包装单页脚文本字段已填写示例值的文档与发票卡片](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

这些字段会填充 Spwig 为订单生成的发票和包装单 —— 例如，当商家下载或发送 PDF 发票，或为发货打印包装单时。
- **税务ID / 增值税号** —— 您的业务税务识别号码。

打印在生成的发票上，以满足本地税务文档要求。
- **发票页脚文字** — 显示在每张生成的发票底部的自由文本。

常见用途：付款条款（"30天内付款"），感谢信息，或银行转账详情。
- **包装单页脚文字** — 显示在每张生成的包装单底部的自由文本。

常见用途：退换货说明或给仓库/履行团队的备注。
- **文档Logo宽度（像素）** — 你的商店Logo在生成的PDF发票和包装单上的宽度（默认：200像素）。

高度会自动调整以匹配，以保持你的Logo的宽高比。

Logo图像本身来自你的 **Logo**（品牌，上方）— SVG格式的Logo不会在PDF文档中绘制，因此如果你在店面使用矢量图形，请上传PNG或JPG格式的Logo版本。

## 邮件设置

在 **设置 > 邮件账户** 和 **设置 > 邮件模板** 中配置邮件发送设置。有关完整详细信息，请参阅 [邮件配置](/help/email-configuration)。

在商店设置中可用的关键邮件设置：

- **订单确认邮件** — 开启或关闭自动确认邮件
- **发货通知邮件** — 开启或关闭发货更新通知
- **库存不足警报** — 当库存低于阈值时向管理员邮箱发送警报
- **邮件发送模式** — 实时（正常发送）、暂停（暂停所有邮件）或仅记录（记录但不发送）
- **测试邮件转发地址** — 为测试目的将所有传出邮件转发到一个地址。

## 安全设置

### 双因素认证（2FA）

控制员工是否需要使用双因素认证：

| 设置 | 描述 |
|---------|-------------|
| **可选** | 员工可以选择启用2FA，但不是必需的 |
| **推荐** | 员工会看到一个提示，鼓励他们设置2FA |
| **必需** | 员工在启用2FA之前无法访问管理界面 |

保留所有markdown格式、图片路径、代码块和术语。

- **Grace Period (Days)** — 员工在启用强制措施后设置2FA的天数
- **Allow Trusted Devices** — 允许员工在已识别设备上跳过2FA验证，持续设定的天数

## Cookie Consent

配置显示给商店访客的cookie同意横幅：

- **Cookie Consent Enabled** — 显示或隐藏cookie横幅
- **Banner Position** — 横幅在屏幕上的显示位置（底部栏、角落弹窗等）
- **Consent Mode** — 简单通知、选择加入或选择退出
- **Banner Title and Text** — 可自定义的标题和描述，显示给访客
- **Category Descriptions** — 为分析、营销和功能cookie分别设置描述

所有横幅文本字段都支持多语言商店的翻译。

## Communications

**Communications** 选项卡控制商店如何获取、确认以及让客户管理营销电子邮件和短信的同意。这些设置决定了您的法律合规性（电子邮件的GDPR，短信的TCPA），因此在启动前请与您的法律顾问审查这些设置 —— Spwig提供控制选项，但不提供建议。

![显示电子邮件营销同意、偏好和取消订阅以及短信同意卡片的Communications选项卡](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Email Marketing Consent

- **Enable Double Opt-In for Marketing Emails** — 当启用时，客户选择加入营销电子邮件后，会收到确认电子邮件，并且必须点击其中的链接，Spwig才会向其发送任何营销信息。当禁用时，勾选营销加入框就足够了。默认启用，符合GDPR最佳实践。
- **Default Marketing Opt-In State** — 新创建的客户帐户的初始营销加入状态。默认为关闭（GDPR选择退出），因此新客户在主动选择加入之前默认未订阅营销电子邮件。

当双倍确认开启时，选择加入会触发一封确认电子邮件，包含验证链接。

保留所有markdown格式、图像路径、代码块和术语。

在客户点击之前，他们会被记录为已同意但未确认，营销邮件会跳过他们 —— 交易性电子邮件（订单确认、运输更新、密码重置）不会受到此设置的影响。

### 首选设置与退订
- **启用客户首选设置中心** —— 当开启时，客户可以从其账户仪表板链接的自助服务页面管理其电子邮件和短信首选项。当关闭时，该页面及其支持的API返回不可用，仪表板链接将被隐藏。无论哪种方式，电子邮件中的一键退订链接仍能正常工作 —— 这个逃生舱是合规性要求，不受此切换的影响。
- **收集退订原因** —— 当开启时，一键退订页面会在客户确认前询问他们简要的原因：*我收到太多电子邮件*, *内容与我不相关*, *我从未注册过*, *我不再感兴趣*, 或 *其他*。客户选择的原因会被记录到同意审计跟踪，以便您可以随时间审查退订模式。

### 短信同意
- **需要短信验证** —— 当开启时（默认），客户必须在Spwig向他们发送任何短信（包括营销短信）之前通过一次性代码验证他们的电话号码。当关闭时，在注册流程中只需勾选短信同意框就足以开始发送。出于TCPA安全原因，此默认值已更改为 **开启** —— 仅在注册流程中有其他验证步骤时才关闭它。

## 维护模式
启用维护模式以临时将您的商店下线：
- 向访客显示自定义维护消息
- 您可以链接一个 **维护页面**，在页面构建器中创建，以获得完全品牌化的维护体验
- 仅限制管理员用户的访问
- 在重大更新或迁移期间非常有用

## 社交媒体
链接您的商店的社交媒体资料。这些将出现在页脚和电子邮件模板中：

- **Facebook网址**
- **Twitter网址**
- **Instagram网址**
- **LinkedIn网址**

## SEO默认设置
保留所有markdown格式、图片路径、代码块和术语。

设置当页面没有自己的SEO设置时使用的默认元标签：

- **Meta Title** — 默认页面标题（最大60个字符）
- **Meta Description** — 默认描述，显示在搜索结果中（最大160个字符）
- **Meta Keywords** — 默认的逗号分隔关键词

## 税务设置

在 **Settings > Tax Settings** 配置税务收集：

1. **计算方法** — 按照送货地址、账单地址或商店地址
2. **税务税率** — 按照地区和产品税务类别定义税率
3. **税务显示** — 显示含税价格、不含税价格或两者都显示

## 提示

- 在处理任何订单之前正确设置时区 — 这会影响所有时间戳和报告。
- 启用访客结账以提高转化率。
- 填写您的公司地址以获得准确的运费和税务计算。
- 上传logo和favicon以获得专业、品牌化的体验。
- 使用 **After Purchase** 账户创建时机以获得最佳注册率。
- 为员工启用双因素认证以保护您的商店管理。
- 在上线前使用 **Test Redirect Email** 设置测试电子邮件流程。
- 设置 **Default Reorder Lead Time** 以匹配您最慢的常规供应商 —— 重新订购预测应用此单一值到您的整个目录，因此请以您最长交货时间的产品为优先。
- 在您的第一张真实发票发送给客户之前填写 **Tax ID / VAT Number** 和页脚文本 —— 两个字段默认为空。
- 除非您有特定原因要关闭，否则保持 **Enable Double Opt-In for Marketing Emails** 开启 —— 这是GDPR的安全默认设置，并通过将未经验证的地址从营销发送中移除来保护您的发件人声誉。
- 保持 **Default Marketing Opt-In State** 关闭。

Pre-checking marketing consent for new accounts undermines the GDPR opt-in requirement even if a customer could technically un-tick it.
- Don't disable **Enable Customer Preference Center** just to simplify your account dashboard — without it, customers can still unsubscribe from a single message type, but they lose the ability to fine-tune preferences (e.g. keep shipping updates but drop the newsletter).
- Keep **Require SMS Verification** on unless your signup flow already confirms phone numbers another way (e.g. an SMS-based login) — the setting exists specifically to keep you inside TCPA rules.

## Troubleshooting

**Changes not appearing on the storefront:**
- Clear your browser cache
- Run a cache clear from the admin panel
- Check if maintenance mode is accidentally enabled

**Emails not sending:**
- Verify your email provider settings in Email Configuration
- Check that the **Email Delivery Mode** is set to **Live**
- Ensure the **Test Redirect Email** is blank if you want emails sent to real recipients

**Currency conversion not working:**
- Verify your exchange rate provider is connected
- Check API credentials in the exchange rate settings
- Try updating rates manually

**Marketing emails aren't reaching customers who opted in:**
- Check whether **Enable Double Opt-In for Marketing Emails** is on — if so, the customer must click the confirmation link in the verification email before marketing sends resume
- Ask the customer to check spam/junk for the confirmation email
- Confirm the customer's marketing opt-in is still on in their preferences — an unsubscribe click turns it back off

**Customers say they can't find the preference center:**
- Check that **Enable Customer Preference Center** is on — when it's off, the dashboard link is hidden and the page is unavailable by design
- The unsubscribe link in any marketing email always works regardless of this setting, so point customers there as a fallback