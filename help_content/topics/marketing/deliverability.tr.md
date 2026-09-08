---
title: E-posta Teslim Edilebilirliği Çalışma Kılavuzu
---

Bir e-postanın *gönderilmesi* kolaydır. Onu spam klasörü yerine gelen kutusuna ulaştırmak asıl iştir — ve Gmail ile Yahoo gibi posta kutusu sağlayıcıları, bir e-postayı değerlendirmeye almadan önce artık katı teknik gereksinimleri uygulamaktadır. Bu çalışma kılavuzu, sipariş onaylarınızın ve kampanyalarınızın müşterilerin görebileceği yere ulaşması için neyin, hangi sırayla yapılandırılması gerektiğini adım adım anlatır.

Buradaki hiçbir şey tek seferlik bir görev değildir. Teslim edilebilirlik, zamanla inşa ettiğiniz ve hızla kaybedebileceğiniz bir duruştur — sonundaki kontrol listesi, her şey yolunda görünmediğinde tekrar gözden geçirilmeye değer.

## Neden önemli?

Tüm büyük gelen kutusu sağlayıcıları, bir e-postayı teslim etmeye, spam klasörüne taşımaya veya tamamen reddetmeye karar vermeden önce gelen postayı gönderici itibarı açısından puanlar. 2024'ten bu yana Gmail ve Yahoo, anlamlı hacimde gönderim yapan herkes için bunu açık **toplu gönderici gereksinimleri** olarak resmileştirdi:

- **Alan adınızı doğrulayın** — geçerli SPF, DKIM ve DMARC kayıtları.
- **Abonelikten çıkmayı kolaylaştırın** — her pazarlama e-postasında çalışan, düşük sürtünmeli bir çıkış seçeneği.
- **Spam şikayetlerini düşük tutun** — yaklaşık %0,3 şikayet oranını aşan toplu göndericilerin postaları tamamen reddedilebilir veya toplu klasöre taşınabilir; en güvenli hedef %0,1'in çok altındadır.

Bu gereksinimleri karşılamazsanız, yalnızca pazarlama kampanyaları zarar görmez — hasarlı bir alan adı itibarı, sipariş onayları ve şifre sıfırlamaları gibi işlem e-postalarını da spama taşıyabilir; çünkü Gmail ve Yahoo, itibarı giderek yalnızca mesaj türüne göre değil, gönderim alan adı düzeyinde de değerlendirmektedir. Aşağıdaki adımlar, bu üç gereksinimin tamamını nasıl karşılayacağınızı gösterir.

## Adım 1: Gönderim alan adınızı doğrulayın

SPF, DKIM ve DMARC, alan adınızdan geldiğini iddia eden postanın gerçekten sizin tarafınızdan gönderildiğini alan posta sunucularına kanıtlayan DNS TXT kayıtlarıdır. Bunları nasıl yapılandırdığınız, mağazanızın kullandığı gönderim moduna bağlıdır — üçü de yönetim kenar çubuğundaki **E-posta Yapılandırması** altında yapılandırılır (bu, E-posta Hesapları listesini açar; tam hesap kurulumu anlatımı için bkz. [E-posta Yapılandırması](email-configuration)).

