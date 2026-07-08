---
title: Webhook Günlükleri
---

Webhook günlükleri, tüm gelen taşıyıcı webhook isteklerinin kalıcı bir denetim kaydı sağlar — istek yöntemi, uç nokta URL'si, başlıklar, yük, işleme durumu (beklemede/işlendi/başarısız), ve yanıt kaydedilir. Her webhook, işleme öncesinde günlüğe kaydedilir, böylece işleme başarısız olduğunda olayların kaybolmaması sağlanır. Günlükler, webhook entegrasyonu sorunlarını gidermeye, taşıyıcı API'sinin güvenilirliğini izlemeye ve müşteri desteği için teslimat zaman çizelgelerini yeniden oluşturmak için kullanılır.

Bu sadece okunabilir admin sayfası, webhook hatalarını gidermeye ve taşıyıcı entegrasyonunun sağlığını doğrulamaya yardımcı olur.

## Webhook Günlüğü Yapısı

Her günlük girdisi şu bilgileri kaydeder:

**İstek Detayları**:
- **Taşıyıcı Anahtarı**: Webhook'u gönderen taşıyıcı (fedex, ups, dhl)
- **Uç Nokta**: Webhook URL yolu (örneğin, `/webhooks/shipping/fedex/`)
- **Yöntem**: HTTP yöntemi (genellikle POST)
- **Başlıklar**: İstek başlıkları (JSON)
- **Yük**: İstek gövdesi (JSON)

**İşleme**:
- **İşleme Durumu**: beklemede, işlendi, başarısız
- **Hata Mesajı**: Durum = başarısız olduğunda hata nedeni
- **Yanıt**: Taşıyıcıya gönderilen HTTP yanıtı
- **Yanıt Durum Kodu**: 200, 400, 500, vb.

**Zaman damgaları**:
- **Alındığı Tarih**: Webhook'un geldiği zaman
- **İşlendiği Tarih**: İşleme tamamlandığında

---

## İşleme Durumu Değerleri

**beklemede**: Webhook alınmış, işleme bekliyor
- Alındıktan hemen sonra normaldir
- Beklemede kalmak, işleme kuyruğunda bir yığılma olduğunu gösterir

**işlendi**: Webhook başarıyla işlendi
- TrackingEvent oluşturuldu
- Müşteri bildirimi gönderildi (uygulanabilirse)
- Taşıyıcıya HTTP 200 yanıtı gönderildi

**başarısız**: Webhook işleme başarısız oldu
- Hata nedenini inceleyin (error_message)
- Ortak nedenler: Geçersiz JSON, bilinmeyen gönderi, tekrar eden olay

---

## Webhook Akışı

**Normal Akış**:
```
1. Taşıyıcı paketi tarar
   ↓
2. Taşıyıcı Spwig webhook uç noktasına POST gönderir
   ↓
3. Spwig WebhookLog oluşturur (durum = beklemede)
   ↓
4. Arka plan işçisi webhook'u işler
   ↓
5. JSON yükünü ayrıştır
   ↓
6. Takip numarasına göre eşleşen Gönderiyi bul
   ↓
7. TrackingEvent oluştur
   ↓
8. WebhookLog'u günceller (durum = işlendi)
   ↓
9. Taşıyıcıya HTTP 200 yanıtı gönderir
```

**Başarısız Senaryolar**:
- **Geçersiz JSON**: Taşıyıcı bozuk veri gönderdi → durum = başarısız, hata = "JSON ayrıştırma hatası"
- **Bilinmeyen Gönderi**: Takip numarası herhangi bir gönderiyle eşleşmiyor → durum = başarısız, hata = "Gönderi bulunamadı"
- **Tekrar**: Olay zaten var → durum = başarısız, hata = "Tekrar eden olay"

---

## Webhook Hatası Giderme

**Adım Adım**:

**1. Durum = Başarısız ile Filtrele**
- Shipping > Webhook Günlükleri'ne gidin
- Filtre: İşleme Durumu = "başarısız"
- Yeni başarısızlıkların gözden geçirilmesi

**2. Hata Mesajını Kontrol Et**
- Günlük girdisine tıklayın
- error_message alanını okuyun
- Ortak hatalar:
  - "Gönderi bulunamadı" → Takip numarası uyuşmazlığı
  - "JSON decode hatası" → Taşıyıcı geçersiz JSON gönderdi
  - "Gerekli alan eksik" → Yük beklenen veriyi eksik

**3. Yükü İnceleyin**
- Ham JSON yükünü görüntüleyin
- Yapısı beklenen formata uyuşuyor mu?
- Eksik alanları kontrol edin (takip_id, event_type, vb.)

**4. Gönderinin Varlığını Doğrula**
- Yükten takip numarasını çıkarın
- Takip numarası için Gönderiler'i ara
- Gönderinin var olduğundan emin olun ve doğru taşıyıcıyı kullanıyor olmalı

**5. Taşıyıcı Yapılandırmasını Kontrol Et**
- Taşıyıcı hesabı etkin olduğundan emin olun
- Webhook uç noktası URL'sinin doğru olduğundan emin olun
- Taşıyıcı API kimlik bilgilerini test edin

**6. İşlemi Yeniden Deneyin** (uygulanabilirse)
- Bazı webhook işleyicileri el ile yeniden deneme desteği sağlar
- Altta yatan sorunu önce çözün
- Başarısız webhook'u yeniden deneyin

---

## Ortak Webhook Sorunları

**Problem 1: "Gönderi bulunamadı"**

