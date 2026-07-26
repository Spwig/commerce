---
title: POS Çevrimdışı Modu & Uygulama Kurulumu
---

<!-- screenshots-needed:
- url: /pos/
  filename: pos-pwa-idle.webp
  description: POS PWA at rest — main login/terminal chooser view showing the Spwig POS branding
  save-to: core/static/core/admin/img/help/pos-offline-mode/
  viewport: 1440x900
  notes: Add-to-Home-Screen screenshots (iPad Safari, Android Chrome) are OS/browser-specific
         annotated reference shots. The session capturing this should use device emulation
         or reference images rather than attempting to trigger the browser install prompt.
-->

Spwig POS, İlerlemeli Web Uygulaması (PWA) türündedir. Tarayıcıda tamamen çalışır ve bir cihazın ana ekranına yerel bir uygulama gibi kurulabilir. Uygulama, ürün kataloğunuz ve son sipariş geçmişiniz cihazda yerel olarak önbelleğe alınmış olduğundan, kısa süreli ağ kesintileri ve yavaş bağlantılar sırasında kasa hâlâ çalışır.

Bu konu, bağlantı kesildiğinde neyin çalıştığını, bağlantı geri geldiğinde sıraya alınmış satışların nasıl eşitlendiğini, POS'u bir cihazın ana ekranına nasıl kuracağınızı ve güncellemelerin kurulan cihazlara nasıl ulaştığını açıklar.

## Çevrimdışı modun nasıl çalıştığı

Bir cihazda POS'u ilk kez açtığınızda, tarayıcı uygulamanın tamamını — arayüzünü, resimlerini ve tüm destekleyici kodlarını — indirir ve önbelleğe alır. Bu önbelleği yöneten, arka planda çalışan bir bileşen Service Worker adını taşır. Bu noktadan sonra, sunucu erişilebilir olmasa bile uygulama yerel önbellekten yüklenir.

Uygulama önbelleğinin üzerine, POS cihazda yerel bir veritabanı (tarayıcının yerleşik IndexedDB depolama özelliğini kullanarak) tutar. Bu veritabanı şu verileri içerir:

- **Ürünler ve varyasyonlar** — kataloğunuzdan senkronize edilir ve çevrimiçi iken beş dakikada bir yenilenir
- **Kategoriler** — başlangıçta senkronize edilir ve ürünlerle birlikte yenilenir
- **Stok seviyeleri** — çevrimiçi iken iki dakikada bir senkronize edilir (sunucu üç saniye içinde yanıt vermezse önbellek verilerine geri döner)
- **Müşteri kayıtları** — en fazla 1.000 son müşteri
- **Sipariş geçmişi** — yapılandırılabilir sayıda son POS siparişi (varsayılan: 14 gün içinde 500 sipariş; terminal başına **POS > POS Terminali** ayarlanabilir)
- **Ürün resimleri** — 24 saat kadar yerel olarak önbelleğe alınır

POS, cihazın çevrimdışı olduğunu tespit ederse, ekranın üst kısmında bir banner görünür: **"Çevrimdışı Mod - Bağlantı geri geldiğinde satışlar eşitlenecektir."** Kasa yerel önbellek verilerini kullanarak hâlâ çalışır.

## Çevrimdışı olarak çalışabilen özellikler

| Özellik | Çevrimdışı kullanılabilirlik |
|---------|---------------------|
| Ürün arama ve tarif | Kullanılabilir — yerel önbellek kataloğunu kullanır |
| Barkod tarayıcı | Kullanılabilir — yerel önbellek ürünleri tarar |
| Sepete ürün ekleme | Kullanılabilir |
| Manuel indirim uygulama | Kullanılabilir |
| Voucher kodları uygulama | Kullanılamaz — bakiye kontrolü canlı bağlantı gerektirir |
| Nakit ödemeleri | Kullanılabilir — yerel olarak kaydedilir ve eşitleme için sıraya alınır |
| Kart ödemeleri (Manuel Giriş) | Kullanılabilir — kasayıcı ayrı bir terminalde işlem yapar ve referans girer; yerel olarak kaydedilir ve eşitleme için sıraya alınır |
| Kart ödemeleri (entegre okuyucu — Stripe Terminal vb.) | Kullanılamaz — entegre kart okuyucular anlık olarak ödeme ağı ile iletişim kurar |
| Hediye kartı ödemeleri | Kullanılamaz — bakiye kontrolü canlı bağlantı gerektirir |
| Nakit ve manuel kartla birlikte bölünmüş ödemeler | Kullanılabilir |
| Ağ yazdırıcısına fatura basma | Cihaz ile aynı yerel ağa bağlıysa kullanılabilir — fatura basma internete ihtiyaç duymaz, sadece yerel ağ bağlantısı gerekir |
| Dijital faturalar (e-posta/SMS/WhatsApp) | Kullanılamaz — gönderim canlı bağlantı gerektirir |
| Sipariş geçmişi tarif | Kullanılabilir — önbelleklenmiş siparişleri gösterir ve çevrimdışı veri görüntülendiğini belirten bir banner gösterir |
| İade ve iptal | Kullanılamaz — bu işlemler canlı bağlantı gerektirir |
| Müşteri sadakat puanı kontrolü | Kullanılamaz |
| İşlem başlangıcı ve bitişi | Kullanılabilir — işlem durumu yerel olarak saklanır |

