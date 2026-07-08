---
title: Translation Service
---

翻譯服務

翻譯服務為您商店的產品描述、頁面內容、部落格文章、SEO欄位和其他商家內容提供AI驅動的翻譯。翻譯在您的伺服器上本地執行，或通過外部提供商進行，因此您的內容保持私密，翻譯在幾秒內完成。

![Language management](/static/core/admin/img/help/translation-service/language-management.webp)

## How It Works

1. 您 **啟用語言** 為您的商店（例如，英語、德語、日語）
2. 當您創建或編輯內容（產品、頁面、部落格文章）時，您使用預設語言進行撰寫
3. 點擊 **Translate** 任何可翻譯的欄位以生成AI翻譯到您啟用的語言
4. 翻譯與原始內容一起儲存，並根據訪客的語言自動提供

## Managing Languages

導航到 **Settings > Languages** 來管理您的商店語言。

### Language Dashboard

儀表板顯示：
- **Total Languages** — 系統中所有可用的語言（100+）
- **Active Languages** — 目前為您的商店啟用的語言
- **Model Coverage** — 安裝的翻譯模型支援多少語言

### Activating Languages

1. 在 **Available Languages** 欄中找到語言
2. 點擊語言以將其移動到 **Active Languages** 欄
3. 語言立即可用於翻譯，並出現在您商店的語言切換器中

### Default Language

一種語言被標記為 **預設**。這是：
- 您撰寫內容的語言
- 當沒有翻譯時的備用語言
- 當訪客尚未選擇偏好時顯示的語言

## Translation Models

Spwig 包含一個本地AI翻譯引擎，完全在您的伺服器上運行——沒有數據發送到外部服務。

### Available Models

| Model | Languages | Speed | Quality |
|-------|-----------|-------|---------|
| **M2M100-418M** | 100 | Fast | 適合常見語言對 |
| **M2M100-1.2B** | 100 | Moderate | 更高的品質，更高的資源使用 |
| **NLLB-200** | 200+ | Moderate | 最佳的覆蓋範圍，包括少數語言 |

### Model Selection

語言管理頁面顯示已安裝的模型及其語言覆蓋範圍。模型作為本地服務運行，使用 CTranslate2 進行高效推理。

## External Providers

對於偏好雲端翻譯或需要特定語言品質的商店，Spwig 支援外部翻譯提供商。

| Provider | Description |
|----------|-------------|
| **DeepL** | 為歐洲和亞洲語言提供高品質翻譯 |
| **Google Translate** | 使用神經機器翻譯的廣泛語言覆蓋 |
| **Azure Translator** | Microsoft 的神經翻譯服務 |
| **AWS Translate** | Amazon 的機器翻譯，支援自定義術語 |

### Connecting a Provider

1. 導航到 **Settings > Translation Providers**
2. 選擇提供商並輸入您的 API 金鑰
3. 設置提供商為預設翻譯引擎
4. 翻譯將使用外部提供商而不是本地模型

您可以同時使用外部提供商和本地模型——例如，使用 DeepL 翻譯歐洲語言，並使用本地模型翻譯其他內容。

## Translating Content

### Field-Level Translation

可翻譯的欄位（產品名稱、描述、SEO 標題等）會在欄位旁顯示 **翻譯按鈕**。點擊它以：

1. **翻譯到所有啟用的語言** — 一次為每個啟用的語言生成翻譯
2. **翻譯到特定語言** — 選擇個別語言進行翻譯

翻譯會出現在編輯器的語言選項卡中。您可以審核並手動編輯任何機器翻譯。

### Bulk Translation Jobs

對於大量內容，請使用 **翻譯工作**：

1. 導航到 **Settings > Translation Jobs**
2. 創建一個新工作，選擇：
   - **內容類型** — 產品、頁面、部落格文章、分類等。
   - **來源語言** — 要翻譯的語言
   - **目標語言** — 一個或多個要翻譯成的語言
   - **範圍** — 所有內容，或僅未翻譯的欄位
3. 提交工作 — 它通過任務佇列在背景中運行
4. 在工作列表中監控進度（已排隊 → 處理中 → 完成）

當您啟用一種新語言並希望一次性翻譯整個目錄時，批量工作非常有用。

## Translation Management

### Reviewing Translations

每個翻譯的欄位追蹤：
- **翻譯狀態** — 欄位是否已機器翻譯、手動編輯或缺失
- **鎖定狀態** — 已鎖定的翻譯不會被未來的機器翻譯覆蓋
- **最後翻譯時間** — 翻譯最後生成或編輯的時間

### Locking Translations

如果您手動編輯機器翻譯以改進它，**鎖定**該欄位以防止在下一次批量翻譯運行時被覆蓋。已鎖定的欄位在自動翻譯期間會被跳過。

### Translation Coverage

覆蓋追蹤器顯示每個語言的內容翻譯百分比。導航到 **Settings > Languages** 以查看：
- 每種語言的完成百分比
- 哪些內容類型存在缺口
- 還需要翻譯的欄位

## UI Translation Overrides

除了產品和頁面內容，您還可以自定義 **前端介面字串** 的翻譯——按鈕、標籤、訊息和其他顯示給訪客的UI文字。

導航到 **Settings > UI Overrides** 以：
1. 搜索特定字串（例如，"Add to Cart"）
2. 為每個語言輸入您偏好的翻譯
3. 儲存 — 覆蓋立即生效

大約有 300 個前端字串可供自定義。覆蓋優先於預設翻譯。

## Tips

- 首先只啟用您的客戶實際使用的語言 — 您始終可以稍後添加更多語言。
- 使用 **本地AI模型** 進行日常翻譯 — 它快速、私密，且沒有每筆翻譯的費用。
- 如果您需要關鍵歐洲語言的最高品質，請考慮 **DeepL** — 它始終產生比通用模型更自然的翻譯。
- 始終 **審核機器翻譯** 產品名稱、品牌術語和營銷文案 — AI 在處理技術內容方面表現良好，但可能在創意文字中遺漏細節。
- **鎖定** 您已手動優化的任何翻譯，以保護它們不被批量翻譯運行覆蓋。
- 當啟用新語言時，使用 **批量翻譯工作** 一次性翻譯整個目錄，而不是逐一翻譯產品。
- 自定義 **UI 覆蓋** 以匹配您的品牌語氣 — 例如，如果這更適合您的商店，可以將 "Add to Cart" 改為 "Buy Now"。

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.