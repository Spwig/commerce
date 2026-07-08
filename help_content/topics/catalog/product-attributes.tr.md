---
title: Ürün Özellikleri
---

Ürün özellikleri, bir ürünün hangi boyutlarda değişebileceğini tanımlar — örneğin, Boyut, Renk veya Malzeme. Bir özellik ve olası değerlerini oluşturduktan sonra, bunu herhangi bir değişken ürünle ilişkilendirebilirsiniz ve Spwig, müşterilerin ödeme sırasında kullandığı varyasyon seçicisini oluşturur.

**Katalog > Ürün Özellikleri**'ne giderek özellikleri ve değerlerini yönetin.

## Özelliklerin nasıl çalıştığı

Özellikler, tüm kataloğunuza boyunca yeniden kullanılabilir. Onları bir kez oluşturursunuz ve ihtiyaç duyduğunuz kadar çok ürünle ilişkilendirebilirsiniz. Her özellik:

- Tanımlayıcı bir **ad** (örneğin, "Boyut")
- Ürün sayfasında seçici görünümünü kontrol eden bir **gösterim türü**
- Mevcut seçenekleri temsil eden bir veya daha fazla **değer** (örneğin, "Küçük", "Orta", "Büyük")

Bir özelliği bir ürüne atadığınızda, o ürün için hangi değerlerin kullanılabilir olduğunu da belirtmeniz gerekir. Bu, "Boyut" özelliği S'den 3XL'e kadar değerler içeriyorsa, belirli bir tişört sadece S, M ve L boyutlarını sunabilir anlamına gelir.

## Özellik Gösterim Türleri

Bir özelliğin **Tip** alanı, özellik seçici widget'ının mağazanızın ürün sayfasında nasıl görünmesini kontrol eder:

| Tip | Görünüm | En Uygun Olduğu Durumlar |
|---|---|---|
| **Açılır Menü Seçimi** | Müşterinin bir değeri seçmek için açtığı bir açılır menü | Çok sayıda değere sahip özellikler (örneğin, 10+ boyut içeren bir boyut aralığı) |
| **Renk Örneği** | Müşterinin tıkladığı renkli daireler veya kareler | Renk özellikleri için görsel tanımlama yardımcı oluyorsa |
| **Düğme Grubu** | Satır içi olarak gösterilen pastel şekilli düğmeler | Az sayıda değere sahip özellikler (örneğin, S, M, L, XL) |
| **Radyo Butonları** | Geleneksel radyo butonu listesi | Seçici, erişilebilir liste düzeni istiyorsanız herhangi bir özellik için |

Müşterilerin özelliğe dair düşünceleriyle uyumlu bir gösterim türü seçin. Renk için, açılır menüden çok renk örnekleri hemen hemen her zaman daha iyidir. Boyut için, 8'ten az seçenek varsa düğme grupları iyi çalışır.

## Özellik Oluşturma

1. **Katalog > Ürün Özellikleri**'ne gidin
2. **+ Ürün Özelliği Ekle**'ye tıklayın
3. **Ad**'ı girin (örneğin, `Boyut`, `Renk`, `Malzeme`)
4. **Slug** otomatik olarak doldurulur — bunu olduğu gibi bırakabilirsiniz
5. **Tip**'i seçin (Açılır Menü, Renk Örneği, Düğme Grubu veya Radyo Butonları)
6. Müşterilerin ürünü sepetine eklemek için bu özelliği seçmeleri zorunluysa **Gerekli**'yi işaretleyin — bu, çoğu boyut ve renk özellikleri için uygun bir durumdur
7. **Sıra Numarası**'nı ayarlayın — daha düşük numaralı özellikler, ürün sayfasındaki varyasyon seçicisinde daha önce görünür
8. Özellik değerlerini doğrudan **Değerler** bölümüne ekleyin (aşağıdaki bölümü görün)
9. **Kaydet**'e tıklayın

## Özellik Değerleri Ekleme

Özellik değerleri, bir özelliğin içindeki bireysel seçeneklerdir. Bir özelliği oluştururken veya düzenlerken, özelliğin detay sayfasının altındaki satır içi değer formunu kullanarak doğrudan ekleyebilirsiniz.

Her değer için:

- **Değer** — görüntüleme etiketi (örneğin, `Küçük`, `Kırmızı`, `Pamuk`)
- **Slug** — değerden otomatik olarak doldurulur; URL'lerde ve varyasyon tanımlayıcılarında kullanılır
- **Renk Hex** — sadece **Renk Örneği** türündeki özellikler için ilgilidir. Bir renk kodu girin (örneğin, `#FF0000` kırmızı için), böylece örnek doğru rengi gösterir.
- **Sıra Numarası** — değerlerin seçici içinde nasıl göründüğünü kontrol eder. İlk olarak görünmesini istediğiniz değerlere daha düşük numaralar atayın.

### Mantıklı Sıralama

Boyut özellikleri için, boyutların küçükten büyüğe doğru sıralanmasını sağlayacak şekilde sıralama numarasını ayarlayın:

| Değer | Sıra Numarası |
|---|---|
| XS | 1 |
| S | 2 |
| M | 3 |
| L | 4 |
| XL | 5 |
| 2XL | 6 |

Renk özellikleri için, alfabetik olarak sıralayabilir veya benzer renkleri gruplayabilirsiniz — müşterileriniz için en fazla anlamlı olanı.

## Özellik Değerlerini Bağımsızca Yönetme

Ayrıca, **Katalog > Özellik Değerleri**'nde özellik değerlerini bağımsızca da yönetebilirsiniz. Bu liste, kataloğunuza erişmeden belirli bir değeri bulmak veya güncellemek gerektiğinde faydalıdır. Liste, özellik adı tarafından filtrelenebilir.

## Özellikleri Ürünlerle İlişkilendirme

Öznitelikler, ürün seviyesinde atanır, küresel değildir.

Bir ürünün özniteliğini eklemek için:

1. **Katalog > Ürünler**'e gidin ve bir değişken ürünü açın
2. **Değişkenlikler** sekmesinde, **Öznitelikler** bölümüne gidin
3. Eklemek istediğiniz özniteliği seçin
4. Bu ürün için kullanılabilir olan özniteliğin değerlerini seçin
5. Ürünü kaydedin — Spwig, ilgili varyasyon kombinasyonlarını oluşturur

Ürün varyasyonlarını ayarlama konusunda detaylı kılavuz için **Ürün Varyasyonları** yardım konusuna bakın.

## Uygulamalı örnekler

### Örnek: Giysi boyutu özniteliği

| Alan | Değer |
|---|---|
| Ad | Boyut |
| Tip | Buton Grubu |
| Gerekli mi? | Evet |
| Sıra Numarası | 1 |
| Değerler | XS (1), S (2), M (3), L (4), XL (5), 2XL (6) |

### Örnek: Renk swatch özniteliği

| Alan | Değer |
|---|---|
| Ad | Renk |
| Tip | Renk Swatch |
| Gerekli mi? | Evet |
| Sıra Numarası | 2 |
| Değerler | Siyah (#000000), Beyaz (#FFFFFF), Lüks Mavi (#001F5B), Kırmızı (#CC0000) |

### Örnek: Malzeme özniteliği

| Alan | Değer |
|---|---|
| Ad | Malzeme |
| Tip | Aşağıdaki Seçenekler |
| Gerekli mi? | Hayır |
| Sıra Numarası | 3 |
| Değerler | 100% Pamuk, Pamuk/Poliester Karışımı, Merino Yün, Yufka |

## İpuçları

- Gerçek alım kararlarını temsil eden öznitelikler oluşturun — eğer müşteriler bunu seçmek zorunda değilse, bu bir öznitelik olmayabilir
- Kataloğunuzda tutarlı isimlendirme kullanın: bazı ürünler "Renk" ve diğerleri "Color" kullanıyorsa, müşteriler ve ekibiniz bu tutarsızlığı bulabilir
- Hem öznitelikler hem de değerlerdeki sıralama önemlidir — en önemli özniteliği ilk (genellikle Boyut veya Renk) ve değerleri mantıklı bir sırayla sıralayın
- Renk Swatch türü, doğru heksadesimal kodlarını gerektirir; kaydetmeden önce bir tarayıcı renk seçicisinde renkleri test edin, swatchın ürünün gerçek rengiyle eşleştiğinden emin olun
- Eğer bir özniteliği yeniden isimlendirmek gerekirse (örneğin "Color" dan "Colour" e), yeni bir öznitelik oluşturmak yerine **Ad** alanını güncelleyin — isim değişikliği mevcut ürün atamalarını etkilemez