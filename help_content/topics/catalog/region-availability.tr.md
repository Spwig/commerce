---
title: Bölge Kullanılabilirliği
---

Bölge kullanılabilirliği, bir ürünün satılabileceği satış bölgelerini kontrol eder ve bu bölgelerin dışında kalan müşterilerin kataloğunu nasıl göreceğini belirler. Ürünün yalnızca belirli ülkelerde lisanslı olması, stokların yerel pazarlar için ayrılmış olması veya yeni bir ürünün bölge bazında dağıtımı sırasında bu özelliği kullanabilirsiniz.

Bu, **Satış Bölgeleri** üzerine kuruludur, bu da ülkeleri isimli pazarlara ayırır (bunları ayarlamak için Satış Bölgeleri rehberine bakın). Bölgeleriniz var olduktan sonra, bireysel ürünleri bunlara sınırlayabilir ve bu bölgelerde alıcı olamayan müşterilere nasıl göründüğünü kararlaştırabilirsiniz.

## Belirli bölgelere ürün sınırlama

Her ürünün, düzenleme sayfasında bir **Bölge Kullanılabilirliği** ayarı vardır. **Ürünler > Tüm Ürünler**'e gidin, bir ürün seçin ve **Durum** bölümünde **Durum**, **Öne Çıkan** ve **Mağaza Arayüzünden Gizle** ile birlikte bulunsun.

