---
title: Yönetici Tek Oturum Açma (SSO)
---

Tek Oturum Açma (SSO), çalışanlarınızın admin paneline giriş yapmak için kendi organizasyonunuzun kimlik sağlayıcısını kullanmalarını sağlar. Spwig, Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak ve diğerleri gibi OpenID Connect (OIDC) protokolünü kullanan herhangi bir kimlik sağlayıcısını destekler.

## Kurumsal SSO Nedir?

Kurumsal SSO, sosyal giriş (kişisel Google veya Facebook hesabıyla giriş yapmak) ile farklıdır. Kurumsal SSO ile:

- Çalışanlar, **organizasyonunuzun kimlik sağlayıcısı** üzerinden kimlik doğrulaması yapar — bu aynı zamanda e-posta, iç araçlar ve diğer iş uygulamaları için kullandıkları sistemdir
- IT ekibiniz erişimi merkezi olarak kontrol eder — biri organizasyondan ayrılırsa, kimlik sağlayıcısında hesabını devre dışı bırakmak, Spwig erişimini hemen iptal eder
- Çok faktörlü kimlik doğrulama (MFA), kimlik sağlayıcısı tarafından zorunlu hale getirilir, bu da tüm uygulamalarda tutarlı bir güvenlik politikası sağlar
- Çalışanlar, Spwig için ayrı bir şifre hatırlamak zorunda değildir

## Nasıl Çalışır

SSO etkinleştirildiğinde, admin giriş sayfasında **[Provider] ile Oturum Aç** butonu görünür. Kimlik doğrulama akışı şu şekilde çalışır:

1. Çalışan, Spwig giriş sayfasındaki SSO butonuna tıklar
2. Microsoft giriş gibi kimlik sağlayıcınızın giriş sayfasına yönlendirilirler
3. Kimlik sağlayıcısıyla kimlik doğrulaması yaparlar (sağlayıcı tarafından gereken MFA da dahil)
4. Kimlik sağlayıcısı, Spwig'a güvenli bir yetkilendirme kodu ile yönlendirirler
5. Spwig, kodu kullanıcı bilgileriyle değiştirir ve bir oturum oluşturur
6. Çalışan, admin panelinde tamamen kimlik doğrulaması yapılmış şekilde görünür

Bu, Microsoft Entra ID, Google Workspace, Okta ve diğerleri gibi neredeyse tüm kurumsal kimlik sağlayıcıları tarafından desteklenen endüstri standardı **OpenID Connect (OIDC)** protokolünü kullanır.

## SSO'yu Etkinleştirme

SSO, iki yerde yapılandırılır:

1. **Site Ayarları > Güvenlik sekmesi** — SSO'yu etkinleştirin veya devre dışı bırakın ve şifre girişinin görünümünü kontrol edin
2. **SSO Sağlayıcı Yapılandırması** — Kimlik sağlayıcınızın OIDC ayrıntılarını girin

### Adım 1: Kimlik sağlayıcınızı yapılandırın

Spwig'de SSO'yu etkinleştirmeden önce, Spwig'ı kimlik sağlayıcınızda bir uygulama olarak kaydetmeniz gerekir. Sağlayıcıya özel kılavuzlara bakın:

- **Microsoft Entra ID** — Microsoft Entra ID kurulum kılavuzunu inceleyin
- **Google Workspace** — Google Workspace kurulum kılavuzunu inceleyin
- **Okta** — Okta kurulum kılavuzunu inceleyin
- **Diğer sağlayıcılar** — Herhangi bir OIDC uyumlu sağlayıcı çalışır. `https://your-store.com/oidc/callback/` yönlendirme URI'si ile bir web uygulaması kaydedin ve sağlayıcınızın OIDC Keşif URL'si, Client ID ve Client Secret bilgilerini sağlayıcınızın bel档lara bakarak alın.

### Adım 2: Spwig'de SSO Sağlayıcısını Yapılandırın

**SSO Sağlayıcı Yapılandırması** sayfasına gidin (Güvenlik sekmesinden bağlantılı veya admin yan çubuğunda **Kurumsal SSO > SSO Sağlayıcı Yapılandırması** adresinden erişilebilir). Aşağıdakileri girin:

1. **Sağlayıcı Adı** — Giriş butonunda görüntülenir (örneğin, "Microsoft Entra ID")
2. **OIDC Keşif URL'si** — Sağlayıcınızın `.well-known/openid-configuration` URL'si. **Otomatik Keşfet**'e tıklayarak uç nokta alanlarını otomatik olarak doldurabilirsiniz.
3. **Client ID** ve **Client Secret** — Kimlik sağlayıcınızın uygulama kaydı üzerinden alınan bilgiler

