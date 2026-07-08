---
title: Özel Elemanlar
---

Özel elemanlar, mağazanızın ihtiyaçlarına göre yeniden kullanılabilir sayfa inşaatı blokları oluşturmanıza olanak tanır. Sayfa inşaatı araçlarının mevcut araçlarını kullanarak bir elemanı görsel olarak tasarlayabilir ve ardından bunu canlı mağaza verileriyle - örneğin ürün isimleri, fiyatları veya görseller - bağlayabilirsiniz. Elemanı bir sayfaya yerleştirdiğinizde otomatik olarak gerçek içerikle doldurulur. Oluşturulduktan sonra özel elemanlar, yerleşik bloklarla birlikte sayfa inşaatının eleman kütüphanesinde görünür.

![Özel Elemanlar Kütüphanesi](/static/core/admin/img/help/custom-elements/custom-elements-list.webp)

## Özel elemanları ne zaman kullanmalısınız

Özel elemanlar, aynı düzeni tekrar tekrar oluşturmak zorunda olduğunuzda en değerlidir. Her sayfada "öne çıkan ürün kartı" gibi bir şeyi sıfırdan yeniden oluşturmak yerine, bunu bir kez özel eleman olarak oluşturup ihtiyaç duyduğunuz her yerde bırakabilirsiniz. Eleman veri bağlantılıysa, fiyatlar veya isimler değiştiğinde manuel güncellemeye gerek kalmadan mevcut ürün bilgilerini otomatik olarak çeker.

### Yaygın kullanım alanları:

- Ürün ismi, fiyat ve ana görseli gösteren ürün vurgu kartları
- Banner, başlık ve bağlantı ile kategori tanıtım blokları
- Logo ve açıklama ile marka sergileme panelleri
- Öne çıkan görsel, başlık ve özeti olan blog gönderisi özeti

## Yeni özel eleman oluşturma

1. **Tasarım > Özel Elemanlar**'a gidin
2. **+ Özel Eleman Ekle**'ye tıklayın
3. Spwig, hemen bir taslak eleman oluşturur ve **Görsel Oluşturucu**'yu açar - önce bir form doldurmanıza gerek yoktur
4. Görsel Oluşturucuda, mevcut sayfa inşaatı araçlarını kullanarak elemanın düzenini oluşturun
5. Tasarımı memnuniyetinizle yaptıktan sonra, yan panelde elemanın ayarlarını (isim, veri bağlaması, simge) yapılandırın
6. Elemanı kütüphaneye yayımlamaya hazırsanız **Aktif**'i açığa alın
7. Elemanı kaydedin

Eleman artık, atadığınız kategori altında sayfa inşaatının eleman panelinde kullanılabilir hale gelir.

## Görsel Oluşturucu

Görsel Oluşturucu, elemanınızı tasarlamak için ayrılmış bir kanvasdır. Standart sayfa inşaatı gibi çalışır ancak bir sayfa yerine tek bir eleman odaklıdır. Aşağıdakileri yapabilirsiniz:

- Alt elemanlar (metin blokları, görseller, kapsüller vb.) ekleyin ve düzenleyin
- Her alt elemanın stilini, boşluklarını ve düzenini ayarlayın
- Örnek verilerle elemanın nasıl görüneceğini önizleyin

Görsel Oluşturucudaki değişiklikler doğrudan eleman tanımına kaydedilir. Ayrı bir yayımlama aşaması yoktur - oluşturucuda kaydettikten sonra, elemanı zaten kullanan sayfalarda hemen güncellenir.

## Eleman ayarlarını yapılandırma

Her özel eleman şu ayarlara sahiptir:

| Alan | Açıklama |
|-------|-------------|
| **İsim** | Eleman kütüphanesinde gösterilen görüntü adı |
| **Slug** | İsimden otomatik olarak oluşturulan URL-güvenli tanımlayıcı |
| **Açıklama** | Bu elemanın ne için olduğunu anlatan isteğe bağlı not |
| **Hedef Model** | Veri bağlamak için kullanılacak mağaza modeli (aşağıya bakın) |
| **Simge** | Eleman kütüphanesinde gösterilen simge |
| **Kategori** | Elemanları kütüphanede gruplamak için |
| **Aktif** | Elemanın sayfa inşaatında kullanılabilir olup olmadığını belirtir |

## Veri bağlaması

Veri bağlaması, eleman düzeninizin parçalarını canlı mağaza verilerine bağlar. Sayfa düzenleyicisi, bir veri bağlantılı elemanı bir sayfaya yerleştirdiğinde, belirli bir kayıt (örneğin bir ürün) seçer ve tüm bağlanmış alanlar o kayıt üzerinden otomatik olarak doldurulur.

### Hedef model seçme

**Hedef Model** ayarı, elemanın hangi tür mağaza verisini görüntüleyebileceğini belirler. Kullanılabilir modeller:

| Model | Ne sağlar |
|-------|-----------------|
| **Ürün** | İsim, fiyat, stok durumu, görseller, açıklama, SKU, kategori, marka ve daha fazlası |
| **Kategori** | İsim, açıklama, görsel, banner, ürün sayısı ve URL |
| **Marka** | İsim, logo, açıklama, marka hikayesi ve URL |
| **Blog Yazısı** | Başlık, öz, öne çıkan görsel, yazar, yayın tarihi ve URL |

