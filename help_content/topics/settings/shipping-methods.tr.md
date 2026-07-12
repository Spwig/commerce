---
title: Kargo Yöntemleri
---

Kargo yöntemleri, müşteriye yönelik ve ödeme sırasında gösterilen teslimat seçenekleridir—her yöntem farklı fiyatlandırma stratejileri kullanarak kargo maliyetlerini hesaplar. Spwig, basit sabit ücretlerden karmaşık taşıyıcı tarafından hesaplanan gerçek zamanlı fiyatlandırma yöntemlerine kadar 7 farklı yöntem türü destekler. Yöntemler, minimum/maksimum sipariş değeri, ağırlık ve coğrafi bölgelere göre kısıtlanabilir. Müşteriler ödeme sırasında tercih ettikleri yöntemi seçer ve hesaplanan ücret sipariş toplamına eklenir.

Bu kılavuzu, temel sabit ücretli kargonuzdan karmaşık bölgelere göre katmanlı fiyatlandırma gibi iş modelinize uygun kargo yöntemlerini yapılandırmak için kullanın.

## Kargo Yöntemi Türleri

Spwig, farklı maliyet hesaplama mantığına sahip 7 kargo yöntemi türü sunar:

### Sabit Ücretli Kargo

**Ne Olduğunu**: Sepet içeriği, hedef veya ağırlıkdan bağımsız sabit bir ücret.

**Ne Zaman Kullanılır**:
- Tahmini kargo maliyetlerine sahip basit mağazalar
- Tek ürün türü (benzer boyut/ağırlık)
- Standart taşıyıcı oranlarıyla sadece ulusal kargo
- Ücretsiz kargo eşik promosyonları (kargo promosyonlarıyla birlikte kullanılabilir)

**Yapılandırma**:
- **Yöntem Türü** = Sabit Ücret
- **Sabit Ücret** girin (örneğin, $9.99)
- Opsiyonel: Minimum/maksimum sipariş değeri kısıtlamaları ayarlayın

**Örnek**: "Standart Kargo - $9.99" tüm ulusal siparişler için.

---

### Ücretsiz Kargo

**Ne Olduğunu**: Müşteriye ücret alınmayan kargo seçeneği.

**Ne Zaman Kullanılır**:
- Ücretsiz kargo promosyonları
- Yüksek değerli siparişler (minimum sipariş değeri ile birlikte kullanılabilir)
- Yerel toplama alternatifi
- Loyalite programı avantajları

**Yapılandırma**:
- **Yöntem Türü** = Ücretsiz Kargo
- Opsiyonel: **Minimum Sipariş Değeri** ayarlayın (örneğin, $50 üzeri ücretsiz)
- Kargo promosyonlarıyla birlikte koşullu ücretsiz kargo için iyi çalışır

**Örnek**: "$50 Üzeri Siparişlerde Ücretsiz Kargo" minimum_sipariş_değeri = $50.

---

### Ağırlık Tabanlı Kargo

**Ne Olduğunu**: Toplam sepet ağırlığına dayalı katmanlı ücret tablosundan hesaplanan ücret.

**Ne Zaman Kullanılır**:
- Değişken ağırlıklara sahip ürünler (kitaplar, donanım, market ürünleri)
- Ağırlık tabanlı taşıyıcı fiyatlandırma modelleri
- Tahmini ağırlık/maliyet oranı

