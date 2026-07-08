---
title: E-posta Yapılandırması
---

E-posta yapılandırması, mağazanızın işlemci e-postaları gönderme şeklini kontrol eder — sipariş onayları, kargo bildirimleri, şifre sıfırlamaları ve daha fazlası. Spwig, iç built-in bir SMTP sunucusu içerir ve yüksek teslimat başarısı için harici e-posta sağlayıcılarını da destekler.

![E-posta hesapları](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Mevcut Sağlayıcılar

| Sağlayıcı | Açıklama |
|----------|-------------|
| **Built-in SMTP** | Spwig ile birlikte gelen ücretsiz, kendi kendine barındırılan e-posta sunucusu. Otomatik DKIM imzalama. |
| **Gmail API** | Google OAuth kimlik doğrulaması kullanarak Gmail veya Google Workspace hesabınızla e-posta gönderin. |
| **Genel SMTP** | Herhangi bir SMTP sunucusunu bağlanın (SendGrid, Mailgun, Amazon SES veya kendi e-posta sunucunuz). |

## E-posta Ayarlama

**Ayarlar > E-posta Hesapları**'na gidin ve kurulum asistanını başlatmak için **E-posta Hesabı Ekle**'ye tıklayın.

### Adım 1: Sağlayıcı Seçin

E-posta sağlayıcınızı seçin. Built-in SMTP sunucusu, başlamak için en basit seçenektir — harici hesaplara ihtiyaç duymaz.

### Adım 2: Kimlik Bilgilerini Yapılandırın

Seçtiğiniz sağlayıcının kimlik bilgilerini girin:

- **Built-in SMTP** — Kimlik bilgileri gerekmez. Sunucu, Spwig kurulumunuzda çalışır.
- **Gmail API** — Google OAuth ile kimlik doğrulayın. Google hesabınızla oturum açmak için yönlendirileceksiniz.
- **Genel SMTP** — SMTP sunucu adresini, bağlantı noktasını, kullanıcı adını ve şifreyi girin.

### Adım 3: Gönderen Yapılandırması

Giden e-postalar için gönderen kimliğini ayarlayın:

- **From E-posta** — "From" alanına görünen e-posta adresi (örneğin, orders@yourstore.com)
- **From Adı** — E-posta adresinin yanındaki görüntülenecek ad (örneğin, "Your Store Name")
- **Reply-To E-posta** — Müşteri yanıtlarının yönlendirildiği yer (From adresinden farklı olabilir)

### Adım 4: DNS Doğrulama

Alan adınızın e-posta kimlik doğrulama kayıtlarını doğrulayın. Asistan, üç DNS kaydını kontrol eder:

| Kayıt | Amaç |
|--------|---------|
| **SPF** | Alan adınızın adı için e-posta göndermek için sunucunuzu yetkilendirir |
| **DKIM** | E-postaların manipüle edilmediğini ispatlamak için dijital imza |
| **DMARC** | SPF/DKIM kontrollerini geçemeyen e-postalar için alıcı sunucularına ne yapılacağını söyler |

Her kayıt için asistan şu bilgileri gösterir:
- **Mevcut durum** — Kayıtın doğru şekilde yapılandırılıp yapılandırılmadığı
- **Gerekli değer** — Alan adı kaydınıza eklemelik tam DNS kaydı
- **Yayılım durumu** — Son değişikliklerin etkisine girip girmedikleri (DNS değişiklikleri 48 saat kadar sürebilir)

Built-in SMTP sunucusu, alan adınız için otomatik olarak DKIM anahtarları oluşturur.

### Adım 5: Test E-postası Gönder

Her şeyin düzgün çalışıp çalışmadığını doğrulamak için test e-postası gönderin:
1. Alıcı e-posta adresini girin
2. **Test Gönder**'e tıklayın
3. Test mesajını kutunuzda kontrol edin
4. E-postanın spam uyarıları olmadan ulaşmış olup olmadığını doğrulayın

### Adım 6: Kaydet ve Etkinleştir

Yapılandırmayı kaydedin ve hesabı etkinleştirin. Hesabı **Varsayılan** olarak işaretleyin, eğer bu, ana e-posta hesabınız olacaksa.

## E-posta Şablonları

Spwig, her işlemci olayı için 30'dan fazla e-posta şablonu içerir. **Ayarlar > E-posta Şablonları**'na gidin ve onları yönetin.

### Şablon Türleri

Şablonlar, tüm mağaza olaylarını kapsar, bunlar:
- **Sipariş Yaşam Döngüsü** — Onay, işleme, gönderildi, teslim edildi, iptal edildi
- **Ödeme** — Fatura, iade onayı, başarısız ödeme
- **Müşteri Hesabı** — Hoş geldiniz, şifre sıfırlama, e-posta doğrulama
- **Hediye Çekleri** — Teslimat, bakiye bildirimi
- **Kargo** — Takip güncelleştirmeleri, teslim onayı
- **Dijital Ürünler** — İndirme bağlantıları, lisans anahtarları
- **Pazarlama** — Bırakılan sepet geri kazanımı, inceleme istekleri

### Şablonları Özelleştirme

1. Şablon listesine gidin
2. Düzenlemek istediğiniz şablonu tıklayın
3. Konu satırını, başlığı, içerik ve altbilgiyi değiştirin
4. Dinamik içerik için şablon değişkenlerini kullanın (örneğin, `{{ order.number }}`, `{{ customer.name }}`)
5. Kaydetmeden önce e-postayı önizleyin

### Çok Dilli Desteğe

E-posta şablonları çok dilli destek sağlar:
- Her şablon, mağazanızın tüm etkin dilleri için çeviriye sahip olabilir
- Sistem, müşterinin tercih ettiği dile e-posta gönderir
- **Dil geri dönüş zinciri** — Eğer bir çeviri mevcut değilse, sistem mağazanın varsayılan diline geri döner
- Diğer dillere şablonları otomatik olarak çevirmek için **AI Çeviri** özelliğini kullanın

### Şablonları Kopyalama

Bir sistem şablonunun özelleştirilmiş bir sürümü oluşturmak için:
1. Düzenlemek istediğiniz şablonu açın
2. **Şablonu Kopyala**'ya tıklayın
3. Kopyalanan sürümü düzenleyin
4. Kopya, orijinal sistem şablonundan önceliklidir

## E-posta Kuyruğu

**Ayarlar > E-posta Kuyruğu**'nda giden e-postaları izleyin:

- **Kuyrukta** — Gönderilmek üzere bekleyen e-postalar
- **Gönderiliyor** — Şu anda iletiliyor
- **Gönderildi** — Başarıyla teslim edildi
- **Başarısız** — Teslim edilemedi (hata ayrıntılarıyla birlikte)
- **Iptal** — Alıcının e-posta sunucusu tarafından reddedildi

Herhangi bir e-postayı tıklayarak onun tam detaylarını görüntüleyin, bunlar arasında alıcı, konu, gönderim zamanı ve teslim durumu yer alır.

## Teslimat Takibi

E-posta etkileşimini izleyin:
- **Açtılar** — Kaç alıcı e-postayı açtı
- **Tıklamalar** — E-postadaki bağlantı tıklamaları
- **Iptaller** — Sert ve yumuşak iptal izleme
- **Şikayetler** — Alıcılar tarafından spam raporları

## Birden Fazla Hesap

Birden fazla e-posta hesabı yapılandırabilirsiniz:
- **Varsayılan Hesap** — Tüm giden e-postalar için kullanılır, aksi takdirde geçersiz
- **Yedek** — Eğer varsayılan hesap başarısız olursa, e-postalar kuyrukta tekrar denenecek
- Farklı amaçlar için farklı hesapları kullanın (örneğin, biri işlemci e-postaları için, diğeri pazarlama için)

## İpuçları

- Hızlı kurulum için **Built-in SMTP** sunucusu ile başlayın, daha sonra yüksek gönderim hacmi veya daha iyi teslimat başarısı gerekirse harici bir sağlayıcıya geçin.
- Her zaman **SPF, DKIM ve DMARC** kayıtlarını yapılandırın — bunlar olmadan e-postalar spam klasörlerine daha muhtemel düşer.
- Her yapılandırma değişikliğinden sonra bir **test e-postası** gönderin, teslimatın düzgün çalıştığını doğrulayın.
- **Başarısız** veya **iptal** edilen e-postaları düzenli olarak izleyin — bunlar teslimat sorunlarını gösterir.
- **Profesyonel bir gönderen adresi** kullanın (örneğin, orders@yourstore.com) yerine ücretsiz bir e-posta adresi, daha iyi güven ve teslimat başarısı için.
- Şablonlarınızı özelleştirin — işlemci e-postaları hızlıca bilgiyi iletmelidir, pazarlama bültenleri olmamalıdır.