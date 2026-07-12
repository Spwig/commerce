---
title: Spwig 托管服务
---

Spwig 包含三种可选的云服务，您的商店可以使用这些服务，而无需您自行配置或托管任何内容：**GeoIP** 可检测访客所在的位置，**Geocoder** 可将客户地址转换为地图坐标，**Push** 可向您的移动 Spwig 管理员应用发送即时通知。在社区（免费）版中，每项服务都附带了充足的每月配额。当任何服务接近其限制时，Spwig 会在管理后台提醒您，以便您决定是否在客户察觉之前升级服务。

## 三项托管服务

### GeoIP — 访客国家检测

GeoIP 根据访客的 IP 地址查找其所在国家。您的商店使用此信息在客户访问时自动显示正确的货币，并在结账时预先填写国家字段。例如，来自德国的访客将看到以欧元显示的价格，而来自日本的访客将看到以日元显示的价格，无需手动选择。

每次运行 GeoIP 查询的页面加载都会计入您的每月配额。同一浏览器会话中的重复访问不会每次消耗一次查询；结果会在会话中缓存。GeoIP 查询仅在商店前端发生，不会在您的管理面板中发生。

### Geocoder — 地址转坐标

Geocoder 将客户输入的地址转换为地理坐标（纬度和经度）。您的商店使用这些坐标用于两个目的：当您有自提点或基于半径的运费规则时，用于计算基于距离的运费，以及在结账页面上提供地址自动补全建议，以便客户快速找到自己的地址。

当客户在结账时选择或确认地址时，会触发一次 Geocoder 查询。与 GeoIP 一样，结果会被缓存，因此同一地址在每个会话中只会查询一次。

### Push — 管理员应用通知

Push 会将实时通知发送到您的 Spwig 商家移动应用。

当有新订单到达、库存低于阈值或客户发送消息时，Push 会立即向您的设备发送通知，这样您无需一直保持管理面板打开即可进行响应。

发送到您设备的每条通知都会消耗您每月配额中的一次推送请求。

## 社区版免费层级

在 Spwig 的社区版中，每项服务在每月请求限制内都是免费提供的。具体的限制由 Spwig 设置，可能会有所变化；您的管理员仪表板始终会显示您当前安装的最新数据。付费计划（入门版、成长版、专业版、专业增强版）以及拥有付费许可证的自托管安装，每项服务的限制更高。

当某项服务达到其社区版配额的 100% 时，对该服务的请求将停止，直到下一个月重新计算计数器。对您的商店的影响取决于受影响的服务：

| 服务 | 达到 100% 时发生的情况 |
|---------|----------------------|
| GeoIP | 货币自动检测将回退到您商店的默认货币。客户仍然可以手动更改货币。 |
| 地理编码器 | 地址自动补全将不再提供建议。客户仍然可以手动输入地址。运费计算将继续使用最后已知的坐标。 |
| Push | 新的管理应用通知将被排队，但直到下个月或升级后才会发送。 |

在所有情况下，您的商店仍能正常运行——不会丢失订单，客户仍然可以结账。这些影响仅限于便利功能。

## 阅读仪表板瓷砖

**Spwig 服务使用情况**瓷砖会显示在您的管理员仪表板首页上。它为三项服务中的每一项都显示一个进度条。

瓷砖中的每一行都遵循相同的布局：

- **服务名称**（左侧）——GeoIP、地址查找（地理编码器）或推送通知。
- **进度条**（中间）——使用量增加时，进度条从左到右填充。

当接近限制时，条形的颜色会发生变化：
  - **绿色**——使用量低于 80%。

Everything is running normally.
  - **Amber** — usage is between 80% and 99%.

The service is still running but getting close to the limit.
  - **Red** — usage has hit 100%.

The service is now throttled for this month.
- **Usage counts** (right) — the exact number of requests used out of the total allowed, for example `3,241 / 10,000`.

The label in parentheses shows the time window, typically `(this month)`.

If the tile cannot reach the Spwig update server to fetch your current usage (for example, if your server has no outbound internet access), the counts column shows a dash (`—`) for that service. This does not mean the service is broken; it means the usage display is temporarily unavailable.

### The Upgrade button