| Gönderim modu | Doğrulama nasıl çalışır |
|---|---|
| **Yerleşik SMTP** (Spwig'in kendi e-posta sunucusu) | Spwig, alan adınız için bir DKIM anahtar çiftini otomatik olarak oluşturur. Bir e-posta hesabı eklediğinizde, kurulum sihirbazının **4. Adımı**, SPF, DKIM ve DMARC durumunu ve eklemeniz gereken tam kaydı, panoya kopyalama ve Cloudflare, GoDaddy, Namecheap ve AWS Route 53 için sağlayıcıya özel talimatlarla birlikte gösterir. Aynı DKIM DNS kaydı, tekrar bulmanız gerekiyorsa, daha sonra hesabın kendi yönetim sayfasında **Yapılandırılan DKIM anahtarları** altında da gösterilir. |
| **Genel SMTP** (SendGrid, Mailgun, Amazon SES veya Google Workspace gibi kendi sağlayıcınızı getirme, SMTP kimlik bilgileriyle bağlanma) | Doğrulama kısmen o sağlayıcının kendi panelinde gerçekleşir. Kurulum sihirbazının DNS adımı, Gmail, Outlook, SendGrid, Mailgun ve Amazon SES için özellikle sekmeli talimatlar içerir — her biri, sağlayıcının konsolunda neyin yapılandırılacağını (ör. SendGrid'de bir gönderim alan adını doğrulama) ve DNS anağınıza hangi sonuçlanan DNS kayıtlarının eklenmesi gerektiğini açıklar. |
| **Spwig barındırmalı posta geçidi** | Spwig barındırmalı planlarda yönetilen bir gönderim seçeneği olarak mevcuttur. Giden postayı otomatik olarak DKIM ile imzalar ve varsayılan olarak Spwig'in kendi doğrulanmış alan adındaki bir adresten gönderim yapar, bu nedenle sıfır kurulumla çalışır. Geçit üzerinden kendi alan adınızdan göndermek isterseniz, doğrulama için barındırma sağlayıcınızla konuşun — bu, kendi kendine hizmet veren bir DNS akışı değil, yönetilen bir hizmettir. |

![E-posta hesabı kurulum sihirbazının 4. adımı, SPF/DKIM/DMARC doğrulamasını, DNS sağlayıcı sekmelerini ve kopyalamaya hazır genişletilmiş bir DKIM kaydını göstermektedir](/static/core/admin/img/help/deliverability/wizard-dns-step.webp)

![Mevcut yerleşik SMTP e-posta hesabının yapılandırılan DKIM anahtarları paneli, DNS TXT kaydı ve DNS Kaydını Kopyala düğmesi ile](/static/core/admin/img/help/deliverability/dkim-dns-record.webp)

Hangi modu kullanırsanız kullanın, **DNS kaydının eklenmesi her zaman harici bir adımdır** — bunu alan adınızın kayıt kuruluşunda veya DNS sağlayıcısında (Cloudflare, GoDaddy, Namecheap, Route 53 veya alan adınızın isim sunucularının işaret ettiği herhangi bir yerde) yaparsınız, Spwig içinde değil.

Spwig, tam olarak ne eklemeniz gerektiğini söyleyebilir ve kaydın yayına girdiğini doğrulayabilir, ancak kayıt kuruluşunuza erişip sizin için ekleyemez.

Başlamadan önce bilmeniz gereken birkaç şey:

- **DNS değişiklikleri anında gerçekleşmez.** Yayılma süresi birkaç dakikadan 48 saate kadar sürebilir. Sihirbazın doğrulama adımı, kayıt gerçekten yayılana kadar başarısız veya eksik olarak gösterecektir — bu beklenen bir durumdur, bir şeyin yanlış olduğuna işaret değildir.
- **Alan başına yalnızca bir SPF kaydı izinlidir.** Zaten bir tane varsa (Google Workspace, başka bir e-posta sağlayıcısı vb.), yeni göndericinizi ikinci bir SPF TXT kaydı oluşturmak yerine `include:` ile mevcut kayda ekleyin — iki SPF kaydı, herkes için kimlik doğrulamayı bozar.
- **DMARC'ın çalışması için SPF veya DKIM'in zaten geçmesi gerekir.** Bunu, SPF ve DKIM her iki taraf da doğrulandıktan sonra, en sona kurun.

## Adım 2: Gerçek bir gönderim kimliği kullanın

Alan adınız kimlik doğrulamasından geçtikten sonra, alıcıların aslında gördüğünün bunu desteklediğinden emin olun:

- **Gönderen adresi** — kendi kimlik doğrulaması yapılmış alan adınızda bir adres kullanın (`orders@yourstore.com`), asla ücretsiz bir sağlayıcı adresi kullanmayın (`yourstore@gmail.com`). Ücretsiz sağlayıcıdan gelen bir Gönderen adresi, SPF/DKIM/DMARC kayıtlarınızla hiç kimlik doğrulanamaz ve gelen kutusu sağlayıcıları bunu bir mağazadan gelen güçlü bir spam sinyali olarak değerlendirir.
- **Gönderen adı** — genel bir etiket olan "Bildirimler" veya "Yanıt Beklenmiyor" yerine mağazanızın tanınabilir adını kullanın.
- **Yanıtla** — izlenen bir adres ayarlayın. Yanıt veren veya yanıtları sessizce silen izlenmeyen bir `noreply@` adresi, kendi başına hafif bir itibar sinyalidir ve müşterilerin size bir şeyin yanlış gittiğini bildirmesi için sahip olduğu tek kanalı engeller.

Üçünü de **E-posta Yapılandırması > (hesabınız) > Gönderen Yapılandırması** altında ayarlayın — tüm alan açıklamaları için [E-posta Yapılandırması](email-configuration) bölümüne bakın.

## Adım 3: Ölçeklendirmeden önce ısınma yapın

Gönderim geçmişi olmayan bir alan adı veya IP'nin henüz itibarı yoktur — iyi veya kötü — ve gelen kutusu sağlayıcıları bilinmeyene karşı temkinlidir. Tamamen yeni bir alandan devasa bir ilk gönderim yapmak, istatistiksel olarak yeni bir kampanya başlatan bir spammer ile aynı görünür ve tüm teknik kutular işaretlenmiş olsa bile toplu klasöre düşmesine neden olabilir.

- Daha küçük başlayın. İlk birkaç kampanyanızı, listenizin tamamına bir anda göndermek yerine, en etkileşimli ve en yüksek açılma olasılığına sahip kitleye gönderin — hedefli bir başlangıç segmenti oluşturmak için [Kitleler](audiences) bölümüne bakın.
- İlk birkaç hafta boyunca hacmi kademeli olarak artırın, doğrudan tam liste gönderimlerine atlamayın.
- Mevcut bir listeyi başka bir platformdan taşıyorsanız, itibar açısından bunu da birinci gün olarak kabul edin — eski platformunuzun gönderim geçmişi alan adıyla birlikte aktarılmaz.

## Adım 4: Listenizi temiz tutun

Her şikayet veya geri dönüş (bounce) itibarınıza mal olur ve her ikisi de büyük ölçüde listenizde kimlerin olduğu ve oraya nasıl geldikleri ile ilgilidir:

- **Yalnızca onay veren kişilere e-posta gönderin.** İçe aktarılan iletişim bilgileri, satın alınan listeler ve kazınan adresler, spam şikayetlerini ve sert geri dönüşleri en hızlı şekilde artıran yollardır.
- **Çift onay (double opt-in) kullanın.** Spwig'in pazarlama onay akışı, abonelere pazarlama e-postası göndermeden önce e-posta adreslerini doğrular — bunun nasıl yapılandırıldığı hakkında [İletişim Tercihleri](communication-preferences) bölümüne bakın.
- **Spwig'in otomatik baskılama işlevinin görevini yapmasına izin verin.** Spwig, sert geri dönüşleri, spam şikayetlerini ve tekrarlayan yumuşak geri dönüşleri izler ve bu adreslere e-posta göndermeyi otomatik olarak durdurur, kurulum gerektirmez — bunun tam olarak nasıl çalıştığı ve (nadir durumlarda) ne zaman devre dışı bırakılacağı hakkında [Liste Hijyeni ve Baskılamalar](list-hygiene) bölümüne bakın.
- **Pasif aboneleri düzenli olarak budayın**, aynı etkileşimsiz adreslere süresiz olarak e-posta göndermek yerine — açan ve tıklayan küçülen bir liste, açmayan ve tıklamayan büyük bir listeden itibarınız için daha değerlidir.

## Adım 5: İzleyin

Teslimat sorunları, bir müşteri size bir e-postanın ulaşmadığını söylemeden önce sayısal olarak ortaya çıkar.

Her gönderiden sonra bir kampanyanın [Rapor](campaign-reports) 'u açın ve şunları izleyin:

| Ölçüm | Ne dikkat etmelisiniz |
|---|---|
| **Yankı oranı** | Genellikle yumuşak yankılar normaldir; artan **sert yankı** oranı, listende eski veya geçersiz adreslerin biriktiğini gösterir. |
| **Spam şikâyetleri** | Her gönderide sıfıra yakın olmalıdır. Gmail ve Yahoo için toplu gönderenlerin uyguladığı yaklaşık %0,3' lük eşiğin altında olmasına dikkat edin - hatta küçük bir artışın da hemen incelenmesi gerekir. |
| **Açma oranı / tıklama oranları** | Aynı listeye gönderilenler arasında, yalnızca bir kampanya değil, tüm gönderimlerde beklenmedik bir düşüş, yankı veya şikâyet sayılarının değişmesinden önce, postanın kutuya değil spam kutusuna atıldığının erken bir işaretidir. |

Ayrıca kampanya oluşturma aracının **Saklı Adresler** kartını düzenli aralıklarla kontrol edin - sabit bir şekilde azalma normaldir, ancak bir sonraki gönderiden önce incelemek için bir anda patlama olursa, [Liste Temizliği](list-hygiene) 'e bakın.

![Kamuya açık Adresler istatistik kartı](/static/core/admin/img/help/deliverability/suppressed-addresses-card.webp)

Bir şey patlarsa: önce DNS kayıtlarınızın hâlâ geçerli olduğundan emin olun (bir domainin süresinin dolması veya yanlışlıkla DNS değişikliği yapmak, SPF/DKIM 'i sessizce bozabilir), ardından bu patlamayı tetikleyen gönderinin içeriği veya hedef kitlesinde ne değişiklikler olduğunu inceleyin.

## Adım 6: İçerik Temizliği

Kimlik doğrulama ve liste kalitesi sizi kapıya getirir; orada iken neye göre davrandığınızı içeriğiniz etkiler.

- **Spam tetikleyici desenleri** konu başlıklarında - Bütün büyük harfler, fazla noktalama işareti ("!!!"), ve "şimdi harekete geçin" veya "ücretsiz para" gibi ifadeler, kimlik doğrulanmış bir domain'den olsalar bile spam filtreleri için size karşı olumsuz etkiye sahiptir.
- **Sadece resim içeren e-postalar göndermeyin.** Tek bir resim ve gerçek metin olmayan bir e-posta, klasik bir spam desenidir; herhangi bir resimle birlikte anlamlı miktarda gerçek metin içermesini sağlayın.
- **Göndermeden önce önizleme yapın.** E-postanın ne kadar renderladığını, mobil cihazlarda da dahil olmak üzere, listene tamamen göndermeden önce kontrol edin.
- **İptal etme bağlantısı zaten işlenmiş.** Spwig, her pazarlama e-postasının altına giriş yapmadan önce çalışır bir iptal etme bağlantısı otomatik olarak ekler - kendi bağlantınızı eklemenize gerek yok (bu akışın nasıl çalıştığını tam olarak öğrenmek için [İletişim Tercihleri](communication-preferences) 'ne bakın). Onu kaldırma veya gizleme; eksik ya da bozuk bir iptal etme bağlantısı, Gmail ve Yahoo'nun toplu gönderen kuralları açısından kendi diğer sayılarınızdan bağımsız olarak bir politika ihlalidir.

## "E-postalarım spam atıyor" - sorun giderme kontrol listesi

İşlerini sırayla yap:

1. **DNS kayıtlarınızı tekrar kontrol edin.** Hesabın DNS adımı (ya da SMTP için yerleşik panel) 'i açın ve SPF, DKIM ve DMARC 'ın hepsinin hâlâ geçerli olduğunu onaylayın.

Bir domain yenilemesi, bir DNS sağlayıcısına geçiş veya zone dosyanızdaki ilgisiz bir değişiklik, bunlardan birini sessizce bozabilir.
2. **Etkilenen gönderiler için kampanya raporunun yankı ve şikayet sayılarını** kontrol edin - [Kamuya açık Raporlar](campaign-reports) 'a bakın.

Herhangi birinde yaşanan ani artış, kimlik doğrulama sorunundan çok liste kalitesi veya içerik sorununa işaret eder.
3. **Bastırma (Suppressions) listesini** ([Liste Hijyeni](list-hygiene)) kontrol edin — listenizin büyük bir bölümü uzun süredir başarısız oluyorsa, kalan kısıma teslim edilebilirlik de düşer.
4. **Gönderen (From) adresinizin, kimlik doğrulaması yapılmış alan adınızda olduğunu** doğrulayın; ücretsiz bir sağlayıcı adresi veya SPF/DKIM/DMARC yapılandırmasıyla eşleşmeyen bir alan adı kullanmayın.
5. **Kendinize ait bir Gmail ve bir Yahoo/Outlook adresine test e-postası gönderin** ve yalnızca ulaşıp ulaşmadığına değil, hangi klasöre düştüğüne bakın.
6. **Gönderim hacminizi veya hedef kitlenizi son zamanlarda keskin bir şekilde değiştirdiyseniz,** bunu taze bir ısınma süreci olarak ele alın — hacmi geri çekin ve daha kademeli olarak artırın.
7. **Yukarıdaki her şey doğruysa ve sorun devam ediyorsa,** bu, yapılandırmanızdaki bir arızadan çok sağlayıcıya özgü bir kısıtlama (throttling) olabilir — altta yatan neden (genellikle şikayetler veya geri dönüşler) çözüldükten sonra bu durumun kendi kendine çözülmesi biraz zaman alabilir.

## İpuçları

- Başka her şeyi düzeltmeden önce DNS kimlik doğrulamasını düzeltin — SPF/DKIM/DMARC geçmiyorsa, diğer tüm teslim edilebilirlik unsurları (içerik, liste hijyeni, ısınma) daha az önem taşır.
- Kurulum sihirbazının DNS doğrulamasını tek seferlik bir işlem olarak değil, anlık bir kontrol olarak ele alın — DNS sağlayıcınızı değiştirdiğinizde veya alan adınızı farklı bir kayıtçı üzerinden yenilediğinizde bunu her zaman yeniden çalıştırın.
- Açılıp tıklanan temiz bir liste, tıklanmayan daha büyük bir listeden her zaman daha iyi performans gösterir — "her ihtimale karşı" diye eski, doğrulanmamış bir listeyi içe aktarma isteğine direnin.
- Sayılarınızı genel bir sektör standardına göre değil, kendi geçmiş gönderimlerinize göre izleyin — gerçek bir sorunun en güvenilir göstergesi kendi geçmişinizdir.
- Spwig barındırmalı bir planda iseniz, barındırılan e-posta geçidinin DKIM imzalama ve itibar yönetimi sizin için halledilir — kalan sorumluluğunuz DNS değil, liste kalitesi ve içeriktir.