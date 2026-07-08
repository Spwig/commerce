---
title: Affiliate Analytics & Reports
---

Affiliate analizleri, ortaklık programınızın performansını izlemenize ve en iyi performansı gösterecek ortakları belirlemenize yardımcı olur. Bu kılavuz, merchant panosunu kullanmayı, istatistikleri yorumlamayı, gelir eğilimlerini analiz etmeyi ve veriye dayalı kararlar vererek ortaklık programınızı optimize etmeyi gösterir.

## Merchant Panosu

**Ortaklık Programı > Dashboard**'a giderek kapsamlı affiliate analizlerine genel bakış elde edin.

Merchant panosu, aktif programlar, affiliate sayıları, komisyon aktivitesi ve gelir eğilimleri gibi tüm ortaklık programınızın performansının gerçek zamanlı bir özetini sağlar. Program sağlığı izlemek ve stratejik kararlar vermek için merkezi bir merkezdir.

![Merchant Dashboard](/static/core/admin/img/help/affiliate-analytics/merchant-dashboard.webp)

## Dashboard İstatistikleri

Dashboard, sayfa üstünde anahtar performans göstergelerini kart formatında gösterir.

### Genel İstatistikler

| İstatistik | Açıklama | Örnek Değer |
|-----------|-------------|---------------|
| **Toplam Programlar** | Oluşturulan toplam programlar (parantez içinde aktif sayı gösterilir) | 3 program (2 aktif) |
| **Aktif Ortaklar** | Ürünlerinizi tanıtıyor olan onaylanmış ortaklar | 47 ortak |
| **Bekleyen Başvurular** | Onayınızı bekleyen yeni ortak başvuruları | 8 bekleyen |
| **Toplam Tıklamalar** | Tüm affiliate izleme bağlantılarında ömür boyu tıklamalar | 12.543 tıklama |
| **Toplam Komisyonlar** | Oluşturulan komisyon kayıtlarının sayısı | 287 komisyon |
| **Bekleyen Tutar** | Onaylanan ancak ödeme bekleyen komisyonların toplam değeri | $4.235,50 |

Bu istatistikler, program ölçeğini ve finansal yükümlülükleri hızlıca görmek için kullanılır.

### Metrikleri Anlamak

- **Aktif Sayısı** — Şu anda başvuruları kabul eden ve komisyonlar oluşturan programların sayısı
- **Bekleyen başvurular** — Onay yükünüzü gösterir (yüksek sayılar daha sık başvuruların incelenmesi gerektiğini gösterir)
- **Toplam Tıklamalar** — Genel affiliate katılımı ve tanıtım aktivitesini ölçer
- **Bekleyen Tutar** — Ortaklara mevcut ödeme yükümlülüğünüzü temsil eder

## Gelir Grafiği

Dashboard, zaman içinde komisyon eğilimlerini gösteren 30 günlük gelir grafiği içerir. Grafiğin arka planı Chart.js ile oluşturulmuştur.

### Grafiğin Özellikleri

- **Zaman Aralığı** — 30 günlük komisyon aktivitesini gösterir
- **Günlük Ayrım** — Her çubuk, o gün oluşturulan komisyonları temsil eder
- **Hover Detayları** — Herhangi bir çubuğun üzerine gelerek tam tarihi ve komisyon toplamını görün
- **Trend Analizi** — Hızlıca büyüme desenlerini, mevsimsel eğilimleri ve anormallikleri tespit edin

### Grafiği Okuma

**Örnek Analiz:"

```
Gün 1-7:   $150-$200/gün  → Temel performans
Gün 8-14:  $300-$450/gün  → Kampanya sıçraması (başarılı olanları inceleyin)
Gün 15-21: $100-$150/gün  → Kampanya sonrası düşüş (beklenen)
Gün 22-30: $200-$250/gün  → Temel seviyesine dönme
```

Bu grafiği kullanarak:

- **Başarılı kampanyaları belirleyin** — Sıçramalar etkili tanıtım olduğunu gösterir
- **Mevsimsel desenleri tespit edin** — Yüksek tрафик dönemlerinde stok ve ortaklık tanıtımı planlayın
- **Sorunları tespit edin** — Aniden düşüşler izleme bağlantılarının bozulduğunu veya program sorunlarını gösterir
- **Değişiklikleri doğrulayın** — Komisyon oranları ayarlamadan önce ve sonra geliri karşılaştırın

## En İyi Performans Gösteren Ortaklar

Dashboard, en çok kazanç sağlayan en yüksek 10 ortakları gösteren bir tablo içerir.

### Ortaklık Performans Metrikleri

