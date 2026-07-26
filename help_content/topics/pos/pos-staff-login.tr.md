---
title: POS Personel Girişi & Biyometrik Giriş
---

Her POS kasasında müşteri hizmeti gören kişiye uygun izinlerle bir personel hesabı gerekir. Bu konu, bu hesabı nasıl oluşturacağınızı, personeli bir terminalle ilişkilendireceğinizi ve ardından onların her girişte şifre yerine parmak izi, yüz tarifi veya donanım anahtarını kullanarak kasayı kilitleyebilmeleri için biyometrik giriş nasıl ayarlanacağını açıklar.

PIN kodları, indirim sınırları ve terminal kilitleme ayarları için [POS Personel İndirimleri & Terminal Güvenliği](pos-staff-discounts) bölümüne bakın.

## Bir personelin POS terminalini kullanabilmesi için gerekenler

POS terminaline giriş yapmak için bir kişiye şunlara ihtiyacı vardır:

1. **Personel hesabı** — **Personel durumu** bayrağı etkin olan bir Spwig kullanıcı.
2. **POS erişimi içeren bir rol** — roller, personelin admin içinde ne yapabileceğini kontrol eder. POS izinleri içeren bir rol, kasayı erişim için gereklidir.
3. **Terminal ataması** — terminal, onu atanan personel olarak listelemelidir veya mağaza konum seviyesinde atamalıdır.

## POS elindeki personel hesabı oluşturma

**Personel & Hesaplar > Personel Üyeleri** (veya `/admin/accounts/staffmember/` adresine gidin).

1. **+ Personel Üyesi Ekle**'ye tıklayın.
2. Personelin **adını**, **soyadını** ve **e-posta adresini** doldurun.
3. Geçici bir şifre ayarlayın ve personeli ilk oturumda değiştirmesini isteyin.
4. **Personel durumu** işaretlenmiş olduğundan emin olun — bu, onların admin ve POS uygulamasına giriş yapmalarını sağlar.
5. **Kaydet**'e tıklayın.

> **Not:** Düzenli kasiyerler veya denetleyiciler için **Süper Kullanıcı durumu** işaretlenmemelidir. Süper Kullanıcı durumu tüm izin kontrollerini atlar ve mağaza sahibi için ayrılmıştır.

### POS erişimi olan bir rol atama

Personel hesapları kendi izinlerini içermez — roller özel yetkileri verir. Hesap oluşturduktan sonra, personelin kaydını açın ve **Roller** bölümüne gidin. POS erişimi içeren bir rol atayın.

Rollerin nasıl çalıştığını ve hangi izinleri içermesi gerektiğini tam olarak anlamak için [Personel Roller](staff-roles) bölümüne bakın.

<!-- ekran görüntüsü gerekli:
- url: /en/admin/accounts/staffmember/
  filename: staff-user-list.webp
  description: POS elindeki kullanıcıyı gösteren personel listesi ve rol bayrağı
-->

![Personel listesi](/static/core/admin/img/help/pos-staff-login/staff-user-list.webp)

## Personeli bir terminalle ilişkilendirme

Ayarlar kaskadı takip eder: **Site varsayılanı → Mağaza grubu → Mağaza konumu → Bireysel terminal**. Çoğu mağazada, personeli atamak için doğru yer terminal seviyesidir.

1. **POS > Terminal** (veya `/admin/pos_app/posterminal/` adresine gidin).
2. Yapılandırmak istediğiniz terminali açın.
3. **Personel Ataması** sekmesine gidin.
4. **Atanan personel** alanına girerek ve personeli ekleyerek arayın.
5. **Kaydet**'e tıklayın.

Bir terminalin **Atanan personel** listesinde görünen personeller, o terminalin giriş ekranında adlarını seçebilir. Hiçbir terminalle ilişkilendirilmemiş personeller hala e-postalarını doğrudan yazarak giriş yapabilir.

> **İpucu:** Mağazanızda birçok personelin terminal arasında döndüğü varsa, onları mağaza konumu (depo) seviyesinde atayın, terminal terminal bazında değil. Konuma atanan herhangi bir personel, o konumda bulunan tüm terminalere erişim sağlar.

## POS kasasında giriş yapma

Bir kasiyer, bir terminalde POS uygulamasını (`/pos/`) açtığında, personel seçme ekranına bakar. Giriş akışı şu şekilde çalışır:

1. Kasiyer, listede adını tıklar veya listede değilse e-postasını yazarak giriş yapar.
2. Şifresini girer.
3. Giriş yapar ve kasa, onun vardiya için açılır.

Vardiya sırasında terminal kilitlendiğinde PIN tabanlı kilitleme için [POS Personel İndirimleri & Terminal Güvenliği](pos-staff-discounts) bölümüne bakın.

