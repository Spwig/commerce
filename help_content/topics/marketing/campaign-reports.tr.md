---
title: Kampanya Raporları
---

<!-- screenshots-needed:
- url: /admin/campaigns/{campaign_id}/report/
  filename: engagement-over-time-chart.webp
  description: The report page scrolled to the "Engagement over time" chart card, with a campaign that has several days of send history so all three lines (Sent, Opened, Clicked) show a realistic shape.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: top-links-table.webp
  description: The report page's "Top links" card, with a campaign whose email contains at least 3 distinct links and a realistic spread of Clicks/Unique/CTR values.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipients-list.webp
  description: The Recipients page with the filters panel open and a mixed list of rows (some opened, some clicked, some bounced) so the engagement states are visibly distinct.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipient-activity-modal.webp
  description: The Recipients page with the "Recipient activity" modal open for a recipient who has multiple event types (delivered, opened, at least one clicked entry naming a link).
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: attributed-revenue-card.webp
  description: A close-up of the report page's "Attributed revenue" stat card, for a campaign with a logged Spend so the orders/AOV/revenue-per-email/ROAS sub-line is fully populated.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: dashboard-attributed-revenue-kpi.webp
  description: The Campaign Studio dashboard's stat card grid, scrolled/cropped to show the "Attributed revenue (30d)" tile alongside its neighboring cards, with a non-zero revenue figure.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: report-stat-cards.webp
  description: 'RECAPTURE NEEDED: the existing report-stat-cards.webp only shows 6 cards (Recipients, Delivered, Open rate, Click rate, Bounce rate, Spam complaints). The stat grid now has a 7th "Attributed revenue" card — recapture this shot with a campaign that has both attribution data and a logged Spend so all 7 cards are visible in a realistic state.'
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
-->

Campaign Studio üzerinden gönderdiğiniz her kampanya için kendi **Rapor** sayfası oluşturulur — kaç kişiye ulaşıldığı, kaç e-postanın gerçekten teslim edildiği ve alıcıların nasıl tepki verdiği hakkında tek sayfalık bir özet. Bir gönderimin sorunsuz gerçekleştiğini kontrol etmek için, teslim edilebilirlik sorunlarını erken tespit etmek için veya farklı kampanyaların zaman içindeki performansını karşılaştırmak için kullanın.

## Bir raporu açma

**Campaign Studio > Campaigns** bölümünden, kontrol etmek istediğiniz kampanyayı bulun ve kartındaki grafik simgesine (**Report**) tıklayın.

![Kampanya rapor sayfasının istatistik kartı ızgarası, alıcılar, teslim edilenler, açılma oranı, tıklanma oranı, sevk oranı ve spam şikayetlerini gösteriyor](/static/core/admin/img/help/campaign-reports/report-stat-cards.webp)

Bir rapor, bir kampanya gerçekten gönderildikten sonra sayı göstermeye başlar — hâlâ **Draft** durumunda olan bir kampanya, henüz ölçülecek bir şey olmadığı için tüm istatistikleri sıfır olarak gösterir.

## İstatistik kartları

