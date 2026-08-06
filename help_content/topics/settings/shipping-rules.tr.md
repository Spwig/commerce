---
title: Kargo Kuralları
---

Kargo kuralları, sepet içeriği, müşteri özellikleri ve teslimat bölgelerine göre kargo yöntemlerine koşullu maliyet ayarları uygular; $50'den fazla siparişlerde otomatik olarak ücretsiz kargo sunabilir, uzak bölgeler için ek ücret ekleyebilir ya da VIP müşterilere kargo için indirim yapabilir. Kurallar, daha yüksek öncelikli işlem (yüksek öncelik önce) ile isteğe bağlı durdurma bayrakları ile birlikte işlemeye devam etmez. Her kural, kart değerini, ağırlığı, bölgeleri, ürünleri ve müşteri gruplarını içeren birden fazla koşulu değerlendirir ve tüm koşullar uyuştuğunda 6 farklı düzeltme türüne sahip olur.

Kargo kurallarını, sipariş bağlamına göre değişen dinamik kargo maliyetlerine ihtiyacınız olduğunda kullanın, kargo yöntemlerinden statik oranlar değil.

## Kargo Kuralı Türleri

Kargo kuralları, 6 tür maliyet ayarlaması uygular:

### Yüzde İndirimi

**Ne Yapar**: Yüzde olarak kargo maliyetini azaltır (örneğin, %25 indirim).

**Formül**: `yeni_maliyet = temel_maliyet × (1 - yüzde/100)`

**Örnek**:
```
Temel maliyet: $20
İndirim: %25
Sonuç: $15
```

**Kullanım Durumları**:
- VIP müşteri indirimi (tüm kargo için %20 indirim)
- Sezonluk kampanyalar (Aralık ayında kargo için %15 indirim)
- Büyük sipariş indirimi (5+ ürün için kargo için %10 indirim)

---

### Sabit İndirim

**Ne Yapar**: Kargo maliyetinden sabit miktarı çıkarır.

**Formül**: `yeni_maliyet = temel_maliyet - tutar` (en az $0)

**Örnek**:
```
Temel maliyet: $15
İndirim: $5
Sonuç: $10
```

**Kullanım Durumları**:
- İlk kez müşteri bonusu ($5 ilk sipariş kargo indirimi)
- Bülten aboneliği ödülleri ($3 kargo indirimi)
- Sadakat programı avantajları ($10 aylık kargo indirimi)

---

### Sabit Maliyet

**Ne Yapar**: Kargo maliyetini belirli bir amounta çeker.

**Formül**: `yeni_maliyet = sabit_miktar`

**Örnek**:
```
Temel maliyet: $25
Ayarla: $9.99
Sonuç: $9.99
```

**Kullanım Durumları**:
- Hızlı satış (bugünkü tüm siparişler için sabit $5 kargo)
- Kategoriye özel kargo (kitaplar her zaman $3.99 kargo)
- Zamanına göre kampanyalar (bu hafta kargo $9.99 ile sınırlı)

---

### Ücretsiz Kargo

**Ne Yapar**: Kargo maliyetini $0 yapar.

**Formül**: `yeni_maliyet = $0`

**Örnek**:
```
Temel maliyet: $18
Kural uygulanır
Sonuç: $0
```

**Kullanım Durumları**:
- $50'den fazla siparişte ücretsiz kargo
- Belirli ürünler için ücretsiz kargo (tanıtım ürünleri)
- VIP müşterilere ücretsiz kargo
- 3+ ürün içeren siparişlerde ücretsiz kargo

---

### Ekstra Ücret (Sabit)

**Ne Yapar**: Kargo maliyetine sabit miktar ekler.

**Formül**: `yeni_maliyet = temel_maliyet + tutar`

**Örnek**:
```
Temel maliyet: $12
Ekstra ücret: $5
Sonuç: $17
```