## Biyometrik giriş

Biyometrik giriş, bir kasiyerin şifre yerine parmak izi sensörüne dokunması, yüz kameraına bakması veya donanım anahtarına dokunması gibi işlemleri yapmasına olanak tanır. Meşgul bir kasada bu, her vardiya başına birkaç saniye tasarruf eder ve zirve saatlerinde hataları önler.

Spwig, biyometrik giriş için **WebAuthn** tarayıcı standardını kullanır.

"WebAuthn kimlik doğrulama bilgisi", cihaza bağlı bir anahtar çiftidir: özel anahtar cihazın güvenli donanımında saklanır ve asla dışarı çıkmaz.

POS uygulaması, bu donanımı tarayıcı üzerinden iletişim kurar.

### Biyometrik girişe destek sağlayan cihazlar ve tarayıcılar

WebAuthn, uyumlu donanıma sahip cihazlarda tüm modern tarayıcılarda — Chrome, Edge, Firefox ve Safari — desteklenir. İyi çalışan yaygın yapılar:

| Cihaz | Kimlik Doğrulayıcı |
|--------|---------------|
| iPad (Touch ID) | Safari veya Chrome üzerinden parmak izi |
| Android tablet | Chrome üzerinden parmak izi veya yüz |
| Windows tableti veya PC | Windows Hello (parmak izi, yüz veya PIN) |
| Herhangi bir cihaz + güvenlik anahtarı | USB, NFC veya Bluetooth FIDO2 anahtarı (örneğin YubiKey) |
| iPhone (Face ID) | Safari üzerinden yüz |

POS uygulaması, tarayıcı ilgili cihazda mevcut kullanıcı için bir kimlik doğrulama bilgisi kayıtlı olduğunda yalnızca biyometrik giriş seçeneğini gösterir.

### Kayıt işleminin nasıl çalıştığı

Kayıt, admin'de değil POS terminalinde yapılır. Personel, önce normal bir şifre ile giriş yapmak zorundadır, ardından POS uygulaması içinde biyometrik giriş kurma seçeneğini seçmelidir. Tarayıcı, ardından cihazın biyometrik sensörü (veya iOS/macOS/Windows hesabında kaydedilmiş bir passkey) kullanarak kimliğini doğrulamalarını isteyecektir. Onaylandıktan sonra kimlik doğrulama bilgisi saklanır ve o cihazda gelecekteki seanslarda biyometrik giriş kullanılabilir.

Bir personel, birden fazla cihaza kaydolabilir — örneğin kişisel bir tablet ve paylaşılan bir kasaya — ve her cihaz kendi kimlik doğrulama bilgisini tutar.

> **Not:** Kayıt isteminin tamamı ("Biyometrik kaydet", "Parmak izi girişini ayarla" vb.) POS uygulamasından gelir ve tarayıcı ve cihaza göre değişebilir.

### Biyometrik ile giriş yapma

Kayıt yaptıktan sonra, giriş ekranındaki kasaya ismi biyometrik giriş butonu (parmak izi simgesi veya benzeri) gösterir. Kasaya:

1. Terminalin giriş ekranında ismini tıklar.
2. **Parmak izi ile giriş yap** (veya benzeri) seçeneğini tıklar.
3. Sensöre dokunur veya kameraya bakar.
4. Terminal hemen kilidini açar.

Eğer biyometrik doğrulama başarısız olursa (parmak tanınmaz, yüz kapanık), kasaya şifresini girmek zorunda kalır.

### Kimlik doğrulama bilgisini iptal etme

Eğer bir cihaz kayıp olur, çalınır veya bir personel işten ayrılırsa, onların biyometrik kimlik doğrulama bilgilerini hemen kaldırmanız gerekir.

1. **Personel & Hesaplar > Personel Üyeleri**'ne gidin.
2. Personelin kaydını açın.
3. **POS Ayarları** bölümüne kaydırın.
4. **Biyometrik Açma** satırında **Tümünü Kaldır**'a tıklayın.
5. İşlemi onaylayın.

Bu, o personel için tüm kayıtlı WebAuthn kimlik doğrulama bilgilerini her cihazda kaldırır. Ardından, herhangi bir terminalde biyometrik giriş yapmaya çalıştıklarında şifresiyle giriş yapmaları gerekir.

> **Önemli:** Burada kimlik doğrulama bilgilerini kaldırma, personelin şifresiyle giriş yapmasını engellememektedir. Erişimi tamamen iptal etmek için, aynı zamanda personel hesabını devre dışı bırakın veya terminalin atanmış personel listesinden kaldırın.

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: Personel kaydı formu, POS Ayarları bölümüne gösteren biyometrik kimlik doğrulama bilgisi sayısı ve Tümünü Kaldır butonu
-->

