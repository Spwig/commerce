---
title: 受眾
---

一個 **分段** 是一個已儲存的受眾，您可以將廣告活動、旅程或 A/B 測試指向它 —— Campaign Studio 自己的分段清單稱之為「目標受眾」，而本指南中會同時使用這兩個詞彙來指稱同一事物。每個分段可以是 **動態** 的，由 Spwig 每次使用時都會重新評估的規則定義，或者是 **靜態** 的，由您手動選擇的訂閱者明確清單。

本指南涵蓋建立動態分段的規則 —— 包括針對您商店本身的客戶價值桶、忠誠度計畫和代理商的較新欄位 —— 以及一鍵 **新增起始受眾** 按鈕，該按鈕會從您商店已有的任何資料中建立一組預設的分段。

## 動態與靜態分段

| 類型 | 如何運作 | 最適合用於 |
|---|---|---|
| **動態（規則）** | 您定義條件 —— 例如「總支出至少為 500 美元」。Spwig 每次使用分段時都會重新計算誰符合條件，因此當您的訂閱者變動時，成員資格會自動變動。 | 永續的受眾，應該始終保持最新，例如「VIP 客戶」或「90 天內未下單」。 |
| **靜態（固定清單）** | 您手動新增或刪除的訂閱者明確清單。除非您變更，否則成員資格永遠不會變更。 | 一次性清單 —— 來自特定活動的每個人，或為一次性發送而手動挑選的小組。 |

建立分段時，請選擇 **類型** 字段。本指南其餘部分將探討動態分段 —— 靜態分段只是沒有設定規則的成員清單。

## 建立動態分段

開啟 **Campaign Studio > 分段**，然後點擊 **+ 新增分段**（或開啟現有的動態分段）以進入 **受眾規則** 編輯器。點擊 **+ 新增條件** 來新增一則規則，選擇要檢查的內容以及如何檢查，並設定訂閱者是否必須符合 **所有** 或 **任何** 您的條件。右上角的即時數字 —— 例如「8 個符合的訂閱者」—— 在每次變更後會立即更新，讓您在儲存前可以精確看到誰符合資格。

