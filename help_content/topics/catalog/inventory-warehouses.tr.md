---
title: Stok & Depolar
---

Depo sistemi, birden fazla konumda stokları yönetmenize, teslimat önceliklerini ayarlamanıza ve stok seviyelerini gerçek zamanlı olarak izlemenize olanak tanır. Yan menüde **Ayarlar > Lisans Yönetimi**'ne gidin veya ürün stok sekmesinden depolara erişin.

![Depo listesi](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Depolar

### Depo Listesi

Depo sayfası, tüm stok konumlarınızı aşağıdaki bilgilerle birlikte kartlar şeklinde gösterir:

- **Ad ve kod** — Depo tanımlayıcısı (örneğin, "Ana Depo", kod "MAIN-WH")
- **Satış bölgesi** — Coğrafi bölge ataması
- **Durum etiketleri** — Aktif/etkin olmayan, mağaza konumu
- **İstatistikler** — Stokta olan ürünler, teslimat önceliği, stok tampon yüzdesi
- **Konum** — Şehir ve ülke
- **Son güncelleme** — Stok seviyelerinin son değiştirildiği zaman

### Depo Oluşturma

1. **+ Depo Ekle**'ye tıklayın
2. Depo ayrıntılarını doldurun:
   - **Ad** — Açıklamalı etiket (örneğin, "ABD Doğu Deposu")
   - **Kod** — Kısa ve benzersiz tanımlayıcı (örneğin, "US-EAST")
   - **Satış Bölgesi** — Teslimat yönlendirme için coğrafi bir bölgeye atayın
   - **Adres** — Teslimat hesaplamaları için tam depo adresi
3. Ayarları yapılandırın:
   - **Aktif** — Teslimat için aktif yapın
   - **Mağaza Konumu** — Bu depo aynı zamanda fiziksel bir mağaza olarak işlev görürse işaretleyin
   - **Teslimat Önceliği** — Daha yüksek sayılar, sipariş teslimatı için daha yüksek öncelik anlamına gelir
   - **Stok Tamponu** — Satın alma için ayrılan güvenlik tamponu yüzdesi
4. **Kaydet**'e tıklayın

### Teslimat Önceliği

Bir sipariş gelirken, sistem aşağıdaki kriterlere göre en iyi depoyu seçer:

1. **Öncelik değeri** — Daha yüksek öncelikli depolar tercih edilir
2. **Stok mevcudiyeti** — Yeterli stok bulunması gerekir
3. **Bölge eşleşmesi** — Müşterinin bölgesine ait depolar tercih edilir

Örneğin, ABD deposu (öncelik 100) ve AB deposu (öncelik 60) olduğunda, ABD siparişleri önce ABD deposundan teslim edilir.

### Stok Tamponu

Stok tamponu, online satışta ayrılmayacak şekilde bir stok yüzdesini ayırır. Bu, aşağıdaki durumlarda faydalıdır:
- Fiziksel mağazalar için zemin stoku gerekir
- Aşırı satışları önlemek için güvenlik stoku
- Wholesale siparişleri için ayrılmış stok

100 birim için 10% bir tampon, yalnızca 90 birim online siparişler için kullanılabilir anlamına gelir.

## Stok Öğeleri

Stok öğeleri, belirli bir ürünün belirli bir depoda olan gerçek stoklarını temsil eder.

### Stok Seviyelerini Görüntüleme

1. Herhangi bir depo kartındaki **stok ikonu**'na tıklayarak stok öğelerini görün
2. Ya da bir ürünün **Stok** sekmesine giderek tüm depolardaki stokları görün

Her stok öğesi aşağıdaki bilgileri gösterir:
- **Ürün adı** ve varyant (uygunsa)
- **Mevcut** — Toplam fiziksel stok
- **Rezervasyon** — Bekleyen siparişler için ayrılan miktar
- **Kullanılabilir** — Mevcut - rezervasyon (satışa açık olan)

### Stok Ekleme

1. Depo stok görünümünden **Stok Öğesi Ekle**'ye tıklayın
2. Ürün ve varyantı seçin
3. **Mevcut** miktarını girin
4. Kaydedin

### Stok Hareketleri

Herhangi bir stok değişikliği, bir **stok hareketi** olarak izlenir:

| Hareket Türü | Açıklama |
|--------------|-------------|
| **Alım** | Tedarikçiden yeni stok alınması |
| **Satış** | Teslim edilen sipariş için stok eksiltme |
| **İade** | Müşteriden iade alınan stok |
| **Ayarlama** | Manuel düzeltme (sayım farklılığı) |
| **Transfer** | Depolar arasında taşınma |
| **Rezervasyon** | Aktif bir sepet için geçici olarak tutulan |

Stok hareketleri, stok değişikliklerinin tam bir denetim kaydını sağlar.

## Ürünlerde Stok Takibi

### Stok Takibi Aktif Etme

Bir ürünün **Stok** sekmesinde:

1. **Stok Takibi** anahtarını açarak stok yönetimi etkinleştirin
2. **Düşük Stok Seviyesi** ayarlayın — stok bu seviyenin altına inerse uyarı tetikler
3. Stokta ürün yoksa siparişleri kabul etmek istiyorsanız **Gerçekleşmeyen Siparişleri Kabul Et** ayarlayabilirsiniz

### Çok Depolama Stokları

Stok takibi etkinleştirildiğinde, Stok sekmesi tüm depolarda stok seviyelerini özet tabloyla gösterir:

- Tüm konumlardaki toplam mevcut stok
- Depo bazlı ayrıntılı kırılım
- Rezervasyonlar ve ayırımlar sonrası kullanılabilir miktarlar

## Düşük Stok Uyarıları

Sistem, stok seviyelerini otomatik olarak izler ve aşağıdaki durumlarda size uyarır:
- Bir ürün, **düşük stok seviyesi** altında kalırsa
- Bir ürün, **kullanılabilir stok** sıfıra ulaşır

Düşük stok uyarıları şu yerlerde görünür:
- **Mağaza Gösterge Paneli**'nde Gerekli Eylemler bölümünde
- Ürün listede görsel bir gösterge ile

## İpuçları

- İşiniz büyüdükçe ekleyebileceğiniz tek bir depo ile başlayın.
- Her bölgeye göre teslimat hızı ve maliyetine göre teslimat önceliklerini ayarlayın.
- Fiziksel mağazalar için stok tamponlarını kullanın ve zemin stokunun kullanılabilirliğini sağlayın.
- Stok hareketlerini düzenli olarak inceleyin ve eksiklik veya farklılıklar tespit edin.
- Stokunuzun yeniden doldurulma süresine göre düşük stok seviyelerini ayarlayın — yeniden doldurmak 2 hafta sürüyorsa, 2 haftalık satışları kapsayan bir eşik ayarlayın.
- Hizmete açılmadan önce stok takibini etkinleştirin ve aşırı satışlardan kaçının.