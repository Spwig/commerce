---
title: Çoklu Para Birimi Kurulumu
---

Çoklu para birimi, müşterilerin tercih ettikleri para biriminde ürünleri tarayıp ödeme işlemini tamamlamasını sağlar. Fiyatlar, bağlı sağlayıcıdan veya manuel olarak tanımlanmış kur üzerinden temel para biriminizden otomatik olarak dönüştürülür.

## Başlamadan Önce

Çoklu para birimini etkinleştirmeden önce aşağıdaki öğelere ihtiyacınız vardır:

1. **Aktif bir döviz kuru sağlayıcısı** - **Ayarlar > Çoklu Para Birimi sekmesi > Döviz Kuru Paneli**'ne gidin ve en az bir sağlayıcıya (örneğin Open Exchange Rates, Fixer.io veya ExchangeRate-API) bağlanın. Sağlayıcı aktif olmalı ve kur eşitlemesi yapmalı.
2. **En az iki para birimi** - Temel para biriminiz ve desteklemek istediğiniz bir veya daha fazla ek para birimi.

## Çoklu para birimini etkinleştirme

**Ayarlar > Çoklu Para Birimi**'ne gidin ve **Çoklu Para Birimini Etkinleştir**'i seçin. Etkinleştirildikten sonra aşağıdaki seçenekleri yapılandırın:

| Ayar | Açıklama |
|---------|-------------|
| **Para Birimi Seçim Modu** | Müşterilerin para birimini nasıl seçebileceğini belirler. *Otomatik* konumlarından algılar, *Manuel* onlara bir anahtarlayıcıdan seçim yapma imkanı tanır, *Her ikisi de* iki yaklaşımı birleştirir. |
| **Para Birimi Anahtarlayıcı Görünümü** | Mağazanızda para birimi seçiciyi görüntüleyin, böylece müşteriler manuel olarak para birimini değiştirebilir. |
| **Anahtarlayıcı Konumu** | Para birimi anahtarlayıcısının nerede görüneceğini belirler (başlık, altbilgi veya yan çubuk). |
| **Döviz Kuru Bilgisi Göster** | Müşterilere fiyatların temel para biriminizden yaklaşık bir dönüştürme olduğunu bildirin. |
| **Yerel Biçimleme Etkinleştir** | Sayıları ve para birimi sembollerini her müşteri için yerel biçimlere göre biçimlendirin (örneğin Avrupa biçimleri için 1.234,56). |

## Ödeme modu

Çoklu para biriminin ödeme sırasında nasıl çalışacağını seçin:

| Mod | Açıklama |
|------|-------------|
| **Tam Çoklu Para Birimi** | Müşteriler, seçtikleri para biriminde ürünleri tarar, sepete ekler ve öder. Döviz kuru, ödeme sırasında kilitlenir ve siparişle birlikte kaydedilir. Bu varsayılan ayarıdır. |
| **Sadece Gösterim** | Müşterilerin rahatlığı için fiyatlar tercih ettikleri para biriminde gösterilir, ancak sepet ve ödeme her zaman temel para biriminizde işlenir. Ödeme sırasında, müşterilere temel para biriminizdeki gerçek ücretin yanı sıra yaklaşık dönüştürülmüş tutarı gösteren bir bildirim görülür. |

**Sadece Gösterim**, ödeme sağlayıcınız sadece temel para biriminizi destekliyorsa veya döviz kuru riskini tamamen önlemek istiyorsanız yararlıdır. Müşteriler hala yerel fiyatlarla tarayabilir, bu da kendi para birimlerinde maliyet hissi verir.

## Döviz kuru eşitleme aralığı

Mağazanızın bağlı sağlayıcısından yeni kur bilgilerini ne sıklıkta alacağını kontrol edin:

| Aralığı | Açıklama |
|----------|-------------|
| **Gerçek Zamanlı** | Her 15 dakikada bir. Yüksek hacimli uluslararası satışlar yapan mağazalar için en iyisidir. |
| **Saatlik** | Saatte bir kez. Yenilik ve API kullanımının iyi bir dengesi. |
| **Günlük** | Günde bir kez. Çoğu mağazaya uygundur. Bu varsayılan ayarıdır. |
| **Haftalık** | Haftada bir kez. Fiyatları sabit olan mağazalar için uygundur. |
| **Aylık / Çeyreklik** | Fiyatları nadiren değiştiren mağazalar için daha az sıklıkta güncellemeler. |
| **Yalnızca Manuel** | Kur bilgileri asla otomatik olarak alınmaz. Tüm kur bilgilerini manuel olarak yönetirsiniz. |

