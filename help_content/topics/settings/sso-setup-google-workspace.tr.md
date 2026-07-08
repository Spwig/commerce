---
title: 'SSO Setup: Google Workspace'
---

SSO Kurulumu: Google Workspace

Bu kılavuz, Spwig'in admin tek oturum açma (SSO) için Google Workspace'e bağlanmasını sağlar. Yapılandırıldıktan sonra, personeliniz Spwig admin paneline Google Workspace hesaplarını kullanarak oturum açabilir.

**Not:** Google zaman içinde Cloud Console arayüzünü güncelleyebilir. Bu talimatlar, 2026 başı itibarıyla arayüz temel alınarak yazılmıştır. Eğer herhangi bir adım gördüğünüzden farklıysa, Google'ın resmi belgelerine bakın: [OAuth 2.0 ayarlama](https://support.google.com/cloud/answer/6158849).

## Önkoşullar

- Google Workspace aboneliği (Google Workspace Business, Enterprise veya Education)
- [Google Cloud Console](https://console.cloud.google.com) üzerinde yönetici erişimi
- Spwig mağazanızın URL'si (örneğin, `https://your-store.com`)
- Personelinizin Spwig'de Google Workspace hesaplarıyla eşleşen e-posta adresleri olmalıdır

## Adım 1: Google Cloud Projesi Oluşturun veya Seçin

1. [Google Cloud Console](https://console.cloud.google.com) adresine gidin
2. Üst çubukta proje seçiciyi tıklayın
3. **Yeni Proje**'yi tıklayın (veya mevcut bir proje seçmek isterseniz)
4. Bir proje adı girin (örneğin, `Spwig SSO`)
5. Kuruluşunuzu seçin
6. **Oluştur**'u tıklayın

## Adım 2: OAuth Onay Ekranını Yapılandırın

1. Cloud Console'da **APIs & Services > OAuth onay ekranı**'na gidin
2. Kullanıcı türü olarak **Internal**'i seçin — bu, oturum açmayı Google Workspace kuruluşunuzdaki kullanıcılarla sınırlar
3. **Oluştur**'u tıklayın
4. Gerekli alanları doldurun:

| Alan | Değer |
|-------|-------|
| **Uygulama adı** | `Spwig Admin` (veya mağazanızın adı) |
| **Kullanıcı destek e-postası** | Yönetici e-posta adresiniz |
| **Yetkili alanlar** | `your-store.com` (mağazanızın domaini, `https://` olmadan) |
| **Geliştirici iletişim e-postası** | Yönetici e-posta adresiniz |

5. **Kaydet ve Devam Et**'i tıklayın
6. **Kapsamlar** sayfasında, **Kapsam Ekle veya Kaldır**'ı tıklayın ve şu kapsamları ekleyin:
   - `openid`
   - `email`
   - `profile`
7. **Kaydet ve Devam Et**'i tıklayın
8. Özetleri inceleyin ve **Gösterge Tablosuna Geri Dön**'e tıklayın

## Adım 3: OAuth Kimlik Bilgileri Oluşturun

1. **APIs & Services > Kimlik Bilgileri**'ne gidin
2. **Kimlik Bilgileri Oluştur > OAuth istemci Kimliği**'ni tıklayın
3. İstemciyi yapılandırın:

| Alan | Değer |
|-------|-------|
| **Uygulama türü** | Web uygulaması |
| **Ad** | `Spwig SSO` |
| **Yetkili yönlendirme URI'leri** | `https://your-store.com/oidc/callback/` |

4. **Oluştur**'u tıklayın
5. **İstemci Kimliği** ve **İstemci Gizli** değerleri gösteren bir iletişim kutusu görüntülenir — her iki değeri de kopyalayın. Ayrıca, JSON olarak indirerek güvenli bir şekilde saklayabilirsiniz.

**Önemli:** Yönlendirme URI'si `https://your-store.com/oidc/callback/` ile tam olarak eşleşmelidir — son eğik çizgi ve `https://` şeması da dahil. `your-store.com`'ı gerçek mağaza domaininizle değiştirin.

## Adım 4: Keşif URL'sini Alın

Google, tüm Workspace kiracıları için tek bir standart Keşif URL'si kullanır:

```
https://accounts.google.com/.well-known/openid-configuration
```

Bu URL, her Google Workspace kuruluşu için aynıdır — kiracı veya domain ile özelleştirmenize gerek yoktur.

## Adım 5: Spwig'de Yapılandırın

1. Spwig admin panelinde **Enterprise SSO > SSO Sağlayıcı Yapılandırması**'na gidin
2. **Sağlayıcı Adı**'nı `Google Workspace` olarak ayarlayın
3. Keşif URL'sini girin: `https://accounts.google.com/.well-known/openid-configuration`
4. **Otomatik Keşif**'i tıklayın — bu, tüm uç nokta alanlarını otomatik olarak doldurur
5. Adım 3'ten **İstemci Kimliği**'ni girin
6. Adım 3'ten **İstemci Gizli**'yi girin
7. **Kaydet**'i tıklayın

### Talep Haritalama

Google, standart OIDC talep isimlerini kullanır, bu nedenle Spwig'in varsayılan yapılandırması doğrudan çalışır:

| Spwig Ayarı | Google Talebi | Varsayılan Değer |
|---------------|-------------|---------------|
| E-posta Talebi | `email` | `email` |
| İsim Talebi | `given_name` | `given_name` |
| Soyisim Talebi | `family_name` | `family_name` |

Talep haritalamaya herhangi bir değişiklik gerekmez.

## Adım 6: Etkinleştir ve Test Et

1.

**Site Ayarları > Güvenlik** sekmesine gidin
2.

**Yönetici oturum açma için SSO'yu Etkinleştir**'i işaretleyin
3.

**Kaydet**'i tıklayın
4.



Admin oturum açma sayfasını **özel/gizli pencere** olarak açın
5.

**Google Workspace ile Oturum Aç** butonunu görmelisiniz
6.

Tıklayın — Google'un oturum açma sayfasına yönlendirilmelisiniz
7.

Spwig'de bir personel kullanıcısıyla eşleşen bir Google Workspace hesabıyla oturum açın
8.

Spwig admin paneline geri yönlendirilmelisiniz

## Grup Tabanlı Rol Haritalama

Microsoft Entra ID veya Okta'dan farklı olarak, Google, standart OIDC token'larında grup üyeliğini varsayılan olarak içermez. Google'da grup taleplerini uygulamak için Google Workspace Directory API'si ve temel OIDC'ten farklı ek yapılandırma gerekir.

Çoğu Google Workspace dağıtımında, Spwig'de otomatik rol haritalaması yerine doğrudan Spwig'de personel ve süper kullanıcı durumunu yönetmeyi öneririz:

1. Spwig'de uygun izinlerle personel hesaplarını oluşturun
2. Spwig'in Personel Roller sistemiyle erişim düzeylerini kontrol edin
3. Personel SSO ile oturum açar ve Spwig mevcut izinlerini kullanır

Grup tabanlı otomatik rol haritalaması gerekirse, özel talepleri yapılandırmak için [Google Workspace Admin SDK Directory API belgelerini](https://developers.google.com/admin-sdk/directory) inceleyin.

## Yaygın Sorunlar

| Sorun | Neden | Çözüm |
|---------|-------|----------|
| **Hata 400: redirect_uri_mismatch** | Google Cloud'daki yeniden yönlendirme URI'si tam olarak eşleşmiyor | Yeniden yönlendirme URI'sinin `https://your-store.com/oidc/callback/` olduğunu ve son eğik çizgiyi kontrol edin. HTTP ile HTTPS'yi kontrol edin. |
| **Hata 403: access_denied** | Kullanıcı Google Workspace organizasyonunda değil | "Internal" kullanıcı türüyle sadece organizasyonunuzdaki kullanıcılar oturum açabilir. Kullanıcının hesabı, Workspace etki alanınızın bir parçası olduğundan emin olun. |
| **OAuth onay ekranı "Bu uygulama doğrulanmamış" yazıyor** | İçerik uygulamalar için normaldir | Bu uyarı, İçerik uygulamalar için beklenen bir uyarıdır ve işlevselliği etkilemez. Organizasyonunuzdaki kullanıcılar hala oturum açabilir. |
| **Google'da oturum açma başarılı ama Spwig'da başarısız** | Spwig'de eşleşen kullanıcı yok | Spwig'de Google Workspace hesabına eş olan bir personel hesabı olduğundan emin olun. "Yalnızca Personel'e Sınırla" doğru yapılandırıldığından emin olun. |
| **"Erişim engellendi: Bu uygulamanın isteği geçersiz"** | Kapsamlar düzgün şekilde yapılandırılmadı | `openid`, `email` ve `profile` kapsamlarının OAuth onay ekranına eklendiğinden emin olun. |

## İpuçları

- **"Internal" kullanıcı türünü kullanın** — bu, oturum açmayı Google Workspace organizasyonunuza kısıtlayacak ve Google'ın uygulama doğrulama sürecini gerektirmeyecektir.
- **Google istemci gizli anahtarları süresizdir** — Microsoft Entra ID'den farklı olarak, Google OAuth istemci gizli anahtarları bir son kullanma tarihi yoktur. Ancak, Kimlik Bilgileri sayfasından herhangi bir zaman diliminde döndürebilirsiniz.
- **Bir projeyi birden fazla uygulama için kullanın** — birden fazla Spwig kurulumunuz varsa, aynı Google Cloud projesi içinde birden fazla OAuth istemci Kimliği oluşturabilirsiniz.
- **Bir yönetici hesabı olmadan test edin** — Spwig'de test personel hesabı oluşturun ve bir normal Google Workspace kullanıcı (süper yönetici değil) kullanarak SSO'nun beklenen şekilde çalışıp çalışmadığını doğrulayın.