---
title: Affiliate Program Overview
---

Spwig affiliate program özelliği, ürünleri tanıtma karşılığında komisyonlar kazanacak ortaklar kazanmanıza olanak tanır. Bu pazarlama kanalı, etkili olanlar, blog yazarları, içerik yaratıcıları ve marka elçileri gibi ortakların, kitlelerine özel izleme bağlantılarını paylaşarak, menfaatinizi genişletmenizi sağlar. Birinin bir ortağın bağlantısını tıklattıktan sonra bir satın alma yapması durumunda, ortak bir komisyon kazanır ve siz bir müşteri kazanırsınız.

Bu genel bakış, affiliate programının ne olduğunu, kimler için olduğunu ve ticari firmaların satışları artırmak için nasıl bir ortaklık ağı oluşturduğunu açıklar.

![Merchant Dashboard](/static/core/admin/img/help/affiliate-program-overview/merchant-dashboard.webp)

## Ana Kavramlar

Bu temel terimleri anlamanız, affiliate programınızı yapılandırmayı ve yönetmeyi yardımcı olacaktır:

| Terim | Tanım |
|------|------------|
| **Affiliate** | Ürünlerinizi tanıtacak ve yönlendirilen satışlar için komisyon kazanan bir ortak |
| **Program** | Oranlar, kurallar ve ayarlar içeren bir komisyon yapısı (birden fazla program oluşturabilirsiniz) |
| **Tracking Link** | Ortakın kodunu içeren benzersiz bir URL (örneğin, `yourstore.com/?ref=CODE`) |
| **Commission** | Yönlendirilen bir satış için affiliate'in kazandığı ödeme, program kurallarına göre hesaplanır |
| **Cookie Lifetime** | Bir müşteri bir affiliate bağlantısını tıklattıktan sonra izleme çerezinin ne kadar süreyle aktif kalacağı (gün cinsinden) |
| **Payout** | Birden fazla onaylanmış komisyonu tek seferde settle eden bir toplu ödeme |
| **Merchant Dashboard** | Programlarınızı, ortaklarınızı, komisyonlarınızı ve ödemelerinizi yönetmek için kullandığınız yönetici arayüzü |
| **Affiliate Portal** | Ortakların kazançlarını görüntüledikleri, izleme bağlantılarını aldıkları ve ödemeleri talep ettikleri kamuya açık yönetici paneli |

## Nasıl Çalışır

Affiliate iş akışı dört ana aşamadan oluşur:

### 1. Başvuru

Affiliates, mağazanızdaki `/affiliate/` adresindeki kamuya açık affiliate portalı üzerinden programınızı keşfeder ve başvuruları gönderir. Açık programlar için **otomatik onaylama** etkinleştirebilir veya davetli-only ortaklıklar için **manuel inceleme** yapabilirsiniz.

### 2. Onay

**Pazarlama > Ortaklar** bölümünde bekleyen başvuruları inceleyin. Her başvuruyu onaylamadan önce, ortağın web sitesini, sosyal medya varlığını ve hedef kitlenin uygunluğunu kontrol edin. Onaylandıktan sonra, affiliate, giriş bilgilerini alır ve yönetici paneline erişebilir.

### 3. Tanıt

Onaylanan affiliate'ler, portalından benzersiz yönlendirme bağlantılarını alırlar. Bu bağlantıları, blog yazılarında, sosyal medyada, e-posta bültenlerinde veya hedef kitlesiyle bağlantı kurdukları her yerde paylaşabilirler. Spwig, birinin bağlantıya tıkladığında izleme çerezini ayarlar.

### 4. Kazanç

Yönlendirilen bir müşteri, çerez ömrü boyunca bir satın alma tamamladığında, Spwig bir komisyon kaydı oluşturur. Komisyonları **Pazarlama > Komisyonlar** bölümünde inceleyip onaylayabilirsiniz. Affiliate'ler minimum ödeme eşik değerine ulaştığında ödemeleri işleme koyun.

## Merchant İş Akışı Genel Bakışı

Satıcı olarak, program yaşam döngüsünü tamamı yönetim panelinizden yönetirsiniz:

### Programlar Oluşturma

Önce **Pazarlama > Affiliate Programları** bölümünde bir veya daha fazla affiliate programı oluşturun. Her program, kendi komisyon yapısına, çerez ömrüne ve onay ayarlarına sahiptir. Influencer'lar için (daha yüksek komisyon) ve genel ortaklar için (daha düşük komisyon) ayrı programlar oluşturabilirsiniz.

### Başvuruları İnceleme

Yeni affiliate başvuruları, **Pazarlama > Ortaklar** bölümünde **Beklemede** durumunda görünür. Her başvuruyu inceleyerek, ortağın markanız için uygun olup olmadığını doğrulayın. Onaylayarak hesabını etkinleştirebilir veya nedeniyle reddedebilirsiniz.

### Komisyonları Onaylama

Affiliate'ler satışlar oluşturduğunda, komisyonlar **Pazarlama > Komisyonlar** bölümünde **Beklemede** durumunda görünür. Bağlantılı siparişi inceleyerek, bunun geçerli olup olmadığını doğrulayın (kendinden yönlendirme değil, iade edilen sipariş değil), ardından onaylayın veya reddedebilirsiniz.

### Ödemeleri İşleme

Affiliate'lerin onaylanmış komisyonları, minimum ödeme eşik değerini aştığında, **Pazarlama > Ödemeler** bölümünde toplu ödemeleri işleme koyun. Spwig, PayPal ve Airwallex ile otomatik ödemeler için entegre olur veya manuel banka transferlerini kaydedebilirsiniz.

## Affiliate İş Akışı Genel Bakışı

