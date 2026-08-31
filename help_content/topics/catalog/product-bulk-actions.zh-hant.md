---
title: 商品批量操作
---

在 **商品** 列表中，您可以一次性对多个商品进行操作，而不是逐一打开每个商品。在商品网格上方的工具栏中的 **批量操作** 下拉菜单中，您可以发布或取消发布商品，将其设为特色或取消特色，将数据导出为 CSV，检查哪些商品已准备好进行国际运输，或删除它们——所有操作均可在一步中完成。

导航至 **商品 > 所有商品** 以使用这些操作。

![显示三个商品卡片已选中，并且 **批量操作** 下拉菜单显示所有选项的 **商品** 列表工具栏，包括导出海关数据 (CSV) 和检查国际运输准备情况](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## 运行批量操作

1. 如果需要，使用筛选面板或 **搜索** 框缩小您想要的商品范围
2. 勾选每个您想包含的商品卡片左上角的复选框 —— **批量操作** 会显示已选商品数量的实时统计
3. 从 **批量操作** 下拉菜单中选择一个操作
4. 点击 **应用**

更改或导出数据的操作会立即执行；由于 **删除所选** 是唯一一个从列表本身无法轻松撤销的操作，因此会先要求您确认。

## 可用操作

| Action | What it does |
|--------|---------------|
| **Mark as Published** | Sets the selected products' status to Published so they're visible on the storefront. |
| **Mark as Draft** | Sets the selected products' status to Draft, hiding them from the storefront while you keep editing. |
| **Mark as Featured** | Enables **Is Featured** on the selected products. |
| **Remove Featured** | Disables **Is Featured** on the selected products. |
| **Export to CSV** | Downloads a CSV of the selected products' ID, name, SKU, status, featured flag, and price. |
| **Export Customs Data (CSV)** | Downloads a CSV of customs information for the selected products. See below. |
| **Check International Shipping Readiness** | Shows a summary of which selected products have the customs data they need for international shipments. See below. |
| **Delete Selected** | Moves the selected products to the recycle bin, after a confirmation prompt. |

## Export Customs Data (CSV)

Use this when you need a customs declaration sheet to hand to a freight forwarder, courier, or customs broker — for example, before a large international shipment, or when setting up a new carrier that asks for HS codes and origin data up front.

Select the products, choose **Export Customs Data (CSV)** from the dropdown, and click **Apply**. Spwig downloads a file named `product_customs_data.csv` with one row per product and these columns:

| Column | Source |
|--------|--------|
| **SKU** | The product's SKU |
| **Name** | The product name |
| **HS Code** | The Harmonized System classification code |
| **Country of Origin** | Where the product is manufactured |
| **Customs Unit Price** | The declared value per unit for customs |
| **Export License** | The export license number, if the product requires one |
| **License Expiry** | The export license's expiration date, if set |
| **International Ready** | `Yes` or `No` — whether the product has the minimum data required for international shipping (see below) |

Preserve all markdown formatting, image paths, code blocks, and technical terms.

這些欄位來自產品表單的 **國際運輸 / 海關** 部分。

如果某個產品缺少其中一個欄位，在匯出時該欄位將留空 - 在依賴此檔案進行實際運輸前，請在產品中填寫缺失的資料。

## 檢查國際運輸準備狀態

在不打開每個產品或等待完整 CSV 匯出的情況下，使用此功能審計一批產品，以準備它們的國際運輸。

選擇產品，選擇 **檢查國際運輸準備狀態**，然後點擊 **套用**。 Spwig 會根據三個必要欄位 - **HS 稅則編碼**、**原產國** 和 **海關單價** - 檢查每個選中的產品，並顯示總結結果的通知：

- 如果每個選中的產品都填寫了所有三個欄位，您將看到確認所有產品都已準備好。
- 如果有些產品缺少資料，通知會報告有多少個已準備好，有多少個未準備好，並列出每個未準備好的產品以及其缺失的欄位（例如，「藍色陶瓷杯（缺失：hs_code, country_of_origin）」）。如果超過 10 個產品缺少資料，通知會列出前 10 個，並告訴您還有多少個。

此操作僅讀取資料 - 它不會變更產品上的任何內容，因此在您填寫目錄中的海關資訊時，可以安全地經常運行此操作。

**出口許可編號** 和 **出口許可到期日** 不屬於準備狀態檢查的一部分。它們僅適用於受控或限制物品，因此產品可以「準備好」國際運輸而沒有它們。

## 提示

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

- 在您收到第一份国际订单之前，对整个商品目录（或一次一个类别）运行 **检查国际运输准备状态** —— 比在货物已经到达边境时才发现缺少 HS 编码要快得多。
- 保留 **导出海关数据 (CSV)** 供经纪人和承运商使用，并使用 **检查国际运输准备状态** 作为您内部的待办清单 —— CSV 是一份记录，准备状态检查是一份待办清单。
- 在添加新产品时，在产品表单（在 **国际运输 / 海关** 下）填写 **HS 编码**、**原产国** 和 **海关单价**，以免之后需要批量处理。
- 当您滚动时，产品网格会自动加载更多产品（无限滚动），并且您的复选框选择会在新产品加载时保留 —— 您可以滚动以构建大量选择，然后再应用操作。

更改过滤器或重新加载页面会清除您的选择，因此请在调整过滤器之前应用操作。
- **设为草稿** 是一种快速方式，可一次将多个产品从商店中移除 —— 例如，在库存重新计算之前 —— 而不会更改它们的其他任何内容。