Client secret, şifrelenerek saklanır ve kaydedildikten sonra hiçbir zaman görüntülenmez.

### Adım 3: Site Ayarlarında SSO'yu Etkinleştirin

**Site Ayarları > Güvenlik** sekmesine gidin ve **Yönetici Girişi için SSO'yu Etkinleştir** seçeneğini işaretleyin. SSO butonu hemen admin giriş sayfasında görünür olur.

## SSO Ayarları

| Ayar | Açıklama |
|---------|-------------|
| **Yönetici Girişi için SSO'yu Etkinleştir** | Yönetici giriş sayfasında SSO butonunu gösterir. Şifre girişini etkilemez, ancak aynı zamanda devre dışı bırakırsanız etkiler |
| **Yönetici Sayfasında Şifre Girişini İzin Ver** | İşaretlenmezse, şifre formu bir kapanabilir anahtarla gizlenir. Çalışanlar, varsayılan olarak yalnızca SSO butonunu görür. Şifre formu, "Yerel Hesapla Oturum Aç" butonuna tıklayarak veya giriş URL'sine `?password=1` ekleyerek hala erişilebilir |

### Giriş Sayfası Davranışı

| SSO Aktif | Şifre Girişi | Sonuç |
|-------------|---------------|--------|
| Kapalı | Açık | Sadece kullanıcı adı/şifre formu olan standart giriş sayfası |
| Açık | Açık | Üstte SSO butonu, "veya" ayırıcısı, ardından altta şifre formu |
| Açık | Kapalı | Sadece SSO butonu. Şifre formu, "Yerel hesapla oturum aç" anahtarlaması arkasında |
| Kapalı | Kapalı | Mümkün değil — SSO devre dışı bırakıldığında veya yapılandırılmadığında şifre girişi otomatik olarak yeniden etkinleştirilir |

## Kullanıcı Eşleme

Bir personel SSO ile oturum açtığında, Spwig onu mevcut bir kullanıcı hesabıyla **e-posta adresi** (küçük/küçük harfe duyarlı değil) üzerinden eşler. Kimlik sağlayıcısının taleplerinden gelen e-posta, personelin Spwig hesabındaki e-posta adresiyle eşleşmelidir.

Eşleşen bir kullanıcı bulunamazsa:

- **Kullanıcı Otomatik Oluşturma Devre Dışı Bırakıldı** (varsayılan) — oturum açma reddedilir. Önce Spwig'de eşleşen e-posta adresiyle personel hesabını oluşturmanız gerekir.
- **Kullanıcı Otomatik Oluşturma Etkin** — kimlik sağlayıcısının taleplerinden gelen isim ve e-posta ile otomatik olarak yeni bir kullanıcı hesabı oluşturulur.

**Personel'e Sınırla** ayarı (varsayılan olarak etkin) ek bir kontrol ekler: kullanıcı hesabı varsa bile, kullanıcıya personel statüsü verilmedikçe oturum açma reddedilir. Bu, personel olmayan hesapların SSO ile admin paneline erişmesini önler.

## Rol Haritalama

Kimlik sağlayıcınız OIDC taleplerinde grup üyeliği bilgisi gönderiyorsa, Spwig grup üyeliğine göre personel ve süper kullanıcı statüsünü otomatik olarak ayarlayabilir.

Rol haritalamayı yapılandırmak için:

1. SSO Sağlayıcı Yapılandırması'nda, **Grup Talebi** alanını sağlayıcınızın kullandığı talep adı olarak ayarlayın (varsayılan: `groups`)
2. **Personel Grupları**'nda, virgülle ayrılmış grup isimlerini veya kimliklerini girin. Bu gruplardan herhangi birinde olan kullanıcılar personel statüsü alır.
3. **Süper Kullanıcı Grupları**'nda, virgülle ayrılmış grup isimlerini veya kimliklerini girin. Bu gruplardan herhangi birinde olan kullanıcılar süper kullanıcı statüsü alır.

Rol haritalaması, kullanıcı SSO ile her oturum açtığında değerlendirilir. Kimlik sağlayıcısından bir kullanıcı bir gruptan kaldırılırsa, bir sonraki SSO oturumunda onun personel veya süper kullanıcı statüsü güncellenir.