| Kart | Ne gösterir |
|------|---------------|
| **Alıcılar** | Bu kampanyaya yönelik kaç abone hedeflendiğini ve bir alt satırında, bunların kaçının, adresinin [suppression listesi](list-hygiene) üzerinde olmasından dolayı atlandığını belirtir. Bir atma her zaman bir suppression değildir - örneğin, bir abonenin kullanılabilecek bir e-posta adresi olmaması durumunda da Spwig bir aboneyi atabilir - bu yüzden iki sayım ayrı ayrı gösterilir. |
| **İletilen** | Alıcıların e-postasını kabul eden ve hiçbir şekilde geri dönülmeyen e-posta sayısı, ayrıca **iade oranı** - Spwig'ın *denediği* her gönderinin bir payı olarak. |
| **Açılma oranı** | *İletilen* e-postaların ne kadarının açıldığını ve **açılan** sayısı. |
| **Tıklama oranı** | *İletilen* e-postaların ne kadarının tıklandığını ve **tıklanan** sayısı ile **açılıma göre tıklama oranı** - açılanların ne kadarının tıklandığını gösteren, ziyaret edenlerin ne kadarı için içeriğinizin ne kadar etkili olduğunu gösteren bir oran. |
| **İade oranı** | *Denenen* gönderilerin ne kadarının iade edildiğini, **sert** ve **yumuşak** iade olarak bölünmüş hali. |
| **Spam şikayeti** | E-postayı spam ya da kaba olarak işaretleyen alıcı sayısı, ayrıca **şikâyet oranı** - *iletilen* posta üzerinden şikayet oranı. |
| **Atfedilen gelir** | Spwig'ın bu kampanyaya dayanarak takip edebileceği siparişlerden elde edilen gelir, sipariş sayısı, ortalama sipariş değeri (**AOV**), e-posta başına gelir ve - kampanyanın maliyetini kaydettiyseniz - **ROAS**'ı da içerir. Aşağıdaki [Atfedilen gelir](#attributed-revenue) başlığına bakınız. |

## Yüzde değerlerinin farklı paydalara sahip olması nedeni

Açılma oranı, tıklama oranı ve şikayet oranı, tüm *iletilen* postalar üzerinden ölçülür - yani e-postayı görebilecek olan alıcılar. Ancak iade oranı ve iade oranı, *denenen* gönderiler üzerinden ölçülür. Bu, e-posta endüstrisi pratiğinde standarttır ve bu yüzden bu oranların hiçbirinin %100'ün üzerinde olamayacağıdır: bir e-posta iade edildiyse, asla iletilemediği için, açma veya tıklama oranına dahil edilmeyecektir ve bir atma (skip) işlemi görülmemişse, hiçbirine dahil edilmeyecektir.

## Sert iade ve yumuşak iade

- **Sert iade** - adres kalıcı olarak iletilemez. Mevcut değil, ya da domain, onun için e-posta alımını reddediyor.
- **Yumuşak iade** - geçici bir problem: dolu bir posta kutusu, geçici olarak erişilemez bir alıcı sunucusu ve benzeri. Yumuşak iade genellikle kendi kendine çözülebilir.

Toplamdan ziyade, ayırma sayısına dikkat edin. Artan **sert iade** sayısı, listende eski ya da yanlış yazılan adreslerin olduğunu gösterir; artan **yumuşak iade** sayısı genellikle alıcının sonunda geçici bir aksilik olduğu anlamına gelir. Herhangi bir sert iade, herhangi bir spam şikayeti ve tekrarlayan yumuşak iade yapan bir adres, Spwig'ın otomatik [suppression listesi](list-hygiene)ne gider. Kendiniz bir şey yapmanıza gerek yok, ancak raporda incelemek için ilk olarak bir artışın farkına varacaksınız.

## Atfedilen gelir

Mağaza ve Kampanya Stüdyosunun aynı sistemin içinde olması nedeniyle, Spwig, bir kampanyanın satışları gerçekten yönlendirdiğini öğrenmek için harici bir analiz platformuna ya da izleme piksi lineerine ihtiyaç duymaz. Bir müşteri bu kampanyanın e-postasındaki bir bağlantıya tıkladığında mağazaya gider ve Spwig, bu ziyareti ödeme sayfasına kadar takip edebilir ve elde edilen siparişin gelirini kampanyaya geri kredilebilir - bu, **Atfedilen gelir** kartının gösterdiği şeydir.

Kartın alt satırı rakamı daha da ayrıntılı hale getirir:

- **Siparişler** - bu kampanyaya kredi verilen sipariş sayısı.
- **AOV** - bu siparişlerdeki ortalama sipariş değeri.
- **E-posta başına gelir** - atfedilen gelir, e-posta *iletilen* sayısına bölünür, raporun açma oranı ve tıklama oranı için kullandığı payda ile aynıdır.
- **ROAS** - reklam harcamasına dair getiri, kampanya için bir **Harcama** miktarı girildikten sonra sadece gösterilir.

Hesaplaması, atfedilen gelirin harcamaya bölünmesidir.

Eğer harcama, mağazanızın varsayılan dövizinden farklı bir para biriminde kaydedildiyse, Spwig, aynı anda karşılaştırılamayan bir rakam göstermek yerine ROAS'ı gizler — bu değeri görmek için mağazanızaki temel para biriminde harcamayı girin.

Bu sayının nasıl hesaplandığına dair bilinmesi gereken birkaç şey:

- **Bu, açıkma temelli değil, tıklama temelidir.** Bir müşteri, e-postadaki izlenen bir bağlantıyı tıklayıp mağazanıza gelmelidir — sadece açıkma, hasılatı atamaz. Bu, Apple Mail Privacy Protection gibi hizmetlerin neredeyse her mesaj için resimleri önceden yüklemesi nedeniyle açık oranlarını artırmaları ve kimse gerçekten e-postayı okumasa da, e-postanın kimse tarafından okunduğunu doğrulamaması nedeniyle giderek daha az güvenilir hale gelmiştir.
- **Mağazanızın atıf modeline göre hareket eder.** Varsayılan olarak **son doğrudan dokunma** ve 90 günlük bakış penceresi ile çalışır — aynı tıklama, bu pencere içinde bir siparişe yol açmalı ve daha sonra yapılan doğrudan ziyaret, bu kampanya tıklaması tarafından zaten kazanılan krediyi silmez.
- **Analiz izniye saygı duyar.** Mağazanızın cookie banner'ında analiz izni kabul eden sadece ziyaretçiler izlenir (eğer bir izin banner'ınız yoksa, izleme mağazanızın kendi varsayılan politikasına göre olur). İzin reddeden bir müşteri hâlâ alım yapabilir — bu durumda siparişi hiçbir kanala, bu da dahil olmak üzere atamayacaktır.
- **Retroaktif değildir.** Hasılat izlemesi, atıf izlemesi mağazanızda açıldıktan sonra gönderilen kampanyalara aittir. Bu tarihten önce gönderilen bir kampanya, Spwig'in bunun için tıklama verisi kaydetmemesi nedeniyle burada hiçbir atıf hasılatı göstermez.
- **A/B testleri ve tekrarlayan kampanyalar da atıf hasılatlarını birleştirir.** Aşağıdaki [A/B testi üzerindeki raporlar](#reports-on-an-ab-test) bölümüne bakın.

Ayrıca, Kampanya Stüdyosu dashboard'unda **Atıf hasılatı (30d)** kartını da bulacaksınız, bu da son 30 gün içinde e-posta üzerinden her kampanyadan atıf hasılatını toplamaktadır — bireysel bir raporu açmadan önce hızlı bir pulse kontrolüdür. E-posta dahil olmak üzere tüm kanalları içeren, organik arama, sosyal medya, afiliyolar ve daha fazlasını içeren bir mağaza genel bakış için, [Hasılat Atıfı](/help/revenue-attribution) dashboard'una bakın ve **Görünüm** altında bulunur.

## Zamanla Etkileşim


İstatistik kartlarının altında, **Zamanla Etkileşim** grafiği, 30 günlük ertesi tarihe kadar olan her gün için bir nokta içeren üç çizgi çizer — kampanyanızın bu kadar uzun süre gönderilmemiş olması durumunda daha önceki tarihe gitmez (grafik kampanyanızın ilk gönderimden itibaren en az ertesi tarihe kadar olur).

Bu çizgilerin nasıl sayıldığını bilmek için bazı şeyleri unutmayın:

- **Açık** ve **Tıklama** her bir alıcıyı bir kez sayar — aynı e-postayı tekrar açan veya bir linki tekrar tıklayan biri için ilk açık veya ilk tıklama gününü temsil eder. Bu, birkaç kişinin aynı e-postayı tekrar tekrar açmasıyla grafikteki eğilimi bozmamak içindir.
- Bu grafiğin arkasındaki toplamlar, onun üzerindeki istatistik kartlarıyla aynıdır: **Gönderilen**, Spwig'ın teslim etmeye çalıştığı postayı temsil ederken, **Açık** ve **Tıklama** her ikisi de teslim edilen postaya göre ölçülür, aynı zamanda **Açma oranı** ve **Tıklama oranı** kartları ile aynıdır.
- Bu grafik, kampanyanızın en az bir gönderimi olduğunda gösterilir — **Taslak** durumundaki bir kampanya, 

| Sütun | Ne gösterir |
|--------|---------------|
| **Link** | E-postanızdaki o linkin hedef URL'sidir. |
| **Tıklamalar** | Bu bağlantının, aynı alıcıdan tekrar tıklamalar dahil olmak üzere toplam tıklama sayısı. |
| **Benzersiz** | Bu bağlantıyı en az bir kez tıklayan farklı kaç alıcı olduğunu gösterir. |
| **Tıklama Oranı (CTR)** | Bu bağlantının **tıklama-geçiş oranı** — **Bildirilen E-posta** sayısına göre **Benzersiz** sayısı. Bu, raporun başlık **Tıklama Oranı** kartındaki aynı payda kullanılarak hesaplanır, bu nedenle tek bir bağlantının pullunu kampanyanın genel tıklama performansına göre karşılaştırabilirsiniz. |

E-postanız birden fazla ürün veya çağrı yapma butonu içermişse, bu tablo, bir sonraki sefere neyin daha ön plana çıkacağını belirlemek için en hızlı yolu gösterir.

## Alıcılar

Bu kampanya için gönderilen herkese ait, her birinin teslim sonucu ve etkileşimiyle birlikte tam, aranabilir bir liste açmak için raporun en üstündeki **Alıcılar**'a tıklayın.

Listeyi daraltmanın iki yolu vardır:

- **Arama** — e-posta adresine göre filtreleme yapar (kısmi eşleşme çalışır, bu nedenle bir domain veya isimin bir kısmını yazmak yeterlidir).
- **Etkileşim** — tek bir durum için filtreleme yapar: **Açıldı**, **Tıklandı**, **Teslim edildi, açılmadı**, veya **İptal edildi**. Tüm listeyi görmek için **Herkes** seçili tutun.

Liste, her seferinde en yeni 100 alıcıyı gösterir, en yeniden en eskiye doğru — listeden önceki sayı, filtrelerinize göre gerçek toplam sayıyı her zaman gösterir, gösterilen sayıdan büyük olsa da. Büyük bir gönderim için, herkese göre kaydırma yapmadan önce önce **Arama** veya **Etkileşim** ile listeyi daraltın.

### Bir alıcının etkinlik zaman çizelgesini görüntüleme

Herhangi bir alıcı satırındaki etkinlik simgesine tıklayarak onun **Alıcı Etkinlikleri** zaman çizelgesini açın — bu kişinin e-postasının her bir takip edilen olayı, tarih sırasına göre: teslim edildi, açıldı, tıklandı (hangi bağlantının tıklandığını belirtir), iptal edildi (iptal nedeniyle), spam olarak bildirildi veya abonelikten çıkarıldı, her biri için kendi zaman damgası ile.

Bu, bir müşteri hakkında belirli bir soruyu cevaplamak için en hızlı yoldur — örneğin, bir abonelerin kampanyayı aldığını doğrulamak ve başka bir kanal aracılığıyla onlarla ilgilenmek için, veya bir müşterinin sipariş vermeden önce hangi bağlantıyı tıkladığını kontrol etmek.

## A/B testi üzerindeki raporlar

Gördüğünüz kampanya [A/B testi](ab-testing) için bir kapsayıcıysa, raporu **her bir varyant** üzerinde toplar — testin tamamı, birlikte, **Atfedilen gelir** dahil olmak üzere — yani tek bir varyantı kendi başına göstermez. Her bir varyantın nasıl performans gösterdiğini görmek için raporun yerine testin kendi sonuç sayfasını açın. [Devam eden bir kampanya](recurring-campaigns) aynı şekilde çalışır: raporu, gönderdiği her bir olayı toplar.

## Neyin iyi olduğunu görmek

Her mağaza veya liste için tek bir sağlıklı sayı yok — hedef kitlen, sektöreler ve içeriklerin temelini değiştirir, ancak her kampanya için dikkat etmeniz gereken birkaç dizi örnektir:

- **İptal oranı**, sadece **yumuşak iptal** ile sınırlıysa ve **sert iptal** nadiren olursa, temiz, iyi bakımlı bir liste olduğunu gösterir. Sert iptaldeki ani bir artış, bir sonraki gönderiden önce incelemeniz gerekir.
- **Spam şikayeti**, her gönderide sıfıra yakındır. Şikâyetler, gönderen güvenilirliğiniz için neredeyse her şeyden daha fazla zarara neden olur — bu kampanyadan sonra neden önemli olduğunu görmek için [Liste Hijyeni](list-hygiene) sayfasına bakın.
- **Açma-çevrimiçi oran**, açık oranına göre sağlıklıysa, açan kişilerin içeriğin değerini kavradığını gösterir — güçlü bir açık oranı ile düşük bir açma-çevrimiçi oranı, genellikle konu başlığının içeriğe göre daha iyi çalıştığını gösterir.

## İpuçaları

Tüm markdown formatlamasını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- Raporu gönderimden hemen sonra değil, biraz zaman geçtikten sonra kontrol edin — açılışlar ve tıklamalar (ve bazı geri sekme raporları) e-posta sağlayıcınızdan gelmesi zaman alabilir.
- **Teslim Edilen** sayısı beklenenden düşük görünüyorsa, önce **Alıcılar** kartındaki atlanma dökümünü kontrol edin — baskılama nedeniyle oluşan bir atlanma grubu genellikle gerçek hikayedir, teslimat sorunu değil.
- Raporu, kampanyayı genel bir sektör rakamıyla değil, kendi geçmiş gönderimlerinizle karşılaştırmak için kullanın — listeniz, içeriğiniz ve hedef kitleniz gerçekçi tabanınızı belirler.
- Belirli bir gönderimdeki şikayetlerdeki bir artış, o kampanyanın içeriğine veya hedeflemesine daha yakından bakmayı hak eder, sadece not alıp geçilecek bir durum değildir.
- A/B testli bir kampanya için, genel sonucu bu rapordan ve hangi varyantın gerçekten kazandığını ve ne kadar farkla kazandığını [A/B test sonuçları](ab-testing) sayfasından okuyun.
- **En çok tıklanan bağlantılar** tablosunu en çok tıklanan bağlantınızı bulmak için kullanın, ardından bunun alıcıların *tıklamasını istediğiniz* şeyle eşleşip eşleşmediğini kontrol edin — ikincil bir bağlantı ana eylem çağrınızı geçiyorsa, bir sonraki e-postada onu daha yukarı taşımak değerli olabilir.
- **Alıcılar** sayfasındaki **Açıldı** ve **Tıklandı** filtreleri, bir takip kitlesi oluşturmanın hızlı bir yoludur — örneğin, listenin geri kalanına bir hatırlatma gönderimi planlamadan önce kimlerin açtığını ama tıklamadığını kontrol etmek.
- Bir gönderim etrafında bir promosyon için ödeme yaptıysanız — desteklenen bir sosyal medya gönderisi, bir influencer duyurusu, ücretli liste kiralama — bunu kampanyanın **Harcama** alanına kaydedin ve raporda **ROAS**'ı açığa çıkarın.

Hangi tür gönderimlerin gerçekten tekrar etmeye değer olduğunu görmenin en hızlı yoludur.