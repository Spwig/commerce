---
title: Komisyon Yönetimi
---

Komisyon yönetimi, yalnızca geçerli satışların kredilendirilmesini sağlamak amacıyla ortak kazançlarını inceleyip onaylamak için yapılan işlemdir. Bu kılavuz, bekleyen komisyonları incelemenizi, geçerli olanları onaylamayı, dolandırıcı veya iade edilen siparişleri reddetmeyi ve toplu eylemler kullanarak komisyonları verimli şekilde yönetmeyi öğreneceksiniz.

## Komisyon Panosu

**Pazarlama > Komisyonlar** menüsüne giderek komisyon yönetimi panosuna erişin.

Panoda, tüm ortak programlar üzerinden komisyon etkinliği genel bir bakış sunar:

| İstatistik | Açıklama |
|-----------|-------------|
| **Bekleyen Komisyonlar** | Onayınızı bekleyen komisyon sayısı |
| **Onaylanan Komisyonlar** | Ödeme için hazır olan onaylanan komisyonlar |
| **Ödenen Komisyonlar** | Ortaklara ödendiği komisyonlar |
| **Reddedilen Komisyonlar** | Dolandırıcılık, iadeler veya politika ihlalleri nedeniyle reddedilen komisyonlar |
| **Ödenmemiş Komisyon Toplamı** | Onaylanan ancak henüz ödenmeyen komisyonların toplam değeri |

Bu istatistikler, ortak programınızın finansal etkisini izlemenize ve inceleme iş yükünüzü izlemenize yardımcı olur.

![Komisyon Panosu](/static/core/admin/img/help/commission-management/commission-dashboard.webp)

## Komisyonları Görüntüleme

Komisyon listesi, tüm komisyon kayıtlarını kronolojik sırayla görüntüler.

### Liste Sütunları

| Sütun | Açıklama |
|--------|-------------|
| **Ortak** | Ortakın adı ve benzersiz kodu |
| **Program** | Bu komisyonu oluşturan ortak program |
| **Sipariş** | Sipariş numarası (tam sipariş detaylarını görmek için tıklayın) |
| **Tutar** | Mağazanızın para birimindeki komisyon değeri |
| **Durum** | Bekleyen, Onaylanan, Reddedilen veya Ödenen |
| **Oluşturulma Tarihi** | Komisyonun oluşturulduğu zaman |

### Komisyonları Filtreleme

Filtreleme menüsü kullanarak komisyonları daraltabilirsiniz:

- **Duruma Göre** — Sadece bekleyen, onaylanan, reddedilen veya ödenen komisyonları göster
- **Ortaklara Göre** — Belirli bir ortak için komisyonları görüntüleyin
- **Programlara Göre** — Belirli bir ortak programdan gelen komisyonları görün
- **Tarih Aralığına Göre** — Oluşturma tarihine göre filtreleyin

### Komisyonları Arama

Arama çubuğunu kullanarak belirli komisyonları bulun:

- **Bir sipariş numarası** girerek belirli bir satış için komisyonu bulun
- **Bir ortak kodu** girerek bir ortak için tüm komisyonları görün

## Komisyon Detayları

Listedeki herhangi bir komisyonu tıklayarak tam detaylarını görüntüleyebilirsiniz.

### Detay Alanları

Detay görünümü şunları gösterir:

- **Sipariş Bilgisi** — Sipariş numarasını tıklayarak yeni bir sekmede tam siparişi görüntüleyin, ürünleri, kargo adresini, ödeme durumunu ve müşteri detaylarını içerir
- **Ortak Bilgisi** — Ortakın adı, kodu, ödeme e-postası ve program üyelik durumu
- **Program Detayları** — Program adı, komisyon türü (oran veya sabit) ve komisyon oranı
- **Zaman damgaları** — Oluşturulma tarihi, onay/red tarihi ve ödeme tarihi
- **Notlar Bölümü** — Sadece satıcılar tarafından görünen iç notlar (aşağıda açıklanmıştır)

Bu bilgiler, komisyonu onaylamadan önce geçerliliğini doğrulamaya yardımcı olur.

