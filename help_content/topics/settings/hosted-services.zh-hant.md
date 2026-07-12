---
title: Spwig 主機服務
---

Spwig 包含三項可選的雲端服務，您的商店可以使用這些服務，而無需自行配置或託管任何內容：**GeoIP** 可偵測訪客所在的地理位置，**Geocoder** 可將客戶地址轉換為地圖座標，而 **Push** 可向您的行動 Spwig 管理員應用程式傳送即時通知。在社區（免費）版中，每個服務都附帶足夠的每月配額。當任何服務接近其限制時，Spwig 會在管理員介面中提醒您，讓您決定是否在客戶尚未察覺之前升級服務。

## 三個主機服務

### GeoIP — 訪客國家檢測

GeoIP 會根據訪客的 IP 位址查找其所在國家。您的商店會使用此資訊，在客戶到達時自動顯示正確的貨幣，並在結帳時預先填寫國家欄位。例如，來自德國的訪客將看到以歐元顯示的價格，而來自日本的訪客將看到以日元顯示的價格，無需手動選擇。

每次 GeoIP 執行查詢的頁面加載都會計入您的每月配額。來自相同瀏覽器會話的重複訪問不會每次都消耗查詢次數；結果會在會話中緩存。GeoIP 查詢僅在商店前端執行，不會在您的管理員面板中執行。

### Geocoder — 地址轉換為座標

Geocoder 會將客戶輸入的地址轉換為地理座標（緯度和經度）。您的商店會使用這些座標做兩件事：當您在有自取點或基於半徑的運費規則時，計算基於距離的運費，以及在結帳頁面上啟動地址自動完成建議，讓客戶可以快速找到自己的地址。

當客戶在結帳時選擇或確認地址時，會觸發 Geocoder 查詢。與 GeoIP 一樣，結果會被緩存，因此相同地址在每個會話中只會查詢一次。

### Push — 管理員應用程式通知

Push 會將即時通知傳送至您的 Spwig 商家行動應用程式。

當有新訂單到來、庫存低於門檻值，或客戶發送訊息時，Push 會立即通知您的設備，讓您無需保持管理面板開啟即可回應。

傳送至您設備的每則通知都會計為一次 Push 請求，佔用您每月的配額。

## 社群版免費層

在 Spwig 的社群版中，每個服務在每月請求限制內都是免費的。具體限制由 Spwig 設定，可能會有所變化；您的管理儀表板始終會顯示您安裝的當前數字。付費方案（入門版、成長版、專業版、專業加強版）和擁有付費許可證的自托管安裝，每個服務的限制會更高。

當某項服務達到其社群版配額的 100% 時，該服務的請求將停止，直到下個日曆月重置計數器。對您商店的影響取決於受影響的服務：

| 服務 | 達到 100% 時的影響 |
|---------|----------------------|
| GeoIP | 貨幣自動偵測將回退到您商店的預設貨幣。客戶仍然可以手動更改貨幣。 |
| 地址編碼器（Geocoder） | 地址自動完成將停止提供建議。客戶仍然可以手動輸入地址。運費計算會繼續使用最後已知的坐標。 |
| Push | 新的管理應用程式通知會被排隊，但直到下個月或升級後才會傳送。 |

在所有情況下，您的商店都會正常運作——不會有任何訂單遺失，客戶仍然可以結帳。這些影響僅限於便利功能。

## 閱讀儀表板瓦片

**Spwig 服務使用情況** 瓦片會出現在您的管理儀表板首頁上。它會顯示每個服務的進度條。

瓦片中的每一行都遵循相同的佈局：

- **服務名稱**（左側）——GeoIP、地址查詢（Geocoder）或 Push 通知。
- **進度條**（中間）——使用情況增加時，進度條會從左到右填充。

當接近限制時，條狀圖的顏色會改變：
  - **綠色**——使用情況低於 80%。

Everything is running normally.
  - **Amber** — usage is between 80% and 99%。

The service is still running but getting close to the limit.
  - **Red** — usage has hit 100%。

The service is now throttled for this month.
- **Usage counts** (right) — the exact number of requests used out of the total allowed, for example `3,241 / 10,000`。

The label in parentheses shows the time window, typically `(this month)`。

If the tile cannot reach the Spwig update server to fetch your current usage (for example, if your server has no outbound internet access), the counts column shows a dash (`—`) for that service. This does not mean the service is broken; it means the usage display is temporarily unavailable。

### The Upgrade button

