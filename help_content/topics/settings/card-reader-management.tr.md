---
title: Kart Okuyucu Yönetimi
---

Kart okuyucu yönetimi, fiziksel ödeme donanım cihazlarını izler, bunları POS terminallerine atar ve operasyonel durumlarını izler. Her kart okuyucu, ödeme sağlayıcınızla kaydedilmiş fiziksel donanımı (Stripe S700, WisePOS E veya P400) temsil eder. Okuyucular, terminallerle birebir ilişkileri vardır - her kayıt, kendi özel kart okuyucuyla eşleşir. Okuyucu durumlarını (çevrimiçi, çevrimdışı, meşgul) gerçek zamanlı olarak izleyin, markanızla özelleştirilmiş splash ekranları oluşturun ve müşteri ödeme deneyimini etkileyebilecek bağlantı sorunlarını önceden giderin.

Kart okuyucu yönetimi, tüm konumlarda ödeme donanımının doğru şekilde yapılandırıldığını, atandığını ve çalıştığını sağlamak için kullanılır.

![Kart Okuyucu Listesi](/static/core/admin/img/help/card-reader-management/reader-list.webp)

## Kart Okuyucuları Anlamak

Kart okuyucular, kredi ve çek kartı ödemelerini işleyen fiziksel donanım cihazlardır:

**Donanım Bileşenleri**:
- EMV çip kart yuvası
- NFC anteni (kontak olmayan/tepkileme)
- Manyetik şerit okuyucu (eski, nadiren kullanılır)
- Ekran (tutar, PIN girmeyi isteyen, imza göstermeyi isteyen)
- Ağ bağlantısı (Wi-Fi veya Ethernet, modeline göre)

**Yazılım Entegrasyonu**:
- Okuyucular, Stripe Terminal API'sine bağlanır (bulut tabanlı, POS cihazına doğrudan bağlantı değil)
- POS terminali, API üzerinden ödeme isteği gönderir
- Stripe, isteği kayıtlı okuyucuya yönlendirir
- Okuyucu, kartı işler ve sonucu POS'a döndürür
- POS ve okuyucu arasında USB/Bluetooth bağlantısı gerekmez

**Bir Okuyucu Bir Terminal İçin**:
- Her POS terminalinin tam olarak bir atanan kart okuyucu olması gerekir
- Birebir ilişki, açık bir sorumluluk ve basitleştirilmiş sorun giderme sağlar
- Birden fazla terminalin bir okuyucuyu paylaşması (çakışmaya neden olur) mümkün değildir

## Kart Okuyucu Türleri

Spwig POS, Stripe Terminal kart okuyucularını destekler:

**BBPOS WisePOS E** (`bbpos_wisepos_e`):
- 5" renkli dokunmatik ekranlı tümleşik Android terminal
- Yazdırma seçeneği (termal fatura)
- En iyi kullanım: Tam özellikli perakende ödeme, restoranlar (renkli ekran üzerinde ipucu istemleri)
- Bağlantı: Sadece Wi-Fi
- Splash ekranı: Renkli 480×800 portre

**Stripe Reader S700** (`stripe_s700`):
- Monokrom LCD'li masa üstü okuyucu
- Küçük boyutlu, suya dayanıklı
- En iyi kullanım: Standart perakende, kompakt ödeme masaları
- Bağlantı: Wi-Fi veya Ethernet
- Splash ekranı: Monokrom 480×800 portre

**Verifone P400** (`verifone_p400`):
- Eski masa üstü okuyucu (eski model)
- Hâlâ destekleniyor ancak yeni dağıtımlar için önerilmiyor
- En iyi kullanım: Mevcut dağıtımlar (çalışan donanımı değiştirmeyin)
- Bağlantı: Wi-Fi veya Ethernet
- Splash ekranı: Monokrom 480×800 portre

