---
title: Özel Ürün Siparişlerini Gerçekleştirme
---

Müşteri bir ürün tasarlar ve sipariş verdiğinde, bu tasarım dondurularak siparişle birlikte saklanır. Bu kılavuz, özel tasarımların sipariş yaşam döngüsüne nasıl akacağını ve üretim için ihtiyacınız olan basma hazıры dosyalarına nasıl erişileceğini açıklar.

## Tasarım yaşam döngüsü

Müşterinin bir tasarım, yaratılmasından üretimine kadar birkaç aşamadan geçer:

### 1. Tasarım yaratımı

Müşteri, mağazanın görsel editörünü kullanarak kendi tasarımını oluşturur. Çalışırken, ilerlemesi tarayıcıda otomatik olarak kaydedilir. Kayıtlı müşteriler, tasarımları hesaplarına kaydedebilir ve daha sonra düzenleyebilir.

### 2. Tasarım taslağı

Müşteri **Sepete Ekle**'ye tıkladığında, mevcut tasarım durumu bir **tasarım taslağı** olarak kaydedilir. Taslağı içerir:

- Her yüzey için tam bir kanvas durumu (öğelerin konumu, metin içeriği, yüklenebilir görseller, grafikler, stiller)
- Uygulanabilir tasarım ücretlerini gösteren fiyat analizi
- Her yüzeyin küçük önizlemeleri

Taslağı, benzersiz bir token ile sepet öğesine bağlar. Bu, müşteri siparişi tamamlamadan alışverişe devam ederse bile, müşteri tarafından oluşturulan tam olarak tasarımın saklandığından emin olur.

**Taslağın sona ermesi:** Müşteri siparişi tamamlamazsa, tasarım taslağı 7 gün sonra otomatik olarak sona erer. Bu, terk edilmiş tasarımların birikmesini önler.

### 3. Tasarım anlık görüntüsü

Müşteri ödeme işlemini tamamladığında ve sipariş verildiğinde, tasarım taslağı bir **değiştirilemez tasarım anlık görüntüsü**'ne dönüştürülür. Bu, tasarımın kalıcı kaydıdır:

- Anlık görüntü, müşteri tarafından satın alınmasından sonra değiştirilemez
- Taslağın tam olarak aynı tasarım verilerini içerir
- Belirli bir sipariş öğesine kalıcı olarak bağlanır

Bu değiştirilemezlik önemlidir — müşteri tarafından sipariş edilen şeyin, ödeme sonrası hiçbir değişiklik olmaksızın tam olarak üretip gönderdiğinize emin olur.

### 4. Üretim dosyası oluşturma

Sipariş verildikten sonra, sistem her yüzey için **yüksek çözünürlüklü üretim dosyaları** otomatik olarak oluşturur. Bu, her yüzey için yapılandırılmış DPI'ye göre tüm tasarım öğelerini (metin, görseller, grafikler) tek bir basma hazırya dönüştüren bileşik görsüllerdir.

Oluşturma işlemi arka planda asenkron olarak gerçekleşir. Çoğu tasarım için oluşturma işlemi birkaç saniye içinde tamamlanır. Anlık görüntünün **Oluşturuldu** durumu, üretim dosyalarının hazır olup olmadığını gösterir.

## Siparişlerde tasarım verilerine erişme

### Sipariş detay sayfası

Yönetim panelinde, özelleştirilebilir ürünler içeren bir siparişi görüntülediğinizde:

1. **Siparişler > Tüm Siparişler**'e gidin
2. Özelleştirilmiş ürünü içeren siparişi açın
3. Özelleştirilebilir ürünün sipariş öğesi, tasarım bilgilerini, yüzey önizlemelerini ve tasarım anlık görüntüsüne bağlantıyı gösterir

### Tasarım anlık görüntülerinin listesi

Ayrıca, tüm tasarım anlık görüntülerine doğrudan erişebilirsiniz:

