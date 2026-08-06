---
title: Satış Bölgeleri
---

Satış bölgeleri, mağazanız için coğrafi pazarlar tanımlamanıza ve her bölgede hangi ürünlerin mevcut olduğuna dair kontrolü sağlar. Bu, birden fazla ülke veya bölge üzerinde satış yaptığınızda ve her yerde farklı ürün kataloğuna, bölgesel dövizlere veya stok erişimine ihtiyacınız olduğunda yararlıdır.

## Satış bölgesi nedir?

Bir satış bölgesi, bir veya daha fazla ülkeden oluşan, isimlendirilmiş coğrafi bir alandır. Her bölgenin bir varsayılan döviz, bir sıralama ve bir veya daha fazla depo ile bağlantılı olabilir. Bir müşteri mağazanızı ziyaret ettiğinde, Spwig, konumuna göre bölgesini belirler ve uygun döviz ve ürün görünüm kurallarını uygular.

Sık kullanılan durumlar:
- Her ülkenin sadece yerel olarak mevcut olan ürünleri gösterilmesi
- Bölgesel dövizler için varsayılan dövizin atanması (örneğin, Yeni Zelanda müşterileri için NZD)
- Her bölgenin siparişlerini nasıl karşılayacağını kontrol etme
- Bazı pazarlarda henüz mevcut olmayan ürünleri gizleme

## Satış bölgesi oluşturma

1. **Envanter > Satış Bölgeleri** sayfasına gidin. Görmüyorsanız, menü öğesini ortaya çıkarmak için **Araçlar > Mağaza Ayarları > E-Ticaret** altında **Çoklu Depo'yu Aç** seçeneğini açın — bu işlemi aslında kullanmanıza gerek yok, sadece bağlantıyı kilidi çözmek için. /admin/catalog/salesregion/ adresine doğrudan da gidebilirsiniz.
2. **+ Satış Bölgesi Ekle** butonuna tıklayın
3. Bölgenin detaylarını doldurun:

| Alan | Açıklama | Örnek |
|-------|-------------|---------|
| **Bölge Adı** | Bu bölge için gösterim ismi | `Asya-Pasifik` |
| **Bölge Kodu** | Kısa benzersiz tanımlayıcı | `APAC` |
| **Ülkeler** | Bu bölgede bulunan iki harflik ISO ülke kodları | `['NZ', 'AU', 'SG', 'FJ']` |
| **Varsayılan Döviz** | Bu bölge için iki harflik döviz kodu | `NZD` |
| **Öncelik** | Daha yüksek öncelikli bölgeler önce eşleştirilir | `10` |
| **Aktif** | Bu bölgenin şu anda kullanılıp kullanılmadığı | İşaretlendi |

4. **Kaydet**'e tıklayın

### Ülke kodları

İki harflik ISO kodlarını bir JSON listesi olarak girin. Örnek:
- Yeni Zelanda ve Avustralya: `['NZ', 'AU']`
- Sadece Singapur: `['SG']`
- Tüm Avrupa: `['DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'AT', 'CH', 'SE', 'NO', 'DK', 'FI', 'PL']`

### Öncelik

Eğer bir müşteri ülkesi birden fazla bölgede eşleşirse, en yüksek öncelik numarasına sahip bölge kullanılır. Daha spesifik bölgeler için daha yüksek bir öncelik ayarlayın (örneğin, `NZ` için öncelik 20 ve `APAC` için öncelik 10 olsun ki Yeni Zelanda müşterileri öncelikle NZ bölgesine eşleştirilsin).

## Bölgeden ürün görünümünü kontrol etme

Özünde, her ürün tüm bölgelerde görünür. Ürünü sınırlamak için **Ürünler > Tüm Ürünler** altında açın ve **Bölge erişim** alanını (Durum bölümünde) ya da belirli bölgelerde sadece izin ver veya belirli bölgeler hariç tüm bölgelerde izin ver, ardından bu alanda aşağıda ki tabloda bölgeleri seçin, ardından tabloyu doldurun.

Bu, ürünün erişilebilir olduğu bölgelerin dışında kalan şahsiyetlerin neye sahip olacağını da belirler — ürün, listelerden tamamen gizleniyor olabilir ya da "[bölge] 'ye sevkiyet yok" notuyla gösteriliyor olabilir. **Bölge Erişimi** rehberine bakın, bu görüntüleme ayarını ve mağaza aracında Ship-To Seçicisi'ni içeren tam adımlar için.

## Bölgesel döviz

Her bölgenin bir varsayılan döviz vardır. Mağazanız birden fazla döviz destekliyorsa (Araçlar > Çoklu Döviz), bir müşteri bölgesi değiştiğinde, bölgesinin varsayılan dövizi otomatik olarak değişir — bu, otomatik bölge istemi veya Ship-To Seçicisi ile olabilir. Tek dövizli mağazalar ya da çoklu dövizleri kasten açmayan mağazalar, bölgeye bakılmaksızın bu tek dövizi gösterir.

Çoklu dövizlerde fiyatlandırma kurulumu yapmak için, **Araçlar > Döviz Kurları** altında değişim oranlarını yapılandırın. Fiyatlar otomatik olarak çevrilebilir ya da her döviz için elle ayarlanabilir.

## Depoları bölgelere bağlama

Depolar, **Envanter > Depolar** altında bir depo oluştururken ya da düzenlerken bir bölgeye bağlanır. Her depo bir bölgeye aittir, bu da siparişleri karşılamak için o bölgenin stoklarını kontrol eder.

Depolama alanları hakkında daha fazla bilgi için **Envanter ve Depolar** yardım konusuna bakın.

## İpuçları

- Bölgesel kodları kısa ve tanımlayıcı tutun (NZ, APAC, EU, US) — bu kodlar iç yapılandırmalarda ve loglarda kullanılır.
- Daha küçük, daha spesifik bölgeler için daha yüksek öncelik numaraları kullanın, böylece daha geniş kapsamlı tüm bölgelerden daha önce gelir.
- Sadece bir ülke için satıyorsanız, hiçbir bölge ayarı yapmanıza gerek yok — Spwig, tek bir küresel katalogla iyi çalışır.
- Ürünün **Bölge Erişilebilirliği** 'ni **Tüm Bölgelerde Mevcut** olarak ayarlamadan önce sadece onu sınırlamak istediğinizi doğrulayın — varsayılan olarak ürünler her yerde mevcut olur ve hiçbir bakım gerektmez.
- Yeni bir Satış Bölgesi eklediğinizde her ürünün bölge kurallarını gözden geçirin, böylece sınırlamaların neye göre olduğunu doğrulayabilirsiniz.
- Başka bir bölgeye geçmek için **Bölge Erişilebilirliği** rehberine bakarak başlığınıza Ship-To Seçici ekleyin, böylece kendi başınıza bölgeleri değiştirebilir ve sınırlı ürünleri nasıl davrandığını kontrol edebilirsiniz.