---
title: Shopify'den Göç
---

Mağazanız şu anda Shopify üzerinde çalışıyorsa, Spwig'in göç asistanı, Shopify Ortaklar panelinde oluşturduğunuz küçük özel bir uygulama ile bağlanarak ürünleri, müşterileri, siparişleri ve içeriği içe aktarabilir. Shopify platformu çoğu platformdan daha kısıtlıdır, bu yüzden bu kılavuzun çoğu, bu uygulamayı doğru şekilde oluşturmakla ilgilidir — uygulama mevcut olduğunda bağlantı kendisi beş dakikalık bir adımdır.

## Başlamadan Önce

İki Shopify özel sınırı burada özellikle belirtmek yeterlidir, sadece daha aşağıda bir tabloda değil:

> **Önemli:** Shopify incelemeleri API'si yoktur, bu yüzden **müşteri incelemeleri hiçbir şekilde göçmez**, hangi uygulama kapsamlarını verirsenizersiniz. İncelemelerinizi ihtiyaç duyarsanız, kullandığınız inceleme uygulamasından (Judge.me, Yotpo, Loox vb.) ayrı ayrı dışa aktarın ve bunları Spwig'e kendiniz içe aktarın.

> **Önemli:** Varsayılan olarak, Spwig sadece **son 60 gün içindeki siparişleri** okuyabilir. Tüm sipariş geçmişinizi aktarmak istiyorsanız, uygulamanızı oluştururken `read_all_orders` kapsamını eklemelisiniz — aşağıda bulunan kapsam listesine bakın. Bu, uygulama hala bağlanır ve başarıyla içe aktarır olsa bile, kolayca kaçırılabilir; çünkü sadece sessizce sipariş geçmişinizin ne kadar geriye gidebileceğini sınırlar.

Diğer her şey iyi aktarılır: kategoriler (Koleksiyonlar olarak — aşağıya bakın), ürünler, görüntüler, varyasyonlar, müşteriler ve adresler, indirimler ve blog içerikleri. Özel alanlar diğer dikkat çeken boşluk — bu kılavuzun sonunda **Shopify metafield'lerine** bakın.

Ayrıca unutmayın:

- Asistanın **Vergi Ayarlarını İçe Aktar** ve **Kargo Bölgelerini ve Yöntemlerini İçe Aktar** seçenekleri, içe aktarılan verilere uygulanmaz. Spwig'de vergi oranlarını ve kargonuzu kendiniz ayarlayın — bkz. [Göçünüz Sonrası](after-migration-review).
- Aynı adımdaki **Fiyat Ayarı** seçeneği, Shopify içe aktarımları için etkili olur, her ürünün temel fiyatını oluştururken değiştirir. Her fiyatın kaydırılmasını istemiyorsanız, bunu **Hiçbiri** olarak bırakın.
- Uygulamayı oluşturmak için Shopify Ortaklar hesabına erişiminiz olmalıdır. Zaten bir tane yoksa, Shopify ücretsiz olarak bir tane oluşturmanıza izin verir: partners.shopify.com.

## Shopify Uygulamasını Oluşturma

