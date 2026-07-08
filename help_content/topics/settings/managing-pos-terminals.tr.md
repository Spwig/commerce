---
title: POS Terminalini Yönetme
---

POS terminalini yönetmek, perakende operasyonlarınızın temelidir. Her terminal, satış personelinin satışları işlemesi için fiziksel bir cihaz (tablet, bilgisayar veya özel POS donanımı) temsil eder. Terminali, depo atamaları, personel yetkileri, donanım entegrasyonları ve çevrimdışı senkronizasyon ayarları ile yapılandırın. Gerçek zamanlı kalp atışı izleme ile terminal durumunu izleyin ve sorunlar oluşduğunda terminali uzaktan kilitleyin. Uygun terminal yönetimi, mağaza içindeki işlemleri kolaylaştırır ve konfigürasyon çakışmalarını önler.

**POS > Terminal**'e gidin, yeni terminal kaydetmek için, terminalin çevrimiçi/çevrimdışı durumunu görüntülemek için ve tüm terminal ayarlarını yönetmek için.

![Terminal Listesi](/static/core/admin/img/help/managing-pos-terminals/terminal-list.webp)

## Terminal Listesi Görünümü

Terminal listesi, kaydedilmiş tüm terminalleri anahtar durum bilgisiyle görüntüler:

**Terminal Adı** - Terminal için tanımcı etiket (örneğin, "Ödeme 1", "Ana Kayıt", "Mobil Terminal")

**UUID** - Oluşturma sırasında otomatik olarak oluşturulan benzersiz tanımlayıcı (cihaz tanımlamak için dahili olarak kullanılır)

**Depo** - Bu terminalin atandığı fiziksel konum (stok kullanılabilirliğini ve sipariş atamasını belirler)

**Çevrimiçi Durumu** - Terminalin şu anda bağlı olup olmadığını gösteren canlı göstergedir:
- **Yeşil nokta** - Çevrimiçi (son 5 dakika içinde kalp atışı alındı)
- **Kırmızı nokta** - Çevrimdışı (5 dakikadan uzun süredir kalp atışı yok)
- **Gri nokta** - Asla eşleştirilmedi (terminal oluşturuldu ancak cihaz asla bağlanmadı)

**Son Kalp Atışı** - Terminalden alınan en son ping zaman damgası (çevrimiçi olduğunda her 5 dakikada bir güncellenir)

**Eşleştirme Kodu** - Başlangıçta cihazı eşlemek için kullanılan 8 karakterlik alfasayısal kod (ilk kullanımından sonra gizlenir)

**Atanmış Kullanıcılar** - Bu terminali kullanmaya yetkili personel sayısı

## Yeni Bir Terminal Oluşturma

Yeni bir POS cihazını kaydetmek için **+ Terminal Ekle**'ye tıklayın:

![Terminal Ekleme Formu](/static/core/admin/img/help/managing-pos-terminals/terminal-add-form.webp)

### Temel Yapılandırma

**Terminal Adı** - Açıklamalı bir ad seçin:
- Fiziksel konum: "Kuzey Girişi Kayıt"
- Fonksiyon: "İade Masa Terminali"
- Sıra: "Ödeme 1", "Ödeme 2", "Ödeme 3"

Adlar, personelin vardiyaları ataması ve sorun giderme sırasında terminali tanımlamasına yardımcı olur. Tüm konumlarda tutarlı adlandırma kurallarını kullanın.

**Depo** - **GEREKLİ** - Bu terminalin çalıştığı depoyu seçin:
- Hangi stokun satılabilir olduğunun belirlenmesi
- Bu terminalde yapılan siparişler bu depoya atılır
- Stok rezervasyonları atanan depoda kullanılabilirliği kontrol eder
- **Depo ataması olmadan satış işlemi yapılamaz**

Birden fazla perakende konumunuz varsa, her konum için ayrı bir depo oluşturun ve terminalleri uygun şekilde atayın.

**Aktif mi?** - Terminali yapılandırmayı silmeden etkinleştirmek/etkinleştirmemek için anahtar:
- Etkin olmayan terminaller eşleştirilemez
- Etkin olmayan terminaldeki mevcut oturumlar hemen sona erer
- Kayıtlı cihazları geçici olarak devre dışı bırakmak için kullanın

### Personel Ataması

