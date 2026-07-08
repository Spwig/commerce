---
title: Ödeme İşlemi
---

Ödeme işlemini, onaylanan komisyonları ortaklarınıza ödemek için kullanabilirsiniz. Bu kılavuz, PayPal veya banka transferi sağlayıcıları üzerinden ödeme oluşturmayı, yönetmeyi ve işleme nasıl yapacağınızı gösterir.

![Ödeme Listesi](/static/core/admin/img/help/payout-processing/payout-list.webp)

## Ödeme Genel Bakış

Bir ödeme, tek bir ortak için birden fazla onaylanan komisyonu gruplayan bir ödeme partisidir. Tüm gecikmiş kazançlar için bir çek yazmak gibi düşünün.

Ana özellikler:
- **Çoklu komisyonları içerir** — Bir ödeme, onaylanan birkaç komisyonu kapsayabilir
- **Minimum eşik gerektirir** — Çoğu program minimum ödeme tutarları ($50-$100 tipik) gerektirir
- **Sağlayıcılar aracılığıyla işlenir** — PayPal veya Airwallex, gerçek para transferini işler
- **Hayat döngüsü vardır** — Beklemede → İşleniyor → Tamamlandı (veya Başarısız)

## Ödeme Akışı

Tam ödeme süreci altı adımdan oluşur:

1. **Ortak komisyon kazanır** — Satışlar ortak izleme bağlantılarına atfedilir
2. **Satıcı komisyonları onaylar** — Bekleyen komisyonları inceleyin ve onaylayın
3. **Bakiye minimum eşikte** — Ortak onaylanan bakiyesi program eşiklerini karşılar
4. **Ortak ödeme talep eder** — Ortak, dashboard'ında ödeme talebi sunar
5. **Satıcı ödeme işler** — Ödeme oluşturup işleme geçirirsiniz
6. **Ödeme tamamlandı** — Sağlayıcı fonları gönderir, komisyonlar "ödenmiş" olarak işaretlenir

## Ödemeleri Görüntüleme

Ödeme yönetimi dashboard'ına ulaşmak için **Ortaklık Programı > Ödemeler**'e gidin.

İstatistik paneli şu bilgileri gösterir:
- **Beklemede** — Oluşturuldu ancak henüz işlenmedi
- **İşleniyor** — Ödeme sağlayıcısına gönderiliyor
- **Tamamlandı** — Başarıyla ödenmiş
- **Başarısız** — Ödeme başarısız oldu (dikkat gerektirir)

Liste görünümü şu bilgileri gösterir:
- Ortak adı ve kodu
- Ödeme tutarı
- Ödeme yöntemi (PayPal veya Banka Transferi)
- Durum etiketi
- Oluşturma ve tamamlama tarihleri
- Eylem düğmeleri

Filtreleri kullanarak şu kriterlere göre daraltın:
- Ortak
- Ödeme yöntemi
- Durum
- Tarih aralığı

## Ödeme Oluşturma

Yeni bir ödeme oluşturmak için şu adımları izleyin:

1. **Gidin** **Ortaklık Programı > Ödemeler**
2. **Tıklayın** **+ Ödeme Ekle** düğmesi
3. **Ortak seçin** açılır listeden
4. **Onaylanan komisyonları inceleyin** — Sistem, bu ortak için tüm ödenmemiş, onaylanan komisyonları görüntüler
5. **Ödeme yapmak için komisyonları seçin** — Ödeme yapmak istediğiniz komisyonların onay kutularını işaretleyin (genellikle tümü)
6. **Toplam tutarı doğrulayın** — Sistem toplamı otomatik olarak hesaplar
7. **Ödeme yöntemini seçin** — PayPal veya Banka Transferi (ortak tercihine göre)
8. **Sağlayıcı hesabını seçin** — Kullanmak istediğiniz PayPal/Airwallex hesabını seçin
9. **Not ekle** (isteğe bağlı) — Kayıt tutmak için iç notlar
10. **Kaydet** tıklayın — Durumu "Beklemede" olan ödeme oluşturulur

