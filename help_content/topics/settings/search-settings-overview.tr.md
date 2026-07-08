---
title: Arama Ayarlarını Anlamak
---

SearchSettings arayüzü, Spwig mağazanızdaki tüm küresel arama davranışını kontrol eder. Bu tek yapılandırma sayfası, temel etkinleştirme ile ileri düzey performans ayarlamaları arasında arama seçeneklerini organize etmek için 8 sekme arayüzünü kullanır. Burada yapılan değişiklikler, motor seviyesinde geçersiz kılınmazsa tüm arama motorlarına uygulanır.

Bu kılavuz, her bir sekmenin ne işe yaradığını ve ne zaman ayarlanması gerektiğini açıklayarak her bir sekme üzerinden geçer.

![Arama Ayarları Genel Sekme](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## 8-Sekme Arayüzü

SearchSettings, bir singleton modelidir - tüm mağazanız için yalnızca bir yapılandırma kaydı vardır (pk=1). Arayüz sekiz sekmeye bölünmüştür:

| Sekme | Amacı |
|-------|-------|
| **Genel** | Arama etkinleştirme/dinleme, temel parametreleri ayarlama |
| **Tamamlama** | Tahmini arama açılır menüsü davranışını yapılandırma |
| **İçerik Türleri** | Aranabilir içerik türlerini seçme |
| **Derin Dizinleme** | Ürün verilerinin ne kadarının dizine alınacağını kontrol etme (performans etkisi) |
| **Karışık Eşleştirme** | Yazım hatalarına tolerans ve benzerlik eşiklerini ayarlama |
| **Ağırlıklar** | Sonuçların sıralanması için ilgililik çarpanlarını ayarlama |
| **Önbellekleme** | Yanıt süresi ile tazeleme arasındaki denge |
| **Analizler** | Sorgu izleme ve gizlilik ayarları |

Her sekme, arama yapılandırmasının belirli bir yönünü odaklanır.

## Genel Sekme

Genel sekme, tüm aramalara etki eden temel ayarları içerir:

**Arama'yı Etkinleştir** - Arama sisteminin ana anahtar. Devre dışı bırakıldığında, tüm arama özellikleri mağazanızda etkin değildir, bunlar arasında tamamlama ve arama sonuçları sayfası da dahildir.

**Minimum Sorgu Uzunluğu** - Varsayılan: 2 karakter. Bu uzunluktan kısa sorgular reddedilir. Bu değeri 1 olarak ayarlamak tek karakterli sorguları (örneğin, "A") etkinleştirir ancak sunucu yükünü artırır.

**Sayfa Başına Sonuçlar** - Varsayılan: 20 öğe. Arama sonuçları sayfaları için sayfa numaralandırmasını kontrol eder. Daha yüksek değerler (30-50) sayfa numaralandırma tıklamalarını azaltır ancak sayfa yükleme süresini artırır.

## İçerik Türleri Sekmesi

![İçerik Türleri Ayarları](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

Arama sonuçlarında görünecek içerik türlerini etkinleştirme/dinleme:

- **Ürünler** - Fiziksel, dijital ve abonelik ürünleri
- **Kategoriler** - Ürün kategorileri
- **Markalar** - Ürün markaları
- **Blog Yazıları** - Blog içerikleri

**Performans Notu**: Daha az içerik türü = daha hızlı aramalar. Her etkinleştirilmiş tür ek veritabanı sorguları ekler. Eğer bir blogunuz yoksa, Blog Yazılarını devre dışı bırakarak yanıt sürelerini iyileştirebilirsiniz.

## Derin Dizinleme Sekmesi

⚠️ **PERFORMANS UYARISI** - Bu ayarlar önemli performans etkilerine sahiptir.

![Derin Dizinleme Ayarları](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Derin dizinleme, ürünle ilgili verilerin aramalarda ne kadarının dahil edileceğini kontrol eder:

**SKU'ları Dizinle** - Varsayılan: AÇIK, Düşük etki. Ürün ve varyant SKU'larını arama sonuçlarına dahil eder. B2B mağazalarında müşteriler ürün kodları ile arama yaparsa bu çok önemlidir.

**Özellikleri Dizinle** - Varsayılan: AÇIK, Orta etki. Ürün özellikleri (renk, boyut, malzeme) aramalarda dahil edilir. Özellikler tablosuna JOIN ekler. Giyim ve yapılandırılabilir ürünler için önemlidir.

**Özel Alanları Dizinle** - Varsayılan: AÇIK, Orta etki. Satıcı tarafından tanımlanmış özel alanları arama sonuçlarına dahil eder. JSONField gezintisi gerekir.

**Değerlendirmeleri Dizinle** - Varsayılan: KAPALI, **ÇOK YÜKSEK ETKİ** ⚠️

Doküman dizinleme, dijital ürünlerle eklenen PDF, DOCX ve XLSX dosyalarından metni çıkarır. Bu özellik:

- Çok pahalı başlangıç dizinleme gerektirir
- Her arama üzerinde önemli sorgu aşıntısına neden olur
- Büyük dosyalar zaman aşımına uğrayabilir
- **Yalnızca arama yapılabilir belgelerle çalışan dijital ürün mağazaları için etkinleştirilmelidir**
- **Kasıtlı olarak asla etkinleştirilmemeli** - önce performans etkisini dikkatle test edin

## Karışık Eşleştirme Sekmesi

![Karışık Eşleştirme Ayarları](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

Karışık eşleştirme, Levenshtein uzaklığı kullanarak yazım hatalarını işler:

**Karışık Eşleştirme'yi Etkinleştir** - Benzer terimlerin (örneğin, "laptop" "labtop" eşleşir) arama yapmasına izin verir

**Benzerlik Eşiği** - Varsayılan: 0.80 (80% benzerlik). Aralık: 0.0-1.0. Daha yüksek değerler daha yakın eşleşmeleri ve daha hızlı çalışmayı gerektirir. Daha düşük değerler daha fazla yazım hatasını yakalar ancak daha az ilgili sonuçlar döndürebilir.

**Maksimum Düzenleme Mesafesi** - Varsayılan: 2 karakter değişikliği. İzin verilen en fazla ekleme, silme veya değiştirme sayısı. Daha düşük değerler (1) performansı artırır ancak daha az yazım hatasını yakalar.

## Ağırlıklar Sekmesi

Ağırlıklar, ilgililik puanlamasını kontrol eder - sonuçların nasıl sıralandığı. Ağırlıklar sekmesi, her aranabilir alan için varsayılan çarpanları gösterir:

- weight_name: 1.50 (ürün isimleri en önemlidir)
- weight_sku: 1.20
- weight_description: 0.80
- weight_categories: 0.80
- weight_attributes: 0.70
- weight_brands: 0.70
- weight_blog_posts: 0.60
- weight_reviews: 0.50

Bu varsayılanlar çoğu e-ticaret mağazaları için iyi çalışır. Ağırlıkları ayarlama ve etkilerini anlama hakkında detaylı bilgi için [İlgililik Ağırlıkları ve Derin Dizinleme](/en/admin/help/relevance-weights-deep-indexing/) konusuna bakın.

## Önbellekleme Sekmesi

![Önbellekleme Ayarları](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

Önbellekleme, sonuçları depolayarak arama performansını büyük ölçüde artırır:

**Tamamlama Önbelleği TTL** - Varsayılan: 60 saniye. Tamamlama sonuçlarının ne kadar süre önbelleğe alınacağı. Daha kısa TTL (30-45s) = daha taze sonuçlar ancak daha fazla veritabanı sorgusu. Daha uzun TTL (90-120s) = daha hızlı ancak potansiyel olarak eski sonuçlar.

**Sonuçlar Önbelleği TTL** - Varsayılan: 300 saniye (5 dakika). Tam arama sonuçları sayfası önbelleği süresi. Daha uzun TTL, performansı önemli ölçüde artırır ancak yeni ürünlerin görünür hale gelmesini gecitirir.

**Denge**: Önbellekleme, tek başına en etkili performans optimizasyonudur. Aramalar yavaşsa, önce bu değerleri artırın, özelliklerini devre dışı bırakmaktan önce.

## Analizler Sekmesi

![Analizler Ayarları](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Arama Sorgularını Takip Et** - Arama analizlerini gösteren panoyu etkinleştirir. Sorgu metnini, sonuç sayısını, yanıt süresini ve zaman damgasını kaydeder.

**Kullanıcı Bilgilerini Takip Et** - Aramaları oturum açmış kullanıcılarla ilişkilendirir. Gizlilik uyumluluğu için (GDPR, CCPA) devre dışı bırakın.

**Oturum Bilgilerini Takip Et** - Oturum kimliklerini kullanarak anonim kullanıcı aramalarını izler. Kişisel veriler olmadan arama desenlerini tanımlamak için faydalıdır.

## Singleton Deseni

SearchSettings, singleton desenini kullanır - veritabanınızda yalnızca bir ayar kaydı vardır (pk=1). Yönetici panelinde Arama Ayarlarına gittiğinizde, her zaman aynı kaydı düzenliyorsunuz.

"Ekle" veya "Sil" seçeneği yoktur - sadece "Değiştir". Tüm arama motorları bu ayarları devralır, ancak her motor için özel motor geçersizliklerini belirtirlerse (nadiren).

## İpuçları

- **Varsayılan ayarları değiştirin, ancak özel bir ihtiyaçınız yoksa** - Varsayılan ayarlar, tipik e-ticaret mağazaları için optimize edilmiştir
- **Doküman dizinleme özelliğini asla kendi kendinize etkinleştirmeyin** - Yalnızca arama yapılabilir belgelerle çalışan dijital ürün mağazaları için ve performans etkisini önce test edin
- **Analizlerde yanıt sürelerini izleyin** - Tamamlama için <200ms, tam arama için <500ms hedefleyin
- **Performans yavaşsa önbellek TTL'sini artırın** - Önbellekleme en kolay performans kazancıdır
- **Haftalık olarak sıfır sonuç sorgularını gözden geçirin** - Eksik ürünler veya gerekli eşanlamlılar ortaya çıkarır
- **Kullanılmayan içerik türlerini devre dışı bırakın** - Blogunuz yoksa, Blog Yazılarını devre dışı bırakarak aramaları hızlandırın

Unutmayın: Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri gösterilen koruma kurallarına uygun şekilde koruyun.