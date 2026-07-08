---
title: E-posta Çıkış Kutusu
---

E-posta Çıkış Kutusu, mağazanızın göndermeye çalıştığı veya gönderdiği tüm e-postaların tam bir kaydını içerir — sipariş onayları, sevkiyat güncellemeleri, yönetici raporları ve tüm diğer işlemle ilgili mesajlar. Onu, teslimatları onaylamak, başarısızlıkları araştırmak ve e-posta kuyruğunu yönetmek için kullanın.

**E-posta Sistemi > E-posta Çıkış Kutusu**'na giderek e-posta kaydını görüntüleyin.

![E-posta Çıkış Kutusu listesi durum etiketleriyle](/static/core/admin/img/help/email-outbox/outbox-list.webp)

## Çıkış kutusunu okuma

Üstteki özeti çubuk, her durum kategorisi için sayıyı gösterir. Aşağıdaki liste, aşağıdaki bilgilerle bireysel e-postaları gösterir:

- **Konu** — e-posta konu satırı
- **A** — alıcının e-posta adresi
- **Gönderen** — kullanılan gönderen adresi
- **Durum** — mevcut teslimat durumu
- **Kuyruğa Alma Zamanı** — e-postanın kuyruğa girdiği zaman
- **Gönderme Zamanı** — e-postanın sağlayıcıya gönderildiği zaman
- **Gönderme Deneme Sayısı** — gönderme denemelerinin sayısı

## E-posta durumları

| Durum | Anlamı |
|--------|---------|
| Kuyrukta | E-posta, gönderilmek üzere kuyrukta bekliyor |
| Gönderiliyor | E-posta şu anda sağlayıcıya gönderiliyor |
| Gönderildi | Sağlayıcı e-postayı kabul etti |
| Beklemede | E-posta duraklatıldı ve serbest bırakılana kadar gönderilmeyecek |
| Kaydedildi | E-posta kaydedildi ancak gönderilmemiştir (test modu veya yalnızca kaydetme ayarı) |
| Başarısız | Sağlayıcı e-postayı reddetti veya gönderememiştir |
| Geri Dönüş | E-posta gönderildi ancak alıcının e-posta sunucusundan geri döndü |
| Atlandı | Gönderme, sistem nedeniyle atlandı |

## E-posta detaylarını görüntüleme

Listedeki herhangi bir e-postayı tıklayarak tam detayları görüntüleyin:

- E-postanın tam **HTML Gövdesi** ve **Metin Gövdesi**
- **Sağlayıcı Mesaj Kimliği** — e-posta sağlayıcınızdan gelen referans (bu, sağlayıcı desteğini kullanırken kullanın)
- **Hata Mesajı** — başarısız veya geri dönen e-postalar için tam hata
- **Gönderme Deneme Sayısı** ve **Maksimum Gönderme Denemeleri** — gönderme denemelerinin sayısı
- Tüm zaman damgaları: oluşturulma, kuyruğa alma, gönderme ve başarısızlık zamanları

## Çıkış kutusunu filtreleme

Görünümünüzü daraltmak için sağdaki filtreleri kullanın:

- **Durum** — belirli bir teslimat durumuna sahip e-postaları göster
- **Tarih** — e-postaların oluşturulma veya gönderme zamanına göre filtrele
- **Şablon Türü** — yalnızca belirli bir bildirim türünden e-postaları göster (örneğin, yalnızca sipariş onayları)

Üstteki arama kutusu, konu, alıcı adresi, gönderen adresi veya sağlayıcı mesaj kimliği üzerinden arama yapar.

## Beklemede olan e-postaları serbest bırakma

**Beklemede** durumunda olan e-postalar duraklatılmıştır — serbest bırakılana kadar gönderilmeyecek. Bir e-posta, mağazanız bakım modunda iken oluşturulduğunda veya bir yönetici eylemiyle bekletildiğinde **Beklemede** durumuna gelebilir.

Beklemede olan e-postaları serbest bırakmak için:
1. Serbest bırakmak istediğiniz e-postaları seçin (soldaki kutuları işaretleyin)
2. **Eylemler** açılır menüsünden **Beklemede olan e-postaları teslimat için serbest bırak**'ı seçin
3. **Git**'e tıklayın

Serbest bırakılan e-postalar **Kuyrukta** durumuna geçer ve bir sonraki kuyruk işleme döngüsünde gönderilecektir.

## Planlanmış e-postalar

Bazı e-postalar, gelecekte belirli bir zamanda gönderilmek üzere planlanmıştır — haftalık özeti raporları gibi, belirli bir gün ve saatte gönderilmek üzere planlanmıştır. **E-posta Sistemi > Planlanmış E-postalar**'a giderek yaklaşan planlanmış göndermeleri görüntüleyin.

