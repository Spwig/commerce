---
title: Göç Sorun Giderme
---

Çoğu göç sorunsuz şekilde tamamlanır, ancak bağlantılar başarısız olabilir, içeri aktarımlar zaman aşımına uğrayabilir ve bazen bir çalışmanın yarısında durması da mümkündür. Bu konu, başarısız bir bağlantıya nasıl tanımlanacağını, içeri aktarma sırasında ilerleme günlüğünü nasıl okuyacağını ve — en önemlisi — bir şey yanlış gittiğinde gerçekten neler yapabileceğinizi, Yeniden Deney, İptal ve Geri Al komutlarının ne yaptığını kapsar.

## 2. Adımda Bağlantı Hataları

**Devam etmeden önce bağlantı testi** seçeneği varsayılan olarak etkindir ve ilk tanımlayıcı testidir — tüm sihirbazın geri kalanını onaylamadan önce kaynak platformunuzdaki kimlik bilgilerini doğrular. Başarısız olursa, hata mesajı genellikle şu durumlardan birini işaret eder:

- **WooCommerce** — Depo URL'sinde `https://` eksik veya sonuna bir yol segmenti eklenmiş; Yanlış yazılan veya yeniden oluşturulan Tüketici Anahtar/Secret; veya REST API anahtarının **WooCommerce > Ayarlar > Gelişmiş > REST API** bölümünde **Okuma** izni olmadan oluşturulmuş olması.
- **Shopify** — Depo Alan Adı `yourstore.myshopify.com` formatında değil; Yanlış uygulamadan alınan Client ID/Secret; veya en yaygın durum olarak, Dev Dashboard'da oluşturulan ama asla **yükümlülük** edilmemiş bir uygulama — bir uygulama sürümü oluşturmak yeterli değildir, özel dağıtım bağlantısına tıklamanız ve **Yükümlülük** butonuna tıklamanız gerekir. Spwig ayrıca, `read_products`, `read_customers` veya `read_orders` izinlerinin uygulamanın izinlerinde yer almadığı durumlarda da uyarı verir.
- **Magento 2** — Depo URL'si mağaza ön yüzüne değil API köküne işaret ediyor veya bir entegrasyon tokenı oluşturuldu ancak asla etkinleştirilmedi (**Kaydet > Etkinleştir > İzin Ver**).
- **SSL sorunları** — Geçersiz, öz imzalı veya yanlış yapılandırılmış sertifika, kimlik bilgileri kontrol edilmeden önce bağlantıyı başarısız kılar ve bu, kimlik doğrulama hatası yerine genel bir hata olarak görünür. Kimlik bilgileri doğruysa, sertifikayı kontrol edin.

Her bir düzeltmeden sonra bağlantı testini yeniden çalıştırın, birkaç kimlik bilgisi aynı anda değiştirmeyin — bu, hangisinin yanlış olduğunu izole eder.

## 5. Adımda Canlı Günlüğü Okuma

Bir içeri aktarma çalışırken, 5. adımda etkinlik günlüğü anlık olarak gösterilir. **Detayları Göster**'e tıklayarak, yalnızca mevcut adım özeti yerine, seviye ve mesaj olarak ayrı ayrı girdileri genişletin. İlerleme durmuş gibi görünürse, bu en hızlı şekilde ne olduğunu görmek için: bir veri türü için "atlandı" mesajlarının bir duvarı, genellikle "Mevcut öğeleri atla" seçeneğinin işe yaradığı anlamına gelir, hiçbir şeyin kilitlendiği anlamına gelmez.

Günlük görünümü yalnızca **en son 500 girdiyi** gösterir, bu nedenle büyük bir göç sırasında en eski girdiler hala aktarım devam ederken görünürden kaybolur. Bir veri türü tamamlandıktan sonra tam günlük gerekirse, sonuç sayfasındaki **Günlükleri İndir** kullanın — bu sınırlama yoktur.

## Başarısız Bir Göçün Gerçek Anlamı

Bir göç başarısız olursa, anlamanız gereken en önemli şey budur.

Bir göç başarısız olursa, tamamlanma sayfası açıkça ne olduğunu söyler: hata oluşmadan önce içeri aktarılan öğeler hâlâ mağazanızda, hiçbir şey otomatik olarak silinmez ve sorunu düzeltip içeri aktarmayı tekrar çalıştırırsanız, ilk kez içeri aktarılan öğeleri atlar. Bu, yüzeyde olduğu gibi alın. İçeri aktarma sırasında hiçbir adım, başarısızlık noktasına kadar başarıyla içeri aktarılan öğeleri (ürünler, kategoriler, müşteriler, siparişler, işin tamamladığı her şey) bir veritabanı işlemi içinde çalışmadığı için birim olarak geri alınmaz — bu öğeler, mağazanızda tam olarak oluşturuldukları gibi kalır. Başarısız bir göç, **kısmi** bir göçtür, iptal edilmiş bir göç değildir.

