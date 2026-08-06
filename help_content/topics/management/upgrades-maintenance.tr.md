---
title: Güncellemeler & Bakım
---

Spwig düzenli olarak yeni özellikleri, performans iyileştirmelerini ve güvenlik düzeltmelerini alır. Bu kılavuz, kurulumunuzu nasıl güncelleyeceğinizi, tanımlayıcı aracı nasıl kullanacağınızı ve bakım görevlerini nasıl ele alacağınızı açıklar.

## Spwig Güncellemesi

### Güncellemeye Başlamadan Önce

1. **Yedek oluştur** — **Yönetim > Sistem Ölçüleri > Tam Yedek Oluştur** menüsüne gidin veya komut satırından yedek betiğini çalıştırın. Herhangi bir sorun oluşursa bu size bir güvenlik ağı sağlar.
2. **Mevcut sürümü kontrol et** — **Yönetim > Sistem Ölçüleri** veya yönetici paneli altbilgisinde görünür.
3. **Değişiklikleri incele** — **Sistem Güncellemesi** sayfasını açın ve yeni sürümün tam sürüm notlarını okuyun, sürümün belirttiği ekstra adımları da içerir (aşağıya bakın).

### Sistem Güncellemesi Sayfasında Yeni Ne Oldu

Spwig bir sonraki sürümü algıladığında, **Sistem Paneli** bir **Güncelleme Mevcut** hızlı eylemini gösterir. Tıklayın — veya önce **Sistem Paneli > Platform Güncellemeleri** menüsüne giderek değişiklik günlüğünü önizleyin, sonra devam edin — **Sistem Güncellemesi** sayfasını açar.

Sayfa şu bilgileri gösterir:

- **Mevcut Sürüm** ve **Mevcut Sürüm** kartları, hangi sürümler arasında geçiş yaptığınızı doğrulamanız için
- **{version} Sürümünde Yeni Özellikler** bölümü — sürümün kısa bir özeti, ardından başlıklar ve madde listesiyle biçimlendirilmiş tam sürüm notları, bakım sağlayıcılarının yazdığı gibi
- **Güncellemeye Hazırlık Kontrolleri** — disk alanı, veritabanı bağlantısı, son yedek, yazma izni ve Spwig güncelleme sunucusuna bağlantı. **Hazırlık Kontrollerini Çalıştır** tıklayın; **Güncellemeyi Başlat** düğmesi, tüm kontrollerin geçmesine kadar devre dışı kalır
- **Güncellemeye Hazırlanırken** başlığı, otomatik olarak bir yedek oluşturulduğunu, mağazanın geçici olarak bakım moduna girileceğini ve güncellemenin çalışması süresince sayfayı kapatmamanız veya başka bir yere gitmeniz gerektiğini hatırlatır

**Yeni Özellikler** bölümündeki **Güncelleme Notlarını** dikkatle okuyun — bazı sürümler, güncellemeyi yaptıktan sonra kendinizin yapmanız gereken adımları belirtir. Örneğin, yeni bir görsel formatı ekleyen bir sürüm, **Medya Kütüphanesi > Görsel İşleme** üzerinden ürün küçük resimlerinizi yeniden oluşturmanızı isteyebilir, böylece kütüphanenizdeki mevcut görseller bu iyileştirmeyi alır; yeni yükleme otomatik olarak bu özelliği alır, ancak mevcut katalogunuzun el ile yeniden başlatılması gerekir.

Hazırlık kontrolleri geçildikten sonra, **Güncellemeyi Başlat** butonuna tıklayarak tarayıcıdan güncellemeyi başlatın. Her aşamayı izleyen bir ilerleme çubuğu vardır ve güncelleme tamamlandığında sayfa otomatik olarak yeniden yüklenir. Bu, çoğu satıcı için önerilen yoludur — işlemi daha doğrudan kontrol etmeniz gerekiyorsa aşağıdaki SSH tabanlı betiği kullanın.

### Bir güncelleme çalıştırma

Sunucunuza SSH ile bağlanın ve Spwig kurulum dizininize gidin (genellikle `/opt/spwig`):

```bash
./upgrade.sh
```

Güncelleme betiği:

1. **Hazırlık kontrolleri** — disk alanı, Docker sağlığı ve hizmet durumunu doğrular
2. **Veritabanı Migrasyonlarını Deneme** — veritabanı değişikliklerinin temiz bir şekilde uygulanacağını test eder, ancak hiçbir şeyi değiştirmemektedir
3. **Bakım Moduna Gir** — güncelleme sırasında ziyaretçiler için bir bakım sayfası gösterilir
4. **Yedek Oluştur** — değişiklikler yapmadan önce otomatik güvenlik yedekini oluşturur
5. **Arka Plan İşçilerini Boşalt** — devam eden görevlerin (e-posta göndermeleri, çeviriler) düzgün şekilde tamamlanmasını bekler
6. **Yeni Görselleri Çek** — Spwig kayıt defterinden güncellenmiş uygulamayı indirir
7. **Veritabanı Migrasyonlarını Uygula** — yeni sürüm için veritabanı şemasını günceller
8. **Hizmetleri Yeniden Başlat** — yeni sürümle uygulamayı başlatır
9. **Sağlık Kontrolü** — tüm hizmetlerin düzgün çalıştığını doğrular
10. **Bakım Modundan Çık** — mağazanız tekrar çevrimiçi olur

Güncelleme sonrası sağlık kontrolü başarısız olursa, betik **otomatik olarak önceki sürüm**e geri döner ve yedekten geri yükler.

### Güncellemeler Seçenekleri