Ödeme artık işleme hazır.

## Ödemeleri İşleme

Ödemeleri işlemek için iki seçenek vardır: el ile veya sağlayıcı tabanlı.

### El ile İşleme

Sistem dışında ödemeleri işlemek (çekler, kredi transferleri vb.) için el ile işleme kullanın:

1. Listede ödeme seçin
2. **İşleme olarak işaretle** eylemini tıklayın
3. Dış yöntemle ödeme tamamlayın
4. Ödemeye geri dönün
5. **Tamamlandı olarak işaretle** eylemini tıklayın
6. Komisyonlar otomatik olarak "Ödenmiş" durumuna güncellenir

El ile işleme esneklik sağlar ancak daha fazla yönetici işi gerektirir.

### Sağlayıcı İşleme (Tavsiye Edilir)

Sağlayıcı işleme, PayPal veya Airwallex üzerinden ödemeleri otomatikleştirir:

1. **Listede ödeme(ler)i seçin** (birden fazla işlem yapabilirsiniz)
2. **Tıklayın** **Sağlayıcı ile İşlem** eylemini
3. **Onaylayın** iletişim kutusunda
4. **Sistem görevi kuyruğa alır** — Celery çalışanı API çağrısını işler
5. **Sağlayıcı ödeme işler**:
   - **PayPal**: Talep başına en fazla 15.000 ödeme toplu işler
   - **Airwallex**: Bireysel banka transferleri
6. **Webhook durumu günceller** — Sağlayıcı tamamlanmasını onaylar
7. **Komisyonlar "ödenmiş" olarak işaretlenir** — Sistem tüm dahil edilen komisyonları günceller

Sağlayıcı işleme daha hızlı, daha güvenilir ve otomatik bir denetim izi oluşturur.

## Ödeme Yöntemleri

Spwig, farklı gereksinimlerle iki ödeme yöntemi destekler:

| Yöntem | Sağlayıcı | Gereksinimler | İşleme Süresi | Ücretler | En Uygun Olduğu Durumlar |
|--------|----------|--------------|-----------------|------|----------|
| **PayPal** | PayPal Ödeme | Ortak, geçerli `payment_email`'e sahip olmalıdır | 1-2 iş günü | ~2% veya ödeme başına $0.25-$1.00 | Çoğu ortak, küresel erişim |
| **Banka Transferi** | Airwallex | Banka hesabı detayları (hesap numarası, yönlendirme, SWIFT) | 2-5 iş günü | Ülkeye göre değişir | Uluslararası ortaklar, büyük tutarlar |

Ortaklar, ödeme yöntemi ve detaylarını kendi dashboard'larında yapılandırır. Sistem, tercihlerine göre uygun sağlayıcıyı otomatik olarak seçer.

### Ödeme Yöntemi Seçim Mantığı

Bir ödeme işleme sırasında Spwig sağlayıcıyı şu şekilde seçer:

1. Ortakın tercih ettiği ödeme yöntemi (PayPal veya Banka Transferi) kontrol edilir
2. Yapılandırılmış sağlayıcı hesabı ile eşleşir (PayPal → PayPal, Banka → Airwallex)
3. Tercih mevcut değilse ilk kullanılabilir sağlayıcıya geri döner
4. Yapılandırılmış sağlayıcı yoksa hata görüntüler

## Ödeme Durumu Akışı

Ödeme durumlarını anlamanız, ödeme ilerlemesini izlemenize yardımcı olur:

| Durum | Anlamı | Sonraki Eylem |
|--------|---------|-------------|
| **Beklemede** | Oluşturuldu ancak sağlayıcıya henüz gönderilmemiş | Sağlayıcı ile işleme veya işleme olarak işaretleyin |
| **İşleniyor** | Ödeme sağlayıcısına gönderildi, onay bekleniyor | Webhook'u bekleyin veya sağlayıcı dashboard'ını kontrol edin |
| **Tamamlandı** | Ödeme başarılı, fonlar gönderildi | Hiçbiri — komisyonlar "ödenmiş" olarak işaretlenir |
| **Başarısız** | Ödeme başarısız oldu (hata detaylarını inceleyin) | Hata inceleyin, sorunu çözün, tekrar deneyin veya iptal edin |
| **İptal Edildi** | Tamamlanmadan önce el ile iptal edildi | Hiçbiri — komisyonlar ödenmemiş kalır |

