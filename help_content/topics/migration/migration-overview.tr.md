---
title: Veri Göçü Genel Bakış
---

Ürünleriniz, müşterileriniz ve siparişleriniz şu anda WooCommerce, Shopify veya Magento'da — veya sadece birkaç CSV dosyasında — ise göç aracı, bunları yeni Spwig mağazanıza taşıyarak elle tekrar girmenize gerek kalmaz. Kategoriler, ürünler, müşteriler, siparişler, incelemeler ve kuponları işler ve WooCommerce için blog içeriğini de taşıyabilir, ve bir köprü eklentisiyle affiliate programınızı da taşıyabilir.

**Sistem Gösterge Paneli > Veri İmport/Export** altında admin yan çubuğunda bulunur (kendi barındırılan kurulumlarda süper kullanıcılar için görünür; görünmüyorsa kurulumunuzu yöneten kişiye sorun). **Veri İmport & Export** başlıklı sayfa, Toplam Göçler, Tamamlandı, Devam Ediyor ve Başarısız olmak üzere her bir göçün istatistik kartlarını listeler ve **Yeni Göç Başlat**, **Günlükleri Görüntüle** ve **Alan Haritalamaları** düğmelerini içerir. Göçler yalnızca sihirbaz aracılığıyla oluşturulabilir.

## Desteklenen platformlar

Spwig, üç platforma doğrudan bağlanabilir, ayrıca düz CSV dosyalarına da:

- **WooCommerce** — en kapsamlı yol; uzantı verileri (abonelikler, paketler, hediye kartları, rezervasyonlar) ve affiliate programınız da aktarılabilir.
- **Shopify** — Shopify geliştirici panelinde oluşturduğunuz özel bir uygulama aracılığıyla bağlanır.
- **Magento 2** — Magento admin panelinizden alınan entegrasyon tokenı aracılığıyla bağlanır.
- **CSV dosyaları** — beş ayrı dosya (ürünler, kategoriler, müşteriler, siparişler, incelemeler), diğer platformlar veya elle hazırlanmış veriler için.

> **Not:** BigCommerce, PrestaShop, Squarespace ve Wix doğrudan bağlantı olarak desteklenmez. Bu platformlardan birinden geçiyorsanız, kataloğunuzu ve müşteri verilerinizi CSV'ye aktarın ve bunun yerine CSV yoluyla kullanın — bkz. [CSV Dosyalarından İmport](csv-import).

## Platformlara Göre Aktarım

Platforma göre kapsama değişiklikler olabilir — lansman tarihinizi onaylamadan önce bu tabloyu kendi mağazanızla karşılaştırın.

| Veri | WooCommerce | Shopify | Magento 2 | CSV |
|---|---|---|---|---|
| Kategoriler | Evet, hiyerarşiyle | Evet, Koleksiyonlar olarak (düz) | Evet | Evet |
| Ürünler | Evet | Evet | Evet | Evet (gerekli dosya) |
| Ürün resimleri | Evet | Evet | Evet | Hayır |
| Variantlar | Evet | Evet | Evet | Hayır |
| Müşteriler + adresler | Evet | Evet | Evet | Evet |
| Siparişler | Evet | Evet, ancak `read_all_orders` kapsamı eklenebilir | Evet | Evet |
| Incelemeler | Evet | Hiç desteklenmiyor | Genellikle kullanılamıyor — Magento Community, incelemeler için REST uç noktası yok | Evet |
| Kuponlar / indirimler | Evet | Evet | Evet | Hayır |
| Blog / CMS içeriği | Evet (gönderiler, kategoriler, etiketler, resimler) | Evet (makaleler) | Evet (CMS sayfaları) | Hayır |
| Affiliate'ler, komisyonlar, ödemeler | Evet, Spwig Göç Köprü Eklentisi gerekir | Hayır | Hayır | Hayır |
| Özel alan algılama | Evet | Hayır — Shopify metafield'ları okunmaz | Hayır | n/a |

