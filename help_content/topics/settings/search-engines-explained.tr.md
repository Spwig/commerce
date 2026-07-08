---
title: Arama Motorları Hakkında
---

Spwig'da arama motorları Elasticsearch veya Algolia gibi harici hizmetler değil, mağazanızın veritabanı içi arama sisteminin içindeki yapılandırma bağlamalarıdır. Her motor, hangi içerik türlerinin aranacağını, neyi dışlayacağını ve sonuçların nasıl sıralanacağını tanımlar. Bu kılavuz, arama motorları hakkında ne olduğunu, ne zaman birden fazla motor oluşturmanız gerektiğini ve bunları nasıl yapılandıracağınızı açıklar.

Çoğu satıcı, tek bir varsayılan "shop" motorunu kullanır. Farklı kullanım durumları için farklı içerik karışımına veya dışlamalara ihtiyaç duyduğunuzda birden fazla motor oluşturun.

![Arama Motorları Listesi](/static/core/admin/img/help/search-engines-explained/search-engines-list.webp)

## Arama Motorları Nedir?

Spwig'da bir arama motoru, aşağıdaki öğeleri belirleyen isimlendirilmiş bir yapılandırmadır:

- **Hangi içerik türlerinin aranacağını** (ürünler, kategoriler, markalar, blog gönderileri)
- **Ne dışlanacağını** (aramadan gizlenmesini istediğiniz özel kategoriler veya markalar)
- **Özel ilgililik ağırlıkları** (opsiyonel, motor başına ağırlık geçersizleştirme)
- **Aktif durum** (motorlar geçici olarak devre dışı bırakılabilir)

Her motor, API çağrılarında ve frontend kodunda hangi motorun bir arama isteğini işlemesini gerektiğini belirlemek için kullanılan benzersiz bir slug'a sahiptir.

## Ne Zaman Birden Fazla Motor Oluşturulur

Çoğu mağaza için yalnızca bir motor yeterlidir. Aşağıdaki senaryolarda ek motorlar oluşturun:

| Kullanım Durumu | Örnek |
|------------------|-------|
| **Farklı içerik karışımı** | Mağaza motoru yalnızca ürünleri arar; Blog motoru yalnızca blog gönderilerini arar |
| **Seçici dışlamalar** | Ana mağaza motoru indirim kategorisini gizler; İndirim motoru yalnızca indirim ürünleri gösterir |
| **Departman özel arama** | Elektronik motoru kıyafet kategorilerini dışlar; Kıyafet motoru elektronikleri dışlar |
| **B2B vs B2C ayrımı** | Toptan motoru yalnızca toptan ürünleri gösterir; Perakende motoru tüketiciler için ürünleri gösterir |

Eğer birden fazla motor ihtiyacınız olup olmadığını emin olamıyorsanız, bir taneyle kalın. Motorlar, belirli bir kullanım durumunuz yoksa, karmaşıklık yaratır ancak fayda sağlamaz.

## 4 Adımlık Sihirbaz

![Sihirbaz Adım 1 - Temel Bilgi](/static/core/admin/img/help/search-engines-explained/wizard-step1-basic.webp)

**Arama > Kurulum Sihirbazı**'na giderek, 4 adımlık bir rehber süreciyle yeni bir motor oluşturabilirsiniz:

### Adım 1: Temel Bilgi

**Motor Adı** - Kullanıcı dostu görüntü adı (örneğin, "Mağaza Araması", "Blog Araması"). Yalnızca yönetici arayüzünde kullanılır.

**Slug** - URL'ye uyumlu tanımlayıcı (örneğin, "shop-search", "blog-search"). API çağrılarında ve frontend kodunda kullanılır. Ad boş bırakılırsa otomatik olarak adından oluşturulur.

**Aktif** - Bu motorun aramalar için kullanılabilir olup olmadığını belirtir. Aktif olmayan motorlar hiçbir sonuç döndürmez.

### Adım 2: İçerik Türleri

Bu motorun hangi içerik türlerini arayacağını seçin:

- Ürünler (tüm ürün türlerini içerir: fiziksel, dijital, abonelikler)
- Kategoriler
- Markalar
- Blog Gönderileri

**İpucu**: Bu motorun amacı ile ilgili içerik türlerini seçin. Blog odaklı bir motor ürünleri etkinleştirmek zorunda değildir.

### Adım 3: Ağırlıklar (Opsiyonel)

![Sihirbaz Adım 3 - Ağırlıklar](/static/core/admin/img/help/search-engines-explained/wizard-step3-weights.webp)