### Başarı Yolu

Beklemede → İşleniyor → Tamamlandı

Bu, mutlu yoludur. Sağlayıcı webhook'ları ödeme ilerledikçe durumu otomatik olarak günceller.

### Başarısızlık Yolu

Beklemede → İşleniyor → Başarısız

Bir ödeme başarısız olursa, ödeme durumu Başarısız olarak değişir ve sorunu incelemelisiniz.

## Başarısız Ödemeleri İşleme

Başarısız ödemeler el ile müdahale gerektirir. Ortaklar için yaygın başarısızlık nedenleri:

| Neden | Sağlayıcı Hatası | Çözüm |
|-------|----------------|----------|
| Geçersiz hesap | "Alıcı hesabı bulunamadı" | Ortakın ödeme e-postasını veya banka detaylarını doğrulayın |
| Yetersiz bakiye | "Yeterli fon yok" | Sağlayıcı hesabınıza fon ekleyin |
| Banka detayı hatası | "Geçersiz yönlendirme numarası" | Ortakın banka bilgilerini güncellemesini isteyin |
| Hesap kısıtlaması | "Alıcı ödemeler alamaz" | Ortakla iletişime geçin ve hesap durumunu çözün |
| Sağlayıcı sorunu | "Hizmet geçici olarak kullanılamıyor" | Birkaç saat sonra tekrar deneyin |

### Başarısız Ödemeyi Tekrar Deneme

1. **Başarısız ödemeni görüntüleyin** — Listede tıklayın
2. **Hata mesajını okuyun** — Sağlayıcı Yanıtı alanını kontrol edin
3. **Alt sorunu çözün** — Ortak detaylarını güncelleyin, sağlayıcı fonlarını ekleyin vb.
4. **Durumu sıfırlayın** — Durumu tekrar Beklemede olarak değiştirin (düzenleme formu)
5. **Tekrar işleme** — **Sağlayıcı ile İşlem** eylemini kullanın

### İptal Etme ve Yeniden Oluşturma

Tekrar deneme başarısız olursa:

1. **Başarısız ödemeni açın**
2. **Durumu İptal Edildi olarak değiştirin**
3. **Ödeme kaydedin**
4. **Yeni ödeme oluşturun** — Oluşturma adımlarını tekrarlayın
5. **Yeni ödemeni işleme**

İptal edilen ödemeler komisyonları ödenmiş olarak işaretlemez, bu yüzden yeni ödemeler için uygun kalırlar.

## Ödeme Sağlayıcı Entegrasyonu

Ödemeleri işlemek için yapılandırılmış bir ödeme sağlayıcı hesabı gerekir. Spwig şu entegrasyonları destekler:

- **PayPal Ödeme API'si** — PayPal ödemeleri için
- **Airwallex** — Uluslararası banka transferleri için

### Kurulum Gereksinimleri

Ödemeleri işlemeye başlamadan önce:
1. En az bir sağlayıcıyı **Ayarlamalar > Ödeme Sağlayıcıları**'nda yapılandırın
2. API kimlik bilgilerini ekleyin (Müşteri Kimliği, Gizli, API Anahtarı)
3. Üretim moduna ayarlayın (test için sandbox)
4. Sağlayıcı dashboard'ında webhook URL'sini yapılandırın
5. Test ödemesi ile bağlantıları doğrulayın

