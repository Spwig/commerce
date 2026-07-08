---
title: 稅務設定
---

為您的商店配置稅務規則，以便根據客戶的位置自動應用正確的稅款。您可以點擊一下載入區域預設值，或為任何國家、州、城市或郵政編碼創建自定義規則。

![稅務儀表板](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## 稅務儀表板

導航至 **Orders > Shipments > Tax Rates** 以打開稅務儀表板。此頁面顯示：

- **統計面板** — 四個卡片顯示總規則數、活動規則數、涵蓋的國家數以及使用的稅務類型
- **篩選器** — 按名稱、國家或州搜索，並按國家、稅務類型（銷售稅、增值稅、商品及服務稅、自定義）或狀態（活動/非活動）篩選
- **稅務規則卡片** — 每個卡片顯示國家旗幟、規則名稱、位置、稅率百分比、稅務類型徽章、狀態徽章、優先級和豁免數量

## 載入稅務預設值

點擊 **Load Presets** 以打開預設值模態框。預設值是某個區域的標準稅率集合，只需點擊一下即可載入到您的商店中。

![Load Presets](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

預設值按世界區域組織：

| Region | Preset Groups |
|--------|--------------|
| **Africa** | Africa VAT (25 rates) |
| **Asia Pacific** | Asia-Pacific VAT/GST (24 rates), Central Asia VAT (6 rates) |
| **Europe** | EU VAT Rates, UK VAT, Other European VAT |
| **Latin America** | Latin America VAT |
| **Middle East** | Middle East VAT |
| **North America** | US State Sales Tax, Canadian GST/HST |
| **Oceania** | Oceania GST/VAT |

### 預設值如何運作

1. 點擊您想要的預設值組的 **Load**
2. 系統會為該組中的每個國家或州創建稅務規則
3. 已有與相同國家、州和稅務類型的規則會自動跳過，以避免重複
4. 載入後，每條規則都可以完全編輯 — 調整稅率、添加豁免或停用不需要的規則

您可以載入多個預設值組。例如，如果您向歐洲各地的客戶銷售，可以同時載入 EU VAT 和 UK VAT。

## 手動創建稅務規則

點擊 **Add Tax Rate** 以創建自定義規則。表單有四個部分：

![Tax Rate Form](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### 基本資訊

| Field | Description |
|-------|-------------|
| **Name** | 規則的顯示名稱（例如，"California Sales Tax"） |
| **Is Active** | 切換以啟用或停用規則 |
| **Tax Type** | 銷售稅、增值稅、商品及服務稅或自定義稅 |
| **Rate (%)** | 稅率以百分比表示（例如，輸入 8.25 表示 8.25%） |
| **Priority** | 當多個規則匹配相同位置時，數字較高的規則具有優先權 |

### 地理範圍

| Field | Description |
|-------|-------------|
| **Country** | ISO 3166-1 alpha-2 編碼（例如，US、GB、DE） |
| **State** | 州或省份（留空以應用整個國家） |
| **City** | 城市名稱（可選，用於城市級稅務規則） |
| **Postal Codes** | 具體郵政編碼列表（可選，用於郵政編碼級稅務規則） |

規則是從最特定到最不特定進行匹配的。特定郵政編碼的規則優先於相同州的規則，而州的規則又優先於國家範圍的規則。

### 應用規則

| Field | Description |
|-------|-------------|
| **Applies to Shipping** | 勾選後，此稅款也適用於運費 |
| **Compound Tax** | 勾選後，此稅款是在其他稅款基礎上計算的（基數加上已應用的稅款） |

### 產品豁免

| Field | Description |
|-------|-------------|
| **Exempt Product Types** | 免稅的產品類型（例如，數字、服務） |
| **Exempt Categories** | 免稅的特定產品類別 |

## 稅務類型

| Type | Used For | Examples |
|------|----------|---------|
| **Sales Tax** | US, Canada | 州和省銷售稅 |
| **VAT** | Europe, UK, much of Asia and Africa | 增值稅 |
| **GST** | Australia, New Zealand, India, Singapore | 商品及服務稅 |
| **Custom Tax** | Special cases | 當地附加稅、環境稅、奢侈品稅 |

## 稅務計算方式

當客戶到達結帳頁面時，系統會根據其運送地址自動計算稅款：

1. **地理匹配** — 找出所有與客戶國家匹配的活動規則，然後根據州、城市和郵政編碼進一步縮小範圍
2. **特定性評分** — 更具體的規則（郵政編碼 > 城市 > 州 > 國家）排名更高
3. **優先級排序** — 在相同特定性層級內，優先級更高的規則具有優先權
4. **產品豁免** — 免稅產品會從每個適用的規則中排除
5. **非複合稅** — 首先根據每個商品的基價計算
6. **複合稅** — 根據基價加上所有已應用的非複合稅計算
7. **運費稅** — 如果規則啟用了 "Applies to Shipping"，運費將包含在應稅金額中

稅務細分會與訂單一起存儲，因此您可以查看確切的規則應用情況以及每個規則的貢獻金額。

## 常見設定

### EU 商店

1. 點擊 **Load Presets** 並載入 **EU VAT Rates** 組
2. 這會為所有歐盟成員國創建增值稅規則，並使用當前標準稅率
3. 如果您還向英國銷售，可選擇載入 **UK VAT**

### US 商店

1. 點擊 **Load Presets** 並載入 **US State Sales Tax** 組
2. 這會為所有徵收銷售稅的美國州創建銷售稅規則
3. 對於城市級稅，手動添加填寫了城市欄位且優先級較高的規則

### 多地區商店

1. 為您銷售的每個市場載入多個預設值組
2. 系統會根據每個客戶的位置應用正確的稅款
3. 根據您的具體業務需求調整個別規則

## 小技巧

- **從預設值開始** — 載入您目標市場的預設值組，然後自定義個別稅率，而不是從頭開始創建每條規則。
- **明智地使用優先級** — 為更特定的本地規則設置更高的優先級值，以確保它們正確地覆蓋更廣泛的區域規則。
- **仔細檢查複合稅** — 複合稅很少見。大多數管轄區使用簡單（非複合）稅。只有在當地法規明確要求稅上稅計算時，才啟用複合稅。
- **保持規則啟用/停用** — 為了季節性或臨時更改，不要刪除稅務規則，而是將其設為停用，並在需要時重新啟用。
- **上線前進行測試** — 設置好稅務規則後，從不同地址下測試訂單，以驗證正確的稅款是否已應用。

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.