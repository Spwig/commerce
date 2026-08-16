---
title: 收入歸因
---

收入歸因會顯示你的銷售實際來自哪裡 —— 不只是客戶購買前最後點擊的連結，而是所有在引導他們到達那裡的過程中發揮作用的管道。如果客戶在社交媒體上閱讀了你分享的部落格文章，然後一週後透過Google搜尋回來，最後點擊通訊稿中的連結購買，這三個接觸點都對該筆銷售有所貢獻。這個儀表板會根據你選擇的模型來歸因所有這些接觸點，讓你可以實際看到你的營銷效果，而不是「最後點擊獲勝」所偽裝的效果。

![收入歸因儀表板：歸因模型切換器、KPI條帶中顯示「與淨收入相符」的徽章、按管道分類的收入、時間序列收入、客戶旅程流程圖，以及活動表](/static/core/admin/img/help/revenue-attribution/dashboard-overview.webp)

## 如何找到它

導覽至側邊欄中的 **洞察 > 收入歸因**。洞察是一個專門的選單群組，位於產品上方，因此收入歸因有其獨特的頁面，與你的訂單和客戶報表分開。

洞察受 **洞察與分析** 權限類別的限制。如果你在側邊欄中沒有看到它，請要求商店管理員為你授予該權限 —— 請參閱 [員工角色與權限](/help/staff-roles) 以了解如何管理員工存取權限。

## 理解多接觸點歸因

大多數商店習慣以「這個訂單來自哪裡？」來思考，好像只有一個答案。實際上，顧客很少在第一次訪問時購買。他們以一種方式發現你，以另一種方式回來，以第三種方式轉化 —— 有時是在數天或數週內分散的幾次訪問中。每一次訪問都是一次 **接觸**：記錄到達你的商店並攜帶關於來源的訊號（電子郵件連結、搜尋結果、社交媒體貼文、聯盟連結等等）。

保留所有markdown格式、圖片路徑、程式碼區塊和技術術語。

**多-touch 傳遞** 意味著承認旅程中的每個接觸點，並決定每個接觸點在最終銷售中應得多少信用，而不是將全部信用給予最後點擊的渠道。

這一點至關重要，因為最後點擊報告系統性地低估了進行早期發現工作的渠道——你的部落格、你的自然搜索存在感、你的社交貼文——因為它們很少能在結帳前成為最後點擊。

## 選擇一個傳遞模型

儀錶板頂部的模型切換器是頁面上最重要的控制元件。點擊任何模型，儀錶板上的每個數字——KPI條紋、渠道條形圖、圖表、活動表格——都會即時重新分配信用以匹配。這是一個即時預覽，切換模型這裡改變了你查看現有收入的方式，它不會重寫任何記錄或更改你的商店的預設模型。

![傳遞模型切換器 - 最後接觸、首次接觸、線性、時間衰減和位置 40/20/40 - 顯示「即時重新分配 · 不重新處理」指示](/static/core/admin/img/help/revenue-attribution/model-switcher.webp)

| Model | What it does | Best for |
|-------|---------------|----------|
| **Last touch** | 給予最後一個接觸渠道全部信用，忽略之前的接觸（「直接」訪問除外，這些會被跳過，以最後一個真實來源為主） | 快速且常見的視圖 —— 大多數基本分析工具報告收入的方式 |
| **First touch** | 給予首次將客戶帶到您商店的渠道全部信用 | 理解什麼驅動新客戶發現和銷售管道頂端的增長 |
| **Linear** | 將信用均分給旅程中的每一個接觸點 | 在您不希望任何一個渠道被偏袒時，一種平衡且無偏見的視圖 |
| **Time decay** | 給予更接近訂單的接觸點更多信用，較遠的接觸點則較少 | 考慮週期較短的營銷活動，其中最近的推動至關重要 |
| **Position 40/20/40** | 給予第一個接觸點 40% 的信用，最後一個接觸點 40%，中間的則均分剩下的 20% | 既承認「誰找到我們」也承認「誰完成銷售」，同時仍將中間的旅程納入信用 |

