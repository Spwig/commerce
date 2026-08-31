---
title: 配置商店设置
---

商店设置是配置商店身份、本地化、品牌和操作首选项的中心位置。导航到 **设置 > 商店设置** 开始。

![商店设置常规选项卡](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## 常规选项卡

**常规** 选项卡包含商店的核心身份设置。

### 商店身份

- **商店名称** — 在页面标题、电子邮件和管理面板标题栏中显示的名称。
- **标语** — 商店的简短描述，用于SEO和社交媒体分享。
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

上传商店标志（推荐PNG或SVG，约200x50像素，透明背景）。标志将出现在：
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

![Inventory Intelligence card showing Default Reorder Lead Time, Safety Stock Multiplier, Velocity Calculation Window, Allow Backorders by Default, and Low Stock Alert Frequency fields](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

These settings tune the automatic reorder, safety-stock, and sales-velocity calculations, and control how out-of-stock and low-stock situations are handled.

- **Default Reorder Lead Time (Days)** — How many days it typically takes to receive restock from your supplier once you place an order (default: 14).

Forecasting uses this to flag products that need reordering *now* to avoid a stockout before the new stock arrives.
- **Safety Stock Multiplier** — A buffer applied on top of expected demand to absorb sales spikes or supplier delays.

For example, a multiplier of `1.5` builds in a 50% buffer above your calculated safety stock; `2.0` doubles it.

Raise this for products where running out is costly (best sellers, seasonal items); lower it for slow-moving stock you don't want to over-order.
- **Velocity Calculation Window (Days)** — The look-back window Spwig uses to calculate each product's sales velocity, which in turn drives reorder suggestions and days-of-supply figures (default: 30).

A shorter window reacts faster to recent demand shifts; a longer window smooths out seasonal spikes so a single busy week doesn't skew the forecast.
- **Allow Backorders by Default** — The initial backorder setting applied to newly created products (off by default).

Each product can still override it individually on its own product page, and existing products keep whatever setting they already have — changing this only changes the default new products start with, it does not retroactively update your catalog.
- **Low Stock Alert Frequency** — How often your Spwig mobile app is notified about low stock: **Real-time** sends a push notification the moment a product crosses its low-stock threshold; **Daily Digest** and **Weekly Summary** instead send a single push summarizing all currently low-stock products on that schedule.

This setting only takes effect while **Low Stock Alerts** (Email Settings, below) is enabled — with alerts off, no notifications go out on any frequency.

### Documents & Invoicing

![Documents & Invoicing card showing Tax ID / VAT Number, Invoice Footer Text, Packing Slip Footer Text, and Document Logo Width fields filled in with example values](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

这些字段会填充Spwig为订单生成的发票和装箱单 —— 例如当商家下载或通过电子邮件发送PDF发票，或者为发货打印装箱单时。

- **税号 / VAT号码** —— 您企业的税务识别号码。在生成的发票上打印，以满足当地的税务文件要求。
- **发票页脚文字** —— 显示在每个生成的发票底部的自由文本。常见用途：付款条款（"30天内付款"）、感谢信息或银行转账详情。
- **装箱单页脚文字** —— 显示在每个生成的装箱单底部的自由文本。常见用途：退换货说明或给仓库/履约团队的备注。
- **文档Logo宽度（像素）** —— 您的商店Logo在生成的PDF发票和装箱单中的宽度（默认：200像素）。高度会自动按比例缩放，以保持您的Logo的宽高比。Logo图片本身来自您的 **Logo**（品牌，见上文） —— SVG格式的Logo不会在PDF文档中绘制，因此如果您在店铺前端使用矢量图形，请上传PNG或JPG格式的Logo版本。

## 邮件设置

在 **设置 > 邮件账户** 和 **设置 > 邮件模板** 中配置邮件发送设置。详见 [邮件配置](/help/email-configuration) 以获取完整细节。

在商店设置中可用的关键邮件设置包括：

- **订单确认邮件** —— 打开或关闭自动确认邮件
- **发货通知邮件** —— 打开或关闭发货更新通知
- **库存不足警报** —— 当库存低于阈值时向管理员邮箱发送警报
- **邮件发送模式** —— 实时（正常发送）、暂停（暂停所有邮件）或仅记录（仅记录但不发送）
- **测试邮件转发地址** —— 所有出站邮件转发到一个地址以进行测试

## 安全设置

### 双因素认证（2FA）

控制员工是否需要使用双因素认证：

保留所有markdown格式、图片路径、代码块和专业技术术语。

| 设置 | 描述 |
|---------|-------------|
| **可选** | 员工可以选择启用 2FA，但并非强制要求 |
| **推荐** | 员工会看到提示，鼓励他们设置 2FA |
| **必需** | 在启用 2FA 之前，员工无法访问管理后台 |

- **宽限期（天）** — 在强制启用后，员工有多少天时间来设置 2FA
- **允许受信任设备** — 允许员工在受识别的设备上跳过 2FA 验证，持续设定的天数

## Cookie 同意

配置向店面访客显示的 Cookie 同意横幅：

- **启用 Cookie 同意** — 显示或隐藏 Cookie 横幅
- **横幅位置** — 横幅在屏幕上的显示位置（底部栏、角落弹窗等）
- **同意模式** — 简单通知、选择加入或选择退出
- **横幅标题和文本** — 向访客显示的自定义标题和描述
- **类别描述** — 针对分析、营销和功能 Cookie 的单独描述

所有横幅文本字段均支持多语言商店的翻译。

## 通信

**通信** 选项卡控制您的商店如何获取、确认并让客户管理营销电子邮件和短信的同意。这些设置决定了您的法律合规状态（电子邮件适用 GDPR，短信适用 TCPA），因此在上线前请与您的法律顾问一起审查——Spwig 提供控制功能，而非法律建议。

![显示电子邮件营销同意、偏好设置与退订以及短信同意卡片的通信选项卡](/static/core/admin/img/help/store-settings/communications-tab.webp)

### 电子邮件营销同意

- **为营销电子邮件启用双重确认** — 开启后，选择加入营销电子邮件的客户会收到一封确认邮件，并且必须点击其中的链接，Spwig 才会向他们发送任何营销信息。

关闭时，仅勾选营销选择加入框即可。


默认启用，符合GDPR最佳实践。
- **默认营销订阅状态** — 新创建的客户帐户的初始营销订阅状态。

默认关闭（GDPR选择退出），因此新客户在主动订阅之前不会接收营销电子邮件。

当启用双重确认时，订阅会触发带有验证链接的确认电子邮件。在客户点击该链接之前，他们会被记录为已订阅但未确认，而营销邮件将跳过他们 —— 交易性邮件（订单确认、发货更新、密码重置）从不受此设置影响。

### 首选设置与退订

- **启用客户首选设置中心** — 当启用时，客户可以从其帐户仪表板链接的自助服务页面管理他们的电子邮件和短信首选设置。当关闭时，该页面及其支持的API返回不可用，仪表板链接将被隐藏。无论哪种方式，电子邮件中的一键退订链接仍能正常工作 —— 这是一个合规性逃生舱口，不受此切换影响。
- **收集退订原因** — 当启用时，一键退订页面会在确认前向客户询问简短的原因：*我收到太多电子邮件*, *内容与我不相关*, *我从未注册过*, *我不再感兴趣*, 或 *其他*。客户选择的原因会被记录到同意审计跟踪中，以便您随时间审查退订模式。

### 短信同意

- **需要短信验证** — 当启用时（默认），客户必须在Spwig向他们发送任何短信（包括营销短信）之前通过一次性代码验证他们的电话号码。当关闭时，在注册流程中如果客户勾选短信订阅框就足以开始发送短信。出于TCPA安全原因，此默认值已更改为**启用** —— 仅在注册流程中有其他验证步骤时才关闭此功能。

## 维护模式

保留所有markdown格式、图片路径、代码块和术语。

启用维护模式将您的商店暂时下线：
- 向访客显示自定义的维护信息
- 您可以链接一个在页面构建器中创建的 **维护页面**，以获得完全品牌化的维护体验
- 仅限制管理员用户访问
- 在重大更新或迁移期间非常有用

## 社交媒体

链接您的商店的社交媒体资料。这些将显示在页脚和电子邮件模板中：

- **Facebook URL**
- **Twitter URL**
- **Instagram URL**
- **LinkedIn URL**

## SEO 默认设置

设置当页面没有自己的 SEO 设置时使用的默认元标签：

- **元标题** — 默认页面标题（最大 60 个字符）
- **元描述** — 默认描述，显示在搜索结果中（最大 160 个字符）
- **元关键词** — 默认的逗号分隔关键词

## 税收设置

在 **Settings > Tax Settings** 配置税收收集：

1. **计算方法** — 按照送货地址、账单地址或商店位置
2. **税收率** — 按照地区和产品税收类别定义税率
3. **税收显示** — 显示含税价格、不含税价格或两者都显示

## 提示

保留所有 markdown 格式、图片路径、代码块和术语。

- 在处理任何订单之前，请正确设置时区——它会影响所有时间戳和报告。
- 启用访客结账以提高转化率。
- 填写您的营业地址，以便准确计算运费和税费。
- 同时上传标志（Logo）和网站图标（favicon），以提供专业且具品牌特色的体验。
- 使用**购买后**账户创建时机，以获得最佳的注册率。
- 为工作人员启用双因素身份验证强制策略，以保护您的商店后台。
- 在正式上线之前，使用**测试重定向邮件**设置测试邮件流程。
- 将**默认补货提前期**设置为与您最慢的常规供应商相匹配——补货预测在整个目录中应用此单一值，因此请倾向于选择提前期最长的产品。
- 如果您经常进行促销或补货，并希望预测能快速响应最近几天的销售情况，请缩短**速度计算窗口**；如果您希望获得更稳定、不易出现峰值的需求视图，请延长该窗口。
- 如果您开启**默认允许缺货**，请记住它仅作为在更改*之后*创建的产品起点——如果您希望当前目录中的现有产品也启用缺货功能，请单独重新检查这些产品。
- 将**低库存警报频率**与您管理库存的活跃程度相匹配：对于快速流转的目录，其中每个缺货风险都需要立即关注，请选择**实时**；对于较大的目录，为避免警报疲劳，请选择**每日摘要**或**每周汇总**。
- 在您的第一张真实发票发送给客户之前，请填写您的**税号 / 增值税号**和页脚文本——这两个字段默认均为空白。
- 如果您的**标志**是 SVG 格式，请同时上传 PNG 或 JPG 版本——**文档标志宽度**对 PDF 没有影响，因为 Spwig 无法在生成的发票和装箱单上绘制 SVG 图形。
- 除非有特定原因需要关闭，否则请保持**为营销邮件启用双重确认**开启——它是 GDPR 下更安全的默认设置，并且通过将未验证的地址排除在营销发送之外来保护您的发件人声誉。
- 保持**默认营销订阅状态**关闭。

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