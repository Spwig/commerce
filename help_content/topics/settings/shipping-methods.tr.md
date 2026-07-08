---
title: Kargo Yöntemleri
---

Kargo yöntemleri, müşteriye yönelik ödeme seçenekleridir ve checkout sırasında gösterilir—her yöntem, farklı fiyatlandırma stratejileri kullanarak kargo maliyetlerini hesaplar. Spwig, basit sabit oranlardan karmaşık taşıyıcı tarafından hesaplanan gerçek zamanlı fiyatlandırma gibi 7 yöntem türü destekler. Yöntemler, minimum/maksimum sipariş değeri, ağırlık ve coğrafi bölgelere göre kısıtlanabilir. Müşteriler, checkout sırasında tercih ettikleri yöntemi seçer ve hesaplanan maliyet sipariş toplamına eklenir.

Bu kılavuzu, iş modelinize uygun kargo yöntemlerini yapılandırmak için kullanın, temel sabit oranlı kargo yöntemlerinden karmaşık bölgelere göre katmanlı fiyatlandırma gibi gelişmiş yöntemlere kadar.

## Kargo Yöntemi Türleri

Spwig, farklı maliyet hesaplama mantığına sahip 7 kargo yöntemi türü sunar:

### Sabit Oranlı Kargo

**Ne Olduğunu**: Sepet içeriği, hedef veya ağırlık ne olursa olsun sabit bir maliyet.

**Ne Zaman Kullanılır**:
- Tahmini kargo maliyetlerine sahip basit mağazalar
- Tek ürün türü (benzer boyut/ağırlık)
- Ulusal kargo ile standart taşıyıcı oranları
- Ücretsiz kargo eşik promosyonları (kargo kuralları ile birlikte kullanılabilir)

**Yapılandırma**:
- **Yöntem Türü** = Sabit Oran
- **Sabit Maliyet** girin (örneğin, $9.99)
- Opsiyonel: Min/max sipariş değeri kısıtlamaları ayarlayın

**Örnek**: "Standart Kargo - $9.99" tüm ulusal siparişler için.

---

### Ücretsiz Kargo

**Ne Olduğunu**: Müşteriye ücret alınmayan kargo seçeneği.

**Ne Zaman Kullanılır**:
- Ücretsiz kargo promosyonları
- Yüksek değerli siparişler (min sipariş değeri ile birlikte)
- Yerel toplama alternatifi
- Loyalite programı avantajları

**Yapılandırma**:
- **Yöntem Türü** = Ücretsiz Kargo
- Opsiyonel: **Min Sipariş Değeri** ayarlayın (örneğin, $50 üzeri ücretsiz)
- Kargo kuralları ile birlikte kullanıldığında koşullu ücretsiz kargo için iyi çalışır

**Örnek**: "$50 Üzeri Siparişlerde Ücretsiz Kargo" min_order_value = $50 ile.

---

### Ağırlık Temelli Kargo

**Ne Olduğunu**: Toplam sepet ağırlığına göre katmanlı oran tablosuna dayalı maliyet hesaplanır.

**Ne Zaman Kullanılır**:
- Değişken ağırlıklara sahip ürünler (kitaplar, donanım, market ürünleri)
- Ağırlık temelli taşıyıcı fiyatlandırma modelleri
- Tahmini ağırlık/maliyet oranı