沒有單一的「正確」模型 —— 每個模型都回答不同的問題。常見的做法是檢查 **First touch** 來查看什麼驅動發現，然後使用 **Last touch** 或 **Position 40/20/40** 來查看什麼驅動轉化，並同時使用這兩種視圖，而不是只選擇一種並忽略其他。

## 讀取 KPI 橫幅

在模型切換器下方，有四個數字總結當前選定的時間段和模型：

- **Attributed revenue** —— 當前模型中所有渠道的總 credited 收入。

當數字正確地與您商店在該期間的實際淨收入對應時，它會帶有 **Reconciles to net revenue** 標籤 —— 也就是說，模型正在將實際收入在渠道之間進行分配，而不是發明或遺失任何收入。
- **Orders** —— 選定日期範圍內的訂單數量。
- **Avg. touches / order** —— 每個訂單的平均記錄接觸次數。

一個大於1的數字證明了大多數客戶的購物旅程涉及多次訪問，這正是為甚麼多接觸點歸因對您的商店至關重要。
- **主要渠道** —— 在所選模型下，目前擁有最大歸因收入份額的渠道，以及其份額百分比和收入。

## 按渠道分類的收入

**按渠道分類的收入** 卡片為每個渠道顯示一個水平條形圖，其大小由歸因收入決定。 切換歸因模型，並觀察條形圖根據等級順序重新排列——這就是相同的底層收入，只是根據不同的規則重新分配，因此一個渠道在 **最後接觸** 下看起來強大，可能在 **首次接觸** 下下降幾個等級，如果它主要扮演支持角色的話。

## 收入隨時間的變化

**收入隨時間的變化** 圖表按渠道在所選時間範圍內的每一天堆疊歸因收入，讓您可以看到不僅僅是每個渠道的價值，還有其貢獻時間。 使用它來發現季節性模式，確認促銷活動的影響是否出現在您預期的日期，或者檢查某個渠道的貢獻是否在該時期內增長或減少。

## 客戶實際到來的方式

**客戶實際到來的方式** 面板 是一個旅程流程圖，將首次帶來客戶的渠道（左側）連接到轉化時的渠道（右側）。 細線表示通過該路徑流動的收入較少。 這是最直觀的方式來快速查看多步驟旅程——例如，從自然搜索到電子郵件 的粗線表示搜索帶來了訪客，但您的電子郵件營銷才是讓他們回購的原因。

![顯示首觸發渠道（左）流到每個訂單轉化所使用的渠道的客戶旅程流程圖，選中的是受影響的透鏡](/static/core/admin/img/help/revenue-attribution/journey-flow-sankey.webp)

在圖表上方使用 **歸因** / **受影響** 切換按鈕以更改透鏡：

- **Attributed** 將每個訂單的收入根據您選擇的模型進行分配，因此總計會等於 100% 的已歸因收入 —— 與儀表板其他地方顯示的數字相同。
- **Influenced** 會為每個接觸過訂單的渠道分配 *所有* 渠道，並以該訂單的 *完整* 金額計入，每個訂單只計一次。

這故意不會總計到 100% —— 一個渠道可能被計入其他渠道的完整收入。

其目的是揭示最後點擊報告所完全隱藏的渠道影響範圍，例如一篇部落格文章或社交分享，這些可能讓某人感興趣，即使他們在最後一次訪問時沒有點擊它。

## 優惠活動

**優惠活動** 表格會根據您標記的每個優惠活動來分解收入、訂單和平均訂單價值 (AOV) —— 連結或代碼，您已標記了優惠活動名稱，包括優惠活動標籤的禮券代碼（見 [禮券優惠活動想法](/help/voucher-campaign-ideas)）。用來比較個別促銷活動、影響者代碼或營銷推廣活動的表現，與其他活動進行對比，與它們所承載的渠道無關。

