---
title: Webhook Genel Bakış
---

Webhooks, mağazanızda bir şey olduğunda, stok araçları, ERPs, teslimat hizmetleri veya özel uygulamalar gibi dış sistemleri otomatik olarak bilgilendirmenizi sağlar. Bu sistemlerin sürekli olarak 'bir şey değişti mi?' diye sormak zorunda kalmadan, mağazanız olay meydana geldiğinde hemen bir bildirim gönderir.

## Webhook'ların ne yaptığı

Mağazanızda bir olay gerçekleştiğinde (bir sipariş verildi, bir ödeme alındı, bir ürün stokta kalmadı), Spwig, yapılandırdığınız bir URL'ye olay verileriyle bir HTTP POST isteği gönderir. Alıcı sistem bu verilere hemen göre işlem yapabilir – örneğin, stokları güncelleyebilir, bir kargo etiketi tetikleyebilir veya özel bir bildirim gönderebilir.

Webhook'ların yaygın kullanım alanları şunlardır:

- Teslimat ortaklarıyla gerçek zamanlı sipariş senkronizasyonu
- Stok değişikliklerinde ERP'de stok güncelleme
- Sipariş durumu değişikliklerinde SMS veya push bildirimleri tetikleme
- Raporlama için veri ambarında olayları kaydetme
- Zapier veya Make gibi otomasyon araçlarıyla entegrasyon

## Uç noktaları görüntüleme ve yönetme

**Entegrasyonlar > Webhook'lar**'a giderek yapılandırılmış tüm webhook uç noktalarınızı görebilirsiniz.

