---
title: Ayarlanabilir Ürünler
---

Ayarlanabilir ürünler, müşterilerin farklı yapılandırma kutularından seçenekler seçerek kendi ürünlerini oluşturmasına olanak tanır. Bu, özel bilgisayarlar, kişiselleştirilmiş hediye kutuları veya özel siparişli mobilya gibi her bileşenin kataloğunda gerçek bir ürün olan "siparişe göre üretilecek" ürünler için idealdir.

![Ürün yapılandırıcısı yönetici](/static/core/admin/img/help/configurable-products/product-configurator.webp)

## Nasıl Çalışır

Bir yapılandırılabilecek ürün, **kutular** (seçenek kategorileri) ve **seçenekler** (müşterilerin seçebilecekleri gerçek ürünler) içerir. Örneğin, özel bir bilgisayarın işlemci, ekran kartı, RAM ve depolama için kutuları olabilir — her kutu, seçilecek birkaç ürün seçeneği içerir.

## Fiyatlandırma Stratejileri

Son fiyatın nasıl hesaplanacağına karar verin:

| Strateji | Açıklama |
|----------|-------------|
| **Bileşenlerin Toplamı** | Son fiyat = tüm seçilen seçenek fiyatlarının toplamı. Temel fiyat gerekmez. |
| **Temel Fiyat + Düzenlemeler** | Ürünün temel fiyatından başlayarak, her seçenek için fiyat düzenlemeleri ekleyin/çıkarın. |
| **Sabit Fiyat** | Müşterinin hangi seçenekleri seçtiğine bakılmaksızın tek bir sabit fiyat. |

## Yapılandırılabilir Ürün Kurulumu

### Adım 1: Ürün Oluşturun

1. **Ürünler > Tüm Ürünler**'e gidin ve **+ Ürün Ekle**'ye tıklayın
2. **Ürün Türünü** **Yapılandırılabilir Ürün** olarak ayarlayın
3. **Fiyatlandırma Stratejisi**'ni seçin (Bileşenlerin Toplamı en yaygınıdır)
4. Ürün adını, açıklamasını ve diğer temel detayları doldurun
5. Ürünü kaydedin

### Adım 2: Yapılandırma Kutuları Ekle

Kaydetme işleminden sonra, **Yapılandırma** sekmesine geçerek kutularınızı ayarlayabilirsiniz.

1. **+ Kutu Ekle**'ye tıklayarak yeni bir yapılandırma kategorisi oluşturun
2. Her kutu için yapılandırın:
   - **Ad** — Müşterinin gördüğü (örneğin, "İşlemci", "Renk")
   - **Simge** — Görsel tanımlamak için Font Awesome simge sınıfı
   - **Gerekli** — Müşterinin bir seçim yapması gerekir mi
   - **Min/Max Seçim Sayısı** — Müşterinin seçebileceğin seçenek sayısı (varsayılan: tam olarak 1)
   - **Sıra Numarası** — Yapılandırma sihirbazında kutuların görüneceği sırayı kontrol eder

### Adım 3: Her Kutuya Seçenekler Ekle

Her kutu, müşterilerin seçebileceği ürün seçeneklerine ihtiyaç duyar:

1. Bir kutunun **Seçenekleri Yönet**'ine tıklayın
2. Kataloğundaki mevcut ürünleri ara ve ekleyin
3. Her seçenek için yapılandırın:
   - **Fiyat Düzenlemesi** — Ekleyeceğiniz veya çıkaracağınız miktar (Temel + Düzenlemeler fiyatlandırma ile kullanılır)
   - **Varsayılan** — Yapılandırıcı yüklendiğinde bu seçeneği öntanımlı olarak seç
   - **Popüler** — Müşterilerin karar vermesine yardımcı olmak için "Popüler" bir etiket göster
   - **Miktar** — Bu bileşenin içerdiği birim sayısı
   - **Uyumluluk Etiketleri** — Toplu uyumluluk kuralı oluşturmak için kullanılan etiketler

