---
title: 許可證密鑰管理
---

許可證密鑰管理讓您能夠控制軟體許可證密鑰的生成、存儲以及在客戶購買數字產品時的交付方式。Spwig 支持內建的密鑰生成、預載的密鑰池以及與外部許可證管理服務的整合。

## 概述

在 Spwig 中有三種管理許可證密鑰的方式：

| 方法 | 最適合用於 |
|--------|---------|
| **許可證模板** | 在購買時自動生成符合自定義格式的唯一密鑰 |
| **許可證池** | 預先生成一批密鑰以供批量分發 |
| **外部供應商** | 將密鑰生成和管理委派給第三方服務，例如 Keygen.sh |

這些方法可以組合使用——例如，一個池可以使用自定義模板來定義密鑰格式，並可選擇將生成的密鑰同步到外部供應商。

## 許可證密鑰模板

許可證密鑰模板定義了生成密鑰的 *格式*。模板使用包含佔位符的模式，Spwig 在生成時會填入這些佔位符。

### 建立模板

1. 點擊 **目錄 > 許可證密鑰模板**
2. 點擊 **+ 添加許可證密鑰模板**
3. 輸入 **名稱**（例如，`Standard App License`）
4. 使用佔位符配置 **模式**（請參閱下方）
5. 如有需要，設置 **前綴** 和 **後綴**（例如，前綴為 `MYAPP` 會在每個密鑰前加上 `MYAPP-`）
6. 選擇 **分隔符** 字元（預設：`-`）
7. 設置 **字元集** — 用於隨機片段的字元。預設值會排除容易混淆的字元，如 `0` 和 `O`、`1` 和 `I`
8. 設置 **最小/最大長度** 以進行驗證
9. 點擊 **保存**

### 模式佔位符


| Placeholder | Description | Example output |
|-------------|-------------|---------------|
| `{RANDOM:N}` | N random characters from the character set | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | N-digit checksum for validation | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | The template's prefix value | `MYAPP` |
| `{SUFFIX}` | The template's suffix value | `PRO` |
| `{ORDER_ID}` | The order number | `10045` |
| `{PRODUCT_SKU}` | The product's SKU | `SOFTPRO` |
| `{DATE:FORMAT}` | Formatted date | `{DATE:YYMMDD}` → `260318` |

**Example pattern**: `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

This produces keys like: `MYAPP-K7JXQ-M3TPR-9BWKN-47`

### Previewing keys

After saving a template, a **Generate Sample Key** action is available on the template list. Use this to verify your pattern produces keys in the expected format before assigning the template to a product.

## License pools

A license pool is a batch of pre-generated keys for a product. Pools are useful when:
- You need keys for physical packaging (retail boxes, printed cards)
- You work with resellers who need batches of keys
- You want keys generated in advance rather than on demand

### Creating a license pool

1. Navigate to **Catalog > License Pools**
2. Click **+ Add License Pool**
3. Fill in the pool details:

| 欄位 | 說明 |
|-------|-------------|
| **名稱** | 描述性名稱（例如：`Retail Pack Q1 2026`） |
| **產品** | 這些金鑰所對應的產品 |
| **授權模板** | 金鑰格式的模板（預設為產品的模板） |
| **總金鑰數** | 要產生的金鑰數量 |
| **金鑰類型** | 永久授權、訂閱或試用版 |
| **最大激活次數** | 每個金鑰可以激活的設備數量 |
| **啟動後到期天數** | 從首次激活後授權到期的天數（留空表示無到期日） |
| **池到期時間** | 之後此池中未使用的金鑰將失效的日期 |
| **同步到提供商** | 可選擇將產生的金鑰同步到外部授權提供商 |

4. 點擊 **保存** — Spwig 開始在背景中生成金鑰

### 池狀態

| 狀態 | 含義 |
|--------|---------|
| **生成中** | 金鑰正在背景中創建 |
| **已準備好** | 所有金鑰已生成，可供分發 |
| **已耗盡** | 所有金鑰都已分配給訂單 |
| **已過期** | 池的到期日期已過 |

### 監控池

池清單顯示已分發的金鑰數量與總共生成的金鑰數量。打開一個池以查看完整的金鑰清單及其個別狀態。

## 外部授權提供商

外部提供商是處理金鑰生成和激活追蹤的第三方授權管理服務。當客戶完成購買時，Spwig 會與提供商通訊以生成並註冊金鑰。

### 支援的提供商

| 提供商 | 類型 |
|----------|------|
| **Spwig 內建授權伺服器** | 內建 — 不需要外部帳戶 |
| **Keygen.sh** | 基於雲端的授權管理 API |
| **LicenseSpring** | 企業級授權管理 |
| **Cryptlex** | 支援離線的授權管理 |
| **自定義 API** | 任何基於 REST 的授權系統 |

### 連接提供商

1.

導航至 **目錄 > 授权提供商**
2.

點擊 **+ 添加授权提供商**
3.


填寫供應商詳細資料：

| 欄位 | 說明 |
|-------|-------------|
| **名稱** | 這個連線的標籤（例如，`Keygen Production`） |
| **供應商類型** | 從支援的供應商中選擇 |
| **API 端點** | 供應商的 API 基底 URL |
| **API 金鑰** | 供應商的驗證金鑰 |
| **API 密碼** | 如果供應商需要的話 |

4. 設定同步行為：
   - **在訂單時同步** — 當顧客完成購買時自動同步
   - **在啟用時同步** — 向供應商報告設備啟用
   - **在停用時同步** — 報告停用（對於許可證轉移和退款很有用）
   - **雙向同步** — 允許供應商透過 Webhook 更新 Spwig 記錄

5. 點擊 **儲存**，然後點擊 **測試連線** 以驗證憑證是否有效

### 連線狀態

每個供應商會顯示三種連線狀態之一：

| 狀態 | 含義 |
|--------|---------|
| **尚未測試** | 還未驗證連線 |
| **已連線** | 上一次測試成功 |
| **錯誤** | 連線測試失敗 — 請查看錯誤訊息 |

### 同步現有許可證

要手動將現有的許可證金鑰推送到供應商（用於初始設定或在同步失敗後），請從供應商清單中使用 **立即同步** 操作。

## 監控同步活動

導覽至 **目錄 > 外部許可證同步** 以查看同步日誌。每個記錄顯示：
- 被同步的許可證金鑰
- 發送到的供應商
- 方向（Spwig → 供應商 或 供應商 → Spwig）
- 狀態（待處理、成功、失敗）
- 失敗同步的錯誤細節

失敗的同步會自動重試。您也可以透過編輯記錄並清除錯誤來強制重試。

## 小技巧

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

- 使用預設的字元集 (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`) 以避免客戶常誤讀的模糊字元 — 它排除了 `0`、`O`、`1` 和 `I`。
- 在您的模板模式中加入 `{CHECKSUM}` 區段，讓客戶和您的支援團隊能快速辨識輸入錯誤的金鑰。
- 對於高銷量產品，使用金鑰池而非按需生成，以確保結帳時金鑰能即時發送。
- 對於季節性或有時間限制的金鑰批次，設定 **Pool Expires At**，讓舊的未使用的金鑰會自動失效。
- 設置後以及任何憑證更改後，務必測試供應商連線 — 如果連線中斷，客戶將無法收到他們的金鑰。
- 如果使用雙向同步，請設定供應商的 webhook URL 指向您商店的許可證 webhook 端點。