## Bağlantı geri geldiğinde sıraya alınmış satışlar ve eşitleme

Çevrimdışı satışlar kaybolmaz.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Kayıt sunucuya ulaşamazsa, her tamamlanan satış cihazın yerel veritabanındaki `pendingTransactions` deposuna yerel bir kuyruk olarak yazılır.

Satış, sepet öğelerini, miktarları, fiyatları, ödeme yöntemini ve tamamlanma zamanını içerir.

İnternet bağlantısı geri geldiğinde POS otomatik olarak:

1. Tarayıcının `online` olayı aracılığıyla yeniden bağlanmayı algılar
2. **"N bekleyen işlem(ler) senkronize ediliyor..."** başlığını gösterir
3. İlk deneme başarısız olursa (her deneme için maksimum 5 dakikalık bir pencere içinde toplamda 10 deneme yaparak) sıraya alınmış satışları arka uç sunucuya sırayla gönderir
4. Arka uç onayladıktan sonra her satışın senkronize olduğunu işaretler

**Çift satış koruma** — her sıraya alınmış satış, cihazdan ayrılmadan önce yerel bir kimliğe sahip olur. Arka uç, bir sipariş oluşturmadan önce bu kimliği kontrol eder. Eğer aynı satış iki kez gönderilmeye çalışılırsa (örneğin, bir tekrar deneme, ilk başarılı deneme ile çakışmışsa), arka uç ikinci gönderimi yok sayar. Çift sayılan satışlara asla ulaşamazsınız.

**Çakışma tespiti** — nadir durumlarda arka uç, sıraya alınmış bir satışın çakıştığını işaretleyebilir (örneğin, cihaz çevrimdışı iken sunucuda bir ürün silinmişse). Çakışan satışlar **POS > Ayarlar > Bekleyen İşlemler** altında görünür, bunları manuel olarak inceleyip çözebilirsiniz.

**Çevrimdışı envanter ayarlamaları** aynı şekilde işlenir: çevrimdışı olarak yapılan envanter değişiklikleri kuyruğa alınır ve bağlantı geri geldiğinde tekrar oynatılır. Cihazdaki yerel envanter rakamları hemen güncellenir, böylece kasiyer yaklaşık (tahmini) sayıyı görebilir.

## POS'u bir cihazın ana ekranına yükleme

POS'u bir ana ekran simgesi olarak yükleme, tarayıcı adres çubuğunu kaldırarak tam ekran deneyim, cihazda bir kısayol simgesi ve daha hızlı başlatma süreleri sunar.

### iPad (Safari)

1. Safari'yi açın ve mağazanızın POS URL'sine gidin: `https://yourstore.com/pos/`
2. Giriş yapın ve bu yeni bir cihaz ise başlangıç eşleme işlemini tamamlayın.
3. Safari araç çubuğundaki **Paylaş** butonuna (yukarı doğru ok olan kare) tıklayın.
4. Paylaş sayfasında aşağı kaydırın ve **Ana Ekran'a Ekle**'ye tıklayın.
5. İsterseniz ismi düzenleyin (varsayılan olarak "Spwig POS"'tir) ve **Ekle**'ye tıklayın.

POS simgesi artık iPad ana ekranınızda görünür. Tıkladığınızda, Safari tarayıcı çubuğu olmadan tam ekran olarak uygulama açılır.

> **Not:** iPad'deki Safari, "Ana Ekran'a Ekle" seçeneği için gereklidir. iOS'da üçüncü parti tarayıcılar (Chrome, Firefox) 2025'in ortasına kadar PWA kurulumunu desteklememektedir.

### Android (Chrome)

1. Chrome'u açın ve mağazanızın POS URL'sine gidin: `https://yourstore.com/pos/`
2. Giriş yapın ve gerekirse eşleme işlemini tamamlayın.
3. Sağ üstteki **üç nokta menüsüne** tıklayın ve **Uygulama'yı Kur** (ya da eski Chrome sürümlerinde **Ana Ekran'a Ekle**) seçeneğine tıklayın.
4. **Kur**'a tıklayarak onaylayın.

