---
title: API Tokenları
---

API tokenları, dış hizmetlerin ve entegrasyonların mağazanızla iletişim kurmasına olanak tanıyan güvenli anahtarlardır. Bir üçüncü taraf hizmeti veya araç, mağazanızın verilerine erişmek veya eylemleri tetiklemek istiyorsa, her istekle birlikte bir API tokenu gönderir. Bu, mağazanızın isteğin yetkilendirildiğini doğrulamasını sağlar. Tüm tokenları, admin panelinizdeki API Tokenları bölümü üzerinden oluşturup yönetirsiniz.

## API tokenu ne zaman gerekir

Genellikle bir API tokenu oluşturmanız gereken durumlar şunlardır:

- Dış bir hizmet veya otomasyon aracı, mağazanıza okuma veya yazma işlemi yapması gerekiyorsa
- Gelen çağrıları doğrulamak için bir webhook alıcısı kuruyorsanız
- Kurulumunuz için Spwig Yardım Sistemi'ni ayarlarken
- Spwig API'sini kullanarak özel bir entegrasyon oluştururken
- Spwig mağazanızla başka bir sistem arasında veri senkronizasyonu yaparken

Her entegrasyonun kendi tokenı olmalıdır. Böylece bir hizmetin erişimini iptal etmeniz, diğerlerini etkilemeden yapılabilir.

## Token türleri

Bir token oluştururken, amacını tanımlayan bir tür seçersiniz. Bu tür, sadece referans olarak kullanılır ve her tokenın ne işe yaradığını takip etmenize yardımcı olur.

| Tür | Amacı |
|------|---------|
| **Yardım Sistemi** | Spwig yardım belgeleri sistemi tarafından kullanılır |
| **Dış Entegrasyon** | Üçüncü taraf hizmetler, otomasyon araçları (örneğin, Zapier) veya veri senkronizasyon araçları |
| **Webhook** | Webhook alıcıları veya uç noktaları için kimlik doğrulama |
| **Özel** | Yukarıdaki kategorilere uymayan herhangi bir diğer amaç |
| **Örnek Senkronizasyonu** | Spwig kurulumları veya dış Spwig hizmetleri arasında senkronizasyon |

## API tokenu oluşturma

1. **Ayarlar > API Tokenları** bölümüne gidin
2. **+ API Tokenu Ekle**'ye tıklayın
3. Tokenın kullanım amacını açıkça tanımlayan bir **Ad** girin (örneğin, `Zapier Ürün Senkronizasyonu` veya `Yardım Sistemi API`)
4. Uygun **Token Türünü** seçin
5. Entegrasyon hakkında daha fazla bilgi içeren isteğe bağlı bir **Açıklama** ekleyin
6. Gerekirse **Aktif** durumu, **Son Kullanım Tarihi** ve **İzin Verilen IP'ler** alanlarını yapılandırın (aşağıya bakın)
7. **Kaydet**'e tıklayın

Kaydetme işleminden sonra, tokenın tam değeri detay sayfasında görüntülenir. **Hemen kopyalayın** — token, listede gizlenmiş olarak gösterilir ve bu sayfadan ayrıldığınızda tam olarak tekrar elde edilemez.

