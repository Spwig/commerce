---
title: Ürün Ekleme
---

# Ürün Ekleme

Bu kılavuz, mağazanıza yeni bir ürün oluşturmanıza yardımcı olur. Ürünler, Temel Bilgiler, Medya, Fiyatlandırma, Stok ve SEO olmak üzere birkaç sekmede organize edilir, böylece her şeyi tek seferde doldurabilir ya da daha sonra tamamlamak için geri dönebilirsiniz.

## Başlangıç

Yan menüden **Ürünler > Tüm Ürünler** sekmesine giderek ürün kataloğunuza bakabilirsiniz. Ürünlere giriş formunu açmak için sağ üst köşedeki **+ Ürün Ekle** butonuna tıklayın.

![Ürün listesi sayfası](/static/core/admin/img/help/add-product/product-list-page.webp)

## Temel Bilgiler Sekmesi

**Temel Bilgiler** sekmesi, ürününüzün temel detaylarını tanımlamak için kullanılır.

![Ürün ekleme formu](/static/core/admin/img/help/add-product/add-product-form.webp)

### Gerekli Alanlar

- **Adı** — Müşterilere gösterilen ürün adı. Diğer diller için çeviriler eklemek için küresel simgeye tıklayın.
- **Slug** — Adın URL dostu sürümü (otomatik olarak oluşturulur). "Otomatik" seçeneğini kapatın ve özelleştirebilirsiniz.
- **SKU** — İç stok takip birim kodunuz.
- **Ürün Tipi** — Seçenekler: Basit, Değişken, Dijital, Takviye, Hediye Kartı, Özelleştirilebilir veya Yapılandırılabilir.
- **Durum** — Çalışırken Taslak olarak ayarlayın, hazırsanız **Yayınla** olarak değiştirin.

### Opsiyonel Alanlar

- **Kategori** — Ürünü organize etmek ve mağaza ön yüzü gezintisini kolaylaştırmak için bir kategoriye atayın.
- **Marka** — Uygunsa bir marka ile ilişkilendirin.
- **Öne Çıkan** — Ürününüzü mağaza ön yüzünde öne çıkarın.
- **Dijital Ürün** — Bu ürün dijital indirme içeriyorsa işaretleyin (dosyalar, lisanslar).
- **Ön Yüzden Gizle** — Ürün kataloğunda görünmez hale getirirken yapılandırıcı bir seçenek veya paket bileşeni olarak hâlâ kullanılabilir.

### Ürün Açıklamaları

- **Kısa Açıklama** — Ürün listeleri ve kartlarda görünür. Kısaca ve etkileyici olun.
- **Detaylı Açıklama** — Ürün detay sayfasında gösterilen detaylı açıklama. Zengin metin düzenleyiciyi kullanarak biçimlendirme, resimler, videolar ve tablolar ekleyin.

Her iki açıklama alanı da çeviri özelliğini destekler — diğer diller için içerik eklemek için küresel simgeye tıklayın.

## Medya Sekmesi

**Medya** sekmesi, entegre Medya Kütüphanesi kullanarak ürün resimlerini yönetmenizi sağlar.

![Medya sekmesi](/static/core/admin/img/help/add-product/media-tab.webp)

1. **+ Medya Kütüphanesinden Görsel Ekle** butonuna tıklayarak medya seçiciyi açın.
2. Mevcut görseller seçin veya doğrudan yeni görseller yükleyin.
3. Görselleri sıralamak için sürükleyin — **ilk görsel**, ürün listeleri ve kartlarda gösterilen ana ürün görseli olur.
4. Ürün sayfasında görsellerin nasıl görüntüleneceğini kontrol etmek için **Galeri Türünü** seçin: Standart Galeri, Karuzel, Ağaç Düzeni, Yakınlaştırma Galeri veya 360° Görünüm.

## Fiyatlandırma Sekmesi

Ürününüzün fiyatlandırmasını ayarlayıp satışları yapılandırın.

