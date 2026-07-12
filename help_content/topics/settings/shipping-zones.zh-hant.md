---
title: 運送區域
---

運送區域用於定義地理區域以進行針對性的運送費用設定—將國家、州或郵遞編碼分組為區域，然後將運送方式連結到特定區域以實現精確的費用控制。當地址符合多個區域時，區域會根據優先順序進行匹配（優先順序最高的區域獲勝）。此系統可實現複雜的定價策略：對偏遠地區收取更高費用、在國內提供免運費，或為特定區域提供折扣價格。

當您在不同地理區域需要不同的運送費用時，請使用區域，從簡單的國內與國際分區到複雜的多區域階梯定價皆可使用。

## 理解運送區域

**區域是什麼**：根據國家、州/省和郵遞編碼模式定義的命名地理區域。

**區域如何運作**：
1. 顧客在結帳時輸入運送地址
2. 系統評估所有活動中的區域
3. 符合顧客地址的區域成為候選
4. 如果多個區域符合，優先順序最高的區域獲勝
5. 顯示與獲勝區域連結的運送方式
6. 顯示未連結到任何區域（或連結到符合區域）的運送方式

**區域組成部分**：
- **名稱**：區域識別碼（例如："Domestic"、"EU"、"Remote Areas"）
- **國家**：包含的國家代碼清單（空白 = 所有國家）
- **州/省**：每個國家的州限制（可選）
- **郵遞編碼模式**：用於 ZIP/郵遞編碼匹配的正則表達式模式（可選）
- **優先順序**：數字越高，當多個區域符合時優先順序越高

---

## 區域匹配邏輯

區域使用 **漸進縮小** 的方式來匹配地址：

### 第1層：國家匹配

**國家清單為空** → 區域匹配所有國家

**提供國家清單** → 地址國家必須在清單中

範例：
```
區域："Domestic"
國家：["US"]
→ 匹配：任何美國地址
→ 不匹配：加拿大、英國等
```

### 第2層：州/省匹配

**未定義州** → 區域匹配允許國家中的所有州

**States defined for specific countries** → Address state must match

Example:
```
Zone: "West Coast"
Countries: ["US"]
States: {"US": ["CA", "OR", "WA"]}
→ Matches: California, Oregon, Washington addresses
→ No match: New York, Texas, etc.
```

### Level 3: Postal Code Matching

**No patterns defined** → Zone matches ALL postal codes in allowed country/states

**Patterns defined** → Address postal code must match at least one pattern

Example:
```
Zone: "Los Angeles Metro"
Countries: ["US"]
States: {"US": ["CA"]}
Postal Patterns: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Matches: 90001, 91210, 90245
→ No match: 94102 (San Francisco)
```

