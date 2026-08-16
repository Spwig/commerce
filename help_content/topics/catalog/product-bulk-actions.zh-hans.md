---
title: 产品批量操作
---

在 **产品** 列表中，您可以一次性对多个产品执行操作，而不是逐一打开每个产品。在产品网格上方的工具栏中的 **批量操作** 下拉菜单中，您可以发布或取消发布产品，将其设为特色或取消特色，将数据导出为 CSV，检查哪些产品已准备好进行国际运输，或删除它们——所有操作均可在一步中完成。

导航至 **产品 > 所有产品** 以使用这些操作。

![显示三个产品卡片已选中，且 **批量操作** 下拉菜单显示所有选项的 **产品** 列表工具栏，包括导出海关数据 (CSV) 和检查国际运输准备情况](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## 运行批量操作

1. 如果需要，使用筛选面板或 **搜索** 框缩小您想要的产品范围
2. 勾选每个您想包含的产品卡片左上角的复选框 —— **批量操作** 会显示已选产品的数量
3. 从 **批量操作** 下拉菜单中选择一个操作
4. 点击 **应用**

更改或导出数据的操作会立即执行；由于 **删除所选** 是唯一一个从列表本身无法轻松撤销的操作，因此会首先要求您确认。

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

这些字段来自产品表单的 **国际运输/海关** 部分。

如果某个产品缺少其中一个字段，在导出时其对应的列将留空 - 在依赖此文件进行实际运输之前，请在产品上填写缺失的数据。

## 检查国际运输准备情况

在不逐个打开每个产品或等待完整 CSV 导出的情况下，使用此功能对一批产品进行审计，以确定是否可以开始国际运输。

选择产品，选择 **检查国际运输准备情况**，然后点击 **应用**。Spwig 会针对三个必填字段 - **HS 编码**、**原产国** 和 **海关单价** - 检查每个选中的产品，并显示一个总结结果的通知：

- 如果每个选中的产品都填写了这三个字段，您将看到确认信息，显示所有产品都已准备就绪。
- 如果某些产品缺少数据，通知将报告有多少个已准备就绪，有多少个未准备就绪，并列出每个未准备就绪的产品及其缺失的字段（例如，“蓝色陶瓷杯（缺失：hs_code，country_of_origin）”）。如果超过 10 个产品缺少数据，通知将列出前 10 个，并告知还有多少个未列出。

此操作仅读取数据 - 它不会更改产品上的任何内容，因此在您填写整个目录的海关信息时，可以安全地频繁运行此操作。

**出口许可证编号** 和 **出口许可证到期日** 不属于准备情况检查的一部分。它们仅适用于受控或受限商品，因此一个产品可以在没有这些信息的情况下“准备就绪”进行国际运输。

## 提示

保留所有 markdown 格式、图片路径、代码块和术语。

- 在您收到第一个国际订单之前，对整个目录（或一次一个类别）运行 **检查国际运输准备状态** —— 这比在货物已经到达边境时发现缺少 HS 编码要快得多。
- 保留 **导出海关数据（CSV）** 供经纪人和承运商使用，并使用 **检查国际运输准备状态** 作为您内部的待办清单 —— CSV 是一份记录，准备状态检查是一份待办清单。
- 在添加新产品时，在产品表单（在 **国际运输/海关** 下）填写 **HS 编码**、**原产国** 和 **海关单价**，这样您以后就不会需要批量处理这些信息。
- 当您滚动时，产品网格会自动加载更多产品（无限滚动），并且您的复选框选择会在新产品加载时保留 —— 您可以滚动以构建一个较大的选择集，然后再应用操作。

更改过滤器或重新加载页面会清除您的选择，因此请在调整过滤器之前应用操作。
- **设为草稿** 是一种快速方式，可以一次将多个产品从商店中移除 —— 例如，在库存重新计算之前 —— 而不会改变它们的其他任何内容。