![Ürün düzenleme formunun Durum bölümü, **Bölge Kullanılabilirliği** menüsünün "Sadece seçili bölgelerde" olarak ayarlandığını ve **Öne Çıkan** ve **Mağaza Arayüzünden Gizle** ile birlikte olduğunu gösterir](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| Seçenek | Ne anlama gelir |
|--------|---------------|
| **Tüm bölgelerde mevcut** | Herhangi bir sınırlama yok. Ürün her yerde satılıyor. Her ürün için varsayılan durumdur. |
| **Sadece seçili bölgelerde** | Bir izin listesi. Seçtiğiniz bölgelerde sadece ürün satılıyor - diğer tüm bölgelerde, ürün mevcut değil olarak kabul ediliyor. |
| **Seçili bölgeler hariç tüm bölgeler** | Bir engel listesi. Seçtiğiniz bölgeler hariç tüm bölgelerde ürün satılıyor. |

### Bölgeleri seçme

Durum bölümünün altında, **Bölge Kullanılabilirliği (seçili bölgeler)** başlıklı bir tablo, yukarıdaki modun uygulandığı bölgeleri listeler.

1. **Bölge Kullanılabilirliği**'ni **Sadece seçili bölgelerde** veya **Seçili bölgeler hariç tüm bölgeler** olarak ayarlayın.
2. **Bölge Kullanılabilirliği (seçili bölgeler)** tablosunda, **Diğer Bölgeler Ekle**'e tıklayın ve bir Satış Bölgesi seçin.
3. Eklemek istediğiniz her bölge için bu işlemi tekrar edin.
4. **Kaydet**'e tıklayın.

![**Bölge Kullanılabilirliği (seçili bölgeler)** inline tablosu, North America ve Europe satırları eklendi](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

**Bölge Kullanılabilirliği** **Tüm bölgelerde mevcut** olarak ayarlandıysa, bu tablodaki herhangi bir şey dikkate alınmaz — bir sınırlamayı silmek için önce modu temizleyin.

Her ürünün bölge kurallarını içeren, bir liste halinde tüm kataloğun bir görünümünü görmek için, `/admin/catalog/productregionvisibility/` adresindeki **Ürün Bölgesi Görünürlüğü**'ne gidin.

## Ürünün sevki olmayan bölgelerde nasıl göründüğünü gösterme

Bir müşterinin bölgesi, bir ürünün kullanılabilirlik kurallarına uymuyorsa, **Stok Gösterim Ayarları**'nda **Bölge Kullanılabilirliği** bölümünde neyin görüneceğini kontrol edebilirsiniz. Bu sayfa şu anda bir yan menü kısayağına sahip değildir — doğrudan `/admin/catalog/stockdisplaysettings/` adresinden açın.

![Stok Gösterim Ayarları, Bölgesel Kullanılabilirlik bölümü — Bölgesel sınırlı gösterim menüsünü, "Göster, mevcut değil olarak işaretle" olarak ayarlayın](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| Seçenek | Müşterilerin gördüğü |
|--------|-------------------|
| **Göster, mevcut değil olarak işaretle** (varsayılan) | Ürün listelerde hâlâ görünür, "Mevcut değil" etiketiyle ve "[Bölge]’ye sevki yok" notuyla birlikte Sepete Ekle butonunun yerine. Listeleme sayfalarının en üstünde "[Hedef]’e sevki yok olan bazı ürünler" banner’ı da bulunur ve sadece oraya sevki olan ürünleri filtrelemek için bir bağlantıya sahiptir. |
| **Listelerden gizle** | Bu bölgedeki müşteriler için ürün, listeleme ve arama sonuçlarından tamamen kaldırılır. |

![Avrupa'ya sevki olan mağaza ürün listesi — grid’in en üstünde "Avrupa'ya sevki yok olan bazı ürünler" banner’ı ve "Avrupa'ya sevki yok" etiketli bir ürün kartı](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

Bir ürünün kendi sayfası, bir alışverişçi doğrudan (örneğin, paylaşılan bir bağlantıdan veya arama motoru sonucundan) ulaştığında, bu ürün [bölge] 'ye götürülmemektedir. Bu, yukarıdaki listeden hangi listeleme seçeneğini seçerseniz seçin, çünkü doğrudan bağlantı listeyi tamamen atlar. 

## Alıcıların kendi bölgelerini seçmelerini veya keşfetmelerini sağlama

Spwig, bir alıcının bölgesini otomatik olarak tespit edip bir geçiş sunabilir ve alıcıların her zaman kendi bölgelerini değiştirebileceği bir seçici ekleyebilirsiniz.

### Başlamadan önce

Bölge tespiti ve geçişinin doğru çalışması için iki şeyin ayarlanmış olması gerekir:

1. **Satış Bölgeleri** — her bir bölgedeki ülkeler ve her bir regionun default dövizidir. Sidebar'da **Envanter** altında **Satış Bölgeleri** 'ni görmezseniz, menü bağlantısını ortaya çıkarmak için **Ayarlar > Mağaza Ayarları > E-Ticaret** altında **Çoklu Depo'yu Etkinleştir** 'i açmanız gerekir (bunu asla kullanmanıza gerek yok — bu ayar sadece menü öğesini açar). /admin/catalog/salesregion/ adresine doğrudan gidebilirsiniz.
2. **Kargo Ülkeleri** — mağazanızın gerçekten kargo verdiğiniz ülkelerdir. Genellikle zaten mevcuttur: bir Kargo Bölgesine eklediğiniz her ülke aynı zamanda buraya da otomatik olarak eklenir. İnceleyebilir veya manuel olarak düzenleyebilirsiniz. /admin/shipping/shippingcountry/ adresine doğrudan gidin (henüz bir sidebar bağlantısı yok).

### Otomatik Bölge Onayı

Spwig, bir alıcının bölgesini konumundan tespit eder ve otomatik olarak uygular. Bu, mağazanızın varsayılan (ana) pazarından farklı bir bölgede olmalarına rağmen, iki veya daha fazla aktif Satış Bölgesi varsa, Spwig, ilk ziyaretinde onlara hangi bölgede olduklarını ve değiştirebileceklerini bildirmek için bir onay gösterir:

> **Bölgenizi [Bölge] olarak ayarladık**
> Konumunuza göre bunu seçtik, doğru ürünleri ve fiyatları görebilmeniz için. Yanılsamak mı? Ülkenizi seçin.
> Kargo: [ülke seçici]  **[Hâlâ alışveriş yap]**

![Mağaza arayüzünde "Bölgenizi Kuzey Amerika olarak ayarladık" onay modalı, "Kargo: " ülkesi seçici ve "Hâlâ alışveriş yap" butonu ile birlikte](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Seçim yapmak için farklı bir ülke seçmek, onları hemen değiştirir. Onayı reddetmek veya **Hâlâ alışveriş yap** 'a tıklamak, şu anki bölgesini korur ve bu tarayıcıda tekrar sorulmaz. Zaten varsayılan bölgesinde olan ziyaretçiler için hiçbir onay gösterilmez.

### Başlık veya Ayak Kismına Kargo Ülkesi Seçici'si Ekleme

Bir alıcının her zaman kendi bölgesini değiştirebileceği (otomatik isteklere yalnızca güvenmeyi tercih etmek yerine), başlık veya ayak kısmina **Kargo Ülkesi Seçici'si** widget'ını ekleyin.

1. **Tasarım > Başlık Oluşturucu** 'a (ya da **Ayak Oluşturucu** ) gidin.
2. Widget Kütüphanesi'nden **Kargo Ülkesi Seçici'si** widget'ını bir satıra sürükleyin.
3. **Kaydet** 'e tıklayın.

![Widget Kütüphanesi'nde "Mağaza" grubu vurgulanmış ve alışveriş sepeti, hesap menüsü ve dil seçici'si ile birlikte Kargo Ülkesi Seçici'si widget'ını gösteren Başlık Oluşturucu](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

Widget için herhangi bir ayar gerekmez — aktif Kargo Ülkelerini otomatik olarak listeler ve bir alıcının şu anki seçimini (veya henüz bir tane seçmemişse GeoIP tarafından tespit edilen ülkesini) gösterir. Başka bir ülke seçmek, bölgesini hemen değiştirir ve sayfanın ürün erişimini ve fiyatlarını yeniden yükler.

Kargo Ülkesi Seçici'si için ayrı bir ayar formu henüz yoktur. **Özelleştirilmiş Yapılandırma (JSON)** alanını doğrudan düzenleyerek buton stilini (dış hat, katı veya gölgeli) değiştirebilir ya da "Kargo et" etiketini gizleyebilirsiniz. `button_style` ve `show_label` kullanın.

### Bölgeye Göre Döviz

Mağazanız birden fazla döviz destekliyorsa (Ayarlar > Çoklu Döviz altında), bölgeyi değiştirme — istek aracılığıyla ya da Kargo Ülkesi Seçici'si aracılığıyla — o bölgenin varsayılan dövizine göre gösterilen dövizi değiştirir.

Mağazanızda yalnızca bir para birimi varsa ya da ikinci birini açıkça etkinleştirmemişse, alışverişçi bir bölgeye geçtiğinde para birimi değişmez.

## İpuçları

- Ürünü belirli bir nedenden ötürü sınırlamak istemiyorsanız, **Bölge erişimini** **Tüm bölgelerde mevcut** olarak bırakın - daha sonra bölgeler eklediğinizde hiçbir bakım yapmanıza gerek kalmaz.
- Küçük bir izin listesi (örneğin, bir ülke için ilk kez lansman gereken bir ürün) için **Sadece seçili bölgelerde** kullanın ve küçük bir engelleme listesi (örneğin, ürün lisanslı olmadığı bir ülke hariç tüm bölgeler) için **Seçili bölgeler hariç tüm bölgeler** - kurulum için daha az satır gerektirenini seçin.
- Alışverişçilerin, görünür olmalı olan bir ürünün eksik olduğunu bildirdiğini fark ederseniz, ürünün **Bölge erişimini** ayarını ve ülkelerinin aktif bir **Satış Bölgesi** ve aktif bir **Kargo Ülkesi** tarafından kapsayıp kapsamadığını kontrol edin.
- **Listelemeden kaldır** ifadesi, bazı ürünlerden alamayan alışverişçiler için kataloğunuzu temiz tutar, ancak aynı zamanda o bölgelerde pazarlama ve arama sonuçlarının daha seyrek görüneceği anlamına gelir. Alışverişçi, ödeme yapamasa da kataloğunu tamamıyla incelemesini istiyorsanız, **Göster, erişilebilir değil**, genellikle daha iyidir.
- Yeni bir lansman sırasında GeoIP algılamasına güvenmeden önce kendi başınıza ülkeler arasında geçiş yaparak **Gönderilecek Yer Seçicisi**ni header'a ekleyin.
- Bölgelerin优先lık değerlerini (Satış Bölgeleri sayfasında) bilinçli bir şekilde ayarlayın - en yüksek öncelikli etkin bölge, ülkesi algılanamayan ya da hiçbir bölgeyle eşleşmeyen alışverişçiler için bir sonraki adımdır.