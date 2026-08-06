---
title: Kargo İndirimleri
---

Kargo kuralları, sepet içeriği, müşteri özellikleri ve teslimat bölgelerine göre kargo yöntemlerine koşullu maliyet ayarları uygular. Otomatik olarak 50$ üzerinde ücretsiz kargo sunabilir, uzak bölgelere ek ücret ekleyebilir veya VIP müşterilere kargo indirimi yapabilirsiniz. Kurallar, öncelik tabanlı yürütme (yüksek öncelikli olanlar önce) ile çalışır ve daha fazla işleme engellemek için isteğe bağlı durdurma bayrakları kullanılır. Her kural, birden fazla koşulu (sepet değeri, ağırlığı, bölgeler, ürünler, müşteri grupları) değerlendirir ve tüm koşullar uyuştuğunda 6 ayarlama türünden birini çalıştırır.

Kargo indirimlerini, sadece kargo yöntemlerinden statik oranlar değil, sipariş bağlamına göre dinamik kargo maliyetlerine ihtiyaç duyduğunuzda kullanın.

## Kargo İndirim Türleri

Kargo kuralları, 6 tür maliyet ayarlama uygular:

### Yüzde İndirim

**Ne Yapar**: Kargo maliyetini yüzdelik olarak azaltır (örneğin, %25 indirim).

**Formül**: `yeni_maliyet = temel_maliyet × (1 - yüzde/100)`

**Örnek**:
```
Temel maliyet: $20
İndirim: %25
Sonuç: $15
```

**Kullanım Alanları**:
- VIP müşteri indirimi (tüm kargo için %20 indirim)
- Mevsimsel kampanyalar (Aralık ayında kargo için %15 indirim)
- Toplu sipariş indirimi (5+ ürün için kargo için %10 indirim)

---

### Sabit İndirim

**Ne Yapar**: Kargo maliyetinden sabit bir tutar çıkarır.

**Formül**: `yeni_maliyet = temel_maliyet - tutar` (en az $0)

**Örnek**:
```
Temel maliyet: $15
İndirim: $5
Sonuç: $10
```

**Kullanım Alanları**:
- İlk sipariş müşterisi bonusu (ilk sipariş kargonuzdan $5 indirim)
- Haberleme aboneliği ödüllü (kargonuzdan $3 indirim)
- Loyalite programı faydası (ayda kargonuzdan $10 indirim)

---

### Maliyeti Değiştir

**Ne Yapar**: Kargo maliyetini belirli bir tutara ayarlar.

**Formül**: `yeni_maliyet = sabit_tutar`

**Örnek**:
```
Temel maliyet: $25
Ayarla: $9.99
Sonuç: $9.99
```

