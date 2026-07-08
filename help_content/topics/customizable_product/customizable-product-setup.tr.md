---
title: Özel Ürün Kurulumu
---

Bu kılavuz, özel bir ürünün tam kurulum sürecini, ürünün oluşturulmasından başlayarak yüzeylerin, fiyatlandırmanın ve yükleme kısıtlamalarının yapılandırılması kadar tüm adımları adım adım size gösterir. Kılavuz boyunca iki uygulamalı örnek kullanılır: **özel bir tişört** (çok yüzeyli giyilebilir ürün) ve **özel bir afiş** (tek yüzeyli basım).

## Adım 1: Ürünü Oluştur

1. **Ürünler > Tüm Ürünler** menüsüne gidin ve **+ Ürün Ekle** butonuna tıklayın
2. **Ürün Türü** alanını **Özel Ürün** olarak ayarlayın
3. Ürün adı, açıklama, resimler ve fiyatlandırma gibi bilgileri herhangi bir ürün için girdiğiniz gibi doldurun
4. Ürünü kaydedin

Kaydetme işleminden sonra, ürün formunda yeni bir **Dizayn Editörü Kurulumu Aç** butonu görünür. Bu buton, bu ürün için görsel dizayn editörünü yapılandırmak üzere ayrılmış sayfaya yönlendirir.

## Adım 2: Dizayn editörü kurulumuna erişin

1. Yeni oluşturduğunuz ürünü admin panelinde açın
2. **Dizayn Editörü Kurulumu Aç** butonuna tıklayın (Özel Ürün bölümü içinde)
3. Kurulum sayfası, **Yüzeyler**, **Ayarlar** ve **Fiyatlandırma** olmak üzere üç sekme ile açılır

Kurulum sayfası, bu ürün için dizayn editörünün her şeyini tanımlamak için kullanılır.

## Adım 3: Dizayn yüzeylerini ekle

Bir yüzey, ürünün bir dizaynlama yüzeyini temsil eder. Her yüzeyi oluşturmak için **+ Yüzey Ekle** butonuna tıklayın.

### Tişört örneği: 3 yüzey

| Yüzey | Ad | Boyutlar | Dizayn alanı | Notlar |
|-------|----|---------|-------------|--------|
| 1 | Ön | 300 x 400 mm | Göğüs ortasında | Ana dizayn alanı |
| 2 | Arka | 300 x 400 mm | Arka üstünde | İkincil dizayn alanı |
| 3 | Sol Kol | 100 x 100 mm | Kol üstünde | Sadece küçük bir logoyu içerecek |

### Afis örneği: 1 yüzey

| Yüzey | Ad | Boyutlar | Dizayn alanı | Notlar |
|-------|----|---------|-------------|--------|
| 1 | Ön | 210 x 297 mm (A4) | Tam basma alanı | Tek yüzey, yüksek DPI |

### Her yüzeyi yapılandırma

Her yüzey için aşağıdaki yapılandırmaları yapabilirsiniz:

**Temel bilgiler:**
- **Ad** — Müşterilerin yüzey sekmesinde gördüğü isim (örneğin, "Ön", "Arka")
- **Slug** — URL'ye uygun tanımlayıcı, isimden otomatik olarak oluşturulur
- **Sıra Numarası** — Yüzeylerin görünme sırasını belirler (düşük numaralı olanlar önce gelir)

**Mockup resmi:**
- Mockup resim alanına tıklayarak Medya Kütüphanesi'ni açın ve bu yüzeyi gösteren bir ürün resmini seçin
- Ürünün doğru açısıyla çekilmiş yüksek kaliteli bir resim kullanın

**Dizayn alanı konumlandırma:**
- Bir mockup resmi seçtikten sonra, önizleme üzerinde bir dikdörtgen örtü görünür
- **Sürükle** ile örtüyü, mockup üzerinde dizayn alanı olacak yere konumlandırın
- **Boyutlandır** ile örtünün kenarlarını sürükleyerek dizayn alanının sınırlarını tanımlayın
- Alan, yüzdelik bazlı koordinatlar olarak saklanır, bu nedenle her ekran boyutuna göre ölçeklenebilir

Dizayn alanı, editörün müşteri dizaynının ürün resminde nerede görüneceğini tam olarak belirtir. Gerçek basma alanına uygun şekilde dikkatlice konumlandırın.

**Fiziksel boyutlar:**
- **Genişlik** ve **Yükseklik** — Dizayn alanının gerçek boyutları
- **Birim** — Milimetre, inç veya piksel
- Bu boyutlar, dizayn kanvasının boyut oranını belirler ve basım DPI hesaplamasında kullanılır

**Basım ayarları:**
- **Minimum DPI** — Kabul edilebilecek en düşük nokta başına inç sayısı. Müşterilerin yüklü resimleri bu değerin altına düştüğünde bir uyarı görür. Varsayılan: 150
- **Önerilen DPI** — En iyi basım kalitesi için ideal çözünürlük. Varsayılan: 300
- **Bleed (mm)** — Basım bleed için dizayn alanının dışındaki ekstra marj. Bleed gerekmezse 0 olarak ayarlayın (giyilebilir ürünler için yaygın), profesyonel basım ürünler için 3 mm olarak ayarlayın
- **Maksimum Renk Sayısı** — Ekran basımı için renk sayısını sınırlayabilirsiniz. Boş bırakın sınırsız (dijital basım için)
- **Arka Plan Rengi** — Varsayılan kanvas arka plan rengi

