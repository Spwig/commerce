---
title: 推薦計劃
---

推薦計劃讓您現有的客戶可以與他們的朋友和家人分享一個獨特的推薦連結。當被推薦的朋友進行他們的第一筆符合資格的購買時，推薦人和新客戶都可以獲得獎勵——透過口碑行銷來推動新客戶的獲取。

## 推薦計劃是如何運作的

1. 顧客與朋友分享他們獨特的推薦連結（或代碼）。
2. 朋友點擊連結，並透過 cookie 跟蹤最多 30 天（可配置）。
3. 朋友註冊並下達他們的第一筆符合資格的訂單。
4. 系統會建立推薦歸因記錄，並執行詐騙和資格檢查。
5. 如果歸因獲得批准，雙方都會獲得獎勵。

您的商店有一個單一的推薦計劃配置。請導航至 **行銷 > 推薦計劃** 來設置。

## 設置您的推薦計劃

### 計劃狀態

該計劃有三種狀態：

- **草稿** — 計劃正在配置中，但尚未上線。推薦連結處於非活動狀態。
- **啟用** — 計劃已上線。顧客可以分享連結並賺取獎勵。
- **暫停** — 計劃暫時停止。現有的歸因仍會處理，但不會追蹤新的推薦。

當您準備好啟動時，將 **狀態** 設置為 **啟用**。您隨時可以暫停它。

### 奖励配置

定義當推薦轉化時發放的獎勵。該計劃支持 **雙方獎勵** — 這意味著您可以獎勵推薦人（分享連結的客戶）和被推薦人（使用連結的新客戶）。

在 **獎勵配置** 欄位中為每位接收者配置獎勵。可用的獎勵類型包括：

| Reward Kind | Description |
|-------------|-------------|
| **Store Credit** | Adds credit to the customer's wallet, usable on future orders |
| **Coupon Code** | Generates a unique discount voucher code |
| **Percentage Discount** | Issues a percentage discount for use at checkout |
| **Exclusive Perk** | A custom perk (e.g., free gift, priority access) — described in the reward's description field |

**Example configuration** — $10 store credit for the referrer and $10 discount for the new customer:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Set "double_sided": false if you only want to reward the referrer.

### Eligibility rules

Eligibility rules determine which referrals qualify for rewards. Configure these in the **Eligibility Rules** field:

| Rule | What it does |
|------|--------------|
| `new_customer_only` | If `true`, the referred friend must be a brand new customer (no prior orders) |
| `min_order_value` | The minimum order amount (in your store currency) the referred friend must spend |
| `exclude_discounts` | If `true`, orders where the referred customer used a voucher do not qualify |
| `exclude_staff` | If `true`, staff accounts cannot be referrers or referees |

**Example** — new customers only, minimum $40 order, staff excluded:

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Timing configuration

The **Timing Configuration** field controls when rewards are issued after a qualifying order:

| Setting | What it does |
|---------|--------------|
| `issue_on` | When to issue the reward: `signup` (immediately on registration), `first_purchase` (immediately after order), or `post_refund` (after the refund window expires) |
| `refund_window_days` | How many days to wait before issuing rewards when using `post_refund` (default: 14 days) |

使用 `post_refund` 是最謹慎的選擇 — 它會等到退貨窗口過後才發放獎勵，從而降低對後續可能被退貨的訂單發放獎勵的風險。

| 設定 | 功能說明 |
|---------|--------------|
| `policy` | 整體嚴格程度：`strict`、`balanced` 或 `lenient` |
| `auto_reject_threshold` | 風險分數（0–100）高於此值的推薦將自動被拒絕（預設：80） |
| `auto_approve_threshold` | 風險分數低於此值的推薦將自動被批准（預設：30） |
| `check_ip` | 若設為 `true`，會檢查推薦人與被推薦人是否使用相同的 IP 位址 |
| `check_device` | 若設為 `true`，會檢查推薦人與被推薦人是否有相同的設備指紋 |
| `check_velocity` | 若設為 `true`，會監控來自單一來源的異常高推薦率 |
| `velocity_window_hours` | 速度檢查的時間窗口（以小時為單位） |
| `max_referrals_per_window` | 在速度窗口內允許來自單一來源的最大推薦數 |

