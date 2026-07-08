---
title: Ödeme Terminali Sağlayıcıları
---

Ödeme terminali sağlayıcıları, POS terminalinizde kredi ve banka kartı kabulünü sağlar. Stripe Terminal, modern kart okuyucuları (S700, WisePOS E, P400), rekabetçi işlem ücretleri ve sorunsuz entegrasyon sunan başlıca desteklenen sağlayıcıdır. API kimlik doğrulama bilgileriyle sağlayıcı hesaplarını yapılandırın, gerçek zamanlı bağlantı durumunu izleyin ve farklı bölgelerde çalışıyorsanız birden fazla sağlayıcıyı yönetin. Sağlayıcı sistemi genişletilebilir - Stripe Terminal'in pazarınızda işlemesi durumunda, ek ödeme sağlayıcıları sağlayıcı çerçevesi aracılığıyla entegre edilebilir.

Ödeme sağlayıcılarını, kart ödemelerini güvenli bir şekilde kabul etmek, işlem durumlarını izlemek ve okuyucu atamalarını yönetmek için kullanın.

![Ödeme Sağlayıcı Listesi](/static/core/admin/img/help/payment-terminal-providers/provider-list.webp)

## Ödeme Sağlayıcıları Genel Bakış

Ödeme sağlayıcıları, işletmenizin behalfında kart ödemelerini işleyen üçüncü taraf hizmetlerdir:

**Sağlayıcı Sorumlulukları**:
- Gerçek zamanlı kart işlemleri onayla
- Fiziksel kart okuyucuları ile iletişim kur
- Ödeme güvenliği (PCI uygunluk, şifreleme) işleyin
- Fonları banka hesabınıza aktarın (bakiye)
- İşlem raporlama ve anlaşmazlık yönetimi sağlayın

**Spwig'in Rolü**:
- Yapılandırılmış sağlayıcıya ödeme isteklerini yönlendirir
- Şifrelenmiş sağlayıcı kimlik doğrulama bilgilerini saklar
- Bağlantı durumunu izler
- Okuyucuları terminalle ilişkilendirir
- Ödeme sonuçlarını siparişlerde kaydeder

## Stripe Terminal (Başlıca Sağlayıcı)

Stripe Terminal, çoğu satıcı için önerilen ödeme sağlayıcısıdır:

**Özellikler**:
- Modern EMV çip kart okuyucuları
- Dokunsuz (NFC) ödeme desteği (Apple Pay, Google Pay, dokunarak ödeme kartları)
- Entegre anlaşmazlık yönetimi
- Gerçek zamanlı onay
- Geliştirici dostu API
- 40'dan fazla ülkede mevcut

**Fiyatlandırma** (2024 itibariyle, güncel ücretleri kontrol edin):
- İşlem ücretleri: Kişisel işlemler için 2,7% + 0,05 $ (ABD)
- Aylık ücret yok, kurulum ücreti yok, PCI uygunluk ücreti yok
- Kart okuyucu donanımı: Tek seferlik satın alma ($59-$299, modeline göre)

**Desteklenen Bölgeler**:
- ABD, Kanada, Birleşik Krallık, Avrupa Birliği, Avustralya, Singapur ve daha fazlası
- Stripe Terminal'in mevcutluğunu kontrol edin: https://stripe.com/terminal

**Desteklenen Okuyucular**:
- BBPOS WisePOS E (tümleşik Android terminali)
- Stripe Reader S700 (masaüstü okuyucu)
- Verifone P400 (eski okuyucu, hâlâ destekleniyor)

## Stripe Terminal Kurulumu

**Adım 1: Stripe Hesabı Oluşturun**
- stripe.com'da kayıt olun
- İşletme doğrulamasını tamamlayın (banka hesabı, vergi kimlik numarası)
- Ödemeleri etkinleştirin

**Adım 2: Stripe Terminal'i Etkinleştirin**
- Stripe Dashboard'da **Ürünler > Terminal**'e gidin
- **Başlamak İçin Tıklayın**'a tıklayın
- Terminal hizmet koşullarını kabul edin

