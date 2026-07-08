---
title: Ürün Beslemeleri
---

Ürün beslemeleri, katalogunuzu Google Shopping ve Facebook Katalog gibi alışveriş platformlarına aktarmayı sağlar. Bağlandıktan sonra ürün verileriniz, bir zamanlamaya göre otomatik olarak senkronize olur ve reklamlarınız her zaman güncel fiyatlar, stoklar ve ürün detaylarını yansıtır.

Mağazanız, beslemeler için bir sağlayıcı bileşen sistemi kullanır. Her besleme sağlayıcısı (Google, Facebook veya diğerleri), bir bileşen olarak yüklenir ve ardından sağlayıcı hesabı aracılığıyla bağlanır. Aynı anda birden fazla besleme sağlayıcısı çalıştırabilirsiniz — örneğin, Google Shopping için bir besleme ve Facebook için ayrı bir besleme.

## Bir besleme sağlayıcısı bağlama

Katalogunuzu senkronize etmeden önce, en az bir besleme sağlayıcı bileşenini yüklemek ve bağlamak gerekir.

### Sağlayıcı bileşenini yükleme

Sağlayıcı bileşenleri, Spwig bileşen pazar yerinde mevcuttur. Mağaza yöneticisi, bileşen güncelleme sistemi aracılığıyla onları yükler. Bir sağlayıcı bileşeni yüklendikten sonra, bir besleme sağlayıcı hesabı oluştururken bir seçenek olarak görünür.

### Bir besleme sağlayıcı hesabı oluşturma

1. **Pazarlama > Besleme Sağlayıcıları**'na gidin
2. **+ Besleme Sağlayıcı Hesabı Ekle**'ye tıklayın
3. Formu doldurun:

**Sağlayıcı Bilgileri bölümü:**
- **Site** — mağazanızı seçin (yalnızca bir tane vardır)
- **Sağlayıcı Bileşeni** — yüklü besleme sağlayıcısını seçin (örneğin, Google Shopping, Facebook Katalog)
- **Hesap Adı** — örneğin `Google Shopping — Ana` veya `Facebook Katalog — ABD` gibi tanımlayıcı bir ad

**Yapılandırma bölümü:**
- **Etkin** — besleme üretimi ve senkronizasyonunu etkinleştirmek için işaretleyin
- **Ana** — bu, bu platform türü için ana besleme sağlayıcınızsa işaretleyin
- **Öncelik** — listedeki sıralama düzenini kontrol eder (düşük sayılar önce görünür)
- **Yapılandırma** — sağlayıcıya özel ayarlar (aşağıya bakın)

4. **Kaydet**'e tıklayın

### Besleme yapılandırma seçenekleri

**Yapılandırma** alanı, aşağıdaki seçenekleri içeren bir JSON nesnesi kabul eder:

