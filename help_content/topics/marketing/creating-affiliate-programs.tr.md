---
title: Affiliate Programları Oluşturma
---

Affiliate programları, ortaklarınızın müşterileri mağazanıza yönlendirdiklerinde nasıl komisyon kazanacaklarını tanımlar. Her program kendi komisyon yapısına, izleme kurallarına ve ödeme eşiklerine sahiptir. Farklı affiliate segmentleri için — örneğin etkili olanlar, içerik yaratıcıları veya toplu yönlendirme ortakları — birden fazla program oluşturabilirsiniz.

![Program Listesi](/static/core/admin/img/help/creating-affiliate-programs/programs-list.webp)

## Program Bileşenleri

Her affiliate programı aşağıdaki bileşenlerden oluşur:

- **Ad ve Açıklama** — Programı tanımlayın ve affiliate'lerle paylaşın
- **Komisyon Yapısı** — Satış başına affiliate'lerin ne kadar kazanacağını (oran veya sabit tutar)
- **Çerez Ömrü** — Bir tıklama sonrası yönlendirme izleme ne kadar sürer (1-365 gün)
- **Otomatik Onay** — Yeni affiliate'lerin otomatik olarak katılması gerekip gerekmediği veya manuel inceleme gerektirip gerektirmeyeceği
- **Minimum Ödeme Eşik** — Affiliate'lerin ödeme talep etmeden önce kazanması gereken miktar
- **Durum** — Aktif, duraklatılmış veya arşivlenmiş

## Komisyon Türleri

Programınızı oluştururken iki komisyon modeli arasında seçim yapabilirsiniz:

| Tür | Nasıl Çalışır | Ne Zaman Kullanılır | Örnek Hesaplama |
|------|-------------|-------------|---------------------|
| **Yüzde** | Affiliate, sipariş alt toplamının bir yüzdesi kazanır | Sipariş değeriyle birlikte büyüyen ölçeklenebilir ödüller | 150 dolarlık siparişin %10 = 15 dolarlık komisyon |
| **Sabit Tutar** | Affiliate, satış başına sabit bir tutar kazanır | Tahmini maliyetler; yüksek hacimli, düşük marjlı ürünler için en iyisidir | Sipariş değeri ne olursa olsun her satış için 25 dolar |

**Yüzde komisyonları** doğal olarak ölçeklenir — affiliate'ler yüksek değerli müşteriler yönlendirirlerse daha fazla kazanırlar. Bu, onların teşviklerini sizinkilerle hizalayarak ve genellikle en yaygın modeldir (tipik olarak 5–15%).

**Sabit komisyonlar**, hizmetler, abonelikler veya toplu yönlendirme programları gibi, satıslarınızın tahmini maliyetlerini isterseniz iyi çalışır. Bu, anlaşılması ve bütçelendirilmesi kolaydır, ancak büyük siparişler getiren affiliate'leri yetersiz ödüllendirir olabilir.

## Program Oluşturma

**Pazarlama > Affiliate Programları**'na gidin ve **+ Program Ekle**'ye tıklayın.

### Adım Adım Kurulum

1. **Program Adı**
   Affiliate'ler tarafından görülebilecek açıklayıcı bir ad girin (örneğin, "Ortak Program" veya "Etkili Seviye").

2. **Slug**
   İsimden otomatik olarak oluşturulan URL dostu bir tanımlayıcı. URL'lerde ve iç başvurularda kullanılır. Gerekirse özelleştirebilirsiniz.

3. **Açıklama**
   Program faydalarını ve koşullarını açıklayan isteğe bağlı metin. Affiliate'ler, katılabilecekleri programları incelediğinde bunu görürler.

4. **Komisyon Türü**
   **Yüzde** veya **Sabit Tutar** seçin.

5. **Komisyon Değeri**
   - Yüzde için: 0 ile 100 arasında bir değer girin (örneğin, 10% için `10`)
   - Sabit tutar için: Satış başına dolar tutarını girin (örneğin, 25 dolar için `25.00`)