**Adım 3: Konum Oluşturun**
- Stripe Terminal, fiziksel mağaza sitesinizi temsil eden bir "Konum" gerekir
- **Terminal > Konumlar**'a gidin
- **Konum Oluştur**'a tıklayın
- Mağaza adresini ve ayrıntılarını girin
- Konum ID'sini kaydedin (gibi görünür `tml_1ABC123...`)

**Adım 4: API Anahtarı Oluşturun**
- **Geliştiriciler > API Anahtarları**'na gidin
- **Gizli Anahtar**'ınızı bulun (üretim için `sk_live_...` ile başlar, test için `sk_test_...`)
- Gizli anahtarı kopyalayın (genelde paylaşmayın)

**Adım 5: Spwig'de Yapılandırın**
- **POS > Ödeme Sağlayıcıları**'na gidin
- **+ Ödeme Sağlayıcısı Ekle**'ye tıklayın
- **Sağlayıcı**: "Stripe Terminal" seçin
- **API Gizli Anahtarı** girin (Adım 4'ten)
- **Konum ID'si** girin (Adım 3'ten)
- Kaydedin

**Adım 6: Bağlantıyı Test Edin**
- Kaydetme sonrasında, sağlayıcı durumu "Bağlantı Kuruldu" (yeşil) olmalıdır
- Durum "Hata" (kırmızı) gösteriyorsa, API anahtarını ve konum ID'sini doğrulayın
- Sağlayıcı ayrıntı görünümünde hata mesajını kontrol edin

![Ödeme Sağlayıcısı Ekleme Formu](/static/core/admin/img/help/payment-terminal-providers/provider-add-form.webp)

## Sağlayıcı Yapılandırma Alanları

**Sağlayıcı Anahtarı** - Ödeme işleme sağlayıcısını seçin:
- **stripe_terminal** - Stripe Terminal (önerilir)
- **manual** - Manuel ödeme girişi (yalnızca test için, gerçek işlem yok)
- Ek sağlayıcılar, bileşen sistemi aracılığıyla yüklendiğinde görünür olabilir

**Kimlik Doğrulama (Şifrelenmiş)** - API kimlik doğrulama bilgilerini içeren JSON yapısı:
- Depolama öncesi otomatik şifrelenir
- Kaydetme sonrasında düz metin olarak asla görünmez
- Örnek yapı (Stripe Terminal):
```json
{
  "api_key": "sk_live_ABC123...",
  "location_id": "tml_1ABC123..."
}
```

**Sağlayıcı Ayarları** - Ek yapılandırma (sağlayıcıya özel):
- İşlem tanımlayıcı (müşterinin kredi kartı faturasında görünür)
- Otomatik yakalama (onaylanan ödemeleri hemen yakalayın vs. el ile yakalama)
- Para birimi geçersizleme (sağlayıcı hesabı, mağaza ile farklı para birimi kullanıyorsa)

**Bağlantı Durumu** - Gerçek zamanlı durum göstergesi:
- **Bağlantı Kuruldu** (yeşil) - Sağlayıcı erişilebilir ve doğru şekilde yapılandırılmıştır
- **Hata** (kırmızı) - Bağlantı başarısız oldu veya geçersiz kimlik doğrulama bilgileri
- **Bilinmeyen** (gri) - Henüz test edilmedi (oluşturma işleminden hemen sonra)

**Son Test** - En son bağlantı testinin zaman damgası:
- İşlem sırasında otomatik olarak güncellenir
- **Bağlantı Testi** admin eylemini manuel olarak tetikleyerek testi başlatın

## Bağlantı Durumu İzleme

Sistem, sağlayıcı bağlantısını izleyerek müşteriler ödeme yapmaya çalışmadan önce sorunları bildirir:

**Otomatik Test**:
- Her ödeme işlemi, bağlantı testini tetikler (gereklilik)
- Arka plan işi, her 6 saatte bir bağlantı testi yapar (önleyici izleme)

**Durum Anlamları**:

**Bağlantı Kuruldu** - Sağlayıcı API'si erişilebilir, kimlik doğrulama bilgileri geçerli, ödemeleri işlemeye hazırdır

**Hata** - Yaygın nedenler:
- Geçersiz API anahtarı (iptal edildi, sona erdi veya yanlış)
- Geçersiz konum ID'si (Stripe'da konum silindi, yanlış ID girildi)
- Ağ bağlantısı sorunları (Stripe API'sini engelleyen güvenlik duvarı)
- Stripe hizmeti aksaklığı (nadir)

**Bilinmeyen** - Sağlayıcı henüz test edilmedi (yeni oluşturulan hesap ilk işlemi bekliyor)

**Hata Durumunu Çözmek**:
1. Sağlayıcı ayrıntı görünümünde hata mesajını kontrol edin (özel sorunu açıklar)
2. Stripe Dashboard'da API anahtarının hâlâ geçerli olduğundan emin olun
3. Stripe Dashboard'da konum ID'sinin hâlâ mevcut olduğundan emin olun
4. **Bağlantı Testi** admin eylemini kullanarak bağlantı testini manuel olarak tetikleyin
5. Gerekirse kimlik doğrulama bilgilerini güncelleyin

![Ödeme Sağlayıcı Ayrıntıları](/static/core/admin/img/help/payment-terminal-providers/provider-detail.webp)

## Desteklenen Kart Okuyucuları Karşılaştırması

Stripe Terminal, birden fazla okuyucu donanımı seçeneği sunar:

| Model | Tür | Ödeme Yöntemleri | Ekran | En Uygun Olduğu | Fiyat |
|-------|------|-----------------|---------|----------|-------|
| **WisePOS E** | Tümleşik | EMV çip, NFC, sürükleyin | 5" renkli dokunmatik ekran | Tam özellikli perakende POS | ~$299 |
| **S700** | Masaüstü | EMV çip, NFC, sürükleyin | Monokrom LCD | Standart perakende ödeme | ~$249 |
| **P400** | Masaüstü | EMV çip, NFC, sürükleyin | Monokrom LCD | Eski dağıtımlar | ~$299 |

**WisePOS E Avantajları**:
- Android tabanlı (uygulamalar çalıştırabilir, özel içerik görüntüleyebilir)
- Renkli dokunmatik ekran (ipotek istekleri, imza yakalama için daha iyi kullanıcı deneyimi)
- Entegre fatura yazdırıcısı (isteğe bağlı)
- En hızlı işlem hızı

**S700 Avantajları**:
- WisePOS E'den daha düşük maliyet
- Daha küçük ayak izi
- Su geçirmez tasarım

**P400** (eski model):
- Hâlâ destekleniyor ancak yeni dağıtımlar için önerilmiyor
- S700/WisePOS E'den daha yavaş çip kart işleme

Tüm okuyucular, Stripe Terminal API'si aracılığıyla Spwig POS'a bağlanır (POS cihazına doğrudan USB/Bluetooth bağlantısı gerekmez).

## Güvenlik Dikkatleri

**Kimlik Doğrulama Şifrelemesi**:
- Tüm sağlayıcı kimlik doğrulama bilgileri veritabanında şifrelenir
- Şifreleme, uygulama gizli anahtarı (uygulama ayarlarında tanımlanmıştır) kullanır
- Kimlik doğrulama bilgileri asla günlüklerde veya hata mesajlarında görünmez

**API Anahtarı İzinleri**:
- Üretimde **sınırlı API anahtarları** kullanın (Terminal'e özel izinleri sınırlayın)
- Sınırsız gizli anahtarları kullanmayın (gereksiz olarak daha geniş erişim = güvenlik riski)
- Stripe Dashboard'da yalnızca **Terminal** izinleriyle sınırlı anahtar oluşturun

**PCI Uygunluk**:
- Stripe Terminal, PCI uygunluğunu işler (kart verisi Spwig sunucularına asla ulaşmaz)
- Kart numaraları tamamen okuyucu donanımında → Stripe sunucularında → kart ağlarında işlenir
- Spwig yalnızca ödeme sonuçlarını (onay/iptal) saklar, asla kart ayrıntılarını saklamaz

**Anahtar Döngüleme**:
- Güvenlik en iyi uygulamaları olarak yılda bir kez anahtar döngüleme yapın
- Anahtar döngüleme sırasında sağlayıcı yapılandırmasında kimlik doğrulama bilgilerini güncelleyin
- Yeni anahtarın işe yaradığını doğruladıktan sonra Stripe Dashboard'da eski anahtarları iptal edin

## Birden Fazla Sağlayıcı

Bazı satıcılar birden fazla sağlayıcı hesabı gerektirir:

**Çok Para Birimi İşlemleri**:
- ABD mağazaları, ABD Stripe hesabı kullanır (USD işlemi)
- Avrupa mağazaları, Avrupa Stripe hesabı kullanır (EUR işlemi)
- Her para birimi için ayrı sağlayıcı yapılandırın

**Yedek Sağlayıcılar**:
- Başlıca sağlayıcı (Stripe Terminal)
- Okuyucular arızalanırsa yedek sağlayıcı (manuel giriş)
- Kasa, ödeme başlatırken sağlayıcıyı seçer

**Test vs. Üretim**:
- Test sağlayıcısı `sk_test_...` API anahtarı ile
- Üretim sağlayıcısı `sk_live_...` API anahtarı ile
- Test fazı sonrası sağlayıcıları değiştirin

## Yaygın Sorun Giderme

**Sorun 1: Durum "Hata" gösteriyor ve mesaj "Geçersiz API anahtarı"**
- **Neden**: API anahtarı iptal edildi veya yanlış kopyalandı
- **Çözüm**: Stripe Dashboard'da yeni API anahtarı oluşturun, sağlayıcı kimlik doğrulama bilgilerini güncelleyin, bağlantı testini yapın

**Sorun 2: Ödeme sırasında okuyucu bulunamadı**
- **Neden**: Okuyucu sağlayıcının konumuna kaydedilmedi
- **Çözüm**: Stripe Dashboard'da okuyucunun aynı konum ID'sinin sağlayıcı yapılandırmasıyla kullanılıp kullanılmadığını doğrulayın

**Sorun 3: Geçerli kart rağmen ödemeler reddedildi**
- **Neden**: Stripe hesabı tamamen etkinleştirilmemiş (doğrulama bekleniyor)
- **Çözüm**: Stripe Dashboard'da işyeri doğrulamasını tamamlayın (banka hesabı, vergi kimlik numarası)

**Sorun 4: Bağlantı durumu "Bilinmeyen" gösteriyor ve asla güncellenmiyor**
- **Neden**: Sağlayıcı asla test edilmedi (hiç işlem denenmedi)
- **Çözüm**: **Bağlantı Testi** admin eylemini kullanarak bağlantı testini manuel olarak tetikleyin

## İpuçları

- **Üretimden önce test modu** - Stripe test API anahtarlarını (`sk_test_...`) başlangıç kurulumu ve test için kullanın
- **Bir sağlayıcı her para birimi için** - ABD tabanlı Stripe hesabıyla EUR işlemi yapmaya çalışmayın; ayrı sağlayıcılar oluşturun
- **Haftalık bağlantı durumunu izleyin** - Proaktif izleme, ödeme başarısızlıklarını önler
- **API anahtarı izinlerini kısıtlayın** - Stripe API anahtarlarını yalnızca Terminal izinlerine sınırlayın (en az izin ilkesi)
- **Konum ID'lerini belgeleyin** - Hangi Stripe konumunun hangi fiziksel mağazaya karşılık geldiğini kaydedin
- **Okuyucu atamalarını test edin** - Sağlayıcı kurulumu sonrası, gerçek kart okuyucuyla ödeme testi yaparak uçtan uca akışı doğrulayın
- **Stripe iletişim bilgilerini güncel tutun** - İşyeri iletişim bilgilerinin Stripe ile eşleştiğinden emin olun (anlaşmazlıklar, uygunluk için önemli)