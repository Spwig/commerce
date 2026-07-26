---
title: CSV Dosyalarından İçe Aktarma
---

CSV içe aktarma, Spwig doğrudan bağlanamadığı her mağazanın alternatif geçiş yoludur. BigCommerce, PrestaShop, Squarespace, Wix, elle yönettiğiniz bir tablo ya da Spwig tarafından anlaşılmayan özel bir sistemden geliyorsanız, burada olacaksınız — verilerinizi CSV dosyalarına dışa aktarın ve canlı bağlantı kurmak yerine buraya yükleyin.

Bu kılavuz, API bağlantısı yerine CSV kullanmanıza ne zaman karar verilmesi gerektiğini, CSV'nin ne taşıyamayacağını, dahil olan beş dosya, bunları nasıl hazırlamanız gerektiğini ve sütun eşleme nasıl çalıştığını kapsar.

## API Bağlantısı Yerine CSV Kullanmanıza Ne Zaman Karar Verilir

Spwig WooCommerce, Shopify ve Magento 2/Adobe Commerce'a doğrudan bağlanır — bunlar için [Veri Geçişine Genel Bakış](migration-overview) bölümüne bakın. Diğer herhangi bir platform için CSV tek seçeneğinizdir; BigCommerce, PrestaShop, Squarespace veya Wix için doğrudan entegrasyon yoktur. Ayrıca, bir tablodan verileri konsolide etmek, özel bir mağazayı kapatmak veya dosyaları kendiniz oluşturarak neyin içe aktarılacağını kontrol etmek istiyorsanız bu da doğru seçimdir.

## CSV'nin Yapamayacağı Şeyler

Herhangi bir şey hazırlamadan önce, bu yolun ne bıraktığını bilmelisiniz — CSV içe aktarma, mağazalar için en büyük sürpriz kaynağıdır:

- **Ürün resimleri yok.** Ürünler resim içermeden içe aktarılır; bunları daha sonra yükleyin.
- **Varyasyonlar yok.** Her ürün basit bir ürün olarak oluşturulur. İçe aktarma sonrası Spwig'de boyut/rengi/stil yapılarını yeniden oluşturun.
- **Kuponlar yok.** İndirim kodları ve kampanyalar CSV formatında değildir.
- **Blog içerikleri yok.** Yazılar veya makaleler için bir CSV dosyası yoktur.

Bu hiçbir şey içe aktarmayı engellememekle birlikte, ürünlerin Spwig'de olmasından sonra ek işler gerektireceğini ima eder. İç aktarma sonrası tam kontrol listesi için [Geçişiniz Sonrası](after-migration-review) bölümüne bakın.

## Beş Dosya

Sihirbazın CSV adımı beş dosya girişi sunar, her biri bir **Şablon İndir** butonu ile. Şablonlardan başlayın ve dosyaları sıfırdan oluşturmak yerine — bunlar doğru sütun isimlerini garanti altına alır ve 4. adımda otomatik algılama işini daha fazla yapmanı sağlar.

| Dosya | Gerekli mi? |
|---|---|
| Ürünler | **Gerekli** |
| Kategoriler | Opsiyonel |
| Müşteriler | Opsiyonel |
| Siparişler | Opsiyonel |
| Değerlendirmeler | Opsiyonel |

Ürünler, Spwig'in zorunlu olduğu tek dosyadır — diğerleri henüz bu verilere sahip değilse boş bırakılabilir.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: csv-file-upload-step.webp
  description: CSV seçilmiş Step 2, beş dosya girişi ve Şablon İndir butonlarını gösteriyor
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

### Ürünler (Gerekli)

| Sütun | Açıklama |
|---|---|
| `id` | Kaynak verilerinizdeki benzersiz tanımlayıcı; müşterilere gösterilmez. |
| `name` | Ürün başlığı. **Zorunludur.** |
| `slug` | İsimin URL dostu sürümü; boş bırakılırsa `name`den otomatik olarak oluşturulur. |
| `description` | Mağaza ön yüzünde gösterilen açıklama. |
| `price` | Ürünün normal fiyatı. **Zorunludur.** |
| `sku` | Stok birimi — **Mevcut Öğeleri Atla** etkin olduğunda eşleşmede kullanılır. |
| `stock_quantity` | Mevcut stok birimleri. |
| `category` | Bu ürünün ait olduğu kategori adı. Kategoriler dosyanızdaki `name` ile eşleşmelidir. |

