---
title: Gelir Atfı
---

Gelir Atfı, bir önceki tıklama yerine, bir müşterinin nereden geldiğinin tüm kanallarını da içeren satışların nereden geldiğini gösterir. Bir müşteri, sosyal medyada paylaştığınız bir blog yazısını okuyor, bir hafta sonra Google aramasından geri dönüyor ve ardından bir bülten bağlantısına tıklayarak satın alıyorsa, bu üç dokunma da bu satışa katkılarda bulunuyor. Bu panel, seçimlerinizin bir modelini kullanarak tümünü krediye tabir eder, bu sayede pazarlamanızın gerçek çalışma şeklinizi, "son tıklama kazanır" yaklaşımının nasıl çalıştığını iddia etmesinden ziyade, nasıl çalıştığını görebilirsiniz.

![Gelir Atfı panosu: Atfı seçimi, KPI bantındaki "Net gelire uyumlu" etiketi, kanala göre gelir, zamanla gelir, müşteri yolculuğu akışı ve kampanyalar tablosu](/static/core/admin/img/help/revenue-attribution/dashboard-overview.webp)

## Nerede Bulunur

Yan menüde **Görünüşler > Gelir Atfı**'na gidin. Görünüşler, Ürünler'in üzerindeki özel bir menü grubudur, bu yüzden Gelir Atfı, sipariş ve müşteri raporlarınızdan ayrı bir ev sahibiğine sahiptir.

Görünüşler, **Görünüşler ve Analiz** izin kategorisine göre sınırlıdır. Eğer yan menüde görünmüyorsa, bir mağaza yöneticisine bu izni vermelerini isteyin — çalışan rolleri ve izinleri hakkında bilgi için [Çalışan Rollerini ve İzinlerini](/help/staff-roles) kontrol edin.

## Çoklu Dokunma Atfı Hakkında Anlamak

Çoğu mağaza, bir siparişin nereden geldiğini düşünme alışkanlığına sahiptir, sanki tek bir cevap varmış gibi. Gerçek hayatta, müşteriler genellikle ilk ziyaretlerinde satın almayacaklardır. Birisi farklı bir yolla sizi keşfeder, başka bir yolla geri dner ve üçüncü bir yolla satın alır — bazen günler veya haftalar içinde birkaç ziyaret arasında.

Bu ziyaretlerin her biri bir **dokunma**dır: bir önceki tıklama yerine göre bir işaret taşıyan, mağazanıza gelen bir ziyaret.

**Çoklu Dokunma Atfı**, bu yolculuktaki her dokunmaya dikkat etmek ve son satış için ne kadar krediye sahip olduğunu belirlemek anlamına gelir, bu da son tıklamanın tüm kredisini vermek yerine. Bu, son tıklama raporlamasının, blogunuz, organik arama varlığı, sosyal gönderileriniz gibi erken keşfetme işini yapan kanalları sistematik olarak az değerli göstermesi nedeniyle önemlidir.

## Atfı Modeli Seçimi

Panonun en üstünde bulunan model değiştirme butonu, sayfadaki en önemli kontrol noktasıdır. Herhangi bir modeli tıklayın ve panodaki her sayı — KPI bantındaki, kanal çubukları, grafik, kampanyalar tablosu — anında kendi kendine yeniden krediye tabir eder. Bu, canlı bir önizlemedir: burada modelleri değiştirme, mevcut gelirinizin nasıl göründüğünü değiştirmeniz, kayıtlı bir modelinizi değiştirmeniz veya kaydetmeniz değildir.

![Atfı modeli değiştirme butonu - Son dokunma, İlk dokunma, Lineer, Zaman azalması ve Pozisyon 40/20/40 - "Yeniden atfı · yeniden işleme yapmaz" göstergesi](/static/core/admin/img/help/revenue-attribution/model-switcher.webp)

| Model | Ne işe yarar | En iyi olanlar | 
|-------|---------------|----------| 
| **Son dokunma** | Siparişe olan son kanala tam puan verir, ancak 

- **Takdim Edilen** her bir siparişün gelirini, seçtiğiniz modele göre parçalar, bu yüzden toplamalar, takdim edilen gelirin %100'üne eşit olur — aynı zamanda masaüstünde başka yerlerde de gösterilen rakamlar.
- **Etkileyen** her bir kanalı, bu siparişin *tam* değerine sahip olduğu ve her bir sipariş başına bir kez sayıldığı bir şekilde *her* siparişe yazar.

Bu amaçla %100'a ulaşmaz — bir kanal, başka bir kanal için tamamen sayılan gelirden etkilenmiş olabilir.

Bu, son tıklama raporlamasının tamamen gizlediği, bir blog yazısı veya bir sosyal paylaşım gibi, birinin son ziyaretinde tıklamadan ilgi duyduğu bir erişim alanını ortaya koymak içindir.

## Kampanyalar

**Kampanyalar** tablosu, etiketlenmiş kampanyalarınız için geliri, siparişleri ve ortalama sipariş değerini (AOV) açıklar — bağlantılar veya kodlar, kamuya açık bir isimle etiketlendiği, kampanya etiketli kupon kodları dahil (bkz. [Kupon Kampanyası İdealleri](/help/voucher-campaign-ideas)). Onları, hangi kanalın taşıyıp taşımadığına bakılmaksızın, bireysel tanıtım, influencer kodları veya pazarlama atışları gibi farklılıkların karşılaştırılması için kullanın.

## Tarih aralığı ve verilerin dışa aktarımı

