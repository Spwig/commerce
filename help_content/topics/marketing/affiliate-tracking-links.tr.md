---
title: Affiliate Tracking & Links
---

Affiliate tracking, müşterilerin satın almalarını referans veren affiliate'lerle ilişkilendirerek tamamı komisyon sisteminin gücünü sağlar. Bu kılavuz, takip bağlantılarının nasıl çalıştığını, müşterilerin bu bağlantıları tıkladığında Spwig'in ne tür veriler kaydettiğini ve cookie tabanlı atama sisteminin her komisyonu hangi affiliate'in kazanacağına nasıl karar verdiğini açıklar.

Takip mekaniklerini anlamanız, atama sorunlarını gidermenizi, bağlantı performansını analiz etmenizi ve affiliate'lerin dönüşüm oranlarını maksimize etmeleri konusunda onları eğitmeyi sağlar.

## Tracking Link Nedir?

Tracking link, müşterileri mağazanıza yönlendirirken affiliate'in kimliğini bir cookie'de kaydeden benzersiz bir URL'dir. Her affiliate, farklı hedeflere (ana sayfa, belirli ürünler, koleksiyon sayfaları veya landing sayfaları) yönlendiren birden fazla tracking linki oluşturabilir.

Tracking link formatı örneği:
```
https://yourstore.com/affiliate/track/a2b7f8c4d1e9/
```

Bu bağlantı, hedefe yönlendirirken, `a2b7f8c4d1e9` link koduna sahip affiliate'in gelecekteki satın almaları ile ilişkilendiren bir tracking cookie ayarlar.

Affiliate'ler, portal panellerinden bu bağlantıları oluşturur. Tam URL'yi kopyalarlar ve potansiyel müşterileri ulaşabildikleri her kanalda (blog yazıları, sosyal medya, e-postalar, vb.) paylaşabilirler.

## Tracking Link Bileşenleri

Her tracking link şu bileşenleri içerir:

| Bileşen | Örnek | Açıklama |
|---------|-------|----------|
| **Base URL** | `https://yourstore.com` | Mağazanızın etki alanı |
| **Tracking Yolu** | `/affiliate/track/` | Spwig'in tracking bitiş noktası |
| **Link Kodu** | `a2b7f8c4d1e9` | Otomatik olarak oluşturulan 12 karakterlik benzersiz kimlik |
| **Hedef** | Link oluşturulduğunda ayarlanır | Yönlendirme sonrası müşteriye giden yer (ana sayfa, ürün, vb.) |

Bir affiliate bir link oluşturduğunda, Spwig otomatik olarak benzersiz 12 karakterlik kodu oluşturur. Affiliate bu kodu elle oluşturmak veya düzenlemek zorunda değildir — sadece hedefi seçerler ve Spwig geri kalanını yönetir.

### Link Etiketleri (Opsiyonel)

Affiliate'ler, kendi organizasyonları için her link'e bir etiket ekleyebilir:
- "Instagram Bio Link"
- "YouTube Açıklaması"
- "Black Friday E-posta Kampanyası"

Etiketler, affiliate'lerin hangi promosyon kanallarının en iyi performansı gösterdiğini takip etmelerini sağlar. Bu etiketler sadece affiliate ve siz tarafından görülür — müşteriler asla etiketi görmez.

## Tracking Nasıl Çalışır?

Tracking ve atama süreci, tıklamadan komisyon oluşturma sürecinde beş adımdan oluşur:

### 1. Müşteri Linki Tıklar

Potansiyel bir müşteri, herhangi bir promosyon kanalından (sosyal medya gönderisi, blog makalesi, e-posta habercisi) affiliate'in tracking linkini tıklar.

### 2. Tıklama Kaydedilir

Spwig'in tracking bitiş noktası, tıklama ayrıntılarını kaydeder:
- IP adresi
- Kullanıcı ajanı (tarayıcı ve cihaz)
- HTTP refereri (tıklamanın nereden geldiğini gösterir)
- Zaman damgası
- Oturum kimliği

Bu veriler, **Tıklamalar** admin panelinde **Affiliate > Tıklamalar** altında analiz ve dolandırıcılık tespiti için görünür.

### 3. Cookie Ayarlanır

Tracking sistemi, müşteriye yönlendirilmeden önce tarayıcısında bir cookie ayarlar. Cookie şu bilgileri içerir:
- Affiliate ID (komisyonu kimin kazanacağı)
- Program ID (hangi komisyon yapısının uygulanacağı)
- Link kodu (hangi özel linkin tıklandığı)