**Gelecekteki Uyumluluk**:
- Stripe Terminal donanım tekliflerini genişlettiğinde ek okuyucu modelleri eklenebilir
- Okuyucu türü açılır menüsü, sağlayıcı yeteneklerinden otomatik olarak doldurulur

## Okuyucu Kayıt Akışı

**Adım 1: Donanımı Satın Alın ve Alın**
- Stripe (stripe.com/terminal) veya yetkili satıcıdan okuyucu satın alın
- Okuyucuyu açın ve güç verin
- Wi-Fi ağına bağlanın (okuyucunun ekranında gösterilen kurulumu takip edin)

**Adım 2: Stripe Dashboard'da Kaydolun**
- **Stripe Dashboard > Terminal > Okuyucular**'a gidin
- **Yeni Okuyucu Kaydet**'e tıklayın
- Ekranında eşleştirme işlemini takip edin (okuyucu, kayıt kodunu görüntüler)
- Okuyucuyu Stripe Konumu'na atayın (konum, ödeme sağlayıcı yapılandırmasıyla eşleşmelidir)
- **Okuyucu Kimliği**'ni not alın (gibi görünür `tmr_ABC123...`)

**Adım 3: Spwig'a Senkronize Olun (Otomatik)**
- Spwig, Stripe konumunuza kaydedilmiş okuyucuları otomatik olarak keşfeder
- Arka plan işi her 30 dakikada bir senkronize olur
- Yeni okuyucular, **POS > Kart Okuyucuları** listesinde 30 dakika içinde görünür

**Adım 4: Terminal'e Atayın (Manuel)**
- **POS > Kart Okuyucuları**'na gidin
- Listede yeni keşfedilen okuyucuyu bulun
- Düzenleme için tıklayın
- Atayacağınız terminali seçin
- Kaydedin

**Adım 5: Ödeme Testi**
- POS terminalinde test işlemi yapın
- Kart ödeme yöntemi seçin
- POS, atanan okuyucuyu keşfetmelidir
- Stripe test kartını (4242 4242 4242 4242) kullanarak testi tamamlayın
- Ödemenin başarıyla tamamlandığını doğrulayın

Okuyucu test sırasında görünmüyorsa, terminal atamasını ve okuyucu durumunu kontrol edin.

## Okuyucu Durumu İzleme

Okuyucular, Stripe Terminal API'sine durumu rapor eder, Spwig her 5 dakikada bir senkronize eder:

**Çevrimiçi** (yeşil) - Okuyucu, açıktır, ağ bağlantısı vardır ve ödemeleri kabul etmeye hazırdır

**Çevrimdışı** (kırmızı) - Okuyucu kapalıdır, ağdan ayrılıştır veya erişilebilir değildir

**Meşgul** (sarı) - Okuyucu şu anda bir ödeme işlemi işliyor

**Son Görüntülenme** - Okuyucunun Stripe API ile en son bağlantı zaman damgası
- Okuyucu çevrimiçi iken ~2 dakikada bir güncellenir
- Bağlantı sorunlarını tanılamak için kullanışlıdır ("okuyucu 3 saat önce çevrimdışı oldu" = iş saatleri sırasında güç veya ağ sorunu)

**Durum Kullanım Durumları**:
- **Açma öncesi kontrolü**: Mağazanızdaki tüm okuyucuların çevrimiçi olduğundan emin olun, kapıları açmadan önce
- **Sorun giderme**: "Kayıt 3 kartları kabul etmiyor" → Okuyucu durumunu kontrol edin → Çevrimdışı gösterir → Güç/ağ kontrolü
- **Denetim**: "Dünkü Terminal 5'de ödemeler işlendi mi?" → Son görüntülenme zaman damgasını kontrol edin

## Terminal Ataması

Kart okuyucuları, terminallerle **birebir ilişki** kullanır:

