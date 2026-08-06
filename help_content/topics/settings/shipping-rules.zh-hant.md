---
title: 運費規則
---

運費規則根據購物車內容、客戶屬性和配送區域對運費方法進行條件成本調整，自動提供超過$50的免運費，對偏遠地區收取附加費，或對VIP客戶提供運費折扣。規則使用基於優先級的執行（優先級較高者優先），並有可選的停止標誌以防止進一步處理。每個規則評估多個條件（購物車金額、重量、區域、產品、客戶群組）並在所有條件匹配時執行6種調整類型之一。

當您需要動態運費成本，根據訂單上下文變化的時候，請使用運費規則，而不是僅從運費方法中獲取靜態率。

## 運費規則類型

運費規則應用6種類型的成本調整：

### 百分比折扣

**它做了什麼**：將運費成本減少百分比（例如，25% 折扣）。

**公式**：`new_cost = base_cost × (1 - percent/100)`

**範例**：
```
基本費用：$20
折扣：25%
結果：$15
```

**使用案例**：
- VIP客戶折扣（所有運費20%折扣）
- 節日促銷（12月運費15%折扣）
- 大宗訂單折扣（5件以上運費10%折扣）

---

### 固定折扣

**它做了什麼**：從運費成本中減去固定金額。

**公式**：`new_cost = base_cost - amount`（最低$0）

**範例**：
```
基本費用：$15
折扣：$5
結果：$10
```

**使用案例**：
- 首次客戶獎勵（首次訂單運費$5折扣）
- 新letter註冊獎勵（運費$3折扣）
- 忠誠計劃福利（每月運費$10折扣）

---

### 設定費用

**它做了什麼**：將運費費用設置為特定金額。

**公式**：`new_cost = fixed_amount`

**範例**：
```
基本費用：$25
設為：$9.99
結果：$9.99
```

**使用案例**：
- 閃購（今天所有訂單flat $5運費）
- 類別特定運費（書籍始終$3.99運費）
- 時間基礎促銷（本周運費上限$9.99）

---

### 免運費

**它做了什麼**：將運費費用設置為$0。

**公式**：`new_cost = $0`

**範例**:
```
基本費用: $18
規則套用
結果: $0
```

**使用場景**:
- 超過 $50 的免運費
- 特定商品的免運費（促銷商品）
- VIP 客戶的免運費
- 購買 3 件以上的免運費


### 加價（固定金額）

**功能**: 將固定金額加到運費上。

**公式**: `new_cost = base_cost + amount`

**範例**:
```
基本費用: $12
加價: $5
結果: $17
```

**使用場景**:
- 遠距離送貨費
- 超尺寸物品處理費
- 週六送貨加價
- 易碎物品包裝費


### 加價（百分比）

**功能**: 以百分比增加運費。

**公式**: `new_cost = base_cost × (1 + percent/100)`

**範例**:
```
基本費用: $20
加價: 15%
結果: $23
```

**使用場景**:
- 高峰季加價（節日期間 20%）
- 快速送貨附加費（50% 加價）
- 燃料加價（根據當前費用變動）


## 規則條件

規則評估 **所有條件都必須通過** 才能套用：

### 時間有效性

- **開始日期**: 規則在此日期後才生效
- **結束日期**: 規則在此日期前才生效
- **使用場景**: 節日促銷、限時優惠

**範例**: 黑 friday 周末免運費
```
開始: 2026-11-27 00:00
結束: 2026-11-30 23:59
```


### 購物車金額範圍

- **最低購物車金額**: 購物車小計必須 ≥ 金額
- **最高購物車金額**: 購物車小計必須 ≤ 金額
- **使用場景**: 免運費門檻、等級折扣

**範例**: $50-$200 的訂單免運費
```
最低: $50
最高: $200
```


### 購物車重量範圍

- **最低重量**: 購物車總重量必須 ≥ 金額
- **最高重量**: 購物車總重量必須 ≤ 金額
- **使用場景**: 輕量運費折扣、重物加價