1. **Özelleştirilebilir Ürünler > Tasarım Anlık Görüntüleri**'ne gidin
2. Liste, sipariş öğelerine bağlı tüm anlık görüntülere sahiptir
3. Bir anlık görüntüye tıklayarak tam tasarım verilerini, oluşturulan görsüleri ve üretim dosyalarını görüntüleyebilirsiniz

Her anlık görüntü aşağıdaki alanları gösterir:

| Alan | Açıklama |
|-------|-------------|
| **Sipariş Öğesi** | İlişkili sipariş öğesine bağlantı |
| **Tasarım Verileri** | Tam kanvas durumu (JSON) |
| **Oluşturulan Görseller** | Her yüzey için önizleme küçük resimleri |
| **Üretim Dosyaları** | Basma için yüksek çözünürlüklü bileşik dosyalar |
| **Oluşturuldu** | Oluşturma işleminin tamamlandığı |
| **Oluşturulma Zamanı** | Dosyaların oluşturulduğu zaman damgası |

## Üretim dosyalarını indirme

Üretim dosyaları, basım sağlayıcınıza gönderdiğiniz ya da üretim sürecinizde kullandığınız dosyalardır.

**Özel bir t-shirt siparişi için:**
- **Ön** yüzey dosyasını indirin (örneğin, 300 DPI bileşik PNG)
- **Arka** yüzey dosyasını indirin
- **Kol** yüzey dosyasını indirin (tasarım yapıldıysa)
- Tüm dosyaları ekran basmacıya ya da DTG (direct-to-garment) basmacına gönderin


**Özel bir afiş siparişi için:**
- Yazdırma çözünürlüğünde tek bir **Ön** yüzey dosyasını indirin
- Yüzey için kanal yapılandırması yapılmışsa dosya kanal alanını içerir
- Afiş/kart basım hizmetinize gönderin

Her dosya, belirtilen yüzey için yapılandırılmış DPI'de tüm tasarım öğelerini birleştiren tek bir bileşik görseldir.

## Kaydedilmiş tasarımlar

Kayıtlı müşteriler, tasarımlarını hesaplarına kaydedebilir ve daha sonra düzenleyebilir. Satıcı olarak, bu kaydedilmiş tasarımları sadece okunabilir bir listede görüntüleyebilirsiniz:

1. **Özel Ürünler > Kaydedilmiş Tasarımlar** menüsüne gidin
2. Liste, müşteri adı, ürün, tasarım adı ve tarihle birlikte tüm müşteri tarafından kaydedilmiş tasarımları gösterir

Kaydedilmiş tasarımlar:
- **Müşteriye ait** — Bu tasarımlar müşteri hesabına aittir
- **Satıcılar için sadece okunabilir** — Görüntüleyebilirsiniz ama değiştiremezsiniz
- **Siparişlerden ayrı** — Kaydedilmiş bir tasarım, müşteri bunu sepete ekleyip ödeme yapana kadar bir sipariş değildir
- **Yeniden kullanılabilir** — Müşteriler, kaydedilmiş bir tasarımı yükleyebilir, düzenleyebilir ve birden fazla kez sipariş verebilir

## Teslimat akışı

### Standart akış

1. **Sipariş alın** — Sipariş, özelleştirilmiş ürünlerle birlikte sipariş listesinizde görünür
2. **Görsel doğrulama** — Tasarım özetinin **Doğrulandı: Evet** gösterip göstermediğini kontrol edin. Eğer görsel işleme tamamlanmamışsa, birkaç dakika bekleyin ve sayfayı yenileyin
3. **Dosyaları indirin** — Her tasarlanmış yüzey için teslimat dosyasını indirin
4. **Kalite incelemesi** — Dosyaları açın ve tasarımın baskı kalite standartlarını karşıladığını kontrol edin (DPI, öğe konumlandırması ve metin okunabilirliği)
5. **Üretim için gönderin** — Dosyaları baskı sağlayıcınıza veya üretim ekibinize iletin
6. **Teslimat ve tamamla** — Üretim tamamlandıktan sonra ürünü müşteriye gönderin ve siparişi tamamlandı olarak işaretleyin

