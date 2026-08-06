---
title: Platform Güncellemeleri
---

Spwig kurulumunuz, temalar, widget'lar, entegrasyonlar, sayfa inşaat öğeleri ve sağlayıcı bağlantıları gibi bileşenlerden oluşur — her biri kendi sürümü olan ve bağımsız olarak güncellenebilen bileşenler. Bileşen Kayıt Defteri, yüklenen her şeyin merkezi bir görünümünü sağlar, hangi bileşenlerin güncellemelerinin beklediğini gösterir ve herhangi bir zamanda güncellemeleri yüklemek veya geri almak için izin verir.

![Bileşen Kayıt Defteri Genel Bakış](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Bileşen Kayıt Defterini Anlamak

**Sistem Panosu > Bileşen Güncellemeleri**'ne giderek mağazanızda yüklenebilecek her bileşeni görebilirsiniz. Her satır şu bilgileri gösterir:

- **Ad** — bileşenin görüntülenecek adı
- **Tip** — bileşenin türü (tema, widget, entegrasyon vb.)
- **Mevcut Sürüm** — mağazanızda şu anda çalışan sürüm
- **Güncelleme Durumu** — bir güncelleme mevcut olup olmadığını gösterir
- **Kanal** — bileşenin takip ettiği güncelleme kanalı
- **Otomatik Güncelle** — güncellemelerin otomatik olarak yüklenebilir olup olmadığını gösterir
- **Kilitli** — bileşenin mevcut sürümünde donmuş olup olmadığını gösterir

Sayfa üstündeki panoda özet sayım bilgileri yer alır: toplam yüklenebilecek bileşen sayısı, güncellemelerin mevcut olduğu bileşen sayısı ve güncel olan bileşen sayısı.

### Bileşen Tipleri

| Tip | Ne olduğunu açıklar |
|------|------------|
| Tema | Mağazanızın görsel tasarımı |
| Widget | Yeniden kullanılabilir sayfa inşaat blokları |
| Sayfa İnşaat Öğesi | Sayfa inşaatı için özel öğeler |
| Sayfa İnşaat Aracı | Düzenleyici araçları ve yardımcı programlar |
| Başlık / Alt Bilgi Şablonu | Başlık ve alt bilgi düzenleri |
| Kargo Sağlayıcısı | Taşıyıcı entegrasyonları (FedEx, UPS vb.) |
| E-posta Sağlayıcısı | E-posta teslim hizmetleri |
| Ödeme Sağlayıcısı | Ödeme ağ geçidi entegrasyonları |
| Döviz Kuru Sağlayıcısı | Döviz kuru veri kaynakları |
| Çeviri Sağlayıcısı | Yapay zeka çevirisi hizmetleri |
| Dil Paketi | Arayüz çeviri dosyaları |

## Güncellemeler Kanalı

Her bileşen, hangi sürümleri alacağına karar veren bir güncelleme kanalına takip eder. Risk toleransınızın ne kadar yüksek olduğuna göre her bileşeni farklı bir kanala atayabilirsiniz.

| Kanal | Açıklama | En iyi uygunluk |
|---------|-------------|----------|
| **Stabil** | Üretim hazırlığı, dikkatlice test edilmiş sürümler | Canlı mağazalardaki tüm bileşenler |
| **Beta** | Yeni özelliklerin stabil olana kadar test edilmesi için ön sürümler | Ön izlemek istediğiniz kritik olmayan bileşenler |
| **Geliştirme** | En son özellikleri, kararsız olabilir | Sadece test ortamları |
| **Güvenlik** | Sadece kritik güvenlik yamaları, en yüksek öncelikle teslim edilir | Güvenilirlik en önemli olan bileşenler |

Bir bileşenin kanalını değiştirmek için, adını tıklayarak detay görünümünü açın, ardından **Güncelleme Kanalı** alanına yeni bir değer seçin ve kaydedin.

## Güncellemeleri Kontrol Etme

Spwig, güncelleme sunucusu ayarlarında yapılandırılan aralıklarla (varsayılan: her 24 saat) otomatik olarak güncellemeleri kontrol eder. Hemen kontrol etmek için:

1. **Sistem Panosu > Bileşen Güncellemeleri**'ne gidin
2. Sayfa üstündeki **Güncellemeleri Kontrol Et** butonuna tıklayın
3. Sistem, Spwig güncellemesi sunucusu ile iletişime geçer ve tüm bileşenlerin güncellemesi durumunu yeniler
4. Mevcut güncellemeleri olan bileşenler vurgulanır ve **Mevcut Güncellemeler** sayacı güncellenir

Bir bileşen için güncellemeyi kontrol etmek için, listedeki eylem menüsünden **Güncellemeleri Kontrol Et** eylemini kullanabilirsiniz.

## Güncellemeleri Yükleme

### Tek Bileşeni Güncellemek

1. **Sistem Panosu > Bileşen Güncellemeleri**'ne gidin
2. Güncellemek istediğiniz bileşeni bulun — mevcut güncellemeleri olan bileşenlerin sürümü yanında bir güncelleme göstergesi vardır
3. O bileşenin satırındaki **Güncelleme Yükle** butonuna tıklayın
4. Güncellemeyi onaylayın
5. Güncellemesi indirilir, doğrulanır ve yüklenir — her aşamada ilerleme göstergesi gösterilir
6. Tamamlandıktan sonra bileşenin **Mevcut Sürüm** alanı yeni sürüm numarasına güncellenir

### Birden Fazla Bileşeni Güncellemek

1.

Güncellemek istediğiniz bileşenlerin yanındaki onay kutularını seçin
2.


Yükleme güncellemelerini **Yükleme güncellemelerini seçin** menüsünden **Eylem** açılır menüsünden seçin
3.

**Devam et**'e tıklayın
4.

Güncellemeler, bağımlılık sırasına göre yüklenecek — diğer bileşenlerin bağımlı olduğu bileşenler önce güncellenir

### Bir güncelleme sırasında ne olur

Güncelleme işlemi şu aşamalardan geçer:

1. **Kontrol etme** — güncellemenin mevcut olduğundan ve lisansınızın geçerli olduğundan emin olur
2. **İndirme** — Spwig güncelleme sunucusundan paketi alır
3. **Doğrulama** — paketin SHA-256 kontrol toplamına göre bütünlüğünü kontrol eder
4. **Çıkarma** — yeni dosyaları çıkarır
5. **Dağıtım** — yeni sürümü etkinleştirir
6. **Sağlık kontrolü** — güncelleme sonrası bileşenin çalışıp çalışmadığını doğrular

Herhangi bir aşama başarısız olursa, sistem otomatik olarak önceki sürümü geri yüklemeye çalışır.

## Platform seviyesindeki güncellemeler

Bireysel bileşenlerin yanı sıra, Spwig platform seviyesindeki güncellemeler alabilir ve bu güncellemeler, çekirdek mağaza motorunu güncelleyebilir. Bu güncellemeler, veritabanı geçişleri ve kısa bir bakım penceresi dahil daha kapsamlı bir süreçten geçer.

**Sistem Panosu > Platform Güncellemeleri**'ne giderek bireysel bileşenlerden ayrı olarak platform seviyesindeki güncellemeleri görüntüleyebilir ve yönetebilirsiniz.

### Yüklemeden önce ne yeni geldiğini inceleme

**Güncellemeleri Kontrol Et**'e tıklayarak yeni bir platform sürümünün mevcut olup olmadığını kontrol edin. Bir sürüm bulunursa, **Yükleme Hazır** kartı sürüm değişikliğini (örneğin, `v1.7.0 → v1.7.1`), **Paket Boyutu**, **Tahmini Süre**, ve güncelleme **Kanali**'nı — ve **Ne Yeni** önizlemesini gösterir, böylece yükleme kararınızdan önce ne değiştiğini görebilirsiniz:

- Yayınlama hakkında kısa bir açıklama satırı
- O sürümdeki en önemli değişikliklerin bir madde listesi (en fazla beş tane, daha fazla değişiklik varsa bir not ile)

Eğer güncelleme veritabanı şemasını değiştirirse, **Veritabanı geçişleri gerekir** uyarısı ve tahmini süre görünür. Güvenlik sürümleri, **Güvenlik güncelleme** etiketiyle birlikte hemen yükleme önerir. Yüklemeden önce **Ne Yeni** önizlemesini okuyun — bu, bir sürümün ekstra dikkat gerektiren herhangi bir şeyi (örneğin, yükseltme tamamlandıktan sonra çağrılan adımlar) hızlıca görmek için en hızlı yoldur.

Platform güncelleme geçmişi sayfanın daha aşağısında görünür. Her girdi sürüm geçişini (örneğin, `v1.3.2 → v1.3.3`), durumu ve güncelleme işleminin süresini gösterir.

Güvenlik güncellemeleri ayrı ayrı işaretlenir ve, **Güvenlik Güncellemelerini Otomatik Yükle** seçeneği, güncelleme sunucu yapılandırmanızda etkinse, elle müdahale olmadan otomatik olarak yüklenir.

## Sürüm geçmişini görüntüleme

Bir bileşenin önceki tüm yüklü sürümlerini görmek için:

1. Bileşen adını tıklayarak detay görünümünü açın
2. Sayfanın altındaki **Bileşen Sürümleri** bölümünü aşağıya kaydırın
3. Her sürüm girdisi sürüm numarasını, ne zaman yüklendiğini, yükleme yöntemini ve sağlığı durumunu gösterir

Sistem, son üç yüklü sürümü geri dönüş için saklar. Bu sürümlerden daha eski olanlar otomatik olarak silinir.

## Bir bileşeni geri döndürme

Bir güncelleme sorunlara neden olursa, önceki bir sürümde geri dönebilirsiniz:

1. Bileşenin detay görünümünü açın
2. Sayfanın altındaki **Geri Dönüş** bölümünü aşağıya kaydırın
3. Geri dönmek istediğiniz sürümü seçin
4. **Bu Sürümde Geri Dön**'e tıklayın

Yalnızca **Geri Dönüş Mevcut** olarak işaretlenmiş sürümler geri yüklenilebilir. Geri dönüş log girdisi, geri dönüşü başlatan kişiyi ve ne zaman yapıldığını kaydeder.

## Bileşenleri kilitleme

Bir bileşeni kilitlemek, otomatik güncellemeler dahil herhangi bir güncellemenin yüklenebilmesini engeller. Bu, özel bir sürüm üzerinde bağımlılıklarınız veya entegrasyonlarınız olduğunda faydalıdır.

1. Bileşenin detay görünümünü açın
2. **Kilit & Dondur** bölümünde **Kilitli** onay kutusunu işaretleyin
3. **Kilit Nedeni** alanına bir neden girin, ekibinizin neden kilitleendiğini anlayabilsin
4. Kaydınızı kaydedin

Kilitli bileşenler, kayıt listesinde bir kilitleme göstergesiyle gösterilir. Kilidi kaldırmak için **Kilitli** onay kutusunu kaldırın ve kaydedin.

## Güncellemeleri okuma günlükleri

Güncelleme günlüğü, her yükleme, güncelleme, geri dönüş ve sağlık kontrolü işlemi kaydeder:

1.

Bileşenin detay görünümünü açın
2.

**Güncelleme Günlüğü** sayfanın alt kısmında inline olarak görünür
3.



Her girdi, alınan eylemi, başlangıç ve bitiş saatlerini, eski ve yeni sürümleri, otomatik ya da el ile olup olmadığını ve işlem başarısız olursa herhangi bir hata mesajını gösterir.

**Başarısız** durumlu log girdileri, sorun gidermeye yardımcı olmak için tam hata mesajını içerir.

## Otomatik güncellemeyi etkinleştirme

Spwig'in güncellemeleri otomatik olarak yüklemesine izin verebilirsiniz:

1. Komponentin detay görünümünü açın
2. **Sürüm & Güncellemeler Durumu** bölümünde **Otomatik Güncelle**'yi işaretleyin
3. Kaydı kaydedin

Otomatik güncelleme etkinse, sistem bir sonraki planlanan kontrol döngüsünde güncellemeleri yükler. Güvenlik güncellemeleri, bireysel komponent ayarlarından bağımsız olarak küresel **Güvenlik Güncellemelerini Otomatik Yükle** ayarına göre uygulanır.

## İpuçları

- Temalar ve ödeme sağlayıcıları için her zaman **Stable** kanalında güncellemeyi yapın — bu en çok müşteriyle etkileşimde bulunan bileşenlerdir ve kararlılık en çok önemlidir
- Bir komponenti özelleştirme yapmadan önce kilitleyin ve nedeni açıkça kaydedin, böylece gelecekteki ekip üyeleri bunun güncellenmesi gerektiğini bilir
- Bir büyük sürüm yükseltmesi yüklemeye başlamadan önce komponentin sürüm girdisindeki **Yayın Notlarını** inceleyin — kırıcı değişiklikler burada işaretlenir
- Platform güncellemesi yüklemeye başlamadan önce **Platform Güncellemeleri** sayfasındaki **Yeni Neler Var** önizlemesini okuyun — yayın notlarını tam olarak görmek ve gereken ek adımları öğrenmek için **Sistem Güncellemesi** sayfasına gidin
- Bir güncelleme yaptıktan sonra mağazanızın etkilenen alanına gidin ve güncellemenin tamamlandığını ilan etmeden önce her şeyin beklenen şekilde görünüp çalıştığını onaylayın
- Bir komponente otomatik güncelleme etkinse, otomatik güncellemelerin başarıyla tamamlandığından emin olmak için periyodik olarak **Güncelleme Günlüklerini** izleyin