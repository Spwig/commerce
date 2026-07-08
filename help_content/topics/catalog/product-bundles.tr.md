---
title: Ürün Paketleri
---

Ürün paketleri, ürünleri önceden birleştirilmiş paketler halinde indirimli bir fiyatla satmanıza olanak tanır. Bu, hediye setleri, başlangıç paketleri veya birlikte sunmak istediğiniz ürün kombinasyonları için harikadır.

![Paket bileşenleri admin](/static/core/admin/img/help/product-bundles/bundle-components.webp)

## Fiyatlandırma Stratejileri

Paket fiyatının nasıl hesaplanacağını seçin:

| Strateji | Açıklama |
|----------|-------------|
| **Sabit Fiyat** | Bileşen fiyatlarından bağımsız olarak tüm paket için bir sabit fiyat belirleyin. |
| **Yüzde İndirim** | Bileşen fiyatlarının toplamından indirimli bir fiyat olarak otomatik olarak hesaplayın. |
| **Bileşenlerin Toplamı** | Paket fiyatı, tüm bileşen fiyatlarının toplamına eşittir (indirim olmadan gruplama için kullanışlıdır). |

## Bir Paket Oluşturma

### Adım 1: Ürün Oluşturma

1. **Ürünler > Tüm Ürünler**'e gidin ve **+ Ürün Ekle**'ye tıklayın
2. **Ürün Tipi**'ni **Ürün Paketi** olarak ayarlayın
3. Paket adını, açıklamasını ve resimlerini doldurun
4. Ürünü kaydedin

### Adım 2: Bileşenler Ekleme

**Paket Öğeleri** sekmesine geçerek paketinize ürünler ekleyin:

1. **+ Bileşen Ekle**'ye tıklayın
2. Açılan listeden bir ürün arayın ve seçin
3. Her bileşen için **Miktar** belirleyin (örneğin, cilt bakımı setinde 2x yüz maskesi)
4. **Sıra Numarası**'nı belirleyerek görüntü sırasını kontrol edin
5. Opsiyonel olarak bir bileşeni **Opsiyonel** olarak işaretleyin (müşteriler bu bileşeni dışlayabilir)
6. Eğer bileşen bir değişken ürünse, aşağıdaki seçeneklerden birini seçin:
   - **Sabit varyant** — tüm müşteriler aynı varyantı alır
   - **Varyant seçimi izin ver** — müşteriler ödeme sırasında tercih ettikleri varyantı seçebilir

Altta yer alan özeti, **Toplam Bileşenler** sayısı ve **Paket Değeri** (bileşen fiyatlarının toplamı) gösterir.

### Adım 3: Fiyatlandırma Yapılandırması

**Fiyatlandırma** sekmesine geçin:

1. **Paket Fiyatlandırma Stratejisi**'ni seçin
2. **Sabit Fiyat** için paket fiyatını doğrudan girin
3. **Yüzde İndirim** için indirim yüzdesini belirleyin (örneğin, 15% indirim)
4. **Bileşenlerin Toplamı** için fiyat otomatik olarak hesaplanır

## Ne Paketlenebilir

| Ürün Tipi | Bileşen Olabilir mi? |
|-------------|-------------------|
| Basit Ürün | Evet |
| Değişken Ürün | Evet (sabit varyant veya müşteri seçimi) |
| Dijital Ürün | Evet |
| Özelleştirilebilir Ürün | Hayır |
| Yapılandırılabilir Ürün | Hayır |
| Ürün Paketi | Hayır (paketler iç içe olamaz) |
| Hediye Çeki | Hayır |

## Stok Yönetimi

Paket stoku bileşenleri üzerinden yönetilir:

- **Tüm bileşenlerin stokta olması** gerekir, aksi takdirde paket satın alınabilir değildir
- Bir paket sipariş verildiğinde, her bileşen ürünün stokundan ayrı ayrı çıkarılır
- Eğer herhangi bir bileşen stokta kalmazsa, paket kullanılamaz hale gelir
- Bileşen stok seviyeleri, ödeme sırasında anlık olarak kontrol edilir

## Opsiyonel Bileşenler

Bir bileşeni **Opsiyonel** olarak işaretleyerek müşterilerin paketlerini özelleştirmesine olanak tanıyın:

- Opsiyonel bileşenler varsayılan olarak dahil edilir ancak müşteri bu bileşeni kaldırabilir
- Opsiyonel bileşenler kaldırıldığında paket fiyatı uygun şekilde ayarlanır
- En az bir bileşenin **gerekli** (non-optional) olması gerekir

## Müşteri Deneyimi

Müşteri, mağazanızda bir paketi görürse:

1. **Bileşen Listesi** — Tüm dahil edilmiş ürünler resimleri ve miktarları ile gösterilir
2. **Paket Tasarrufu** — Ürünleri ayrı ayrı satın almakla karşılaştırılan indirim gösterilir
3. **Varyant Seçimi** — Varyant seçimi etkin olan bileşenler için müşteriler tercih ettikleri seçeneği seçebilir
4. **Opsiyonel Ürünler** — Müşteriler opsiyonel bileşenleri aç/kapa olarak ayarlayabilir
5. **Tek Tıklamayla Sepete Ekle** — Tüm paket bir öğe olarak sepete eklenir

## İpuçları

- Komponent fiyatları değiştiğinde otomatik olarak ayarlanan **Yüzde İndirim** stratejisini kullanın. En esnek fiyatlandırma için idealdir.
- Ürün açıklamalarınızda paket satın alımını teşvik etmek için tasarruf miktarını öne çıkarın.
- Müşteri deneyimi için paketleri 3-5 bileşene sınırlayın. Çok fazla ürün, müşteriyi yoran hissettirebilir.
- Opsiyonel bileşenleri kullanarak aynı paketin "temel" ve "premium" sürümlerini sunun.
- Tüm bileşen ürünlerin hala aktif ve stokta olduğundan düzenli olarak emin olun.