When any service reaches 80% or more, an **Upgrade** button appears in the top-right corner of the tile. Clicking it opens the Spwig upgrade page where you can compare plans and raise your service limits. The button disappears once usage drops back below 80% at the start of the next month。

## The quota warning banner

In addition to the dashboard tile, a banner appears at the top of every admin page whenever any service crosses the 80% threshold. The banner only appears on Community installs。

**Amber banner — approaching the limit (80–99%)**

> **Approaching hosted-services limit:** One of your Spwig services is over 80% of its Community-tier quota. Upgrade to raise the limit before it's hit。

This banner is an early heads-up. Your services are still running, and you have time to decide whether to upgrade before the month ends。

**Red banner — limit reached (100%)**

> **Spwig services limit reached:** One of your hosted services has hit its Community-tier quota. Upgrade to keep them running without interruption。

This banner appears when at least one service has hit 100% and is now throttled. Clicking **Upgrade** on either banner opens the same upgrade page as the tile button。

橫幅在計數器重置時會在下一個日曆月的第一天自動消失，或在您升級到付費計劃後立即消失。

## 電子郵件提醒 90%

當任何服務使用量達到其配額的 90% 時，Spwig 也會向您商店設置中配置的電子郵箱 (**設置 > 商店設置 > 聯絡 > 管理員郵箱**) 發送一次警告郵件。每個服務每個日曆月最多只會發送一次郵件，因此您不會收到大量郵件。當使用量達到 100% 時不會發送郵件，因為此時管理員介面中的橫幅已經清楚說明了情況。

如果您沒有收到郵件，請檢查您的管理員郵箱是否已在 **設置 > 商店設置** 中正確設置。

## 升級您的方案

當您從社群版升級到任何付費方案時，更高的限制會立即生效 — 不需要重新啟動商店或更改配置。儀表板磁磚會在下次刷新時顯示新的更高限制（在五分鐘內）。

要升級，請點擊儀表板磁磚或配額橫幅上的 **升級** 按鈕，或直接訪問 Spwig 的升級頁面。付費方案包含與社群版相同的三個託管服務（GeoIP、Geocoder、Push），但每月限制提高，並包含 Spwig 主機的電子郵件傳遞和優先支援。

## 自主託管和 Pro 授權

如果您使用自託管的 Spwig 安裝並擁有付費授權，您的授權等級將決定您的服務限制，與對應的託管方案相同。您的商店仍然需要出站互聯網訪問以連接到 `updates.spwig.com`，以便平台可以獲取和驗證您的等級配置。儀表板磁磚中顯示的使用計數器會從託管服務端點 `geoip.spwig.com`、`geocoder.spwig.com` 和 `push.spwig.com` 獲取。

目前還沒有選項可以將 GeoIP、Geocoder 或 Push 替換為自託管的替代方案 — 這些服務僅由 Spwig 的基礎設施提供，並包含在所有版本中。

## 小技巧

保留所有 markdown 格式、圖片路徑、程式碼塊和技術術語。

- **定期在忙碌月份結束後檢查此圖塊** —— 促銷活動或銷售事件可能會大幅增加 GeoIP 和 Geocoder 查詢次數。

此圖塊會在客戶受到影響之前提前通知您。
- **貨幣備用方案對大多數客戶來說是無形的** —— 如果 GeoIP 達到限制，客戶將看到您商店的預設貨幣。

對於主要服務單一市場的商店來說，這很少會成為嚴重問題；對於真正國際化的商店則更重要。
- **地址自動補全是一種便利功能，而非阻礙** —— 當 Geocoder 被限流時，客戶仍然可以正常輸入並提交地址。

如果您經常舉辦促銷活動，導致結帳流量高，請考慮在忙碌時期前升級。
- **推送限流不會永久丟失通知** —— 限流期間隊列中的通知在月份重置或升級後不會回溯發送。

如果您嚴重依賴推送來接收時間敏感的訂單提醒，請在達到限制前升級，以確保不會錯過任何通知。
- **5分鐘緩存意味著圖塊不是完全即時的** —— 使用量數據大約每五分鐘在後台刷新一次。

在異常高流量時期，實際使用量可能略微高於圖塊顯示的數據。
- **設定您的管理員電子郵件地址** —— 只有在 **設定 > 商店設定 > 管理員電子郵件** 已填寫的情況下，90% 警告電子郵件才會生效。

確認此處已正確設定，以便在問題發生前收到提醒。