**Kullanım Durumları**:
- Uzak bölge teslimat ücreti
- Büyük boyutlu ürün işleme
- Cumartesi teslimatı ekstra ücreti
- Kırılgan ürün paketleme ücreti

---

### Ekstra Ücret (Yüzde)

**Ne Yapar**: Kargo maliyetini yüzde olarak artırır.

**Formül**: `yeni_maliyet = temel_maliyet × (1 + yüzde/100)`

**Örnek**:
```
Temel maliyet: $20
Ekstra ücret: %15
Sonuç: $23
```

**Kullanım Durumları**:
- Zirve sezonu ekstra ücreti (yeni yıl gibi %20)
- Hızlı teslimat premiumu (50% ekstra ücret)
- Yakıt ekstra ücreti (mevcut oranlara göre değişken)

---

## Kural Koşulları

Kurallar, **tüm koşullar geçerli olmalı** kural uygulanması için:

### Zaman Geçerliliği

- **Başlangıç Tarihi**: Bu tarihten sonra kural sadece aktif olur
- **Bitiş Tarihi**: Bu tarihe kadar kural sadece aktif olur
- **Kullanım Durumu**: Sezonluk kampanyalar, sınırlı süreli teklifler

**Örnek**: Sadece Karanlık Bayramı haftasonu ücretsiz kargo
```
Başlangıç: 2026-11-27 00:00
Bitiş: 2026-11-30 23:59
```

---

### Sepet Değeri Aralığı

- **En Az Sepet Değeri**: Sepet toplamı ≥ miktar olmalı
- **En Fazla Sepet Değeri**: Sepet toplamı ≤ miktar olmalı
- **Kullanım Durumu**: Ücretsiz kargo eşiği, seviyeli indirimler

**Örnek**: $50-$200 arası siparişlerde ücretsiz kargo
```
En Az: $50
En Fazla: $200
```

---

### Sepet Ağırlığı Aralığı

- **En Az Ağırlık**: Toplam sepet ağırlığı ≥ miktar olmalı
- **En Fazla Ağırlık**: Toplam sepet ağırlığı ≤ miktar olmalı
- **Kullanım Durumu**: Hafif sevkiyat indirimleri, ağır ürün ekstra ücretleri

**Örnek**: 20kg'dan fazla siparişler için $5 ekstra ücret
```
En Az Ağırlık: 20kg
En Fazla Ağırlık: null (sınırsız)
```

---

### Ürün Sayısı Aralığı

- **Min Item Count**: Sepete en az sayıda ürün olmalı
- **Max Item Count**: Sepete en fazla sayıda ürün olmalı
- **Kullanım Durumu**: Toplu sipariş indirimleri, tek ürün ücretleri

**Örnek**: 5+ ürün için kargo ücretsiz
```
Min Items: 5
Max Items: null
```

---

### Kargo Bölgesi

- **Bölgeler**: Müşteri adresinin en azından seçilen bir bölgeye eşleşmesi durumunda kural uygulanır
- **Boş seçim**: Kural tüm bölgeler için geçerlidir
- **Kullanım Durumu**: Bölgesel ek ücretler veya indirimler

**Örnek**: Sadece Yerel bölge için kargo ücretsiz
```
Zones: ["Yerel ABD"]
```

---

### Kargo Yöntemi

- **Yöntemler**: Kuralın yalnızca belirli kargo yöntemlerine uygulanması
- **Boş seçim**: Kural tüm yöntemler için geçerlidir
- **Kullanım Durumu**: Yönteme özel kampanyalar

**Örnek**: 25% İfade edilen Kargo için indirim
```
Methods: ["İfade Edilen Teslimat"]
```

---

### Ürün Gereksinimleri

**Gereken Ürünler**: Sepette bu ürünlerden en az bir tane olmalı

**Gereken Kategoriler**: Sepette bu kategorilerden en az bir ürün olmalı

**Kullanım Durumu**: Ürün özel kargo ücretsizliği, kampanya paketleri

