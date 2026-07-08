---
title: SSL Kurulumu
---

SSL (Güvenli Soket Katmanı), müşterilerinin tarayıcıları ve mağazanız arasındaki bağlantıyı şifreler. SSL etkin olduğunda, mağazanızın URL'si `https://` ile başlar ve tarayıcılar bir kilidi simgesi görüntüler. Ödeme alma, müşteri verilerini koruma ve arama motorlarında iyi sıralanma için SSL çok önemlidir.

Spwig, farklı sunucu yapılandırmalarına uygun birkaç SSL modu destekler. Bu kılavuz, her modu açıklar ve size uygun olanı seçmenize yardımcı olur.

## SSL Modu Seçimi

| Mod | En Uygun | Sertifika Ücreti | Yenileme |
|------|----------|-----------------|---------|
| **Let's Encrypt** | Çoğu mağaza için | Ücretsiz | Otomatik |
| **Cloudflare Origin CA** | Cloudflare proxy kullanan mağazalar için | Ücretsiz | Manuel (maksimum 15 yıl) |
| **Özel Sertifika** | Satın alınan sertifikaları olan mağazalar için | Değişir | Manuel |
| **Dışarıdan Yönetilen** | Yük dengeleyiciler, Cloudflare Esnek | Yok | Yok |
| **Kendi İmzalı** | Geliştirme ve test için | Ücretsiz | Manuel |
| **Hiçbiri (HTTP)** | Yalnızca yerel geliştirme için | Yok | Yok |

Hangi modunun kullanılacağından emin değilseniz, **Let's Encrypt** çoğu mağaza için en iyi seçimdir. Ücretsiz, otomatik ve tüm tarayıcılar tarafından güvenilirdir.

## Let's Encrypt

Let's Encrypt, 60-90 günde otomatik olarak yenilenen ücretsiz ve güvenilir SSL sertifikaları sağlar. Bu, çoğu satıcı için önerilen seçenektir.

