---
title: Çoklu Para Birimi Hediye Kartları
---

Farklı ülkelerde müşterilere hizmet veriyorsanız, belirli para birimlerinde hediye kartları çıkarabilirsiniz. Örneğin, Yeni Zelanda'daki bir müşteri 50 NZD hediye kartı satın alabilir ve alıcı bu kartı NZD olarak kullanabilir — yüzey değeri döviz kuru dalgalanmalarına bakılmaksızın aynı kalır.

Bu özellik, en az bir döviz kuru sağlayıcısının yapılandırılmış olduğu durumlarda etkinleştirilmelidir.

## Nasıl Çalışır

Bir hediye kartı ürününde **Hediye Kartı Para Birimi** ayarladığınızda, sistem, satın alma sırasında mevcut döviz kuru kullanarak ürün fiyatını hedef para birimine dönüştürür. Sonuç olarak, hediye kartı o para biriminde ifade edilir ve aynı para biriminde alışveriş yapan müşteriler tarafından sadece o para biriminde kullanılabilir.

| Adım | Ne Olur |
|------|-------------|
| **Ürün Ayarları** | Ürün fiyatını temel para biriminizde ayarlar ve hedef para birimi (örneğin, NZD) seçersiniz |
| **Satın Alma** | Bir müşteri hediye kartı satın alır. Temel fiyat mevcut döviz kuru kullanılarak NZD'ye dönüştürülür |
| **Hediye Kartı Oluşturulur** | Hediye kartı, değeri NZD olarak ifade edilir (örneğin, NZ$78.50) |
| **Kullanım** | Alıcı, alışveriş sırasında NZD kullanırken kodu uygular. NZD bakiyesi düşer |

## Önkoşullar

Çoklu para birimi hediye kartlarını ayarlamadan önce aşağıdaki öğelerin mevcut olduğundan emin olun:

1. **Çoklu para birimi etkinleştirildi** — **Ayarlar > Mağaza Ayarları**'na gidin ve çoklu para birimi desteğini etkinleştirin
2. **Desteklenen para birimleri yapılandırıldı** — Sunmak istediğiniz para birimlerini ekleyin (örneğin, NZD, SGD, EUR)
3. **Döviz kuru sağlayıcısı bağlandı** — **Ayarlar > Döviz Kurları**'na gidin ve bir sağlayıcı yapılandırın, böylece canlı kurlar mevcut olur

## Çoklu Para Birimi Hediye Kartı Ürününü Ayarlama

### Adım 1: Hediye Kartı Ürünü Oluşturun veya Düzenleyin

1. **Ürünler > Tüm Ürünler**'e gidin
2. **+ Ürün Ekle**'ye tıklayın veya mevcut bir hediye kartı ürününü açın
3. **Ürün Türü**'nü **Hediye Kartı** olarak ayarlayın

### Adım 2: Hediye Kartı Para Birimini Ayarlayın

1. **Hediye Kartı** sekmesine tıklayın
2. Adet ayarlarınızı normalde gibi yapılandırın (sabit miktarlar, özel miktarlar veya her ikisi de)
3. **Hediye Kartı** sekmesinin alt kısmında, **Hediye Kartı Para Birimi** açılır menüsünü bulun
4. Hedef para birimini seçin (örneğin, **NZD - Yeni Zelanda Doları**)
5. Ürünü kaydedin

Açılır menü, mağaza ayarlarınızda etkinleştirilen tüm para birimlerini gösterir. **Mağaza temel para birimi (varsayılan)** seçiliyse, hediye kartları temel para biriminizde çıkar — bu standart davranıştır.

### Adım 3: Fiyat Ayarları

Ürün fiyatını temel para biriminizde normalde olduğu gibi ayarlayın. Bir müşteri bu hediye kartını satın alırsa, fiyat mevcut döviz kuru kullanılarak hedef para birimine otomatik olarak dönüştürülür.

**Örnek:** Temel para biriminiz USD'dir. 50 USD fiyatlı bir hediye kartı ürününü oluşturursunuz ve Hediye Kartı Para Birimi NZD olarak ayarlanmıştır. Eğer döviz kuru 1 USD = 1.57 NZD ise, sonuçta elde edilen hediye kartı NZ$78.50 değerinde olur.

## Para Birimi Eşleşmesi ve Kullanım

Çoklu para birimi hediye kartları **aynı para birimi kullanımını** kullanır — müşterinin aktif alışveriş para birimi, hediye kartının para birimiyle eşleşmelidir.

### Müşterilerin Deneyimi

- **NZD** para biriminde alışveriş yapan bir müşteri, ödeme sırasında NZD hediye kartını kullanabilir
- **USD** para biriminde alışveriş yapan bir müşteri, NZD hediye kartını kullanamaz — döviz eşleşmeme mesajını görecekler
- Müşteriler, hediye kartını kullanmadan önce mağaza ön yüzünde bulunan para birimi seçicisini kullanarak alışveriş para birimlerini değiştirebilirler

### Bakiye Nasıl Çalışır

Hediye kartı bakiyesi her zaman kendi yerel para biriminde izlenir:

