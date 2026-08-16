---
title: 收入归因
---

收入归因会显示您的销售实际来自何处 —— 不只是客户购买前点击的最后一个链接，而是所有在获取客户过程中起到作用的渠道。如果客户在社交媒体上阅读了您分享的博客文章，一周后通过谷歌搜索返回，然后在点击电子邮件中的链接后最终购买，这三个接触点都对此次销售做出了贡献。此仪表板会根据您选择的模型对所有接触点进行归因，这样您可以以实际的营销方式而不是“最后一次点击获胜”所假定的方式来看待您的营销效果。

![收入归因仪表板：归因模型切换器、带有“与净收入一致”徽章的KPI条形、按渠道划分的收入、随时间变化的收入、客户旅程流程图以及活动表](/static/core/admin/img/help/revenue-attribution/dashboard-overview.webp)

## 如何找到它

在侧边栏中导航至 **洞察 > 收入归因**。洞察是一个专门的菜单组，位于产品上方，因此收入归因有其独立的主页，与您的订单和客户报告分开。

洞察受 **洞察与分析** 权限类别保护。如果您在侧边栏中看不到它，请让店铺管理员授予您该权限 —— 有关如何管理员工访问权限，请参阅 [员工角色与权限](/help/staff-roles)。

## 理解多触点归因

大多数商店习惯于以“这个订单来自哪里？”的方式来思考，仿佛只有一个答案。实际上，客户很少在第一次访问时就购买。他们以一种方式发现您，以另一种方式返回，以第三种方式完成购买 —— 有时是在数天或数周内多次访问。每次访问都是一个 **接触点**：记录的到达您店铺的信号，表明其来源（电子邮件链接、搜索结果、社交媒体帖子、联盟链接等）。

保留所有markdown格式、图像路径、代码块和术语。

**多-touch 原则** 意味着识别旅程中的每一次接触，并决定每一步对最终销售应得多少信用，而不是将 100% 的信用交给最后点击的渠道。

这一点很重要，因为最后点击报告系统性地低估了那些进行早期发现工作的渠道——你的博客、你的自然搜索存在感、你的社交媒体帖子——因为它们很少能在结账前成为最终点击。

## 选择归因模型

仪表板顶部的模型切换器是页面上最重要的控制选项。点击任何模型，仪表板上的每个数字——KPI 条、渠道条形图、图表、活动表——都会立即重新分配信用以匹配。这是一个实时预览：在此处切换模型会改变你查看现有销售额的方式，它不会重写任何记录或更改你商店的默认模型。

![归因模型切换器 - 最后点击、首次点击、线性、时间衰减和位置 40/20/40 - 以及 "重新归因实时 · 不重新处理" 指示](/static/core/admin/img/help/revenue-attribution/model-switcher.webp)

| Model | What it does | Best for |
|-------|---------------|----------|
| **Last touch** | Gives full credit to the last channel before the order, ignoring earlier touches (except pure "direct" visits, which are skipped in favor of the last real source) | A quick, familiar view — how most basic analytics tools report revenue |
| **First touch** | Gives full credit to whichever channel first brought the customer to your store | Understanding what's driving new customer discovery and top-of-funnel growth |
| **Linear** | Splits credit evenly across every touch in the journey | A balanced, no-opinion view when you don't want any single channel favored |
| **Time decay** | Gives more credit to touches closer to the order, less to touches further back | Campaigns with a short consideration window, where recent nudges matter most |
| **Position 40/20/40** | Gives 40% credit to the first touch, 40% to the last touch, and splits the remaining 20% across everything in between | Recognizing both "who found us" and "who closed the sale" while still crediting the middle of the journey |

There's no single "correct" model — each one answers a different question. A common approach is to check **First touch** to see what's driving discovery, then **Last touch** or **Position 40/20/40** to see what's driving conversions, and use both views together rather than picking one and ignoring the rest.

## Reading the KPI strip

Just below the model switcher, four figures summarize the selected period and model:

- **Attributed revenue** — the total revenue credited across all channels for the current model.

It carries a **Reconciles to net revenue** badge when the figures add up correctly to your store's actual net revenue for the period — in other words, the model is splitting real revenue between channels, not inventing or losing any of it.
- **Orders** — how many orders fall in the selected date range.
- **Avg. touches / order** — the average number of recorded touches per order.

一个数字大于1表明你的大多数客户旅程涉及多次访问，这正是为什么多触点归因对你的商店如此重要的原因。
- **主导渠道** —— 在所选模型下，当前拥有最大归属销售额的渠道，以及其占比和销售额。

## 按渠道划分的销售额

**按渠道划分的销售额** 仪表板为每个渠道显示一个水平条形图，其大小由归属的销售额决定。切换归因模型，并观察条形图按排名平滑重新排序 —— 这是相同的底层销售额，只是根据不同的规则重新分配，因此一个渠道在 **最后点击** 模式下看起来表现强劲，可能在 **首次点击** 模式下排名大幅下降，如果它主要扮演辅助角色的话。

## 销售额随时间的变化

**销售额随时间的变化** 图表按渠道在所选时间范围内每天的归属销售额进行堆叠，因此你可以不仅看到每个渠道的价值，还能看到其贡献的时间。你可以用它来发现季节性模式，确认广告活动的影响是否落在你预期的日期，或者检查某个渠道在该时间段内的贡献是否增长或减少。

