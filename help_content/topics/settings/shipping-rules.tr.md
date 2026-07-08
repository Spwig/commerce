---
title: Kargo Kuralları
---

Kargo kuralları, sepet içeriği, müşteri öznitelikleri ve teslimat bölgelerine göre kargo yöntemlerine koşullu maliyet ayarlamaları uygular - otomatik olarak 50$ üzerinde ücretsiz kargo sunar, uzak bölgelere ek ücretler ekler veya VIP müşterilere kargo indirimi yapar. Kurallar, öncelik temelli bir şekilde çalışır (yüksek öncelikli olanlar önce) ve daha fazla işleme engellenmesi için isteğe bağlı durdurma bayrakları kullanılır. Her kural, birden fazla koşulu değerlendirir (sepet değeri, ağırlığı, bölgeler, ürünler, müşteri grupları) ve tüm koşullar uyuştuğunda 6 ayarlama türünden birini çalıştırır.

Kargo kurallarını, kargo maliyetlerinin sadece statik oranlardan değil, sipariş bağlamına göre dinamik olarak değişmesi gerektiğinde kullanın.

## Kargo Kural Türleri

Kargo kuralları 6 tür maliyet ayarlama uygular:

### Yüzde İndirimi

**Ne Yapar**: Kargo maliyetini yüzdelik olarak azaltır (örneğin, %25 indirim).

**Formül**: `yeni_maliyet = temel_maliyet × (1 - yüzde/100)`

**Örnek**:
```
Temel maliyet: 20$
İndirim: %25
Sonuç: 15$
```

**Kullanım Alanları**:
- VIP müşteri indirimi (tüm kargo için %20 indirim)
- Mevsimsel kampanyalar (Aralık ayında kargo için %15 indirim)
- Toplu sipariş indirimi (5+ ürün için kargo için %10 indirim)

---

### Sabit İndirim

**Ne Yapar**: Kargo maliyetinden sabit bir tutar çıkarır.

**Formül**: `yeni_maliyet = temel_maliyet - tutar` (en az 0$)

**Örnek**:
```
Temel maliyet: 15$
İndirim: 5$
Sonuç: 10$
```

**Kullanım Alanları**:
- İlk sipariş müşterisi bonusu (ilk sipariş kargonun 5$ indirimi)
- Haberleme listesine kayıt ödüllü (kargonun 3$ indirimi)
- Loyalite programı faydası (ayda kargonun 10$ indirimi)

---

### Belirli Maliyet

**Ne Yapar**: Kargo maliyetini belirli bir tutara ayarlar.

**Formül**: `yeni_maliyet = sabit_tutar`

**Örnek**:
```
Temel maliyet: 25$
Ayarla: 9.99$
Sonuç: 9.99$
```

**Kullanım Alanları**:
- Flash satış (bugün tüm siparişler için 5$ sabit kargo)
- Kategori özel kargo (kitaplar her zaman 3.99$ kargo)
- Zaman bazlı kampanyalar (bu hafta kargonun 9.99$ üst sınırı)

---

### Ücretsiz Kargo

**Ne Yapar**: Kargo maliyetini 0$ yapar.

**Formül**: `yeni_maliyet = 0$`

**Örnek**:
```
Temel maliyet: 18$
Kural uygulanıyor
Sonuç: 0$
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
Temel maliyet: 12$
Ek Ücret: 5$
Sonuç: 17$
```

**Kullanım Alanları**:
- Uzak bölgelere teslimat ücreti
- Aşırı büyük ürün işleme ücreti
- Cumartesi teslimatı ek ücreti
- Kırılgan ürün ambalajlama ücreti

---

### Ek Ücret (Yüzde)

**Ne Yapar**: Kargo maliyetini yüzdelik olarak artırır.

**Formül**: `yeni_maliyet = temel_maliyet × (1 + yüzde/100)`

**Örnek**:
```
Temel maliyet: 20$
Ek Ücret: %15
Sonuç: 23$
```

**Kullanım Alanları**:
- Zirve sezonu ek ücreti (tatillerde %20)
- Hızlı teslimat ek ücreti (%50)
- Yakıt ek ücreti (mevcut oranlara göre değişken)

---

## Kural Koşulları

Kurallar, kuralın uygulanabilmesi için **tüm koşulların geçmesi** gerekir:

### Zaman Geçerliliği

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
- **Kullanım Alanı**: Ücretsiz kargo eşiği, katmanlı indirimler

