---
title: Mağaza Dashboard
---

Mağaza Dashboard, mağazanızın performansına dair tam bir bakış sağlar — gelir, siparişler, en iyi satan ürünler, ziyaretçi trafiği ve daha fazlası — hepsi bir yerde. Bunu kullanarak neyin satıldığını, müşterilerinizin nereden geldiğini ve mağazanızın zaman içinde nasıl bir trend izlediğini anlayabilirsiniz.

**Yönetim > Sistem Metrikleri**'ne gidin ve araç çubuğundan **Mağaza Dashboard**'a tıklayın.

![Mağaza Dashboard genel bakış](/static/core/admin/img/help/shop-dashboard/overview.webp)

## Zaman aralığı seçme

Dashboard, seçilen dönemle göreli tüm metrikleri filtreler. Sayfanın üstündeki dönem seçiciyi kullanarak aşağıdaki seçeneklerden birini seçin:

| Dönem | Ne gösterir |
|--------|---------------|
| Bugün | Bugün vs. dün |
| Bu hafta | Pazartesi ile bugün vs. geçen hafta |
| Bu ay | Bu ay vs. geçen ay |
| Bu yıl | Yıllık vs. aynı dönem geçen yıl |
| Geçen 30 gün | Kayan 30 günlük pencere |
| Geçen 90 gün | Kayan 90 günlük pencere |
| Özel | Belirli bir başlangıç ve bitiş tarihi girin |

Çoğu görünüm, geçmişteki eşdeğer dönemle bir **karşılaştırma** gösterir, bu sayede performansın iyileşip düştüğünü görebilirsiniz. Sadece mevcut rakamları görmek istiyorsanız **Karşılaştır** anahtarını kapatın.

## Eylem kartları

Dashboardın üstünde, şu anda dikkatinizi çekecek öğeleri vurgulayan eylem kartları yer alır:

- **Tamamlanmamış siparişler** — teslimatı bekleyen siparişler
- **Bırakılan sepetler** — müşteri ürün ekledi ancak ödeme tamamlamadığı oturumlar
- **Okunmamış mesajlar** — cevap bekleyen müşteri sorguları
- **Düşük stok uyarısı** — stokta azalan ürünler

Herhangi bir eylem kartına tıklayarak ilgili yönetici bölümüne doğrudan gidin.

## Satış performansı

Satış performansı bölümü, seçilen dönem için ana gelir rakamlarınızı gösterir:

- **Toplam gelir** — kesintilerden önceki brüt satışlar
- **Toplam siparişler** — tamamlanmış sipariş sayısı
- **Ortalama sipariş değeri** — gelir bölü sipariş sayısı
- **Net kâr** — gelir eksi ürün maliyeti ve giderler (ayarlandıysa)

Her rakam, karşılaştırma döneminden değişimini gösteren bir ok ve yüzde içerir.

## Zaman içinde satışlar grafiği

Ana grafik, seçilen dönem boyunca satışlarınızı veya siparişlerinizi çizer. Spwig, en faydalı gruplamayı otomatik olarak seçer:

- Kısa dönemler (haftaya kadar) gün gruplaması yapar
- Orta dönemler (üç aya kadar) hafta gruplaması yapar
- Uzun dönemler ay gruplaması yapar

Grafik üzerindeki **Grupla** kontrolünü kullanarak gruplamayı geçersiz kılabilirsiniz. Herhangi bir noktaya gelin ve o tarih için tam değeri görmek için üzerine gelin.

## En iyi satan ürünler

En iyi satan ürünler tablosu, seçilen dönemdeki en çok satan ürünleri gelir sırasına göre listeler. Her satır aşağıdaki bilgileri gösterir:

- **Ürün adı**
- **Satılan birim sayısı**
- **Üretilen gelir**

Bu, en iyi performans gösteren ürünleri belirlemek ve promosyonlara veya stok yenilenmesine odaklanmak için kullanışlıdır.

## Ziyaretçi analitiği

Ziyaretçi analitiği bölümü, mağazanıza gelen kişi sayısını ve davranışlarını gösterir:

- **Toplam ziyaretçiler** — mağaza ön yüzüne gelen benzersiz ziyaretçiler
- **Sayfa görüntüleme sayısı** — toplam görüntülenen sayfa sayısı
- **Bounce oranı** — sadece bir sayfa görüntüleyen ziyaretçilerin yüzdesi
- **Zaman içinde görüntüleme sayısı** — seçilen dönem boyunca trafiğin hacmini gösteren bir grafik

