---
title: Ödeme Ayarları
---

Ödeme sağlayıcıları, mağazanızı ödeme geçitlerine bağlayarak, müşterilerinizin ödeme sırasında kredi kartlarını, dijital cüzdanları ve diğer ödeme yöntemlerini kabul edebilmesini sağlar. Spwig, birden fazla sağlayıcıyı aynı anda destekleyerek müşterilerinize esnek ödeme seçenekleri sunar.

![Ödeme sağlayıcıları](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Mevcut Sağlayıcılar

| Sağlayıcı | Açıklama |
|----------|-------------|
| **Stripe** | Kredi kartları, Apple Pay, Google Pay ve 135+ döviz |
| **PayPal** | PayPal bakiyesi, kredi/borç kartları ve Daha Sonra Öde seçenekleri |
| **Airwallex** | Çarşaf ticaretine yönelik optimize edilmiş çok dövizli ödemeler |
| **Square** | Entegre POS desteğiyle yüz yüze ve çevrimiçi ödemeler |
| **Revolut** | Rekabetçi FX oranlarıyla hızlı Avrupa ödemeleri |

## Sağlayıcıyı Bağlama

**Ayarlar > Ödeme Sağlayıcıları**'na gidin ve **Sağlayıcıyı Bağla**'ya tıklayarak kurulum asistanını başlatın.

### Adım 1: Sağlayıcı Seçin

Mevcut ödeme sağlayıcılarından birini seçin. Her kart, sağlayıcının desteklediği özellikler ve bölgeleri gösterir.

### Adım 2: Kurulum Talimatları

Sağlayıcıya özel kurulum kılavuzunu inceleyin. Bu şunları içerir:
- Sağlayıcı ile bir hesap oluşturmak (eğer yoksa)
- Sağlayıcının paneline girerek API kimlik bilgilerinizi nerede bulabileceğinizi
- Herhangi bir önkoşul (örneğin, iş doğrulaması)

### Adım 3: Kimlik Bilgilerini Girin

API kimlik bilgilerinizi girin:
- **API Anahtarı / Gizli Anahtar** — Sağlayıcının paninden alınan kimlik bilgileriniz
- **Ödeme Modu** — Müşterilerin ödeme formuyla nasıl etkileşime geçeceği:

| Mod | Açıklama |
|------|-------------|
| **Barındırılmış** | Müşteriler, sağlayıcının ödeme sayfasına yönlendirilir (örneğin, Stripe Checkout). En basit kurulum, sağlayıcı tarafından PCI uygunluğu yönetilir. |
| **Entegre** | Ödeme formu, ödeme sayfasına doğrudan entegre edilir. Daha akıcı deneyim, ancak sağlayıcının JavaScript SDK'sı gereklidir. |

- **Deneme / Yaşam Modu** — Test için deneme modunda başlayın, hazırsanız canlı moduna geçin

### Adım 4: Bağlantıyı Test Et

**Bağlantıyı Test Et**'e tıklayarak kimlik bilgilerinizin geçerli olup olmadığını doğrulayın. Asistan şu şeyleri kontrol eder:
- API anahtarı kimlik doğrulaması
- Hesap izinleri
- Webhook uç noktası erişilebilirliği

### Adım 5: Ayarla ve Kaydet

Sağlayıcı ayarlarını tamamlayın:
- **Aktif** — Sağlayıcıyı etkinleştirin veya devre dışı bırakın
- **Varsayılan Sağlayıcı** — Ödeme sırasında ana ödeme yöntemi olarak ayarlayın
- **Gösterilecek Ad** — Müşterilere ödeme sırasında gösterilecek ad
- **Sıra Numarası** — Ödeme sağlayıcılarının ödeme sırasında görünme sırasını kontrol eder (daha düşük numaralar önce görünür)

## Ödeme Panosu

**Ayarlar > Ödeme Panosu**'na giderek ödeme aktivitenizin genel bir görünümüne ulaşın:

### Yapılacak İşler

En üstteki uyarı kartları, dikkat gerektiren sorunları vurgular:
- **Başarısız İşlemler** — İşlem yapılamayan ödemeler
- **Bekleyen Yakalama** — Yakalanmayı bekleyen onaylanmış ödemeler
- **Bağlantı Hataları** — Bağlantı sorunları olan sağlayıcılar

### Gelir Analitiği

- **Gelir Grafiği** — Zaman içinde ödeme hacminin görsel analizi, gün, hafta veya ay bazında gruplandırılmış
- **Performans Metrikleri** — Toplam gelir, başarı oranı, ortalama işlem değeri ve iade oranı
- **Sağlayıcı Karşılaştırması** — Bağlantılı her sağlayıcı için yan yana performans kartları

### İşlem Ayrıştırması

- **Durum Dağılımı** — Tamamlanan, bekleyen, başarısız ve iade edilen işlem sayıları
- **Ödeme Yöntemi Karışımı** — Müşterilerin en çok kullandığı ödeme yöntemleri (kredi kartı, PayPal, dijital cüzdanlar)

## Ödeme Yöntemlerini Yönetme

Her sağlayıcı farklı ödeme yöntemlerini destekler. Ülkeye göre belirli yöntemleri etkinleştirebilir ya da devre dışı bırakabilirsiniz:

1. Bir sağlayıcının yapılandırma sayfasına gidin
2. **Ödeme Yöntemleri** bölümüne kaydırın
3. Bireysel yöntemleri açıp kapatın
4. Ülkeye göre kontrolleri kullanarak yöntemleri belirli pazarlara sınırlayın

Bir ödeme yöntemi bir bölgede popüler ancak başka bir bölgede değilse bu çok yararlıdır (örneğin, Hollanda'da iDEAL, Belçika'da Bancontact).

## Webhook'lar

Webhooks, mağazanızı ödeme sağlayıcısıyla gerçek zamanlı olarak senkronize tutar.

Aşağıdaki olayları işler:
- Ödeme tamamlandı veya başarısız oldu
- İadeler işlendi
- Dispute ve chargeback açıldı
- Abonelik yenilenmeleri

### Otomatik Kurulum

Bir sağlayıcıyı bağladığınızda, Spwig otomatik olarak bir webhook uç noktasını sağlayıcıyla kaydeder. Webhook URL'si sağlayıcının yapılandırma sayfasında referans olarak görüntülenir.

### Webhook İzleme

Her gelen webhook, aşağıdaki bilgilerle birlikte kaydedilir:
- **Olay türü** (örneğin, payment_intent.succeeded)
- **Zaman damgası** ve işleme durumu
- **Payload**, hata ayıklama için

Bir webhook işleme başarısız olursa, hata olarak kaydedilir ve bunu inceleyebilirsiniz.

## Birden Fazla Sağlayıcı Kullanma

Aynı anda birden fazla ödeme sağlayıcısını bağlayabilirsiniz:

- **Varsayılan Sağlayıcı** — Ödeme sırasında varsayılan olarak seçilen sağlayıcı. Sağlayıcının yapılandırmasında bir sağlayıcıyı varsayılan olarak işaretleyin.
- **Sıra Numarası** — Ödeme sırasında görüntülenme sırasını kontrol eder. Müşteriler tüm aktif sağlayıcıları görür ve tercih ettiklerini seçebilir.
- **Yedekleme** — Bir sağlayıcıda kesinti yaşanırsa, müşteriler hâlâ alternatif bir sağlayıcı kullanarak ödeme yapabilir.

## İpuçları

- Başlamak için **Stripe** veya **PayPal** kullanın — bunlar en geniş ödeme yöntemlerini ve bölgelerini kapsar.
- **Test ortamı** kullanarak canlıya geçmeden önce test işlemleri yapın. Her sağlayıcı belgelerinde test kart numaraları vardır.
- **Birden fazla sağlayıcıyı** etkinleştirin, böylece bir sağlayıcıda sorun yaşanırsa müşterilere alternatif ödeme seçeneği sunulur.
- Tercih ettiğiniz sağlayıcının **düşük bir sıralama numarası** ayarlayın, böylece ödeme sırasında ilk olarak görünür.
- Haftalık olarak **Ödeme Panelini** izleyin, başarısız işlemler ve bağlantı sorunlarını erken fark edin.
- API kimlik bilgilerinizi güvenli tutun — veritabanında şifrelenerek saklanırlar ancak hiçbir şekilde paylaşilmemelidir.