**Atama Neden Önemlidir**:
- Ödeme sırasında, POS hangi okuyucuyla iletişim kuracağını bilmelidir
- Bir okuyucunun birden fazla terminal tarafından paylaşılması çakışmaya neden olur (iki kasir aynı okuyucuyu aynı anda kullanamaz)
- Atanmamış okuyucular kullanılamaz (boş donanım)

**Atama Kuralları**:
- Her terminalin **tam olarak bir** kart okuyucu ataması olabilir
- Her kart okuyucunun **tam olarak bir** terminal ataması olabilir
- Okuyucu Terminal A'ya atandığında, önceki terminalden otomatik olarak kaldırılır

**Atamaları Değiştirme**:
- Okuyucu kaydını düzenle
- **Terminal** alanını yeni terminal olarak değiştir
- Kaydet
- Önceki terminal kart okuyucu atamasını kaybeder (ödeme sırasında "Hiçbir okuyucu atanmamış" hatası gösterir)

**Atanmamış Okuyucular**:
- Yeni keşfedilen okuyucular atanmamış olarak başlar
- Atanmamış okuyucular listede görünür ancak kullanılamaz
- Aktif hale getirmek için terminal atayın

## Splash Ekranı Özelleştirmesi

Okuyucu splash ekranları, boşta iken müşteri odaklı ekran üzerinde marka bilgilerini görüntüler:

**Splash Ekranı Nedir?**
- Ödeme işlemi yapmadığında okuyucunun ekranında gösterilen bir görsel
- Varsayılan Stripe logolarını marka bilgilerinizle değiştirir
- Müşterilerin ödeme sırasında bekleme ekranında görünür

**Otomatik Oluşturulmuş vs. Özelleştirilmiş**:

**Otomatik Oluşturulmuş** (varsayılan):
- Spwig, mağazanızın logolarından splash ekranı oluşturur (mağaza ayarlarında logo yapılandırılmışsa)
- Otomatik olarak okuyucu belirtilerine uygun şekilde boyutlandırılır (480×800 portre)
- S700/P400 için monokrom, WisePOS E için renkli
- Yapılandırma gerekmez

**Özelleştirilmiş Splash** (ileri düzey):
- Kendi özelleştirilmiş splash ekranı görselinizi yükleyin
- Tasarım ve marka bilgileri üzerinde tam kontrol
- Görsel gereksinimlerini karşılamalıdır (aşağıdaki bölümü görün)

**Özelleştirilmiş Splash Gereksinimleri**:
- **Çözünürlük**: Tam olarak 480×800 piksel (portre yönünde)
- **Format**: PNG veya JPG
- **S700/P400**: Sadece monokrom (siyah ve beyaz, gri yok)
- **WisePOS E**: Tam renk desteklenir
- **Dosya boyutu**: <200KB

**Özelleştirilmiş Splash Ayarlama**:
1. Kart okuyucu kaydını düzenle
2. **Splash Görseli Üzerine Yaz** alanına görsel yükle (veya Medya Kütüphanesinden seçin)
3. Kaydet
4. Splash, okuyucuya 5 dakika içinde senkronize olur

**Özelleştirilmiş Splash Kaldırma**:
- **Splash Görseli Üzerine Yaz** alanını temizleyin
- Kaydet
- Okuyucu, otomatik olarak oluşturulan splash'a döner (veya Stripe varsayılanına, mağaza logosu yoksa)

**Splash Testi**:
- Yükleme sonrası, 5 dakika senkronizasyon için bekleyin
- Okuyucu cihazını ziyaret edin
- Splash, boşta ekranında görünmeli
- Görsel kalitesini, merkezlenmesini ve kontrastını kontrol edin

## Stripe Splash Ayarı

Arka planda, Spwig Stripe Terminal splash ekranı yapılandırmasını yönetir:

**stripe_splash_file_id** - Stripe tarafından yüklenecek splash görseli için iç ID
- Splash yüklendiğinde otomatik olarak ayarlanır
- Stripe API'sinde splash'ı referanslamak için kullanılır