**Coğrafya** paneli, ziyaretçilerinizin nereden geldiğini, ülkeye ve (mevcut olduğunda) şehre göre ayrıntılı olarak gösterir.

## Trafik kaynakları

Trafik kaynakları paneli, ziyaretçilerin mağazanıza nasıl geldiğini gösterir:

| Kaynak | Açıklama |
|--------|-------------|
| Doğrudan | URL'nizi yazan veya favori bir işaretleyiciyi kullanan ziyaretçiler |
| Organik arama | Arama motorlarından gelen ziyaretçiler |
| Sosyal | Sosyal medya platformlarından gelen ziyaretçiler |
| Referans | Diğer sitelerden size bağlantı veren ziyaretçiler |
| E-posta | E-postalardaki bağlantıları tıklayan ziyaretçiler |

Bu bilgiyi, hangi pazarlama kanallarının en çok trafiği çektiğini anlamak ve nereye yatırım yapmanız gerektiğini belirlemek için kullanın.

## Dönüşüm funnel'ı

Dönüşüm funnel'ı, ziyaretçilerin alışverişe kadar nasıl ilerlediğini gösterir:

1. **Ziyaretçiler** — toplam benzersiz ziyaretçiler
2. **Ürün görüntülemeleri** — en az bir ürünün görüntülendiği ziyaretçiler
3. **Sepete ekle** — bir ürünün sepete eklendiği ziyaretçiler
4. **Ödeme sürecine başlama** — ödeme sürecine başlanan ziyaretçiler
5. **Tamamlanan siparişler** — sipariş verilen ziyaretçiler

Her adımdaki yüzdelik oran, düşüş oranını gösterir. "Sepete ekle" ve "Ödeme sürecine başlama" arasındaki büyük düşüş, ödeme akışınızda bir sürtünme olduğunu gösterir.

## Kupon performansı

Eğer kupon kampanyaları düzenliyorsanız, bu bölüm seçilen dönemdeki kuponların performansını gösterir:

- **Toplam kullanım** — kuponların kaç kez kullanıldığını gösterir
- **Toplam indirim** — uygulanan tüm kupon indirimlerinin toplamı
- **Kuponlu gelir** — kupon içeren siparişlerden elde edilen toplam gelir

## Müşteri segmentasyonu

Müşteri segmentasyonu paneli, müşteri tabanınızı gruplara ayırır:

- **Yeni müşteriler** — seçilen dönemde ilk satın alan müşteriler
- **Dönen müşteriler** — önce satın alan müşteriler
- **Hesapsız ödemeler** — hesap oluşturmadan yapılan siparişler

Yeni ve dönen müşterilerin oranı, daha fazla alım (pazarlama) veya müşteri tutma (oyalite programları) üzerine yatırım yapmaya karar vermenize yardımcı olur.

## Ortaklık ve sadakat özeti

Mağazanızda aktif bir ortaklık programı veya sadakat programı varsa, burada toplam komisyon kazançları, toplam puan dağıtımları ve en iyi performans gösteren ortaklar veya puan kullanıcılara özete alınır.

## İpuçları

- Haftanın başında kontrol panelini inceleyerek haftalık bir gözden geçirmeyi yapın — "Bu hafta" dönemine göre son dönem performansının net bir örneği alınır
- Belirli bir kampanyanın etkisini ölçmek için **Özel** tarih aralığını kullanın: kampanya döneminin başlangıç ve bitiş tarihlerini ayarlayın
- Eğer dönüşüm funnel'ı **Ödeme sürecine başlama** aşamasında büyük bir düşüş gösteriyorsa, ödeme akışınızı basitleştirmeyi veya güven belgeleri eklemeyi göz önünde bulundurun
- Yüksek sepet bırakma sayıları ve düşük dönüşüm oranları, fiyat veya kargo maliyeti sorununu gösterebilir — ödeme maliyetlerinizi gözden geçirin
- Yıllık karşılaştırmalar yapmak için **Bu yıl** dönemini kullanın, işinizde mevsimsel desenleri anlayabilirsiniz
- Büyük stoklama kararları vermeden önce, en iyi ürünler tablosunu dışa aktarın veya ekran görüntüsü alın, doğru miktarda sipariş verdiğinize emin olun