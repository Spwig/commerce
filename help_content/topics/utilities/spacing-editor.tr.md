---
title: Ara Uzay Düzenleyici
---

Görsel uzay düzenleyici, kullanıcı dostu bir kutu model diyagramı kullanarak kenar boşluklarını ve dolguları yapılandırmaya olanak tanır. Hassas uzay kontrolü, mağazanızın tüm sayfalarında tutarlı düzenler ve konforlu okuma deneyimleri sağlar. Herhangi bir öğenin **Stil sekmesine** gidin ve **Uzay** bölümünü arayın, düzenleyiciye erişebilirsiniz.

![Uzay Düzenleyici](/static/core/admin/img/help/spacing-editor/spacing-editor.webp)

## Kutu Model Diyagramı

Düzenleyici, üç iç içe geçmiş katmanla birlikte görsel bir kutu modelini görüntüler:

- **Kenar boşluğu** (dış halka, genellikle turuncu olarak gösterilir) — Elemanın kenar çizgisinin dışında, komşu öğelerden ayıran alan
- **Dolgu** (iç halka, genellikle yeşil olarak gösterilir) — Elemanın kenar çizgisi ile içeriği arasındaki alan
- **İçerik** (merkez alan) — Elemanın gerçek içeriği, örneğin metin veya bir resim

Diyagramın her tarafında (üst, sağ, alt, sol) sürükleyilebilir bir tutamaç ve sayısal bir girdi vardır. Bir tutamaç dışa doğru sürükleyerek değeri artırın veya içeri doğru sürükleyerek azaltın. Ayrıca, bir tarafın değerine doğrudan tıklayarak kesin bir sayı girebilirsiniz.

## Kenar Boşluğu ve Dolgu Sekmeleri

Düzenleyicinin üst kısmında bulunan iki sekme, **Kenar boşluğu** ve **Dolgu** görünümü arasında geçiş yapar. Kenar boşluğu seçildiğinde, dış halka vurgulanır ve düzenlenebilir hale gelir. Dolgu seçildiğinde, iç halka vurgulanır ve düzenlenebilir hale gelir. Aktif olmayan halka, referans olarak görünür ama koyulaşır.

Her iki sekme aynı kontrol ve birim seçeneklerini paylaşır, bu nedenle kenar boşluğu ve dolgu yapılandırması için iş akışı aynıdır.

## Yan Taraf Kontrolleri

Her tarafın bağımsız bir değer girişi ve birim seçicisi vardır:

| Taraf | Açıklama |
|------|-------------|
| **Üst** | Elemanın üstündeki boşluk (kenar boşluğu) veya içeriğin üstündeki boşluk (dolgu) |
| **Sağ** | Elemanın veya içeriğin sağındaki boşluk |
| **Alt** | Elemanın veya içeriğin altındaki boşluk |
| **Sol** | Elemanın veya içeriğin solundaki boşluk |

Diyagramda herhangi bir tarafın değerine tıklayarak onu seçin, ardından bir sayı girin veya yukarı/aşağı ok tuşlarını kullanarak 1 artırın. Ok tuşlarını basarken Shift tuşuna basılı tutarak 10 artırın.

## Birimler

Her değer girişi yanındaki birim seçicisi, ölçüm birimini seçmenizi sağlar:

| Birim | Açıklama |
|------|-------------|
| **px** | Piksel. Cihazlara göre sabit boyut. Küçük ve hassas uzay değerleri için en iyisidir. |
| **em** | Elemanın font boyutuna göre. Tipografi değişikliklerine göre ölçeklenir. |
| **rem** | Kök font boyutuna göre. Sayfada tutarlı ölçeklendirme sağlar. |
| **%** | Ana öğenin genişliğinin yüzdesi. Akışkan ve yanıt veren düzenler için faydalıdır. |
| **auto** | Tarayıcıya değer otomatik olarak hesaplatır. Genellikle sol/sağ kenar boşluklarıyla yatay merkekleme için kullanılır. |

İhtiyacınıza uygun bir birim seçin — `px` sabit boşluklar için, `rem` tema tipografi token'larıyla ölçeklenebilir uzaylar için ve `%` konteyner genişliğine uyum sağlayacak düzenler için kullanın.

## Yan Tafilleri Bağla

Diyagramın merkezindeki **bağlantı simgesi**, bağlantılı modu açıp kapatmak için kullanılır:

- **Bağlantılı** (bağlantılı zincir simgesi) — Herhangi bir tarafın değerini değiştirmek, dört tarafın değerini aynı değere günceller. Tutarlı uzaylar için kullanışlıdır.
- **Bağlantısız** (kesilmiş zincir simgesi) — Her taraf ayrı ayrı kontrol edilir. Tavan/alt ve sol/sağ değerleri farklı olacaksa bu modu kullanın.

Bağlantı simgesine tıklayarak modlar arasında geçiş yapın. Bağlantısızdan bağlantılıya geçiş yaparsanız, dört tarafın değeri en son düzenlenmiş tarafın değeriyle ayarlanır.

## Hızlı Ayarlar

Diyagramın altındaki ayar butonları satırı, bir tıklamayla uzay yapılandırmaları sağlar:

| Ayar | Değerler |
|--------|--------|
| **Hiçbiri** | Tüm taraflar 0 |
| **Küçük** | Dar düzenler ve satır içi öğeler için uygun kompakt uzay |
| **Orta** | Kartlar ve bölümler için genel amaçlı uzay |
| **Büyük** | Hero bölgeleri ve yüksek vurgu bölümleri için genel uzay |
| **XL** | Genişlik boyunca yayılmış afişler ve sayfa bölümleri için ekstra geniş uzay |

Ayarlar, şu anki aktif sekme (Kenar boşluğu veya Dolgu) için geçerlidir ve dört tarafı bir anda ayarlar. Bir ayar uyguladıktan sonra gerekirse bireysel tarafları ayarlayabilirsiniz.

## Nerede Görünür

Uzay düzenleyici, düzen uzaylarını destekleyen her öğe için kullanılabilir:

- **Sayfa Oluşturucu** — Bölümler, konteynerler, sütunlar ve bireysel öğelerdeki **Stil sekmesi**, **Uzay** bölümü
- **Başlık/Ayakta Oluşturucu** — Dikey ve yatay boşluk kontrolleri için satır ve widget ayarları
- **Menü Oluşturucu** — Menü öğesi dolgusu ve konteyner kenar boşluğu ayarları

Tüm yerlerde aynı düzenleyici arayüzü kullanılır, bu da oluşturucular arasında tutarlı bir deneyim sağlar.

## İpuçları

- Sayfalarınızda tutarlı uzay değerleri kullanın — 2-3 standart boyut seçin ve onlarla kalın, temiz ve profesyonel bir düzen elde edin.
- Sol ve sağ kenar boşluklarını **auto** olarak ayarlayarak, sabit genişlikli bir öğeyi ebeveyn öğesinin içinde yatay olarak merkezleyin.
- Temanız yanıt veren tipografi kullanıyorsa, uzay için `rem` birimlerini tercih edin, böylece uzay metin boyutuyla orantılı olarak ölçeklenir.
- Bağlantılı modu kullanarak hızlıca eşit dolgular ayarlayın, içerik asimetrik uzay gerektiriyorsa bağlantıyı kaldırın ve bireysel tarafları ince ayarlayın.
- Mobil cihazlarda aşırı dolgulardan kaçının — dar viewport genişliklerinde uzayınızı test edin, içerik sıkışmış veya aşırı dolgulu olmasın.
