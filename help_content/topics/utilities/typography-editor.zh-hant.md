---
title: 字型編輯器
---

字型編輯器是一個共用的樣式工具，讓您可以完全控制文字的外觀。當您在 Page Builder、Header/Footer Builder 或 Menu Builder 的任何元素上編輯字型屬性時，它會以浮動面板的形式開啟。

![字型編輯器](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## 實時預覽

編輯器在面板頂部顯示側邊對比比較：

| Box | Purpose |
|-----|---------|
| **Current** | 顯示 "The quick brown fox..." 的現有字型樣式 |
| **New** | 當您調整設定時即時更新，顯示套用前的結果 |

這讓您可以在套用任何更改之前比較更改前後的差異。

## 字型選項卡

字型選項卡是編輯器開啟時的預設視圖。

**字型家族** — 可搜尋的下拉選單，包含 70 多種按類別組織的字型。每個字型都會以自己的字型預覽，讓您在選擇前看到實際效果。當需要時，字型會從 Google Fonts 動態載入。

**字型大小** — 支援 px、em、rem 和 % 的數值輸入，預設為 16px。

**字型粗細** — 從 100（細）到 900（黑）的滑動條：

| Value | Name |
|-------|------|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

並非所有字型都支援這九種粗細。編輯器會顯示所選字型家族支援的粗細。

**字型樣式** — 切換按鈕，用於 Normal、Italic 和 Oblique。

## 間距選項卡

精準調整字元之間及周圍的間距：

| Control | What It Does | Default |
|---------|-------------|---------|
| **行高** | 文字行之間的垂直間距 | normal |
| **字距** | 單個字元之間的水平間距 | normal |
| **字間距** | 字之間的水平間距 | normal |
| **文字縮進** | 段落第一行的縮進 | 0 |

每個間距控制都包含單位選擇器（px、em、rem、%）。

## 樣式選項卡

控制文字裝飾和視覺效果：

- **文字裝飾** — 無、底線、頂線或刪除線
- **裝飾樣式** — 實線、虛線、點線、雙線或波浪線（當啟用裝飾時應用）
- **裝飾顏色** — 裝飾線的顏色選擇器，預設為文字顏色
- **文字陰影** — 可選的陰影效果，包含偏移、模糊和顏色控制

## 變換選項卡

在不編輯內容的情況下更改文字的大小寫：

| Option | Result |
|--------|--------|
| **None** | 文字以原樣顯示 |
| **全大寫** | ALL LETTERS ARE CAPITALIZED |
| **全小寫** | all letters are lowercase |
| **首字母大寫** | Each Word's First Letter Is Capitalized |

此選項卡的其他控制包括 **文字對齊**（左對齊、居中、右對齊、兩端對齊）、**垂直對齊** 和 **文字方向**（LTR 或 RTL）。

## 可用字型家族

編輯器包含一個經過精心挑選的系統字型和 Google Fonts 圖書館，按類別分組：

| 分類 | 字型
|----------|-------|
| **系統** | 系統預設, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS
| **無襯線 (現代)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans
| **無襯線 (經典)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend
| **有襯線** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya
| **有襯線 (系統)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria
| **等寬字型** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono
| **顯示字型** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black |

Google Fonts 在選擇後會自動載入。系統字型會使用正確的 CSS 備用字型鏈，以確保在不同平台上可靠地渲染。

## 出現位置

字型編輯器在需要文字樣式的地方都可以使用：

- **頁面構建器** — 選中任何元素，打開樣式選項卡，點擊字型部分
- **首頁/頁尾構建器** — 為導覽連結、標誌文字、選單項目和頁尾內容設定文字樣式
- **選單構建器** — 控制選單標籤和子選單項的字型
- **目錄管理員** — 在產品描述和內容編輯器中使用，當字型控制功能可用時

無論上下文如何，編輯器始終通過相同的介面進行訪問。

## 小技巧

- **有意識地搭配字型** — 對於標題使用顯示或有襯線字型，對於正文使用乾淨的無襯線字型。經典組合如 Playfair Display + Inter 或 Montserrat + Merriweather 效果很好。
- **限制每頁的字型家族數量** — 每頁使用兩到三個字型家族通常就足夠了。超過這個數量可能會導致加載時間變慢並造成視覺混亂。
- **使用相對單位進行響應式文字** — em 和 rem 會根據基本字型大小進行縮放，使您的字型自動適應不同的螢幕尺寸。
- **檢查字重的可用性** — 如果文字在 400 和 500 之間看起來一樣，則所選字型可能不支援該字重。編輯器會顯示每個字型提供的字重。
- **在所有設備上預覽** — 在桌面尺寸上看起來不錯的文字可能在行動設備上太小或太大。使用頁面構建器的設備預覽功能進行確認。
- **使用即時預覽** — 在套用之前，始終在預覽框中比較 Current vs New，以避免出現預期之外的更改。