### 4. Müşteri Satın Alır

Müşteri, mağazanızda tarifat yapar ve bir satın alma tamamlar. Bu hemen olabilir ya da günler veya haftalar sonra, ancak cookie ömrü penceresinde satın alma yapmaları süresince olabilir.

### 5. Komisyon Oluşturulur

Ödeme sırasında, Spwig affiliate cookie'sini kontrol eder. Eğer cookie bulunur ve hala geçerlidir (cookie ömrü içinde), sistem komisyon kaydı oluşturur ve bu komisyon kaydı, affiliate, program ve siparişe bağlı olarak **Beklemede** durumuna sahip olur.

## Cookie Tabanlı Atama

Tracking cookie, satın almaları affiliate'lerle ilişkilendiren temel mekanizmadır. Cookie'lerin nasıl çalıştığını anlamanız, optimal atama pencereleri ayarlamanız ve tracking sorunlarını gidermeniz açısından önemlidir.

### Cookie Yapısı

| Özellik | Değer |
|--------|-------|
| **Ad** | `aff_{program_id}` (örneğin, program ID 7 için `aff_7`) |
| **Değer** | Affiliate ID, link kodu ve zaman damgasını içeren JSON |
| **Alan** | Mağazanızın etki alanı |
| **Yol** | `/` (site genelinde erişim) |
| **Ömür** | Programın cookie ömrü (1–365 gün) |
| **HttpOnly** | `true` (güvenlik için JavaScript erişimini engeller) |
| **SameSite** | `Lax` (dış refererlardan tracking yapılmasını sağlar) |
| **Güvenli** | HTTPS sitelerinde `true` (tavsiyelidir) |

### Cookie Ömrü Penceresi

Cookie ömrü, müşterilerin bir affiliate linkini tıklattıktan sonra bir satın alma yapmaları için ne kadar süre olduğunu belirler. Bu pencere, **Pazarlama > Affiliate Programları** altında bir program oluştururken veya düzenlerken ayarlanır.

Sanayi standardı cookie ömrü:
- **7 gün**: Hızlı karar verme ürünleri (gida, etkinlik biletleri)
- **30 gün**: Standart e-ticaret (en yaygın ayarlama)
- **60–90 gün**: Düşünülen satın almalar (mobilya, elektronik, B2B ürünleri)
- **365 gün**: Uzun satış döngüleri (lakat ürünleri, yüksek ücretli hizmetler)

Eğer bir müşteri 1 Ocak'ta bir affiliate linkini tıklarsa ve cookie ömrünüz 30 günse, 30 Ocak'a kadar yapılan tüm satın almalar o affiliate'e kredi olur. 31 Ocak veya daha sonra yapılan satın almalar komisyon oluşturur çünkü cookie sona erdi.

### Son Tıklama Atama Modeli

Spwig, **son tıklama atama** kullanır: en son tıklanan affiliate linki kazanır. İşte bu nasıl çalışır:

**Senaryo**: Bir müşteri, Pazartesi affiliate A'nın linkini tıklar, sonra Çarşamba affiliate B'nin linkini tıklar, sonra Cuma günü satın alır.

**Sonuç**: Affiliate B komisyonu kazanır çünkü linki en son tıkladı.

Son tıklama cookie'si önceki affiliate cookie'lerini geçersiz kılar. Bu model, anlaşılması kolaydır ve çift komisyonları önler, ancak bu da her sipariş için sadece bir affiliate'in kredisi alacağı anlamına gelir (satın alma öncesi en son tıklama).

## Tıklama Kaydı

Spwig, her affiliate linki üzerindeki her tıklamayı kaydeder, böylece hem sizin hem de affiliate'lerin analizlerini sağlar. Tıklama verileri, link performansını ölçmek, dolandırıcılık tespiti yapmak ve promosyon stratejilerini optimize etmek için kullanılır.

### Her Tıklamada Kaydedilen Veri

**Affiliate > Tıklamalar** paneline giderek tüm kaydedilmiş tıklamaları görüntüleyebilirsiniz. Her girdi şu bilgileri içerir:

| Alan | Açıklama |
|------|----------|
| **Link** | Hangi tracking linkinin tıklandığı |
| **Affiliate** | Linki oluşturan kişi |
| **IP Adresi** | Müşterinin IP'si (dolandırıcılık tespiti için) |
| **Kullanıcı Ajanı** | Tarayıcı ve cihaz bilgisi |
| **Referer** | Müşterinin linki tıkladığı sayfa (örneğin, "https://instagram.com") |
| **Oturum Kimliği** | Bu tarifat oturumu için benzersiz kimlik |
| **Zaman Damgası** | Tıklamanın tam tarihi ve saati |

### Tıklama Sınırlaması

Tıklama dolandırıcılığı ve bot saldırılarını önlemek için, Spwig her IP adresi için dakikada **100 tıklamayı** sınırlar. Aynı IP bu eşikleri aşırsa, ekstra tıklamalar göz ardı edilir ve tıklama sayacı artmaz.

Bu koruma, sahte tıklama istatistiklerini artırma girişimlerini engellerken, geçerli trafiği engellememektedir. Gerçek müşteriler, dakikada 100 tıklamayı asla aşmaz.

### Gizlilik Dikkatinde Olunma

Tıklama verileri, dolandırıcılık tespiti için IP adreslerini ve kullanıcı ajanlarını içerir. Gizlilik politikasınızda, affiliate referanslarını izlediğinizi ve affiliate'lerle anonim performans verilerini paylaşacağınızı açıklayınız.

## Affiliate Linklerini Görüntüleme

Tüm affiliate tarafından oluşturulan tracking linkleri, izleme ve yönetim için admin panelinizde görünür.

### Link Listesine Erişim

**Affiliate > Linkler** paneline giderek tüm affiliate ve programlar için tracking linklerini görüntüleyebilirsiniz. Liste görünümü şu bilgileri gösterir:

- **Link Kodu**: Benzersiz 12 karakterlik kimlik
- **Affiliate**: Linki oluşturan kişi
- **Program**: Hangi komisyon yapısının uygulanacağı
- **Etiket**: Affiliate tarafından sağlanan isteğe bağlı açıklama
- **Hedef**: Linkin müşterileri yönlendirdiği yer
- **Toplam Tıklamalar**: Tüm zaman boyunca tıklama sayısı
- **Aktif Durum**: Linkin şu anda takip etmeye devam edip etmediği

### Linkleri Filtreleme

Admin filtrelerini kullanarak listeyi daraltabilirsiniz:
- **Affiliate'e Göre**: Belirli bir ortak için tüm linkleri görüntüleyin
- **Programa Göre**: Belirli bir komisyon yapısını tanıtan linkleri görüntüleyin
- **Aktif Duruma Göre**: Devre dışı bırakılmış linkleri bulun

Bu filtreleme, affiliate ağı boyunca link dağılımını analiz etmenizi ve en iyi performansı gösteren linkleri tanımlamanızı sağlar.

## Link İstatistikleri

Her tracking link, affiliate'lerin promosyon stratejilerini optimize etmelerine ve sizin en iyi performansı gösteren ortaklarınızı tanımlamanıza yardımcı olan performans metriklerini biriktirir.

### Bir link kaydını tıklayarak detaylı istatistikleri görüntüleyin:

| Metrik | Açıklama | Hesaplama |
|--------|----------|-----------|
| **Toplam Tıklamalar** | Link oluşturulmasından beri kaydedilmiş tüm tıklamalar | Tıklama kaydı sayısı |
| **Tıklamalar (7 gün)** | Son etkinlik göstergesi | Geçmiş 7 gün içindeki tıklamalar |
| **Dönüşümler** | Bu link'e atanan siparişler | Bu link kodundan gelen komisyon sayısı |
| **Dönüşüm Oranı** | Tıklamaların ne kadarının satın alıma dönüşmüş | (Dönüşümler ÷ Toplam Tıklamalar) × 100 |
| **Toplam Gelir** | Bu link'ten gelen tüm sipariş değerlerinin toplamı | Dönüşmüş tıklamalar için sipariş toplamlarının toplamı |

### İstatistikleri Kullanarak Optimizasyon

**Affiliate'ler için**: Bu sayılar, hangi promosyon kanallarının en iyi çalıştığını gösterir. Eğer bir Instagram bio linki %5 dönüşüm oranı gösterirken, bir blog yazısı linki %15 dönüşüm oranı gösteriyorsa, affiliate blog içeriğine daha fazla odaklanmalıdır.

