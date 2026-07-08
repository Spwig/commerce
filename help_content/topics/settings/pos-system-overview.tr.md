---
title: POS Sistemi Genel Bakış
---

Spwig POS sistemi, mağazanızı modern nokta-üstü terminallerle birlikte tam bir perakende çözümüne dönüştürür. Sınırsız sayıda konumda sınırsız sayıda terminalleri, yıllık €499 sabit ücretle lisanslayabilirsiniz. Her terminaller, çevrimdışı çalışabilen, otomatik olarak senkronize olan ve stok, müşteri verileri ve ödeme işleme ile tamamen entegre olan ilerici web uygulamasıdır (PWA). Admin panelinden her şeyi yönetin - terminallerin yapılandırılması, vardiya dengelemesi, fatura özelleştirmesi ve donanım entegrasyonu.

Fiziksel perakende konumları, pop-up mağazaları, fuarları veya müşterilerin çevrimiçi değil, fiziksel olarak alışveriş yaptığı herhangi bir ortamda POS sistemini kullanın.

![POS Dashboard](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Spwig POS Nedir?

Spwig POS, hem çevrimiçi hem de fiziksel konumlarda satış yapan satıcılar için tamamen entegre bir nokta-üstü sistemdir. Üçüncü taraf POS sistemlerinin karmaşık entegrasyonları gerektirmesi aksine, Spwig POS, platformunuza doğrudan entegre edilmiştir ve tüm satış kanalları arasında mükemmel veri senkronizasyonu sağlar.

**Önemli Özellikler**:
- **Sınırsız Terminaller** - Ekstra maliyet olmadan gerekli olan kadar terminalleri dağıtın
- **Çevrimdışı Öncelikli Mimari** - İnternet bağlantısı kaybolduğunda bile satış işleme devam eder
- **İlerici Web Uygulaması** - Uygulama mağazasına kurulum gerekmez; herhangi bir cihazda (tabletlar, bilgisayarlar, özel terminaller) tarayıcı üzerinden erişilebilir
- **Gerçek Zamanlı Stok Senkronizasyonu** - Stok rezervasyonu (15 dakika TTL) kanallar arasında aşırı satışı önler
- **Ödeme Yöntemi Bölünmesi Desteği** - İşlem başına birden fazla ödeme yöntemi (nakit + kart + hediye kartı)
- **Donanım Entegrasyonu** - ESC/POS termal yazıcılar, barkod okuyucular, kasalar, müşteri ekranları
- **Vardiya Yönetimi** - Nakit dengeleme ile açılış/kapanış sayım ve fark takibi
- **Çok Konumlu Hazır** - Franchise ve bölgesel yönetim için ayarlar miras alma ile mağaza grupları

## Lisanslama ve Etkinleştirme

**Sabit Fiyatlandırma**: Yıllık €499, sınırsız konumlarda sınırsız terminalleri kapsar. Terminal başına ücret, işlem ücreti, gizli maliyet yok.

**Lisans Formatı**: `POS-XXXX-XXXX-XXXX-XXXX` (satın alma sonrası sağlanır)

**Etkinleştirme**: **Ayarlar > POS Lisanslama** içinde lisans anahtarınızı girin. Sistem, Spwig lisanslama sunucusu ile doğrular ve tüm POS özellikleri hemen etkinleştirilir. Lisanslar, ödeme işleme gecikmelerini önlemek için sona erdikten sonra 14 günlük bir geçiş dönemi içerir.

**Neler Alırsınız**:
- Sınırsız terminal kaydı
- Sınırsız personel ataması
- Tüm POS özellikleri (vardiyalar, nakit yönetimi, fatura özelleştirmesi, müşteri ekranları)
- Ödeme sağlayıcı entegrasyonları (Stripe Terminal ve genişletilebilir sağlayıcı sistemi)
- Donanım entegrasyonu desteği
- Lisans süresi boyunca güncellemeler ve hata düzeltmeleri

Geçerli bir lisans olmadan POS özellikleri erişilemez - terminal eşleştirme arayüzü, vardiya yönetimi ve POS admin sayfaları tümüyle etkinleştirme gerektirir.

## Sistem Mimarisi

**Ön uç** - React 18 İlerici Web Uygulaması:
- Çevrimdışı öncelikli, Service Worker önbelleğe alma ile (internet olmadan çalışır)
- Hızlı yükleme için Vite derleme sistemi
- CSS Modülleri + tasarım tokenları (mağaza temanızla uyumlu)
- Lokal veri kalıcılığı için IndexedDB
- 10 desteklenen dil (İngilizce, Çince Basit/Tradiyonel, Fransızca, Almanca, İspanyolca, Portekizce, Japonca, Rusça, Arapça)

**Arka uç** - Arka uç Entegrasyonu:
- 13 POS modeli (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, vb.)
- Terminal işlemleri için 43+ REST API uç noktası
- TTL yönetimi ile stok rezervasyon sistemi
- Arka plan senkronizasyonu için Celery görevleri
- Ödeme sağlayıcıları için şifrelenmiş kimlik bilgileri depolama

**Güvenlik**:
- 8 karakterli kodlarla terminal eşleştirme (sunucu tarafında oluşturulur, kullanımdan sonra sona erer)
- Personel atama, hangi kullanıcıların hangi terminalleri erişebileceğini kontrol eder
- Yönetici acil durumlar için uzaktan kilitleme/kilit açma yeteneği
- Şifrelenmiş ödeme sağlayıcı kimlik bilgileri
- Oturum tabanlı kimlik doğrulama ile biyometrik kilitleme desteği (tarayıcıya bağlı)

## Başlangıç Akışı

İlk POS terminalinizi dağıtmak için bu 5 adımı takip edin:

**Adım 1: POS Lisansını Etkinleştirin**
- **Ayarlar > POS Lisanslama**'ya gidin
- Lisans anahtarınızı girin (`POS-XXXX-XXXX-XXXX-XXXX`)
- Lisansı doğrulayın (internet bağlantısı gerekir)
- Etkinleştirme işlemini onaylayın

**Adım 2: Depo Oluşturun**
- **Katalog > Depolar**'a gidin
- Mağaza konumunuzu temsil eden bir depo oluşturun
- Adres ve iletişim bilgilerini yapılandırın
- Bu depo, POS satışları için fiziksel stokları izleyecektir

**Adım 3: Terminali Kaydettirin**
- **POS > Terminaller**'e gidin
- **+ Terminal Ekle**'ye tıklayın
- Terminal adını belirleyin (örneğin, "Ana Kayıt", "Ödeme 1")
- Adım 2'den depoyu atayın
- Yazıcı, tarayıcı, nakit kasası donanım ayarlarını yapılandırın
- Kaydetmek için 8 karakterli eşleştirme kodunu oluşturun

**Adım 4: Personel Atayın**
- Terminal yapılandırması içinde, **Atanmış Kullanıcılar** kısmına kaydırın
- Bu terminali kullanmaya yetkili personel üyelerini seçin
- Sadece atanan kullanıcılar terminalde oturum açabilir
- Kullanıcılara, görev rolüne uygun POS izinleri olmalıdır

**Adım 5: Cihazı Eşleştirin**
- Terminal cihazınızda (tablet/bilgisayar) `/pos/` URL'sine gidin
- Adım 3'ten alınan 8 karakterli eşleştirme kodunu girin
- Terminal yapılandırmasını indirir ve başlangıç verilerini senkronize eder
- Atanmış personel kimlik bilgileriyle oturum açın
- Terminal satışlar için hazırdır

Eşleştirme sonrası, terminaller her 5 dakikada bir otomatik olarak senkronize olur (ayarlanabilir). Çevrimdışı mod, internet bağlantısı yokken devam eden işlemi sağlar - bağlantı geri döndüğünde satışlar otomatik olarak senkronize olur.

## POS Ana Özellikler

**Satış İşleme**:
- İsim, SKU veya barkod ile ürün arama
- Bölünmüş ödeme (sipariş başına birden fazla ödeme yöntemi)
- Bekletilmiş sepetler (tamamlanmamış işlemler kaydedilir)
- İade ve iptal ile neden takibi
- İndirim uygulama (kuponlar, hediye kartları, kampanyalar)
- Müşteri arama ve sadakat puanı geri ödemesi

**Nakit Yönetimi**:
- Vardiya başlangıcı ile başlangıç nakit sayımı
- Vardiya bitişi ile beklenen vs. gerçek dengeleme
- Nakit hareketleri (kasa eklemeleri, küçük para çekmeleri nedenleriyle)
- Nakit satışlarına dayalı otomatik beklenen nakit hesaplama
- Fark takibi ve raporlama

**Donanım Entegrasyonu**:
- ESC/POS termal fatura yazıcıları (ağ veya seri)
- USB barkod okuyucuları
- Kasa kilit açma, yazıcı pulsu ile
- Müşteri odaklı ekranlar (boşta kampanya karuzeli)
- Stripe Terminal kart okuyucuları (S700, WisePOS E, P400)

**Çevrimdışı Özellikler**:
- Service Worker, tüm terminal varlıklarını önbelleğe alır
- IndexedDB, son satışları saklar (ayarlanabilir: 7-30 gün, 200-1000 satış)
- 15 dakika TTL ile stok rezervasyonu, aşırı satışları önler
- Bağlantı geri döndüğünde senkronizasyon için satışları kuyruğa al
- Otomatik yeniden bağlanma algılama

## POS Admin Sayfaları

POS dağıtımınızın tüm yönlerini yönetmek için bu admin sayfalarına erişin:

**POS Dashboard** (`/admin/pos/`)
- Sistem genel bakışı ve hızlı istatistikler
- Son terminal etkinliği
- Aktif vardiya özeti
- Lisans durumu ve sona erme tarihi

**Terminal Yönetimi** (`/admin/pos_app/posterminal/`)
- Terminali kaydetme ve yapılandırma
- Personel ve depoları atama
- Çevrimiçi/çevrimdışı durumunu izleme (kalp atışı izleme)
- Uzaktan kilidi açma
- [Daha fazla bilgi: POS Terminali Yönetimi](managing-pos-terminals)

**Vardiya Yönetimi** (`/admin/pos_app/posshift/`)
- Tüm vardiya görüntüleme (açık, kapalı, tarihi)
- Nakit dengeleme raporlarını inceleme
- Nakit hareketlerini ve farkları izleme
- Vardiya etkinliklerini denetleme
- [Daha fazla bilgi: POS Vardiya ve Nakit Yönetimi](pos-shifts-cash-management)

**Mağaza Grupları** (`/admin/pos_app/storegroup/`)
- Konum/ bölgeye göre terminalleri organize etme
- Grup seviyesi ayarlarını yapılandırma (para birimi, dil, saat dilimi)
- Ayar miras alma hiyerarşisini uygulama
- [Daha fazla bilgi: POS Mağaza Grupları](pos-store-groups)

**Fatura Şablonları** (`/admin/pos_app/receipttemplate/`)
- Yazdırılan faturaları özelleştirme (kağıt genişliği, logo, başlık/altbilgi)
- Uygunluk alanlarını yapılandırma (vergi kimlikleri, iş kayıt bilgileri)
- Kampanyalar için QR kodlarını ekleme
- Şablonları belirli mağazalar veya gruplara kapsamlandırma
- [Daha fazla bilgi: Fatura Şablonu Özelleştirmesi](receipt-template-customization)

**Promosyon Kaydırıcıları** (`/admin/pos_app/promoslide/`)
- Müşteri ekranı karuzeli içeriği oluşturma
- Belirli mağazalar veya gruplara kaydırıcıları hedefleme
- Mevsimsel kampanyaları planlama
- [Daha fazla bilgi: Müşteri Ekranı Promosyon Kaydırıcıları](customer-display-promo-slides)

**Ödeme Sağlayıcıları** (`/admin/pos_app/posterminalprovider/`)
- Stripe Terminal entegrasyonunu yapılandırma
- Ödeme sağlayıcı kimlik bilgilerini yönetme
- Bağlantı durumunu izleme
- [Daha fazla bilgi: Ödeme Terminali Sağlayıcıları](payment-terminal-providers)

**Kart Okuyucuları** (`/admin/pos_app/posterminalreader/`)
- Fiziksel kart okuyucularını kaydetme
- Okuyucuları terminallere atama
- Splash ekranlarını özelleştirme (müşteri odaklı ekran markalaşması)
- Okuyucu durumunu izleme (çevrimiçi/çevrimdışı/şu anda meşgul)
- [Daha fazla bilgi: Kart Okuyucu Yönetimi](card-reader-management)

## Çok Konumlu Dağıtım

Birden fazla perakende konumu olan satıcılar için Spwig POS, hiyerarşik ayar miras alınmasını destekler:

**Ayar Hiyerarşisi** (en yüksek öncelikten en düşük):
1. Terminal özel ayarları (tümünü geçersiz kılar)
2. Mağaza özel ayarları (grup ve siteyi geçersiz kılar)
3. Grup ayarları (site varsayılanlarını geçersiz kılar)
4. Site varsayılanları (tüm için geri dönüş)

Grup seviyesinde paylaşılan ayarları yapılandırın (örneğin, bölgesel para birimi, dil) ve gerekirse belirli mağazalar veya terminaller için geçersiz kılın. [POS Mağaza Grupları](pos-store-groups) için ayrıntılı yapılandırma kılavuzu için bakın.

## İpuçları

- **Bir terminal ile başlayın** - Geniş dağıtım öncesi tek bir terminal ile POS kurulumunu ve iş akışını test edin
- **Eşleştirme öncesi depo atayın** - Terminal, bir depo ataması olmadan satış işlemeyemez
- **Fatura şablonlarını erken yapılandırın** - Vergi kimlikleri bölgesel olarak değişebilir; canlıya geçmeden önce kurulum yapın
- **Çevrimdışı modu test edin** - İnterneti kesin ve satışların devam ettiğini doğrulayın; yeniden bağlanıldığında senkronizasyonu onaylayın
- **Çok konumlu için mağaza gruplarını kullanın** - Franchise veya bölgesel dağıtımlar için yapılandırma yönetimini kolaylaştırır
- **Kalp atışı durumunu izleyin** - Terminal her 5 dakikada bir sunucuya pings; çevrimdışı terminaller admin panelinde görünür
- **Performans için senkronizasyon sınırlarını yapılandırın** - Yavaş bağlantılar için daha düşük sync_days/sync_limit ayarları faydalıdır
- **Donanım yapılandırmasını yedekleyin** - Yazıcı IP'leri, tarayıcı ayarları, nakit kasası yapılandırması için acil durum kurtarma için belgeleyin

