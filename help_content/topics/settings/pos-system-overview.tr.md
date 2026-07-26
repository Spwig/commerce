---
title: POS Sistemi Genel Bakış
---

Spwig POS sistemi, modern nokta-üstü terminallerle mağazanızı tam bir perakende çözümüne dönüştürür. Bu sistem, her bir sürümde — Topluluk, Profesyonel ve Kurumsal — sınırsız lokasyonlarda sınırsız terminallerle ek maliyet olmadan dahildir. Her terminaller, çevrimdışı çalışabilen, otomatik olarak senkronize olan ve stok, müşteri verileri ve ödeme işleme ile tümleşik olan İlerleyen Web Uygulaması (PWA) olarak çalışır. Her şeyi admin panelden yönetin — terminal yapılandırması, vardiya dengeleme, fatura özelleştirme ve donanım entegrasyonu.

POS sistemini fiziksel perakende lokasyonlarınızda, geçici mağazalarda, fuarlarda veya müşterilerin doğrudan çevrimiçi olmayan ortamlarda alışveriş yaptığı herhangi bir ortamda kullanın.

![POS Dashboard](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Spwig POS Nedir?

Spwig POS, hem çevrimiçi hem de fiziksel lokasyonlarda satış yapan satıcılar için tamamen entegre bir nokta-üstü sistemdir. Üçüncü taraf POS sistemlerinin karmaşık entegrasyonları gerektirmesi aksine, Spwig POS, platformunuza doğrudan entegre edilmiştir ve tüm satış kanalları arasında mükemmel veri senkronizasyonunu garanti altına alır.

**Önemli Özellikler**:
- **Sınırsız Terminaller** - Ek maliyet olmadan ihtiyaç duyduğunuz kadar terminalleri dağıtın
- **Çevrimdışı Öncelikli Mimari** - İnternet bağlantısı kaybolduğunda bile satış işleme devam eder
- **İlerleyen Web Uygulaması** - Uygulama mağazasına kurulum gerekmez; herhangi bir cihazda (tabletlar, bilgisayarlar, özel terminaller) tarayıcı üzerinden erişilebilir
- **Gerçek Zamanlı Stok Senkronizasyonu** - (15 dakikalık TTL) stok rezervasyonu, kanallar arasında aşırı satışı önler
- **Ödeme Yöntemi Bölünmesi Desteği** - Bir işlem için birden fazla ödeme yöntemi (nakit + kart + hediye kartı) kabul edin
- **Donanım Entegrasyonu** - ESC/POS termal yazıcılar, barkod okuyucular, nakit kasaları, müşteri ekranları
- **Vardiya Yönetimi** - Açılış/kapanış sayım ve fark takibi ile nakit dengeleme
- **Çok Lokasyonlu Hazır** - Franchise ve bölgesel yönetim için ayarlar miras alma ile mağaza grupları

## Sürüm

POS, Spwig 1.5.8 sürümünden itibaren her Spwig sürümünde — Topluluk, Profesyonel ve Kurumsal — dahildir. Ayrı bir POS lisansı, etkinleştirme adımı veya terminale göre ücret yoktur.

**Her sürümde dahil olanlar**:
- Sınırsız terminal kaydı
- Sınırsız personel ataması
- Tüm POS özellikleri (vardiyalar, nakit yönetimi, fatura özelleştirmesi, müşteri ekranları)
- Ödeme sağlayıcı entegrasyonları (Stripe Terminal ve diğer desteklenen sağlayıcılar)
- Donanım entegrasyonu desteği

Spwig-hosted mağazaları işleten veya Profesyonel/Kurumsal lisans ödemeleri yapan satıcılar, isteğe bağlı Spwig-hosted hizmetlerinde (GeoIP, coğrafi kodlayıcı, push bildirimleri) daha yüksek sınırlara ve öncelikli destekle sahip olur, ancak POS özellik seti tüm sürüm arasında aynıdır.

## Sistem Mimari

**Ön uç** - React 18 İlerleyen Web Uygulaması:
- Çevrimdışı öncelikli, Service Worker önbellekleme ile (internet olmadan çalışır)
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
- Yönetici acil durumlarında uzaktan kilitleme/kilit açma yeteneği
- Şifrelenmiş ödeme sağlayıcı kimlik bilgileri
- Oturum tabanlı kimlik doğrulama ile biyometrik kilitleme desteği (tarayıcıya bağlı)

## Başlangıç Akışı

İlk POS terminalinizi dağıtmak için bu 4 adımı takip edin.



POS ile başlamanın adım adım bir kontrol listesini, personel kurulumu, ödeme sağlayıcıları ve ilk satışınızı yapma dahil, [POS ile Başlarken](getting-started-with-pos) kısmında bulabilirsiniz.

**Adım 1: Depo Oluştur**
- **Katalog > Depolar** bölümüne gidin
- Mağazanızın fiziksel konumunu temsil eden bir depo oluşturun
- Adres ve iletişim bilgilerini yapılandırın
- Bu depo, POS satışları için fiziksel stok takibini sağlayacaktır

**Adım 2: Terminali Kaydet**
- **POS > Terminal** bölümüne gidin
- **+ Terminal Ekle**'ye tıklayın
- Terminal adını belirleyin (örneğin, "Ana Kayıt", "Ödeme 1")
- Adım 2'den depoyu atayın
- Donanım ayarlarını yapılandırın (yazıcı, tarayıcı, para çekme çekmecesi)
- Kaydetmek için 8 karakterlik eşleştirme kodunu oluşturun

**Adım 3: Personel Ata**
- Terminal yapılandırmasında, **Atanmış Kullanıcılar** bölümüne kaydırın
- Bu terminali kullanmaya yetkili personel üyelerini seçin
- Sadece atanan kullanıcılar terminalde oturum açabilir
- Kullanıcılar, personel rolüne uygun POS izinlerine sahip olmalıdır

**Adım 4: Cihazı Eşle**
- Terminal cihazınızda (tablet/bilgisayar) `/pos/` URL'sine gidin
- Adım 3'ten alınan 8 karakterlik eşleştirme kodunu girin
- Terminal yapılandırmasını indirir ve başlangıç verilerini senkronize eder
- Atanmış personel kimlik bilgileriyle oturum açın
- Terminal satışlar için hazırdır

Eşleştirme işlemi tamamlandıktan sonra terminaler 5 dakikada bir otomatik olarak senkronize olur (ayarlanabilir). Çevrimdışı mod, internet bağlantısı kesildiğinde devam eden işlemi sağlar — bağlantı geri geldiğinde satışlar otomatik olarak senkronize olur.

## POS Çekirdek Özellikleri

**Satış İşlemleri**:
- Ürün adı, SKU veya barkod ile ürün arama
- Ödeme yöntemi bölünmesi (tek bir sipariş için birden fazla ödeme yöntemi)
- Bekletilmiş sepetler (tamamlanmamış işlemler kaydedilebilir)
- Neden takibiyle iade ve iptal
- İndirim uygulama (kuponlar, hediye kartları, kampanyalar)
- Müşteri arama ve sadakat puanı geri ödemesi

**Para Yönetimi**:
- İş başlangıcı ile başlangıç para sayımı
- İş bitişi ile beklenen vs. gerçek senkronizasyonu
- Para hareketleri (para eklemeleri, nedenle küçük para çekmeleri)
- Para satışlarına dayalı otomatik beklenen para hesaplaması
- Sapma takibi ve raporlama

**Donanım Entegrasyonu**:
- ESC/POS termal fatura yazıcıları (ağ veya seri)
- USB barkod tarayıcıları
- Yazıcı pulsu aracılığıyla para çekme çekmecesi tetikleme
- Müşteri odaklı ekranlar (boşta promosyon karuzeli)
- Stripe Terminal kart okuyucuları (S700, WisePOS E, P400)

**Çevrimdışı Özellikler**:
- Service Worker, tüm terminal varlıklarını önbelleğe alır
- IndexedDB, son satışları saklar (ayarlanabilir: 7-30 gün, 200-1000 sipariş)
- 15 dakikalık TTL ile stok rezervasyonu, aşırı satışları önler
- Bağlantı geri geldiğinde senkronizasyon için satış kuyruğu
- Otomatik yeniden bağlanma algılama

## POS Yönetici Sayfaları

POS dağıtımınızın tüm yönlerini yönetmek için bu yönetici sayfalarına erişin:

**POS Dashboard** (`/admin/pos/`)
- Sistem genel bakışı ve hızlı istatistikler
- Son terminal etkinliği
- Aktif iş özetleri
- Barındırılmış hizmet kullanımına dair modüller (GeoIP, coğrafi kodlayıcı, push — bkz. [Spwig Barındırılmış Hizmetler](hosted-services))

**Terminal Yönetimi** (`/admin/pos_app/posterminal/`)
- Terminali kaydetme ve yapılandırma
- Personel ve depoları atama
- Çevrimiçi/çevrimdışı durumunu izleme (kalp atışı izleme)
- Uzaktan terminal kilidini kaldırma
- [Daha fazla bilgi: POS Terminal Yönetimi](managing-pos-terminals)

**İş Yönetimi** (`/admin/pos_app/posshift/`)
- Tüm işleri görüntüleme (açık, kapalı, tarihi)
- Para senkronizasyonu raporlarını inceleme
- Para hareketlerini ve sapmaları izleme
- İş etkinliklerini denetleme
- [Daha fazla bilgi: POS İşleri ve Para Yönetimi](pos-shifts-cash-management)

**Mağaza Grupları** (`/admin/pos_app/storegroup/`)
- Terminali konum/bölgeye göre organize etme
- Grup seviyesi ayarlarını yapılandırma (para birimi, dil, saat dilimi)
- Ayar kalıtım hiyerarşisini uygulama
- [Daha fazla bilgi: POS Mağaza Grupları](pos-store-groups)

**Fatura Şablonları** (`/admin/pos_app/receipttemplate/`)
- Yazdırılan faturaları özelleştirin (kağıt genişliği, logo, üst/başlık)
- Uygunluk alanlarını yapılandırın (vergi kimlik numarası, iş kaydı)
- İndirimler için QR kodları ekleyin
- Şablonları belirli mağazalara veya gruplara uygulayın
- [Daha fazla bilgi: Fatura Şablonu Özelleştirmesi](receipt-template-customization)

**Promosyon Kayakları** (`/admin/pos_app/promoslide/`)
- Müşteri ekranı için kaydırma içeriği oluşturun
- Kayakları belirli mağazalara veya gruplara hedefleyin
- Mevsimsel promosyonları planlayın
- [Daha fazla bilgi: Müşteri Ekranı Promosyon Kayakları](customer-display-promo-slides)

**Ödeme Sağlayıcıları** (`/admin/pos_app/posterminalprovider/`)
- Stripe Terminal entegrasyonunu yapılandırın
- Ödeme sağlayıcı kimlik bilgilerini yönetin
- Bağlantı durumunu izleyin
- [Daha fazla bilgi: Ödeme Terminal Sağlayıcıları](payment-terminal-providers)

**Kart Okuyucuları** (`/admin/pos_app/posterminalreader/`)
- Fiziksel kart okuyucularını kaydolun
- Okuyucuları terminalere atayın
- Splash ekranlarını özelleştirin (müşteri odaklı ekran markalaştırması)
- Okuyucu durumunu izleyin (çevrimiçi/çevrimdışı/şeffaflıkta)
- [Daha fazla bilgi: Kart Okuyucu Yönetimi](card-reader-management)

## Çok Konumlu Dağıtım

Birden fazla perakende konumu olan ticari işletmeler için Spwig POS, hiyerarşik ayar miraslığına destek sağlar:

**Ayar Hiyerarşisi** (en yüksek öncelikten en düşük):
1. Terminal özel ayarları (tümünü geçersiz kıl)
2. Mağaza özel ayarları (grup ve siteyi geçersiz kıl)
3. Grup ayarları (site varsayılanlarını geçersiz kıl)
4. Site varsayılanları (tüm için geri dönüş)

Grup düzeyinde paylaşılan ayarları yapılandırın (örneğin, bölgesel para birimi, dil) ve gerekirse belirli mağazalar veya terminaler için geçersiz kılın. Ayrıntılı yapılandırma kılavuzu için [POS Mağaza Grupları](pos-store-groups)’ye bakın.

## İpuçları

- **Bir terminalle başlayın** - Dağıtım genelinde test etmeden önce tek bir terminalle POS kurulumunu ve iş akışını test edin
- **Eşleştirme öncesi depo atayın** - Terminal, bir depo ataması olmadan satış işlemi yapamaz
- **Fatura şablonlarını erken yapılandırın** - Vergi kimlikleri bölgesel olarak değişebilir; canlıya geçmeden önce kurulum yapın
- **Çevrimdışı modu test edin** - İnterneti keserek satışların devam ettiğini doğrulayın; yeniden bağlanıldığında senkronizasyonu onaylayın
- **Çok konumlu için mağaza gruplarını kullanın** - Franchise veya bölgesel dağıtımlar için yapılandırma yönetimini basitleştirir
- **Kalp atışı durumunu izleyin** - Terminal, sunucuya her 5 dakikada bir ping gönderir; çevrimdışı terminaller yönetici panelinde görünür
- **Performans için senkronizasyon sınırlarını yapılandırın** - Yavaş bağlantıya sahip terminaler için daha düşük sync_days/sync_limit ayarları faydalıdır
- **Donanım yapılandırmasını yedekleyin** - Yazıcı IP'leri, tarayıcı ayarları, nakit çekme cihazı yapılandırması için acil durum kurtarma için belgeleyin