**範例**: 超過 20kg 的訂單加收 $5
```
最低重量: 20kg
最高重量: null（無限）
```


### 商品數量範圍

- **Min Item Count**: 購物車必須有 ≥ 數量的商品
- **Max Item Count**: 購物車必須有 ≤ 數量的商品
- **Use Case**: 大宗訂單折扣，單一商品手續費

**Example**: 5件以上商品免運費
```
Min Items: 5
Max Items: null
```


### 運送區域

- **Zones**: 僅在客戶地址符合至少一個選定區域時適用
- **未選擇任何選項**: 該規則適用於所有區域
- **Use Case**: 區域特定附加費或折扣

**Example**: 僅適用於國內區域的免運費
```
Zones: ["Domestic USA"]
```


### 運送方式

- **Methods**: 該規則僅適用於特定運送方式
- **未選擇任何選項**: 該規則適用於所有方式
- **Use Case**: 方式特定促銷

**Example**: 快速運送8折優惠
```
Methods: ["Express Delivery"]
```


### 商品要求

**Requires Products**: 購物車必須包含這些商品中的一個或更多

**Requires Categories**: 購物車必須包含這些類別中的一個或更多商品

**Use Case**: 商品特定免運費，促銷套裝

**Example**: 購物車包含"Promotion Item A"時免運費
```
Requires Products: [Product ID 123]
```


### 商品排除

**Excludes Products**: 若購物車包含這些商品中的任何一個，則規則不適用

**Excludes Categories**: 若購物車包含這些類別中的任何商品，則規則不適用

**Use Case**: 排除重型/大型物品的免運費

**Example**: 免運費不適用於家具類別
```
Excludes Categories: [Furniture]
```


### 客戶群組

- **Customer Groups**: 該規則僅適用於所選群組中的客戶（VIP、批發等）
- **未選擇任何選項**: 該規則適用於所有客戶群組
- **Use Case**: VIP福利，批發折扣

**Example**: VIP成員享15%運費折扣
```
Customer Groups: ["VIP"]
```


### 新會員註冊
Preserve all markdown formatting, image paths, code blocks, and technical terms.

- **First Time Customer**: Toggle to restrict rule to customers with no previous orders
- **Use Case**: New customer welcome offers

**Example**: $5 off shipping for first order
```
First Time Customer: Yes
```


## Rule Priority & Execution

Rules execute in **priority order** (higher number = earlier execution):

### Priority Mechanics

**Example Execution**:
```
Rule A (Priority 100): Free shipping if cart > $50
Rule B (Priority 50): 10% discount on all shipping
Rule C (Priority 1): $2 surcharge for remote zones

Cart: $60, Remote zone
Base shipping cost: $15

Step 1: Rule A evaluates (Priority 100)
  Cart > $50? YES
  Apply: Set cost to $0
  Cost now: $0

Step 2: Rule B evaluates (Priority 50)
  Apply 10% discount to $0
  Cost now: $0 (still free)

Step 3: Rule C evaluates (Priority 1)
  Add $2 surcharge to $0
  Cost now: $2

Final cost: $2
```

**Stop Further Rules Flag**:

If Rule A has `stop_further_rules = True`:
```
Rule A (Priority 100, stop_further_rules=True): Free shipping if cart > $50
Rule B (Priority 50): 10% discount
Rule C (Priority 1): $2 surcharge

Cart: $60
Base: $15

Step 1: Rule A applies, sets cost to $0
        stop_further_rules = True → STOP

Final cost: $0 (Rules B and C never execute)
```


## Creating Shipping Rules

**Step-by-Step Workflow**:

1. **Navigate to Rules**
   - Settings > Shipping > Shipping Rules
   - Click "Add Shipping Rule"

2. **Basic Configuration**
   - **Name**: Internal identifier (e.g., "Free Shipping Over $50")
   - **Description**: Optional notes (not shown to customers)
   - **Active**: Toggle to enable/disable
   - **Priority**: Set execution order (100 for high priority, 1 for low)