### Tişört vs. afis basım ayarları

| Ayar | Tişört | Afis |
|------|------|-----|
| Minimum DPI | 150 | 200 |
| Önerilen DPI | 300 | 300 |
| Bleed | 0 mm | 3 mm |
| Maksimum Renk Sayısı | 6 (ekran basımı) | Boş (sınırsız) |
| Arka Plan Rengi | Giyilebilir ürünün rengine uyu | `#ffffff` (beyaz) |

## Adım 4: Yüzey bazlı kısıtlamalar

Her yüzey, küresel özellik ayarlarını geçersiz kılabilir. Bu, farklı yüzeylerde farklı araçların kullanılmasına izin verir.

Kısıtlama seçenekleri:

| Ayar | Seçenekler | Açıklama |
|---------|---------|-------------|
| **Metin Ekleme İzin Ver** | Miras al / Evet / Hayır | Müşterilerin bu yüzeye metin ekleyebilip ekleyemeyeceğini belirler |
| **Resim Yükleme İzin Ver** | Miras al / Evet / Hayır | Müşterilerin bu yüzeye resim yükleyebilip ekleyemeyeceğini belirler |
| **Küçük Resim İzin Ver** | Miras al / Evet / Hayır | Müşterilerin bu yüzeyde küçük resim kullanıp kullanamayacağını belirler |
| **Maksimum Eleman Sayısı** | Sayı veya boş | Bu yüzeyde izin verilen maksimum tasarım öğesi sayısı |

**Miras al** olarak ayarlandığında, yüzey küresel ayarlarda yapılandırılanları kullanır (Adım 6). **Evet** veya **Hayır** olarak ayarlandığında, bu belirli yüzey için küresel ayarı geçersiz kılar.

### Örnek: T-shirt kol yüzeyi kısıtlaması

T-shirt'in kol yüzeyi için, sadece küçük bir logoyu özelleştirmek isteyebilirsiniz:

| Ayar | Değer | Neden |
|---------|-------|--------|
| Metin Ekleme İzin Ver | Hayır | Okunabilir metin için çok küçük |
| Resim Yükleme İzin Ver | Evet | Küçük bir logo yükleme izni ver |
| Küçük Resim İzin Ver | Hayır | Basit tut |
| Maksimum Eleman Sayısı | 1 | Sadece bir logo |

Ön ve arka yüzeyler **Miras al** olarak kalır, küresel ayarlarda tanımlanmış tüm araçlara izin verir.

### Örnek: Poster kısıtlaması

Bir poster için, genellikle sadece bir yüzey olduğundan ve tüm araçların kullanılması gereken, tüm yüzeyler küresel yapılandırmadan miras alınır. Her yüzey için geçersizlikler gerekmez.

## Adım 5: Yükleme kısıtlamalarını yapılandırın

**Ayarlar** sekmesinde, müşterilerin dosyaları nasıl yükleyebileceğini yapılandırın:

| Ayar | Açıklama | T-shirt örneği | Poster örneği |
|---------|-------------|-----------------|----------------|
| **Maksimum Yükleme Boyutu** | Yükleme başına maksimum dosya boyutu | 10 MB | 20 MB |
| **Yüzey Başına Maksimum Yükleme Sayısı** | Yüzey başına kaç resim | 5 | 3 |
| **İzin Verilen Yükleme Türleri** | Kabul edilen dosya formatları | JPG, PNG, WebP | JPG, PNG, WebP |

Yazdırma ürünlerinde müşterilerin yüksek çözünürlüklü resim yüklemesi gereken durumlarda, daha büyük dosya boyutu sınırları önerilir.

## Adım 6: Düzenleyici ayarları

**Ayarlar** sekmesinde, küresel düzenleyici davranışını yapılandırın:

**Düzenleyici Modu:**
- **Kanvas Düzenleyici** — Canvastaki canlı önizlemesi olan tam görsel düzenleyici. Çoğu ürün için önerilir.
- **Basit Form** — Temel özelleştirmeler için geleneksel form alanları (örneğin, sadece gravür metni).

**Özellik anahtarları (küresel varsayılanlar):**
- **Metin Ekleme İzin Ver** — Müşterilerin metin öğeleri ekleyebilmesine izin ver
- **Resim Yükleme İzin Ver** — Müşterilerin kendi resimlerini yükleyebilmesine izin ver
- **Küçük Resim İzin Ver** — Müşterilerin küçük resim kütüphanesini tarayıp kullanmasına izin ver

Bu küresel ayarlar, yüzey bazlı kısıtlamalar (Adım 4) tarafından geçersiz kılınmadıkça tüm yüzeyler için geçerlidir.

