---
title: API Tokenları
---

API tokenları, dış hizmetlerin ve entegrasyonların mağazanızla iletişim kurmasına olanak tanıyan güvenli anahtarlardır. Bir üçüncü taraf hizmeti veya araç, mağazanızın verilerine erişmek veya eylemleri tetiklemek istiyorsa, her istekle birlikte bir API tokenu gönderir. Bu, mağazanızın isteğin yetkilendirildiğini doğrulamasını sağlar. Tokenları, onların mağazanızın hangi bölümlerine erişebileceğini tam olarak belirleyerek, yönetici panelinizdeki API Tokenları bölümü üzerinden oluşturup yönetirsiniz.

## API tokenu ne zaman gerekir

Genellikle bir API tokenu oluşturmanız gerekirken:

- Dış bir hizmet veya otomasyon aracı, mağazanıza okuma veya yazma yapmak için gerekiyorsa
- Gelen çağrıları doğrulamak için bir webhook alıcısı kurarken
- Spwig Yardım Sistemi'nizi kurulumunuz için yapılandırırken
- Spwig API'sini kullanarak özel bir entegrasyon oluştururken
- Spwig mağazanızla başka bir sistem arasında veri senkronizasyonu yaparken

Her entegrasyon kendi tokenı olmalıdır, böylece bir hizmetin erişimini iptal etmeniz diğerlerini etkilemez.

## Token türleri

Bir token oluştururken, onun amacını tanımlayan bir tür seçersiniz. Bu tür sadece referans olarak kullanılır ve her tokenın ne işe yaradığını takip etmenize yardımcı olur.

| Tür | Amaç |
|------|---------|
| **Yardım Sistemi** | Spwig yardım belgeleri sistemi tarafından kullanılır |
| **Dış Entegrasyon** | Üçüncü taraf hizmetler, otomasyon araçları (örneğin, Zapier) veya veri senkronizasyon araçları |
| **Webhook** | Webhook alıcıları veya uç noktaları için kimlik doğrulama |
| **Özel** | Yukarıdaki kategorilere uymayan herhangi bir diğer amaç |
| **Örnek Senkronizasyonu** | Spwig kurulumları veya dış Spwig hizmetleri arasında senkronizasyon |

## API kapsamları: bir tokenın neye erişebileceğini kontrol etme

Her token, **API Kapsamları** bölümüne sahiptir ve bu, tokenın mağazanızın hangi bölümlerine erişebileceğini belirler. Bir tokenun her şeyi erişim hakkı olmaması yerine, entegrasyonun gerçekten ihtiyaç duyduğu seviyede, bir alan bir bir erişim izni verilir.

**Hiçbir kapsam seçilmeden bir token hiçbir API'ya erişemez**, bile aktif ve geçerli olsa bile. Yeni bir token için bu varsayılan ayar olduğundan, bir entegrasyonun çalışması için ona erişim izni vermeniz gerekir.

Her kapsam için üç erişim seviyesinden birini seçersiniz:

| Erişim Seviyesi | Ne izin verir |
|------------------|------------------|
| **Hiçbir erişim** | Token, bu alandaki hiçbir uç noktaya çağrı yapamaz |
| **Okuma** | Token, bu alandan veri alabilir, ancak hiçbir şeyi değiştiremez |
| **Okuma & Yazma** | Token, bu alandan veri alabilir ve ayrıca oluşturabilir, güncelleyebilir veya silebilir |

Kapsamlar, yönetici panelinizin alanlarıyla eşleşecek şekilde gruplandırılmıştır:

| Grup | Kapsam | Okuma & Yazma mevcut? | Erişim sağlar |
|-------|-------|:---:|-------------------|
| Analizler | **Satış Analizleri** | Sadece Okuma | Satış panoları, KPI'ler, ürün/müşteri/kategori analizleri, karşılaştırmalar ve dışa aktarımlar |
| Analizler | **Web Analizleri** | Sadece Okuma | Ziyaretçi ve trafik analizleri: genel bakış, eğilimler, en çok ziyaret edilen sayfalar, coğrafi konum ve referanslar |
| Katalog | **Ürünler** | Evet | Ürünler, varyasyonlar, görüntüler, stok ayarlamaları ve öznitelik atamaları |
| Katalog | **Kategoriler** | Evet | Ürün kategorileri, görüntüler ve afişler dahil |
| Katalog | **Markalar** | Evet | Ürün markaları |
| Katalog | **Öznitelikler** | Evet | Ürün öznitelik tanımları |
| Katalog | **Stok** | Evet | Stok panoları, stok hızı, hareketler, yeniden sipariş önerileri ve stok ayarları |
| Siparişler | **Siparişler** | Evet | Siparişler, sipariş notları, durum/izleme güncellemeleri, iptaller, iadeler ve sipariş belgeleri |
| Müşteriler | **Müşteri Mesajları** | Evet | İletişim formlarından gelen müşteri mesajları ve sipariş notları, durum güncellemeleri ve yanıtlar |
| Mağaza & Ayarlar | **Mağaza Ayarları** | Evet | Mağaza ayarları, mevcut diller ve markalama (ad, renkler, logolar) |
| Kullanıcılar & Erişim | **Personel & Roller** | Evet | Personel hesapları, davetler, roller ve izin kataloğu |

İki **Analizler** kapsamı her zaman sadece okunabilir – raporlama verisi için "yazma" kavramı yoktur, bu yüzden seçici sadece **Hiçbir erişim** veya **Okuma** seçeneğini sunar.

[![API Kapsamları seçici, Analytics ve Catalog kapsamları grubu üzerinde bir erişim notu ile](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)]

Kapsam seçici altında, **"Bu token şu alanlara erişebilir:"** başlığı altında, token'a verdiğiniz tüm kapsamlar ve seviyeleri listeleyen bir özet vardır. Bu sayede token'ın erişimini, picker'ı çözmeden hızlıca kontrol edebilirsiniz.

[!["Bu token şu alanlara erişebilir:" özetinin her bir verilen kapsama ve okuma veya okuma & yazma seviyesine göre listelendiği](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)]

### Bir token'un gerçekten hangi izinleri kullandığı

Bir token'un kapsamları, onun yapabileceği şeyin *tepe noktası* - yani üst sınırı -dır. Ancak token, onu yaratan personelin gerçek dünyadaki izinlerini de miras alır:

- Token, yaratan personel bir süper kullanıcı olsa bile, asla **süper kullanıcı** yetkileriyle işlem yapamaz.
- Bir kapsama **Okuma & Yazma** izni, yaratan personelin rolü o alana yazma izni veriyorsa çalışır. Örneğin, Products için sadece görüntüleme izni olan bir rol, "Products: Okuma & Yazma" izni ile yarattığı bir token hala sadece okuyabilir - rol, kapsamın üzerine ek bir kilit görevi görür.
- Eğer bir token yaratan personel silinir veya hesabı devre dışı bırakılırsa, token hemen API erişimini kaybeder, kapsamına bakılmaksızın - artık onun adına işlem yapacak bir izinli kullanıcı kalmamıştır.

Bu, token'ı güvenli şekilde sınırlamak için en emniyetli yolun, token'ı oluştururken, token'ın sahip olması gereken erişimi zaten sağlıyor olan bir personel olarak oturum açmış olmanız anlamına gelir.

## API Tokenu Oluşturma

1. **Ayarlar > API Tokenları** bölümüne gidin
2. **+ API Token Ekle**'ye tıklayın
3. Token'ın ne için kullanıldığını açıkça belirten bir **Ad** girin (örneğin, `Zapier Ürün Senkronizasyonu` veya `Yardım Sistemi API`)
4. Uygun **Token Türü**'nü seçin
5. Entegrasyon hakkında daha fazla bilgi içeren isteğe bağlı bir **Açıklama** ekleyin
6. **API Kapsamları** bölümünde, entegrasyonun ihtiyaç duyduğu her alanda **Hiçbir erişim**, **Okuma** veya **Okuma & Yazma** seçin - diğer tüm kapsamları **Hiçbir erişim** olarak bırakın
7. Gerekirse **Aktif** durumu, **Son Kullanma Tarihi** ve **İzin Verilen IP'ler** alanlarını yapılandırın (aşağıya bakın)
8. **Kaydet**'e tıklayın

Kaydetme işlemi tamamlandıktan sonra, token'ın tam değeri detay sayfasında görüntülenir. **Hemen kopyalayın** - token, listede görüntülenirken güvenlik nedeniyle maskeleyilmiş olur ve bu sayfadan ayrıldığınızda tam olarak tekrar elde edilemez.

[![API Token Detayı](/static/core/admin/img/help/api-tokens/api-token-detail.webp)]

