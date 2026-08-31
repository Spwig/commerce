---
title: A/B Testi
---

Campaign Studio'nun **A/B testi**, bir önceki gönderimden önce, hedef kitlenizin bir bölümünde aynı kampanyanın iki ila dört **varyantı** - farklı sürümleri - üzerinde deneyebilirsiniz. Sadece konu başlığığını değiştirin, ya da her varyant için tamamen farklı içerik tasarımı oluşturun. Spwig, listenedeki bir örneği varyantlara eşit şekilde böler, her birinin nasıl performans gösterdiğini takip eder ve en iyi performans gösteren varyantı, testi görmemiş olan herkese otomatik olarak gönderir.

## Test kurulumu

Öncelikle Campaign Studio'nun görsel oluşturucusunda kampanyayı normalde olduğu gibi oluşturun - bir konu başlığığı yazın, içeriği tasarlayın ve ulaşmak istediğiniz **Segment**'i seçin. Bu kampanya, testin **kapsayıcısı** olur. A/B testini buna eklediğinizde, kapsayıcı doğrudan gönderilmez - ayarları tutar ve ulaşılmak istenen hedef kitle, testin çalıştığı pool'dur.

İkinci bir yer A/B testi sihirbazını açar:

- Görsel oluşturucunun araç çubuğundaki **A/B testi** butonu.
- **Campaign Studio > Kampanyalar**'daki kampanya kartındaki **A/B testi** simgesi.

Bir test, bir kampanyada mevcut olduğunda, aynı buton testin sonuçlarına gider, sihirbaz yerine ve kampanya kartı, listede aniden fark edilebilecek küçük bir **A/B** etiketi alır.

## Ne test edilecek

Sihirbazın ilk adımı, varyantlar arasında neyin farklılaşacağını sorar:

| Seçenek | Ne değişir | Ölçülür | 
|--------|--------------|-------------| 
| **Konu başlığı** | Her varyant, aynı içeriği gönderir - sadece konu başlığı farklıdır. En yaygın test. | Açma oranı | 
| **İçerik** | Her varyant, görsel oluşturucuda kendi inşa ettiğiniz ayrı bir tasarımdır. | Tıklama oranı | 

!["Ne test etmek istiyorsun?" adımlı, konu başlığı seçili](/static/core/admin/img/help/ab-testing/ab-test-what-to-test.webp)

## Varyantlarınızı seçin

Ardından neye göre seçtiğiniz bağlı olarak ne yazarsınız:

- **Konu başlığı** - her varyant için bir konu yazın (2-4). Başlangıçta iki satır gösterilir; üçüncü veya dördüncü için **Diğer konuyu ekle**'ye tıklayın.
- **İçerik** - kaç tane varyant istediğini (2-4) seçin. Her varyant, kapsayıcının mevcut tasarımının tamamı ile başlar, yani test etmek istediğiniz şey dışında neyi değiştirmeniz gerekir.

Her iki durumda da, Spwig, varyantları **A**, **B**, **C** ve **D** olarak, girdiğiniz sıraya göre etikiler - buradan "Varyant A", "Varyant B" ve böyle devam eder.

![A, B ve C varyantları için üç konu başlığı ile Varyantlar adımı](/static/core/admin/img/help/ab-testing/ab-test-variants.webp)

İçerik testi için, sihirbazın kendisinde varyantları tasarlamazsınız - testi oluşturduktan sonra, her varyantın sonuç hub'ındaki kartı, aynı kapsayıcıyı oluşturmak için kullandığınız görsel oluşturucuda açılacak küçük bir kalem simgesi alır. Bu, test **Taslak** durumunda iken sadece mevcuttur; testi başlatırsanız, tasarımı kilitlenir ve test sırasında ölçümleriniz değişmez.

## Test ayarları

Sihirbazın son adımı, testin nasıl yapıldığını ve kararın neye göre alındığını kapsar:

| Ayar | Ne yapar | 
|---------|--------------| 
| **Test örneği** | Test için kullanılan hedef kitlenin payı, varyantlara eşit şekilde bölünür: %20, %30, %50 veya %100. Geri kalanı - **tutar** - ardından kazananı alır. %100 seçimi, tüm listeyi aynı anda test eder, bu nedenle kazanana ulaştırmak için bir tutar kalmaz. | 
| **Kazanan neye göre belirlenir** | **Açma oranı** veya **Tıklama oranı**. Konu başlığı testi için açık artışı, içerik testi için tıklama oranı olarak varsayılan olarak ayarlanır, çünkü her biri gerçekten ölçtüğü şeydir - her iki yönden de değiştirebilirsiniz. | 
| **Test penceresi (saat)** | Kazanıcıyı seçmek için açma ve tıklamaları toplamak için ne kadar süre, 1-168 saat (bir hafta). | 
| **Kazananı diğer hedef kitlenize otomatik olarak gönder** | Varsayılan olarak açıktır. Seçili olduğunda, pencere sona erdiğinde, sizin için hiçbir eyleme gerek kalmadan tutarın kazanan varyantını e-postayla gönderir. | 

