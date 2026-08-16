---
title: AI 購物
---

AI 購物讓 AI 購物助手找到您的產品，並在您允許的情況下，代表客戶從您的商店購買。預設情況下是關閉的——開啟此功能是明確的選擇，直到您開啟之前，您的商店不會向這些助手顯示任何內容。

## 開啟它

打開 **設定 → AI 購物**，並切換 **Agentic commerce enabled** 開啟。從那時起，支援 Universal Commerce Protocol 的助手可以發現您的商店並讀取您的目錄。您常規的 storefront 不會有任何變更。

## 就緒儀表板

AI 購物頁面的頂部用一句話回答了一個問題：**AI 助手現在真的能從您的商店購買嗎？**

- **"AI 助手可以從您的商店購買"** —— 購買所需的內容都已準備好。
- **"AI 助手可以瀏覽您的商店，但還不能購買"** —— 您的商店可以被發現，但在購買完成之前還有一些東西缺失（通常是連接的支付提供者）。
- **"緊急停止已打開"** 或 **"Agentic commerce 關閉"** —— 沒有任何內容被提供給助手。

在判決下方您會看到一個短清單——支付提供者已連接、運費可以報價、產品對助手可見——任何仍需關注的項目旁邊都有提示。計數器顯示助手可以銷售多少產品、您隱藏了多少給他們、多少助手訪問過，以及您阻止了多少。

清單反映了您的 **即時** 設定：連接支付提供者或新增運輸方式，下次打開頁面時判決會更新。

## 緊急停止

**緊急停止** 是與主開關分開的切換按鈕。當您發現有問題時，可以馬上切換它來停止所有助手活動——而無需更改您的設定。清除它以恢復。將主開關視為「此功能是否已設定」，緊急停止則是「馬上停止一切」。

## 助手可以做什麼

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

Two levels of access, controlled separately:

- **Reading** (discovery and browsing) is lower-risk. An assistant can find your store and read product details.
- **Checkout** (actually buying) is higher-stakes and stays closed to unverified assistants unless you allow it.

A store can be discoverable without being purchasable — a useful way to start.

## Hiding specific products

Every product has a **Visible to AI shopping agents** setting (on by default). Switch it off to keep a particular product off assistants while it stays on your storefront — handy for items you'd rather sell only through your own site.

## Managing individual assistants

When an assistant first buys — or tries to — Spwig records it under **AI Shopping → Agent Identities**. Each entry shows the assistant's verified home (the directory it signs with), its trust level, and how many requests it has made. The name and logo an assistant presents are shown only as *claimed* details — treat them as a label, not proof of identity; the verified home is the part that can be trusted.

Every assistant sits in one of three trust levels:

| Trust level | What it means |
|---|---|
| **Capped (verified, limited)** | The default for a new assistant. Spwig has recorded its identity, and it carries the order-value cap, spend cap, and tender restrictions set on its policy (see below). |
| **Verified (limits removed)** | A deliberate decision by you to trust this assistant fully. Its order-value and daily spend caps are cleared. |
| **Blocked** | The assistant can no longer buy from your store. Open checkouts end, though any payment already taken is left untouched. |

To stop an assistant, select it in the list and choose **Block selected assistants**. **Unblock selected assistants** always returns it to **Capped** — never straight to Verified — because lifting limits is a separate, deliberate step.

To lift an assistant's limits entirely, select it and choose **Promote to verified (remove limits)**.

這會清除其最髙訂單金額和每日消費上限，並將助理移至已驗證狀態。

被阻止的助理會被跳過 - 請先解鎖它，然後再提升其等級。

將此視為真實的信任決策：僅有足夠信心的助理才可被提升等級，因為驗證會刪除新助理出發時的防護機制。

## 設定助理的限制

開啟助理的詳情頁面，並使用 **策略（限制與允許的提議）** 部分來設定其可執行的內容：

| 欄位 | 它控制的內容 |
|---|---|
| **最髙訂單金額** | 這個助理可以下單的最大單筆金額。留空表示無上限。 |
| **每日消費上限** | 這個助理在一天內所有訂單中可以花費的最多金額。留空表示無上限。 |
| **允許折扣代碼** | 這個助理是否可以在結帳時套用優惠券代碼。 |
| **允許禮品卡** | 這個助理是否可以兌換禮品卡。 |
| **允許數位商品** | 這個助理是否可以購買數位產品。 |
| **速率限制（每分鐘）** | 這個助理每分鐘可以向你的商店發出多少個請求。 |

新助理預設會有具體的訂單金額和消費上限，並預設關閉折扣代碼、禮品卡和數位商品 - 這是一種故意保守的預設設定。更改任何這些欄位並儲存；每次變更都會寫入 **代理事件**，包含變更前後的值，因此你始終有紀錄顯示誰何時更改了什麼。將助理提升至已驗證狀態會為你清除其最髙訂單金額和每日消費上限 - 你不需要手動將它們留空。

## 活動紀錄

**AI Shopping → 代理事件** 是一個防偽的紀錄，顯示助理做了什麼 - 每個驗證過的請求、每個被阻止的嘗試、你所做的每個變更。它只能檢視，無法編輯或刪除，因此如果助理所購買的物品有任何爭議，它會成為你的證據鏈。

## 關於助理平台的注意事項

保留所有Markdown格式、圖片路徑、程式碼區塊和技術術語。

這些助手的運營公司（以及出現在其中的規則）是新出現的，且經常變更。

有些助手要求您在產品可以通過它購買之前先申請或滿足地區條件。

Spwig 會讓您的商店準備就緒；是否會列出您取決於該助手。
