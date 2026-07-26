---
title: İndirimleri Birleştirme
---

Platform, birbirleriyle çalışabilen dört tür indirim sunar: ürün satışları, kampanyalar, kupon kodları ve hediye kartları. Onların nasıl etkileştiğini anlamak, beklenmedik sonuçlar veya istenmeyen çift indirimler olmadan etkili kampanyalar düzenlemenize yardımcı olur.

> **Hediye kartları henüz çevrimiçi ödeme sırasında uygulanamaz.** Aşağıda açıklanan tasarım — diğer tüm indirimlerden sonra hediye kartının uygulanması — o özellik sunulduğunda bu şekilde çalışacaktır. Şu anda bir hediye kartı sadece **Satış Noktası**'nda (Point of Sale) geri ödenemez. Dolayısıyla aşağıda açıklanan çevrimiçi mağaza etkileşimleri şu anda hediye kartları için geçerli değildir. Hediye kartları için geçerli durumu görmek için **Hediye Kartları** yardım konusuna bakın.

## Dört İndirim Katmanı

Her indirim türü farklı bir düzeyde çalışır ve müşterilere farklı şekillerde görünür.

| Katman | Nerede Ayarlanır | Nasıl Uygulanır | Müşteriye Görünür |
|-------|---------------|-----------------|-------------------|
| **Ürün Satışı** | Ürün düzenleme formu > Satış bölümü | Görüntülenen fiyatı otomatik olarak değiştirir | Evet — orijinal fiyat olarak çizili şekilde gösterilir |
| **Kampanya** | Pazarlama > Satışlar & Kampanyalar | Uygun ürünler otomatik olarak uygulanır | Evet — ürün kartlarında satış fiyatı olarak gösterilir |
| **Kupon Kodu** | Pazarlama > Kuponlar | Müşteri ödeme sırasında bir kod girer | Kod girildikten sonra sadece ödeme sırasında görünür |
| **Hediye Kartı** | Hediye kartı bakiyesi karşılanır | Ödeme toplamını azaltır | Şu anda sadece Satış Noktası'nda (Point of Sale) (yukarıdaki notu görün) |

## Öncelik Nasıl Çalışır

Kampanyalar, **Öncelik** alanına 0 ve yukarı değerleri kabul eden bir alan sunar. Daha yüksek sayılar daha yüksek önceliği ifade eder.

Aynı ürün için birden fazla kampanya eşleşirse, **en yüksek önceliğe sahip olan kazanır**. Onlar üst üste binmez — her ürün için sadece bir kampanya uygulanır.

**Örnek:** "Anlık Satış %50 indirim" (öncelik 10) ve "Yaz Kampanyası %20 indirim" (öncelik 5) her iki kampanya da tüm ürünleri hedefler. Müşteri %50 anlık satış fiyatını görür, %70 toplamı değil.

Aynı öncelik düzeyinde, sistem müşteriye en büyük indirimi sunan kampanyayı seçer.

## Üst Üste Binme Kuralları

Aşağıdaki tablo, hangi indirim kombinasyonlarının izin verildiğini ve bunları nasıl kontrol edebileceğinizi gösterir.

| Kombinasyon | İzin Verilir mi? | Nasıl Kontrol Edilir |
|-------------|----------|-------------------|
| Ürün Satışı + Kampanya | Sadece etkinleştirilirse | Kampanyanın Gelişmiş Ayarlarında **"Ürün Satışlarıyla Birleştir"** işaretini kontrol edin |
| Kampanya + Kampanya | Hayır — en yüksek öncelik kazanır | Öncelik değerlerini ayarlayarak hangisinin uygulanacağını kontrol edin |
| Kampanya + Kupon Kodu | Evet | Kampanya ürün fiyatını indirir, kupon sepet toplamını ayrı ayrı indirir |
| Kupon + Kupon | Yapılandırılabilir | Kuponun **"Diğer kuponlarla birleştirilemez"** bayrağı bu durumu kontrol eder (varsayılan olarak etkinleştirilir) |
| Kupon + Satış Ürünleri | Yapılandırılabilir | Kuponun **"Satış ürünleri hariç tut"** bayrağı bu durumu kontrol eder |
| Hediye Kartı + Herhangi Bir İndirim | Evet — her zaman | Hediye kartları, diğer tüm indirimlerden sonra uygulanır ve son ödeme miktarını azaltır. Şu anda sadece Satış Noktası'nda (Point of Sale) mümkündür — yukarıdaki notu görün |

