---
title: GeoIP Kurulumu
---

GeoIP, mağazanızın ziyaretçilerin IP adreslerine göre nereden geldiklerini otomatik olarak tespit etmesine olanak tanır. Bu, mağazanızdaki konum tabanlı özellikleri sağlar — varsayılan para birimini göstermekten, coğrafi iş kurallarını çalıştırmaya, analizlerinizde ülke düzeyindeki bölümleri görmekle sınırlı değildir.

Mağazanız, Spwig GeoIP hizmetiyle önceden yapılandırılmıştır, bu nedenle coğrafi tespit "kutudan çıkar" şekilde çalışır. Ayrıca, daha yüksek doğruluk için ek sağlayıcılar bağlayabilir, kendiniz indirdiğiniz bir veritabanını kullanabilir veya CDN'den gelen başlıkları kullanarak sıfır gecikmeli sorgular için güvence alabilirsiniz.

## Sağlayıcıların nasıl çalıştığı

**Müşteriler > GeoIP Sağlayıcıları** menüsüne giderek mağazanız için yapılandırılmış sağlayıcıları görebilirsiniz. Her sağlayıcı, farklı bir yöntemle IP adresi konum sorguları yapar. Bir ziyaretçi gelir gelmez, mağazanız öncelik sırasına göre etkin sağlayıcıları sorgular ve ilk başarılı sonucu kullanır.

Birden fazla sağlayıcı aynı anda etkin olabilir — daha düşük öncelik numaraları önce denenir. Eğer en yüksek öncelikli sağlayıcı başarısız olur veya veri döndürmezse, bir sonraki otomatik olarak denenir.

### Kullanılabilir sağlayıcı türleri

| Sağlayıcı | Açıklama |
|----------|-------------|
| **Spwig GeoIP** | Spwig hizmeti aracılığıyla bulut tabanlı varsayılan sorgulama. Kurulum gerekmez. |
| **MaxMind GeoLite2** | MaxMind'den indirilebilen çevrimdışı veritabanı. Yüksek doğruluk. Ücretsiz bir lisans anahtarı gerekir. |
| **DB-IP Lite** | DB-IP'den indirilebilen çevrimdışı veritabanı. Web sitesinden indirin. |
| **IP2Location LITE** | IP2Location'dan indirilebilen çevrimdışı veritabanı. Ücretsiz bir kayıt gerekir. |
| **CDN Edge Başlıkları** | CDN'iniz tarafından eklenen konum başlıklarını okur (örneğin, Cloudflare). Sıfır gecikme. |
| **Tarayıcı İpuçları** | Tarayıcı tarafından sağlanan saat dilimi/dilini kullanarak yumuşak bir konum sinyali olarak. |
| **Özel Sağlayıcı** | Spwig bileşen pazar yerinden yüklenen bir sağlayıcı bileşeni. |

## Sağlayıcı ekleme

### Spwig GeoIP hizmetini kullanma (varsayılan)

Spwig GeoIP sağlayıcısı, yeni kurulumlarda otomatik olarak eklenir. Listede görünüp **Etkin** işaretinin seçili olduğundan emin olun. Ekstra yapılandırma gerekmez.

### MaxMind GeoLite2 veritabanı ekleme

MaxMind, dış hizmete sorgu göndermeden doğru sonuçlar veren ücretsiz bir çevrimdışı veritabanı sunar.

1. maxmind.com'da ücretsiz bir hesap oluşturun ve bir lisans anahtarı oluşturun
2. **Müşteriler > GeoIP Sağlayıcıları** menüsüne gidin ve **+ GeoIP Sağlayıcı Ekle**'ye tıklayın
3. Formu doldurun:
   - **Ad**: `MaxMind GeoLite2` (veya herhangi bir açıklayıcı ad)
   - **Sağlayıcı Türü**: MaxMind GeoLite2
   - **Etkin**: işaretli
   - **Öncelik**: `1` (Spwig varsayılanından daha düşük olacak şekilde ilk denenecek veya alternatif olarak daha yüksek olacak)
   - **Lisans Anahtarı**: MaxMind lisans anahtarınızı yapıştırın
   - **Veritabanı URL'si**: MaxMind hesap paneline girerek indirme URL'sini alın
4. **Kaydet**'e tıklayın

Kaydetme işleminden sonra, sağlayıcıyı listeden seçin ve **Seçili sağlayıcı veritabanlarını güncelle** eylemini kullanarak veritabanı URL'sinin erişilebilir olduğundan emin olun.

### CDN kenar başlıkları ekleme

