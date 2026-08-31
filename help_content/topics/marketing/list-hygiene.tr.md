---
title: List Hijyeni ve Bastırmalar
---

Sert sekme (hard-bounce) veren, e-postalarınızı spam olarak işaretleyen veya mesajlarınızı tekrar tekrar alamayan her e-posta adresi, listenizin geri kalanını riske atar — posta kutusu sağlayıcıları, gönderim itibarınızı gönderimlerin ne kadar temiz olduğuna göre değerlendirir ve kirli bir liste, *her* kampanyanın daha fazlasının spama düşmesi anlamına gelir. Campaign Studio, **liste hijyeni** ile sizi otomatik olarak korur: teslim edilemeyen ve şikâyetçi adresleri izler ve bunlara pazarlama e-postası göndermeyi durdurur, bunun için tarafınızdan herhangi bir kurulum gerekmez.

Bu, abonelik iptallerinden farklıdır. Aboneliği iptal edilmiş bir adres, onayını geri çekmiştir; **bastırılmış** (suppressed) adres ise Spwig'in, onay durumundan bağımsız olarak, e-posta göndermeye devam etmenin güvenli veya mümkün olmadığını öğrendiği adrestir.

## Adresler nasıl bastırılır

Spwig, aşağıdaki durumlarda bir adresi otomatik olarak **Bastırılmış adresler** listesine ekler:

| Tetikleyici | Anlamı |
|---------|---------------|
| **Sert sekme (Hard bounce)** | Adres mevcut değil veya alan adı, bu adres için posta kabul etmeyi reddetti — kalıcı olarak teslim edilemez. |
| **Spam şikâyeti** | Bir alıcı, e-postanızı spam veya çöp olarak işaretledi. |
| **Tekrarlayan yumuşak sekmeler (soft bounces)** | Adres, kayan 30 günlük bir pencere içinde 5 kez yumuşak sekme verdi (posta kutusu dolu, sunucu geçici olarak kullanılamıyor). Tek bir yumuşak sekme, geçici bir aksilik olarak kabul edilir ve yok sayılır — yalnızca tekrarlayan başarısızlıkların bir deseni bastırmayı tetikler. |
| **Manuel olarak engellendi** | Adresi kendiniz eklediniz. |

Bir adres bastırıldığında, Spwig derhal o adrese daha fazla **kampanya** veya **yolculuk** (journey) e-postası göndermeyi durdurur — sizden başka bir işlem gerektirmez.

## Sinyal nereden gelir

Spwig, bir sekme veya şikâyet hakkında birkaç farklı kaynaktan bilgi edinebilir; bunlar her bastırılmış adreste **Kaynak** olarak gösterilir:

- **Gönderimde reddedildi** — Spwig adrese göndermeye çalıştığında, e-posta sunucunuz adresi derhal reddetti.
- **Sağlayıcı web kancası (webhook)** — Bir e-posta sağlayıcısı (örneğin SendGrid, Amazon SES, Mailgun veya Postmark) bağladıysanız, bu sağlayıcı sekmeleri ve şikâyetleri Spwig'e gerçekleştikçe raporlar.
- **E-posta geçidi (Mail gateway)** — Mağazanız Spwig tarafından barındırılan e-posta geçidi üzerinden gönderiyorsa, Spwig adına sekmeleri geçitten çeker.
- **Manuel olarak eklendi** — Adresi yönetim panelinden kendiniz girdiniz.

Bundan faydalanmak için herhangi bir şey yapılandırmanıza gerek yok — e-postayı hangi yolla gönderirseniz gönderin, Spwig başarısızlıkları izliyor ve listenizi temiz tutuyor.

## Campaign Studio paneli

**Campaign Studio**'yu açın ve **Bastırılmış adresler** kartını bulun. Bu kart, şu anda bastırılmış adreslerin toplam sayısını ve son 30 günde yeni eklenenlerin sayısını gösterir. Tam Bastırmalar listesini açmak için karta tıklayın.

![Campaign Studio panelinin Bastırılmış adresler istatistik kartı, bir toplam ve "son 30 günde yeni" sayısını gösteriyor](/static/core/admin/img/help/list-hygiene/dashboard-suppressed-card.webp)

Kademeli olarak artan bir sayı normaldir — insanlar iş değiştirirken, hesaplarını kapatırken veya posta kutularını terk ederken her liste zamanla bazı kötü adresler biriktirir. Ani bir artış araştırılmaya değerdir; belirli bir gönderimin alışılmadık sayıda başarısızlıkla karşılaşıp karşılaşmadığını kontrol etmek için [E-posta Gönderim Kutusu](email-outbox) bölümüne bakın.

