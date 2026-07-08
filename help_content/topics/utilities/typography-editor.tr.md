---
title: Tipografi Düzenleyici
---

Tipografi Düzenleyici, metin görünümü üzerinde tam kontrol sağlayabilmeniz için kullanılan bir stil yardımcı programıdır. Sayfa Oluşturucu, Başlık/Araç Çubuğu Oluşturucu veya Menü Oluşturucu'da herhangi bir öğenin tipografi özelliklerini düzenlediğinizde, bu panel bir浮动 panel olarak açılır.

![Tipografi Düzenleyici](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## Canlı Önizleme

Düzenleyici, panelin üst kısmında yan yana bir karşılaştırma gösterir:

| Kutu | Amacı |
|-----|---------|
| **Mevcut** | Mevcut tipografi stiliyle "The quick brown fox..." görüntüler |
| **Yeni** | Ayarları değiştikçe anında güncellenir ve uygulamadan önce sonucu gösterir |

Bu, herhangi bir değişiklik yapmadan önce ve sonra karşılaştırmayı sağlar.

## Tipografi Sekmesi

Düzenleyici açıldığında varsayılan olarak Tipografi sekmesi görünür.

**Tipografi Ailesi** — Kategoriye göre 70'den fazla font içeren arama yapabilen bir açılır menü. Her font, seçmeden önce nasıl görüneceğini göstermek için kendi tipografisinde önizlenir. Gerekli olduğunda Google Fonts'ten istek üzerine yüklenir.

**Tipografi Boyutu** — px, em, rem ve % birimlerini destekleyen sayısal giriş. Varsayılan 16px'dir.

**Tipografi Ağırlığı** — 100 (İnce) ile 900 (Kara) arasında bir kaydırıcı:

| Değer | Adı |
|-------|------|
| 100 | İnce |
| 200 | Ekstra İnce |
| 300 | Hafif |
| 400 | Normal |
| 500 | Orta |
| 600 | Yarı Koyu |
| 700 | Koyu |
| 800 | Ekstra Koyu |
| 900 | Kara |

Her font, tüm dokuz ağırlığı desteklemeyebilir. Düzenleyici, seçilen font ailesi için hangi ağırlıkların mevcut olduğunu gösterir.

**Tipografi Stili** — Normal, İtalyanca ve Eğik için geçiş butonları.

## Aralıklar Sekmesi

Karakterler etrafındaki ve aralarındaki boşluğu ince ayarlayın:

| Kontrol | Ne Yapar | Varsayılan |
|---------|-------------|---------|
| **Satır Aralığı** | Metin satırları arasındaki dikey boşluk | normal |
| **Harf Aralığı** | Bireysel karakterler arasındaki yatay boşluk | normal |
| **Kelime Aralığı** | Kelimeler arasındaki yatay boşluk | normal |
| **Metin Girişi** | Bir paragrafın ilk satırının girintisi | 0 |

Her aralık kontrolü, birim seçici (px, em, rem, %) içerir.

## Stil Sekmesi

Metin süslemesi ve görsel etkileri kontrol edin:

- **Metin Süslemesi** — Hiçbiri, Alt Çizgi, Üst Çizgi veya Çizgi Atla
- **Süsleme Stili** — Katı, Noktalı, Nokta, Çift veya Dalgalı (bir süsleme etkin olduğunda uygulanır)
- **Süsleme Rengi** — Süsleme çizgisinin rengi için renk seçici, varsayılan metin rengidir
- **Metin Gölgesi** — Kayma, bulanıklık ve renk kontrolü ile isteğe bağlı gölgelendirme etkisi

## Dönüşüm Sekmesi

İçeriği düzenlemek zorunda kalmadan metnin büyük/küçük harf durumunu değiştirin:

| Seçenek | Sonuç |
|--------|--------|
| **Hiçbiri** | Metin yazıldığı gibi görünür |
| **Büyük Harf** | TÜM HARFLER BÜYÜK HARFLE YAZILIR |
| **Küçük Harf** | Tüm harfler küçük harf olur |
| **Harf Başına Büyük Harf** | Her kelimenin ilk harfi büyük harf olur |

Bu sekmedeki ek kontroller **Metin Hizalama** (sol, orta, sağ, gerekli), **Dikey Hizalama** ve **Metin Yönü** (LTR veya RTL) içerir.

## Kullanılabilir Tipografi Aileleri

Düzenleyici, kategoriye göre gruplandırılmış sistem ve Google Font'ları içeren bir seçkin kütüphane içerir:

| Kategori | Yazı Tipleri |
|----------|-------|
| **Sistem** | Sistem Varsayılanı, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS |
| **Sans-Serif (Modern)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans |
| **Sans-Serif (Klasik)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend |
| **Serif** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya |
| **Serif (Sistem)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria |
| **Monospace** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono |
| **Görsel** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black |

Google Yazı Tipleri, seçildiğinde otomatik olarak yüklenir. Sistem yazı tipleri, platformlar arasında güvenilir bir şekilde işlenmesi için uygun CSS fallback zincirlerini kullanır.

## Nerede Görünür

Tipografi Düzenleyicisi, metin stillendirme gereken her yerde kullanılabilir:

- **Sayfa Oluşturucu** — Herhangi bir öğeyi seçin, Stil sekmesini açın ve Tipografi bölümünü tıklayın
- **Başlık/Açılış Sayfası Oluşturucu** — Menü bağlantılarında, logo metninde, menü öğelerinde ve alt bilgi içeriklerinde metni stillendirin
- **Menü Oluşturucu** — Menü etiketleri ve alt menü öğeleri için tipografiyi kontrol edin
- **Katalog Yönetimi** — Ürün açıklaması ve içerik editörlerinde tipografi kontrolleri açıkken kullanılır

Düzenleyici, bağlamdan bağımsız olarak her zaman aynı tutarlı arayüz üzerinden erişilir.

## İpuçları

- **Yazı tiplerini dikkatli bir şekilde eşleştirin** — başlıklarda bir görsel veya serif yazı tipi kullanın ve vücut metninde temiz bir sans-serif kullanın. Playfair Display + Inter veya Montserrat + Merriweather gibi klasik kombinasyonlar iyi çalışır.
- **Sayfa başına yazı tipi ailesini sınırlayın** — genellikle bir sayfada iki veya üç yazı tipi ailesi yeterlidir. Daha fazlası, yükleme sürelerini yavaşlatabilir ve görsel kargaşaya neden olabilir.
- **Duyarlı metin için göreli birimleri kullanın** — em ve rem, temel yazı tipi boyutuyla ölçeklenir, bu da tipografinin farklı ekran boyutlarına otomatik olarak uyum sağlamasını sağlar.
- **Ağırlık kullanılabilirliğini kontrol edin** — 400 ve 500 ağırlığında metin aynı görünüyorsa, seçilen yazı tipi o ağırlığı desteklemeyebilir. Düzenleyici, her yazı tipinin hangi ağırlıkları sağladığını gösterir.
- **Tüm cihazlarda önizleme yapın** — masaüstü boyutlarında iyi görünen metin, mobil cihazlarda çok küçük ya da çok büyük olabilir. Sayfa Oluşturucu cihaz önizleme özelliğini kullanarak doğrulayın.
- **Canlı önizlemeyi kullanın** — uygulamadan önce önizleme kutularında Mevcut vs. Yeni'yi her zaman karşılaştırın, beklenmedik değişikliklerden kaçının.