Mağazanız, geolocation başlıkları ekleyen bir CDN (örneğin, Cloudflare'ın `CF-IPCountry`) arkasında bulunuyorsa, bu başlıkları anında, sıfır gecikmeli ülke tespiti için kullanabilirsiniz.

1. **Müşteriler > GeoIP Sağlayıcıları** menüsüne gidin ve **+ GeoIP Sağlayıcı Ekle**'ye tıklayın
2. **Sağlayıcı Türü** alanını **CDN Kenar Başlıkları** olarak ayarlayın
3. **Öncelik** alanını `0` olarak ayarlayın (en yüksek öncelik, çünkü başlıklar en hızlı kaynaktır)
4. **Yapılandırma** alanına, CDN'iniz tarafından kullanılan başlığı belirtin:
   ```json
   {
     "header_name": "CF-IPCountry"
   }
   ```
5. **Kaydet**'e tıklayın

### Sağlayıcı testi

Bir sağlayıcı ekledikten sonra, doğru çalışıp çalışmadığını doğrulayabilirsiniz:

1. GeoIP Sağlayıcılar listesinde sağlayıcıyı onay kutusu kullanarak seçin
2. **Eylem** açılır menüsünü açın ve **Seçili sağlayıcıları test et**'i seçin
3. **Git**'e tıklayın

Spwig, bilinen bir IP adresi (Google'ın genel DNS, `8.8.8.8`) için bir test sorgusu gönderecek ve size sonucu gösterecek. Başarılı bir test, döndürülen ülkeyi ve yanıt süresini milisaniyeler cinsinden gösterecektir.

## Sağlayıcı önceliğini ayarlama

Birden fazla sağlayıcı aktif olduğunda, **Öncelik** alanı hangisinin önce deneneceğini kontrol eder.

Daha düşük sayılar daha yüksek öncelik anlamına gelir.

Örneğin, CDN başlıklarını önce (en hızlı) kullanmak ve başarısız olursa Spwig GeoIP'e geçmek istiyorsanız:

| Sağlayıcı | Öncelik |
|----------|----------|
| CDN Edge Başlıkları | 0 |
| Spwig GeoIP | 10 |

Liste görünümünde doğrudan önceliği düzenleyebilirsiniz — **Öncelik** sütunu satır içi düzenlenebilir.

## Sağlayıcı performansını izleme

Her sağlayıcı kaydı kendi doğruluk istatistiklerini izler:

- **Toplam Sorgular** — denenen toplam IP sorgu sayısı
- **Başarılı Sorgular** — sonuç döndüren sorgular
- **Başarısız Sorgular** — veri döndürmeyen veya hata döndüren sorgular
- **Ortalama Yanıt (ms)** — milisaniyeler cinsinden ortalama yanıt süresi
- **Doğruluk** — başarılı sorguların yüzdesi

Bir sağlayıcının düşük doğruluk oranı veya yüksek yanıt süreleri gösteriyorsa, önceliğini ayarlamayı veya daha iyi performans gösteren bir seçeneğe geçmeyi göz önünde bulundurun.

## Ülke eşleme

**Müşteriler > Ülke Eşleme**'ye giderek, para birimi, dil, vergi ve kargo için ülke bazlı varsayılanları yapılandırabilirsiniz. Her ülke girişi şunları kontrol eder:

- **Varsayılan Para Birimi** — o ülkeye ait ziyaretçiler için önceden seçili para birimi
- **Varsayılan Dil** — o ülkeye ait ziyaretçiler için gösterilen dil
- **Vergi Oranı** — o ülkeye uygulanan varsayılan vergi yüzdesi
- **EU Üyesi** / **Vergi Gerektirir** — EU vergi uyumluluğu mantığı için kullanılır
- **Kargo Bölgesi** — ülkeyi bir kargo bölgesiyle ilişkilendirir
- **COD Destekler** — o ülkeye için Nakit ile Ödeme (COD) özelliğini etkinleştirir

**Aktif**, **Varsayılan Para Birimi** ve **Varsayılan Dil** alanlarını her kayıt açmadan doğrudan listede düzenleyebilirsiniz.

## İpuçları

- Spwig GeoIP sağlayıcısı yapılandırma olmadan hemen çalışır — daha yüksek doğruluk veya çevrimdışı işlem için ek sağlayıcılar ekleyin
- Cloudflare kullanıyorsanız, CDN Edge Başlıkları sağlayıcısı en iyi seçimdir: gecikme eklemeyen ve herhangi bir API kotasına karşı gelmeyen
- Gerçekten ihtiyaç duyduğunuz sağlayıcıları aktif tutun — ilk sağlayıcı başarılı olursa, birçok aktif sağlayıcı doğruluku artırmaz
- Haftalık olarak doğruluk istatistiklerini kontrol edin ve başarı oranı %80'in altında olan sağlayıcıları devre dışı bırakın
- Ülke eşleme, varsayılanlar olarak kullanılır; müşteriler dükkanın ön tarafında her zaman para birimi ve dili manuel olarak değiştirebilir