Başarısızlık ayrıca işi geri alınamaz hale getirir, bu yüzden **Geri Al** butonu başarısız bir **içeri aktarmada** kullanılabilir olmaz — yalnızca bir göç tamamlandığında görünür, ya da tamamlanmış bir göçün geri alınması kendisi yarıda başarısız olursa tekrar sunulur, böylece yeniden deneyebilirsiniz. Otomatik bir geri almayı en çok isteyeceğiniz durum — başarısız bir içeri aktarma — hâlâ tam olarak butonun sunulmadığı durumdur.

Yani, bir göç başarısız olursa:

1. **İçeri aktarılan verileri gözden geçirin**, Imported/Skipped/Failed sayılarını ve indirilen günlükleri kullanarak mağazanızdaki verilerle neyin aktarıldığını ve neyin aktarılmadığını bir resim oluşturun.

2. **Temizlik nasıl yapılacağını kararlaştırın.** Küçük miktarda kısmi veri için, bunları manuel olarak gözden geçirin ve normal admin listesi görünümlerinden istemediğiniz verileri silin.

Daha büyük ya da daha karmaşık bir kısmi aktarım için, verileri sıfırdan temizlemek ve yeniden başlamak, öğe öğe dengelemekten daha hızlı olabilir.

3. Hangi temizlik yolunu seçerseniz seçin, **Mevcut öğeleri atla** seçeneğini etkinleştirerek tekrar deneme işlemini yapın — bu, önceki denemede kalan verilerin tekrarlanmasını önler.

## Tekrar Deneyin

**Tekrar Deneyin**, aktarıma tamamen baştan başlar. İşin önceki sayaçlarını ve günlüklerini temizler ve her şeyi sıfırdan yeniden aktarır — başarısız olan denemenin durduğu yerden devam etmez. **Mevcut öğeleri atla** seçeneğini etkin tutun, böylece ilk denemede aktarılan öğeler ikinci denemede tekrarlanmaz.

Eğer bir geçiş 4 saatlik sınırı bulursa, göreceğiniz mesaj doğrudur: aktarıma tekrar başlatmak baştan başlar ve zaten aktarılan öğeleri atlar, durduğu yerden devam etme gibi bir geri alma işlemi değildir. 4 saatlik sınırı bulacak kadar büyük bir mağaza için, tüm işlemi tekrarlamak nadiren tamamlanır; bunun yerine, her bir çalıştırma sırasında adım 3'te daha az veri türü seçerek (örneğin, bir çalışırda ürünleri, diğerinde siparişleri) birkaç küçük geçiş yapın.

## İptal

**İptal**, çalışan bir geçiş için kullanılabilir ve bu, kontrol panelinde işi hemen başarısız olarak işaretler. Arka planda çalışan aktarıma görevini durdurur değildir — bu görev, doğal bir durma noktasına kadar çalışmaya ve veri yazmaya devam eder. İptal yaptıktan sonra aktarılan sayıların bir müddet daha artmaya devam etmesini bekleyin — temizlik yapmadan önce bu sayıların stabil hale gelmesini bekleyin, iptal butonuna tıkladığınız andaki sayılarla hareket etmekten kaçının.

## Duraklatma veya Devam Etme Yok

Spwig, bir işlemi duraklatıp daha sonra devam ettirmeyi desteklemez. Kontrol panelindeki **Devam Et** butonu farklı bir durum için kullanılır: bir geçiş, sihirbaz aracılığıyla yapılandırıldı ama hiç başlatılmadı. Bu, sihirbazı yapılandırma işlemini bıraktığınız yerden yeniden açar — zaten çalışan bir işleme değil.

## Geri Al

> **Uyarı:** Geri alma kalıcı ve yıkıcı bir eylemdir. Kullanmadan önce bu bölümü tamamen okuyun.

Geri alma, **tamamlanmış** bir göçte sunulur ve kendi geri alması daha önce yarıda başarısız olmuş bir göçte de tekrar sunulur (durum: **Geri Alma Başarısız**), böylece takılı kalmış bir geri alma yeniden denenebilir. Yalnızca içeri aktarmanın kendisinin oluşturduğunu kaldırır ve mağazanızın artık bağımlı olduğu her şeyi korur:

- İçeri aktarmadan sonra gerçek bir sipariş vermiş taşınan bir müşteri **korunur** — hesabı, adresleri, sadakat geçmişi ve mağaza kredisi kendisinde kalır ve bu gerçek sipariş dokunulmadan bırakılır. Yalnızca içeri aktarmanın oluşturduğu siparişler kaldırılır.
- Herhangi bir sipariş, paket, hediye kartı veya yapılandırıcı yuvası tarafından hâlâ referans verilen taşınan bir ürün **korunur**. Diğer müşterilere ait siparişler asla değiştirilmez — geri alma artık ilgisiz bir siparişten kalem çıkaramaz veya onu yanlış bir toplamla bırakamaz.
- Korunan her şey, ada ve sayıya göre, nedeniyle birlikte size raporlanır — örneğin "1 Ürün korundu, hâlâ bir sipariş kalemi tarafından referans veriliyor" — böylece hâlâ neyin orada olduğunu ve nedenini tam olarak bilirsiniz.
- İçeri aktarmanın oluşturduğu Affiliate'ler, komisyonlar ve ödemeler, içeri aktarmanın oluşturduğu affiliate hesaplarıyla birlikte **kaldırılır**. Zaten var olan bir müşteriye bağlı bir affiliate, hesabını korur; yalnızca affiliate kaydı gider.
- Sadakat geçmişi ve mağaza kredisi müşteriyi takip eder: müşteri kaldırılırsa kaldırılır, müşteri korunursa korunur.

Hâlâ mağaza uzantıları tarafından oluşturulan abonelik planlarını, fiyatlandırma katmanlarını veya rezervasyon kaynaklarını **kaldırmaz** — bunlar bir geri almadan sonra da kalır ve istemiyorsanız elle temizlenmesi gerekir.

Onaylamadan önce, onay sayfası tam olarak neyin kaldırılacağını ve neyin korunacağını gösteren bir önizleme sunar; bu, canlı verilerinize göre hesaplanır — **Evet, Göçü Geri Al** butonuna tıklamadan önce okuyun. Geri alma ardından tarayıcınızda değil, arka planda çalışır, bu yüzden sekmeyi kapatmak güvenlidir; tamamlandığında gerçekte neyin kaldırıldığının ve korunduğunun raporu için göçün durumunu kontrol edin.

Geri alma artık içeri aktarmanın oluşturduğunun ötesine geçmediği için, artık yalnızca aynı gün kullanılabilecek bir araç değildir — taşınan bir müşterinin gerçek siparişleri ve taşınan bir ürünün gerçek satışları, göçün üzerinden ne kadar zaman geçmiş olursa olsun korunur. Yine de kaldırdığı satırlar üzerinde kalıcı ve yıkıcı bir eylem olmaya devam eder, bu yüzden gelişigüzel değil bilinçli kullanın ve Spwig'in koruduğu ama gerçekten istemediğiniz her şeyi elle temizleyin.

Kullanılabilirlik açısından: Geri alma butonu, iş kaydı var olduğu sürece tamamlanmış bir göçün özeti üzerinde kalır — çoğu platform için sabit bir zaman sınırı yoktur. Magento bu durumun istisnasıdır ve belirli bir zaman penceresinden sonra geri alma kullanılabilirliği kaybolur, bu yüzden Magento üzerindeyseniz hızlıca karar verin. İş kayıtları herhangi bir takvime göre silinmez, bu nedenle kaydı kendiniz silmediğiniz sürece bir göç süresiz olarak geri alınabilir durumda kalır.

## Büyük mağaza stratejisi ve yavaş içeri aktarımlar

Bir mağaza kadar büyük ki tek bir çalıştırma 4 saatlik limite risk oluşturuyorsa:

- **Adım 3'te toplu boyutunu artırın** (en fazla 100'e kadar) — daha büyük toplular genellikle daha az yuvarlama seferi ve daha hızlı bir geçiş anlamına gelir.
- **Veri türüne göre göçü birden fazla çalıştırma arasında bölün** — kategoriler ve ürünler bir çalışırmada, müşteriler ve siparişler bir sonraki çalışırmada, her şeyi bir seferde değil.
- **İlk çalışırdan sonra her çalışırmada "Mevcut öğeleri atla" seçeneğini açık bırakın**, böylece tekrarlı çalışırmalar zaten başarılı olan şeyleri çoğaltmaz.
- **"Ürün resimlerini içeri aktar" seçeneğini kapatın.** Her resmin indirilmesi ve işlenmesi genellikle yavaş çalışırmaların tek en büyük etkenidir. Diğer veriler yerine koyulduktan sonra, ürünlerin resimlerini bireysel olarak veya ayrı bir CSV içeri aktarımıyla ekleyebilirsiniz.

## İpuçları

- **Her kimlik bilgisi değişikliğinden sonra bağlantı testini yapın**, değil sadece sonunda — bu, hangi değer yanlış olduğunu izole eder.
- **Başarısız bir işin kendini temizlediğini varsaymayın** — temizleme veya tekrar denemeye karar vermeden önce mağazanızda gerçekten ne olduğunu kontrol edin.
- **"Mevcut öğeleri atla" seçeneği her tekrar denemede açık bırakılmalıdır** — ikinci geçişte çoğalma önleyen tek şeydir.
- **4 saatlik limite daha fazla tekrar denemeyle direnmeyin** — bunun yerine veri türüne göre bölün.
- **Onaylamadan önce geri alma önizlemesini okuyun** — bu, canlı verilerinize göre kaldırılacak ve korunacak şeyin tam adını verir, bu yüzden hiçbir sürpriz olmaz.