**Atanmış Kullanıcılar** - Bu terminali erişim için hangi personel üyelerinin seçileceğini belirleyin:
- Sadece atanan kullanıcılar terminalde oturum açabilir
- Kullanıcılar aynı zamanda personel rolünde POS izinlerine sahip olmalıdır
- Sıfır kullanıcı ataması terminali etkili bir şekilde kilitleyecektir
- Yaygın desen: Tüm mağaza personelini tüm mağaza terminaline atayın

**Kullanım Durumu Örnekleri**:
- **Genel Mağaza**: Tüm personeli tüm terminalere atayın (herhangi bir kasır herhangi bir kaydı işlemek için çalışabilir)
- **Departman Mağazası**: Departman özel personeli departman terminaline atayın
- **Çok Konumlu**: Konum özel personeli konum terminaline atayın
- **Yöneticiler**: Tüm terminalere yönetim atayın, denetim erişimi için

Terminal ataması olmayan kullanıcılar, oturum açmaya çalıştığında "Bu terminal için yetkili değil" hatasını görür.

### Donanım Yapılandırması

**Donanım Yapılandırması** alanı, periferik cihazları tanımlayan bir JSON yapısıdır:

**Termal Yazıcı**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  }
}
```

**USB Barkod Okuyucu**:
```json
{
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  }
}
```

**Kasa** (yazıcıya bağlı):
```json
{
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

**Tam Örnek**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  },
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  },
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

Terminalde periferik donanım yoksa boş bırakın (tablet veya yazıcı/okuyucu olmayan mobil terminal için uygun)

### Çevrimdışı Önbellek Ayarları

Terminalin çevrimdışı işlem için ne kadar veri önbelleğe alacağını yapılandırın:

**Sipariş Senkronizasyon Günleri** (7-30 gün, varsayılan: 14):
- Son 7-30 gün içindeki siparişlerin yerel önbelleğe alınması için gün sayısı
- Daha yüksek değerler = daha fazla tarihi veri çevrimdışı olarak kullanılabilir
- Daha düşük değerler = daha hızlı senkronizasyon, daha az depolama alanı kullanılır
- **Öneri**: Yüksek hacimli terminaller için 7 gün, normal kullanım için 14 gün, denetim ağırlıklı işlemleri için 30 gün

**Sipariş Senkronizasyon Sınırı** (200-1000 sipariş, varsayılan: 500):
- Tarih aralığına bakılmaksızın önbelleğe alınacak maksimum sipariş sayısı
- Yüksek hacimli terminalde aşırı depolama kullanımını önler
- **Öneri**: Sınırlı depolama alanına sahip tabletler için 200, standart terminal için 500, özel POS cihazları için 1000

**İşlem**:
- **Daha yüksek ayarlar**: Tarihi verilere daha iyi çevrimdışı erişim, daha yavaş başlangıç senkronizasyonu, daha fazla depolama alanı kullanılır
- **Daha düşük ayarlar**: Daha hızlı senkronizasyon, daha az depolama alanı, sınırlı çevrimdışı tarih

Terminal, her senkronizasyon döngüsünde en son X siparişini (Y gün içinde) indirir. Eğer terminal 50 sipariş/gün işlerse ve sync_days 14 ise, yaklaşık 700 sipariş önbelleğe alınır (sync_limit sınırına ulaşabilir).

## Terminal Eşleştirme Akışı

Terminal oluşturduktan sonra fiziksel cihazı eşleştirin:

1. **Eşleştirme Kodu Oluştur** - Terminali kaydettikten sonra otomatik olarak oluşturulur (8 alfasayısal karakter)

2. **Kodu Not Edin** - Terminal listesi ve detay görünümünde görüntülenir (ilk başarılı eşleştirme sonrası sona erer)

3. **Terminal Cihazına Git** - Fiziksel cihaz (tablet/bilgisayar) üzerinde tarayıcıyı açın ve `https://yourstore.com/pos/` adresine gidin

4. **Eşleştirme Kodunu Girin** - İstenildiğinde 8 karakterlik kodu girin

5. **Terminal Yapılandırmasını İndir** - Cihaz alır:
   - Depo ataması
   - Donanım yapılandırması (yazıcı, okuyucu, kasa)
   - Çevrimdışı önbellek ayarları
   - Atanmış kullanıcı listesi
   - İlk ürün kataloğu senkronizasyonu

