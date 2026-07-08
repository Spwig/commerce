---
title: Veritabanı Yedekleri
---

Regüler yedekler, mağazanızın verilerini — siparişler, müşteriler, ürünler ve yapılandırmalar — donanım hatalarına, yanlış silinmelere ve diğer beklenmedik olaylara karşı korur. Spwig'ın yedek sistemi, isteğe bağlı yedekler oluşturmanıza, otomatik zamanlamalar ayarlamanıza, yedekleri yerel olarak indirmenize, herhangi bir kaydedilmiş yedekten geri yükleme yapmanıza ve yedekleri Amazon S3 veya Google Drive gibi uzak depolama hedeflerine kopyalamanıza olanak tanır.

**Yönetim > Sistem Metrikleri**'ne gidin ve araç çubuğundaki bağlantıları kullanarak yedek araçlarına erişin.

![Yedek araçlarıyla birlikte sistem panosu](/static/core/admin/img/help/database-backups/system-dashboard.webp)

## Manuel bir yedek oluşturma

Önemli değişiklikler yapmadan önce — örneğin ürün içeriği, tema güncellemesi veya platform yükseltmesi — bir yedek oluşturun.

1. **Yönetim > Sistem Metrikleri**'ne gidin
2. Araç çubuğundan **Tam Yedek Oluştur**'a tıklayın
3. Yedek için tanımlayıcı bir **Ad** girin (örneğin, `before-july-import`)
4. Bu yedek nedeniyle kendinizi hatırlatmak için isteğe bağlı olarak bir **Açıklama** ekleyin
5. **Yedek Türünü** seçin:
   - **Tam Sistem** — veritabanını ve tüm medya dosyalarını yedekler (önerilir)
   - **Sadece Veritabanı** — sadece mağaza verilerini yedekler, yüklenebilir görüntüler ve dosyalar hariç tutulur
6. **Sıkıştırma**'yı seçin (`gzip` varsayılan ve çoğu mağaza için iyi çalışır)
7. **Yedek Oluştur**'a tıklayın

Spwig, yedekleme işlemini arka planda gerçekleştirir. Bir ilerleme göstergesi, şu anki aşamayı gösterir. İşlem tamamlandığında, yedek **Veritabanı Yedekleri** listesinde **Tamamlandı** durumuyla ve dosya boyutuyla görünür.

## Yedek indirme

Herhangi bir tamamlanmış yedekleri bilgisayarınıza yerel bir kopya oluşturmak için indirebilirsiniz.

1. **Yönetim > Veritabanı Yedekleri**'ne gidin
2. İndirmek istediğiniz yedekleri bulun
3. Yanındaki **İndir** butonuna tıklayın

Yedek dosyası, sıkıştırılmış bir arşiv olarak indirilir. Güvenli bir yerde saklayın — ayrı bir cihazda veya bulut depolama alanında — böylece sunucunuzdan bağımsız bir kopyanız olur.

## Otomatik yedek planlama

Otomatik yedekler, herhangi bir eylem olmadan arka planda çalışır, bu nedenle manuel yedekler oluşturmayı unutursanız bile verileriniz korunur.

1. **Yönetim > Sistem Metrikleri**'ne gidin
2. **Yedek Zamanlaması**'na tıklayın
3. **Otomatik Yedekleri Etkinleştir** onay kutusunu işaretleyin
4. **Sıklığı** ayarlayın:
   - **Günlük** — belirttiğiniz zaman diliminde her gün bir kez çalışır
   - **Haftalık** — seçtiğiniz günde her hafta bir kez çalışır
   - **Aylık** — ayın belirli bir gününde çalışır
5. Yedekin çalışması gereken **Zamanı** ayarlayın (sunucu zamanı, genellikle UTC — 03:00 AM düşük trafiğe uygun iyi bir zaman)
6. **Yedek Türünü** seçin (Tam Sistem veya Sadece Veritabanı)
7. **İlkelik Günleri** ayarlayın — bu günden eski yedekler otomatik olarak silinir (varsayılan: 30 gün)
8. Yedek dosyasının istirahat halinde şifrelenmesi için isteğe bağlı olarak **Yedek Şifrele** onay kutusunu işaretleyin
9. Uzak depolama hedeflerinizi yapılandırdıysanız, **Uzak Hedefler** altında bunları seçerek planlanan yedekleri otomatik olarak yüklemeyi sağlayın
10. **Zamanlamayı Kaydet**'e tıklayın

**Bir Sonraki Çalışma** zaman damgası hemen güncellenir ve bir sonraki otomatik yedekin ne zaman gerçekleşeceği gösterilir.

## Yedekten geri yükleme

Geri yükleme, mevcut mağaza verilerinizi bir yedekin içeriğiyle değiştirir. Bu, veri kaybından kurtulmak veya istenmeyen değişiklikleri geri almak için kullanılır.

> **Önemli:** Geri yükleme, mevcut tüm verileri yedek verileriyle değiştirir. Geri yükleme sırasında mağaza bakım moduna alınır. Bir geri yükleme yapmadan önce ekibinizi bilgilendirin.

