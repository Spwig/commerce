---
title: CDN Kurulumu
---

A Content Delivery Network (CDN) stores copies of your store's images, stylesheets, and scripts on servers around the world. When a customer visits your store, these files are served from the server closest to them rather than from your main hosting server. This reduces page load times, especially for customers located far from where your store is hosted.

Spwig already optimizes static asset delivery out of the box with Brotli and gzip pre-compression, fingerprinted asset caching with 1-year immutable headers, and proper content negotiation. Adding a CDN is optional, but it can further improve speed for stores with an international customer base.

## Does Your Store Need a CDN?

Not every store benefits equally from a CDN. Use these guidelines to decide:

**A CDN is recommended if**:
- Your customers are spread across multiple countries or continents
- Your store features many product images or media-heavy pages
- You want the fastest possible page load times worldwide
- You sell to regions far from your hosting server (e.g., server in Europe, customers in Asia)

**A CDN is likely unnecessary if**:
- Your customers are mostly local or within the same country as your server
- Your store has a small catalog with few images
- Your hosting provider already includes a built-in CDN

When in doubt, a CDN does not hurt performance. Services like Cloudflare offer free tiers, so there is no cost to try.

## How Spwig Works with CDNs

Spwig is CDN-ready by default. You do not need to change any code or settings inside your Spwig admin panel. Here is what Spwig already does for you:

- **Fingerprinted static files** -- Every CSS, JavaScript, and image file includes a unique version hash in its filename. This means CDNs can safely cache these files for a long time without serving outdated content.
- **Long-lived cache headers** -- Static assets are served with 1-year immutable cache headers, telling CDNs and browsers to cache them aggressively.
- **Pre-compressed files** -- Spwig pre-compresses assets using Brotli and gzip, so your CDN can deliver smaller files without extra processing.
- **Proper content negotiation** -- Spwig sends the correct content-type and encoding headers that CDNs rely on for proper caching.

All you need to do is point your domain's DNS to the CDN provider, and everything works automatically.

## Setting Up Cloudflare

Cloudflare is the most popular CDN and offers a free tier that works well for most stores. Follow these steps:

**Step 1: Create a Cloudflare Account**
- Visit cloudflare.com and sign up for a free account

**Step 2: Add Your Domain**
- Click **Add a Site** and enter your store's domain name
- Select the **Free** plan (sufficient for most stores)

**Step 3: Update Your DNS Nameservers**
- Cloudflare will show you two nameservers (e.g., `anna.ns.cloudflare.com`)
- Log in to your domain registrar (where you purchased your domain)
- Replace your current nameservers with the Cloudflare nameservers
- DNS changes can take up to 24 hours to take effect

**Step 4: Configure SSL/TLS**
- In the Cloudflare dashboard, go to **SSL/TLS**
- Set the encryption mode to **Full (strict)**
- This ensures all traffic between Cloudflare and your server stays encrypted

**Step 5: Verify It Is Working**
- Once DNS propagates, visit your store and check for the `cf-cache-status` header in your browser (see Verifying Your CDN below)

## Setting Up AWS CloudFront

If you already use Amazon Web Services, CloudFront integrates naturally with your infrastructure:

1. Open the **CloudFront** console in your AWS account
2. Create a new **Distribution** with your store's domain as the origin
3. Set the **Origin Protocol Policy** to "HTTPS Only"
4. Under **Cache Behavior**, set **Cache Policy** to "CachingOptimized" for static assets
5. Add your store's domain as an **Alternate Domain Name (CNAME)**
6. Attach an SSL certificate from AWS Certificate Manager
7. Update your domain's DNS to point to the CloudFront distribution URL

CloudFront fiyatlandırması kullanım temelli olup, çoğu mağazada maliyetler minimumdur çünkü Spwig'in parmak izli (fingerprinted) varlıkları uzun süreli önbelleğe alınır.

## Önerilen CDN Ayarları

En iyi sonuçlar için CDN'inizi doğru içeriği önbelleğe alacak şekilde ve geri kalanları atlayacak şekilde yapılandırın.

