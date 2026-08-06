---
title: Müşteri Aboneliklerini Yönetme
---

Müşteri abonelikleri bölümü, mağazanızdaki tüm aktif, duraklatılmış ve iptal edilmiş tekrarlayan abonelikler hakkında tam bir görünüm sunar. Buradan faturalandırma sağlığını izleyebilir, bireysel abonelik detaylarını görüntüleyebilir ve sorunlar oluştuğunda eylem alabilirsiniz.

## Müşteri aboneliklerini görüntüleme

**Abonelikler > Müşteri Abonelikleri**'ne giderek tüm müşteriler arasındaki aboneliklerin tamamını görebilirsiniz.

![Müşteri abonelikleri listesi](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

Liste, her abonelik için müşteri, plan adı, mevcut durum, bir sonraki faturalandırma tarihi ve tamamlanan faturalandırma döngüsünün sayısını gösterir.

### Filtreleme ve arama

Sağdaki filtre panelini kullanarak abonelikleri şu şekilde daraltabilirsiniz:

- **Durum** — Aktif, Deneme, Vadesi Doldu, Duraklatılmış, İptal Edildi veya Süresi Doldu olarak filtreleme
- **Plan** — Belirli bir plan için abonelikleri görüntüleme
- **Sağlayıcı Modu** — Özgün (Stripe/PayPal tarafından yönetilen) veya Geri Dönüş (iç faturalandırma)

Arama çubuğunu kullanarak müşteri e-posta adresine göre abonelikleri arayabilirsiniz.

## Abonelik durumları

Her durumun ne anlama geldiğini anlamak, dikkat edilmesi gereken abonelikleri belirlemek için size yardımcı olur:

| Durum | Ne anlama gelir |
|--------|----------------|
| **Deneme** | Müşteri, ücretsiz ya da indirimli fiyatlı deneme dönemindeler |
| **Aktif** | Abonelik sağlıklıdır — faturalandırma güncel ve erişim aktiftir |
| **Vadesi Doldu** | Bir ödeme denemesi başarısız oldu — sistem yeniden denemektedir. Müşteri, geçim süresi boyunca erişimine devam eder |
| **Duraklatılmış** | Abonelik geçici olarak duraklatılmıştır — faturalandırma yapılmaz, erişim yok |
| **İptal Edildi** | İptal talebi yapılmıştır. Müşteri, dönem sonuna kadar erişimine devam edebilir |
| **Süresi Doldu** | Abonelik tamamen sona erdi — deneme süresi doldu, maksimum faturalandırma döngüsü eklendi veya iptal süresi geçti |

**Vadesi Doldu** olan abonelikler, en çok dikkat etmeniz gerekenlerdir — ödeme devam ederse ve geçim süresi biterse, abonelik duraklatılacaktır.

## Bir aboneliğin detaylarını görüntüleme

Herhangi bir aboneliğe tıklayarak detay görünümünü açabilirsiniz. Bunu gösterir:

### Şu anki faturalandırma dönemi

- **Şu anki Dönem Başlangıç / Bitiş** — Aktif faturalandırma penceresinin tarihleri
- **Bir Sonraki Faturalandırma Tarihi** — Bir sonraki tahsilatın yapılması beklenen tarih
- **Son Faturalandırma Tarihi** ve **Son Faturalandırma Durumu** — En son faturalandırma denemesinin sonucu
- **Faturalandırma Döngüsü Sayısı** — Tamamlanan başarılı faturalandırma döngüsünün sayısı

### Abonelik bilgisi

- **Plan** ve **Faturalandırma Seviyesi** — Müşterinin hangi plan ve faturalandırma sıklığı üzerinde olduğuna dair bilgi
- **Ürün / Variant** — Bu abonelikle ilişkili olan katalog ürününü (varsa)
- **Miktar** — Kullanım hakkı veya birim sayısı (miktar temelli planlar için)
- **Ödeme Tokenı** — Tekrarlayan faturalandırma için kullanılan saklı ödeme yöntemi

### Deneme detayları

Abonelik deneme aşamasındaysa, **Deneme Bitiş Tarihi**, müşterinin denemenin bittiğini ve tam faturalandırmanın başladığını gösterer.

### İptal detayları

İptal edilmiş abonelikler için şunları görebilirsiniz:

- **İptal Türü** — İptal, dönem sonuna kadar ya da planlanmış mı
- **İptal Edildiğinde** — İptalin istendiği tarih
- **İptal Nedeni** — Müşterinin iptal nedeniyle notlar (varsa)
- **Yeniden Aktivasyon Süresi** — Müşterinin tamamen yeniden abone olmadan önce yeniden aktif hale gelebileceği son tarih

### Geçim süresi ve taahhütler

- **Geçim Süresi Bitiş Tarihi** — Bir ödeme başarısız olursa, erişimin askıya alınmadan önceki son tarih
- **Minimum Taahhüt Bitiş Tarihi** — Minimum taahhütleri olan planlar için, en erken iptal tarihi

## Bir aboneliği duraklatma

Bir abonelik, geçici olarak faturalandırma yapmayı ve erişimi askıya almayı durdurur. Bu, tamamen iptal etmek yerine bir süre durmak isteyen müşteriler için yararlıdır.

Duraklatılmış abonelikleri görüntülemek için **Durum: Duraklatılmış**'a göre filtreleme yapabilirsiniz. Detay görünümü şunları gösterir:

- **Duraklatma Zamanı** — Duraklatmanın başladığı tarih
- **Duraklatma Nedeni** — Nedeniyle duraklatıldığını belirten notlar
- **Otomatik Olarak Devam Etme Tarihi** — Ayarlandıysa, aboneliğin faturalandırma ve erişim açısından otomatik olarak devam edeceği tarih

Abonelikler, otomatik devam tarihi veya müşteri tarafından elle yeniden başlatıldığında devam eder.

## Faturalandırma döngüsü kayıtları

Her faturalandırma denemesi — başarılı ya da başarısız olsa da — faturalandırma döngüsü loguna kaydedilir. Bu tarihi görüntülemek için **Abonelikler > Faturalandırma Döngüsü Kayıtları**'na gidin.

![Faturalandırma döngüsü logu listesi](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Bir faturalandırma döngüsü logu girişini okuma

Her log girişi şunları kaydeder:

- **Abonelik** — Bu faturalandırma denemesinin hangi müşteri aboneliğine ait olduğunu belirtir
- **Döngü Numarası** — Sıralı faturalandırma döngüsü (Döngü 1 = deneme sonrası ilk ödeme)
- **Faturalandırma Tarihi** — Ödemenin yapıldığı tarih
- **Durum** — Bekleme, İşleme, Başarılı, Başarısız veya Tekrarlama
- **Tutar analizi**:
  - **Temel Tutar** — Herhangi bir düzeltme yapılmadan önce plan fiyatını belirtir
  - **Miktar Tutarı** — Koltuk/birim miktarı için ekstra ödeme
  - **Ekstra Tutarı** — Etkin ekstra eklerin toplam maliyeti
  - **İndirim Tutarı** — Uygulanan toplam indirimler
  - **Toplam Tutar** — Sonuçta tahsil edilen (ya da denenen) tutar
- **Ödeme Yöntemi** — Kullanılan karta ya da ödeme yöntemine ait bilgi
- **Sağlayıcı İşlem Kimliği** — Ödeme sağlayıcısının referans numarası (iade sorguları için yararlıdır)
- **Başarısızlık Nedeni** — Faturalandırma başarısız olursa, nedeninin ne olduğu (örneğin, kart reddedildi, yetersiz bakiye)

### Ödeme hatalarının tanılanması

Bir müşteri, faturalandırma sorunu hakkında size ulaşırsa, aboneliğini bul ve faturalandırma döngüsü kayıtlarını kontrol et. **Başarısızlık Nedeni** alanı neyin yanlış gittiğini açıklar. Sık karşılaşılan başarısızlık nedenleri şunlardır:

- **Kart reddedildi** — Müşteri kartı bankası tarafından reddedildi
- **Yetersiz bakiye** — Faturalandırma anında hesap bakiyesi yetersiz
- **Kart süresi doldu** — Kayıtlı ödeme yöntemi süresi doldu
- **Ağ hatası** — Ödeme sağlayıcısıyla olan geçici bir bağlantı problemi — genellikle tekrar denemede çözülür

Sürekli başarısızlıklar için, müşteriye hesap ayarlarında ödeme yöntemini günclemesini önerin.

## Yeniden doğrulanmanın nasıl yerine getirildiğine dair

Her başarılı yeniden doğrulanma ödemesi, bu faturalandırma döngüsü için yeni bir ödeme siparişi oluşturur — sadece bir ödeme kaydı değildir. Bu sipariş, alışveriş yaparken yapılan bir siparişle aynı şekilde normal teslimat sürecine girer:

- **Fiziksel ürünler** — Yeniden doğrulanma siparişi, abonelik ile başlayan siparişin sevkiyat ve faturalandırma bilgilerini kopyalar. Bu nedenle, kartın hemen ardından stoktan ayrılmaz, bu nedenle geçici stok eksikliği, zaten başarılı olan bir ödemeyi engellemez — yine de siparişi görür ve stok miktarına göre teslim edebilirsiniz.
- **Dijital ürünler** — Yeniden doğrulanma siparişi oluşturulduğunda, ilk kez satın alındığı gibi, indirme linkleri, lisans anahtarları gibi erişim otomatik olarak yeniden verilir.

Yeniden doğrulanma siparişleri, aboneliği başlatan siparişin sevkiyat ve faturalandırma bilgilerini kopyalar, bu nedenle bir şeyi tekrar girmek gerekmez. **Siparişler** listesinde özel bir nişangah taşımayabilir, ancak herhangi bir döngüyü o siparişe izleyebilirsiniz. **Abonelikler > Faturalandırma Döngüsü Kayıtları**'na açın, bu döngü için log girişi üzerine tıklayın ve **Sipariş** alanındaki bağlantı doğrudan ona gider.

## Otomatik abonelik e-postaları

Spwig, abonelik yaşam döngüsü e-postalarını otomatik olarak gönderir — bunları manuel olarak tetiklemek gerekmez. İş sahiplerinin en çok sorduğu e-postalar:

| E-posta | Ne zaman gönderildiği |
|-------|----------------|
| **Yeniden doğrulama hatırlatması** | Bir sonraki yeniden doğrulama ödemesinden önce |
| **Deneme bitiyor** | Ücretsiz ya da indirimli deneme süresinin tamamlayıcı faturalandırma ile dönüştüğüne dair |
| **Ödeme başarısızlığı** | Yeniden doğrulama ödemesi başarısız olduğunda hemen sonra, ve grace periodunun biteceği zaman son bir uyarı olarak |
| **İptal onayı** | Abonelik iptal edildiğinde |

Spwig, ilgili abonelik yaşam döngüsünde noktalarda konuk, ödeme başarılı, duraklatma/devam, sona erme, yeniden başlatma, plan değişikliği ve ödeme yöntemi sona erme e-postalarını da gönderir.

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

Bunların hepsi sıradan bir e-posta şablonudur — içeriklerini inceleyip özelleştirmek ve bunların etkin olduğundan emin olmak için [E-posta Şablonları](/help/email-templates)'na bakın.

## Müşteri tarafından kendi kendine hizmet

Müşteriler, sıradan bir abonelik değişikliği için sana ulaşmak zorunda kalmaz — hesaplarında bulunan aboneliklerini, detayları ve fatura tarihçesi, duraklatma, devam ettirme, iptal etme ve dosyadaki ödeme yöntemini güncelleme gibi işlemleri kendi hesaplarından yönetebilirler. Bu, destek kuyruğuna gelenlerin çoğu için yeterli olur. Bir müşteri aboneliği hakkında sana ulaşır ise, onun hesap sayfasını denediğini kontrol etmek için önce senin onlar için değişikliği yapman gerekir.

## İpuçları

- Aboneliklerin çerez riski taşıyıp taşımadığını kontrol etmek için **Gecikmiş** filtresini haftada bir kez kontrol edin. Müşteriye kısa bir e-posta atmak, kurtarma süresi dolmadan önce ödeme sorunlarını çözebilir.
- Faturalandırma döngüsü logları sadece okunur olup, otomatik olarak oluşturulur ve değiştirilemez. Bunu, güvenilir bir denetim izi sağlar.
- Bir müşterinin aboneliği **Gecikmiş** olarak görünürse ve zaten ödeme yöntemini güncellediyse, bir sonraki otomatik tekrar denemesi yeni kartı alır. Tekrarlar, plan içinde yapılandırılan kurtarma süresi planına göre gerçekleşir.
- **Süresi dolduğu** abonelikler silinmez — raporlama için görünür kalır. Şu anki aktif aboneliklere odaklanmak için tarih filtrelerini kullanın.
- **Deneme** aşamasındaki abonelikler için **Deneme Bitiş Tarihi**'ni kontrol ederek yakında gelecek ilk ödeme ve ödeme yöntemi sorunlarını önceden tahmin edin.
- Bir müşteri, fiziksel bir yenilemenin "hiç gönderilmediğini" söylüyorsa, abonelik kaydına değil, normal teslimat kuyruğuna bakın — yeniden yapılan abonelikler, diğer tüm siparişler gibi aynı şekilde işlenir ve kuyruğu atlar.