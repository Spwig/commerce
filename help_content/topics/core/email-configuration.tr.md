---
title: E-posta Yapılandırması
---

E-posta yapılandırması, mağazanızın işlem e-postalarını nasıl gönderdiğini kontrol eder — sipariş onayları, kargo bildirimleri, şifre sıfırlamaları ve daha fazlası. Spwig, daha yüksek teslim edilebilirlik için dahili bir SMTP sunucusu içerir ve harici e-posta sağlayıcılarını destekler.

![E-posta hesapları](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Kullanılabilir Sağlayıcılar

| Sağlayıcı | Açıklama |
|----------|-------------|
| **Dahili SMTP** | Spwig ile birlikte gelen ücretsiz, kendi kendine barındırılan e-posta sunucusu. Otomatik DKIM imzalama. |
| **Gmail API** | OAuth kimlik doğrulaması kullanarak Gmail veya Google Workspace hesabınız üzerinden gönderim yapın. |
| **Genel SMTP** | Herhangi bir SMTP sunucusuna bağlanın (SendGrid, Mailgun, Amazon SES veya kendi e-posta sunucunuz). |

## E-posta Kurulumu

**Ayarlar > E-posta Hesapları** bölümüne gidin ve kurulum sihirbazını başlatmak için **E-posta Hesabı Ekle**'ye tıklayın.

### Adım 1: Sağlayıcı Seçimi

E-posta sağlayıcınızı seçin. Dahili SMTP sunucusu, başlamak için en basit seçenektir — harici hesaplara gerek yoktur.

### Adım 2: Kimlik Bilgilerini Yapılandırma

Seçtiğiniz sağlayıcı için kimlik bilgilerini girin:

- **Dahili SMTP** — Kimlik bilgisi gerekmez. Sunucu Spwig kurulumunuzda çalışır.
- **Gmail API** — Google OAuth ile kimlik doğrulaması yapın. Google hesabınızla oturum açmak için yönlendirileceksiniz.
- **Genel SMTP** — SMTP sunucu adresini, portu, kullanıcı adını ve şifreyi girin.

### Adım 3: Gönderen Yapılandırması

Giden e-postalar için gönderen kimliğini ayarlayın:

- **Gönderen E-posta** — "Gönderen" alanında görünen e-posta adresi (ör. orders@yourstore.com)
- **Gönderen Adı** — E-posta adresinin yanında görünen ad (ör. "Mağaza Adınız")
- **Yanıt Adresi** — Müşteri yanıtlarının yönlendirildiği adres (Gönderen adresinden farklı olabilir)

### Adım 4: DNS Doğrulama

Alan adınızın e-posta kimlik doğrulama kayıtlarını doğrulayın. Sihirbaz üç DNS kaydını kontrol eder:

| Kayıt | Amaç |
|--------|---------|
| **SPF** | Sunucunuzun alan adınız adına e-posta göndermesine izin verir |
| **DKIM** | E-postaların değiştirilmediğini kanıtlamak için dijital olarak imzalar |
| **DMARC** | SPF/DKIM kontrollerinden geçmeyen e-postalarla ilgili alıcı sunuculara ne yapmaları gerektiğini söyler |

Her kayıt için sihirbaz şunları gösterir:
- **Mevcut durum** — Kaydın doğru yapılandırılıp yapılandırılmadığı
- **Gerekli değer** — Alan adı kayıtçınızda eklemeniz gereken tam DNS kaydı
- **Yayılma durumu** — Son değişikliklerin geçerli olup olmadığı (DNS değişiklikleri 48 saate kadar sürebilir)

Dahili SMTP sunucusu, alan adınız için DKIM anahtarlarını otomatik olarak oluşturur.

### Adım 5: Test E-postası Gönder

Her şeyin çalıştığını doğrulamak için bir test e-postası gönderin:
1. Bir alıcı e-posta adresi girin
2. **Test Gönder**'e tıklayın
3. Gelen kutunuzda test mesajını kontrol edin
4. E-postanın spam uyarıları olmadan ulaştığını doğrulayın

### Adım 6: Kaydet ve Etkinleştir

Yapılandırmayı kaydedin ve hesabı etkin olarak ayarlayın. Birincil e-posta hesabı olması gerekiyorsa **Varsayılan** olarak işaretleyin.

## E-posta Şablonları

Spwig, her işlem olayı için 30'dan fazla e-posta şablonu içerir. Bunları yönetmek için **Ayarlar > E-posta Şablonları** bölümüne gidin.

### Şablon Türleri

Şablonlar, aşağıdakiler dahil tüm mağaza olaylarını kapsar:
- **Sipariş Yaşam Döngüsü** — Onay, işleme, kargoya verildi, teslim edildi, iptal edildi
- **Ödeme** — Makbuz, iade onayı, başarısız ödeme
- **Müşteri Hesabı** — Hoş geldiniz, şifre sıfırlama, e-posta doğrulama
- **Hediye Kartları** — Teslimat, bakiye bildirimi
- **Kargo** — Takip güncellemeleri, teslimat onayı
- **Dijital Ürünler** — İndirme bağlantıları, lisans anahtarları
- **Pazarlama** — Terk edilen sepet kurtarma, yorum istekleri

### Şablonları Özelleştirme

1. Şablon listesine gidin
2. Düzenlemek için bir şablona tıklayın
3. Konu satırını, başlığı, gövde içeriğini ve alt bilgisi değiştirin
4. Dinamik içerik için şablon değişkenlerini kullanın (ör. `{{ order.number }}`, `{{ customer.name }}`)
5. Kaydetmeden önce e-postayı önizleyin

### Çok Dilli Destek

E-posta şablonları birden fazla dili destekler:
- Her şablon, mağazanızdaki etkin tüm diller için çevirilere sahip olabilir
- Sistem, e-postaları müşterinin tercih ettiği dilde gönderir
- **Dil yedekleme zinciri** — Bir çeviri mevcut değilse, sistem mağazanın varsayılan diline geri döner
- Şablonları diğer dillere otomatik olarak çevirmek için **Yapay Zeka Çevirisi** özelliğini kullanın

### Şablon Klonlama

Bir sistem şablonunun özelleştirilmiş bir sürümünü oluşturmak için:
1. Değiştirmek istediğiniz şablonu açın
2. **Şablonu Klonla** seçeneğine tıklayın
3. Klonlanmış sürümü düzenleyin
4. Klon, orijinal sistem şablonuna öncelik kazanır

## E-posta Kuyruğu

Giden e-postaları **Ayarlar > E-posta Kuyruğu** bölümünde izleyin:

- **Kuyrukta** — Gönderilmeyi bekleyen e-postalar
- **Gönderiliyor** — Şu anda iletilen e-postalar
- **Gönderildi** — Başarıyla teslim edilen e-postalar
- **Başarısız** — Teslim edilemeyen e-postalar (hata ayrıntılarıyla birlikte)
- **Geri Dönen** — Alıcının e-posta sunucusu tarafından reddedilen e-postalar

Alıcı, konu, gönderim zamanı ve teslim durumu dahil olmak üzere tam ayrıntılarını görüntülemek için herhangi bir e-postaya tıklayın.

## Teslimat Takibi

E-posta etkileşimini izleyin:
- **Açılışlar** — E-postayı açan alıcı sayısı
- **Tıklamalar** — E-posta içindeki bağlantı tıklamaları
- **Geri Dönüşler** — Sert ve yumuşak geri dönüş takibi
- **Şikayetler** — Alıcılardan gelen spam bildirimleri

## Birden Fazla Hesap

Birden fazla e-posta hesabı yapılandırabilirsiniz:
- **Varsayılan Hesap** — Aşırı yazılmadıkça tüm giden e-postalar için kullanılır
- **Yedek** — Varsayılan hesap başarısız olursa, e-postalar yeniden deneme için kuyruğa alınır
- Farklı amaçlar için farklı hesaplar kullanın (ör. biri işlem e-postaları için, diğeri pazarlama için)

## E-posta Teslimat Modu

Mağazanızın giden e-postaları nasıl işlediğini kontrol etmek için **Ayarlar > Mağaza Ayarları** bölümüne gidin. Bu ayarlar, geliştirme ve test sırasında faydalıdır.

| Mod | Açıklama |
|------|-------------|
| **Canlı** | E-postalar gerçek alıcılara normal şekilde teslim edilir |
| **Duraklatıldı** | E-postalar kuyrukta tutulur ve Canlı moduna geri dönene kadar gönderilmez |
| **Yalnızca Kayıt** | E-postalar gönderi kutusuna kaydedilir ancak asla teslim edilmez |

### Test Yönlendirme E-postası

Tüm giden e-postaları kesip tek bir adrese yönlendirmek için bir **Test Yönlendirme E-postası** adresi belirleyin. Belirlendiğinde, gerçek alıcıdan bağımsız olarak her e-posta bu adrese gider. Bu, gerçek müşterilere yanlışlıkla göndermeden e-posta şablonlarını test etmek için faydalıdır. E-postaları gerçek alıcılara göndermek için boş bırakın.

### Sandbox E-posta Beyaz Liste

Sandbox veya geliştirme modunda, e-posta teslimatını onaylanmış adreslerin beyaz listesine kısıtlayabilirsiniz. Yalnızca beyaz listedeki adreslere gönderilen e-postalar teslim edilir. Diğer tüm e-postalar kaydedilir ancak asla gönderilmez. Yönetici e-postası her zaman otomatik olarak dahil edilir. En fazla 10 adres ekleyebilirsiniz.

## İpuçları

- Hızlı kurulum için **Yerleşik SMTP** sunucusuyla başlayın, ardından daha yüksek gönderim hacimleri veya daha iyi teslimat için harici bir sağlayıcıya geçin.
- Her zaman **SPF, DKIM ve DMARC** kayıtlarını yapılandırın — bunlar olmadan, e-postaların spam klasörlerine düşme olasılığı çok daha yüksektir.
- Teslimatın çalıştığını doğrulamak için herhangi bir yapılandırma değişikliğinden sonra bir **test e-postası** gönderin.
- **Başarısız** veya **geri dönen** e-postalar için e-posta kuyruğunu düzenli olarak izleyin — bunlar teslimat sorunlarını gösterir.
- Daha iyi güven ve teslimat için ücretsiz bir e-posta adresi yerine **profesyonel bir gönderici adresi** (ör. orders@yourstore.com) kullanın.
- Şablonlarınızı kısa tutun — işlem e-postaları pazarlama bültenleri olmamalı, bilgileri hızla iletmelidir.