### Kategoriler

| Sütun | Açıklama |
|---|---|
| `id` | Kaynak verilerinizdeki benzersiz tanımlayıcı. |
| `name` | Kategori adı. **Zorunludur.** |
| `slug` | İsimin URL dostu sürümü; boş bırakılırsa otomatik olarak oluşturulur. |
| `description` | Kategori açıklaması metni. |
| `parent_id` | Bu kategorinin ebeveyninin `id`si. Boş bırakılırsa üst düzey anlamına gelir. |

### Müşteriler

| Sütun | Açıklama |
|---|---|
| `id` | Kaynak verilerinizdeki benzersiz tanımlayıcı. |
| `email` | Müşterinin e-posta adresi. **Zorunludur** — siparişler ve değerlendirmeleri doğru müşteriye bağlar. |
| `first_name` | Müşterinin adı. |
| `last_name` | Müşterinin soyadı. |
| `phone` | Müşterinin telefon numarası. |

### Siparişler


| Sütun | Açıklama |
|---|---|
| `id` | Kaynak verilerinizdeki benzersiz tanımlayıcı. |
| `customer_email` | Siparişi veren müşterinin e-postası. **Zorunludur** — siparişi bir müşteri kaydıyla ilişkilendirir. |
| `order_date` | Siparişin verildiği tarih. |
| `status` | Siparişin durumu (örneğin tamamlandı, işleme). |
| `total` | Sipariş toplamı. **Zorunludur.** |
| `currency` | Sipariş toplamı için para birimi kodu. |

### Değerlendirmeler (Opsiyonel)

| Sütun | Açıklama |
|---|---|
| `id` | Kaynak verilerinizdeki benzersiz tanımlayıcı. |
| `product_id` | Değerlendirilen ürünün `id` si, ürünler dosyanızla eşleşmelidir. **Zorunludur** — değerlendirme doğru ürüne ilişkilendirilir. |
| `customer_email` | Değerlendiren kişinin e-posta adresi. |
| `rating` | Verilen yıldız puanı. |
| `comment` | Değerlendirme metni. |
| `date` | Değerlendirmenin yayınlandığı tarih. |

## Dosyalarınızı Hazırlama

- **UTF-8 olarak kaydedin** — farklı bir kaynak kodlamasından gelen çakışmış tırnaklı karakterleri önlemek için özellikle. |
- **Virgül içeren alanları tırnakla çevirin** — bir açıklama veya ad virgül içeriyorsa, çift tırnakla sarın, böylece sütun ayrımı olarak yanlış yorumlanmaz. |
- **Başlık satırını ekleyin.** İlk satır, sütun isimlerini içermelidir — başlık satırı olmayan bir dosya reddedilir. |
- **`parent_id` ile kategori hiyerarşisini oluşturun.** Her kategoriye benzersiz bir `id` verin, ardından bir alt kategorinin `parent_id` sini, üst kategorinin `id` sine ayarlayın. Boş bırakmak, en üst düzey anlamına gelir. |
- **`customer_email` ile siparişleri müşterilere bağlayın**, müşteriler dosyanızdaki `email` sütununa karşı eşleştirin (veya bir misafir kaydı oluşturulur), iç platformlar arasında genellikle uyum sağlayamayan iç ID numaralarına değil. |
- **`product_id` ile değerlendirmeleri ürünlerle bağlayın**, ürünler dosyanızdaki `id` sütununda bir değere eşleşir ya da o değerlendirme atlanır. |

## 4. Adımda Sütunları Haritalama