**Hedef Model** boş bırakılırsa, dinamik veri olmadan statik bir eleman oluşturursunuz. Statik elemanlar, dekoratif afişler veya düzen boşlukları gibi sabit tasarım bileşenleri için faydalıdır.

Görsel Oluşturucu içinde, öğenin görüntülemesi gereken model alanını seçerek bireysel alt öğeleri veri bağlantılı olarak işaretleyebilirsiniz.

Örneğin:
- Bir **metin** alt öğesi, **Ürün Adı**'na bağlanabilir, böylece seçilen ürünün adını gösterir
- Bir **görsel** alt öğesi, **Ana Görsel**'e bağlanabilir, böylece ürünün ana fotoğrafını gösterir
- Bir **metin** alt öğesi, **Fiyat**'a bağlanabilir, böylece her zaman geçerli fiyatı yansıtır

Her bağlama, bir öğe içerik alanı ile bir model alanı eşler. Bir özel öğeye birden fazla bağlama ekleyebilirsiniz — örneğin, bir metin bloğunu **Ürün Adı**'na ve aynı anda ayrı bir görsel bloğunu **Ana Görsel**'e bağlayabilirsiniz.

### Görsel küçük resim ön ayarları

Görsel bağlamaları için isteğe bağlı olarak bir **Küçük Resim Ön Ayarı** (örneğin `thumbnail` veya `medium`) belirtebilirsiniz. Bu, öğenin düzenine uygun boyuttaki görseli yüklemeyi kontrol eder ve sayfaların daha hızlı yüklenmesine yardımcı olur.

## Öğeleri devre dışı bırakma ve etkinleştirme

Bir öğeyi devre dışı bırakmak, öğe kütüphanesinden kaldırır ve yeni sayfalara eklenemeyecek hale getirir. Mevcut sayfalar, zaten bu öğeyi kullanıyorsa etkilenmez — öğe bu sayfalarda hala işlenir.

Devre dışı bırakmak için:
1. **Tasarım > Özel Öğeler**'e gidin
2. Öğe adını tıklayın
3. **Etkin** kutusunu kaldırın
4. Kaydedin

Etkinleştirmek için aynı adımları izleyin ve **Etkin** kutusunu tekrar işaretleyin.

## Öğe kütüphanesini filtreleme

Öğe listesi şu kriterlere göre filtreleme destekler:
- **Etkin / Etkin Değil** — yalnızca yayımlanmış veya yalnızca taslak öğeleri göster
- **Hedef Model** — öğenin bağlandığı modele göre filtrele
- **Kategori** — öğe kategorisine göre filtrele
- **Arama** — isim, slug veya açıklamaya göre arama yap

Bu, birçok özel öğeniz olduğunda ve belirli bir öğeyi hızlıca bulmanız gerektiğinde yardımcı olur.

## Örnek: Ürün vurgu kartı

**Hedef:** Ürünün ana görselini, adını ve fiyatını gösteren bir kart öğesi.

| Ayar | Değer |
|------|-------|
| Ad | Ürün Vurgu Kartı |
| Hedef Model | Ürün |
| Kategori | Ürünler |
| Simge | fas fa-box |

Görsel Oluşturucu'da ekleyin:
- **Görsel** öğesi, **Ana Görsel**'e bağlanmış ve küçük resim ön ayarı `medium` olan
- **Metin** öğesi, **Ürün Adı**'na bağlanmış
- **Metin** öğesi, **Fiyat**'a bağlanmış

Kaydedildikten ve etkinleştirildikten sonra, öğe sayfa oluşturucu altında **Ürünler** kategorisinde görünür. Bir sayfa düzenleyicisi bunu bir sayfaya eklerse, hangi ürünü vurgulayacağını seçer ve kart otomatik olarak doldurulur.

## İpuçları

- Öğelere amacını ve veri türünü içeren açıklayıcı isimler verin — örneğin, "Ürün Vurgu Kartı" yerine "Kart 1" — bu, kütüphanenin büyümesiyle birlikte kolayca navigasyon sağlar
- **Kategori** alanını ilgili öğeleri gruplamak için kullanın (Ürünler, Blog, Kampanyalar) — bu, sayfa düzenleyicileri için öğe kütüphanesini organize eder
- Bağlantılı veri öğelerini test etmek için bir taslak sayfaya ekleyin ve yayımlamadan önce gerçek bir kaydı seçin, böylece bağlama doğru bilgiyi çekip çekmediğini onaylayabilirsiniz
- Kullanmadığınız öğeleri devre dışı bırakın, silmeyin — bu, bunları hâlâ referans alan sayfaları korur ve daha sonra tekrar etkinleştirmenizi sağlar
- Hedef modeli olmayan statik öğeler, sitenin farklı bölümlerinde tekrar kullanılacak düzen desenleri için idealdir, örneğin ayırıcılar, CTA panelleri veya marka boşlukları