POS simgesi artık ana ekran ve uygulama menüsünde görünür. Simgeye tıklayarak uygulama tek başına açılır.

### Masaüstü (Chrome veya Edge)

1. Chrome veya Edge'de mağazanızın POS URL'sine gidin.
2. Tarayıcının adres çubuğunda **yükleme simgesini** arayın (bir bilgisayar monitörü ile aşağı doğru ok olan bir simge ya da versiyona göre bir '+' simgesi).
3. Alternatif olarak, **üç nokta menüsünü** açın ve **Spwig POS'u Kur** (Chrome) veya **Uygulamalar > Bu sitesi uygulama olarak kur** (Edge) seçeneğini seçin.
4. Kurulumu onaylayın.

POS, tarayıcı sekmesi veya adres çubuğu olmadan tek başına bir pencere olarak açılır. Sistem uygulama listesinde görünür ve görev çubuğuna sabitlenebilir.

## Uygulamanın güncellemesi nasıl yapılır

POS, kendi güncellemelerini Service Worker aracılığıyla yönetir. Uygulama mağazasına gitmeniz veya herhangi bir şeyi manuel olarak indirmeniz gerekmez.

**Güncelleme döngüsü:**

1.

POS'u her açtığınızda (veya sekme arka planda olduğunda aktif hale geldiğinde), Service Worker sunucuda yeni bir sürüm olup olmadığını kontrol eder.
2.

Yeni bir sürüm mevcutsa, Service Worker arka planda indirirken (çalışmaya devam ederken) mevcut oturumunuz kesilmez.
3.

Güncelleme, POS'u bir sonraki kez açtığınızda etkin olur.

Uygulama zaten açık ve senkronizasyon bekliyorsa, POS, yeniden yükleme hazır olduğunda sinyal vermeden önce kuyruğun boşalmasını bekler, böylece aktif bir vardiyayı senkronize edilmemiş satışlarla kesintiye uğratmaz.

**Satışlar bekliyorsa 'yeniden yükleme' ne anlama gelir** — bir güncelleme için yeniden yükleme istemi görürsen ve çevrimdışı satışların varsa, mevcut vardiyayı temiz bir şekilde kapat veya senkronizasyon banner'ı temizlenecek şekilde bekle, sonra yeniden yükle. Satışlar kuyruğunda iken yeniden yükleme onları silmez — yerel veritabanında kalmaya devam ederler — ancak önce senkronize etmek daha güvenlidir, böylece alınmış olduğundan emin olursunuz.

**Yüklenebilir sürümü kontrol etme** — POS'u açın, **menü simgesine** (üç yatay çizgi) dokunun ve **Ayarlar**'a gidin. Ayarlar panelinin alt kısmında mevcut inşaat sürümü gösterilir.

## Depolama ve kurulumun temizlenmesi

POS, yerel olarak birkaç tür veriyi depolar:

| Ne | Tipik boyut |
|----|-------------|
| Uygulama kabuğu (HTML, CSS, JS, ikonlar) | ~3–5 MB |
| Ürün kataloğu (metin ve meta veri) | Katalog boyutuna göre 1–10 MB |
| Ürün resimleri (önbelleğe alınmış) | Katalog boyutuna göre 5–50 MB |
| Sipariş geçmişi | 1–5 MB (500 sipariş) |
| Müşteri kayıtları | 1–3 MB (1.000 müşteri) |
| Bekleyen işlem kuyruğu | Minimum; senkronizasyon sırasında temizlenir |

**Cihazda depolama alanı azalırsa** — cihaz doluyken tarayıcılar önbellek depolamasına baskı uygular. POS, tarayıcı izin veriyorsa önbellekleri kalıcı olarak ayarlar, ancak çok dolu cihazlarda tarayıcı ürün resimlerini önce kaldırabilir. Eğer resimler yüklenemiyorsa, POS, bir sonraki senkronizasyon sırasında onları tekrar önbelleğe alır. Senkronize edilmiş satışlar ve uygulama kabuğu etkilenmez.

**Kurulumu sıfırlama** — POS beklenmedik şekilde davranıyorsa (eski bir sürümde sıkışmış, katalog yenilenmiyor, senkronizasyon kalıcı olarak sıkışmış), temiz bir sıfırlama yapabilirsiniz:

