---
title: 從 Shopify 移植
---

如果您的商店目前運行在 Shopify 上，Spwig 的移植向導可以通過連接到您在 Shopify Partners 仪表板中創建的小型自定義應用程序，來導入您的產品、客戶、訂單和內容。與大多數平台相比，Shopify 的平台限制更多，因此本指南的大部分內容是關於正確創建該應用程序的——一旦應用程序存在，連接本身只需五分鐘。

## 在開始之前

有兩個 Shopify 特有的限制足夠重要，需要在此特別指出，而不仅仅是後面表格中的內容：

> **重要事項：** Shopify 沒有評論 API，因此 **客戶評論完全不會被遷移**，無論您授予應用程序哪些權限。如果您需要評論，請從您使用的評論應用程序（如 Judge.me、Yotpo、Loox 等）中單獨導出它們，並自行導入到 Spwig 中。

> **重要事項：** 默認情況下，Spwig 只能讀取 **最近 60 天的訂單**。要遷移完整的訂單歷史記錄，您必須在創建應用程序時添加 `read_all_orders` 權限 — 請參閱下面的權限列表。這一點很容易被忽略，因為即使沒有這個權限，應用程序仍然可以連接並成功導入數據；只是會靜默地限制您的訂單歷史記錄回溯的範圍。

其他內容遷移效果良好：分類（作為集合 — 請參見下文）、產品、圖片、變體、客戶和地址、折扣以及博客內容。自定義字段是另一個明顯的缺口 — 請參見本指南末尾的 **Shopify 元字段**。

還請注意以下事項：

- 向導的 **導入稅務設置** 和 **導入運費區域和方法** 選項不會應用於導入的數據。

在遷移後自行在 Spwig 中設置稅率和運費 — 請參閱 [遷移後](after-migration-review)。
- 同一步驟中的 **價格調整** 選項 *確實* 對 Shopify 的導入生效，會在創建每個產品時更改其基本價格。

除非您有意圖地希望每個價格都進行調整，否則請保留其設置為 **無**。
- 您需要訪問 Shopify Partners 帳戶才能創建應用程序。

如果你還沒有一個，Shopify 讓你可以在 partners.shopify.com 免費創建一個。

## 創建 Shopify 應用

Spwig 會透過你創建並安裝在自己商店上的自定義應用來連接到 Shopify。這與產品內的 **Shopify API 設置指南** 對話框（透過向導第二步的 **打開設置指南** 開啟）相匹配，因此以下步驟與你會在那裡看到的完全一致 — 你可以選擇跟隨其中任何一個。

### 第 1 步：創建應用

