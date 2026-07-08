---
title: 基於位置的商業規則
---

基於位置的商業規則讓您在訪客從特定國家、地區或設備類型到來時自動採取行動。您可以使用規則為來自特定地區的客戶設定貨幣，將訪客導向本地化頁面，顯示促銷橫幅，或限制對某些內容的訪問。

每次建立訪客會話時，都會按照優先順序評估規則。當規則匹配時，會立即執行其配置的動作。

## 商業規則的工作原理

每個規則由兩個部分組成：

- **條件** — 規則觸發所需的條件（例如，「訪客來自德國」）
- **動作** — 當所有條件都匹配時發生的動作（例如，「將貨幣設定為 EUR」）

條件和動作以 JSON 物件的形式儲存在規則表單中。Spwig 會按照優先順序（數字較小的先執行）評估所有活動規則，並套用匹配的規則。

## 瀏覽商業規則

導航至 **Customers > Business Rules** 以查看所有配置的規則。清單會顯示每個規則的名稱、狀態、優先順序、觸發次數以及最後觸發的時間。

點擊任何規則以查看或編輯它，或點擊 **+ Add Business Rule** 來建立一個新規則。

## 建立商業規則

### 第 1 步：基本資訊

填寫規則的識別細節：

- **名稱** — 一個清晰且具描述性的名稱（例如，`Set EUR for Eurozone`）
- **描述** — 可選的筆記，用來說明規則的目的
- **啟用** — 勾選此選項以啟用規則；取消勾選以暫停規則而不刪除它
- **優先順序** — 數字較小的會先執行；使用 `10`、`20`、`30` 為未來的規則預留空間

### 第 2 步：定義條件

在 **Conditions** 欄位中，輸入一個 JSON 物件，用來描述規則應該觸發的條件。物件中的所有條件都必須為 true，規則才會匹配。

#### 可用的條件鍵

| Condition | Format | Example |
|-----------|--------|---------|
| `country_in` | Array of ISO country codes | `["DE", "FR", "IT"]` |
| `country_not_in` | Array of ISO country codes | `["US", "CA"]` |
| `region_in` | Array of region names | `["Bavaria", "Catalonia"]` |
| `region_not_in` | Array of region names | `["Quebec"]` |
| `is_mobile` | Boolean | `true` |
| `is_vpn` | Boolean | `false` |

#### Example conditions

Visitors from Germany, France, or Italy:
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Visitors from the United States who are on a mobile device:
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Visitors from outside the European Union:
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Step 3: define actions

In the **Actions** field, enter a JSON object describing what should happen when the rule triggers.

#### Available action keys

| Action | Format | Description |
|--------|--------|-------------|
| `set_currency` | Currency code string | Pre-select a currency for the visitor |
| `set_language` | Language code string | Set the display language |
| `show_banner` | Boolean | Trigger a promotional banner |
| `redirect_to` | URL path string | Redirect the visitor to a different URL |

#### Example actions

Set currency to Euro:
```json
{
  "set_currency": "EUR"
}
```

Redirect to a localized landing page:
```json
{
  "redirect_to": "/de/"
}
```

Set both currency and language together:
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Practical examples

### Example: Eurozone currency rule

**Scenario:** Automatically show Euro pricing to visitors from Eurozone countries.

| 欄位 | 值 |
|-------|-------|
| 名稱 | `Eurozone — Set EUR` |
| 優先順序 | `10` |
| 是否啟用 | 已勾選 |
| 條件 | `"{\"country_in\": [\"AT\",\"BE\",\"DE\",\"ES\",\"FI\",\"FR\",\"GR\",\"IE\",\"IT\",\"LU\",\"NL\",\"PT\"]}"` |
| 動作 | `"{\"set_currency\": \"EUR\"}"` |

### 範例：英國定價規則

**情境：** 向來自英國的訪客顯示英鎊定價。

| 欄位 | 值 |
|-------|-------|
| 名稱 | `UK — Set GBP` |
| 優先順序 | `20` |
| 是否啟用 | 已勾選 |
| 條件 | `"{\"country_in\": [\"GB\"]}"` |
| 動作 | `"{\"set_currency\": \"GBP\"}"` |

### 範例：導向本地化商店區塊

**情境：** 將來自澳洲的訪客導向專屬的澳洲頁面。

| 欄位 | 值 |
|-------|-------|
| 名稱 | `Australia — Redirect` |
| 優先順序 | `30` |
| 是否啟用 | 已勾選 |
| 條件 | `"{\"country_in\": [\"AU\"]}"` |
| 動作 | `"{\"redirect_to\": \/au\/}"` |

## 測試規則

您可以不需等待實際流量，即可驗證規則是否符合預期的訪客資料：

1. 在「商業規則」清單中，使用複選框選取規則
2. 開啟 **動作** 下拉選單，選擇 **測試選取的規則**
3. 點擊 **開始**

Spwig 將根據一個美國為基礎的範例訪客資料評估規則，並報告是否匹配以及會觸發哪些動作。

## 監控規則活動

「規則清單」中的 **觸發次數** 欄位顯示每個規則觸發的次數。點擊規則以在「統計」區塊中查看 **最後觸發** 的時間戳。

若您想從特定日期開始測量，可使用 **重置統計資料** 來將觸發次數歸零。

## 小技巧

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

- 使用間隔優先級（10、20、30）而非連續數字（1、2、3）來設定優先級，這樣可以在不重新編號所有規則的情況下後續插入新規則
- 規則會按照優先級順序觸發，所有匹配的規則都會被套用 —— 如果兩個規則都設定了貨幣，優先級較低（數字較大）的規則動作會最後被套用
- 使用 **是否啟用** 按鈕，可以在促銷期間暫時停用規則，而無需刪除配置
- 在將新規則啟用到實際環境之前，務必先進行測試，以確保條件設定正確
- 如果您希望對偽裝位置的訪客採取不同的處理方式，可以使用 VPN 檢測（`"is_vpn": true`），但請注意有些合法客戶會使用 VPN 來保護隱私