1. **Yönetim > Sistem Metrikleri**'ne gidin
2. Araç çubuğundan **Geri Yükle**'ye tıklayın
3. Geri yükleme listesi, tüm mevcut yedekleri tarihleri ve boyutlarıyla gösterir
4. Kullanmak istediğiniz yedekin yanındaki **Geri Yükle**'ye tıklayın
5. Onay ekranını gözden geçirin — neyin değiştirileceğini tam olarak listeler
6. Onay ifadesi istenirse girin ve ardından **Geri Yükle**'ye tıklayın

Spwig, geri yükleme aşamaları sırasında bir ilerleme çubuğu gösterir (mevcut durumun yedeklenmesi, uzak bir yedek indirilmesi, veritabanının geri yüklenmesi, medya dosyalarının geri yüklenmesi). İşlem tamamlandığında, mağaza otomatik olarak bakım modundan çıkar.


## Uzak depolama kurulumu

Uzak depolama, yedeklerinizi otomatik olarak Amazon S3, Google Drive, Dropbox veya bir SFTP sunucusu gibi harici bir hedefe kopyalar. Bu, sunucu düzeyindeki hatalara karşı koruma sağlar.

1. **Yönetim > Sistem Metrikleri**'ne gidin
2. **Uzak Depolama**'ya tıklayın
3. **Hedef Ekle**'ye tıklayın
4. Kurulum asistanı, size üç adımı rehberlik eder:
   - **Adım 1**: Depolama türünü seçin (S3, Google Drive, Dropbox veya SFTP)
   - **Adım 2**: Seçtiğiniz sağlayıcı için kimlik bilgilerini girin (aşağıdaki ayrıntıları görün)
   - **Adım 3**: Hedefi isimlendirin ve bağlantıyı test edin
5. Bağlantı testi geçerse, **Kaydet**'e tıklayın

### Amazon S3 (ve S3 uyumlu hizmetler)

Aşağıdakilere ihtiyacınız olacak:
- **Erişim Anahtar Kimliği** ve **Gizli Erişim Anahtarı** AWS IAM kullanıcıdan
- **Buket Adı** — yedekleri yükleyeceğiniz S3 buketi
- **Bölge** — buketin bulunduğu AWS bölge (örneğin, `us-east-1`)
- Opsiyonel olarak bir **Önek** (buket içindeki klasör yolu, örneğin `spwig-backups/`)

S3 uyumlu hizmetler (Backblaze B2, Wasabi, MinIO vb.) aynı şekilde çalışır — istenen anda özel uç nokta URL'sini girin.

### Google Drive

Kimlik bilgileri adımı sırasında **Google ile Bağlan**'a tıklayın. Spwig, Google OAuth penceresini açar — oturum açın ve dosyaları yüklemek için izin verin. Manuel kopyalama yapmak gerekmez.

### Dropbox

Kimlik bilgileri adımı sırasında **Dropbox ile Bağlan**'a tıklayın. Dropbox'a oturum açın ve erişimi onaylayın. Yedekler, Dropbox hesabınızda `Apps/Spwig` klasörüne yüklenir.

### SFTP

Aşağıdakilere ihtiyacınız olacak:
- **SFTP sunucunuzun** ana bilgisayar adı
- **Port** (varsayılan: 22)
- **Kullanıcı adı** ve **Şifre** (veya SSH özel anahtarı)
- **Uzak Yol** — sunucuda yedekleri yükleyeceğiniz dizin

### Hedefi varsayılan olarak ayarlama

**Uzak Depolama** sayfasında, herhangi bir hedefin yanındaki anahtarın üzerine tıklayarak onu **varsayılan** olarak ayarlayın. Varsayılan hedef, her yedek — el ile veya planlı — her seferinde seçilmeksizin otomatik olarak alınır.

## İpuçları

- Önemli her değişiklikten önce el ile bir yedek alın: ürün içeriği, tema düzenlemeleri, platform yükseltmeleri veya indirim kampanyaları
- Günlük yedekleri düşük trafiğe sahip bir saatte (örneğin, sabah 3:00) planlayın, böylece performans etkisini minimize edersiniz
- En az bir uzak depolama hedefi kurun, böylece sunucu kendine ait bir sorun yaşasa bile yedekler korunur
- **İlkesizlik Günleri** ayarı, yerel yedeklerin ne kadar süre tutulacağını kontrol eder — çoğu mağazalar için 30 gün uygun bir varsayılan değerdir, ancak depolama alanı izin veriyorsa bunu artırın
- Geri yükleme yaptıktan sonra, mağazayı bakım modundan çıkarmadan önce birkaç sipariş ve ürün kontrol edin, verilerin doğru göründüğünden emin olun
- Şifreli yedekler, ek bir güvenlik katmanı sağlar ancak geri yükleme için şifre çözme anahtarına ihtiyaç duyar — bunu kaybetmeyin