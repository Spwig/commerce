---
title: Ürün Koleksiyonları
---

Koleksiyonlar, mağazanızın ön yüzünde ürünleri gruplamak için kullanılır. Kategoriler gibi, tüm kataloğunu kalıcı bir hiyerarşiye organize etmek yerine, koleksiyonlar belirli bir amaç için oluşturduğunuz esnek ve seçilmiş gruplamalardır. Bir koleksiyon yeni ürünlerin vurgulanması, mevsimsel kampanyalar için ürünleri göstermek veya en iyi satanlar için el ile seçilmiş bir koleksiyon sunmak gibi amaçlar için kullanılabilir.

**Katalog > Koleksiyonlar** menüsüne giderek koleksiyonlarınızı yönetebilirsiniz.

## Koleksiyonlar vs. kategoriler

Her iki kategori ve koleksiyon da ürünleri gruplar, ama farklı amaçlar için kullanılır:

| | Kategoriler | Koleksiyonlar |
|---|---|---|
| **Amaç** | Kalıcı katalog yapısı | Esnek, seçilmiş gruplamalar |
| **Hiyerarşi** | Evet — iç içe ebeveyn/çocuk yapısı | Hayır — düz gruplamalar |
| **Gruba göre ürün sayısı** | Her ürün bir kategoriye aittir | Bir ürün birçok koleksiyonda görülebilir |
| **Tipik kullanım** | Mağaza navigasyon menüsü, bölüm bazlı tarif | Ana sayfalar, kampanyalar, vurgulanan setler |

Kategorileri "mağazanızın nasıl organize edildiğini" belirtmek için kullanın ve koleksiyonları "şimdi vurgulamak istediğiniz şey" için kullanın.

## Koleksiyon türleri

Bir koleksiyon oluştururken, ürün listesini nasıl yönetmek istediğinize uygun bir tür seçin:

| Tür | Ürünlerin nasıl eklendiği |
|---|---|
| **El ile Seçim** | Ürünlerin hangilerinin görüneceğini tek tek seçersiniz |
| **Otomatik Kurallar** | Ürünler, tanımladığınız kriterlere göre otomatik olarak eklenir |
| **Öne Çıkan Ürünler** | El ile yönetilen, düzenlenmiş bir seçim |
| **Mevsimsel** | Zaman bazlı bir seçim, genellikle kampanyalar için el ile yönetilir |

El ile ve Öne Çıkan türleri, size kesin kontrol sağlar. Otomatik koleksiyonlar, kataloğunuza büyüdükçe sürekli bakım olmadan büyüyebilir.

## Koleksiyon oluşturma

1. **Katalog > Koleksiyonlar** menüsüne gidin
2. **+ Koleksiyon Ekle**'ye tıklayın
3. **Temel Bilgiler** bölümünü doldurun:
   - **Ad** — koleksiyonun mağazanızda nasıl görüneceğini belirleyen ad
   - **Slug** — koleksiyon sayfası için URL yolu (adından otomatik doldurulur; özelleştirebilirsiniz)
   - **Açıklama** — koleksiyonun ön yüz sayfasında görünen açıklama
4. Bir **Koleksiyon Türü** seçin
5. Ürünleri ekleyin:
   - **El ile Seçim** ve **Öne Çıkan Ürünler** türleri için: **Ürünler** alanını kullanarak ürünleri ara ve ekleyin
   - **Otomatik** türü için: **Otomatik Kriterler** alanına kriterleri tanımlayın
6. Görseller yükleyin:
   - **Görsel** — listeleme sayfalarında ve küçük önizlemede kullanılan ana koleksiyon görseli
   - **Banner Görseli** — koleksiyon sayfasının üst kısmında görünen daha geniş bir banner görseli
7. **SEO** alanlarını yapılandırın (isteğe bağlı ama önerilir):
   - **Meta Başlık** — arama sonuçlarında görünen sayfa başlığı
   - **Meta Açıklama** — başlığın altında görünen açıklama
8. **Gösterim Ayarlarını** yapılandırın:
   - **Aktif mi?** — koleksiyonun mağazanızda görünür olup olmadığını kontrol eder
   - **Öne Çıkan mı?** — koleksiyonu şablonunuzda öne çıkarılan yerlerde göstermek için işaretler
   - **Sıra Numarası** — listeleme sayfalarında koleksiyonların görünen sırasını kontrol eder (düşük numaralar önce görünür)