**Örnek**: 50$-200$ arası siparişler için ücretsiz kargo
```
Min: 50$
Max: 200$
```

---

### Sepet Ağırlığı Aralığı

- **Min Ağırlık**: Toplam sepet ağırlığı ≥ tutar olmalıdır
- **Max Ağırlık**: Toplam sepet ağırlığı ≤ tutar olmalıdır
- **Kullanım Alanı**: Hafif gönderim indirimleri, ağır ürün ek ücretleri

**Örnek**: 20kg üzerindeki siparişler için 5$ ek ücret
```
Min Ağırlık: 20kg
Max Ağırlık: null (sınırsız)
```

---

### Ürün Sayısı Aralığı

- **Min Ürün Sayısı**: Sepette ≥ ürün sayısı olmalıdır
- **Max Ürün Sayısı**: Sepette ≤ ürün sayısı olmalıdır
- **Kullanım Alanı**: Toplu sipariş indirimleri, tek ürün ücretleri

**Örnek**: 5+ ürün için ücretsiz kargo
```
Min Ürünler: 5
Max Ürünler: null
```

---

### Kargo Bölgesi

- **Bölgeler**: Kural, müşteri adresi seçilen bölgelerden en az birine uyuşuyorsa uygulanır
- **Boş seçim**: Kural tüm bölgelere uygulanır
- **Kullanım Alanı**: Bölgesel ek ücretler veya indirimler

**Örnek**: Sadece Ulusal bölge için ücretsiz kargo
```
Bölgeler: ["Domestic USA"]
```

---

### Kargo Yöntemi

- **Yöntemler**: Kural sadece belirli kargo yöntemlerine uygulanır
- **Boş seçim**: Kural tüm yöntemlere uygulanır
- **Kullanım Alanı**: Yöntem özel kampanyalar

**Örnek**: Hızlı Teslimat için %25 indirim
```
Yöntemler: ["Hızlı Teslimat"]
```

---

### Ürün Gereksinimleri

**Gerekli Ürünler**: Sepette bu ürünlerden en az bir tane olmalıdır

**Gerekli Kategoriler**: Sepette bu kategorilerden en az bir ürün olmalıdır

**Kullanım Alanı**: Ürün özel ücretsiz kargo, promosyon paketleri

**Örnek**: Sepette "Promosyon Ürün A" varsa ücretsiz kargo
```
Gerekli Ürünler: [Ürün Kimliği 123]
```

---

### Ürün Hariç Tutma

**Hariç Tutulan Ürünler**: Kural, sepet bu ürünlerden herhangi birini içeriyorsa uygulanmaz

**Hariç Tutulan Kategoriler**: Kural, sepet bu kategorilerden herhangi bir ürünü içeriyorsa uygulanmaz

**Kullanım Alanı**: Ağır/boyutlu ürünlerin ücretsiz kargonun dışına çıkarma

**Örnek**: Mobilya kategorisi hariç ücretsiz kargo
```
Hariç Tutulan Kategoriler: [Mobilya]
```

---

### Müşteri Grubu

- **Müşteri Grupları**: Kural, seçilen gruplardaki müşterilere uygulanır (VIP, Toptan, vb.)
- **Boş seçim**: Kural tüm müşteri gruplarına uygulanır
- **Kullanım Alanı**: VIP faydaları, toptan indirimler

**Örnek**: VIP üyelerine %15 kargo indirimi
```
Müşteri Grupları: ["VIP"]
```

---

### İlk Sipariş Müşterisi

- **İlk Sipariş Müşterisi**: Kuralın sadece önceki siparişi olmayan müşterilere uygulanmasını sağlar
- **Kullanım Alanı**: Yeni müşteri hoş geldiniz teklifleri

**Örnek**: İlk sipariş için kargonun 5$ indirimi
```
İlk Sipariş Müşterisi: Evet
```

---

## Kural Önceliği ve Uygulama

Kurallar **öncelik sırasına** göre çalışır (yüksek sayı = daha erken uygulama):

### Öncelik Mekanizması

**Örnek Uygulama**:
```
Kural A (Öncelik 100): Sepet > 50$ ise ücretsiz kargo
Kural B (Öncelik 50): Tüm kargo için %10 indirim
Kural C (Öncelik 1): Uzak bölgelere 2$ ek ücret

Sepet: 60$, Uzak bölge
Temel kargo maliyeti: 15$

Adım 1: Kural A değerlendirilir (Öncelik 100)
  Sepet > 50$? EVET
  Uygula: Maliyeti 0$ yap
  Maliyet şimdi: 0$

Adım 2: Kural B değerlendirilir (Öncelik 50)
  0$'a %10 indirim uygula
  Maliyet şimdi: 0$ (hâlâ ücretsiz)

Adım 3: Kural C değerlendirilir (Öncelik 1)
  0$'a 2$ ek ücret ekle
  Maliyet şimdi: 2$

Son maliyet: 2$
```

