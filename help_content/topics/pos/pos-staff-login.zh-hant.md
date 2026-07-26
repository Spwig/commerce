---
title: POS員工登錄與生物特徵登錄
---

每個在POS櫃檯服務顧客的人都需要一個具有正確權限的員工帳戶。本主題說明如何創建該帳戶，將員工指派到終端機，並設置生物特徵登錄，讓他們可以使用指紋、臉部掃描或硬體密碼來解鎖櫃檯，而不是每次都要輸入密碼。

如需PIN碼、折扣限制和終端機鎖定設置，請參閱[POS員工折扣與終端機安全](pos-staff-discounts)。

## 員工使用POS終端機所需的條件

要登錄POS終端機，一個人需要：

1. 一個**員工帳戶** — 一個啟用**員工狀態**標記的Spwig用戶。
2. 一個**包含POS訪問權限的角色** — 角色控制員工在管理後台可以做什麼。需要一個具有POS權限的角色才能訪問櫃檯。
3. **指派到終端機** — 終端機必須將其列為已指派的員工，或者他們必須在商店位置層面被指派。

## 創建具有POS資格的員工帳戶

導航至 **員工與帳戶 > 員工**（或前往 `/admin/accounts/staffmember/`）。

1. 點擊 **+ 添加員工**。
2. 填寫員工的 **名字**、**姓氏** 和 **電子郵件地址**。
3. 設置一個臨時密碼，並請員工在首次登錄時更改密碼。
4. 確保 **員工狀態** 已勾選 — 這就是讓他們能夠登錄管理後台和POS應用程序的條件。
5. 點擊 **保存**。

> **注意：** 不要為普通收銀員或主管勾選 **超級用戶狀態**。超級用戶狀態會繞過所有權限檢查，應僅保留給商店老闆。

### 指派具有POS訪問權限的角色

員工帳戶本身沒有權限 — 角色授予特定功能。創建帳戶後，打開員工的記錄並前往 **角色** 一節。指派一個包含POS訪問權限的角色。

如需完整說明角色的工作方式以及應包含哪些權限，請參閱[員工角色](staff-roles)。

screenshot-needed

/en/admin/accounts/staffmember/

staff-user-list.webp

Staff member list showing a POS-eligible user with their role badge

image

Staff member list

/static/core/admin/img/help/pos-staff-login/staff-user-list.webp

heading

Assigning staff to a terminal

paragraph

Settings follow a cascade: **Site default → Store group → Store location → Individual terminal**. For most stores, the right place to assign staff is at the terminal level.

list

paragraph

Staff members who appear in the **Assigned staff** list for a terminal are able to select their name on that terminal's login screen. Staff not assigned to any terminal can still log in by typing their email directly.

blockquote

**Tip:** If your store has many staff rotating across terminals, assign them at the store location (warehouse) level rather than terminal by terminal. Any staff member assigned to the location automatically has access to all terminals at that location.

heading

Logging in at the POS register

paragraph

When a cashier opens the POS application (`/pos/`) on a terminal, they see a staff selection screen. The login flow works as follows:

list

paragraph

For PIN-based unlock (after the terminal locks during a shift), see [POS Staff Discounts & Terminal Security](pos-staff-discounts).

heading

Biometric login

paragraph

Biometric sign-in lets a cashier touch a fingerprint sensor, glance at a face camera, or tap a hardware key instead of typing a password. On a busy register this saves several seconds per shift and avoids mistakes during peak hours.

Spwig 使用 **WebAuthn** 瀏覽器標準進行生物特徵登錄。

"WebAuthn 凭證" 是一個與設備綁定的金鑰對：私鑰儲存在設備的安全硬體中，且永遠不會離開設備。

POS 應用程式透過瀏覽器與該硬體進行通訊。

### 支援生物特徵登錄的設備和瀏覽器

WebAuthn 受所有現代瀏覽器支援 — Chrome、Edge、Firefox 和 Safari — 在具有相容硬體的設備上。常見且運作良好的組合如下：

| 設備 | 驗證器 |
|--------|---------------|
| iPad (Touch ID) | 透過 Safari 或 Chrome 的指紋 |
| Android 平板 | 透過 Chrome 的指紋或臉部辨識 |
| Windows 平板或電腦 | Windows Hello（指紋、臉部或 PIN） |
| 任何設備 + 安全鍵 | USB、NFC 或藍牙 FIDO2 鍵（例如 YubiKey） |
| iPhone (Face ID) | 透過 Safari 的臉部辨識 |

當瀏覽器確認該設備上為當前用戶註冊了憑證時，POS 應用程式才會顯示生物特徵登錄選項。

### 註冊流程

註冊是在 POS 終端進行，而不是在管理後台。員工必須先完成正常的密碼登錄，然後在 POS 應用程式中選擇設置生物特徵登錄。瀏覽器會提示他們使用設備的生物特徵感應器（或儲存在他們 iOS/macOS/Windows 帳戶中的 passkey）來驗證身分。確認後，憑證會被儲存，未來在該設備上上班時即可使用生物特徵登錄。