![Fiyatlandırma sekmesi](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Standart Fiyatlandırma

- **Standart Fiyat** — Müşterilerin göreceği standart perakende fiyatı.
- **Para Birimi** — Para birimi seçin (mağazanızın varsayılan para birimi önceden seçili olarak ayarlanmıştır).
- **Maliyet** — Ürün maliyetiniz, kâr hesaplamalarında kullanılır. Bu, müşterilere asla gösterilmez.

### Satış Ayarları

Geçici indirimleri yapılandırın:

- **Satış Türü** — Seçenekler: Satış Yok, Sabit Satış Fiyatı, Tutar İndirimi veya Yüzde İndirimi.
- **Satış Değeri** — İndirim tutarı veya yüzdesi.
- **Başlangıç/Zaman Sonu Tarihleri** — Satışın etkinleşeceği ve sona ereceği tarihleri planlayın. Hemen başlamak veya son tarih olmadan boş bırakın.

## Stok Sekmesi

Stok seviyelerini ve fiziksel ürün özelliklerini yönetin.

![Stok sekmesi](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Stok Yönetimi

- **Stok Takibi** — Stok miktarlarını izlemek için etkinleştirin (varsayılan olarak etkinleştirilir).
- **Düşük Stok Seviyesi** — Stok, bu sayıya düştüğünde uyarı alırsınız (varsayılan: 5).
- **Stok Miktarı** — Mevcut birim sayısı.
- **Stok Yoksa Sipariş Kabul Et** — Stokta ürün yoksa bile siparişleri kabul etmek için etkinleştirin.

### Fiziksel Özellikler

Doğru kargo hesaplamaları için ürünün ağırlığını (kg) ve boyutlarını (uzunluk, genişlik, yükseklik cm) girin.

### Ürün Tanımlayıcıları

Pazar yerinde ürün listeleri ve stok sistemleri için standart ürün kodları:

- **GTIN** — Global Trade Item Number
- **EAN** — Avrupa Ürün Numarası
- **UPC** — Ulusal Ürün Kodu (ABD)
- **ISBN** — Kitaplara ait
- **ASIN** — Amazon tanımlayıcısı
- **MPN** — Üretici Parça Numarası

### Uluslararası Kargo / Gümrük

Uluslararası kargo için gerekli:

- **HS Kodu** — Harmonize Sistem sınıflandırma kodu
- **Üretim Ülkesi** — Ürünün üretildiği yer
- **Gümrük Birim Fiyatı** — Gümrük için birim başına bildirilen değer

## SEO Sekmesi

Ürününüzün arama motoru görünürlüğünü optimize edin.

![SEO sekmesi](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Meta Başlık** — Arama motoru sonuçlarında görünen başlık. Diğer diller için çeviri yapmak için küresel simgeye tıklayın.
- **Meta Açıklama** — Arama sonuçları için kısaca açıklama (maksimum 160 karakter). Diğer diller için çeviri yapmak için küresel simgeye tıklayın.
- **SEO Otomatik Oluşturma** — Ürün kaydedildiğinde SEO içeriğini otomatik olarak oluşturmak için işaretleyin.

**Arama Sonucu Önizlemesi** (canlı), ürününüzün Google arama sonuçlarında nasıl görüneceğini tam olarak gösterir.

## Ürününüzü Kaydetme

Hazırsanız, sağ üst köşedeki kaydetme butonlarını kullanın:

- **Kaydet** (onay işareti) — Ürün sayfasında kalmak üzere kaydedin.
- **Kaydet ve Düzenlemeye Devam Et** — Kaydedin ve formda kalmak üzere devam edin.

Ürün, durumu **Yayınla** olarak ayarlandığında mağaza ön yüzünde görünecektir.

## İpuçları

- İlk olarak **Taslak** durumunu kullanın, ürününüzü müşterilerin görmesinden önce tamamlayabilirsiniz.
- Birden fazla görsel yükleme — birkaç fotoğrafı olan ürünler daha iyi dönüşüm sağlar.
- **SEO** alanlarını doldurun, arama motorlarında daha iyi bulunabilirlik için.
- **Kategoriler** ve **Markalar** kullanın, müşterilerin kataloğunuza kolayca erişmesine yardımcı olun.
- Değişken ürünler için (örneğin, farklı boyutlar veya renkler), **Değişken Ürün** tipini seçin ve kaydetme işleminden sonra varyasyonlar ekleyin.