6. **Çerez Ömrü Günleri**
   İzleme çerezinin kaç gün sürer (1–365). Aşağıdaki bölümde rehberlik için bilgi edinin.

7. **Affiliate'leri Otomatik Onayla**
   - **Onaylı** — Yeni affiliate'ler otomatik olarak katılır
   - **Onaysız** — Her başvuru için manuel inceleme ve onay yapmanız gerekir

8. **Minimum Ödeme**
   Affiliate'lerin ödeme talep etmeden önce biriktirmesi gereken minimum bakiye (örneğin, 50 dolar için `50.00`).

9. **Durum**
   Yeni affiliate'leri kabul etmek ve yönlendirmeleri izlemek için **Aktif** olarak ayarlayın.

10. **Programı Kaydet**

## Çerez Ömrü Açıklaması

Çerez ömrü, Spwig'in bir müşteriye affiliate'ın yönlendirme bağlantısını tıklattığını ne kadar süre hatırlayacağını belirler.

### Nasıl Çalışır

1. Bir müşteri, affiliate'ın bağlantısını tıklar
2. Spwig, müşterinin tarayıcısında bir izleme çerezini ayarlar
3. Müşteri, çerez ömrü içinde bir satın alma tamamlarsa, sipariş affiliate'ye atfedilir
4. Çerez süresi bitmeden önce satın alma tamamlanmazsa, affiliate komisyon kazanmaz

### Süre Seçimi

| Süre | Kullanım Durumu | Tipik Senaryo |
|----------|----------|------------------|
| **1–7 gün** | Anlık satın almalar, flash satışı | Hızlı tüketici malları, sınırlı süreli teklifler |
| **30 gün** | Standart e-ticaret | Genel çevrimiçi perakende, varsayılan önerme |
| **60–90 gün** | Düşünülen satın almalar | Yüksek değerli ürünler, B2B, hizmetler |
| **180+ gün** | Uzun satış döngüleri | Kurumsal yazılım, abonelikler, lüks mallar |

**Sektör standartı 30 gündür.** Bu, affiliate'ler için adil atama ve pratik izleme sınırlarını dengeler. Daha kısa ömürler, hızlı dönüşüm yapan müşterilere fayda sağlar; daha uzun ömürler, müşterilere araştırma yapma ve satın almayı tamamlama zamanı verir.

### Teknik Not

Çerez ömrü sadece **atama**'yı etkiler. Onaylanan komisyonlar sonsuza kadar geçerlidir — çerez ömrü, siparişin ilk olarak affiliate'ye kredite edilip edilmeyeceğini belirler.

## Otomatik Onay Ayarları

Otomatik onay ayarı, yeni affiliate başvurularının manuel inceleme gerektirip gerektirmeyeceğini kontrol eder.

### Otomatik Onayı Etkinleştirme Zamanı

- **Açık programlar** — Affiliate tabanınızı hızlıca büyütmek istiyorsanız ve tıkanıklık olmaması istiyorsanız
- **Düşük riskli ürünler** — Fraude veya marka riski minimaldir
- **Yüksek hacimli programlar** — Çok sayıda başvurunun beklenmesi ve her birini manuel inceleyememeniz

### Manuel İnceleme Gerektiren Zamanlar

- **Davet etme programları** — Sadece önceden incelenmiş ortakları kabul edersiniz
- **Premium programlar** — Yüksek komisyon oranları veya özel faydalar
- **Marka hassasiyetli ürünler** — Affiliate'lerin marka değerlerinizle uyumlu olduğundan emin olmak istiyorsunuz
- **Fraude önleme** — Şüpheli hesapları ekranlamak istiyorsunuz

### Güvenlik Dikkatleri

