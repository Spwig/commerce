---
title: İzleme Olayları
---

İzleme olayları, teslimat yaşam döngüsü boyunca gönderi durumu kontrol noktalarını kaydeder—her olay, durum (teslimat sırasında, teslim için çıktı, teslim edildi), tarih, konum, açıklama ve orijinal taşıyıcı verilerini içerir. Olaylar, taşıyıcı webhook bildirimleri aracılığıyla otomatik olarak veya satıcılar tarafından elle oluşturulur. Müşteriler, hesaplarında ve sipariş onay e-postalarında izleme olay geçmişini görür, bu da gerçek zamanlı teslimat görünürlüğü sağlar.

Bu yönetici sayfası, denetim ve müşteri desteği amaçlı olarak salt okunur olay geçmişini görüntüler.

## İzleme Olayı Yapısı

Her olay şu bilgileri içerir:

**Durum Bilgisi**:
- **Durum**: in_transit, out_for_delivery, delivered, exception, failed, returned
- **Açıklama**: İnsan tarafından okunabilir durum (örneğin, "Paket sıralama tesisine ulaştı")
- **Taşıyıcı Durum Kodu**: Orijinal taşıyıcı durumu (örneğin, "DEP" için ayrıldı)

**Konum Verisi**:
- **Şehir**: Olay konumu şehri
- **Eyalet**: Olay konumu eyaleti/ilaç
- **Ülke**: Olay konumu ülkesi
- **Posta Kodu**: Olay konumu ZIP/posta kodu

**Zaman Damgaları**:
- **Olay Zamanı**: Olayın gerçekten ne zaman gerçekleştiğini belirtir (taşıyıcı zamanı)
- **Kayıt Zamanı**: Olayın Spwig'de ne zaman kaydedildiğini belirtir (sistem zamanı)

**Meta Veri**:
- **Ham Veri**: Taşıyıcı API'sinden tam JSON yanıtı
- **Gönderi**: Bağlantılı gönderi kimliği

---

## Olay Durumu Türleri

**in_transit**: Paket, taşıyıcı ağı üzerinden hareket ediyor
- Örnekler: "Tesisden ayrıldı", "Hub'a ulaştı", "Bir sonraki tesis için teslimat sırasında"

**out_for_delivery**: Paket, teslimat aracı üzerinde
- Örnekler: "Teslim için çıktı", "Teslimat aracı üzerinde"

**delivered**: Paket başarıyla teslim edildi
- Örnekler: "Ön kapıya teslim edildi", "Resepsiyona bırakıldı", "Alıcıya teslim edildi"

**exception**: Teslimat sorunu, dikkat gerektiren bir durum
- Örnekler: "Hava koşulları gecikmesi", "Yanlış adres", "Teslimat denemesi başarısız"

**failed**: Teslimat kalıcı olarak başarısız oldu
- Örnekler: "Adrese göre teslim edilemez", "Alıcı tarafından reddedildi"

**returned**: Paket göndericiye iade ediliyor
- Örnekler: "Göndericiye iade başlatıldı", "Paket iade ediliyor"

---

## İzleme Olaylarının Oluşturulması

### Otomatik (Taşıyıcı Webhook'ları)

**İş Akışı**:
1. Taşıyıcı paketi tarar (açılış, varış, teslimat)
2. Taşıyıcı, Spwig webhook uç noktasına webhook gönderir
3. Webhook, WebhookLog tablosunda kaydedilir
4. Sistem webhook yükünü analiz eder
5. TrackingEvent, çıkarılan verilerle oluşturulur
6. Müşteri e-posta bildirimi gönderilir (konfigüre edilmişse)

**Avantajlar**:
- Gerçek zamanlı güncellemeler (sorgulamaya gerek yok)
- Taşıyıcıdan gelen doğru zaman damgaları
- Olay geçmişinin otomatik olarak korunması

### Elle (Satıcı Girişi)

**İş Akışı**:
1. Gönderi detayına gidin
2. "İzleme Olayı Ekle"yi tıklayın
3. Açılır listeden durumu seçin
4. Açıklama girin
5. Opsiyonel: Konum verisi girin
6. Olay zamanını ayarlayın
7. Kaydedin

**Kullanım Durumları**:
- Webhook desteği olmayan taşıyıcılar
- Elle gönderi düzeltmeleri
- Yerel teslimat (taşıyıcı dışı)
- İç durum güncellemeleri

---

## Olay Gösterimi Sırası

Olaylar, **ters kronolojik sırayla** (en yeni öncelikli) gösterilir:

