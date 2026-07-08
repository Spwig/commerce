---
title: Bırakılan Sepetler
---

Giriş yapmış bir müşteri, sepetine ürün ekledikten sonra 24 saat içinde ödeme tamamlamazsa, bir bırakılan sepet oluşturulur. Spwig, bu sepetleri otomatik olarak takip eder, kaybedilen gelirleri anlamanıza, müşterilerin neden terk ettiklerini belirlemek için desenleri tanımanıza ve satışları geri kazanmak için eylem almanıza yardımcı olur.

**Müşteriler > Bırakılan Sepetler** menüsüne giderek kaydedilen tüm bırakılan sepetleri görüntüleyebilirsiniz.

## Bırakılan sepetler listesinde ne görebilirsiniz

Liste görünümü, aşağıdaki bilgilerle birlikte her bırakılan sepeti gösterir:

| Sütun | Açıklama |
|---|---|
| **Müşteri** | Müşterinin adı ve e-postası |
| **Bırakılma Zamanı** | Sepetin bırakıldığı tarih ve saat |
| **Toplam Değer** | Bırakılma zamanında sepetteki ürünlerin maliyeti |
| **Toplam Ürün Sayısı** | Sepetteki ürün sayısı |
| **Tahmini Neden** | Spwig'in sepetin bırakılma nedeni hakkında en iyi tahmini |
| **Kurtarma Durumu** | Bu sepetin kurtarıldığı (tamamlanmış bir sipariş haline dönüştürüldüğü) mi yoksa kurtarılmadığı mı |
| **Bırakılma Sonrası Gün Sayısı** | Sepetin ne kadar önce bırakıldığını gösterir |

### Bırakılan sepetleri filtreleme

Listeyi daraltmak için sağ taraftaki filtreleri kullanın:

- **Tahmini Neden** — bırakılma nedenine göre filtreleyin (örneğin, yalnızca tahmini neden yüksek kargo ücreti olan sepetleri gösterin)
- **Kurtarıldı** — yalnızca kurtarılmış veya kurtarılmamış sepetleri göstermek için filtreleyin
- **Bırakılma Zamanı** — tarih aralığına göre filtreleyin, son bırakılan sepetleri veya belirli bir kampanya dönemini odaklanın

## Bırakılma nedenlerini anlama

Spwig, her bırakılan sepet için bir tahmini neden kaydeder. Bu nedenler, ödeme sürecinde yakalanan sinyallere dayanır ve kesin olarak garanti altına alınamaz, ancak bırakılma desenlerini tanılamak için faydalı bir başlangıç noktası sağlar.

| Neden | Ne ifade edebileceğini gösterir |
|---|---|
| **Bilinmeyen** | Özel bir sinyal yakalanmadı — en yaygın neden |
| **Yüksek Kargo Ücreti** | Müşteri, ödeme sırasında gösterilen kargo ücretiyle korkulmuş olabilir |
| **Toplam Çok Yüksek** | Genel sipariş toplamı, beklentiden daha yüksek olabilir |
| **Ödeme Sorunları** | Müşteri, ödeme sürecinde bir sorunla karşılaştı |
| **Ödeme Başarısız Oldu** | Ödeme denemesi yapıldı ancak başarısız oldu |
| **Fiyat Karşılaştırması** | Müşteri, fiyat karşılaştırması yapmak için ziyaret etmiş olabilir |
| **Daha Sonra için Kaydet** | Müşteri, ürünleri gelecekteki bir ziyaret için amaçlı olarak kaydetmiş olabilir |

Eğer aynı nedenle bırakılan sepetlerin büyük bir kısmı varsa — örneğin, "Yüksek Kargo Ücreti" bırakmalarının önemli bir kümelenmesi varsa — bu, kargo ayarlarınızı veya ödeme sunumunuzu incelemek için bir sinyaldir.

## Bireysel bırakılan sepeti görüntüleme

Listedeki herhangi bir satırı tıklayarak detay görünümünü açabilirsiniz. Aşağıdakileri göreceksiniz:

- **Bırakılma Detayları** — müşteri, sepet referansı, ne zaman bırakıldı ve tahmini neden
- **Sepet Özeti** — bırakılma zamanında ürün sayısı ve toplam değer
- **Kurtarma Takibi** — sepetin kurtarıldığı, ne zaman kurtarıldığı ve hangi siparişe dönüştürüldüğü

**Sepet** alanı, temel sepet kaydına doğrudan bağlantı sağlar, bu nedenle sepetteki ürünlerin neler olduğunu tam olarak görebilirsiniz.

## Kurtarma akışı

Spwig, her bırakılan sepetin sonunda tamamlanmış bir sipariş haline dönüştürüldüğünü takip eder. Müşteri, bırakılan sepetten bir satın alma tamamladığında, kayıt otomatik olarak **Kurtarıldı** olarak işaretlenir ve sonuçta oluşan sipariş bağlantılı hale gelir.

**Kurtarma E-postaları Gönderildi** sayacı, bu sepet için müşteriye gönderilen otomatik kurtarma e-postalarının sayısını gösterir. Bu, e-posta kampanyalarınızın müşterilerin geri dönmelerini teşvik edip etmediğini anlamaya yardımcı olur.

### Manuel kurtarma eylemleri

Bırakılan sepetler görünümü salt okunur — neyin olduğunu kaydeden bir kayıt, sepet içeriğini düzenlemek için bir araç değildir. Bırakılan sepetler üzerinde eylem almak için:

1. 

Bırakılan sepet kaydından müşterinin e-posta adresini not alın
2. 

E-posta sisteminizi veya pazarlama araçlarınızı kullanarak kişiselleştirilmiş bir mesaj gönderin
3. 

Müşterinin satın almayı tamamlaması için bir kupon kodu eklemeyi düşünün
4. 

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

Gerçekleşen (**Recovered**) durumunu takip edin ve ulaşımın etkili olup olmadığını sonraki günlerde görün