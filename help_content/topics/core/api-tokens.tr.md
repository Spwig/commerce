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

Her entegrasyonun kendi tokenu olmalıdır, böylece bir hizmetin erişimini iptal etmeniz diğerlerini etkilemez.

## Token türleri

Bir token oluştururken, onun amacını tanımlayan bir tür seçersiniz. Bu tür, sadece referans olarak kullanılır ve her tokenın ne yaptığını takip etmenize yardımcı olur.

| Tür | Amacı |
|------|---------|
| **Yardım Sistemi** | Spwig yardım belgeleri sistemi tarafından kullanılır |
| **Dış Entegrasyon** | Üçüncü taraf hizmetler, otomasyon araçları (örneğin, Zapier) veya veri senkronizasyon araçları |
| **Webhook** | Webhook alıcıları veya uç noktaları için kimlik doğrulama |
| **Özel** | Yukarıdaki kategorilere uymayan herhangi bir diğer amaç |
| **Örnek Senkronizasyonu** | Spwig kurulumları veya dış Spwig hizmetleri arasında senkronizasyon |

## API kapsamları: bir tokenın neye erişebileceğini kontrol etme

Her token, **API Kapsamları** bölümüne sahiptir ve bu, tokenın mağazanızın hangi bölümlerine erişebileceğini belirler. Bir tokenun her şeyi erişim hakkı olmaması yerine, entegrasyonun gerçekten ihtiyaç duyduğu seviyede, bir alana bir seferde erişim izni verirsiniz.

**Hiçbir kapsam seçilmeden bir token, API'ye erişemez**, hatta aksi takdirde aktif ve geçerli olsa bile. Yeni bir token için bu varsayılan ayar olduğundan, bir entegrasyonun çalışması için ona erişim izni vermeniz gerekir.

Her kapsam için, üç erişim seviyesinden birini seçersiniz:

| Erişim Seviyesi | Ne izin verir |
|------------------|------------------|
| **Hiçbir erişim** | Token, bu alandaki herhangi bir uç noktaya çağrı yapamaz |
| **Okuma** | Token, bu alandan veri alabilir, ancak hiçbir şeyi değiştiremez |
| **Okuma & Yazma** | Token, bu alandan veri alabilir ve ayrıca oluşturabilir, güncelleyebilir veya silebilir |

Kapsamlar, yönetici panelinizin alanlarıyla eşleşecek şekilde gruplandırılmıştır:

| Grup | Kapsam | Okuma & Yazma mevcut mu? | Erişim sağlar |
|-------|-------|:---:|-------------------|
| Analitikler | **Satış Analitiği** | Sadece Okuma | Satış panoları, KPI'ler, ürün/müşteri/kategori analitiği, karşılaştırmalar ve dışa aktarma |
| Analitikler | **Web Analitiği** | Sadece Okuma | Ziyaretçi ve trafik analitiği: genel bakış, eğilimler, en çok ziyaret edilen sayfalar, coğrafi konum ve referanslar |
| Katalog | **Ürünler** | Evet | Ürünler, varyasyonlar, resimler, stok ayarlamaları ve öznitelik atamaları |
| Katalog | **Kategoriler** | Evet | Ürün kategorileri, resimler ve afişler dahil |
| Katalog | **Markalar** | Evet | Ürün markaları |
| Katalog | **Öznitelikler** | Evet | Ürün öznitelik tanımları |
| Katalog | **Stok** | Evet | Stok panoları, stok hızı, hareketler, yeniden sipariş önerileri ve stok ayarları |
| Siparişler | **Siparişler** | Evet | Siparişler, sipariş notları, durum/izleme güncellemeleri, iptaller, iadeler ve sipariş belgeleri |
| Müşteriler | **Müşteri Mesajları** | Evet | İletişim formlarından gelen müşteri mesajları ve sipariş notları, durum güncellemeleri ve yanıtlar |
| Mağaza & Ayarlar | **Mağaza Ayarları** | Evet | Mağaza ayarları, kullanılabilir diller ve markalama (ad, renkler, logolar) |
| Kullanıcılar & Erişim | **Personel & Roller** | Evet | Personel hesapları, davetler, roller ve izin kataloğu |

