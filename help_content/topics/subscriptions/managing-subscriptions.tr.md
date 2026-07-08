---
title: Müşteri Aboneliklerini Yönetme
---

Müşteri abonelikleri bölümü, mağazanızdaki tüm etkin, duraklatılmış ve iptal edilmiş tekrar eden aboneliklerin tam bir görünümünü sağlar. Buradan faturalandırma sağlığına bakabilir, bireysel abonelik detaylarını görebilir ve sorunlar ortaya çıktığında işlem yapabilirsiniz.

## Müşteri aboneliklerini görüntüleme

**Abonelikler > Müşteri Abonelikleri** menüsünden tüm müşterilerin aboneliklerinin tam listesini görebilirsiniz.

![Müşteri abonelikleri listesi](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

Liste, her abonelik için müşteri, plan adı, geçerli durum, son fatura tarihi ve tamamlanmış fatura döngü sayısını gösterir.

### Filtreleme ve arama

Sağdaki filtre panelini kullanarak abonelikleri aşağıdaki kriterlere göre daraltabilirsiniz:

- **Durum** — Aktif, Deneme, Gecikmiş, Duraklatılmış, İptal Edilmiş veya Süresi Dolmuş durumlarına göre filtreleyin
- **Plan** — Belirli bir plan için abonelikleri görüntüleyin
- **Provider Mode** — Yerel (Stripe/PayPal yönetilen) veya Geri Dönüş (iç faturalandırma)

Arama çubuğunu kullanarak abonelikleri müşteri e-posta adresine göre bulabilirsiniz.

## Abonelik durumları

Her durumun anlamını anlamak, dikkat gerektiren abonelikleri tanımanıza yardımcı olur:

| Durum | Ne anlama gelir |
|--------|---------------|
| **Deneme** | Müşteri ücretsiz veya indirimli fiyatlı deneme döneminde |
| **Aktif** | Abonelik sağlıklı — faturalandırma güncel ve erişim aktif |
| **Gecikmiş** | Ödeme denemesi başarısız oldu — sistem tekrar deniyor. Müşteri, geçiş süresi boyunca erişimi korur |
| **Duraklatılmış** | Abonelik geçici olarak duraklatıldı — faturalandırma yok, erişim yok |
| **İptal Edilmiş** | İptal isteği yapıldı. Müşteri, dönem sonu tarihine kadar hala erişim sağlayabilir |
| **Süresi Dolmuş** | Abonelik tamamen sona erdi — deneme süresi doldu, maksimum fatura döngüleri ulaşıldı veya iptal süresi geçti |

**Gecikmiş** durumda olan abonelikler en çok dikkat gerektirir — ödeme devam edememişse ve geçiş süresi bittiğinde abonelik duraklatılacaktır.

## Bir abonelik detaylarını görüntüleme

Herhangi bir abonelik üzerine tıklayarak detay görünümünü açabilirsiniz. Bu, aşağıdaki bilgileri gösterir:

### Mevcut fatura dönemi

- **Mevcut Dönem Başlangıcı / Bitişi** — Aktif fatura penceresinin tarihleri
- **Sonraki Fatura Tarihi** — Sonraki ödeme denemesinin yapılacağı tarih
- **Son Fatura Tarihi** ve **Son Fatura Durumu** — En son fatura denemesinin sonucu
- **Fatura Döngü Sayısı** — Başarılı fatura döngü sayısının tamamlanması

### Abonelik bilgileri

- **Plan** ve **Fiyatlandırma Seviyesi** — Müşterinin hangi plan ve fatura sıklığında olduğunu gösterir
- **Ürün / Değişken** — Bu abonelikle ilişkili katalog ürününü (uygunsa) gösterir
- **Miktar** — Oturum sayısı veya birim sayısı (miktar bazlı planlar için)
- **Ödeme Token** — Tekrar eden faturalandırma için kullanılan depolanan ödeme yöntemi

### Deneme detayları

Abonelik deneme dönemindeyse, **Deneme Bitiş Tarihi** müşterinin deneme süresinin sona erdiği ve tam faturalandırmanın başladığı tarihi gösterir.

### İptal detayları

İptal edilmiş abonelikler için aşağıdaki bilgileri görebilirsiniz:

- **İptal Türü** — İptal, hemen, dönem sonunda veya planlanan bir tarihte yapıldı mı
- **İptal Tarihi** — İptal isteğinin yapıldığı tarih
- **İptal Nedeni** — Müşterinin neden iptal ettiğini belirten notlar (kayıt edilmişse)
- **Yeniden Aktifleştirme Son Tarihi** — Müşterinin yeniden aktifleştirmesi için son tarih (tekrar abone olmaksızın)

### Geçiş süresi ve taahhütler

- **Geçiş Süresi Bitiş Tarihi** — Ödeme başarısız olursa, erişimin durdurulacağı tarihi gösterir
- **Minimum Taahhüt Bitiş Tarihi** — Minimum taahhütlere sahip planlar için en erken iptal tarihi

## Bir aboneliği duraklatma

Duraklatılmış bir abonelik, faturalandırma geçici olarak durdurulurken erişimi de durdurur. Bu, tamamen iptal etmek istemeyen müşteriler için bir ara verme imkanı sağlar.

Duraklatılmış abonelikleri görmek için **Durum: Duraklatılmış** ile filtreleyin. Detay görünümü aşağıdaki bilgileri gösterir:

- **Duraklatılma Tarihi** — Duraklatmanın başladığı tarih
- **Duraklatma Nedeni** — Neden duraklatıldığını belirten notlar
- **Otomatik Devam Tarihi** — Ayarlanmışsa, abonelik faturalandırma ve erişimi otomatik olarak yeniden başlatılacağı tarih


Abonelikler, otomatik yeniden başlatma tarihinde veya müşteri tarafından el ile yeniden etkinleştirildiğinde devam eder.

## Fatura döngüsü günlükleri

Her fatura denemesi — başarılı veya başarısız — fatura döngüsü günlüğüne kaydedilir. **Abonelikler > Fatura Döngüsü Günlükleri**'ne giderek bu tarihi görüntüleyebilirsiniz.

![Fatura döngüsü günlüğü listesi](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Bir fatura döngüsü günlüğü girdisini okuma

Her günlük girdi aşağıdaki bilgileri kaydeder:

- **Abonelik** — Bu fatura denemesinin hangi müşteri aboneliğine ait olduğunu belirtir
- **Döngü Numarası** — Sırasıyla fatura döngüsü (Döngü 1 = deneme döneminden sonra ilk ücret)
- **Fatura Tarihi** — Ücretin ne zaman denendiği
- **Durum** — Beklemede, İşlemde, Başarılı, Başarısız veya Yeniden Deneme
- **Tutar analizi**:
  - **Temel Tutar** — Herhangi bir ayarlama yapılmadan önce plan fiyatı
  - **Miktar Tutarı** — Koltuk/ünite sayısına ek olarak ek ücret
  - **Ekstra Tutar** — Aktif ekstra maliyetlerin toplamı
  - **İndirim Tutarı** — Uygulanan toplam indirimler
  - **Toplam Tutar** — Sonuçta alınan (veya denenen) toplam tutar
- **Ödeme Yöntemi** — Kullanılan kredi kartı veya ödeme yöntemi
- **Provider İşlem Kimliği** — Ödeme sağlayıcısının referans numarası (iade araştırmaları için faydalıdır)
- **Başarısızlık Nedeni** — Eğer fatura başarısız olursa, neden başarısız olduğunu açıklar (örneğin, kredi kartı reddedildi, yetersiz bakiye)

### Ödeme başarısızlıklarını tanımlama

Bir müşteri bir fatura sorunundan bahsediyorsa, aboneliğini bulun ve fatura döngüsü günlüklerini inceleyin. **Başarısızlık Nedeni** alanı neyin yanlış gittiğini açıklar. Ortak başarısızlık nedenleri şunlardır:

- **Kart reddedildi** — Müşterinin bankası tarafından kredi kartı reddedildi
- **Yetersiz bakiye** — Fatura zamanında hesap bakiyesi çok düşüktü
- **Kartın son kullanma tarihi geçti** — Kaydedilmiş ödeme yöntemi sona erdi
- **Ağ hatası** — Ödeme sağlayıcısıyla geçici bir bağlantı sorunu — genellikle yeniden deneme ile çözülür

Sürekli başarısızlıklar varsa, müşteriyi hesap ayarlarında ödeme yöntemini güncellemeye yönlendirin.

## İpuçları

- Haftada bir kez **Gecikmiş** filtresini kontrol ederek churn riski taşıyan abonelikleri yakalayın. Müşteriye hızlı bir e-posta göndermek, genellikle grâce periodun sona ermeden önce ödeme sorunlarını çözer.
- Fatura döngüsü günlükleri sadece okunabilir — otomatik olarak oluşturulur ve değiştirilemez. Bu, güvenilir bir denetim kaydı sağlar.
- Eğer bir müşterinin aboneliği **Gecikmiş** olarak gösteriliyor ancak zaten ödeme yöntemini güncellediyse, sonraki otomatik yeniden deneme yeni kartı seçer. Yeniden denemeler, planda yapılandırılan grâce periodunun zaman çizelgesine göre yapılır.
- **Sona Eren** abonelikler silinmez — raporlama için görünür kalırlar. Tarih filtrelerini kullanarak şu anda aktif olan aboneliklere odaklanın.
- **Deneme** aşamasındaki abonelikler için **Deneme Bitiş Tarihi**'ni kontrol ederek yaklaşan ilk ücretleri öngörün ve ödeme yöntemi sorunlarını önceden çözmek için müşteriyle iletişime geçin.