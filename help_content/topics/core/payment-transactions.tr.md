---
title: Ödeme İşlemleri
---

Ödeme işlemleri, mağazanız üzerinden işlenen her ödeme olayının tamamını kaydeder — ücretler, iadeler, onaylamalar ve daha fazlası. Bu bölüm, ödeme sağlayıcılarınızdan gelen webhooks günlüklerini ve checkout sırasında oluşturulan ödeme niyetlerini de içerir.

## Ödeme İşlemleri

**Ödemeler > Ödeme İşlemleri** menüsüne giderek mağazanızın işlediği tüm işlemleri görebilirsiniz.

### İşlem Türleri

| Tür | Ne anlama gelir |
|-----|----------------|
| **Ödeme** | Anında ödeme — işlem sırasında para toplanır |
| **Onaylama** | Müşterinin kartında para tutulur ama henüz toplanmaz |
| **Toplama** | Önceki bir onaylamadan para toplanır |
| **İptal** | Toplama işleminden önce onaylama iptal edilir |
| **İade** | Müşteriye ödeme iade edilir |

### İşlem Durumları

| Durum | Ne anlama gelir |
|------|----------------|
| **Beklemede** | İşlem başlatıldı ama henüz işlenmedi |
| **İşleniyor** | Ödeme sağlayıcısı tarafından işleniyor |
| **Onaylandı** | Para tutuldu — toplamaya bekliyor |
| **Tamamlandı** | Ödeme başarılı oldu |
| **Başarısız** | Ödeme reddedildi veya bir hata oluştu |
| **İptal Edildi** | Toplama işleminden önce onaylama iptal edildi |
| **İade Edildi** | Tamamen iade edildi |
| **Kısmi İade** | Ödemenin bir kısmı iade edildi |

### Bir işlem kaydında ne görebilirsiniz

Her işlem şu bilgileri gösterir:
- **İşlem Kimliği** — Spwig içi referans
- **Sağlayıcı İşlem Kimliği** — Ödeme sağlayıcınızdan gelen referans (örneğin, Stripe ödeme kimliği)
- **Tutar** — İşlem tutarı ve para birimi
- **Durum** ve **Tür**
- **Müşteri E-postası** ve **Müşteri Adı**
- **Ödeme Yöntemi** — Tür (kredi kartı, banka havale vb.) ve son 4 hane
- **Sipariş** — Bu işlemin ait olduğu sipariş
- **Sağlayıcı Hesabı** — Bu işlemin işlendiği ödeme sağlayıcısı
- **Sağlayıcı Yanıtı** — Ödeme sağlayıcısından gelen ham teknik yanıt
- **Hata Mesajı** — İşlem başarısız olursa sağlayıcı tarafından verilen neden
- Oluşturma, son güncelleme ve tamamlama tarihleri

### İşlemleri Filtreleme

Yönetim filtrelerini kullanarak işlemleri şu kriterlere göre daraltabilirsiniz:
- Durum (örneğin, sadece başarısız işlemleri göster)
- Tür (örneğin, sadece iadeleri göster)
- Sağlayıcı hesabı
- Tarih aralığı

Bu, gün sonu dengeleme veya belirli bir müşterinin ödeme geçmişini incelemek için faydalıdır.

### Bir işlem ne zaman iade edilebilir?

Bir işlem iade edilebilir:
- Durumu **Tamamlandı** ise
- Türü **Ödeme** veya **Toplama** ise

Bir iade oluşturmak için **İade** eylemini sipariş detay sayfasından kullanın. Sipariş üzerinden işlenen iadeler, türü **İade** olan yeni bir işlem kaydı oluşturur.

### Onaylama ve toplama akışı

Bazı ödeme yöntemleri (ve bazı ödeme sağlayıcıları) ayrı onaylama ve toplama işlemi destekler. Bu, kargo göndermeden önce ödeme doğrulamak isterseniz faydalıdır:

1. **Onaylama** — Müşterinin kartında para tutulur (durum: `Onaylandı`)
2. **Toplama** — Sipariş kargo gönderildiğinde veya tamamlandığında tetiklenir
3. Onaylama penceresi içinde toplanmazsa, tutar **otomatik olarak sona erer**

İşlemdeki **Son Kullanım Zamanı** alanı, onaylamanın ne zaman sona ereceğini gösterir.

## Ödeme Webhook'ları

Ödeme sağlayıcıları, ödeme durumu değişikliklerini bildirmek için webhook olayları gönderir — örneğin, ödeme başarılı, başarısız veya bir anlaşmazlık başlatıldığında. Spwig tüm gelen webhook'ları kaydeder.

**Ödemeler > Ödeme Webhook'ları** menüsüne giderek günlükleri görüntüleyebilirsiniz.

### Webhook Kayıtları Ne Gösterir


| Alan | Açıklama |
|-------|-------------|
| **Sağlayıcı** | Webhook'u gönderen ödeme sağlayıcısı |
| **Olay Kimliği** | Sağlayıcının benzersiz olay kimliği |
| **Olay Türü** | Olay türü (örneğin, `payment_intent.succeeded`, `charge.refunded`) |
| **İşlenmiş** | Spwig'in bu webhook'a işlem yaptı olup olmadığı |
| **İmza Doğrulandı** | Webhook'un güvenlik imzasının geçerli olup olmadığı |
| **Yük** | Sağlayıcı tarafından gönderilen tam veri |
| **İşleme Sonucu** | Spwig'in bu işleme verdiği yanıt |
| **İşleme Hatası** | İşleme sırasında meydana gelen herhangi bir hata |
| **Alındığı Tarih** | Webhook'un ne zaman alındığı |

