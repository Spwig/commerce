---
title: Platform Güncellemeleri
---

Spwig kurulumunuz, temalar, widget'lar, entegrasyonlar, sayfa inşaat öğeleri ve sağlayıcı bağlantıları gibi bileşenlerden oluşur — her biri kendi sürümü olan ve bağımsız olarak güncellenebilen bileşenler. Bileşen Kayıt Defteri, yüklenen her şeyin merkezi bir görünümünü sağlar, hangi bileşenlerin güncellemelerinin beklediğini gösterir ve herhangi bir zamanda güncellemeleri yüklemek veya geri almak için izin verir.

![Bileşen Kayıt Defteri Genel Bakış](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Bileşen Kayıt Defterini Anlamak

**Uzantılar > Bileşen Kayıt Defteri**'ne giderek mağazanızda yüklene bileşenleri görebilirsiniz. Her satır şu bilgileri gösterir:

- **Ad** — bileşenin görüntülenen adı
- **Tip** — bileşenin türü (tema, widget, entegrasyon vb.)
- **Mevcut Sürüm** — mağazanızda şu anda çalışan sürüm
- **Güncelleme Durumu** — bir güncelleme mevcut olup olmadığını gösterir
- **Kanal** — bileşenin takip ettiği güncelleme kanalı
- **Otomatik Güncelle** — güncellemelerin otomatik olarak yüklenip yüklenmeyeceğini gösterir
- **Kilitli** — bileşenin mevcut sürümünde donmuş olup olmadığını gösterir

Sayfa üstündeki panoda özet sayım bilgileri yer alır: toplam yüklene bileşen sayısı, güncellemelerin mevcut olduğu bileşen sayısı ve güncel olan bileşen sayısı.

### Bileşen Türleri

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
| Döviz Kuru Sağlayıcısı | Para birimi kuru veri kaynakları |
| Çeviri Sağlayıcısı | Yapay zeka çevirisi hizmetleri |
| Dil Paketi | Arayüz çeviri dosyaları |

## Güncellemeler Kanalı

Her bileşen, hangi sürümleri alacağına karar veren bir güncelleme kanalına takip eder. Risk toleransınızın ne kadar yüksek olduğuna göre her bileşeni farklı bir kanala atayabilirsiniz.

| Kanal | Açıklama | En iyi uygulandığı yer |
|---------|-------------|----------|
| **Stabil** | Üretim hazıры, dikkatle test edilmiş sürümler | Canlı mağazalardaki tüm bileşenler |
| **Beta** | Yeni özelliklerin stabil olana kadar test edilmesi için ön sürümler | Ön izlemek istediğiniz kritik olmayan bileşenler |
| **Geliştirme** | En son özellikleri, kararsız olabilir | Sadece test ortamlarında |
| **Güvenlik** | Sadece kritik güvenlik yamaları, en yüksek öncelikle teslim edilir | Güvenilirlik en önemli olan bileşenler |

Bir bileşenin kanalını değiştirmek için, adını tıklayarak detay görünümünü açın, ardından **Güncelleme Kanalı** alanına yeni bir değer seçin ve kaydedin.

## Güncellemeleri Kontrol Etme

Spwig, güncelleme sunucu ayarlarınızda yapılandırılan aralıklarla (varsayılan: her 24 saat) otomatik olarak güncellemeleri kontrol eder. Hemen kontrol etmek için:

1. **Uzantılar > Bileşen Kayıt Defteri**'ne gidin
2. Sayfa üstündeki **Güncellemeleri Kontrol Et** butonuna tıklayın
3. Sistem, Spwig güncelleme sunucusuna bağlanır ve tüm bileşenlerin güncellemesi durumunu yeniler
4. Mevcut güncellemeleri olan bileşenler vurgulanır ve **Mevcut Güncellemeler** sayısı güncellenir

Bir bileşen için güncellemeyi kontrol etmek için, listedeki eylem menüsünden **Güncellemeleri Kontrol Et** eylemini kullanabilirsiniz.

## Güncellemeleri Yükleme

### Tek bir bileşeni güncelleme

1. **Uzantılar > Bileşen Kayıt Defteri**'ne gidin
2. Güncellemesi istenen bileşeni bulun — güncellemesi mevcut bileşenlerin sürümü yanında bir güncelleme göstergesi gösterir
3. O bileşenin satırındaki **Güncelleme Yükle** butonuna tıklayın
4. Güncellemeyi onaylayın
5. Güncelleme indirilir, doğrulanır ve yüklenir — her aşamada ilerleme göstergesi gösterilir
6. Tamamlandıktan sonra bileşenin **Mevcut Sürüm** alanı yeni sürüm numarasına güncellenir

### Birden fazla bileşeni güncelleme

1.

Güncellemek istediğiniz bileşenlerin yanındaki onay kutularını seçin
2.



Yükseltmeler, bağımlılık sırasına göre yüklenir — diğer bileşenlerin bağımlı olduğu bileşenler önce güncellenir

### Yükseltme sırasında ne olur

Yükseltme işlemi şu aşamalardan geçer:

1. **Kontrol etme** — yükseltmenin mevcut olduğundan ve lisansınızın geçerli olduğundan emin olur
2. **İndirme** — Spwig yükseltme sunucusundan paketi alır
3. **Doğrulama** — paketin SHA-256 kontrol toplamına göre bütünlüğünü kontrol eder
4. **Çıkarma** — yeni dosyaları çıkarır
5. **Dağıtım** — yeni sürümü etkinleştirir
6. **Sağlık kontrolü** — yükseltme sonrası bileşenin çalışıp çalışmadığını doğrular

Herhangi bir aşama başarısız olursa, sistem otomatik olarak önceki sürümü geri yüklemeye çalışır.

## Platform seviyesindeki yükseltmeler

Bireysel bileşenlerin yanı sıra, Spwig platform seviyesindeki yükseltmeler alabilir ve bu yükseltmeler, veritabanı geçişlerini ve kısa bir bakım penceresini içeren daha kapsamlı bir süreçten geçer.

Platform yükseltme geçmişi, kayıt defterinin **Platform Yükseltmeleri** bölümünde görünür. Her girdi, sürüm geçişini (örneğin, `v1.3.2 → v1.3.3`), durumu ve yükseltme işleminin süresini gösterir.

Güvenlik yükseltmeleri ayrı ayrı işaretlenir ve güncelleme sunucu yapılandırmanızda **Güvenlik Yükseltmelerini Otomatik Yükle** seçeneği etkinse, elle müdahale olmadan otomatik olarak yüklenir.

## Sürüm geçmişini görüntüleme

Bir bileşenin önceki tüm yüklü sürümlerini görmek için:

1. Bileşen adını tıklayarak detay görünümünü açın
2. Sayfanın altındaki **Bileşen Sürümleri** bölümünü aşağıya kaydırın
3. Her sürüm girdisi, sürüm numarasını, yüklendiği zamanı, yükleme yöntemini ve sağlığı durumunu gösterir

Sistem, geri yükleme için son üç yüklü sürümü saklar. Bunların ötesindeki sürümler otomatik olarak silinir.

## Bir bileşeni geri yükleme

Bir yükseltme sorunlara neden olursa, önceki bir sürümü geri yükleyebilirsiniz:

1. Bileşenin detay görünümünü açın
2. Sayfanın altındaki **Geri Yükleme** bölümünü aşağıya kaydırın
3. Geri yüklemek istediğiniz sürümü seçin
4. **Bu Sürümü Geri Yükle**'ye tıklayın

Yalnızca **Geri Yükleme Mevcut** olarak işaretlenmiş sürümler geri yüklenir. Geri yükleme günlük girdisi, geri yükleme işlemini başlatan kişiyi ve zamanı kaydeder.

## Bileşenleri kilitleme

Bir bileşeni kilitlemek, otomatik yükseltmelerin bile yüklenmesini engeller. Belirli bir sürümü gerektiren özelleştirmeler veya entegrasyonlar olduğunda bu yararlıdır.

1. Bileşenin detay görünümünü açın
2. **Kilitle & Dondur** bölümünde **Kilitli** onay kutusunu işaretleyin
3. **Kilit Nedeni** alanına bir neden girin, ekibinizin neden kilitleendiğini anlayabilsin
4. Kaydınızı kaydedin

Kilitli bileşenler, kayıt defteri listesinde bir kilitleme göstergesiyle gösterilir. Kilidi kaldırmak için **Kilitli** onay kutusunu kaldırın ve kaydedin.

## Yükseltme günlüklerini okuma

Yükseltme günlüğü, her yükleme, yükseltme, geri yükleme ve sağlık kontrolü işlemiyle ilgili bilgileri kaydeder:

1. Bir bileşenin detay görünümünü açın
2. Sayfanın altında **Yükseltme Günlüğü** görünür
3. Her girdi, alınan eylemi, başlangıç ve bitiş saatlerini, eski ve yeni sürümleri, işlemin otomatik mi yoksa el ile mi yapıldığını ve işlem başarısız olursa oluşan hata mesajlarını gösterir

**Başarısız** durumlu günlük girdileri, sorun gidermeye yardımcı olmak için tam hata mesajını içerir.

## Otomatik yükseltmeleri etkinleştirme

Spwig'in yükseltmeleri otomatik olarak yüklemesine izin verebilirsiniz:

1. Bileşenin detay görünümünü açın
2. **Sürüm & Yükseltme Durumu** bölümünde **Otomatik Yükseltme** onay kutusunu işaretleyin
3. Kaydınızı kaydedin

Otomatik yükseltme etkinleştirildiğinde, sistem, sonraki planlanmış kontrol döngüsünde yükseltmeleri yükler. Güvenlik yükseltmeleri, bireysel bileşen ayarlarından bağımsız olarak, küresel **Güvenlik Yükseltmelerini Otomatik Yükle** ayarına göre işler.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- Her zaman temalar ve ödeme sağlayıcıları için **Stable** kanalında güncellemekten emin olun - bu bileşenler en çok müşteriyle etkileşimde bulunulan bileşenlerdir ve kararlılık en çok önemlidir
- Bir bileşeni özelleştirilmiş değişiklikler yapmadan önce kilitleyin ve nedeni açıkça kaydedin, gelecekteki ekip üyeleri bunun güncellenmesi gerektiğini bilmesi için
- Bir bileşenin sürüm girdisindeki **Yayın Notlarını** büyük bir sürüm artışı yapmadan önce inceleyin - kırılgan değişiklikler burada işaretlenir
- Bir güncelleme yaptıktan sonra mağazanızın etkilenen alanına gidin ve güncelleme tamamlandı deklare etmeden önce her şeyin beklenen şekilde görünmesini ve çalışmasını onaylayın
- Bir bileşen üzerinde otomatik güncelleme etkinse, otomatik güncellemelerin başarıyla tamamlandığından emin olmak için periyodik olarak **Güncelleme Günlüklerini** izleyin