---
title: 'SSO Kurulumu: Microsoft Entra ID'
---

Bu kılavuz, Spwig'in admin tek oturum açma (SSO) için Microsoft Entra ID (önceki adıyla Azure Active Directory) ile nasıl bağlanacağını size adım adım anlatır. Yapılandırıldıktan sonra, personeliniz Spwig admin paneline Microsoft iş hesabı kullanarak oturum açabilir.

**Not:** Microsoft, zaman içinde Entra admin merkezi arayüzünü güncelleyebilir. Bu talimatlar, 2026 başı itibarıyla arayüzün durumuna göre yazılmıştır. Eğer herhangi bir adım sizin gördüğünüzden farklıysa, Microsoft'un resmi belgelerine bakın: [Microsoft kimlik platformu ile uygulama kaydetme](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app).

## Önkoşullar

- Microsoft Entra ID erişimine sahip bir Azure aboneliği
- Entra ID kiracınızda **Uygulama Yöneticisi** veya **Genel Yönetici** rolü
- Spwig mağazanızın URL'si (örneğin, `https://your-store.com`)
- Personelinizin Spwig'deki e-posta adresleri, Microsoft hesaplarıyla eşleşmelidir

## Adım 1: Bir Uygulama Kaydetme

1. [Microsoft Entra admin merkezine](https://entra.microsoft.com) oturum açın
2. **Kimlik > Uygulamalar > Uygulama Kayıtları**'na gidin
3. **Yeni Kayıt**'a tıklayın
4. Kaydı yapılandırın:

| Alan | Değer |
|-------|-------|
| **Ad** | `Spwig Admin SSO` (veya tercih ettiğiniz herhangi bir isim) |
| **Desteklenen hesap türleri** | **Bu örgütsel dizindeki hesaplar yalnızca** (Tek kiracılı) |
| **Yönlendirme URI'si** | Platform: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. **Kaydet**'e tıklayın

**Önemli:** Yönlendirme URI'si `https://your-store.com/oidc/callback/` ile tam olarak eşleşmelidir — son eğik çizgiyi de dahil edin. `your-store.com`'ı gerçek mağaza etki alanınızla değiştirin.

## Adım 2: Uygulama Kimliklerini Not Edin

Kayıt yaptıktan sonra, uygulamanın **Genel Bakış** sayfasını göreceksiniz. Bu iki değeri not edin — bunları daha sonra kullanacaksınız:

| Değer | Nerede Bulunur | Ne İçin Kullanılır |
|-------|-----------------|---------------|
| **Uygulama (istemci) Kimliği** | Genel Bakış sayfası, üst bölüm | Spwig'de **İstemci Kimliği** olarak girilir |
| **Dizin (kiracı) Kimliği** | Genel Bakış sayfası, üst bölüm | Keşif URL'si oluşturmak için kullanılır |

## Adım 3: İstemci Gizli Anahtarını Oluşturun

1. Uygulama kaydı içinde **Sertifikalar & Gizli Anahtarlar**'a gidin
2. **Yeni İstemci Gizli Anahtarı**'na tıklayın
3. Açıklama girin (örneğin, `Spwig SSO`) ve bir sonlama süresi seçin
4. **Ekle**'ye tıklayın
5. **Değeri hemen kopyalayın** — yalnızca bir kez gösterilir. Bu, Spwig'de gireceğiniz istemci gizli anahtarıdır.

**Gizli Anahtar Kimliği'ni kopyalamayın** — ihtiyacınız olan **Değer** sütunudur, kimlik sütunu değil.

**Bir hatırlatma ayarlayın** gizli anahtarın sonlamadan önce döndürülmesi için. Bir gizli anahtar sonlandığında, SSO çalışmayı durdurur, yeni birini oluşturup Spwig'de güncellemene kadar.

## Adım 4: API İzinlerini Yapılandırın

1. **API izinleri**'ne gidin
2. **Microsoft Graph > User.Read** (delege) izinin listede olduğundan emin olun. Bu, varsayılan olarak eklenir.
3. Eğer `openid`, `email` ve `profile` izleri listede değilse, **Bir izin ekle > Microsoft Graph > Delege izinleri**'ne tıklayın ve bunları ekleyin.
4. İstenirse, **[your organization] için yönetici onayı ver**'e tıklayın.

## Adım 5: Keşif URL'sini Oluşturun

OIDC Keşif URL'si şu formattır:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

{tenant-id}'yi Adım 2'den alınan **Dizin (kiracı) Kimliği** ile değiştirin.

Örnek: kiracınızın kimliği `a1b2c3d4-e5f6-7890-abcd-ef1234567890` ise, Keşif URL'si:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## Adım 6: Grup Taleplerini Yapılandırın (Opsiyonel)

Spwig'in Entra ID grup üyeliğine göre personel veya süper kullanıcı statüsünü otomatik atamasını istiyorsanız:

1. Uygulama kaydı içinde **Token yapılandırması**'na gidin
2. **Grup talebi ekle**'ye tıklayın
3. Dahil edilecek grup türlerini seçin (genellikle **Güvenlik grupları**)
4. **Türe göre token özellikleri özelleştir** altında, **ID** token için **Grup Kimliği**'ni seçin
5. **Ekle**'ye tıklayın

**Önemli:** Entra ID, grup **Nesne Kimliklerini** (örneğin `a1b2c3d4-...` gibi UUID'leri), değil grup görüntü adlarını gönderir.

Spwig'de rol eşleme yapılandırırken bu Nesne Kimliklerini kullanmanız gerekir.

Bir grubun Nesne Kimliğini bulmak için:
1. Entra admin merkezinde **Kimlik > Gruplar > Tüm gruplar**'a gidin
2. Grubu tıklayın
3. Grubun genel bakış sayfasından **Nesne Kimliği**'ni kopyalayın

### Grup Sınırlaması

Microsoft Entra ID, token içinde en fazla **200 grup** içerir. Kullanıcının 200'den fazla gruba ait olması durumunda, grup talebi Microsoft Graph API'sine yönlendirme bağlantısı ile değiştirilir. Çok sayıda gruba sahip olan kuruluşlar için, Spwig erişimi için özel bir güvenlik grubu oluşturmayı ve [grup filtreleme](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) kullanarak hangi grupların dahil edileceğini sınırlamayı düşünün.

## Adım 7: Spwig'de Yapılandırma

1. Spwig admin panelinde **Enterprise SSO > SSO Sağlayıcı Yapılandırması**'na gidin
2. **Sağlayıcı Adı**'nı `Microsoft Entra ID` olarak ayarlayın
3. Adım 5'ten elde ettiğiniz Keşif URL'sini **OIDC Keşif URL'si**'ne yapıştırın
4. **Otomatik Keşfet**'i tıklayın — bu, tüm uç nokta alanlarını otomatik olarak doldurur
5. Adım 2'den elde ettiğiniz **Client ID**'yi girin
6. Adım 3'ten elde ettiğiniz **Client Secret** (Değer) girin
7. Adım 6'da grup taleplerini yapılandırdıysanız:
   - **Grup Talebi**'ni `groups` olarak ayarlayın
   - **Personel Grupları**'nda, personel olacak üyelerin bulunduğu grupların Nesne Kimliklerini (virgülle ayrılmış) girin
   - **Süper Kullanıcı Grupları**'nda, süper kullanıcı olacak üyelerin bulunduğu grupların Nesne Kimliklerini (virgülle ayrılmış) girin
8. **Kaydet**'e tıklayın

## Adım 8: Etkinleştir ve Test Et

1. **Site Ayarları > Güvenlik** sekmesine gidin
2. **Yönetici Girişi için SSO'yu Etkinleştir**'i işaretleyin
3. **Kaydet**'e tıklayın
4. **özel/incognito penceresinde** admin giriş sayfasını açın
5. **Microsoft Entra ID ile Giriş Yap** butonunu görmelisiniz
6. Butona tıklayın — Microsoft'un giriş sayfasına yönlendirilmelisiniz
7. Spwig'de personel kullanıcıya eşleşen bir Microsoft hesabıyla giriş yapın
8. Spwig admin paneline geri yönlendirilmelisiniz

## Yaygın Sorunlar

| Sorun | Neden | Çözüm |
|-------|-------|----------|
| **AADSTS50011: Yeniden yönlendirme URI'si eşleşmiyor** | Entra'daki yeniden yönlendirme URI'si tam olarak eşleşmiyor | Yeniden yönlendirme URI'sinin `https://your-store.com/oidc/callback/` olduğunu ve son eğik çizgiyi kontrol edin. HTTP ile HTTPS eşleşmeyi kontrol edin. |
| **AADSTS700016: Uygulama bulunamadı** | Yanlış Client ID veya kiracı | Client ID'yi ve Keşif URL'sinin doğru kiracı kimliği kullandığını tekrar kontrol edin |
| **Microsoft'da giriş başarılı ama Spwig'de başarısız** | Spwig'de eşleşen kullanıcı yok | Spwig'de Microsoft hesabıyla aynı e-posta adresine sahip bir personel hesabı olduğundan emin olun. Restrict to Staff etkinse kullanıcıya personel statüsü olduğundan emin olun. |
| **Grup talebi boş** | Grup talepleri yapılandırılmadı | Adım 6'ya göre token yapılandırmasına grup talebi ekleyin |
| **Grup talebi URL yerine ID'ler döndürüyor** | Kullanıcının 200'den fazla gruba ait olması | Token'da grupları sınırlamak için grup filtreleme kullanın veya belirli grupları atayın |
| **Birkaç ay sonra SSO çalışmayı bırakıyor** | Client secret sona erdi | Entra'da yeni bir client secret oluşturun ve Spwig SSO Sağlayıcı Yapılandırması'nda güncelleyin |

## İpuçları

- **Güvenlik gruplarını** rol eşleme için kullanın, Microsoft 365 grupları veya dağıtım listeleri yerine.

Güvenlik grupları, erişim kontrolü için tasarlanmıştır ve OIDC talepleriyle en iyi şekilde çalışır.
- **Tek kiracı önerilir** — "Bu örgütsel dizindeki hesaplar" seçeneği, SSO'yu sadece kuruluşunuzun kullanıcılarına sınırlar.

Çok kiracılı yapılandırmalar ek validation gerektirir.
- **Uzun bir gizli anahtar süresi ayarlayın** — client secret oluştururken 24 ay seçin ve 22 ayda bir gizli anahtar döndürme için takvim hatırlatıcısı ayarlayın.
- **Koşullu erişim** — Entra ID'de Spwig uygulama kaydı için özel koşullu erişim ilkeleri oluşturabilirsiniz.

Örneğin, MFA gerekli olabilir, güvenilir olmayan konumlardan oturum açma işlemi engellenebilir veya uyumlu cihazlar gerekli olabilir.
- **Bir admin olmayan hesap ile test yapın** — Spwig'de test personel hesabı oluşturun ve SSO'nun tüm ekibinize uygulanmasından önce çalışıp çalışmadığını doğrulayın.