## Ortak Senaryolar

### Senaryo A: Genel kampanya + kupon kodu

- **Ayarlamalar:** Her şeyde %20 indirim (kampanya) + müşteri $10 indirimli bir kupon kodu sahibi
- **Sonuç:** $100'lık bir ürün $80 (kampanya) olur, ardından $10 kupon kodu sepet toplamına uygulanır. Müşteri **$70** öder.

### Senaryo B: Satışta olan ürün + genel kampanya

- **Ayarlamalar:** Ürün %30 ürün seviyesinde satışa sunuluyor + %20 genel kampanya mevcut
- **Sonuç (üst üste binme devre dışı):** Sadece ürün satış uygulanır. Müşteri **$70** öder.
- **Sonuç (üst üste binme etkin):** Her ikisi de uygulanır. İlk %30 indirim = $70, ardından %20 indirim = **$56**.

### Senaryo C: Aynı ürün üzerinde iki kampanya

- **Ayarlamalar:** "Anlık Satış %40 indirim" (öncelik 10) + "Yaz Kampanyası %20 indirim" (öncelik 5), her ikisi de tüm ürünleri hedefler
- **Sonuç:** Anlık Satış kazanır çünkü daha yüksek önceliğe sahiptir. Müşteri $100'lık bir ürün için **$60** öder.

### Senaryo D: Satışta olan ürün üzerinde kupon

- **Ayarlamalar:** Ürün %25 indirimli satışta.

# Müşteri Kuponu Kullanımı

Müşteri, "Satış ürünleri hariç" seçeneği etkin olan %10'lık bir kupon kodu girer.
- **Sonuç:** Bu ürün için kupon uygulanmaz.

Sepette satış dışı ürünler varsa, kupon sadece bu ürünlere uygulanır.

## Hangi İndirim Türünü Kullanmalı

| Hedef | Önerilen Yaklaşım | Neden |
|------|---------------------|-----|
| Mevsimsel stok hareketi | **Promosyon** (kategorili veya koleksiyon hedefleme) | Otomatik, müşteri eylemi gerekmez, ürün kartlarında görünür |
| Belirli bir müşteriyi ödüllendirme | **Kupon Kodu** (tek kullanımlık, müşteri başına limit) | Hedefli, izlenebilir, kişisel his verir |
| Hızlı tek ürün indirimi | **Ürün Satışı** (ürün düzenleme formunda) | En hızlı kurulum, promosyon sihirbazına gerek yok |
| Mağaza kredisi veya hediye | **Hediye Çeki** | Bakiye tabanlı; şu anda sadece kasada kullanılabilir |
| Sitewide etkinlik | **Promosyon** (tüm ürünler hedefleme) | En geniş erişim, tek bir kurulum her şeyi kapsar |
| Müşteri geri kazanma kampanyası | **Kupon Kodu** (ilk kullanım veya dönen müşteri kısıtlamaları) | Belirli müşteri gruplarını hedefleyebilir |

## İpuçları

- **Gerçek bir sepetle test edin** — promosyonlar ve kuponlar kurulduktan sonra, bir sepete ürün ekleyin ve ödeme sürecini geçerek indirimlerin beklenen şekilde uygulanıp uygulanmadığını kontrol edin.
- **"Etkilenen ürünler" sayısını kontrol edin** — promosyonu gözden geçirme adımda, etkilenen ürün sayısı kastedilen amaçla eşleştiğinden emin olun.
- **Öncelikleri dikkatle kullanın** — birden fazla promosyon aynı anda çalışıyorsa, her zaman farklı öncelik değerleri ayarlayarak hangisinin kazanacağını kontrol edin.
- **Yığışmayı varsayılan olarak devre dışı bırakın** — sadece çift indirim istiyorsanız "Ürün Satışlarıyla Yığıştır" seçeneğini etkinleştirin.
- **Stratejinizi belgeleyin** — promosyon Açıklama alanını kullanarak promosyonun neden mevcut olduğunu ve diğer aktif promosyonlarla nasıl ilişkili olduğunu not alın.