**Gereksinimler:**
- Alan adınız, sunucunuza işaret etmelidir (DNS'de A kaydı)
- 80 numaralı port, internet üzerinden erişilebilir olmalıdır (sertifika doğrulaması için)
- Sertifika sona erme bildirimleri için bir e-posta adresi

**Kurulum adımları:**
1. **Ayarlar > Site Ayarları**'na gidin ve **Alan Adı & SSL** sekmesini açın
2. Alan adınızı girin
3. **Let's Encrypt**'i seçin
4. Yönetici e-posta adresinizi girin
5. **Ayarları Uygula**'ya tıklayın

Spwig, diğer her şeyi otomatik olarak yönetir: alan adınızı doğrulama, sertifikayı alma, NGINX'i yapılandırma ve otomatik yenileme kurulumu.

## Cloudflare Origin CA

Cloudflare Origin CA sertifikaları, Cloudflare'nin kenar sunucuları ve mağazanız arasındaki bağlantıyı şifreler. Bu sertifikalar ücretsizdir ve 15 yıla kadar sürebilir, ancak sadece **Cloudflare tarafından güvenilir**dir – sunucunuza doğrudan bağlanan tarayıcılar sertifika uyarısı görecektir.

Bu mod, alan adınız için Cloudflare proxy'sini (turuncu bulut etkin) kullandığınızda idealdir. Cloudflare, ziyaretçilere kendi güvenilir sertifikasını sunar ve Origin CA sertifikası, Cloudflare ve sunucunuz arasındaki bağlantıyı güvenli hale getirir.

**Gereksinimler:**
- Alan adınızla birlikte bir Cloudflare hesabı
- Cloudflare panelden oluşturulan bir Origin CA sertifikası ve özel anahtar
- Cloudflare SSL/TLS modu, **Full (Strict)** olarak ayarlanmış olmalı

**Origin CA sertifikasını oluşturma:**
1. Cloudflare paneline giriş yapın
2. Alan adınızı seçin
3. **SSL/TLS > Origin Server**'a gidin
4. **Sertifika Oluştur**'a tıklayın
5. RSA veya ECC seçin (RSA en uyumludur)
6. Alan adınızı ekleyin (örneğin, `example.com` ve `*.example.com`)
7. Geçerlilik süresi seçin (15 yıl önerilir)
8. **Oluştur**'a tıklayın ve sertifikayı ve özel anahtarı kopyalayın

**Spwig'de Ayarlama:**
1. **Ayarlar > Site Ayarları**'na gidin ve **Alan Adı & SSL** sekmesini açın
2. Alan adınızı girin
3. **Cloudflare Origin CA**'yı seçin
4. Sertifikayı **Sertifika (PEM)** alanına yapıştırın
5. Özel anahtarı **Özel Anahtar (PEM)** alanına yapıştırın
6. **Ayarları Uygula**'ya tıklayın

**Ayarlamadan Sonra:**
- Cloudflare'de SSL/TLS modunu **Full (Strict)** olarak ayarlayın
- Alan adınızın DNS kaydı için Cloudflare proxy'sini (turuncu bulut) etkinleştirin
- Mağazanız, Cloudflare'ın güvenilir sertifikasıyla HTTPS üzerinden erişilebilir olacak

## Özel Sertifika

Bir sertifika otoritesi (CA) örneğin DigiCert, Sectigo veya GoDaddy'den bir SSL sertifikası satın aldıysanız veya hosting sağlayıcınızdan bir sertifika verildiyse bu modu kullanın.

**Kurulum adımları:**
1.

**Ayarlar > Site Ayarları**'na gidin ve **Alan Adı & SSL** sekmesini açın
2.

Alan adınızı girin
3.

**Özel Sertifika**'yı seçin
4.

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

Sertifika zincirinizi (**Sertifika (PEM)** alanına yapıştırın
5.

Özel anahtarınızı (**Özel Anahtar (PEM)** alanına yapıştırın
6.

**Yapılandırmayı Uygula**'ya tıklayın

Sertifikanız, tam zinciri içermelidir: alan adı sertifikası, ardından ara sertifikalar. Özel anahtar, PEM formatında olmalıdır ("-----BEGIN PRIVATE KEY-----" veya "-----BEGIN RSA PRIVATE KEY-----" ile başlamalıdır).

## Dışarıdan Yönetilen

SSL, trafiğin sunucunuza ulaşmadan önce bir dış hizmet tarafından sonlandırıldığında bu modu seçin. Bu yapılandırmada, sunucunuz sadece düz HTTP trafiği alır -- sunucuya sertifika yüklenecek değildir.

**Tümleşik senaryolar:**
- **Cloudflare Esnek SSL** -- Cloudflare, tarayıcıdan Cloudflare'a giden trafiği şifreler, ancak sunucunuza HTTP gönderir
- **Bulut yük dengeleyicileri** -- AWS ALB, Google Cloud Load Balancer veya DigitalOcean Load Balancer SSL'yi sonlandırır ve HTTP iletir
- **Ters proxy** -- Spwig'in önündeki başka bir sunucu SSL'yi yönetir

**Ayarlama adımları:**
1. **Ayarlar > Site Ayarları**'na gidin ve **Alan Adı & SSL** sekmesini açın
2. Alan adınızı girin
3. **Dışarıdan Yönetilen**'i seçin
4. **Yapılandırmayı Uygula**'ya tıklayın

Spwig, NGINX'i sadece HTTP sunacak şekilde yapılandırır ve proxy'nizden gelen `X-Forwarded-Proto` başlığını güvenerek HTTPS ziyaretçilerini doğru bir şekilde tespit eder.

## Kendi İmzalı Sertifika

Kendi imzalı sertifikalar, bağlantıyı şifreler ancak tarayıcılar tarafından güvenilmez. Ziyaretçiler, bunu manuel olarak atlamaları gereken bir güvenlik uyarısı görecekler. Bu mod, yalnızca geliştirme sunucuları ve iç testler için uygundur.

**Ayarlama adımları:**
1. **Ayarlar > Site Ayarları**'na gidin ve **Alan Adı & SSL** sekmesini açın
2. Alan adınızı girin
3. **Kendi İmzalı**'yı seçin
4. **Yapılandırmayı Uygula**'ya tıklayın

Spwig, otomatik olarak bir kendi imzalı sertifika oluşturur. Bu modu üretim mağazalarınızda kullanmayın.

## Sorun Giderme

**Yapılandırma sonrası sertifika çalışmıyor:**
- Alan adınızın A kaydı, sunucunuzun IP adresine işaret ettiğini doğrulayın
- Yangın duvarınızda 80 ve 443 portlarının açık olduğundan emin olun
- DNS değişikliklerinin yayılmasını birkaç dakika bekleyin

**Let's Encrypt sertifika veremiyor:**
- Alan adınızın bu sunucunun IP adresine çözüldüğünden emin olun
- Yangın duvarınızda 80 portunun engellenmediğinden emin olun
- Cloudflare'ın arkasındaysanız, sertifika verme sırasında DNS'i "DNS Only" (gri bulut) olarak geçici olarak ayarlayın

**Cloudflare, "Hata 526" (Geçersiz SSL Sertifikası) gösteriyor:**
- **Cloudflare Origin CA** modunu ("Dışarıdan Yönetilen" değil) seçtiğinizden emin olun
- Cloudflare SSL/TLS modunun **Full (Strict)** olarak ayarlandığından emin olun
- Origin CA sertifikasının zaman aşımına uğramadığından emin olun

**SSL'e sahip olmalarına rağmen tarayıcı "Güvenilir Değil" gösteriyor:**
- Bazı sayfalar, HTTP üzerinden resimler veya betikler yükleyebilir (karışık içerik). Tarayıcınızın geliştirici konsolunda karışık içerik uyarısı için kontrol edin.
- Ayarlamalarda site URL'sinin `https://` kullanıldığından emin olun