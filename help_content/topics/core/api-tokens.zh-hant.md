---
title: API 令牌
---

API 令牌是安全密钥，允许外部服务和集成与您的商店进行通信。当第三方服务或工具需要访问您的商店数据或触发操作时，它会在每次请求中发送一个 API 令牌，以便您的商店可以验证请求是否已授权。您可以在管理后台的 API 令牌部分创建和管理所有令牌，包括它们可以访问的商店部分。

## 何时需要 API 令牌

您通常在以下情况下需要创建 API 令牌：

- 连接需要读取或写入您商店的外部服务或自动化工具
- 设置需要验证传入调用的 Webhook 接收器
- 为您的安装配置 Spwig 帮助系统
- 使用 Spwig 的 API 构建自定义集成
- 在您的 Spwig 商店与其他系统之间同步数据

每个集成应使用自己的令牌，这样您可以撤销一个服务的访问权限而不影响其他服务。

## 令牌类型

创建令牌时，您选择一个类型来描述其用途。该类型仅供您参考，有助于您跟踪每个令牌的作用。

| 类型 | 用途 |
|------|---------|
| **帮助系统** | 用于 Spwig 帮助文档系统 |
| **外部集成** | 第三方服务、自动化工具（例如 Zapier）或数据同步工具 |
| **Webhook** | Webhook 接收器或端点的认证 |
| **自定义** | 任何不属于上述类别的其他用途 |
| **实例同步** | Spwig 安装或外部 Spwig 服务之间的同步 |

## API 范围：控制令牌可以访问的内容

每个令牌还有一个 **API 范围** 部分，用于决定它确切可以调用商店的哪些部分。而不是让令牌对所有内容都有完全访问权限，您可以一次一个区域地授予访问权限——并且仅在集成实际需要的层级上进行授权。

**未选择任何范围的令牌无法访问任何 API**，即使它本身处于活动且有效状态。

這是一個全新令牌的預設值，因此在您主動授予它訪問權限之前，集成將無法正常工作。

對於每個範圍，您可以選擇以下三種訪問等級之一：

| 訪問等級 | 它允許的內容 |
|----------|------------------|
| **無訪問權限** | 令牌無法調用此區域的任何端點 |
| **只讀** | 令牌可以從此區域檢索數據，但不能更改任何內容 |
| **讀取與寫入** | 令牌可以檢索數據，也可以創建、更新或刪除數據 |

範圍按您的管理員區域進行分組：

| 群組 | 範圍 | 是否有讀取與寫入權限？ | 授予訪問權限的內容 |
|------|------|:---:|---------------------|
| 分析 | **銷售分析** | 只讀 | 銷售儀表板、KPI、產品/客戶/類別分析、比較和導出 |
| 分析 | **網站分析** | 只讀 | 訪客和流量分析：概覽、趨勢、頂部頁面、地理和來源 |
| 目錄 | **產品** | 是 | 產品、變體、圖片、庫存調整和屬性分配 |
| 目錄 | **類別** | 是 | 產品類別，包括圖片和橫幅 |
| 目錄 | **品牌** | 是 | 產品品牌 |
| 目錄 | **屬性** | 是 | 產品屬性定義 |
| 目錄 | **庫存** | 是 | 庫存儀表板、庫存速度、庫存移動、補貨建議和庫存設置 |
| 訂單 | **訂單** | 是 | 訂單、訂單備註、狀態/跟蹤更新、取消、退款和訂單文件 |
| 顧客 | **顧客消息** | 是 | 來自聯繫表單和訂單備註的顧客消息，包括狀態更新和回覆 |
| 商店與設置 | **商店設置** | 是 | 商店設置、可用語言和品牌（名稱、顏色、標誌） |
| 用戶與訪問 | **員工與角色** | 是 | 員工賬戶、邀請、角色和權限目錄 |

這兩個 **分析** 範圍始終是只讀的 —— 報告數據沒有「寫入」的概念，因此選擇器只為它們提供 **無訪問權限** 或 **只讀** 選項。

[![API範圍選擇器，Analytics和Catalog範圍組上方有一個訪問說明](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)]

在範圍選擇器下方，只讀的**"此令牌可以訪問："**摘要會列出您授予的每個範圍及其等級，因此您可以快速查看令牌的訪問權限，而無需解碼選擇器。

[!["此令牌可以訪問"摘要列出每個授予的範圍及其讀取或讀取和寫入等級](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)]

### 令牌實際使用的權限

令牌的範圍描述了它所能執行的*上限* —— 但令牌也會繼承創建它的員工的實際權限：

- 即使創建令牌的員工是超級用戶，令牌也永遠無法以**超級用戶**權限執行操作。
- 如果創建員工的角色也允許對該區域進行寫入訪問，則範圍上的**讀取和寫入**才會生效。如果他們的角色僅對產品具有只讀權限，那麼他們創建的令牌即使具有"產品：讀取和寫入"權限，也只能讀取 —— 角色會作為範圍的第二道門。
- 如果創建令牌的員工被刪除，或其帳戶被停用，則無論令牌的範圍如何，令牌會立即失去API訪問權限 —— 沒有允許的用戶讓它作為代理。

