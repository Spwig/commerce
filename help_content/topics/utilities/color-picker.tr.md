---
title: Renk Seçici
---

Gelişmiş renk seçici, birden fazla girdi yöntemi ve tema bilinçli önceden ayarlanmış renkleri kullanarak renk seçmenizi sağlar. Platformun her yerinde renk özelliği kullanıldığında — sayfa inşası, başlık/altbilgi inşası, menü inşası ve katalog yönetimi — görünür. Renk seçiciyi açmak için herhangi bir renk swatch'ına veya renk girdi alanına tıklayın.

![Renk Seçici](/static/core/admin/img/help/color-picker/color-picker.webp)

## Renk Girdi Yöntemleri

Seçici, bir renk tanımlamak için birkaç yöntemi destekler:

| Yöntem | Açıklama | Örnek |
|--------|-------------|---------|
| **Hex** | Doğrudan 6 hanelik bir hex kodu girin | `#FF5733` |
| **RGB** | Kırmızı, Yeşil ve Mavi kaydırıcılarını (her biri 0-255) ayarlayın | `rgb(255, 87, 51)` |
| **HSL** | Ton (0-360), Doyma (0-100%) ve Parlaklık (0-100%) ayarlayın | `hsl(14, 100%, 60%)` |
| **RGBA** | Alfa şeffaflık kanalı ile RGB | `rgba(255, 87, 51, 0.8)` |
| **HSLA** | Alfa şeffaflık kanalı ile HSL | `hsla(14, 100%, 60%, 0.8)` |
| **Görsel Spektrum** | Renk spektrumu alanına tıklayıp sürükleyerek görsel olarak renk seçin | Nokta ve tıklama seçimi |

Seçiciye tıkladığınızda, alt kısmındaki metin girdisine doğrudan bir değer girebilirsiniz.

## Format Seçici

Seçicinin üst kısmında bir açılır menü, **HEX**, **RGB**, **RGBA**, **HSL** ve **HSLA** çıktı modları arasında geçiş yapmanıza olanak tanır. Formatları değiştirdiğinizde, mevcut renk otomatik olarak dönüştürülür — hiçbir değer kaybolmaz. İş akışınız veya tasarım sisteminiz gereksinimlerine en uygun formatı seçin.

## Renk Önceden Ayarlamaları

Spektrum alanının alt kısmında, ortak renkler için hızlı erişim için bir satır renk swatch'ı bulunur. Bu swatch'lar **tema bilinçli**dir: aktif tema'nın ana, ikincil, vurgu ve nötr renk paletlerini otomatik olarak yansıtır. Bu, markanızla tutarlı kalmanıza yardımcı olur ve hex kodlarını ezberlemek zorunda kalmazsınız.

Bir önceden ayarlamayı uygulamak için swatch'a tıklayın. Seçici, seçilen rengi spektrum ve girdi alanlarında hemen günceller.

## Şeffaflık / Alfa

RGBA veya HSLA modunda kullanıldığında, spektrumun altında bir yatay **alfa kaydırıcısı** görünür. Kaydırıcısı sürükleyerek şeffaflığı 0% (tamamen şeffaf) ile 100% (tamamen opak) arasında ayarlayabilirsiniz. Şeffaflık değeri ayrıca kaydırıcının yanındaki sayısal girdiyle düzenlenebilir ve hassas kontrol sağlar.

Yarı şeffaf renkler, örtü, hover efektleri ve katmanlı tasarım öğeleri için faydalıdır.

## Mevcut vs Yeni Önizleme

Seçicinin alt kısmında, **mevcut** uygulanan renk ve **yeni** seçilen renk için yan yana iki kutu bulunur. Bu karşılaştırma, değişikliği onaylamadan önce değerlendirmenizi sağlar. Yeni rengi onaylamak için **Uygula**'ya tıklayın veya seçici dışına tıklayarak mevcut değeri koruyarak iptal edin.

## Nerede Görünür

Renk seçici, adminin tümünde kullanılan bir paylaşılan yardımcıdır:

- **Sayfa İnşası** — Stil sekmesindeki öğe metni rengi, arka plan rengi, kenarlık rengi ve hover durumları
- **Başlık/Altbilgi İnşası** — Widget metni, arka plan, ikon ve bağlantı renkleri
- **Menü İnşası** — Menü öğesi bağlantı renkleri ve hover/etkin durum renkleri
- **Katalog Yönetimi** — Ürün etiket renkleri ve kategori vurgu renkleri

Herhangi bir renk değeri kabul eden alan bu aynı seçiciyi açar, bu nedenle her yerde deneyim tutarlıdır.

## İpuçları

- Temanızın önceden ayarlanmış swatch'larını kullanarak sayfalar ve bileşenler arasında marka tutarlılığını koruyun.
- Aynı tonun daha açık veya daha koyu varyasyonları oluşturmanız gerekiyorsa HSL moduna geçin — sadece Parlaklık değerini ayarlayın.
- Metin girdisinden hex kodunu kopyalayın ve aynı rengi başka bir alana tekrar kullanın veya bir tasarımcıyla paylaşın.
- Görseller ve anasayfa bölümlerinde ince örtü efektleri için RGBA ile azaltılmış şeffaflık kullanın.
- Seçici, oturumunuz boyunca son kullanılan renkleri hatırlar, bu nedenle sık sık kullanılan özel renkler hala erişilebilir kalır.
- Herhangi bir desteklenen formatta bir renk değeri hex girdisine yapıştırırsanız, seçici bunu otomatik olarak tanıyıp dönüştürecektir.