## Güvenlik notları

- **Kimlik doğrulama bilgileri donanıma bağlıdır.** Özel anahtar, cihazın güvenli bileşeninden asla çıkmaz.

Bir tablet hırsızlanırsa, saldırgan biyometrik anahtarı çıkaramaz — cihazın kendi kilit ekranını geçmeden tarayıcı anahtarı vermez.
- **Cihaz kaybolması şifreyi sızdırmaz.** WebAuthn, bu cihaz için şifreyi değiştirir; çalışanın şifresi ayrıdır ve etkilenmez.
- **Çalışan ayrıldığında hemen iptal edin.** Bir çalışanı çıkarma işlemi sırasında, biyometrik kimlik bilgilerini kaldırın ve çalışan hesabını aynı oturumda devre dışı bırakın.
- **Biyometrik veri asla iletilmez.** Parmak izi veya yüz taraması, cihaz donanımı tarafından tamamen işlenir.

Spwig sadece imzalı bir zorlama yanıtı alır, herhangi bir biyometrik veri değil.

## Sorun Giderme

### "Parmak iziyle oturum aç" butonu görünmüyor

Biyometrik seçenek yalnızca şu durumlarda görünür:
- Çalışan bu belirli cihazda bir kimlik bilgisi kaydetti.
- Tarayıcı WebAuthn'i destekliyor (tüm modern tarayıcılar bunu destekliyor — eski bir sürümdeyseniz güncelleyin).

Eğer buton eksikse, çalışan bu cihazda henüz kaydolmamıştır. Şifresiyle oturum açmalı ve POS uygulaması üzerinden biyometrik oturum açma işlemini ayarlmalıdır.

### Kayıt başarısız oldu

Sık karşılaşılan nedenler:
- **Tarayıcı izin verilmedi.** Tarayıcı, doğrulayıcıya erişim izni istemiş ve çalışan izin vermemiştir. Tekrar denemeli ve istek geldiğinde **İzin Ver**'i seçmelidir.
- **Uyumlu bir doğrulayıcı bulunamadı.** Cihazda parmak izi sensörü, yüz kamera veya güvenlik anahtarı yok. Cihaz donanımını kontrol edin.
- **Çift kimlik bilgisi.** Çalışan bu cihazda zaten kaydolmuş olabilir. Mevcut kimlik bilgileri, tekrar kayıt sırasında çoğaltılmasını önlemek için hariç tutulur.

### Biyometrik bir cihazda işe yararken diğerinde çalışmıyor

Her cihaz kendi kimlik bilgisini saklar. Bir iPad'de kayıt yaptırmak, ikinci bir iPad'de otomatik olarak işe yaramaz. Çalışan, kullanacağı her cihazda ayrı ayrı kayıt işlemini tamamlamalıdır.

### Çapraz cihazlı geçiş anahtarları

Bazı işletim sistemleri (iOS 16+, macOS Ventura+, Windows 11 Microsoft hesabı ile) iCloud Keychain veya Windows Hello üzerinden cihazlar arasında geçiş anahtarlarını senkronize edebilir. Eğer çalışan senkronize edilmiş bir geçiş anahtarı ile kayıt yaptıysa, bu geçiş anahtarı birden fazla cihazda otomatik olarak işe yarayabilir. Davranış işletim sistemi ve tarayıcıya bağlıdır, Spwig'a değil.

## İpuçları

- Çalışanların vardiyasına gelmeden önce, paylaşılan kayıtlar üzerinde biyometrik oturum açma işlemini ayarlayın — iki dakikalık kayıt süreci, müşterilerin beklemesi olmadan çok daha akıcıdır.
- Kasiyerler için sınırlı POS izni olan bir rol atayın ve süpervizörler için ayrı bir yönetici rolü atayın. Hesaplarını mağaza sahibi hesabıyla ayrı tutun.
- Bir çalışan yeni bir tablet veya yeni bir telefon aldıysa, önce yeni cihazda kayıt yaptırmalarını sağlayın, sonra cihaz kullanılmıyorsa admin panelinden eski kimlik bilgisini iptal edin.
- Yüksek çalışan dönüşümü olan mağazalarda, her terminalde **Atanmış çalışanlar** listesini düzenli olarak inceleyin ve konumda artık çalışan olmayan kişileri kaldırın.
- Eğer donanım güvenlik anahtarları (YubiKey veya benzeri) kullanıyorsanız, bir anahtar birden fazla terminalde kayıt yapılabilir ve admin panelinde herhangi bir değişiklik gerekmez — sadece anahtarı takın ve her terminalde kayıt işlemini tamamlayın.