---
title: Göçünüz Sonrası
---

Bir tamamlanmış göç, incelemenizin başlangıcıdır, değil sonu. Sihirbazın 6. adımı, neyin geçtiğini özetleyen bir araç, eski sitesine hâlâ işaret eden bağlantıları düzeltmek için bir araç ve kayıtlarınız için indirebileceğiniz bir rapor sağlar. Bu konu, göçünüzü tamamlamayı düşündüğünüzde kontrol etmeniz gerekenleri adım adım açıklar, bu da vergi, kargo ve canlıya geçiş işlerini sihirbazın kendisi yapmaz.

## Sonuçlarınızı Okuma

Tamamlanma sayfasının üst kısmında, her veri türü (Ürünler, Kategoriler, Müşteriler, Siparişler ve bunlara benzerler) için bir istatistik kartı satırı görürsünüz. Bu, ardından her çalıştırılan adımda **İçe Aktarma Özeti** tablosu ile birlikte **İçe Aktarıldı**, **Atlandı**, **Başarısız Oldu** ve **Toplam** sütunlarını içerir.

- **İçe Aktarıldı** — Spwig'de başarıyla oluşturulmuş öğeler.
- **Atlandı** — kaynak platformunuzda olan ama Spwig tarafından oluşturulmayan öğeler. Bu neredeyse her zaman beklenen bir durumdur: 3. adımda **Mevcut öğeleri atla** seçeneği açıkken, Spwig'de zaten var olan bir öğeyle (SKU, e-posta vb. ile) eşleşen her şey, çoğaltılmak yerine yalnızca bırakılır. Bir tekrar deneme sonrasında yüksek bir atlama sayısı genellikle ilk deneme zaten bu kayıtları oluşturmuş olmasından başka bir şey değildir.
- **Başarısız Oldu** — Spwig'in denemesi ve oluşturamadığı öğeler. Bu, veri sorunundan, eksik bir bağımlılıktan veya kaynak tarafında bir hata nedeniyle olabilir. Sıfırdan farklı bir başarısızlık sayısı araştırmaya değerdir; [Göç Sorun Giderme](migration-troubleshooting) konusuna bakarak günlükleri nasıl okuyacağınızı ve temizlik seçeneklerinizi neler olduğunu öğrenin.

> **Not:** Eğer herhangi bir adımda başarısızlıklar varsa, mağazanın bunları telafi ettiğini varsaymayın — bunu yapmaz. Başarısızlık öncesi ne kadar şey import edilmişse, mağazanızda başarılı olan her şeyle birlikte duruyor. Bu sonuçları normal bir kısmi sonuç gibi inceleyin.

## Bağlantı Yeniden Yazımı

Eski platformunuzdan içeri aktarılan ürünler, sayfalar ve blog gönderileri genellikle orijinal domain'lerine geri dönen bağlantılar içerir — bir resim URL'si, bir "ilgili ürün" bağlantısı, bir iç bağlantı. Spwig, içeri aktarılan içerikte bunlardan herhangi birini tespit ederse, tamamlama sayfasında **Bağlantı Yeniden Yazımı** paneli görünür.

Her tespit edilen bağlantı, geldiği sayfa veya ürün tarafından gruplandırılır ve şu şekilde gösterilir:

- **Orijinal URL** — içeri aktarılan içerikte tam olarak görünen bağlantı.
- **Önerilen URL** — Spwig'in yeni mağazanızda eşdeğer sayfayı bulduysa, önerdiği URL.
- **Eşleşme** — bu önerinin güvenilirlik yüzdesi. Herhangi bir mantıklı eşleşme olmayan bağlantılar **Hiçbiri** olarak gösterilir ve onaylamak için önerilen bir URL yoktur.

Her bağlantı için öneriyi **Onayla** veya **Atla** seçeneğini tek tek seçebilirsiniz. **Yüksek güvenilirliği otomatik onayla** seçeneği, 85% ve üzeri her öneriyi tek bir tıklamayla onaylar — zaman kazandırmak için faydalıdır, ancak sonrasında hâlâ birkaç kontrol yapmak değerlidir. 85% altında öneriler, el ile açmanızı gerektirenlerdir: 50-70% eşleşme, yanlış isim altında doğru ürün olabilir veya çok uzakta olabilir, ve bunu sadece bir insanın gözden geçirmesiyle anlamanız gerekir.