**Yapılandırma**:
1. **Yöntem Türü** = Ağırlık Tabanlı
2. **Kargo Ücret Tablosu** oluşturun, basis_type = "weight"
3. **Kargo Ücret Katmanları** ekleyin (örneğin, 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Opsiyonel: Belirli bölgelere kısıtlayabilirsiniz

**Örnek**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**Nasıl Çalışır**: Sepet toplam ağırlığını hesaplar → uygun katmanı bulur → katmanın ücretini döndürür.

---

### Fiyat Tabanlı Kargo

**Ne Olduğunu**: Sepet alt toplamına dayalı katmanlı ücret tablosundan hesaplanan ücret.

**Ne Zaman Kullanılır**:
- Kargo maliyeti sipariş değerine göre değişir
- Daha yüksek sepet değerlerini teşvik etmek (daha yüksek katmanlarda dolar başına daha düşük ücret)
- Benzer fiyatlı ürünler için ağırlık tabanlı alternatif

**Yapılandırma**:
1. **Yöntem Türü** = Fiyat Tabanlı
2. **Kargo Ücret Tablosu** oluşturun, basis_type = "price"
3. **Kargo Ücret Katmanları** ekleyin (örneğin, $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Örnek**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Ücretsiz
```

**Nasıl Çalışır**: Sepet alt toplamını hesaplar → uygun katmanı bulur → katmanın ücretini döndürür.

---

### Gerçek Zamanlı Taşıyıcı Ücretleri

**Ne Olduğunu**: Ödeme sırasında taşıyıcı API'lerinden (FedEx, UPS, DHL) alınan canlı ücretler.

**Ne Zaman Kullanılır**:
- Hedefe göre değişken kargo maliyetleri
- Müşteriler için birden fazla taşıyıcı seçeneği
- Manuel ücret tabloları olmadan doğru taşıyıcı fiyatlandırması
- Karmaşık fiyatlandırma ile uluslararası kargo

**Yapılandırma**:
1. **Yöntem Türü** = Gerçek Zamanlı
2. **Sağlayıcı Hesabı** oluşturun (Ayarlar > Kargo > Sağlayıcı Hesapları)
3. Taşıyıcı API kimlik bilgilerini girin (hesap numarası, API anahtarı, gizli)
4. Sağlayıcı hesabını kargo yöntemiyle bağlayın
5. Opsiyonel: Markup yüzdesi veya sabit markup ekleyin

**Gereksinimler**:
- Aktif taşıyıcı hesabı (FedEx, UPS, DHL vb.)
- Taşıyıcıdan alınan API kimlik bilgileri
- Teslimat paketleri tanımlanmış (boyut ağırlığı hesaplaması için)

**Örnek**: "FedEx Ground" yöntemi, ödeme sırasında sepet ağırlığı, boyutları ve hedefe göre canlı FedEx ücretlerini alır.

**Nasıl Çalışır**:
1. Müşteri ödeme sırasında adresini girer
2. Sistem, orijin, hedef, paket boyutları ve ağırlığı ile taşıyıcı API'sini çağırır
3. Taşıyıcı ücret teklifini döndürür
4. Opsiyonel olarak marj uygulanır
5. Ücret müşteriye gösterilir

---

### Yerel Toplama

**Ne Olduğunu**: Müşteri, fiziksel bir konumda siparişi toplar (kargo ücreti yok).

**Ne Zaman Kullanılır**:
- Toplama sunan mağazalar
- Depo toplama seçenekleri
- Etkinlikler veya pazar stantları
- Yerel müşterilere kargo ücreti kaldırma

**Yapılandırma**:
1. **Yöntem Türü** = Yerel Toplama olarak ayarla
2. **Konum** oluştur (Ayarlar > Kargo > Konumlar)
   - Adres, çalışma saatleri, toplama kapasitesi ayarla
3. Konum(lar)ı yönteme bağla
4. Opsiyonel: Hazırlama süresi ayarla (örneğin, "2 saat içinde hazır").

**Müşteri Deneyimi**:
- Ödeme sırasında "Yerel Toplama" seçer
- Birden fazla konum varsa toplama konumunu seçer
- Kullanılabilirlik temelinde toplama tarih/saati seçer
- Sipariş hazır olduğunda bildirim alır

**Örnek**: "Mağazada Toplama - Ücretsiz" 3 mağaza konumu ile 24 saat içinde hazır.

---

### Tablo Ücretli Kargo

**Ne Olduğunu**: Ağırlık, fiyat veya miktar temelli esnek katmanlı fiyatlandırma ile gelişmiş bölge hedefleme.

**Ne Zaman Kullanılır**:
- Karma fiyatlandırma (bölge ve ağırlık temelli farklı ücretler)
- Ağırlık temelli veya fiyat temelli yöntemlerden daha fazla kontrol gerekirse
- Birden fazla fiyat faktörü (örneğin, ağırlık + hedef + miktar)

**Yapılandırma**:
1. **Yöntem Türü** = Tablo Ücreti olarak ayarla
2. **Kargo Ücreti Tablosu** oluştur
3. **basis_type** tanımla: ağırlık, fiyat veya miktar
4. Ağırlık, fiyat veya miktar temelli **Kargo Ücreti Katmanları** ekle
5. Opsiyonel: Katmanları belirli bölgeler veya ülkelere kısıtla

**Ağırlık/Fiyat Temelli ile Farkı**: Tablo ücreti, her katmanda coğrafi kısıtlamaları destekler, böylece aynı ağırlık/fiyat için farklı bölgelerde farklı ücretler olabilir.

**Örnek**:
```
A Bölgesi (Yerel):
  0-5kg: 10 $ 
  5-10kg: 15 $ 

B Bölgesi (Uzak):
  0-5kg: 18 $ 
  5-10kg: 25 $ 
```

**Nasıl Çalışır**: Sepet, temel değeri (ağırlık/fiyat/miktar) hesaplar → müşteri bölümlerine uygun katmanı bulur → katmanın ücretini döndürür.

---

## Kargo Yöntemi Yapılandırması

Tüm kargo yöntemleri bu ortak ayarları paylaşır:

### Temel Ayarlar

- **Ad**: İçerik tanımlayıcısı (müşterilere gösterilmez)
- **Gösterilecek Ad**: Ödeme sırasında müşteriye gösterilen ad (örneğin, "Standart Kargo", "Hızlı Teslimat")
- **Açıklama**: Ödeme sırasında gösterilecek isteğe bağlı yardım metni (örneğin, "3-5 iş gününde teslimat")
- **Yöntem Türü**: Yukarıdaki 7 türden biri
- **Aktif**: Yöntemi silmeden etkinleştirme/devre dışı bırakma anahtarı

### Maliyet Ayarları

- **Sabit Maliyet**: Sadece düz ücret yöntemleri için
- **Ücret Tablosu**: Ağırlık temelli, fiyat temelli, tablo ücretli yöntemler için
- **Taşıyıcı Hesabı**: Gerçek zamanlı taşıyıcı yöntemleri için
- **Vergi Sınıfı**: Kargo maliyetine vergi uygulansın mı (uygunsa)

### Kısıtlamalar

**Sipariş Değeri Kısıtlamaları**:
- **Min Sipariş Değeri**: Sipariş toplamı bu miktardan büyük veya eşitse yöntem kullanılabilir (örneğin, 50 $ üzerinde ücretsiz kargo)
- **Max Sipariş Değeri**: Sipariş toplamı bu miktardan büyükse yöntem gizlenir (örneğin, 100 $ altında düz ücret)

**Ağırlık Kısıtlamaları**:
- **Min Ağırlık**: Sipariş ağırlığı bu miktardan büyük veya eşitse yöntem kullanılabilir
- **Max Ağırlık**: Sipariş ağırlığı bu miktardan büyükse yöntem gizlenir (hafif kargo seçenekleri için yaygın)

**Coğrafi Kısıtlamalar**:
- **Kargo Bölgeleri**: Yöntemi belirli bölgelere (yerel, uluslararası, bölgesel) bağla
- Boş bölgeler = tüm adreslere erişilebilir
- Birden fazla bölge = herhangi bir eşleşen bölgeye erişilebilir

### Gelişmiş Ayarlar

- **Öncelik**: Ödeme sırasında gösterim sırası (düşük sayı = listede daha yukarı)
- **İşlem Ücreti**: Hesaplanan maliyete eklenen ekstra sabit ücret
- **Ücretsiz Kargo Eşiği**: Sipariş toplamı bu eşikten büyük veya eşitse maliyeti otomatik olarak 0 $ yap (min_order_value alternatifi)

---

## Kargo Yöntemi Oluşturma

**Adım Adım İş Akışı**:

1. **Kargo Yöntemlerine Git**
   - Ayarlar > Sepet > Kargo Yöntemlerine git
   - "Kargo Yöntemi Ekle"ye tıkla


2. **Yöntem Türünü Seçin**
   - Fiyatlandırma stratejinize göre uygun türü seçin
   - Tür, kullanılabilir maliyet yapılandırma alanlarını belirler

3. **Temel Bilgileri Yapılandırın**
   - Ad: İç referans (örneğin, "domestic_ground")
   - Görünür Ad: Müşteri odaklı (örneğin, "Ground Shipping")
   - Açıklama: Teslimat süresi (örneğin, "5-7 iş günü")

4. **Maliyet Hesaplamasını Ayarla**
   - **Dolaylı Maliyet**: Sabit maliyet girin
   - **Ağırlık/Fiyat/Tablo Maliyeti**: Tablo oluşturun (aşağıya bakın)
   - **Gerçek Zamanlı**: Sağlayıcı hesabını bağlayın
   - **Ücretsiz/Toplu Alma**: Maliyet yapılandırması gerekmez

5. **Kısıtlamalar Ekle (Opsiyonel)**
   - Min/max sipariş değeri
   - Min/max ağırlık
   - Teslimat bölgeleri

6. **Önceliği Ayarla**
   - Düşük sayılar, ödeme sırasında önce görünür
   - Önerilen sıralama: Ücretsiz (1), Yerel Toplu Alma (2), Standart (3), İkinci (4)

7. **Yöntemi Etkinleştir**
   - "Etkin"i etkinleştir = Evet
   - Kaydet

---

## Fiyatlandırma Tabloları Oluşturma

Ağırlık temelli, fiyat temelli ve tablo maliyeti yöntemleri için:

**Adım 1: Fiyatlandırma Tablosu Oluştur**
- Ayarlar > Teslimat > Fiyatlandırma Tablolarına gidin
- "Fiyatlandırma Tablosu Ekle"ye tıklayın
- **Ad** ayarlayın (örneğin, "Yurtiçi Ağırlık Seviyeleri")
- **Temel Türü** ayarlayın: ağırlık, fiyat veya miktar

**Adım 2: Seviyeler Ekle**
- "Seviye Ekle"ye tıklayın
- **Min Değer** ve **Max Değer** ayarlayın (eşleşen aralığı belirler)
- **Fiyat** ayarlayın (bu seviye için maliyet)
- Opsiyonel: Belirli bölgelere veya ülkelere kısıtla
- Seviyeyi kaydet

**Adım 3: Tüm Seviyeleri Tekrarlayın**
- Tam aralığı kapsayın (0 ile beklenen maksimum değer arasında)
- Aralıklar arasında boşluk bırakmayın (örneğin, 0-5, 5-10, 10-20, 20+)
- Son seviyede **Max Değer** için `null` kullanın (sınırsız)

**Adım 4: Teslimat Yöntemine Bağla**
- Teslimat yönteminin düzenleyin
- Aşağıdaki listeden fiyatlandırma tablosunu seçin
- Kaydet

**Örnek Ağırlık Temelli Tablo**:
```
Ad: Yurtiçi Ağırlık Seviyeleri
Temel: Ağırlık

Seviyeler:
1. Min: 0g, Max: 2000g, Fiyat: $8
2. Min: 2000g, Max: 5000g, Fiyat: $12
3. Min: 5000g, Max: 10000g, Fiyat: $18
4. Min: 10000g, Max: null, Fiyat: $25
```

---

## Ortak Teslimat Senaryoları

### Senaryo 1: Temel Yurtiçi Teslimat

**Hedef**: Tüm yurtiçi siparişler için basit $9.99 sabit maliyet.

**Çözüm**:
- Yöntem Türü: Dolaylı Maliyet
- Sabit Maliyet: $9.99
- Teslimat Bölgesi: "Yurtiçi" (sadece ülkeniz)

---

### Senaryo 2: $50 Üzeri Ücretsiz Teslimat

**Hedef**: Müşterilerin daha yüksek sepet değerlerine yönlendirilmesi için ücretsiz teslimat eşiği.

**Çözüm Seçeneği A** (Tavsiyelidir):
- Yöntem Türü: Ücretsiz Teslimat
- Min Sipariş Değeri: $50
- Görünür Ad: "Ücretsiz Teslimat (Sipariş $50+)")

**Çözüm Seçeneği B** (Kurallar Kullanarak):
- Yöntem Türü: Dolaylı Maliyet
- Sabit Maliyet: $9.99
- Teslimat Promosyonu Oluştur:
  - Koşul: Sepet değeri ≥ $50
  - Eylem: Maliyeti $0 yap

---

### Senaryo 3: Ağırlık Temelli Yurtiçi + Uluslararası

**Hedef**: Yurtiçi ve uluslararası için ağırlık temelli farklı oranlar.

**Çözüm**:
1. 2 bölge oluşturun: "Yurtiçi", "Uluslararası"
2. 2 fiyatlandırma tablosu oluşturun: "Yurtiçi Ağırlık", "Uluslararası Ağırlık"
3. 2 yöntem oluşturun:
   - "Yurtiçi Teslimat" → Yurtiçi bölge + Yurtiçi Ağırlık tablosuna bağlanır
   - "Uluslararası Teslimat" → Uluslararası bölge + Uluslararası Ağırlık tablosuna bağlanır

---

### Senaryo 4: Birden Fazla Taşıyıcı Seçeneği

**Hedef**: Müşterilerin FedEx Ground, FedEx Express, UPS Ground arasında seçim yapmasına izin verin.

**Çözüm**:
1. FedEx API için Sağlayıcı Hesabı oluşturun
2. UPS API için Sağlayıcı Hesabı oluşturun
3. 3 gerçek zamanlı yöntem oluşturun:
   - "FedEx Ground" → FedEx sağlayıcısı, hizmet kodu = "FEDEX_GROUND"
   - "FedEx Express" → FedEx sağlayıcısı, hizmet kodu = "FEDEX_EXPRESS"
   - "UPS Ground" → UPS sağlayıcısı, hizmet kodu = "UPS_GROUND"
4. Tüm 3 yöntem, ödeme sırasında taşıyıcı API'lerini sorgular ve canlı oranları gösterir

---

### Senaryo 5: Yerel Toplu Alma + Teslimat

**Hedef**: Mağaza hem toplu alma hem de teslimat seçeneklerini sunar.

**Çözüm**:
1. "Ana Mağaza" adında bir konum oluşturun (adres, saatler, hazırlama süresi ile)
2. 2 yöntem oluşturun:
   - "Yerel Toplu Alma" → Yerel Toplu Alma türü, "Ana Mağaza" konumuna bağlanır
   - "Standart Teslimat" → Dolaylı Maliyet $9.99
3. Müşteriler ödeme sırasında her iki seçeneği görür

---

## Teslimat Yöntemlerini Test Etme

Yaşamaya hazır olmadan önce tüm yöntemleri test edin:

1. **Test Cart Oluştur
   - Farklı ağırlıklar/fiyatlarla ürün ekle
   - Ödeme sürecine geç

2. **Her Yöntemi Test Et
   - Farklı bölgelerde adresler gir
   - Doğru yöntemlerin görünür olduğundan emin ol
   - Hesaplanan ücretlerin beklentilerle eşleştiğinden emin ol

3. **Kısıtlamaları Test Et
   - Min_order_value'a ulaşana kadar ürün ekle → ücretsiz kargo görünür olduğundan emin ol
   - Ağır ürünler ekle → ağırlık bazlı katmanların işlediğinden emin ol
   - Bölge kısıtlamalarını test et → dışlanan bölgeler için yöntemlerin gizlendiğinden emin ol

4. **Gerçek Zamanlı Yöntemleri Test Et** (uygulanabilirse)
   - Taşıyıcı test kimlik bilgilerini kullan
   - Dönen ücretlerin başarıyla alındığından emin ol
   - Ücretin taşıyıcı web sitesiyle uyumlu olduğundan emin ol

---

## Sorun Giderme

**Sorun 1: Ödeme sırasında yöntem görünmüyor

**Nedenleri**:
- Yöntem etkin değil
- Sepet min/max sipariş değerini karşılamıyor
- Sepet min/max ağırlığı karşılamıyor
- Müşteri adresi herhangi bir bağlı bölgeyle eşleşmiyor
- Ağırlık/fiyat için hiçbir ücret tablosu katmanı kapsamıyor

**Çözüm**: Kısıtlamaları kontrol et, etkin durumunu doğrula, bölgeler/katmanların müşteri senaryosunu kapsadığından emin ol.

---

**Sorun 2: Gerçek zamanlı ücretler başarısız oluyor

**Nedenleri**:
- Geçersiz API kimlik bilgileri
- Sağlayıcı hesabı etkin değil
- Taşıyıcı için herhangi bir sevkiyat paketi tanımlanmadı (boyutlar gerekli)
- Kaynak adresi ayarlanmadı
- Taşıyıcı API hizmeti kapalı

**Çözüm**: Sağlayıcı bağlantısını test et, kimlik bilgilerini doğrula, paketlerin yapılandırıldığından emin ol, ayarlardaki kaynak adresini kontrol et.

---

**Sorun 3: Yanlış ücret hesaplandı

**Nedenleri**:
- Ücret tablosu katmanlarında boşluklar veya çakışmalar var
- Katman min/max değerleri yanlış birimlerde (gram vs kg)
- Beklenmedik şekilde bir işlem ücreti eklendi
- Sevkiyat kuralı ücreti değiştiriyor

**Çözüm**: Ücret tablosu katmanlarını incele, birimleri doğrula, sevkiyat kampanyalarının önceliğini kontrol et.

---

## İpuçları

- **Basitten başla** - İlk yöntemin için sabit ücret kullan, gerekirse karmaşıklığı artır
- **Ayrıntılı test et** - Üretimde etkinleştirmeden önce tüm yöntemlerin staging ortamında işlediğinden emin ol
- **Açıklayıcı isimler kullan** - "Standart Kargo (5-7 gün)" "Yöntem 1"'den daha iyi
- **Gerçekçi teslimat süreleri belirle** - Müşteri memnuniyeti için az tahmin et, çok teslim et
- **Mümkünse toptan alım seçeneği sun** - Sevkiyat maliyetlerini azaltır, müşteri kolaylığını artırır
- **Taşıyıcı API güvenilirliğini izle** - Gerçek zamanlı ücretler başarısız olursa sabit ücret alternatifi sağla
- **Uluslararası için bölgeler kullan** - Farklı bölgelere göre ücretler, pahalı hedeflerde zararları önler
- **Sevkiyat kampanyalarıyla birleştir** - Kurallar koşullu mantık ekler (ücretsiz kargo kampanyaları, uzak bölgeler için ek ücretler)
- **Yöntemleri sınırlı tut** - 2-4 seçenek, ödeme sırasında karar verme korkusunu önler
- **Sezonlara göre ücret tablolarını güncelle** - Taşıyıcı ücretleri değişir, yıllık olarak incele
- **Öncelikleri akıllıca kullan** - Ücretsiz/ucuz seçenekleri ilk, pahalı olanları sona koy