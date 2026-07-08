---
title: SSL 設置
---

SSL (Secure Sockets Layer) 會加密客戶瀏覽器與您商店之間的連線。當 SSL 啟用時，您商店的 URL 會以 `https://` 開頭，瀏覽器會顯示一個鎖頭圖示。SSL 對於接受付款、保護客戶資料以及在搜索引擎中獲得良好排名非常重要。

Spwig 支援多種 SSL 模式，以適應不同的主機設定。本指南說明每種模式，並幫助您選擇合適的模式。

## 選擇 SSL 模式

| 模式 | 最適合 | 證書費用 | 更新 |
|------|----------|-----------------|---------|
| **Let's Encrypt** | 大多數商店 | 免費 | 自動 |
| **Cloudflare Origin CA** | 使用 Cloudflare 代理的商店 | 免費 | 手動（最多 15 年） |
| **自訂證書** | 擁有購買證書的商店 | 各異 | 手動 |
| **外部管理** | 負載平衡器、Cloudflare 柔性模式 | 無 | 無 |
| **自簽證書** | 開發與測試 | 免費 | 手動 |
| **無（HTTP）** | 本地開發僅限 | 無 | 無 |

如果您不確定使用哪種模式，**Let's Encrypt** 是大多數商店的最佳選擇。它是免費、自動的，並受到所有瀏覽器的信任。

## Let's Encrypt

Let's Encrypt 提供免費且受信任的 SSL 證書，每 60-90 天自動更新。這是大多數商家的推薦選項。

**需求：**
- 您的域名必須指向您的伺服器（DNS 中的 A 記錄）
- 端口 80 必須能從網際網路存取（用於證書驗證）
- 一個用於證書到期通知的電子郵件地址

**設定步驟：**
1. 前往 **設定 > 網站設定** 並開啟 **域名與 SSL** 索引標籤
2. 輸入您的域名
3. 選擇 **Let's Encrypt**
4. 輸入您的管理員電子郵件地址
5. 點擊 **套用設定**

Spwig 會自動處理其他所有事項：驗證您的域名、取得證書、設定 NGINX 以及設定自動更新。

## Cloudflare Origin CA

Cloudflare Origin CA 證書會加密 Cloudflare 的邊緣伺服器與您商店之間的連線。這些證書是免費的，最多可持續 15 年，但它們**僅被 Cloudflare 所信任**——直接連接到您伺服器的瀏覽器會看到證書警告。

如果您的域名使用 Cloudflare 作為代理（啟用橙色雲），此模式是理想的選擇。Cloudflare 向訪客展示其自己的受信任證書，而 Origin CA 證書則用於加密 Cloudflare 與您伺服器之間的連線。

**需求：**
- 一個包含您域名的 Cloudflare 帳號
- 從 Cloudflare 控制台產生的 Origin CA 證書和私鑰
- Cloudflare SSL/TLS 模式設定為 **Full (Strict)**

**產生 Origin CA 證書：**
1. 登入您的 Cloudflare 控制台
2. 選擇您的域名
3. 前往 **SSL/TLS > Origin Server**
4. 點擊 **建立證書**
5. 選擇 RSA 或 ECC（RSA 最具兼容性）
6. 輸入您的域名（例如，`example.com` 和 `*.example.com`）
7. 選擇有效期限（建議 15 年）
8. 點擊 **建立** 並複製證書和私鑰

**在 Spwig 中設定：**
1. 前往 **設定 > 網站設定** 並開啟 **域名與 SSL** 索引標籤
2. 輸入您的域名
3. 選擇 **Cloudflare Origin CA**
4. 將證書貼到 **證書（PEM）** 欄位
5. 將私鑰貼到 **私鑰（PEM）** 欄位
6. 點擊 **套用設定**

**設定完成後：**
- 在 Cloudflare 中，將 SSL/TLS 模式設定為 **Full (Strict)**
- 啟用 Cloudflare 代理（橙色雲）於您的域名 DNS 記錄
- 您的商店將透過 HTTPS 以 Cloudflare 的受信任證書存取

## 自訂證書

如果您從證書權威機構（CA）如 DigiCert、Sectigo 或 GoDaddy 購買了 SSL 證書，或您的主機提供商為您發行了證書，請使用此模式。

**設定步驟：**
1.

前往 **設定 > 網站設定** 並開啟 **域名與 SSL** 索引標籤
2.

輸入您的域名
3.

選擇 **自訂證書**
4.

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

將您的證書鏈（包括中間證書）貼入 **Certificate (PEM)** 欄位
5.

將您的私鑰貼入 **Private Key (PEM)** 欄位
6.

點擊 **Apply Configuration**

您的證書應包含完整的鏈：您的域名證書後面接任何中間證書。私鑰應為 PEM 格式（以 `-----BEGIN PRIVATE KEY-----` 或 `-----BEGIN RSA PRIVATE KEY-----` 開頭）。

## Managed Externally

當您選擇此模式時，SSL 在流量到達您的伺服器之前由外部服務終止。在此設定中，您的伺服器只會收到純 HTTP 流量——伺服器本身不會安裝證書。

**常見情境：**
- **Cloudflare Flexible SSL** -- Cloudflare 加密瀏覽器到 Cloudflare 的流量，但會以 HTTP 將流量傳送至您的伺服器
- **雲端負載平衡器** -- AWS ALB、Google Cloud Load Balancer 或 DigitalOcean Load Balancer 終止 SSL 並轉發 HTTP
- **反向代理** -- Spwig 前面的另一台伺服器處理 SSL

**設定步驟：**
1. 前往 **Settings > Site Settings** 並開啟 **Domain & SSL** 索引標籤
2. 輸入您的域名
3. 選擇 **Managed Externally**
4. 點擊 **Apply Configuration**

Spwig 會設定 NGINX 僅提供 HTTP 並信任來自代理的 `X-Forwarded-Proto` 標頭，以正確偵測 HTTPS 訪問者。

## Self-Signed Certificate

自簽證書會加密連線，但瀏覽器不信任。訪問者會看到必須手動繞過的安全警告。此模式僅適合開發伺服器和內部測試。

**設定步驟：**
1. 前往 **Settings > Site Settings** 並開啟 **Domain & SSL** 索引標籤
2. 輸入您的域名
3. 選擇 **Self-Signed**
4. 點擊 **Apply Configuration**

Spwig 會自動產生自簽證書。請勿在生產環境中使用此模式。

## Troubleshooting

**設定後證書無法正常運作：**
- 確認您的域名的 A 記錄指向您的伺服器 IP 位址
- 確保防火牆已開放 80 和 443 埠
- 等待幾分鐘讓 DNS 變更生效

**Let's Encrypt 無法發佈證書：**
- 檢查您的域名是否解析到此伺服器的 IP 位址
- 確保防火牆未阻擋 80 埠
- 如果您使用 Cloudflare，請在證書發佈期間暫時將 DNS 設為 "DNS only"（灰色雲端）

**Cloudflare 顯示 "Error 526"（無效的 SSL 證書）：**
- 確認您選擇了 **Cloudflare Origin CA** 模式（而非 Managed Externally）
- 檢查 Cloudflare 的 SSL/TLS 模式是否設定為 **Full (Strict)**
- 確認 Origin CA 證書尚未過期

**瀏覽器顯示 "Not Secure" 即使已啟用 SSL：**
- 某些頁面可能透過 HTTP 載入圖片或腳本（混合內容）。請檢查瀏覽器的開發人員控制台是否有混合內容警告。
- 確保設定中的網站 URL 使用 `https://`