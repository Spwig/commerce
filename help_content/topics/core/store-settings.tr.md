---
title: Mağaza Ayarlarını Yapılandırma
---

Mağaza Ayarları, mağazanızın kimliği, yerel ayarlar, markalaşma ve operasyonel tercihlerini yapılandırmak için merkezi bir yerdir. **Ayarlar > Mağaza Ayarları**'na giderek başlayın.

![Mağaza ayarları genel sekmesi](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Genel Sekme

**Genel** sekmesi, mağazanızın temel kimlik ayarlarını barındırır.

### Mağaza Kimliği

- **Mağaza Adı** — Sayfa başlıklarında, e-postalarda ve yönetici başlığında gösterilen görüntülenen ad.
- **Alt Başlık** — Mağazanızın kısa bir açıklaması, SEO ve sosyal paylaşım için kullanılır.
- **Site URL** — Mağazanızın kamuya açık web adresi. Bu, e-postalarda, harita oluşturmakta ve bağlantı oluşturma işlemlerinde kullanılır.

### İletişim Bilgileri

- **İletişim E-postası** — Sipariş bildirimlerini alır ve müşteri iletişimlerinde gösterilir.
- **Telefon Numarası** — Altyapı ve e-postalarda gösterilen isteğe bağlı destek telefon numarası.

### İş Adresi

Tam adresinizi girin (sokak, şehir, eyalet, posta kodu, ülke). Aşağıdakiler için kullanılır:
- Nakliye başlangıç hesaplamaları
- Vergi hesaplamaları
- Hukuki gereklilikler ve faturalar

## Markalaşma

### Logotype

Mağaza logonuzu yükleyin (PNG veya SVG önerilir, şeffaf arka planla ~200x50px). Logotype aşağıdaki yerlerde görünür:
- Mağaza ön yüzü başlığı
- E-posta şablonları
- Yönetici paneli

### Favicon

Kare bir favicon yükleyin (ICO veya PNG, 32x32px). Aşağıdaki yerlerde görünür:
- Tarayıcı sekmesi ikonu
- Yıldız işaret ikonu
- Mobil ana ekran ikonu

## Yerel Ayarlar

### Varsayılan Dil

Mağazanızın ana dilini 10 desteklenen seçenekten seçin:

| Dil | Kod |
|----------|------|
| İngilizce | en |
| İspanyolca | es |
| Fransızca | fr |
| Almanca | de |
| Portekizce | pt |
| Japonca | ja |
| Basit Çince | zh-hans |
| Geleneksel Çince | zh-hant |
| Rusça | ru |
| Arapça | ar |

Varsayılan dil, yönetici arayüz dilini ve mağaza ön yüzü içeriği için geri dönüşü kontrol eder.

### Saat Dilimi

Mağazanızın saat dilimini seçin, böylece sipariş zaman damgaları, planlanan kampanyalar ve raporlama doğru olur.

### Para Birimi

- **Varsayılan Para Birimi** — Fiyatlandırma ve muhasebe için ana para birimi.
- **Çoklu Para Birimi** — Etkinleştirin, böylece müşteriler kendi tercih ettikleri para biriminde fiyatları görür ve gerçek zamanlı döviz kurları kullanarak otomatik dönüşüm yapılır.

**Ayarlar > Mağaza Ayarları > Para Birimi** içinde ek para birimlerini yapılandırın.

## E-Ticaret Ayarları

### Ziyaretçi Siparişleri

Hesap oluşturmadan satın almayı sağlayın:
- Daha hızlı ödeme akışı
- İlk kez satın alanlar için daha az sürtünme
- Daha az müşteri verisi toplar

### Sipariş Numarası Biçimi

Sipariş numaralarının nasıl görüneceğini özelleştirin:
- **Önek** — Örneğin, "ORD-"
- **Başlangıç Numarası** — İlk sipariş numarası
- **Doldurma** — Örneğin, 00001

### Stok Varsayılanları

- **Stok Takibi** — Genel olarak stok takibini etkinleştirin
- **Düşük Stok Seviyesi** — Uyarı seviyesi (varsayılan: 5 birim)
- **Stok Yoksa Geri Siparişleri Kabul Et** — Stokta ürün kalmadığında siparişleri kabul et

## E-posta Ayarları

### Gönderen Bilgisi

- **Gönderen Adı** — E-posta gönderen olarak görünür (genellikle mağaza adınız)
- **Gönderen E-postası** — Doğrulanmış bir domainden olmalıdır
- **Yanıt E-postası** — Müşterilerin yanıtlandığı yer

### E-posta Sağlayıcısı

**Ayarlar > E-posta Yapılandırması** içinde e-posta teslim hizmetinizi yapılandırın. Desteklenen sağlayıcılar arasında SMTP, SendGrid, Mailgun ve Amazon SES yer alır.

## Hukuki & Uygunluk

Yasal gereklilikleri karşılamak için mağaza politikalarınızı ekleyin:

- **Şartlar ve Koşullar** — Ödeme için gereklidir; müşteriler satın almadan önce onaylamalıdır
- **Gizlilik Politikası** — GDPR/CCPA uygunluğu; alt bölüme bağlantılıdır
- **İade Politikası** — İade penceresini, koşulları ve iade sürecini tanımlayın

## Bakım Modu

Mağazayı geçici olarak çevrimdışı yapmak için bakım modunu etkinleştirin:
- Ziyaretçilere özel bir bakım mesajı gösterir
- Sadece yönetici kullanıcılarına erişimi kısıtlar
- Büyük güncellemeler veya geçişler sırasında yararlıdır

## Vergi Ayarları

**Ayarlar > Vergi Ayarları** içinde vergi toplamayı yapılandırın:

1. **Hesaplama Yöntemi** — Nakliye adresine göre, fatura adresine göre veya mağaza konumuna göre
2. **Vergi Oranları** — Bölgesel olarak ve ürün vergi sınıfına göre oranları tanımlayın
3. **Vergi Gösterimi** — Vergiyle birlikte, vergisiz veya her ikisini de göster

## İpuçları

- Herhangi bir sipariş işlemeden önce saat dilimini doğru ayarlayın — tüm zaman damgaları ve raporları etkiler.
- Ziyaretçi siparişlerini etkinleştirerek dönüşüm oranlarını artırın.
- Nakliye ve vergi hesaplamaları için iş adresinizi doldurun.
- Profesyonel ve markalaşmış bir deneyim için hem logotype hem de favicon yükleyin.
- Yerel düzenlemelere uyum sağlamak için hukuki sayfalarınızı düzenli olarak gözden geçirin.

## Sorun Giderme

**Mağaza ön yüzünde değişiklikler görünmüyor:**
- Tarayıcı önbelleğini temizleyin
- Yönetici panelinden önbelleği temizleyin
- Bakım modunun yanlışlıkla etkinleştirildiğini kontrol edin

**E-postalar gönderilmemiş:**
- E-posta sağlayıcısı ayarlarını E-posta Yapılandırması bölümünden doğrulayın
- "Gönderen E-postası" domaininin doğrulandığını kontrol edin
- Sağlayıcı kurulum sayfasından bağlantıyı test edin

**Para birimi dönüşümü çalışmıyor:**
- Döviz kuru sağlayıcınının bağlı olduğundan emin olun
- Döviz kuru ayarlarında API kimlik bilgilerini kontrol edin
- Manuel olarak kuruları güncellemeyi deneyin

