---
title: Yükleme Kılavuzu
---

Bu kılavuz, Spwig'i kendi sunucunuzda nasıl yükleyeceğinizi adım adım anlamanızı sağlar. Tüm süreç otomatikleştirilmiştir — tek bir komut, Docker kurulumunu, veritabanı oluşturma, hizmet yapılandırması ve SSL sertifikalarını işler.

## Başlamadan Önce

İhtiyacınız olanlar:

- **Ubuntu 22.04 veya 24.04** çalıştıran bir sunucu (Debian 12 de desteklenir)
- Sunucuya **root veya sudo erişimi**
- En az **4 GB RAM** ve **20 GB disk alanı** (8 GB RAM önerilir)
- Spwig alımınızdan alınan **lisans tokenı** (e-posta faturasını kontrol edin)
- Opsiyonel olarak, sunucunuzun IP adresine yönlendirilen bir **alan adı**

> **İpucu:** Alan adı olmadan da kurulum yapabilir ve daha sonra alan adı yapılandırma aracıyla ekleyebilirsiniz. Bu süre zarfında mağazanıza sunucunuzun IP adresi üzerinden erişilebilir olacak.

## Kurulum Aracı'nı Çalıştırma

Sunucunuza SSH ile bağlanın ve alım onayı e-postasından kurulum komutunu çalıştırın. Komut şu şekilde görünür:

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash -s -- --token YOUR_LICENSE_TOKEN
```

`YOUR_LICENSE_TOKEN` ifadesini e-postanızdaki token ile değiştirin.

Kurulum aracı otomatik olarak sekiz aşamadan geçer:

1. **Ön kontrol** — sunucunuzun gereksinimleri karşılayıp karşılamadığını kontrol eder (OS, disk, RAM, bağlantı noktaları)
2. **Token doğrulama** — lisansınızı doğrular ve mağazanızın yapılandırmasını çıkarır
3. **Mod tespiti** — sunucunuz için en iyi kurulum modunu belirler (aşağıya bakın)
4. **Yapılandırma** — güvenli şifreler, veritabanı kimlik bilgileri ve hizmet yapılandırması oluşturur
5. **Görüntü indirme** — Spwig uygulama görüntülerini registry'den çeker
6. **Hizmet başlatma** — sırayla veritabanı, önbellek, uygulama ve arka plan çalışanlarını başlatır
7. **SSL kurulumu** — alan adınız yapılandırılmışsa bir SSL sertifikası alır
8. **Sonlandırma** — yönetici hesabınızı oluşturur ve kullanışlı komut dosyaları oluşturur

İnternet hızına bağlı olarak süreç 5–15 dakika sürer.

## Kurulum Modları

Kurulum aracı sunucu ortamınızı otomatik olarak tespit eder ve en uygun modu seçer. Ayrıca `--mode` bayrağıyla manuel olarak birini belirtebilirsiniz.

### Tekil Mod

**En iyi durum:** Spwig'in tek web uygulaması olduğu dedikod sunucuları ve VPS örnekleri için.

- 80 ve 443 bağlantı noktalarını doğrudan kullanır
- Let's Encrypt aracılığıyla SSL sertifikalarını otomatik olarak yönetir
- Bu en yaygın ve önerilen moddur

### Yan Ekip Modu

**En iyi durum:** 80/443 bağlantı noktalarında zaten başka bir web uygulaması (WordPress, şirket web sitesi vb.) çalışan sunucular için.

- Spwig başka bir bağlantı noktasında çalışır (otomatik olarak tespit edilir, genellikle 8080 veya 8443)
- Kurulum aracı mevcut web sunucunuzda eklemek üzere bir nginx proxy yapılandırması oluşturur
- Mevcut web sunucunuz SSL'yi yönetir ve trafiği Spwig'e yönlendirir

### Yerel Mod

**En iyi durum:** Kendi bilgisayarınızda geliştirme ve test için.

- Sadece `localhost` veya `127.0.0.1` adresinden erişilebilir
- Kendi imzalı bir SSL sertifikası kullanır (tarayıcınızda güvenlik uyarısı görünecek — bu normaldir)
- Hata ayıklama özellikleri etkinleştirilir
- Lisans doğrulaması gerekmez

## Kurulum Sürecinde Ne Olur

### Docker

Docker zaten yüklü değilse, kurulum aracı bunu sizin için kurmaya teklif eder. Spwig, Docker konteynerleri içinde tamamen çalışır — Docker dışındaki sunucu işletim sisteminde hiçbir şey doğrudan yüklenmez.

### Oluşturulan Hizmetler

Kurulum aracı şu hizmetleri oluşturur:

| Hizmet | Amacı |
|---------|---------|
| **Veritabanı** (PostgreSQL 16) | Mağazanızın tüm verilerini saklar — ürünler, siparişler, müşteriler, ayarlar |
| **Önbellek** (Redis) | Sayfa yükleme hızını artırır ve arka plan görev kuyruklarını yönetir |
| **Bağlantı havuzu** (PgBouncer) | Veritabanı bağlantılarını verimli şekilde yönetir |
| **Nesne depolama** (MinIO) | Yüklenecek görüntüler, dosyalar ve medya depolanır |
| **Uygulama** (Spwig) | Mağaza kendisi — yönetici paneli ve mağaza ön yüzü |
| **Web sunucusu** (Nginx) | Basınç ve önbellekleme ile ziyaretçilerinize mağazanızı sunar |
| **Arka plan çalışanı** (Celery) | E-postalar, çeviriler, analizler ve diğer arka plan görevlerini işler |
| **Görev planlayıcısı** (Celery Beat) | Otomatik yedekleme ve e-posta kampanyaları gibi planlanmış görevleri çalıştırır |
| **Çevirmen** | Çok dilli mağazalar için yapay zeka destekli çeviri hizmeti |
| **Güncelleyici** | Spwig pazar yerinden bileşen güncellemelerini yönetir |

### Yönetici hesabı

Yükleme sonunda, bir yönetici hesabı oluşturmanız istenir. Bu hesap, mağazanızın yönetici paneline giriş yapmak için kullanacağınız hesaptır.

### Bakım modu

Mağazanız **bakım modunda** başlar — ziyaretçiler "Yakında" sayfasını görür. Bu, mağazanızı canlıya çıkarmadan önce (ürün ekleme, ödeme yöntemlerini ayarlama, tema kişiselleştirme) yapılandırmak için zaman sağlar.

Hazır olduğunuzda, kurulum sırasında oluşturulan kolaylık betiğini çalıştırın:

```bash
./go-live.sh
```

Ya da **Yönetici > Mağaza Ayarları > Bakım** üzerinden bakımı kapatın.

## Kurulum sonrası

Kurulum tamamlandığında, aşağıdaki özetle karşılaşacaksınız:

- Mağazanızın URL'si
- Yönetici panelinizin URL'si (genellikle `https://yourdomain.com/en/admin/`)
- Yapılandırma dosyalarının konumu
- Kullanılabilir kolaylık betikleri