Affiliate'leri manuel incelemek, aşağıdaki durumları önlemeye yardımcı olur:
- Kendi yönlendirme şemaları (affiliate'lerin kendi hesaplarını oluşturarak komisyon kazanmaya çalışması)
- Tescil ihlalleri (affiliate'lerin ödemeli arama'da marka terimleriniz için teklif vermesi)
- Marka uyumsuzluğu (affiliate'lerin ürünleri uygun olmayan bağlamda tanıtmaları)

Çoğu mağaza için başlangıçta **manuel onay** daha güvenlidir. Güven kalıpları oluşturduktan sonra otomatik onayı her zaman etkinleştirebilirsiniz.

## Minimum Ödeme Eşik

Minimum ödeme eşikleri, birçok küçük ödeme işleme neden olan idari yükü azaltır.

### Neden Minimum Ayarlamak

- **İşlem ücretlerini azaltır** — Ödeme sağlayıcıları işlem başına ücret alır, bu yüzden ödemeleri birleştirme para tasarrufu sağlar
- **Muhasebeyi basitleştirir** — Daha az ödeme olayı, daha az dengeleme işi anlamına gelir
- **Sektör standartları** — Çoğu affiliate programında minimumlar vardır ($25–$100)

### Tipik Eşikler

| Eşik | Kullanım Durumu |
|-----------|----------|
| **$25–$50** | Yüksek hacimli programlar, burada affiliate'ler hızlıca minimuma ulaşır |
| **$50–$100** | Çoğu program için standart eşik |
| **$100–$200** | Premium programlar veya yüksek işlem ücretleri olan uluslararası ödemeler |

### Affiliate Memnuniyetini Dengeler

Eşik **çok yüksek** ayarlanırsa, affiliate'ler ilk ödeme talep etmeden aylar beklemek zorunda kalabilir. Eşik **çok düşük** ayarlanırsa, idari yük artar ve ücretlerle marjınız azalabilir.

**Öneri:** 50 dolarla başlayın. Bu, aktif affiliate'lerin ilk birkaç satışlarında ulaşabileceği kadar düşük, ancak ödemeleri etkili bir şekilde birleştirebileceğiniz kadar yüksek bir eşik.

### Maksimum Yok

Maksimum bir bakiye yoktur — affiliate'ler ödeme talep etmeden önce kazançlarını sonsuza kadar biriktirebilir. Bazı affiliate'ler, vergi planlama için yıllık veya çeyrek bazında taleplerini birleştirmeyi tercih eder.

## Program Durumu Yönetimi

Programlar şu üç durumdan birinde olabilir:

| Durum | Açıklama | Davranış |
|--------|-------------|----------|
| **Aktif** | Program çalışıyor | Yeni affiliate'leri kabul eder, yönlendirmeleri izler, komisyonları hesaplar |
| **Duraklatılmış** | Geçici olarak devre dışı bırakılmış | Mevcut affiliate'ler hala aktif ancak yeni başvurular yok; mevcut yönlendirme çerezleri hala çalışır |
| **Arşivlenmiş** | Kalıcı olarak kapatılmış | Yeni affiliate'ler yok, yeni yönlendirmeler izlenmez; geçmiş veriler raporlama için korunur |

### Programı Duraklatma Zamanı

- Komisyon oranlarını veya koşulları gözden geçiriyorsanız
- Bu çeyrekte affiliate ödemeleri için bütçenizi aşıyor olabilirsiniz
- Yeni bir program yapısını test ediyorsanız ve eski programın yeni affiliate'lerin katılması önlenmeli

Duraklatılmış programlar, mevcut izleme çerezlerini ve bekleyen komisyonları hala onaylar — sadece yeni affiliate'lerin katılması engellenir.

### Programı Arşivleme Zamanı

- Programı yeni bir yapıyla değiştirdiniz
- Program zaman sınırlıydı (örneğin, mevsimsel kampanya)
- Birden fazla programı bir tane programa konsolide ediyorsunuz

Arşivlenmiş programlar, geçmiş raporlamalar için veritabanında kalır ancak aktif yönetim görünümünden kaldırılır.

## Örnek Programlar

### Örnek 1: Influencer Programı (Yüzde)

| Alan | Değer |
|-------|-------|
| Ad | Influencer Programı |
| Komisyon Türü | Yüzde |
| Komisyon Değeri | 10 |
| Çerez Ömrü Günleri | 30 |
| Otomatik Onay | Onaysız (manuel inceleme) |
| Minimum Ödeme | 50.00 |
| Durum | Aktif |

**Kullanım Durumu:** Sosyal medya influencer'larını ve içerik yaratıcılarını işe alın. 10% komisyon, sipariş değerine göre ölçeklenir ve yüksek harcama yapan müşterileri çeken affiliate'leri ödüllendirir. Manuel onay, her influencer'ın kitle ve marka uyumunu incelemeyi sağlar.

### Örnek 2: Toplu Yönlendirme Programı (Sabit)

| Alan | Değer |
|-------|-------|
| Ad | Yönlendirme Ortak Programı |
| Komisyon Türü | Sabit Tutar |
| Komisyon Değeri | 25.00 |
| Çerez Ömrü Günleri | 7 |
| Otomatik Onay | Onaylı |
| Minimum Ödeme | 100.00 |
| Durum | Aktif |

**Kullanım Durumu:** Deal siteleri, kupon toplama siteleri ve yönlendirme ağları gibi yüksek hacimli yönlendirmeleri sağlayan ortaklarla işbirliği yapın. 25 dolar sabit komisyon, maliyetleri tahmin etmeyi kolaylaştırır ve kısa çerez ömrü (7 gün) hızlı dönüşümü hedefler. Bu ortaklar genellikle kendine hizmet verdiğinden otomatik onay etkinleştirilmiştir.

### Örnek 3: Premium Ortak (Yüksek Yüzde)

| Alan | Değer |
|-------|-------|
| Ad | Premium Ortak Seviyesi |
| Komisyon Türü | Yüzde |
| Komisyon Değeri | 15 |
| Çerez Ömrü Günleri | 90 |
| Otomatik Onay | Onaysız |
| Minimum Ödeme | 200.00 |
| Durum | Aktif |

**Kullanım Durumu:** En iyi performans gösteren affiliate'ler veya stratejik ortaklar için özel bir program. Daha yüksek komisyon (15%) kaliteli trafiği ödüllendirir ve 90 günlük çerez ömrü, daha uzun düşünme döngüsünü kapsar. Sadece davet etme seviyesi — bu, özel bir seviyedir.

## İpuçları

- Çoğu program için başlangıçta **yüzde komisyonu** (5–15%) kullanın — affiliate'lerle açıklamak daha kolaydır ve sipariş değerine göre doğal olarak ölçeklenir.
- **30 günlük çerez ömrü**'nü temel alın — bu, sektör standartıdır ve adil atama ile pratik izleme sınırları arasında dengedir.
- İlk olarak **manuel onay** etkinleştirin — affiliate'leri inceleyin, daha sonra güven kalıpları ve fraude kontrolü kurduktan sonra otomatik onayı etkinleştirin.
- **Minimum ödeme** eşiklerini 50–100 dolar arasında ayarlayın — affiliate memnuniyetini (çok yüksek olmayan bir eşik) ve idari verimliliği (çok sayıda küçük ödeme olmaması) dengeler.
- Farklı affiliate segmentleri (etkili olanlar, içerik siteleri, deal toplama siteleri) için **ayrı programlar** oluşturun — böylece performansı izleyebilir ve komisyon oranlarını bağımsız olarak ayarlayabilirsiniz.
- **Analitik panelleri** düzenli olarak izleyin — yüksek performans gösteren affiliate'leri tespit edin ve en iyi ortakları tutmak için komisyon oranlarını ayarlayın.