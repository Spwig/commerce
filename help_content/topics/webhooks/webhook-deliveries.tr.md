---
title: Webhook Teslimat Günlükleri
---

Mağazanız bir webhook göndermeye çalıştığında, her seferinde bir teslimat günlüğü girişi oluşturulur. Bu günlükler, neyin gönderildiğini, başarılı olup olmadığını ve herhangi bir tekrar deneme sırasında ne olduğunu görmek için kullanılır. Bu kılavuz, teslimat günlüklerini nasıl okuyacağınızı ve teslimatlar başarısız olduğunda sorunları nasıl giderileceğini açıklar.

## Teslimat Günlüklerini Görüntüleme

**Entegrasyonlar > Webhook Teslimatları** menüsünden, tüm uç noktalarınız için tüm webhook teslimatı girişlerinin tam tarihini görebilirsiniz.

![Webhook teslimat günlükleri](/static/core/admin/img/help/webhook-deliveries/delivery-list.webp)

Liste, her teslimatın uç nokta adını, olay türünü, durumunu, HTTP yanıt kodunu, yanıt süresini ve kaç deneme yapıldığını gösterir.

Teslimat günlükleri sadece okunabilir – olaylar tetiklendiğinde otomatik olarak oluşturulur ve düzenlenemez.

## Teslimat Durumları

Her teslimat şu durumlardan birine sahiptir:

| Durum | Ne anlama gelir |
|--------|---------------|
| **Beklemede** | Teslimat kuyruğa alındı ve henüz deneme yapılmadı |
| **Başarılı** | Alıcı sunucu HTTP 2xx durum kodu ile yanıt verdi – teslimat onaylandı |
| **Başarısız** | Tüm teslimat denemeleri tükendi – teslimat tekrar denemeyecek |
| **Yeniden Deneme** | En son deneme başarısız oldu, ancak sistem planlanan yeniden deneme zamanında tekrar deneyecek |
| **Kutu Engellendi** | Teslimat, mevcut ortamda uç nokta URL'si erişilebilir değil olduğu için engellendi |

Teslimat, alıcı sunucunun herhangi bir HTTP 2xx yanıt kodu (200, 201, 202 vb.) döndürmesi durumunda başarılı olarak kabul edilir. Diğer herhangi bir yanıt – 3xx yönlendirmeleri veya 4xx/5xx hataları – başarısız olarak kabul edilir.

## Teslimatları Filtreleme

Sağdaki filtre panelini kullanarak listeyi daraltabilirsiniz:

- **Durum** – Sadece başarısız, yeniden deneme veya başarılı teslimatları görüntüleyin
- **Olay Türü** – Belirli bir olay için tüm teslimatları görün (örneğin, tüm `order.created` teslimatları)
- **Uç Nokta** – Belirli bir uç nokta için teslimatları görüntüleyin
- **Oluşturulma Zamanı** – Tarih aralığına göre filtreleyin

Arama çubuğunu, olay türüne veya uç nokta adına göre aramak için veya belirli bir teslimatı ID'sine göre bulmak için kullanın.

## Teslimat Detayı Okuma

Herhangi bir teslimatı tıklayarak tam detayını görüntüleyebilirsiniz. Teslimat kayıtları sadece okunabilir.

### Özet

- **ID** – Bu teslimat girişinin benzersiz kimliği
- **Uç Nokta** – Bu teslimatın gönderildiği webhook uç noktası (uç nokta kaydı bağlantısı)
- **Olay Türü** – Bu teslimatı tetikleyen olay (örneğin, `order.paid`)
- **Durum** – Mevcut teslimat durumu

### Yük

**Yük** bölümü, uç noktanıza gönderilen tam JSON verisini gösterir. Bu, olay türünü, bir zaman damgasını ve tam olay verisini içerir. Bu, alıcı sunucunuzun doğru veri yapısını alıp almadığını doğrulamak için kullanılır.

### Yanıt

**Yanıt** bölümü, sunucunuzun verdiği yanıtı gösterir:

- **Yanıt Durum Kodu** – Sunucunuzun döndürülen HTTP durum kodu. Renk kodlama: 2xx (başarı) için yeşil, 4xx (istemci hatası) için sarı, 5xx (sunucu hatası) için kırmızı.
- **Yanıt Süresi** – Sunucunuzun yanıt vermesi için geçen süre milisaniyeler cinsinden. Renk kodlama: 500 ms altında yeşil, 2 saniyeye kadar sarı, 2 saniyeden fazla kırmızı.
- **Yanıt Vücudu** – Sunucunuzun yanıtı (1.000 karaktere kadar kırpılmış). Bu, sunucunuzun webhook'u neden reddettiğini belirlemeye yardımcı olabilir.
- **Yanıt Başlıkları** – Sunucunuzun döndürülen başlıklar.

