---
title: Webhooks 概述
---

Webhooks 讓您的商店在發生特定事件時自動通知外部系統 — 例如庫存工具、ERP、履行服務或自定義應用程式。與這些系統不斷詢問『有什麼改變嗎？』不同，您的商店會在事件發生的那一刻推送通知。

## Webhooks 的功能

當您的商店發生事件（例如訂單下單、收到付款、產品缺貨）時，Spwig 會將事件資料以 HTTP POST 請求傳送至您設定的 URL。接收系統可以立即根據這些資料採取行動 — 例如更新庫存、觸發運送標籤或發送自定義通知。

Webhooks 的常見用途包括：

- 與履行夥伴即時同步訂單
- 當庫存變動時更新 ERP 中的庫存
- 在訂單狀態變更時觸發簡訊或推送通知
- 在資料倉儲中記錄事件以供報告
- 連接到 Zapier 或 Make 等自動化工具

## 查看和管理端點

導航至 **整合 > Webhooks** 以查看所有已配置的 Webhook 端點。

![Webhook 端點列表](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

清單顯示每個端點的名稱、URL、啟用狀態、它訂閱了多少個事件、其健康狀態以及上次接收傳遞的時間。

### 健康狀態指標

**健康狀態** 欄位可讓您一目了然地了解每個端點的表現：

- **健康** — 所有最近的傳遞都已成功
- **退化** — 有些最近的失敗，但端點仍然處於啟用狀態
- **不健康 / 已停用** — 端點在連續失敗太多次（預設為 10 次）後自動停用。您必須在根本問題解決後手動重新啟用它。

## 建立 Webhook 端點

點擊 **+ 添加 Webhook 端點** 以打開設定向導。向導會引導您完成四個步驟。

### 第 1 步：基本資訊

- **名稱** — 用來識別此端點的友好標籤（例如，`Order Fulfilment Service` 或 `Inventory Sync`）。
- **URL** — 將接收 webhook POST 請求的伺服器的完整 URL。

此 URL 必須是公開可訪問的（不是 localhost URL）。
- **描述** — 關於此端點用途的可選說明。
- **啟用** — 是否應將交付傳送至此端點。

取消勾選可暫時停止交付，而無需刪除端點。

### 第 2 步：事件訂閱

選擇哪些事件應觸發向此端點的交付。事件按類別分組：

#### 訂單事件

| 事件 | 觸發時機 |
|-------|---------------|
| `order.created` | 新訂單產生 |
| `order.paid` | 訂單付款確認 |
| `order.cancelled` | 訂單被取消 |
| `order.fulfilled` | 訂單中所有商品已發貨 |
| `order.partially_fulfilled` | 訂單中部分商品已發貨 |
| `order.status_changed` | 訂單狀態變更 |
| `order.note_added` | 向訂單添加備註 |

#### 支付事件

| 事件 | 觸發時機 |
|-------|---------------|
| `payment.received` | 收到付款 |
| `payment.failed` | 付款嘗試失敗 |
| `payment.pending` | 付款正在等待確認 |

#### 運送事件

| 事件 | 觸發時機 |
|-------|---------------|
| `shipment.created` | 建立運送 |
| `shipment.shipped` | 運送已發出 |
| `shipment.delivered` | 運送已送達 |
| `shipment.returned` | 運送已退回 |
| `shipment.tracking_updated` | 跟進資訊已更新 |

#### 存貨事件

| 事件 | 觸發時機 |
|-------|---------------|
| `inventory.low_stock` | 存貨低於閾值 |
| `inventory.out_of_stock` | 產品缺貨 |
| `inventory.restocked` | 產品已補貨 |
| `inventory.adjusted` | 存貨已手動調整 |

#### 產品事件

產品的 `created`、`updated`、`deleted`、`published`、`unpublished` 事件

#### 顧客事件

`customer.created`、`customer.updated`、`customer.deleted`

#### 訂閱事件

`subscription.created`、`subscription.activated`、`subscription.renewed`、`subscription.cancelled`、`subscription.expired`、`subscription.paused`、`subscription.resumed`、`subscription.payment_failed`

#### 其他事件

`refund.created`、`refund.completed`、`refund.failed`、`cart.abandoned`、`cart.recovered`、`translation.job_completed`、`translation.job_failed`

若要接收所有事件，請訂閱 `*`（萬用字元）。這對於一般用途的日誌端點很有用，但會產生更多流量 —— 僅在生產整合中訂閱您實際需要的事件。

### 第 3 步：設定

- **最大重試次數** — Spwig 在放棄之前應重試失敗的傳遞多少次（預設：5）。每次重試都會使用指數退避間隔。
- **逾時時間（秒）** — 等待接收伺服器回應的時間，超過此時間後將標記傳遞為失敗（預設：30 秒）。只有在確定伺服器已知較慢時才增加此值。

### 第 4 步：安全性

每個 Webhook 端點都會自動產生一個 **簽名密鑰** — 一個 64 個字符的隨機金鑰。Spwig 使用此密鑰對每個 Webhook 負載使用 HMAC-SHA256 簽名進行簽名。

簽名包含在 `X-Webhook-Signature` 請求標頭中。您的接收伺服器應驗證此簽名，以確認請求確實來自您的商店，且未被篡改。

密鑰在管理介面中會被遮蔽顯示。若要查看或輪換密鑰，請使用 Spwig API。如果您懷疑密鑰已被泄露，請立即輪換密鑰。

## 啟用和停用端點

若要快速啟用或停用一個或多個端點，而無需逐一打開每個端點：

1.

勾選您要更改的端點旁的複選框
2.

保留所有 Markdown 格式、圖片路徑、程式碼塊和技術術語。

使用 **Action** 下拉選單選擇 **啟用選定的端點** 或 **停用選定的端點**
3.

點擊 **Go**

若要重新啟用因失敗而自動停用的端點，請選中該端點，並使用 **重置失敗次數** 的動作，然後重新啟用。請先解決導致失敗的問題，否則它會很快再次被停用。

## 小技巧

- 只訂閱你實際需要的事件 —— 無關的事件會在你的日誌中產生雜訊，並增加傳遞負載。
- 在處理載入的資料前，務必在接收伺服器上驗證 Webhook 的簽名。這可以保護你免受偽造請求的影響。
- 使用 **Description** 欄位來記錄這個端點連接到的系統或整合。這有助於幾個月後進行故障排除。
- 設定一個略高於伺服器典型回應時間的 **Timeout**。對於大多數整合來說，10–15 秒的超時時間已經足夠。
- 如果端點狀態變為 **Unhealthy**，請先檢查傳遞日誌（參見 **Webhook Deliveries**），了解失敗模式，再重新啟用它。
- 為了測試，可以將 Webhook 指向像 [webhook.site](https://webhook.site) 這樣的工具，以檢查原始資料載入，而無需使用實際的伺服器。