**Örnek**: Sepette "Promosyon Ürünü A" varsa kargo ücretsiz
```
Gereken Ürünler: [123 Numaralı Ürün]
```

---

### Ürün Hariçleri

**Harici Ürünler**: Sepette bu ürünlerden herhangi biri varsa kural uygulanmaz

**Harici Kategoriler**: Sepette bu kategorilerden herhangi bir ürün varsa kural uygulanmaz

**Kullanım Durumu**: Kargo ücretsizliğinden hariç tutulacak ağır/boyutlu ürünler

**Örnek**: Mobilya kategorisi hariç kargo ücretsiz
```
Harici Kategoriler: [Mobilya]
```

---

### Müşteri Grubu

- **Müşteri Grupları**: Seçilen gruplarda (VIP, Toptancı, vb.) olan müşterilere yalnızca kural uygulanır
- **Boş seçim**: Kural tüm müşteri grupları için geçerlidir
- **Kullanım Durumu**: VIP avantajları, toptancı indirimleri

**Örnek**: VIP üyeler için %15 kargo indirimi
```
Müşteri Grupları: ["VIP"]
```

---

### İlk Kez Müşteri

- **İlk Kez Müşteri**: Önceki siparişi olmayan müşterilere kuralın sınırlı hale getirilmesi için aç/kapa anahtarı
- **Kullanım Durumu**: Yeni müşteri için hoş geldiniz teklifleri

**Örnek**: İlk sipariş için $5 kargo indirimi
```
İlk Kez Müşteri: Evet
```

---

## Kuralların Önceliği ve Çalıştırılması

Kurallar **öncelik sırasına** göre çalışır (daha yüksek sayı = daha erken çalıştırma):

### Öncelik Mekaniği

**Örnek Çalışma**:
```
Kural A (Öncelik 100): Sepet > $50 ise kargo ücretsiz
Kural B (Öncelik 50): Tüm kargo için %10 indirim
Kural C (Öncelik 1): Uzak bölgeler için $2 ek ücret

Sepet: $60, Uzak bölge
Temel kargo maliyeti: $15

1. Adım: Kural A değerlendirilir (Öncelik 100)
   Sepet > $50? EVET
   Uygula: Maliyeti $0 olarak ayarla
   Maliyet şu an: $0

2. Adım: Kural B değerlendirilir (Öncelik 50)
   $0 üzerinde %10 indirim uygula
   Maliyet şu an: $0 (hâlâ ücretsiz)

3. Adım: Kural C değerlendirilir (Öncelik 1)
   $0'ya $2 ek ücret ekleyin
   Maliyet şu an: $2

Son maliyet: $2
```

**Daha Fazla Kuralları Durdur Flag**:

Eğer Kural A'nın `stop_further_rules = True` olması durumunda:
```
Kural A (Öncelik 100, stop_further_rules=True): Sepet > $50 ise kargo ücretsiz
Kural B (Öncelik 50): Tüm kargo için %10 indirim
Kural C (Öncelik 1): Uzak bölgeler için $2 ek ücret

Sepet: $60
Temel: $15

1. Adım: Kural A uygulanır, maliyeti $0 olarak ayarlar
        stop_further_rules = True → DUR

Son maliyet: $0 (Kurallar B ve C asla çalıştırılmaz)
```

---

## Kargo Kuralları Oluşturma

**Adım Adım İşlem Süreci**:

1. **Kurallara Git**
   - Ayarlar > Kargo > Kargo Kuralları
   - "Kargo Kuruluşu Ekle" butonuna tıkla

2. **Temel Yapılandırma**
   - **İsim**: İçsel tanımlayıcı (örneğin, "$50 Üzeri Kargo Ücretsizliği")
   - **Açıklama**: Opsiyonel notlar (müşterilere gösterilmez)
   - **Aktif**: Etkin/kapalı yapmak için aç/kapa
   - **Öncelik**: Gerçekleşme sırasını ayarla (yüksek öncelik için 100, düşük öncelik için 1)