Onaylama veya atlamak sadece bir bağlantıyı işaretler — içerikteki hiçbir şey, **Onaylanan Bağlantıları Uygula**'ya tıklanana kadar değişmez. Bu, onaylanan bağlantıları bir seferde yeniden yazmak anlamına gelir. Bu nedenle, onaylamadan önce listede çalışmak, birden fazla oturumda yapılabilir ve güvenli olur.

> **İpucu:** Emin olmadığınız herhangi bir bağlantıyı **Atla** olarak bırakın, bir tahmin onaylamaktan ziyade. Daha sonra herhangi bir eski domain bağlantısını elle düzeltmek her zaman mümkündür; onlarca ürün üzerinde yanlış bir yeniden yazımın tersine çevrilmesi daha fazla iş olur.

## Verilerinizi Doğrulama

İstatistik kartlarını başlangıç noktası olarak değerlendirin, her şeyin doğru olduğuna dair kanıt olarak değil. Birkaç dakika boyunca hızlı incelemeler yapın:

- **Ürünler** — Birkaç ürün açın, özellikle varyasyonları (boyut, renk vb.) olanları ve varyasyon seçeneklerinin ve fiyatların doğru geldiğini, resimlerin eklenmiş ve mağazanın ön yüzünde görüldüğünü, sadece yönetici panelinde değil onaylayın.
- **Kategoriler** — Kategori hiyerarşisinin doğru göründüğünden emin olun, özellikle Shopify'den göç yaptıysanız, koleksiyonlar düz bir liste olarak değil, iç içe ağac olarak içe aktarılır.
- **Müşteri hesapları** — Bazı kayıtlarda e-posta ve adresleri hızlıca inceleyin.


Migre edilmiş müşteriler eski şifrelerini taşımaz — Spwig, kaynak platformdan bunu okuyamaz — bu yüzden **müşteriler ilk oturum açmaları sırasında şifrelerini sıfırlamaları gerekir**.

Çalışmaya başladığınızda bir başlangıç e-postası gönderin.
- **Siparişler** — Örnek siparişlerde toplamlar, durumlar ve satır öğelerinin eski platformda gördüğünüzle eşleştiğinden emin olun.
- **Uzantı türetilmiş ürünler** — WooCommerce'dan migre ediyorsanız, Abonelikler, Takımlar, Hediye Kartları, Bileşik Ürünler veya Rezervasyonlar gibi uzantılarla çalışıyorsanız, bunları kullandığı ürünlerin örneklerini inceleyin.

Okunamayan uzantı verileri ürünün içeriğinin aktarılmasını engellemiyor — sadece ek konfigürasyon olmadan gelir — bu yüzden bu ürünlerin çoğu el ile düzeltmeye ihtiyaç duyabilir.

## Vergi ve kargo ayarlaması

Sihirbazın 4. adımı vergi ayarlarını ve kargo bölgelerini içeri aktarma seçeneklerini kaydeder, ancak bunlar içeri aktarma işlemine uygulanmaz — onlardan vergi oranları veya kargo bölgeleri oluşturulmaz. Bu beklenen bir durumdur: **vergi ve kargo ayarlaması, veri içeri aktarımı tamamlandıktan sonra Spwig'de doğrudan tamamlanacak, yeni bir mağaza ayarlamak gibi normal ve ayrı bir adımdır**.

Aynı adımdaki **Fiyat ayarı** kontrolü istisnadır — WooCommerce, CSV ve Shopify içeri aktarımları için etkili olur, ürünün temel fiyatını oluştururken değiştirir. Eğer bir ayar belirlediniz ve fiyatlar yanlış görünüyorsa, bu değişikliğin kaynağı buradan gelir. Ayrıntılar için [Migration Field Mapping](migration-field-mapping) bölümüne bakın.

Çalışmaya başlamadan önce ayarlayın:

- Vergi oranlarınızı — [Tax Configuration](tax-configuration) bölümüne bakarak ülkeye, eyalet veya bölgeye göre oranları ve ürünlerinizin gereken muafiyetleri ayarlayın.
- Kargo bölgelerinizi ve yöntemlerinizi — [Setting Up Shipping](setup-shipping) bölümüne bakarak eski platformda müşterilerinizin kullandığı kargo seçeneklerini yeniden oluşturun.

Test ödeme sürecinden önce bunu yapın, böylece test siparişiniz gerçek toplamları yansıtır.

## Raporunuzu İndirme

Tamamlanma sayfası üç indirme seçeneği sunar:

- **PDF İndir** — biçimlendirilmiş bir özeti, iş meta verileri, adımlar başına sayım ve hata listesi, **ilk 20 hata** ile sınırlı.
- **CSV İndir** — aynı özeti, tablo biçiminde, **ilk 50 hata** ile sınırlı.
- **Günlükleri İndir** — iş için her günlük girdi, sınırsız.

Hata sayısı küçükse, PDF veya CSV yeterlidir. Çok sayıda hata olan bir migre işlemi için günlükleri indirin — üçünden sadece bu biri tam kaydı içerir, diğerleri kırpılmış bir örnektir.

> **İpucu:** Migre iş kayıtları — bunların günlükleri ve raporları da dahil — Spwig'de sonsuza kadar kalır; hiçbir şey onları bir zaman çizelgesine göre silmez. Bunları offline kayıtlar için veya admin erişimi olmayan birine paylaşmak isterseniz, kopyasını indirin, ancak bugün bunu yapmak zorunda değilsiniz.

## Çalışmaya Başlama

Verileriniz, vergi ve kargo ayarlamalarınız memnuniyet vericiyse:

1. **Ödeme sürecini baştan sonuna test edin.** Bir ürün sepete ekleyin, ödeme işlemini tamamlayın ve vergi, kargo ve ödeme hesaplanıp işlemini doğru şekilde işlediğinden emin olun, ideal olarak test modunda gerçek bir ödeme yöntemiyle.
2. **DNS'inizi sadece bu test başarılı olduktan sonra Spwig'e yönlendirmeyin.** İlk olarak DNS'i değiştirip sonra hata ayıklamayın — bu süre zarfında müşteriler kırık bir ödeme sürecine yönlendirilebilir.
3. **Eski mağazanızı, yeni mağaza siparişlerini doğru şekilde işlediğinden emin olana kadar sadece okunabilir veya "kapalı" bir hale getirin.** Bu, geçişten sonra eski platformda siparişlerin alınmasını risk etmeden bir geri dönüş noktası sağlar.

## Kaynak platform kimlik doğrulama bilgilerini iptal etme

Migre işleminin tamamlandığını doğruladığınızda ve tekrar çalıştırmayı beklemiyorsanız, kaynak platformunuza geri dönün ve onun için oluşturduğunuz API anahtarını, uygulamayı veya entegrasyonu iptal edin veya silin (bkz. [Migrating from WooCommerce](migrate-from-woocommerce) veya eşdeğer platform kılavuzunda bu kimlik doğrulama bilgisi nerede olduğunu öğrenin).


Spwig, içeri aktarma tamamlandıktan sonra eski mağazanıza sürekli erişim gerektirmez, bu yüzden onu kaldırarak artık kullanmadığınız bir kimlik bilgisi kapatmış olursunuz.

## İpuçları

- **Atlanan genellikle iyi, başarısız olan değil** — "Skip existing items on" seçeneğiyle bir tekrar sonrasında büyük miktarda atlanan sayısının olması beklenir; sıfırdan farklı bir başarısız sayısı loglara bir göz atmayı gerektirir.
- **Onaylanmış Bağlantıları Uygula"yı acele etmeyin** — onaylar ve atlamalar, Uygula'ya tıklamadan önce kolayca değişebilir, bu yüzden düşük güvenilirlikteki bağlantıları üzerinde zaman ayırın.
- **İlk canlı satışınızdan önce vergi ve kargo ayarlarını yapın**, değil de sonra — içeri aktarma bunu sizin için yapmaz ve yapılandırılmamış bir vergi oranı, müşteri tarafından yakın zamanda bir yakınma olana kadar kolayca kaçırılabilir.
- **Müşterilerinize şifre sıfırlamaları hakkında uyarı** verin, eğer mağaza geçişinden dolayı müşteri listesine e-posta gönderiyorsanız, ilk oturum açma işlemi bir sürpriz olmasın diye.
- **Hesaplamalar veya uyumluluk kayıtları için 90 günlük işaretten önce raporunuzu indirin**.
- **Eski mağazayı bir süre okunabilir şekilde tutun** — maliyeti düşüktür ve Spwig'de ilk günlerinizde bir güvenlik ağı sağlar.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-results-summary.webp
  description: İçeri aktarma tamamlanma sayfası, istatistik kartlarını ve İçeri Aktarılan/Atlanan/Başarısız/Toplam özeti tablosunu gösteriyor
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-link-rewriting.webp
  description: Bağlantı Yeniden Yazma paneli, gruplandırılmış öneriler, güvenilirlik yüzdelikleri ve Onayla/Atla/Onaylanmış Bağlantıları Uygula denetimleri
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
-->