1. 前往你的 [Shopify Partners 開發人員儀表板](https://dev.shopify.com/dashboard) 並打開 **應用程式**
2. 點擊 **創建應用程式**
3. 選擇 **從開發人員儀表板開始**
4. 輸入應用程式名稱：`Spwig Migration`
5. 點擊 **創建**

![在 Shopify 開發人員儀表板中創建 Spwig Migration 應用程式](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### 第 2 步：設置應用程式 URL 和權限範圍

在新應用程式的配置頁面中，在 **版本** 下設置：

- **應用程式 URL**：`https://shopify.dev/apps/default-app-home`
- **權限範圍**：`read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![設置應用程式 URL 和所需權限範圍](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| 權限範圍 | 給予 Spwig 的訪問權限 |
|---|---|
| `read_products` | 產品、變體、圖片、集合 |
| `read_customers` | 顧客姓名、電子郵件、地址 |
| `read_orders` | 最近 60 天的訂單 |
| `read_content` | 博客文章和頁面 |
| `read_discounts` | 折扣碼和規則 |
| `read_files` | 上傳的媒體文件 |

> **注意**：想要獲得完整的訂單歷史記錄，而不是僅僅最近 60 天？請在上面的權限範圍清單中添加 `read_all_orders`。

### 第 3 步：複製你的 Client ID 和 Secret

前往 **設定 > 憑證**，並複製那裡顯示的 **Client ID** 和 **Secret** — 你將在稍後粘貼到 Spwig 向導中。

![從應用程式的設定頁面複製 Client ID 和 Secret](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### 第 4 步：生成自定義分發連結

1. 進入 **分發**，並選擇 **自定義分發**
2. 輸入您的商店網域（例如，`yourstore.myshopify.com`）
3. 點擊 **生成連結**，然後 **複製** 它產生的安裝連結

![複製生成的自定義分發安裝連結](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### 第 5 步：在您的商店上安裝應用程式

在瀏覽器中打開您剛複製的安裝連結（請確保您已登入 Shopify 商店管理員），查看它請求的權限，然後點擊 **安裝**。

![在 Shopify 商店上安裝應用程式](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **重要提示：** 最後這一步很容易被忽略。生成安裝連結不會安裝應用程式 — 您必須實際打開連結並點擊安裝，否則 Spwig 將無法連接。如果下一節的連接測試失敗，這就是第一個需要檢查的地方。

## 將您的憑證複製到 Spwig

在 Spwig 管理介面中，前往 **資料導入與導出 > 開始新遷移**，在第 1 步選擇 **Shopify**，在第 2 步輸入：

- **商店網域** — `yourstore.myshopify.com`
- **客戶端 ID** — 從 設定 > 憑證
- **客戶端密碼** — 從 設定 > 憑證

如果您更想遵循產品內的逐步引導，而不是這份指南，請在這一步點擊 **開啟設定指南** — 它涵蓋了上述相同的五個步驟，並附有相同的螢幕截圖，全程約需 10 分鐘。

保留 **在繼續前測試連接** 的勾選狀態。如果您的應用程式範圍中缺少 `read_products`、`read_customers` 或 `read_orders`，Spwig 會在您繼續之前提醒您 — 返回 Shopify 仪表板中的應用程式版本頁面，新增缺少的範圍，儲存新版本，然後重試。

## 檢閱和選擇資料

第 3 步會從您的商店中提取即時數量，並顯示前五個產品的範例。與其他平台相比，有幾點看起來有所不同：

- **集合，而非分類** — Shopify 將產品組織為集合（Collections），而非分類（categories），且集合不支援巢狀，因此層級導入會是扁平的。

如果您的 Shopify 商店使用集合來代表分類樹，請計畫在導入後使用 Spwig 的分類管理員重建該結構。
- **折扣，而非優惠券** — Shopify 的折扣碼和規則會導入為 Spwig 的折扣。
- **沒有評論欄位** — 因為 Shopify 沒有評論 API，因此這種資料類型在這步完全不會出現，與 WooCommerce 或 CSV 導入不同。

**導入選項** 在其他平台上的運作方式相同：**跳過現有項目**（開啟）會根據 SKU 和電子郵件進行比對，以避免重複；**導入產品圖片**（開啟）會較慢，但建議使用；**盡可能保留原始 ID**（關閉）應保持關閉，除非您有特定理由要更改它；**批次大小** 預設為 25。

## Shopify 元資料欄位

如果您使用 Shopify 元資料欄位來儲存產品、客戶或訂單的額外資料，請注意 Spwig 不會偵測或讀取它們 — 與 WooCommerce 不同，Shopify 導入沒有自訂欄位對應步驟。任何您儲存在元資料欄位中的資料，都需要在遷移後手動重新輸入到 Spwig 中，使用 [自訂欄位](migration-field-mapping)。因此，在開始遷移前，值得從 Shopify 導出一份您的元資料欄位及其值的清單。

## 執行導入

一旦您審核完第三步，就可以開始導入。導入會在後台執行 — 您可以關閉瀏覽器視窗，導入仍會繼續。第五步會顯示即時進度，每個資料類型一行，並有可展開的活動日誌。

第六步會顯示您的結果：已導入、跳過或失敗的內容，以及如果在導入的內容中發現了對舊的 `myshopify.com` 域名的內部連結，會顯示一個 **連結重寫** 工具。

```python
# 示例代码块，保持原样
print("Hello, Spwig!")
```

![示例图片](/static/core/admin/img/example.png) 這是一張示例圖片。

仔細查看摘要，然後按照 [遷移後](after-migration-review) 中的清單逐步進行 — 它涵蓋驗證您的資料、重建任何收藏層級、設定稅率和運費（向導不會為您設定這些），以及重新輸入儲存在 metafields 中的任何內容。

## 從 Shopify 刪除應用程式

確認遷移成功完成後，返回 Shopify 管理介面的 **應用程式** 頁面，或 Partners 仪表板，並刪除 Spwig Migration 應用程式（或至少從您的商店中卸載它）。遷移完成後，沒有理由讓應用程式保留對商店資料的讀取權限。

## 小提示

- **預設情況下訂單歷史記錄是有限的** — 如果您需要超過最近 60 天的訂單，請在生成安裝連結之前，而不是之後，將 `read_all_orders` 加入範圍清單。
- **評論需要單獨導出** — 在遷移之前就做好規劃，因為完全無法透過向導將評論遷移過來。
- **生成連結與安裝應用程式並不相同** — 始終完成步驟 5 並點擊安裝，否則 Spwig 的連線測試將會失敗。
- **收藏會以扁平方式導出** — 如果您的分類結構對導覽或 SEO 有影響，請預留時間在導入後在 Spwig 中重建層級。
- **先導出 metafields** — Spwig 無法讀取它們，因此如果您之後需要這些資料，請在開始遷移前從 Shopify 中導出 metafields。
- **驗證後刪除應用程式** — 不要在遷移後保留指向舊商店的活躍整合。