**Daha Fazla Kuralı Durdur Bayrağı**:

Eğer Kural A'nın `stop_further_rules = True`:
```
Kural A (Öncelik 100, stop_further_rules=True): Sepet > 50$ ise ücretsiz kargo
Kural B (Öncelik 50): %10 indirim
Kural C (Öncelik 1): 2$ ek ücret

Sepet: 60$
Temel: 15$

Adım 1: Kural A uygulanır, maliyeti 0$ yapar
        stop_further_rules = True → DUR

Son maliyet: 0$ (Kural B ve C asla uygulanmaz)
```

---

## Kargo Kuralları Oluşturma

**Adım Adım İş Akışı**:

1. **Kurallara Git**
   - Ayarlar > Kargo > Kargo Kuralları
   - "Kargo Kuralı Ekle"ye tıklayın

2. **Temel Yapılandırma**
   - **Ad**: İçerik tanımlayıcısı (örneğin, "50$ Üzeri Ücretsiz Kargo")
   - **Açıklama**: Opsiyonel notlar (müşterilere gösterilmez)
   - **Aktif**: Kuralı etkinleştirmek için anahtar
   - **Öncelik**: Uygulama sırasını belirleyin (100 yüksek öncelik, 1 düşük öncelik)

3. **Kural Türünü Seçin**
   - Ayarlama türünü seçin (indirim %, sabit indirim, belirli maliyet, ücretsiz, yüzde ek ücret, sabit ek ücret)
   - Tutar veya yüzdelik girin

4. **Durdurma Bayrağını Ayarla** (Opsiyonel)
   - Bu kuralın daha düşük öncelikli kuralların çalışmasını engellemesi gerekiyorsa "Daha Fazla Kuralı Durdur" seçeneğini işaretleyin
   - Son/kesin kurallar için kullanın (örneğin, ücretsiz kargo sonrasında ek ücretler eklenmemeli)

5. **Koşulları Tanımlayın** (Opsiyonel - boş bırakın "her zaman uygula")
   - Zaman geçerliliği: Başlangıç/Bitiş tarihleri
   - Sepet değeri: Min/max
   - Sepet ağırlığı: Min/max
   - Ürün sayısı: Min/max
   - Bölgeler: Uygulanabilecek bölgeleri seçin
   - Yöntemler: Uygulanabilecek yöntemleri seçin
   - Ürünler: Gerekli veya hariç tutulan
   - Müşteri: Gruplar veya sadece ilk sipariş

6. **Kuralları Kaydet**
   - Kaydet'e tıklayın
   - Kural, etkin anahtar "Evet" ise hemen aktif olur

---

## Ortak Kargo Kural Senaryoları

### Senaryo 1: 50$ Üzeri Ücretsiz Kargo

**Hedef**: Sepet alt toplamı ≥ 50$ olduğunda ücretsiz kargo sunun.

**Yapılandırma**:
```
Ad: 50$ Üzeri Ücretsiz Kargo
Tip: Ücretsiz Kargo
Öncelik: 100
Koşullar:
  Min Sepet Değeri: 50$
Daha Fazla Kuralı Durdur: Evet
```

---

### Senaryo 2: Uzak Bölge Ek Ücreti

**Hedef**: Uzak bölgelere teslimat için 10$ ek ücret ekle.

**Yapılandırma**:
```
Ad: Uzak Bölge Ek Ücreti
Tip: Ek Ücret (Sabit)
Tutar: 10$
Öncelik: 50
Koşullar:
  Bölgeler: ["Uzak Bölgeler"]
Daha Fazla Kuralı Durdur: Hayır
```

---

### Senaryo 3: VIP Müşteri %20 İndirimi

**Hedef**: VIP müşterilere tüm kargo için %20 indirim.

**Yapılandırma**:
```
Ad: VIP Kargo İndirimi
Tip: İndirim (Yüzde)
Yüzde: 20
Öncelik: 75
Koşullar:
  Müşteri Grupları: ["VIP"]
Daha Fazla Kuralı Durdur: Hayır
```

---