**Kullanım Alanları**:
- Anlık indirim (bugün tüm siparişler için $5 kargo)
- Kategori özel kargo (kitaplar her zaman $3.99 kargo)
- Zaman bazlı kampanyalar (bu hafta kargonuz $9.99'ın üstüne kapatılmış)

---

### Ücretsiz Kargo

**Ne Yapar**: Kargo maliyetini $0 yapar.

**Formül**: `yeni_maliyet = $0`

**Örnek**:
```
Temel maliyet: $18
Kural uygulanıyor
Sonuç: $0
```

**Kullanım Alanları**:
- 50$ üzerinde ücretsiz kargo
- Belirli ürünler için ücretsiz kargo (promosyon ürünleri)
- VIP müşterilere ücretsiz kargo
- 3+ ürün içeren siparişler için ücretsiz kargo

---

### Ek Ücret (Sabit)

**Ne Yapar**: Kargo maliyetine sabit bir tutar ekler.

**Formül**: `yeni_maliyet = temel_maliyet + tutar`

**Örnek**:
```
Temel maliyet: $12
Ek Ücret: $5
Sonuç: $17
```

**Kullanım Alanları**:
- Uzak bölgelere teslimat ücreti
- Aşırı boyutlu ürün işleme ücreti
- Cumartesi teslimatı ek ücreti
- Kırılgan ürün ambalaj ücreti

---

### Ek Ücret (Yüzde)

**Ne Yapar**: Kargo maliyetini yüzdelik olarak artırır.

**Formül**: `yeni_maliyet = temel_maliyet × (1 + yüzde/100)`

**Örnek**:
```
Temel maliyet: $20
Ek Ücret: %15
Sonuç: $23
```

**Kullanım Alanları**:
- Zirve sezonu ek ücreti (tatil zamanında %20)
- Hızlı teslimat ek ücreti (%50)
- Yakıt ek ücreti (mevcut oranlara göre değişken)

---

## Kampanya Koşulları

Kampanyalar, kuralın uygulanabilmesi için **tüm koşulların geçmesi** gerekir:

### Zaman Geçerlilikleri

- **Başlangıç Tarihi**: Kural bu tarihten sonra aktif olur
- **Bitiş Tarihi**: Kural bu tarihten önce aktif olur
- **Kullanım Alanı**: Mevsimsel kampanyalar, sınırlı süreli teklifler

**Örnek**: Sadece Black Friday haftasonu ücretsiz kargo
```
Başlangıç: 2026-11-27 00:00
Bitiş: 2026-11-30 23:59
```

---

### Sepet Değeri Aralığı

- **Min Sepet Değeri**: Sepet alt toplamı ≥ tutar olmalıdır
- **Max Sepet Değeri**: Sepet alt toplamı ≤ tutar olmalıdır
- **Kullanım Alanı**: Ücretsiz kargo eşikleri, katmanlı indirimler

**Örnek**: 50$-200$ arası siparişler için ücretsiz kargo
```
Min: $50
Max: $200
```

---

### Sepet Ağırlığı Aralığı

- **Min Ağırlık**: Toplam sepet ağırlığı ≥ tutar olmalıdır
- **Max Ağırlık**: Toplam sepet ağırlığı ≤ tutar olmalıdır
- **Kullanım Alanı**: Hafif sevkiyat indirimleri, ağır ürün ek ücretleri

**Örnek**: 20kg üzerindeki siparişler için $5 ek ücret
```
Min Ağırlık: 20kg
Max Ağırlık: null (sınırsız)
```

---

### Ürün Sayısı Aralığı


- **Min Item Count**: Sepet en az öğe miktarına sahip olmalıdır
- **Max Item Count**: Sepet en fazla öğe miktarına sahip olmalıdır
- **Use Case**: Toplu sipariş indirimleri, tek öğe ücretleri

**Örnek**: 5+ öğe için ücretsiz kargo
```
Min Items: 5
Max Items: null
```

---

### Kargo Bölgesi

- **Zones**: Kural yalnızca müşteri adresi en az bir seçilen bölgeyle eşleşiyorsa uygulanır
- **Empty selection**: Kural tüm bölgelere uygulanır
- **Use Case**: Bölgesel ek ücretler veya indirimler

**Örnek**: Yalnızca Ulusal bölge için ücretsiz kargo
```
Zones: ["Domestic USA"]
```

---

### Kargo Yöntemi

- **Methods**: Kural yalnızca belirli kargo yöntemlerine uygulanır
- **Empty selection**: Kural tüm yöntemlere uygulanır
- **Use Case**: Yöntem özel teklifler

**Örnek**: Express Kargo için %25 indirim
```
Methods: ["Express Delivery"]
```

---

### Ürün Gereksinimleri

**Requires Products**: Sepet bu ürünlerden en az birini içermelidir

**Requires Categories**: Sepet bu kategorilerden en az bir ürün içermelidir

**Use Case**: Ürün özel ücretsiz kargo, promosyon paketleri

**Örnek**: Sepette "Promotion Item A" varsa ücretsiz kargo
```
Requires Products: [Product ID 123]
```

---

### Ürün Hariç Tutma

**Excludes Products**: Kural, sepet bu ürünlerden herhangi birini içeriyorsa uygulanmaz

**Excludes Categories**: Kural, sepet bu kategorilerden herhangi bir ürünü içeriyorsa uygulanmaz

**Use Case**: Ağır/çok büyük ürünlerin ücretsiz kargodan hariç tutulması

**Örnek**: Mobilya kategorisi hariç ücretsiz kargo
```
Excludes Categories: [Furniture]
```

---

### Müşteri Grubu

- **Customer Groups**: Kural yalnızca seçilen gruplardaki müşterilere uygulanır (VIP, Wholesale vb.)
- **Empty selection**: Kural tüm müşteri gruplarına uygulanır
- **Use Case**: VIP avantajları, toptan indirimler

**Örnek**: VIP üyeleri için %15 kargo indirimi
```
Customer Groups: ["VIP"]
```

---

### İlk Zamanlı Müşteri

- **First Time Customer**: Kuralın yalnızca önceki siparişi olmayan müşterilere uygulanmasını sağlar
- **Use Case**: Yeni müşteri hoş geldiniz teklifleri

**Örnek**: İlk sipariş için $5 kargo indirimi
```
First Time Customer: Yes
```

---

## Promosyon Önceliği & Uygulama

Promosyonlar **öncelik sırasına** göre uygulanır (daha yüksek sayı = daha erken uygulama):

### Öncelik Mekanikleri

**Uygulama Örneği**:
```
Promotion A (Priority 100): Sepet $50'den fazla ise ücretsiz kargo
Promotion B (Priority 50): Tüm kargo için %10 indirim
Promotion C (Priority 1): Uzak bölgelere $2 ek ücret

Cart: $60, Uzak bölge
Base shipping cost: $15

Step 1: Promotion A evaluates (Priority 100)
  Cart > $50? YES
  Apply: Set cost to $0
  Cost now: $0

Step 2: Promotion B evaluates (Priority 50)
  Apply 10% discount to $0
  Cost now: $0 (still free)

Step 3: Promotion C evaluates (Priority 1)
  Add $2 surcharge to $0
  Cost now: $2

Final cost: $2
```

**Daha Fazla Promosyonları Durdur Flag**:

Eğer Promotion A'nın `stop_further_promotions = True`:
```
Promotion A (Priority 100, stop_further_promotions=True): Sepet $50'den fazla ise ücretsiz kargo
Promotion B (Priority 50): %10 indirim
Promotion C (Priority 1): Uzak bölgelere $2 ek ücret

Cart: $60
Base: $15

Step 1: Promotion A applies, sets cost to $0
        stop_further_promotions = True → STOP

Final cost: $0 (Rules B and C never execute)
```

---

## Kargo Promosyonları Oluşturma

**Adım Adım İş Akışı**:

1. **Kurallara Git**
   - Ayarlar > Kargo > Kargo Promosyonları
   - "Kargo Promosyonu Ekle"ye tıklayın

2. **Temel Yapılandırma**
   - **Name**: İçerik tanımlayıcısı (örneğin, "$50 Üzeri Ücretsiz Kargo")
   - **Description**: Opsiyonel notlar (müşterilere gösterilmez)
   - **Active**: Etkin/etkisiz yapmak için anahtar
   - **Priority**: Uygulama sırasını belirleyin (100 yüksek öncelik için, 1 düşük öncelik için)

3. **Promosyon Türünü Seçin**
   - Ayarlama türünü seçin (indirim %, indirim sabit, maliyet ayarla, ücretsiz, ek ücret %, ek ücret sabit)
   - Miktar veya yüzdesini girin


4. **Durdur Flag'ı Ayarla** (Opsiyonel)
   - Bu kuralın düşük öncelikli promosyonların çalışmasını engellemesi gerekiyorsa, "Daha Fazla Promosyonları Durdur" seçeneğini işaretleyin
   - Son/kesin kural için kullanın (örneğin, ücretsiz kargo üzerine ek ücretler eklenmemeli)

5. **Şartları Tanımlayın** (Opsiyonel - boş bırakın "her zaman uygula")
   - Zaman geçerliliği: Başlangıç/son tarihleri
   - Sepet değeri: Min/max
   - Sepet ağırlığı: Min/max
   - Ürün sayısı: Min/max
   - Bölgeler: Uygulanabilir bölgeleri seçin
   - Yöntemler: Uygulanabilir yöntemleri seçin
   - Ürünler: Gerekli veya hariç tut
   - Müşteri: Gruplar veya sadece ilk sipariş için

6. **Kuralları Kaydet**
   - Kaydet'e tıklayın
   - Kural hemen aktif hale gelir (eğer aktif anahtar Yes ise)

---

## Yaygın Kargo Promosyonu Senaryoları

### Senaryo 1: 50$ Üzeri Ücretsiz Kargo

**Hedef**: Sepet alt toplamı ≥ 50$ olduğunda ücretsiz kargo sunun.

**Ayarlamalar**:
```
Ad: 50$ Üzeri Ücretsiz Kargo
Tip: Ücretsiz Kargo
Öncelik: 100
Şartlar:
  Min Sepet Değeri: 50$
Daha Fazla Promosyonları Durdur: Evet
```

---

### Senaryo 2: Uzak Bölge Ücreti

**Hedef**: Uzak bölgelere teslimat için 10$ ücreti ekle.

**Ayarlamalar**:
```
Ad: Uzak Bölge Ücreti
Tip: Ücret (Sabit)
Miktar: 10$
Öncelik: 50
Şartlar:
  Bölgeler: ["Uzak Bölgeler"]
Daha Fazla Promosyonları Durdur: Hayır
```

---

### Senaryo 3: VIP Müşteri %20 İndirim

**Hedef**: VIP müşterilere tüm kargo için %20 indirim.

**Ayarlamalar**:
```
Ad: VIP Kargo İndirimi
Tip: İndirim (Yüzde)
Yüzde: 20
Öncelik: 75
Şartlar:
  Müşteri Grupları: ["VIP"]
Daha Fazla Promosyonları Durdur: Hayır
```

---

### Senaryo 4: Tatil Dönemi Sabit Ücret

**Hedef**: Aralık ayında tüm kargo ücreti 9,99$'a kadar sınırlı.

**Ayarlamalar**:
```
Ad: Aralık Sabit Ücret Promosyonu
Tip: Ücreti Değiştir
Miktar: 9,99$
Öncelik: 100
Şartlar:
  Başlangıç Tarihi: 2026-12-01
  Bitiş Tarihi: 2026-12-31
Daha Fazla Promosyonları Durdur: Evet
```

---

### Senaryo 5: Ağır Ürün Ücreti

**Hedef**: 25kg'dan fazla siparişler için 15$ ücreti ekle.

**Ayarlamalar**:
```
Ad: Ağır Sipariş Ücreti
Tip: Ücret (Sabit)
Miktar: 15$
Öncelik: 50
Şartlar:
  Min Ağırlık: 25kg
Daha Fazla Promosyonları Durdur: Hayır
```

---

### Senaryo 6: İlk Sipariş Ücretsiz Kargo

**Hedef**: Yeni müşterilere ilk sipariş için ücretsiz kargo.

**Ayarlamalar**:
```
Ad: İlk Sipariş Ücretsiz Kargo
Tip: Ücretsiz Kargo
Öncelik: 100
Şartlar:
  İlk Zamanlı Müşteri: Evet
Daha Fazla Promosyonları Durdur: Evet
```

---

### Senaryo 7: Kategoriye Özel Ücretsiz Kargo

**Hedef**: Promosyon kategori ürünleri içeren siparişler için ücretsiz kargo.

**Ayarlamalar**:
```
Ad: Promosyon Kategorisi Ücretsiz Kargo
Tip: Ücretsiz Kargo
Öncelik: 90
Şartlar:
  Gerekli Kategoriler: ["Promosyonlar"]
Daha Fazla Promosyonları Durdur: Evet
```

---

### Senaryo 8: Mobilya Ücretsiz Kargo Hariç

**Hedef**: 50$ üzeri ücretsiz kargo, ancak sepet mobilya içeriyorsa hariç.

**Çözüm**: İki kural

**Promosyon 1**:
```
Ad: Genel Ücretsiz Kargo
Tip: Ücretsiz Kargo
Öncelik: 50
Şartlar:
  Min Sepet Değeri: 50$
  Hariç Kategoriler: ["Mobilya"]
Daha Fazla Promosyonları Durdur: Hayır
```

**Promosyon 2**:
```
Ad: Mobilya Siparişleri 5$ İndirim
Tip: İndirim (Sabit)
Miktar: 5$
Öncelik: 40
Şartlar:
  Gerekli Kategoriler: ["Mobilya"]
  Min Sepet Değeri: 50$
Daha Fazla Promosyonları Durdur: Hayır
```

---

## Promosyon Kombinasyon Stratejileri

### Strateji 1: İndirimleri Yığma

**Birden fazla indirimin yığılmasını sağlayın**:
```
Promosyon A (Öncelik 100): VIP için %10 indirim → stop_further_promotions=Hayır
Promosyon B (Öncelik 50): 100$ üzeri siparişler için %15 indirim → stop_further_promotions=Hayır

VIP müşteri 120$ siparişi:
Temel: 15$
Promosyon A'dan sonra: 13,50$ (10% indirim)
Promosyon B'den sonra: 11,48$ (13,50$'nın %15 indirimi)
```

### Strateji 2: Özel Kurallar

**Sadece bir kural uygulanır** (en yüksek öncelik):
```
Promosyon A (Öncelik 100): 50$ üzeri ücretsiz kargo → stop_further_promotions=Evet
Promosyon B (Öncelik 50): Tüm kargo için %20 indirim → stop_further_promotions=Evet

50$ üzeri sepet:
Promosyon A uygulanır → Ücretsiz kargo → DUR
Promosyon B asla uygulanmaz
```

### Strateji 3: Koşullu Ücretler


**İndirimler önce, ekstra ücretler sonra**:
```
Promotion A (Priority 100): Free shipping >$75
Promotion B (Priority 75): 15% VIP discount
Promotion C (Priority 50): 10% general discount
Promotion D (Priority 25): $5 remote area surcharge
Promotion E (Priority 1): 10% fuel surcharge

Order: $80, Remote zone, VIP customer
Base: $20
A: $80 > $75 → Free ($0)
B: VIP → 15% off $0 = $0
C: 10% off $0 = $0
D: Remote +$5 = $5
E: Fuel +10% of $5 = $5.50

Final: $5.50 (not free due to surcharges)
```

**Bunu önlemek için stop_further_promotions=Yes kullanın**:
```
Promotion A (Priority 100, stop=Yes): Free shipping >$75

Same order:
A: $80 > $75 → Free ($0) → STOP
Final: $0 (truly free)
```

---

## Testing Shipping Promotions

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
   - Check stop_further_promotions behavior

4. **Test Edge Cases**
   - Cart value exactly at threshold
   - Multiple conditions matching
   - Conflicting rules

---

## Troubleshooting

**Issue 1: Promotion not applying**

**Causes**:
- Rule is inactive
- One or more conditions not met
- Higher priority rule set stop_further_promotions=Yes
- Time validity outside current date

**Solution**: Review all conditions, check priority, verify active status.

---

**Issue 2: Unexpected discount amount**

**Causes**:
- Multiple promotions stacking
- Percentage applied to already-discounted cost
- Rule priority incorrect

**Solution**: Check priority order, review stop_further_promotions flags, trace execution manually.

---

**Issue 3: Free shipping not working**

**Causes**:
- Lower priority surcharge rule adding cost after free shipping promotion
- Cart doesn't meet min value threshold
- Excluded products in cart

**Solution**: Use stop_further_promotions=Yes on free shipping promotion, verify conditions, check exclusions.

---

## Tips

- **Use high priority for free shipping** - Priority 100 ensures it executes before other adjustments
- **Set stop_further_promotions for absolute rules** - Free shipping should stop further processing
- **Test rule combinations** - Multiple promotions can interact unexpectedly
- **Use descriptive names** - "VIP 20% Discount (Priority 75)" better than "Promotion 3"
- **Document complex logic** - Add notes in description field
- **Start with simple promotions** - Add complexity gradually
- **Monitor rule performance** - Check if rules are being used or causing confusion
- **Avoid excessive promotions** - Too many promotions slow checkout, use 5-10 max
- **Use zones for geography** - Better than multiple similar rules per country
- **Combine with methods** - Rules + Methods work together for sophisticated pricing
- **Set clear time windows** - Always include end dates for promotions
- **Test edge cases** - Exactly $50, exactly 5 items, etc.