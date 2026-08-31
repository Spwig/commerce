---
title: 訂閱方案
---

訂閱方案可讓您的產品提供定期計費功能——非常適合消耗品、服務、精選禮盒，或任何客戶會重複購買的產品。本指南將說明如何建立與設定方案、設定價格層級、加入試用期，以及附加選配的附加項目。

## 快速入門

在管理側邊欄中前往 **Subscriptions > Subscription Plans**。方案列表會顯示您所有的方案，包括其定價模式、活躍訂閱者數量以及可見性狀態。

![訂閱方案列表](/static/core/admin/img/help/subscription-plans/plan-list.webp)

若要建立新方案，請點擊 **Create with Wizard** 按鈕——這將開啟方案建立嚮導，逐步引導您完成設定。旁邊的 **+ Add Plan** 按鈕則會開啟一個空白表單，供偏好手動設定所有項目的商家使用。

單獨的方案本身無法購買——它是一個範本。在此建立完成後，請從產品的 **Subscriptions** 分頁（僅限 Simple、Variable 和 Digital 產品）將其附加到一個或多個產品上，讓客戶實際進行訂閱。有關該步驟，請參閱 [Selling Products as Subscriptions](/help/selling-products-as-subscriptions)。

## 方案編輯器

開啟現有方案（從列表中點擊其名稱或鉛筆圖示）將帶您進入方案編輯器。標題會顯示方案名稱、其定價模式、**Active**/**Inactive** 與 **Public**/**Private** 狀態徽章，以及建立日期。標題右上角的兩個按鈕用於儲存您的變更——帶圓圈的勾號圖示會儲存並返回列表，而普通的勾號圖示則會儲存並讓您留在該頁面，以便繼續編輯。

標題下方，一個統計條會以一目瞭然的方式總結方案資訊：**Active Subscriptions**、**Pricing Tiers**、**Add-ons** 以及 **Total Revenue**。

表單的其餘部分組織為五個分頁：

| 分頁 | 內容 |
|-----|-------------------|
| **一般** | 方案資訊（名稱、識別碼、描述）與狀態（啟用/公開） |
| **定價** | 定價設定、試用期，以及限制與規範 |
| **層級與附加功能** | 定價層級與附加功能編輯器 |
| **生命週期** | 取消政策與方案變更行為 |
| **進階** | 供應商整合與統計資料 |

以下各節將逐步說明每個分頁的設定。當您直接透過 **+ 新增方案**（而非精靈）建立全新方案時，相同的欄位會顯示在單一可捲動的表單中，而非分頁形式——請先儲存方案一次，再重新開啟以取得完整的分頁式編輯器。

## 方案資訊（一般分頁）

**方案資訊** 卡片用於記錄您方案的核心識別資訊。

- **方案名稱** — 客戶訂閱時看到的名稱。點擊地球圖示可為其他商店語言新增翻譯。
- **識別碼 (Slug)** — 從名稱自動生成的 URL 友善識別碼（例如：`premium-plan`）。此識別碼用於內部系統及整合。
- **描述** — 選填文字，用於說明方案包含的內容。支援翻譯。