### Kolaylık betikleri

Kurulum dizininizde bu betikler oluşturulur:

- **`./go-live.sh`** — mağazanızı bakım modundan çıkarır
- **`./configure-domain.sh`** — alan adınızı ekler veya değiştirir ve SSL sertifikası alır

### Bir sonraki adımlar

1. Yönetici panelinize giriş yapın
2. **Kurulum Sihirbazı'nı** tamamlayın — mağaza adı, para birimi, saat dilimi ve temel ayarlar için size kılavuzluk eder
3. Ürünlerinizi ekleyin
4. Ödeme yönteminizi yapılandırın
5. Bir tema seçin ve kişiselleştirin
6. Hazır olduğunuzda `./go-live.sh` komutunu çalıştırın

## Bulut pazar yerlerinde kurulum

Spwig, birkaç bulut sağlayıcısında tek tıklamayla uygulama olarak mevcuttur:

- **DigitalOcean** — DigitalOcean Pazar Yerinden dağıtın
- **Akamai (Linode)** — Linode Pazar Yerinden dağıtın
- **Vultr** — Vultr Pazar Yerinden dağıtın

Bu pazar yeri görüntülerinde kurulum programı önceden yüklüdür. Sunucuyu oluşturduktan sonra SSH ile bağlanın ve lisans token'ınızla kurulumu tamamlamak için ekran görüntüsündeki talimatları izleyin.

## Yardım alma

Kurulum başarısız olursa veya bir hata ile karşılaşırsanız:

1. **Tanıma aracı**'nı çalıştırın: `./doctor.sh` (kurulum sırasında oluşturulur)
2. Doktor, tüm hizmetleri, bağlantıyı, SSL ve yaygın sorunları kontrol eder
3. `./doctor.sh --fix` ile otomatik onarımlar deneyin
4. Sorun devam ederse, Spwig destek ekibiyle iletişime geçin ve doktor çıktısını paylaşın