Aşağıda, karar vermeden önce seçimlerinizi özetleyen kısa bir inceleme kartı vardır.

![Örnek, metrik, pencere ve otomatik gönderim seçenekleri ayarlanmış, ayrıca bir inceleme kartı içeren Ayarlar adımı](/static/core/admin/img/help/ab-testing/ab-test-settings.webp)

## Testi Başlatma

Kurulumu kaydetmek için **Test oluştur** düğmesine tıklayın — bu işlem henüz hiçbir şey göndermez. **Taslak** durumunda, şu ana kadar sıfır alıcı gösteren her bir varyantı ve iki düğümü (**Testi başlat** ve **Testi iptal et**) içeren testin sonuç merkezine yönlendirilirsiniz.

![Başlatılmaya hazır üç varyantı gösteren, Taslak durumunda yeni oluşturulmuş bir test](/static/core/admin/img/help/ab-testing/ab-test-draft.webp)

Hazır olduğunuzda **Testi başlat** düğmesine tıklayın. Spwig, test örneğinizi varyantlar arasında eşit olarak dağıtır ve her birine hemen e-posta gönderir — başka bir şey yapmanıza gerek yoktur; arka plan işi, test penceresi geçtiğinde kontrol eder ve kazananı kendi kendine belirler. Tüm bu süreç boyunca kapsayıcı kampanyanın kendi durumu **Taslak** olarak kalır — bu beklenen bir durumdur, çünkü asıl gönderilen şey varyantlardır (ve daha sonra kazanan), asla kapsayıcı değil.

Hedef kitlenizin, her bir varyantın anlamlı bir alıcı sayısına sahip olması için yeterince büyük olması gerekir. Spwig, herhangi bir varyantın sıfır kişiye düşmesi durumunda testi başlatmayı engeller, ancak gerçekten okunmaya değer bir test için asgari düzeyden fazlası gerekir — sonuca güvenmeden önce birkaç yüz alıcı veya daha fazlasını hedefleyin.

## Test Çalışırken

Başlatıldıktan sonra, merkez **Test Ediliyor** durumuna geçer ve pencerenin sona ereceği tarih ve saati gösteren "Test çalışıyor — kazanan otomatik olarak şu tarihte belirlenir" ifadesini görüntüler. Alıcı sayıları ve canlı açılma/tıklama oranları her ziyarette güncellenir; kazananı belirlemek için seçtiğiniz metrikten bağımsız olarak, her bir varyantın açılma ve tıklama oranlarını yan yana karşılaştıran bir çubuk grafik eşlik eder.

![Canlı alıcı sayılarını, açılma/tıklama oranlarını ve bir karşılaştırma grafiğini gösteren çalışan bir test](/static/core/admin/img/help/ab-testing/ab-test-running.webp)

Ayrıca, **Kampanya Stüdyosu panelinden** her testi izlemeye devam edebilirsiniz: *Son A/B testleri* paneli, çalışan ve kısa süre önce sonuçlanan testlerinizi listeler — her biri bir bakışta güven düzeyiyle birlikte — ve sonuçlara doğrudan bağlantı verir; ayrıca son 30 günde kaç testin çalıştığı ve kaçının sonuçlandığını sayan kartlarla birlikte.

## Sonuçları Okuma

Test penceresi sona erdiğinde, Spwig seçtiğiniz metrikte en yüksek orana sahip varyantı seçer, testi **Tamamlandı** olarak işaretler ve — **Kazananı otomatik olarak gönder** seçeneği işaretliyse ve gönderilecek bir kontrol grubu varsa — o varyantı testin parçası olmayan herkese e-posta olarak gönderir. Kazanan varyantın kartı çerçevelenir ve bir **Kazanan** rozeti taşır; varyantların nasıl karşılaştırıldığını görebilmeniz için karşılaştırma grafiği yerinde kalır.

