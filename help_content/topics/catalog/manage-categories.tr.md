---
title: Kategorileri Yönetme
---

Kategoriler, ürün kataloğunu organize etmenize yardımcı olur ve müşterilerin ürünlerini kolayca tarayarak bulmasını sağlar. Yönetici yan çubuğunda **Ürünler > Kategoriler**'e gidin.

![Kategori listesi](/static/core/admin/img/help/manage-categories/category-list.webp)

## Kategori Listesi

Kategori yönetimi sayfası, aşağıdaki öğelerle birlikte tüm kategorilerinizi kartlar halinde gösterir:

- **Küçük resim** — Kategorinin görsel kimliği
- **Ad ve slug** — Görünür ad ve URL dostu kimlik
- **Ürün sayısı** — Bu kategoriye atanan ürün sayısı
- **Durum** — Yayınlandı veya taslak

Üstteki **filtre sekme**leri kullanarak Tümü, Yayınlandı veya Taslak kategorilerini hızlıca görüntüleyin. **Arama çubuğu**, kategorileri adına göre bulmanıza olanak tanır.

## Kategori Oluşturma

1. Üst sağ köşedeki **+ Kategori Ekle**'ye tıklayın
2. Kategori detaylarını doldurun:
   - **Ad** — Müşterilerin göreceği görünür ad
   - **Slug** — Adından otomatik olarak oluşturulur, URL'de kullanılır
   - **Ana Kategori** — Üst düzey kategori için boş bırakın veya bir ana kategori seçerek alt kategori oluşturun
   - **Açıklama** — Kategori sayfasında gösterilen zengin metin açıklaması
3. Bir **kategori resmi** yükleyin — navigasyon menüleri ve kategori listelerinde görüntülenir
4. SEO sekmesinde **SEO alanları** (meta başlık, açıklama) ayarlayın
5. **Kaydet**'e tıklayın

## Kategori Hiyerarşisi

Kategoriler, ağaç yapısı oluşturmak için sınırsız iç içe geçme destekler:

- **Üst seviye kategoriler** — Ana navigasyon öğeleri (örneğin, "Giysi", "Elektronik")
- **Alt kategoriler** — Bir ebeveyn altında iç içe (örneğin, "Giysi > Erkek > T-Shirt")

Ana kategori açılır menüsü, doğru seviyeyi seçmenize yardımcı olmak için tam hiyerarşisi yolunu gösterir.

## Kategori Ayarları

### Görünürlük

- **Yayınlandı** — Kategori mağaza ön yüzünde ve navigasyonda görünür
- **Taslak** — Kategori müşterilere gizlenir ancak yönetici panelinde erişilebilir

### Öne Çıkan Kategoriler

Kategorileri **öne çıkan** olarak işaretleyin, bunları ana sayfada veya özel navigasyon bölümlerinde vurgulamak için kullanın. Öne çıkan kategoriler, Sayfa Oluşturucu'nun kategori ağı öğesi ile görüntülenebilir.

### Sıra Numarası

Navigasyon menülerinde kategorilerin nasıl görüneceğini kontrol etmek için bir **sıra numarası** değeri ayarlayın. Düşük numaralar önce görünür.

## Ürünleri Kategorilere Atama

Ürünleri atamak için iki yol vardır:

1. **Ürün düzenleme formundan** — Temel Bilgiler sekmesindeki Kategori açılır menüsünden bir kategori seçin
2. **Toplu atama** — Ürün listesinden birden fazla ürün seçin ve bunları bir kategoriye atamak için toplu eylemi kullanın

Her ürün, birincil bir kategoriye ait olabilir. Ekstra gruplamak için etiketler veya koleksiyonlar kullanın.

## Mağaza Ön Yüzünde Kategori Sayfaları

Her yayınlanan kategori, aşağıdaki öğeleri gösteren ayrı bir sayfa alır:
- Kategori adı ve açıklaması
- Banner resmi (ayarlanırsa)
- Tüm atanan ürünleri içeren ürün ağı
- Filtreleme ve sıralama seçenekleri

Kategori sayfa URL'si şu kalıba uyar: `yourstore.com/category/category-slug/`

## İpuçları

- Kategori ağacınızı sığ tutun — navigasyon kullanım kolaylığı için 2-3 seviye derinlik idealdir.
- Müşterilerin aradığı şeyle eşleşen açıklamalı kategori isimleri kullanın.
- Kategori resimleri ekleyin, daha görsel bir tarayış deneyimi sağlayın.
- Ürünleri eklemeye başlamadan önce kategori yapısını ayarlayın, her şeyi organize edin.
- Kategori açıklamasını SEO için kullanın — ilgili anahtar kelimeleri doğal bir şekilde dahil edin.
