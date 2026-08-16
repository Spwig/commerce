---
title: 配置商店設置
---

商店設置是用來配置商店的身分識別、本地化、品牌和操作偏好設置的中心地點。導覽至 **設定 > 商店設置** 開始。

![商店設置常規選項卡](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## 常規選項卡

**常規** 選項卡包含商店的核心身分識別設置。

### 商店身分識別

- **商店名稱** — 在頁面標題、電子郵件和管理員標頭中顯示的名稱。
- **副標題** — 簡短描述您的商店，用於SEO和社交分享。
- **網站網址** — 您商店的公眾網址。這用於電子郵件、地圖產生和連結建立。

### 聯繫資訊

- **聯絡電郵** — 接收訂單通知，並在客戶通訊中顯示。
- **電話號碼** — 可選的支援電話號碼，顯示在頁腳和電子郵件中。

### 營業地址

輸入完整的地址（街道、城市、州、郵遞區號、國家）。這用於：
- 運費起點計算
- 稅務計算
- 法律要求和發票

## 品牌

### 商標

上傳商店商標（建議PNG或SVG，約200x50像素，透明背景）。商標出現在：
- 商店前端標頭
- 電子郵件模板
- 管理員面板

### 網站圖示

上傳正方形網站圖示（ICO或PNG，32x32像素）。它出現在：
- 瀏覽器標籤圖示
- 書籤圖示
- 移動主螢幕圖示

## 本地化

### 預設語言

從10種支援選項中選擇商店的主要語言：

| 語言 | 碼 |
|----------|------|
| 英語 | en |
| 西班牙語 | es |
| 法語 | fr |
| 德語 | de |
| 葡萄牙語 | pt |
| 日語 | ja |
| 簡體中文 | zh-hans |
| 繁體中文 | zh-hant |
| 俄語 | ru |
| 阿拉伯語 | ar |

預設語言控制管理介面語言和 storefront 內容的預設值。

### 時區

選擇商店的時區以確保訂單時間戳、計畫促銷和報告的準確性。

### 幣別

保留所有markdown格式、圖片路徑、程式碼區塊和技術術語。

- **預設貨幣** — 價格和會計的主 currency。
- **多幣別** — 啟用以讓客戶查看他們首選貨幣的價格，並使用即時匯率自動轉換。

在 **設定 > 商店設定 > 貨幣** 中設定其他貨幣。

## 電商設定

### 來賓結帳

允許購買時不建立帳戶：
- 更快的結帳流程
- 減少首次買家的障礙
- 收集較少的客戶資料

### 帳號建立時機

控制客戶何時被提示建立帳戶：

| 選項 | 說明 |
|--------|-------------|
| **購買後（推薦）** | 在成功下單後提示建立帳戶 — 利用購買後的忠誠度以達到最佳轉化率 |
| **結帳期間** | 在處理付款前建立帳戶 |
| **結帳前** | 要求在購物前建立帳戶（不推薦 — 會降低轉化率） |

您也可以設定自定義的 **帳號建立訊息** 來說明註冊的好處。

### 库存預設值

- **追蹤庫存** — 全域啟用庫存追蹤
- **庫存低限** — 當庫存水準達到此值時，會傳送庫存不足通知至管理員電郵（預設：10 單位）

### 库存智能

![顯示預設再訂購提前時間、安全庫存倍數、速度計算視窗、預設允許預購、庫存不足通知頻率欄位的庫存智能卡片](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

這些設定調整自動再訂購、安全庫存和銷售速度計算，並控制如何處理缺貨和庫存不足的情況。

- **預設再訂購提前時間（天數）** — 一旦下訂單，通常需要多少天從供應商處補貨（預設：14 天）。


預測功能會使用此來標記需要立即補貨的產品，以避免新貨到達前庫存不足。
- **安全庫存係數** — 在預期需求之上應用的緩衝，用於吸收銷售突增或供應商延遲。

例如，係數為 `1.5` 時，會在您計算出的安全庫存基礎上增加 50% 的緩衝；`2.0` 則會使其翻倍。

對於庫存耗盡代價較高的產品（熱門商品、季節性商品）請提高此值；對於流動較慢的庫存，不希望過度訂購的產品請降低此值。
- **速度計算視窗（天數）** — Spwig 用來計算每個產品銷售速度的回溯視窗，這會進一步影響補貨建議和庫存天數數字（預設：30）。

較短的視窗能更快響應近期需求變動；較長的視窗能平滑季節性波峰，這樣單一忙碌週不會扭曲預測。
- **預設允許預訂** — 新創建產品的初始預訂設置（預設關閉）。

每個產品仍可以在其自己的產品頁面中覆蓋此設置，現有產品會保留其當前設置 —— 更改此設置只會改變新產品的預設值，不會回溯更新您的目錄。
- **低庫存警報頻率** — Spwig 移動應用程式通知低庫存的頻率：**即時** 在產品庫存低於門檻時立即發送推送通知；**每日摘要** 和 **每周總結** 則會在該排程時間發送單一推送通知，總結所有當前低庫存的產品。

此設置僅在 **低庫存警報**（下方的電子郵件設置）啟用時生效 —— 警報關閉時，不會發出任何頻率的通知。

### 文件與發票

![顯示稅務ID / VAT 編號、發票頁腳文字、包裝清單頁腳文字和文件 Logo 寬度欄位已填入範例值的「文件與發票」卡片](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

這些欄位會填入 Spwig 為訂單產生的發票和包裝清單 —— 例如當商家下載或電子郵件發票 PDF 時，或列印用於運送的包裝清單。

- **稅務 ID / VAT 編號** —— 您公司的稅務識別編號。會列印在產生的發票上，以符合當地稅務文件要求。
- **發票頁尾文字** —— 顯示在每張產生的發票底部的自由文字。常見用途：付款條件（「30 天內付款」）、感謝訊息或銀行轉帳明細。
- **包裝清單頁尾文字** —— 顯示在每張產生的包裝清單底部的自由文字。常見用途：退貨說明或給倉儲/履行團隊的備註。
- **文件版頭圖片寬度 (px)** —— 您商店的標誌在產生的 PDF 發票和包裝清單中的寬度（預設：200px）。高度會自動縮放以匹配，以保持您的標誌的比例。標誌圖片本身來自您的 **Logo**（品牌，上方）—— SVG 標誌不會在 PDF 文件中繪製，因此如果您在商店前端使用向量圖案，請上傳 PNG 或 JPG 格式的標誌。

## 電子郵件設定

在 **設定 > 電子郵件帳戶** 和 **設定 > 電子郵件範本** 中設定電子郵件傳送設定。詳情請參閱 [電子郵件設定](/help/email-configuration)。

商店設定中可用的關鍵電子郵件設定：

- **訂單確認電子郵件** —— 開啟或關閉自動確認電子郵件
- **運送通知電子郵件** —— 開啟或關閉運送更新通知
- **庫存不足警告** —— 當庫存低於門檻時傳送警告至管理員電子郵件
- **電子郵件傳送模式** —— 實際（正常傳送）、暫停（暫停所有電子郵件）或僅記錄（僅記錄但不傳送）
- **測試電子郵件轉向** —— 所有送出的電子郵件都會轉向單一位址以供測試

## 安全設定

### 兩步驗證 (2FA)

控制員工是否需要使用兩步驗證：

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

| 設定 | 描述 |
|---------|-------------|
| **可選** | 員工可以選擇啟用兩步驗證，但不是必填 |
| **推薦** | 員工會看到提示鼓勵他們設置兩步驗證 |
| **必填** | 員工在啟用兩步驗證之前無法訪問管理後台 |

- **寬限期（天數）** — 員工在啟用執行後設置兩步驗證的天數 |
- **允許信任裝置** — 允許員工在已識別的裝置上跳過兩步驗證驗證，持續一組天數

## Cookie 同意

配置顯示給商店訪客的 Cookie 同意橫幅:

- **Cookie 同意已啟用** — 顯示或隱藏 Cookie 橫幅 |
- **橫幅位置** — 橫幅在螢幕上的顯示位置（底部欄、角落彈窗等） |
- **同意模式** — 簡單通知、選擇加入、選擇退出 |
- **橫幅標題和文字** — 可自定義的標題和描述顯示給訪客 |
- **分類描述** — 分別為分析、營銷和功能 Cookie 的描述

所有橫幅文字欄位都支援多語言商店的翻譯。

## 通訊

**通訊**選項卡控制您的商店如何獲取、確認以及讓客戶管理營銷電子郵件和簡訊的同意。這些設置會影響您的法律合規立場（電子郵件的GDPR，簡訊的TCPA），因此在上線前請與您自己的法律顧問審查它——Spwig提供控制，而不是建議。

![通訊選項卡顯示電子郵件營銷同意、偏好與退訂、以及簡訊同意卡片](/static/core/admin/img/help/store-settings/communications-tab.webp)

### 電子郵件營銷同意

- **為營銷電子郵件啟用雙重選擇** — 當啟用時，選擇加入營銷電子郵件的客戶會收到確認電子郵件，並必須點擊其中的連結，Spwig才會發送任何營銷訊息給他們。

當關閉時，勾選營銷選擇加入方塊就足夠了。

保留所有markdown格式、圖片路徑、代碼塊和技術術語。

預設啟用，符合GDPR最佳實務。
- **預設營銷同意狀態** — 新建立的客戶帳戶預設套用的營銷同意狀態。

預設關閉（GDPR選擇退出），因此新客戶預設未訂閱營銷電子郵件，直到他們主動同意訂閱。

當雙重確認啟用時，同意訂閱會觸發一封確認電子郵件，內含驗證連結。在客戶點選之前，他們會被記錄為已同意但未驗證，營銷電子郵件將跳過他們——交易電子郵件（訂單確認、運送更新、密碼重設）永遠不會受到此設定的影響。

### 偏好設定與退訂

- **啟用客戶偏好中心** — 當啟用時，客戶可以從其帳戶儀表板連結的自我服務頁面管理其電子郵件和簡訊偏好設定。當關閉時，該頁面及其支援API會回傳不可用，儀表板連結也會隱藏。電子郵件中的單擊退訂連結無論如何都能正常運作——這是一種合規性逃生通道，不受此切換的影響。
- **收集退訂原因** — 當啟用時，單擊退訂頁面會要求客戶提供簡短的原因：*我收到太多電子郵件*、*內容與我不相關*、*我未註冊此服務*、*我不再感興趣* 或 *其他*。客戶選擇的原因會記錄到共識審計追蹤中，讓您可以隨時審查退訂模式。

### 短訊同意

- **需要簡訊驗證** — 當啟用時（預設），客戶必須使用一次性代碼驗證其電話號碼，Spwig才會向其發送任何簡訊，包括營銷簡訊。當關閉時，在註冊時勾選簡訊同意方框就足夠啟動發送。此預設已更改為 **啟用** 以確保TCPA安全——只有在註冊流程中有其他驗證步驟時才關閉此功能。

## 維護模式

保留所有markdown格式、圖片路徑、程式碼區塊和技術術語。

啟用維護模式以暫時將您的商店下線：
- 向訪客顯示自定義的維護訊息
- 您可以連結在頁面編輯器中建立的 **維護頁面**，以提供完整的品牌體驗
- 僅限管理員訪問
- 在重大更新或遷移期間非常實用

## 社交媒體

連結您的商店的社交媒體個人資料。這些會出現在頁腳和電子郵件模板中：

- **Facebook 網站地址**
- **Twitter 網站地址**
- **Instagram 網站地址**
- **LinkedIn 網站地址**

## SEO 默認設置

設置當頁面沒有自己的 SEO 設置時使用的預設 meta 標籤：

- **Meta 標題** — 預設頁面標題（最多 60 個字元）
- **Meta 描述** — 預設描述，顯示在搜尋結果中（最多 160 個字元）
- **Meta 關鍵字** — 預設逗號分隔的關鍵字

## 稅務設置

在 **Settings > Tax Settings** 設定稅務收集：

1. **計算方式** — 依據運費地址、賬單地址或商店所在地
2. **稅率** — 依據地區和產品稅種定義稅率
3. **稅務顯示** — 顯示含稅價格、不含稅價格或兩者皆顯示

## 提示

請保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

- 在处理任何订单之前，正確設置您的時區 —— 這會影響所有時間戳和報告。
- 啟用訪客結賬以提高轉化率。
- 填寫您的公司地址以確保運費和稅務計算準確。
- 上傳商標和網站圖示以提供專業的品牌體驗。
- 使用 **購買後** 的帳戶創建時機以獲得最佳註冊率。
- 啟用員工的雙因素驗證強制執行，以保護您的商店管理後台。
- 在上線前使用 **測試重定向電郵** 設定測試電郵流程。
- 設定 **預設重新訂購提前期** 以匹配您最慢的常規供應商 —— 重新訂購預測會套用此單一值到您整個目錄，因此請以您最長提前期的產品為主。
- 如果您經常進行促銷或補貨，請縮短 **速度計算視窗**，以便預測能快速回應最近幾天的銷售；對於較穩定、不易波動的需求視圖，請延長它。
- 如果您啟用 **預設允許預購**，請記住這只會設定在變更 *之後* 創建的產品的起始點 —— 如果您希望現有目錄中的所有產品都允許預購，請個別檢查現有產品。
- 將 **低庫存警報頻率** 設定為與您管理庫存的活躍程度相符：**即時** 用於快速流動的目錄，其中每個庫存短缺風險都需要即時關注；**每日摘要** 或 **每周總結** 用於避免大型目錄的警報疲勞。
- 在您的第一張真實發票發送到客戶之前，填寫您的 **稅務ID / VAT號碼** 和頁腳文字 —— 兩個欄位預設為空白。
- 如果您的 **商標** 是 SVG 格式，請同時上傳 PNG 或 JPG 版本 —— **文件商標寬度** 對 PDF 無影響，因為 Spwig 無法在生成的發票和包裝單上繪製 SVG 圖形。
- 除非您有具體原因需要關閉，請保持 **營銷電郵的雙重確認啟用** 開啟 —— 這對於 GDPR 是更安全的預設設置，並透過將未驗證的地址排除在營銷發送之外來保護您的發件人聲譽。
- 保持 **預設營銷訂閱狀態** 關閉。

Pre-checking marketing consent for new accounts undermines the GDPR opt-in requirement even if a customer could technically un-tick it.
- Don't disable **Enable Customer Preference Center** just to simplify your account dashboard — without it, customers can still unsubscribe from a single message type, but they lose the ability to fine-tune preferences (e.g. keep shipping updates but drop the newsletter).
- Keep **Require SMS Verification** on unless your signup flow already confirms phone numbers another way (e.g. an SMS-based login) — the setting exists specifically to keep you inside TCPA rules.

## Troubleshooting

**Changes not appearing on the storefront:**
- Clear your browser cache
- Run a cache clear from the admin panel
- Check if maintenance mode is accidentally enabled

**Emails not sending:**
- Verify your email provider settings in Email Configuration
- Check that the **Email Delivery Mode** is set to **Live**
- Ensure the **Test Redirect Email** is blank if you want emails sent to real recipients

**Currency conversion not working:**
- Verify your exchange rate provider is connected
- Check API credentials in the exchange rate settings
- Try updating rates manually

**Marketing emails aren't reaching customers who opted in:**
- Check whether **Enable Double Opt-In for Marketing Emails** is on — if so, the customer must click the confirmation link in the verification email before marketing sends resume
- Ask the customer to check spam/junk for the confirmation email
- Confirm the customer's marketing opt-in is still on in their preferences — an unsubscribe click turns it back off

**Customers say they can't find the preference center:**
- Check that **Enable Customer Preference Center** is on — when it's off, the dashboard link is hidden and the page is unavailable by design
- The unsubscribe link in any marketing email always works regardless of this setting, so point customers there as a fallback