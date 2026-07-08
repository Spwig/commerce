---
title: 運遞預設值
---

運遞預設值用於定義在未使用 API 整合的情況下創建的運送單的手動運遞方式（DHL、FedEx、UPS、自定義運遞方式）—每個預設值提供運遞商標誌、追蹤 URL 模板和顯示設定。系統預設值（DHL、FedEx、UPS、USPS）已經預先設定且無法刪除，而自定義預設值允許商家添加區域性或專業運遞方式。預設值會連結到手動運送單，商家在這些運送單中手動輸入追蹤號碼，而非透過運遞商 API 購買標籤。

在創建手動運送單或當您想要追蹤連結但又不希望完全整合 API 時，請使用運遞預設值。

## 系統預設值 vs 自定義預設值

**系統預設值**（預裝）：
- DHL、FedEx、UPS、USPS、Royal Mail、Canada Post、Australia Post
- 無法刪除（is_system=True）
- 可覆蓋追蹤 URL 或標誌
- 提供預設追蹤 URL 模板

**自定義預設值**（商家創建）：
- 區域性運遞商（OnTrac、LaserShip、區域郵政）
- 專業運遞商（貨運、白手套配送）
- 可編輯或刪除
- 需要手動輸入追蹤 URL 模板

---

## 運遞預設值設定

每個預設值定義：

**基本設定**：
- **名稱**：運遞商顯示名稱（例如，"DHL Express"、"Local Courier"）
- **代碼**：內部識別碼（例如，"dhl"、"local_courier"）
- **標誌**：運遞商標誌圖片（可選，若未提供則使用圖示）
- **圖示**：FontAwesome 圖示作為備用（例如，"fa-truck"）
- **啟用**：切換顯示狀態

**追蹤設定**：
- **追蹤 URL 模板**：包含 {tracking_id} 占位符的 URL 模式
- **追蹤 URL 覆蓋**：自定義 URL（會覆蓋預設模板）

**系統設定**（僅限系統預設值）：
- **是系統**：無法刪除
- **是預設**：每種運遞類型有一個預設

---

## 追蹤 URL 模板

追蹤 URL 使用 `{tracking_id}` 占位符：

**範例**：

DHL：`https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx：`https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS：`https://www.ups.com/track?tracknum={tracking_id}`

USPS：`https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

自定義：`https://track.localcourier.com/tracking/{tracking_id}`

**如何運作**：
1. 商家創建運送單並輸入追蹤號碼 "1234567890"
2. 系統將 {tracking_id} 替換為實際號碼
3. 顧客點擊追蹤連結 → 跳轉到運遞商網站
4. 結果：`https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## 創建自定義運遞預設值

**步驟說明**：

1. 輸入 Settings > Shipping > Carrier Presets
2. 點擊 "Add Carrier Preset"
3. 輸入名稱（例如，"OnTrac"）
4. 輸入代碼（slug："ontrac"）
5. 可選：上傳標誌圖片
6. 選擇圖示（fa-truck、fa-shipping-fast 等）
7. 輸入包含 {tracking_id} 的追蹤 URL 模板
8. 啟用 = 是
9. 儲存

**範例 - OnTrac**：
```
Name: OnTrac
Code: ontrac
Tracking URL: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
Icon: fa-truck
Active: Yes
```

---

## 覆蓋系統預設值追蹤 URL

系統預設值可以有追蹤 URL 覆蓋：

**使用情境**：您的運遞商帳號有特殊的追蹤門戶

**如何覆蓋**：
1. 編輯系統預設值（例如，DHL）
2. 在 "Tracking URL Override" 欄位輸入覆蓋 URL
3. 覆蓋會優先於預設模板
4. 儲存

**範例**：
```
System: DHL
Default URL: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
Override URL: https://track.dhl.com/special-account/{tracking_id}
Result: Override URL 用於所有 DHL 運送單
```

---

## 運遞商標誌

**商標誌指南**：
- 格式：PNG 或 SVG（SVG 可伸縮，為首選）
- 大小：建議 200×60 像素
- 背景：透明或白色
- 顏色：完整的運遞商品牌顏色

**備用圖示**：
如果未上傳商標誌，系統會顯示 FontAwesome 圖示：
- fa-truck（預設）
- fa-shipping-fast（快遞）
- fa-plane（航空貨運）
- fa-box（包裹）

---

## 在運送單中使用運遞預設值

當創建手動運送單時：

1. 訂單 > 訂單明細 > 創建運送單
2. 選擇 "Manual Shipment" 模式
3. 從預設值下拉選單中選擇運遞商
4. 輸入追蹤號碼
5. 可選：為此運送單覆蓋追蹤 URL
6. 儲存

**運送單顯示**：
- 顯示運遞商標誌（或圖示）
- 顯示追蹤號碼
- 可點擊的追蹤連結（使用預設值 URL 模板）

---

## 預設運遞商

每種系統中可設置一個預設值：

**使用情境**：最常用運遞商在創建運送單時自動選擇

**如何設置**：
1. 編輯運遞預設值
2. 勾選 "Is Default"
3. 儲存
4. 如果有任何先前預設值，會自動取消設定

**僅允許一個預設值** - 設置新預設值會移除先前的預設標誌。

---

## 小技巧

- **使用描述性名稱** - "DHL Express" 比 "DHL" 更好
- **測試追蹤 URL** - 確認模板與真實追蹤號碼一起使用時有效
- **上傳運遞商標誌** - 在客戶郵件中呈現專業外觀
- **不要刪除系統預設值** - 它們已正確預先設定
- **僅在運遞商更改追蹤系統時使用覆蓋**
- **為主要運遞商設置預設** - 節省運送單創建時間
- **保持預設值啟用** - 僅在運遞商停用時停用
- **記載自定義運遞商** - 添加關於區域性運遞商的備註

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.