---
title: Kenar Düzenleyici
---

Kenar Düzenleyici, kenar stilleri, renk, kenar genişliği (her kenar için) ve köşe yuvarlama (her köşe için) gibi öğelerin kenarlarını ince düzeyde kontrol etmenizi sağlar. Canlı önizleme ile birlikte iki sekme (temel ve gelişmiş ayarlar) içeren bir kayan panel olarak açılır.

![Kenar Düzenleyici](/static/core/admin/img/help/border-editor/border-editor.webp)

## Canlı Önizleme

Düzenleyici üst kısmında bir önizleme kutusu, kenar ayarlarınızı gerçek zamanlı olarak gösterir. Bu kutu, "Önizleme" kelimesini içeren ve kenar stilleri, renk, genişlik ve yuvarlama değerlerini ayarladıkça anında güncellenen bir kenarlı dikdörtgen içerir.

## Temel vs Gelişmiş Mod

Düzenleyici iki sekmeye bölünmüştür:

| Sekme | İçerdiği İşlevler |
|-------|------------------|
| **Temel** | Kenar stili, renk, genişlik (her kenar için kontroller) ve kenar yuvarlaması (her köşe için kontroller) |
| **Gelişmiş** | Bireysel köşe yuvarlamalarının ince ayarları ve deneme amaçlı Köşe Şekli özelliği |

Çoğu kenar düzenlemesi, Temel sekmede tamamen yapılır. Gelişmiş sekme, bireysel köşelerin hassas kontrolü gerekliyse veya yeni CSS özellikleriyle deneme yapmak istiyorsanız kullanışlıdır.

## Kenar Stili

Kenar çizgisinin görünümünü kontrol eden dokuz seçeneği içeren bir açılır menü:

| Stil | Açıklama |
|------|---------|
| **Hiçbiri** | Kenar yok (var olan herhangi bir kenarı kaldırır) |
| **Katı** | Tek bir sürekli çizgi (varsayılan) |
| **Çizgili** | Kısa çizgilerden oluşan bir dizi |
| **Noktalı** | Yuvarlak noktaların bir dizi |
| **Çift** | İki paralel katı çizgi |
| **Çukur** | Yüzeye bastırılmış gibi görünen, 3D efektli bir kenar |
| **Kıvrım** | Çukurun zıt yönünde, 3D efektli bir yükselen kenar |
| **İçeride** | Öğenin içeriye bastırılmış gibi görünmesini sağlar |
| **Dışa** | Öğenin dışa çıkmış gibi görünmesini sağlar |

Stili "Hiçbiri" olarak ayarlarsanız, genişlik veya renk ayarlarına bakılmaksızın kenar tamamen kaldırılır.

## Kenar Rengi

Bir metin girişi alanı ve bir Renk Seçici butonu eşleşmiş durumda. Doğrudan bir heksadesimal değer girin (örneğin `#3b82f6`) veya renk swatch'ını tıklayarak heksadesimal, RGB ve HSL girişi modları ile birlikte görsel bir renk alanı içeren tam Renk Seçici'yi açın. Varsayılan renk siyah (`#000000`)dır.

## Kenar Genişliği

Kenarın kalınlığını piksel cinsinden kontrol eder. Temel sekme, dört kenar için bireysel girdileri gösterir:

| Kenar | Girdi |
|------|-------|
| **Üst** | Sayısal girdi, minimum 0 |
| **Sağ** | Sayısal girdi, minimum 0 |
| **Alt** | Sayısal girdi, minimum 0 |
| **Sol** | Sayısal girdi, minimum 0 |

Etiketin yanındaki **bağlantı anahtar butonu** (zincir simgesi), dört kenarın bağlı olup olmadığını kontrol eder:

- **Bağlı** (varsayılan) — herhangi bir değeri değiştirirseniz, dört kenar birlikte güncellenir
- **Bağlı Değil** — her kenar farklı bir genişlik olabilir, sadece alt kenar veya sol kenar vurgusu gibi etkiler için kullanışlıdır