When any service reaches 80% or more, an **Upgrade** button appears in the top-right corner of the tile. Clicking it opens the Spwig upgrade page where you can compare plans and raise your service limits. The button disappears once usage drops back below 80% at the start of the next month.

## The quota warning banner

In addition to the dashboard tile, a banner appears at the top of every admin page whenever any service crosses the 80% threshold. The banner only appears on Community installs.

**Amber banner — approaching the limit (80–99%)**

> **Approaching hosted-services limit:** One of your Spwig services is over 80% of its Community-tier quota. Upgrade to raise the limit before it's hit.

This banner is an early heads-up. Your services are still running, and you have time to decide whether to upgrade before the month ends.

**Red banner — limit reached (100%)**

> **Spwig services limit reached:** One of your hosted services has hit its Community-tier quota. Upgrade to keep them running without interruption.

This banner appears when at least one service has hit 100% and is now throttled. Clicking **Upgrade** on either banner opens the same upgrade page as the tile button.

横幅在计数器重置时会在下一个日历月开始时自动消失，或者在您升级到付费计划后立即消失。

## 90% 时的电子邮件提醒

当任何服务使用量达到其配额的 90% 时，Spwig 也会向您商店设置中配置的电子邮件地址 (**设置 > 商店设置 > 联系 > 管理员电子邮件**) 发送一次警告电子邮件。每项服务每月最多发送一次电子邮件，因此您不会收到大量消息。在 100% 时不会发送电子邮件，因为此时管理员界面中的横幅已经清楚地说明了情况。

如果您未收到电子邮件，请检查 **设置 > 商店设置** 下的管理员电子邮件地址是否已正确设置。

## 升级您的计划

当您从社区版升级到任何付费计划时，更高的限制会立即生效 —— 不需要重启商店或更改配置。仪表板瓷砖将在下一次刷新时显示新的更高限制（在五分钟内）。

要升级，请点击仪表板瓷砖或配额横幅上的 **升级** 按钮，或直接访问 Spwig 升级页面。付费计划包含与社区版相同的三项托管服务（GeoIP、Geocoder、Push），但月度限制更高，并且包括 Spwig 托管的电子邮件投递和优先支持。

## 自托管和 Pro 许可证

如果您使用带有付费许可证的自托管 Spwig 安装，您的许可证等级将决定您的服务限制，与相应的托管计划相同。您的商店仍然需要出站互联网访问以连接到 `updates.spwig.com`，以便平台获取和验证您的等级配置。仪表板瓷砖中显示的使用计数器是从托管服务端点 `geoip.spwig.com`、`geocoder.spwig.com` 和 `push.spwig.com` 获取的。

目前没有选项可以将 GeoIP、Geocoder 或 Push 替换为自托管的替代方案 —— 这些服务仅由 Spwig 的基础设施提供，并包含在所有版本中。

## 小贴士

保留所有 markdown 格式、图片路径、代码块和专业术语。

- **在繁忙月份结束时定期检查该面板** —— 促销活动或销售事件可能会显著增加 GeoIP 和 Geocoder 的查询次数。

该面板会在客户受到影响之前提前通知您。
- **货币回退对大多数客户是不可见的** —— 如果 GeoIP 达到其限制，客户将看到您商店的默认货币。

对于主要面向单一市场的商店，这很少会成为严重问题；但对于真正面向国际的商店则更为重要。
- **地址自动补全是一种便利，而非障碍** —— 当 Geocoder 被限流时，客户仍可以正常输入并提交他们的地址。

如果您经常举办促销活动，导致结账流量很高，建议在繁忙时段之前升级。
- **推送限流不会永久丢失通知** —— 限流期间排队的通知在月份重置或升级后不会回溯发送。

如果您严重依赖推送来接收时效性强的订单提醒，请在达到限制之前升级，以确保不会错过任何信息。
- **5 分钟缓存意味着面板不是完全实时的** —— 使用情况数据在后台大约每五分钟刷新一次。

在异常高流量期间，实际使用情况可能略微领先于面板显示的数据。
- **设置您的管理员电子邮件地址** —— 仅当 **设置 > 商店设置 > 管理员电子邮件** 已填写时，90% 警告电子邮件才有效。

确认该设置是否正确，以便在出现问题之前及时收到提醒。