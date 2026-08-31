---
title: E-posta Teslim Edilebilirliği Çalışma Kılavuzu
---

<!-- screenshots-needed:
- url: /admin/email_system/emailaccount/add/
  filename: wizard-dns-step.webp
  description: Step 4 (DNS Configuration) of the email account setup wizard for the built-in SMTP provider, showing the SPF/DKIM/DMARC validation one-liners and the DNS provider tabs (Cloudflare/GoDaddy/Namecheap/Route 53/Other) with at least one record's "Details" panel expanded so a copyable TXT record is visible.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/email_system/emailaccount/{account_id}/change/
  filename: dkim-dns-record.webp
  description: An existing built-in SMTP EmailAccount's change form scrolled to the "DKIM keys configured" panel, showing the DNS TXT record Name/Value and the Copy DNS Record button.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: suppressed-addresses-card.webp
  description: The Campaign Studio dashboard's Suppressed addresses stat card, for the "monitor" section of this runbook.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
-->

Bir e-postanın *gönderilmesi* kolaydır. Onun spam klasörü yerine gelen kutusuna ulaşmasını sağlamak asıl işin kendisidir — ve Gmail ile Yahoo gibi posta kutusu sağlayıcıları, e-postayı değerlendirmeye başlamadan önce katı teknik gereksinimleri uygulamaktadır. Bu çalışma kılavuzu, sipariş onaylarınızın ve kampanyalarınızın müşterilerin görebileceği yere ulaşması için neyin, hangi sırayla yapılandırılacağını adım adım anlatır.

Buradaki hiçbir şey tek seferlik bir görev değildir. Teslim edilebilirlik, zamanla inşa ettiğiniz ve hızla kaybedebileceğiniz bir statüdür — sonundaki kontrol listesi, herhangi bir şey ters gittiğinde tekrar gözden geçirilmeye değer.

## Neden önemli

Tüm büyük gelen kutusu sağlayıcıları, bir e-postayı teslim etmeye, spam klasörüne katlamaya veya tamamen reddetmeye karar vermeden önce gelen postayı gönderici itibarı açısından puanlar. 2024'ten bu yana Gmail ve Yahoo, anlamlı hacimde gönderim yapan herkes için bunu açık **toplu gönderici gereksinimleri** olarak resmileştirdi:

- **Alan adınızı doğrulayın** — geçerli SPF, DKIM ve DMARC kayıtları.
- **Abonelikten çıkmayı kolaylaştırın** — her pazarlama e-postasında çalışan, düşük sürtünmeli bir opt-out seçeneği.
- **Spam şikayetlerini düşük tutun** — yaklaşık %0,3 şikayet oranını aşan toplu göndericilerin postaları tamamen reddedilebilir veya toplu klasöre atılabilir; en güvenli hedef %0,1'in çok altıdır.

Bu gereksinimleri karşılamazsanız, yalnızca pazarlama kampanyaları etkilenmez — hasarlı bir alan adı itibarı, Gmail ve Yahoo'nun itibarı giderek yalnızca mesaj türüne göre değil, gönderim alan adı düzeyinde değerlendirmesi nedeniyle, işlem e-postalarını (sipariş onayları, şifre sıfırlamaları) da spama sürükleyebilir. Aşağıdaki adımlar, bu üç gereksinimin tümünü nasıl karşılayacağınızı gösterir.

## Adım 1: Gönderim alan adınızı doğrulayın

SPF, DKIM ve DMARC, alan adınızdan geldiğini iddia eden postanın gerçekten sizin tarafınızdan gönderildiğini alan posta sunucularına kanıtlayan DNS TXT kayıtlarıdır. Bunları nasıl yapılandıracağınız, mağazanızın kullandığı gönderim moduna bağlıdır — üçü de yönetim kenar çubuğundaki **E-posta Yapılandırması** altında yapılandırılır (bu, E-posta Hesapları listesini açar; tam hesap kurulumu anlatımı için bkz. [E-posta Yapılandırması](email-configuration)).