## 日期範圍和匯出您的資料

使用右上角的日期範圍選擇器來在 **最後 7 天**、**最後 14 天**、**最後 30 天**、**最後 90 天** 和 **本月至今** 之間 切換。整個儀表板會根據新時間段重新整理。

點擊 **匯出 CSV** 以下載當前所選模型和日期範圍的渠道分佈 —— 對於將數字導出到試算表或與合作機構分享非常有用。

## 點擊次數如何被記錄

Spwig 會在訪客到達您的商店並攜帶可識別的來源信號時自動捕捉點擊次數，且僅在訪客已給予您的商店的 cookie 訊息中的 **分析** 同意（如果您沒有運行同意訊息，預設會啟用追蹤，根據您商店自身的政策）。

這確保了收入歸因與您商店其他部分的分析在相同的隱私 足球場上。

保留所有 markdown 格式、圖片路徑、程式碼區塊和技術術語。

Several sources are tagged automatically, with no setup required:

| Channel | How it's identified |
|---------|----------------------|
| **Email** | Links in your marketing emails (not order or shipping emails) |
| **Organic / Paid Search** | Search engine referrers, or `utm_medium` values marking a paid search campaign |
| **Organic / Paid Social** | Social network referrers, or social `utm_medium` values |
| **Affiliate** | Links generated through your Affiliate program |
| **Refer a Friend** | Links generated through your customer referral program |
| **Campaign** | Any link or code carrying a campaign tag, including campaign-tagged voucher codes |
| **External Link** | An inbound link from another website that isn't otherwise categorized |
| **Direct** | No source signal was present — the visitor typed your address, used a bookmark, or arrived from an app with no referrer |

Blog posts that were auto-shared to your connected social accounts are automatically tagged, so traffic they generate shows up under the right social channel rather than being lost to Direct or External Link.

You can also tag your own links by hand using standard `utm_source`, `utm_medium`, and `utm_campaign` parameters on any URL pointing at your store — useful for print materials, partner newsletters, or any channel Spwig doesn't auto-tag.

## Limitations to keep in mind

- **Attribution follows a browser, not a person.** If a customer researches on their phone and buys on their laptop, those are two separate journeys as far as tracking is concerned — there's no way to link activity across different devices.

這意味著一些本應來自其他裝置上早期接觸的信用將會出現在Direct（直接）渠道。
- **Direct（直接）是未追蹤流量的歸屬渠道。** Direct（直接）渠道的高比例並不必然表示人們是從記憶中輸入你的網址 —— 也可能表示客戶的早期接觸發生在其他裝置上，或者他們使用的連結未被追蹤。
- **未同意的隱私權表示沒有接觸被記錄。** 在你的Cookie通知中拒絕隱私權同意的訪客不會被追蹤，因此他們的訂單會顯示為Direct（直接），即使他們是通過你通常能識別的渠道到達的。

## 小技巧

- 在得出結論之前，檢查多個模型 —— 一個渠道在 **最後接觸** 下看起來很弱，但在 **首次接觸** 下可能成為你最強的發現來源。
- 如果 **Direct（直接）** 占據了你收入的很大一部分，請查看你是否可以將更多營銷連結加上 `utm_source`/`utm_medium`/`utm_campaign` 優UTM追蹤參數 —— 未追蹤的流量沒有其他地方可以歸屬。
- 當你在決定是否繼續投資於像自然搜索或博客內容這樣的渠道時（這些渠道很少獲得最後點擊，但卻能持續引導旅程），請在旅程流程圖中使用 **Influenced（影響）** 觀點。
- 比較 **平均每次訂單的接觸次數** 隨時間的變化 —— 一個上升的數字通常表示客戶做出決策的時間更長，這是在規劃追蹤電郵或再行銷時間時的一個有用信號。
- 在你再次切換模型之前，導出你正在報告的模型和時間段的CSV文件，因為導出的內容反映的是你點擊 **導出CSV** 按鈕時所選的模型。