## Bastırmalar listesi

Her bastırılmış adresi, neden bastırıldığını ve sinyalin nereden geldiğini görmek için **Bastırmalar** bölümüne gidin.

![Neden ve Kaynak sütunlarıyla bastırılmış adresleri gösteren Bastırmalar listesi](/static/core/admin/img/help/list-hygiene/suppressions-list.webp)

Listeyi daraltmak için sağdaki filtreleri **Neden** veya **Kaynak** olarak kullanın — örneğin, tüm manuel olarak engellenmiş adresleri incelemek veya sağlayıcı web kancası üzerinden gelen her şeyi görmek için.

## Bir adresi manuel olarak ekleme

Bir adresi kendiniz engellemek için — bilinen bir kötüye kullanım adresi, bülteninizi kazıyan bir rakip veya listenizden uzak tutmak istediğiniz başka bir şey — **+ Bastırılmış adres ekle** düğmesine tıklayın ve şunları doldurun:

- **E-posta** — engellemek için adres
- **Sebep** — kendi eklediğiniz bir giriş için **El ile Engellendi** seçin
- **Detay** — isteğe bağlı bir not, nedenini açıklayacak (kendi kayıtlarınız ve daha sonra liste üzerinde inceleme yapan herhangi bir personel için faydalı olur)
- **Kaynak** — **El ile Eklenen** seçin

Giriş kaydını kaydedin ve Spwig, bu adresin kampanya veya yol email'ini hemen durdurur.

## Ne zaman bir adresi serbest bırakırım?

Bir adresi serbest bırakmak (engellemeyi kaldırmak), nadir ve bilinçli olmalıdır. Aşağıdakiler gibi bir sorunun aslında çözüldüğünden emin olduğunuz zamanlarda yapın:

- Bir müşteri, posta kutusunun dolu olduğunu ve temizlendiğini söylüyor.
- Bir önceki gönderiden sonra bir mail sağlayıcısında geçici bir arıza nedeniyle meydana gelen bir yumuşak geri dönüş sonucu engellenmiş bir adres.
- El ile engellediğiniz bir adres ve daha sonra engelin bir hata olduğunu karar verdiğiniz zaman.

Bir adresi serbest bırakmak için, Engelliler listesindeki girişini açın ve kaydı silin — bu engeli kaldıracak ve adresin tekrar e-posta almasına olanak sağlayacak. Eğer bir hata nedeniyle bir abone kaybı isterseniz, adresin mevcut olmadığını ve tekrar göndermenin sadece yankılayacağını ve ikinci seferde reputasyonunuzu kaybetmenize neden olacağını unutmayın. Aynı şekilde, spam şikayeti adresini serbest bırakmak nadiren faydalı olur — bu alıcı, posta sağlayıcısına mailinizi istemediğini bildirmiştir ve tekrar göndermenin başka bir şikayete neden olma riskini taşır.

## Etkilenmeyenler

Engelleme, Campaign Studio aracılığıyla gönderilen **pazarlama kampanyaları ve seyahatleri** için geçerlidir. **İşlemci e-postası** - sipariş onayları, kargo güncellemeleri, şifre sıfırlama ve mağaza tarafından bir sipariş ya da hesap eylemi kapsamında gönderilen diğer e-postalar, engellenmiş bir adrese bile ulaşır, çünkü engelleme, pazarlama gönderim güvenliğinizi korumak içindir; mağazanızın genel bir e-posta engel listesi değildir.

## İpuçları

- Bir sert geri dönüş görürseniz, sistemi fight etmeyin — sert geri dönüş, adresin olmadığını gösterir ve bu adresi tekrar eklemek sadece tekrar geri dönecektir.
- Büyük bir gönderimden sonra Engelliler listesini kontrol edin, açılım oranı beklenmedikçe düşük görünüyorsa — bir şirket posta sunucusunda sorun varsa gibi paylaşım alan adında bir dalganın yumuşak geri dönüşleri, geçici bir teslim problemi olup olmadığını incelemek için bir işaret olabilir.
- Spwig'den başka bir platformdan geçiyorsanız, eski bloklistinizi el ile aktarmayın — bu listede gerçek geri dönüşler ve şikayetlerden öğrenmesini sağlayın, çünkü bu adreslerin teslim edilebileceğini yanlışlıkla engellememek için.
- **Kaynak** sütununu sık sık inceleyin — birçok **Sağlayıcı web kancası** girişi, e-posta sağlayıcınızın geri dönüş raporunun bağlı ve çalıştığını doğrular.
- El ile engelleme yaparken **Detay** alanını anlamlı tutun; zaman geçtikten sonra bu kararın nedeni hakkında tek kayıt olur.