風險分數介於自動拒絕與自動批准閾值之間的推薦將處於 **Pending** 狀態，需要手動審核。

### 使用條款與條件

在 **Terms & Conditions** 欄位中輸入任何法律條款與條件。當客戶查看推薦計劃時，會顯示此文字。支援 Markdown 格式。

## 查看推薦記錄

導覽至 **Marketing > Referral Attributions**，可查看所有推薦案例 — 也就是推薦人與被推薦客戶之間的連結。

![Referral attributions list](/static/core/admin/img/help/referral-program/attribution-list.webp)

每個推薦記錄會顯示推薦人、被推薦客戶、他們放置的第一筆訂單、目前的狀態以及風險分數。

### 推薦狀態

| 狀態 | 含義 |
|--------|---------------|
| **Pending** | 等待審核 — 風險分數處於需要手動審核的範圍 |
| **Approved** | 推薦有效 — 優惠已經或將會發放 |
| **Rejected** | 推薦不符合資格或被標記為詐騙 |
| **Expired** | 推薦在追蹤窗口內未被轉換 |


### 手動批准或拒絕歸因

對於狀態為 **待處理** 的歸因，您可以通過打開歸因記錄並使用操作按鈕來手動批准或拒絕它們。拒絕時，請選擇 **拒絕原因**：

- 自我推薦
- 非新客戶
- 未達最低訂單價值
- 一次性郵箱
- 資本上限已達
- 有詐騙風險
- 訂單已退款或取消
- 手動拒絕

您還可以為自己的記錄添加 **拒絕備註**。

### 按風險等級過濾

使用側邊欄中的 **風險等級** 過濾器，專注於需要審核的高風險歸因：

- 低風險（分數 0–30）— 自動批准
- 中風險（分數 31–70）— 手動審核
- 高風險（分數 71–89）— 手動審核，需謹慎處理
- 非常高風險（分數 90+）— 自動拒絕

## 查看已發放的獎勵

導航至 **行銷 > 已發放獎勵**，查看所有因已批准的歸因而發放的獎勵。

每個獎勵條目都會顯示客戶、他們是推薦人還是被推薦人、獎勵類型和金額，以及當前的兌換狀態。

### 奖励状态

| 状态 | 含义 |
|------|------|
| **待处理** | 奖励已创建但尚未交付给客户 |
| **已发放** | 奖励已激活，客户可以使用 |
| **已兑换** | 客户已使用奖励 |
| **已过期** | 奖励在到期前未被使用 |
| **已撤销** | 奖励被手动取消（例如，如果奖励发放后原订单被退款） |

### 撤销奖励

如果需要取消奖励——例如，符合条件的订单被退回——请打开奖励记录并使用 **撤销** 操作。为您的记录添加一个说明撤销原因的备注。

## 小贴士

- 从 `post_refund` 时间设置开始。

在發放獎勵之前等待退貨窗口過期，可避免對最終被退貨的訂單進行獎勵。
- `balanced` 的詐騙政策對大多數商店來說是一個不錯的預設選擇。

如果您發現來自少數帳戶的推薦量異常激增，請切換至 `strict`。
- 設定實際的每月和終身上限。

如果您的獎勵價值較高，每月每位推薦者的上限設定為 10–20 是合理的，以防止濫用。
- 每週審核 **Pending** 的歸因記錄。

讓它們長時間未經審核可能會讓等待獎勵的合法推薦者感到沮喪。
- 使用 **Risk Level** 篩選器來優先處理您的手動審核隊列 —— 從風險極高的歸因開始，再轉向中等風險。
- 保持您的條款與條件簡短且使用通俗語言。

當客戶清楚了解規則時，他們更有可能參與。