**Yapılandırma**:
1. **Yöntem Türü** = Ağırlık Temelli olarak ayarlayın
2. **Kargo Oran Tablosu** oluşturun, basis_type = "weight"
3. **Kargo Oran Katmanları** ekleyin (örneğin, 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Opsiyonel: Belirli bölgelere kısıtla

**Örnek**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**Nasıl Çalışır**: Sepet toplam ağırlığını hesaplar → uygun katmanı bulur → katmanın oranını döndürür.

---

### Fiyat Temelli Kargo

**Ne Olduğunu**: Sepet alt toplamına göre katmanlı oran tablosuna dayalı maliyet hesaplanır.

**Ne Zaman Kullanılır**:
- Kargo maliyeti sipariş değerine göre değişir
- Daha yüksek sepet değerlerini teşvik et (daha yüksek katmanlarda dolar başına daha düşük oran)
- Benzer fiyatlı ürünler için ağırlık temelli alternatif

**Yapılandırma**:
1. **Yöntem Türü** = Fiyat Temelli olarak ayarlayın
2. **Kargo Oran Tablosu** oluşturun, basis_type = "price"
3. **Kargo Oran Katmanları** ekleyin (örneğin, $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Örnek**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Ücretsiz
```

**Nasıl Çalışır**: Sepet alt toplamını hesaplar → uygun katmanı bulur → katmanın oranını döndürür.

---

### Gerçek Zamanlı Taşıyıcı Oranları

**Ne Olduğunu**: Checkout sırasında taşıyıcı API'lerinden (FedEx, UPS, DHL) alınan canlı oranlar.

**Ne Zaman Kullanılır**:
- Hedefe göre değişken kargo maliyetleri
- Müşteriler için birden fazla taşıyıcı seçeneği
- Manuel oran tabloları olmadan doğrudan taşıyıcı fiyatlandırma
- Karmaşık fiyatlandırma ile uluslararası kargo

**Yapılandırma**:
1. **Yöntem Türü** = Gerçek Zamanlı olarak ayarlayın
2. **Taşıyıcı Hesap** oluşturun (Ayarlar > Kargo > Taşıyıcı Hesapları)
3. Taşıyıcı API kimlik bilgilerini girin (hesap numarası, API anahtarı, gizli)
4. Taşıyıcı hesabını kargo yöntemi ile bağlayın
5. Opsiyonel: Markup yüzdesi veya sabit markup ekleyin

**Gereksinimler**:
- Aktif taşıyıcı hesabı (FedEx, UPS, DHL vb.)
- Taşıyıcıdan alınan API kimlik bilgileri
- Kargo paketleri tanımlanmış (boyut ağırlığı hesaplaması için)

**Örnek**: "FedEx Ground" yöntemi, checkout sırasında sepet ağırlığı, boyutları ve hedefe göre canlı FedEx oranlarını alır.

**Nasıl Çalışır**:
1. Müşteri checkout sırasında adres girer
2. Sistem, orijin, hedef, paket boyutları ve ağırlığı ile taşıyıcı API'sini çağırır
3. Taşıyıcı oran teklifini döndürür
4. Opsiyonel markup uygulanır
5. Oran müşteriye gösterilir

---

### Yerel Toplama

**Ne Olduğunu**: Müşteri, fiziksel bir konumda siparişi toplar (kargo maliyeti yoktur).

**Ne Zaman Kullanılır**:
- Toplama sunan mağazalar
- Depo toplama seçenekleri
- Etkinlikler veya pazar stantları
- Yerel müşterilere kargo maliyetlerini kaldırır

**Yapılandırma**:
1. **Yöntem Türü** = Yerel Toplama olarak ayarlayın
2. **Konum** oluşturun (Ayarlar > Kargo > Konumlar)
   - Adres, çalışma saatleri, toplama kapasitesi ayarlayın
3. Konumu yönteme bağlayın
4. Opsiyonel: Toplama hazırlama süresi ayarlayın (örneğin, "2 saat içinde hazır").

**Müşteri Deneyimi**:
- Checkout sırasında "Yerel Toplama" seçer
- Birden fazla konum varsa konumu seçer
- Kullanılabilirlik temelinde toplama tarih/saati seçer
- Sipariş hazır olduğunda bildirim alır

**Örnek**: "Mağaza'da Toplama - Ücretsiz" 3 perakende konumu ile, 24 saat içinde hazır.

---

### Tablo Oranlı Kargo

**Ne Olduğunu**: Ağırlık, fiyat veya miktar temelli esnek katmanlı fiyatlandırma, ileri düzey bölge hedefleme ile.

**Ne Zaman Kullanılır**:
- Karmaşık fiyatlandırma (zona göre ve ağırlıkla farklı oranlar)
- Ağırlık temelli veya fiyat temelli yöntemlerden daha fazla kontrol gerekir
- Birden fazla fiyatlandırma faktörü (örneğin, ağırlık + hedef + miktar)

**Yapılandırma**:
1. **Yöntem Türü** = Tablo Oranı olarak ayarlayın
2. **Kargo Oran Tablosu** oluşturun
3. **basis_type** tanımlayın: ağırlık, fiyat veya miktar
4. **Kargo Oran Katmanları** ekleyin ve min/max değerlerini ayarlayın
5. Opsiyonel: Katmanları belirli bölgelere veya ülkelere kısıtla

**Ağırlık/Fiyat Temelli ile Farkı**: Tablo oranı, katman başına coğrafi kısıtlamaları destekler, farklı bölgelerde aynı ağırlık/fiyat için farklı oranlara izin verir.

**Örnek**:
```
Zona A (Ulusal):
  0-5kg: $10
  5-10kg: $15

Zona B (Uzak):
  0-5kg: $18
  5-10kg: $25
```

**Nasıl Çalışır**: Sepet, basis değeri (ağırlık/fiyat/miktar) hesaplar → müşteri bölgesi için uygun katmanı bulur → katmanın oranını döndürür.

---

## Kargo Yöntemi Yapılandırması

Tüm kargo yöntemleri, bu ortak ayarları paylaşır:

### Temel Ayarlar

- **Ad**: İçerik tanımlayıcısı (müşterilere gösterilmez)
- **Gösterilecek Ad**: Checkout sırasında müşteriye yönelik ad (örneğin, "Standart Kargo", "Hızlı Teslimat")
- **Açıklama**: Checkout sırasında gösterilecek yardım metni (örneğin, "3-5 iş günü içinde teslimat")
- **Yöntem Türü**: Yukarıdaki 7 türden biri
- **Aktif**: Yöntemi silmeden etkin/etkin değil olarak anahtarlayın

### Maliyet Ayarları

- **Sabit Maliyet**: Sabit oran yöntemleri için yalnızca
- **Oran Tablosu**: Ağırlık temelli, fiyat temelli, tablo oranlı yöntemler için
- **Taşıyıcı Hesabı**: Gerçek zamanlı taşıyıcı yöntemleri için
- **Vergi Sınıfı**: Kargo maliyetine vergi uygulayın (uygulanabilirse)

### Kısıtlamalar

**Sipariş Değeri Kısıtlamaları**:
- **Min Sipariş Değeri**: Sipariş alt toplamı ≥ miktar ise yöntem yalnızca kullanılabilir (örneğin, $50 üzeri ücretsiz kargo)
- **Max Sipariş Değeri**: Sipariş alt toplamı > miktar ise yöntem gizlenir (örneğin, $100 altında sabit oran)

**Ağırlık Kısıtlamaları**:
- **Min Ağırlık**: Sipariş ağırlığı ≥ miktar ise yöntem yalnızca kullanılabilir
- **Max Ağırlık**: Sipariş ağırlığı > miktar ise yöntem gizlenir (hafif kargo seçenekleri için yaygın)

**Coğrafi Kısıtlamalar**:
- **Kargo Bölgeleri**: Yöntemi belirli bölgelere (ulusal, uluslararası, bölgesel) bağlayın
- Boş bölgeler = tüm adresler için kullanılabilir
- Birden fazla bölge = herhangi bir eşleşen bölge için kullanılabilir

### Gelişmiş Ayarlar

- **Öncelik**: Checkout'da gösterim sırası (düşük sayı = listede daha yüksek)
- **İşlem Ücreti**: Hesaplanan maliyete eklenen ek sabit ücret
- **Ücretsiz Kargo Eşiği**: Sipariş alt toplamı ≥ eşik ise maliyeti otomatik olarak $0 yap (min_order_value alternatifi)

---

## Kargo Yöntemi Oluşturma

**Adım Adım İş Akışı**:

1. **Kargo Yöntemlerine Git**
   - Ayarlar > Sepet > Kargo Yöntemlerine gidin
   - "Kargo Yöntemi Ekle"ye tıklayın

2. **Yöntem Türünü Seçin**
   - Fiyatlandırma stratejinize göre uygun türü seçin
   - Tür, kullanılabilir maliyet yapılandırma alanlarını belirler

3. **Temel Bilgileri Yapılandırın**
   - Ad: İçerik referansı (örneğin, "domestic_ground")
   - Gösterilecek Ad: Müşteriye yönelik (örneğin, "Zemin Kargo")
   - Açıklama: Teslimat zaman çerçevesi (örneğin, "5-7 iş günü")

4. **Maliyet Hesaplamasını Ayarlayın**
   - **Sabit Oran**: Sabit maliyet girin
   - **Ağırlık/Fiyat/Tablo Oranı**: Oran tablosu oluşturun (aşağıya bakın)
   - **Gerçek Zamanlı**: Taşıyıcı hesabı bağlayın
   - **Ücretsiz/Toplama**: Maliyet yapılandırması gerekmez

5. **Kısıtlamalar Ekle (Opsiyonel)**
   - Min/max sipariş değeri
   - Min/max ağırlık
   - Kargo bölgeleri

6. **Önceliği Ayarlayın**
   - Düşük sayılar checkout'da daha önce gösterilir
   - Önerilen sıralama: Ücretsiz (1), Yerel Toplama (2), Standart (3), Hızlı (4)

7. **Yöntemi Etkinleştirin**
   - "Aktif" = Evet olarak anahtarlayın
   - Kaydedin

---

## Oran Tabloları Oluşturma

Ağırlık temelli, fiyat temelli ve tablo oranlı yöntemler için:

**Adım 1: Oran Tablosu Oluşturun**
- Ayarlar > Kargo > Oran Tablolarına gidin
- "Oran Tablosu Ekle"ye tıklayın
- **Ad** ayarlayın (örneğin, "Ulusal Ağırlık Katmanları")
- **Basis Türü** ayarlayın: ağırlık, fiyat veya miktar

**Adım 2: Katman Ekle**
- "Katman Ekle"ye tıklayın
- **Min Değer** ve **Max Değer** ayarlayın (eşleşen aralık)
- **Oran** ayarlayın (bu katman için maliyet)
- Opsiyonel: Belirli bölgelere veya ülkelere kısıtla
- Katmanı kaydedin

**Adım 3: Tüm Katmanlar İçin Tekrarlayın**
- Tam aralığı kapsayın (0 ile maksimum beklenebilir değer)
- Boşluk bırakmayın (örneğin, 0-5, 5-10, 10-20, 20+)
- Son katmanda **Max Değer** için `null` kullanın (sınırsız)

**Adım 4: Kargo Yöntemine Bağlayın**
- Kargo yöntemi düzenle
- Dropdown'dan oran tablosunu seçin
- Kaydedin

**Örnek Ağırlık Temelli Tablo**:
```
Ad: Ulusal Ağırlık Katmanları
Basis: Ağırlık

Katmanlar:
1. Min: 0g, Max: 2000g, Oran: $8
2. Min: 2000g, Max: 5000g, Oran: $12
3. Min: 5000g, Max: 10000g, Oran: $18
4. Min: 10000g, Max: null, Oran: $25
```

---

## Ortak Kargo Senaryoları

### Senaryo 1: Temel Ulusal Kargo

**Hedef**: Tüm ulusal siparişler için basit $9.99 sabit oranı.

**Çözüm**:
- Yöntem Türü: Sabit Oran
- Sabit Maliyet: $9.99
- Kargo Bölgesi: "Ulusal" (yalnızca ülkeniz)

---

### Senaryo 2: $50 Üzeri Ücretsiz Kargo

**Hedef**: Daha yüksek sepet değerlerini teşvik etmek için ücretsiz kargo eşik.

**Çözüm Seçeneği A** (Tavsiyelidir):
- Yöntem Türü: Ücretsiz Kargo
- Min Sipariş Değeri: $50
- Gösterilecek Ad: "$50 Üzeri Siparişlerde Ücretsiz Kargo"

**Çözüm Seçeneği B** (Kurallar Kullanarak):
- Yöntem Türü: Sabit Oran
- Sabit Maliyet: $9.99
- Kargo Kuralı Oluşturun:
  - Koşul: Sepet değeri ≥ $50
  - Eylem: Maliyeti $0 yapın

---

### Senaryo 3: Ulusal + Uluslararası Ağırlık Temelli

**Hedef**: Ulusal ve uluslararası için ağırlık temelli farklı oranlar.

**Çözüm**:
1. 2 bölge oluşturun: "Ulusal", "Uluslararası"
2. 2 oran tablosu oluşturun: "Ulusal Ağırlık", "Uluslararası Ağırlık"
3. 2 yöntem oluşturun:
   - "Ulusal Kargo" → Ulusal bölge + Ulusal Ağırlık tablosu ile bağlanır
   - "Uluslararası Kargo" → Uluslararası bölge + Uluslararası Ağırlık tablosu ile bağlanır

---

### Senaryo 4: Birden Fazla Taşıyıcı Seçeneği

**Hedef**: Müşterilerin FedEx Ground, FedEx Express, UPS Ground arasında seçim yapmasına izin verin.

**Çözüm**:
1. FedEx API için Taşıyıcı Hesabı oluşturun
2. UPS API için Taşıyıcı Hesabı oluşturun
3. 3 gerçek zamanlı yöntem oluşturun:
   - "FedEx Ground" → FedEx sağlayıcısı, hizmet kodu = "FEDEX_GROUND"
   - "FedEx Express" → FedEx sağlayıcısı, hizmet kodu = "FEDEX_EXPRESS"
   - "UPS Ground" → UPS sağlayıcısı, hizmet kodu = "UPS_GROUND"
4. Tüm 3 yöntem, checkout sırasında taşıyıcı API'lerini sorgular ve canlı oranları gösterir

---

### Senaryo 5: Yerel Toplama + Teslimat

**Hedef**: Perakende mağaza hem toplama hem de teslimat seçeneklerini sunar.

**Çözüm**:
1. "Ana Mağaza" adında bir konum oluşturun, adres, saatler, hazırlama süresi ayarlayın
2. 2 yöntem oluşturun:
   - "Yerel Toplama" → Yerel Toplama türü, Ana Mağaza konumu ile bağlanır
   - "Standart Teslimat" → Sabit Oran $9.99
3. Müşteriler checkout sırasında her iki seçeneği görür

---

## Kargo Yöntemlerini Test Etme

Yaşamaya hazır olana kadar tüm yöntemleri test edin:

1. **Test Sepeti Oluşturun**
   - Farklı ağırlıklar/fiyatlarla ürünler ekleyin
   - Checkout'a gidin

2. **Her Yöntemi Test Edin**
   - Farklı bölgelere ait adresler girin
   - Doğru yöntemlerin görünür olduğundan emin olun
   - Hesaplanan maliyetlerin beklentilerinizle eşleştiğinden emin olun

3. **Kısıtlamaları Test Edin**
   - Min_order_value eşiklerine kadar ürün ekleyin → ücretsiz kargonun görünür olduğundan emin olun
   - Ağır ürünler ekleyin → ağırlık temelli katmanların çalıştığını doğrulayın
   - Bölge kısıtlamalarını test edin → dışlanan bölgelerde yöntemlerin gizlendiğinden emin olun

4. **Gerçek Zamanlı Yöntemleri Test Edin** (uygulanabilirse)
   - Taşıyıcı test kimlik bilgilerini kullanın
   - Oranların başarıyla döndürüldüğünden emin olun
   - Oran doğruluğunu taşıyıcı web sitesiyle karşılaştırın

---

## Sorun Giderme

**Sorun 1: Yöntem checkout'ta görünmüyor**

**Nedenleri**:
- Yöntem etkin değil
- Sepet min/max sipariş değerini karşılamıyor
- Sepet min/max ağırlığını karşılamıyor
- Müşteri adresi herhangi bir bağlı bölgeye uyuşmuyor
- Oran tablosu katmanları sepet ağırlığı/fiyatını kapsamlı değil

**Çözüm**: Kısıtlamaları kontrol edin, aktif durumu doğrulayın, müşteri senaryosunu kapsayan bölgeler/katmanları emin olun.

---

**Sorun 2: Gerçek zamanlı oranlar başarısız oluyor**

**Nedenleri**:
- Geçersiz API kimlik bilgileri
- Sağlayıcı hesabı etkin değil
- Tanımlanmamış kargo paketleri (taşıyıcı boyutları gerekir)
- Orjin adresi ayarlanmamış
- Taşıyıcı API'si çöküyor

**Çözüm**: Sağlayıcı bağlantısını test edin, kimlik bilgilerini doğrulayın, paketlerin yapılandırıldığını kontrol edin, ayarlardaki orjin adresini kontrol edin.

---

**Sorun 3: Yanlış maliyet hesaplandı**

**Nedenleri**:
- Oran tablosu katmanlarında boşluklar veya çakışmalar
- Katman min/max değerleri yanlış birimlerde (gram vs kg)
- Beklenmedik şekilde işlem ücreti eklendi
- Kargo kuralı maliyeti değiştiriyor

**Çözüm**: Oran tablosu katmanlarını inceleyin, birimleri doğrulayın, kargo kuralları önceliğini kontrol edin.

---

## İpuçları

- **Basitten başlayın** - İlk yöntem için sabit oran kullanın, gerekirse karmaşıklığı artırın
- **Ayrıntılı test edin** - Üretimde etkinleştirmeden önce tüm yöntemleri staging ortamında test edin
- **Açıklayıcı adlar kullanın** - "Standart Kargo (5-7 gün)" "Yöntem 1"'den daha iyi
- **Gerçekçi teslimat zamanları ayarlayın** - Müşteri memnuniyeti için azda olsa verin
- **Yerel toplama sunulabilirse** - Kargo maliyetlerini azaltır, müşteri kolaylığı sağlar
- **Taşıyıcı API'si güvenilirliğini izleyin** - Gerçek zamanlı oranlar başarısız olursa sabit oran alternatifi kullanın
- **Uluslararası için bölgeler kullanın** - Fiyatlandırma farklı bölgelere göre ayarlanabilir, pahalı hedeflerde kayıpları önler
- **Kargo kuralları ile birlikte kullanın** - Kurallar, koşullu mantık ekler (ücretsiz kargo promosyonları, uzak bölgeler için ek ücretler)
- **Yöntemleri sınırlı tutun** - Checkout'ta 2-4 seçenek, karar verme kargaşasını önler
- **Oran tablolarını mevsimsel olarak güncelleyin** - Taşıyıcı oranları değişir, yıllık olarak gözden geçirin
- **Öncelikleri akıllıca kullanın** - Ücretsiz/ucuz seçenekleri öne, pahalıları sona koyun
