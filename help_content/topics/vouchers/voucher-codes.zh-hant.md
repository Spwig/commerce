---
title: 優惠券代碼
---

優惠券代碼讓您可以創建折扣碼、優惠券和禮品卡，讓客戶在結帳時輸入以獲得折扣。請前往管理側邊欄的 **Marketing > Vouchers**。

![Voucher list](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Voucher Dashboard

優惠券頁面顯示一個概覽，包含：

- **Stats Cards** — 啟用、停用、兌換次數和總共的優惠券數量
- **Filters** — 透過代碼或名稱搜尋，過濾類型、狀態和範圍
- **Voucher Cards** — 每個優惠券都會顯示使用情況和狀態詳情

## Creating a Voucher

1. 點擊頂部右側的 **+ Add Voucher**
2. 填寫優惠券詳情：
   - **Code** — 客戶在結帳時輸入的代碼（例如："SAVE20", "FREESHIP"）
   - **Name/Description** — 為您參考的內部描述
   - **Discount Type** — 選擇折扣的應用方式
   - **Discount Value** — 折扣金額或百分比
3. 設置使用規則：
   - **Usage Limit** — 最大總兌換次數（0 = 無限制）
   - **Per-Customer Limit** — 每位客戶的最大使用次數
   - **Minimum Order Value** — 所需的最低購物車總額
4. 設置 **範圍**：
   - **Entire Cart** — 折扣適用於整筆訂單
   - **Specific Products** — 僅適用於選定的商品
   - **Specific Categories** — 僅適用於選定類別中的商品
5. 可選設定到期日：
   - **Expiry Date** — 優惠券停止使用的日期
6. 點擊 **Save**

## Voucher Types

| Type | Description | Example |
|------|-------------|---------|
| **Fixed Amount** | 扣除固定金額 | $20 折扣 |
| **Percentage** | 扣除總金額的百分比 | 15% 折扣 |
| **Free Shipping** | 移除運費 | 任何訂單免運費 |

## Managing Vouchers

### Voucher Cards

每個優惠券卡片顯示：
- **Code** — 以粗體顯示的優惠券代碼
- **Description** — 優惠券的功能
- **Status badge** — 啟用或停用
- **Discount details** — 類型和價值（例如："$ 20.00" 或 "15.00%"）
- **Scope** — 是否適用於整筆購物車或特定商品
- **Usage count** — 優惠券已被兌換的次數
- **Created date** — 優惠券創建的日期
- **Expiry** — 到期日或 "No expiry"

### Voucher Actions

每個卡片都有操作按鈕：
- **Edit** — 修改優惠券設定
- **View History** — 查看兌換歷史
- **Delete** — 刪除優惠券

### Filtering Vouchers

使用篩選欄來查找特定優惠券：
- **Search** — 透過代碼、名稱或描述查找
- **Type** — 固定金額、百分比或免運費
- **Status** — 啟用或停用
- **Scope** — 整筆購物車或特定商品

## Bulk Voucher Generation

對於大型活動，您可以批量生成優惠券：
1. 系統會自動生成唯一的代碼（例如："COUPONX1600406498"）
2. 設置所有生成優惠券的通用參數
3. 透過電子郵件、社群媒體或印刷分發代碼

## Customer Experience

當客戶擁有優惠券代碼時：
1. 他們前往 **checkout**
2. 在 **discount code** 欄位輸入代碼
3. 如果優惠券有效，折扣會立即套用
4. 訂單摘要會更新以顯示折扣

如果優惠券無效（過期、使用次數達上限、未達最低金額），客戶會看到明確的錯誤訊息。

## Tips

- 為市場活動使用易記的代碼（例如："SUMMER20" 而不是隨機字串）。
- 設置每位客戶的使用次數上限，以防止高價值折扣被濫用。
- 使用最低訂單金額來維持利潤（例如："$10 折扣適用於 $50 以上的訂單"）。
- 在儀表板上監控兌換次數，以追蹤活動效果。
- 創建有時間限制的優惠券以營造緊迫感（例如："僅限本週末有效"）。
- 使用啟用/停用狀態來暫停優惠券而不刪除它們。