| Seçenek | Değerler | Açıklama |
|--------|--------|-------------|
| `sync_interval` | `hourly`, `daily`, `weekly`, `manual` | Beslemenin ne sıklıkla otomatik olarak yeniden oluşturulacağı |
| `format_preference` | `xml`, `csv`, `json` | Çıktı formatı (çoğu platform XML'yi tercih eder) |
| `include_variants` | `true` / `false` | Ürün varyasyonlarını ayrı besleme girdileri olarak dahil et |
| `target_country` | Ülke kodu örneğin `"US"` | Besleme için hedef ülke |
| `content_language` | Dil kodu örneğin `"en"` | Ürün verilerinin dili |

#### ABD'ye yönelik günlük XML besleme için örnek yapılandırma:

```json
{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}
```

## Beslemeye dahil olacak ürünleri filtreleme

Hangi ürünlerin beslemeye dahil olacağını kontrol etmek için yapılandırmaya bir `product_filter` bölümü ekleyebilirsiniz:

```json
{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}
```

| Filtre seçeneği | Açıklama |
|---------------|-------------|
| `status` | Sadece bu durumlara sahip ürünleri dahil et. Sadece canlı ürünleri için `["published"]` kullanın. |
| `in_stock_only` | `true` olarak ayarlayarak stokta olmayan ürünleri dışlayabilirsiniz |
| `categories` | Belirli kategori kimliklerine sınırlayın |
| `brands` | Belirli marka kimliklerine sınırlayın |

Ayrıca, `exclude_products` kullanarak belirli ürünleri ID'leriyle dışlayabilirsiniz:

```json
{
  "exclude_products": [42, 87, 103]
}
```

## Senkronizasyon durumunu izleme

Besleme sağlayıcı hesapları listesi, her bağlı beslemenin senkronizasyon durumunu hızlıca gösterir:

- **Beklemede** — henüz hiçbir senkronizasyon yapılmadı veya besleme oluşturulmasını bekliyor
- **Senkronize ediliyor** — şu anda bir senkronizasyon devam ediyor
- **Başarı** — son senkronizasyon hata olmadan tamamlandı
- **Hata** — son senkronizasyon başarısız oldu; hata iletisi hesap detay sayfasında gösterilir

Liste ayrıca mevcut beslemedeki ürün sayısı ve son senkronizasyonun ne zaman yapıldığı da gösterir.

## Oluşturulan beslemeleri görüntüleme

**Pazarlama > Ürün Beslemeleri**'ne giderek oluşturulan besleme dosyalarını görüntüleyin. Her girdi, bir oluşturulan besleme anlık görüntüsünü temsil eder ve aşağıdaki bilgileri gösterir:

- **Provider Account** — bu beslemenin ait olduğu hesap
- **Format** — XML, CSV veya JSON
- **Product Count** — dahil edilen ürün sayısı
- **Size** — oluşturulan beslemenin dosya boyutu
- **Generated At** — ne zaman oluşturulduğu
- **Expires At** — bu önbelleklenmiş sürümün ne zaman sona erdiği
- **Status** — beslemenin hâlâ geçerli olup olmadığını veya zaman aşımına uğramış olup olmadığını gösterir
- **Download Count** — bu besmenin kaç kez indirildiğini gösterir

Yönetici panelinde beslemeler sadece salt okunur durumdadır — bu beslemeler senkronizasyon süreci tarafından otomatik olarak oluşturulur.

## Senkronizasyon geçmişini görüntüleme

**Pazarlama > Besleme Senkronizasyon Günlüğü**'ne giderek tüm besleme hesaplarınız için her senkronizasyon girişinin tamamını görebilirsiniz. Her günlük girdi şu bilgileri kaydeder:

- Senkronize edilen sağlayıcı hesabı
- Senkronizasyon türü (Tam, Artımlı, Manuel veya Planlı)
- Durum (Başarılı, Kısmi Başarı, Başarısız vb.)
- Senkronize edilen, başarısız olan ve atlanan ürünler
- Senkronizasyon süresi
- Herhangi bir hata mesajı

Sayfa üstündeki senkronizasyon günlükleri panosu genel istatistikleri gösterir: toplam senkronizasyonlar, başarı oranı ve ortalama senkronizasyon süresi. **Hesap** ve **Senkronizasyon Türü** filtrelerini kullanarak belirli bir beslemeye daraltabilirsiniz.

### Bir senkronizasyon başarısız olduğunda ne yapılmalı

1. **Pazarlama > Besleme Senkronizasyon Günlüğü**'ne gidin ve başarısız girdiyi bulun
2. Günlük girdiyi tıklayarak tam **Hata Mesajı** ve **Hata Ayrıntıları**'nı görüntüleyin
3. Yaygın nedenler şunlardır:
   - Gerekli ürün alanlarının eksikliği (başlık, fiyat, resim)
   - Geçersiz veya zaman aşımına uğramış API kimlik doğrulama bilgileri — sağlayıcı bileşenini yeniden yükleyerek kimlik doğrulama bilgilerini yenile
   - Sağlayıcının API'sine bağlanırken ağ hatası
4. Sorun çözüldüğünde, bir sonraki planlı senkronizasyon otomatik olarak çalışacaktır veya sağlayıcı hesabından el ile bir senkronizasyon tetikleyebilirsiniz

## İpuçları

- Çoğu kullanım durumu için `"sync_interval": "daily"` ayarlayın — Google ve Facebook, ürün fiyatlarında çok yüksek dalgalanmalar yoksa daha sık güncellemeye gerek yoktur
- Ürün filtresine daima `"in_stock_only": true` ekleyin, müşterilerin satın alamayacağı ürünleri reklam vermeyin
- Platform ve hedef pazarı içeren açıklayıcı bir hesap adı kullanın (örneğin, `Google Shopping — UK`), böylece birden fazla beslemeyi kolayca yönetebilirsiniz
- Sağlayıcı hesabındaki **Beslemedeki Ürünler** sayısı, beklenenden daha az ürünün dahil edildiğini hemen gösterir — sayının düşük görünmesi durumunda ürün filtresi ayarlarınızı kontrol edin
- Her sağlayıcı türü için bir hesabı **Ana Besleme** olarak işaretleyin; bazı raporlama araçları bunu ana beslemenizi tanımlamak için kullanır
- Ürün kataloğunuza yapılan toplu değişikliklerden sonra senkronizasyon günlüklerini inceleyin, güncellenmiş verilerin doğru şekilde alınmış olduğundan emin olun