### Hata Detayı

Teslimat başarısız olursa, **Hata Detayı** bölümü hata mesajını gösterir – örneğin, `Bağlantı reddedildi`, `30 saniye sonra zaman aşımı` veya sunucunuzdan gelen HTTP hatası.

### Yeniden Deneme Bilgisi

- **Deneme Sayısı** – Kaç tane teslimat denemesi yapıldı (ilk deneme dahil)
- **Bir Sonraki Yeniden Deneme Zamanı** – Bir sonraki yeniden deneme ne zaman yapılacağı (yalnızca **Yeniden Deneme** durumunda olan teslimatlar için gösterilir)

Yeniden denemeler, üstel geri çekilme zamanlamasına göre yapılır – yeniden denemeler arasındaki aralık, her denemeyle birlikte artar ve geçici olarak kullanılamayan bir sunucuyu aşmamak için. 5 yeniden deneme (varsayılan) ile, yeniden deneme zamanlaması birkaç saat boyunca uzanır.

## Manually retrying failed deliveries

Eğer teslimatı otomatik zamanlamadan hemen tekrar denemek istiyorsanız:

1. Tekrar denemek istediğiniz teslimatların yanındaki onay kutularını seçin
2. **Eylem** açılır menüsünden **Seçilen teslimatları tekrar deneyin**'i seçin
3. **Git**'e tıklayın

Sadece **Başarı** durumunda olmayan teslimatlar tekrar deneme kuyruğuna alınır. Başarılı teslimatlar atlanır.

Bu, alıcı sunucunuzdaki bir sorunu düzelttiğinizde ve beklemek zorunda kalmadan başarısız olayları tekrar işleme isteğiniz olduğunda yararlıdır.

## Diagnosing common failures

### HTTP 4xx response codes

Sunucunuzdan gelen 4xx yanıt genellikle istekte bir sorunun olduğunu gösterir — kimlik doğrulama başarısız oldu, uç nokta URL'si değişti veya sunucunuz yük paylaşımlı formatı reddetti. Kontrol edin:

- Uç nokta URL'si doğru mu?
- Sunucunuz HMAC imzasını doğru şekilde doğruluyor mu? Uyuşmazlık, birçok sunucunun 401 veya 403 döndürmesine neden olur.
- Yük paylaşımlı yapı değişti mi? Teslimat günlüğündeki yük paylaşımlı veriyi sunucunuzun beklediği şeyle karşılaştırın.

### HTTP 5xx response codes

5xx yanıt, webhook işleme sırasında sunucunuzun iç hatası olduğunu gösterir. Sunucunuzun kendi hata günlüklerini inceleyerek sorunu tanımlayın.

### Connection refused / Timeout

Bu hatalar, Spwig'in sunucunuza hiç ulaşamadığını gösterir:

- Sunucu çalışıyor ve genel erişime açık mı?
- URL doğru mu (dahil edilen protokol — http veya https doğru mu)?
- Gelen istekleri engelleyen bir güvenlik duvarı var mı?
- Sunucunun yanıt süresi yapılandırılmış zaman aşımını aşıyor mu? Eğer öyleyse, uç nokta için **Zaman Aşımı** ayarını artırın veya sunucunuzun webhook işleyicisini hızlı yanıt vermesi için optimize edin (ideal olarak 5 saniye içinde).

### Sandbox Blocked

Teslimatlar localhost URL'lerine veya iç ağ adreslerine engellenir. Webhook uç noktaları genel erişime açık olmalıdır. Geliştirme sırasında bir yerel sunucuyu genel olarak göstermek için ngrok gibi bir araç kullanın.

## Tips

- **Başarısız** teslimatları hızlıca ele alın — olay verisi hâlâ yük paylaşımlı içinde ve sorun çözüldüğünde el ile tekrar deneyebilirsiniz.
- Eğer bir uç nokta için birçok **Tekrar Deneniyor** teslimatı varsa, uç nokta kaydını açın ve **Sağlık** bölümünü kontrol edin — uç nokta otomatik olarak devre dışı bırakılabilir.
- Yanıt süresi önemlidir: webhook işleyicinizi hızlı yanıt vermesi için yapılandırın (birkaç saniye içinde) ve yük paylaşımlı veriyi arka planda asenkron olarak işleme alın. Yavaş bir işleyici, mantığınız doğru olsa bile zaman aşımı hatalarına neden olur.
- **Olay Türü** filtresini kullanarak belirli bir olay türü için teslimat geçmişini kontrol edin, entegrasyonunuzun doğru olayları alıp almadığını araştırırken.
- Teslimat günlükleri zamanla birikir. Tarih filtresini kullanarak yeni teslimatlara odaklanın ve eski geçmişler arasında kaybolmaktan kaçının.