İki **Analitikler** kapsamı her zaman sadece okunabilir - raporlama verisi için "yazma" kavramı yoktur, bu yüzden seçici sadece **Hiçbir erişim** veya **Okuma** seçeneğini sunar.

[![API Scope Seçici, Analytics ve Catalog scope grupları üzerinde bir erişim notu](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)](https://example.com)

Scope seçici altında, **"Bu token şu alanlara erişebilir:"** başlığı altında, token'a verdiğiniz tüm scope'ları ve seviyelerini listeleyen bir özet vardır. Bu sayede token'ın erişimini hızlıca kontrol edebilirsiniz, picker'ı çözmeden.

!["Bu token şu alanlara erişebilir:" özetinin her bir verilen scope ve Read veya Read & Write seviyesini listelemesi](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)

### Bir token'un gerçekten hangi izinleri kullanır

Bir token'un scope'ları, onun yapabileceği şeyin *tepe noktası* - ama token, onu yaratan personelin gerçek dünyadaki izinlerini de miras alır:

- Token, yaratan personel bir superuser olsa bile, asla **superuser** gücü ile işlem yapamaz.
- Bir scope üzerindeki **Read & Write** sadece yaratan personelin rolü o alana yazma izni veriyorsa çalışır. Örneğin, Products için sadece görüntüleme izni olan bir personel, "Products: Read & Write" ile yarattığı bir token hala sadece okuyabilir - rol, scope'un üzerine ek bir kilit görevi görür.
- Eğer bir token yaratan personel silinir veya hesabı devre dışı bırakılır, token hemen API erişimini kaybeder, scope'ları ne olursa olsun - artık onun adına işlem yapacak bir izinli kullanıcı kalmamıştır.

Bu, token'ı güvenli şekilde sınırlamak için en emniyetli yolun, token'ı oluştururken, kendi rolü token'ın sahip olması gereken erişime eşleşen bir personel olarak oturum açmak anlamına gelir.

## API Token Oluşturma

1. **Ayarlar > API Token'lar** bölümüne gidin
2. **+ API Token Ekle**'ya tıklayın
3. Token'ın ne için kullanıldığını açıkça belirten bir **Ad** girin (örneğin, `Zapier Product Sync` veya `Help System API`)
4. Uygun **Token Türü**'nü seçin
5. Entegrasyon hakkında daha fazla bilgi içeren isteğe bağlı bir **Açıklama** ekleyin
6. **API Scope'ları** bölümünde, entegrasyonun ihtiyaç duyduğu her alanda **Erişim Yok**, **Okuma** veya **Okuma & Yazma** seçin - diğer tüm scope'ları **Erişim Yok** olarak bırakın
7. Gerekirse **Aktif** durumu, **Son Kullanım Tarihi** ve **İzin Verilen IP'ler** alanlarını yapılandırın (aşağıya bakın)
8. **Kaydet**'e tıklayın

Kaydetme işlemi tamamlandıktan sonra, token'ın tam değeri detay sayfasında görüntülenir. **Hemen kopyalayın** - token, listede görüntülenirken güvenlik nedeniyle maskelenir ve bu sayfadan ayrıldığınızda tam olarak tekrar elde edilemez.

![API Token Detay](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Token Değeri Güvenliği

Spwig, yeni bir token kaydettikten hemen sonra token değerinin tamamını yalnızca bir kez gösterir. Bunun ardından, listede sadece maskelenmiş bir sürüm (örneğin, `spw_••••••••••••••••••••3f8a`) gösterilir.

Eğer token değerini kaybederseniz, onu geri alamazsınız. Eski token'ı silmeniz ve yeni bir token oluşturmanız gerekir, ardından onu kullanan entegrasyonu güncellemeniz gerekir.

**Token değerlerini e-postalarda, sohbet mesajlarında veya kaynak kodunda asla paylaşmayın.** Onları şifreler gibi tedirgin edin.

## Son Kullanım Tarihi Ayarlama

**Son Kullanım Tarihi** alanı, token'ın otomatik olarak çalışmayı durduracağı bir tarih ve saat belirler. Token'ın son kullanma tarihi olmaması gerekiyorsa, bu alanı boş bırakın.

Son kullanma tarihleri şu durumlarda faydalıdır:

- Belirli bir son tarihe sahip geçici entegrasyonlar
- Üçüncü taraflara verilen token'lar için otomatik erişim kaldırma
- Yüksek yetkili entegrasyonlara ek bir güvenlik katmanı eklemek

Bir token son kullanma tarihine ulaştığında, onunla yapılan istekler reddedilir. Erişimi uzatmak için **Son Kullanım Tarihi** tarihini güncelleyebilir veya bir değiştirilmiş token oluşturabilirsiniz.

## Belirli IP Adreslerine Sınırlama

**İzin Verilen IP'ler** alanı, IP adreslerinin bir listesini kabul eder. Bu liste boş değilse, token sadece bu adreslerden gelen istekler için çalışır.

Örneğin, analiz araçlarının çalıştığı sunucu `203.0.113.42` adresindeyse, bu IP'yi eklemek token'ın başka bir yerden kötüye kullanılmasını önler, hatta token kaçak olursa bile.

**İzin Verilen IP'ler** alanını boş bırakarak, herhangi bir IP adresinden gelen istekleri kabul edebilirsiniz.

**Süre sonu ve IP kısıtlamaları, kapsamlardan bağımsız olarak kontrol edilir.** Süresi dolmuş veya allowlist dışında olan bir token, kapsamları dahi değerlendirilmeden reddedilir. Geniş kapsamlara sahip bir token, süresi dolunca veya listede olmayan bir IP adresinden çağrıldığında hemen reddedilir.

## Token ile API'yi Çağırma

Entegrasyonlar, Spwig'in admin API'sine erişmek için token'ı bir `Authorization` başlığı ile gönderir:

```
Authorization: Bearer <your-token-value>
```

Her admin API uç noktası `/api/admin/...` altında yer alır. Entegrasyonunuzu geliştiren geliştirici, hangi uç noktaların çağrılacağını belirler. Satıcı olarak, token'ın **API Kapsamları** ilgili uç noktaları kapsamasını sağlamaktan sorumlusunuz. İstek bir izin hatasıyla reddedilirse, ilk kontrol edilmesi gereken şey token'ın doğru erişim seviyesinde doğru kapsamın verilmiş olup olmadığıdır.

### Örnek: Web Trafik Analitiği Okuma

Spwig, `GET /api/admin/analytics/traffic/` uç noktasını, mağazanız için ziyaretçi ve trafik analitiği döndürür — ziyaretlerin ve benzersiz ziyaretçilerin genel bakışı, zaman içindeki eğilimler, en çok ziyaret edilen sayfalar, ziyaretçi coğrafyası ve referer kaynakları. Bu verilere raporlama aracı veya dashboard'ın okuyabilmesi için:

1. Bu entegrasyon için bir token (veya mevcut bir tokenı düzenleyin)
2. **API Kapsamları** altında **Web Analitiği**'ni **Oku** olarak ayarlayın
3. Tokenı kaydedin ve entegrasyona sağlayın

**Web Analitiği**, sadece okunabilir bir kapsam olduğu için "Oku & Yaz" seçeneği yoktur — entegrasyon sadece analitik verileri alabilir, mağazanızın yapılandırmasını asla değiştiremez.

## Token Kullanımını İzleme

Token listesi aşağıdaki bilgileri gösterir:

- **Kullanım Sayısı** — tokenın toplam kaç kez kullanıldığını gösterir
- **Son Kullanım Zamanı** — tokenın bir istek yapmak için son kez ne zaman kullanıldığını gösterir

Bu alanlar, kullanılmayan tokenları (iptal edilmesi gereken adaylar) tanımlamaya ve beklenmedik aktiviteyi tespit etmeye yardımcı olur. Kullanım sayısında ani bir artış, tokenın amaçlanan entegrasyonun dışında biri tarafından kullanılıyor olabileceğini gösterir.

## Tokenı İptal Etme

Tokenı silmeden hemen durdurmak için:

1. Token adını tıklayın
2. **Aktif** kutusunu kaldırın
3. Kaydedin

Token, listede referans olarak kalır ancak sonraki tüm isteklerde reddedilir. Bu, bir sorunla ilgili bir soruşturma yaparken entegrasyonu geçici olarak durdurmak gerektiğinde yararlıdır.

Tokenı kalıcı olarak kaldırmak için:

1. Listede tokenın onay kutusunu seçin
2. Eylem menüsünden **Seçilen API tokenlarını Sil**'i seçin
3. Silmeyi onaylayın

Silindikten sonra token geri kazanılamaz. Entegrasyonun hala erişim ihtiyacı varsa, yeni bir token oluşturun ve entegrasyonun yapılandırmasını güncelleyin.

## Örnek: Zapier Entegrasyonunu Kurma

**Senaryo:** Mağazanızı Zapier ile bağlamak istiyorsunuz, sipariş bildirimlerini otomatikleştirmek için.

| Alan | Değer |
|-------|-------|
| Ad | `Zapier Sipariş Otomasyonu` |
| Token Türü | Dış Entegrasyon |
| Açıklama | Zapier tarafından yeni siparişleri okumak ve bildirimleri tetiklemek için kullanılır |
| API Kapsamları | **Siparişler**: Oku & Yaz |
| Aktif | Evet |
| Süresi Bitirme | *(boş bırakın)* |
| İzin Verilen IPs | *(boş bırakın — Zapier dinamik IP'ler kullanır)* |
|

Yalnızca **Siparişler** kapsamı verildiğinden, bu token herhangi bir şekilde açıklansa bile ürünleri, müşteri mesajlarını, personel hesaplarını veya mağazanızın diğer bölümlerini etkileyemez. Kaydetmekten sonra tokenın tam değerini kopyalayın ve Zapier'in Spwig entegrasyonu ayarlarına yapıştırın.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- Her token'a açık ve spesifik bir isim verin — aylar sonra sorun giderirken `Shopify Sync v2` gibi isimler, `Token 3` gibi isimlerden çok daha faydalıdır
- Her entegrasyon için ayrı bir token oluşturun — bir entegrasyonun ihlal edildiğini fark ettiğinizde, sadece o token'ı iptal edebilir ve diğerlerini etkilemeden devam edebilirsiniz
- **Entegrasyonun gerçekten ihtiyaç duyduğu kapsamları verin** — bir raporlama aracı, Ürünler veya Personel & Roller üzerinde Okuma & Yazma erişimine ihtiyaç duymaz, sadece Satış Analitiği veya Web Analitiği üzerinde Okuma erişimine ihtiyaç duyar
- Bir token'ı üçüncü bir partiye vermeden önce, değişiklik formunda **"Bu token şu alanlara erişebilir:"** özeti kısmını kontrol edin — bu, kasten daha fazla erişim verdiğinizden emin olmanın en hızlı yolu olur
- Yazma erişiminin, token'ı oluşturan personelin kendi rolüne de bağlı olduğunu unutmayın — bir kapsamda Okuma & Yazma erişimi gösteriliyor ama yazmalar hala başarısız oluyorsa, o kullanıcının rol izinlerini de kontrol edin
- Tek seferlik projeler veya geçici entegrasyonlarda kullanılan token'lar için bir son kullanma tarihi belirleyin — bu, unutulmuş token'ların sonsuza kadar aktif kalmaya devam etme riskini azaltır
- Token listesini birkaç ayda bir gözden geçirin ve **Son Kullanım** tarihi beklenmedik şekilde eski olan token'ları devre dışı bırakın, çünkü bu token'lar artık çalışan entegrasyonlara ait olabilir
- Bir token'ın açıklığa çıkmış olabileceğini düşünüyorsanız, hemen devre dışı bırakın, bir değiştirme oluşturun ve etkilenen entegrasyonu güncelleyin, sonra erişimi yeniden etkinleştirin