**Örnek Gösterim**:
```
13 Şubat 2026 10:30 - Teslim edildi (Brooklyn, NY)
13 Şubat 2026 08:15 - Teslim için çıktı (Brooklyn, NY)
12 Şubat 2026 23:45 - Yerel tesis'e ulaştı (Brooklyn, NY)
12 Şubat 2026 18:30 - Teslimat sırasında (Newark, NJ)
12 Şubat 2026 14:15 - Kaynakta ayrıldı (Philadelphia, PA)
12 Şubat 2026 09:00 - Toplandı (Philadelphia, PA)
```

---

## Müşteri Görünümü

Müşterilere gösterilen izleme olayları:

**Sipariş Onayı E-postası**:
- En son olay durumu
- Tahmini teslim tarihi
- Takip bağlantısı

**Müşteri Hesabı > Sipariş Detayı**:
- Tam olay zaman çizelgesi
- Olay açıklamaları
- Konum geçmişini
- Zaman damgaları

**Takip Sayfası** (etkinse):
- Özel takip URL'si
- Görsel zaman çizelgesi
- Taşıyıcı logolu
- Teslim haritası (konum verisi mevcutsa)

---

## İzleme Olaylarını Filtreleme

**Yararlı Filtreler**:
- **Gönderi**: Belirli bir gönderi için olayları görüntüle
- **Durum**: Olay türüne göre filtrele (teslim edildi, in_transit vb.)
- **Tarih Aralığı**: Belirli bir zaman dilimindeki olaylar
- **Konum**: Belirli bir şehir/eyaletteki olaylar

**Kullanım Durumları**:
- "Bugün teslim edilen tüm gönderileri göster"
- "Geçen hafta tüm istisnaları bul"
- "Mevcut in_transit gönderilerini izle"

---

## Ham Veri (Hata Ayıklama)

**Ham Veri Alanı**:
- Taşıyıcı API'sinden tam yanıtı JSON olarak saklar
- Webhook sorunlarını ayıklamak için kullanışlıdır
- Taşıyıcı özel meta verileri içerir

**Örnek Ham Veri** (FedEx):
```json
{
  "event_type": "OD",
  "event_description": "Out for delivery",
  "timestamp": "2026-02-13T08:15:00Z",
  "location": {
    "city": "Brooklyn",
    "state": "NY",
    "postal_code": "11201",
    "country": "US"
  },
  "delivery_signature": null,
  "estimated_delivery": "2026-02-13T17:00:00Z"
}
```

**Ham Veriyi Ne Zaman Kontrol Etmeli**:
- Olay açıklaması net değilse
- Konum verisi eksikse
- Webhook işleme hataları
- Taşıyıcı destek talebi

---

## Olay Zamanlama

**Olay Zamanı** vs **Kayıt Zamanı**:

**Olay Zamanı**: Taşıyıcı olayının gerçekten ne zaman gerçekleştiğini belirtir
- Örnek: Paket 10:30'da tarandı

**Kayıt Zamanı**: Spwig'ın webhook'ı aldığını belirtir
- Örnek: Webhook 10:32'de alındı (2 dakikalık gecikme)

**Neden Farklı?**:
- Ağ gecikmeleri
- Taşıyıcı toplu işleme
- Webhook tekrar gecikmeleri

**Müşteri Görüntülemesi için Olay Zamanını Kullanın** - Gerçek teslimat ilerlemesini daha doğru yansıtır.

---

## İpuçları

- **Olaylar salt okunur** - Oluştuktan sonra düzenlenemez (denetim bütünlüğü)
- **Detaylar için ham veriyi kontrol edin** - Görüntülenen alanlardan daha fazla bilgi içerir
- **Webhook gecikmelerini izleyin** - Olay_zamanı ve kayıt_zamanı arasındaki büyük gecikme webhook sorunlarını gösterebilir
- **Müşteri desteği için kullanın** - Olay zaman çizelgesi, teslimat sorunlarını tanımlamaya yardımcı olur
- **Teslimat desenlerini izleyin** - Olay zamanlamalarını analiz ederek taşıyıcı performansını değerlendirin
- **Bildirimleri ayarlayın** - Anahtar olaylarda (out_for_delivery, delivered) müşterilere otomatik e-posta gönderin
- **Olayları silmeyin** - Tam denetim izini koruyun
- **WebhookLog'da hataları kontrol edin** - Eksik olaylar, webhook işleme hatalarını gösterebilir
- **Konum verisi taşıyıcıya göre değişebilir** - Bazı taşıyıcılar detaylı konum verileri sağlar, bazıları minimal
- **İstisna olayları dikkat gerektirir** - Teslimat istisnalarını izleyin ve takip edin