同一分頁上的 **狀態** 卡片用於控制 **啟用** 與 **公開** 切換選項——請參閱下方的 [可見性與狀態](#visibility-and-status)。

![方案編輯器的一般分頁](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## 定價模型（定價分頁）

**定價設定** 卡片用於控制此方案的定價結構：

| 定價模型 | 適用情境 |
|---------------|----------|
| **分層定價** | 提供月付、季付及年付的承諾選項，並對較長期限提供折扣 |
| **基於數量** | 按席位或按使用者計價，總金額隨數量增加而調整（例如：團隊授權） |
| **固定費率** | 單一固定價格，無其他變體 |

For **Quantity-Based** plans, check **Allow Quantity** and set the **Minimum Quantity** (minimum seats required) and optionally a **Maximum Quantity** to cap how many seats a subscriber can purchase.

![Pricing tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Pricing tiers (Tiers & Add-ons tab)

Pricing tiers define the billing frequency and discount options available to customers on this plan. Add them in the **Pricing Tiers** card on the **Tiers & Add-ons** tab, alongside the Add-ons editor.

Each tier has these fields:

- **Tier Name** — The label shown to customers (e.g., `Monthly`, `Annual — Save 20%`). Supports translations.
- **Billing Cycle** — How often the customer is charged: Daily, Weekly, Monthly, Quarterly, Semi-Annual, or Annual.
- **Billing Interval** — The multiplier for the billing cycle. Set to `2` with Monthly to bill every 2 months.
- **Discount Percentage** — The discount applied to the product price for this tier. Set to `0` for full price, or `20` to give 20% off. This discount stacks on top of any sale pricing on the product itself.
- **Default Tier** — Mark one tier as the default to pre-select it for customers when they view the subscription options.

The discount applies starting from the customer's very first billing cycle, not just on renewals — a tier with a 20% discount charges 20% off from day one (or from the first charge after a trial, if the plan has one).

### Example: tiered plan with three options

For a "Coffee Club" subscription plan:

| Tier Name | Billing Cycle | Discount |
|-----------|---------------|----------|
| Monthly | Monthly | 0% |
| Quarterly — Save 10% | Quarterly | 10% |
| Annual — Save 20% | Annual | 20% |

## Plan add-ons (Tiers & Add-ons tab)

Add-ons are optional extras that subscribers can attach to their plan. Add them in the **Add-ons** card, directly below Pricing Tiers on the same tab:

- **Add-on Name** — The name shown to customers.

支援翻譯。
- **描述** — 附加功能提供的內容。
- **價格** — 附加功能的費用。
- **計費頻率** — 附加功能是在訂閱開始時**按計費週期**（定期）或**一次性**收費。
- **允許數量** — 啟用後可讓客戶購買多個附加功能單位。
- **必要** — 勾選此選項可自動將附加功能包含在所有新訂閱中。

必要附加功能無法由客戶移除。

![方案編輯器的層級與附加功能分頁](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## 試用期（定價分頁）

試用期讓客戶在首次完整收費前試用您的訂閱。請在定價設定下方的**試用期**卡片中進行設定：

- **試用期（天數）** — 免費試用天數。設定為 `0` 可停用試用。最長為 365 天。
- **試用價格** — 試用期間的選填優惠價格（例如，首月 $1）。留空則為完全免費試用。

## 限制與規範（定價分頁）

**限制與規範**卡片同樣位於定價分頁，包含：

- **最大計費週期數** — 訂閱自動結束前的總計費週期數。留空則為無限定期計費。適用於分期方案或限時訂閱。

**設定費**與**排序順序**不屬於此卡片 — 它們是在您首次透過**精靈建立**流程建立方案時設定一次，之後無法從編輯畫面變更。如果需要調整任一數值，請停用該方案並使用精靈重新建立，而非編輯現有方案。請注意，在此版本中，設定費尚未在結帳時自動收取 — 請將此欄位視為保留給未來更新，而非現行可用的收費項目。

## 取消政策（生命週期分頁）

在**取消政策**卡片中控制客戶如何取消訂閱：

| 政策 | 描述 |
|--------|-------------|
| **隨時取消** | 客戶可以隨時立即取消 |
| **在週期結束時取消** | 取消將在付費週期結束時生效 — 客戶在到期前可繼續使用 |
| **需要最低承諾週期** | 客戶必須完成最低數量的計費週期後才能取消 |

附加設定：

- **最低承諾週期** — 使用承諾政策時，設置所需的計費週期數量（例如，`3` 表示 3 個月的最低要求）。
- **寬限期（天數）** — 在支付失敗後，繼續訪問的天數，之後訂閱將被暫停。設為 `0` 表示立即暫停。
- **重新激活週期（天數）** — 取消後的天數內，客戶可以重新激活其訂閱而無需從頭開始重新訂閱。

## 計劃變更行為（生命週期標籤）

**計畫變更行為** 卡片位於取消政策下方，用來控制客戶在不同計畫之間升級或降級時的行為：

- **升級行為** — 設為 **立即**（現在收取比例金額）或 **在續訂時**（在下一個計費日期切換）。
- **降級行為** — 設為 **立即**（將信用額度應用到下一個帳單）或 **在續訂時**（在下一個計費日期切換）。

![計畫編輯器的生命週期標籤](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## 進階選項卡

**進階** 選項卡包含您日常很少需要的設定：

- **供應商整合** — 將此計畫對應到您支付供應商的計畫/價格 ID（例如，`{"stripe": "price_xxx", "paypal": "P-xxx"}`），適用於那些透過供應商本地管理訂閱的商店，而不是使用 Spwig 自己的計費引擎。
- **統計** — 只讀數字：**活躍訂閱**、**總收入** 和計畫的 **建立於** / **更新於** 時戳。這些數字與頁面頂部的統計條顯示的數據相同。



![方案編輯器的進階分頁](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## 可見性與狀態（一般分頁）

- **啟用** — 取消勾選以停用方案，使無法建立新的訂閱。現有訂閱不受影響。
- **公開** — 取消勾選以在客戶端頁面隱藏該方案（適用於現有訂閱者仍在使用中的內部或舊版方案）。

## 提示

- 使用**試用期**來減少猶豫——即使是短短 7 天的免費試用，也能顯著提高訂閱產品的轉換率。
- 設定**三個價格層級**（月付、季付、年付）並提供遞增的折扣，以鼓勵年付承諾並改善現金流。
- 對於服務型訂閱，將**取消政策**設為**期間結束時取消**，讓客戶在付費期間內保留存取權——這感覺公平且能減少拒付。
- 將**寬限期**設為 3–7 天以應對付款失敗。這讓客戶有時間在失去存取權之前更新付款方式。
- 謹慎使用附加元件的**必要**旗標——僅用於真正強制要求的事項（例如：服務協議），不要將其作為抬高價格的手段。
- 停用沒有訂閱者的方案，而不是刪除它們——這可以保留先前訂閱客戶的歷史數據。