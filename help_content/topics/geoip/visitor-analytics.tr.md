---
title: Ziyaretçi Analitiği
---

Ziyaretçi Analitiği, müşterilerin mağazanızda nasıl hareket ettiğini açık bir şekilde gösterir. Hangi sayfaların en çok ziyaret edildiğini, toplam trafikin zaman içinde nasıl değiştiğini, müşterilerin hangi cihazları kullandığını ve yeni ziyaretçilerle geri dönen ziyaretçilerin karşılaştırılmasını görebilirsiniz — bunun için harici analitik araçlara ihtiyaç duymadan.

## Analitik ekranların genel bakışı

Mağazanız, GeoIP sistemi etkin olduğunda ziyaretçi aktivitesini otomatik olarak izler. Veriler, her birinin farklı bir detay seviyesi sunan üç farklı görünümde düzenlenir.

### Günlük trafik özeti

**Müşteriler > Günlük Trafik İstatistikleri** menüsüne giderek mağazanızın her gün için genel trafik durumunu görebilirsiniz. Her satır, bir takvim gününe karşılık gelir ve aşağıdaki bilgileri gösterir:

| Sütun | Ne anlatır |
|--------|-------------------|
| **Tarih** | Trafikin kaydedildiği gün |
| **Toplam Görüntüleme** | Tüm sayfa görüntüleme sayıları, botlar dahil |
| **Benzersiz Ziyaretçiler** | Oturum bazında benzersiz ziyaretçiler |
| **Bot Görüntüleme** | Botlar ve otomatik araçlar tarafından yapılan görüntüleme |
| **Yeni Ziyaretçiler** | Önceki tarihlerde bir geçmişe sahip olmayan oturumlar |
| **Geri Dönen Ziyaretçiler** | Önceki ziyaretlerde görülen ziyaretçilerin oturumları |
| **Masaüstü Görüntüleme** | Masaüstü tarayıcılarından yapılan görüntüleme |
| **Mobil Görüntüleme** | Mobil cihazlardan yapılan görüntüleme |
| **Tablet Görüntüleme** | Tablet cihazlardan yapılan görüntüleme |

Listenin en üstündeki tarih hiyerarşisi navigasyonu ile belirli bir ay veya yıla hızlıca geçiş yapabilirsiniz. Toplamlar, otomatik bir arka plan süreciyle günde bir güncellenir, bu nedenle şu anki günün verileri bir sonraki sabah görünecektir.

### Sayfa bazlı istatistikler

**Müşteriler > Günlük Sayfa İstatistikleri** menüsüne giderek bireysel sayfalar bazında trafik analizini yapabilirsiniz. Her satır, bir gün içinde bir URL yolunu gösterir, bu da belirli sayfaların zaman içindeki performansını karşılaştırmanıza olanak tanır.

| Sütun | Ne anlatır |
|--------|-------------------|
| **Tarih** | Bu istatistiklerin geçerli olduğu gün |
| **URL Yolu** | Normalleştirilmiş sayfa yolu (örneğin, `/products/blue-widget`) |
| **Görünümler** | O gün içinde bu sayfa için toplam görüntüleme sayısı |
| **Benzersiz Ziyaretçiler** | Bu sayfayı görüntüleyen benzersiz ziyaretçiler |
| **Bot Görüntüleme** | Bu sayfada botlar tarafından yapılan görüntüleme |
| **Girişler** | Bu sayfadan başlayan oturum sayısı (bu sayfa ziyaretçinin giriş sayfasıydı) |

**URL Yolu** arama kutusunu kullanarak belirli bir sayfa için istatistikleri bulabilirsiniz. Örneğin, `/products/` için arama yaparak tüm ürün sayfa trafiğini görebilirsiniz veya belirli bir ürün slug'ı için arama yaparak tek bir ürün üzerinde odaklanabilirsiniz.

### Bireysel sayfa görüntüleme olayları

**Müşteriler > Sayfa Görüntüleme** menüsüne giderek izlenebilir her sayfa navigasyonunun ham bir kaydını görebilirsiniz. Bu kayıt sadece okunabilir olup, giriş veya düzenleme yapılamaz. Bu, belirli oturumları incelemek veya izlemenin doğru kaydedildiğini doğrulamak için kullanılabilir.

Her kayıt aşağıdaki bilgileri gösterir:
- **URL Yolu** — ziyaret edilen sayfa
- **Oturum** — ziyaretçinin oturumuna kısa bir kimlik
- **Kaynak** — ziyaretin başsız frontend'den mi yoksa standart mağaza ön yüzünden mi geldiğini belirtir
- **Bot mu?** — ziyaretçinin otomatik trafiğe mi tanımlandığını belirtir
- **Giriş Sayfası mı?** — bu sayfanın ziyaretçinin oturumundaki ilk sayfa olup olmadığını belirtir
- **Zaman Damgası** — ziyaretin tam zamanı

