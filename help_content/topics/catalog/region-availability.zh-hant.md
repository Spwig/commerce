---
title: 地區可用性
---

地區可用性控制您的銷售區域中哪些產品可以出售，以及這些產品在這些區域之外的購物者如何體驗您的目錄。當您僅有某些國家的許可證時，當庫存保留給本地市場時，或者當您按地區逐步推出新產品時，請使用此功能。

這基於**銷售區域**，它將國家分組為名稱市場（請參閱銷售區域指南以了解設置方法）。一旦您的區域存在，您可以限制單個產品到它們，並決定受限制的產品在無法購買它們的購物者面前如何顯示。

## 將產品限制為特定區域

每個產品在其編輯頁面上都有**地區可用性**設置。打開**產品 > 所有產品**，選擇一個產品，並在**狀態**部分中找到它，與**狀態**、**特色**和**從商店front hide**一起。

![產品編輯表單的狀態部分，其中地區可用性下拉選單設置為「僅在所選區域」，與特色和從商店front hide一起](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| 選項 | 代表含義 |
|--------|---------------|
| **在所有區域都可用** | 沒有限制。產品在所有地方都可出售。這是每個產品的預設值。 |
| **僅在所選區域** | 允許清單。產品僅在您在下面選擇的區域中出售——其他所有地方，它都被視為不可用。 |
| **所有區域，除了所選區域** | 阻止清單。產品在所有區域都可出售，*除了*您在下面選擇的區域。 |

### 選擇區域

在狀態部分下方，標題為**地區可用性（所選區域）**的表格列出了上述模式適用的區域。

1. 將**地區可用性**設置為**僅在所選區域**或**所有區域，除了所選區域**。
2. 在**地區可用性（所選區域）**表格中，點擊**新增另一個區域**並選擇一個銷售區域。
3. 為每個您要新增的區域重複此步驟。
4. 點擊**儲存**。

[The "Region availability (selected regions)" inline table with North America and Europe rows added](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

如果 **Region availability** 設定為 **Available in all regions**，則此表格中的任何內容都會被忽略 —— 如果您想移除限制但不刪除欄位，請先清除模式下拉選單。

若要查看目錄中所有產品的區域規則清單（便於審計多個產品），請前往 `/admin/catalog/productregionvisibility/` 的 **Product Region Visibility**。

## 顯示 shoppers 哪些產品無法運送到

當 shopper 的區域與產品的可用性規則不匹配時，您可以在 **Stock Display Settings** 的 **Region Availability** 節控製他們看到的內容。此頁目前還沒有側邊欄快捷方式 —— 請直接訪問 `/admin/catalog/stockdisplaysettings/` 開啟它。

![Stock Display Settings，Region Availability 節 —— Region-restricted display 下拉選單，設定為「Show, marked as unavailable」](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| 選項 | shoppers 看到的內容 |
|--------|-------------------|
| **Show, marked as unavailable**（預設） | 產品仍然出現在清單中，顯示「Unavailable」徽章，並在「Add to Cart」按鈕的位置顯示「Does not ship to [region]」訊息。清單頁面頂部也會顯示橫幅（「Some products don't ship to [destination]」），並包含連結以過濾出僅運送到那裡的產品。 |
| **Hide from listings** | 針對該區域的 shopper，產品將從清單和搜尋結果中完全移除。 |

![Storefront 產品清單運送到歐洲 —— 網格上方的「Some products don't ship to Europe」橫幅，以及標記為「Unavailable」的產品卡和「Does not ship to Europe」訊息](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

一個受限制商品的專屬頁面在顧客直接訪問時（例如，從共享連結或搜尋引擎結果）始終會顯示「此商品不運送到[地區]」的提示——無論你選擇上方的哪個清單選項，都會套用，因為直接連結會完全跳過清單頁面。

## 允許顧客選擇或發現他們的地區

Spwig 可以自動檢測顧客的地區並提供切換選項，你也可以新增選擇器，讓顧客隨時手動變更。

### 開始前

你需要設定兩項以正確運作地區檢測和切換：

1. **銷售區域** — 每個區域中的國家以及每個區域的預設貨幣。如果你在側邊欄的 **庫存** 下沒有看到 **銷售區域**，請在 **設定 > 商店設定 > 電商** 下啟用 **啟用多倉庫** 以顯示選單連結（你不需要實際使用多個倉庫——此設定僅解鎖選單項目）。你可以直接前往 `/admin/catalog/salesregion/`。
2. **運送國家** — 你商店實際運送的國家。這些通常已經設置好了：你加入運送區域的每個國家也會自動加入這裡。要審查或手動調整清單，請直接打開 `/admin/shipping/shippingcountry/`（目前還沒有側邊欄連結）。

### 自動地區確認

Spwig 從顧客的地理位置檢測其地區並自動套用。當這使他們處於你商店的預設（主要）市場以外的地區——且你有兩個或更多活躍的銷售區域——Spwig 會在他們第一次訪問時顯示確認訊息，讓他們知道他們所在的地區並可以切換：

> **我們已將你的地區設為 [區域] **
> 我們從你的位置中選擇了這個地區，以便你看到正確的產品和價格。不對？選擇你的國家。
> 運送到：[國家選擇器]  **[繼續瀏覽] **

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

![The "We've set your region to North America" confirmation modal on the storefront, with a "Ship to" country picker and a Keep browsing button](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Choosing a different country in the picker switches them immediately. Dismissing it or clicking **Keep browsing** keeps their current region, and they won't be asked again on that browser. Visitors who are already in your default region aren't shown the confirmation at all.

### Adding a Ship-To Selector to your header or footer

If you'd rather let shoppers change region themselves at any time (instead of relying only on the automatic prompt), add the **Ship-To Selector** widget to your header or footer.

1. Navigate to **Design > Header Builder** (or **Footer Builder**).
2. Drag the **Ship-To Selector** widget from the Widget Library into a row.
3. Click **Save**.

![The Header Builder widget library with the Shop group highlighted, showing the Ship-To Selector widget alongside Shopping Cart, Account Menu and Language Selector](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

The widget needs no setup — it lists your active Shipping Countries automatically, and shows a shopper's current selection (or their GeoIP-detected country, if they haven't chosen one yet). Picking a different country updates their region immediately and reloads the page's product availability and pricing.

The Ship-To Selector doesn't have a dedicated settings form yet. If you want to change its button style (outline, solid, or ghost) or hide the "Ship to" label, open the widget's settings in the builder and edit the **Custom Configuration (JSON)** field directly, using `button_style` and `show_label`.

### Currency follows region

Preserve all markdown formatting, image paths, code blocks, and technical terms.

如果您的商店支持多种貨幣（在 **設定 > 多幣別** 中設置），則切換地區——無論是透過提示還是 Ship-To 選擇器——也會切換到該地區的預設貨幣。

如果您的商店只有一種貨幣，或者未明確啟用第二種貨幣，當顧客更換地區時，貨幣將保持不變。

## 小技巧

- 除非您有具體原因要限制某個產品，否則請將 **地區可用性** 設為 **所有地區均可**——這是最簡單的選項，當您之後新增地區時也無需維護。
- 若您需要小範圍的允許清單（例如某個產品首先在一個國家發售），請使用 **僅限所選地區**；若需要小範圍的拒絕清單（例如除了某個國家外的其他地區），請使用 **所有地區除外所選地區**——選擇其中一種，取決於哪一種設定所需的行數較少。
- 如果顧客報告某個產品不見了卻應該可見，請檢查該產品的 **地區可用性** 設定，以及他們的國家是否被活躍的 **銷售地區** 和活躍的 **運送國家** 覆蓋。
- **從目錄隱藏** 可以讓您的目錄看起來更整潔，讓無法購買某些商品的顧客瀏覽，但這也意味著在這些地區，商品推廣和搜尋結果會較少——如果仍希望顧客在無法結帳的地區瀏覽完整目錄，**顯示，標記為不可用** 通常是更好的選擇。
- 透過在頁首加入 Ship-To 選擇器來測試地區行為，在依賴 GeoIP 檢測進行發佈前，親自切換國家進行測試。
- 請明確設定各個地區的優先順序值（在銷售地區頁面中）——最高優先順序的活躍地區會作為無法檢測到或與任何地區不匹配的顧客的預設選擇。