Spwig, kendi mağazanızda oluşturduğunuz ve yüklediğiniz özel bir uygulama üzerinden Shopify'a bağlanır. Bu, ürün içindeki **Shopify API Kurulum Kılavuzu** modal'ına (asistanın 2. adımı üzerinden **Kurulum Kılavuzu'nu Aç** ile açılır) eşdeğerdir, bu yüzden aşağıda verilen adımlar tam olarak orada göreceğinizle eşleşir — herhangi birini takip edebilirsiniz.

### Adım 1: Uygulamayı Oluştur

1. [Shopify Ortaklar geliştirme paneline](https://dev.shopify.com/dashboard) gidin ve **Uygulamalar**'ı açın
2. **Uygulama Oluştur**'a tıklayın
3. **Geliştirme Panelinden Başla**'yı seçin
4. Uygulama adı: `Spwig Göç`
5. **Oluştur**'a tıklayın

![Shopify geliştirme panelinde Spwig Göç uygulaması oluşturma](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### Adım 2: Uygulama URL'sini ve kapsamları ayarla

Yeni uygulamanın yapılandırma sayfasında, **Sürümler** altında ayarlayın:

- **Uygulama URL'si**: `https://shopify.dev/apps/default-app-home`
- **Kapsamlar**: `read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![Uygulama URL'si ve gerekli kapsamları ayarlama](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| Kapsam | Spwig'in erişimini sağlar |
|---|---|
| `read_products` | Ürünler, varyasyonlar, görüntüler, koleksiyonlar |
| `read_customers` | Müşteri isimleri, e-postaları, adresler |
| `read_orders` | Son 60 gün içindeki siparişler |
| `read_content` | Blog gönderileri ve sayfalar |
| `read_discounts` | İndirim kodları ve kurallar |
| `read_files` | Yüklenebilir medya dosyaları |

> **Not:** Sadece son 60 gün değil, tamamı sipariş geçmişinizi istiyorsanız, yukarıdaki kapsam listesine `read_all_orders` ekleyin.

### Adım 3: Client ID ve Secret'ınızı kopyalayın

**Ayarlar > Kimlik Bilgileri**'ne gidin ve orada görünen **Client ID** ve **Secret**'ı kopyalayın — bunları biraz sonra Spwig asistanına yapıştıracaksınız.

![Uygulamanın Ayarlar sayfasından Client ID ve Secret kopyalama](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### Adım 4: Özel bir dağıtım bağlantısı oluşturun

1.

Go to **Dağıtım** and select **Özel dağıtım**
2.

Enter your store domain (for example, `yourstore.myshopify.com`)
3.

Click **Link oluştur**, then **Kopyala** the install link it produces

![Copying the generated custom-distribution install link](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### Step 5: Install the app on your store

Open the install link you just copied in your browser (make sure you're logged into your Shopify store admin), review the permissions it requests, and click **Yükle**.

![Installing the app on the Shopify store](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **Önemli:** Bu son adım kolayca kaçırılabilir. Install linki oluşturmak uygulamayı yüklemek anlamına gelmez — linki gerçekten açıp **Yükle**'ye tıklamak gerekir, aksi halde Spwig bağlanamayacaktır. Eğer bir sonraki bölümde bağlantı testi başarısız olursa, ilk kontrol edilecek şey bu olacaktır.

## Spwig'a Kimlik Bilgilerinizi Kopyalama

Spwig admin paneline gidin, **Veri İmportu ve İhraç > Yeni Göçü Başlat**, 1. adımda **Shopify**'i seçin ve 2. adımda aşağıdaki bilgileri girin:

- **Mağaza Alan Adı** — `yourstore.myshopify.com`
- **Müşteri Kimliği** — Ayarlar > Kimlik Bilgileri'den
- **Müşteri Gizli Anahtarı** — Ayarlar > Kimlik Bilgileri'den

Eğer bu kılavuz yerine ürün içindeki adım adım kılavuzu takip etmek isterseniz, bu adımda **Kurulum Kılavuzu'nu Aç**'a tıklayın — yukarıdaki beş adımı ve aynı ekran görüntülerini kapsar ve baştan sona yaklaşık 10 dakika sürer.

**Test etmeden devam et** seçeneğini işaretli bırakın. Eğer uygulamanızın izinlerinde `read_products`, `read_customers` veya `read_orders` eksikse, Spwig size devam etmeden önce uyarı verir — Shopify paneline gidin, uygulamanızın **Sürümler** sayfasına gidin, eksik izni ekleyin, yeni bir sürüm kaydedin ve tekrar deneyin.

## Veriyi İnceleme ve Seçme

3. adımda mağazanızdan canlı sayılar çekilir ve ilk beş ürünün bir örneği gösterilir. Diğer platformlardan bazı farklılıklar vardır:

- **Koleksiyonlar, kategoriler değil** — Shopify, ürünlerin kategorilerine göre değil koleksiyonlara göre organize edilir ve koleksiyonlar iç içe geçemez, bu nedenle hiyerarşi düz olarak aktarılır. Eğer Shopify mağazanızda koleksiyonlar kategori ağacını temsil ediyorsa, aktarımın ardından Spwig'in kategori yöneticisinde bu yapıyı yeniden oluşturmanız gerekir.
- **İndirimler, kuponlar değil** — Shopify'in indirim kodları ve kuralları Spwig indirimleri olarak aktarılır.
- **Değerlendirmeler satırı yok** — Shopify'da değerlendirme API'si olmadığı için bu veri türü bu adımda hiç görünmez, WooCommerce veya CSV aktarımlarıyla karşılaştırıldığında.

**İmport Seçenekleri**, diğer platformlarda olduğu gibi çalışır: **Mevcut öğeleri atla** (açık) SKU ve e-postaya göre eşleşir, yinelenmeleri önlemek için; **Ürün resimlerini aktar** (açık) daha yavaş ama önerilir; **Orijinal kimlikleri mümkün olduğunca koru** (kapalı) değiştirilmemeli, özel bir nedeniniz varsa aksi halde; **Toplu boyut** 25'e varsayılan olarak ayarlanır.

## Shopify Meta Alanları

Shopify meta alanlarını ürünler, müşteriler veya siparişlerde ek veri depolamak için kullanıyorsanız, Spwig bunları tespit etmez veya okumaz — WooCommerce ile farklı olarak, Shopify aktarımları için özel alan haritalama adımı yoktur. Meta alanlarında sakladığınız herhangi bir veriyi, aktarımın ardından Spwig'de [özel alanlar](migration-field-mapping) kullanarak manuel olarak yeniden girmeniz gerekir, bu nedenle aktarımın başlamadan önce Shopify'dan meta alanlarını ve değerlerini içeren bir liste çıkartmak faydalı olabilir.

## Aktarımla Göçü Başlatma

3. adımı inceledikten sonra aktarıma başlayın. Arka planda çalışır — tarayıcı penceresini kapatın ve devam eder. 5. adımda her veri türü için bir satır ve genişletilebilir aktivite günlüğüyle canlı ilerleme gösterilir.

6. adımda sonuçlarınızı görürsünüz: ne aktarıldı, atlandı veya başarısız oldu, ayrıca içeriğinizde eski `myshopify.com` alan adına yapılan iç bağlantılar bulunursa, **Bağlantı Yeniden Yazma** aracı gösterilir.

Gönderimden sonra özetleri dikkatle inceleyin, ardından [After Your Migration](after-migration-review) başlığındaki kontrol listesini tamamlayın — bu, verilerinizi doğrulamak, koleksiyon hiyerarşisini yeniden inşa etmek, vergi oranlarını ve kargo ayarlarını (sihirbaz bunları size yapılandırmaz) ayarlamak ve metaalanlarda saklanan herhangi bir şeyi tekrar girmek konularını kapsar.

## Shopify'dan Uygulamayı Silin

Gönderimin başarıyla tamamlandığını doğruladıktan sonra Shopify admin panelinin **Uygulamalar** sayfasına veya Ortaklar paneline gidin ve Spwig Migration uygulamasını silin (veya en azından mağazanızdan kaldırın). Gönderim tamamlandıktan sonra mağaza verilerinize okuma erişimi aktif kalmasına gerek yoktur.

## İpuçları

- **Sipariş geçmişi varsayılan olarak sınırlıdır** — daha önceki 60 günden fazla sipariş geçmişine ihtiyacınız varsa, yüklemeniz gereken bağlantı linkini oluşturmadan önce `read_all_orders` kapsam listesine ekleyin, sonrasında değil.
- **Değerlendirmeler ayrı bir dışa aktarma gerektirir** — bu, gönderimden önce planlamalısınız çünkü sihirbazla değerlendirmeleri hiçbir şekilde aktarmanız mümkün değildir.
- **Bağlantı linki oluşturmak, uygulamanın yüklenmesiyle aynı şey değildir** — her zaman 5. Adımı tamamlayıp "Yükle"yi tıklayın, aksi takdirde Spwig'de bağlantı testi başarısız olur.
- **Koleksiyonlar düz olarak gelir** — kategori yapısı navigasyon veya SEO için önemliyse, gönderimden sonra Spwig'de hiyerarşiyi yeniden inşa etmek için zaman ayırın.
- **Önce metaalanları dışa aktarın** — Spwig bunları okuyamaz, bu yüzden daha sonra ihtiyaç duyarsanız, gönderimden önce Shopify'dan bu verileri alın.
- **Doğrulama tamamlandıktan sonra uygulamayı silin** — eski mağazanıza yönelik canlı entegrasyonu, artık kullanmıyorsanız bırakmayın.