**Bot mu?**, **Kaynak** ve **Giriş Sayfası mı?** filtrelerini yan panel filtreleri kullanarak filtreleyebilir ve en üstteki tarih hiyerarşisi kullanarak tarih bazında navigasyon yapabilirsiniz.

## Trafik eğilimlerini okuma

Günlük trafik özeti, eğilimleri tespit etmenin en iyi aracıdır. Aşağıdaki desenleri inceleyin:

- **Trafik zirveleri**, bir kampanya yürüttükten veya pazarlama e-postası gönderdikten sonra
- **Kademeli büyüme**, mağazanızın organik görünürlüğün artmasıyla haftalar ve aylar boyunca
- **Hafta sonu vs. hafta içi desenleri**, müşterilerin en aktif olduğu zamanları anlamak için
- **Mobil vs. masaüstü bölünmeleri**, mobil optimize tasarım değişikliklerini önceliklendirip önceliklendirmemenizi kararlamak için

**Yeni Ziyaretçiler** ve **Geri Dönen Ziyaretçiler** sütunları birlikte, müşterilerin ne kadar iyi korunduğunu gösterir. Sağlıklı bir mağaza genellikle her ikisinin bir karışımını görecektir — yeni ziyaretçilerin yüksek bir oranı güçlü bir kazanç gösterirken, geri dönenlerin daha yüksek bir oranı müşteri sadakatiinin gelişmeye başladığını gösterir.

Sayfa başına istatistik görünümü, varsayılan olarak görüntüleme sayısına göre azalan sırada, herhangi bir günde en çok trafik oluşturan sayfaları hemen gösterir.

Arama yap:

- **Yüksek giriş, düşük görüntüleme sayfası** — arama veya reklamlardan ziyaretçilerin geldiğini ancak dikkat çekmeyen sayfalar
- **Yüksek görüntüleme sayfası ve birçok benzersiz ziyaretçi** — popüler hedef sayfalar, güncellenmesi değerli sayfalar
- **Görüntüleme sayısında artış gösteren ürün sayfaları** — arama görünürlüğü kazanmaya başlayan ürünler

### Örnek: bir ürünün trafikini bulma

En çok satan ürünün geçen hafta ne kadar trafik aldığını görmek için:

1. **Müşteriler > Günlük Sayfa İstatistikleri**'ne gidin
2. Tarih hiyerarşisini kullanarak ilgili haftayı seçin
3. Arama kutusuna ürünün URL slug'ını girin (örneğin, `/blue-widget`)
4. Gösterilen günler boyunca **Görüntüleme**, **Benzersiz Ziyaretçi** ve **Giriş** sayısını inceleyin

## Ziyaretçi konum verileri

**Müşteriler > Ziyaretçi Konumları**'na giderek ziyaretçilerinizin nerede bulunduğunu oturum düzeyinde görebilirsiniz. Her kayıt bir ziyaretçi oturumunu temsil eder ve şunları içerir:

- Ülke ve şehir (GeoIP sistemi tarafından otomatik olarak çözülür)
- Cihaz türü (masaüstü, mobil, tablet)
- Ziyaretçi tarafından seçilen para birimi ve dil tercihleri
- UTM kampanya ataması (kaynak, orta, kampanya adı)
- Bot ve yönetici trafik bayrakları

Ülkeye, cihaz türüne, UTM kaynağına ve onların bot olup olmadığını ya da yönetici personeli olup olmadığını göre göre filtreleyebilirsiniz. **Bot mu?** filtresini false olarak ayarlayarak gerçek müşteri trafiklerine odaklanın ve **Yönetici Trafik mi?** filtresini kullanarak kendi test oturumlarınızı analizden dışlayabilirsiniz.

## İpuçları

- Bot görüntüleme ayrı ayrı izlenir ve benzersiz ziyaretçi sayımından otomatik olarak çıkarılır — trafik rakamlarınız gerçek müşteri etkinliklerini yansıtır
- Sayfa başına istatistiklerdeki **Girişler** sütunu, arama ve reklamlar aracılığıyla mağazanızın ön kapısını oluşturan sayfaları gösterir; bu sayfaları optimize etmek en büyük etkiyi sağlar
- Ziyaretçi konumlarını **UTM Kaynak**'a göre filtreleyerek, belirli bir pazarlama kanalının (örneğin, bir e-posta bülteni veya Google reklamı) gerçekten ne kadar trafik gönderdiğini ölçebilirsiniz
- Günlük istatistikler gece yarısı toplanır — aynı günün trafikini kontrol etmeniz gerekiyorsa, doğrudan Sayfa Görüntüleme Günlüğü'ni kullanın
- Günlük özeti içindeki cihaz analizi, tasarım çalışmalarınızı önceliklendirmenize yardımcı olur; ziyaretlerin yarısından fazlası mobil cihazlardan geliyorsa, ürün sayfalarınız ve ödeme sürecinizin küçük ekranlarda da iyi göründüğünden emin olun