Ayrıntılı yapılandırma talimatları için [Ödeme Sağlayıcı Kurulumu](#) kılavuzunu inceleyin.

### Ortak Tarafından Sağlayıcı Seçimi

Ortaklar, kendi dashboard'larında tercih ettikleri ödeme yöntemini seçer:
- PayPal: `payment_email` girin
- Banka Transferi: Banka hesabı detaylarını girin

Sistem, ödemeleri eşleşen sağlayıcıya yönlendirir.

## Ödeme Programı En İyi Uygulamaları

Ortaklarla güven oluşturmak için düzenli ödeme programı oluşturun:

| Program | Sıklık | İş Yükü | Ortak Memnuniyeti | Önerilen Kullanım |
|----------|-----------|----------|------------------------|-----------------|
| Haftalık | Her Cuma | Yüksek | Mükemmel | Yeni programlar, yüksek hacimli |
| İki haftada bir | 1. ve 15. | Orta | İyi | Orta hacimli programlar |
| Aylık | Ayın 1. günü | Düşük | Kabul edilebilir | Kurumlaşmış programlar |
| Üç ayda bir | Her 3 ayda bir | Çok düşük | Kötü | Önerilmez |

Program boyutunuz ve yönetici kapasiteniz dikkate alınarak bir program seçin.

## İşleme En İyi Uygulamaları

Ödeme işlemleri için şu kılavuzları takip edin:

- **Tarihlerine göre ödeme toplu işlemi yapın** — Her hafta/ay aynı günde tüm uygun ödemeleri işleme geçirin
- **İşlemeden önce detayları doğrulayın** — Büyük tutarlar için özellikle ortak ödeme bilgilerini kontrol edin
- **Sağlayıcı bakiyenizi izleyin** — PayPal/Airwallex hesabınızda yeterli fon olduğundan emin olun
- **Açık minimum eşikler belirleyin** — Program koşullarında ödeme minimumlarını belirtin ($50-$100 tipik)
- **Programınızda ödeme programınızı belgeleyin** — Ortak koşullarına ve portal ayarlarına ödeme programınızı ekleyin
- **Sağlayıcı işleme kullanın** — Mümkünse el ile işleme kullanmayın
- **Başarısız ödemeleri hemen inceleyin** — 24 saat içinde başarısızlıkları çözün
- **Webhook'ları yapılandırın** — Webhook'lar otomatik durum güncellemelerini sağlar
- **Aylık ödeme raporlarını düzenli olarak dışa aktarın** — Muhasebe için aylık raporları indirin

## Ödeme Kayıtları ve Raporlama

Her ödeme, aşağıdaki bilgilerle değiştirilemez bir kayıt oluşturur:
- Ortak bilgileri
- Dahil edilen komisyon kimlikleri
- Toplam tutar
- Ödeme yöntemi ve sağlayıcı
- Oluşturma ve tamamlama zaman damgaları
- Sağlayıcı işlem kimliği (işlem sonrası)
- Sağlayıcı yanıt verisi (hata ayıklama için)
- İç notlar

Herhangi bir ödemenin listesinde tıklanarak bu verilere erişebilirsiniz. Muhasebe veya vergi amaçlı ödeme raporlarını indirmek için yönetici arayüzü dışa aktarma özelliğini kullanın.

## İpuçları

- Ödemeleri sabit bir programda işleme (örneğin, her Cuma öğleden sonra 2'de) yapın, böylece ortaklar ödeme zamanını bilir.
- Her zaman sağlayıcı işleme kullanın, el ile işleme yerine — daha hızlı, daha güvenilir ve daha iyi denetim izi oluşturur.
- Programlarda minimum ödeme eşiklerini ayarlayarak yönetici iş yükünü azaltın — $50 veya $100 tipik minimumlardır.
- Büyük toplu işlemler işlemeye başlamadan önce sağlayıcı hesabınızda bakiyeyi izleyin, başarısızlıkları önleyin.
- Gerçek ödeme işlemlerine geçmeden önce sandbox modunda ödeme entegrasyonunu test edin.
- Her ödeme için bir not ekleyin, hangi dönem kapsadığını açıklayın (örneğin, "2026 Ocak komisyonları").
- Başarısız ödemeleri hemen inceleyin — gecikmeler ortakları kızdırır ve güveni zarar verir.
- Gecikmeleri önceden bildirin — program zamanında ödeme yapamazsanız, etkilenen ortaklara önceden haber verin.