**Regex Pattern Examples**:
- `^90[0-9]{3}$` - Los Angeles area (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Canadian postal code format (K1A 0B1)
- `^SW[0-9]{1,2}` - London UK postcodes starting with SW

---

## Priority-Based Zone Selection

When multiple zones match an address, **priority** determines which zone applies:

**How Priority Works**:
- Higher number = higher priority
- If address matches zones with priority 100 and 50, priority 100 wins
- Only winning zone's shipping methods are available

**Use Cases**:

**Scenario 1: Specific Overrides General**
```
Zone A: "Remote Alaska"
  Countries: ["US"]
  States: {"US": ["AK"]}
  Priority: 100

Zone B: "Domestic USA"
  Countries: ["US"]
  Priority: 50

Address: Anchorage, AK
→ Matches both zones
→ Priority 100 wins
→ "Remote Alaska" zone applies (higher shipping cost)
```

**Scenario 2: Postal Code Overrides State**
```
Zone A: "Manhattan Premium"
  Countries: ["US"]
  States: {"US": ["NY"]}
  Postal Patterns: ["^100[0-2][0-9]$"]
  Priority: 100

Zone B: "New York State"
  Countries: ["US"]
  States: {"US": ["NY"]}
  Priority: 50

Address: New York, NY 10001
→ Matches both zones
→ Priority 100 wins
→ "Manhattan Premium" applies (premium delivery service)
```

---

## Creating Shipping Zones

**Step-by-Step Workflow**:

- 點擊 **設定 > 運送 > 運送區域**

- 點擊 **新增運送區域**

- **名稱**：描述性標識（例如："歐盟"、"西岸"、"偏遠地區"）

- **優先順序**：設定相對重要性（100 為特定區域，50 為一般區域，1 為預設區域）

- **啟用**：切換以啟用或停用

**選項 A：所有國家**（不選擇任何國家）

- 該區域適用於全球所有地址

- 適用於預設/備用區域

**選項 B：特定國家**

- 點擊 **新增國家**

- 從下拉選單中選擇國家（如：US、CA、UK 等）

- 對所有包含的國家重複此操作

**選項 C：特定州/省份**

- 在新增國家後，為每個國家點擊 **新增州**

- 從下拉選單中選擇州

- 範例：US → CA、OR、WA（西岸）

**選項 D：郵遞區號模式**（高階）

- 輸入正則表達式模式（每行一個）

- 使用範例郵遞區號測試模式

- 點擊 **驗證模式** 以檢查語法

- 在編輯運送方式時可以連結（不在區域設定中）

- 或將區域連結到現有運送方式：**編輯運送方式 → 運送區域 → 選擇區域**

- 當多個區域匹配時，優先順序較高的區域會覆蓋優先順序較低的區域

- 建議：特定區域（100）、區域性區域（50）、預設區域（1）

- 將 **啟用** 設為 **是**

- 儲存

### 設定 2：多區域國際

**目標**：歐盟、北美、亞洲、世界其他地區的不同運費率。

```
Zone 1: "European Union"
  Countries: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Priority: 100

Zone 2: "North America"
  Countries: [US, CA, MX]
  Priority: 100

Zone 3: "Asia Pacific"
  Countries: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Priority: 100

Zone 4: "Rest of World"
  Countries: [Leave empty]
  Priority: 1
```

**運送方式**：
- "EU Shipping" → 歐盟區域
- "North America Shipping" → 北美區域
- "Asia Pacific Shipping" → 亞太區域
- "International Standard" → 世界其他地區區域

---

### 設置 3：遠離地區附加費用

**目標**：在國內區域中對遠離的郵政編碼增加附加費用。

```
Zone 1: "Remote Domestic"
  Countries: [US]
  Postal Patterns: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Priority: 100

Zone 2: "Standard Domestic"
  Countries: [US]
  Priority: 50
```

**運送方式**：
- "Remote Shipping" → 遠離國內區域（費用較高）
- "Standard Shipping" → 標準國內區域

---

### 設置 4：州特定區域

**目標**：針對美國各個地區設定不同的費用。

```
Zone 1: "West Coast"
  Countries: [US]
  States: {"US": ["CA", "OR", "WA"]}
  Priority: 100

Zone 2: "East Coast"
  Countries: [US]
  States: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Priority: 100

Zone 3: "Midwest"
  Countries: [US]
  States: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Priority: 100

Zone 4: "South"
  Countries: [US]
  States: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Priority: 100

Zone 5: "Other US States"
  Countries: [US]
  Priority: 50
```

---

## 郵政編碼模式範例

郵政編碼使用 **regex**（正則表達式）進行模式匹配：

### 美國（ZIP 編碼）

**格式**：5 個數字（例如：90210）

```
California (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### 加拿大 (郵遞區號)

**格式**: A1A 1A1 (字母-數字-字母 空格 數字-字母-數字)

```
所有加拿大郵遞區號:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$
安大略省 (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$
魁北克省 (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$
```

### 英國 (郵編)

**格式**: AA1A 1AA 或 A1A 1AA

```
倫敦 (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}
曼徹斯特 (M):                        ^M[0-9]{1,2}
伯明翰 (B):                        ^B[0-9]{1,2}
```

### 澳大利亞 (郵編)

**格式**: 4 位數字 (例如，2000)

```
新南威爾斯州 (1000-2999):  ^[12][0-9]{3}$
維多利亞州 (3000-3999, 8000-8999):  ^[38][0-9]{3}$
昆士蘭州 (4000-4999, 9000-9999):  ^[49][0-9]{3}$
```

### 模式測試

**在儲存模式之前**，請使用已知的郵遞區號進行測試：

1. 輸入模式: `^90[0-9]{3}$`
2. 測試輸入: "90210" → 應該匹配
3. 測試輸入: "10001" → 應該不匹配
4. 測試輸入: "9021" → 應該不匹配 (只有 4 位數字)

使用線上正則表達式測試工具 (regex101.com) 來驗證複雜模式。

---

## 區域覆蓋總覽

區域在管理員清單視圖中顯示 **覆蓋總覽**，顯示包含內容：

**範例**：
- "所有國家" → 無國家限制
- "US, CA, MX" → 3 個國家
- "US (CA, OR, WA)" → 美國包含 3 個州
- "US (90xxx-91xxx)" → 美國包含郵遞區號模式

**使用總覽來**：
- 快速驗證區域覆蓋，無需打開
- 發現覆蓋重疊或缺口
- 一目了然地審計區域配置

---

## 將區域連結到運輸方式

區域和方式具有 **多對多關係**：

**從方式端** (建議)：
1. 編輯運輸方式
2. 滾動到 "運輸區域" 區段
3. 選擇適用的區域 (多選)
4. 儲存方式


- Zones don't directly link to methods
- Linking is always done from method configuration

```
Method: "Domestic Standard"
Linked Zones: ["Domestic USA"]
→ Only shown to US addresses

Method: "International Express"
Linked Zones: ["EU", "Asia Pacific", "Rest of World"]
→ Shown to all non-US addresses
```

- Use addresses in different zones
- Verify correct zone matches

- Use address that matches multiple zones
- Verify highest priority zone wins
- Confirm expected shipping methods appear

- Border postal codes (e.g., 90999 vs 91000)
- State boundaries
- International addresses with similar postal codes

- Enter test address
- See which zone(s) match
- View priority resolution

- Lower priority zone selected despite higher priority zone matching
- Postal code pattern syntax error (pattern fails silently)
- State code mismatch (CA vs California)

- Verify priority values (higher number = higher priority)
- Test postal code patterns with regex validator
- Use 2-letter state codes (CA, not California)

**原因**:
- 方法未連結任何區域（適用於所有地區）
- 多個區域匹配，意外區域的優先級更高
- 區域覆蓋範圍意外重疊

**解決方案**:
- 檢查方法連結的區域
- 檢查匹配區域的優先級
- 審核區域覆蓋範圍摘要以查找重疊

---

## 小技巧

- **從 2 個區域開始** - 國內和國際，根據需要逐步擴展
- **明智地使用優先級** - 具體區域 100，區域 50，預設 1
- **徹底測試郵政模式** - 正則表達式錯誤會靜默失敗，導致區域無法匹配
- **記錄區域邏輯** - 在區域描述中添加筆記，說明覆蓋意圖
- **避免過多區域** - 過多區域會使配置變得複雜；複雜場景請使用運費促銷
- **使用州代碼而非名稱** - "CA" 而非 "California"，"NY" 而非 "New York"
- **建立預設區域** - 所有國家，優先級 1，確保至少有一個運費選項始終可用
- **監控區域表現** - 如果許多客戶看到 "沒有可用運費"，請審核區域覆蓋範圍
- **更新新區域的區域** - 當新成員加入時，將國家添加到 EU 區域
- **使用描述性名稱** - "EU（不含英國）" 比 "區域 3" 更好
- **使用真實地址進行測試** - 測試時使用客戶實際地址，而非虛構地址