3. **Choose Rule Type**
   - Select adjustment type (discount %, discount fixed, set cost, free, surcharge %, surcharge fixed)
   - Enter amount or percentage

4. **設置停止標誌**（可選）
  - 勾選「停止後續規則」以防止此規則阻止低優先級規則的執行
  - 用於最終/絕對規則（例如，免運費不應在之後添加附加費）

5. **定義條件**（可選 - 留空表示「始終套用」）
  - 時間有效性：開始/結束日期
  - 購物車金額：最低/最高
  - 購物車重量：最低/最高
  - 商品數量：最低/最高
  - 區域：選擇適用的區域
  - 方式：選擇適用的方式
  - 商品：必要或排除的商品
  - 客戶：群組或僅限新客戶

6. **儲存規則**
  - 點擊儲存
  - 規則立即生效（如果啟用切換為是）


## 常見運費規則場景

### 場景 1: 超過 $50 免運費

**目標**: 當購物車小計 ≥ $50 時提供免運費。

**設定**:
```
名稱: 超過 $50 免運費
類型: 免運費
優先順序: 100
條件:
  最低購物車金額: $50
停止後續規則: 是
```


### 場景 2: 遠距地區附加費

**目標**: 對遠距地區的配送收取 $10 附加費。

**設定**:
```
名稱: 遠距地區附加費
類型: 附加費（固定金額）
金額: $10
優先順序: 50
條件:
  區域: ["遠距地區"]
停止後續規則: 否
```


### 場景 3: VIP 客戶 20% 折扣

**目標**: VIP 客戶所有運費打 8 折。

**設定**:
```
名稱: VIP 運費折扣
類型: 折扣（百分比）
百分比: 20
優先順序: 75
條件:
  客戶群組: ["VIP"]
停止後續規則: 否
```


### 場景 4: 節日固定費用

**目標**: 十二月所有運費上限為 $9.99。

**設定**:
```
名稱: 十二月固定費用促銷
類型: 設定費用
金額: $9.99
優先順序: 100
條件:
  開始日期: 2026-12-01
  結束日期: 2026-12-31
停止後續規則: 是
```


### 場景 5: 重型商品附加費

**目標**: 對超過 25kg 的訂單收取 $15 費用

**設定**:
```
名稱: 大額訂單附加費
類型: 附加費 (固定金額)
金額: $15
優先順序: 50
條件:
  最小重量: 25kg
停止後續規則: 否
```


### 範例 6: 首次訂單免運費

**目標**: 新客戶首次訂單免運費。

**設定**:
```
名稱: 首次訂單免運費
類型: 免運費
優先順序: 100
條件:
  首次購買客戶: 是
停止後續規則: 是
`


### 範例 7: 針對特定類別的免運費

**目標**: 包含促銷類別商品的訂單免運費。

**設定**:
```
名稱: 促銷類別免運費
類型: 免運費
優先順序: 90
條件:
  需要類別: ["Promotions"]
停止後續規則: 是
```


### 範例 8: 免運費不適用家具

**目標**: 免運費超過 $50，但購物車中不含家具。

**解決方案**: 兩條規則

**規則 1**:
```
名稱: 一般免運費
類型: 免運費
優先順序: 50
條件:
  最低購物金額: $50
  排除類別: ["Furniture"]
停止後續規則: 否
```

**規則 2**:
```
名稱: 家具訂單 $5 折扣
類型: 折扣 (固定金額)
金額: $5
優先順序: 40
條件:
  需要類別: ["Furniture"]
  最低購物金額: $50
停止後續規則: 否
```


## 规则组合策略

### 策略 1: 折扣叠加

**允许多個折扣叠加**:
```
規則 A (優先順序 100): VIP 享 10% 折扣 → stop_further_rules=No
規則 B (優先順序 50): 購買金額超過 $100 享 15% 折扣 → stop_further_rules=No

VIP 客戶訂單 $120:
基底: $15
套用規則 A 後: $13.50 (10% 折扣)
套用規則 B 後: $11.48 (15% 折扣 $13.50)
```

