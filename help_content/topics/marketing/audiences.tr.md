---
title: Hedef Kitleler
---

Bir **Segment**, bir kampanya, bir yolculuk veya bir A/B testine yönlendirebileceğiniz kayıtlı bir hedef kitledir — Campaign Studio'nun kendi Segmentler listesi bunlara "Hedeflenen kitleler" der ve bu kılavuz aynı şey için her iki terimi de kullanır. Her segment ya **dinamik**tir, yani Spwig'in her kullanımda yeniden değerlendirdiği kurallarla tanımlanır, ya da **statik**tir, yani elle seçtiğiniz açık bir abone listesidir.

Bu kılavuz, mağazanızın kendi müşteri değer kovalarını, sadakat programını ve bayilerini hedefleyen daha yeni alanlar dahil olmak üzere dinamik bir segmentin kurallarını oluşturmaya ve mağazanızın zaten sahip olduğu verilerden hazır segmentler seti oluşturan tek tıkla **Başlangıç kitlelerini ekle** düğmesine odaklanır.

## Dinamik ve statik segmentler

| Tür | Nasıl çalışır | En iyi kullanım alanı |
|---|---|---|
| **Dinamik (kurallar)** | Koşulları tanımlarsınız — örn. "Toplam harcama en az 500 $." Spwig, segment her kullanıldığında kimlerin eşleştiğini yeniden hesaplar, böylece aboneleriniz değiştikçe üyelik otomatik olarak değişir. | "VIP müşteriler" veya "90 gündür sipariş vermemiş" gibi her zaman güncel kalması gereken sürekli kitleler. |
| **Statik (sabit liste)** | Elle eklediğiniz veya çıkardığınız açık bir abone listesi. Siz değiştirmedikçe üyelik asla değişmez. | Tek seferlik bir liste — belirli bir etkinlikteki herkes veya tek seferlik bir gönderim için elle seçilmiş bir grup. |

Bir segment oluştururken türü **Tür** alanıyla seçin. Bu kılavuzun geri kalanı dinamik segmentler hakkındadır — statik olanlar, yapılandırılacak kuralı olmayan sadece bir üye listesidir.

## Dinamik bir segment oluşturma

**Campaign Studio > Segmentler**'i açın, ardından **Audience rules** oluşturucusuna ulaşmak için **+ Yeni Segment**'e (veya mevcut bir dinamik segmenti açın) tıklayın. Bir kural eklemek için **+ Koşul ekle**'ye tıklayın, neyi kontrol edeceğinizi ve nasıl edeceğinizi seçin ve bir abonenin koşullarınızın **tümüne** mi yoksa **herhangi birine** mi uyması gerektiğini belirleyin. Sağ üst köşedeki canlı sayaç — örn. "8 eşleşen abone" — her değişiklikten bir an sonra güncellenir, böylece kaydetmeden önce tam olarak kimlerin uygun olduğunu görebilirsiniz.

