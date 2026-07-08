---
title: Güncellemeler & Bakım
---

Spwig düzenli olarak yeni özellikler, performans iyileştirmeleri ve güvenlik düzeltmeleri ile güncellenir. Bu kılavuz, kurulumunuzu nasıl güncelleyeceğinizi, tanımlayıcı aracı nasıl kullanacağınızı ve bakım görevlerini nasıl ele alacağınızı açıklar.

## Spwig\'i Güncellemek

### Güncellemeye Başlamadan Önce

1. **Yedek oluştur** — **Yönetim > Sistem Ölçüleri > Tam Yedek Oluştur** menüsünden gidin veya komut satırından yedek betiğini çalıştırın. Herhangi bir sorun oluşursa bu size bir güvenlik ağı sağlar.
2. **Mevcut sürümü kontrol et** — **Yönetim > Sistem Ölçüleri** menüsünde veya admin panelinin alt kısmında görünür.
3. **Yayın notlarını oku** — yeni bir sürüm algılanırsa, admin panelinde **Yönetim > Bileşen Güncellemeleri** altında mevcuttur.

### Güncellemeyi Çalıştırmak

Sunucunuza SSH ile bağlanın ve Spwig kurulum dizininize gidin (genellikle `/opt/spwig`):

```bash
./upgrade.sh
```

Güncelleme betiği:

1. **Ön kontrol** — disk alanı, Docker sağlığı ve hizmet durumunu doğrular
2. **Veritabanı geçişlerini test et** — veritabanı değişikliklerinin uygulanacağından emin olur ancak hiçbir şeyi değiştirmemektedir
3. **Bakım moduna gir** — güncellemeye başlarken mağazanız ziyaretçilere bir bakım sayfası gösterir
4. **Yedek oluştur** — değişiklikler yapmadan önce otomatik bir güvenlik yedek oluşturur
5. **Arka plan çalışanlarını boşalt** — mevcut görevlerin (e-posta göndermeleri, çeviriler) düzgün şekilde tamamlanmasını bekler
6. **Yeni görüntüler çek** — Spwig kayıt defterinden güncellenmiş uygulamayı indirir
7. **Veritabanı geçişlerini uygula** — yeni sürüm için veritabanı şemasını günceller
8. **Hizmetleri yeniden başlat** — yeni sürümle uygulamayı başlatır
9. **Sağlık kontrolü** — tüm hizmetlerin düzgün çalıştığını doğrular
10. **Bakım modundan çık** — mağazanız tekrar çevrede

Güncelleme sonrası sağlık kontrolü başarısız olursa, betik **otomatik olarak önceki sürüm**e geri döner ve yedekleri geri yükler.

### Güncellemeleri Seçenekleri

```bash
./upgrade.sh              # Bakım modu ile standart güncelleme
./upgrade.sh --dry-run    # Değişiklikleri uygulamadan kontrol et
```

## Tanımlayıcı Araç

Spwig, tüm kurulumunuzu kontrol etmek için yerleşik bir tanımlayıcı araç içerir:

```bash
./doctor.sh
```

Tanımlayıcı aşağıdaki şeyleri kontrol eder:

| Kategori | Ne Kontrol Ediyor |
|----------|---------------|
| **Sistem** | Disk alanı, RAM kullanımı, CPU yükü |
| **Docker** | Docker motoru sağlığı, konteyner durumu, görüntü sürümleri |
| **Veritabanı** | PostgreSQL bağlantısı, geçiş durumu, bağlantı havuzu sağlığı |
| **Önbellek** | Redis bağlantısı, bellek kullanımı |
| **Nesne depolama** | MinIO bağlantısı, bucket erişilebilirliği |
| **Ağ** | DNS çözümleme, port erişilebilirliği, SSL sertifikası geçerliliği |
| **Uygulama** | Hizmet sağlığı uç noktaları, arka plan çalışan durumu |

Her kontrol, bir sorun varsa detaylarla birlikte geç/ başarısız sonucunu gösterir.