Bu özel motor için ilgililik ağırlıklarını isteğe bağlı olarak özelleştirebilirsiniz. Eğer atlanırsa, motor, SearchSettings'ten küresel ağırlıkları miras alır.

Çoğu motor bu adımı atlayıp küresel varsayılanları kullanmalıdır. Sadece bu motorun özel sıralama ihtiyaçları varsa (örneğin, bir blog motoru weight_blog_posts'ı 1.2'ye artırabilir) ağırlıkları özelleştirin.

### Adım 4: Gözden Geçir ve Oluştur

Yapılandırmanızı gözden geçirin ve **Motor Oluştur**'a tıklayarak kaydedin.

## Motor Yapılandırma Alanları

Eğer bir motoru doğrudan (sihirbazı atlayarak) düzenliyorsanız, aşağıdaki alanları göreceksiniz:

**Ad ve Slug** - Görünür ad ve URL tanımlayıcısı

**Aktif Durum** - Etkinleştirme/Devre dışı bırakma anahtarlaması

**İçerik Türleri** - `["product", "category"]` gibi JSON dizi

**Ağırlık Geçersizleştirme** - `{"weight_name": 1.8}` gibi JSON nesnesi (küresel ağırlıklar kullanılıyorsa boş)

**Dışlanan Kategoriler** - Kategori modeline M2M ilişki. Bu kategorilere ait ürünler arama sonuçlarında görünmez.

**Dışlanan Markalar** - Marka modeline M2M ilişki.


Bu markalara sahip ürünler, arama sonuçlarında görünmeyecektir.

## Hariç Tutmalar Kullanımı

Hariç tutmalar, bu motor için arama sonuçlarından belirli içerikleri gizler:

**Örnek: İndirim Ürünlerini Gizleme**

1. Bir "Ana Mağaza" motoru oluşturun
2. Hariç Tutulan Kategoriler alanına, "İndirim" kategorinizi seçin
3. Hariç Tutulan Markalar alanına, gizlemek istediğiniz bütçe markalarını seçin
4. Kaydedin

Şimdi "Ana Mağaza" motoru üzerinden yapılan aramalar, site üzerinde görünmelerine rağmen indirim ürünleri döndürmeyecektir. İndirim ürünleri için ayrı bir "İndirim" motoru oluşturabilir ve sadece indirim ürünleri üzerinde arama yapabilirsiniz.

## Frontend'de Motor Kullanımı

Frontend kodunuz, API çağrıları aracılığıyla hangi motorun kullanılacağını belirler:

```javascript
// "shop" motorunu kullan (en yaygın olan)
fetch('/api/search/?q=laptop&engine=shop')

// "blog" motorunu kullan
fetch('/api/search/?q=ecommerce tips&engine=blog')

// Motor parametresi belirtilmezse varsayılan motor
fetch('/api/search/?q=laptop')
```

Motor slug'ı bir sorgu parametresi haline gelir. Eğer bir motor belirtilmezse, Spwig alfabetik olarak ilk aktif motoru kullanır.

## Motor-Spesifik Eşanlamlılar ve Yönlendirmeler

Hem Eşanlamlı hem de AramaYönlendirme modelleri, isteğe bağlı bir `engine` yabancı anahtara sahiptir. Ayarlanırsa, bu eşanlamlı veya yönlendirme sadece o belirli motora yapılan aramalarda geçerlidir.

**Örnek**: Bir blog motorunda "tutorial" → "guide" gibi eşanlamlılar olabilir ve bu, ürün aramalarında geçerli olmayabilir.

Çoğu eşanlamlı ve yönlendirme motor-spesifik olmamalıdır - motor alanını boş bırakarak onları genel olarak uygulayın.

## İpuçları

- **Bir motorla başlayın** - Varsayılan "shop" motorunu oluşturun ve birden fazla motor ihtiyacınız olana kadar her şey için onu kullanın
- **Açıklayıcı slug'lar kullanın** - "shop", "blog", "wholesale" gibi, motorun amacını açıkça gösteren slug'lar seçin
- **Aktif etmeden önce motorları test edin** - Aktif olmayan durumda motorlar oluşturun, API üzerinden test edin, sonra aktif edin
- **Gerekmedikçe motor oluşturmayın** - Daha fazla motor, aynı şeyi yapan motorlar için daha fazla yapılandırma karmaşıklığı getirir
- **Motorlara göre analitikleri inceleyin** - Arama Analitiği panosu, motorlara göre filtreleyerek hangi motorların en çok kullanıldığını gösterebilir