| Sütun | Açıklama | Örnek |
|--------|-------------|---------|
| **Ortak** | Ortakın adı ve benzersiz kodu | Sarah Johnson (AFF-12345) |
| **Toplam Gelir** | Bu ortakın ömür boyu satışları | $18.450,00 |
| **Siparişler** | Başarılı siparişlerin sayısı | 87 sipariş |
| **Komisyon Sayısı** | Oluşturulan komisyon kayıtlarının sayısı | 87 komisyon |
| **Toplam Ödemeler** | Bu ortak için şimdiye kadar yapılan ödeme miktarı | $2.767,50 |

Tablo, **toplam gelir** (en yüksekten en düşüğe) sıralanmıştır, böylece en değerli ortaklarınızı hızlıca belirleyebilirsiniz.

### En İyi Ortaklık Verilerini Kullanma

**VIP Ortaklarını Belirleyin:"

En iyi performans gösterenleri inceleyin ve aşağıdaki konuları göz önünde bulundurun:

- **Özel oranlar** — En iyi 3 ortakınıza daha yüksek komisyon oranları sunun (örneğin, 10%’den 12%’ye artırın)
- **Erken erişim** — En iyi ortaklara yeni ürünlerin veya satışların erken bildirimi sağlayın
- **Özel içerikler** — Kişiselleştirilmiş afişler veya ürün resimleri sağlayın
- **Doğrudan destek** — En iyi ortaklarınız için özel bir iletişim atayın

**Örnek:"

```
Ortak: Emily Chen (AFF-00123)
Gelir:   $24.500
Siparişler:    142
Ödemeler:   $2.450 (10% komisyon)

Eylem: 12% komisyon seviyesi sun + erken ürün erişimi
Beklenen etki: Bu ortaktan 20-30% gelir artışı
```

## Son Aktivite

Dashboard, bekleyen eylemleri izlemenize yardımcı olmak için son affiliate aktivitelerini gösterir.

### Son Başvurular

5 en son bekleyen affiliate başvurularını gösterir:

- Ortakın adı
- Başvuru tarihi
- Başvurulduğu program
- Hızlı **İnceleme** bağlantısı onaylamak veya reddetmek için

Bu bölüm, yeni affiliate başvurularını önceliklendirmenize ve başvuruların birikmesini önlemeye yardımcı olur.

### Son Komisyonlar

10 en son oluşturulan komisyonu (bekleyen durum) gösterir:

- Sipariş numarası (sipariş detaylarını görmek için tıklayın)
- Ortak adı
- Komisyon tutarı
- Oluşturulma tarihi
- Hızlı **Onayla** veya **Reddet** eylemleri

Günlük olarak bu bölümü inceleyin, komisyonların onay sürecinde ilerlemesini sağlayın.

## Program Seviyesinde İstatistikler

Bir programın ayrıntı sayfasına giderek program özelı analizlerini görün.

### Program İstatistiklerine Erişim

1. **Ortaklık Programı > Programlar**'a gidin
2. Analiz etmek istediğiniz programın adını tıklayın
3. Program ayrıntı sayfasında istatistikler panelini görün

### Program Özelı Metrikler

| Metrik | Açıklama | Ne Anlama Gelir |
|--------|-------------|---------------|
| **Aktif Ortaklar** | Bu programdaki onaylanmış ortaklar | 23 ortak |
| **Toplam Tıklamalar** | Bu programın izleme bağlantıları üzerindeki tıklamalar | 5.432 tıklama |
| **Toplam Komisyonlar** | Bu program için oluşturulan komisyon kayıtları | 127 komisyon |
| **Bekleyen Komisyonlar** | Bu program için henüz ödenmeyen komisyon değeri | $1.245,00 |

### Programın Yeni Ortakları

Program ayrıntı sayfası, bu programa katılan 10 en yeni ortakı gösterir, bunlar:

- Ortak adı ve kodu
- Katılım tarihi
- Başvuru durumu

Bu, program büyümesini izlemek ve hangi programların en çok ilgi gördüğünü belirlemek için kullanılır.

## Program Bazlı Ortaklık Performansı

Belirli bir programda, affiliate bazlı istatistikleri görün.

### Program Bazlı Ortakları Görüntüleme

1. **Ortaklık Programı > Programlar**'a gidin
2. Program adını tıklayın
3. **Ortaklar** bölümüne kaydırın
4. **Tüm Ortakları Görüntüle**'ye tıklayarak tam listeyi görün

Ortak listesi, **toplam komisyonlar** tarafından sıralanmıştır, böylece her programdaki en iyi performanları vurgular.

### Karşılaştırmalı Analiz

**Örnek: İki programı karşılaştırma"

**İnfluencer Programı (10% komisyon):"
- 47 aktif ortak
- 8.234 tıklama
- 187 komisyon
- Ortalama komisyon değeri: $32,50