3. **Kurul Türlerini Seç**
   - İndirim %'i, sabit indirim, maliyeti ayarla, ücretsiz, %'lik ek ücret, sabit ek ücret gibi düzenleme türünü seçin
   - Miktarı veya yüzdelik sayıyı girin

4. **Durdurma Bayrağını Ayarla** (Opsiyonel)
   - Bu kuralın daha düşük öncelikli kuralları engellemesi için "Daha Fazla Kuralları Durdur" seçeneğini işaretle
   - Son/kesin kurallar için kullanın (örneğin, kargo ücretsizliği, daha sonra ek ücret eklenmemelidir)


5. **Koşulları Tanımlayın** (Opsiyonel - "her zaman uygula" için boş bırakın)
  - Zaman geçerliliği: Başlangıç/bitiş tarihleri
  - Sepet değeri: Min/max
  - Sepet ağırlığı: Min/max
  - Ürün sayısı: Min/max
  - Bölgeler: Uygun olanları seçin
  - Yöntemler: Uygun olanları seçin
  - Ürünler: Gerekli veya hariç tutulanlar
  - Müşteriler: Gruplar veya ilk seferlik yalnızca

6. **Kuralı Kaydet**
  - Kaydet butonuna tıklayın
  - Kural, aktiflik anahtarı Evet ise hemen aktif hale gelir


## Ortak Kargo Kuralı Senaryoları

### Senaryo 1: $50'den Fazla Ücretsiz Kargo

**Hedef**: Sepet toplamı ≥ $50 iken ücretsiz kargo sunun.

**Yapılandırma**:
```
İsim: $50'den Fazla Ücretsiz Kargo
Tür: Ücretsiz Kargo
Öncelik: 100
Koşullar:
  En Az Sepet Değeri: $50
Daha Fazla Kuralı Durdur: Evet
```


### Senaryo 2: Uzak Bölge Ücreti

**Hedef**: Uzak bölgelere yapılan teslimatlarda $10 ücret ekleyin.

**Yapılandırma**:
```
İsim: Uzak Bölge Ücreti
Tür: Ücret (Sabit)
Miktar: $10
Öncelik: 50
Koşullar:
  Bölgeler: ["Uzak Alanlar"]
Daha Fazla Kuralı Durdur: Hayır
```


### Senaryo 3: VIP Müşteri %20 İndirim

**Hedef**: VIP müşteriler, tüm kargo için %20 indirim alsın.

**Yapılandırma**:
```
İsim: VIP Kargo İndirimi
Tür: İndirim (Yüzde)
Yüzde: 20
Öncelik: 75
Koşullar:
  Müşteri Grupları: ["VIP"]
Daha Fazla Kuralı Durdur: Hayır
```


### Senaryo 4: Bayramda Sabit Tutarlı Kargo

**Hedef**: Aralık ayında tüm kargo $9.99 olarak sınırlansın.

**Yapılandırma**:
```
İsim: Aralık Sabit Tutarlı Kampanyası
Tür: Sabit Maliyet
Miktar: $9.99
Öncelik: 100
Koşullar:
  Başlangıç Tarihi: 2026-12-01
  Bitiş Tarihi: 2026-12-31
Daha Fazla Kuralı Durdur: Evet
```


### Senaryo 5: Ağırlıklı Ürün Ücreti

**Hedef**: 25kg'dan fazla siparişler için $15 ücret ekleyin.

**Yapılandırma**:
```
İsim: Ağırlıklı Sipariş Ücreti
Tür: Ücret (Sabit)
Miktar: $15
Öncelik: 50
Koşullar:
  En Az Ağırlık: 25kg
Daha Fazla Kuralı Durdur: Hayır
```


### Senaryo 6: İlk Sipariş Ücretsiz Kargo

**Hedef**: Yeni müşterilerin ilk siparişinde ücretsiz kargo.