**İpucu:** Bileşen ürünleri, bileşen ürünün temel bilgi sekmesinde **Mağazadan Gizle** seçeneğini işaretleyerek mağazadan gizlenebilir. Bu, onları yapılandırma seçenekleri olarak kullanılabilir hâle getirirken ürün kataloğunu kirletmeden tutar.

### Adım 4: Uyumluluk Kurallarını Tanımlayın

Uyumluluk kuralları, müşterilerin uyumsuz kombinasyonlar seçmesini önler:

| Kural Türü | Açıklama |
|-----------|-------------|
| **Gerekir** | Seçenek A seçilirse, hedef kutuda yalnızca listelenen seçenekler mevcuttur |
| **Dışlar** | Seçenek A seçilirse, hedef kutuda listelenen seçenekler gizlenir |

Kural ekleme:

1. Yapılandırma sekmesindeki **Uyumluluk Kuralları** bölümüne kaydırın
2. **+ Kural Ekle**'ye tıklayın
3. **kaynak seçeneği** (tetikleyici) seçin
4. **kural türünü** (Gerekir veya Dışlar) seçin
5. **hedef kutuyu** ve **etkilenen seçenekleri** seçin

Ayrıca, seçeneklere atanan uyumluluk etiketlerinden kuralları otomatik olarak oluşturabilirsiniz. Bu, birçok kombinasyon yönetimi yaparken daha hızlıdır.

### Adım 5: Önceden Ayarlanmışlar (Opsiyonel)

Önceden ayarlanmışlar, müşterilere hızlı bir başlangıç noktası sağlayan önceden inşa edilmiş yapılandırmalardır:

1. **Yapılandırma Önceden Ayarlanmışları** bölümüne kaydırın
2. **+ Önceden Ayarla**'ya tıklayın
3. Önceden ayarlanmış bir ad ve açıklama verin (örneğin, "Oyun Yapılandırması", "Bütçe Başlangıcı")
4. Her kutu için seçenekleri seçin
5. Önizleme resmi yükleyin ve **Öne Çıkan** olarak işaretleyin

Müşteriler, bir önceden ayarlanmışlardan başlayabilir ve ardından bireysel kutuları tercihlerine göre özelleştirebilir.

## Müşteri Deneyimi

Müşteri, mağazanızdaki yapılandırılabilir ürünü görürse:

1. **Sihirbaz Arayüzü** — Kutular, her seçime müşteriye rehberlik eden adımlar olarak sunulur
2. **Filtreleme** — Uyumluluk kurallarına göre uyumsuz seçenekler otomatik olarak gizlenir
3. **Popüler Etiketler** — Popüler olarak işaretlenmiş seçenekler, karar vermede yardımcı olacak bir etiket gösterir
4. **Önceden Ayarlanmışlar** — Öne çıkarılan önceden ayarlanmışlar, hızlı başlangıç seçenekleri olarak görünür
5. **Fiyat Güncellemesi** — Seçenekler seçildikçe toplam fiyat anlık olarak güncellenir
6. **Özet** — Sepete eklemekten önce seçilen tüm seçenekleri gösteren bir inceleme adımı

## İpuçları

- "Bileşenlerin Toplamı" fiyatlandırma stratejisinden başlayın — bu, müşteriler için en sezgisel ve en kolay sürümüdür.
- Uyumluluk kuralları, müşteri bilgisine değil, geçersiz yapılandırmaları önlemek için kullanın.
- En popüler yapılandırmalarınız için 2-3 tane önceden ayarlanmış oluşturun, karar verme yorgunluğunu azaltın.
- Yapılandırıcı üzerinden kullanılmalı olan bileşen ürünleri mağazadan gizleyin.
- Kurulumdan sonra, frontend'de tam yapılandırma akışını test edin, tüm kuralların beklenen şekilde çalıştığından emin olun.