### Otomatik Onarım Modu

Sık karşılaşılan sorunlar için tanımlayıcı, otomatik onarımlar yapmaya çalışabilir:

```bash
./doctor.sh --fix
```

Otomatik onarım şu sorunları çözebilir:

- Durdurulmuş konteynerler (yeniden başlatır)
- Kullanılamayan veritabanı bağlantıları (bağlantı havuzunu yeniler)
- Süresi geçmiş SSL sertifikaları (yenileme tetikler)
- Eski Docker görüntülerinden dolu disk (kullanılmayan görüntülerin temizlenmesi)

Tanımlayıcı, herhangi bir eylem almadan önce neyi onaracağını her zaman açıklar.

## Bakım Modu

Bakım modu, değişiklikler yaparken ziyaretçilere "mağaza geçici olarak kullanılamıyor" sayfası gösterir. Yönetici paneliniz hala erişilebilir olur.

### Bakım Modunu Açmak

Yönetici panelinden: **Mağaza Ayarları > Bakım > Bakım Modunu Aç**

Veya komut satırından:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Bakım Modunu Kapatmak

Yönetici panelinden: bakım modu anahtarını kapat.

Veya komut satırından:

```bash
./go-live.sh
```

### Bakım Modunda Erişim Atlamak

Bakım modu etkinken, URL\'ye gizli bir parametre ekleyerek mağazaya normal şekilde erişebilirsiniz. Atlama gizli, `.env` yapılandırma dosyasında `MAINTENANCE_SECRET` altında gösterilir.

## Hizmetleri Yönetmek

### Hizmet Durumunu Görüntüleme


# Spwig Hizmetlerinin Durumunu Kontrol Etme

Tüm Spwig hizmetlerinin durumunu kontrol edin:

```bash
docker compose ps
```

Bu, her bir hizmetin durumunu (çalışıyor, durdu, yeniden başlatılıyor) ve sağlığı gösterir.

### Günlükleri Görüntüleme

Belirli bir hizmetin günlüklerini kontrol edin:

```bash
docker logs spwig_shop          # Uygulama günlükleri
docker logs spwig_celery         # Arka plan çalışan günlükleri
docker logs spwig_nginx          # Web sunucu erişim günlükleri
docker logs spwig_db             # Veritabanı günlükleri
```

`--tail 100` ekleyerek son 100 satırı görebilirsiniz, ya da `--follow` ile gerçek zamanlı olarak günlükleri izleyebilirsiniz.

### Bir Hizmeti Yeniden Başlatma

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

## Bileşen Güncellemeleri

Spwig, temalar, ödeme sağlayıcıları, kargo entegrasyonları ve diğer uzatımları yükleyebileceğiniz bir bileşen pazar yerine sahiptir. Bileşenler, çekirdek platformdan bağımsız olarak güncellenir.

**Yönetim > Bileşen Güncellemeleri**'ne giderek mevcut bileşen güncellemelerini kontrol edin. Onayladığınızda güncellemeler otomatik olarak indirilir ve uygulanır.

## İpuçları

- **Sürekli yükseltme yapın** — en son sürümde kalmanız, güvenlik düzeltmelerine ve yeni özelliklere erişim sağlar
- **Her zaman yedek alın** — yükseltme betiği otomatik bir yedek oluşturmakla birlikte, kendi yedekleriniz ekstra güvence sağlar
- **Sorunlar sonrası doctor komutunu çalıştırın** — mağazanız beklenmedik şekilde davranıyorsa, `./doctor.sh` sorunları tanımlamak için en hızlı yoldur
- **Düşük trafiğe sahip saatlerde yükseltmeleri planlayın** — bakım modu müşteri erişimini kısa süreliğine keser, bu yüzden yoğun saatler dışında yükseltin
- **Disk alanı boş bırakın** — yükseltmeler yeni görüntüler ve yedekler için geçici alan gerektirir. En az 5 GB boşluk tutun.