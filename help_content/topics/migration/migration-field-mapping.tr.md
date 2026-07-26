---
title: Alan Haritalama
---

Her platform, şeyleri biraz farklı isimlendirir — WooCommerce'un `regular_price`'i Shopify'ın `price`'ına eşit değildir ve bir CSV sütunu `barcode` olarak isimlendirilmiş olabilir ve bu da Spwig'in `sku` olarak beklediği şey olabilir. Göç asistanının 4. adımı, **Alan Haritalama**, verilerin Spwig'e nasıl aktarılacağını göreceğiniz yerdir. Bu konu, bu sayfadaki her bloğu ve WooCommerce, Shopify, Magento ve CSV göçleri için geçerlidir, platform farkları önemli olduğunda belirtilmiştir. Kimlik bilgileri ve daha önceki asistan adımları için [WooCommerce'den Göç](migrate-from-woocommerce) veya platformunuz için eşdeğer kılavuzu inceleyin.

## Otomatik Haritalamalar

Bu blok, 3. adımda seçtiğiniz veri türleri için, kaynak alanların okunabilir bir listesini ve her birinin Spwig alanına hangi şekilde aktarıldığını gösterir — örneğin bir ürünün `name` alanı Spwig'in ürün başlığına, bir müşterinin `email` alanı hesap e-postasına eşlenir. Sadece gerçekten aktarıyor olduğunuz veri türleri burada görünür; 3. adımda Gözden Geçirme'yi seçmediyseniz, bu sayfada Gözden Geçirme bölümü görünmez.

Bu satırlar okunabilir olduğundan, yapılandırmaya hiçbir şey yoktur — bunlar, aktarma işlemini onaylamadan önce haritalamayı kontrol etmeniz için vardır. Eğer bir haritalama verileriniz için yanlış görünüyorsa, bu ekrandan bunu geçersiz kılma seçeneği yoktur; seçeneğiniz, göçten önce kaynak veriyi düzeltmek ya da göç tamamlandıktan sonra Spwig'de etkilenen kayıtları düzeltmektir.

## CSV Sütun Haritalama

Bu blok sadece CSV göçleri için görünür ve yüklediğiniz her dosya için bir tablo vardır. Spwig, sütun başlıklarınızdan muhtemel eşleşmeleri otomatik olarak algılar — örneğin `sku` eşlemesi `barcode`, `part_number` veya `item_number` gibi başlıkları da tanır — bu nedenle çoğu durumda burada hiçbir şeyi değiştirmenize gerek yoktur.

Her CSV sütunu, bu dosya türü için Spwig'in beklediği alanları listeleri olan bir açılır menüye sahiptir:

- **ürünler** — `id, name, slug, description, price, sku, stock_quantity, category`
- **kategoriler** — `id, name, slug, description, parent_id`
- **müşteriler** — `id, email, first_name, last_name, phone`
- **siparişler** — `id, customer_email, order_date, status, total, currency`
- **değerlendirmeler** — `id, product_id, customer_email, rating, comment, date`

Her açılır menüde ayrıca **— Bu sütunu atla —** seçeneği vardır, bu da bu sütunun tamamen aktarımdan dışlanmasını sağlar. Başlığınız Spwig'in tanımadığı bir isimlendirme konvansiyonu kullanıyorsa veya bir sütun gerçekten Spwig'in aktarıdığı hiçbir şeye karşılık gelmiyorsa (örneğin iç not alanı gibi) — Atla seçeneğini seçin, en yakın mevcut alanı zorlamaktan kaçının.

## Özel Alanlar

Bu blok sadece WooCommerce için geçerlidir. Spwig, mağazanızdan 10 ürün, müşteri ve sipariş örneği alır ve standart WooCommerce alanları dışında bulduğu özel meta alanları listeler, tespit edilen tür ve örnek bir değer ile birlikte.

Her alan için nereye aktarılacağını seçin:

- **Harita** — Ürünler için Özel Alan 1, 2 veya 3 (Müşteriler ve Siparişler için Özel Alan 1 veya 2), veya **Meta Veri (JSON)** olarak tüm özel alanları kapsayan bir seçenek, numaralı alanlardan daha fazla özel alanınız varsa, veya bunu **— Bu alanı atla —** olarak bırakın.
- **Dönüştür** — değerin içeri aktarılırken nasıl dönüştürüleceğini belirtir: Metin olarak, Sayı (Tamsayı) olarak, Ondalık olarak, Doğru/Yanlış (Boole) olarak, JSON olarak, Tarih olarak, URL olarak veya E-posta olarak.

> **Not:** Shopify meta alanları bu özellik tarafından hiç algılanmaz — Shopify göçleri, mağazanızda ne kadar meta alan verisi olursa olsun, hiçbir zaman Özel Alanlar bloğu göstermez. Eğer ürün özelliklerini, müşteri özniteliklerini veya benzerlerini Shopify meta alanlarına bağımlıysanız, göç tamamlandıktan sonra Spwig'de bu veriyi manuel olarak yeniden girmeyi planlayın.

Eğer Spwig, örneklerinizde özel alan tespit edemiyorsa, bu blok yerine bir onay mesajı göreceksiniz ve yapılandırılacak başka bir şey yoktur.

Kaynak kategorilerinizin bazılarının Spwig'de açık bir eşleşme bulunmuyorsa, bu blok size üç seçenek sunar: **Yeni kategoriler oluştur**, **Varsayılan kategoriye atama** (tüm "Kategorisiz" ürünleri yakalayan bir "Kategorisiz" kategorisi) veya **Eşleşmeyen kategorilere sahip öğeleri atla**.

> **Not:** Burada hangi seçeneği seçersen, Spwig şu anda herhangi bir ürünün kaynak kategori verisi olduğunda otomatik olarak eşleşen bir kategori oluşturur ve yalnızca tamamen kategori bilgisi olmayan ürünler için "Kategorisiz"e geri döner. Bu seçimi çok düşünmenize gerek yok — eğer istenmeyen kategorilerle sonuçlanırsanız, içeri aktarma işlemi tamamlandıktan sonra **Katalog > Kategoriler** bölümünde bunları birleştirmek ya da silmek daha hızlıdır.

## Vergi, kargo ve fiyat ayarları

Son blok, **Vergi & Kargo Ayarları**, üç kontrol içerir: **Vergi ayarlarını içeri aktar**, **Kargo bölgelerini ve yöntemlerini içeri aktar** ve bir **Fiyat ayarı** türü ve değeri.

İki onay kutusu şu anda içeri aktarmayı etkilemez — eski platformunuzdan vergi oranları veya kargo bölgeleri, nasıl ayarlandığına bakılmaksızın gelmez. İçeri aktarma tamamlandıktan sonra Spwig'de doğrudan yapılandırın: vergi oranları **Ayarlar > Vergi & Para Birimi** altında, kargo bölgeleri ve yöntemleri **Ayarlar > Kargo** altında.

**Fiyat ayarı**, kaynak platformunuza bağlı olarak farklı davranır:

- **WooCommerce, CSV ve Shopify geçişleri** — bu kontrol yukarıda açıklanan şekilde çalışır. **Yüzde** veya **Sabit Tutar** seçin, bir değer girin (örneğin, 10% artış için `10` veya 5$ azalış için `-5`), ve her ürünün temel fiyatı bu miktar kadar içeri aktarılırken ayarlanır. Sadece temel fiyata uygulanır — indirim/ karşılaştırılabilir fiyatlar değişmeden gelir.
- **Magento geçişleri** — sayfa üzerinde aynı kontrol görünür, ancak hiçbir etkisi yoktur; Magento fiyatları, ne girerseniz girin, değişmeden içeri aktarılır. Magento geçişinde genel fiyat değişikliği gerekirse, bu alan yerine Spwig'in katalog toplu fiyat araçlarını kullanarak bunu geçişten sonra uygulayın.

> **Uyarı:** WooCommerce, CSV veya Shopify'dan geçiş yapıyorsanız ve fiyatların değişmesini istemiyorsanız, **Fiyat ayarı**'nı **Hiçbiri** olarak bırakın. Bu sayfadaki tek gerçek verinizi değiştiren kontrol budur ve yukarıda yer alan vergi ve kargo onay kutularının aynı şekilde çalıştığını yanlış varsaymak kolaydır.

## Haritalamalar, bir sonraki sefer için kaydedilir

Bu sayfada yapılandırdığınız her şey, geçiş işiyle birlikte kaydedilir ve Spwig, aynı platformdan gelecek geçişleriniz için başlangıç noktası olarak yeniden kullanır — özellikle fazla geçiş yaparsanız (önce kategoriler ve ürünler, sonra siparişler) veya veri sorunlarını düzeltip yeniden içeri aktarma yapmanız gerekirse yararlıdır. Bir geçiş tamamlandıktan sonra, geçiş panosundaki **Alan Haritalamaları** butonu üzerinden kaydedilmiş haritalamaları yeniden inceleyip ayarlayabilirsiniz, tüm sihirbazı tekrar çalıştırmadan.

## İpuçları

- **Düzenleyememenize rağmen Otomatik Haritalamalar bloğunu kontrol edin** — başlangıçta "İçe Aktar" butonuna tıklamadan önce yanlış bir haritalama yakalamanız, daha sonra yüzlerce içe aktarılmış kaydı düzeltmeye göre çok daha ucuzdur.
- **CSV başlıklarını otomatik algılama olmadan yüklemeyi denemeden yeniden adlandırın** — eşleşmeyen bir alanı aşağıya doğru açılan listeden zorla eşleştirmeye çalışmak yerine.
- **Meta Veri (JSON) özel alan taşınması olarak kullanın** — bu, iki veya üç alanın ardından tavan yapmayan tek haritalama hedefidir.
- **Vergi, kargo veya (Magento'da) fiyat için bu sayfaya güvenmeyin** — bunları içeri aktarma tamamlandıktan hemen sonra el ile yapılandırma görevi olarak ele alın, sihirbazın bunları sizin için işlemesi değil.
- **Yeni bir geçişin ilk çalıştırmasında Fiyat ayarı'ni Hiçbiri olarak bırakın**, ardından küçük bir test partisi ile matematiği onayladıktan sonra tam kataloğunuzda uygulayın.