4. Adım, bir CSV Sütun Haritalama paneli gösterir. Spwig, başlıkları tarar ve yaygın eşleşmeler listesiyle otomatik olarak algılar — örneğin, `sku` alanı `barcode`, `part_number` veya `item_number` ile eşleşebilir. Diğer bir platformdan doğrudan dışa aktarılan başlıklar genellikle manuel iş yapmadan doğru şekilde eşleşir.

Her sütun için, otomatik algılanan tahmini kabul edebilir, farklı bir hedef alanı seçerek geçersiz kılabilir veya "— Bu sütunu atla —" seçeneğini seçerek dışlamak da mümkündür. Haritalamalar kaydedilir ve gelecekteki CSV geçişlerinde yeniden kullanılır. 4. adımdaki tam resmi görmek için [Geçiş Alanı Haritalama](migration-field-mapping) bölümüne bakın, otomatik alan haritalamaları, kategori haritalamaları ve vergi/teslimat seçenekleri dahil.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: 4. Adım CSV Sütun Haritalama paneli, otomatik algılanan haritalamalarla geçersizleştirme açılır menüleri gösteriyor
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Yaygın Hatalar ve Ne Anlama Gelmeleri

| Hata | Anlamı |
|---|---|
| `Products CSV is required.` | Ürünler dosyası yüklemeye çalıştınız ama bir ürün dosyası yüklememişsiniz. Bu, Spwig'in gerekli tek dosyasıdır — bir tane yükleyin ve devam edin. |
| `{Type} CSV has no headers.` | Belirtilen dosyanın ilk satırı boş ya da eksik. Sütun isimlerini içeren bir başlık satırı ekleyin ve tekrar yükleyin. |
| `{Type} CSV could not be read: ...` | Spwig, belirtilen dosyayı okuyamadı — genellikle bozuk bir dosya, yanlış kodlama veya uzantısı CSV olsa da aslında CSV olmayan bir dosya. Tekrar dışa aktarın ve tekrar yüklemeye başlamadan önce dosyanın temiz şekilde açılmasını kontrol edin. |

## İmportu Başlatma

Haritalama onaylandıktan sonra, 5. adımdan geçiş işlemini başlatın. Arka planda çalışır, bu yüzden pencereyi kapatmak için izin verilir — tamamlanmadan önce geri dönerseniz, ilerleme ve canlı log mevcuttur. Sonuçları doğrulamak için [Geçişiniz Sonrası](after-migration-review) bölümüne bakın.

CSV içeriği, özellikle **ürün resimleri** ve **varyasyonları** için el ile tamamlamanızı gerektirir — bu, dosyalarınızın ne kadar tam olduğuna bakılmaksızın otomatik olarak geçmez.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Her dosya için 'Şablonu İndir' butonundan başlayın** — aksi takdirde manuel haritalama yapmaya mecbur kalacağınız sütun adı yazım hatalarından kurtarır.
- **Değerlendirmeleri yüklemeden önce `product_id` eşleşmelerini düzeltin** — bir değerlendirinin `product_id`si herhangi bir ürünün `id`siyle eşleşmiyorsa, bu değerlendirinin ekleyeceği bir şey yoktur ve atlanır.
- **Diğer bir platformun dışa aktarımından gelen başlıkları yeniden adlandırmayın** — otomatik algılama genellikle bunları olduğu gibi takma isimler aracılığıyla tanır, bu nedenle manuel iş yapmaya gerek olmayabilir.
- **İçe aktarma hemen ardından görseller ve varyasyonlar için zaman ayırın** — bu iki şey CSV dosyası tarafından asla aktarılmaz ve müşteri bir ürün sayfasının boş olduğunu fark edene kadar unutulabilir.
- **`parent_id` kullanarak çok seviyeli kategorileri modelleyin** — bir alt kategorinin `parent_id`sini, üst kategorinin `id`siyle eşleştirerek iç içe yapın; üst düzey kategoriler için boş bırakın.
- **"Okunamadı" hatası olduğunda tekrar dışa aktarın ve tekrar kontrol edin** — bu hata neredeyse her zaman kaynak dosyadaki kodlama veya bozulmaya dayanır, Spwig'de onarılmaması gerekir.