```bash
./upgrade.sh              # Bakım modu ile standart güncelleme
./upgrade.sh --dry-run    # Değişiklikleri uygulamadan kontrol et
```

## Tanımlayıcı Araç


Spwig, tüm kurulumunuzu sorunlar için kontrol eden yerleşik bir tanımlama aracı içerir:

```bash
./doctor.sh
```

Doktor şu şeyleri kontrol eder:

| Kategori | Ne kontrol eder |
|----------|---------------|
| **Sistem** | Disk alanı, RAM kullanımı, CPU yükü |
| **Docker** | Docker motoru sağlığı, konteyner durumu, image sürümleri |
| **Veritabanı** | PostgreSQL bağlantısı, geçiş durumu, bağlantı havuzu sağlığı |
| **Önbellek** | Redis bağlantısı, bellek kullanımı |
| **Nesne depolama** | MinIO bağlantısı, bucket erişilebilirliği |
| **Ağ** | DNS çözümleme, port erişilebilirliği, SSL sertifikasının geçerliliği |
| **Uygulama** | Hizmet sağlığı uç noktaları, arka plan çalışan durumu |

Her kontrol, bir şey yanlışsa detaylarla birlikte geç/bozuk sonuç gösterir.

### Otomatik onarım modu

Sık karşılaşılan sorunlar için doktor otomatik onarımlar yapmaya çalışabilir:

```bash
./doctor.sh --fix
```

Otomatik onarım şu sorunları çözebilir:

- Durdurulmuş konteynerler (yeniden başlatır)
- Kullanılamaz hale gelen veritabanı bağlantıları (bağlantı havuzunu yeniler)
- Süresi dolmuş SSL sertifikaları (yenileme tetikler)
- Eski Docker image'larından dolayı dolu disk (kullanılmayan image'ları temizler)

Doktor, eylem almadan önce neyi onarıp onarılmayacağını her zaman açıklar.

## Bakım modu

Bakım modu, değişiklikler yaparken ziyaretçilere "mağaza geçici olarak kullanılamıyor" sayfası gösterir. Yönetici paneliniz hala erişilebilirdir.

### Bakım modunu etkinleştirme

Yönetici panelinden: **Mağaza Ayarları > Bakım > Bakım Modunu Etkinleştir**

Ya da komut satırından:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Bakım modunu devre dışı bırakma

Yönetici panelinden: Bakım modu anahtarını kapat.

Ya da komut satırından:

```bash
./go-live.sh
```

### Bakım modu sırasında erişimi atlamak

Bakım modu etkinken, URL'ye gizli bir parametre ekleyerek mağazaya normal şekilde erişebilirsiniz. Atla gizli, `.env` yapılandırma dosyasında `MAINTENANCE_SECRET` altında gösterilir.

## Hizmetleri yönetme

### Hizmet durumunu görüntüleme

Tüm Spwig hizmetlerinin durumunu kontrol edin:

```bash
docker compose ps
```

Bu, her hizmetin durumunu (çalışıyor, durdu, yeniden başlatılıyor) ve sağlığı gösterir.

### Günlükleri görüntüleme

Belirli bir hizmetin günlüklerini kontrol edin:

```bash
docker logs spwig_shop          # Uygulama günlükleri
docker logs spwig_celery         # Arka plan çalışan günlükleri
docker logs spwig_nginx          # Web sunucusu erişim günlükleri
docker logs spwig_db             # Veritabanı günlükleri
```

`--tail 100` ekleyerek son 100 satırı, ya da `--follow` ekleyerek gerçek zamanlı günlükleri izleyebilirsiniz.

### Bir hizmeti yeniden başlatma

Belirli bir hizmetin yeniden başlatılması gerekiyorsa:

```bash
docker compose restart shop      # Uygulamayı yeniden başlat
docker compose restart celery    # Arka plan çalışanları yeniden başlat
docker compose restart nginx     # Web sunucusunu yeniden başlat
```

Tüm hizmetleri yeniden başlatmak için:

```bash
docker compose restart
```

## Bileşen güncellemeleri

Spwig, temalar, ödeme sağlayıcıları, kargo entegrasyonları ve diğer uzantılar gibi bileşenleri yükleyebileceğiniz bir bileşen pazarı sunar. Bileşenler, çekirdek platformdan bağımsız olarak güncellenir.

**Yönetim > Bileşen Güncellemeleri**'ne giderek mevcut bileşen güncellemelerini kontrol edin. Onayladığınızda güncellemeler otomatik olarak indirilir ve uygulanır.

## İpuçları

- **Sürekli yükseltme yapın** — en son sürümde olmak, güvenlik düzeltmelerini ve yeni özelliklere erişimi sağlar
- **Yükseltmeye başlamadan önce What's New bölümünü okuyun** — bu, gerekli veritabanı geçişini, güvenlik düzeltmesini veya yükseltme notlarını hızlıca tespit etmenin en hızlı yolu olur
- **Her zaman yedek alın** — yükseltme betiği otomatik bir yedek oluşturmakla birlikte, kendi yedekleriniz ekstra güvence sağlar
- **Sorunlar sonrası doktoru çalıştırın** — mağazanız beklenmedik şekilde davranıyorsa, `./doctor.sh` sorunları tanımlamak için en hızlı yoldur
- **Düşük trafiğe sahip saatlere yükseltmeyi planlayın** — bakım modu müşteri erişimini kısa süreliğine keser, bu yüzden yoğun saatlerde yükseltin
- **Disk alanını açık tutun** — yükseltmeler yeni image'lar ve yedekler için geçici alan gerektirir. En az 5 GB boş tutun.