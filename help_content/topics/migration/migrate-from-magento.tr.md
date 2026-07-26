---
title: Magento'dan Göç
---

Spwig, Magento 2 veya Adobe Commerce mağazasından doğrudan REST API kullanarak kataloğunuzu, müşterilerinizi, siparişlerinizi, kuponlarınızı ve CMS sayfalarınızı içe aktarabilir. Bu kılavuz, entegrasyon kimlik doğrulama bilgilerinin nasıl oluşturulacağını, göç asistanının nasıl çalıştırılacağını ve Magento'dan gelen ticari firmaların planlaması gereken önemli bir eksikliği: ürün incelemelerini açıklayacaktır.

Yalnızca **Magento 2 ve Adobe Commerce** desteklenir. Magento 1, yıllar önce yaşam döngüsü sonuna ulaştı ve bu göç işlemi için gereken REST API'yi sunmaz — hâlâ Magento 1 üzerindeyseniz, bunun yerine [CSV Dosyalarından İçe Aktarma](csv-import) kullanın.

## Başlamadan Önce

[Veri Göçü Genel Bakış](migration-overview) kılavuzunu genel planlama rehberi için inceleyin. Magento için özel olarak:

- **Kategoriler** — hiyerarşileri olduğu gibi içe aktarılır.
- **Ürünler** — içe aktarılır, resimler de dahil.
- **Müşteriler ve adresler** — içe aktarılır.
- **Siparişler** — içe aktarılır.
- **Kuponlar** — Spwig kuponları olarak içe aktarılır, Magento satış kurallarından kaynaklanır.
- **CMS Sayfaları** — Spwig sayfaları olarak içe aktarılır.
- **İncelemeler** — genellikle **içe aktarılmaz**. Bu konuda daha fazla bilgi almak için bir sonraki bölümü inceleyin.
- Yapılandırılabilir ürünler için varyantlar desteklenir.

> **Not:** Magento göçleri, ortaklık programlarını, komisyonları veya ödemeleri taşımaz — Spwig'ın ortaklık köprüsü entegrasyonu yalnızca WooCommerce mağazaları için mevcuttur.

### İnceleme Sınırlaması

Magento Community Edition, ürün incelemeleri için bir REST uç noktasını sunmaz — bir stok Community kurulumunda `/reviews` rotası basitçe mevcut değildir. Spwig, bunu içe aktarma öncesi kontrol eder ve eğer orada değilse, bir mesaj kaydeder ve işin geri kalanını tamamlar, tüm görevi başarısız kılma yerine. Kategorileriniz, ürünleriniz, müşterileriniz, siparişleriniz, kuponlarınız ve sayfalarınız hâlâ geçerlidir; yalnızca incelemeler atlanır.

İncelemeler, mağazanız **Adobe Commerce** (bu uç noktayı sunar) çalışıyorsa veya Magento kurulumunuzda uyumlu incelemeler rotası ekleyen özel bir modül varsa **içe aktarılacaktır**.

Magento Community üzerindeyseniz ve Spwig'de incelemelerinizi istiyorsanız, onları ayrı olarak dışa aktarın (çoğu inceleme uzantısı CSV dışa aktarma sunar) ve daha sonra [CSV Dosyalarından İçe Aktarma](csv-import) içindeki incelemeler dosyasını kullanarak, `product_id` ile ürünlerinize göre onları içe aktarın.

## Adım 1: Magento'ı Seçin

**Veri İçe Aktarma & Dışa Aktarma** göç panelinden, **Yeni Göç Başlat**'a tıklayın ve platform olarak **Magento**'ı seçin.

## Adım 2: Mağazanıza Bağlanın

Magento mağazanızın URL'sine ve bir entegrasyon erişim token'ına ihtiyacınız olacaktır. Magento admin, bazı platformlar gibi basit bir API anahtarı vermez — bir **Entegrasyon** oluşturursunuz, bu, bir bağlı uygulama gibi davranan, kapsamlandırılmış bir kimlik doğrulama bilgisi olan bir şeydir.

