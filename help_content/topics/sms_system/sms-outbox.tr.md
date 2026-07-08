---
title: SMS Çıkış Kutusu
---

SMS Çıkış Kutusu, mağazanızın göndermeye çalıştığı her metin mesajının tamamını kaydeder. Bu, bildirimlerin müşterilere ulaşıp ulaşmadığını doğrulamak, teslimat hatalarını araştırmak ve genel mesajlaşma aktivitenizi anlamak için kullanılır.

**SMS Sistemi > SMS Çıkış Kutusu**'na giderek mesaj günlüğünü görüntüleyin.

![SMS Çıkış Kutusu listesi durum pankartlarıyla](/static/core/admin/img/help/sms-outbox/outbox-list.webp)

## Çıkış kutusunu okuma

Çıkış kutusundaki her satır, bir mesaj girişimini temsil eder ve şunları gösterir:

- **Telefon** — alıcının telefon numarası
- **Mesaj Türü** — SMS veya WhatsApp
- **Durum** — geçerli teslimat durumu (aşağıya bakın)
- **Oluşturulma Tarihi** — mesajın oluşturulma zamanı
- **Gönderme Zamanı** — mesajın sağlayıcıya gönderildiği zaman

Üstteki özeti çubuk, en önemli durumlar için hızlıca toplam sayıları gösterir.

## Mesaj durumları

| Durum | Anlamı |
|--------|---------|
| Beklemede | Mesaj, gönderme kuyruğu tarafından alınmaya hazırlanıyor |
| Kuyruğa Alındı | Mesaj kuyruğa alındı ve kısa sürede gönderilecek |
| Gönderildi | Sağlayıcı, mesajın teslimatı için kabul etti |
| Teslim Edildi | Sağlayıcı, mesajın alıcının cihazına ulaştığını onayladı |
| Başarısız Oldu | Sağlayıcı mesajı reddetti veya teslim edemedi |
| Atlandı | Gönderme işlemi amaçlı olarak atlandı (aşağıdaki atlama nedenlerine bakın) |
| Test Modunda Kaydedildi | Mesaj yalnızca kaydedildi (mağaza test/sandbox modunda) |

> **Gönderildi vs. Teslim Edildi:** **Gönderildi** durumu, mesajın mağazanızdan çıktı ve sağlayıcı tarafından kabul edildiğini gösterir. **Teslim Edildi** durumu, sağlayıcının taşıyıcıdan bir teslimat onayı aldığını gösterir. Tüm sağlayıcılar teslimat onaylarını desteklemez — sağlayıcınız bunu desteklemiyorsa, mesajlar **Gönderildi** olarak görünür ancak asla **Teslim Edildi** durumuna geçmez, bu normaldir.

## Mesaj detaylarını görüntüleme

Çıkış kutusundaki herhangi bir satırı tıklayarak o mesajın tam detaylarını görüntüleyin:

- Gönderilen tam **Mesaj** metni
- **Sağlayıcı Mesaj Kimliği** — SMS sağlayıcısından gelen referans numarası (sağlayıcı desteğini ararken yararlıdır)
- **Hata Mesajı** (başarısız mesajlar için) — sağlayıcı tarafından döndürülen tam hata
- **Gönderme Sayısı** — Spwig'in mesajı göndermeye çalıştığı kez sayısı
- Tüm zaman damgaları (oluşturuldu, kuyruğa alındı, gönderildi, teslim edildi)

## Çıkış kutusunu filtreleme

Listeyi daraltmak için sağ taraftaki filtreleri kullanın:

- **Durum** — belirli bir duruma sahip mesajları göster
- **Mesaj Türü** — yalnızca SMS veya yalnızca WhatsApp mesajlarını göster
- **Tarih** — mesajın oluşturulduğu günde filtrele

Üstteki arama kutusu, telefon numarasına, mesaj içeriğine veya sağlayıcı mesaj kimliğine göre arama yapmanıza olanak tanır.

## Atlama nedenlerini anlama

Atlanan mesajlar, Spwig'in göndermenin uygun olmadığını veya gerekli olmadığını belirlediği için gönderilmemiştir. Ortak atlama nedenleri:

| Atlama Nedeni | Ne anlama gelir |
|-------------|---------------|
| `user_preference_disabled` | Müşteri, hesap ayarlarında SMS bildirimlerini kapatmıştır |
| `unsubscribed` | Müşteri, SMS mesajlarından abonelikten çıkmıştır |
| `no_provider` | Etkin bir varsayılan SMS sağlayıcı hesabı yapılandırılmadı |
| `template_inactive` | Bu bildirim türü için şablon etkin değil |

Atlanan bir mesaj, bir hata değildir — sistem, amaçlandığı gibi çalıştığını gösterir. Ancak `no_provider` atlamalarının yüksek bir sayısı, bir SMS sağlayıcı hesabı yapılandırılıp etkinleştirilmesi gerektiğini gösterir.

## Başarısız teslimatları giderme

Mesajlar **Başarısız** durumu gösteriyorsa, aşağıdaki adımları izleyin:

1. Başarısız mesajı tıklayarak **Hata Mesajını** görüntüleyin
2. Ortak hata nedenleri:


   | Hata | Muhtemel neden |
   |-------|-------------|
   | Geçersiz telefon numarası | Müşterinin telefon numarası eksik veya E.164 formatında değil |
   | Kimlik doğrulama başarısız | Sağlayıcınızın kimlik bilgileri geçersiz veya zaman aşımına uğramış — bunları **SMS Sağlayıcı Hesapları**'nda güncelleyin |
   | Hesap askıya alındı | Sağlayıcınızın hesabı askıya alınmış — sağlayıcının dashboard'ına girin |
   | Yeterli bakiye yok | Sağlayıcınızın hesabındaki bakiye çok düşük — bakiyeyi artırın |
   | Taşıyıcı reddi | Hedef taşıyıcı mesajı engelledi (genellikle içerik filtrelemeye bağlı olarak) |

3. Temel sorun düzeltilirse, gelecekteki mesajlar normal şekilde gönderilecektir — outbox sadece okunabilir bir log ve bireysel mesajlar manuel olarak yeniden gönderilemez

## Outbox sadece okunabilir

SMS Outbox, sadece bir kayıttır. Outbox'a manuel olarak mesaj ekleyemezsiniz ve buradan bireysel mesajları yeniden gönderemezsiniz. Mesajlar, ilgili olaylar gerçekleştiğinde (örneğin, bir sipariş verildiğinde) Spwig tarafından otomatik olarak gönderilir.

## İpuçları

- Meşgul bir dönemden sonra outbox'u inceleyerek tüm sipariş onay mesajlarının başarıyla teslim edildiğini doğrulayın
- Bir müşteri SMS almadığını söylüyorsa, telefon numarasına göre outbox'u araştırın ve mesajın gönderildiğini, başarısız oldığını veya atlandığını görün
- **Başarısız** mesajlarının ani bir artış genellikle sağlayıcı kimlik bilgilerinizin veya hesap bakiyenizin bir sorununu gösterir — bunları hemen kontrol edin
- Eğer birçok **Atlandı** mesajı varsa ve nedeni `no_provider` ise, **SMS Sistemi > SMS Sağlayıcı Hesapları**'na gidin ve etkin bir varsayılan hesap yapılandırıldığından emin olun
- Listeyin en üstündeki tarih hiyerarşisi, geçmiş mesajları incelemek için hızlıca gün, ay veya yıl bazında navigasyon sağlar