這意味著最安全的方法是創建一個範圍緊密的令牌，即在以一個其自身角色已經與令牌所需訪問權限匹配的員工身份登錄時創建令牌。

## 創建API令牌

1.

導航至 **設置 > API令牌**
2.

點擊 **+ 添加API令牌**
3.

輸入一個 **名稱**，清楚地描述令牌的用途（例如，`Zapier產品同步` 或 `幫助系統API`）
4.

選擇適當的 **令牌類型**
5.

可選地添加 **描述**，提供更多關於集成的細節
6.

在 **API範圍** 中，為集成所需的每個區域選擇 **無訪問權限**、**讀取** 或 **讀取和寫入** —— 將所有其他範圍保留為 **無訪問權限**
7.

保留所有markdown格式、圖片路徑、程式碼塊和技術術語。

Configure the **Active** status, **Expiry Date**, and **Allowed IPs** as needed (see below)
8.

Click **Save**

After saving, the full token value is displayed on the detail page. **Copy it immediately** — the token is masked in the list view for security and cannot be retrieved in full again after you leave this page.

![API Token Detail](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Token value security

Spwig shows the complete token value only once: immediately after you save a new token. After that, the list view shows only a masked version (e.g., `spw_••••••••••••••••••••3f8a`).

If you lose a token value, you cannot recover it. You will need to delete the old token and create a new one, then update the integration that was using it.

**Never share token values in emails, chat messages, or source code.** Treat them like passwords.

## Setting an expiry date

The **Expires At** field sets a date and time after which the token will stop working automatically. Leave it blank for tokens that should not expire.

Expiry dates are useful for:

- Temporary integrations with a fixed end date
- Tokens given to third parties where you want automatic access removal
- Adding an extra layer of security to high-privilege integrations

When a token expires, requests using it are rejected. You can extend access by updating the **Expires At** date or creating a replacement token.

## Restricting to specific IP addresses

The **Allowed IPs** field accepts a list of IP addresses. When the list is not empty, the token only works when the request comes from one of those addresses.

For example, if your analytics tool runs on a server at `203.0.113.42`, adding that IP means the token cannot be misused from any other location, even if it is leaked.

Leave **Allowed IPs** empty to allow requests from any IP address.

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

點擊令牌名稱
2.

取消勾選 **啟用**
3.

保存

該令牌會保留在您的列表中以供參考，但會拒絕任何後續請求。當您在調查問題時需要臨時暫停某個整合時，這會很有幫助。

要永久刪除令牌：

1. 在列表中選中其複選框
2. 從操作菜單中選擇 **刪除選中的 API 令牌**
3. 確認刪除

一旦刪除，令牌就無法恢復。如果整合仍然需要訪問權限，請創建一個新令牌並更新整合的配置。

## 示例：設置 Zapier 整合

**場景：** 您希望將商店連接到 Zapier 以自動化訂單通知。

| 欄位 | 值 |
|-------|-------|
| 名稱 | `Zapier 訂單自動化` |
| 令牌類型 | 外部整合 |
| 描述 | 用於 Zapier 讀取新訂單並觸發通知 |
| API 範圍 | **訂單**：讀取與寫入 |
| 啟用 | 是 |
| 到期時間 | *(留空)* |
| 允許的 IP 地址 | *(留空 — Zapier 使用動態 IP)* |

僅授予 **訂單** 範圍，因此即使此令牌被洩露，它也無法訪問產品、客戶訊息、員工帳戶或商店的其他部分。保存後，複製完整的令牌值並粘貼到 Zapier 的 Spwig 整合設置中。

## 小技巧

保留所有 markdown 格式、圖片路徑、程式碼塊和技術術語。

- 為每個令牌給予清晰且具體的名稱 — 當你幾個月後進行問題排除時，`Shopify Sync v2` 比 `Token 3` 有用得多
- 為每個整合建立一個令牌 — 如果某個整合遭到入侵，你可以只撤銷該令牌，而不會影響到其他令牌
- **僅授予整合實際需要的權限範圍** — 報告工具只需要對銷售分析或網站分析的讀取權限，而不需要對產品或員工與角色的讀取與寫入權限
- 在將令牌交給第三方之前，請檢查變更表單上的 **"此令牌可以存取："** 總結 — 這是確認你是否誤授予過多權限的最快方式
- 請記住寫入權限也取決於創建員工本身的職位 — 如果某個權限範圍顯示為讀取與寫入，但寫入仍然失敗，請同時檢查該使用者的職位權限
- 為用於一次性專案或臨時整合的令牌設定到期日期 — 這能降低遺忘的令牌無限期處於活動狀態的風險
- 每幾個月審查一次你的令牌列表，並停用任何 **最後使用日期** 非常久遠的令牌，因為這些可能屬於已經不再運行的整合
- 如果你懷疑某個令牌已經被洩露，請立即停用它，建立一個替代令牌，並在重新啟用存取之前更新受影響的整合