![API Token Detay](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Token değeri güvenliği

Spwig, yeni bir token kaydedildikten hemen sonra yalnızca bir kez tam token değerini gösterir. Sonrasında, listede sadece gizlenmiş bir sürüm (örneğin, `spw_••••••••••••••••••••3f8a`) gösterilir.

Token değerini kaybettiyseniz, onu geri alamazsınız. Eski tokenı silmeniz ve yeni bir token oluşturmanız gerekir. Ardından, onu kullanan entegrasyonu güncellemeniz gerekir.

**Token değerlerini e-postalarda, sohbet mesajlarında veya kaynak kodunda asla paylaşmayın.** Bunları şifreler gibi tedirginlikle ele alın.

## Son kullanım tarihi ayarlama

**Son Kullanım Tarihi** alanı, tokenın otomatik olarak çalışmayı durduracağı bir tarih ve saat ayarlar. Tokenın son kullanma tarihi olmaması gerekiyorsa, bu alanı boş bırakın.

Son kullanım tarihleri, aşağıdaki durumlarda faydalıdır:

- Belirli bir son tarihe sahip geçici entegrasyonlar
- Üçüncü taraflara verilen tokenlar, otomatik erişim kaldırılması istendiğinde
- Yüksek yetkili entegrasyonlara ek bir güvenlik katmanı eklemek için

Token son kullanma tarihi geçtiğinde, onunla yapılan istekler reddedilir. Erişimi uzatmak için **Son Kullanım Tarihi** tarihini güncelleyebilir veya bir değiştirilmiş token oluşturabilirsiniz.

## Belirli IP adreslerine kısıtlama

**İzin Verilen IP'ler** alanı, IP adreslerinin bir listesini kabul eder. Bu liste boş değilse, token yalnızca bu adreslerden gelen istekler için çalışır.

Örneğin, analiz araçlarının çalıştığı sunucu `203.0.113.42` adresindeyse, bu IP adresini eklemek, tokenın başka bir yerden kötüye kullanılmasını önler, hatta bu IP adresi sızdırılmış olsa bile.

**İzin Verilen IP'ler** alanını boş bırakarak, herhangi bir IP adresinden gelen istekleri kabul edebilirsiniz.

## Token kullanımını izleme

Token listesi aşağıdaki bilgileri gösterir:

- **Kullanım Sayısı** — tokenın toplam kaç kez kullanıldığını gösterir
- **Son Kullanım** — tokenın bir istek yapmak için son kez ne zaman kullanıldığını gösterir

Bu alanlar, kullanılmayan tokenları (iptal edilmesi gereken adaylar) tanımanıza ve beklenmedik aktiviteyi tespit etmenize yardımcı olur.

Kullanım sayısında ani bir artış, tokenın amaçlanan entegrasyonun dışında biri tarafından kullanıldığını gösterebilir.

## Tokenı Geri Çekme

Tokenı silmeden hemen durdurmak için:

1. Token adını tıklayın
2. **Aktif** seçeneğini kaldırın
3. Kaydedin

Token, referans olarak listede kalır ancak sonraki tüm isteklerde reddedilir. Bu, bir sorun araştırırken geçici olarak bir entegrasyonu durdurmak gerektiğinde yararlıdır.

Tokenı kalıcı olarak kaldırmak için:

1. Listede onun yanındaki onay kutusunu seçin
2. Eylem menüsünden **Seçili API tokenlarını sil**'i seçin
3. Silmeyi onaylayın

Silindikten sonra token geri kazanılamaz. Entegrasyonun hâlâ erişim ihtiyacı varsa, yeni bir token oluşturun ve entegrasyonun yapılandırmasını güncelleyin.

## Örnek: Zapier entegrasyonunu ayarlama

**Senaryo:** Mağazanızı Zapier ile bağlamak istiyorsunuz ve sipariş bildirimlerini otomatikleştirmek istiyorsunuz.

| Alan | Değer |
|-------|-------|
| Ad | `Zapier Sipariş Otomasyonu` |
| Token Türü | Dış Entegrasyon |
| Açıklama | Zapier tarafından yeni siparişleri okumak ve bildirimleri tetiklemek için kullanılır |
| Aktif | Evet |
| Son Kullanım Tarihi | *(boş bırakın)* |
| İzin Verilen IP'ler | *(boş bırakın — Zapier dinamik IP'ler kullanır)* |

Kaydettikten sonra tokenın tam değerini kopyalayın ve Zapier'in Spwig entegrasyonu ayarlarına yapıştırın.

## İpuçları

- Her tokena açık ve spesifik bir isim verin — aylar sonra sorun giderirken `Shopify Sync v2` gibi isimler, `Token 3` gibi isimlerden çok daha faydalıdır
- Her entegrasyon için ayrı bir token oluşturun — bir entegrasyonun ihlal edildiğine dair bir şüphede olduğunuzda, diğerlerini etkilemeden sadece o tokenı geri çekebilirsiniz
- Tek seferlik projeler veya geçici entegrasyonlarda kullanılan tokenlara bir son kullanma tarihi belirleyin — bu, unutulmuş tokenların sonsuza kadar aktif kalmaması riskini azaltır
- Her birkaç ayda bir token listesinizi gözden geçirin ve **Son Kullanım** tarihi beklenmedik şekilde eski olan tokenları devre dışı bırakın, çünkü bu, artık çalışan entegrasyonlara ait olabilir
- Bir tokenın açıklığa çıkmış olabileceğini düşünüyorsanız, hemen devre dışı bırakın, bir değiştirici oluşturun ve etkilenen entegrasyonu güncelleyin, ardından erişimi yeniden etkinleştirmekten önce