**Önbelleğe alınacaklar** (statik varlıklar):
- `/static/` -- Tüm stiller, betikler, fontlar ve tema varlıkları
- `/media/` -- Ürün resimleri ve yüklenebilir medya dosyaları
- Görüntü dosyaları (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- Font dosyaları (`.woff`, `.woff2`)

**Önbelleğe alınmaması gerekenler** (dinamik sayfalar):
- `/admin/` -- Yönetici paneli her zaman taze içerik sunmalıdır
- `/cart/` -- Sepet sayfaları oturum özel veri içerir
- `/checkout/` -- Ödeme sayfaları güvenlik nedeniyle asla önbelleğe alınmamalıdır
- `/accounts/` -- Müşteri hesap sayfaları özel veri içerir
- Oturum gerekli veya kişiselleştirilmiş içerik gösteren herhangi bir sayfa

**Genel önbellekleme kuralları**:
- **Kaynak önbellekleme başlıklarını saygılı olun** -- Spwig, her içerik türü için doğru cache-control başlıklarını gönderir. CDN'inizi bu başlıkları geçersiz kilmek yerine onları saygılı olacak şekilde yapılandırın.
- **Brotli sıkıştırmasını etkinleştirin** -- Hem Cloudflare hem de CloudFront Brotli desteği sunar. Spwig'in önceden sıkıştırılmış varlıklarından faydalanmak için bunu etkinleştirin.
- **Tarayıcı Önbellekleme TTL'sini "Mevcut Başlıkları Saygılı Ol" olarak ayarlayın** -- Bu, Spwig'in yerleşik önbellekleme politikasının davranışını belirlemesine olanak tanır.

## CDN'inizi Doğrulama

Ayarlamadan sonra CDN'inizin içeriklerinizi doğru şekilde sunup sunmadığını doğrulayın:

**Adım 1: Tarayıcı Geliştirici Araçlarını Açın**
- Chrome veya Firefox'ta **F12** tuşuna basarak geliştirici araçlarını açın
- **Ağ** sekmesine tıklayın

**Adım 2: Mağazanızı Yükleme**
- Geliştirici araçları açıkken mağazanızın anasayfasını ziyaret edin
- Herhangi bir statik dosya isteğine tıklayın (örneğin, bir `.css` veya `.js` dosyası)

**Adım 3: Yanıt Başlıklarını Kontrol Edin**
- **Cloudflare**: `cf-cache-status` başlığını arayın. `HIT` değeri, dosyanın CDN önbelleğinden sunulduğunu gösterir. `MISS` değeri, dosyanın sunucunuzdan alınmış olduğunu (yalnızca ilk istek) gösterir.
- **CloudFront**: `x-cache` başlığını arayın. `Hit from cloudfront` değeri, CDN ile sunulduğunu onaylar.

**Adım 4: Başka Bir Konumdan Test Edin**
- gtmetrix.com veya webpagetest.org gibi ücretsiz araçları kullanarak mağazanızı farklı coğrafi konumlardan test edin
- CDN kurulumu öncesi ve sonrası yükleme sürelerini karşılaştırın

## Yaygın Sorunlar

### Tema Değişikliklerinden Sonra Taze İçerik Olmaması

**Sorun**: Temanızı güncelledikten veya tasarım değişikliklerinden sonra müşteriler hâlâ eski sürümü görür.

**Çözüm**: CDN önbelleğini temizleyin. Cloudflare'de **Önbellekleme > Yapılandırma > Tümünü Temizle**'ye gidin. CloudFront'te `/*` için bir **Geçersizleştirme** oluşturun. Spwig'in parmak izli varlıklarının genellikle bu sorunu önlemesine dikkat edin çünkü güncellenmiş dosyalar otomatik olarak yeni dosya isimleri alır. Bu sorun genellikle parmak izli olmayan varlıklar gibi özel yükleme dosyalarında görülür.

---

### Karma İçerik Uyarıları

**Sorun**: CDN'i etkinleştirdikten sonra tarayıcınız "karma içerik" hakkında bir güvenlik uyarısı gösterir.

**Çözüm**: CDN'inizin SSL modunun **Tam (sıkı)** olarak ayarlandığından emin olun, "Esnek" mod değil. Esnek mod, sunucunuzun HTTPS yerine HTTP isteklerini almasına neden olabilir ve bu da karma içerik uyarılarına yol açabilir. Cloudflare'de **SSL/TLS > Genel Bakış**'ı kontrol edin ve modu doğrulayın.

---

### Yönetici Paneli Yavaş Çalışıyor

**Sorun**: CDN ekledikten sonra yönetici paneli daha yavaş hissediliyor.

**Çözüm**: CDN, yönetici sayfalarını önbelleğe almalıdır. Cloudflare'de bir **Sayfa Kuralı** veya CloudFront'te bir **Önbellekleme Davranışı** oluşturun ve `/admin/*` ile eşleşen tüm URL'ler için önbellekleme "Geç" olarak ayarlayın. Bu, yönetici isteklerinin CDN ağırlığı olmadan doğrudan sunucunuza yönlendirilmesini sağlar.

---

### Görüntüler Yüklenmiyor

**Sorun**: CDN kurulumundan sonra ürün resimleri veya medya dosyaları hatalar döndürüyor.

**Çözüm**: CDN'inizin kökeninin doğru protokol (HTTPS) ve port ile yapılandırıldığını kontrol edin. Ayrıca sunucunuzun güvenlik duvarının CDN'in IP aralıklarından gelen bağlantıları izin verdiğinden emin olun.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Cloudflare'ın ücretsiz planıyla başlayın** -- Bu, çoğu mağazanın ihtiyaçlarını karşılar ve kurulum sadece birkaç dakika sürer
- **Her zaman Full (strik) SSL modunu kullanın** -- Esnek mod güvenlik açıklarına neden olabilir ve ödeme sürecini bozabilir
- **Temanızda büyük güncellemeler yaptıktan sonra CDN önbelleğini temizleyin** -- Spwig'in parmak izli dosyaları çoğu durumu ele alsa da, tam bir önbellek temizliği eski içeriklerin kalmamasını sağlar
- **Ödeme veya sepet sayfalarını önbellekleme** -- Bu sayfaların önbelleklenmesi, bir müşterinin verilerinin başka bir müşteriye açılmasına neden olabilir
- **Müşterilerinizin konumlarından test edin** -- webpagetest.org gibi ücretsiz araçları kullanarak, müşterilerinizin alışveriş yaptıkları bölgelerden gerçek dünya performansını ölçün
- **CDN analitiklerinizi izleyin** -- Hem Cloudflare hem de CloudFront, önbellek vurum oranlarını, kaydedilen bant genişliğini ve ülkeye göre trafiği gösteren paneller sunar
- **CDN'e geçiş sırasında DNS TTL'nizi düşük tutun** -- CDN'e geçiş sırasında DNS TTL'yi 300 saniye (5 dakika) olarak ayarlayın ve her şeyin düzgün çalıştığını onayladıktan sonra artırmak suretiyle artırın
- **Bir CDN, iyi bir hosting'i değiştirmez** -- Dinamik sayfalar gibi ödeme, sepet ve yönetici sayfaları için kök sunucunuz hâlâ önemlidir

Kaliteli hosting'i bir CDN ile birlikte seçin