- 78.50 NZD hediye kartı, başlangıçta 78.50 NZD bakiyesi ile gelir
- Eğer bir müşteri 30 NZD değerinde bir alışveriş yaparsa, kalan bakiye 48.50 NZD olur
- Bakiye döviz kurlarıyla dalgalanmaz — yüzey değeri sabittir

Hediye kartı ödeme sırasında uygulandığında, sistem, sipariş hesaplamaları için içinden temel para birimine indirgemeyi yapar, ancak hediye kartı bakiyesi her zaman kendi yerel para biriminde düşer.

## Çoklu Para Birimi Hediye Kartlarını Yönetme

**Ürünler > Hediye Kartları**'na gidin ve tüm çıkarılan hediye kartlarını görüntüleyin. Çoklu para birimi hediye kartları, kendi yerel para birimlerinde görüntülenir:

- **Bakiye**, hediye kartının para biriminde gösterilir (örneğin, NZ$48.50)
- **İşlemler**, miktarları hediye kartının para biriminde kaydeder
- **Başlangıç değeri**, satın alma zamanındaki dönüştürülmüş miktarı gösterir

### Döviz Kuru Detaylarını Kontrol Etme

Her hediye kartı işlemi, işlem sırasında kullanılan döviz kuru kaydeder. Bu, muhasebe amaçlarıyla tam bir denetim izi sağlar.

## Örnekler

### Örnek 1: Yeni Zelanda İçin Bölgesel Hediye Kartı

**Senaryo:** ABD'den çalışıyorsunuz ancak Yeni Zelanda'da müşterileriniz var. NZD ifade eden hediye kartları satmak istiyorsunuz.

| Ayar | Değer |
|---------|-------|
| Ürün adı | NZ Hediye Kartı |
| Ürün türü | Hediye Kartı |
| Fiyat | 50.00 $ (USD — temel para biriminiz) |
| Adet türü | Sabit Adetler |
| Sabit adetler | 25, 50, 100, 200 |
| Hediye Kartı Para Birimi | NZD - Yeni Zelanda Doları |
| Süre | 365 gün |

Müşteri 50 $ adet seçerse:
- Sistem, mevcut kura göre 50 $ USD'yi NZD'ye dönüştürür
- NZD eşdeğeri olan bir hediye kartı oluşturulur (örneğin, NZ$78.50)
- Alıcı, Yeni Zelanda'da alışveriş yaparken bu hediye kartını kullanabilir

### Örnek 2: Çoklu Para Birimi Hediye Kartları

**Senaryo:** Singapur, Avustralya ve Birleşik Krallık'ta müşterilere hizmet veriyorsunuz. Üç hediye kartı ürünü oluşturun:

1. **SG Hediye Kartı** — Hediye Kartı Para Birimi: SGD
2. **AU Hediye Kartı** — Hediye Kartı Para Birimi: AUD
3. **UK Hediye Kartı** — Hediye Kartı Para Birimi: GBP

Her ürün, satın alma sırasında temel fiyatın hedef para birimine dönüştürülmesini sağlar. Her bölgedeki müşteriler, kendi yerel para birimlerinde hediye kartını kullanabilir.

### Örnek 3: Karma Hediye Kartı Sunumu

**Senaryo:** Hem temel para birimi hem de bölgesel hediye kartları sunmak istiyorsunuz.

- **Mağaza Hediye Kartı** — Hediye Kartı Para Birimi: *Mağaza temel para birimi (varsayılan)* — temel para biriminde kullanılabilir
- **NZ Hediye Kartı** — Hediye Kartı Para Birimi: NZD — sadece NZD'de kullanılabilir

Her iki ürün de kataloğunuzda bir arada bulunabilir. Müşteriler, bakiye kontrol ederken hediye kartının hangi para biriminde ifade edildiğini görebilir.

## İpuçları

- İlk olarak bir bölgesel para birimiyle başlayıp (satın alma, teslimat, kullanım) tam akışı test edin, daha fazla para birimi eklemeyin.
- Satın alma zamanındaki döviz kuru, hediye kartı değerini belirler. Kurlar önemli ölçüde değişirse, hediye kartı değeri sabit kalır — bu hem sizin hem de müşterilerinizin korunmasını sağlar.
- Ürün adında para birimini açıkça belirtin (örneğin, "NZ Hediye Kartı" veya "Hediye Kartı (NZD)") böylece müşterilerin ne satın aldığını bilirler.
- Para birimi ayarlanmamış hediye kartları, temel para birimindeki işleviyle aynı şekilde çalışır — mevcut ürünler etkilenmez.
- Döviz kuru sağlayıcınızı izleyin ve kurların güncel olduğundan emin olun. Tarihi kurlar, hediye kartlarının aşırı değerli veya düşük değerli olmasına neden olabilir.
- Adetleri dikkatle seçin. 25 $ USD adet, yaklaşık NZ$39'a eşdeğerdir — hedef para birimindeki yuvarlanmış adetler daha iyi görünebilir. Hedef para birimindeki yuvarlanmış sayılarla adetleri olan ayrı ürünleri oluşturabilirsiniz.