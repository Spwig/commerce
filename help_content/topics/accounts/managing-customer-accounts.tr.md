---
title: Müşteri Hesaplarını Yönetme
---

Müşteri hesapları, satıcıların müşteri bilgilerini, sipariş geçmişini ve tercihlerini izlemesini sağlar. Yönetmek için admin yan çubuğunda **Müşteriler > Tüm Müşteriler** bölümüne gidin.

![Müşteri Ekle](/static/core/admin/img/help/managing-customer-accounts/add-customer.webp)

## Müşteri Hesapları ve Müşteri Profillerini Anlamak

**Müşteri Hesapları**, Kullanıcı modelinde saklanan oturum açma kimlik bilgileri (e-posta/şifre) anlamına gelir. **Müşteri Profilleri**, telefon numarası, doğum tarihi, tercihler ve analizler gibi ek müşteri bilgilerini saklar. Her müşteri hesabı, bu genişletilmiş veriyi saklayan bir profil ile ilişkilidir.

Admin panelinde müşterileri yönetirken, arka planda kullanıcı hesaplarına bağlanan Müşteri Profilleri ile çalışıyorsunuz.

## Tüm Müşterileri Görüntüleme

Müşteri listesi, anahtar metriklerle birlikte kayıtlı tüm müşterileri gösterir:

| Sütun | Açıklama |
|--------|-------------|
| **Kullanıcı** | Müşteri adı ve e-posta adresi |
| **Ortaklık Durumu** | Müşterinin aynı zamanda bir ortaklık ortağı olup olmadığı |
| **Müşteri Değeri** | Müşterinin harcadığı toplam tutar (renk kodlu) |
| **Müşteri Segmenti** | RFM segmenti (Şampiyon, Loyal, Riskli, vb.) |
| **Toplam Siparişler** | Tamamlanan sipariş sayısı |
| **Son Siparişden Gün Sayısı** | Son satın alma tarihi |
| **VIP Müşteri** | Müşteri VIP olarak işaretlenmişse bir badge |

### Müşterileri Filtreleme

Filtre yan çubuğunu kullanarak listeyi daraltın:

- **Ortaklık Durumu** — Ortak, Ortak Değil, Ortak Bekleme, Aktif, Askıda, Reddedildi
- **Dashboard Düzeni** — Müşterinin tercih ettiği dashboard düzeni
- **Bülten Aboneliği** — Müşterinin bültenlere abone olup olmadığı
- **Pazarlama E-postaları** — Müşterinin pazarlama e-postalarına abone olup olmadığı
- **Oluşturulma Tarihi** — Kayıt tarihine göre filtrele

### Müşteri Arama

Arama çubuğunu kullanarak müşterileri şu kriterlerle bulun:

- Kullanıcı adı
- E-posta adresi
- İsim
- Soyisim
- Telefon numarası

## Müşteri Detaylarını Görüntüleme

Bir müşterinin adını tıklayarak tam profilini görüntüleyin. Müşteri detay sayfası aşağıdaki bilgileri gösterir:

![Müşteri Detayı](/static/core/admin/img/help/managing-customer-accounts/customer-detail.webp)

### Müşteri Bilgisi Bölümü

Temel iletişim detayları ve hesap durumu:
- **Kullanıcı** — Arka planda saklanan Kullanıcı hesabına bağlantı
- **Telefon** — Müşterinin telefon numarası
- **Doğum Tarihi** — Yaş doğrulama ve doğum günleri kampanyaları için

### Dashboard Tercihleri

Müşterinin hesap dashboard'ını nasıl özelleştirdiğini gösterir:
- **Dashboard Düzeni** — Ağaç, liste veya sıkışık görünüm
- **Sipariş Geçmişi Göster** — Dashboard'da sipariş geçmişi görünür mü
- **İstek Listesi Göster** — Dashboard'da istek listesi görünür mü
- **Son Görülen Ürünler Göster** — Son görüntülenen ürünler görünür mü
- **Öneriler Göster** — Ürün önerileri görünür mü

### İletişim Tercihleri

