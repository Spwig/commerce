---
title: 'SSO Kurulumu: Okta'
---

Bu kılavuz, Spwig'in admin tek oturum açma (SSO) için Okta ile nasıl bağlanacağını size adım adım anlatır. Yapılandırıldıktan sonra, personeliniz Spwig admin paneline Okta hesaplarını kullanarak oturum açabilir.

**Not:** Okta, zaman içinde admin konsol arayüzlerini güncelleyebilir. Bu talimatlar, 2026 başı itibarıyla Okta admin konsoluna dayanarak yazılmıştır. Eğer herhangi bir adım sizin gördüğünüzden farklıysa, Okta'nın resmi belgelerine bakın: [OIDC uygulama entegrasyonu oluşturma](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/).

## Önkoşullar

- Bir Okta organizasyonu (herhangi bir seviye — test için ücretsiz geliştirici hesaplar çalışır)
- Okta'da **Super Administrator** veya **Application Administrator** rolü
- Spwig mağazanızın URL'si (örneğin, `https://your-store.com`)
- Personelinizin Spwig'de Okta hesaplarıyla eşleşen e-posta adresleri olmalıdır

## Adım 1: Bir Uygulama Oluşturun

1. [Okta Admin Konsolu](https://your-org-admin.okta.com)\'ye oturum açın
2. **Uygulamalar > Uygulamalar** bölümüne gidin
3. **Uygulama Entegrasyonu Oluştur**\'a tıklayın
4. Aşağıdakileri seçin:

| Alan | Değer |
|-------|-------|
| **Oturum açma yöntemi** | OIDC - OpenID Connect |
| **Uygulama türü** | Web Uygulaması |

5. **İleri**\'ye tıklayın

## Adım 2: Uygulamayı Yapılandırın

Uygulama ayarlarını doldurun:

| Alan | Değer |
|-------|-------|
| **Uygulama entegrasyonu adı** | `Spwig Admin SSO` (veya tercih ettiğiniz herhangi bir isim) |
| **İzin türü** | Yetkilendirme Kodu (varsayılan olarak seçili olmalıdır) |
| **Oturum açma yönlendirme URI\'leri** | `https://your-store.com/oidc/callback/` |
| **Oturum kapatma yönlendirme URI\'leri** | `https://your-store.com/en/admin/login/` |
| **Kontrol edilen erişim** | İhtiyacınıza göre seçin (aşağıdaki bilgileri görün) |

**Kontrol edilen erişim** için şu seçeneklerden birini seçin:

- **Organizasyonunuzdaki herkesin erişimine izin ver** — tüm Okta kullanıcıları oturum açabilir (Spwig erişimini "Personel'e Sınırla

İlgili **İddia Ekle**'ye tıklayın
5.

İddiyayı yapılandırın:

| Alan | Değer |
|-------|-------|
| **Ad** | `groups` |
| **Token türüne dahil et** | ID Token, Her Zaman |
| **Değer türü** | Gruplar |
| **Filtre** | Regex ile eşleşir: `.*` (tüm grupları dahil etmek için) |
| **Dahil edilecek** | Herhangi bir kapsam (veya `openid` sınırlamak isterseniz) |

6. **Oluştur**'a tıklayın

**İpucu:** Microsoft Entra ID, Nesne Kimlikleri gönderirken, Okta varsayılan olarak **grup adlarını** gönderir. Bu, rol eşleme işlemini daha mantıklı hale getirir — Spwig'in Personel Grupları ve Süper Kullanıcı Grupları alanlarında doğrudan Okta gruplarınızın görüntü adlarını kullanabilirsiniz.

### Grupları Filtreleme

Kullanıcılarınız birçok Okta grubuna aitse ve token içinde yalnızca belirli olanları dahil etmek istiyorsanız:

- `.*` filtresini daha spesifik bir regex'e değiştirin, örneğin `^Spwig.*` sadece "Spwig" ile başlayan grupları dahil etmek için
- Ya da regex yerine **Başlar**, **Eşit** veya **İçerir** filtrelerini kullanın

## Adım 7: Spwig'de Yapılandırma

1. Spwig admin panelinde **Enterprise SSO > SSO Sağlayıcı Yapılandırması**'na gidin
2. **Sağlayıcı Adı**'nı `Okta` olarak ayarlayın
3. Adım 4'ten alınan Keşif URL'sini girin
4. **Otomatik Keşfet**'e tıklayın — bu, tüm uç nokta alanlarını otomatik olarak doldurur
5. Adım 3'ten alınan **Client ID**'yi girin
6. Adım 3'ten alınan **Client Secret**'i girin
7. Eğer Adım 6'da grup iddialarını yapılandırdıysanız:
   - **Groups Claim**'i `groups` olarak ayarlayın
   - **Personel Grupları**'nda, personel olacak üyelerin bulunduğu Okta gruplarının adlarını girin (virgülle ayrılmış)
   - **Süper Kullanıcı Grupları**'nda, süper kullanıcı olacak üyelerin bulunduğu Okta gruplarının adlarını girin (virgülle ayrılmış)
8. **Kaydet**'e tıklayın

## Adım 8: Etkinleştir ve Test Et

1. **Site Ayarları > Güvenlik** sekmesine gidin
2. **Yönetici Girişi için SSO'yu Etkinleştir**'i işaretleyin
3. **Kaydet**'e tıklayın
4. **özel/incognito penceresinde** admin giriş sayfasını açın
5. **Okta ile Giriş Yap** butonunu görmelisiniz
6. Tıklayın — Okta'nın giriş sayfasına yönlendirilmelisiniz
7. Spwig'de bir personel kullanıcıya eşleşen e-posta adresine sahip olan bir Okta hesabıyla giriş yapın
8. Spwig admin paneline geri yönlendirilmelisiniz

## Yaygın Sorunlar

| Sorun | Neden | Çözüm |
|---------|-------|----------|
| **Yönlendirme URI'si izin verilmiyor** | Yönlendirme URI'si uygulama yapılandırmasıyla eşleşmiyor | Yönlendirme URI'sinin tam olarak `https://your-store.com/oidc/callback/` olduğunu kontrol edin, son eğik çizgiyi unutmayın |
| **Kullanıcı, istemci uygulamasına atanmamış** | Kullanıcı, Okta uygulamasına atanmamış | Kullanıcıyı veya grubunu Uygulama Atamaları sekmesinde uygulamaya atayın |
| **Okta'da giriş başarılı ama Spwig'de başarısız** | Spwig'de eşleşen bir kullanıcı yok | Spwig'de aynı e-posta adresine sahip bir personel hesabı olduğundan emin olun. "Yalnızca Personel'e Sınırla" ayarını kontrol edin |
| **Groups iddiası boş** | Groups iddiası yetkilendirme sunucusunda yapılandırılmadı | Adım 6'ya göre groups iddiası ekleyin. Doğru yetkilendirme sunucusuna eklediğinizden emin olun |
| **Yanlış yetkilendirme sunucusu** | Keşif URL'si, groups iddiasının yapılandırıldığı yetkilendirme sunucusuyla farklı |
| **"Verilen client_id geçersiz"** | Client ID eşleşmiyor veya uygulama etkin değil | Client ID'in doğru olduğundan ve Okta'da uygulama durumunun Aktif olduğundan emin olun |

## İpuçları

- **Okta, grup adları değil ID'ler gönderir** — bu, rol eşleme işlemini daha basitleştirir.

Spwig'in Personel Grupları veya Süper Kullanıcı Grupları alanlarına tam olarak grup görüntü adlarını girin (örneğin, `Spwig Admins`).
- **Erişim kontrolü için grup ataması kullanın** — Spwig uygulamasına tüm kullanıcıları değil, belirli Okta gruplarını atayın.

# SSO Ayarları

Bu şekilde, yalnızca amaçlanan personel oturum açabilir.
- **Okta istemci gizli anahtarları varsayılan olarak sona ermeyebilir** — ancak güvenlik en iyi uygulamalar için uygulamanın Genel sekmesinden herhangi bir zaman döndürebilirsiniz.
- **Bir admin olmayan hesapla test edin** — uygulamaya atanan bir Okta kullanıcı (super admin olmayan) kullanarak SSO'nun beklenen şekilde çalışıp çalışmadığını doğrulayın.
- **Okta'daki MFA** — Okta'nın küresel oturum ilkesini veya kimlik doğrulama ilkelerini MFA gerekli hale getirmek için yapılandırın.

Bu, Spwig'de MFA'yı ayrı olarak yapılandırmadan Spwig'a yapılan tüm SSO oturumlarına uygulanacaktır.