Planlanmış e-postalar listesi aşağıdaki bilgileri gösterir:

- **Şablon Türü** — planlanmış e-posta türü
- **Alıcı E-posta** — gönderileceği adres
- **Planlanan Zaman** — gönderileceği tarih ve saat
- **Durum** — Beklemede (henüz gönderilmemiş), Gönderildi veya Başarısız

Planlanmış e-postalar, planlanan zamanı geldiğinde otomatik olarak işlenir — el ile bir eylem gerekmez.

## Başarısız teslimatları giderme

E-postalar **Başarısız** durumunu gösteriyorsa, hata mesajını görmek için tıklayın ve aşağıdaki adımları izleyin:

### Yaygın nedenler ve çözümler

| Symptom | Likely cause | What to do |
|---------|-------------|------------|
| "Authentication failed" | E-posta sağlayıcısının kimlik bilgileri geçersiz | **E-posta Sistemi > E-posta Hesapları**'nda kimlik bilgilerini güncelle |
| "Connection refused" / "Timeout" | E-posta sunucunuz erişilebilir değil | E-posta sağlayıcınızın durum sayfasını kontrol edin; **E-posta Hesapları**'nda bağlantıyı test edin |
| "Invalid recipient" | Müşterinin e-posta adresi hatalı | Müşterinin hesabını inceleyin ve e-postasını düzeltin |
| Geri dönen e-postalar | Alıcının e-posta sunucusu e-postayı reddetti | Adres mevcut olmayabilir veya posta kutusu doludur; aşırı tekrar denemeyin |
| Aniden yüksek başarısızlık oranı | Sağlayıcı sorunu veya kimlik bilgileri sona erdi | Sağlayıcı durumunu kontrol edin; **E-posta Hesapları**'nda bağlantıyı tekrar test edin |

### E-posta hesabınızın bağlantısını kontrol etme

Eğer birçok e-posta başarısız oluyorsa, e-posta hesabınızı test edin:

1. **E-posta Sistemi > E-posta Hesapları**'na gidin
2. Aktif hesabınızı bulun ve **Bağlantı** durumunu kontrol edin
3. Bağlantıda bir hata varsa, hesaba tıklayın ve **Bağlantıyı Test Et** seçeneğini kullanarak sorunu tanılayın

### Tekrar deneme davranışı

Spwig, başarısız e-postaları **Maksimum Tekrar Sayısı** sınırına kadar otomatik olarak tekrar deneyebilir. Her e-posta üzerinde gösterilen tekrar sayısı, kaç deneme yapıldığını gösterir. Tekrar sınırına ulaşıldığında, e-posta **Başarısız** durumunda kalır ve daha fazla otomatik tekrar denemesi yapılmaz.

## Geri dönen e-postalar

**Geri dönen** bir e-posta gönderildi ancak alıcının e-posta sunucusu tarafından döndürüldü. İki tür geri dönen e-posta vardır:

- **Kırmızı geri dönen** — e-posta adresi mevcut değil veya alan adı e-posta almaz. Kırmızı geri dönenleri tekrar denemeyin; adres geçersizdir
- **Yumuşak geri dönen** — geçici bir sorun (posta kutusu dolu, sunucu geçici olarak kullanılamaz). Tekrar deneme ile başarılı olabilir

Aynı adrese yapılan tekrarlayan geri dönenler, e-posta sağlayıcılarıyla gönderici itibarınızı olumsuz etkileyebilir. Aynı müşteri adresine tekrarlayan geri dönenler görüyorsanız, o adresi müşterinin hesabından güncelleyin veya kaldırın.

## İpuçları

- Ani bir satış veya büyük ürün lansmanı gibi büyük olaylardan sonra, tüm sipariş onay e-postalarının başarıyla gönderildiğini doğrulamak için outbox'u inceleyin
- Bir müşteri bir e-posta almadığını söylüyorsa, onun e-posta adresine göre outbox'u araştırın ve e-postanın gönderildiğini, başarısız olduğunu veya atlandığını görün
- Aniden artan başarısızlıklar genellikle bir kimlik bilgisi veya hesap sorununu gösterir — hemen **E-posta Hesapları**'nı kontrol edin
- **Beklemede** durumu bir başarısızlık değildir — sadece e-postanın beklediğini gösterir. E-postaları göndermeye hazırsanız, bekleyen e-postaları serbest bırakın
- **Şablon Türü** filtresini kullanarak bir türdeki tüm e-postaları hızlıca denetleyin — örneğin, son 7 gün içindeki tüm sipariş onaylarının **Gönderildi** durumunda olduğundan emin olun
- Listede en üstte bulunan tarih hiyerarşisi (gün / ay / yıl), belirli bir dönem için outbox'u incelemek için faydalıdır