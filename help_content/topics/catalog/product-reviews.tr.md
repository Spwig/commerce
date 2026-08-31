---
title: Ürün Yorumları
---

Ürün yorumları, müşterilerin bir ürün hakkındaki deneyimlerini puanlamasını ve yazmasını sağlar. Onayladığınız yorumlar, mağaza arayüzünde ürün sayfasında görünür, bu da diğer alışverişçilerin ne alacaklarını kararlaştırmalarına yardımcı olur. Spwig, hangi yorumların yayınlandığında tam kontrolü size verir; onaylayana kadar hiçbir şey yayınlanmaz.

Yorumlar, yan menüde **Ürünler > Yorumlar** altında bulunur, burada bir grup olarak açılır: en üstteki bağlantı **Yorumlar Paneli**'ne gider, **Yorumları Düzenle** ise doğrudan yorum listesine gider.

## Yorumlar Paneli

Yorumlar Paneli'ne **Ürünler > Yorumlar**'a giderek erişilebilir — mağazanızdaki yorumların nasıl işlediğine dair tek sayfa özetini sunar.

![Yorumlar Paneli](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

Üstte, altı KPI kartı yorum aktivitesini özetler:

| Kart | Ne gösterir |
|---|---|
| **Toplam Yorum** | Her zaman verilen tüm yorumlar, onaylanan veya onaylanmayan |
| **Ortalama Puanlama** | Her yorumdaki ortalama yıldız puanı |
| **Onay Bekliyor** | Onaylamadan veya reddetmeden önce bekleyen yorumlar |
| **Onay Oranı** | Onayladığınız tüm yorumların oranı |
| **Doğrulanmış Alışverişler** | O ürün için onaylı bir siparişle alışveriş yapan müşterilerin oranı |
| **Yeni (30 gün)** | Son 30 gün içinde gönderilen yorumlar |

KPI'lar altında, üç grafik daha fazla ayrıntı verir:

- **Puan Dağılımı** — 1-5 yıldız aralığında kaç yorum olduğunu gösteren bir çubuk grafiği. Burada 1 yıldızlı yorumların bir araya gelmesi, hemen incelemek gerekir.
- **Yorum Miktarı (12 hafta)** — haftalık yorum sayılarını gösteren bir çizgi grafiği, bir kampanyadan sonra artışları veya dikkat çekmeyi gerektiren düşüşleri tespit etmenize yardımcı olur.
- **Yorumcunun Alışveriş Kanunu** — her yorum arkasındaki *alışverişi* sağlayan pazarlama kanalı (doğrudan, e-posta, ücretli arama, organik sosyal medya vb.) olan bir donut grafiği. Bu, atıf verilerinizi yeniden kullanır ve hangi kanalların müşteri getirdiğini görmek için gerçekten yararlıdır — ama bu, müşterinin inceleme formunu nasıl bulduğunu kaydetmez. Spwig bunu ayrı olarak takip etmez; bu rehberin ilerleyen kısmında daha fazla 

On the **Review** tab, check or uncheck **Is approved**
3.

Click the checkmark button in the header to save

## The review edit page

Opening a review gives you a dashboard-style view built around that one review — a header with the product name, the star rating, an **Approved**/**Pending** badge, a **Verified Purchase** badge when it applies, who wrote the review and when, and a stats row (**Rating**, **Helpful Votes**, **Customer Orders**, **Lifetime Spend**). Below that, the detail is organised into four tabs.

![Review edit page — Review tab with image gallery](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Review tab

This is where you moderate the review itself:

- **Review Images** — if the customer attached photos, they appear here as a thumbnail gallery; click any thumbnail to open the full-size image in a new tab. Photo reviews are a strong trust signal for shoppers, so this is worth a glance before you approve.
- **Rating**, **Title**, **Comment** — the content the customer submitted
- **Is approved** — controls whether the review is visible on your storefront
- **Is verified purchase** — flags the review as coming from a confirmed buyer; Spwig sets this automatically when a fulfilled order for the product exists (see the **Purchase** tab), but you can override it here if needed
- **Images** — the underlying list of image URLs behind the gallery above; you don't normally need to touch this, but it stays editable for edge cases (for example, removing one photo from a multi-image review)

You cannot edit the review's wording — approving or rejecting, and managing images, is the extent of what you control here.

### Customer & Journey tab

![Review edit page — Customer & Journey tab](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

This tab gives you context on who left the review: total orders, how many reviews they've written, their average rating given, how long they've been a customer, and their contact details, with a link to open their full customer record.

Below that sits the **Traffic-source journey** — the channels, campaigns, and referrers that brought this customer to your store, pulled from your attribution data and shown as a timeline.

#### What the "journey" does and doesn't tell you

Read this timeline as the customer's **arrival and purchase journey** — how they originally found your store and went on to buy. It is **not** a record of the visit in which they wrote this review. Spwig does not track where a customer was, or what device or session they used, at the moment they submitted a review. If the timeline shows "Email > summer-skincare" three weeks before the review date, that tells you the email campaign likely drove the *purchase* — it says nothing about whether the customer came back from a search result, a bookmark, or a follow-up email to actually leave the review. Treat this tab as useful marketing context, not as a literal trace of the review submission.

### Purchase tab

![Review edit page — Purchase tab](/static/core/admin/img/help/product-reviews/review-edit-purchase-tab.webp)

This tab lists every order in which the customer bought the reviewed product — order number, date, total, status, and the purchase channel for that order. If any of those orders has reached a fulfilled status (shipped or delivered), you'll see a confirmation note that this is a verified purchase — the same signal that sets **Is verified purchase** automatically on the Review tab.

If no matching order appears here, the reviewer either bought the product before your store tracked orders in Spwig, or they never actually purchased it — worth knowing before you decide how much weight to give the review.

### Advanced tab

Metadata you rarely need to touch: **Helpful Count** (how many customers marked the review as helpful), import provenance if the review was migrated from another platform, and the created/updated timestamps.

## Tips

- Dashboard'da **Moderasyona Bekleyen** listesini mutlaka kontrol edin — tam inceleme listesini açmadan neyin bir karar alması gerektiğini görmek için en hızlı yoldur
- **Puan Dağılımı** grafiğindeki aynı üründe 1 yıldızlı bir dizi inceleme, paketleme, ürün kalitesi veya listelenmiş metniniz hakkında inceleme yapmak için net bir işaret sayılır
- **Doğrulanmış** filtresini, sınırda olan incelemeleri nasıl elececeğinizi kararlaştırmak için kullanın — onaylı bir siparişle gelen müşteri geri bildirimi, herhangi bir tartışmada daha fazla ağırlık taşır
- İncelemeleri, kritik olanları da dahil olmak üzere hızlıca onaylayın — görünür bir olumsuz inceleme ve hiçbir yanıt olmazsa, ele alınmış bir şikayette daha kötü görünebilir ve yavaşça ortaya çıkan incelemeler, müşterilerin gelecekte geri bildirimde bulunmalarını engeller
- **Trafiğe Ait Yolculuk** veya dashboard'un **İnceleyicilerin Alışveriş Kanadı** grafiğini fazla okumayın — her ikisi de müşteri nin nasıl ulaştığını ve neyi aldığını açıklar, inceleme yazmak için nasıl ulaştığını değil
- Fotoğrafı olan incelemeleri onaylamadan önce daha dikkatli bir şekilde inceleyin; müşteri tarafından çekilmiş ürün fotoğrafları, mağazanızdaki en çok ikna edici içeriğe sahip olanlardan biridir