Eşitleme aralığı, arka plan görevinin sağlayıcınızdan kur bilgilerini ne sıklıkta alacağını belirler. Eşitlemeler arasında önbelleğe alınan kur bilgileri kullanılır. Anında eşitleme yapmak istiyorsanız, **Döviz Kuru Paneli** üzerindeki **Şimdi Eşitle** butonunu veya **Manuel Döviz Kurları** sayfasındaki **Sağlayıcıdan Eşitle** butonunu kullanın.

## Manuel döviz kurları

Manuel döviz kurları, belirli para birimi çiftleri için kesin dönüşüm oranlarını ayarlamanıza olanak tanır. Bu, sağlayıcıdan alınan kur oranlarına göre önceliklidir ve fiyat üzerinde tam kontrol sağlar.

**Döviz Kurları > Manuel Döviz Kurları**'na gidin ve bunları yönetin.

### Manuel olarak oran ayarlama

**Oran Ekle**'ye tıklayarak bir para birimi çifti için bir oran oluşturun. Temel para birimini, hedef para birimini ve oranı belirtin. Örneğin, USD/EUR'ı 0,92 olarak ayarlarsanız, 1 USD = 0,92 EUR anlamına gelir.

### Sağlayıcıdan eşitleme

**Sağlayıcıdan Eşitle**'ye tıklayarak bağlı sağlayıcınızın en son kur oranlarından manuel oranları otomatik olarak doldurun.

Bu, tüm desteklenen diller için el ile oranlar oluşturur ve ince ayarlamaya başlamak için bir başlangıç noktası sağlar.

Kilitli oranlar senkronizasyon sırasında atlanır, bu nedenle el ile ayarladığınız oranlar silinmez.

### Oranları kilitleme

Herhangi bir orana tıklayarak, sağlayıcı senkronizasyonu sırasında bu oranın üzerine yazılmasını önlemek için kilitleme simgesini seçin. Bu, özel bir oran müzakere ettiğinizde veya piyasa hareketlerinden bağımsız olarak sabit bir oran korumak istiyorsanız yararlıdır.

- **Kilitli** oranlar, bir kilitleme simgesi gösterir ve otomatik senkronizasyon dışındadır.
- **Kilit açılmış** oranlar, Sağlayıcıdan Senkronize'ye tıkladığınızda güncellenebilir.

### Sağlayıcı karşılaştırması

Her el ile oran, sağlayıcı oranıyla birlikte ve bir yüzde farkıyla gösterilir. Bu, el ile oranlarınızın piyasa oranlarıyla nasıl karşılaştırıldığını hızlıca görebilmenizi sağlar:

- **Yeşil** bir yüzde, oranınızın sağlayıcı oranından yüksek olduğunu gösterir.
- **Kırmızı** bir yüzde, oranınızın sağlayıcı oranından düşük olduğunu gösterir.

## Döviz kuru ekleme

Döviz kurlarına bir yüzde eklenebilir, bu da müşteri bir sipariş verdiğinde ve ödeme alındığında döviz kuru dalgalanmalarına karşı koruma sağlamak ve döviz çevirme ücretlerini karşılamak için kullanılır.

Örneğin, 1.18 USD/EUR kuru için 2% bir ekleme, bunu yaklaşık 1.20 USD/EUR yapar. Bu küçük tampon, döviz çevirilerinde para kaybetmemenizi sağlar.

## Oran seçimi stratejisi

Çok sayıda döviz kuru sağlayıcısı bağlı olduğunda, oranların nasıl seçileceğini seçebilirsiniz:

- **Ana Sağlayıcı** - Her zaman belirtilmiş ana sağlayıcınızdan gelen oranları kullanır. Bu, mağazanızdaki fiyatların tutarlılığını sağlar. Ana sağlayıcı bir para birimi çifti için veri yoksa, herhangi bir sağlayıcıdan en son mevcut oranı kullanır.
- **En Son Mevcut** - Herhangi bir aktif sağlayıcıdan senkronize edilen en yeni oranı kullanır. Bu, en güncel verileri sağlar ancak sağlayıcılar arasında oranlar hafifçe değişebilir.

