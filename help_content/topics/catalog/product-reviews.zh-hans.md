---
title: 产品评价
---

产品评价让客户可以对他们在产品上的体验进行评分和撰写评论。您审核通过的评价会显示在您的商店产品页面上，帮助其他购物者决定购买什么。Spwig为您提供完全的控制权，决定哪些评价可以发布——在您审核之前，没有任何内容会被发布。

评价位于侧边栏的 **产品 > 评价** 下方，展开后会显示一组链接：顶部链接带您到 **评价仪表板**，而 **管理评价** 则直接带您到评价列表。

## 评价仪表板

导航到 **产品 > 评价** 以打开仪表板——这是您商店中评价表现的单屏概览。

![评价仪表板](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

在顶部，六个KPI卡片总结了您的评价活动：

| 卡片 | 显示内容 |
|---|---|
| **总评价** | 所有已提交的评价，无论是否被批准 |
| **平均评分** | 每个评价的平均星级 |
| **待审核** | 等待您批准或拒绝的评价 |
| **批准率** | 您已批准的所有评价的比例 |
| **已验证的购买** | 由确认购买该产品的客户留下的评价的比例 |
| **最近（30天）** | 最近30天内提交的评价 |

在KPI下方，有三个图表提供了更多细节：

- **评分分布** —— 某个星级评分（1-5）的评价数量的柱状图。

此处1星评价的聚集需要立即调查。
- **评价数量（12周）** —— 每周评价数量的折线图，让您能够识别促销后的峰值或需要关注的下降趋势。
- **评价者的购买渠道** —— 一个环形图，显示驱动每个评价背后购买行为的营销渠道（直接、电子邮件、付费搜索、自然社交等）。

保留所有markdown格式、图片路径、代码块和术语。

This reuses your attribution data and is genuinely useful for seeing which channels bring in customers who go on to leave reviews — but it is **not** a record of how the customer found the review form itself.

Spwig doesn't track that separately; see "What the journey does and doesn't tell you" further down this guide.

Two lists round out the dashboard:

- **Top Reviewed Products** — your most-reviewed products, each with its review count and average rating, linking straight to the product.
- **Awaiting Moderation** — your most recent pending reviews, so you can jump directly into anything that needs a decision without leaving the dashboard.

## The review list

Click **Moderate Reviews** (or **Products > Reviews > Moderate Reviews**) to see every review as a card, with filters above the list.

![Product Reviews list with filters and pending review cards](/static/core/admin/img/help/product-reviews/review-list.webp)

Each card shows the product thumbnail, review title, star rating, an **Approved**/**Pending** badge, a **Verified Purchase** badge when it applies, a preview of the comment, and who wrote it and when.

### Filtering reviews

Use the filters panel to narrow the list:

- **Search** — matches product name, customer username, or review title
- **Rating** — show only reviews with a specific star rating (useful for investigating 1-star complaints)
- **Approval** — quickly separate approved from pending reviews
- **Verified** — filter to reviews from customers with a confirmed order for that product

Filtering runs instantly without reloading the page.

## Approving and rejecting reviews

Reviews are not visible on your storefront until you approve them. You can approve or reject reviews individually or in bulk.

### Bulk actions

1. In the review list, tick the checkboxes next to the reviews you want to act on
2. Select **Approve selected reviews** or **Reject selected reviews** from the action dropdown
3. Click **Go**

这是处理一批新评论的最快方法。

### 单个评论

1. 点击评论卡片上的编辑图标，或其标题，以打开评论
2. 在 **评论** 选项卡中，勾选或取消勾选 **已批准**
3. 点击标题栏中的复选标记按钮以保存

## 评论编辑页面

打开评论会显示一个以该评论为中心的仪表板式视图 —— 标题栏中包含产品名称、星级评分、**已批准**/**待审核** 标签、当适用时的 **已验证购买** 标签、评论者及其评论时间，以及一个统计行（**评分**、**有用投票**、**客户订单**、**终身消费**）。在此之下，详情被组织成四个选项卡。

![评论编辑页面 —— 评论选项卡中的图片库](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### 评论选项卡

这是您审核评论本身的地方：

- **评论图片** —— 如果客户附加了照片，它们会以缩略图画廊的形式显示在这里；点击任何缩略图可在新标签页中打开全尺寸图片。图片评论是购物者的重要信任信号，因此在批准之前值得看一下。
- **评分**、**标题**、**评论** —— 客户提交的内容
- **已批准** —— 控制评论是否在您的商店前台显示
- **已验证购买** —— 标记该评论为来自确认买家；当存在该产品的已履行订单时，Spwig会自动设置此选项（参见 **购买** 选项卡），但您可以在需要时在此覆盖它
- **图片** —— 上面画廊中图片URL的底层列表；您通常不需要修改此内容，但为了特殊情况（例如，从多图评论中删除一张图片）仍保持可编辑

您无法编辑评论的措辞 —— 批准或拒绝，以及管理图片，是您在此处能控制的全部内容。

### 客户与旅程选项卡

![评论编辑页面 —— 客户与旅程选项卡](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

此选项卡为您提供留下该评价的客户背景信息：总订单数、已撰写的评价数量、其给出的平均评分、成为客户的时间长度，以及其联系方式，并附有链接以打开其完整的客户记录。

下方是**流量来源旅程**——展示将这位客户引导至您商店的渠道、广告活动和推荐来源，数据取自您的归因数据，并以时间线形式呈现。

#### “旅程”能告诉您什么，不能告诉您什么

请将此时间线视为客户的**到达与购买旅程**——他们最初如何发现您的商店并进而完成购买。它**并非**记录他们撰写此评价的那次访问。Spwig 不会追踪客户提交评价时所在的地理位置，或他们使用的设备或会话。如果时间线显示在评价日期前三周有“Email > summer-skincare”，这表明电子邮件营销活动很可能促成了*购买*——但它并未说明客户是搜索结果、书签还是后续电子邮件返回来实际留下评价的。请将此选项卡视为有用的营销背景信息，而非评价提交的直接追踪记录。

### 购买选项卡

![评价编辑页面 — 购买选项卡](/static/core/admin/img/help/product-reviews/review-edit-purchase-tab.webp)

此选项卡列出了客户购买所评价产品的所有订单——订单号、日期、总额、状态以及该订单的购买渠道。如果其中任何订单已达到已履行状态（已发货或已送达），您将看到一条确认说明，表明这是一次已验证的购买——这与在评价选项卡上自动设置**是否为已验证购买**的信号相同。

如果此处未显示匹配的订单，则评价者要么是在您的商店在 Spwig 中开始追踪订单之前购买了该产品，要么他们实际上从未购买过该产品——在决定给予该评价多大权重之前，了解这一点很有价值。

### 高级选项卡

元数据你很少需要修改：**有用数**（多少位客户标记该评论为有用），如果该评论是从其他平台迁移过来的，则显示导入来源，以及创建/更新时间戳。

## 技巧

- 首先在仪表板上检查 **待审核** 列表 —— 这是查看需要决策的内容的最快方式，而无需打开完整的评论列表
- **评分分布** 图表中同一产品出现的一堆 1 星评论是需要调查包装、产品质量或您的商品描述的明确信号
- 在决定如何处理边缘案例评论时，使用 **已验证** 筛选器 —— 来自已确认订单的客户反馈在任何争议中都更具说服力
- 及时批准评论，包括负面评论 —— 可见的负面评论如果没有回应，可能比处理过的投诉看起来更糟糕，而出现缓慢的评论会阻止客户留下未来的反馈
- 不要过度解读 **流量来源旅程** 或仪表板的 **评论者购买渠道** 图表 —— 两者都描述了客户是如何到达并购买的，而不是他们是如何到达来撰写评论的
- 在批准之前，仔细查看带有图片的评论；来自真实客户的商品图片是您店铺中最具说服力的内容之一