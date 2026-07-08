---
title: SSO設定：Microsoft Entra ID
---

本指南將引導您將 Spwig 連接到 Microsoft Entra ID（原 Azure Active Directory），以實現管理員的單一登入（SSO）。設定完成後，您的員工可以使用他們的 Microsoft 工作帳戶登入 Spwig 管理面板。

**注意：** Microsoft 可能會隨著時間推移更新 Entra 管理中心介面。這些說明是根據 2026 年初的介面撰寫的。如果任何步驟與您看到的有所不同，請參閱 Microsoft 的官方文件 [在 Microsoft 身份驗證平台註冊應用程式](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)。

## 前提條件

- 有權訪問 Microsoft Entra ID 的 Azure 訂閱
- 在您的 Entra ID 租戶中具有 **應用程式管理員** 或 **全域管理員** 角色
- 您的 Spwig 商店 URL（例如：`https://your-store.com`）
- 員工的電子郵件地址必須與他們的 Microsoft 帳戶匹配

## 第 1 步：註冊應用程式

1. 登入 [Microsoft Entra 管理中心](https://entra.microsoft.com)
2. 導航至 **身分識別 > 應用程式 > 應用程式註冊**
3. 點擊 **新註冊**
4. 設定註冊：

| 欄位 | 值 |
|-------|-------|
| **名稱** | `Spwig Admin SSO`（或您偏好的任何名稱） |
| **支援的帳戶類型** | **僅限此組織目錄中的帳戶**（單租戶） |
| **重新導向 URI** | 平台：**Web**，URI：`https://your-store.com/oidc/callback/` |

5. 點擊 **註冊**

**重要：** 重新導向 URI 必須完全匹配 `https://your-store.com/oidc/callback/` — 包括結尾的斜線。請將 `your-store.com` 替換為您的實際商店網域。

## 第 2 步：記下應用程式 ID

註冊後，您將看到應用程式的 **概覽** 頁面。請記下這兩個值 — 您稍後會需要它們：

| 值 | 何处查找 | 用途 |
|-------|-----------------|---------------|
| **應用程式 (客戶端) ID** | 概觀頁面，頂部區域 | 在 Spwig 中輸入為 **Client ID** |
| **目錄 (租戶) ID** | 概觀頁面，頂部區域 | 用於構建發現 URL |

## 第 3 步：建立客戶端密碼

1. 在應用程式註冊中，導航至 **憑證與密碼**
2. 點擊 **新增客戶端密碼**
3. 輸入描述 (例如，`Spwig SSO`) 並選擇過期時間
4. 點擊 **新增**
5. **立即複製值** — 它只顯示一次。這是您要在 Spwig 中輸入的客戶端密碼。

**不要複製密碼 ID** — 您需要的是 **值** 欄位，而不是 ID 欄位。

**設置提醒**，在密碼過期前輪換密碼。當密碼過期時，SSO 將停止運作，直到您建立新的密碼並在 Spwig 中更新。

## 第 4 步：配置 API 權限

1. 導航至 **API 權限**
2. 確認 **Microsoft Graph > User.Read** (委派) 已列出。這是預設添加的。
3. 如果 `openid`、`email` 和 `profile` 權限未列出，點擊 **新增權限 > Microsoft Graph > 委派權限** 並添加它們。
4. 如果有提示，點擊 **為 [您的組織] 授予管理員同意**。

## 第 5 步：構建發現 URL

OIDC 發現 URL 的格式如下：

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

將 `{tenant-id}` 替換為第 2 步中的 **目錄 (租戶) ID**。

示例：如果您的租戶 ID 是 `a1b2c3d4-e5f6-7890-abcd-ef1234567890`，則發現 URL 是：

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## 第 6 步：配置群組聲明 (可選)

如果您希望 Spwig 根據 Entra ID 群組成員資格自動分配員工或超級用戶狀態：

1.

在應用程式註冊中，導航至 **令牌配置**
2.

點擊 **新增群組聲明**
3.

保留所有 markdown 格式、圖片路徑、程式碼塊和技術術語。

# 選擇要包含的群組類型（通常為 **Security groups**）
4.

在 **Customize token properties by type** 下，針對 **ID** 標記，選擇 **Group ID**
5.

點擊 **Add**

**Important:** Entra ID 會傳送群組 **Object IDs**（UUID，例如 `a1b2c3d4-...`），而不是群組顯示名稱。當您在 Spwig 中設定角色對應時，必須使用這些 Object IDs。

要查找群組的 Object ID：
1. 在 Entra 管理中心，前往 **Identity > Groups > All groups**
2. 點擊群組
3. 從群組的概覽頁面複製 **Object ID**

### Group Limit

Microsoft Entra ID 在標記中最多包含 **200 個群組**。如果用戶屬於超過 200 個群組，群組聲明將會被替換為連結到 Microsoft Graph API。對於群組數量非常多的組織，請考慮建立一個專用的安全群組以供 Spwig 使用，並使用 [group filtering](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) 來限制包含哪些群組。

## Step 7: 在 Spwig 中進行設定

1. 在 Spwig 管理介面中，前往 **Enterprise SSO > SSO Provider Configuration**
2. 將 **Provider Name** 設為 `Microsoft Entra ID`。
3. 將步驟 5 中的 Discovery URL 貼到 **OIDC Discovery URL** 中。
4. 點擊 **Auto-Discover** — 這會自動填寫所有端點欄位。
5. 輸入來自步驟 2 的 **Client ID**。
6. 輸入 **Client Secret**（值）來自步驟 3。
7. 如果您在步驟 6 中設定了群組聲明：
   - 將 **Groups Claim** 設為 `groups`。
   - 在 **Staff Groups** 中，輸入應為員工的群組的 Object ID（以逗號分隔）。
   - 在 **Superuser Groups** 中，輸入應為超級用戶的群組的 Object ID（以逗號分隔）。
8. 點擊 **Save**

## Step 8: 啟用並測試

1.

前往 **Site Settings > Security** 紙頁
2.

勾選 **Enable SSO for admin login**
3.

點擊 **Save**
4.

在 **private/incognito window** 中打開管理員登入頁面
5.

您應該會看到 **Sign in with Microsoft Entra ID** 按鈕
6.



# 4. 設定 Microsoft 登入

點擊它 — 您應該會被導向 Microsoft 的登入頁面
7.

使用電子郵件與 Spwig 員工用戶相符的 Microsoft 帳戶登入
8.

您應該會被導回 Spwig 管理儀表板

## 常見問題

| 問題 | 原因 | 解決方案 |
|---------|-------|----------|
| **AADSTS50011: 重導向 URI 不匹配** | Entra 中的重導向 URI 不完全匹配 | 確認重導向 URI 是 `https://your-store.com/oidc/callback/`，並包含結尾斜線。檢查 HTTP 與 HTTPS 是否不匹配。 |
| **AADSTS700016: 應用程式未找到** | 錯誤的 Client ID 或租戶 | 再次確認 Client ID，並確保發現 URL 使用正確的租戶 ID |
| 在 Microsoft 登入成功但 Spwig 登入失敗 | Spwig 中沒有對應的用戶 | 確保 Spwig 中存在與 Microsoft 帳戶相同電子郵件地址的員工帳戶。如果啟用了「僅限員工」，請確認用戶具有員工狀態。 |
| **Groups claim 為空** | 群組聲明未配置 | 跟隨步驟 6 將群組聲明加入令牌配置 |
| **Groups claim 返回 URL 而非 ID** | 用戶屬於超過 200 個群組 | 使用群組過濾來限制令牌中的群組，或指定特定群組 |
| **SSO 在幾個月後停止運作** | Client secret 過期 | 在 Entra 中建立新的 Client secret，並在 Spwig 的 SSO 提供者配置中更新 |

## 小技巧

- **使用安全性群組** 進行角色映射，而不是 Microsoft 365 群組或分發清單。

安全性群組是用於存取控制的，與 OIDC 声明配合使用時最可靠。
- **建議使用單一租戶** — 選擇「僅此組織目錄中的帳戶」可將 SSO 限制於您組織的用戶。


# 多租戶配置需要額外的驗證
- **設定較長的密钥過期時間** — 創建客戶端密钥時選擇24個月，並在22個月時設定日曆提醒以輪換它。
- **條件訪問** — 您可以在Entra ID中創建條件訪問策略，這些策略專門應用於Spwig應用程式註冊。

例如，要求多重驗證（MFA）、阻止來自不受信任位置的登錄，或要求使用合規設備。
- **使用非管理員帳戶進行測試** — 在Spwig中創建一個測試員工帳戶，以驗證SSO在全面部署到整個團隊之前是否正常運作。