---
title: İndirim Örnekleri
---

Bu kılavuz, farklı indirim türlerini nasıl yapılandıracağınızla ilgili somut örnekleri göstermektedir. Her örnek, indirim sihirbazında girmeniz gereken tam olarak alan değerlerini içerir, böylece kılavuzunuzu takip edebilir veya mağazanız için uyarlayabilirsiniz.

![Promotion Card](/static/core/admin/img/help/promotion-examples/promotion-card.webp)

## Örnek: Kategoriye Yüzde İndirim

**Senaryo:** Kışlık temizleme için tüm ayakkabılar için %30 indirim.

**Marketing > Sales & Promotions**'a gidin ve **+ Create Promotion**'a tıklayın. Sihirbazın her adımda aşağıdaki değerleri girin:

| Step | Field | Value |
|------|-------|-------|
| Basics | Name | Winter Clearance — 30% Off Shoes |
| Basics | Description | End-of-season clearance for all footwear |
| Basics | Active | Checked |
| Discount | Type | Percentage Off |
| Discount | Value | 30 |
| Schedule | Start Date | Jan 15, 2026 |
| Schedule | End Date | Feb 28, 2026 |
| Products | Apply To | Categories |
| Products | Selected | Shoes, Boots, Sandals |

Bu, seçilen kategorilerdeki her ürünün otomatik olarak indirimini uygulayan bir zaman sınırlı satış oluşturur. $120lık bir bot $84, $60lık bir çanta $42 olur.

## Örnek: Bir Koleksiyona Sabit Tutar İndirimi

**Senaryo:** Summer Essentials koleksiyonundaki ürünlerde $15 indirim.

| Step | Field | Value |
|------|-------|-------|
| Basics | Name | Summer Essentials — $15 Off |
| Basics | Active | Checked |
| Discount | Type | Amount Off |
| Discount | Value | 15.00 |
| Schedule | Start Date | Jun 1, 2026 |
| Schedule | End Date | (empty — no expiration) |
| Products | Apply To | Collections |
| Products | Selected | Summer Essentials |

> **Note:** $15 indirimi, her uygun ürün için ayrı ayrı uygulanır. $50lik bir ürün $35, $30lik bir ürün $15 olur. Bitiş Tarihi boş bırakıldığında, promosyonun sona ermesi gerekmez, bu nedenle promosyonun manuel olarak devre dışı bırakılana kadar süresiz olarak devam eder.

## Örnek: Temizleme için Sabit Satış Fiyatı

**Senaryo:** Tüm temizleme ürünleri için $9.99 fiyatına ayarla.

| Step | Field | Value |
|------|-------|-------|
| Basics | Name | Final Clearance — Everything $9.99 |
| Basics | Active | Checked |
| Discount | Type | Fixed Sale Price |
| Discount | Value | 9.99 |
| Schedule | Start Date | (today) |
| Products | Apply To | Collections |
| Products | Selected | Final Clearance |

> **Note:** Sabit Satış Fiyatı, orijinal fiyattan bağımsız olarak tam olarak satış fiyatını ayarlar. $75lik bir ürün ve $25lik bir ürün her ikisi de $9.99 olur. Bu, temizleme rafları veya aynı fiyat noktasında olmak isterseniz kullanışlıdır.

![Category Promotion](/static/core/admin/img/help/promotion-examples/category-promotion.webp)

## Doğru İndirim Türünü Seçme

| Type | How It Works | Best For | Example |
|------|-------------|----------|---------|
| **Percentage Off** | Fiyatı bir yüzde oranıyla azaltır | Fiyatları değişken olan genel satışlar | %20 indirim — $100 $80, $50 $40 olur |
| **Amount Off** | Sabit bir dolar tutarını çıkarır | Belirli bir dolar tasarruf mesajı olan promosyonlar | $15 indirim — $100 $85, $50 $35 olur |
| **Fixed Sale Price** | Tam olarak satış fiyatını ayarlar | Temizleme, eşit fiyatlandırma, "tüm ürünler $X" | $9.99 — orijinal fiyattan bağımsız olarak tüm ürünler $9.99 olur |

## Doğru Hedefi Seçme

| Target | How It Works | Best For |
|--------|-------------|----------|
| **All Products** | Mağazanızdaki tüm ürünleri etkiler | Sitewide satışlar, mağaza genelindeki etkinlikler |
| **Categories** | Seçilen kategorilerdeki tüm ürünleri etkiler | Departman satışları, mevsimsel temizleme türlerine göre |
| **Brands** | Seçilen markalardan tüm ürünleri etkiler | Marka ortaklıkları, marka özel etkinlikler |
| **Collections** | Seçilen koleksiyonlardaki tüm ürünleri etkiler | Seçilmiş promosyonlar, temalı satışlar |
| **Products** | Bireysel olarak seçilen ürünleri etkiler | El ile seçilmiş fırsatlar, sınırlı seçimler |

## Planlama Desenleri

Üç yaygın promosyon planlama deseni:

| Pattern | Start Date | End Date | Use Case |
|---------|-----------|----------|----------|
| **Immediate, ongoing** | Today | (empty) | Kalıcı fiyat düşürmeleri, uzun vadeli satışlar |
| **Date range** | Future date | Future date | Mevsimsel etkinlikler, bayram satışları |
| **Future start, no end** | Future date | (empty) | Belirli bir tarihte başlayan kalıcı fiyatlandırma |

Gelecekteki bir Başlangıç Tarihi ayarlayarak planlanmış bir promosyon oluşturabilirsiniz. Bu, promosyon panosunda **Planlanmış** sekmesinde görünür ve tarih gelince otomatik olarak etkinleşir. Bitiş Tarihi boş bırakıldığında, promosyonun manuel olarak devre dışı bırakılana kadar aktif kalır.

## İpuçları

- **Açıklayıcı isimler kullanın** — İndirim değerini ve hedefi isimde belirtin (örneğin, "Summer 20% Off Shoes") böylece panoda promosyonları hızlıca tanıyabilirsiniz.
- **Etkilenen ürün sayısını kontrol edin** — İnceleme aşaması, kaç ürünün indirimleneceğini gösterir. Sayı yanlış gibi görünüyor ise, hedefleme ayarlarınızı kontrol edin.
- **Küçükten başlayın** — Bir indirimi emin olamıyorsanız, daha küçük bir yüzdeyle başlayın ve gerekirse artırın.
- **Pazarlama için Tutar İndirimi kullanın** — "$15 indirim" somut bir tasarruf sağlar ve ilanlarda ve e-posta kampanyalarında kolayca iletilir.
- **Adil olmak için Yüzde İndirimi kullanın** — Yüzde indirimi fiyatla ölçeklenebilir, farklı fiyat noktalarında orantılı tasarruf sağlar.