![Webhook uç noktaları listesi](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

Liste, her uç noktanın adını, URL'sini, etkin durumunu, kaç olaya abone olduğunu, sağlığı durumunu ve son teslimatın ne zaman gerçekleştiğini gösterir.

### Sağlık göstergeleri

**Sağlık** sütunu, her uç noktanın nasıl çalıştığını hızlıca gösterir:

- **Sağlıklı** — Tüm son teslimatlar başarılı oldu
- **Düşük performanslı** — Bazı son başarısızlıklar var ama uç nokta hâlâ etkin
- **Sağlıksız / Devre dışı** — Uç nokta, çok fazla ardışık başarısızlık (varsayılan olarak 10) sonucu otomatik olarak devre dışı bırakıldı. Temel sorun çözüldüğünde, manuel olarak tekrar etkinleştirmeniz gerekir.

## Webhook uç noktası oluşturma

**+ Webhook Uç Noktası Ekle**'ye tıklayarak kurulum asistanını açın. Asistan, size dört adımı rehberlik eder.

### Adım 1: Temel bilgiler

- **Ad** — Bu uç noktayı tanımlamak için kullanıcı dostu bir etiket (örneğin, `Sipariş Teslimat Hizmeti` veya `Stok Senkronizasyonu`).
- **URL** — Webhook POST isteklerini alacak sunucunun tam URL'si. Bu, bir localhost URL'si olmamalı ve genel erişime açık olmalıdır.
- **Açıklama** — Bu uç noktanın ne için kullanıldığını anlatacak isteğe bağlı notlar.
- **Etkin** — Bu uç noktanın teslimatları alıp almayacağını belirler. Etkinleştirmeyi kaldırarak uç noktayı silmeden geçici olarak durdurabilirsiniz.

### Adım 2: Olay abonelikleri

Bu uç noktaya hangi olayların tetikleyeceği seçin. Olaylar kategoriye göre gruplandırılmıştır:

### Sipariş olayları

| Olay | Ne zaman tetiklenir |
|-------|---------------|
| `order.created` | Yeni bir sipariş verildi |
| `order.paid` | Bir sipariş için ödeme onaylandı |
| `order.cancelled` | Bir sipariş iptal edildi |
| `order.fulfilled` | Bir siparişin tüm ürünleri gönderildi |
| `order.partially_fulfilled` | Bir siparişin bazı ürünleri gönderildi |
| `order.status_changed` | Sipariş durumu değişti |
| `order.note_added` | Bir siparişe not eklendi |

### Ödeme olayları

| Olay | Ne zaman tetiklenir |
|-------|---------------|
| `payment.received` | Ödeme alındı |
| `payment.failed` | Ödeme denemesi başarısız oldu |
| `payment.pending` | Ödeme onay bekliyor |

### Teslimat olayları

| Olay | Ne zaman tetiklenir |
|-------|---------------|
| `shipment.created` | Teslimat oluşturuldu |
| `shipment.shipped` | Teslimat gönderildi |
| `shipment.delivered` | Teslimat teslim edildi |
| `shipment.returned` | Teslimat iade edildi |
| `shipment.tracking_updated` | Takip bilgileri güncellendi |

### Stok olayları

| Olay | Ne zaman tetiklenir |
|-------|---------------|
| `inventory.low_stock` | Stok, eşik düzeyinin altına düştü |
| `inventory.out_of_stock` | Bir ürün stokta kalmadı |
| `inventory.restocked` | Bir ürün yeniden stoke edildi |
| `inventory.adjusted` | Stok el ile ayarlandı |

### Ürün olayları

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

### Müşteri olayları

`müşteri.olusturuldu`, `müşteri.guncellendi`, `müşteri.silindi`

#### Abonelik olayları

`subscription.olusturuldu`, `subscription.etkinlestirildi`, `subscription.yenilendi`, `subscription.ibrazedildi`, `subscription.suresi_bitmis`, `subscription.duraklatildi`, `subscription.devam ettirildi`, `subscription.odeme_hatali`

#### Diğer olaylar

`geri_odeme.olusturuldu`, `geri_odeme.tamamlandi`, `geri_odeme.hatali`, `sepet.bırakıldı`, `sepet.kurtarildi`, `dil.dosya_tamamlandi`, `dil.dosya_hatali`

Tüm olayları almak için `*` (joker karakterine) abone olun. Bu, genel amaçlı günlükleme uç noktaları için faydalıdır ancak daha fazla trafiğe neden olur — üretim entegrasyonları için sadece gerçekten ihtiyacınız olan olaylara abone olun.

### Adım 3: Yapılandırma

- **Maksimum Tekrar Denemeleri** — Spwig'in başarısız bir teslimatı ne kadar tekrar denemelidir (varsayılan: 5). Her tekrar deneme, üssel geri çekilme aralığı kullanır.
- **Süre (Saniye)** — Alıcı sunucunun yanıt vermesini ne kadar bekleyeceğiniz (varsayılan: 30 saniye). Sunucunuzun yavaş olduğu biliniyorsa bu değeri artırın.

### Adım 4: Güvenlik

Her webhook uç noktası, otomatik olarak oluşturulan bir **imza gizli anahtarı** ile gelir — 64 karakterlik rastgele bir anahtar. Spwig, bu gizli anahtarı her webhook yüküne HMAC-SHA256 imzası ile imzalamak için kullanır.

İmza, `X-Webhook-Signature` istek başlığında yer alır. Alıcı sunucunuz, bu imzayı doğrulamalıdır, böylece isteğin gerçekten mağazanızdan geldiğini ve manipüle edilmediğini onaylayabilir.

Gizli anahtar, yönetici panelinde maskelenmiş şekilde gösterilir. Gizli anahtarı görmek veya döndürmek için Spwig API'sini kullanın. Gizli anahtarın ihlal edildiğini düşünüyorsanız, hemen döndürün.

## Uç noktaları etkinleştirme ve devre dışı bırakma

Bir veya birkaç uç noktayı her birini açmadan hızlıca etkinleştirmek veya devre dışı bırakmak için:

1. Değiştirmek istediğiniz uç noktaların yanındaki onay kutularını seçin
2. **Eylem** açılır menüsünden **Seçilen uç noktaları etkinleştir** veya **Seçilen uç noktaları devre dışı bırak** seçeneğini seçin
3. **Git**'e tıklayın

Bir uç noktanın başarısızlıklar nedeniyle otomatik olarak devre dışı bırakıldığını fark ederseniz, onu seçin ve **Hata sayısını sıfırla** eylemini kullanın, ardından tekrar etkinleştirin. Hatalara neden olan şeyi önce düzeltin, aksi takdirde tekrar kısa sürede devre dışı bırakılacaktır.

## İpuçları

- Sadece gerçekten ihtiyacınız olan olaylara abone olun — gereksiz olaylar günlüklerinizde gürültü oluşturur ve teslimat yükünü artırır.
- Payload'ı işleyebilmeden önce alıcı sunucunuzda webhook imzasını her zaman doğrulayın. Bu, sahte isteklere karşı korunmanıza yardımcı olur.
- **Açıklama** alanını, bu uç noktanın hangi sistem veya entegrasyonla bağlantılı olduğunu kaydetmek için kullanın. Bu, aylar sonra sorun giderirken yardımcı olur.
- **Süre** değerini, sunucunuzun tipik yanıt süresinden biraz yüksek ayarlayın. 10–15 saniyelik bir süre, çoğu entegrasyon için yeterlidir.
- Bir uç nokta **Sağlam Değil** hale gelirse, önce (bkz. **Webhook Teslimatları**) teslimat günlüklerini kontrol edin, başarısızlık modelini anlayın ve ardından tekrar etkinleştirmeyi düşünün.
- Test etmek için, [webhook.site](https://webhook.site) gibi bir araçta webhook'ları yönlendirin, böylece canlı bir sunucuya ihtiyaç duymadan ham payload'ları inceleyebilirsiniz.