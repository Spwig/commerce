---
title: OAuth & Sosyal Giriş Kurulumu
---

OAuth ve sosyal giriş, müşterilerin mevcut Google, Apple veya Microsoft hesaplarını kullanarak mağazanıza giriş yapmalarını sağlar — başka bir şifre oluşturmak ve hatırlamak zorunda kalmazlar.

![OAuth ayarları](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## OAuth / Sosyal Giriş Nedir?

OAuth, güvenli bir kimlik doğrulama standartıdır ve müşterilerin Google, Apple veya Microsoft gibi güvenilir sağlayıcıların kimlik bilgilerini kullanarak giriş yapmalarını sağlar.

### Avantajlar

- **Daha Hızlı Ödeme** — Müşteriler kayıt formunu atlar ve tek bir tıklamayla giriş yapar
- **Daha Az Sürtünme** — Şifre oluşturma, doğrulama e-postaları veya unutulan şifre akışları gerekmez
- **Daha İyi Dönüşüm** — Araştırmalar, sosyal girişin dönüşüm oranlarını %20-40 arasında artırabileceğini gösteriyor
- **Artırılmış Güvenlik** — Kimlik bilgileri mağazanıza geçmez; kimlik doğrulama sağlayıcı tarafından yapılır
- **Müşteri Güveni** — Müşteriler, mevcut sağlayıcılarla kimlik bilgilerini güvenir

### Nasıl Çalışır

1. Müşteri, giriş sayfanızda "Google ile Giriş Yap" (veya Apple/Microsoft) butonuna tıklar
2. Sağlayıcının güvenli giriş sayfasına yönlendirilirler
3. Müşteri, sağlayıcı kimlik bilgileriyle kimlik doğrular
4. Sağlayıcı, doğrulanmış kimlik bilgilerini mağazanıza geri gönderir
5. Müşteri otomatik olarak giriş yapar

İlk girişde, sağlayıcıdan alınan e-posta ve profil bilgileriyle yeni bir müşteri hesabı otomatik olarak oluşturulur.

## Desteklenen Sağlayıcılar

Spwig, üç büyük OAuth sağlayıcısını destekler:

| Sağlayıcı | Kullanım Durumu | Kimlik Bilgisi Gereksinimleri |
|----------|----------|------------------------|
| **Google** | En popüler, en kolay kurulum | Client ID, Client Secret |
| **Apple** | iOS uygulamaları için gerekli, gizlilik odaklı | Client ID, Team ID, Key ID, Private Key |
| **Microsoft** | Kurumsal müşteriler, Office 365 kullanıcıları | Client ID, Client Secret, Tenant ID |

Bir, iki veya üç sağlayıcıyı etkinleştirebilirsiniz. Her biri bağımsız olarak çalışır.

## Google OAuth Kurulumu

Google OAuth, en popüler ve en kolay kurulumu olan seçeneğidir.

### Önkoşullar

- Bir Google hesabı
- Google Cloud Console erişimi

### Adım Adım Kurulum

1. **OAuth Ayarlarına Git

   - Yönetici panelinizde **Ayarlar > Mağaza Ayarları**'na gidin
   - **OAuth Sağlayıcıları** bölümüne kaydırın
   - **Google'ı Yapılandır**'a tıklayın

2. **Google Cloud Projesi Oluştur

   - [Google Cloud Console](https://console.cloud.google.com/) adresine gidin
   - **Proje Oluştur**'a tıklayın
   - Bir proje adı girin (örneğin, "Mağaza OAuth")
   - **Oluştur**'a tıklayın

3. **Google+ API'yi Etkinleştir

   - Sol menüde **APIs & Services > Kütüphane**'ye gidin
   - "Google+ API" arayın
   - **Etkinleştir**'e tıklayın

4. **OAuth Kimlik Bilgileri Oluştur

   - **APIs & Services > Kimlik Bilgileri**'ne gidin
   - **Kimlik Bilgisi Oluştur > OAuth Client ID**'ye tıklayın
   - Uygulama türü seçin: **Web Uygulaması**
   - Bir ad girin (örneğin, "Mağaza Giriş")

5. **Yönlendirme URI'sini Yapılandır

   - **Yetkili Yönlendirme URI'leri** altında şu adresi ekleyin:
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - `yourdomain.com`'ı gerçek domaininizle değiştirin
   - **Oluştur**'a tıklayın

6. **Kimlik Bilgilerini Kopyala

   - Popup'tan **Client ID** ve **Client Secret**'i kopyalayın

7. **Spwig'de Kimlik Bilgilerini Girin

   - Spwig yönetici paneli OAuth ayarlarına geri dönün
   - Client ID ve Client Secret'yi yapıştırın
   - **Kaydet**'e tıklayın
   - **Google OAuth'ı Etkinleştir**'i etkinleştirmek için anahtarlayın

### Test Etme

- Mağaza ön yüzü giriş sayfanızı ziyaret edin
- "Google ile Giriş Yap" butonunu arayın
- Tıklayın ve Google hesabınızla kimlik doğrulayın
- Giriş yapmış ve müşteri kontrol panelinize yönlendirilmelisiniz

## Apple OAuth Kurulumu

Apple OAuth, anahtar tabanlı kimlik doğrulama sistemi nedeniyle Google'dan daha karmaşık olabilir.

### Önkoşullar

- Apple Developer hesabı (ödeme gerektiren üyelik)
- Apple Developer portal erişimi

### Adım Adım Kurulum

1. **OAuth Ayarlarına Git

   - **Ayarlar > Mağaza Ayarları > OAuth Sağlayıcıları**'na gidin
   - **Apple'ı Yapılandır**'a tıklayın

2. **Servis Kimliği Oluştur

   - [Apple Developer](https://developer.apple.com/account/) adresine girin
   - **Sertifikalar, Kimlikler & Profiller**'e gidin
   - **Kimlikler**'e tıklayın ve ardından **+** butonuna
   - **Servis Kimlikleri** seçin ve **Devam**'a tıklayın
   - Bir açıklama girin (örneğin, "Mağaza Giriş")
   - Bir kimlik girin (örneğin, `com.yourstore.login`)
   - **Devam**'a tıklayın ve ardından **Kaydet**

3. **Servis Kimliğini Yapılandır

   - Yeni oluşturduğunuz Servis Kimliği'ne tıklayın
   - **Apple ile Giriş Yap**'ı işaretleyin
   - **Yapılandır**'a tıklayın
   - Domain ve return URL'yi ekleyin:
     - **Domainler**: `yourdomain.com`
     - **Return URLs**: `https://yourdomain.com/accounts/apple/login/callback/`
   - **Kaydet**'e tıklayın ve ardından **Devam**'a ve **Kaydet**'e tekrar tıklayın

4. **Anahtar Oluştur

   - Sol menüde **Anahtarlar**'a tıklayın ve ardından **+** butonuna
   - Bir anahtar adı girin (örneğin, "Mağaza OAuth Anahtarı")
   - **Apple ile Giriş Yap**'ı işaretleyin
   - **Yapılandır**'a tıklayın ve temel Uygulama Kimliği'ni seçin
   - **Kaydet**'e tıklayın, ardından **Devam**'a ve **Kaydet**'e tekrar tıklayın
   - **İndirilen anahtar dosyasını** (.p8) indirin — tekrar indiremezsiniz

5. **Gerekli Bilgileri Topla

   Gerekli olanlar:
   - **Client ID** (Servis Kimliği): Oluşturduğunuz kimlik (örneğin, `com.yourstore.login`)
   - **Team ID**: Apple Developer portalının sağ üst köşesinde bulunur
   - **Key ID**: Anahtar oluşturduğunuzda gösterilir
   - **Private Key**: İndirdiğiniz .p8 dosyasının içeriği

6. **Spwig'de Kimlik Bilgilerini Girin

   - Spwig OAuth ayarlarına geri dönün
   - Client ID, Team ID ve Key ID'yi yapıştırın
   - .p8 dosyasını bir metin düzenleyici ile açın ve içeriğini kopyalayın
   - Anahtarın tamamını (başlıklar dahil) Özel Anahtar alanına yapıştırın
   - **Kaydet**'e tıklayın
   - **Apple OAuth'ı Etkinleştir**'i etkinleştirmek için anahtarlayın

### Test Etme

- Apple ID ile bir cihazda mağaza ön yüzü giriş sayfanızı ziyaret edin
- "Apple ile Giriş Yap" butonuna tıklayın
- Apple ID ile kimlik doğrulayın
- Başarıyla giriş yapmış olmalısınız

## Microsoft OAuth Kurulumu

Microsoft OAuth, Office 365 veya Azure AD kullanan iş müşterilerine yönelik mağazalar için idealdir.

### Önkoşullar

- Bir Microsoft hesabı
- Azure Portal erişimi

### Adım Adım Kurulum

1. **OAuth Ayarlarına Git

   - **Ayarlar > Mağaza Ayarları > OAuth Sağlayıcıları**'na gidin
   - **Microsoft'u Yapılandır**'a tıklayın

2. **Azure'da Uygulama Kaydet

   - [Azure Portal](https://portal.azure.com/) adresine gidin
   - **Azure Active Directory > Uygulama Kayıtları**'na gidin
   - **Yeni Kayıt**'a tıklayın
   - Bir ad girin (örneğin, "Mağaza OAuth")
   - **Herhangi bir örgütsel dizin ve kişisel Microsoft hesapları** seçin
   - **Yönlendirme URI**'si altında **Web** seçin ve şu adresi girin:
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - **Kayıt**'a tıklayın

3. **Uygulama Kimliğini Kopyala

   - Uygulama özeti sayfasında, **Uygulama (istemci) Kimliği**'ni kopyalayın

4. **İstemci Gizli Anahtarı Oluştur

   - Sol menüde **Sertifikalar & Gizli Anahtarlar**'a tıklayın
   - **Yeni İstemci Gizli Anahtarı**'na tıklayın
   - Bir açıklama girin (örneğin, "OAuth Gizli Anahtarı")
   - Bir süre seçin (önerilen: 24 ay)
   - **Ekle**'ye tıklayın
   - **Gizli anahtar değerini hemen kopyalayın** — tekrar gösterilmeyecektir

5. **Spwig'de Kimlik Bilgilerini Girin

   - Spwig OAuth ayarlarına geri dönün
   - Uygulama (istemci) Kimliğini Client ID olarak yapıştırın
   - Gizli anahtar değerini Client Secret olarak yapıştırın
   - Seçenek olarak bir Tenant ID girin (tek kiracılı uygulamalar için; çok kiracılı için boş bırakın)
   - **Kaydet**'e tıklayın
   - **Microsoft OAuth'ı Etkinleştir**'i etkinleştirmek için anahtarlayın

### Test Etme

- Mağaza ön yüzü giriş sayfanızı ziyaret edin
- "Microsoft ile Giriş Yap" butonuna tıklayın
- Microsoft hesabıyla kimlik doğrulayın
- Başarıyla giriş yapmış olmalısınız

## OAuth Bağlantılarını Yönetme

### Müşteri Görünümü

Müşteriler, hesap panellerinden bağlı OAuth sağlayıcılarını görüntüleyebilir ve yönetebilir:

- **Hesabım > Bağlı Hesaplar**'a gidin
- Hangi sağlayıcıların bağlı olduğunu görün (Google, Apple, Microsoft)
- Bir sağlayıcıyı bağlantısını kesmek için **Bağlantıyı Kes**'e tıklayın
- Tekrar bağlamak için o sağlayıcı ile tekrar giriş yapın

### Birden Fazla Sağlayıcı

Bir müşteri hesabı, birden fazla OAuth sağlayıcısına bağlanabilir. Örneğin, bir müşteri aynı hesabı hem Google ve Apple ile bağlayabilir.

Eğer bir müşteri aynı e-posta adresini kullanarak farklı bir OAuth sağlayıcısıyla giriş yapmaya çalışırsa, Spwig otomatik olarak mevcut hesabına bağlar.

### Yönetici Yönetimi

Yönetici olarak, müşteri OAuth bağlantılarını görüntüleyebilirsiniz:

- **Müşteriler > Müşteriler**'e gidin
- Bir müşteri kaydını açın
- **Bağlı Hesaplar** bölümüne kaydırın
- Hangi sağlayıcıların bağlı olduğunu ve ne zaman bağlandıklarını görün

Müşterilerin behalfında sağlayıcıları bağlantısını kesemezsiniz — güvenlik nedenleriyle onlar bunu kendileri yapmalıdır.

## Sorun Giderme

### Yönlendirme URI Eşleşmeme

**Hata**: "Yönlendirme URI eşleşmiyor" veya "Geçersiz redirect_uri"

**Çözüm**:
- Sağlayıcı ayarlarınızda yönlendirme URI'sinin Spwig'deki ile tam olarak eşleştiğinden emin olun
- Son çizgileri kontrol edin — eşleşmelidir
- `https://` kullanıldığını doğrulayın (değil `http://`)
- Tarayıcı önbelleğini temizleyin ve tekrar deneyin

### Geçersiz Kimlik Bilgileri

**Hata**: "Geçersiz client ID" veya "Kimlik doğrulama başarısız"

**Çözüm**:
- Client ID ve Client Secret'in doğru kopyalandığını tekrar kontrol edin
- Ekstra boşluklar veya satır atlamaları olup olmadığını kontrol edin
- Kimlik bilgilerinin doğru proje/uygulamadan geldiğini doğrulayın
- Apple için, Özel Anahtarın .p8 dosyasının tam içeriğini içerdiğinden emin olun

### Sağlayıcı API'si Etkin Değil

**Hata**: "API etkin değil" veya "Erişim yapılandırılmadı"

**Çözüm**:
- Google için: Google Cloud projesinizde Google+ API'nin etkin olduğundan emin olun
- Microsoft için: Uygulama kaydınızın onaylanmış ve etkin olduğundan emin olun
- Apple için: Servis Kimliğiniz için "Apple ile Giriş Yap"ın etkin olduğundan emin olun

### SSL Gerekli

**Hata**: "OAuth HTTPS gerektirir" veya "Güvenli olmayan yönlendirme URI"

**Çözüm**:
- OAuth sağlayıcıları güvenlik için SSL/TLS (HTTPS) gerektirir
- Mağazanızın geçerli bir SSL sertifikası yüklendiğinden emin olun
- Yönlendirme URI'lerini `https://` kullanacak şekilde güncelleyin
- Eğer yerel olarak test ediyorsanız, ngrok gibi bir hizmeti kullanarak HTTPS tüneli oluşturun

### Buton Görünmüyorsa

**Sorun**: "Google/Apple/Microsoft ile Giriş Yap" butonu giriş sayfasında görünmüyor

**Çözüm**:
- Sağlayıcının OAuth ayarlarında etkin olduğundan emin olun
- Tarayıcı önbelleğini temizleyin ve sayfayı yenileyin
- Temanızın sosyal giriş şablonunu içerdiğinden emin olun
- Tarayıcı konsolunda JavaScript hatalarını inceleyin

## İpuçları ve En İyi Uygulamalar

### Güvenlik

- **Gizli anahtarları düzenli olarak döndürün** — Client Secret'leri yılda 12-24 ayda bir güncelleyin
- **Başarısız giriş denemelerini izleyin** — Anormal kimlik doğrulama desenlerini izleyin
- **Çevre başına ayrı kimlik bilgileri kullanın** — Test ve üretim için farklı kimlik bilgileri kullanın
- **Yönlendirme URI'lerini kısıtlayın** — Sadece ihtiyacınız olan URI'leri ekleyin

### Kullanıcı Deneyimi

- **Üç sağlayıcıyı da etkinleştirin** — Müşterilere seçim hakkı verin; farklı demografik gruplar farklı sağlayıcıları tercih eder
- **Butonları öne çıkarın** — Sosyal giriş butonları e-posta/şifre formunun üstünde olmalıdır
- **Tanınabilir markalama kullanın** — Google/Apple/Microsoft standart buton stillerini koruyun
- **Mobil cihazlarda test edin** — OAuth akışları mobil tarayıcılarda farklı çalışır

### Uygunluk

- **Gizlilik Politikası** — OAuth sağlayıcılarını kullandığınızı ve hangi verileri aldığınızı açıklamalısınız
- **Kullanım Koşulları** — Sağlayıcı koşullarına uyun (Google, Apple ve Microsoft her biri kendi gereksinimlerini有自己的)
- **Veri Azaltımı** — Sadece gerçekten ihtiyaç duyduğunuz profil bilgilerini isteyin

### Test Kontrol Listesi

Yaşamaya hazır olduğunuzda test edin:

- [ ] Her sağlayıcı ile masaüstüde giriş yapma
- [ ] Her sağlayıcı ile mobil cihazda giriş yapma
- [ ] İlk giriş (hesap oluşturma)
- [ ] Sonraki girişler (hesap bağlama)
- [ ] Aynı e-posta adresiyle farklı sağlayıcılarla giriş yapma
- [ ] Bir sağlayıcıyı bağlantısını kes ve tekrar bağla
- [ ] OAuth olmayan kullanıcılar için şifre sıfırlama akışı hala işler

