---
title: Bölge Kullanılabilirliği
---

Bölge kullanılabilirliği, bir ürünün satılabileceği satış bölgelerini kontrol eder ve bu bölgelerin dışında kalan müşterilerin kataloğunu nasıl göreceğini belirler. Ürünün yalnızca belirli ülkelerde lisanslandığı, stokların yerel pazarlar için ayrıldığı ya da yeni bir ürünün bölge bazında yayımının yapıldığı durumlarda kullanılır.

Bu, **Satış Bölgeleri** üzerine kuruludur, bu da ülkeleri isimli pazarlara ayırır (bunları ayarlamak için Satış Bölgeleri rehberine bakın). Bölgeleriniz mevcutsa, bireysel ürünleri bunlara sınırlayabilir ve bu bölgelerde alamayacak olan müşterilere nasıl göründüğünü belirleyebilirsiniz.

## Belirli bölgelere ürün sınırlama

Her ürünün, düzenleme sayfasında bir **Bölge Kullanılabilirliği** ayarı vardır. **Ürünler > Tüm Ürünler**'e gidin, bir ürün seçin ve **Durum** bölümünde **Durum**, **Öne Çıkan** ve **Mağaza Arayüzünden Gizle** ile birlikte bulunsun.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-field.webp
  description: Product edit page scrolled to the Status section, with the Region availability dropdown visible and set to "Only in selected regions"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Use a product with at least 2 regions already selected below, if possible, so the inline table has visible rows in the second screenshot.
-->

| Seçenek | Ne Anlamına Gelir |
|--------|------------------|
| **Tüm bölgelerde mevcut** | Hiçbir sınırlama yok. Ürün her yerde satılıyor. Her ürün için varsayılan durumdur. |
| **Sadece seçilen bölgelerde** | Izın veren bir liste. Ürün, aşağıda seçtiğiniz bölgelerde sadece satılıyor - diğer tüm bölgelerde, mevcut değil olarak kabul ediliyor. |
| **Seçilen bölgeler hariç tüm bölgeler** | Engelleme listesi. Ürün, aşağıda seçtiğiniz bölgeler hariç her yerde satılıyor. |

### Bölgeleri seçme

Durum bölümünün altında, **Bölge Kullanılabilirliği (seçilen bölgeler)** başlıklı bir tablo, yukarıdaki modun uygulandığı bölgeleri listeler.

1. **Bölge Kullanılabilirliği**'ni **Sadece seçilen bölgelerde** ya da **Tüm bölgeler hariç** olarak ayarlayın.
2. **Bölge Kullanılabilirliği (seçilen bölgeler)** tablosunda, **Diğer Bölgeler Ekle**'ye tıklayın ve bir Satış Bölgesi seçin.
3. Eklemek istediğiniz her bölge için bu işlemi tekrar edin.
4. **Kaydet**'e tıklayın.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-inline.webp
  description: The "Region availability (selected regions)" inline table with two or three region rows added
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

**Bölge Kullanılabilirliği** **Tüm bölgelerde mevcut** olarak ayarlandıysa, bu tablodaki herhangi bir şey göz ardı edilir — bir sınırlamayı silmek için satır silmeden önce modu temizleyin.

Her ürünün bölge kurallarını içeren, birçok ürünü aynı anda incelemek için faydalı olacak, tek bir listede tüm kataloğun bölgesel görünümünü görebilirsiniz. **Ürün Bölgesi Görünürlüğü** sayfasına /admin/catalog/productregionvisibility/ adresinden gidin.

## Ürünün bölgede nakli olmayanı için şükranlar nerede gösteriliyor

Bir müşterinin bölgesi, bir ürünün kullanılabilirlik kurallarına uymuyorsa, **Stok Gösterimi Ayarları**'nda **Bölge Kullanılabilirliği** bölümünde neyin görüldüğünü kontrol edebilirsiniz. Bu sayfada henüz bir yan menü kısayolu yoktur — doğrudan /admin/catalog/stockdisplaysettings/ adresinden açın.

<!-- screenshots-needed:
- url: /en/admin/catalog/stockdisplaysettings/1/change/
  filename: stock-display-region-availability.webp
  description: Stock Display Settings change form scrolled to the "Region Availability" fieldset, showing the Region-restricted display dropdown
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Tüm markdown formatlamalarını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

