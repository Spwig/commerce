---
title: Ödeme Ayarları
---

Ödeme sağlayıcıları, mağazanızı ödeme geçitlerine bağlayarak müşterilerinizin kredi kartları, dijital cüzdanlar ve diğer ödeme yöntemlerini ödeme sırasında kabul edebilmesini sağlar. Spwig, birden fazla sağlayıcıyı aynı anda destekler, böylece müşterilerinize esnek ödeme seçenekleri sunar.

![Ödeme sağlayıcıları](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Mevcut Sağlayıcılar

| Sağlayıcı | Açıklama |
|----------|-------------|
| **Stripe** | Kredi kartları, Apple Pay, Google Pay ve 135+ döviz |
| **PayPal** | PayPal bakiyesi, kredi/borc kartları ve Daha Sonra Öde seçenekleri |
| **Airwallex** | Çarşaf ticaretine yönelik optimize edilmiş çok dövizli ödemeler |
| **Adyen** | Dünyanın 250+ ödeme yöntemi ile kurumsal düzeyde ödemeler |
| **Square** | Entegre POS desteği ile yüz yüze ve çevrimiçi ödemeler |
| **Revolut** | Rekabetçi FX oranlarıyla hızlı Avrupa ödemeleri |

## Sağlayıcıyı Bağlama

**Ayarlar > Ödeme Sağlayıcıları**'na gidin ve **Sağlayıcıyı Bağla**'yı tıklayarak kurulum asistanını başlatın.

### Adım 1: Sağlayıcı Seçin

Mevcut ödeme sağlayıcılarından birini seçin. Her kart, sağlayıcının desteklediği özellikler ve bölgeleri gösterir.

### Adım 2: Kurulum Talimatları

Sağlayıcıya özel kurulum kılavuzunu inceleyin. Bu şunları içerir:
- Sağlayıcı ile bir hesap oluşturmak için nasıl yapmanız gerektiğini (eğer bir hesabınız yoksa)
- Sağlayıcının paneline girerek API kimlik bilgilerinizi nerede bulabileceğinizi
- Herhangi bir önkoşul (örneğin, iş doğrulaması)

### Adım 3: Kimlik Bilgilerini Girin

API kimlik bilgilerinizi girin:
- **API Anahtarı / Gizli Anahtar** — Sağlayıcının paneline girerek elde ettiğiniz kimlik bilgileriniz
- **Ödeme Modu** — Müşterilerin ödeme formuyla nasıl etkileşime geçeceği:

| Mod | Açıklama |
|------|-------------|
| **Barındırılmış** | Müşteriler, sağlayıcının ödeme sayfasına yönlendirilir (örneğin, Stripe Checkout). En basit kurulum, sağlayıcı tarafından PCI uygunluğu sağlanır. |
| **Entegre** | Ödeme formu, ödeme sayfasına doğrudan entegre edilir. Daha akıcı bir deneyim, ancak sağlayıcının JavaScript SDK'sı gereklidir. |

- **Deneme / Yaşam Modu** — Test etmek için deneme modunda başlayın, hazırsanız yaşam moduna geçin

### Adım 4: Bağlantıyı Test Et

**Bağlantıyı Test Et**'e tıklayarak kimlik bilgilerinizin geçerli olduğundan emin olun. Asistan, şunları kontrol eder:
- API anahtarı kimlik doğrulaması
- Hesap izinleri
- Webhook uç noktasının erişilebilirliği

### Adım 5: Yapılandır ve Kaydet

Sağlayıcı ayarlarını sonlandırın:
- **Etkin** — Sağlayıcıyı etkinleştirin veya devre dışı bırakın
- **Varsayılan Sağlayıcı** — Ödeme sırasında ana ödeme yöntemi olarak ayarlayın
- **Gösterilen Ad** — Müşterilere ödeme sırasında gösterilen ad
- **Sıra Numarası** — Sağlayıcıların ödeme sırasında görünüm sırasını kontrol eder (düşük numaralar önce görünür)

## Ödeme Paneli

**Ayarlar > Ödeme Paneli**'ne gidin, ödeme aktivitelerinizin genel bir görünümü için.

### Gerekli Eylemler

Üstteki uyarı kartları, dikkat gerektiren sorunları vurgular:
- **Başarısız İşlemler** — İşlem yapılamayan ödemeler
- **Bekleyen Yakalama** — Yetkilendirilmiş ödemelerin yakalanmasını bekleyenler
- **Bağlantı Hataları** — Bağlantı sorunları olan sağlayıcılar

### Gelir Analitiği

- **Gelir Grafiği** — Zaman içinde ödeme hacminin görsel analizi, gün, hafta veya ay bazında gruplandırılmıştır
- **Performans Metrikleri** — Toplam gelir, başarı oranı, ortalama işlem değeri ve iade oranı
- **Sağlayıcı Karşılaştırması** — Bağlantılı sağlayıcılar için yan yana performans kartları

### İşlem Ayrıştırması

- **Durum Dağılımı** — Tamamlanan, bekleyen, başarısız ve iade edilen işlem sayıları
- **Ödeme Yöntemi Karışımı** — Müşterilerin en çok kullandığı ödeme yöntemleri (kredi kartı, PayPal, dijital cüzdanlar)

## Ödeme Yöntemlerini Yönetme

Her sağlayıcı farklı ödeme yöntemlerini destekler. Ülkeye göre belirli yöntemleri etkinleştirebilir ya da devre dışı bırakabilirsiniz:

1. Sağlayıcının yapılandırma sayfasına gidin
2. **Ödeme Yöntemleri** bölümüne kaydırın
3. Bireysel yöntemleri açıp kapatın
4. Ülkeye göre kontrolleri kullanarak yöntemleri belirli piyasalara sınırlayın

Bir ödeme yöntemi bir bölgede popüler ama başka bir bölgede değilse bunu faydalı hale getirir (örneğin, Hollanda'da iDEAL, Belçika'da Bancontact).

## Webhook'lar

Webhook'lar, ödeme sağlayıcısıyla mağazanızı gerçek zamanlı olarak senkronize eder. Aşağıdaki olayları işler:
- Ödeme tamamlandı veya başarısız oldu
- İadeler işlendi
- Tartışmalar ve iadeler açıldı
- Abonelik yenilenmeleri

### Otomatik Kurulum

Bir sağlayıcıyı bağladığınızda, Spwig sağlayıcıyla bir webhook uç noktası otomatik olarak kaydeder. Webhook URL'si sağlayıcının yapılandırma sayfasında gösterilir.

### Webhook İzleme

Her gelen webhook, şunlarla birlikte kaydedilir:
- **Olay Türü** (örneğin, payment_intent.succeeded)
- **Zaman damgası** ve işleme durumu
- **Yük** hata ayıklamak için

Bir webhook işleme başarısız olursa, bir hata olarak kaydedilir ve bunu inceleyebilirsiniz.

## Birden Fazla Sağlayıcı Kullanma

Birden fazla ödeme sağlayıcısını aynı anda bağlayabilirsiniz:

- **Varsayılan Sağlayıcı** — Ödeme sırasında varsayılan olarak seçilen sağlayıcı. Ayarlar sayfasında bir sağlayıcıyı varsayılan olarak işaretleyin.
- **Sıra Numarası** — Ödeme sırasında görüntülenme sırasını kontrol eder. Müşteriler, tüm etkin sağlayıcıları görür ve tercih ettikleri birini seçebilir.
- **Yedekleme** — Bir sağlayıcıda kesinti yaşanırsa, müşteriler hala alternatif bir sağlayıcı kullanarak ödeme yapabilir.

## İpuçları

- **Stripe** veya **PayPal** ile başlayın — bunlar, ödeme yöntemleri ve bölgeler açısından en geniş yelpazeyi kapsar.
- **Deneme/test modu** kullanarak canlı ortama geçmeden önce test işlemleri yapın. Her sağlayıcı, bel档ında test kart numaralarına sahiptir.
- **Birden fazla sağlayıcıyı** etkinleştirin, böylece bir sağlayıcıda sorun yaşanırsa müşterilerinize alternatif ödeme seçeneği olur.
- Tercih ettiğiniz sağlayıcının **düşük sıralama numarasını** ayarlayarak ödeme sırasında ilk olarak görünmesini sağlayın.
- Haftada bir **Ödeme Paneli**'ni izleyin, başarısız işlemleri ve bağlantı sorunlarını erken fark edin.
- API kimlik bilgilerinizi güvenli tutun — veritabanında şifrelenerek saklanırlar ancak hiçbir zaman paylaşmamalısınız.