**Satıcılar için**: Link istatistikleri, hangi affiliate'lerin kaliteli trafiği getirdiğini gösterir. Yüksek tıklama sayıları ama düşük dönüşüm oranları, affiliate'in izleyicisinin ürünleriniz için uygun olmayabileceğini gösterir.

## Linkleri Yönetme

Yönetim ve sorun giderme amaçlı, affiliate linklerini admin panelinden yönetebilirsiniz.

### Linkleri Devre Dışı Bırakma

Bir linkin yeni tıklamaları izlemeden eski verileri korumak için:

1. **Affiliate > Linkler** paneline gidin
2. Devre dışı bırakmak istediğiniz linki tıklayın
3. **Aktif** kutusunu kaldırın
4. **Kaydet**'e tıklayın

Devre dışı bırakılmış linkler, müşterileri hedefe yönlendirir, ancak izleme cookie'leri ayarlamaz veya tıklamaları kaydeder. Bu, bir affiliate'in geçici bir kampanya yürütmesi veya belirli bir promosyon kanalını devre dışı bırakmanız gerektiğinde yararlıdır.

### Link Detaylarını Düzenleme

Aşağıdakileri değiştirebilirsiniz:
- **Etiket**: Affiliate tarafından sağlanan açıklamayı güncelleyin
- **Hedef**: Linkin yönlendirildiği yeri değiştirin (örneğin, bir ürün sayfası taşındığında yararlıdır)
- **Aktif durum**: İzlemeyi etkinleştirmek veya devre dışı bırakmak

Link kodunu düzenleyemezsiniz — bu kalıcıdır ve geçmiş tıklama ve komisyon verileriyle ilişkilidir.

### Kullanılmayan Linkleri Silme

Kullanılmayan ve geçmiş tıklamaları veya dönüşümleri olmayan linkleri silin. Bu, link listesini temiz tutar ve değerli analiz verilerini kaybetmeden.

**Uyarı**: Bir linki silmek, ilişkili tüm tıklama kayıtlarını siler. Sadece tıklama sayısı sıfır olan linkleri silin veya geçmiş verilerin kesinlikle ihtiyaç duyulmadığından emin olun.

## Atama Modeli

Spwig'in atama mantığını anlamanız, affiliate'lerle beklentilerinizi ayarlamanıza ve komisyon anlaşmazlıklarını gidermenize yardımcı olur.

### Son Tıklama Atama

Daha önce belirtildiği gibi, Spwig, son tıklama atama kullanır: bir müşteri birden fazla affiliate linkini tıklattıktan sonra satın alırsa, sadece en son tıklanan affiliate komisyon kazanır.

**Avantajlar**:
- Anlaşılması ve açıklanması kolaydır
- Çift komisyonları önler
- Satın alma tamamlama yapan affiliate'leri ödüllendirir

**Dezavantajlar**:
- Müşteriyi tanıtan erken affiliate'ler kredi alamaz
- Çoklu dokunum müşteri yolculuklarını yansıtmaz
- Affiliate'lerin yüksek niyetli müşterileri hedeflemesini teşvik edebilir ("link hırsızlığı")

### Cookie Ömrü, Elde Edilebilirliki Belirler

Sadece cookie ömrü penceresi içindeki satın almalar komisyon oluşturur. Eğer cookie önceden ödeme sırasında sona ererse, müşteri bir favori olarak geri dönsede komisyon oluşturulmaz.

**Örnek**: 30 günlük cookie ömrü
- Müşteri 1 Ocak'ta linki tıklar → Cookie ayarlanır, 31 Ocak'ta sona erer
- Müşteri 25 Ocak'ta satın alır → Komisyon oluşturulur
- Müşteri 5 Şubat'ta satın alır → Komisyon oluşturulmaz (cookie sona erdi)

### Oturum Takibi

Cookie'lerin yanı sıra, Spwig her tıklamada oturum kimliğini takip eder. Bu, cookie'ler engellenmiş veya temizlenmiş olsa bile, aynı oturum içindeki birden fazla ziyaret için çoklu dokunum atama sağlar.

Bir müşteri bir linki tıklar, mağazanızda tarifat yapar, birden fazla sayfa yüklenir ve sonra satın alır — tüm bu işlemler aynı oturumda gerçekleşirse, affiliate'ler hala kredi alır çünkü kalıcı bir cookie ayarlanmamıştır.