**Önemli:** Microsoft Entra ID, varsayılan olarak grup **Nesne Kimlikleri** (UUID'ler) gönderir, grup isimleri değil. Rol haritalaması yapılandırırken Azure portal'dan Nesne Kimliğini kopyalayın. Okta gibi diğer sağlayıcılar genellikle grup isimlerini gönderir.

## Talep Haritalama

Spwig, kullanıcı bilgilerini standart OIDC taleplerinden okur. Varsayılanlar çoğu sağlayıcıyla çalışır, ancak SSO Sağlayıcı Yapılandırması'nda talep alan isimlerini özelleştirebilirsiniz:

| Ayar | Varsayılan | Açıklama |
|---------|---------|-------------|
| **E-posta Talebi** | `email` | Kullanıcının e-posta adresini içeren talep |
| **İsim Talebi** | `given_name` | Kullanıcının adını içeren talep |
| **Soyisim Talebi** | `family_name` | Kullanıcının soyismini içeren talep |
| **Grup Talebi** | `groups` | Grup üyeliğini içeren talep (boş bırakılırsa rol haritalaması devre dışı bırakılır) |

## MFA Davranışı

Bir personel SSO ile oturum açtığında, Spwig'ın yerleşik iki faktörlü kimlik doğrulama (2FA) gerekliliği otomatik olarak atlanır. Bu, kimlik sağlayıcısının SSO oturum açma akışının bir parçası olarak MFA'yi zorlamakla yükümlü olması nedeniyledir.

Şirketiniz MFA gerektiriyorsa, bunu kimlik sağlayıcınızın koşullu erişim politikalarında yapılandırın, Spwig'ın 2FA ayarlarında değil. Bu, tüm uygulamalarınız için merkezi MFA yönetimi sağlar.

## Kurtarma Erişimi

Kimlik sağlayıcınızda kesinti veya yapılandırma hatası oluşursa, hâlâ admin giriş formuna erişebilirsiniz:

- **Anahtarlayıcıyı tıklayın** — Şifre girişi devre dışı bırakılmışsa, giriş sayfasında "Yerel hesapla oturum aç" butonuna tıklayarak şifre formunu gösterin
- **URL parametresi** — Admin giriş URL'sine `?password=1` ekleyin (örneğin, `https://your-store.com/en/admin/login/?password=1`) ve şifre formunu doğrudan gösterin
- **Şifre girişi her zaman mevcuttur** — Arayüzden gizlense bile, şifre kimlik doğrulama arka planı etkin kalır. Sadece formun görünürlüğü etkilenir.

Spwig, SSO hem etkin hem de düzgün şekilde yapılandırılmışsa olmazsa olmaz parola oturumu devre dışı bırakmanı engeller — kendi kendine kilitlenme riskine karşı korur.

## Desteklenen Sağlayıcılar

Spwig, OpenID Connect (OIDC) protokolünü destekleyen herhangi bir kimlik sağlayıcısıyla çalışır. Aşağıdakiler için ayrıntılı kurulum kılavuzları mevcuttur:

- **Microsoft Entra ID** (önceki adıyla Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

Diğer OIDC uyumlu sağlayıcılar (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud vb.) için Spwig yapılandırma adımları aynıdır — sağlayıcının OIDC Keşif URL'si, Client ID ve Client Secret'e ihtiyacınız vardır. Bu kimlik bilgilerini almak için sağlayıcınızın belgelerini inceleyin. Kullanmanız gereken yönlendirme URI'si her zaman `https://your-store.com/oidc/callback/` olur.

## İpuçları

- **Parola oturumu ile başlayın** — Parola oturumunu etkinleştirmeyi SSO ile birlikte başlatın. SSO'nun ekibiniz için işe yaradığını doğruladığınızda, parola oturumunu isteğe bağlı olarak devre dışı bırakabilirsiniz.
- **Gizli pencere ile test edin** — Mevcut yönetici oturumunuzun etkisinden kurtulmak için özel/gizli bir tarayıcı penceresi kullanarak SSO testi yapın.
- **Önce personel hesaplarını oluşturun** — Otomatik Kullanıcı Oluşturma özelliğini etkinleştirmedikçe, personel üyeleri SSO ile oturum açmadan önce eşleşen bir e-posta adresiyle bir Spwig hesabıya ihtiyaç duyarlar.
- **Otomatik Keşfet butonunu kullanın** — Sağlayıcınızın OIDC Keşif URL'sini girin ve Otomatik Keşfet'e tıklayarak tüm uç nokta alanlarını otomatik olarak doldurun. Bu, uç noktaları elle girmekten daha hızlı ve hata yapmaya daha az meyilli bir yöntemdir.
- **Yerel yönetici hesabı tutun** — Kimlik sağlayıcısı sorunları durumunda geri dönüş seçeneği olarak en az bir yerel yönetici hesabıyla birlikte parola kullanın.
- **Müşteri gizli anahtarın son kullanım tarihini izleyin** — Bazı sağlayıcılar (özellikle Microsoft Entra ID), müşteri gizli anahtarlarını son kullanma tarihleriyle verir. Anahtarın son kullanma tarihi yaklaşmadan önce değiştirilmesi için takvimde bir hatırlatıcı ayarlayın.