Shopify mağazaları, import sonrası metafield verilerini (özel ürün özellikleri, ek müşteri alanları) elle girmeyi planlamalıdır, çünkü bu veriler algılanmaz veya aktarılmaz. Diğer her şey için, kaynak alanlarının Spwig alanlarına nasıl haritalandığını görmek için [Göç Alan Haritalaması](migration-field-mapping) bölümüne bakın.

## Göçünüzü Planlaması

- **Yaşamaya başlamadan önce göç yapın**, Spwig kurulumunuz henüz gerçek trafiği işlememektedir ve domain'inizin DNS'sini ona yönlendirmeden — bu şekilde müşterilerin bir tamamlanmamış katalogu görmesine engel olabilirsiniz.
- **Eski mağazanızı okunur şekilde açık tutun**, Spwig kopyasının doğru olduğundan emin olana kadar.
- **Vergi ve kargo ayarları için zaman ayırın** — sihirbazın bu ayarları, oranlarınızı ve bölgelerinizi import etmeye benzer, ancak uygulanmaz (bkz. [Göç Alan Haritalaması](migration-field-mapping)). Kendiniz **Ayarlar > Vergi & Para Birimi** ve **Ayarlar > Kargo** ayarlarını yapılandırın.
- **Örneklemek yerine gözden geçirmeyi planlayın** — uzantı verileri en iyi çaba temelinde import edilir; uzantı verileri okunamayan bir ürün hala oluşturulur, ancak bunlar olmadan. Müşterilere herhangi bir şey duyurmadan önce [Göçünüz Sonrası](after-migration-review) bölümüne bakın.

- **Kaynak platformunuza admin erişimi** API kimlik bilgileri oluşturmak için — WooCommerce'da bir REST API anahtarı, Shopify'da özel bir uygulama veya Magento'da bir entegrasyon tokenu.

CSV için gerekli değil.
- **Sadece okunabilir kapsamlar**, kaynak platformunun bunları sunması durumunda — Spwig, eski mağazanızdan sadece okur, asla geri yazmaz.
- **Zaman bütçesi** — her çalıştırma, 4 saatlik sert bir limitle çalışır.

Büyük bir mağaza için, bir seferde değil, fazlalıklarla (önce kategoriler ve ürünler, sonra siparişler) planlayın.

> **Önemli:** Spwig, sihirbazda girdiğiniz API kimlik bilgilerini şifrelemiyor. Göç doğrulandıktan sonra, kaynak platformda kimlik bilgisini iptal edin veya silin.

## Göç sihirbazı, adım adım

Sihirbazda altı adım vardır, bunlar arasında ilerleme kaydedilir:

1. **Platform** — WooCommerce, Shopify, Magento veya CSV İçe Aktarma seçin.
2. **Bağlantı** — kimlik bilgilerini girin, önce bağlantı testi yapma seçeneği (varsayılan olarak etkin). Platforma özel kılavuzlar, oluşturmanız gereken şeyi tam olarak açıklar.
3. **Önizleme** — kaynak mağazanızdan canlı sayılar, ilk 5 ürünün bir örneği ve hangi veri türlerinin dahil edileceğini seçmek için onay kutuları, toplu işlem boyutu gibi seçenekler.
4. **Haritalama** — kaynak alanlarının Spwig alanlarına nasıl haritalandığı, WooCommerce özel alanları ve eşleşmeyen kategoriler. Detaylı bilgi için [Göç Alan Haritalama](migration-field-mapping).
5. **İçe Aktarma** — arka planda çalışır; sekme kapatılabilir ve işlem devam eder, canlı bir günlük kaydı ile.
6. **Tamamlandı** — sonuç özeti, eski domaininize işaret eden içerikler için bağlantı yeniden yazma aracı ve PDF/CSV rapor indirme seçenekleri.

## Göçünüzden sonra

Başarılı bir içe aktarma, hedef çizgisi değildir — [Göçünüzden Sonra](after-migration-review) tam bir kontrol listesi için, veri doğrulama, hâlâ eski domaininize işaret eden iç bağlantıların düzeltimi ve sihirbazın sizin için işlemeyen vergi ve kargo yapılandırması konularını inceleyin.

## Geri alma, güvenlik ağı değil

Başlamadan önce bunu anlayın, bir şey yanlış gider sonra değil. Geri alma mevcuttur, ama bunun bir geri alma butonu gibi görünmesi gibi değil:

- Bir içe aktarma kısmen başarısız olursa, otomatik geri alma yoktur. Başarısızlık öncesinde içe aktarılan veri mağazanızda kalır ve başarısız bir içe aktarma admin'den geri alınamaz — kısmi veriyi elle inceleyip temizlemeniz gerekir.
- Tamamlanmış bir göç geri alınabilir ve geri alma yalnızca içe aktarmanın kendisinin oluşturduğu veriyi kaldırır — asla daha fazlasını değil. İçe aktarmadan sonra gerçek bir sipariş vermiş taşınan bir müşterinin hesabı, adresleri, sadakat geçmişi ve mağaza kredisi korunur ve o gerçek sipariş dokunulmadan bırakılır; yalnızca içe aktarmanın oluşturduğu siparişler kaldırılır. Herhangi bir sipariş, paket, hediye kartı veya yapılandırıcı yuvası tarafından hâlâ referans verilen taşınan bir ürün de korunur ve diğer müşterilere ait siparişler asla değiştirilmez.
- İçe aktarmanın oluşturduğu Affiliate'ler, komisyonlar ve ödemeler, içe aktarmanın oluşturduğu affiliate hesaplarıyla birlikte kaldırılır — zaten var olan bir müşteriye bağlı bir affiliate hesabını korur, yalnızca affiliate kaydı gider. Mağaza uzantıları tarafından oluşturulan abonelik planları, fiyatlandırma katmanları ve rezervasyon kaynakları hâlâ kaldırılmaz — bunları elle temizleyin.
- Onaylamadan önce Spwig, tam olarak neyin kaldırılacağını ve neyin korunacağını, ada ve sayıya göre, nedeniyle birlikte gösteren bir önizleme sunar — bu, canlı verilerinize göre hesaplanır. Onaylamadan önce okuyun. Geri alma ardından arka planda çalışır, bu yüzden sekmeyi kapatmak güvenlidir; tamamlandığında raporu görmek için göçün özetini kontrol edin.
- Geri alma, kaldırdığı satırlar üzerinde hâlâ kalıcı ve yıkıcı bir eylemdir, bu yüzden bilinçli kullanın — ve Spwig'in koruduğu ama gerçekten istemediğiniz her şeyi elle temizleyin. Ancak artık içe aktarmanın oluşturduğunun ötesine geçmediği için, eskiden olduğu gibi yalnızca aynı gün kullanılabilecek bir araç değildir.
- Göç tamamlandıktan sonra, iş kaydı var olduğu sürece Geri Alma butonu mevcuttur ve bir geri alma denemesinin kendisi yarıda başarısız olursa tekrar sunulur, böylece tekrar deneyebilirsiniz. Kayıtlar herhangi bir takvime göre silinmez, bu yüzden bu durum kendiliğinden sona ermez.

Eğer başarısız veya takılı bir göçle karşılaşırsanız, [Göç Sorun Giderme](migration-troubleshooting) tekrar deneme, iptal etme ve günlükleri okuma konularını kapsar.

## İpuçları

- **Küçük bir test çalışmasıyla başlayın** — kategoriler ve birkaç ürün, katalogun tamamı aktarılmadan önce alan eşlemesinin doğru olduğundan emin olur.
- **Platforma özel kılavuza önce bakın** — [Migrating from WooCommerce](migrate-from-woocommerce), [Migrating from Shopify](migrate-from-shopify) ve [Migrating from Magento](migrate-from-magento), tam olarak hangi kimlik bilgileri ve kapsamların gerektiğini kapsar.
- **Yukarıdaki yetenek matrisini atlamayın** — Shopify incelemeleri veya CSV varyasyonları, DNS değiştirdikten sonra bir sürpriz olur.
- **Kaynak platformunuzun yönetici panelini başka bir sekmede açık tutun** — kimlik bilgilerini oluştururken veya kopyalarken kullanışlı olur.
- **Sihirbazın onay kutularını harfiyen alın** — burada bir ayarın işe yaradığı belirtilmemişse, Spwig'de doğrudan yapılandırın, sihirbazı güvence altına almayın.