Müşterinin çeşitli iletişimler için aboneliği durumu:
- **Bülten Aboneliği** — Genel bültenlere abone olundu
- **Pazarlama E-postaları** — Pazarlama e-postalarına abone olundu
- **Sipariş Bildirimleri** — Sipariş durumu güncellemeleri için abone olundu

### Müşteri Analitiği

Müşteri davranışları ve değerleri için salt okunur özeti:
- **Müşteri Analitiği Özeti** — RFM puanları, segmenti, ömür değeri
- **Satın Alma Davranışı Özeti** — Sipariş sıklığı, ortalama sipariş değeri, tercih edilen kategoriler
- **Etkileşim Özeti** — Son oturum, e-posta açma oranları, site etkinliği

Bu analitik alanları otomatik olarak hesaplanır ve el ile düzenlenemez. Ayrıntılar için [Müşteri Analitiği'ni Anlamak](customer-analytics.md) bölümüne bakın.

## Müşteri Hesabı Oluşturma

Satıcılar, telefon siparişleri, mağaza toplama işlemleri veya toptan müşteri kaydı için manuel olarak müşteri hesapları oluşturabilir.

1. Üst sağ köşedeki **+ Müşteri Profili Ekle**'ye tıklayın
2. Gerekli ve isteğe bağlı alanları doldurun:

| Alan | Gerekli | Açıklama |
|-------|----------|-------------|
| **Kullanıcı** | Evet | Mevcut bir Kullanıcı hesabı seçin veya yeni bir tane oluşturun |
| **Telefon** | Hayır | Müşterinin telefon numarası |
| **Doğum Tarihi** | Hayır | Yaş doğrulama ve doğum günleri kampanyaları için |
| **Bülten Aboneliği** | Hayır | Müşteriyi bültenlere abone edin |
| **Pazarlama E-postaları** | Hayır | Müşteriyi pazarlama e-postalarına abone edin |

### Profil Ekleme Esnasında Yeni Kullanıcı Oluşturma

Müşteri henüz bir Kullanıcı hesabı oluşturmadıysa:
1. Kullanıcı alanının yanındaki **+** simgesine tıklayın
2. Müşterinin **e-posta adresini** girin (bu, kullanıcı adı olur)
3. İsteğe bağlı olarak **ad** ve **soyad** girin
4. İsteğe bağlı olarak bir **şifre** ayarlayın
5. Şifre ayarlamadıysanız, **Şifre sıfırlama e-postası gönder** kutusunu işaretleyin
6. Kullanıcı hesabını kaydedin
7. Müşteri Profili alanlarını tamamlayın
8. **Kaydet**'e tıklayın

## Hoş geldiniz E-postaları

Müşteri hesabı oluşturduktan sonra:
- Eğer bir şifre ayarladıysanız, müşteri hemen bu şifreyle oturum açabilir
- Eğer bir şifre ayarlamadıysanız, sistem müşteriye bir şifre sıfırlama e-postası gönderir, müşteri kendi şifresini ayarlayabilir
- Müşteri ile iletişime geçmek için **Pazarlama > E-posta Kampanyaları** üzerinden manuel bir hoş geldiniz e-postası tetikleyebilirsiniz

## Müşteri Bilgilerini Düzenleme

Müşteri bilgilerini güncellemek için:
1. **Müşteriler > Tüm Müşteriler** bölümüne gidin
2. Müşterinin adını tıklayın
3. Güncellemek istediğiniz alanları düzenleyin
4. **Kaydet**'e tıklayın

### Düzenlenebilecek Alanlar

**İletişim Bilgileri:**
- Ad (Kullanıcı hesabı üzerinden)
- E-posta adresi (Kullanıcı hesabı üzerinden)
- Telefon numarası
- Doğum tarihi

**Tercihler:**
- Bülten aboneliği durumu
- Pazarlama e-postası aboneliği
- Sipariş bildirim tercihleri
- Dashboard düzeni ve görünürlük ayarları

### Düzenlenemeyen Alanlar

Bu alanlar, müşteri davranışlarına göre otomatik olarak hesaplanır:
- Toplam harcama / Müşteri değeri
- Sipariş sayısı
- Müşteri segmenti (Şampiyon, Loyal, Riskli, vb.)
- RFM puanları
- Ömür değeri tahminleri
- Son sipariş tarihi
- Analitik özeti

Bu alanlar yanlış görünürse, temel sipariş verilerini kontrol edin veya **Müşteriler > Analitik** → **Ölçüleri Yeniden Hesapla**'dan manuel bir yeniden hesaplama tetikleyin.

## Müşteri Notları

Müşteri hakkında iç notlar ekleyerek destek sorunlarını, VIP taleplerini veya takip görevlerini izleyebilirsiniz.

### Not Ekleme

1. Müşterinin profilini açın
2. **Müşteri Notları** bölümüne kaydırın (ayrı bir sekme olabilir)
3. **+ Not Ekle**'ye tıklayın
4. Not detaylarını doldurun:

| Alan | Açıklama |
|-------|-------------|
| **Not Türü** | Genel, Destek Sorunu, Şikayet, Yorum, VIP Hizmeti, Takip Gerekiyor, Ödeme Sorunu, Teslimat Sorunu |
| **Başlık** | Notun kısa özeti |
| **İçerik** | Ayrıntılı not içeriği |
| **Takip Gerekiyor** | Bu görevin bir eyleme ihtiyaç duyup duymadığını işaretleyin |
| **Takip Tarihi** | Takip edilecek tarih |
| **Tamamlandı** | Takip tamamlandıysa işaretleyin |

### Not Türleri

| Tür | Kullanım Durumu |
|------|----------|
| **Genel Not** | Müşteri hakkında herhangi bir genel gözlem |
| **Destek Sorunu** | Destek bileti veya sorunun bir kaydı |
| **Şikayet** | Müşteri şikayetini izleme ve çözme için |
| **Yorum** | Müşteri hakkında pozitif geri bildirim veya sizin hakkınızda |
| **VIP Hizmeti** | VIP müşteriler için özel işlem talepleri |
| **Takip Gerekiyor** | Belirli bir tarihe kadar eyleme ihtiyaç duyulan görevler |
| **Ödeme Sorunu** | Ödeme sorunları veya anlaşmazlıklar hakkında notlar |
| **Teslimat Sorunu** | Teslimat sorunları veya özel teslimat talepleri hakkında notlar |

### Not Tarihi Görüntüleme

Tüm notlar, müşteri profilinde kronolojik sırayla görünür. Her not aşağıdaki bilgileri gösterir:
- Oluşturulma tarihi ve saati
- Oluşturan (personel adı)
- Not türü badge
- Başlık ve içerik
- Gerekirse takip durumu

### İç Notlar ve Müşteri Görünür Notları

Tüm müşteri notları, **iç kullanıma özel** olarak varsayılan olarak ayarlanmıştır — müşteriler bu notları asla göremez. Bu, satıcı ekipleri arasında iletişim için kullanılır.

Müşteri ile iletişim kurmanız gerekiyorsa, **Pazarlama > E-posta Kampanyaları** üzerinden e-posta sistemi kullanın veya ilgili sipariş üzerine bir sipariş yorumu ekleyin.

## Ziyaretçi Müşteriyi Kayıtlı Müşteriye Dönüştürme

Ziyaretçi müşteriler, bir müşteri hesabı oluşturmadan ödeme tamamladığında otomatik olarak oluşturulur. Kullanıcı adı `guest_10374` gibi bir desen izler, burada sayı bir benzersiz kimliktir.

Ziyaretçiyi kayıtlı müşteriye dönüştürmek için:
1. **Müşteriler > Tüm Müşteriler** bölümüne gidin
2. Müşterinin sipariş e-postasına göre ziyaretçiyi arayın
3. Ziyaretçi müşteri profilini tıklayın
4. **Kullanıcı** bağlantısına tıklayarak arka plandaki Kullanıcı hesabını düzenleyin
5. **Kullanıcı adını** `guest_10374`'den müşterinin gerçek e-posta adresine değiştirin
6. **E-posta** adresini eşle
7. İsteğe bağlı olarak **ad** ve **soyad** ekleyin
8. Müşterinin bir şifre ayarlayabileceği şekilde **Şifre sıfırlama e-postası gönder** kutusunu işaretleyin
9. **Kaydet**'e tıklayın

Müşteri artık e-posta adresiyle oturum açabilir ve geçmiş ziyaretçi siparişlerini sipariş geçmişinde görebilir.

### Neden Ziyaretçileri Kayıtlı Müşterilere Dönüştürmek?

- Ziyaretçi siparişleri müşteri analitiği veya segmentlerine katılmaz
- Ziyaretçiler siparişleri izleyemez ve sipariş geçmişine erişemez
- Ziyaretçileri kayıtlı müşteriye dönüştürmek, kayıtlı müşteri sayısını artırır ve analitik doğruluğunu iyileştirir
- Kayıtlı müşteriler, tekrar satın alma olasılığı daha yüksektir

## Hesap Devre Dışı Bırakma vs Silme

### Müşteri Hesabını Devre Dışı Bırakma

Devre dışı bırakma, oturum açmayı engellerken tüm veriyi korur:

1. Müşterinin profilini açın
2. **Kullanıcı** bağlantısına tıklayarak Kullanıcı hesabını düzenleyin
3. **"Aktif"** kutusunu kaldırın
4. **Kaydet**'e tıklayın

**Ne olur:**
- Müşteri oturum açamaz
- Sipariş geçmişi korunur
- Müşteri daha sonra tekrar aktif hale getirilebilir
- Analitik ve metrikler korunur

**Devre dışı bırakmayı kullanın:**
- Ödeme anlaşmazlıkları nedeniyle geçici olarak hesapları devre dışı bırakmak için
- Abusif müşterileri engellemek için
- Müşteri, erişimi durdurmak istedi ancak verileri silmemek için

### Müşteri Hesabını Silme

Silme, hesabı kaldırır ve sipariş geçmişini orphant bırakabilir:

1. Müşterinin profilini açın
2. Aşağı kaydırın ve **Sil**'e tıklayın
3. Silmeyi onaylayın

**Ne olur:**
- Müşteri hesabı kalıcı olarak kaldırılır
- Müşteri profili silinir
- Sipariş geçmişinde orphant olabilir (siparişler var ancak müşteriye bağlanmamış)
- Geri alınamaz

**Silme için kullanın:**
- GDPR/CCPA veri silme talepleri (önce veriyi dışa aktarın)
- Asla olmaması gereken test hesapları için
- Yanlışlıkla oluşturulan yinelenen hesaplar için

## GDPR Uygunluğu

Bir GDPR talebi nedeniyle müşteri hesabı silmeden önce:

1. **Müşteriler > Tüm Müşteriler** bölümüne gidin
2. Müşteriyi seçin
3. **Veri İhracatı** eylemini kullanarak tam veri ihracatı oluşturun
4. Müşteri istiyorsa ihracatı müşteriye gönderin
5. Daha sonra silme işlemini gerçekleştirin

İhracat, müşteri profilini, sipariş geçmişini, adresleri, notları ve analitik verileri içerir.

## İpuçları

- **Yüksek değerli müşterileri tanımlamak için filtreleri kullanın** — Müşteri Değeri'ne göre filtreleyerek Şampiyon ve VIP'leri bulun
- **Müşteri notlarını düzenli olarak gözden geçirin** — En az haftada bir kez açık takip görevlerini kontrol edin
- **Analitikleri el ile düzenlemeyin** — RFM puanlarını ve segmentlerini sistemin otomatik olarak hesaplamasını sağlayın
- **Ziyaretçileri proaktif olarak dönüştürün** — Ziyaretçi ikinci bir satın alma yaptıktan sonra ulaşın ve uygun bir hesap oluşturmayı teklif edin
- **Silme yerine devre dışı bırakmayı kullanın** — Devre dışı bırakma, veriyi korur ve gerekirse geri döndürülebilir
- **Destek görüşmeleri sırasında notlar ekleyin** — Diğer ekip üyeleri için bağlam sağlayarak destek etkileşimlerini belgeleyin
- **Takip tarihlerini ayarlayın** — Notlardaki takip görevi sisteminin kullanarak hiçbir şeyin kaçırılmamasını sağlayın
- **İletişim tercihlerine saygı duyun** — Pazarlama e-postalarını istemeyen müşterilere asla göndermeyin