## Sorun Giderme

Yaygın tracking sorunları ve çözümleri:

### Link Tıklamalarını Takip Etmiyor

**Belirtiler**: Affiliate'lerin linki paylaşmasından sonra tıklama sayısı sıfır kalmaya devam ediyor.

**Nedenleri ve çözümleri**:
1. **Link devre dışı bırakılmış**: Link detay sayfasında **Aktif** durumunu kontrol edin
2. **Program devre dışı bırakılmış**: **Affiliate > Programlar** paneline gidin ve programın durumunun **Aktif** olduğundan emin olun
3. **Affiliate hesabı devre dışı bırakılmış**: **Affiliate > Affiliate'ler** panelinde affiliate hesabının durumunu kontrol edin
4. **Tıklama sınırlaması**: Aynı IP'nin aşırı tıklama üretip üretmediğini kontrol edin (bot trafiği)

### Düşük Dönüşüm Oranı

**Belirtiler**: Yüksek tıklama sayıları ama çok az sipariş ataması.

**Nedenleri ve çözümleri**:
1. **Cookie ömrü çok kısa**: Ürünlerinizin araştırmaya ve düşünmeye ihtiyaç duyuyorsa, programın cookie ömrünü artırın
2. **Hedef sayfa kalitesi**: Hedef sayfayı kontrol edin — mobil dostu mu? Hızlı yüklüyor mu? Ürün stokta mı?
3. **Hedef kitle uyumsuzluğu**: Affiliate'in izleyicisi ürünleri uygun olmayabilir
4. **Tarayıcı cookie'leri engelliyor**: Bazı gizlilik araçları üçüncü taraf cookie'leri engeller, ancak Spwig, birinci taraf cookie'leri kullanır ki bu daha az engellenir

### Çift Tıklama Kayıtları

**Belirtiler**: Aynı müşteri, kısa sürede birden fazla tıklama kaydı oluşturur.

**Neden**: Bu normal davranıştır. Tracking linkinin her sayfa yükleme işlemi, bir tıklama kaydı oluşturur. Eğer bir müşteri bir linki tıklar, sayfa yavaş yüklenebilir ve tekrar tıklarsa, birden fazla kayıt görülebilir.

**Çözüm**: Herhangi bir eylem gerekmez. Tıklama sınırlayıcı, kötü amaçlı tıklamaları engeller (100 tıklama/dakika/IP), ve aynı oturumda çift tıklamalar atama üzerinde etkili değildir — sadece bir cookie ayarlanır.

## İpuçları

- **Lansman öncesi tracking testi yapın** — Test affiliate hesabı oluşturun, tracking linki oluşturun, gizli tarayıcıda linki tıklayın ve test satın almayı tamamlayın. Komisyonun doğru affiliate atamasıyla birlikte görünür olup olmadığını kontrol edin.
- **Affiliate'leri cookie ömrü hakkında eğitin** — Affiliate'lerin sadece cookie penceresi içindeki satın almalar için komisyon kazanacaklarını emin olun. Bu, gerçekçi beklentileri ayarlamanıza ve yüksek niyetli trafiği odaklanmalarına yardımcı olur.
- **Tıklama desenlerini dolandırıcılık için izleyin** — Bir IP'den anormal derecede yüksek tıklama sayısı veya kullanıcı ajanı dizisi olmayan tıklamalar bot trafiğini gösterebilir. Bu affiliate'leri komisyon onayı vermeden dikkatle inceleyin.
- **Link etiketlerini tutarlı şekilde kullanın** — Affiliate'leri, kanallara göre (Instagram, Blog, E-posta) linklerini etiketlemeye teşvik edin. Böylece, hangi promosyon kanallarının en iyi dönüşümleri sağladığını analiz edebilirsiniz.
- **Yüksek değerli ürünler için daha uzun cookie ömrü düşünün** — Ortalama sipariş değeri yüksek ve müşteriler genellikle satın almadan önce araştırmalar yaparsa, cookie ömrünü 60–90 güne uzatın. Bu, gecikmiş dönüşümleri yakalayabilir.
- **Referer verilerini kanal analizi için kontrol edin** — Referer alanı, tıklamaların nereden geldiğini gösterir. Eğer "instagram.com" veya "youtube.com" gibi birçok tıklama görürseniz, affiliate'lerin hangi sosyal platformları en etkili kullandığını biliyorsunuz.