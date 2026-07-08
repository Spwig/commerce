---
title: Eşanlamlı Kelimeler ve Yönlendirmeleri Yönetme
---

Eşanlamlı kelimeler ve yönlendirmeler, eşdeğer terimleri işlemek ve belirli sorguları hedef sayfalara yönlendirmek suretiyle aramanızı daha akıllı hale getirir. Eşanlamlı kelimeler, aramaları ilgili terimlerle genişletir ("laptop" aynı zamanda "notebook" bulur), yönlendirmeler ise "sale" gibi sorguları doğrudan satış sayfanıza yönlendirir. Bu kılavuz, arama ilgiliğini ve müşteri deneyimini artırmak için bu iki özelliğin nasıl oluşturulacağını ve yönetileceğini açıklar.

Eşanlamlı kelimeleri terim eşdeğerliği için, yönlendirmeleri ise navigasyon kısayolları için kullanın.

![Eşanlamlı Kelimeler Listesi](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## Eşanlamlı Kelimeleri Anlamak

Eşanlamlı kelimeler, arama sisteminin belirli terimlerin eşdeğer olarak kabul edilmesi gerektiğini söyler. Bir müşteri bir terimle arama yaparsa, sistem otomatik olarak eşanlamlı terimlerle eşleşen sonuçları da içerir.

**Örnek**: "laptop" → "notebook", "taşınabilir bilgisayar" eşanlamlılığı oluşturun. Artık "laptop" araması, "notebook" veya "taşınabilir bilgisayar" kelimelerinin ürün isimlerinde veya açıklamalarında yer aldığı ürünlerin sonuçlarını da içerir.

Eşanlamlı kelimeler özellikle şu durumlarda değerlidir:
- İngilizce (İngiltere) vs Amerikan İngilizcesi (jumper/sweater, trainers/sneakers)
- Marka vs genel terimler (tissues/Kleenex)
- Yaygın yazım hataları (accommodate/accomodate)
- Endüstri jargonu vs basit dil (CPU/processor)

## Eşanlamlı Kelimeler Oluşturma

**Arama > Eşanlamlı Kelimeler** bölümüne gidin ve **+ Eşanlamlı Kelime Ekle**'ye tıklayın.

![Eşanlamlı Kelime Ekle Formu](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Kelime** - Eşanlamlı kelimeleri genişleten orijinal arama terimi

**Eşanlamlılar** - Eşdeğer terimlerin JSON dizisi, örneğin `['sweater', 'pullover', 'jumper']`

**İki Yönlü** - Varsayılan: Etkin. Etkinleştirildiğinde, eşanlamlı ilişkiler her iki yönde de çalışır:
- "laptop" araması "notebook" ürünleri bulur
- "notebook" araması "laptop" ürünleri bulur

İki yönlü işaretini kaldırın (aşağıya bakın) tek yönlü eşleme için.

**Dil** - Opsiyonel. Bu eşanlamlıyı belirli bir dildeki aramalara sınırlayın. Boş bırakınca tüm dillere uygulanır.

**Motor** - Opsiyonel. Bu eşanlamlıyı belirli bir arama motoruna sınırlayın. Boş bırakınca genel olarak uygulanır.

**Aktif** - Bu eşanlamlının şu anda kullanılıp kullanılmadığı. Geçici olarak devre dışı bırakmak için işaretini kaldırın.

## İki Yönlü Eşanlamlı Örnekler

Çoğu eşanlamlı kelime iki yönlü olmalıdır - her iki yönde de çalışan gerçek eşdeğerler:

| Kelime | Eşanlamlılar | Kullanım Durumu |
|--------|--------------|------------------|
| laptop | notebook, taşınabilir bilgisayar | Amerikan/İngilizce + genel terimler |
| sofa | couch, settee | Bölgesel farklılıklar |
| trainers | sneakers, running shoes | İngiltere/ABD İngilizcesi |
| mobile | cell phone, cellular | Uluslararası farklılıklar |

İki yönlü işaretli olduğunda, tüm bu terimler müşteri tarafından kullanılan terime bakılmaksızın aynı ürünleri bulur.

## Tek Yönlü Eşanlamlı Örnekler

"İki Yönlü" işaretini kaldırın tek yönlü ilişkiler için:

**Sık Kullanılan Durumlar**:
- **Yazım Hataları**: Kelime: "acco modate" → Eşanlamlılar: `['accommodate']` (tek yönlü olduğu için doğru yazım yazım hatasını bulmaz)
- **Özel → Genel**: Kelime: "MacBook" → Eşanlamlılar: `['laptop']` (MacBooks laptoplardır, ancak tüm laptoplar MacBook değildir)
- **Kısaltmalar**: Kelime: "CPU" → Eşanlamlılar: `['processor']` (CPU, işlemci ürünleri bulur, ancak işlemci aramaları her zaman CPU'yu içermemelidir)

## Dil Özel Eşanlamlılar

Dil alanını kullanarak bölgeye özel eşanlamlı kelimeler oluşturun:

**Örnek**: İngilizce (İngiltere) mağazası
- Kelime: "jumper", Eşanlamlılar: `['sweater', 'pullover']`, Dil: İngilizce (İngiltere)
- Kelime: "trainers", Eşanlamlılar: `['sneakers']`, Dil: İngilizce (İngiltere)

**Örnek**: Çok dilli mağaza
- Kelime: "ordinateur portable", Eşanlamlılar: `['laptop', 'notebook']`, Dil: Fransızca
- Kelime: "zapatos", Eşanlamlılar: `['shoes']`, Dil: İspanyolca

Dil özel eşanlamlılar, müşteri belirli bir dilde tarayıcaksa uygulanır.

## Motor Özel Eşanlamlılar

Çoğu eşanlamlı kelime genel olarak uygulanmalıdır (Motor alanını boş bırakın). Motor özel eşanlamlılar sadece farklı arama bağlamlarında farklı terim eşleme gerekirse kullanın:

**Örnek**: Ayırma "shop" ve "blog" motorlarınıza sahipsiniz
- Blog eşanlamlısı: Kelime: "tutorial" → Eşanlamlılar: `['guide', 'how-to']`, Motor: blog
- Bu eşanlamlı sadece blog aramalarına uygulanır, ürün aramalarına değil

## Yönlendirmeleri Anlamak

Arama yönlendirmeleri, belirli sorguları doğrudan belirli sayfalara yönlendirir, normal arama sonuçlarını atlar. Yönlendirmeleri, müşteri tam olarak nereye gitmesi gerektiğini bildiğinizde kullanın.

**Örnek**: "sale" → `/products/sale/` için bir yönlendirme oluşturun. Artık "sale" araması, arama sonuçlarını atlar ve doğrudan satış sayfanıza yönlendirilir.

Yönlendirmeler şu durumlarda harikadır:
- Yaygın navigasyon kısayolları ("returns" → iade politikası sayfası)
- Mevsimsel kampanyalar ("summer sale" → yaz koleksiyonu)
- Popüler kategoriler ("laptops" → laptop kategori sayfası)
- Politika sayfaları ("shipping" → kargo bilgisi)

![Yönlendirmeler Listesi](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## Eşleşme Türleri

Yönlendirmeler, arama sorgusunun ne kadar sıkı eşleşmesi gerektiğini kontrol eden dört eşleşme türünü destekler:

**Tam** - Büyük/küçük harfe duyarlı tam eşleşme. Sorgu, terimle tam olarak eşleşmelidir (büyük/küçük harfe bakılmadan).
- Terim: "sale"
- Eşleşmeler: "sale", "SALE", "Sale"
- Eşleşmez: "summer sale", "on sale"

**İçerir** - Sorgu, terimin herhangi bir yerinde bulunur.
- Terim: "sizing"
- Eşleşmeler: "sizing guide", "help with sizing", "what sizing"
- Eşleşmez: "size chart" (farklı kelime)

**Başlar** - Sorgu, terimle başlar.
- Terim: "return"
- Eşleşmeler: "returns", "return policy", "returning items"
- Eşleşmez: "how to return" (terimle başlamaz)

**Regex** - Düzenli ifadeler kullanarak desen eşleştirme. **⚠️ Performans dikkat**: Karmaşık regex desenleri aramaları yavaşlatır. Sadece gerekli olduğunda kullanın.
- Desen: `^(laptop|notebook)s?$`
- Eşleşmeler: "laptop", "laptops", "notebook", "notebooks"
- Diğer eşleşme türleri işe yaramazsa sadece bu kullanın

## Yönlendirme Oluşturma

**Arama > Yönlendirmeler** bölümüne gidin ve **+ Yönlendirme Ekle**'ye tıklayın.

![Yönlendirme Ekle Formu](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Kelime** - Eşleşmesi gereken arama sorgusu

**Eşleşme Türü** - Tam, İçerir, Başlar, Regex (yukarıdaki gibi)

**Yönlendirme URL'si** - Müşteriyi nereye yönlendireceğiniz. Göreli (`/products/sale/`) veya mutlak (`https://example.com/page/`) olabilir

**Yönlendirme Türü** - HTTP durum kodu:
- **302 (Geçici)**: Önerilir. Tarayıcı önbelleklemeyi yapmaz, daha sonra hedefi değiştirebilirsiniz
- **301 (Kalıcı)**: Tarayıcı ve arama motorları önbellekler. Sadece kalıcı yönlendirmeler için kullanın

**Motor** - Opsiyonel. Belirli bir arama motoruna sınırlayın

**Vurum Sayısı** - Bu yönlendirme her kullanıldığında otomatik olarak artırılır. Popüler kısayolları tanımlamak için kullanılır

**Aktif** - Bu yönlendirmeyi etkinleştirin/etkinleştirme

## Yönlendirme Örnekleri

| Kelime | Eşleşme Türü | URL | Kullanım Durumu |
|--------|--------------|-----|------------------|
| sale | Tam | `/products/sale/` | "sale" aramalarını doğrudan satış sayfasına yönlendirir |
| clearance | Tam | `/clearance/` | Temizlik ürünleri için arama atla |
| sizing | İçerir | `/pages/size-guide/` | Boyutla ilgili herhangi bir sorgu kılavuza yönlendirilir |
| return | Başlar | `/pages/returns/` | İade ile ilgili sorgular politika sayfasına yönlendirilir |

Tümü 302 (geçici) yönlendirmeleri kullanır, çünkü esneklik sağlar.

## Yönlendirme Türü: 302 vs 301

**302 (Geçici)** - Çoğu yönlendirme için önerilir
- Tarayıcı her seferinde yeni bir istek yapar
- Hedef URL'yi her zaman değiştirebilirsiniz
- Emin olamadığınızda daha güvenli bir seçimdir

**301 (Kalıcı)** - Sadece gerekli olduğunda kullanın
- Tarayıcı önbelleklemeyi yapar
- Arama motorları indekslerini günceller
- Daha sonra değiştirmek zordur

**Öneri**: 302 kullanın, emin olamadığınızda 301 kullanmayın.

## Vurum Sayısı Analitiği

Vurum Sayısı alanı, yönlendirme her tetiklendiğinde otomatik olarak artırılır. Bu alanı şu şekilde kullanabilirsiniz:
- En çok kullanılan navigasyon kısayollarını tanımlamak
- Hiç kullanılmayan yönlendirmeleri bulmak (kaldırmayı düşünün)
- Popüler arama desenlerini keşfetmek

Aylık olarak vurum sayılarını inceleyerek yönlendirme stratejinizi optimize edin.

## Eşanlamlı Kelime Fırsatlarını Bulma

**Sıfır Sonuç Aramalarını Kullanın**: **Arama > Arama Analitiği** bölümüne gidin ve sıfır sonuç aramaları için filtreleyin. Bu, şu şeyleri gösterir:
- Müşterilerin kullandığı, ürün açıklamalarınızla eşleşmeyen terimler
- Dikkate alınmamış bölgesel farklılıklar
- Yaygın yazım hataları

**İş Akışı**:
1. Haftalık olarak sıfır sonuç aramalarını inceleyin
2. Desenleri tanımlayın (aynı terimlerin tekrar tekrar görünmesi)
3. Müşteri dili ile ürün isimlerinizi eşleştirmek için eşanlamlılar ekleyin
4. Sıfır sonuçların azalıp azalmadığını izleyin

## İpuçları

- **Haftalık olarak sıfır sonuç aramalarını inceleyin** - Müşteri dili ile ürün açıklamalarınız arasındaki boşlukları gösterir
- **Genel eşanlamlılarla başlayın, verilere göre genişletin** - Bölgesel farklılıklarla başlayın, sonra gerçek arama davranışlarına göre ekleyin
- **Gerçek eşdeğerler için iki yönlü kullanın** - Çoğu eşanlamlı her iki yönde de çalışmalı (laptop ↔ notebook)
- **Karmaşık regex desenlerinden kaçının** - Regex eşleşmeleri diğer eşleşme türlerinden daha yavaş; sadece gerekli olduğunda kullanın
- **Varsayılan olarak 302 yönlendirmeleri (geçici) kullanın** - Daha sonra hedefleri değiştirmek için esneklik sağlar
- **Gerçek sorgularla eşanlamlıları test edin** - Eşanlamlı terimleri arayarak beklenen sonuçların döndürüp döndürmediğini doğrulayın
- **Çok dilli mağazalar için dil özel eşanlamlılar oluşturun** - Desteklediğiniz her dil için bölgeye özel terim eşleme haritaları oluşturun
