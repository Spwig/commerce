---
title: Satış Bölgeleri
---

Satış bölgeleri, mağazanız için coğrafi pazarları tanımlamanıza ve her bölgede hangi ürünlerin mevcut olacağını kontrol etmenize olanak tanır. Bu, birden fazla ülke veya bölgeye yayılmış satış yapmanız ve farklı ürün kataloğu, bölgesel para birimleri veya konum bazlı stok mevcudiyeti ihtiyacınız olduğunda yararlıdır.

## Satış Bölgesi Nedir?

Bir satış bölgesi, bir veya daha fazla ülkeyi içeren isimlendirilmiş bir coğrafi alan. Her bölge, bir varsayılan para birimi, bir öncelik ve bir veya daha fazla depo ile ilişkilendirilebilir. Bir müşteri mağazanızı tararken, Spwig, müşterinin konumuna göre bölgesini belirler ve uygun para birimi ve ürün görünürlük kurallarını uygular.

### Yaygın Kullanım Durumları:
- Her ülkeye özel olarak sadece yerel olarak mevcut olan ürünleri göstermek
- Bölgeden bağımsız olarak varsayılan para birimleri atamak (örneğin, Yeni Zelanda müşterileri için NZD)
- Her bölgede siparişleri yerine getirecek depoları kontrol etmek
- Belirli pazarlarda henüz mevcut olmayan ürünleri gizlemek

## Satış Bölgesi Oluşturma

1. **Katalog > Satış Bölgeleri**'ne gidin
2. **+ Satış Bölgesi Ekle**'ye tıklayın
3. Bölgedeki detayları doldurun:

| Alan | Açıklama | Örnek |
|-------|-------------|---------|
| **Bölge Adı** | Bu bölgenin görüntülenecek adı | `Asya-Pasifik` |
| **Bölge Kodu** | Bu bölgenin kısa ve benzersiz tanımlayıcısı | `APAC` |
| **Ülkeler** | Bu bölgede yer alan iki harfli ISO ülke kodları | `["NZ", "AU", "SG", "FJ"]` |
| **Varsayılan Para Birimi** | Bu bölgenin varsayılan para birimi | `NZD` |
| **Öncelik** | Daha yüksek öncelikli bölgeler önce eşleşir | `10` |
| **Aktif** | Bu bölge şu anda aktif mi? | İşaretli |

4. **Kaydet**'e tıklayın

### Ülke Kodları

Ülkeleri, iki harfli ISO kodlarının bir JSON listesi olarak girin. Örneğin:
- Yeni Zelanda ve Avustralya: `["NZ", "AU"]`
- Sadece Singapur: `["SG"]`
- Tüm Avrupa: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Öncelik

Eğer bir müşterinin ülkesi birden fazla bölgeye uysa, en yüksek öncelik numarasına sahip bölge kullanılır. Daha spesifik bölgelere daha yüksek öncelik verin (örneğin, `NZ`'e 20 öncelik ve `APAC`'e 10 öncelik verin, böylece Yeni Zelanda müşterileri önce `NZ` bölgesine eşleşir).

## Bölgeden Bağımlı Ürün Görünürlüğünü Kontrol Etme

Varsayılan olarak, her ürün tüm bölgelerde görünür. Bir ürünün belirli bölgelere sınırlanmasını istiyorsanız, **Ürün Bölgesel Görünürlüğü** kayıtlarını kullanın.

### Bir Ürünü Belirli Bölgelere Sınırlama

1. **Katalog > Ürün Bölgesel Görünürlüğü**'ne gidin
2. **+ Ürün Bölgesel Görünürlüğü Ekle**'ye tıklayın
3. **Ürün**'ü seçin
4. **Bölge**'yi seçin
5. **Görünür**'ü gerekli şekilde açın veya kapatın
6. **Kaydet**'e tıklayın

Bir ürün için herhangi bir görünürlük kaydı varsa, Spwig kuralları uygular. Görünürlük kaydı olmayan ürünler her yerde görünür.

### Yaygın Desenler

**Sadece bir bölgeye sınırla**

Desteklemek istediğiniz her bölge için bir görünürlük kaydı ekleyin ve izin verilen bölgeler için **Görünür**'ü `Evet` olarak ayarlayın. Diğer bölgelerdeki müşteriler ürünleri görmeyecektir.

**Bir bölgeden hariç tut**

Hariç tutmak istediğiniz bölge için tek bir görünürlük kaydı ekleyin ve **Görünür**'ü `Hayır` olarak ayarlayın. Ürün diğer tüm bölgelerde görünür kalır.

## Ürün Sayfasından Görünürlük Düzenleme

Ürün düzenleme formundan doğrudan bölge görünürlüğünü da yönetebilirsiniz. Ürünün **Bölge Görünürlüğü** bölümünde, o ürün için tüm bölgeler ve görünürlik ayarlarını gösteren bir satır içi tablo bulacaksınız.

## Bölgesel Para Birimi

Her bölge için bir varsayılan para birimi vardır. Bu bölgeden tarayıcıya giren müşteriler, bölgenin para birimindeki fiyatları görür. Kullanılan para birimi, ödeme sırasında belirlenir.

Birden fazla para biriminde fiyatlandırma yapmak için, **Ayarlar > Döviz Kurları** altında döviz kurlarını yapılandırın. Fiyatlar otomatik olarak dönüştürülebilir veya her para birimi için manuel olarak ayarlanabilir.

## Depoları Bölgelere Bağlama

Depolar, **Katalog > Depolar** altında bir depo oluştururken veya düzenlerken bölgelere bağlanır. Her depo bir bölgeye aittir ve bu, hangi bölgenin stoklarının siparişleri yerine getirmek için kullanıldığını kontrol eder.

Depolar hakkında daha fazla bilgi için **Stok ve Depolar** yardım konusuna bakın.

## İpuçları

- Bölgesel kodları kısa ve açıklayıcı tutun (`NZ`, `APAC`, `EU`, `US`) — bunlar içsel olarak ve günlük kayıtlarda kullanılır.
- Daha küçük ve daha spesifik bölgeler için daha yüksek öncelik numaraları kullanın, böylece daha geniş kapsamlı bölgelerden öncelik kazanırlar.
- Sadece bir ülkeye satış yapıyorsanız, bölgeleri yapılandırmaya gerek yoktur — Spwig, tek bir küresel katalogla iyi çalışır.
- Bölgeden bağımlı görünürlüğü test etmek için, admin panelinde belirli bir bölgeye göre filtreleme yaparak mağazanızı ön izleleyin.
- Ürün görünürlüğü kayıtları, ürünleri kısıtlamak istediğinizde oluşturulmalıdır. Bir ürüne görünürlük kaydı bırakmazsanız, ürün herkese açık olur.
- Yeni bir bölge eklediğinizde, mevcut ürün kısıtlamalarının doğru olduğundan emin olmak için görünürlük kurallarınızı gözden geçirin.