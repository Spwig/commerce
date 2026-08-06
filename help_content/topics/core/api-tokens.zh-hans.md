---
title: API令牌
---

API令牌是安全密钥，允许外部服务和集成与您的商店进行通信。当第三方服务或工具需要访问您的商店数据或触发操作时，它会在每次请求中发送一个API令牌，以便您的商店可以验证请求是否已授权。您可以在管理后台的API令牌部分创建和管理所有令牌，包括它们可以访问的商店具体部分。

## 您需要API令牌的情况

您通常需要创建API令牌的情况包括：

- 连接需要读取或写入您商店数据的外部服务或自动化工具
- 设置需要验证传入调用的Webhook接收器
- 为您的安装配置Spwig帮助系统
- 使用Spwig API构建自定义集成
- 在您的Spwig商店和其他系统之间同步数据

每个集成应使用自己的令牌，这样您可以撤销一个服务的访问权限而不影响其他服务。

## 令牌类型

创建令牌时，您选择一个类型来描述其用途。该类型仅供您参考，有助于您跟踪每个令牌的作用。

| 类型 | 用途 |
|------|---------|
| **帮助系统** | 用于Spwig帮助文档系统 |
| **外部集成** | 第三方服务、自动化工具（例如Zapier）或数据同步工具 |
| **Webhook** | Webhook接收器或端点的认证 |
| **自定义** | 任何不属于上述类别的其他用途 |
| **实例同步** | Spwig安装或外部Spwig服务之间的同步 |

## API作用域：控制令牌可以访问的内容

每个令牌还有一个**API作用域**部分，用于决定它确切可以调用商店的哪些部分。而不是让令牌对所有内容都有完全访问权限，您可以一次一个区域地授予访问权限，并且仅在集成实际需要的层级上进行授权。

**未选择任何作用域的令牌无法访问任何API**，即使它本身处于活动且有效状态。

这是新令牌的默认设置，因此在您有意授予其访问权限之前，集成将无法工作。

对于每个作用域，您可以选择以下三种访问级别之一：

| 访问级别 | 允许的操作 |
|----------|------------|
| **无访问权限** | 该令牌无法调用此区域的任何端点 |
| **只读** | 该令牌可以从该区域检索数据，但不能进行任何更改 |
| **读写** | 该令牌可以检索数据，并且可以创建、更新或删除数据 |

作用域按您的管理区域进行分组：

| 组 | 作用域 | 是否有读写权限？ | 授予访问权限的区域 |
|----|-------|:---:|-------------------|
| 分析 | **销售分析** | 仅读 | 销售仪表板、KPI、产品/客户/分类分析、比较和导出 |
| 分析 | **网站分析** | 仅读 | 访客和流量分析：概览、趋势、热门页面、地理和来源 |
| 目录 | **产品** | 是 | 产品、变体、图片、库存调整和属性分配 |
| 目录 | **分类** | 是 | 产品分类，包括图片和横幅 |
| 目录 | **品牌** | 是 | 产品品牌 |
| 目录 | **属性** | 是 | 产品属性定义 |
| 目录 | **库存** | 是 | 库存仪表板、库存速度、变动、补货建议和库存设置 |
| 订单 | **订单** | 是 | 订单、订单备注、状态/跟踪更新、取消、退款和订单文档 |
| 客户 | **客户消息** | 是 | 来自联系表单和订单备注的客户消息，包括状态更新和回复 |
| 商店与设置 | **商店设置** | 是 | 商店设置、可用语言和品牌（名称、颜色、标志） |
| 用户与访问 | **员工与角色** | 是 | 员工账户、邀请、角色和权限目录 |

这两个 **分析** 作用域始终是只读的 —— 报告数据没有“写入”概念，因此选择器只提供 **无访问权限** 或 **只读** 选项。