**Yapılandırma**:
```
İsim: İlk Sipariş Ücretsiz Kargo
Tür: Ücretsiz Kargo
Öncelik: 100
Koşullar:
  İlk Seferlik Müşteri: Evet
Daha Fazla Kuralı Durdur: Evet
```


### Senaryo 7: Kategoriye Özel Ücretsiz Kargo

**Hedef**: İndirimli kategori ürünlerini içeren siparişler için ücretsiz kargo.

**Yapılandırma**:
```
İsim: İndirimli Kategori Ücretsiz Kargo
Tür: Ücretsiz Kargo
Öncelik: 90
Koşullar:
  Gerekli Kategoriler: ["İndirimler"]
Daha Fazla Kuralı Durdur: Evet
```


### Senaryo 8: Ücretsiz Kargo'dan Mobilya Hariç Tutma

**Hedef**: $50'den fazla ücretsiz kargo, ancak sepet mobilya içermiyorsa.

**Çözüm**: İki kural

**Kural 1**:
```
İsim: Genel Ücretsiz Kargo
Tür: Ücretsiz Kargo
Öncelik: 50
Koşullar:
  En Az Sepet Değeri: $50
  Hariç Tutulan Kategoriler: ["Mobilya"]
Daha Fazla Kuralı Durdur: Hayır
```

**Kural 2**:
```
İsim: Mobilya Siparişleri $5 İndirimi
Tür: İndirim (Sabit)
Miktar: $5
Öncelik: 40
Koşullar:
  Gerekli Kategoriler: ["Mobilya"]
  En Az Sepet Değeri: $50
Daha Fazla Kuralı Durdur: Hayır
```


## Kural Birleştirme Stratejileri

### Strateji 1: Biriktirilen İndirimler

**Birden fazla indirimin biriktirilmesine izin verin**:
```
Kural A (Öncelik 100): VIP için %10 indirim → stop_further_rules=Hayır
Kural B (Öncelik 50): $100'den fazla siparişler için %15 indirim → stop_further_rules=Hayır

VIP müşteri $120 tutarında sipariş:
Temel: $15
Kural A'dan sonra: $13.50 (VIP %10 indirim)
Kural B'den sonra: $11.48 (Kurallı %15 indirim)
```

### Strateji 2: Özel Kurallar

**Sadece bir kural uygulanır** (en yüksek öncelik):
```
Kural A (Öncelik 100): $50'den fazla ücretsiz kargo → stop_further_rules=Evet
Kural B (Öncelik 50): Tüm kargo için %20 indirim → stop_further_rules=Evet

$50'den fazla sepet:
Kural A uygulanır → Ücretsiz kargo → DUR
Kural B asla çalışmayacak
```

### Strateji 3: Koşullu Ücretler

**İndirimler önce, ücretler sonra**:
```
Kural A (Öncelik 100): $75'den fazla ücretsiz kargo
Kural B (Öncelik 75): %15 VIP indirimi
Kural C (Öncelik 50): %10 genel indirim
Kural D (Öncelik 25): $5 uzak bölge ücreti
Kural E (Öncelik 1): %10 yakıt ücreti

Sipariş: $80, Uzak bölge, VIP müşteri
Temel: $20
A: $80 > $75 → Ücretsiz ($0)
B: VIP → $0 için %15 indirim = $0
C: $0 için %10 indirim = $0
D: Uzak bölge +$5 = $5
E: Yakıt +$5'in %10'u = $5.50
```


Preserve all markdown formatting, image paths, code blocks, and technical terms.

Final: $5.50 (ücret eklemesi nedeniyle ücretsiz değil)
```

**Bunun önüne geçmek için stop_further_rules=Hayır kullanın**:
```
Kural A (Öncelik 100, stop=Hayır): 75$'dan fazla için kargo ücretsiz

