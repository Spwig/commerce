---
title: Özelleştirilebilir Ürünler
---

Özelleştirilebilir ürünler, müşterilerinize mağazanızda bulunan görsel bir editör aracılığıyla kendi ürünlerini tasarlamalarını sağlar. Özel t-shirt'ler, kişisel afişler, markalı ürünler veya mektup kartları satıyorsanız, bu özellik müşterilerin metin eklemelerini, resim yüklemelerini ve klipart kullanarak benzersiz tasarımlar oluşturabilmeleri için gerekli araçları sağlar — tüm bu işlemleri mağazanızdan çıkmadan yapabilirler.

## Nasıl Çalışır

Bir özelleştirilebilir ürün, standart bir Spwig ürünü ile bir **görsel tasarım editörü** kombinasyonunu içerir. Ürünün tasarım editleyebilecekleri yüzeylerini tanımlarsınız (örneğin, bir t-shirt'in ön ve arka yüzeyi), müşterilerin tasarımını bağlamda görebilecekleri mockup resimlerini yüklersiniz ve her yüzeyde müşterilerin ne yapabileceğini belirleyen kuralları ayarlarsınız.

Müşteri, mağazanızda bir özelleştirilebilir ürün ziyaret ederken, ürün mockup resminin üzerine yerleştirilmiş bir canlı bir canvas editörü görür. Metin ekleyebilir, kendi resimlerini yükleyebilir ve klipart kütüphanesini tarayarak tasarımını oluşturabilir. Editör, tasarımın tamamlanmış ürün üzerinde nasıl görüneceğini tam olarak gösterir.

### İki Kullanım Durumu

Özelleştirilebilir ürünler, genellikle iki yaygın senaryoda iyi çalışır:

| Kullanım Durumu | Örnek | Yüzeyler | Tipik Ayarlar |
|------------------|-------|----------|----------------|
| **Kıyafet Tasarımı** | Özel t-shirt'ler, kürk giysiler, çantalar | Birden fazla (ön, arka, kol) | Kalın yazı tipleri, eğlence/spor klipartları, yüzey bazlı kısıtlamalar |
| **Yazdırma Tasarımı** | Afişler, mektup kartları, iş kartları | Tek (yalnızca ön) | Yüksek DPI, kenar boşluğu ayarları, zarif yazı tipleri, dekoratif kenarlar |

Ayarlama süreci her ikisinde de aynıdır — fark, tanımladığınız yüzey sayısında, sağladığınız klipart ve yazı tiplerinde ve yazdırma ayarlarını nasıl yapılandıracağınızda yatmaktadır.

## Ana Kavramlar

### Tasarım Yapılandırması

Her özelleştirilebilir ürün, **tasarım yapılandırması** ile kontrol edilir. Bu yapılandırma, genel editör davranışını kontrol eder: hangi araçların kullanılabilir (metin, resim yükleme, klipart), yükleme sınırları ve fiyatlandırma kuralları. Bu, ürün tasarım editörü için ana kontrol panelidir.

### Yüzeyler

Bir **yüzey**, ürünün tasarım editleyebileceğiniz yüzeyidir. Bir t-shirt genellikle üç yüzey içerir (ön, arka, kol), bir afiş ise sadece bir yüzey içerir. Her yüzeyin kendi mockup resmi, tasarım alanı konumu, fiziksel boyutları ve yazdırma kalite ayarları vardır.

### Tasarım Alanı

**Tasarım alanı**, müşterilerin tasarım öğelerini yerleştirebileceği mockup resmindeki dikdörtgen alanıdır. Bu alanı, admin ayar sayfasında mockup resmine sürükleyerek ve yeniden boyutlandırarak görsel olarak tanımlarsınız. Bu alan, tasarımın tamamlanmış ürün üzerinde nerede görüneceğini tanımlar.

### Şablonlar

**Tasarım şablonları**, müşteriler için oluşturduğunuz önceden hazırlanmış başlangıç tasarımlarıdır. Boş bir canvas'tan başlamak yerine, müşteriler şablon galerinizi tarayabilir, beğendiklerini seçebilir ve özelleştirebilir. Şablonlar, müşterilerin değiştiremeyeceği kilitlenmiş öğeler de içerebilir — örneğin, her zaman aynı pozisyonda görünecek bir şirket logolu.

### Klipart ve Yazı Tipi

Müşterilerin tasarımlarına ekleyebilecekleri bir **klipart kütüphanesi** oluşturursunuz. Bu klipartlar, kategorilere (örneğin, "Spor", "Kenarlar", "Bayram") göre düzenlenir. Ayrıca, standart sistem yazı tipleri dışında **özel yazı tipleri** de yükleyebilirsiniz, böylece müşterilere daha fazla yaratıcı seçenek sunabilirsiniz.

### Fiyatlandırma

Tasarım editörü, dört ücret bileşenine sahip esnek bir fiyatlandırma modelini destekler:

| Ücret Türü | Açıklama |
|------------|----------|
| **Temel Tasarım Ücreti** | Herhangi bir özelleştirme uygulandığında eklenen sabit ücret |
| **Yüzey Başına Ücret** | İlk yüzeyden sonra kullanılan her yüzey için ek ücret |
| **Yükleme Başına Ücret** | Müşteri tarafından yüklenen her resim için ücret |
| **Metin Başına Ücret** | Eklenen her metin öğesi için ücret |

Müşteri öğeler eklerken ücretler anlık olarak güncellenir, bu nedenle ödeme sırasında sürpriz olmaz.

## Editör Modları

Spwig, iki editör modu sunar:

- **Canvas Editörü** — Canvastaki canlı bir görsel tasarım editörü, metin araçları, resim yükleme, klipart tarayıcı ve ürün mockup resminde anlık önizleme içerir.

Bu, çoğu özelleştirilebilir ürün için önerilen modüldür.
- **Basit Form** — Müşterilerin metin alanlarını doldurması ve görsel bir kanvas olmadan görseller yüklemesi için geleneksel bir form tabanlı yaklaşım.

Adını bir bileşen üzerine kazıtmak gibi minimal özelleştirme gerektiren ürünler için uygundur.

## Satıcı iş akışı

Özelleştirilebilir bir ürün ayarlamak şu iş akışı izlenir:

1. **Ürün oluştur** — Türünü **Özelleştirilebilir Ürün** olarak ayarlayarak yeni bir ürün ekleyin
2. **Yüzeyleri ayarla** — Tasarım edilebilecek her yüzeyi tanımlayın, mockup görselleri yükleyin ve tasarım bölgelerini konumlandırın
3. **Ayarları yapılandır** — Hangi araçları etkinleştireceğinizi seçin, yükleme sınırlarını ayarlayın ve fiyatlandırma yapılandırın
4. **Varlıklar ekle** — Kliptograf kütüphanesini oluşturun ve özel fontlar yükleyin
5. **Şablonlar oluştur** — Seçenek olarak kilitleme kontrolleri ile önceden hazırlanmış başlangıç noktaları tasarlayın
6. **Test et ve yayımla** — Mağazanızda düzenleyiciyi önizleyin ve her şeyin düzgün çalıştığını doğrulayın

Detaylı ayarlamalar için [Özelleştirilebilir Ürün Ayarlama](/admin/customizable-product/)

## Müşteri deneyimi

Bir müşteri, mağazanızda özelleştirilebilir bir ürüne girerken:

1. **Şablonları incele** — Hazır şablonlardan başlayabilir ya da boş bir kanvasla başlayabilir
2. **Yüzeyleri değiştir** — Üstteki sekme, t-shirt'in ön ve arka yüzeyi gibi yüzeyler arasında geçiş yapmalarını sağlar
3. **Eleman ekle** — Araç paneli, metin, görsel yükleme ve kliptograf araçlarını sağlar
4. **Özelleştir** — Fontlar, renkler, boyutlar, konumlar ve görsel filtreler gibi ayarları özelleştirebilir
5. **Fiyatı gör** — Elemanlar eklerken tasarım ücreti anında güncellenir
6. **Tasarımı kaydet** — Kayıtlı müşteriler tasarımları daha sonra düzenlemek için kaydedebilir
7. **Sepete ekle** — Tasarım, sipariş verildiğinde sepet öğesine bağlanır ve dondurulur

## Sipariş verildikten sonra ne olur

Bir müşteri, özelleştirilmiş bir ürün içeren bir sipariş verdiğinde:

- Tasarım **donmuş bir anlık görüntü** olarak dondurulur — satın alma sonrası değiştirilemez
- Sistem, her yüzey için **yüksek çözünürlüklü teslimat dosyaları** oluşturur
- Bu baskıya hazır dosyaları, admin panelinizdeki sipariş detay sayfasından indirebilirsiniz
- Dosyalar, her yüzey için yapılandırdığınız DPI'de işlenir

Özelleştirilmiş siparişleri tamamlamak için [Özelleştirilebilir Ürün Siparişlerini Tamamlama](/admin/orders/)

## İpuçları

- Çok yüzeyli ürünler gibi t-shirt'leri ele almadan önce, bir yüzeyli basit ürün (örneğin bir afiş) ile ayarlamayı öğrenin.
- Yüksek kaliteli mockup görselleri yükleyin — bunlar müşterilerin ilk gördüğü şeydir ve tüm deneyim için kalite beklentisini belirler.
- Her ürün için 3-5 tasarım şablonu oluşturun — boş kanvas korkusunu azaltın ve müşterileri ilhamlandırın.
- Her yüzey için kısıtlamalar kullanın ve müşterilerin her yüzeyde ne yapabileceğini kontrol edin. Örneğin, bir t-shirt koluna sadece küçük bir logoyu yükleme izni verirken, ön yüzeyde tam tasarım özgürlüğü sağlayabilirsiniz.
- Yazdırma yönteminize uygun minimum DPI gerekliliklerini ayarlayın — ekran baskıları için 150 DPI, yüksek kaliteli dijital baskılar için 300 DPI.
- Özelleştirilebilir bir ürün yayımlamadan önce tam müşteri akışını (tasarım, kaydet, sepete ekle, ödeme) test edin.