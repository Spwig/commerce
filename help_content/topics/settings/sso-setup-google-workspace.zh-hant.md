---
title: SSO設定：Google Workspace
---

本指南將引導您將 Spwig 連接到 Google Workspace，以實現管理員的單一登入（SSO）。設定完成後，您的員工可以使用其 Google Workspace 帳戶登入 Spwig 管理面板。

**注意：** Google 可能會隨著時間更新 Cloud Console 的介面。這些說明是根據 2026 年初的介面撰寫的。如果任何步驟與您看到的有所不同，請參閱 Google 的官方文件 [設定 OAuth 2.0](https://support.google.com/cloud/answer/6158849)。

## 前提條件

- Google Workspace 訂閱（Google Workspace Business、Enterprise 或 Education）
- [Google Cloud Console](https://console.cloud.google.com) 的管理員存取權限
- 您的 Spwig 商店 URL（例如，`https://your-store.com`）
- 員工的電子郵件地址必須與其 Google Workspace 帳戶相符

## 第 1 步：建立或選擇 Google Cloud 專案

1. 訪問 [Google Cloud Console](https://console.cloud.google.com)
2. 點擊頂欄的專案選擇器
3. 點擊 **New Project**（或選擇現有專案，如果您偏好如此）
4. 輸入專案名稱（例如，`Spwig SSO`）
5. 選擇您的組織
6. 點擊 **Create**

## 第 2 步：設定 OAuth 授權畫面

1. 在 Cloud Console 中，導覽至 **APIs & Services > OAuth 授權畫面**
2. 選擇 **Internal** 作為使用者類型 — 這會限制登入僅限於您 Google Workspace 組織內的使用者
3. 點擊 **Create**
4. 填寫所需的欄位：

| 欄位 | 值 |
|-------|-------|
| **應用程式名稱** | `Spwig Admin`（或您的商店名稱） |
| **使用者支援電子郵件** | 您的管理員電子郵件地址 |
| **授權域名** | `your-store.com`（您的商店域名，不包含 `https://`） |
| **開發人員聯絡電子郵件** | 您的管理員電子郵件地址 |

5. 點擊 **Save and Continue**
6. 在 **Scopes** 頁面，點擊 **Add or Remove Scopes** 並新增：
   - `openid`
   - `email`
   - `profile`
7. 點擊 **Save and Continue**
8. 檢閱摘要並點擊 **Back to Dashboard**

## 第 3 步：建立 OAuth 凭證

1. 進入 **APIs & Services > Credentials**
2. 點擊 **Create Credentials > OAuth client ID**
3. 設定客戶端：

| 欄位 | 值 |
|-------|-------|
| **應用程式類型** | Web application |
| **名稱** | `Spwig SSO` |
| **授權重導向 URI** | `https://your-store.com/oidc/callback/` |

4. 點擊 **Create**
5. 對話框會顯示您的 **Client ID** 和 **Client Secret** — 複製這兩個值。您也可以將其下載為 JSON 以備存檔。

**重要：** 重導向 URI 必須完全符合 `https://your-store.com/oidc/callback/` — 包括結尾的斜線和 `https://` 協議。請將 `your-store.com` 替換為您實際的商店網域。

## 第 4 步：取得發現 URL

Google 為所有 Workspace 租戶使用單一標準的發現 URL：

```
https://accounts.google.com/.well-known/openid-configuration
```

此 URL 對每個 Google Workspace 組織都相同 — 您不需要根據租戶或網域進行自訂。

## 第 5 步：在 Spwig 中進行設定

1. 在 Spwig 管理介面中，進入 **Enterprise SSO > SSO Provider Configuration**
2. 將 **Provider Name** 設為 `Google Workspace`。
3. 輸入發現 URL：`https://accounts.google.com/.well-known/openid-configuration`。
4. 點擊 **Auto-Discover** — 這會自動填寫所有端點欄位。
5. 輸入第 3 步中的 **Client ID**。
6. 輸入第 3 步中的 **Client Secret**。
7. 點擊 **Save**。

### 声明映射

Google 使用標準的 OIDC 声明名稱，因此預設的 Spwig 設定可以直接使用：

| Spwig 設定 | Google 声明 | 預設值 |
|---------------|-------------|---------------|
| 電子郵件聲明 | `email` | `email` |
| 名字聲明 | `given_name` | `given_name` |
| 姓氏聲明 | `family_name` | `family_name` |

不需要對聲明映射進行任何更改。

## 第 6 步：啟用並測試

1.

進入 **Site Settings > Security** 索引標籤
2.

勾選 **Enable SSO for admin login**
3.

點擊 **Save**
4.


在 **私人/無痕模式** 瀏覽器中打開管理員登錄頁面
5.

您應該會看到一個 **使用 Google Workspace 登入** 按鈕
6.

點擊它 — 您應該會被導向 Google 的登錄頁面
7.

使用與 Spwig 員工用戶電子郵件匹配的 Google Workspace 帳戶進行登錄
8.

您應該會被導回 Spwig 管理員儀錶板

## 基於群組的角色映射

與 Microsoft Entra ID 或 Okta 不同，Google 預設不會在標準 OIDC 標記中包含群組成員資格。要在 Google 中實現群組聲明，需要使用 Google Workspace 目錄 API 並進行超出基本 OIDC 的額外配置。

對於大多數 Google Workspace 部署，我們建議直接在 Spwig 中管理員工和超級用戶狀態，而不是通過自動角色映射：

1. 在 Spwig 中創建具有適當權限的員工帳戶
2. 使用 Spwig 的員工角色系統來控制訪問權限
3. 員工通過 SSO 登入，Spwig 會使用他們現有的權限

如果您需要自動基於群組的角色映射，請參閱 [Google Workspace 管理員 SDK 目錄 API 文件](https://developers.google.com/admin-sdk/directory) 以配置自定義聲明。

## 常見問題

| 問題 | 原因 | 解決方法 |
|---------|-------|----------|
| **錯誤 400: redirect_uri_mismatch** | Google Cloud 中的重定向 URI 不完全匹配 | 確認重定向 URI 是 `https://your-store.com/oidc/callback/`，並包含結尾斜線。檢查 HTTP 與 HTTPS 的差異。 |
| **錯誤 403: access_denied** | 使用者不在 Google Workspace 組織中 | 使用 "Internal" 用戶類型時，只有組織內的使用者才能登入。確認使用者的帳號屬於您的 Workspace 域。 |
| **OAuth 許可畫面顯示 "此應用程式未驗證"** | 對於 Internal 應用程式來說是正常的 | 這個警告對 Internal 應用程式來說是預期的，不會影響功能。組織內的使用者仍然可以登入。 |
| **在 Google 登入成功但在 Spwig 登入失敗** | Spwig 中沒有匹配的使用者 | 確保 Spwig 中存在一個與 Google Workspace 帳號相同電子郵件的員工帳號。確認已正確配置 "限制為員工" 選項。 |
| **"存取被阻止：此應用程式的請求無效"** | 範圍未正確配置 | 確認已將 `openid`、`email` 和 `profile` 範圍新增至 OAuth 許可畫面。 |

## 小技巧

- **使用 "Internal" 用戶類型** — 這會限制登入至您的 Google Workspace 組織，且不需要 Google 的應用程式驗證流程。
- **Google 客戶密鑰不會過期** — 與 Microsoft Entra ID 不同，Google OAuth 客戶密鑰沒有過期日期。不過，您可以隨時從憑證頁面輪換它們。
- **一個專案用於多個應用程式** — 如果您有多個 Spwig 安裝，可以在同一個 Google Cloud 專案中建立多個 OAuth 客戶 ID。
- **使用非管理員帳號進行測試** — 在 Spwig 中建立一個測試員工帳號，並使用一般 Google Workspace 使用者（非超級管理員）來驗證 SSO 是否如預期運作。