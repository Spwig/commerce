---
title: Özel Ürünler için Kullanılabilir Kliptart ve Yazı Tipleri
---

Tasarım editörü, müşterilere sunabileceğiniz iki tür yaratıcı varlığa sahiptir: **kliptart** (tasarımlarına ekleyebilecekleri hazırdan grafikler) ve **özel yazı tipleri** (standart sistem yazı tipleri dışında). İyi bir şekilde derlenmiş bir varlık kütüphanesi, editörün daha faydalı hale gelmesine yardımcı olur ve müşterilerin daha iyi tasarımlar oluşturmasına olanak tanır.

## Kliptart Kütüphanesi

Kliptart, müşterilere tek bir tıklamayla tasarımlarına ekleyebilecekleri hazır grafiklerin bir kütüphanesini sunar. İkonlar, kenarlıklar veya dekoratif grafikler gibi ortak öğeler için müşterilerin kendi resimlerini bulup yüklemelerini istemek yerine, onlara hazırdan kullanıma hazır grafikler sunarsınız.

### Kliptart Kategorileri Oluşturma

Kliptart, müşterilerin tarayabileceği kategorilere ayrılmıştır. Kategoriler, müşterilerin ihtiyaçlarını hızlıca bulmalarına yardımcı olur.

1. **Özel Ürünler > Kliptart Kategorileri** kısmına gidin
2. **+ Kliptart Kategorisi Ekle**'ye tıklayın
3. Aşağıdakileri doldurun:
   - **Kategori Adı** — Müşterilerin göreceği ad (örneğin, "Spor", "Kenarlıklar", "Bayram")
   - **Slug** — Adından otomatik olarak oluşturulur
   - **İkon** — Kategori sekmesi için bir Font Awesome ikon sınıfı (örneğin, `fas fa-football-ball`)
   - **Sıra Numarası** — Kategorilerin editörde görüneceği sırayı kontrol eder
4. **Kaydet**'e tıklayın

**Bir t-shirt mağazası için örnek kategoriler:**

| Kategori | İkon | Örnek Kliptart |
|----------|------|-----------------|
| Spor | `fas fa-football-ball` | Takım logoları, spor ekipmanları, spor sembolleri |
| Humor | `fas fa-laugh` | Memeler, komik alıntılar, çizgi karakterler |
| Doğa | `fas fa-leaf` | Hayvanlar, çiçekler, manzaralar |
| Geometrik | `fas fa-shapes` | Desenler, soyut şekiller, halka desenleri |

**Bir baskı/afis mağazası için örnek kategoriler:**

| Kategori | İkon | Örnek Kliptart |
|----------|------|-----------------|
| Kenarlıklar | `fas fa-border-all` | Dekoratif çerçeveler, köşe süslemeleri |
| Mevsimsel | `fas fa-snowflake` | Bayram ikonları, mevsimsel motifler |
| İkonlar | `fas fa-icons` | Yıldızlar, kalpler, oklar, onay işaretleri |
| Arka Planlar | `fas fa-image` | Dokular, gradyanlar, desenler |

### Kliptart Varlıkları Ekleme

Her kliptart varlığı, müşterilerin kanvasına yerleştirebileceği bir resim dosyasıdır (PNG veya SVG).

1. **Özel Ürünler > Kliptart Varlıkları** kısmına gidin
2. **+ Kliptart Varlığı Ekle**'ye tıklayın
3. Aşağıdakileri doldurun:
   - **Ad** — Açıklamalı bir ad (örneğin, "Altın Yıldız", "Futbol Kaskı")
   - **Kategori** — Kliptart kategorilerinizden birini seçin
   - **Resim Varlığı** — Medya Kütüphanesini açmak için tıklayın ve resim dosyasını seçin veya yükleyin
   - **Kapsam** — Kullanılabilirliği seçin (aşağıdaki açıklamaları görün)
   - **Etiketler** — Bu kliptart için aranabilir anahtar kelimeler (örneğin, `['yıldız', 'altın', 'dekorasyon']`)
   - **Sıra Numarası** — Kategorideki konumu kontrol eder
