---
title: Ürün Markaları
---

Markalar, ürünlerin üretici veya etiketiyle ilişkilendirilmesine olanak tanır ve müşterilere mağazayı marka bazında tarayabilme yolunu sağlar. Her marka, mağaza ön yüzünde kendi sayfasına sahiptir ve müşteriler bu sayfadan o markanın tüm ürünleri, marka hikayesini okuyabilir ve markanın web sitesine yönlendirilebilir.

**Katalog > Markalar** menüsüne giderek markalarınızı yönetin.

## Markaların Kullanım Nedenleri

Spwig'de markalar iki amaç için kullanılır:

1. **Organizasyon** — ürünler bir marka ile etiketlenir, bu da belirli bir etikete sadık olan müşterilerin aradıklarını kolayca bulmalarını sağlar
2. **Satış Stratejisi** — marka sayfaları, marka hikayesini, logoyu ve ürün yelpazesini sergileme için ayrılmış bir alan sağlar ve marka bilinçli müşteriler için dönüşümü artırabilir

Markalar ayrıca promosyon sistemiyle çalışır — belirli bir markanın tüm ürünlerine uygulanacak bir satış oluşturabilirsiniz, bireysel ürünleri seçmek zorunda kalmadan.

## Marka Oluşturma

1. **Katalog > Markalar** menüsüne gidin
2. **+ Marka Ekle**'ye tıklayın
3. **Temel Bilgiler** bölümünü doldurun:
   - **Ad** — mağaza ön yüzünde görünecek marka adı (benzersiz olmalıdır)
   - **Slug** — marka sayfası için URL yolu (adından otomatik doldurulur; özelleştirebilirsiniz)
   - **Açıklama** — marka sayfasında görünecek kısa bir açıklama
   - **Web Sitesi** — markanın resmi web sitesi URL'si (isteğe bağlı — marka sayfasında bir bağlantı olarak gösterilir)
4. Marka varlıklarını ekleyin:
   - **Logo** — marka logosu resmi, marka listelerinde ve marka sayfasında kullanılır
   - **Bannerviz** — marka sayfasının üst kısmında görünecek geniş bir bannerviz
5. **Marka Hikayesi** (isteğe bağlı) yazın — markanın tarihi, değerleri veya ne kadar özel olduğu hakkında daha uzun bir editöryel metin. Bu, markanın mağaza ön yüzü sayfasında görünür ve ilgilenen müşterilere marka hikayesini anlatmak için etkili bir yoldur.
6. **SEO** alanlarını yapılandırın:
   - **Meta Başlık** — arama motoru sonuçlarında görünen sayfa başlığı
   - **Meta Açıklama** — başlığın altındaki kısa açıklama
7. Gösterim seçeneklerini ayarlayın:
   - **Marka Sayfasını Göster** — markanın genel erişime açık bir sayfası olup olmadığını kontrol eder. İşaretlemeyi kaldırarak markayı mağazadan gizleyebilir, ancak sistemde tutabilirsiniz.
   - **Aktif mi?** — markanın ürün atamasına ve mağazada görünür olmasına izin verip vermediğini kontrol eder
   - **Öne Çıkan mı?** — markayı temanızdaki öne çıkan yerlerde (örneğin, ana sayfa logosu satırı) gösterir
8. **Kaydet**'e tıklayın

## Ürünleri Bir Markaya Atama

Markalar, ürün kayıtlarında bireysel olarak atanır, marka yönetimi sayfasından değil. Bir markayı bir ürüne atamak için:

1. **Katalog > Ürünler** menüsüne gidin ve ürünü açın
2. Ürün formunda **Marka** alanını bulun
3. Uygun markayı arayın ve seçin
4. Ürünü kaydedin

Bir marka atandıktan sonra, ürün o markanın mağaza ön yüzü sayfasında otomatik olarak görünür.

## Mağaza Ön Yüzündeki Marka Sayfaları

**Marka Sayfasını Göster** seçeneği etkin olan her marka, `/brand/{slug}/` adresinde kendi sayfasına sahiptir. Sayfa şu öğeleri görüntüler:

- Marka logosu ve bannerviz
- Marka adı ve açıklaması
- Marka hikayesi (eğer sağlanırsa)
- Markanın web sitesine bağlantı (eğer sağlanırsa)
- O markaya atanan tüm aktif ürünler

Müşteriler, bir ürün sayfasındaki marka adını tıklayarak veya navigasyonunuzda veya sayfa oluşturucunuzda oluşturduğunuz bağlantılar aracılığıyla marka sayfalarına ulaşabilir.

## Marka Sayfaları için SEO

Her marka için **Meta Başlık** ve **Meta Açıklama** alanlarını doldurmak, marka sayfalarının arama sonuçlarında iyi görünmesine yardımcı olur. Etkili marka SEO başlıkları genellikle marka adını ve markanın ne satıyorunu birleştirmektedir:

| Marka | İyi Meta Başlığı |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

Eğer SEO alanlarını boş bırakırsanız, temanız marka adına geri döner.

### Otomatik SEO Oluşturma

Bir marka üzerinde **SEO Otomatik Oluşturulmuş** seçeneği etkinse, Spwig marka kaydedildiğinde meta başlık ve açıklama içeriğini otomatik olarak oluşturur.

Bu, birçok markası olan mağazalar için pratik bir özelliktir ancak tam olarak kullanılan ifadeler üzerindeki kontrolünüzü azaltır.

Otomatik oluşturma anahtarını devre dışı bırakarak doğrudan alanlara yazarak oluşturulan içeriği her zaman geçersiz kılabilirsiniz.

## Öne Çıkan Markalar

**Öne Çıkan** bayrağı, temalar tarafından marka logolarının özelleştirilmiş bir satır ya da ızgara olarak gösterilmesi için kullanılır — genellikle anasayfada. Herhangi bir zamanda yalnızca çok az sayıda marka öne çıkarılmalıdır; tema belgelerinizi inceleyerek hangi sayıdaki öne çıkarılan markanın en iyi şekilde gösterildiğini öğrenin.

## İpuçları

- Bir marka logosu olarak PNG veya WebP formatında şeffaf arka plana sahip bir dosya yükleme — tema içindeki herhangi bir arka plan renginde temiz bir şekilde görünecektir
- Bilinmeyen markalar için bile etkileyici bir marka hikayesi yazın; marka hakkında bilgi edinmeyen müşteriler, ürünün kendileri için uygun olup olmadığını karar vermek için bağlamı değerlidir
- Belirli markalara yönelik kampanyalar düzenliyorsanız, Spwig'deki marka adının tam olarak eşleştiğinden emin olun — kampanyalar ürünlerdeki marka ilişkisini kullanarak elverişlilik durumunu belirler
- Ürünlerini artık taşıyamayacağınızda bir markayı devre dışı bırakmak yerine silmeyin — silme işlemi, ilgili tüm ürünlerden marka referansını kaldırır, ancak devre dışı bırakma geçmişini korur
- **Öne Çıkan** bayrağını az kullanın; anasayfada 20 marka logosu gösteren bir sayfa, 6–8 dikkatle seçilmiş marka logosu gösteren bir sayfaya göre etkisini kaybeder