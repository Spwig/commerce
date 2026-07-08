---
title: İndirimlerin Birleştirilmesi
---

Platform, birbirleriyle çalışabilen dört tür indirim sunar: ürün satışı, kampanyalar, kupon kodları ve hediye kartları. Onların nasıl etkileştiğini anlamak, beklenmedik sonuçlar veya istenmeyen çift indirimler olmadan etkili kampanyalar düzenlemenize yardımcı olur.

## Dört İndirim Katmanı

Her indirim türü farklı bir seviyede çalışır ve müşterilere farklı şekillerde görünür.

| Katman | Nerede Ayarlanır | Nasıl Uygulanır | Müşteriye Görünür |
|-------|---------------|-----------------|-------------------|
| **Ürün Satışı** | Ürün düzenleme formu > Satış bölümü | Görünen fiyatı otomatik olarak değiştirir | Evet — orijinal fiyat olarak çizili gösterilir |
| **Kampanya** | Pazarlama > Satışlar & Kampanyalar | Uygun ürünleri otomatik olarak uygular | Evet — ürün kartlarında satış fiyatı olarak gösterilir |
| **Kupon Kodu** | Pazarlama > Kuponlar | Müşteri checkout sırasında bir kod girer | Kod girildikten sonra sadece checkout sırasında |
| **Hediye Kartı** | Satın alma sırasında hediye kartı bakiyesinden uygulanır | Ödeme toplamını azaltır | Sadece checkout sırasında |

## Öncelik Nasıl Çalışır

Kampanyalar, 0 ve üzeri değerler alan bir **Öncelik** alanına sahiptir. Daha yüksek sayılar daha yüksek önceliği ifade eder.

Aynı ürün için birden fazla kampanya eşleşiyorsa, **en yüksek öncelikli olan kazanır**. Onlar üst üste binmez — her ürün için sadece bir kampanya uygulanır.

**Örnek:** "Flash Sale 50% indirim" (öncelik 10) ve "Summer Sale 20% indirim" (öncelik 5) her iki kampanya da tüm ürünleri hedefler. Müşteri 50% flash sale fiyatını görür, 70% birleşik değil.

Aynı öncelik düzeyinde, sistem müşteriye en büyük indirimi sunan kampanyayı seçer.

## Birleştirme Kuralları

Aşağıdaki tablo, hangi indirim kombinasyonlarının izin verildiğini ve bunları nasıl kontrol edebileceğinizi gösterir.

| Kombinasyon | İzin Verilir mi? | Nasıl Kontrol Edilir |
|-------------|----------|-------------------|
| Ürün Satışı + Kampanya | Sadece etkinleştirilirse | Kampanyanın Gelişmiş Ayarlarında **"Ürün satışlarıyla birleştirilebilir"** işaretlemesini kontrol edin |
| Kampanya + Kampanya | Hayır — en yüksek öncelik kazanır | Öncelik değerlerini ayarlayarak hangisinin uygulanacağını kontrol edin |
| Kampanya + Kupon Kodu | Evet | Kampanya ürün fiyatını indirir, kupon sepet toplamını ayrı olarak indirir |
| Kupon + Kupon | Yapılandırılabilir | Kuponun **"Diğer kuponlarla birleştirilemez"** bayrağı bu durumu kontrol eder (varsayılan olarak etkinleştirilir) |
| Kupon + Satış Ürünleri | Yapılandırılabilir | Kuponun **"Satış ürünleri hariç tut"** bayrağı bu durumu kontrol eder |
| Hediye Kartı + Herhangi Bir İndirim | Evet — her zaman | Hediye kartları en son uygulanır, diğer tüm indirimlerden sonra ödeme miktarını azaltır |

## Ortak Senaryolar

### Senaryo A: Sitewide kampanya + kupon kodu

- **Ayarlamalar:** Her şeyde %20 indirim (kampanya) + müşteri $10 indirimli bir kupon kodu vardır
- **Sonuç:** $100 ürün $80 (kampanya) olur, ardından $10 kupon kodu sepet toplamına uygulanır. Müşteri **$70** öder.

### Senaryo B: Satışta olan ürün + sitewide kampanya

- **Ayarlamalar:** Ürün %30 ürün seviyesinde satışa sunulur + %20 sitewide kampanya mevcuttur
- **Sonuç (birleştirme devre dışı):** Sadece ürün satış uygulanır. Müşteri **$70** öder.
- **Sonuç (birleştirme etkin):** Her ikisi de uygulanır. İlk %30 indirim = $70, ardından %20 indirim = **$56**.

### Senaryo C: Aynı ürün üzerinde iki kampanya

- **Ayarlamalar:** "Flash Sale 40% indirim" (öncelik 10) + "Summer Sale 20% indirim" (öncelik 5), her ikisi de tüm ürünleri hedefler
- **Sonuç:** Flash Sale kazanır çünkü daha yüksek önceliği vardır. $100 ürün için müşteri **$60** öder.

### Senaryo D: Satışta olan bir ürüne kupon

- **Ayarlamalar:** Ürün %25 indirimle satışa sunulur. Müşteri "Satışta olan ürünleri hariç tut" etkin olan %10 kupon kodu girer.
- **Sonuç:** Kupon bu ürüne uygulanmaz. Eğer sepetin içinde satışta olmayan ürünler varsa, kupon sadece bu ürünler için uygulanır.

## Hangi İndirim Türünü Kullanmalısınız

| Hedef | Önerilen Yaklaşım | Neden |
|------|---------------------|-----|
| Mevsimsel stok hareketi | **Kampanya** (kategoriler veya koleksiyonlar hedefleme) | Otomatik, müşteri eylemi gerekmez, ürün kartlarında görünür |
| Belirli bir müşteriyi ödüllendirme | **Kupon Kodu** (tek kullanımlık, müşteri başına limit) | Hedefli, izlenebilir, kişisel his verir |
| Hızlı tek ürün teklifi | **Ürün Satışı** (ürün düzenleme formunda) | En hızlı kurulum, kampanya sihirbazına gerek yok |
| Mağaza kredisi veya hediye | **Hediye Kartı** | Bakiye tabanlı, müşteri kendi kredisini yönetir |
| Sitewide etkinlik | **Kampanya** (tüm ürünler hedefleme) | En yüksek erişim, tek kurulum her şeyi kapsar |
| Müşteri geri kazanma kampanyası | **Kupon Kodu** (ilk kez veya dönen müşteri kısıtlamaları) | Belirli müşteri gruplarını hedefleyebilir |

## İpuçları

- **Gerçek bir sepetle test edin** — kampanyalar ve kuponlar kurulumundan sonra, bir sepete ürünler ekleyin ve checkout sürecini takip ederek indirimlerin beklenen şekilde uygulanıp uygulanmadığını doğrulayın.
- **"Etkilenen ürünler" sayısını kontrol edin** — kampanya Gözden Geçirme adımda, etkilenen ürün sayısı kastedilenle eşleştiğini doğrulayın.
- **Öncelikleri dikkatli kullanın** — aynı anda birden fazla kampanya çalıştırıyorsanız, her zaman farklı öncelik değerleri ayarlayarak hangisinin kazanacağını kontrol edin.
- **Birleştirme özelliğini varsayılan olarak devre dışı bırakın** — sadece çift indirim istiyorsanız "Ürün satışlarıyla birleştirilebilir" özelliğini etkinleştirin.
- **Stratejinizi belgeleyin** — kampanya Açıklama alanını kullanarak bir kampanyanın neden mevcut olduğunu ve diğer etkin kampanyalarla nasıl ilişkili olduğunu not alın.