### Webhook günlüklerini sorun gidermede kullanma

Ödeme takılı kalmış ya da ödeme sonrası sipariş durumu güncellenmemişse:

1. **Ödemeler > Ödeme Webhook'ları** bölümüne gidin
2. Sağlayıcıya göre filtreleyin ve yeni olayları inceleyin
3. **İşlenmiş** sütununu kontrol edin — işlenmeyen bir webhook, teslimat sorununu gösterebilir
4. **İmza Doğrulandı**'yı kontrol edin — başarısız bir imza, webhook gizli anahtarınızın yanlış yapılandırılmış olabileceğini gösterir
5. **İşleme Hatası**'nı inceleyerek herhangi bir hata mesajını kontrol edin

Çift olaylar otomatik olarak işlenir — `Olay Kimliği` ve sağlayıcı kombinasyonu benzersizdir, bu nedenle aynı webhook iki kez işlenemez.

## Ödeme niyetleri

Ödeme niyeti, müşteri ödeme sürecine başladığında ödeme sürecinin yaşam döngüsünü izler ve sonucu takip eder. Ödeme niyetleri, müşteri ödeme adımına ulaştığında otomatik olarak oluşturulur.

**Ödemeler > Ödeme Niyetleri** bölümüne giderek listeyi görüntüleyin.

### Ödeme niyeti durumları

| Durum | Anlamı |
|--------|---------|
| **Oluşturuldu** | Niyet oluşturuldu, ödeme yöntemi bekleniyor |
| **Ödeme Yöntemi Gerekli** | Müşterinin kart bilgilerini girmesi bekleniyor |
| **Onay Gerekli** | Ödeme bilgileri girildi, onay bekleniyor |
| **Eylem Gerekli** | Müşteri bir eylemi tamamlamalıdır (örneğin, 3D Güvenlik doğrulaması) |
| **İşleniyor** | Ödeme işleniyor |
| **Başarılı** | Ödeme başarıyla tamamlandı |
| **İptal Edildi** | Ödeme terk edildi veya iptal edildi |
| **Başarısız** | Ödeme denemesi başarısız oldu |

### Ödeme niyeti ile sipariş akışı

1. Müşteri ödeme adımına ulaşıyor → Spwig bir **Ödeme Niyeti** ve bir taslak **Sipariş** (ödenmemiş) oluşturur
2. Müşteri ödeme bilgilerini girer ve onaylar
3. Ödeme sağlayıcısı ödemesi işler
4. Başarı durumunda, Sipariş **Ödenmiş** olarak güncellenir ve Ödeme Niyeti **Başarılı** durumuna geçer
5. **Ödeme İşlemi** kaydı oluşturulur ve son ödeme detayları ile birlikte saklanır

Ödeme niyeti, ödeme oturumu, sağlayıcı hesabı ve siparişi birbirine bağlar — müşteri ödeme yolculuğunu tam bir şekilde anlamanıza olanak tanır.

### Ödeme niyetlerini destek için kullanma

Müşteri ödeme yaptı ama siparişi ödenmiş olarak gösterilmiyorsa:

1. Müşterinin siparişini **Siparişler** bölümünde bulun
2. **Ödemeler > Ödeme Niyetleri** bölümüne gidin ve o siparişe bağlı niyetleri arayın
3. Niyet durumunu kontrol edin — eğer **Başarılı** ise, bağlı işlemi inceleyin
4. Eğer niyet **Eylem Gerekli** ise, müşteri 3D Güvenlik doğrulamasını tamamlamadı olabilir
5. Eğer niyet **Başarısız** ise, ödeme reddedilme nedenini açıklayan hata detaylarını inceleyin

## İpuçları

- Günlük olarak başarısız işlemleri inceleyin — başarısızlık desenleri (örneğin, belirli bir ödeme yöntemi veya ülke) yapılandırma sorunu veya dolandırıcılık girişimi gösterebilir.
- Webhook günlükleri ödeme farklılıklarını araştırırken değerlidir.

Eğer bir sipariş ödendi ama onaylanmadıysa, webhook günlüğü genellikle ne yanlış gittiğini belirtecektir.
- Yetkilendirme tutarları otomatik olarak sona erer — eğer yetkilendirme-sonra-çekme kullanıyorsanız, yetkilendirme işleminin, sona erme penceresi kapanmadan önce (çoğu sağlayıcı için genellikle 7 gün) fonları çektiğinden emin olun.
- İşlemler üzerindeki **Sağlayıcı Yanıtı** alanı, ödeme sağlayıcısından alınan ham veriyi içerir.

Bir işlem sorununu çözmek için destek ekibinize yardımcı olmak gerekirse bunu paylaşın.
- Webhook'lar üzerinde imza doğrulama hataları hemen incelenmeli — bu, webhook gizli anahtarının yanlış yapılandırılmış olmasından veya mağazanıza sahte webhook olayları göndermeye çalışan bir girişimden kaynaklanabilir.