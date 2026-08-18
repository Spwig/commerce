---
title: 訂閱方案
---

訂閱方案讓您為您的產品提供重複計費 —— 對於消耗品、服務、精選禮盒或任何客戶會反覆購買的產品都非常理想。本指南說明如何建立和設定方案、設定定價等級、新增試用期間，以及附加可選的附加功能。

## 開始使用

導覽至管理介面側邊欄中的 **Subscriptions > Subscription Plans**。方案清單會顯示所有您的方案及其定價模式、活躍訂閱者數量和可見性狀態。

![訂閱方案清單](/static/core/admin/img/help/subscription-plans/plan-list.webp)

要建立新方案，請按一下 **Create with Wizard** 按鈕 —— 這會開啟方案建立精靈，逐步引導您進行設定。旁邊的 **+ Add Plan** 按鈕則會開啟空白表單，讓想要手動設定所有內容的商家可以自行設定。

單獨的方案無法購買 —— 它只是一個範本。在此建立之後，請從產品的 **Subscriptions** 標籤（僅限簡單、變量和數位產品）將其附加到一個或多個產品上，讓客戶實際上可以訂閱。請參閱 [將產品作為訂閱方案銷售](/help/selling-products-as-subscriptions) 來完成這一步。

## 方案編輯器

開啟現有的方案（從清單中按一下其名稱，或按鈕筆圖示）會帶您到方案編輯器。標題列顯示方案名稱、其定價模式、**Active**/**Inactive** 和 **Public**/**Private** 狀態徽章，以及建立日期。標題列右上角的兩個按鈕用來儲存變更 —— 檢查圓圈圖示儲存並返回清單，普通檢查圖示儲存並讓您留在頁面上以繼續編輯。

在標題列下方，有一個統計條目快速總覽方案：**Active Subscriptions**、**Pricing Tiers**、**Add-ons** 和 **Total Revenue**。

其餘表單分為五個標籤：