**Toplu Referans Programı (sabit $25 komisyon):"
- 23 aktif ortak
- 3.421 tıklama
- 94 komisyon
- Ortalama komisyon değeri: $25,00

**Görüş:** Influencer programı daha yüksek katılımı ve komisyon değerlerine sahip, bu mağaza için yüzdelik bazlı komisyonların daha iyi işe yaradığını gösterir.

## Komisyon Raporları

Komisyon yönetimi, detaylı raporlama için gelişmiş filtreleme ve dışa aktarma yeteneklerine sahiptir.

### Komisyon Raporlarını Erişim

**Pazarlama > Komisyonlar**'a giderek filtreleme ile tam komisyon listesini görün.

### Gelişmiş Filtreleme

Filtreleme yan panelini kullanarak özel raporlar oluşturun:

- **Tarih Aralığına Göre** — Belirli tarihler arasında oluşturulan komisyonları seçin (örneğin, Ocak 1-31 için aylık raporlama)
- **Ortaklara Göre** — Bir ortak için tüm komisyonları görün
- **Programlara Göre** — Belirli bir programdan gelen komisyonları görün
- **Duruma Göre** — Sadece bekleyen, onaylanan, reddedilen veya ödenen komisyonları göster

### Dışa Aktarma Yetenekleri

Spwig yönetimi arayüzü, yerleşik dışa aktarma işlevlerine sahiptir:

1. Filtreleri uygulayarak komisyon listesini daraltın
2. Dışa aktarmak istediğiniz komisyonları seçin (veya "Tümünü Seç" kullanın)
3. **Eylemler** açılır menüsünden **Seçilenleri Dışa Aktar**'ı seçin
4. Biçim seçin (CSV, Excel)
5. Raporu indirin ve analiz için offline kullanın

**Ortak Raporları:"

- **Aylık komisyon özeti** — Tarih aralığına göre filtreleyin, tüm onaylanan komisyonları dışa aktarın
- **Ortaklık performansı** — Ortaklara göre filtreleyin, tüm komisyonları dışa aktarın ve ROI hesaplayın
- **Program karşılaştırması** — Her program için ayrı ayrı komisyonları dışa aktarın, tabloda karşılaştırın

## Ödeme Raporları

Ödeme yönetimi, finansal izleme ve dengeleme araçlarına sahiptir.

### Ödeme Raporlarını Erişim

**Ortaklık Programı > Ödemeler**'a giderek ödeme geçmişini ve istatistiklerini görün.

### Ödeme İstatistikleri

Ödeme panosu aşağıdaki durumları gösterir:

| Durum | Açıklama |
|--------|-------------|
| **Bekleyen** | Oluşturuldu ama henüz işlenmedi |
| **İşlenmekte** | Ödeme sağlayıcısına (PayPal/Airwallex) gönderildi |
| **Tamamlandı** | Ortaklara başarıyla ödendi |
| **Başarısız** | Ödeme işleme hataları |

### Ödeme Sağlayıcı Hesabı Ayrışımı

Ödeme sağlayıcılarına göre ödeme ayrışımını görün:

- **PayPal** — PayPal üzerinden işlenen ödemeler (toplam sayı ve tutar gösterir)
- **Airwallex** — Banka transferi ile işlenen ödemeler (toplam sayı ve tutar gösterir)

Bu ayrışım, size yardımcı olur:

- Sağlayıcı maliyetlerini izleme (PayPal ücretlerini Airwallex ücretleriyle karşılaştırın)
- Ödeme yöntemlerini dengелеme (ortaklara daha düşük maliyetli seçenekleri kullanmalarını teşvik edin)
- İşleme sorunlarını belirleme (bir sağlayıcıda yüksek başarısızlık oranı)

### Tarihî Ödeme Verileri

Tarihî ödeme geçmişini filtreleyin ve dışa aktarın:

- **Çeyrek raporları** — Çeyrek başına ortaklık programı maliyetlerini hesaplayın
- **Vergi belgeleri** — 1099 formları (ABD) veya eşdeğerleri için yıllık ödeme verilerini dışa aktarın
- **Ortaklık sorguları** — Ortakların soruları olduğunda ödeme tarihlerini ve tutarlarını hızlıca araştırın

## Analizleri Kullanarak Optimizasyon

Analiz verilerinizi kullanarak program performansını sürekli iyileştirin.

### En İyi Performanları Belirleyin

**Eylem:** Aylık olarak en iyi ortaklar tablosunu inceleyin ve:

- **Başarıyı ödüllendirin** — En iyi %10 ortakların komisyon oranlarını artırın
- **Taktikleri anlayın** — En iyi performans gösterenlerle iletişime geçin ve hangi tanıtım yöntemlerinin en iyi çalıştığını öğrenin
- **Başarıyı kopyalayın** — Diğer ortaklarla en iyi ortak stratejilerini paylaşın (izin verildiğinde)

**Örnek:"

```
En İyi Ortak: Marcus Lee (AFF-00456)
Gelir:       3 ayda $31.200
Yöntem:        YouTube ürün incelemeleri

Eylem:
1. Komisyonu 10%’den 12%’ye artırın
2. Marcus’a bir ortaklık durum analizi oluşturmasını isteyin
3. Marcus’ın başarı hikayesini kullanarak daha fazla YouTube etkili kişisini işe alın
```

### Düşük Performanslı Ortaklara Destek

**Eylem:** Komisyon sayısına göre filtreleyin ve 90 günde < 5 komisyon olanları belirleyin:

- **Kaynak sağlayın** — Tanıtım malzemeleri, ürün fotoğrafları, örnek metin gönderin
- **Eğitim sunun** — Etkili tanıtım taktiklerini gösteren bir webinara katılın
- **Konum ayarlayın** — Ortakın kitleleri bir programla uyuşmuyorsa, farklı bir programa geçmelerini önerin
- **Pasif ortakları kaldırın** — 6-12 ay boyunca etkinlik göstermeyenleri programdan kaldırın

### Program Karşılaştırması

**Eylem:** Programlara göre toplam komisyonları ve tıklama-çevrim oranlarını karşılaştırın:

| Program | Tıklamalar | Komisyonlar | Çevrim Oranı | Ortalama Komisyon |
|---------|--------|-------------|-----------------|----------------|
| Program A | 8.234 | 187 | 2,27% | $32,50 |
| Program B | 3.421 | 94 | 2,75% | $25,00 |

**Görüşler:"

- Program B, **daha yüksek çevrim oranı** sahibidir, daha az tıklamaya rağmen (daha iyi hedefleme)
- Program A, **daha yüksek komisyon değerleri** üretir (gelir açısından daha iyi)

**Optimizasyonlar:"

- Program B için komisyon oranını artırın, daha fazla ortak çekmek için (çevrimin kanıtlandığı)
- Program B’nin daha iyi çevrimini sağlayanları analiz edin ve Program A’ya uygulayın

### Mevsimsel Eğilimler

**Eylem:** Gelir grafiğini kullanarak mevsimsel eğilimleri belirleyin:

```
Ocak:  $5.200   → Tatil sonrası düşüş
Şubat: $4.800   → Devam eden düşük sezon
Mart:    $6.100   → Bahar artışı
Nisan:    $7.300   → Büyüme devam ediyor
Mayıs:      $6.800   → Stabilize ediliyor
```

**Kampanyaları planlayın:"

- **Q1 yavaşlama** — Şubat ayında "Bahar Satış" kampanyasını başlatın, Mart/Nisan gelirini artırın
- **Tatil hazırlığı** — Q4 tatil satışları için Eylül/Ocak ayında yeni ortaklar işe alın
- **Stok planlama** — Ortaklık tarafından yönetilen gelir sıçramalarından önce stok alın

## İpuçları

- **Merchant panosunu günlük olarak inceleyin** — Bekleyen başvuruları ve komisyonları birikmeden önce yakalayın — günlük 5 dakikalık bir kontrol, haftalık 2 saatlik bir takipten daha verimlidir
- **Gelir grafiğini kullanarak program değişikliklerini doğrulayın** — Komisyon oranlarını ayarladığınızda, değişiklikten önce ve sonra 30 gün karşılaştırın
- **Komisyon verilerini aylık olarak dışa aktarın** ve raporları muhasebe sisteminizde saklayın, vergi hazırlığı ve finansal tahminler için kolayca kullanın
- **En iyi 3 ortakınızı çeyrek olarak** iletişime geçin, ilişkileri koruyun ve program iyileştirmeleri hakkında geri bildirim alın
- **Gelir grafiğindeki sıçramaları izleyin** ve bunların nedenini araştırın — başarılı kampanyalar diğer ortaklarla veya gelecekteki mevsimlerde kopyalanabilir
- **Aylık bir inceleme rutini kurun:** 1. hafta = analizleri inceleyin, 2. hafta = en iyi performanları iletişime geçin, 3. hafta = düşük performanları destekleyin, 4. hafta = gelecek aylık kampanyaları planlayın
- **Her ortak için tıklama sayısını ve komisyon sayısını karşılaştırın** — 5.000 tıklama ancak sadece 10 komisyon olan bir ortak düşük kaliteli trafiği sürüyor olabilir