## Adım 7: Fiyatlandırma yapılandırması

**Fiyatlandırma** sekmesinde, ürünün temel fiyatına eklenen tasarım ücretlerini ayarlayın:

| Ücret | Açıklama |
|-----|-------------|
| **Temel Tasarım Ücreti** | Herhangi bir özelleştirme uygulandığında eklenen sabit ücret |
| **Yüzey Başına Ücret** | İlk yüzeyden sonra kullanılan her yüzey için ek ücret |
| **Yükleme Başına Ücret** | Müşteri tarafından yüklenen her resim için ücret |
| **Metin Başına Ücret** | Eklenen her metin öğesi için ücret |

### Örnek: T-shirt fiyatlandırması

| Ücret | Tutar | Neden |
|-----|--------|-----------|
| Temel Tasarım Ücreti | 5,00 $ | Herhangi bir özel sipariş için kurulum maliyetini kapsar |
| Yüzey Başına Ücret | 2,00 $ | Ekstra her yüzey baskı maliyetini ekler |
| Yükleme Başına Ücret | 1,00 $ | Özel resimlerin işlenmesi gerekir |
| Metin Başına Ücret | 0,50 $ | Metin, resimlerden daha basit üretilir |

**Hesaplama örneği:** Bir müşteri, bir t-shirt'in ön yüzeyinde metin ve arka yüzeyinde bir logo tasarlar:
- Temel tasarım ücreti: 5,00 $
- 1 ekstra yüzey (arka): 2,00 $
- 1 yüklenecek logo: 1,00 $
- 1 metin öğesi: 0,50 $
- **Toplam tasarım ücreti: 8,50 $** (ürünün temel fiyatına eklenir)

### Örnek: Poster fiyatlandırması


| Ücret | Tutar | Sebep |
|-----|--------|-----------|
| Temel Tasarım Ücreti | $0.00 | Temel ücret yok — ürün fiyatı bunu kapsar |
| Yüzey Başına Ücret | $0.00 | Tek yüzey, uygunsuz |
| Yükleme Başına Ücret | $2.00 | Yüksek çözünürlüklü işleme |
| Metin Başına Ücret | $0.00 | Metin temel deneyimde dahildir |

**Hesaplama örneği:** Bir müşteri, 2 yüklenecek fotoğraf ve 3 metin öğesi ile bir afiş oluşturur:
- Temel tasarım ücreti: $0.00
- 2 yüklenecek fotoğraf: $4.00
- 3 metin öğesi: $0.00
- **Toplam tasarım ücreti: $4.00**

Tasarım ücreti, müşteri öğeler eklerken anlık olarak gösterilir, bu da onların sepete eklemeyi yapmadan önce her ekleme üzerindeki maliyet etkisini görebilmelerini sağlar.

## Genel bakışta ayar karşılaştırması

| Özellik | Özel T-Shirt | Özel Afis |
|--------|---------------|---------------|
| Yüzeyler | 3 (ön, arka, kol) | 1 (ön) |
| Mockup resimleri | 3 ürün fotoğrafı | 1 ürün fotoğrafı |
| Bölge konumlandırması | Göğüs/arka/kol bölgeleri | Tam yazdırılabilir alan |
| Boyutlar | 300x400mm, 100x100mm | 210x297mm (A4) |
| Minimum DPI | 150 | 200 |
| Kenar boşluğu | 0 mm | 3 mm |
| Maksimum renk sayısı | 6 | Sınırsız |
| Yüzey başına kısıtlamalar | Kol kısıtlaması | Hiçbir gereksinim yok |
| Fiyatlandırma modeli | Temel + yüzey + yükleme + metin | Yükleme başına ücretler |

## İpuçları

- Ayarları tamamladıktan sonra her zaman müşteri perspektifinden tasarım editörünü test edin. Mağazanın ürün sayfasına gidin ve metin ekleyin, bir resim yükleme ve yüzeyleri değiştirme deneyin.
- Gerçek ürün görünümünü yansıtan mockup resimlerini her zaman yükleyin. T-shirt'ler için her açı ayrı ayrı fotoğraf alın. Afisler için temiz bir yatay fotoğraf veya bir çerçeve mockup kullanın.
- Tasarım alanını konservatif şekilde konumlandırın — daha küçük bir alan tanımlamak, tasarımların dikişler veya kenarlara girmesinden daha iyi olur.
- Basım yönteminize göre minimum DPI'yi ayarlayın: 150 ekran basımı için, 200 standart dijital basımı için, 300 yüksek kaliteli ofset basımı için.
- Basım sonrası kesilecek her ürün için 3 mm kenar boşluğu kullanın (afisler, iş kartları, broşürler). Tasarım mevcut bir yüzeye uygulanacak ürünlerde (t-shirt'ler, fincanlar, telefon kılıfı) kenar boşluğunu 0 olarak ayarlayın.
- Basit bir fiyatlandırma ile başlayın ve müşteri geri bildirimlerine göre ayarlayın. Birçok satıcı, sadece temel bir tasarım ücreti ile başlar ve daha sonra öğe başına ücretleri ekler.