## Komisyonları Onaylama

Bir komisyonu onaylamak, onun geçerli olduğunu doğrular ve ortakın kullanıma hazır bakiyesine ekler, bu da ödeme için elverişli hale gelir.

### Ne Zaman Onaylamalısınız

Komisyonları şu durumlarda onaylayın:

- **Sipariş başarıyla tamamlandı** — Ürün gönderildi veya dijital ürün teslim edildi
- **İade veya iade talebi yok** — Müşteri bir iade talep etmedi (teslimat sonrası 14-30 gün beklemeyi göz önünde bulundurun)
- **Kalite standartları karşılandı** — Satış, programınızın koşullarını karşılar (örneğin, kendini referans verme, müşteri gerçek ödeme yöntemi kullandı)
- **Dolandırıcılık tespit edilmedi** — Sipariş dolandırıcılık ekranını geçer (IP, fatura/kargo adresi uyuşmazlığı, anormal sipariş desenleri kontrol edin)

### Nasıl Onaylamalısınız

**Tek Komisyon Onayı:**

1. **Pazarlama > Komisyonlar** menüsüne gidin
2. Onaylamak istediğiniz komisyonu tıklayın
3. Detay sayfasının üst kısmındaki **Onayla** butonuna tıklayın
4. Seçenek olarak bir not ekleyin (örneğin, "Teslimat sonrası onaylandı")
5. Durum **Onaylandı** olarak değişir ve komisyon ortakın bakiyesine eklenir

**Toplu Onaylama:**

1. **Pazarlama > Komisyonlar** menüsüne gidin
2. Onaylamak istediğiniz komisyonların yanındaki kutuları işaretleyin
3. **Eylemler** açılır menüsünden **Seçilenleri Onayla**'yı seçin
4. **Git**'e tıklayın
5. Tüm seçilen komisyonların durumu **Onaylandı** olarak değişir

Onaylanan komisyonlar, ortakın panosunda kullanıma hazır bakiye olarak görünür ve bir sonraki ödeme partisiyle birlikte dahil edilebilir.

## Komisyonları Reddetme

Bir komisyonu reddetmek, onu ortakın bakiyesinden kaldırır ve ödeme için elverişli olmayan olarak işaretler.

### Ne Zaman Reddetmelisiniz

Komisyonları şu durumlarda reddetmelisiniz:

- **Dolandırıcı sipariş** — Sipariş dolandırıcılık belirtileri gösteriyor (hırsızca ödeme yöntemi, IP uyuşmazlığı, ortak kendi bağlantısını kullanıyor)
- **Müşteri ürün iade etti** — Müşteri tam iade talep etti
- **Kalite sorunları** — Satış program koşullarını karşılamıyor (örneğin, ortak reklam kılavuzlarını ihlal etti)
- **Koşullar ihlali** — Ortak yasaklanmış promosyon yöntemlerini kullandı (spamlama, tescil yarışmaları, çerez doldurma)
- **Sipariş iptal edildi** — Müşteri teslimat öncesi iptal etti

### Nasıl Reddetmelisiniz

**Tek Komisyon Reddetme:**

1. **Pazarlama > Komisyonlar** menüsüne gidin
2. Reddetmek istediğiniz komisyonu tıklayın
3. Detay sayfasının üst kısmındaki **Reddet** butonuna tıklayın
4. **Bir not ekleyin** ve nedeni açıklayın (dispute çözümü için önerilir)
5. Durum **Reddedildi** olarak değişir

**Toplu Reddetme:**

1. **Pazarlama > Komisyonlar** menüsüne gidin
2. Reddetmek istediğiniz komisyonların yanındaki kutuları işaretleyin
3. **Eylemler** açılır menüsünden **Seçilenleri Reddet**'i seçin
4. **Git**'e tıklayın
5. Tüm seçilen komisyonların durumu **Reddedildi** olarak değişir

Reddedilen komisyonlar, ortakın bakiyesinden kaldırılır ve ödenemez. Kayıt amaçlı olarak komisyon geçmişinde görünürler.

