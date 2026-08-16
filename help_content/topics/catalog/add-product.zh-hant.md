---
title: 新增商品
---

<!-- screenshots-needed:
- url: /admin/catalog/product/<id>/change/
  filename: inventory-tab.webp
  description: 库存標籤，捲動以顯示實體屬性、運費，
    和預購卡一起（需要勾選需要運費，選擇首選運費包裝，
    和勾選預購並填入發行日期和訊息，讓所有新欄位一次可見）。
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
  notes: 取代現有的 inventory-tab.webp，這張圖片在運費
    和預購卡出現之前就已存在，現在已不符合即時表單。
- url: /admin/catalog/product/<id>/change/
  filename: tags-card.webp
  description: 基本資訊標籤，捲動至標籤卡，顯示已套用幾個標籤
    在商品的標籤選擇器中。
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
- url: /admin/catalog/product/<id>/change/
  filename: advanced-tab.webp
  description: 進階標籤顯示商品頁面設定卡（頁面範本下拉選單選擇非預設選項）
    和下方的技術細節卡。
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
-->

此指南將引導您完成在商店中建立新商品的過程。商品表單分為多個部分，涵蓋基本資訊、媒體、定價、庫存、SEO 等 - 您可以一次填寫所有內容，或稍後再回來完成某些部分。

## 開始

從側邊欄導覽至 **Products > All Products** 以查看您的商品目錄。點擊右上角的 **+ 新增商品** 按鈣以開啟商品建立表單。

![商品清單頁面](/static/core/admin/admin/img/help/add-product/product-list-page.webp)

## 基本資訊

**基本資訊** 區域是您定義商品核心身分的地方。

![新增商品表單](/static/core/admin/admin/img/help/add-product/add-product-form.webp)

### 必填欄位

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

- **名稱** — 顯示給客戶的產品名稱。

點擊地球圖示以新增其他語言的翻譯。
- **Slug** — 友好網址的名稱（自動產生）。

如需自定義，請進行調整。
- **SKU** — 您的內部庫存單位代碼。
- **產品類型** — 選擇：簡單、變動、數位、套裝組合、禮品卡、自定義、可配置或預訂。
- **分類** — 將產品分配到某個分類中，以便進行組織和商店目錄導航。

### 狀態和可見性

位於表單底部的 **狀態** 部分：

- **狀態** — 在編輯時設為 **草稿**，準備銷售時設為 **已發佈**，或設為 **已停售** 以標示不再提供的產品。
- **是否為特色產品** — 勾選以在您的商店目錄中強調此產品。
- **是否為數位產品** — 勾選以標示此產品包含數位下載（檔案、許可證）。可以與任何產品類型結合使用。
- **隱藏於商店目錄** — 在目錄清單中隱藏此產品，同時保持其作為組裝選項或套裝組合組件的可用性。

### 可選欄位

- **品牌** — 如果適用，關聯至一個品牌。
- **標籤** — 在此選項卡下方的 **標籤** 卡片中指派一個或多個標籤。標籤與集合不同——它們是用於組織和過濾產品的快速、自由格式標籤，而不是商品陳列的分組。開始輸入以搜尋現有標籤，或輸入新名稱以即時建立一個新標籤。請參閱 **產品標籤** 助手主題以直接建立、重新命名和批量刪除標籤。

### 產品描述

- **簡短描述** — 出現在產品清單和卡片中。請保持簡潔且有說服力。
- **完整描述** — 顯示在產品詳情頁的詳細產品描述。使用豐富文字編輯器來新增格式、圖片、影片和表格。

兩個描述欄位都支援翻譯功能 — 點擊地球圖示以提供其他語言的內容。

### 特性和規格

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

The **Product Details** section contains two structured data fields:

- **Features** — Key-value pairs for product highlights (e.g., "Battery Life: 20 hours").
- **Specifications** — Technical details for the specifications tab on the product page (e.g., "Processor: Intel i7").

## Media

The **Media** section lets you manage product images using the integrated Media Library.

![Media tab](/static/core/admin/img/help/add-product/media-tab.webp)

1. Click **+ Add Images from Media Library** to open the media picker.
2. Select existing images or upload new ones directly.
3. Drag images to reorder them — the **first image** becomes the primary product image shown in listings and cards.

The **Gallery Type** field, in the **Gallery Settings** card below the image list, controls how images are displayed on the storefront: Standard Gallery, Carousel, Grid Layout, Zoom Gallery, or 360° View.

## Pricing

Set your product's pricing and configure sales.