![Müşteri segmenti, Sadakat kademesi, Yaşam boyu değer ve Bayi koşulları ayarlanmış ve canlı eşleşen-abone sayacı içeren Audience rules oluşturucusu](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

Sabit bir **doğru**-stil kontrolü içeren bir koşul — **Sipariş verdi**, **Pazarlamaya katıldı**, **Sadakat üyesi**, **Bayi** — alanın kendisini seçmenin ötesinde hiçbir şeye ihtiyaç duymaz; ayarlanacak bir operatör veya değer yoktur.

## Hedefleyebilecekleriniz

| Alan | Ne kontrol eder |
|---|---|
| **Toplam harcama** | Yaşam boyu sipariş toplamı. |
| **Sipariş sayısı** | Tamamlanan sipariş sayısı. |
| **Yaşam boyu değer** | Müşterinin hesaplanan yaşam boyu değeri. |
| **Ortalama sipariş değeri** | Tamamlanan sipariş başına ortalama tutar. |
| **Son siparişten geçen gün** | Müşterinin en son siparişinden bu yana geçen süre — geri kazanım kitleleri için 90+ günü hedefleyin. |
| **Sipariş verdi** | Müşterinin en az bir tamamlanmış siparişi olup olmadığı. |
| **Pazarlamaya katıldı** | Abonenin pazarlama e-postasına onay verip vermediği. |
| **Dil** | Abonenin kayıtlı dili. |
| **Kaynak** | Abonenin nasıl katıldığı — Mağaza ön yüzü kaydı, İçe aktarma, Sipariş, Manuel eklendi veya API. |
| **Şu tarihten sonra katıldı** | Seçilen tarihte veya sonrasında katılan aboneler. |
| **Etikete sahip** | Abonenin oluşturduğunuz bir [etikete](/help/subscriber-tags) sahip olup olmadığı. |
| **Müşteri segmenti** | Müşterinin mağazanızın kendi adlandırılmış [müşteri segmentlerinden](/help/customer-segments) birine girip girmediği — Misafir Müşteri, Yeni Müşteri, Düzenli Müşteri, Sık Alıcı, Yüksek Değer, VIP Müşteri, Fırsat Avcısı, Risk Altında veya Pasif. |
| **Sadakat üyesi** | Müşterinin sadakat programınızın aktif bir üyesi olup olmadığı. |
| **Sadakat puanları** | Üyenin mevcut kullanılabilir puan bakiyesi. |
| **Sadakat kademesi** | Üyenin şu anda sahip olduğu sadakat kademesi. |
| **Bayi** | Müşterinin aktif bayi ortaklarınızdan biri olup olmadığı. |

**Müşteri segmenti**, iki **Loyalty** (Loyallik) değeri, **Loyalty seviyesi**, ve **Ortak** daha yeni eklenenlerdir ve mağazanızın bu tür veriye sahip olması durumunda koşul seçiciinde görünür: loyalty alanları, loyalty programınızın üyeleri ve en az bir etkin seviyesi olduğunda görünür, **Ortak** en az bir ortak olduğunda görünür, ve **Müşteri segmenti** en az bir tane etkin müşteri segmenti ayarlandığında görünür.

Yeni bir mağazada, kimseyi de匹配 edemeyecek bir seçenek göremezsiniz.

Bilinmesi gereken şu anki bir sınırlama: **Dil**, **Kaynak**, **Etiket var**, **Müşteri segmenti**, **Loyalty seviyesi** gibi seçimlerin olduğu bir koşul için, **herhangi biri** operatörü sadece bir değeri aynı anda seçebilir. Birden fazla değeri (örneğin, VIP veya Yüksek Değerli segmentte olan müşterileri) eşleştirmek isterseniz, her değer için bir koşul ekleyin ve **Eşleş**'i **herhangi biri** olarak ayarlayın.

## Başlangıç segmentleri ekle

Spwig zaten uygun olanları görebiliyorsa, her açık segment için kural oluşturmak, VIPleriniz, loyalty üyeleri, her ne kadar sessiz kalmış olsalar da, zaman alıcıdır. Segmentler listesinde **Başlangıç segmentleri ekle**'ye tıklayın ve Spwig, mağazanızın zaten sahip olduğu müşteri, loyalty ve ortak verilerinden yararlanarak hazır, düzenlenebilir dinamik segmentler oluşturur.

![Segmentler listesi ve Yeni Segment ve Başlangıç segmentleri ekle butonları](/static/core/admin/img/help/audiences/segments-changelist.webp)

| Başlangıç | Hedefler | Gereksinimler |
|---|---|---|
| **VIP müşteriler** | VIP müşteri segmentiniz | Etkin bir VIP müşteri segmenti |
| **Yüksek değerli müşteriler** | VIP ve Yüksek Değerli müşteri segmentleriniz | Etkin bir VIP veya Yüksek Değerli müşteri segmenti |
| **Tekrarlayan alıcılar** | Frekanslı Alıcı ve Düzenli müşteri segmentleriniz | Etkin bir Frekanslı Alıcı veya Düzenli müşteri segmenti |
| **Yeni müşteriler** | Yeni müşteri segmentiniz | Etkin bir Yeni müşteri segmenti |
| **Daha az aktif olanlar** | Daha önce sipariş vermiş ancak son 90 günde vermemiş müşteriler | Herhangi bir müşteri sipariş geçmişi |
| **Loyalty üyeleri** | Loyalty programınızda aktif olan herkes | Etkin bir loyalty programı ve üyeleri |
| **En yüksek loyalty seviyesi** | En yüksek seviyedeki loyalty üyeleriniz | En az bir tane etkin loyalty seviyesi |
| **Ortaklar** | Etkin ortak iş ortaklarınız | En az bir tane ortak |

Spwig, sadece sahip olduğu veri türleri için başlangıçları oluşturur — henüz bir loyalty programı olmayan bir mağaza, **Loyalty üyeleri** başlangıcını, kimseyi de eşleştiremeyecek boş bir başlangıçtan ziyade, basitçe oluşturmayacaktır. Spwig, eklediğini tam olarak doğrular, örneğin: "7 başlangıç segmenti eklendi: Yüksek Değerli Müşteriler, Tekrarlayan Alıcılar, Yeni Müşteriler, Daha az aktif olanlar, Loyalty üyeleri, En yüksek loyalty seviyesi, Ortaklar."

![Yeni eklenen başlangıç segmentlerini doğrulayan başarı mesajı](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

**Başlangıç segmentleri ekle**'ye birden fazla kez tıklamak güvenlidir. Spwig, zaten mevcut olan başlangıçları asla oluşturmaz, bu yüzden ilk kez loyalty programınızı kurduktan sonra tekrar tıklarsanız, sadece yeni mevcut olanları ekler — her şey zaten kurulmuşsa, sadece onu söyler.

![Tüm başlangıç segmentlerinin zaten mevcut olduğunu gösteren bilgi mesajı](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

İsterseniz bir başlangıç silin, **Başlangıç segmentleri ekle**'ye tekrar tıklarsanız onu geri getirmez — Spwig, bunu kendi başınıza sildiğinizi, yeniden yaratmaya çalışmadığınızı düşünerek, bir segment olarak görür.

Bir başlangıç, oluşturulduktan sonra sadece normal bir dinamik segment olur: kuralını incelemek, adını değiştirmek veya silmek için listeden açabilirsiniz, kendi başınıza oluşturduğunuz herhangi bir segment ile aynı şekilde.

## Bu segmentlerin aslında neyi kapsadığını öğrenin

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

Yukarıdaki müşteri, sadakat ve ortak (affiliate) koşulları yalnızca e-posta adresi bir müşteri hesabına bağlı olan aboneleri eşleştirir — anonim bir bülten kaydı, Spwig'in karşılaştırma yapabileceği bir sipariş veya sadakat geçmişi olmadığı için, doğru bir şekilde **Sadakat üyesi** veya **VIP** koşulunu eşleştiremez.

Müşterilerinizin çoğunun hesabı var ama henüz abone olmadılarsa, Spwig kurulumunuzu yöneten kişiden bir abone senkronizasyonu çalıştırmasını isteyin — bu işlem, mevcut her müşteri hesabı için tek adımda bir Abone kaydı oluşturur, böylece bu kitlelerin eşleştirilebilecek gerçek kişiler olur.

Bir segment kaç abone sayarsa sayar, bu sayı bir kampanyayı *alabilecek* kişileri tanımlar, alacak kişileri değil. Her gönderim yine de önce her abonenin kendi pazarlama onayını kontrol eder, bu nedenle bir segment asla bu onayın etrafından dolaşmanın bir yolu değildir.

## İpuçları

- Aynı kuralı elle oluşturmak yerine, bir başlangıç kitlesinden başlayın ve onu ayarlayın — oluşturulduktan sonra, bir başlangıç kitle, kendinizin oluşturduğu herhangi bir segmentten farklı değildir.
- **Sadakat üyesi**, **Ortak (Affiliate)** ve **Sipariş verdi** gibi Boole koşulları operatör veya değer gerektirmez — koşulu eklemeniz yeterlidir.
- Daha dar hedefleme için yeni alanları orijinalleriyle birleştirin, örneğin **Sadakat üyesi** ile **Pazarlamaya katıldı**, tek bir koşula güvenmek yerine.
- Bir segmentin kuralları, o zamandan beri kaldırılmış bir şeye atıfta bulunuyorsa — silinmiş bir müşteri segmenti, boşaltılmış bir etiket vb. — Spwig bunu kimseyi eşleştirmiyor olarak ele alır, tüm abone listenize geri düşmez. Bozuk hedefleme az gönderir; asla yanlışlıkla herkese göndermez.
- Bir segmentin üye sayısı eski görünüyorsa, hemen yeniden hesaplamak için açın ve tekrar kaydedin veya Segmentler listesinden **Üye sayılarını yeniden oluştur** toplu işlemini kullanın.
- Bir kural oluştururken canlı "eşleşen aboneler" sayısını izleyin — kaydetmeden önce, niyetinizden daha dar (veya geniş) bir koşulu yakalamanın en hızlı yoludur.