[![API作用域选择器，Analytics和Catalog作用域组上方有一个访问说明](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)](https://example.com)

在作用域选择器下方，一个只读的**"此令牌可以访问："**摘要列出了您授予的所有作用域及其级别，因此您可以快速查看令牌的访问权限，而无需解码选择器。

[!["此令牌可以访问"摘要列出每个已授予的作用域及其读取或读取和写入级别](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)](https://example.com)

### 令牌实际使用的权限

令牌的作用域描述了它所能执行操作的*上限*——但令牌还会继承创建它的员工的实际权限：

- 即使创建令牌的员工是超级用户，令牌也无法以**超级用户**权限执行操作。
- 如果创建员工的角色也允许对某个区域进行写入访问，那么作用域上的**读取和写入**才有效。如果他们的角色仅允许查看，比如产品，那么他们创建的带有"产品：读取和写入"的令牌仍然只能读取——角色会作为作用域的第二道门。
- 如果创建令牌的员工被删除，或者其账户被停用，无论令牌的作用域如何，令牌会立即失去API访问权限——因为不再有允许其作为用户的用户。

这意味着，最安全的方法是创建一个令牌时，以一个其角色已经与令牌所需访问权限相匹配的员工身份登录。

## 创建API令牌

1.

导航到 **设置 > API令牌**
2.

点击 **+ 添加API令牌**
3.

输入一个 **名称**，明确描述令牌的用途（例如，`Zapier产品同步` 或 `帮助系统API`）
4.

选择适当的 **令牌类型**
5.

可选地添加 **描述**，提供更多关于集成的详细信息
6.

在 **API作用域** 中，为集成所需的每个区域选择 **无访问权限**、**读取** 或 **读取和写入**——将其他所有作用域保留为 **无访问权限**
7.

保留所有Markdown格式、图片路径、代码块和技术术语。

配置 **Active** 状态、**Expiry Date** 和 **Allowed IPs**（见下文）
8.

点击 **Save**

保存后，完整令牌值会显示在详情页面上。**请立即复制** —— 为了安全起见，列表视图中令牌会被遮蔽，离开此页面后无法再次获取完整令牌。

![API Token Detail](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Token value security

Spwig 仅在您保存新令牌后立即显示完整的令牌值。之后，列表视图中只会显示一个遮蔽版本（例如，`spw_••••••••••••••••••••3f8a`）。

如果您丢失了令牌值，将无法恢复。您需要删除旧令牌并创建一个新令牌，然后更新使用该令牌的集成。

**切勿通过电子邮件、聊天消息或源代码共享令牌值。** 请将它们视为密码。

## Setting an expiry date

**Expires At** 字段设置一个日期和时间，之后令牌将自动停止工作。如果令牌不应过期，请留空此字段。

过期日期适用于以下情况：

- 有固定结束日期的临时集成
- 提供给第三方的令牌，您希望自动移除访问权限
- 为高权限集成添加额外的安全层

当令牌过期后，使用它的请求将被拒绝。您可以通过更新 **Expires At** 日期或创建一个替代令牌来延长访问权限。

## Restricting to specific IP addresses

**Allowed IPs** 字段接受一个 IP 地址列表。当列表不为空时，令牌仅在请求来自这些地址之一时才有效。

例如，如果您的分析工具运行在 `203.0.113.42` 的服务器上，添加该 IP 地址意味着即使令牌泄露，也无法从其他位置滥用该令牌。

将 **Allowed IPs** 留空以允许来自任何 IP 地址的请求。

**Expiry and IP restrictions are checked independently of scopes.** An expired or off-allowlist token is rejected before its scopes are even considered, and a token with generous scopes is still rejected the moment it expires or is called from an unlisted IP.

## Calling the API with a token

Integrations authenticate to Spwig's admin API by sending the token in an `Authorization` header:

```
Authorization: Bearer <your-token-value>
```

Every admin API endpoint lives under `/api/admin/...`. The developer building your integration decides which endpoints to call — your job as the merchant is to make sure the token's **API Scopes** cover those endpoints. If a request is rejected with a permissions error, the first thing to check is whether the token has been granted the right scope at the right access level.

### Example: reading web traffic analytics

Spwig exposes a `GET /api/admin/analytics/traffic/` endpoint that returns visitor and traffic analytics for your store — an overview of visits and unique visitors, trends over time, top pages, visitor geography, and referrer sources. To let a reporting tool or dashboard read this data:

1. Create a token (or edit an existing one) for that integration
2. In **API Scopes**, set **Web Analytics** to **Read**
3. Save the token and provide it to the integration

Because **Web Analytics** is a read-only scope, there is no "Read & Write" option to choose — the integration can only retrieve analytics data, never change your store's configuration.

## Monitoring token usage

The token list shows:

- **Usage Count** — total number of times the token has been used
- **Last Used** — when the token was last used to make a request

These fields help you identify unused tokens (candidates for revocation) and spot unexpected activity. A sudden spike in usage count may indicate a token is being used by someone other than the intended integration.

## Revoking a token

To immediately stop a token from working without deleting it:

1.

点击令牌名称
2.

取消勾选 **Active**
3.

保存

该令牌仍保留在您的列表中供参考，但会在后续任何请求中被拒绝。当您需要临时暂停某个集成以调查问题时，这非常有用。

要永久删除令牌：

1. 在列表中选择其复选框
2. 从操作菜单中选择 **Delete selected API tokens**
3. 确认删除

一旦删除，令牌无法恢复。如果该集成仍需要访问权限，请创建一个新令牌并更新集成的配置。

## 示例：设置 Zapier 集成

**场景：** 您希望将商店连接到 Zapier 以自动化订单通知。

| Field | Value |
|-------|-------|
| Name | `Zapier Order Automation` |
| Token Type | External Integration |
| Description | Used by Zapier to read new orders and trigger notifications |
| API Scopes | **Orders**: Read & Write |
| Active | Yes |
| Expires At | *(leave blank)* |
| Allowed IPs | *(leave blank — Zapier uses dynamic IPs)* |

仅授予 **Orders** 范围，因此即使此令牌被泄露，也无法访问产品、客户消息、员工账户或商店的其他部分。保存后，复制完整的令牌值并粘贴到 Zapier 的 Spwig 集成设置中。

## Tips

保留所有 markdown 格式、图片路径、代码块和专业术语。

- 为每个令牌赋予清晰且具体的名称 —— 在数月后排查问题时，`Shopify Sync v2` 比 `Token 3` 要有用得多
- 每个集成创建一个令牌 —— 如果某个集成被入侵，你可以仅撤销该令牌，而不会影响其他令牌
- **仅授予集成实际需要的权限范围** —— 报告工具只需对销售分析或网络分析具有读取权限，而不需要对产品或员工与角色具有读写权限
- 在将令牌交给第三方之前，检查更改表单上的 **"此令牌可以访问："** 概要 —— 这是确认你是否意外授予了过多权限的最快方式
- 请记住，写入权限还取决于创建员工自身的角色 —— 如果某个权限范围显示为读写，但写入仍然失败，请同时检查该用户的角色权限
- 为用于一次性项目或临时集成的令牌设置到期日期 —— 这可以降低被遗忘的令牌无限期保持活动状态的风险
- 每隔几个月查看一次你的令牌列表，停用任何 **最后使用** 日期异常陈旧的令牌，因为这些可能属于不再运行的集成
- 如果你怀疑某个令牌已被泄露，请立即停用它，创建一个替代令牌，并在重新启用访问权限之前更新受影响的集成