Same order:
A: $80 > $75 → Ücretsiz ($0) → DURDUR
Final: $0 (aslında ücretsiz)
```

---

## Kargo Kurallarını Test Etme

**Canlıya geçmeden önce**:

1. **Test Sepetleri Oluşturun**
   - Sepet A: $25 (eşik değerinin altında)
   - Sepet B: $55 (eşik değerinin üzerinde)
   - Sepet C: $200 + Uzak bölge
   - Sepet D: VIP müşteri

2. **Her Kuralı Test Edin**
   - Ödeme sayfasına geçin
   - Kargo ücretinin doğru şekilde gösterildiğinden emin olun
   - Kural işleme sırasını kontrol edin

3. **Öncelik Çözümlemesini Test Edin**
   - Birden fazla uyan kural
   - En yüksek önceliğin önce çalıştığını doğrulayın
   - stop_further_rules davranışını kontrol edin

4. **Kenar durumlarını test edin**
   - Sepet tutarının tam olarak eşik değerinde olması
   - Birden fazla koşulun uyması
   - Çakışan kurallar

---

## Sorun Giderme

**Problem 1: Kural uygulanmamakta**

**Nedenler**:
   - Kural etkin değil
   - Bir ya da daha fazla koşul karşılanmamış
   - Daha yüksek öncelikli bir kural stop_further_rules=Yes ayarına sahip
   - Geçerlilik süresi güncel tarihten farklı

**Çözüm**: Tüm koşulları gözden geçirin, önceliği kontrol edin, etkinlik durumunu doğrulayın.

---

**Problem 2: Beklenmeyen indirim miktarı**

**Nedenler**:
   - Birden fazla kuralın birlikte çalışması
   - Yüzde oranının zaten indirimi yapılan miktara uygulanması
   - Kural önceliğinin yanlış olması

**Çözüm**: Öncelik sırasını kontrol edin, stop_further_rules bayraklarını gözden geçirin, işlemi elle izleyin.

---

**Problem 3: Ücretsiz kargo çalışmıyor**

**Nedenler**:
   - Daha düşük öncelikli bir ek ücret kuralının, ücretsiz kargo kuralından sonra maliyet eklemesi
   - Sepet, minimum değer eşiğine ulaşmamış
   - Sepette hariç tutulan ürünler

**Çözüm**: ücretsiz kargo kuralında stop_further_rules=Yes kullanın, koşulları doğrulayın, hariçlikleri kontrol edin.

---

## İpuçları

- **Ücretsiz kargo için yüksek öncelik kullanın** - 100 önceliği, diğer düzeltmelerden önce çalışmasını sağlar
- **Kesin kurallar için stop_further_rules ayarlayın** - Ücretsiz kargo, daha fazla işleme izni vermemelidir
- **Kural kombinasyonlarını test edin** - Birden fazla kural beklenmedik şekilde etkileşime girebilir
- **Açıklamalı isimler kullanın** - "VIP %20 İndirimi (Öncelik 75)" gibi isimler "Kural 3" den daha iyidir
- **Kompleks mantığı belgeleyin** - Açıklama alanına not ekleyin
- **Basit kurallarla başlayın** - Karmaşıklığı yavaş yavaş ekleyin
- **Kural performansını izleyin** - Kuralların kullanılıp kullanılmadığını ya da kafa karıştırıp karıştırmadığını kontrol edin
- **Aşırı kural kullanmayın** - Çok fazla kural, ödeme işlemini yavaşlatabilir, maksimum 5-10 kuralı geçmeyin
- **Coğrafi bölgeler için bölgeler kullanın** - Birden fazla benzer kural yerine ülkeler için kullanın
- **Yöntemlerle birleştirin** - Kurallar + Yöntemler, gelişmiş fiyatlandırma için birlikte çalışır
- **Açık zaman aralıkları belirleyin** - İndirimler için son tarihleri kesinlikle ekleyin
- **Kenar durumlarını test edin** - Tam olarak $50, tam olarak 5 ürün, vb.