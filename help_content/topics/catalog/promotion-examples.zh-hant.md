---
title: 促銷範例
---

本指南展示了如何配置不同類型的促銷活動的具體範例。每個範例都包含在促銷向導中需要輸入的精確欄位值，讓您可以跟著操作或根據您的商店進行調整。

![Promotion Card](/static/core/admin/img/help/promotion-examples/promotion-card.webp)

## 範例：類別的百分比折扣

**情境：** 冬季清倉期間所有鞋子享有30%折扣。

前往 **Marketing > Sales & Promotions** 並點擊 **+ Create Promotion**。在向導的每個步驟中輸入以下值：

| Step | Field | Value |
|------|-------|-------|
| Basics | Name | Winter Clearance — 30% Off Shoes |
| Basics | Description | 結束季節的鞋子清倉 |
| Basics | Active | 勾選 |
| Discount | Type | Percentage Off |
| Discount | Value | 30 |
| Schedule | Start Date | 2026年1月15日 |
| Schedule | End Date | 2026年2月28日 |
| Products | Apply To | Categories |
| Products | Selected | 鞋子、靴子、涼鞋 |

這會創建一個有時間限制的促銷活動，自動對所選類別中的每件商品進行折扣。價值120美元的一雙靴子將變成84美元，價值60美元的一雙涼鞋將變成42美元。

## 範例：系列商品固定金額折扣

**情境：** 對「夏季必備」系列的商品減15美元。

| Step | Field | Value |
|------|-------|-------|
| Basics | Name | Summer Essentials — $15 Off |
| Basics | Active | 勾選 |
| Discount | Type | Amount Off |
| Discount | Value | 15.00 |
| Schedule | Start Date | 2026年6月1日 |
| Schedule | End Date | (空白 — 無限期) |
| Products | Apply To | Collections |
| Products | Selected | Summer Essentials |

> **注意：** 15美元的折扣會針對每個符合條件的商品單獨應用。價值50美元的商品會變成35美元，價值30美元的商品會變成15美元。將結束日期留空表示促銷活動會無限期進行，直到您手動停用為止。

## 範例：清倉固定售價

**情境：** 將所有清倉商品設定為9.99美元。

| Step | Field | Value |
|------|-------|-------|
| Basics | Name | 最後清倉 — 所有商品9.99美元 |
| Basics | Active | 勾選 |
| Discount | Type | Fixed Sale Price |
| Discount | Value | 9.99 |
| Schedule | Start Date | (今天) |
| Products | Apply To | Collections |
| Products | Selected | 最後清倉 |

> **注意：** 固定售價會設定確切的售價，不論原價是多少。價值75美元的商品和價值25美元的商品都會變成9.99美元。當您希望所有商品都以相同價格出售時，例如清倉專區或統一售價，請使用此功能。

![Category Promotion](/static/core/admin/img/help/promotion-examples/category-promotion.webp)

## 選擇正確的折扣類型

| Type | How It Works | Best For | Example |
|------|-------------|----------|---------|
| **Percentage Off** | 以百分比降低價格 | 全面促銷，產品價格各不相同 | 20%折扣 — 100美元變成80美元，50美元變成40美元 |
| **Amount Off** | 減去固定金額 | 具體節省金額的促銷活動 | 15美元折扣 — 100美元變成85美元，50美元變成35美元 |
| **Fixed Sale Price** | 設定確切的售價 | 清倉、統一售價、『所有商品X美元』 | 9.99美元 — 無論原價是多少，所有商品都變成9.99美元 |

## 選擇正確的目標

| Target | How It Works | Best For |
|--------|-------------|----------|
| **All Products** | 應用於商店中的所有商品 | 全站促銷、全店活動 |
| **Categories** | 應用於所選類別中的所有商品 | 部門促銷、按類型進行的季節性清倉 |
| **Brands** | 應用於所選品牌的所有商品 | 品牌合作、品牌專屬活動 |
| **Collections** | 應用於所選系列中的所有商品 | 精選促銷、主題性銷售 |
| **Products** | 應用於個別選中的商品 | 手選優惠、限量選擇 |

## 設定促銷活動時間表

設定促銷活動時間表的三種常見模式：

| Pattern | Start Date | End Date | Use Case |
|---------|-----------|----------|----------|
| **Immediate, ongoing** | Today | (empty) | 永久性價格減免、長期促銷 |
| **Date range** | Future date | Future date | 季節性活動、節日促銷 |
| **Future start, no end** | Future date | (empty) | 從特定日期開始的永久性新價格 |

設定未來的開始日期會創建一個預定的促銷活動。它會出現在促銷儀表板的 **Scheduled** 索引標籤中，並在日期到來時自動啟動。將結束日期留空表示促銷活動會保持啟用狀態，直到您手動停用為止。

## 小技巧

- **使用描述性的名稱** — 在名稱中包含折扣金額和目標（例如，『夏季20%鞋子折扣』），這樣您可以在儀表板上快速識別促銷活動。
- **檢查受影響商品數量** — 檢查步驟會顯示有多少商品將被折扣。如果數字看起來不正確，請返回並檢查您的目標設定。
- **從小開始** — 如果您不確定折扣效果，請從較小的百分比開始，如有需要再增加。
- **使用固定金額折扣進行市場推廣** — 『15美元折扣』是一個具體的節省金額，容易在廣告和電子郵件活動中傳達。
- **使用百分比折扣來確保公平** — 百分比折扣會根據價格調整，讓不同價格點的節省比例相同。