4. **Kaydet**'e tıklayın

### Kliptart Kapsamını Anlamak

Her kliptart varlığı, nerede kullanılabilir olduğunu kontrol eden bir kapsam içerir:

| Kapsam | Açıklama | Kullanım Durumu |
|-------|-------------|----------|
| **Tüm Ürünler İçin Kullanılabilir** | Her özelleştirilebilir ürün için kliptart tarayıcısında görünür | Yıldızlar, kenarlıklar ve ortak ikonlar gibi genel amaçlı grafikler |
| **Yalnızca Belirli Bir Ürün İçin** | Sadece bir seçilmiş ürün için görünür | Ürün özel grafikleri gibi marka logoları veya ürün temalı sanat eserleri |

Çoğu varlık için **Tüm Ürünler İçin Kullanılabilir** kullanın. Ürün özel kapsamı, sadece bir ürün bağlamında anlamlı olan varlıklar için ayrılmıştır — örneğin, bir takımla ilgili ürünler için takım özel logoları.

### Kliptart Dosya Kılavuzu

- **Format:** Raster grafikler için PNG, vektör grafikler için SVG kullanın. SVG dosyaları, kalite kaybı olmadan ölçeklenebilir, bu nedenle müşterilerin büyük ölçüde yeniden boyutlandırabileceği kliptartlar için idealdir
- **Çözünürlük:** İyi baskı kalitesi için PNG dosyaları en az 500x500 piksel olmalıdır
- **Arka Plan:** Saydam arka planlar (alpha kanalı olan PNG veya SVG) kullanın, böylece kliptart tasarım ile doğal bir şekilde birleşir
- **Dosya boyutu:** Editörde hızlı yükleme için her kliptart dosyasını 500KB'ın altında tutun

## Özel Yazı Tipleri

Özel yazı tipleri, tasarım editöründeki yazı tipi seçicisini standart sistem yazı tipleri ötesine taşır.

Bu, markanız veya ürün stilinizle eşleşen özelleştirilmiş tipografi sunmanıza olanak tanır.

### Özelleştirilmiş bir font ekleyin

1. **Özelleştirilebilir Ürünler > Özelleştirilmiş Fontlar**'a gidin
2. **+ Özelleştirilmiş Font Ekle**'ye tıklayın
3. Aşağıdakileri doldurun:
   - **Font Adı** — Font seçici içinde görünen görüntü adı (örneğin, "Playfair Display")
   - **Font Ailesi** — İçinde kullanılan CSS font-family adı (örneğin, `PlayfairDisplay`)
   - **Normal** — Medya Kütüphanesi üzerinden WOFF2 veya TTF uzantılı normal ağırlık font dosyasını yüklemek için tıklayın
   - **Kalın** — Opsiyonel kalın ağırlık varyasyonu
   - **İtaliyata** — Opsiyonel italik varyasyonu
   - **Kalın İtaliyata** — Opsiyonel kalın italik varyasyonu
4. **Kaydet**'e tıklayın

**Normal** ağırlık, özelleştirilmiş fontlar için zorunludur. Kalın, italik ve kalın italik varyasyonları isteğe bağlıdır — sağlanmazsa, tarayıcı normal fonttan bu stilleri senetirleymeye çalışacaktır, ancak sonuçlar özel font dosyalarından elde edilenler kadar iyi görünmeyebilir.

### Sistem fontları vs. özelleştirilmiş fontlar

Çoğu cihazda önceden yüklenmiş olan sistem fontlarını da kaydedebilirsiniz:

1. Yeni bir özelleştirilmiş font girişi ekleyin
2. **Sistem Fontu**'nu işaretleyin
3. CSS'te görünen font ailesi adını tam olarak girin (örneğin, `Georgia`, `Courier New`)
4. Sistem fontları için dosya yükleme gerekmez