**Neden**: Webhook'daki takip numarası herhangi bir gönderiyle eşleşmiyor
- Gönderi oluştururken yazım hatası
- Farklı hesap için webhook
- Webhook alınmadan önce gönderi silindi

**Çözüm**:
- Takip numarasının yazımını kontrol edin
- Gönderinin taşıyıcı eşleşip eşleşmediğini kontrol edin
- Gerekirse gönderiyi yeniden oluşturun

---

**Problem 2: "JSON decode hatası"**

**Neden**: Taşıyıcı bozuk JSON gönderdi
- Nadir, genellikle taşıyıcı API hatası
- Karakter kodlama sorunları

**Çözüm**:
- Ham yük ile taşıyıcı destek ekibine ulaşın
- Başlıkların charset kodlamasını kontrol edin
- Taşıyıcı panosunda webhook uç noktası URL'sini kontrol edin

---

**Problem 3: Tekrar eden webhooks**

**Neden**: Taşıyıcı aynı olayı birden fazla kez gönderiyor
- Yeniden deneme mantığı (taşıyıcı 200 yanıtını alamadı)
- Taşıyıcı hata

**Çözüm**:
- Sistem tekrar edenleri otomatik olarak reddeder (normal davranış)
- response_status_code 200 olduğundan emin olun
- Sürekli olursa taşıyıcı destek ekibine ulaşın

---

**Problem 4: Webhook eksikliği**

**Neden**: Beklenen webhook asla alınmadı
- Taşıyıcı göndermedi (tarama kaçırıldı)
- Taşıyıcı panosunda webhook uç noktası yanlış yapılandırıldı
- Güvenlik duvarı istekleri engelliyor

**Çözüm**:
- Taşıyıcı panosunda webhook yapılandırmasını kontrol edin
- Uç nokta URL'sinin genel ve erişilebilir olduğundan emin olun
- curl/Postman ile uç noktayı test edin
- Sunucu güvenlik duvarı kurallarını kontrol edin

---

## Webhook Uç Noktası Yapılandırması

**Tipik Webhook URL'leri**:
```
FedEx: https://yourdomain.com/webhooks/shipping/fedex/
UPS: https://yourdomain.com/webhooks/shipping/ups/
DHL: https://yourdomain.com/webhooks/shipping/dhl/
```

**Taşıyıcı Panosu Kurulumu**:
1. Taşıyıcı geliştirici portalına girin
2. Webhook ayarlarına gidin
3. Spwig webhook URL'sini girin
4. Abone olunacak olayları seçin (takip güncellemeleri, teslimat, istisnalar)
5. Yapılandırmayı kaydedin
6. Taşıyıcının test araçlarıyla webhook'u test edin

**Güvenlik**:
- Webhook'lar HTTPS gerektirir (HTTP değil)
- Bazı taşıyıcılar istekleri imzalar (imzanın doğrulanması)
- IP adresi beyaz listesi (taşıyıcı statik IP aralıkları sağlıyorsa)

---

## Webhook Sağlığı İzleme

**Ana Metrikler**:

**Başarı Oranı**:
```
Başarı Oranı = (İşlendi / Toplam) × 100%

Hedef: >98%
```

**İşleme Zamanı**:
```
Ortalama Zaman = İşlendiği Tarih - Alındığı Tarih

Hedef: <2 saniye
```

**Başarısızlık Desenleri**:
- Ani başarısızlık artışı → Taşıyıcı API değişikliği veya kesinti
- Sürekli "gönderi bulunamadı" → Takip numarası senkronizasyon sorunu
- Tüm webhooks başarısız → Uç nokta yapılandırma sorunu

**İzleme Stratejisi**:
- Günlük olarak başarısızlık oranını kontrol edin
- Başarısızlık oranı >5% olduğunda uyarı verin
- Haftalık olarak hata mesajlarını inceleyin
- Taşıyıcı durum sayfasına karşılaştırın

---

## Webhook Saklama

**Günlükler kalıcıdır** - asla otomatik olarak silinmez

**Neden Kalıcı**:
- Denetim uygunluğu
- Müşteri desteği (teslimat zaman çizelgesini yeniden oluşturma)
- Dispute çözümü
- Webhook hata ayıklama

**Depolama**: Günlükler etkili bir şekilde saklanır (sıkıştırılmış JSON)

---

## İpuçları

- **Webhook'lar kalıcı bir denetim günlüğüdür** - İşlendikleri halde bile asla silinmeleri
- **Günlük olarak başarısız webhook'ları kontrol edin** - Entegrasyon sorunlarını erken fark edin
- **İşleme gecikmesini izleyin** - Uzun gecikme, performans sorununu gösterir
- **Ham yükleri saklayın** - Taşıyıcı API değişikliklerini ayıklamak için kritik öneme sahiptir
- **Uç nokta yapılandırmasını test edin** - Taşıyıcının test araçlarını kullanarak kurulumu doğrulayın
- **Webhook imzalama özelliğini etkinleştirin** - İsteklerin gerçekten taşıyıcıdan geldiğini doğrulayın
- **Taşıyıcı IP adreslerini beyaz listeye alın** - Taşıyıcı statik IP aralıkları sağlıyorsa
- **Aşırı kullanım uyarılarını ayarlayın** - Başarısızlık oranı eşik değerini aştığında bildirim alın
- **Taşıyıcı durumuyla karşılaştırın** - Webhook eksiklikleri taşıyıcı kesintisini gösterebilir
- **Taşıyıcı yük formatlarını belgeleyin** - Taşıyıcı API güncellemeleri zamanında yardımcı olur
- **Webhook URL'lerini sabit tutun** - URL'leri değiştirmek taşıyıcı panosunda güncelleme gerektirir