### Senaryo 4: Aralık Ayı Sabit Oran

**Hedef**: Aralık ayında tüm kargonun 9.99$ üst sınırına getirilmesi.

**Yapılandırma**:
```
Ad: Aralık Ayı Sabit Oran Kampanyası
Tip: Belirli Maliyet
Tutar: 9.99$
Öncelik: 100
Koşullar:
  Başlangıç Tarihi: 2026-12-01
  Bitiş Tarihi: 2026-12-31
Daha Fazla Kuralı Durdur: Evet
```

---

### Senaryo 5: Ağır Ürün Ek Ücreti

**Hedef**: 25kg üzerindeki siparişler için 15$ ücreti ekle.

**Yapılandırma**:
```
Ad: Ağır Sipariş Ek Ücreti
Tip: Ek Ücret (Sabit)
Tutar: 15$
Öncelik: 50
Koşullar:
  Min Ağırlık: 25kg
Daha Fazla Kuralı Durdur: Hayır
```

---

### Senaryo 6: İlk Sipariş Ücretsiz Kargo

**Hedef**: Yeni müşterilere ilk sipariş için ücretsiz kargo sunun.

**Yapılandırma**:
```
Ad: İlk Sipariş Ücretsiz Kargo
Tip: Ücretsiz Kargo
Öncelik: 100
Koşullar:
  İlk Sipariş Müşterisi: Evet
Daha Fazla Kuralı Durdur: Evet
```

---

### Senaryo 7: Kategori Özel Ücretsiz Kargo

**Hedef**: Promosyon kategori ürünleri içeren siparişler için ücretsiz kargo.

**Yapılandırma**:
```
Ad: Promosyon Kategorisi Ücretsiz Kargo
Tip: Ücretsiz Kargo
Öncelik: 90
Koşullar:
  Gerekli Kategoriler: ["Promosyonlar"]
Daha Fazla Kuralı Durdur: Evet
```

---

### Senaryo 8: Mobilya Ücretsiz Kargonun Dışında Kal

**Hedef**: 50$ üzerinde ücretsiz kargo, ancak sepet mobilya içeriyorsa hariç tutun.

**Çözüm**: İki kural

**Kural 1**:
```
Ad: Genel Ücretsiz Kargo
Tip: Ücretsiz Kargo
Öncelik: 50
Koşullar:
  Min Sepet Değeri: 50$
  Hariç Tutulan Kategoriler: ["Mobilya"]
Daha Fazla Kuralı Durdur: Hayır
```

**Kural 2**:
```
Ad: Mobilya Siparişleri için 5$ İndirimi
Tip: İndirim (Sabit)
Tutar: 5$
Öncelik: 40
Koşullar:
  Gerekli Kategoriler: ["Mobilya"]
  Min Sepet Değeri: 50$
Daha Fazla Kuralı Durdur: Hayır
```

---

## Kural Kombinasyon Stratejileri

### Strateji 1: İndirimleri Yığma

**Birden fazla indirimin yığılmasını sağlayın**:
```
Kural A (Öncelik 100): VIP için %10 indirim → stop_further_rules=Hayır
Kural B (Öncelik 50): 100$ üzerinde %15 indirim → stop_further_rules=Hayır

VIP müşteri 120$ siparişi:
Temel: 15$
Kural A'dan sonra: 13.50$ (10% indirim)
Kural B'den sonra: 11.48$ (15% indirim 13.50$)
```

### Strateji 2: Özel Kurallar

**Sadece bir kural uygulanır** (en yüksek öncelik):
```
Kural A (Öncelik 100): 50$ üzerinde ücretsiz kargo → stop_further_rules=Evvet
Kural B (Öncelik 50): Tüm kargo için %20 indirim → stop_further_rules=Evvet

Sepet > 50$:
Kural A uygulanır → Ücretsiz kargo → DUR
Kural B asla uygulanmaz
```

### Strateji 3: Koşullu Ek Ücretler

**İndirimleri önce, ek ücretleri sonra**:
```
Kural A (Öncelik 100): 75$ üzerinde ücretsiz kargo
Kural B (Öncelik 75): VIP için %15 indirim
Kural C (Öncelik 50): Genel %10 indirim
Kural D (Öncelik 25): Uzak bölge için 5$ ek ücret
Kural E (Öncelik 1): Yakıt için %10 ek ücret

Sipariş: 80$, Uzak bölge, VIP müşteri
Temel: 20$
A: 80$ > 75$ → Ücretsiz (0$)
B: VIP → 0$'a %15 indirim = 0$
C: 0$'a %10 indirim = 0$
D: Uzak bölge +5$ = 5$
E: Yakıt +10% 5$ = 5.50$

Son: 5.50$ (ücretsiz değil, çünkü ek ücretler var)
```