## 客户实际到达的方式

**客户实际到达的方式** 面板 是一个流程图，连接首次带来客户的渠道（左侧）和转化时的渠道（右侧）。较粗的带状图表示通过该路径的销售额更多。这是快速查看多步骤旅程的最清晰方式 —— 例如，从自然搜索到电子邮件的粗带状图表明搜索带来了访客，但你的电子邮件营销才是促使他们购买的原因。

![选择影响透镜时的客户旅程流程图，显示左侧的首次点击渠道流向每个订单转化的渠道](/static/core/admin/img/help/revenue-attribution/journey-flow-sankey.webp)

在图表上方使用 **归属** / **影响** 切换按钮来切换透镜：

- **Attributed** 将每个订单的收入分配到您所选的模型中，因此总计为 100% 的归因收入 —— 与仪表板上的其他地方显示的数字相同。
- **Influenced** 会为每个接触过订单的渠道分配该订单的*全部*价值，每个订单只计算一次。

此功能故意不总计为 100% —— 一个渠道可能被计入其他渠道的全部收入。

它用于揭示最后点击报告完全隐藏的渠道影响力，例如一篇博客文章或社交媒体分享，这些内容可能让某人产生兴趣，即使他们在最终访问时没有点击它。

## Campaigns

**Campaigns** 表格将每个标记的活动的收入、订单和平均订单价值（AOV）分解出来 —— 链接或代码，您已用活动名称标记，包括活动标记的优惠券代码（参见 [优惠券活动创意](/help/voucher-campaign-ideas)）。可用于比较各个促销活动、影响者代码或营销活动的表现，无论它们是由哪个渠道带来的。

## 日期范围和导出您的数据

使用右上角的日期范围选择器在 **Last 7 days**（最近 7 天）、**Last 14 days**（最近 14 天）、**Last 30 days**（最近 30 天）、**Last 90 days**（最近 90 天）和 **Month to date**（本月至今）之间切换。整个仪表板将根据新时间段刷新。

点击 **Export CSV** 以下载当前所选模型和日期范围的渠道分解数据 —— 对于将数字导入电子表格或与合作伙伴机构共享非常有用。

## 如何记录触点

当访客携带可识别的来源信号到达您的商店时，Spwig 会自动记录一次触点，并且仅当访客在您商店的 cookie 通知中给予 **Analytics** 同意（如果您不使用通知栏，跟踪默认开启，根据您商店的隐私政策）。
此设置确保收入归因与您店铺其他分析部分的隐私标准保持一致。


Several sources are tagged automatically, with no setup required:

| Channel | How it's identified |
|---------|----------------------|
| **Email** | Links in your marketing emails (not order or shipping emails) |
| **Organic / Paid Search** | Search engine referrers, or `utm_medium` values marking a paid search campaign |
| **Organic / Paid Social** | Social network referrers, or social `utm_medium` values |
| **Affiliate** | Links generated through your Affiliate program |
| **Refer a Friend** | Links generated through your customer referral program |
| **Campaign** | Any link or code carrying a campaign tag, including campaign-tagged voucher codes |
| **External Link** | An inbound link from another website that isn't otherwise categorized |
| **Direct** | No source signal was present — the visitor typed your address, used a bookmark, or arrived from an app with no referrer |

Blog posts that were auto-shared to your connected social accounts are automatically tagged, so traffic they generate shows up under the right social channel rather than being lost to Direct or External Link.

You can also tag your own links by hand using standard `utm_source`, `utm_medium`, and `utm_campaign` parameters on any URL pointing at your store — useful for print materials, partner newsletters, or any channel Spwig doesn't auto-tag.

## Limitations to keep in mind

- **Attribution follows a browser, not a person.** If a customer researches on their phone and buys on their laptop, those are two separate journeys as far as tracking is concerned — there's no way to link activity across different devices.

这意味着一些本应归因于另一台设备上的早期触点的信用将归入直接流量。
- **直接流量是未追踪流量的归宿。** 直接流量占比高并不一定意味着人们是从记忆中输入你的网址——也可能是客户在其他设备上进行了早期触点，或者他们使用的链接未被标记。
- **拒绝同意意味着不记录任何触点。** 在你的 Cookie 通知中拒绝分析权限的访客不会被追踪，因此他们的订单即使通过你通常能识别的渠道到达，也会显示为直接流量。

## 技巧

- 在得出结论之前，请检查多个模型 —— 一个在 **最后点击** 下看起来较弱的渠道，在 **首次点击** 下可能成为你最强的发现驱动。
- 如果 **直接流量** 占据了你收入的很大一部分，查看你的营销链接是否可以更多地使用 `utm_source`/`utm_medium`/`utm_campaign` 标签 —— 未标记的流量没有其他地方可去。
- 在决定是否继续投资于有机搜索或博客内容等渠道时，使用旅程流程图上的 **影响** 视角，这些渠道很少获得最后点击，但持续启动旅程。
- 随着时间的推移，比较 **平均触点/订单** —— 数字上升通常意味着客户做出决定的时间更长，这是规划跟进电子邮件或再营销时间的重要信号。
- 在你再次切换模型之前，导出你正在报告的模型和时间段的 CSV 文件，因为导出的内容反映的是你点击 **导出 CSV** 时所选的模型。