### Entegrasyon Erişim Token'ı Oluşturma

1. Magento admin panelinizde **Sistem > Entegrasyonlar**'a gidin.
2. **Yeni Entegrasyon Ekle**'ye tıklayın.
3. Adı `Spwig Göç` olarak ayarlayın, böylece daha sonra kolayca tanımlayabileceksiniz.
4. **API** sekmesini açın ve **Kaynak Erişimi**'ni **Tümü** olarak ayarlayın.
5. **Kaydet**'e tıklayın, ardından **Etkinleştir**'e tıklayın.
6. İzinlerin listelendiği pop-up penceresinde **İzin Ver**'e tıklayarak onaylayın.
7. Etkinleştirme sonrası gösterilen erişim token'ını kopyalayın — Magento yalnızca bir kez gösterir.

> **Not:** Kaynak Erişimi **Tümü** olarak ayarlanmıştır çünkü Magento'nun kaynak ağacı çok ince granülerdir — katalog, satış, müşteriler ve CMS için yüzlerce ayrı izin, tek bir "her şeyi oku" ana açma düğmesi olmadan — bunların tümünü seçmekten başka bir yol yoktur. Göç yalnızca mağazanızdan okur; hiçbir şey geri yazmaz ve göçünüz doğrulandığında entegrasyonu iptal edebilirsiniz (bu kılavuzun sonunda ele alınmıştır).

Spwig asistanına geri döndüğünüzde, **Mağaza URL**'nizi ve kopyaladığınız **Erişim Token**'ı girin. **İlerlemeye Devam Etmeden Önce Bağlantıyı Test Et** seçeneğini açık bırakın (varsayılan olarak etkindir), böylece Spwig, ilerlemeye devam etmeden önce mağazanızla bağlantı kurabildiğini ve kimlik doğrulamasını sağlayabildiğini doğrular. Test başarısız olursa, URL'yi kontrol edin ve Magento'da entegrasyonun hâlâ **Etkin** olduğundan emin olun. **İleri**'ye tıklayın.

comment

 screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: magento-connection-step.webp
  description: Step 2 of the wizard with Magento selected, showing the Store URL and Access Token fields and the Test connection checkbox
  save-to: core/static/core/admin/img/help/migrate-from-magento/
  viewport: 1440x900


heading

## Step 3: Review What Will Be Imported

paragraph

Spwig, Magento mağazanızı sorgular ve bulduğu her veri türü için canlı sayılar gösterir: kategoriler, ürünler, müşteriler, siparişler, kuponlar (satış kurallarından kaynaklanan) ve CMS sayfaları. Her tür için bir onay kutusu vardır, Spwig import edilecek öğeler bulduğunda otomatik olarak işaretlenir ve sayacın sıfır olduğunda devre dışı bırakılır.

paragraph

Ayrıca ilk beş ürünün bir örneği de göreceksiniz, bu da tam importu onaylamadan önce başlık, fiyat ve resimlerin doğru göründüğünden emin olmanıza yardımcı olur.

paragraph

Sayılar altında, **Import Options** (İçe Aktarma Seçenekleri), importun nasıl davrandığını kontrol etmenizi sağlar:

list

paragraph

Belirli alanların haritalanması方式进行 (özel nitelikler, kategori eşleme, vergi veya kargo işleme) adım 4'te yapılır ve [Migration Field Mapping](migration-field-mapping) içinde ele alınmıştır. **Sonraki**'ye tıklayarak haritalama adımına geçin, sonra haritalamayı gözden geçtikten sonra **Start Migration**'a tıklayın.

heading

## Running the Import

paragraph

İçe aktarma arka planda çalışır — pencereyi kapatmakta özgürsünüz ve işlem devam eder. İlerleme sayfası, her veri türü (kategoriler, ürünler, müşteriler, siparişler, incelemeler, kuponlar) için canlı durumu gösterir ve detay için genişletilebilecek bir günlük içerir.

paragraph

