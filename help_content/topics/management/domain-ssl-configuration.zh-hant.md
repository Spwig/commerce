---
title: 域名與SSL設定
---

本指南說明如何將自訂域名連接到您的Spwig商店，並設定SSL憑證以實現安全的HTTPS存取。您可以在安裝時配置域名，或稍後新增一個。

## 安裝後新增域名

如果您在沒有域名的情況下安裝Spwig（使用伺服器的IP位址），您可以隨時新增一個。

### 第1步：設定DNS

透過您的域名註冊商或DNS服務商：

1. 建立一個**A記錄**，將您的域名（或子域名）指向伺服器的IP位址
2. 如果使用類似`shop.example.com`的子域名，請為`shop`建立A記錄
3. 等待DNS傳播——這通常需要5–60分鐘

驗證DNS記錄是否生效：

```bash
dig +short shop.example.com
```

這應該會傳回您的伺服器IP位址。

### 第2步：執行域名設定腳本

透過SSH連接到您的伺服器，並導航到Spwig安裝目錄：

```bash
./configure-domain.sh
```

此腳本將：

1. 要求您的域名
2. 驗證DNS是否指向您的伺服器
3. 更新商店的設定
4. 從Let's Encrypt取得免費的SSL憑證
5. 設定網頁伺服器使用HTTPS
6. 重新啟動相關服務

您的商店現在可以透過`https://yourdomain.com`存取。

### 第3步：更新商店設定

新增域名後，請登入您的管理面板，前往**商店設定**。確認**商店URL**與您的新域名相符。這確保電子郵件、發票和連結使用正確的位址。

## SSL憑證

### 自動SSL（Let's Encrypt）

在**獨立模式**下，安裝程式會自動從Let's Encrypt取得免費的SSL憑證。這些憑證：

- 為所有主要瀏覽器所信任
- 有效期限為90天
- 可自動續約——每日執行續約檢查，當憑證剩下不到30天時會自動續約
- 覆蓋您的精確域名（例如`shop.example.com`）

您不需要手動管理續約。

### 自簽名憑證


在某些情況下，Spwig 會使用自簽證書代替：

- **本地模式** 安裝（開發/測試）
- 當 Let's Encrypt 無法連接到您的伺服器（防火牆阻擋 80 埠，DNS 尚未傳播）
- 當未配置域名（僅通過 IP 訪問）

自簽證書會加密流量，但瀏覽器不信任它 — 訪問者會看到安全警告。這對於測試是可以接受的，但不應該用於生產環境。

### Sidecar 模式 SSL

在 **sidecar 模式** 中，您現有的網頁伺服器（Apache、Nginx、Caddy 等）會處理 SSL 終止。Spwig 在您的代理後面運行在 HTTP 埠上。請按照平常方式在您的主網頁伺服器上配置 SSL。

安裝程式會生成一個代理配置區塊，您可以將其添加到您的網頁伺服器中。對於 Nginx，它看起來類似於：

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 更改您的域名

要切換到不同的域名：

1. 為新域名設置 DNS（A 記錄指向您的伺服器）
2. 再次運行 `./configure-domain.sh` 並使用新域名
3. 腳本會更新所有配置，獲取新證書，並重新啟動服務
4. 在管理面板中更新 **商店設置** 中的新 URL

一旦更新配置，您的舊域名將停止運作。

## 故障排除

### "DNS 驗證失敗"

configure-domain 腳本會在請求證書之前檢查您的域名是否指向您的伺服器。如果此檢查失敗：

- 使用 `dig +short yourdomain.com` 驗證 A 記錄是否正確
- 等待幾分鐘讓 DNS 傳播
- 檢查您是否配置了正確的域名或子域名（而不是萬用字元）

### "Let's Encrypt 請求限制已達"

Let's Encrypt 對每個域名每週的證書請求限制為 5 個。如果您達到此限制：

- 等待 7 天後再嘗試
- 在此期間使用不同的子域名
- 在等待期間，商店仍可透過 HTTP 或使用自簽證書存取

### "端口 80 無法連接"

Let's Encrypt 必須連接到您的伺服器的 80 端口以驗證域名所有權。請確保：

- 防火牆允許來自端口 80 的入站 TCP 連接
- 沒有其他應用程式阻擋端口 80
- 您的雲端服務提供商的安全群組或網絡防火牆允許端口 80

### 證書更新失敗

如果自動更新失敗，證書在 90 天後將過期。要手動更新：

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

如果此操作失敗，請檢查更新日誌以獲取詳細資訊。最常見的原因是在初始安裝後防火牆更改阻擋了端口 80。