## Toplu Eylemler

Toplu eylemler, büyük partileri işlemek için birden fazla komisyonu aynı anda onaylamaya veya reddetmeye olanak tanır.

### Toplu Eylemleri Kullanma

1. **Pazarlama > Komisyonlar** menüsüne gidin
2. İşlemek istediğiniz komisyonları gösteren listeyi filtreleyin (örneğin, durum **Bekleyen**'e göre filtreleyin)
3. Her komisyonun yanındaki kutuyu işaretleyin, veya sayfadaki tüm komisyonları seçmek için başlık kutusunu işaretleyin
4. **Eylemler** açılır menüsünden bir eylem seçin:
   - **Seçilenleri Onayla** — Tüm seçilen komisyonları onayla
   - **Seçilenleri Reddet** — Tüm seçilen komisyonları reddet
5. **Git**'e tıklayın
6. Güncellenen komisyon sayısı gösteren onay mesajını inceleyin

### Verimli Toplu İşleme

- **Programla filtrele** — Güvenilir ve yüksek performanslı bir ortakın tüm komisyonlarını tek seferde onaylayın
- **Tarih aralığına göre filtrele** — 14 gün önceki komisyonları işlemek için (iade pencerenizden çıktı)
- **Yüksek değerli komisyonları ayrı ayrı inceleyin** — Küçük komisyonlar için toplu eylemleri kullanın, büyükleri manuel olarak inceleyin

## Komisyon Notları

Not alanı, kararlarınızı belgelemek ve ekibinizle iletişim kurmak için kullanılır.

### Not Ekleme

Notlar şu şekilde eklenebilir:

- **Onaylama sırasında** — Komisyonu tıklayın, Not alanı içine bir not ekleyin, sonra **Onayla**'yı tıklayın
- **Reddetme sırasında** — Reddetme nedenini açıklayan bir not ekleyin
- **Herhangi bir zaman** — Komisyonu tıklayın, Not alanı içine not ekleyin veya düzenleyin ve kaydedin

### Ne Zaman Not Kullanmalısınız

- **Reddedilen komisyonlar** — Her zaman nedeni belgeleyin ("Müşteri 2/10/26 tarihinde #12345 siparişini iade etti")
- **Yüksek değerli komisyonlar** — Doğrulama adımlarını not edin ("Teslimat, takip numarası ABC123 ile doğrulandı")
- **Dispute edilen komisyonlar** — Ortakla iletişim kurulumu belgeleyin
- **Dolandırıcılık desenleri** — Gelecekte referans olarak şüpheli aktiviteyi not edin

Notlar **yalnızca iç**dir — ortaklar bunları göremez. Kayıt amaçlı bir araçtır.

## Komisyon Akışı

Tamamı komisyon yönetimi iş akışı aşağıdadır:

```
Sipariş Verildi → Komisyon Oluşturuldu (Bekleyen)
                      ↓
              Satıcı İnceleme
                      ↓
                ┌─────┴─────┐
                ↓           ↓
            Onaylandı     Reddedildi
                ↓           ↓
        Ödeme Hazırı  Ödenemez
                ↓
        Ödeme İçerisinde
                ↓
              Ödenmiş
```

**Zaman Çizelgesi Örneği:**

- **Gün 1:** Müşteri, ortak bağlantısı üzerinden $100 sipariş verir → $10 komisyonu oluşturulur (Bekleyen)
- **Gün 15:** Sipariş tamamlanır ve iade penceresi geçildi → Satıcı komisyonu onaylar
- **Gün 20:** Satıcı aylık ödeme partisini işler → Komisyon durumu Ödenmiş olarak değişir
- **Gün 21:** Ortak PayPal üzerinden ödeme alır

## En İyi Uygulamalar

### İnceleme Penceresi

Konsistanslı bir inceleme zamanlaması kurun:

- **Günlük incelemeler** — Bekleyen komisyonları her sabah işleyin (yüksek hacimli programlar için önerilir)
- **Haftalık incelemeler** — Her Pazartesi günü, önceki haftanın komisyonlarını onaylamak için zaman ayırın
- **İki haftalık incelemeler** — Ödeme zamanlamasıyla hizalayın (ortalarında komisyonları onaylayın, ay sonunda ödemeleri işleyin)

### Kalite Kontrol Kontrolleri

Komisyonları onaylamadan önce doğrulayın:

1. **Sipariş tamamlandı** — Yönetici panelinde sipariş durumunu kontrol edin
2. **Ödeme onaylandı** — Ödeme yönteminin başarıyla işlendiğini doğrulayın
3. **İade penceresi geçildi** — Teslimat sonrası 14-30 gün bekleyin, iadeleri hesaba katın
4. **Dolandırıcılık bayrakları yok** — Siparişte şüpheli desenleri inceleyin (adres uyuşmazlığı, yüksek riskli ülkeler, aynı IP üzerinden aynı affiliate bağlantısıyla birden fazla sipariş)
5. **Ortak iyi durumda** — Ortakın geçmişini kontrol edin, önceki dolandırıcılık veya ihlalleri için

### Dolandırıcılık Önleme

Aşağıdaki kırmızı bayrakları izleyin:

- **Kendi referansları** — Ortak, kendi takip bağlantısını kullanarak siparişler veriyor
- **Çerez doldurma** — Anormal yüksek tıklama-çevrim oranı ve düşük sipariş değerleri
- **Çift siparişler** — Aynı müşteri/IP üzerinden aynı affiliate bağlantısıyla birden fazla sipariş
- **Coğrafi konum uyuşmazlığı** — Ortak A Ülkesi'nde, ancak B Ülkesi'nde satışlar yapıyor
- **İade ücretleri** — Ortak bağlantısı üzerinden verilen siparişlerde yüksek iade oranı

Dolandırıcılık tespit edilirse, **komisyonları reddederek** ve ortak program üyeliğini sonlandırarak önlem alın.

### Ortaklarla İletişim

- **Beklentileri belirleyin** — Program koşullarında komisyon onayı politikasını açıkça belgeleyin
- **Açıklık sağlayın** — Komisyonları reddediyorsanız, ortaklara nedeni açıklayan bir e-posta gönderin (notları referans olarak kullanın)
- **Dispute'leri yanıtlayın** — Ortak bir reddi sorguluyorsa, notları ve sipariş detaylarını inceleyin
- **Kılavuzları yayınlayın** — Ortak portalınızda "Komisyon Onayı Politikası" sayfası oluşturun, karışıklığı önlemek için

## İpuçları

- **İade penceresi kapanmadan sonra** komisyonları onaylayın (genellikle 14-30 gün) ve müşterilerin daha sonra iade etmesi durumunda komisyonları onaylamaktan kaçının
- **Filtreleme ile toplu eylemleri** kullanarak güvenilir ortaklardan gelen komisyonları verimli şekilde işleyin, yeni veya yüksek riskli ortakları manuel olarak inceleyin
- **Reddettiklerinizi not alanına** belgeleyin — bu, bir ortak kararını tartışmaya başlarsa size koruma sağlar ve desenleri tanımlamaya yardımcı olur
- **Kendi referansları** izleyin — ortaklar kendi bağlantılarını kullanarak kişisel alımlar için komisyon kazanmak isteyenlerin yaygın ihlali
- **Minimum onay eşik değeri** ayarlayın — örneğin, $10'dan düşük komisyonları otomatik olarak onaylayın, ancak $50'den yüksek olanları manuel olarak inceleyin, verimlilik ile riski dengeler
- **Dolandırıcılık kontrol listesi** oluşturun — inceleme sürecinizi standartlaştırmak için kırmızı bayrakların listesini kullanın (IP uyuşmazlığı, şüpheli sipariş desenleri, yüksek riskli ödeme yöntemleri)
- **Ortaklara göre reddetme oranlarını** izleyin — bir ortakta birçok reddetme varsa, dolandırıcılık veya program koşulları üzerine ekstra eğitim ihtiyacı olabilir