| Option | Ne işe yarar |
|--------|-------------------|
| **Göster, 'Kullanılamaz' olarak işaretle** (varsayılan) | Ürün, listelerde hâlâ görünür, 'Kullanılamaz' etiketiyle ve 'Add to Cart' butonunun yerine '[bölge]'ye gitmiyor. Aynı zamanda, listeleme sayfalarının en üstünde bir banner de bulunur ('[hedef]'ye bazı ürünler gitmiyor) ve sadece oraya giden ürünleri filtrelemek için bir bağlantıya sahiptir. |
| **Listelerden kaldır** | Bu bölgeye sahip alışverişçiler için ürün, listelerden ve arama sonuçlarından tamamen kaldırılır. |

<!-- screenshots-needed:
- url: /en/products/
  filename: storefront-region-restricted-listing.webp
  description: Storefront ürün listesi, en üstte bölge bandı ve 'Kullanılamaz' etiketi ve '[bölge]'ya gitmiyor notu olan en az bir ürün kartı içermelidir
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Bir mağaza için geçerli bir sevkiyet seçimi (veya GeoIP algılama) gerektirir, demo ürününün sınırlı olduğu bir bölgeye sahip olmalıdır.
-->

Kısıtlı bir ürünün kendi sayfası, bir alışverişçinin doğrudan (örneğin, paylaşılan bir bağlantıdan veya arama motoru sonucundan) eriştiğinde her zaman '[bölge]'ya gitmiyor diye bir not gösterir — bu, yukarıda ki listede hangi seçeneği seçerseniz seçin, listeleme seçeneğine göre değişmez, çünkü doğrudan bir bağlantı listeleme sayfasını atlar.

## Alıcıların kendi bölgelerini seçmelerini veya keşfetmelerini sağlama

Spwig, bir alışverişçinin bölgesini otomatik olarak algılayabilir ve bir geçiş sunabilir, aynı zamanda alışverişçilerin her zaman kendi bölgelerini değiştirebileceği bir seçici ekleyebilirsiniz.

### Başlamadan Önce

Bölge algılama ve geçişinin doğru çalışması için iki şeye ihtiyacınız vardır:

1. **Satış Bölgeleri** — her bir bölgedeki ülkeler ve her bir regionun varsayılan dövizidir. Sidebar'da **Envanter** altında **Satış Bölgeleri** görünmüyorsa, menü bağlantısını ortaya çıkarmak için **Ayarlar > Mağaza Ayarları > E-Ticaret** altında **Çoklu Depo'yu Etkinleştir** ayarını açın (aslında çoklu depo kullanmanıza gerek yok — bu ayar sadece menü öğesini açar). Aynı zamanda doğrudan `/admin/catalog/salesregion/`'a gidebilirsiniz.
2. **Kargo Ülkeleri** — mağazanızın aslında kargo verdiğ埠 ülkeleridir. Genellikle zaten mevcut olur: bir Kargo Bölgesine eklediğiniz her ülke aynı zamanda buraya da otomatik olarak eklenir. İnceleyebilir veya manuel olarak düzenleyebilirsiniz, `/admin/shipping/shippingcountry/`'a doğrudan erişin (henüz bir sidebar bağlantısı yok). 

### Otomatik Bölge Onayı

Spwig, bir alışverişçisinin bölgesini konumundan algılar ve otomatik olarak uygular. Bu, mağazanızın varsayılan (ana) pazarından farklı bir bölgeye girerse — ve iki veya daha fazla aktif Satış Bölgesi varsa — Spwig, ona ilk ziyaretinde ona hangi bölgede olduğunu bildiren bir onay gösterir, böylece değiştirebilirler.

> **[Bölge]'ye ayarladık**
> Konumundan dolayı bunu seçtik, doğru ürünleri ve fiyatları görebileceksiniz. Yanlış mı? Ülkenizi seçin.
> Kargo: [ülke seçimi]  **[Hâlâ alışveriş yap] **

<!-- screenshots-needed:
- url: /en/
  filename: region-confirmation-modal.webp
  description: Mağaza anasayfasında "[Bölge]'ye ayarladık" onay modalı, ülke seçimi ve Hâlâ alışveriş yap butonu
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Varsayılan olmayan bir bölgeye GeoIP çözünürlüğü gerektirir ve en az 2 aktif Satış Bölgesi olmalıdır. Yerel olarak, "geo_country" cookiesini varsayılan olmayan bir ülkeye ayarlayarak simüle edin.
-->

Seçim yapmak için farklı bir ülkeyi seçmek onları hemen değiştirir. Onayı reddetmek veya **Hâlâ alışveriş yap**'a tıklamak, şu anki bölgesini korur ve bu tarayıcıda tekrar sorulmaz. Zaten varsayılan bölgesine sahip ziyaretçiler için hiçbir onay gösterilmez.