![The Audience rules builder with Customer segment, Loyalty tier, Lifetime value, and Affiliate conditions set, and a live matching-subscriber count](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

一個具有固定 **is true** 模式的條件 - **已下單**, **已訂閱營銷郵件**, **忠誠會員**, **合作夥伴** - 僅需選擇欄位本身即可; 不需要設定運算子或值。

## 您可以針對的內容

| 欄位 | 檢查內容 | 
|---|---| 
| **總消費金額** | 累計訂單總金額。 | 
| **訂單數量** | 完成的訂單數量。 | 
| **終身價值** | 客戶的計算終身價值。 | 
| **平均訂單金額** | 每筆完成訂單的平均金額。 | 
| **自最後下單以來的天數** | 客戶最近下單以來的天數 —— 選擇 90 天以上以建立回籮客群。 | 
| **已下單** | 客戶是否至少有一筆完成的訂單。 | 
| **已訂閱營銷郵件** | 會員是否同意接收營銷郵件。 | 
| **語言** | 會員的儲存語言。 | 
| **來源** | 會員加入的方式 —— 商店註冊、匯入、下單、手動新增，或 API。 | 
| **加入日期後** | 在所選日期或之後加入的會員。 | 
| **有標籤** | 會員是否擁有您建立的 [標籤](/help/subscriber-tags)。 | 
| **客戶群組** | 客戶是否屬於您商店的自定 [客戶群組](/help/customer-segments) —— 一般顧客、新顧客、常客、頻繁買家、高價值顧客、VIP 顧客、貪婪買家、有風險顧客，或無活躍顧客。 | 
| **忠誠會員** | 客戶是否為忠誠計畫的活躍成員。 | 
| **忠誠點數** | 成員目前可使用的點數餘額。 | 
| **忠誠等級** | 成員目前所屬的忠誠等級。 | 
| **合作夥伴** | 客戶是否為您活躍的合作夥伴。 | 

**客戶分群**、兩個**忠誠度**值欄位、**忠誠度等級**以及**聯盟行銷**是較新的新增項目，且只有在您的商店實際擁有該類數據時，才會在條件選擇器中顯示：忠誠度欄位會在您的忠誠度計畫有會員且至少有一個活躍等級時出現，**聯盟行銷**會在您至少擁有一位聯盟行銷夥伴時出現，而**客戶分群**則會在您至少設定了一個活躍的客戶分群時出現。

在一個全新的商店中，您不會看到任何不可能匹配到任何人的選項。

有一個目前值得了解的限制：對於任何具有選項下拉選單的條件——**語言**、**來源**、**擁有標籤**、**客戶分群**、**忠誠度等級**——**是其中任一**操作員目前仍一次只能選擇一個值。如果您想要匹配多個值（例如，屬於您的 VIP 或高價值分群的客戶），請為每個值添加一個條件，並將**匹配**設定為**任一**。

## 添加初始受眾

為每個明顯的受眾（您的 VIP、忠誠度會員、所有已沉默的客戶）從零開始建立規則會很繁瑣，因為 Spwig 已經可以看到誰符合資格。在分群列表中，點擊**添加初始受眾**，Spwig 將根據您商店現有的客戶、忠誠度和聯盟行銷數據，創建一組現成且可編輯的動態分群。

![帶有「新增分群」和「添加初始受眾」按鈕的分群列表](/static/core/admin/img/help/audiences/segments-changelist.webp)


| Starter | Targets | Needs |
|---|---|---|
| **VIP customers** | Your VIP customer segment | An active VIP customer segment |
| **High-value customers** | Your VIP and High Value customer segments | An active VIP or High Value customer segment |
| **Repeat buyers** | Your Frequent Buyer and Regular customer segments | An active Frequent Buyer or Regular customer segment |
| **New customers** | Your New customer segment | An active New customer segment |
| **Lapsing customers** | Customers who've ordered before but not in the last 90 days | Any customer order history |
| **Loyalty members** | Everyone active in your loyalty programme | An active loyalty programme with members |
| **Top loyalty tier** | Members in your highest-ranked loyalty tier | At least one active loyalty tier |
| **Affiliates** | Your active affiliate partners | At least one affiliate |

Spwig only creates the starters it actually has data for — a store with no loyalty programme yet simply won't get a **Loyalty members** starter, rather than an empty one that could never match anyone. Spwig confirms exactly what it added, for example: "Added 7 starter audience(s): High-value customers, Repeat buyers, New customers, Lapsing customers, Loyalty members, Top loyalty tier, Affiliates."

![Success message confirming which starter audiences were just added](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

It's safe to click **Add starter audiences** more than once. Spwig never creates a duplicate of a starter that already exists, so clicking it again after setting up (say) your loyalty programme for the first time only adds whatever's newly available — if everything's already set up, it simply says so.

![Info message shown when every starter audience already exists](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

如果刪除了不想再使用的起始群組，再次點擊 **新增起始群組** 也不會再出現它，Spwig 會將其視為您刻意移除的群組，而不是需要重新建立的群組。

一旦設定完成，起始群組就會變成一般的動態群組：您可以從清單中開啟它來檢閱或調整其規則，重新命名它，或刪除它，與您自行建立的任何群組操作方式完全相同。

## 這些群組實際上會觸及哪些受眾

上述的客戶、忠誠會員和合作夥伴條件只會符合電子郵件已連結至客戶帳戶的訂閱者 —— 未登入的通訊名單註冊不會符合 **忠誠會員** 或 **VIP** 條件，即使正確無誤，因為 Spwig 沒有訂單或忠誠資料可供比對。如果您的許多客戶已有帳戶但尚未訂閱，請請管理 Spwig 安裝的人執行一次訂閱者同步 —— 這會在一步之內為每個現有客戶帳戶建立一個訂閱者記錄，讓這些群組有真實的人可以比對。

不管一個群組有多少個訂閱者，該數字僅描述誰 *可以* 接收推播訊息，而不是誰實際會接收到。每次傳送時仍會先檢查每個訂閱者的行銷同意意願，因此群組永遠不會是繞過此程序的方式。

## 小技巧

- 從起始群組出發並調整它，而不是手動建立相同的規則 —— 一旦建立，起始群組與您自行建立的任何群組沒有差異。
- 布林條件如 **忠誠會員**、**合作夥伴** 和 **已下過訂單** 不需要運算子或值 —— 只需加入該條件即可。
- 將較新的欄位與原始欄位結合，以達到更精準的定位，例如 **忠誠會員** 加上 **已同意行銷**，而不是單獨依賴一個條件。
- 如果一個群組的規則引用了之後已被刪除的內容 —— 一個已刪除的客戶群組、一個已清空的標籤等等 —— Spwig 會將其視為匹配到無人，而不是回退到整個訂閱者清單。

受眾定位錯誤的傳送；它不會意外地向所有人廣播。
- 如果某個群組的成員數看起來已過時，請開啟它並再次儲存，或從「群組」清單中使用 **重建成員數** 批次動作，馬上重新計算。
- 當您建立規則時，請注意即時「符合訂閱者」數目 —— 這是最快的方式，可在儲存前發現條件過於狹窄（或過於寬泛）的情況。