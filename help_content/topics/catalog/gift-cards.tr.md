---
title: Hediyelik Kartlar
---

Hediyelik kartlar, müşterilerinize bir hediye olarak gönderilebilecek veya kişisel kullanım için saklanabilecek mağaza kredisi satın almak için olan bir yöntemdir. Alıcılar, checkout sırasında kullanabilecekleri benzersiz bir kod alırlar.

![Hediyelik kart yönetimi](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Adet Türleri

Müşterilerin hediyelik kartı tutarını nasıl seçebileceğini kontrol edin:

| Tür | Açıklama |
|------|-------------|
| **Sabit Adetler** | Müşteriler, önceden belirlenmiş tutarlardan (örneğin, $25, $50, $100) seçim yapar |
| **Özel Tutar** | Müşteriler, min/max aralığı içinde herhangi bir tutar girer |
| **Her İkisi** | Önceden belirlenmiş adetler ve özel tutar seçeneği sunulur |

## Hediyelik Kart Ürünü Oluşturma

### Adım 1: Ürünü Kurun

1. **Ürünler > Tüm Ürünler** menüsüne gidin ve **+ Ürün Ekle**'ye tıklayın
2. **Ürün Türünü** **Hediyelik Kart** olarak ayarlayın
3. Ürün adını ve açıklamasını doldurun
4. Adet ayarlarını yapılandırın:
   - **Adet Türünü** seçin (Sabit, Özel veya Her İkisi)
   - Sabit için: kullanılabilir adet tutarlarını ayarlayın
   - Özel için: **Minimum** ve **Maksimum** izin verilen tutarları ayarlayın
5. **Son kullanma tarihi (gün)** ayarlayın (0 = asla sona ermeyen) — bu, hediyelik kartlarının satın alınmasından sonra geçerli olma süresini belirler
6. Ürünü kaydedin ve yayınlayın

### Adım 2: Yayınla ve Sat

Yayınlandığında, hediyelik kart ürününüz mağaza ön yüzünde diğer ürünler gibi görünür. Müşteriler, ürününüzü tarayarak, bir tutar seçerek ve sepetine ekleyerek erişebilir.

## Hediyelik Kart Yaşam Döngüsü

Bir hediyelik kartı şu yaşam döngüsünü takip eder:

1. **Satın Alma** — Müşteri hediyelik kartı ürününü satın alır ve alıcı detaylarını sağlar
2. **Teslimat** — Hediyelik kart kodu ile bir e-posta otomatik olarak alıcıya gönderilir
3. **Kullanım** — Alıcı, checkout sırasında kodu girerek bakiyeyi uygular
4. **Bakiye Takibi** — Her kullanım bakiyeden düşülür ve sıfıra ulaşana kadar devam eder

## Müşteri Satın Alma Akışı

Bir müşteri hediyelik kartı satın alırken:

1. **Tutar Seçin** — Bir adet seçin veya özel bir tutar girin
2. **Alıcı Bilgileri** — Alıcının e-posta adresini ve ismini girin
3. **Kişisel Mesaj** — Teslimat e-postasına eklemek için isteğe bağlı bir mesaj ekleyin
4. **Gönderen Adı** — E-posta için gönderenin adını sağlayın
5. **Planlı Teslimat** — İsteğe bağlı olarak e-postayı gelecekteki bir tarihe (örneğin, bir doğum günü) planlayabilirsiniz
6. **Ödeme Yapın** — Diğer ürünler gibi satın alımı tamamlayın

## Otomatik Teslimat

Satın alma sonrası, hediyelik kartı otomatik olarak teslim edilir:

- Alıcıya stilize edilmiş bir e-posta gönderilir ve şu bilgileri içerir:
  - Benzersiz hediyelik kart kodu
  - Hediyelik kart değeri
  - Gönderenden gelen kişisel mesaj
  - Kalan bakiyeyi kontrol etmek için bir bağlantı
- Eğer planlı teslimat ayarlandıysa, e-posta belirtilen tarih ve saatte gönderilir
- Gönderen, hediyelik kart detaylarını içeren bir sipariş onayı alır

## Yönetici Hediyelik Kartları

**Ürünler > Hediyelik Kartlar** menüsüne giderek tüm hediyelik kartlarınızı yönetin:

### İstatistikler Paneli

Sayfa üstünde dört kart, anahtar ölçüleri gösterir:

- **Toplam Hediyelik Kartlar** — Toplam olarak verilen hediyelik kart sayısı
- **Aktif** — Mevcut bakiye ile aktif kartlar
- **Toplam Bakiye** — Tüm kartlarda kalan toplam bakiye
- **Kısmen Kullanılmış** — Kısmen kullanılmış kartlar

### Filtreler

Hediyelik kartlarını şu kriterlerle filtreleyin:

- **Arama** — Kod, e-posta veya alıcı adı ile bulun
- **Durum** — Aktif, Pasif, Süresi Dolmuş, Tamamen Kullanılmış veya Kısmen Kullanılmış
- **Bakiye** — Bakiye Var veya Bakiyesiz
- **Oluşturulma Tarihi** — Zaman aralığı (Bugün, Bu Hafta, Bu Ay, Bu Yıl)

### Hediyelik Kart Detayları

Her hediyelik kartı şu bilgileri gösterir:

- **Kod** — Benzersiz kullanım kodu (örneğin, GC-XXXX-XXXX-XXXX)
- **Alıcı** — E-posta ve isim
- **Durum** — Mevcut durum ve renk kodlaması ile durum etiketleri
- **Bakiye / Başlangıç / Kullanılan** — Finansal özeti ve kullanılan yüzdelik oran
- **Anahtar Tarihler** — Oluşturulma, verilme ve ilk kullanım tarihi
- **Gönderen** — Hediyelik kartı satın alan kişi

### Eylemler

Her hediyelik kartı için şu işlemleri yapabilirsiniz:

- **Düzenle** — Hediyelik kartı detaylarını görüntüleyin ve düzenleyin
- **İşlemleri Görüntüle** — Tam işlem geçmişini görüntüleyin
- **E-postayı Yeniden Gönder** — Alıcıya teslimat e-postasını yeniden gönderin
- **Devre Dışı Bırak** — Kartı devre dışı bırakın (bakiye korunur ancak kullanılamaz)

## Ödeme sırasında Kullanım

Bir müşteri checkout sırasında bir hediyelik kart kodu girerken:

1. Kod doğrulanır (aktif, süresi dolmamış ve bakiye var)
2. Mevcut bakiye görüntülenir
3. Bakiye sipariş toplamına uygulanır
4. Eğer bakiye siparişin tamamını karşılıyorsa, ekstra ödeme gerekmez
5. Eğer bakiye sipariş toplamından azsa, müşteri kalan kısmını öder
6. İşlem kaydedilir ve bakiye güncellenir

## İade İşlemi

Bir hediyelik kartı kullanılarak yapılan siparişlerin iadesi sırasında:

- **Kullanılmamış hediyelik kartlar** — Hediyelik kartı tamamen devre dışı bırakılır
- **Kısmen kullanılan kartlar** — Bakiye, bir işlem aracılığıyla manuel olarak ayarlanmalıdır
- **Tam iade** — İade işlemi aracılığıyla hediyelik kart bakiyesine tutarın kredisi verilir

## İpuçları

- Yerel hediyelik kart yönetmeliklerine uygun olmak için, akıllıca son kullanma sürelerini ayarlayın (örneğin, 365 gün) — bazı yerel yönetmelikler minimum geçerlilik süreleri gerektirir.
- **Her İkisi** adet türünü kullanarak hem kolaylık (önceden belirlenmiş tutarlar) hem de esneklik (özel tutarlar) sunun.
- Toplam Bakiye ölçümünü düzenli olarak izleyin — bu, kitabınızdaki bir borç olarak temsil eder.
- Mevsimsel kampanyalar için planlı teslimatı kullanın — müşteriler erken hediyelik kart satın alabilir ve tam tarihte teslim edilebilir.
- Lansman öncesi, test siparişi ile tam akışı (satın alma, e-posta teslimatı, kullanım) test edin.
- Eğer birden fazla ülkeye müşteri satıyorsanız, belirli döviz birimlerinde hediyelik kartlar çıkarabilirsiniz — **Çok Dövizli Hediyelik Kartlar** yardım konusunu inceleyin.

