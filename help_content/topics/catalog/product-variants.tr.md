---
title: Ürün Variantları
---

Ürün variantları, tek bir ürünün farklı boyutlar, renkler veya malzemeler gibi birden fazla seçeneğinde sunulmasını sağlar. Her bir variant kendi SKU'su, fiyatı ve stok seviyesi ile birlikte gelir. Herhangi bir **Değişken Ürün**'e gidin ve **Variations** sekmesini tıklayın.

![Ürün variantları](/static/core/admin/img/help/product-variants/product-variants.webp)

## Variantları Anlamak

**Değişken Ürün**, birden fazla varyasyonu destekleyen bir ürün türüdür. Örneğin, bir T-Shirt şu şekilde gelir:
- **Renkler**: Mavi, Kırmızı, Yeşil
- **Boyutlar**: S, M, L, XL

Her bir kombinasyon (örneğin, "Mavi / Büyük") kendi stok ve fiyatıyla ayrı bir varyasyon haline gelir.

## Değişken Ürün Ayarlamak

### Adım 1: Ürün Tipini Ayarla

1. Ürün düzenleme formunu açın (veya yeni bir ürün oluşturun)
2. **Temel Bilgiler** sekmesinde, **Ürün Tipi**'ni **Değişken Ürün** olarak ayarlayın
3. Ürünü kaydedin

### Adım 2: Öznitelikleri Tanımla

Öznitelikler, variantlarınızı farklılaştıran seçeneklerdir (örneğin, Boyut, Renk).

1. **Variations** sekmesine gidin
2. **Ürün Öznitelikleri** bölümünde, mevcut bir özniteliği atamak için **+ Öznitelik Ekle**'yi tıklayın veya yeni birini tanımlamak için **Yeni Oluştur**'u tıklayın
3. Her öznitelik için kullanılabilir değerleri belirtin (örneğin, Küçük, Orta, Büyük)

### Adım 3: Variantlar Oluştur

1. **Ürün Variantları** bölümünde **+ Yeni Variant Ekle**'yi tıklayın
2. Her variantı yapılandırın:
   - **Ad** — Açıklamalı etiket (örneğin, "Mavi", "Büyük / Kırmızı")
   - **SKU** — Benzersiz stok takip kodu
   - **Fiyat** — Variant özel fiyatı (temel üründen farklı olabilir)
   - **Stok** — Mevcut stok seviyesi
3. Gerekli variantlar için bu işlemi tekrarlayın

## Variantları Yönetmek

### Variant Detayları

Her variant kartı şu bilgileri gösterir:
- **Ad** ve **SKU** — Kimlik bilgileri
- **Fiyat** — Mevcut satış fiyatı
- **Stok seviyesi** — Mevcut stok miktarı ile durum göstergesi (Stokta / Stokta Az / Stokta Yok)

Bir variant kartını tıklayarak tüm detaylarını genişletip düzenleyebilirsiniz.

### Variant Özel Ayarlar

Her variant kendi ayarlarına sahip olabilir:

| Ayar | Açıklama |
|---------|-------------|
| **Fiyat** | Temel ürün fiyatını geçersiz kılar |
| **Karşılaştırmalı Fiyat** | Çizgili satış fiyatını gösterir |
| **SKU** | Stok takip için benzersiz kimlik |
| **Stok Seviyesi** | Bağımsız stok izleme |
| **Ağırlık** | Kargo hesaplamaları için |
| **Görsel** | Variant özel ürün görseli |

### Bir Variantı Düzenlemek

1. Variant kartındaki **düzenleme simgesine** tıklayın
2. Düzenlemek istediğiniz alanları değiştirin
3. Değişiklikleri kaydetmek için **Kaydet**'i tıklayın

### Bir Variantı Silmek

1. Variant kartındaki **silme simgesine** tıklayın
2. Silmeyi onaylayın

**Not:** Bir variantı silmek, o variantın stok kaydını kaldırır. Bu işlem geri alınamaz.

## Öznitelikler

### Öznitelikler Nedir?

Öznitelikler, tekrar kullanılabilir seçenek tanımlarıdır. "Boyut" isimli bir öznitelik oluşturduğunuzda "S, M, L, XL" değerleriyle, bunu herhangi bir değişken ürüne atayabilirsiniz.

### Öznitelikler Oluşturmak

1. Variations sekmesinde, **Ürün Öznitelikleri** bölümündeki **Yeni Oluştur**'u tıklayın
2. Öznitelik adını girin (örneğin, "Renk")
3. Değerler ekleyin (örneğin, "Kırmızı", "Mavi", "Yeşil")
4. Özniteliği kaydedin

### Öznitelikleri Atamak

Öznitelikler, birden fazla ürüne atanabilir. Aynı "Boyut" özniteliği, T-Shirt, Pantolon ve Ayakkabılar gibi ürünler arasında kullanılabilir.

## Mağaza Görünümü

Mağazada, değişken ürünler şu öğeleri gösterir:
- Her özniteliğe ait seçenek seçicileri (açılır menüler veya swatchlar)
- Bir varyasyon seçildiğinde otomatik fiyat güncellemesi
- Varyasyon bazlı stok durumu
- Varyasyon özel görseller

## İpuçları

- Ürünler arasında tutarlı öznitelik isimleri kullanın, alışveriş deneyimini düzgün hale getirmek için.
- Variantları oluşturmadan önce tüm öznitelikleri ayarlayarak süreci kolaylaştırın.
- Müşterilerin ne satın aldığını net bir şekilde görebilmesi için varyasyon özel görseller yükleyin.
- Stok yönetimi için SKU'ları sistematik tutun (örneğin, "TSHIRT-MALI-L")
- Varyasyonlarda karşılaştırmalı fiyatı kullanarak boyut veya renk özel indirimler düzenleyin.