Çoğu mağaza için **Ana Sağlayıcı**, en tahmin edilebilir fiyatlandırma sağlar ve önerilir.

## Desteklenen diller

Desteklediğiniz dilleri seçmek için sürükle bırak diller yöneticisini kullanın:

1. **Mevcut Diller** (sol sütun), etkinleştirebileceğiniz tüm dilleri gösterir.
2. **Aktif Diller** (sağ sütun), mağazanızda şu anda etkin olan dilleri gösterir.
3. Dilleri sütunlar arasında sürükleyerek etkinleştirme veya devre dışı bırakma işlemi yapabilirsiniz.
4. Aktif sütun içinde sürükleyerek dillerin switcher'da nasıl görüneceğini sıralayabilirsiniz.
5. Değişikliklerinizi uygulamak için **Dil Yapılandırmasını Kaydet**'e tıklayın.

Temel dili her zaman aktif tutarsınız ve kaldırılamaz.

## Döviz kurları nasıl çözülür

Bir fiyatın dönüştürülmesi gerekiyorsa, sistem şu sırayla oranları kontrol eder:

1. **El ile döviz kuru** - Eğer aktif bir el ile oran mevcutsa, bu oran her zaman ilk olarak kullanılır.
2. **Sağlayıcı oranı** - Eğer el ile oran yoksa, bağlı sağlayıcınızdan alınan en son oran kullanılır.

Bu, çoğu döviz için sağlayıcıları kullanmanıza ve özel çiftlerde el ile oranlarla hassas kontrol sağlamanıza olanak tanır.

## Önemli: Bu ayar kalıcıdır

Çok dilli mod etkin hale getirildikten sonra müşteriler yabancı dillerde sipariş verirse, bu ayar **devre dışı bırakılamaz**. Bunun nedeni:

- Siparişler müşterinin seçtiği dili ve satın alma zamanında kullanılan döviz kuru kalıcı olarak saklanır.
- Finansal raporlar ve iade hesaplamaları bu tarihî diller verisine bağlıdır.
- Çok dilli modu devre dışı bırakmak, mevcut çok dilli siparişleri tutarsız hale getirebilir.

Yabancı dillerde sipariş alınmamışsa, hala çok dilli modu devre dışı bırakabilirsiniz.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Önce küçük bir siparişle test yapın** - Yabancı bir para birimiyle test siparişi vererek ödeme akışını doğrulayın ve kur oranlarının doğru uygulandığından emin olun.
- **Döviz kurlarını düzenli olarak izleyin** - Döviz Kurları Panelini düzenli olarak kontrol ederek sağlayıcınızın kurları senkronize ettirdiğinden ve bunların mantıklı göründüğünden emin olun.
- **Değişkenlikli para birimleri için marj ekleyin** - Yüksek değişkenlik gösteren para birimlerini destekliyorsanız, marjınızı korumak için hafifçe daha yüksek bir marj (2-3%) eklemeyi düşünün.
- **Büyük para birimleriyle başlayın** - EUR, GBP, JPY, CAD ve AUD gibi yaygın kullanılan para birimleriyle başlayın ve müşteri talebine göre genişleyin.
- **Ödeme sağlayıcısı uyumluluğunu gözden geçirin** - Tüm ödeme sağlayıcıları tüm para birimlerini desteklemeyebilir.

Ödeme sağlayıcınızın belgelerini kontrol ederek hangi para birimlerini işlemelerini onaylayın.
- **Eğer emin değilse Sadece Göster modunu kullanın** - Ödeme sağlayıcınızın çok dilli ödeme işlemini desteklediğinden emin değilse, başlangıçta Sadece Göster modunu kullanın.

Daha sonra Tam Çok Dilli Para Birimi moduna geçebilirsiniz.
- **Promosyon döneminden önce kurları kilitleyin** - Bir kampanya düzenliyorsanız, kampanya sırasında fiyatların tutarlı kalmasını sağlamak için önce döviz kurlarını kilitleyin.