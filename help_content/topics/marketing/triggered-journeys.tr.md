---
title: Tetiklenen Yolculuklar
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/{journey_id}/report/
  filename: journey-report.webp
  description: Bir yolculuk için Yolculuk raporu sayfası — anlamlı bir kaynak takibi olan bir yolculuk için, Kayıt yuvarlakları (Kayıt Oldu/Şu an aktif/Oluşturuldu/Çıkış Yaptı) ve Etkilenen gelir kartı her ikisi de sıfır olmayan sayılar gösteriyor, ayrıca en az bir düz adım ve bir A/B adımını olan "Adım Bazında Gelir" tablosu (Adım/Gelir/Siparişler/Gönderildi/Açıldı/Çevrildi) ile gerçek Gönderildi/Açıldı/Çevrildi sayıları gösteriliyor.
  save-to: core/static/core/admin/img/help/triggered-journeys/
  viewport: 1440x900
-->

Campaign Studio'nun **Yolculukları**, bir müşteri belirli bir şey yaptığında kendi başı sıra gelir — kaydolur, bir sipariş verir, sepetinde ürün bırakır, bir süre sessiz kalırsa veya bir sipariş teslim edilirse. Tek seferlik bir tanıtımla veya indirim için el ile bir hoş geldin e-postası, bir sepet kurtarma ipucu veya bir inceleme istemi e-postası göndermeyi unutmanıza gerek yok — bir kere oluşturduğun sırayı, yolculuk aktif kaldığı sürece, her biri için Spwig çalıştırır.

## E-posta göndermenin üç yolu

Campaign Studio artık üç ayrı gönderme kalıbını kapsar:

| Tür | Davranış |
|------|-----------|
| **Yayın** | Bir kere - hemen veya tek bir planlanan tarih ve saatte. Tek seferlik bir duyuru veya indirim için kullanın. |
| **Sürekli** | Tekrarlayan bir düzene göre gönderilen bir şablon (bkz. [Sürekli Kampanyalar](/help/recurring-campaigns)). |
| **Yolculuk** | Bir yaşam döngüsü olayı olduğunda, bir müşteri için kendi başı sıra gelen çok adımlı bir dizi. Ardından saatler veya günler boyu adımlarını sırayla gönderir. |

Bir yolculuk için kendi "gönder" butonu ve yapılandırılması gereken bir zamanlaması yok — saate değil, olaylara yanıt verir.

## Tetikleyiciler

Her yolculuk, yolculuğun **Tetikleyicisi** olarak ayarlanan tam olarak bir olayı dinler:

| Tetikleyici | Ne zaman ateşlenir |
|---------|-----------|
| **Müşteri kaydolur** | Yeni bir müşteri hesabı oluşturulduğunda. |
| **Sipariş verilir** | Yeni veya eski bir müşteri tarafından herhangi bir sipariş verildiğinde. |
| **İlk sipariş verilir** | Özellikle bir müşterinin ilk siparişidir. |
| **Sepete eklenen ürün bırakıldı** | Bir alışverişçi sepetine bir şey ekler, daha sonra ödeme yapmadan sessiz kalır. |
| **Müşteri devre dışı (tekrar kazanma)** | Bir müsteri uzun bir süre önce sipariş vermemiş. |
| **Sipariş teslim edildi** | Bir siparişin durumu Teslim Edildi'ye döner. |
| **Ürün stokta** | Bir müşteri tarafından bildirilmek istenen bir ürün tekrar mevcut hale gelir. |

## Kurtarma ve tekrar kazanma tetikleyicileri, detaylı olarak

**Sipariş teslim edildi** ve **Ürün stokta** tetikleyicileri, **Sipariş verilir** ile aynı anda hemen ateşlenir. **Sepete eklenen ürün bırakıldı** ve **Müşteri devre dışı (tekrar kazanma)** farklı çalışır: tek bir an yerine, Spwig, eşleşen alışverişçileri ve müşterileri periyodik olarak kontrol eder, bu nedenle bir sepetteki ürünün sessiz kalması (veya bir müşterinin devre dışı kalması) ile kayıt arasında kısa bir gecikme olabilir.