{"| Tab | What it contains |\n|-----|-------------------|\n| **General** | Plan Information (name, slug, description) and Status (active/public) |\n| **Pricing** | Pricing Configuration, Trial Period, and Limits & Restrictions |\n| **Tiers & Add-ons** | The Pricing Tiers and Add-ons editors |\n| **Lifecycle** | Cancellation Policy and Plan Change Behavior |\n| **Advanced** | Provider Integration and Statistics |\n\nThe sections below walk through each tab's settings. When you create a brand-new plan directly from **+ Add Plan** (rather than the wizard), the same fields appear in a single scrollable form instead of tabs — save the plan once and reopen it to get the full tabbed editor.\n\n## Plan information (General tab)\n\nThe **Plan Information** card captures the core identity of your plan.\n\n- **Plan Name** — The name customers see when subscribing. Click the globe icon to add translations for other store languages.\n- **Slug** — A URL-friendly identifier auto-generated from the name (e.g., `premium-plan`). This is used internally and in integrations.\n- **Description** — Optional text describing what the plan includes. Supports translations.\n\nThe **Status** card on the same tab controls the **Active** and **Public** toggles — see [Visibility and status](#visibility-and-status) below.\n\n![General tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)\n\n## Pricing model (Pricing tab)\n\nThe **Pricing Configuration** card controls how pricing is structured for this plan:\n\n| Pricing Model | Best For |\n|---------------|----------|\n| **Tiered Pricing** | Offering monthly, quarterly, and annual commitment options with discounts for longer terms |\n| **Quantity-Based** | Per-seat or per-user pricing where the total scales with quantity (e.g., team licenses) |\n| **Flat Rate** | A single fixed price with no variations |}

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
- **描述** — 該附加模組提供的內容。
- **價格** — 該附加模組的費用。
- **計費頻率** — 該附加模組是按 **計費週期**（重複計費）還是 **一次性** 費用在訂閱開始時收取。
- **允許數量** — 選擇以讓客戶購買多個該附加模組單元。
- **必填** — 勾選此選項以在所有新訂閱中自動包含該附加模組。

必填的附加模組無法由客戶刪除。

![方案編輯器的等級與附加模組標籤](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## 試用期（定價標籤）

試用期讓客戶在第一次完整收費前嘗試您的訂閱。在下面的 **試用期** 卡中進行此設置：

- **試用期（天數）** — 免費試用天數。設為 `0` 以關閉試用期。最大為 365 天。
- **試用價格** — 試用期間的可選降低價格（例如，第一個月為 $1）。留空以完全免費試用。

## 限制和限制（定價標籤）

**限制與限制** 卡，也在定價標籤上，包含：

- **最大計費週期** — 訂閱自動結束前的總計費週期數。留空以無限重複計費。適用於分期付款計畫或時間限制的訂閱。

**設定費用** 和 **排序順序** 不屬於此卡 —— 它們是在您第一次透過 **建立精靈** 流程建立方案時設置的，之後無法從編輯畫面更改。如果您需要調整任一值，請停用方案並透過精靈重新建立，而不是編輯現有方案。請注意，在此版本中設定費用還未在結帳時自動收取 —— 請將此欄位視為未來更新的保留欄位，而不是工作費用。

## 取消政策（生命週期標籤）

在 **取消政策** 卡中控制客戶如何取消其訂閱：

| 政策 | 描述 |
|--------|-------------|
| **隨時取消** | 客戶可以隨時立即取消 |
| **在週期結束時取消** | 取消將在付費週期結束時生效 —— 客戶在到期前可繼續使用 |
| **需要最低承諾週期** | 客戶必須完成最低數量的計費週期後才能取消 |

額外設定：

- **最低承諾週期** —— 使用承諾政策時，設置所需的計費週期數量（例如，`3` 表示 3 個月的最低要求）。
- **寬限期（天數）** —— 在支付失敗後，繼續訪問的天數，直到訂閱被暫停。設為 `0` 表示立即暫停。
- **重新激活週期（天數）** —— 取消後的天數內，客戶可以重新激活其訂閱而無需從頭開始重新訂閱。

## 計劃變更行為（生命周期標籤）

**計劃變更行為** 卡片位於取消政策下方，用來控制客戶在不同計劃之間升級或降級時的行為：

- **升級行為** —— 設為 **立即**（現在收取比例金額）或 **在續訂時**（在下一個計費日期切換）。
- **降級行為** —— 設為 **立即**（將信用額度應用到下一個帳單）或 **在續訂時**（在下一個計費日期切換）。

![計劃編輯器的生命周期標籤](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## 高級選項卡

**高級** 選項卡包含您日常很少需要的設置：

- **供應商整合** —— 將此計劃對應到您支付供應商的計劃/價格 ID（例如，`{"stripe": "price_xxx", "paypal": "P-xxx"}`），適用於那些通過供應商本地管理訂閱的商店，而不是使用 Spwig 自己的計費引擎。
- **統計** —— 只讀數字：**活躍訂閱**、**總收入** 和計劃的 **建立於** / **更新於** 時戳。這些數字與頁面頂部的統計條顯示的數據相同。

{"![高階選項](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)}

## 可見性與狀態 (常規選項)

- **啟用** — 取消勾選以停用方案，這樣就無法建立新的訂閱。現有訂閱不受影響。
- **公開** — 取消勾選以將方案隱藏於客戶頁面 (適用於內部或舊方案，現有訂閱者仍可使用)。

## 小技巧

- 使用 **免費試用期** 來減少顧客猶豫 — 即使是短至 7 天的免費試用期也能顯著提高訂閱商品的轉化率。
- 設定 **三種定價等級** (每月、每季、每年) 並提供逐級折扣，以鼓勵年度承諾並改善現金流。
- 對基於服務的訂閱，將 **取消政策** 設為 **在週期結束時取消**，讓顧客在付費週期內持續存取 — 這會讓顧客覺得公平並減少爭議。
- 將 **寬限期** 設為 3–7 天，以應對付款失敗。這會給顧客時間更新付款方式，以免失去存取權。
- 對附加功能使用 **必要** 標記時要謹慎 — 僅用於真正必要的項目 (例如服務協議)，而不是用來提高定價。
- 停用沒有訂閱者的方案，而不是刪除它 — 這樣可以保留歷史資料，供之前訂閱過的顧客參考。"