9. **Kaydet**'e tıklayın

## Bir koleksiyona ürün ekleme

El ile koleksiyonlar için, **Ürünler** otomatik tamamlama alanını kullanarak kataloğunuza göre ürünleri ara ve seçin. Gerekirse ne kadar çok ürün ekleyebilirsiniz — herhangi bir sınır yoktur.

Ürünler aynı anda birden fazla koleksiyona ait olabilir. Örneğin, bir ürün hem "Yaz Kampanyası" koleksiyonunuzda hem de "En Çok Satılanlar" koleksiyonunuzda olabilir ve bu hiçbir çelişki yaratmaz.

## Koleksiyonları mağazanızda gösterme

Her koleksiyon, otomatik olarak kendi sayfasını `/collection/{slug}/` adresinde alır. Navigasyon menüsünden, sayfa oluşturucudan veya promosyon bannerlarından koleksiyon sayfalarına bağlantı kurabilirsiniz.

**Öne Çıkan** bayrağı, şablonunuz tarafından hangi koleksiyonların öne çıkarılan yerlerde görüneceğini belirlemek için kullanılır — örneğin, anasayfada vurgulanan koleksiyonların bir ızgara düzeni. Şablon belgelerinizi kontrol ederek, öne çıkarılan koleksiyonların nasıl görüntülendiğini tam olarak anlayabilirsiniz.

## Koleksiyon görünürlüğünü yönetme

- **Aktif mi?** koleksiyon sayfasının genel erişilebilir olup olmadığını kontrol eder.

Aktif olmayan bir koleksiyon, müşterilerden gizlenir ancak admin'de korunur ve daha sonra tekrar etkinleştirebilirsiniz.
- **Sıra Numarası**, koleksiyonların listeleme sayfalarında görünme sırasını belirler.

Listede öncelikle görünmesini istediğiniz koleksiyonlara daha düşük numaralar atayın.

## Koleksiyonlar için SEO

Her koleksiyonun kendi **Meta Başlık** ve **Meta Açıklama** alanları vardır. Bu alanlar, kimse koleksiyon sayfanızı bulduğunda arama motoru sonuçlarında ne görüleceğini kontrol eder. Bu alanları boş bırakırsanız, temanız genellikle koleksiyon adını ve açıklamasını kullanır.

İyi koleksiyon SEO başlıkları açıklayıcı ve spesifik olmalıdır:
- "2026 Yaz Elbiseleri — Çiçekli & Hafif Stiller" "Yaz Koleksiyonu" dan daha iyi performans gösterir
- "Erkek Koşu Ayakkabıları — Hafif & Havaalanı" "Koşu Ayakkabıları" dan daha iyi performans gösterir

## İpuçları

- Koleksiyon isimlerini kısa ve net tutun — bu isimler, mağazanızın navigasyonunda sayfa başlıkları ve bağlantı metni olarak görünür
- Mevsimsel veya kampanya koleksiyonları oluşturun ve başlangıç ve bitiş planları ile birlikte kullanın: koleksiyonu oluşturun, kampanya başladığında etkinleştirin ve kampanya bittiğinde (silmek yerine) devre dışı bırakın, böylece daha sonra başvurabilirsiniz
- **Sıra Numarası** alanını dikkatle ayarlamak değerlidir — varsayılan olarak tüm koleksiyonlar için 0'dır, bu da alfabetik sıralamaya neden olur. Belirli numaralar atayarak hangi koleksiyonların en öne çıkacağına kontrol edebilirsiniz
- Ürünü olmayan bir koleksiyon, müşterilere boş bir sayfa gösterir — etkinleştirmeden önce ürünler ekleyin veya koleksiyonun hazır olana kadar devre dışı bırakın
- Gerçekten vurgulamak istediğiniz koleksiyonlar için yalnızca **Öne Çıkan** bayrağını kontrol edin; çoğu tema, yalnızca birkaç koleksiyon için öne çıkan yuvaları ayırır ve çok fazla koleksiyon işaretlenirse görüntü yoğun görünebilir