### 策略 2: 獨占規則

**只有一條規則適用** (優先順序最高):
```
規則 A (優先順序 100): 購買金額超過 $50 免運費 → stop_further_rules=Yes
規則 B (優先順序 50): 所有運費享 20% 折扣 → stop_further_rules=Yes

購物車金額超過 $50:
規則 A 執行 → 免運費 → 停止
規則 B 不會執行
```

### 策略 3: 條件附加費

保留所有 markdown 格式，圖片路徑，程式碼區塊，以及技術術語。

**Discounts first, surcharges last**:
```
Rule A (Priority 100): Free shipping >$75
Rule B (Priority 75): 15% VIP discount
Rule C (Priority 50): 10% general discount
Rule D (Priority 25): $5 remote area surcharge
Rule E (Priority 1): 10% fuel surcharge

Order: $80, Remote zone, VIP customer
Base: $20
A: $80 > $75 → Free ($0)
B: VIP → 15% off $0 = $0
C: 10% off $0 = $0
D: Remote +$5 = $5
E: Fuel +10% of $5 = $5.50

Final: $5.50 (not free due to surcharges)
```

**To prevent this, use stop_further_rules=Yes**:
```
Rule A (Priority 100, stop=Yes): Free shipping >$75

Same order:
A: $80 > $75 → Free ($0) → STOP
Final: $0 (truly free)
```

---

## Testing Shipping Rules

**Before going live**:

1. **Create Test Carts**
   - Cart A: $25 (below threshold)
   - Cart B: $55 (above threshold)
   - Cart C: $200 + Remote zone
   - Cart D: VIP customer

2. **Test Each Rule**
   - Proceed to checkout
   - Verify correct shipping cost displayed
   - Check rule execution order

3. **Test Priority Resolution**
   - Multiple matching rules
   - Verify highest priority executes first
   - Check stop_further_rules behavior

4. **Test Edge Cases**
   - Cart value exactly at threshold
   - Multiple conditions matching
   - Conflicting rules

---

## Troubleshooting

**Issue 1: Rule not applying**

**Causes**:
- Rule is inactive
- One or more conditions not met
- Higher priority rule set stop_further_rules=Yes
- Time validity outside current date

**Solution**: Review all conditions, check priority, verify active status.

---

**Issue 2: Unexpected discount amount**

**Causes**:
- Multiple rules stacking
- Percentage applied to already-discounted cost
- Rule priority incorrect

**Solution**: Check priority order, review stop_further_rules flags, trace execution manually.

---

**Issue 3: Free shipping not working**

**Causes**:
- Lower priority surcharge rule adding cost after free shipping rule
- Cart doesn't meet min value threshold
- Excluded products in cart

**解決方案**: 在免運費規則中使用 stop_further_rules=Yes，驗證條件，檢查排除項目。


## 小技巧

- **為免運費設置高優先級** - 優先級 100 確保它在其他調整之前執行
- **為絕對規則設置 stop_further_rules** - 免運費應停止進一步處理
- **測試規則組合** - 多個規則可能會意外地相互影響
- **使用描述性名稱** - 「VIP 20% 折扣（優先級 75）」比「規則 3」更好
- **記錄複雜邏輯** - 在描述欄位中添加備註
- **從簡單規則開始** - 漸進式增加複雜度
- **監控規則性能** - 檢查規則是否被使用或造成混淆
- **避免過多規則** - 太多規則會減慢結帳程序，最多使用 5-10 個
- **使用區域進行地理設置** - 比為每個國家設置多個類似規則更優
- **與支付方式結合使用** - 規則 + 支付方式一起使用可實現複雜定價
- **設置明確的時間窗口** - 當然在促銷中包含結束日期
- **測試邊界情況** - 恰好 50 美元，恰好 5 個物品等