1. **Uygulamayı kaldırın** — mobil cihazda POS simgesini uzun süre basıp **Kaldır** veya **Kuruluğu Kaldır** seçeneğini seçin. Masaüstüde, uygulama penceresinin başlık çubuğuna sağ tıklayıp **Kuruluğu Kaldır** seçeneğini seçin.
2. Tarayıcıda doğrudan POS URL'sini açın ve tekrar oturum açın.
3. Cihaz, terminalin 8 karakterlik eşleştirme kodunu tekrar isteyecektir. Bu kodu **POS > POS Terminali**'nde bulabilir veya yeniden oluşturabilirsiniz — terminali açın ve **Eşleştirme Kodunu Yeniden Oluştur**'a tıklayın.
4. Yeni bir eşleştirme, tüm önbellek verilerinin tamamen yeniden senkronize edilmesine zorlar.

> **Sıfırlama sonrası**: sıfırlama öncesi kuyruktaki ancak henüz senkronize edilmemiş çevrimdışı satışlar kaybolur, çünkü yerel veritabanı temizlenir. Her zaman kurulumu sıfırlamadan önce bağlantının geri kazanılması ve senkronizasyon banner'ının temizlenmesi emin olun.

## Sorun Giderme

### POS eski bir sürümde sıkışmış

Servis Çalışanı yeni sürümü henüz etkinleştirmemiş olabilir. POS'u açık olan tüm tarayıcı sekmesini kapatıp tekrar açmayı deneyin. Sorun devam ederse, yukarıda açıklanan kurulum sıfırlamasını yapın.

### 'Bağlantı Yok' banner'ı temizlenmiyor

POS dışındaki cihazın internet erişimini kontrol edin (başka bir siteyi yükleyin). Eğer cihaz çevrimiçi ama banner hâlâ devam ediyorsa:

- POS sunucusu geçici olarak erişilebilir olmayabilir — bir dakika bekleyin ve POS otomatik olarak tekrar deneyecektir.
- Eğer ağınız bir oturum sayfası gerektiriyorsa (kaptif portal), yeni bir tarayıcı sekmesi açın, oturumu tamamlayın ve sonra POS'a geri dönün.

### POS'ta bir ürün, admin'de mevcut ama POS'ta yok

POS çevrimiçi iken her 5 dakikada bir ürünleri senkronize eder. Eğer admin'de çok yeni bir ürün eklediyseniz, **menü simgesine** tıklayıp **Ayarlar > Şimdi Senkronize Et**'e gidin, hemen bir senkronizasyon tetikleyin. Eğer ürün hâlâ görünmüyorsa, ürün ayarlarında **Aktif** olarak işaretlenmiş olduğundan ve POS kullanılabilirliği dışlanmamış olduğundan emin olun.

### Bekleyen işlemler 'Çakışma' durumunda sıkışmış

**POS > Ayarlar** (POS uygulaması içinde) ve **Bekleyen İşlemler** panelini kontrol edin.

Çakışan işlemler genellikle satışın çevrimdışı olarak yapılması ve senkronize edilmesi arasında ürün veya fiyatın değişmesiyle oluşur.

Satış detaylarını görüntüleyebilir ve satışın doğru şekilde alınmışsa, onu incelemiş olarak işaretleyebilirsiniz.

## İpuçları

- POS'u yerel Wi-Fi'ye bağlı kalan özel bir cihazda çalıştırın. Kısık Wi-Fi düşüşleri otomatik olarak işlenir, ancak uzun süre çevrimdışı kalan bir cihaz, tekrar çevrimiçi olduğunda daha fazla zaman alarak senkronize olur.
- Senkronizasyon aralıkları cihaz başına ayarlanır. Birden fazla terminaliniz varsa, her biri bağımsız olarak senkronize olur. Bir terminalde yapılan bir satış, senkronize olduğunda hemen admin panelinde görünür, ancak diğer terminalin yerel sipariş önbelleği yalnızca kendi senkronizasyon döngüsünde yenilenir.
- Planlı bir internet kesintisi (örneğin, Wi-Fi olmayan bir etkinliğe geçiş yapmak) öncesi, hâlâ bağlı olduğunuzda POS'u açın, böylece katalog ve stok verileri tamamen güncel olur. Nakit satışlar güvenilir şekilde kuyruğa alınır; yalnızca çevrimiçi olduğunuzda entegre kart ödemelerini kullanmaktan kaçının.
- Eğer bir etkinlikte yalnızca nakit satışlar yapacaksanız, Manuel kart ödemeleri yöntemi (kasa görevlisi tek başına bir terminalde işlem yapar ve referans girer) kart işlemleri için çevrimdışı olarak da çalışır.
- Uzun bir vardiyada cihazı şarjlı tutun — yerel veritabanı ve senkronizasyon süreci ekranla kıyaslandığında bataryaya büyük ölçüde etki etmez, ancak ticaret yapmak için şarjlı bir cihaz her zaman daha güvenlidir.