## Token Değeri Güvenliği

Spwig, yeni bir token kaydettikten hemen sonra token değerinin tamamını yalnızca bir kez gösterir. Bunun sonrasında, listede yalnızca maskelenmiş bir sürüm (örneğin, `spw_••••••••••••••••••••3f8a`) gösterilir.

Token değerini kaybetirseniz, onu geri alamazsınız. Eski token'ı silmeniz ve yeni bir token oluşturmanız gerekir, ardından onu kullanan entegrasyonu güncellemeniz gerekir.

**Token değerlerini e-postalarda, sohbet mesajlarında veya kaynak kodunda asla paylaşmayın.** Onları şifreler gibi tedirgin edin.

## Son Kullanma Tarihi Ayarlama

**Son Kullanma Tarihi** alanı, token'ın otomatik olarak çalışmayı durduracağı bir tarih ve saat belirler. Token'ın son kullanma tarihi olmaması gerekiyorsa, bu alanı boş bırakın.

Son kullanma tarihleri, aşağıdaki durumlarda faydalıdır:

- Belirli bir son tarihe sahip geçici entegrasyonlar
- Üçüncü taraflara verilen token'lar için otomatik erişim kaldırma
- Yüksek yetkili entegrasyonlara ek bir güvenlik katmanı eklemek

Token son kullanma tarihi geçtiğinde, onunla yapılan istekler reddedilir. Erişimi uzatmak için **Son Kullanma Tarihi** tarihini güncelleyebilir veya bir değiştirilmiş token oluşturabilirsiniz.

## Belirli IP Adreslerine Sınırlama

**İzin Verilen IP'ler** alanı, IP adresleri listesini kabul eder. Bu liste boş değilse, token yalnızca bu adreslerden gelen istekler için çalışır.

Örneğin, analiz araçlarının çalıştığı sunucunun IP adresi `203.0.113.42` ise, bu IP'yi eklemek token'ın başka bir yerden kötüye kullanılmasını önler, hatta token kaçak olursa bile.

**İzin Verilen IP'ler** alanını boş bırakarak, herhangi bir IP adresinden gelen istekleri kabul edebilirsiniz.

**Süre sonu ve IP kısıtlamaları, kapsamlardan bağımsız olarak kontrol edilir.** Süresi dolmuş veya allowlist dışında olan bir token, kapsamları dahi değerlendirilmeden reddedilir. Geniş kapsamlara sahip bir token, süresi dolunca veya listede olmayan bir IP adresinden çağrıldığında hemen reddedilir.

## Token ile API'yi çağırma

Entegrasyonlar, Spwig'in admin API'sine erişmek için token'ı bir `Authorization` başlığı ile gönderir:

```
Authorization: Bearer <your-token-value>
```

Her admin API uç noktası `/api/admin/...` altında yer alır. Entegrasyonunuzu geliştiren geliştirici, hangi uç noktaların çağrılacağını belirler. Satıcı olarak, token'ın **API Kapsamları** ilgili uç noktaları kapsamasını sağlamaktan sorumlusunuz. İstek bir yetki hatasıyla reddedilirse, ilk kontrol edilmesi gereken şey token'ın doğru erişim seviyesinde doğru kapsamın verilmiş olup olmadığıdır.

### Örnek: web trafiği analitiği okuma

Spwig, `GET /api/admin/analytics/traffic/` uç noktasını, mağazanız için ziyaretçi ve trafiği analizlerini döndürür — ziyaretlerin ve benzersiz ziyaretçilerin genel bakış, zaman içindeki eğilimler, en çok ziyaret edilen sayfalar, ziyaretçi coğrafyası ve referer kaynakları. Bu verilere raporlama aracı veya dashboard'ın okuyabilmesi için:

1. Bu entegrasyon için bir token (veya mevcut bir tokenı düzenleyin)
2. **API Kapsamları** altında **Web Analitiği**'ni **Oku** olarak ayarlayın
3. Tokenı kaydedin ve entegrasyona sağlayın

**Web Analitiği**, sadece okunabilir bir kapsam olduğu için "Oku & Yaz" seçeneği yoktur — entegrasyon sadece analitik verileri alabilir, mağazanızın yapılandırmasını asla değiştiremez.

## Token kullanımını izleme

Token listesi aşağıdaki bilgileri gösterir:

- **Kullanım Sayısı** — tokenın toplam kaç kez kullanıldığını gösterir
- **Son Kullanım Zamanı** — tokenın bir istek yapmak için son kez ne zaman kullanıldığını gösterir

Bu alanlar, kullanılmayan tokenları (iptal edilmesi gereken adaylar) tanımlamaya ve beklenmedik aktiviteyi tespit etmeye yardımcı olur. Kullanım sayısında ani bir artış, tokenın amaçlanan entegrasyonun dışında biri tarafından kullanılıyor olabileceğini gösterir.

## Token iptal etme

Tokenı silmeden hemen durdurmak için:

1. Token adını tıklayın
2. **Aktif** kutusunu kaldırın
3. Kaydedin

Token, listede referans olarak kalır ancak sonraki tüm isteklerde reddedilir. Bu, bir sorunla ilgili bir soruşturma yaparken entegrasyonu geçici olarak durdurmak gerektiğinde yararlıdır.

Tokenı kalıcı olarak kaldırmak için:

1. Listede tokenın onay kutusunu seçin
2. Eylem menüsünden **Seçilen API tokenlarını sil**'i seçin
3. Silmeyi onaylayın

Silindikten sonra token geri kazanılamaz. Entegrasyonun hala erişim ihtiyacı varsa, yeni bir token oluşturun ve entegrasyonun yapılandırmasını güncelleyin.

## Örnek: Zapier entegrasyonunu ayarlama

**Senaryo:** Mağazanızı Zapier ile bağlamak istiyorsunuz, sipariş bildirimlerini otomatikleştirmek için.

| Alan | Değer |
|-------|-------|
| Ad | `Zapier Sipariş Otomasyonu` |
| Token Türü | Dış Entegrasyon |
| Açıklama | Zapier tarafından yeni siparişleri okumak ve bildirimleri tetiklemek için kullanılır |
| API Kapsamları | **Siparişler**: Oku & Yaz |
| Aktif | Evet |
| Süresi Biten | *(boş bırakın)* |
| İzin Verilen IPs | *(boş bırakın — Zapier dinamik IP'ler kullanır)* |
|

Sadece **Siparişler** kapsamı verildiğinden, bu token herhangi bir şekilde açıklansa bile ürünleri, müşteri mesajlarını, personel hesaplarını veya mağazanızın diğer bölümlerini etkileyemez. Kaydetmekten sonra tokenın tam değerini kopyalayın ve Zapier'in Spwig entegrasyonu ayarlarına yapıştırın.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- Her token'a açık ve belirli bir isim verin — aylar sonra sorun giderirken `Shopify Sync v2` gibi isimler, `Token 3` gibi isimlerden çok daha faydalıdır
- Her entegrasyon için ayrı bir token oluşturun — bir entegrasyonun ihlal edildiğini fark ederseniz, sadece o token'ı iptal edebilir ve diğerlerini etkilemeden devam edebilirsiniz
- **Entegrasyonun gerçekten ihtiyaç duyduğu kapsamları verin** — bir raporlama aracı sadece Satış Analitiği veya Web Analitiği'ne Okuma erişimi gerektirir, Ürünler veya Personel & Roller üzerinde Okuma & Yazma erişimi gerekmez
- Bir token'ı üçüncü bir partiye vermeden önce, değişiklik formunda **"Bu token şu alanlara erişim sağlar:"** özetini kontrol edin — bu, kasten daha fazla erişim verdiğinizden emin olmanın en hızlı yolu olur
- Yazma erişiminin, token'ı oluşturan personelin kendi rolüne de bağlı olduğunu unutmayın — bir kapsamda Okuma & Yazma gösteriliyor ancak yazmalar hâlâ başarısız oluyorsa, o kullanıcının rol izinlerini de kontrol edin
- Tek seferlik projeler veya geçici entegrasyonlarda kullanılan token'lar için bir son kullanma tarihi belirleyin — bu, unutulmuş token'ların sonsuza kadar aktif kalmaya devam etme riskini azaltır
- Token listesini birkaç ayda bir gözden geçirin ve **Son Kullanım** tarihi beklenmedik şekilde eski olan token'ları devre dışı bırakın, çünkü bu, artık çalışan entegrasyonlara ait olabilir
- Bir token'ın açıklığa çıkmış olabileceğini düşünüyorsanız, hemen devre dışı bırakın, bir değiştirme oluşturun ve etkilenen entegrasyonu güncelleyin, sonra erişimi yeniden etkinleştirin