---
title: Çoklu Para Birimi Hediye Kartları
---

İkinci ülkelere müşterilerinize hizmet veriyorsanız, belirli para birimlerinde hediye kartları çıkarabilirsiniz. Örneğin, Yeni Zelanda müşterisi 50 NZD değerinde bir hediye kartı satın alabilir ve alıcı bu kartı NZD olarak kullanabilir — döviz kuru dalgalanmalarına rağmen yüz değeri değişmez.

Bu özellik, en az bir döviz kuru sağlayıcısı yapılandırılarak çoklu para birimi özelliğinin etkinleştirilmesi gerektirir.

> **Hediye kartı satışları geçici olarak duraklatılmıştır** — otomatik teslimat akışını tamamladığımızda bu konuda **Hediye Kartları** yardım konusunu inceleyin. Şu anda bir ürün üzerinde **Hediye Kartı Para Birimi** yapılandırabilirsiniz, böylece satışlar yeniden başlatıldığında hemen satıma sunulur. Ayrıca bugün manuel olarak bir para birimi özel kartı çıkarabilirsiniz, bu şekilde herhangi bir diğer hediye kartı gibi (kartın **Başlangıç Değeri**'ni istenen para biriminde ayarlayarak).

## Nasıl Çalışır

Bir hediye kartı ürününde **Hediye Kartı Para Birimi** ayarladığınızda, sistem ürün fiyatını satın alma sırasında mevcut döviz kuru kullanarak hedef para birimine dönüştürür. Sonuç olarak hediye kartı, o para biriminde değerlendirilir ve aynı para biriminde alışveriş yapan müşteriler tarafından sadece kuponlanabilir.

| Adım | Ne Olur |
|------|-------------|
| **Ürün Ayarı** | Ürün fiyatını temel para biriminizde ayarlar ve hedef para birimi (örneğin, NZD) seçersiniz |
| **Satın Alma** | Müşteri hediye kartını satın alır. Temel fiyat mevcut döviz kuru kullanılarak NZD'ye dönüştürülür |
| **Hediye Kartı Oluşturuldu** | Hediye kartı, değeri NZD olarak (örneğin, NZ$78.50) verilir |
| **Kuponlama** | Alıcı, NZD alışveriş yaparken kupon kodunu kasanın yanında uygular. NZD bakiyesi düşer |

## Önkoşullar

Çoklu para birimi hediye kartlarını ayarlamadan önce aşağıdaki öğelerin mevcut olduğundan emin olun:

1. **Çoklu para birimi etkin** — **Ayarlar > Mağaza Ayarları**'na gidin ve çoklu para birimi desteğini etkinleştirin
2. **Desteklenen para birimleri yapılandırılmış** — sunmak istediğiniz para birimlerini ekleyin (örneğin, NZD, SGD, EUR)
3. **Döviz kuru sağlayıcısı bağlanmış** — **Ayarlar > Döviz Kurları**'na gidin ve bir sağlayıcı yapılandırın, böylece canlı kurlar mevcut olur

## Çoklu Para Birimi Hediye Kartı Ürününü Ayarlama

### Adım 1: Hediye Kartı Ürünü Oluşturun veya Düzenleyin

1. **Ürünler > Tüm Ürünler**'e gidin
2. **+ Ürün Ekle**'ye tıklayın veya mevcut bir hediye kartı ürününü açın
3. **Ürün Türü**'nü **Hediye Kartı** olarak ayarlayın

### Adım 2: Hediye Kartı Para Birimini Ayarlayın

1. **Hediye Kartı** sekmesine tıklayın
2. Adet ayarlarını normal şekilde yapılandırın (sabit miktarlar, özel miktarlar veya her ikisi de)
3. **Hediye Kartı** sekmesinin alt kısmında, **Hediye Kartı Para Birimi** açılır menüsünü bulun
4. Hedef para birimini seçin (örneğin, **NZD - Yeni Zelanda Doları**)
5. Ürünü kaydedin

Açılır menü, mağaza ayarlarınızda etkin olan tüm para birimlerini gösterir. **Mağaza temel para birimi (varsayılan)** seçildiğinde, hediye kartları temel para biriminizde çıkar — bu standart davranıştır.

### Adım 3: Fiyat Ayarları

Ürün fiyatını temel para biriminizde normal şekilde ayarlayın. Müşteri bu hediye kartını satın alırsa, fiyat mevcut döviz kuru kullanılarak hedef para birimine otomatik olarak dönüştürülür.

**Örnek:** Temel para biriminiz USD'dir. 50 USD fiyatlı bir hediye kartı ürünü oluşturursunuz ve Hediye Kartı Para Birimi'ni NZD olarak ayarlarsınız. Eğer döviz kuru 1 USD = 1.57 NZD ise, sonuç olarak hediye kartı NZ$78.50 değerinde olur.

## Para Birimi Eşleşmesi ve Kuponlama

Çoklu para birimi hediye kartları, **aynı para birimi kuponlama** kullanır — müşterinin aktif alışveriş para birimi, hediye kartının para birimiyle eşleşmelidir.

### Müşterilerin Deneyimi

- **NZD** para biriminde alışveriş yapan bir müşteri, kasanın yanında bir NZD hediye kartı uygulayabilir
- **USD** para biriminde alışveriş yapan bir müşteri, bir NZD hediye kartı uygulayamaz — döviz eşleşmeyi açıklayan bir mesaj görecektir
- Müşteriler, hediye kartını uygulamadan önce mağaza ön yüzünde bulunan para birimi seçicisini kullanarak alışveriş para birimlerini değiştirebilir

### Bakiye Nasıl Çalışır

Hediye kartı bakiyesi her zaman kendi yerel para biriminde izlenir:

```python
# Örnek: Hediye kartı bakiyesi
balance = 78.50  # NZD

# Kuponlama işlemi
if gift_card_currency == "NZD" and shopping_currency == "NZD":
    balance -= 10.00  # 10 NZD harcanır
else:
    print("Para birimi eşleşmiyor")
```

Hediye kartı bakiyesi her zaman kendi yerel para biriminde izlenir. Kuponlama sırasında, müşteri alışveriş para birimi hediye kartı para birimiyle eşleşiyorsa, bakiye düşer. Aksi takdirde, müşteriye para birimi eşleşmeyi açıklayan bir mesaj gösterilir.

- Bir NZ$78.50 liralık hediye kartı, başlangıçta NZ$78.50 bakiyesiyle gelir
- Eğer bir müşteri NZ$30 değerinde bir alışveriş yaparsa, kalan bakiye NZ$48.50 olur
- Bakiye döviz kuru değişimleriyle değişmez — nominal değer sabittir

Hediye kartı ödeme sırasında uygulandığında, sistem indirimi kendi temel para biriminize göre içinde hesaplamalar için dönüştürür, ancak hediye kartı bakiyesi her zaman kendi yerel para biriminde düşer.

## Çoklu para birimi hediye kartlarını yönetme

**Ürünler > Hediye Kartları** menüsüne giderek tüm verilen hediye kartlarını görüntüleyin. Çoklu para birimi hediye kartları, kendi yerel para birimlerinde gösterilir:

- **Bakiye**, hediye kartının para biriminde gösterilir (örneğin, NZ$48.50)
- **İşlemler**, hediye kartının para birimindeki tutarları kaydeder
- **Başlangıç değeri**, satın alma zamanındaki dönüştürülmüş tutarı gösterir

### Döviz kuru detaylarını kontrol etme

Her hediye kartı işlemi, işlem yapıldığı zaman kullanılan döviz kuru kaydeder. Bu, muhasebe amaçlı tam bir denetim izi sağlar.

## Örnekler

### Örnek 1: Yeni Zelanda için bölgesel hediye kartı

**Senaryo:** ABD'den çalışıyorsunuz ancak Yeni Zelanda'da müşterileriniz var. Yeni Zelanda doları (NZD) ile belirtilmiş hediye kartları satmak istiyorsunuz.

| Ayar | Değer |
|-----|-----|
| Ürün adı | NZ Hediye Kartı |
| Ürün türü | Hediye Kartı |
| Fiyat | $50.00 (USD — temel para biriminiz) |
| Nominal tür | Sabit Nominal Değerler |
| Sabit nominal değerler | 25, 50, 100, 200 |
| Hediye Kartı Para Birimi | NZD - Yeni Zelanda Doları |
| Süre | 365 gün |

Müşteri $50 nominal değerini seçtiğinde:
- Sistem $50 USD'yi mevcut kura göre NZD'ye dönüştürür
- NZD eşdeğeri olan bir hediye kartı oluşturulur (örneğin, NZ$78.50)
- Alıcı, alışveriş sırasında NZD ile kullanabilir

### Örnek 2: Çoklu para birimi hediye kartları

**Senaryo:** Singapur, Avustralya ve Birleşik Krallık'ta müşterilerinize hizmet veriyorsunuz. Üç hediye kartı ürünü oluşturun:

1. **SG Hediye Kartı** — Hediye Kartı Para Birimi: SGD
2. **AU Hediye Kartı** — Hediye Kartı Para Birimi: AUD
3. **UK Hediye Kartı** — Hediye Kartı Para Birimi: GBP

Her ürün, satın alma zamanında temel fiyatın hedef para birimine dönüştürülmesiyle oluşturulur. Her bölgedeki müşteriler, kendi yerel para biriminde hediye kartını kullanabilir.

### Örnek 3: Karma hediye kartı teklifi

**Senaryo:** Hem temel para birimi hem de bölgesel hediye kartları sunmak istiyorsunuz.

- **Mağaza Hediye Kartı** — Hediye Kartı Para Birimi: *Mağaza temel para birimi (varsayılan)* — temel para biriminde kullanılabilir
- **NZ Hediye Kartı** — Hediye Kartı Para Birimi: NZD — sadece NZD'de kullanılabilir

Her iki ürün de kataloğunuzda bir arada bulunabilir. Müşteriler, hediye kartının hangi para biriminde belirtilmiş olduğunu bakiye kontrol ederken görebilir.

## İpuçları

- İlk olarak bir bölgesel para birimiyle başlayarak (satın alma, teslimat, kullanım) tam akışı test edin, daha sonra diğer para birimlerini ekleyin.
- Satın alma zamanındaki döviz kuru, hediye kartı değerini belirler. Eğer kur önemli ölçüde değişirse, hediye kartı değeri sabit kalır — bu hem sizin hem de müşterilerinizin korunmasını sağlar.
- Ürün adında para birimini açıkça belirtin (örneğin, "NZ Hediye Kartı" veya "Hediye Kartı (NZD)") böylece müşterilerin ne satın aldığını bilirler.
- Para birimi ayarlanmamış hediye kartları, temel para birimindeki işlevleriyle aynı kalır — mevcut ürünler etkilenmez.
- Döviz kuru sağlayıcınızı izleyin ve oranların güncel olduğundan emin olun. Tarihinden eski oranlar, hediye kartlarının aşırı değerli veya düşük değerli görünmesine neden olabilir.
- Nominal değerlerinizi dikkatle seçin. $25 USD nominal değeri yaklaşık NZ$39'a eşdeğerdir — hedef para birimindeki yuvarlanmış nominal değerler daha iyi görünebilir. Hedef para biriminde yuvarlanmış sayılarla nominal değerler içeren ayrı ürünler oluşturabilirsiniz.