Affiliate'lerin programınızı nasıl deneyimlediklerini anlamak, daha iyi onboarding ve destek tasarlamaya yardımcı olur:

### Başvuru

Affiliate'ler, affiliate portalını ziyaret eder, program detaylarını (komisyon oranı, çerez ömrü, ödeme koşulları) okur ve iletişim bilgilerini ve tanıtım kanallarını içeren bir başvuru gönderir.

### Link Oluşturma

Onaylandıktan sonra, affiliate'ler, yönetici paneline girerek izleme bağlantılarını oluştururlar. Genel mağaza bağlantıları veya tanıtım istedikleri ürünler/kategoriler için bağlantılar oluşturabilirler.

### Tanıt

Affiliate'ler, potansiyel müşterilerle bağlantı kurdukları her yerde izleme bağlantılarını paylaşır — blog yazılarında, YouTube videolarında, Instagram hikayelerinde, e-posta bültenlerinde veya karşılaştırma sitelerinde.

### Ödeme Talep Etme

Affiliate'ler, affiliate portalı yönetici paneli üzerinden kazançlarını anlık olarak izlerler. Onaylanmış bakiyeleri minimum ödeme eşik değerine ulaştığında, ödeme talep edebilirler.

## Her Özellikin Nerede Olduğunu Bulun

| Özellik | Yönetici Konumu | Açıklama |
|---------|---------------|-------------|
| **Programlar** | Pazarlama > Affiliate Programları | Komisyon yapılarını oluşturun ve yapılandırın |
| **Affiliates** | Pazarlama > Ortaklar | Başvuruları inceleyin, affiliate hesaplarını yönetin |
| **Komisyonlar** | Pazarlama > Komisyonlar | Bekleyen komisyonları inceleyin ve onaylayın |
| **Ödemeler** | Pazarlama > Ödemeler | Affiliate'ler için toplu ödemeleri işleme koyun |
| **Ayarlar** | Pazarlama > Affiliate Ayarları | Genel ayarlar, ödeme sağlayıcıları, portal özelleştirmesi |
| **Dashboard** | Pazarlama > Affiliate Dashboard | Tıklamalar, siparişler ve komisyon toplamları ile analiz genel bakışı |

Kamuya açık portal, mağazanızın genel URL'sinde `/affiliate/` adresinde otomatik olarak mevcuttur.

## Ortak Kullanım Durumları

Satıcıların Spwig affiliate programını işlerini büyütmek için kullandığı dört ispatlanmış yoldan bahsediyoruz:

### Influencer Ortaklıklar

Markanızın alanına yönelik etkili sosyal medya influencer'ları ile ortaklık kurun. Kaliteli influencer'ları çekmek için daha yüksek komisyon oranları (15–20%) sunun. Her ortaklık için ROI'yi ölçmek için izleme bağlantılarını kullanın.

### Marka Elçileri

Markanızın sadık müşterilerinin bir ağı oluşturun ve onları marka savunucularına dönüştürün. Bu tekrarlayan müşterilere affiliate hesapları sunarak, arkadaşlarını ve ailelerini yönlendirerek komisyon kazanmalarını sağlayın. Bu, tutkulu topluluklarla birlikte özel ürünler için özellikle iyi çalışır.

### İçerik Yaratıcıları

Satın alma kılavuzları, incelemeler veya karşılaştırma içerikleri oluşturan blog yazarlarını, YouTuberi ve podcastcileri işe alın. Her ay aylık olarak sürekli yönlendirmeler oluşturabilen evergreen içerikle affiliate'ler için iyi çalışır.

### Yönlendirme Ağları

Mevcut müşterilerin programınıza katılmalarını ve sevdikleri ürünleri paylaşarak komisyon kazanmalarını sağlayın. Bu, memnuniyetli müşterilerin tanıtıcılar haline gelmesine neden olur ve yeni müşterileri getirir, bu da yeni müşterilerin affiliate olma ihtimalini artırır.

## İpuçları

- **Bir programla başlayın** — 10% komisyon oranı ve 30 günlük çerez ömrü ile genel ortak programı oluşturun. Hangi ortakların en iyi performansı gösterdiğini anladığınızda, daha sonra özel programlar ekleyebilirsiniz.
- **Açık uçlu beklentileri belirleyin** — Affiliate portalında onaylama sürecinizi, komisyon zamanlamalarınızı ve ödeme zamanlamasınızı belgeleyin. Şeffaflık, güven kurar ve destek taleplerini azaltır.
- **Kurallara uygunluk için izleyin** — Komisyonları inceleyin ve kendi başvuruları (ortakların kendi bağlantılarından alışveriş yapmaları), anormal yüksek iade oranları veya şüpheli tıklama desenleri gibi kırmızı bayrakları kontrol edin. Hileli komisyonları hemen reddedebilirsiniz.
- **Sık sık iletişim kurun** — Affiliate'lerinize aylık olarak program haberlerini, tanıtım takvimini ve en iyi performansları takdir etme ile ilgili güncellemeler gönderin. Aktif iletişim, affiliate'leri etkin tutar ve tanıtım yapmaya devam eder.
- **Mobil için optimize edin** — Çoğu affiliate, sosyal medya üzerinden bağlantı paylaşır ve buradan çoğu tıklama mobil cihazlardan gelir. Telefonlarda ödeme akışınızı test edin ve yönlendirilen müşteriler için kolay bir deneyim sağlayın.
- **Kreatif varlıklar sağlayın** — Affiliate'lerin ürünleri tanıtmasını kolaylaştırmak için, banner resimleri, ürün fotoğrafları ve içeriklerinde kullanabilecekleri önceden yazılan metinler sağlayın.