![Kazanan varyantın vurgulandığı ve Kazanan rozeti taşıyan tamamlanmış bir test](/static/core/admin/img/help/ab-testing/ab-test-complete.webp)

Bu sayfadaki sayıların her zaman test örneği için olduğunu, tüm listeniz için olmadığını aklınızda bulundurun — %20'lik bir örnekle, kitlenizin tamamının değil, beşte birinin nasıl tepki verdiğini okuyorsunuz.

## Sonuç ne kadar güvenilir?

Daha yüksek bir açılma veya tıklama oranı, bir varyantın gerçekten daha iyi olduğu anlamına gelmeyebilir — küçük bir kitlede, bir varyant tamamen şans eseri öne çıkabilir. Bu nedenle, kazananın yanı sıra Spwig, farkın büyüklüğüne ve alıcı sayısına dayalı olarak **sonucun gerçek olduğuna ne kadar güvendiğini** gösterir. Üç okumadan birini göreceksiniz:

- **Net bir sonuç** — Spwig, önde gelen varyantın diğerlerinden gerçekten daha iyi olduğuna en az %95 güveniyor. Bu, harekete geçebileceğiniz bir sonuçtur.
- **Çok yakın, karar verilemiyor** — bir lider var, ancak fark, şans eseri olabilecek kadar küçük. Gösterilen yüzde, Spwig'in %95 eşiğinin altında ne kadar güvendiğini gösterir. Sonuçlar çıkarmadan önce daha büyük bir kitleyle veya daha uzun bir test penceresiyle yeniden çalışmayı düşünün.
- **Henüz yeterli veri yok** — varyantları birbirinden ayırt etmek için çok az alıcı (veya çok az açılma ve tıklama). Bu, küçük listelerde yaygındır; kitleyi büyütün veya testi daha uzun süre çalıştırın.


![Net bir sonuç gösteren tamamlanmış bir test — kazanan varyant bir güven rozeti taşır ve özet "istatistiksel olarak net" olarak okunur](/static/core/admin/img/help/ab-testing/ab-test-confidence.webp)

Aynı okuma, bir test hâlâ çalışırken de görünür, böylece pencere kapanmadan önce bir sonucun pekişip pekişmediğini izleyebilirsiniz. Güven, büyük ölçüde izleyici kitlesinin boyutuna bağlı olduğundan, bu, her test için birkaç yüz veya daha fazla alıcı hedeflemenin pratik nedenidir: çok küçük bir listede, büyük görünen bir fark bile genellikle "çok yakın, karar verilemez" olarak okunur.

Otomatik gönderim açıkken, Spwig, sonuç belirsiz olsa bile en yüksek oranlı varyantı izleyici kitlenizin geri kalanına göndermeye devam eder — güven okuması, sonucu ne kadar güvenebileceğinizi söylemek içindir, gönderimi durdurmak için değil.

## Bir testi iptal etme

**Testi iptal et**, bir test **Taslak** veya **Test Ediliyor** durumundayken kullanılabilir ve kazanan asla gönderilmeden testi durdurur. Bu, fikrinizi değiştirdiğinizde veya kurulumda bir hata yaptığınızda oradadır — bir test iptal edildikten (veya normal şekilde tamamlandıktan) sonra, aynı kampanya üzerinde yeni bir test kurmak için bir düğme olmadığından, hafife alınacak bir şey değildir. Daha sonra başka bir karşılaştırma çalıştırmak istiyorsanız, bunun için yeni bir kampanya oluşturun.

## İpuçları

- Önce bir **Konu satırı** testi yapın — kurulumu en basit olan ve A/B testinin en yaygın nedenidir.
- Sadece konudaki ifadeleri değil, gerçekten farklı tasarımları veya teklifleri karşılaştırmak istediğinizde bir **İçerik** testi kullanın.
- Bir içerik testinin her varyantını tasarlamayı bitirin — her kartta kalem simgesini kullanarak — **Testi başlat** düğmesine tıklamadan önce. Test çalışırken bir varyantın tasarımını düzenleyemezsiniz.
- Spwig'in kazananı daha sonra listenizin geri kalanına otomatik olarak e-posta göndermesini istiyorsanız **Test örneği** değerini %100'ün altında bırakın — %100'de ulaşması için bir kenara ayrılmış kitle kalmaz.

- Test penceresine, abonelerinizin normal okuma alışkanlıklarını kapsayacak kadar zaman verin (24 saat, saat dilimlerini ve gelen kutularının tam bir gününü rahatça kapsar) ve kazananı sadece ilk bir-iki saate göre belirlemeyin.