## Kenar Yuvarlaması

Her köşenin yuvarlamasını kontrol eder. Temel sekme, dört köşe girdisini gösterir:

| Köşe | Etiket |
|------|-------|
| **Sol Üst** | TL |
| **Sağ Üst** | TR |
| **Sol Alt** | BL |
| **Sağ Alt** | BR |

**Bağlantı anahtar butonu**, kenar genişliği ile aynı şekilde çalışır:

- **Bağlı** (varsayılan) — dört köşe aynı yuvarlama değerini paylaşır
- **Bağlı Değil** — her köşe farklı bir yuvarlama değeri olabilir

Ortak yuvarlama değerleri:

| Değer | Etki |
|-------|------|
| 0px | Keskin kare köşeler |
| 4-8px | İnce yuvarlama, kartlar ve butonlar için iyi |
| 12-16px | Dikkat çeken yuvarlama, modern ve yumuşak bir görünüm |
| 50% | Tam daire veya pil şeklinde (öğenin boyutuna bağlı olarak) |

Birim seçici, genişlik ve yuvarlama değerleri için px, em, rem ve % destekler.

## Köşe Şekli (Gelişmiş)

Gelişmiş sekme, deneme amaçlı bir **Köşe Şekli** özelliğini içerir. Bu CSS özelliği, yuvarlak köşelerin standart yuvarlak şekli kullanılıp kullanılmayacağını ya da daha açılı bir "scoop" şekli kullanılıp kullanılmayacağını kontrol eder. Tarayıcı desteği sınırlıdır ve düzenleyici, şu anki tarayıcı bu özelliği desteklemiyorsa uyumluluk uyarısı görüntüler.

## Alt Bölüm Eylemleri

| Buton | Eylem |
|--------|--------|
| **Sıfırla** | Düzenleyici açıldığında tüm değerleri eski durumuna döndürür |
| **İptal** | Değişiklikleri uygulamadan düzenleyiciyi kapatır |
| **Uygula** | Kenar ayarlarını kaydeder ve düzenleyiciyi kapatır |

## Nerede Görünür

Kenar Düzenleyici, birkaç inşaatçıda kullanılabilir:

- **Sayfa İnşaatçı** — herhangi bir öğeyi seçin, Stil sekmesini açın ve Kenar bölümüne tıklayın
- **Başlık/Ayakta İnşaatçı** — başlık bölümlerine, navigasyon konteynerlerine ve ayakta alanlara kenar ekleyin
- **Menü İnşaatçı** — menü öğelerine ve açılır menü konteynerlerine kenar stilini uygulayın

Düzenleyici, canvas'taki canlı öğeden mevcut hesaplanan kenar stillerini okur, bu yüzden her zaman doğru mevcut değerlerle açılır.

## İpuçları

- **Kenarları az kullanın** — hafif bir açık gri 1px kenar, bölümler arasında temiz bir ayırıcı oluşturur ve görsel ağırlık eklemeyebilir.
- **Yuvarlama ile gölgeleri birleştirin** — yuvarlak köşeleri, gölgeler düzenleyici ile birlikte kullanarak polisajlı bir kart etkisi oluşturabilirsiniz.
- **Tek kenarlı kenarlar deneyin** — kenarları bağlantılı hale getirin ve sadece alt veya sol kenarı ayarlayarak vurgu çizgileri, bölümler ayırıcıları veya yan çubuk göstergeleri oluşturun.
- **Pil şekilleri için yüzde yuvarlaması kullanın** — bir buton veya etiketin tüm köşelerini 50% olarak ayarlayarak, içerik boyutuna göre uyarlanabilen bir pil şekli oluşturun.
- **Önizlemeyi kontrol edin** — canlı önizleme kutusu hemen güncellenir, bu yüzden uygulamadan önce özgürce deneyin.