**Bunu önlemek için stop_further_rules=Evvet kullanın**:
```
Kural A (Öncelik 100, stop=Evvet): 75$ üzerinde ücretsiz kargo

Aynı sipariş:
A: 80$ > 75$ → Ücretsiz (0$) → DUR
Son: 0$ (gerçekten ücretsiz)
```

---

## Kargo Kurallarını Test Etme

**Yaşamaya hazır olana kadar**:

1. **Test Sepetleri Oluşturun**
   - Sepet A: 25$ (eşiğin altında)
   - Sepet B: 55$ (eşiğin üstünde)
   - Sepet C: 200$ + Uzak bölge
   - Sepet D: VIP müşteri

2. **Her Kuralı Test Edin**
   - Ödeme ekranına gidin
   - Doğru kargo maliyetinin görüntülendiğini doğrulayın
   - Kural uygulama sırasını kontrol edin

3. **Öncelik Çözümünü Test Edin**
   - Birden fazla eşleşen kural
   - En yüksek önceliğin önce uygulandığını doğrulayın
   - stop_further_rules davranışını kontrol edin

4. **Kenar Durumları Test Edin**
   - Sepet değeri tam olarak eşikte
   - Birden fazla koşulun eşleştiği
   - Çelişen kurallar

---

## Sorun Giderme

**Sorun 1: Kural uygulanmıyor**

**Nedenleri**:
- Kural etkin değil
- Bir veya daha fazla koşul karşılanmamış
- Daha yüksek öncelikli kural stop_further_rules=Yes ayarlanmış
- Zaman geçerliliği geçerli tarihten farklı

**Çözüm**: Tüm koşulları gözden geçirin, önceliği kontrol edin, etkin durumunu doğrulayın.

---

**Sorun 2: Beklenmedik indirim tutarı**

**Nedenleri**:
- Birden fazla kuralın yığılması
- Yüzde, zaten indirilmiş maliyete uygulanıyor
- Kural önceliği yanlış

**Çözüm**: Öncelik sırasını kontrol edin, stop_further_rules bayraklarını gözden geçirin, uygulamayı elle takip edin.

---

**Sorun 3: Ücretsiz kargo çalışmıyor**

**Nedenleri**:
- Daha düşük öncelikli ek ücret kuralı, ücretsiz kargo kuralından sonra maliyeti ekliyor
- Sepet, min değer eşiklerini karşılamıyor
- Sepette hariç tutulan ürünler var

**Çözüm**: Ücretsiz kargo kuralında stop_further_rules=Yes ayarlayın, koşulları doğrulayın, hariç tutmaları kontrol edin.

---

## İpuçları

- **Ücretsiz kargo için yüksek öncelik kullanın** - Öncelik 100, diğer ayarlamaların önce uygulanmasını sağlar
- **Açık uçlu kurallar için stop_further_rules ayarlayın** - Ücretsiz kargo, daha fazla işleme engellenmeli
- **Kural kombinasyonlarını test edin** - Birden fazla kural beklenmedik şekilde etkileşebilir
- **Açıklık veren isimler kullanın** - "VIP %20 İndirimi (Öncelik 75)" "Kural 3"'ten daha iyi
- **Karmaşık mantığı belgeleyin** - Açıklama alanına not ekleyin
- **Basit kurallarla başlayın** - Karmaşıklığı yavaş yavaş artırın
- **Kural performansını izleyin** - Kuralların kullanılıp kullanılmadığını, karışıklığa neden olup olmadığını kontrol edin
- **Aşırı kurallardan kaçının** - Çok fazla kural ödeme sırasında yavaşlatır, 5-10 kadar kullanın
- **Bölgeler için coğrafi bölge kullanın** - Ülkeler için benzer kurallar yerine
- **Yöntemlerle birlikte kullanın** - Kurallar + Yöntemler, sofistike fiyatlandırma için birlikte çalışır
- **Açık zaman penceresi ayarlayın** - Kampanyalar için her zaman bitiş tarihini ekleyin
- **Kenar durumlarını test edin** - Tam olarak 50$, tam olarak 5 ürün, vb.

Unutmayın: Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri gösterilen koruma kurallarına uygun şekilde koruyun.