一名員工可以在多個設備上註冊 — 例如個人平板和共用收銀機 — 且每個設備都會儲存自己的憑證。

> **注意：** 註冊提示的確切文字（例如 "註冊生物特徵"、"設置指紋登錄" 等）來自 POS 應用程式，可能因瀏覽器和設備而異。

### 使用生物特徵登錄

註冊後，登錄畫面上會顯示一個生物特徵登錄按鈕（指紋圖示或其他類似圖示）。收銀員：

1.

在终端的登录屏幕上輕觸他們的名字。
2.

輕觸 **使用指紋登入**（或等效選項）。
3.

觸碰感應器或看向鏡頭。
4.

終端會立即解鎖。

如果生物特徵驗證失敗（指紋未被識別、面部被遮擋），收銀員將回退到輸入密碼。

### 撤銷憑證

如果設備遺失、被盜或員工離職，您應立即移除其生物特徵憑證。

1. 進入 **員工與賬戶 > 員工**。
2. 打開員工的記錄。
3. 向下滾動到 **POS 設置** 一節。
4. 在 **生物特徵解鎖** 行中，點擊 **全部移除**。
5. 確認操作。

這會移除該員工在所有設備上註冊的所有 WebAuthn 憑證。下次他們嘗試在任何終端使用生物特徵登入時，將需要改用密碼登入。

> **重要提示：** 在此處移除憑證不會阻止員工使用密碼登入。要完全撤銷訪問權限，還需停用其員工賬戶或從終端的指定員工列表中移除他們。

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: 員工更改表單顯示 POS 設置部分，包含生物特徵憑證數量和全部移除按鈕
-->

## 安全提示

- **憑證與硬體綁定。** 私鑰永遠不會離開設備的安全元件。

如果平板電腦遭竊，攻擊者無法提取生物特徵密鑰 — 他們仍需繞過設備本身的鎖屏畫面，瀏覽器才會釋放密鑰。
- **遺失設備不會洩漏密碼。** WebAuthn 會取代該設備的密碼；員工的密碼是獨立且不受影響的。
- **員工離職時應立即撤銷。** 在為員工進行離職處理時，請在同一個會話中移除生物特徵憑證並停用員工帳號。
- **生物特徵本身從未傳輸。** 指紋或臉部掃描完全由設備硬體處理。

Spwig 只會收到已簽名的挑戰回應，而不會收到任何生物特徵資料。

## 故障排除

### "使用指紋登入" 按鈕未顯示

生物特徵選項只會在以下情況出現：
- 員工已在這台特定設備上註冊了憑證。
- 瀏覽器支援 WebAuthn（所有現代瀏覽器都支援 — 如果使用的是舊版瀏覽器，請進行更新）。

如果按鈕未顯示，表示員工尚未在這台設備上註冊。他們應使用密碼登入，並透過 POS 應用程式設定生物特徵登入。

### 註冊失敗

常見原因：
- **瀏覽器拒絕權限。** 瀏覽器請求訪問驗證器的權限，但員工拒絕了。員工需要再次嘗試，並在提示時點選 **允許**。
- **未找到相容的驗證器。** 設備沒有指紋感應器、臉部攝像頭或安全金鑰。請檢查設備硬體。
- **重複的憑證。** 員工可能已經在這台設備上註冊過。在重新註冊時，現有的憑證會被排除，以避免重複。

### 生物特徵在一台設備上可用，但在另一台設備上不可用

每台設備都會儲存自己的憑證。在 iPad 上註冊不會自動在第二台 iPad 上生效。員工必須在他們將使用的每台設備上分別完成註冊。

### 跨設備的 Passkey

# 一些操作系统（iOS 16+、macOS Ventura+、使用 Microsoft 帳戶的 Windows 11）可以透過 iCloud Keychain 或 Windows Hello 在多個裝置之間同步 passkey。

如果員工使用同步的 passkey 登記，可能會自動在多個裝置上運作。

行為取決於作業系統和瀏覽器，而不是 Spwig。

## 小技巧

- 在員工到達班次前，在共用收銀機上設定生物特徵登入 —— 在沒有顧客等待的情況下，兩分鐘的登記過程會更順利。
- 為收銀員分配一個具有有限 POS 權限的角色，並為主管分配一個獨立的管理員角色。請確保他們的帳號與商店擁有者帳號不同。
- 當員工更換裝置（新平板、新手機）時，請先讓他們在新裝置上完成登記，如果舊裝置不再使用，請從管理員介面撤銷舊憑證。
- 對於員工流動率較高的商店，請定期檢查每個終端機上的 **已指派員工** 清單，並移除不再在該地點工作的員工。
- 如果您使用硬體安全金鑰（如 YubiKey 或類似產品），一個金鑰可以在多個終端機上登記，而無需對管理員進行任何更改 —— 只需插入金鑰並在每個終端機上完成登記即可。