| Gönderim modu | Kimlik doğrulama nasıl çalışır |
|---|---|
| **Yerleşik SMTP** (Spwig'in kendi e-posta sunucusu) | Spwig, alan adınız için bir DKIM anahtar çiftini otomatik olarak oluşturur. Bir e-posta hesabı eklediğinizde, kurulum sihirbazının **4. Adım**'ında SPF, DKIM ve DMARC durumunuz ile eklemeniz gereken tam kayıt, panoya kopyalama özelliği ve Cloudflare, GoDaddy, Namecheap ve AWS Route 53 için sağlayıcıya özel talimatlar gösterilir. Daha sonra hesabın kendi yönetim sayfasında, **Yapılandırılan DKIM anahtarları** altında, tekrar bulmanız gerekiyorsa aynı DKIM DNS kaydı da gösterilir. |
| **Genel SMTP** (SendGrid, Mailgun, Amazon SES veya Google Workspace gibi kendi sağlayıcınızı getirme, SMTP kimlik bilgileri üzerinden bağlanma) | Kimlik doğrulama kısmen o sağlayıcının kendi panelinde gerçekleşir. Kurulum sihirbazının DNS adımı, özellikle Gmail, Outlook, SendGrid, Mailgun ve Amazon SES için sekmeli talimatlar içerir — her biri, sağlayıcının konsolunda ne yapılandırılacağını (ör. SendGrid'de bir gönderim alan adını doğrulama) ve DNS sunucunuza hangi sonuçlanan DNS kayıtlarının eklenmesi gerektiğini açıklar. |
| **Spwig barındırmalı e-posta geçidi** | Spwig barındırmalı planlarda yönetilen bir gönderim seçeneği olarak mevcuttur. Giden postaları otomatik olarak DKIM ile imzalar ve varsayılan olarak Spwig'in kendi doğrulanmış alan adındaki bir adresten gönderim yapar, bu da sıfır kurulumla çalışmasını sağlar. Geçit üzerinden kendi alan adınızdan göndermek istiyorsanız, bunu doğrulamak için barındırma sağlayıcınızla konuşun — bu bir yönetilen hizmettir, kendi kendine hizmet veren bir DNS akışı değildir. |

Hangi modu kullanırsanız kullanın, **DNS kaydının kendisini eklemek her zaman harici bir adımdır** — bunu alan adı tescilcinizde veya DNS sunucunuzda (Cloudflare, GoDaddy, Namecheap, Route 53 veya alan adınızın isim sunucularının işaret ettiği herhangi bir yerde) yaparsınız, Spwig'in içinde değil. Spwig, tam olarak ne eklemeniz gerektiğini söyleyebilir ve canlı olduğunu doğrulayabilir, ancak tescilcinize erişip sizin için ekleyemez.

Başlamadan önce bilmeniz gereken birkaç şey:

- **DNS değişiklikleri anında gerçekleşmez.** Yayılma süresi birkaç dakikadan 48 saate kadar sürebilir. Sihirbazın doğrulama adımı, kayıt gerçekten yayılana kadar başarısız veya eksik olarak gösterir — bu beklenen bir durumdur, bir şeyin yanlış olduğunun bir işareti değildir.
- **Alan başına yalnızca bir SPF kaydı izin verilir.** Zaten bir tane varsa (Google Workspace, başka bir e-posta göndericisi vb.), yeni göndericinizi ikinci bir SPF TXT kaydı oluşturmak yerine mevcut kayda `include:` ile ekleyin — iki SPF kaydı herkes için kimlik doğrulamayı bozar.
- **DMARC'ın çalışması için SPF veya DKIM'in zaten geçmesi gerekir.** SPF ve DKIM her iki taraf da doğrulandıktan sonra son olarak yapılandırın.

## Adım 2: Gerçek bir gönderim kimliği kullanın

Alan adınız kimlik doğrulamasından geçtikten sonra, alıcıların aslında gördüğünün bunu desteklediğinden emin olun:

- **Gönderen adresi** — kendi doğrulanmış alan adınızda bir adres kullanın (`orders@yourstore.com`), asla ücretsiz bir sağlayıcı adresi kullanmayın (`yourstore@gmail.com`). Ücretsiz sağlayıcıdan gelen bir Gönderen adresi, SPF/DKIM/DMARC kayıtlarınızla hiç kimlik doğrulanamaz ve gelen kutusu sağlayıcıları bunu bir mağazadan gelen güçlü bir spam sinyali olarak değerlendirir.
- **Gönderen adı** — mağazanızın tanınabilir adını kullanın, "Bildirimler" veya "Yanıtlanmaz" gibi genel etiketler kullanmayın.
- **Yanıt** — izlenen bir adres ayarlayın. Yanıt veren veya yanıtları sessizce silen izlenmeyen bir `noreply@` adresi, kendisi hafif bir itibar sinyalidir ve müşterilerin size bir şeyin yanlış gittiğini söyleyebildiği tek kanalı engeller.

Üçünü de **E-posta Yapılandırması > (hesabınız) > Gönderen Yapılandırması** altında ayarlayın — tüm alan açıklamaları için [E-posta Yapılandırması](email-configuration) bölümüne bakın.

## Adım 3: Ölçeklendirmeden önce ısınma yapın

Gönderim geçmişi olmayan bir alan adı veya IP'nin henüz itibarı yoktur — iyi veya kötü — ve gelen kutusu sağlayıcıları bilinmeyene karşı temkinlidir. Tamamen yeni bir alan adından devasa bir ilk gönderim yapmak, istatistiksel olarak yeni bir kampanya başlatan bir spammer ile aynı görünür ve tüm teknik kutular işaretlenmiş olsa bile toplu klasöre düşmesine neden olabilir.

- Daha küçük başlayın.

İlk birkaç kampanyanızı tüm listenize bir anda göndermek yerine, en çok etkileşimde bulunan ve açma olasılığı en yüksek kitleye gönderin — hedefli bir başlangıç segmenti oluşturmak için [Kitleler](audiences) bölümüne bakın.
- İlk birkaç hafta boyunca hacmi kademeli olarak artırın, doğrudan tam liste gönderimlerine geçmeyin.
- Mevcut bir listeyi başka bir platformdan taşıyorsanız, itibar açısından bunu da birinci gün olarak kabul edin — eski platformunuzun gönderim geçmişi alan adıyla birlikte taşınmaz.

## Adım 4: Listenizi temiz tutun

Her şikayet veya geri dönüş (bounce) itibarınıza zarar verir ve her ikisi de büyük ölçüde listenizde kimlerin olduğu ve onların nasıl oraya geldiğiyle ilgilidir:

- **Yalnızca rıza gösteren kişilere e-posta gönderin.** İçe aktarılan iletişim bilgileri, satın alınan listeler ve kazınan adresler, spam şikayetlerinin ve sert geri dönüşlerin (hard bounce) hızla artmasının en hızlı yoludur.
- **Çift onay (double opt-in) kullanın.** Spwig'in pazarlama onay akışı, pazarlama e-postası göndermeden önce abonenin e-posta adresini doğrular — bunun nasıl yapılandırıldığına dair [İletişim Tercihleri](communication-preferences) bölümüne bakın.
- **Spwig'in otomatik baskılama (suppression) işlevinin çalışmasına izin verin.** Spwig, sert geri dönüşleri, spam şikayetlerini ve tekrarlayan yumuşak geri dönüşleri izler ve bu adreslere e-posta göndermeyi otomatik olarak durdurur; kurulum gerektirmez — bunun tam olarak nasıl çalıştığına ve (nadir durumlarda) nasıl devre dışı bırakılacağına dair [Liste Hijyeni ve Baskılamalar](list-hygiene) bölümüne bakın.
- **Pasif aboneleri düzenli olarak temizleyin**, aynı etkileşimsiz adreslere süresiz olarak e-posta göndermek yerine — açan ve tıklayan küçülen bir liste, açmayan ve tıklamayan büyük bir listeden itibarınız için daha değerlidir.

## Adım 5: İzleme

Teslim edilebilirlik sorunları, bir müşterinin size e-postanın ulaşmadığını söylemeden önce rakamlarda kendini gösterir.

Her gönderimden sonra bir kampanyanın [Raporunu](campaign-reports) açın ve şunları izleyin:

| Metrik | Ne aramalısınız |
|---|---|
| **Geri dönüş oranı** | Ağırlıklı olarak yumuşak geri dönüşler normaldir; artan **sert geri dönüş** oranı, listenizde eski veya geçersiz adreslerin biriktiği anlamına gelir. |
| **Spam şikayetleri** | Her gönderimde sıfıra yakın olmalıdır. Gmail ve Yahoo'da toplu gönderici yaptırımını tetikleyen yaklaşık %0,3 eşiğinin çok altında tutun — küçük bir artış bile derhal araştırılmaya değer olarak kabul edilmelidir. |
| **Açılma oranı / tıklama-açılma oranı** | Aynı listeye yapılan gönderimlerde (sadece bir kampanyada değil) ani ve açıklanamayan bir düşüş, geri dönüş veya şikayet rakamları hareket etmeden önce bile, e-postaların gelen kutusu yerine spam klasörüne düştüğünün erken bir işareti olabilir. |

Ayrıca, Campaign Studio panelindeki **Baskılanmış adresler** kartını düzenli olarak kontrol edin — sürekli az miktarda artış normal liste aşınmasıdır, ancak ani bir artış, bir sonraki gönderimden önce araştırılmaya değerdir (bkz. [Liste Hijyeni](list-hygiene)).

Bir şey artarsa: Önce DNS kayıtlarınızın hâlâ geçerli olup olmadığını kontrol edin ve duraklayın (süresi dolmuş bir alan adı yenileme veya kazara yapılan bir DNS değişikliği, SPF/DKIM'i sessizce bozabilir), ardından tetikleyici olan gönderimin içeriği veya kitlesinde ne değiştiğine bakın.

## Adım 6: İçerik hijyeni

Kimlik doğrulama ve liste kalitesi sizi kapıdan içeri sokar; içerik, orada olduğunuzda nasıl muamele göreceğinizi hâlâ etkiler.

- **Konu satırlarında spam tetikleyici kalıplardan kaçının** — BÜYÜK HARFLER, aşırı noktalama işaretleri ("!!!") ve "hemen harekete geç" veya "ücretsiz para" gibi ifadeler, kimlik doğrulanmış bir alan adından gelse bile spam filtreleri tarafından aleyhinize işler.
- **Yalnızca görsel içeren e-postalar göndermeyin.** Gerçek metin içermeyen tek bir görselden oluşan bir e-posta klasik bir spam kalıbıdır; görsellerin yanında anlamlı miktarda gerçek metin içeriği bulundurun.
- **Göndermeden önce önizleme yapın.** E-postanın tam listenize gitmeden önce, mobil cihazlarda dahil olmak üzere, nasıl göründüğünü kontrol edin.
- **Abonelikten çıkma bağlantısı zaten halledildi.** Spwig, her pazarlama e-postasının alt kısmına otomatik olarak çalışan, giriş gerektirmeyen bir abonelikten çıkma bağlantısı ekler — kendi bağlantınızı eklemenize gerek yoktur (bu akışın tam olarak nasıl çalıştığına dair [İletişim Tercihleri](communication-preferences) bölümüne bakın). Bunu kaldırmayın veya gizlemeyin; eksik veya bozuk bir abonelikten çıkma bağlantısı, diğer rakamlarınız ne olursa olsun, Gmail ve Yahoo'nun toplu gönderici kurallarına göre kendisi bir politika ihlalidir.


## "E-postalarım spam klasörüne düşüyor" — sorun giderme kontrol listesi

Bunları sırasıyla uygulayın:

1. **DNS kayıtlarınızı yeniden kontrol edin.** Hesabın kurulum sihirbazı DNS adımını (yerleşik SMTP için hesabın yönetim sayfasındaki DKIM panelini) açın ve SPF, DKIM ve DMARC'ın hâlâ geçerli olduğunu doğrulayın. Alan adı yenileme, DNS sağlayıcı göçü veya bölge dosyanıza yapılan ilgisiz bir değişiklik, bunlardan birini sessizce bozabilir.
2. **Etkilenen gönderim(ler) için kampanya raporundaki sekme ve şikayet sayılarını kontrol edin** — bkz. [Kampanya Raporları](campaign-reports). Herhangi birinde ani bir artış, kimlik doğrulama sorunundan ziyade liste kalitesi veya içerik sorununa işaret eder.
3. **Bastırma listesini** ([Liste Hijyeni](list-hygiene)) ani bir artış için kontrol edin — listenizin büyük bir kısmı bir süredir başarısız oluyorsa, kalan kısıma teslim edilebilirlik de düşer.
4. **Gönderen adresinizin kimliği doğrulanmış alan adınızda olduğunu, ücretsiz bir sağlayıcı adresinde veya SPF/DKIM/DMARC için yapılandırılanla eşleşmeyen bir alan adında olmadığını doğrulayın.**
5. **Kendinize ait bir Gmail ve bir Yahoo/Outlook adresine test e-postası gönderin** ve yalnızca ulaşıp ulaşmadığına değil, hangi klasöre düştüğüne bakın.
6. **Gönderim hacmini veya hedef kitlesini son zamanlarda keskin bir şekilde değiştirdiyseniz,** bunu taze bir ısınma süreci olarak ele alın — hacmi geri çekin ve daha kademeli olarak artırın.
7. **Yukarıdaki her şey doğruysa ve sorun devam ediyorsa,** bu bir yapılandırma hatasından ziyade sağlayıcıya özgü kısıtlama olabilir — altta yatan neden (genellikle şikayetler veya sekmeler) düzeltilene kadar kendi kendine çözülmesi biraz zaman alabilir.

## İpuçları

- Başka bir şeyi düzeltmeden önce DNS kimlik doğrulamasını düzeltin — SPF/DKIM/DMARC geçerli değilse, diğer tüm teslim edilebilirlik unsurları (içerik, liste hijyeni, ısınma) daha az önem taşır.
- Kurulum sihirbazının DNS doğrulamasını tek seferlik bir işlem olarak değil, belirli bir anlık kontrol olarak ele alın — DNS sağlayıcılarını taşıdığınızda veya alan adını farklı bir kayıtçı üzerinden yenilediğinizde her zaman yeniden çalıştırın.
- Açılıp tıklanan temiz bir liste, açılıp tıklanmayan daha büyük bir listeden her zaman daha iyi performans gösterir — "her ihtimale karşı" eski, doğrulanmamış bir listeyi içe aktarma isteğine direnin.
- Sayılarınızı genel bir sektör standardına değil, kendi geçmiş gönderimlerinize göre izleyin — kendi geçmişiniz, gerçek bir sorunun en güvenilir göstergesidir.
- Spwig barındırmalı bir planda iseniz, barındırılan e-posta ağ geçidinin DKIM imzalama ve itibar yönetimi sizin için halledilir — kalan sorumluluğunuz DNS değil, liste kalitesi ve içeriktir.