### Başlık veya Ayarlar Bölümünde Kargo Ülkesi Seçicisi Ekleme

Otomatik teklif yerine, alışverişçilerin her zaman kendi bölgelerini değiştirebileceği bir seçici eklemek istiyorsanız, **Kargo Ülkesi Seçicisi** widget'ını başlık veya ayarlar bölümünüze ekleyin.

1.

İlk olarak **Tasarım > Başlık Oluşturucusuna** (ya da **Ayağı Oluşturucusu**) gidin.

2.

Widget Kitaplığı'ndan **Gönderim Yerine Seçici** widget'ını bir satıra sürükleyin.

3.

**Kaydet**'e tıklayın.

<!-- screenshots-needed:
- url: /en/theme/header/builder/
  filename: ship-to-selector-widget-library.webp
  description: Widget Kitaplığı yan menüsü açık ve Ship-To Selector widget'ı görülebilir/belirgin şekilde gösterilen Başlık Oluşturucusu
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->


Bu widget için herhangi bir ayar gerekmez — aktif olan Gönderim Ülkeleri otomatik olarak listelenir ve bir mağaza sahibinin mevcut seçimini (ya da GeoIP ile tespit edilen ülkesini, henüz bir seçim yapmamışsa) gösterir. Farklı bir ülke seçmek, bölgeyi anında günceller ve sayfanın ürün erişimini ve fiyatlarını yeniden yükler.

Ship-To Selector'ın şu anda ayrı bir ayar formu yoktur. Dilerseniz, widget'in **Özel Yapılandırma (JSON)** alanını doğrudan düzenleyerek buton stilini (dışlama, katı ya da gölgeli) değiştirebilir ya da "Ship to" etiketini gizleyebilirsiniz.

### Bölgeye göre Para Birimi

Mağazanız birden fazla para birimini destekliyorsa (**Ayarlar > Çoklu Para Birimi** altında ayarlanır), bölgeyi değiştirmek — istek ya da Ship-To Selector aracılığıyla olsa da — o bölgenin varsayılan para birimine göre gösterilen para birimini değiştirir. Mağazanızın yalnızca bir para birimi olması ya da açıkça ikinci bir para birimi etkinleştirilmemişse, bir alışverişçi bölgeyi değiştirdiğinde para birimi değişmez.

## İpuçları

- Ürünlerinizi daha sonra ekleyeceğiniz bölgeler için bakım gerektirmediği sürece, **Bölge erişimi**'ni **Tüm bölgelerde mevcut** olarak bırakın — en basit seçenek budur.

- Küçük bir izin listesi (örneğin, bir ülkeye ilk kez tanıtılan bir ürün) için **Sadece seçili bölgelerde** kullanın ve küçük bir engelleme listesi (örneğin, ürünün lisansı olmayan bir ülkede hariç tutulması) için **Seçili bölgeler hariç tüm bölgeler**'i seçin — kurulum için gerekli satır sayısına göre hangisini seçtiğiniz önemli değildir.

- Alıcılar, olmaları gereken bir ürünün eksik olduğunu belirtiyorsa, ürünün **Bölge erişimi** ayarını ve ülkelerinin aktif bir **Satış Bölgesi** ve aktif bir **Gönderim Ülkesi** tarafından kapsayıp kapsamadığını kontrol edin.

- **Listelerden gizle**, belirli ürünlerden alamayan alışverişçiler için kataloğunuzu temiz tutar, ancak aynı zamanda bu bölgelerdeki malzeme sunumu ve arama işlemleri daha da seyrek hale gelir — alışverişçi hâlâ ödeme yapamasa da kataloglarını incelemesini sağlayacak şekilde **Göster, mevcut değil olarak işaretle** genellikle daha iyidir.

- Ship-To Selector'ı başlığa ekleyerek bölge davranışını test edin ve GeoIP tespiti sırasında bir lansman sırasında güvenip güvenemeyeceğinizi kontrol etmeden önce kendi başınıza ülkeler arasında geçiş yapın.

- Sales Region sayfasında bölgelerin öncelik değerlerini (aktif bölgeler için) bilinçli bir şekilde ayarlayın — en yüksek öncelikli aktif bölge, ülkesi tespit edilemeyen ya da hiçbir bölgeyle eşleşmeyen alışverişçiler için bir sonraki seçenektir.