### T-shirt teslimat örneği

1. Sipariş alın: "Özel Takım T-shirt"i, ön ve arka yüzeyde tasarımlarla
2. Siparişi açın → tasarımla ilgili özet görüntüleyin
3. `front.png` (300 DPI, 300x400mm) ve `back.png` (300 DPI, 300x400mm) dosyalarını indirin
4. Siparişin varyant seçimiyle elbise rengi ve boyutunu DTG basıcıma ile birlikte gönderin
5. Basım ve kalite kontrol tamamlandıktan sonra müşteriyi gönderin

### Afiş teslimat örneği

1. Sipariş alın: "Özel A4 Afiş"i, tek bir tasarlanmış yüzeyle
2. Siparişi açın → tasarımla ilgili özet görüntüleyin
3. `front.png` (300 DPI, 210x297mm ile 3mm kanal) dosyasını indirin
4. Afiş basım hizmetinize gönderin
5. Basım ve kesim tamamlandıktan sonra müşteriyi gönderin

## Sorun giderme

**Sorun:** Tasarım özetinde "Doğrulandı: Hayır" yazıyor ve işleme tamamlanmamış

- **Neden:** Arka plan işleme görevi başarısız olabilir veya hala işleniyor olabilir
- **Çözüm:** Birkaç dakika bekleyin. Eğer işleme tamamlanmazsa, arka plan görevi günlüklerini kontrol edin. Ayrıca, tasarım verilerini doğrudan özet görüntüleyerek müşteri tasarımının korunduğunu onaylayabilirsiniz

**Sorun:** Teslimat dosyası beklenenden daha düşük kalitede görünüyor

- **Neden:** Müşteri düşük çözünürlüklü görseller yükleyebilir
- **Çözüm:** Yüzeyin DPI ayarlarını kontrol edin. Minimum DPI uyarıları yapılandırılmışsa, müşteri tasarım süreci sırasında uyarılmış olurdu. Gelecekteki ürünler için minimum DPI gerekliliğini artırmayı düşünün

**Sorun:** Müşteri sipariş verdikten sonra tasarımında değişiklik istiyor

- **Çözüm:** Tasarım özetleri tasarım olarak değiştirilemez. Müşteri değişiklik istiyorsa, güncellenmiş tasarımla yeni bir sipariş vermelidir. Eğer bu değişikliği yapmaya razı iseniz, müşteri bir sipariş oluşturmak için kaydettiği tasarımları (eğer kaydetti ise) başlangıç noktası olarak kullanabilir

## İpuçları

- Üretim başlamadan önce her zaman görselin tamamlandığını kontrol edin.

Tasarım özetindeki **Doğrulandı** alanını kontrol edin.
- Yazdırma yönteminize uygun DPI ayarlarını koruyun.

Daha yüksek DPI daha iyi kalite sağlar ama dosya boyutları daha büyük olur. 300 DPI, çoğu profesyonel baskı ürünleri için standarttır.
- Müşterilerin sipariş vermeden önce tasarımlarını kaydetmesini teşvik edin.



# Üretimde Sorun Oluşursa
Eğer üretimde bir sorun oluşur ve sipariş yeniden hazırlanması gerekiyorsa, kaydedilmiş tasarım siparişin tekrarını kolaylaştırır.
- Üretim zaman çizelgenize özelleştirilebilir ürünler için bir tampon ekleyin.

Standart ürünlerden farklı olarak, her öğe bireysel dosya işleme gerektirir.
- Eğer yüksek hacimde özelleştirilebilir siparişler işliyorsanız, basım sağlayıcınızın API'siyle entegrasyon yaparak dosya indirme adımını otomatikleştirmeyi düşünün.