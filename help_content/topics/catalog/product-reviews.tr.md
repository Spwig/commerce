---
title: Ürün Yorumları
---

Ürün yorumları, müşterilerin bir ürün hakkındaki deneyimlerini puanlamasını ve yazmasını sağlar. Onayladığınız yorumlar, mağaza arayüzünde ürün sayfasında görünür, bu da diğer alışverişçilerin ne alacaklarını kararlaştırmasına yardımcı olur. Spwig, hangi yorumların yayınlandığında tam kontrolü size verir; hiçbir şey onaylanmadan yayınlanmaz.

Yorumlar, yan menüde **Ürünler > Yorumlar** altında bulunur, burada bir grup olarak açılır: en üstteki bağlantı **Yorumlar Paneli**'ne gider, **Yorumları Düzenle** ise doğrudan yorum listesine gider.

## Yorumlar Paneli

Yorumlar panelini açmak için **Ürünler > Yorumlar**'a gidin — mağazanızdaki yorumların performansı hakkında tek sayfa genel bakış.

![Yorumlar Paneli](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

Üstte, altı KPI kartı yorum aktivitenizi özetler:

| Kart | Ne gösterir |
|---|---|
| **Toplam Yorum** | Her zaman onaylanmamış ya da onaylanmış tüm yorumlar |
| **Ortalama Puanlama** | Her yorumdaki ortalama yıldız puanı |
| **Onay Bekliyor** | Onaylamadan veya reddetmeden önce bekleyen yorumlar |
| **Onay Oranı** | Onayladığınız tüm yorumların oranı |
| **Doğrulanmış Alışveriş** | O ürün için onaylı bir sipariş olan müşterilerin yorumlarının oranı |
| **Yeni (30 gün)** | Son 30 gün içinde gönderilen yorumlar |

KPI'lar altında, üç grafik daha fazla ayrıntı verir:

- **Puan Dağılımı** — 1-5 yıldız aralığında kaç yorum olduğunu gösteren bir çubuk grafiği. Burada 1 yıldızlı yorumların bir araya gelmesi hemen incelemeye değer.
- **Yorum Miktarı (12 hafta)** — haftalık yorum sayılarını gösteren bir çizgi grafiği, bir kampanyadan sonra artışları veya dikkat çekmek için gerekli olan bir düşüşü tespit etmenize yardımcı olur.
- **Yorumcuların Alışveriş Kanalı** — her yorum arkasındaki *alışverişi* sağlayan pazarlama kanadını (doğrudan, e-posta, ücretli arama, organik sosyal medya vb.) gösteren bir donut grafiği. Bu, atıf verilerinizi yeniden kullanır ve hangi kanalların, daha sonra yorum yazan müşterileri getirdiğini görmek için gerçekten yararlıdır — ancak bu, müşterinin inceleme formunu nasıl bulduğunu kaydetmez. Spwig bunu ayrı olarak takip etmez; bu rehberin ilerleyen kısmında bulunan "Yolun neyi ve neyi içerdiğini" daha fazlasını inceleyin.

Panelin tamamını tamamlayan iki liste vardır:

- **En Çok Yorumlanan Ürünler** — her biri yorum sayısı ve ortalama puanı ile birlikte, doğrudan ürüne giden en çok yorumlanan ürünler.
- **Onay Bekliyor** — en son onay bekleyen yorumlar, bu nedenle panelde kalmadan doğrudan karar vermeniz gereken herhangi bir şeye atlayabilirsiniz.

## Yorum listesi

Her yorumu bir kart şeklinde görebilmek için **Yorumları Düzenle**'e (ya da **Ürünler > Yorumlar > Yorumları Düzenle**) tıklayın, listeden önceki filtrelerle.

![Filtreler ve onaylanmamış yorum kartlarıyla Ürün Yorumları listesi](/static/core/admin/img/help/product-reviews/review-list.webp)

Her kart, ürün küçük resmi, yorum başlığı, yıldız puanı, **Onaylandı**/**Bekliyor** etiketi, ilgili olduğunda **Doğrulanmış Alışveriş** etiketi, yorumun bir örneği ve kimin yazdığı ve ne zaman yazdığı bilgisini gösterir.

### Yorumları filtreleme

Listeyi daraltmak için filtre panelini kullanın:

- **Ara** — ürün adı, müşteri kullanıcı adı veya yorum başlığı ile eşleşir
- **Puanlama** — belirli bir yıldız puanına sahip yorumları gösterir (1 yıldızlı şikayetleri incelemek için yararlıdır)
- **Onay** — onaylananları ve bekleyenleri hızlıca ayırır
- **Doğrulanmış** — o ürün için onaylı bir siparişi olan müşterilerden gelen yorumları filtreler

Filtreleme, sayfayı yeniden yüklemeden anında çalışır.

## Yorumları onaylama ve reddetme

Yorumlar, onaylanmadıkça mağazanızda görünür olmaz. Tek tek ya da toplu olarak yorumları onaylayabilir ya da reddedebilirsiniz.

### Toplu eylemler

1. Yorum listesinde, işlem yapmak için ilgilendiğiniz yorumların yanındaki onay kutularını seçin
2. Eylem dropdown'undan **Seçilen Yorumları Onayla** ya da **Seçilen Yorumları Reddet**'i seçin
3. **Git**'e tıklayın

Bu, yeni yorumların tamamını işlemenin en hızlı yoludur.

### Tek tek yorum

1.

Bir yorum kartındaki düzenleme simgesine ya da başlığına tıklayarak yorumu açın
2.

Tüm markdown formatlamasını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

İnceleme sekmesinde, **Onaylandı**'yı kontrol edin ya da kaldırın
3.
Headerdaki onay butonuna tıklayarak kaydedin

## İnceleme düzenleme sayfası

Bir incelemeyi açmak, o incelemeye dayalı, bir ürün adı, yıldız puanı, **Onaylandı**/**Bekliyor** etiketi, ilgili olduğunda **Doğrulanmış Alışveriş** etiketi, incelemeyi kimin yazdığını ve ne zaman yazdığını ve bir stats satırı (**Puan**, **Yararlı Oy**, **Müşteri Siparişi**, **Yaşam Boyu Harcama**) içeren bir dashboard tarzı görünüm sunar. Aşağısında, detay dört sekmeye ayrılmıştır.

![İnceleme düzenleme sayfası — İnceleme sekmesi ve resim galerisi](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### İnceleme sekmesi

Bu, incelemeyi denetlediğiniz yerdir:

- **İnceleme Resimleri** — müşteri resim eklediyse, burada küçük resimlerin bir galerisi olarak görünür; herhangi bir küçük resme tıklayarak tam boyutlu resmi yeni bir sekmede açabilirsiniz. Fotoğraf incelemeleri, alışveriş yapanlar için güçlü bir güven belirtisi olduğu için, onu onaylamadan önce bir göz atmak iyi olur.
- **Puan**, **Başlık**, **Yorum** — müşteri tarafından gönderilen içerik
- **Onaylandı** — incelemenin mağazanızda görünür olup olmadığını kontrol eder
- **Doğrulanmış Alışveriş** — incelemeyi doğrulanmış bir alıcıdan gelen olarak işaretler; Spwig, bir ürün için tamamlanmış bir sipariş varsa (bkz. **Alışveriş** sekmesi), buna otomatik olarak ayarlar, ancak gerekirse buradan bunu geçersiz kılabilirsiniz
- **Resimler** — yukarıdaki galerinin arkasındaki resim URL'leri listesi; genellikle bu alanı değiştirmenize gerek yoktur, ancak bazı durumlarda (örneğin, çoklu resimli bir incelemeye ait bir resmi kaldırma) düzenlenebilir kalır

İncelemenin kelime metnini değiştiremezsiniz — onaylamak ya da reddetmek ve resimleri yönetmek, burada neye sahip olduğunuzun tümüdür.

### Müşteri & Seyahat sekmesi

![İnceleme düzenleme sayfası — Müşteri & Seyahat sekmesi](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

Bu sekme, incelemeyi kimin yaztığınıza dair bağlam sunar: toplam sipariş, yazdıkları inceleme sayısı, vermiş oldukları ortalama puan, müşteri olmaya ne kadar süredir sahip oldukları ve iletişim bilgileri, tam müşteri dosyasına açma bağlantısı ile.

Ardında, **Trafiğe Giriş Seyahati** - bu müşteriye mağazanıza nasıl ulaştıran kanallar, kampanyalar ve referrer'lar, atıf verilerinden alınan ve bir zaman çizelgesi olarak gösterilenler.

#### 

- Dashboard'da **Moderasyona Bekleyen** listesini ilk olarak kontrol edin — tam inceleme listesini açmadan neyin bir karar alması gerektiğini görmek için en hızlı yoldur
- **Puan Dağılımı** grafiğindeki aynı üründe 1 yıldızlı bir dizi inceleme, paketleme, ürün kalitesi veya listelenmiş metniniz hakkında inceleme yapmak için net bir işaret sayılır
- **Doğrulanmış** filtresini, sınırda olan incelemeleri nasıl eleceğine dair karar verirken kullanın — onaylanmış bir siparişten gelen müşteri geri bildirimi, herhangi bir tartışmada daha fazla ağırlık taşır
- İncelemeleri, kritik olanları da dahil olmak üzere hızlıca onaylayın — görünür bir olumsuz inceleme ve hiçbir yanıt olmaması, işlenmemiş bir şikayettekinden daha kötü görünebilir ve yavaşça onaylanan incelemeler, müşterilerin gelecekte geri bildirimde bulunmalarını engeller
- **Trafiğe Ait Yolculuk** veya dashboard'un **İnceleyicilerin Alışveriş Kanadı** grafiğini fazla okumayın — her ikisi de müşteri tarafından nasıl ulaştığını ve neyi aldığını açıklar, fakat incelemeyi yazmaya nasıl ulaştığını değil
- Fotoğraf içeren incelemeleri onaylamadan önce daha dikkatli bir şekilde inceleyin; gerçek müşterilerin ürün fotoğrafları, mağazanızdaki en çok ikna edici içeriğe sahip olanlardır