---
title: Stok & Depolar
---

Depo sistemi, birden fazla konumda stok yönetmenizi, yerine getirme önceliklerini ayarlamanızı ve stok seviyelerini anlık olarak takip etmenizi sağlar. Depo konumlarınızı yönetmek için admin yan menüsündeki **Ürünler > Depolar** sayfasına gidin.

![Depo listesi](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Depolar

### Depo Listesi

Depo sayfası, aşağıdaki bilgilerle tüm stok konumlarınızı kart şeklinde gösterir:

- **İsim ve kod** — Depo tanımlayıcısı (örneğin, "Ana Depo", kod "ANA-DEPO")
- **Satış bölgesi** — Coğrafi bölge ataması
- **Durum etiketleri** — Aktif/pasif, perakende mağazası
- **İstatistikler** — Stoktaki ürün sayısı, yerine getirme önceliği, stok yedekleme yüzdesi
- **Konum** — Şehir ve ülke
- **Son güncelleme** — Stok seviyelerinin son olarak değiştirilme tarihi

### Bir depo oluşturma

1. **+ Depo Ekle** butonuna tıklayın
2. **Temel Bilgileri** doldurun:
   - **İsim** — Tanımlayıcı etiket (örneğin, "Kuzey Amerika Deposu")
   - **Kod** — Kısa benzersiz tanımlayıcı (örneğin, "KUZEY-AMERİKA") — Tüm depolar arasında benzersiz olmalıdır
   - **Satış Bölgesi** — Yerine getirme yönlendirme için coğrafi bölgeye atama yapın
   - **Aktif** — Yerine getirme için dahil etmek için etkinleştirin
3. Depo adresini tam olarak girin
4. **Yerine Getirme Ayarlarını** yapılandırın:
   - **Yerine Getirme Önceliği** — Yüksek sayılar = sipariş yerine getirme için daha yüksek öncelik
   - **Stok Yedekleme Yüzdesi** — Online satış için rezerve edilecek stok yüzdesi (0-100)
   - **Kargo Konumu** — Bu deponun müşteri toplama noktasına sahip olup olmadığına göre isteğe bağlı olarak bir toplama konumuna bağlanın
5. **Müşteri Görsüni** ayarlarını yapılandırın (opsiyonel):
   - **Gösterilen İsim** — Müşteriye açıklayan etiket (örneğin, "Avrupa'dan kargo") — Depo adını kullanmak için boş bırakın.
   - **Frontend'de Göster** — Ürün sayfalarında müşterilere bu deponun originini gösterin
6. **POS / Perakende Mağazası** ayarlarını yapılandırın (opsiyonel):
   - **Perakende Konumu** — Bu deponun fiziksel bir mağaza olarak da işlev gördüğüne dair kontrol yapın
   - **POS Gösterilen İsim** — POS arayüzünde gösterilen kısa isim
   - **Mağaza Grubu** — Ayar kalıtımları için POS mağaza grubuna atama yapın
7. Gerekirse **İletişim Bilgileri** ekleyin (isim, e-posta, telefon)
8. **Kaydet**'e tıklayın

### Yerine Getirme Önceliği

Bir sipariş geldiğinde sistem, en iyi depoyu aşağıdaki değerlere göre seçer:

1. **Öncelik değeri** — Daha yüksek öncelikli depolar tercih edilir
2. **Stok mevcudiyeti** — Yeterli stok olmalıdır
3. **Bölge eşleşmesi** — Müşteri bölgesine ait depolar tercih edilir

Örneğin, ABD deponuz (öncelik 100) ve Avrupa deponuz (öncelik 60) varsa, ABD siparişleri önce ABD deponuzdan yerine getirilir.

### Stok Yedekleme

Stok yedeklemesi, online satış için satılmayacak envanterin bir yüzdesini korur. Bu, şu gibi durumlarda yararlıdır:
- Fiziksel perakende mağazalarının zemin stoklarına ihtiyacı vardır
- Overselling'i önlemek için güvenlik stokları
- Toptancı siparişleri için rezerve envanter

100 birimde %10'luk bir yedekleme, sadece 90 birim online siparişler için mevcut olur.

## Stok Ürünleri

Stok ürünleri, belirli bir ürünün belirli bir deponundaki gerçek envanterini temsil eder.

### Stok Seviyelerini Görme

1. Herhangi bir deponun kartındaki **stok simgesine** tıklayın ve stok ürünlerini görün
2. Veya bir ürünün **Envanter** tabını açın ve tüm depolar arasındaki envanteri görün

Her stok ürünü şunları gösterir:
- **Ürün adı** ve (varsa) varyant
- **Mevcut** — Toplam fiziksel envanter
- **Atanmış** — Bekleyen siparişler için ayrılmış miktar
- **Mevcut** — Mevcut - atanmış (satılabilir olan)

### Stok Ekleme

1. **Ürünler > Stok Ürünleri**'ne gidin ve **+ Stok Ürünü Ekle**'ye tıklayın, veya
2. Bir ürünün düzenleme formunu açın ve en alttaki **Stok Ürünleri** aralığını kullanın
3. **Ürün** ve **Depo** seçin (değişken ürünler için isteğe bağlı olarak **Varyant** da seçin)
4. **Mevcut** miktarını girin
5. **Düşük Stok Eşiği**'ni ayarlayın — bu ürün için bu eşik, düşük stok uyarısı tetikler
6. Kaydet

### Stok Hareketleri

Envanterdeki her değişiklik bir **stok hareketi** olarak takip edilir.

| Hareket Türü | Açıklama |
|--------------|-------------|
| **Giriş** | Satıcıdan alınan yeni stok |
| **Satış** | Tamamlanmış bir sipariş için stok azaltılması |
| **İade** | Bir müşteriden dönen stok |
| **Düzeltme** | Manuel düzeltme (sayım eksikliği) |
| **Transfer** | Depolar arası hareket |
| **Rezervasyon** | Aktif bir sepet için geçici olarak tutuldu |
| **Hasar** | Hasarlı veya kaybolmuş olarak yazılmış |
| **Yeniden Sayım** | Fiziksel stok sayımına göre düzeltilmiş |

Stok hareketleri, envanter değişikliklerinin tam bir denetim izini sağlar. **Stok seviyelerini** eylemlemekten başka, Spwig, Stock Items listesinde çoklu eylemler sunar ve birçok ürün için aynı anda stok transferi, yazdırma ve yeniden sayım yapmanı sağlar — [Çoklu Stok Eylemleri](/help/stock-bulk-actions)"e bakınız.

## Ürünlerde Envanter Takibi

### Envanter takibini etkinleştirme

Bir ürünün **Envanter** bölümünde:

1. Bu ürün için stok yönetimi için **Envanteri Takip Et** kipini açın
2. **Düşük Stok Eşiği**'ni ayarlayın — herhangi bir depoda stok bu seviyenin altında olduğunda panoda uyarılar oluşturur
3. Stokta kalmadığında emri kabul etmek istiyorsanız **Gerçekleştirilebilir Siparişleri Aç** ayarını yapılandırın
4. Bu ürün için site genelinde veya kategori davranışını geçersiz kılmak üzere isteğe bağlı olarak **Stokta Kalmadığında Eylemi** ayarlayabilirsiniz

Takip etmeyi etkinleştirdikten sonra, ürün formunun altındaki **Stock Items** inline bölümünü kullanarak gerçek stok miktarlarını yönetin, ya da **Ürünler > Stock Items** üzerinden yapın.

### Çoklu Depo Stokları

Envanter takibi etkinleştirildiğinde, Envanter sekmesi tüm depolar arasındaki stok seviyelerini bir özet tablosunda gösterir:

- Tüm konumlardaki toplam mevcut stok
- Depo bazında bölünmüş stok
- Rezervasyonlar ve tahsisler sonrası mevcut miktarlar

## Düşük Stok Uyarıları

Sistem, stok seviyelerini otomatik olarak takip eder ve şunlarda uyarılar verir:
- Ürün **düşük stok eşiğinin** altına düştüğünde
- Ürün **sıfır mevcut stok** seviyesine ulaştığında

Düşük stok uyarıları şunlarda görünür:
- **Mağaza Dashboard**'daki Eylem Gerektiren bölümde
- Ürün listesinde görsel bir uyarı ile

## İpuçları

- İşiniz büyüdükçe tek bir depo ile başlayın ve daha fazlasını ekleyin.
- Her bölgeye olan kargo hızı ve maliyetine göre tamamlama önceliklerini belirleyin.
- Satış noktaları için stok buffer'ları kullanarak zemin stok mevcudiyetini sağlayın.
- Stok hareketlerini düzenli olarak inceleyerek, çalınma veya eksiklikleri belirleyin.
- Stok yeniden sipariş zamanınıza göre düşük stok eşikleri ayarlayın — 2 hafta içinde tedarik edilebiliyorsa, eşik 2 haftalık satışları kaplayacak şekilde ayarlanmalıdır.
- Overselling olmaması için, etkinleştirmeden önce envanter takibini etkinleştirin.