**stripe_splash_config_id** - Stripe tarafından splash yapılandırması için iç ID
- Splash dosyasını okuyucuya bağlar
- Okuyucuya splash atandığında otomatik olarak yönetilir

Bu alanlar salt okunur ve otomatik olarak yönetilir - doğrudan onlarla etkileşimde bulunmanıza gerek yoktur.

## Yaygın Sorunların Giderilmesi

**Sorun 1: Okuyucu çevrimdışı gösteriliyor ama açık**
- **Nedenleri**: Ağ bağlantısı sorunu, Wi-Fi şifresi değiştirildi, okuyucu aralık dışında
- **Çözüm**: Okuyucunun ağ ayarlarını kontrol edin, Wi-Fi'ye yeniden bağlanın, Stripe API'nin ağdan erişilebilir olduğundan emin olun

**Sorun 2: Ödeme sırasında POS "Hiçbir okuyucu atanmamış" diyor**
- **Neden**: Okuyucu terminal atamasız veya atama tamamlanmamış
- **Çözüm**: Okuyucuyu düzenleyin, terminal atayın, kaydedin, ödeme testini tekrarlayın

**Sorun 3: Okuyucu sürekli meşgul (ödeme ekranında sıkışmış)**
- **Neden**: İşlem zaman aşımına uğradı veya çöktü, okuyucu durumu sıfırlanmadı
- **Çözüm**: Okuyucuyu yeniden başlatın (güç döngüsü), devam ederse Stripe destek ile iletişime geçin

**Sorun 4: Özelleştirilmiş splash görünmüyor**
- **Nedenleri**: Görsel çözünürlüğü yanlış, senkronizasyon henüz tamamlanmadı, monokrom gereksinimi karşılanmadı (S700/P400)
- **Çözüm**: Görselin tam olarak 480×800 olduğunu doğrulayın, 5 dakika senkronizasyon için bekleyin, renksiz okuyucular için monokrom olduğundan emin olun

**Sorun 5: Stripe'da kaydedilmiş okuyucu Spwig'da görünmüyor**
- **Neden**: Okuyucu, sağlayıcı yapılandırmasıyla farklı bir Stripe konumuna kaydedildi
- **Çözüm**: Stripe Dashboard'da, okuyucunun konumu sağlayıcının konum ID'siyle eşleştiğinden emin olun

## İpuçları

- **Bir okuyucu bir terminal için** - Terminaller arasında okuyucuları paylaşmayın; çakışmaları önler ve sorumlulukları basitleştirir
- **Okuyucuları zemine koyduktan önce Stripe'da kaydedin** - Okuyucuyu ödeme masasına koyduğunuzdan önce Stripe kaydı ve Spwig atamasını tamamlayın
- **Mağazada splash ekranlarını test edin** - Kontrast, okuyucu modeline ve aydınlatmaya göre değişebilir; splash'ın gerçek ortamda iyi göründüğünden emin olun
- **Açma öncesi durumu izleyin** - Her sabah, mağaza açılmadan önce tüm okuyucuların çevrimiçi olduğundan emin olun
- **Donanımı fiziksel olarak etiketleyin** - Terminal adı ile okuyucuyu etiketleyin ("Terminal 1 Okuyucu") sorun giderme sırasında kolayca tanımlanması için
- **Okuyucuları kesintisiz güçle besleyin** - İş sırasında elektrik kesintisi okuyucu durumunu bozabilir; UPS önerilir
- **Okuyucu seri numaralarını belgeleyin** - Garanti ve destek için seri numaraları kaydedin (okuyucu donanım etiketinde bulunur)
- **Okuyucu firmware güncellemelerini yapın** - Stripe firmware güncellemelerini otomatik olarak gönderir, ancak periyodik olarak okuyucuların en son sürümde olduğundan emin olun (Stripe Dashboard'ı kontrol edin)