![Pricing tab](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Regular pricing

- **Regular Price** — The standard retail price customers will see. The currency is set alongside the price amount.
- **Cost** — Your cost of goods, used for profit calculations. This is never shown to customers.

### Sale settings

Configure temporary discounts:

- **Sale Type** — Choose from: No Sale, Fixed Sale Price, Amount Off, or Percentage Off.
- **Sale Value** — The discount amount or percentage.
- **Sale Start Date / Sale End Date** — Schedule when the sale activates and expires. Leave empty for an immediate start or no end date.

### Multi-currency pricing

If multi-currency is enabled on your store, a **Pricing Strategy** field appears:

- **Dynamic Pricing** — Prices in other currencies are automatically calculated using your configured exchange rates.
- **Fixed Pricing** — Set a specific price for each currency independently using the **Multi-Currency Pricing** section that appears below.

## Inventory

Preserve all markdown formatting, image paths, code blocks, and technical terms.

管理庫存數量、運輸行為和實體產品屬性。

![庫存標籤](/static/core/admin/img/help/add-product/inventory-tab.webp)

### 庫存管理

- **追蹤庫存** — 啟用以追蹤庫存數量（預設已啟用）。
- **低庫存門檻** — 當庫存低於此數字時收到通知（預設：5）。
- **允許預購** — 啟用以在庫存不足時接受訂單。
- **庫存不足時的動作** — 當此產品庫存不足時覆蓋網站或分類的預設行為：隱藏它、顯示為不可用、顯示「通知我」按鈕，或允許預購。

庫存數量會根據倉庫進行管理。保存產品後，使用表單底部的 **庫存項目** 部分（或導航至 **產品 > 庫存項目**）來設置每個倉庫地點的數量。

### 實體屬性

輸入產品的重量（kg）和尺寸（長度、寬度、高度，單位：cm），以進行準確的運輸計算。

### 運輸

- **需要運輸** — 該產品是否需要運送到客戶。預設為實體產品啟用；你的 storefront 和結帳會使用它來判斷是否收集運輸地址並為訂單提供運費估算。Spwig 會自動關閉數位產品、預訂和禮品卡產品的此功能，因為這些產品從來不會被寄送 —— 你不需要（也不能）重新啟用此功能。對於外觀類似數位產品的實體產品，請保持此選項為已勾選，例如一張列印的禮品卡，會以盒子運送。
- **首選運輸包裝** — 選擇你已設定的運輸包裝之一。設定後，會使用包裝本身的尺寸進行運費計算，而不是使用此產品的重量和尺寸 —— 當產品始終使用相同的標準盒子或信封時非常有用。留空以使用產品本身的實體屬性。在 **運輸 > 包裝** 下管理可用的包裝。

### 預購

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

使用 **預購** 卡片在商品沒有庫存時進行銷售 - 對於您希望提前開始接受訂單的即將推出的產品非常有用：

- **是否為預購** — 啟用此選項，讓顧客即使在商品缺貨時也能購買此商品。
- **預購發售日期** — 顯示給顧客的預期可用日期。
- **預購訊息** — 顯示給顧客的短自定訊息，最多 200 個字元（例如："預計 2026 年 3 月發貨"）。

### 產品識別碼

用於市場平台清單和庫存系統的標準產品代碼：

- **GTIN** — 全球貿易項目編號
- **EAN** — 歐洲產品編號
- **UPC** — 統一產品代碼（美國）
- **ISBN** — 用於書籍
- **ASIN** — 亞馬遜識別碼
- **MPN** — 製造商零件編號

### 國際運輸 / 海關

適用於國際運輸（展開 **國際運輸 / 海關** 部分）：

- **HS Code** — 通用系統分類代碼
- **原產國** — 產品製造國家
- **海關單元價格** — 海關申報單元價格
- **出口許可編號** — 僅適用於受控或限制物品
- **出口許可有效期** — 出口許可的有效期

## SEO

優化您的產品的搜索引擎可見度。

![SEO 標籤](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Meta 標題** — 在搜索引擎結果中顯示的標題。點擊地圖圖示進行翻譯。
- **Meta 描述** — 搜索結果的簡短描述（最多 160 個字元）。點擊地圖圖示進行翻譯。
- **自動產生 SEO** — 勾選以在保存產品時自動產生 SEO 內容。

即時 **搜尋結果預覽** 顯示您的產品在 Google 搜索結果中將如何顯示。

## 產品頁面設定

在 **高階** 標籤中，**產品頁面設定** 卡片讓您控制此產品 storefront 頁面的外觀：

- **頁面模板** — 覆蓋網站預設的商品頁面佈局，為此商品選擇：經典、全寬度、相册焦點或數位。

將其設為 **使用網站預設** 以繼承設計設定中指定的佈局 — 大多數商品應保持預設，以便模板變更自動套用。
- **顯示相關商品** — 在頁面底部顯示相關商品。
- **顯示評論** — 顯示客戶評論。
- **顯示規格** — 顯示規格選項卡。

**相册類型** 字段 — 控制商品圖片顯示方式（標準相册、滑動圖片、網格佈局、放大相册或360°檢視） — 請在 **媒體** 標籤中單獨設定。

## 銷售管道

**銷售管道** 字段（在狀態部分）控制商品可以銷售的地點：

- **所有管道** — 線上和實體店（POS）均可銷售。
- **僅限在線** — 不可在POS終端銷售。
- **僅限實體店** — 不在線上市；僅可在您的實體店購買。

也有一個 **條碼** 字段用於POS條碼掃描。

## 保存您的商品

當您準備好時，請使用右上角的保存按鈕。當您將狀態設為 **已發佈** 後，商品將會出現在 storefront 中。

## 提示

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

- 以 **草稿** 状态開始，這樣您可以在客戶看到產品之前完善它。
- 上傳多張圖片 —— 具有多張照片的產品轉化率更高。
- 填寫 **SEO** 字段以提高在搜索引擎中的可發現性。
- 使用 **分類**, **品牌** 和 **標籤** 來幫助客戶導覽您的目錄。
- 對於變量產品（例如不同尺寸或顏色），請選擇 **變量產品** 類型，並在保存後新增變體。
- 使用 **特點** 和 **規格** 來新增結構化產品資料，這些資料會在產品頁面的專門標籤中顯示。
- 如果 **需要運輸** 選項無法保持勾選狀態，請查看 **產品類型** —— Spwig 會自動關閉數位、預訂和禮品卡產品的運輸功能，因為這些產品都不會被實際寄送。
- 為始終使用相同盒子運送的產品設置 **預ferred 運輸包裝** —— 這可以節省您不必始終同步該產品的重量和尺寸與實際使用的盒子。