Tarih aralığı seçicisini sağ üst köşede kullanarak **Son 7 gün**, **Son 14 gün**, **Son 30 gün**, **Son 90 gün** ve **Ay başından beri** arasında geçiş yapın. Tüm masaüstü, yeni periyot için yeniden yüklenir.

Seçili model ve tarih aralığı için kanal bölünümünü dışa aktarmak için **CSV'yi Dışa Aktar**'a tıklayın — sayıları bir tablo üzerine çekmek veya bir ortak ajansla paylaşmak için yararlıdır.

## Dokunmaların nasıl kaydedildiğine dair

Spwig, ziyaretçinin mağazanıza tanıdık bir kaynak sinyaliyle geldiğinde ve ziyaretçi, mağaza korsanın cookie bildiriminde **Analiz** izni verdiyse (eğer bir izin bildirimi kullanmıyorsanız, izin verilir, çünkü mağazanızın kendi politikası dikkate alındığında). Bu, mağaza eklentisinin analizleriyle aynı gizlilik düzeyinde kalmasını sağlar.

Birçok kaynak, hiçbir kurulum yapmanıza gerek kalmadan otomatik olarak etiketlenir:

| Kanal | Nasıl tanımlanır |
|---------|----------------------|
| **E-posta** | Pazarlık e-postalarınızda (sipariş veya kargo e-postaları değil) bulunan bağlantılar |
| **Organik / Paid Arama** | Arama motoru referansları, ya da bir pazarlık kampanyası olarak işaretlenen `utm_medium` değerleri |
| **Organik / Paid Sosyal** | Sosyal ağ referansları, ya da sosyal `utm_medium` değerleri |
| **Ajans** | Ajans programınız aracılığıyla oluşturulan bağlantılar |
| **Birini Tavsiye Et** | Müşteri teşviki programı aracılığıyla oluşturulan bağlantılar |
| **Kampanya** | Herhangi bir bağlantı veya kod, kampanya etiketi taşıyor, kampanya etiketli kupon kodları dahil |
| **Dış Bağlantı** | Başka bir web sitesinden gelen ve aksi şekilde kategorilenmemiş bir bağlantı |
| **Doğrudan** | Kaynak sinyeti bulunmamış — ziyaretçi adresi yazdı, bir yıldız ekledi ya da referansı olmayan bir uygulamadan geldi |

Bağlantılı sosyal hesaplarınıza otomatik olarak paylaşılan blog yazıları, otomatik olarak etiketlenir, bu nedenle onlar tarafından oluşturulan trafiğin doğru sosyal kanalda görünmesi ve doğrudan ya da dış bağlantıya kaybolmaması sağlanır.

Kendi bağlantılarınızı manuel olarak etiketleyebilirsiniz — Spwig tarafından otomatik olarak etiketlenmeyen her kanal için, mağazanıza giden herhangi bir URL'de standart `utm_source`, `utm_medium` ve `utm_campaign` parametrelerini kullanın — basılı materyaller, ortak bültenler ya da Spwig tarafından otomatik olarak etiketlenmeyen herhangi bir kanal için yararlıdır.

## Dikkat edilmesi gereken sınırlamalar

- **Takdim, bir tarayıcıya, bir kişiye göre değil.** Bir müşteri cep telefonunda araştırmakla laptopunda satın alırsa, izleme açısından iki ayrı yol olur — farklı cihazlar arasında aktiviteyi bağlama yolu yoktur.


Bu, bir önceki cihazdaki bir dokunma için 'sağlaması gereken' kredi miktarının Direct'e gideceği anlamına gelir.
- **Direct, izlenmeyen gelirin gittiği yerdir.** Yüksek bir Direct payı, insanların URL'nizi hafızadan yazmadığını göstermez — aynı zamanda bir müşterinin daha önceki dokunmalarının farklı bir cihazda olduğu ya da kullandığı bağlantının etiketlenmediği anlamına da gelebilir.
- **Reddedilen izin, hiçbir dokunmanın kaydedilmediği anlamına gelir.** Çerez banner'ınızda analiz izni reddeden ziyaretçiler, izlenmez, bu yüzden siparişleri Direct olarak görünür, ancak genellikle tanıdıklayabileceğiniz bir kanaldan geldiler.

## İpuçları

- **Son dokunma** altında zayıf gibi göründüğü için bir kanalın en güçlü keşif aracı olup olmadığını anlamak için **İlk dokunma** altında daha güçlü olabileceğini kontrol edin.
- **Direct**, gelirinizin büyük bir kısmını oluşturuyorsa, `utm_source`/`utm_medium`/`utm_campaign` ile etiketlenmemiş pazarlama bağlantılarınızın daha fazlasının olup olmadığını kontrol edin — etiketsiz trafiğin başka hiçbir yere gitmesi gerekmez.
- **İlgilendiren** lensi, sonraki tıklamayı almayan ama yolda sürekli ilk dokunmayı başlatan bir kanal gibi organik arama veya blog içeriği gibi kanallara yatırım yapıp yapmamayı karar verirken kullanın.
- **Ort. dokunma / sipariş** değerini zamana göre karşılaştırın — artan bir sayı, müşterilerin karar vermede daha uzun sürede olduğunu gösterir, bu da takip eden e-posta veya tekrar hedefleme zamanlaması planlaması için faydalı bir sinyaldir.
- **CSV** dosyasını, raporladığınız model ve dönem için **CSV'yi İndir** butonuna bastığınız an hangi modelin seçili olduğunu gösterdiğinden emin olmak için tekrar model değiştirmeden önce CSV'yi dışa aktarın.