Sistem fontları, zaten müşteri cihazında olduğundan anında yüklenir. Özelleştirilmiş yüklenebilir fontlar önce indirilmesi gerekir, bu da font ilk seçildiğinde küçük bir gecikmeye neden olur.

### Ürün türüne göre font önerileri

**T-shirt ve giyilebilir ürünler için:**
- En iyi etkileyici fontlar: Impact, Anton, Bebas Neue, Oswald
- Dokuma yüzeylerde en okunabilir olanlar: Blok harfler ve sans-serif fontlar
- Dokuma yüzeylerde iyi yazdırılmayabilecek ince veya hassas fontlardan kaçının

**Posterler ve basılı ürünler için:**
- Formal tasarımlar için zarif serif fontlar: Playfair Display, Merriweather, Lora
- Davetler ve kartlar için el yazısı fontları: Great Vibes, Dancing Script, Pacifico
- Modern tasarımlar için temiz sans-serif: Montserrat, Raleway, Open Sans

### Font dosya formatları

| Format | Uzantı | Öneri |
|--------|-----------|----------------|
| WOFF2 | `.woff2` | Tercih edilir — en küçük dosya boyutu, en hızlı yükleme |
| TrueType | `.ttf` | İyi bir alternatif — yaygın uyumluluk |

WOFF2 dosyaları genellikle TTF dosyalarından 30-50% daha küçük olduğundan, müşteri editöründe daha hızlı yüklenebilir. WOFF2 kullanılabilirse onu kullanın.

## Varlıklar kütüphanesini yönetme

### Müşteriler için organize etme

Varlıkların editördeki sırası, kategoriler ve bireysel varlıklar üzerindeki **Sıra Numarası** alanıyla kontrol edilir. Düşük numaralar önce görünür. Bu şu amaçlarla kullanılabilir:
- En popüler klipart kategorilerinizi en başa koyun
- Her kategoride en iyi ve en esnek klipartları en üst sıraya yerleştirin
- En çok kullanılan fontları en öne koyun

### Kütüphaneyi güncel tutma

- Tatiller öncesi mevsimsel klipart ekleyin (Halloween, Christmas, Valentine's Day) ve sonra devre dışı bırakın
- **Aktif** onay kutusunu kullanarak varlıkları silmeden geçici olarak gizleyin
- Müşterilerin en çok kullandığı klipart ve fontları izleyin ve bu kategorileri genişletin

## İpuçları

- Küçükten başlayın — 3-4 kategori arasında 20-30 adet yüksek kaliteli klipart varlığı, yüzlerce orta kaliteli seçeneğe göre daha iyidir. Müşterilerin ne istediğini öğrendikçe her zaman daha fazlasını ekleyebilirsiniz.
- Klipart için mümkün olduğunca SVG formatını kullanın. SVG dosyaları daha küçük, her boyuta mükemmel şekilde ölçeklenebilir ve rastgele görüntilere göre daha net basım üretir.
- Yüklenecek her fontu tasarım editöründe test edin, tüm karakterlerin doğru şekilde işlendiğinden emin olun, özellikle müşterilerin birden fazla dil kullanıyorsa özel karakterler ve aksanlar için.
- Klipartları kapsamlı şekilde etiketleyin — müşteriler anahtar kelimelere göre arama yapar, bu nedenle "altın", "yıldız", "beş köşeli", "dekorasyon" gibi açıklayıcı etiketler, doğru varlığı hızlıca bulmalarına yardımcı olur.
- İlgili klipartları aynı kategoriye gruplayın. Takım ürünleri satıyorsanız, her spor türü için bir kategori oluşturun, tek bir "Spor" kategorisi yerine.
- Varlıklar kütüphanesini müşteri perspektifinden düzenli olarak inceleyin, mağazanın ön yüzünde tasarım editörünü ziyaret ederek.