**Sepete eklenen ürün bırakıldı** — bir ürün sepetine ekledikten sonra ödeme yapmadan sessiz kalan bir alışverişçiyi kaydeder. Varsayılan olarak bu, yaklaşık bir saatlik bir eylemsizlik sonrası olur; tam olarak ne kadar eylemsizlik penceresi (ve Spwig'ın ne kadar geriye bakacağı) bir önceki eylemsizlik süresi, sahibin mağazanız için ayarlayabileceği bir eşiktir. Bu, oturum açmış alışverişçiler ve misafirler için de geçerlidir — bir misafir için, Spwig ödeme sırasında alınan e-posta adresini kullanır. Eğer alışverişçi geri döner ve siparişini tamamlar, otomatik olarak yolculuktan çıkarılır, bu nedenle bir siparişin tamamlanması, "ne unuttuğunuzu

Bir müşteri, en fazla o pencere boyunca bir daha tekrar kazanma yolculuğuna girebilir, bu yüzden biri geçici olarak bir daha tekrar kazanma yolculuğuna giremez.

**Sipariş teslim edildi** — bir müşterinin sipariş durumu **Teslim edildi** olarak değiştirildiğinde, birkaç gün sonra bir inceleme istemek için doğal bir an. Bu, Teslim edildi'ye geçişte bir kez ateşlenir — zaten teslim edilmiş bir siparişe daha sonra yapılan düzenlemeler bu olayı ateşlemez. Sipariş listesindeki **Seçilen siparişleri Teslim edildi olarak işaretle** çoklu eyleminin, siparişleri doğrudan güncellediğini ve bu tetiği (ya da teslim konfirmasyonu e-postasını) ateşlemediğini unutmayın; bu tetiği ateşlemek için siparişleri tek tek güncelleyin ya da Spwig mobil uygulaması aracılığıyla güncelleyin.

**Ürün stokta** — bir müşterinin bildirim almasını istediği bir ürün stokta iken, Spwig, bu tetikleyiciyi dinleyen aktif bir yolculuk olup olmadığını kontrol eder. Eğer varsa, müşteri düz bir tek seferlik uyarı yerine bu yolculuğa alınır. Böylece bir gecikme, stokta olan ürünü gösteren bir **Gösterge Ürünü** bloğu ya da bir sonraki e-posta ekleyebilirsiniz. Stokta ürün için aktif bir yolculuk yoksa, müşteriler hâlâ öncekiyle aynı şekilde standart tek seferlik bildirim e-postası alır, bu tetikleyici için bir yolculuk açmak zorunluluğu yoktur.

## Bir yolculuk oluşturma

**Kampanya Stüdyosu > Yolculuklar**'a gidin ve **Yolculuk Ekle**'ye tıklayın.

1. Yolculuk için bir **İsim** verin — bu, sadece kendi referansınız içindir; müşteriler bunu asla görmez.
2. **Tetikleyici** olayını seçin.
3. İsteğe bağlı olarak **Sadece segment için** kısmına bir Segment ayarlayın — ayarlandığında, bu segmente ait olan aboneler sadece bu yola alınır. Herhangi bir segment ayarlamayın, tüm uygun aboneleri alır.
4. **Abone başına bir kez** ve **Yeniden kayıt soğutma süresi (gün)** ayarlayın — aşağıda ki [Yeterli kaydolmaya karşı koruma](#guarding-against-over-enrollment) bölümüne bakın.
5. Yolculuğu açmak için **Durum**'u **Aktif** olarak ayarlayın. Henüz tasarımı bitirmeden **Taslak** olarak bırakın ya da yeni kayıtları durdurmak için **Duraklatılmış** olarak ayarlayın.
6. **Kaydet**'e tıklayın — Spwig size hemen [Yolculuk Oluşturucusu](/help/journey-builder) sayfasına götürür, bu sayfada gerçek sırayı tasarlayabilirsiniz: hangi e-postaların gönderileceği, aralarında ne kadar beklenmesi gerektiği ve farklı abonelerin farklı yollar izleyip izlemeyeceği.

Kanvas üzerinde tasarlandığında, basit bir üç adımlık tanışma serisi şöyle görünebilir:

| Adım | Bekler | Gönderir |
|------|-------|-------|
| 1 | Hemen | Hoş Geldiniz E-postası |
| 2 | 3 gün sonra | Başlamaya Dair İpuçuları |
| 3 | Ondan sonraki 7 gün sonra | İlk Sipariş İndirimi |

E-postaların kendisi, bir yayın için kullanıdığınız görsel oluşturucuda tasarladığınız, konu satırı, içerik blokları ve tümüyle aynı olan normal kampanyalardır. Kendiniz bir tarih belirlemek ya da göndermek gerekmez; sadece oluşturucudaki adımın aşağı açılan menüsünden seçin. Yolculuk, her bir abonenin bu adıma ulaştığında size göre gönderir.

Kanvas üzerinde adımların nasıl tasarlanacağını, bir **Evet/Hayır** koşuluyla yolculuğu dallandırmayı ve boş bir kanvastan ziyade hazır bir şablondan başlatmayı içeren tam rehber için [Yolculuk Oluşturucusu](/help/journey-builder)'a bakın.

## Bir adımı A/B testi yapma

Herhangi bir **E-posta Gönder** adımı, bir A/B testine dönüştürülebilir, bu yüzden yolculuk otomatik olarak en iyi performansı elde eden e-postayı keşfeder ve ardından bunu kullanmaya devam eder. Bir yolculuk sürekli olarak çalışır (aboneler zamanla gelir), bu yüzden Spwig sabit bir batch testi yapmaz ve durmaz; bunun yerine **kaynaklardan gelenleri eşit şekilde varyantlara ayırır, her birinin nasıl çalıştığını izler ve biri net bir istatistik kazanıcısı olduğunda, bu varyantı her yeni kayıtlı abone için sabitleştirir.** Zaten bu adımda ilerlemeye başlayan aboneler, ilk gönderilen versiyonu korur.

[Journey Builder](/help/journey-builder) içinde bir **E-posta Gönder** adımını açın ve **Adım türü**'nü ayarlayın:

- **Tek e-posta** — normal davranış: herkesin seçtiğiniz tek e-postayı alması.
- **A/B: farklı e-postalar** — **iki ile dört** e-posta seçin (farklı tasarımlar, teklifler veya yerleşimler); her katılımcı birini alır.
- **A/B: farklı konu satırları** — bir e-posta seçin ve **iki ile dört** konu satırı girin; her katılımcı farklı bir konu ile o e-postayı alır.

Ardından **Kazananı şu şekilde belirle** — **Açılma oranı** (genellikle bir konu testi için en iyisi) veya **Tıklama oranı** — seçin ve işiniz biter. Yolculuğu **Aktif** olarak ayarlayın ve katılımcılar varyantlar arasında dağıtılmaya başlar.

Adımın paneli, veri geldikçe bir **canlı skor tablosu** gösterir — her varyantın alıcıları, açılma oranı ve tıklama oranı, ayrıca Spwig'in lider konusunda ne kadar emin olduğu ("%92 güvenle önde"). Kazanan, Spwig en az **%95 emin** olduğunda *ve* güvenilmesini sağlayacak kadar veri olduğunda kilitlenir, bu nedenle düşük trafiğe sahip bir yolculuk aceleci sonuçlara varmaz. Kilitlendikten sonra adım **"Kazanan kilitlendi: Varyant B"** olarak okunur ve her yeni katılımcı o varyantı alır; tuvalde kart, test sırasında **"A/B · N e-posta"** gösterir, karar verildikten sonra ise **"A/B kazananı: B"** olarak değişir.

Bilmeniz gereken birkaç şey:

- **Trafik verin.** Güven, hacme bağlıdır — sadece birkaç kişinin ulaştığı bir adım bir süre "Henüz yeterli veri yok" durumunda kalabilir. A/B testleri, istikrarlı kayıt olan yolculuklarda parlar.
- **Varyantları veya kazanan metriklerini düzenlemek yeni bir test başlatır** — daha önce kilitlenmiş bir kazanan temizlenir, böylece yeni kurulum kendi sonucunu elde eder.
- İki varyanttan az içeren bir A/B adımı, tamamlayana kadar (veya tek e-postaya geri değiştirene kadar) **yolculuğun Aktif olmasını engeller**.

Spwig'in güven ve anlamlılığı nasıl okuduğu hakkında daha fazla bilgi için [A/B Testi](ab-testing) bölümüne bakın.

## Kayıt nasıl çalışır

Bir müşteri için tetikleyici olay gerçekleştiğinde, Spwig o olayı dinleyen tüm aktif yolculukları kontrol eder ve müşterinin uygun olduğu her biri için, akışın başlangıç noktasında onları **kaydeder**. Oradan itibaren, Spwig aboneyi tuvalde tasarladığınız her şeyden ileriye taşır — her **Bekle** adımını bekler, her **E-posta gönder** adımının e-postasını gönderir ve herhangi bir **Dal** adımında doğru **Evet**/**Hayır** yolunu izler — ta ki bir **Çıkış** adımına ulaşana kadar, bu noktada yolculuk o abone için **Tamamlandı** olarak işaretlenir.

**Onay her zaman saygı gösterilir.** Pazarlama e-postasına katılmamış veya daha sonra aboneliğini iptal etmiş bir abone, basitçe atlanır — yolculuk diğer aboneler için durmaz ve yolculuk ortasında yapılan iptaller, o abonenin kalan gönderimlerini otomatik olarak durdurur. Yolculuklarınızı onay durumuna göre kendiniz filtrelemenize asla gerek yoktur.

## Aşırı kayıttan korunma

Yolculuktaki iki ayar, bir abonenin ne sıklıkla bu yolculuktan geçebileceğini kontrol eder:

| Ayar | Ne yapar | Tipik kullanım |
|---------|--------------|-------------|
| **Abone başına bir kez** *(varsayılan olarak açık)* | Her abone, tetikleyici olay onlar için tekrar ne kadar çok olursa olsun, en fazla bir kez kaydedilir. | Bir hoş geldiniz serisi — bir müşteri bunu yalnızca bir kez almalıdır. |
| **Yeniden kayıt soğuma süresi (gün)** | **Abone başına bir kez** kapalıyken, bir abonenin yeniden kaydedilmeden önce son kayıtlarından bu yana geçmesi gereken minimum gün sayısını belirler. Soğuma süresi yoksa `0` olarak ayarlayın. | Yeni bir sipariş için tekrar çalışması gereken ancak aynı hafta verilen her sipariş için yeniden tetiklenmemesi gereken bir sipariş tetiklemeli seri. |

Sipariş başına çalıştırmak istediğiniz bir yolculuk için (örneğin satın alma sonrası teşekkür) **Abone başına bir kez** ayarını kapatın ve bir müşteri aynı gün iki kez sipariş verdiğinde yalnızca bir kez kaydedilmesini sağlamak için bir soğuma süresiyle eşleştirin. Zaten aktif olarak bir yolculukta ilerleyen bir abone, bu ayarlardan bağımsız olarak, aynı yolculuğun ikinci, örtüşen çalışmasına asla kaydedilmez.

## Yolculukları izleme


The **Campaign Studio > Journeys** list shows each journey's **Trigger**, **Status**, the number of **Emails** it sends, and running **Enrolled** / **Completed** totals, so you can see at a glance whether a journey is actually reaching people.

![The Journeys list showing two active journeys with enrollment and completion counts](/static/core/admin/img/help/triggered-journeys/journey-list.webp)

To see individual subscribers rather than totals, open the **Journey Enrollments** list at `/admin/email_marketing/journeyenrollment/`. Each row shows one subscriber's progress through one journey: which **Journey** they're in, their **Current step**, **Status** (Active, Completed, or Cancelled), and when their **Next step** is due. Use the filters to narrow it down to one journey or one status — for example, filtering to **Active** shows everyone currently mid-sequence.

![The Journey Enrollments list showing subscriber progress across two journeys](/static/core/admin/img/help/triggered-journeys/journey-enrollments.webp)

## Journey report

Every journey has its own **Report** page, opened by clicking the **Report** button on the journey's card in **Campaign Studio > Journeys**, or on the journey's own settings page. It's a single-page summary of how far enrollees get through the sequence and, where your emails contain tracked links, how much revenue the journey has driven.

![The Journey report page showing the enrollment funnel, attributed revenue card, and revenue-by-step table](/static/core/admin/img/help/triggered-journeys/journey-report.webp)

### Enrollment funnel

Four cards show where enrollees currently stand:

| Card | What it shows |
|------|---------------|
| **Enrolled** | The total number of subscribers who have ever entered this journey. |
| **Active now** | Enrollees currently partway through the sequence, waiting on or working through their next step. |
| **Completed** | Enrollees who reached the journey's **Exit** step. |
| **Exited** | Enrollees taken out of the journey before completing it — for example, a shopper who finished checkout mid-way through a cart-abandonment sequence, or a subscriber who unsubscribed. |

If the journey has no enrollments yet, all four cards read zero and a note reminds you that metrics appear once customers start entering the journey.

### Attributed revenue

The **Attributed revenue** card works the same way as a [campaign report's](campaign-reports) — Spwig traces orders back to clicks on links in the journey's emails, the same click-through, consent-gated attribution described in [Attributed revenue](campaign-reports#attributed-revenue) on that page. The same caveats apply here: attribution is click-through only (an open alone never attributes revenue), it follows your store's active attribution model and lookback window, it respects analytics consent, and it isn't retroactive — a journey only shows revenue from emails sent after attribution tracking was switched on for your store.

The card's sub-line breaks the total down into:

- **Orders** — how many orders are credited to this journey, across every step's emails combined.
- **AOV** — the average order value across those orders.
- **Revenue per enrollee** — attributed revenue divided by total **Enrolled**. A journey doesn't have a single "spend" the way a campaign does — it runs continuously rather than costing something once — so there's no ROAS figure here. **Revenue per enrollee** is the closest equivalent: a steady, comparable measure of how efficiently the journey turns an enrollment into a sale, that you can track over time or compare against another journey.

### Revenue by step

When the journey has at least one **Send email** step, a **Revenue by step** table breaks the total down further, one row per step, so you can see which email in the sequence is actually earning its keep:


| Sütun | Ne gösterir |
|--------|---------------|
| **Adım** | Adımın e-postası; o adım bir [A/B testi](ab-testing) çalıştırıyorsa **A/B** rozetiyle birlikte. |
| **Gelir** | O adımın e-postasına kadar izlenebilen siparişlerden kaynaklanan atfedilen gelir. |
| **Siparişler** | Bu gelir rakamının arkasındaki sipariş sayısı. |
| **Gönderilen** | Bu adımın e-postasının kaç kez gönderildiği. |
| **Açılışlar** / **Tıklamalar** | Bu gönderimlerin kaçının açıldığı ve kaçının tıklanmış olduğu. Spwig, her adımın gönderimleri için (sade ve A/B fark etmeksizin) açılışları ve tıklamaları izler. |

Bu tabloyu, genel olarak sağlıklı bir yolculuktaki zayıf halkayı tespit etmek için kullanın — örneğin, ilk e-postanın gelirin büyük kısmını sağladığı ve sonraki bir adımın az katkıda bulunduğu bir hoş geldiniz serisi, tüm dizinin yeniden düşünülmesi yerine daha güçlü bir teklif veya yeniden yazım adayı olabilir.

## İpuçları

- Sepet terk etme, geri kazanma, teslimat sonrası inceleme veya stokta geri bildirme yolculuğunu başlatmanın en hızlı yolu bir başlangıç şablonudur — bu tetikleyicilerden biriyle yeni bir yolculuk kaydettiğinizde, [Journey Builder](/help/journey-builder)'ın **Şablonlar** seçicisi, sıfırdan oluşturmak yerine ayarlayabileceğiniz hazır bir akış (**Terk edilen sepet kurtarma**, **Kayıp müşterileri geri kazanma**, **Teslimat sonrası inceleme isteği** veya **Stokta geri bildirim uyarısı**) sunar.
- Adımlarını oluştururken her yolculuğu **Taslak** olarak başlatın, ardından e-postaları ve gecikmeleri kontrol ettikten sonra **Durum**u **Aktif** olarak değiştirin — Aktif olana kadar kimse kaydolmaz.
- Tek seferlik bir kilometre taşıyla (kayıt, ilk sipariş) ilişkili olan her şey için **Abone başına bir kez** seçeneğini açık tutun; satın alma sonrası serisi gibi tekrarlaması gereken her şey için makul bir soğuma süresiyle kapatın.
- Belirli bir kitle için farklı bir hoş geldiniz serisi çalıştırmak için **Yalnızca segment için** seçeneğini kullanın — örneğin, bir VIP segmenti diğerlerinden daha zengin bir dizi alır.
- İlk e-postanın tetikleyici ateşlendikten sonra beklenmeden hemen gitmesini istiyorsanız, ilk adımın bekleme süresini `0` olarak ayarlayın.
- Yeni bir yolculuğu etkinleştirdikten sonra, abonelerin gerçekten kaydolunduğunu ve adımlarında beklenildiği gibi ilerlediğini doğrulamak için **Journey Enrollments** listesini kontrol edin.
- Bir yolculuğu duraklatmak (**Durum: Duraklatıldı**) yeni kayıtları durdurur, ancak zaten yarıda olan aboneleri iptal etmez — kalan adımlarını almaya devam ederler.