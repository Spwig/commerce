---
title: Ödeme Sağlayıcısı Kurulumu
---

Ödeme sağlayıcısı kurulumu, otomatik komisyon ödemeleri için PayPal ve Airwallex'i yapılandırmayı sağlar. Bu kılavuz, ödeme sağlayıcısı hesaplarını bağlamak, webhooks'ı yapılandırmak ve entegrasyonunuzu test etmek için nasıl yapılması gerektiğini size gösterir.

## Desteklenen Ödeme Sağlayıcıları

Spwig, komisyon ödemelerini otomatikleştirmek için iki ödeme sağlayıcısı ile entegre olur:

| Sağlayıcı | Ödeme Yöntemi | İşlem | Toplu Desteğe | En Uygun | 
|----------|----------------|------------|---------------|----------|
| **PayPal** | PayPal hesap transferleri | API tabanlı | Evet (15.000'e kadar) | Çoğu komisyon sağlayıcısı, küresel erişim | 
| **Airwallex** | Uluslararası banka transferleri | API tabanlı | Hayır (bireysel) | Banka transferleri, uluslararası ödemeler | 

### Ana Farklar

**PayPal Ödemeleri**:
- Komisyon sağlayıcısının PayPal hesabı (ödeme e-postası) gereklidir
- 15.000'e kadar ödeme topluluğunu aynı anda işler
- Daha hızlı işlem (1-2 iş günü)
- Daha düşük kurulum karmaşıklığı
- Ücretler: ~2% veya ödeme başına $0.25-$1.00
- Tüm topluluk için tek bir webhook

**Airwallex**:
- Direkt banka transferlerini destekler
- Bireysel ödemeleri tek tek işler
- Daha uzun işlem (2-5 iş günü)
- Birden fazla döviz ve ülke destekler
- Ücretler, hedef ülke tarafından değişir
- Her ödeme için bireysel webhook

Her iki sağlayıcıyı da yapılandırabilir ve komisyon sağlayıcılarının tercih ettikleri ödeme yöntemini seçmelerine izin verebilirsiniz.

## Ödeme Sağlayıcılarını Neden Kullanmalısınız?

Ödeme sağlayıcılarını entegre etmek, manuel ödemelerden önemli avantajlar sunar:

- **Otomatik işleme** — Manuel veri girişi veya ödeme yürütmesi gerekmez
- **Toplu verimlilik** — Bir tıklamayla onlarca veya yüzlerce ödeme işleme
- **Webhook onayları** — Ödemeler tamamlandığında otomatik durum güncellemeleri
- **Hata azaltma** — Sistem, işlemden önce hesap bilgilerini doğrular
- **Denetim izi** — İşlemler ve sağlayıcı yanıtları için tam kayıt
- **Daha hızlı ödemeler** — Komisyon sağlayıcıları daha hızlı para alır
- **Ölçeklenebilirlik** — Büyüyen komisyon programlarını, yönetici işinin orantılı olarak artmadan yönetin

Sağlayıcı entegrasyonu olmadan, her ödeme için bankanız veya PayPal paneline manuel olarak işlem yapmanız gerekir, ardından Spwig'e dönmelisiniz ve ödemeleri tamamlanmış olarak işaretlemelisiniz.

## PayPal Kurulumu

Otomatik komisyon ödemeleri için PayPal Ödemelerini yapılandırmak için aşağıdaki adımları izleyin.

### Önkoşullar

Başlamadan önce ihtiyacınız olanlar:
- PayPal Business hesabı (Kişisel hesaplar Payouts API'sini kullanamaz)
- PayPal Geliştirici Paneli'ne erişim
- Payouts API için üretim onayı (sandbox testi sonrası)

### Adım 1: PayPal Uygulaması Oluşturun

1. **Git** [PayPal Geliştirici Paneli](https://developer.paypal.com/dashboard/)
2. **PayPal Business hesabıyla oturum açın**
3. **Sol menüdeki** **My Apps & Credentials**'e tıklayın
4. **Live** sekmesini seçin (veya Sandbox test için)
5. **Create App**'a tıklayın
6. **Uygulama adı girin** (örneğin, "Spwig Komisyon Ödemeleri")
7. **Uygulama türü**: Satıcı
8. **Create App**'a tıklayın

PayPal, kimlik bilgilerinizi oluşturur.

### Adım 2: API Kimlik Bilgilerini Alın

Uygulama oluşturduktan sonra:

1. **Client ID kopyalayın** — Uzun alfasayısal dize
2. **Secret altında** **Show**'a tıklayın
3. **Client Secret kopyalayın** — Bu bilgi gizli tutulmalıdır
4. **Modu not alın** — Sandbox veya Live

### Adım 3: Ödeme Özelliğini Etkinleştirin

PayPal uygulamaları, Ödeme özelliğini kullanmak için açık rızayı gerektirir:

1. **Uygulamanızda** **Features** bölümüne kaydırın
2. **Ödeme** özelliğini bulun
3. **Ekle**'ye tıklayın, eğer zaten etkin değilse
4. **Onay için gönderin** eğer Live modda kullanıyorsanız (onay 1-2 iş günü sürer)

### Adım 4: Spwig'de Sağlayıcıyı Ekleyin

Şimdi PayPal hesabını Spwig'e ekleyin:

1. **Git** **Ayarlar > Ödeme Sağlayıcıları**
2. **+ PayPal Hesabı Ekle**'ye tıklayın
3. **Formu doldurun**:
   - **Hesap Adı**: Açıklamalı etiket (örneğin, "Ana PayPal Hesabı")
   - **Client ID**: PayPal Geliştirici Panelinden kopyalayın
   - **Client Secret**: PayPal Geliştirici Panelinden kopyalayın
   - **Mod**: Test için Sandbox veya üretim için Production seçin
   - **Aktif mi?**: Aktif yapmak için işaretleyin
4. **Kaydet**'e tıklayın

Spwig, bir erişim jetonu isteyerek kimlik bilgilerini doğrular. Doğrulama başarısız olursa, Client ID ve Secret'ınızı tekrar kontrol edin.

### Adım 5: Bağlantıyı Test Edin

PayPal entegrasyonunuzu doğrulayın:

1. **Komisyon Programı > Ödemeler** içinde test ödemesi oluşturun
2. **Kendi PayPal e-postanızı** alıcı olarak kullanın
3. **Miktarı** $0.01 olarak ayarlayın (üretimde) veya herhangi bir miktar (sandboxta)
4. **Sağlayıcı ile işleme alın**
5. **PayPal hesabınıza gelen ödemeyi kontrol edin**
6. **Webhook güncellemesini doğrulayın** ödemenin durumunu Spwig'de

Eğer Sandbox modda kullanıyorsanız, test ödemesi almak için [PayPal Sandbox](https://developer.paypal.com/dashboard/accounts) adresinden test PayPal hesabı oluşturun.

## Airwallex Kurulumu

Airwallex, doğrudan yatırımlar tercih eden komisyon sağlayıcıları için uluslararası banka transferlerini destekler.

### Önkoşullar

Başlamadan önce ihtiyacınız olanlar:
- Airwallex hesabı (https://www.airwallex.com adresinden oluşturun)
- Doğrulanmış iş hesabı durumu
- API erişimi etkin (gerekiyorsa Airwallex destek ile iletişime geçin)
- Airwallex hesabınızda yeterli bakiye

### Adım 1: API Kimlik Bilgilerini Oluşturun

1. **https://www.airwallex.com/app/ adresine oturum açın**
2. **Ayarlar > API Anahtarları**'na gidin
3. **API Anahtar Oluştur**'a tıklayın
4. **Açıklama girin**: "Spwig Komisyon Ödemeleri"
5. **İzinleri seçin**: **Ödeme** (okuma ve yazma) etkinleştirin
6. **Oluştur**'a tıklayın
7. **API Anahtarını kopyalayın** — Sadece bir kez gösterilir
8. **Client ID'yi kopyalayın** — Anahtarla birlikte gösterilir

### Adım 2: Ortamınızı Not alın

Airwallex, iki ortam sağlar:

- **Demo**: Sahte işlemlerle test için
- **Üretim**: Gerçek para transferleri için

Hangi ortamın API anahtarınızın ait olduğunu bildiğinizden emin olun.

### Adım 3: Spwig'de Sağlayıcıyı Ekleyin

Airwallex hesabını Spwig'e ekleyin:

1. **Git** **Ayarlar > Ödeme Sağlayıcıları**
2. **+ Airwallex Hesabı Ekle**'ye tıklayın
3. **Formu doldurun**:
   - **Hesap Adı**: Açıklamalı etiket (örneğin, "Airwallex EUR Hesabı")
   - **API Anahtarı**: Airwallex panelinden kopyalayın
   - **Client ID**: Airwallex panelinden kopyalayın
   - **Ortam**: Demo veya Üretim seçin
   - **Aktif mi?**: Aktif yapmak için işaretleyin
4. **Kaydet**'e tıklayın

Spwig, hesap bakiyenizi sorgulayarak kimlik bilgilerini doğrular.

### Adım 4: Desteklenen Ülkeleri Doğrulayın

Airwallex, birçok ülkeye transfer destekler ancak hepsine değil. Desteklenen ülkelerin listesini doğrulamak için [Airwallex coverage](https://www.airwallex.com/global-business-account/global-transfers) sayfasını kontrol edin.

Desteklenen yaygın ülkeler:
- ABD
- Birleşik Krallık
- Avrupa Birliği ülkeleri
- Avustralya
- Kanada
- Singapur
- Hong Kong

### Adım 5: Banka Transferini Test Edin

Airwallex entegrasyonunuzu test edin:

1. Banka bilgileri olan bir komisyon sağlayıcısı için test ödemesi oluşturun
2. Üretim modunda küçük bir miktar ($1-$5) kullanın
3. **Sağlayıcı ile işleme alın**
4. **Airwallex panelinde işlemi kontrol edin**
5. **Webhook onayı bekleyin**
6. **Ödemenin Spwig'de tamamlandığını doğrulayın**

Demo modu anında işler. Üretim modu 2-5 iş günü alır.

## Sağlayıcı Seçim Mantığı

Bir ödeme işlendiğinde, Spwig, komisyon sağlayıcısının ödeme yöntemi temel alınarak uygun sağlayıcıyı otomatik olarak seçer.

### Seçim Akışı

1. **Komisyon sağlayıcısının ödeme yöntemini kontrol edin**:
   - Eğer `payment_email` ayarlanmışsa → Komisyon sağlayıcısı PayPal'ı tercih eder
   - Eğer banka bilgileri ayarlanmışsa → Komisyon sağlayıcısı Banka Transferini tercih eder
2. **Sağlayıcıya eşleştirin**:
   - PayPal e-postası → Aktif PayPal sağlayıcı hesabı kullanın
   - Banka bilgileri → Aktif Airwallex sağlayıcı hesabı kullanın
3. **Tercih edilen sağlayıcı yapılandırılmamışsa** ilk kullanıma geçin
4. **Eşleşen sağlayıcı yoksa** hata gösterin

### Aynı Sağlayıcı İçin Birden Fazla Hesap

Aynı sağlayıcı için birden fazla hesap yapılandırabilirsiniz (örneğin, farklı bölgeler için iki PayPal hesabı). Spwig, ödeme yöntemiyle eşleşen ilk aktif hesabı seçer. Hangi hesabın kullanılacağına kontrol etmek için yönetici listesinde sıralamayı değiştirin veya sadece bir tanesini aktif yapın.

## Ödeme Entegrasyonunu Test Etme

Gerçek komisyon ödemeleri için entegrasyonu test etmeden önce her zaman sağlayıcıyı test edin.

### Sandbox/Demo Modu Testi

1. **Sağlayıcıyı sandbox moduna ayarlayın** (PayPal Sandbox veya Airwallex Demo)
2. **Test komisyon sağlayıcısı** ile test ödeme bilgileri oluşturun
3. **Test komisyonları** oluşturun ve onaylayın
4. **Test ödemesi** oluşturun, bu komisyonları içeren
5. **Sağlayıcı ile işleme alın** menüden
6. **Celery günlüklerini izleyin** API istekleri için
7. **Sağlayıcı panelini kontrol edin** işlem için
8. **Webhook'ı bekleyin** ödemenin durumunu güncellemek için
9. **Komisyonların ödenmiş olarak işaretlendiğini doğrulayın**

### Üretim Testi

Üretimde olmaya başlamadan önce:

1. **Sağlayıcı ayarlarında üretim moduna geçin**
2. **Kendinize küçük bir test ödemesi oluşturun** ($0.01-$1.00)
3. **İşlem yapın** ve tamamlanmasını bekleyin
4. **Kendi hesabınıza gelen parayı doğrulayın**
5. **Webhook'un ateşlendiğini** ve durumun güncellendiğini kontrol edin
6. **Sağlayıcı işlem ücretlerini gözden geçirin**

### Ortak Test Sorunları

| Sorun | Neden | Çözüm |
|-------|-------|----------|
| "Geçersiz kimlik bilgileri" | Yanlış API anahtarı veya mod eşleşmeme | Kimlik bilgilerini tekrar kontrol edin, sandbox ile üretim arasında eşleşmeyi doğrulayın |
| Webhook asla ateşlenmez | Sağlayıcıda URL yapılandırılmadı | Sağlayıcı panelinde webhook URL'sini ekleyin |
| Ödeme "İşlemde" kalır | Webhook imzası başarısız oldu | Webhook gizli anahtarının eşleştiğini kontrol edin |
| Sağlayıcı bulunamadı | Ödeme yöntemi için aktif bir sağlayıcı yok | En az bir sağlayıcı hesabını etkinleştirin |

## Toplu İşleme (PayPal)

PayPal, verimlilik ve maliyet tasarrufu için toplu işleme destekler.

### Toplu İşleme Nasıl Çalışır

Birden fazla ödeme seçip **Sağlayıcı ile İşlem**'e tıkladığınızda:

1. Spwig, tüm PayPal ödemelerini tek bir toplu olarak gruplar
2. Sistem, tüm ödeme detaylarını içeren tek bir API isteği gönderir (15.000'e kadar)
3. PayPal, tüm topluyu tek bir işlem olarak işler
4. Webhook, toplu sonuçlarla birlikte döner
5. Spwig, toplu yanıtına göre tüm ödemeleri günceller

### Toplu İşleme Avantajları

- **Daha az API çağrıları** — Yüzlerce ödeme için tek bir istek
- **Daha düşük ücretler** — Bazı PayPal ücret yapıları toplu işleme tercih eder
- **Daha hızlı işleme** — Tüm toplu için paralel yürütme
- **Tek webhook** — İzleme ve günlük kaydı daha kolay

### Toplu Sınırlamalar

PayPal, şu sınırlamaları uygular:
- Toplu başına maksimum 15.000 alıcı
- Toplu başına maksimum $100.000 toplam
- İşleme genellikle dakikalar içinde tamamlanır

15.000'den fazla ödeme yaparsanız, Spwig otomatik olarak birden fazla toplu haline ayırır.

## Bireysel İşleme (Airwallex)

Airwallex, ödemeleri tek tek işler, bu farklı avantajlar ve dezavantajlar sunar.

### Bireysel İşleme Nasıl Çalışır

Airwallex ödemeleri işlerken:

1. Sistem, her ödeme için ayrı bir API isteği gönderir
2. Airwallex, transferleri ayrı ayrı kuyruğa alır
3. Her transfer, bağımsız olarak tamamlanır (2-5 gün)
4. Her transfer tamamlandığında bireysel webhook ateşlenir
5. Spwig, webhook'lar gelirken ödemeleri günceller

### Bireysel İşleme Avantajları

- **Daha iyi hata izolasyonu** — Bir hata diğerlerini engellemez
- **Ödeme başına izleme** — Bireysel işlem kimlikleri
- **Daha fazla ödeme bilgisi** — Her transfer için banka özel bilgileri
- **Esnek zamanlama** — Transferler farklı hızlarda tamamlanır

### İşleme Süresi

PayPal'in anlık toplu işleme aksine, Airwallex transferleri daha uzun sürer:
- Ulusal transferler: 1-2 iş günü
- Uluslararası transferler: 3-5 iş günü
- Bazı ülkeler: 7 iş günü kadar

Program koşullarınızda komisyon sağlayıcılarının bu süreye göre beklentilerini ayarlayın.

## Webhook Yapılandırması

Webhook'lar, sağlayıcılar işlemleri tamamladığında otomatik ödeme durumu güncellemelerini sağlar.

### Webhook URL Biçimi

Sağlayıcı panelinde bu URL'yi yapılandırın:

```
https://yourdomain.com/api/payout-providers/{provider}/webhook/
```

{provider} şu şekilde değiştirin:
- `paypal` PayPal webhook'ları için
- `airwallex` Airwallex webhook'ları için

Örnekler:
- `https://shop.example.com/api/payout-providers/paypal/webhook/`
- `https://shop.example.com/api/payout-providers/airwallex/webhook/`

### PayPal Webhook Kurulumu

1. **Git** [PayPal Geliştirici Paneli](https://developer.paypal.com/dashboard/)
2. **Uygulama adınızı tıklayın**
3. **Webhooks** bölümüne kaydırın
4. **Webhook Ekle**'ye tıklayın
5. **Webhook URL'sini girin** (yukarıdaki biçim)
6. **Olayları seçin**:
   - `PAYMENT.PAYOUTSBATCH.SUCCESS`
   - `PAYMENT.PAYOUTSBATCH.DENIED`
   - `PAYMENT.PAYOUTS-ITEM.SUCCEEDED`
   - `PAYMENT.PAYOUTS-ITEM.FAILED`
7. **Kaydet**'e tıklayın

PayPal, bir webhook imza anahtarı sağlar. Spwig, bunu webhook doğruluğu için kullanır.

### Airwallex Webhook Kurulumu

1. **Git** [Airwallex Paneli](https://www.airwallex.com/app/)
2. **Ayarlar > Webhook'lar**'a gidin
3. **Webhook Oluştur**'a tıklayın
4. **Webhook URL'sini girin** (yukarıdaki biçim)
5. **Olayları seçin**:
   - `transfer.created`
   - `transfer.completed`
   - `transfer.failed`
6. **Oluştur**'a tıklayın

Airwallex, webhook'ları API gizli anahtarı ile imzalar.

### Webhook Güvenliği

Webhook'lar şu mekanizmalarla doğrulanır:

- **İmza doğrulama** — Sağlayıcı, webhook yükünü gizli anahtarla imzalar
- **Zaman damgası kontrolü** — Eski webhook'ları reddeder (tekrar saldırılarını önler)
- **IP adresi listesi (isteğe bağlı)** — Sağlayıcı IP aralıklarına sınırlı olur
- **HTTPS gerekli** — Webhook'lar sadece SSL üzerinden çalışır

Üretimde imza doğrulamasını asla devre dışı bırakmayın.

### Webhook'ları Test Etme

Çoğu sağlayıcı, webhook test araçları sunar:

**PayPal**: Geliştirici Panelindeki "Simülatör"i kullanarak test webhook'ları ateşleyin

**Airwallex**: Demo modunda test transferi oluşturun ve webhook'ı izleyin

Spwig'de webhook günlüklerini **Ayarlar > Sistem Günlükleri**'nde kontrol edebilirsiniz (günlük etkinse).

## Sorun Giderme

### Geçersiz Kimlik Bilgileri Hatası

**Belirti**: Sağlayıcı hesabı kaydederken "Kimlik doğrulama başarısız" hatası

**Nedenleri**:
- Yanlış Client ID veya Secret
- Sandbox kimlik bilgileri üretim modunda kullanılıyor (veya tam tersi)
- API anahtarı zaman aşımına uğramış veya iptal edilmiş
- Hesap doğrulanmamış

**Çözümler**:
- Sağlayıcı panelinden kimlik bilgilerini tekrar kopyalayın
- Modun eşleştiğini doğrulayın (sandbox vs üretim)
- API anahtarlarını yeniden oluşturun
- Sağlayıcı desteğiyle hesap durumunu doğrulayın

### Webhook Alınmadı

**Belirti**: Ödeme "İşlemde" durumuyla kalır

**Nedenleri**:
- Sağlayıcı panelinde webhook URL'si yapılandırılmadı
- HTTPS sertifikası geçersiz
- Güvenlik duvarı sağlayıcı IP'lerini engelliyor
- Webhook imza doğrulaması başarısız

**Çözümler**:
- Sağlayıcı ayarlarında webhook URL'sini tekrar kontrol edin
- HTTPS sertifikasının geçerli olduğundan emin olun
- Güvenlik duvarında sağlayıcı IP aralıklarını beyaz listeleyin
- Celery günlüklerinde imza hatalarını kontrol edin
- Sağlayıcının simülatör aracıyla webhook'ı test edin

### Ödeme Başarısız Oldu

**Belirti**: Ödeme durumu "Başarısız" olarak değişir ve hata mesajı ile birlikte

**Nedenleri**:
- Geçersiz komisyon sağlayıcısı ödeme bilgileri (yanlış e-posta veya banka hesabı)
- Sağlayıcı hesabında yeterli bakiye yok
- Alıcı hesabı ödemeleri alamaz
- Ülke desteklenmiyor (Airwallex)
- Ödeme sağlayıcı sınırlarını aşıyor

**Çözümler**:
- **Sağlayıcı Yanıt** alanındaki hatayı inceleyin
- Komisyon sağlayıcısının ödeme bilgilerinin doğru olduğundan emin olun
- Sağlayıcı hesabına bakiye ekleyin
- Komisyon sağlayıcısına hesap durumunu kontrol etmesini isteyin
- Sağlayıcının ülke ve döviz desteği durumunu kontrol edin
- Sınırları aşıyan büyük ödemeleri bölün

### Mod Eşleşmeme

**Belirti**: Test ödemeleri çalışıyor ancak üretim ödemeleri başarısız oluyor

**Nedenleri**:
- Sağlayıcı Sandbox modunda ancak üretim komisyon sağlayıcıları kullanılıyor
- API kimlik bilgileri yanlış ortamdan

**Çözümler**:
- Sağlayıcı modunu Production'a değiştirin
- Üretim API kimlik bilgilerini yeniden oluşturun
- Webhook URL'sinin üretim domain'ine işaret ettiğini doğrulayın

## Güvenlik En İyi Uygulamaları

Ödeme entegrasyonunuzu aşağıdaki güvenlik önlemleriyle koruyun:

### Kimlik Bilgisi Depolama

- **Kimlik bilgilerini sürüm kontrolüne eklemeyin** — Ortam değişkenleri veya güvenli depolama kullanın
- **API anahtarlarını çeyrek olarak döndürün** — Her 3 ayda bir yeni anahtarlar oluşturun
- **Sandbox ve üretim için ayrı anahtarlar kullanın** — Ortamları asla karıştırmayın
- **API izinlerini sınırlayın** — Sadece Ödeme erişimini verin, tam hesap kontrolü değil

Spwig, sağlayıcı kimlik bilgilerini veritabanında şifrelenerek saklar. Veritabanı yedeklerinizi güvenli tutun.

### Webhook Güvenliği

- **Her zaman imzaları doğrulayın** — İmza doğrulamasını asla atlamayın
- **Sadece HTTPS kullanın** — HTTP webhook'ları desteklenmez
- **IP adresi beyaz listesi uygulayın** — Webhook'ları sağlayıcı IP aralıklarına sınırlayın
- **Tüm webhook'ları günlüğe alın** — Şüpheli aktiviteyi izleyin
- **Webhook uç noktalarını hız sınırlaması uygulayın** — Abusmanı önleyin

### Erişim Kontrolü

- **Personel erişimini sınırlayın** — Sadece güvenilir personel ödemeleri işleyebilir
- **İki faktörlü kimlik doğrulama kullanın** — Personel hesapları için 2FA gereklidir
- **Ödeme eylemlerini denetleyin** — Kimin hangi ödemeleri işlediğini inceleyin
- **Görevleri ayırın** — Onaylama ve işleme için farklı personel kullanın

### İzleme

- **Günlük olarak başarısız ödemeleri kontrol edin** — Sorunları hızlıca çözmek için
- **Sağlayıcı hesap bakiyelerini izleyin** — Yeterli bakiyenin olduğundan emin olun
- **Haftalık işlem günlüklerini inceleyin** — Anomalileri erken yakalayın
- **Uyarıları ayarlayın** — Büyük veya başarısız ödemeler için e-posta bildirimleri

## İpuçları

- Üretim moduna geçmeden önce sandbox modunda entegrasyonu dikkatlice test edin — sahte para ile sorunları yakalayın.
- PayPal ve Airwallex'i ikisini de yapılandırın, komisyon sağlayıcılarının ödeme yöntemi seçimi için seçenek sunun — farklı komisyon sağlayıcıları farklı yöntemleri tercih eder.
- İlk kurulum sırasında webhook URL'lerini yapılandırın ve doğru şekilde ateşlendiğini doğrulayın — webhook'lar otomasyon için kritik öneme sahiptir.
- Toplu işleme sırasında başarısız ödemeleri önlemek için sağlayıcı hesap bakiyelerini daima doldurun.
- Birden fazla sağlayıcı yapılandırırsanız, hesap isimlerini açıklayıcı olarak ayarlayın (örneğin, "PayPal USD", "PayPal EUR").
- Güvenlik en iyi uygulamaları olarak API kimlik bilgilerini her çeyrekte bir döndürün.
- Webhook URL'lerini ve kimlik bilgilerinizi birlikte paylaşacağınız güvenli şifreleme programında belgeleyin.
- Başarısız ödemeleri hemen kontrol edin — gecikmeler komisyon sağlayıcılarını kızdırır ve programın itibarını zarar verir.
- Spwig kurulumunuzu her zaman HTTPS ile kullanın — webhook'lar SSL sertifikaları gerektirir.
- Kalıcı hatalarla karşılaşırsanız sağlayıcı desteğiyle iletişime geçin — onlar hesap durumunuzu ve izinlerinizi doğrulayabilir.

Unutmayın: Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruma kurallarında gösterildiği gibi tam olarak koruyun.