İçe aktarma tamamlandığında, sonuç özeti sayfasına yönlendirilirsiniz. [After Your Migration](after-migration-review) üzerinden, neyin geçtiğini doğrulayın, eski Magento URL'lerini referans alan içerikler için bağlantı yeniden yazma işlemini yapın ve wizard tarafından toplanmış ancak otomatik olarak uygulanmamış vergi ve kargo yapılandırmasını düzenleyin.

comment

 screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step5/
  filename: magento-import-progress.webp
  description: Import progress page showing per-step status rows during a Magento migration
  save-to: core/static/core/admin/img/help/migrate-from-magento/
  viewport: 1440x900


heading

## Rollback Deadline

paragraph

Magento, rollback işlemi için zaman sınırlaması olan tek platformdur. Migrasyonunuz tamamlandığında, işin özeti sayfasında **Rollback** butonu görünür — ancak özellikle Magento için, tamamlanma sonrası bir süre sonra bu buton sunulmamaya başlanabilir. Diğer migrasyon türleri (WooCommerce, Shopify, CSV) bu zaman sınırlamasına sahip değildir, ancak Magento sahiptir, bu yüzden doğrulamayı daha sonra bırakmayın.

block_quote

**Uyarı:** Rollback, migrasyon tarafından oluşturulanlardan daha fazlasını siler — migrasyon sonrası migrasyon edilen müşterilerin oluşturduğu siparişleri ve migrasyon edilen ürünlerle ilgili sipariş kalemlerini, hatta migrasyon edilmemiş müşterilerden gelen siparişlerde bile. Sadece migrasyon sonrası, mağazada herhangi bir gerçek ticari işlem gerçekleşmeden hemen sonra kullanımı güvenlidir. Rollback'in neyi sileceğini ve neyi silemeyeceğini tam olarak öğrenmek için [Migration Troubleshooting](migration-troubleshooting)'e bakın.

paragraph

Rollback hâlâ kullanılabilirken, içe aktarılan verilerinizi kontrol edin, çünkü gerekiyorsa bunu kullanmanız gerekebilir.

heading

## Revoke the Integration

paragraph

Spwig'de verilerinizi doğruladığınızda — ürünler, fiyatlar, resimler, müşteriler, siparişler, kuponlar ve sayfaların hepsi doğru görünüyorsa — Magento'da **System > Integrations** geri dönün, `Spwig Migration`'ı bulun ve devre dışı bırakın veya silin.

Token, göçü tekrar çalıştırmayı planladığınız sürece tekrar gerekmez ve onu kaldırmak, artık ihtiyacınız olmayan açık bir okuma erişim kimlik doğrulama bilgisini kapatır.

## İpuçları

- **Değerlendirmeler, Magento tüccarları için en büyük sürprizdir** — Community Edition üzerinde olduğunuzda ve değerlendirmeler mağazanız için önemliyse, ayrı bir dışa aktarma/içe aktarma planlayın.
- **Erişim tokenını hemen kopyalayın** — Magento, entegrasyonu etkinleştirdiğinizde sadece bir kez gösterir; kaybederseniz, entegrasyonu devre dışı bırakıp yeniden oluşturmanız gerekir.
- **Doğrulamayı geciktirmeyin** — Rollback butonunun kullanılabilirliği, diğer platformlara göre Magento için zaman sınırlı bir özelliktir.
- **3. adımdaki örnek önizlemeyi kullanın** — tam içe aktarma çalıştırmadan önce, açıkça haritalama sorunlarını (yanlış fiyatlar, eksik görüntüler) yakalayın.
- **Kampanya kuponları satış kurallarından gelir** — bir Magento kuponu karmaşık koşullara bağlıysa, Spwig'de bunu kontrol edin çünkü her kural türüne doğrudan bir karşılık yoktur.
- **İçe aktarma sonrası Spwig'de vergi oranlarını ve sevkiyat bölgelerini yapılandırın** — sihirbazın vergi ve sevkiyat seçenekleri kaydedilir ancak mağazanıza otomatik olarak uygulanmaz.