6. **Oturum Açma İstemi Görünür Olur** - Terminal, atanan kullanıcılar için oturum açma ekranını gösterir

7. **Personel Oturum Açar** - Bu terminalin atanan kullanıcı için kimlik bilgilerini girin

8. **İlk Senkronizasyon Tamamlanır** - Terminal indirir:
   - Son siparişler (sync_days ve sync_limit'e göre)
   - Atanan depo için tam ürün kataloğu
   - Müşteri veritabanı
   - Promosyon yapılandırmaları

9. **Terminal Hazır** - "Satışa Hazır" ekranı, arama çubuğu ile birlikte görünür

10. **Eşleştirme Kodu Kullanıldı** - Kod admin'den kaldırılır; yeniden eşleştirme gerekirse yeni bir kod oluşturun

**Eşleştirme Kodu Yeniden Oluşturma**: Eğer terminali yeniden eşleştirmek gerekirse (cihaz sıfırlanmış, tarayıcı önbelleği temizlenmiş, yeni donanım), **Eşleştirme Kodu Yeniden Oluştur** admin eylemini kullanın. Bu, eski kodu geçersiz kılar ve yeni bir kod oluşturur.

## Terminal Durumunu İzleme

### Kalp Atışı Sistemi

Terminal, sunucuya her **5 dakikada bir** kalp atışı sinyali ile birlikte gönderir:
- Terminal UUID
- Mevcut zaman damgası
- Çevrimiçi kullanıcı sayısı
- Son senkronizasyon zaman damgası
- Hizmet İşçisi durumu

**Çevrimiçi Durumu Gösterge**:
- **Yeşil** - Kalp atışı son 5 dakika içinde alınmış (terminal çevrimiçi ve işlemi yapabilir)
- **Kırmızı** - 5 dakikadan uzun süredir kalp atışı alınmamış (terminal çevrimdışı veya bağlantısı kesilmiş)
- **Gri** - Terminal asla eşleştirilmemiş (asla kalp atışı alınmamış)

**Kullanım Durumu**:
- **Günlük açılış**: Mağaza açılmadan önce tüm terminalin çevrimiçi olduğundan emin olun
- **Sorun Giderme**: Bağlantı sorunları yaşayan terminali tanımlayın
- **Denetim**: İş saatlerinde terminalin aktif olduğundan emin olun

### Son Kalp Atışı Zaman Damgası

En son kalp atışı tarihini ve saatini gösterir. Bu, şunları belirlemek için kullanılır:
- Terminalin ne kadar süredir çevrimdışı olduğunu
- Desenleri tanımlamak (örneğin, terminal her gece kapanışta çevrimdışı olur)
- Senkronizasyon sıklığını doğrulamak (çevrimiçi olduğunda yaklaşık 5 dakikada bir güncellenmelidir)

## Uzaktan Kilitleme Özelliği

Terminal, bir ekran üzerinde takılı kalırsa (yazılım çökmesi, oturum zaman aşımı sorunları, tarayıcı takılı kalması) **Uzaktan Kilitleme** admin eylemini kullanın:

**Nasıl Çalışır**:
1. Admin listeden sorunlu terminali seçin
2. Admin eylemlerinden **Uzaktan Kilitleme**'yi seçin
3. Eylemi onaylayın
4. Sunucu, kalp atışı yanıtıyla kilitleme sinyali gönderir
5. Terminal, sonraki kalp atışı döngüsünde (5 dakikadan kısa) sinyali alır
6. Terminal, mevcut kullanıcıyı zorla oturumdan çıkarır ve oturum açma ekranına döner

**Ne Zaman Kullanılır**:
- Terminal işlem ekranında takılı kalırsa
- Personel oturum açamıyorsa (oturum açma düğmesi yanıt vermiyor)
- Oturum aktif görünüyor ancak terminal yanıt vermiyorsa
- Tarayıcı çöktü ancak oturum çerezleri hala varsa

**Önemli**: Uzaktan kilitleme, cihazı veya tarayıcıyı yeniden başlatmaz - sadece oturum kilitleme ve oturum temizleme zorlar. Eğer terminal tamamen takılıysa, personel tarayıcıyı veya cihazı elle yeniden başlatmalıdır.

## Terminal Yapılandırmasını Düzenleme

Listede bir terminali seçerek yapılandırmasını düzenleyin:

![Terminal Düzenleme Formu](/static/core/admin/img/help/managing-pos-terminals/terminal-edit-form.webp)

**Terminal Çevrimiçi Olduğunda Güvenli Değiştirilebilir**:
- Terminal adı
- Atanmış kullanıcılar
- Donanım yapılandırması (terminal uygulamasını yeniden başlatmakla etkinleşir)
- Çevrimdışı önbellek ayarları (sonraki senkronizasyonla etkinleşir)

**Yeniden Eşleştirme Gerektirir**:
- Depo ataması (depo değişikliği yeni stok senkronizasyonu için yeniden eşleştirme gerektirir)

**Değiştirilemez**:
- UUID (değiştirilemez tanımlayıcı)

Çoğu ayar değişikliği, sonraki kalp atışı/senkronizasyon döngüsünde uygulanır. Donanım yapılandırması değişiklikleri, personelin POS uygulamasını kapatıp yeniden açması (veya tarayıcıyı yenilemesi) gerektirir.

## Yaygın Sorunların Giderilmesi

**Terminal Oturum Açma Ekranında "Yetkisiz" Gösteriyor**:
- Bu terminalin **Atanmış Kullanıcılar** listesinde kullanıcı olduğundan emin olun
- Kullanıcının **Personel & İzinler > Roller** içinde POS izinlerine sahip olduğundan emin olun
- Terminalin **Aktif mi?** işaretlenmiş olduğundan emin olun

**Terminal Eşleşmiyor (Geçersiz Kod)**:
- Eşleştirme kodları ilk kullanımından sonra sona erer - gerekirse yeniden oluşturun
- Kodlar büyük/küçük harfe duyarlıdır - büyük/küçük harf uyumunu kontrol edin
- Terminalin **Aktif mi?** işaretlenmiş olduğundan emin olun

**Terminal Çevrimdışı (Kırmızı Nokta)**:
- Cihazın internet bağlantısının olduğundan emin olun
- Terminalin gerçekten çalıştığını kontrol edin (tarayıcı /pos/ URL'sine açık)
- Yangın duvarının kalp atışı isteklerini engellemesi durumunu kontrol edin
- 5 dakika bekleyin, sonraki kalp atışı döngüsünü kontrol edin

**Terminal Senkronizasyonu Yavaş**:
- **Sipariş Senkronizasyon Günleri**'ni 30'tan 7'ye azaltın
- **Sipariş Senkronizasyon Sınırı**'nı 1000'den 200'e azaltın
- Terminal konumundaki ağ hızını kontrol edin
- Sunucunun yoğun yük altında olup olmadığını kontrol edin

**Yazıcı Çalışmıyor**:
- **Donanım Yapılandırması** içinde yazıcı IP ve portunu kontrol edin
- Terminal cihazından yazıcı bağlantısını test edin (IP adresine ping atın)
- Yazıcının ESC/POS uyumlu olduğundan emin olun
- Yazıcının açık ve çevrimiçi olduğundan emin olun

## İpuçları

- **Adlandırma kuralları önemlidir** - Konum + numara kullanarak ölçekleme ile yönetim kolaylaştırın
- **Eşleştirme yapmadan önce her zaman depo atayın** - Terminal, depo ataması olmadan satış işlemi yapamaz
- **Yeni cihaza dağıtım yapmadan önce donanım yapılandırmasını test edin** - Test faturası yazdırarak yazıcı/kasa entegrasyonunu doğrulayın
- **Günlük olarak kalp atışı izleyin** - Mağaza açılışında tüm terminalin çevrimiçi olduğundan emin olmak için rutin oluşturun
- **Mobil terminal için senkronizasyon sınırlarını düşürün** - Tabletler ve telefonlar için sync_days: 7, sync_limit: 200 ayarları faydalıdır
- **Uzaktan kilitleme özelliğini az kullanın** - Aktif işlemler için oturum kilitleme keser; terminalin gerçekten takılı olduğundan emin olun
- **Eşleştirme kodlarını belgeleyin** - Terminali perakende alanına dağıtmadan önce kodu yazın (kurulumun beklendiğinden daha uzun sürmesi durumunda)
- **Tüm terminalere yönetici atayın** - Denetleyicilerin herhangi bir kaydı void, iade ve sorun giderme için erişimini sağlar

