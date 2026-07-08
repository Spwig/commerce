---
title: POS Personel İndirimleri ve Terminal Güvenliği
---

POS personel indirim ayarları, her personelin satış noktası (POS) sisteminde ne kadar indirim uygulayabileceğini kontrol etmenizi sağlar. Terminal kilitleme olayları, terminalin her kilidi açma veya kilitlenme anını izlemek için bir denetim izi oluşturur — bu da terminalin kimin tarafından erişildiğini ve başarısız oturum girişi denemelerinin olup olmadığını takip etmenizi sağlar.

## Personel İndirim Sınırları

POS sistemini kullanan her personel için bireysel indirim izni olabilir. Varsayılan olarak, personel öğelere veya sepetin tamamına kadar 10% indirim uygulayabilir. Bu limiti kişiye göre artırabilir veya azaltabilir ya da personeli, standart sınırları aşan indirimleri onaylayan yöneticiler olarak belirtebilirsiniz.

### Personel İndirim Sınırlarını Yapılandırma

1. **POS > Personel İndirimleri** bölümüne gidin
2. **+ POS Personel İndirimi Ekle**'ye tıklayın veya mevcut bir personeli düzenlemek için tıklayın
3. Listeden **Personel**'i seçin
4. İndirim sınırlarını ayarlayın:

| Alan | Açıklama |
|-------|-------------|
| **Maksimum İndirim %** | Bu kişi tarafından uygulanabilecek maksimum yüzde indirim (örneğin, `10` 10% için) |
| **Maksimum İndirim Tutarı** | İşlem başına sabit dolar tutarı (sabit tavan olmadan boş bırakın) |
| **Öğe İndirimleri Uygulayabilir** | Bireysel satır öğelerine indirim uygulamayı izin verir |
| **Sepet İndirimleri Uygulayabilir** | Sepet toplamına indirim uygulamayı izin verir |
| **Neden Gerekiyor** | İşaretlendiğinde, personel herhangi bir indirim uygulamadan önce bir neden yazmak zorundadır |

5. **Kaydet**'e tıklayın

### POS'da İndirim Sınırlarının Nasıl Çalışması

Kasayıcı bir indirim uygulamaya çalıştığında:
- İndirim, sınırları içindeyse hemen uygulanır
- İndirim, sınırlarını aşıyorsa terminal **yönetici onayı** istemektedir
- Bir yönetici, onaylamak için PIN'ini girer ve indirim uygulanır

Bu işlem, geçersiz yüksek değerli indirimlerin önlenmesini sağlarken, gerçek indirimlerin gerekliliği durumunda esneklik sağlar.

## Yönetici Roller

**Yönetici** olarak işaretlenmiş personel, diğer personel sınırlarını aşan indirimleri onaylayabilir. Yöneticiler, onay istendiğinde terminalde girdikleri bir PIN ile tanımlanır.

### Yöneticiyi Ayarlama

1. Bir personelin indirim kaydını açın
2. **Yönetici** işaretini seçin
3. **Yönetici PIN** (4-6 haneli) girin — bu, kaydedildiğinde güvenli şekilde hashlenir
4. **Kaydet**'e tıklayın

Yönetici PIN, terminal kilitleme/kilit açma için kullanılan kasayıcı PIN'den ayrıdır. Bir yönetici hem yönetici PIN'ine (indirim onayı için) hem de kasayıcı PIN'ine (terminal erişimi için) sahip olabilir.

### Yönetici PIN Güvenliği

Yönetici PIN'ini admin formunda girip kaydederken, Spwig otomatik olarak hashler — düz PIN asla saklanmaz. Düz PIN alanı kaydedildikten sonra temizlenir, bu beklenen davranıştır.

## Kasayıcı PIN'leri ve Kart Erişimi

Her personel ayrıca terminali kilitleme ve kilidini açmak için bir **Kasayıcı PIN** de olabilir:

- **Kasayıcı PIN** — 4-6 haneli PIN, terminal otomatik olarak kilitlendikten veya elle kilitlendikten sonra kilidini açmak için kullanılır
- **Kart Kimliği** — Kayıtlı bir kart (swipe kartı veya NFC) da terminali kilidini açmak için kullanılabilir

Kasayıcı PIN'ini ayarlamak için **Kasayıcı PIN** alanına girin ve kaydedin. Yönetici PIN'ine benzer şekilde, kaydedildiğinde otomatik olarak hashlenir.

## Terminal Kilitleme Olayları

Her terminalin kilidi açıldığında veya kilitlendiğinde, Spwig bir terminal kilitleme olayı kaydeder. Bu, tam bir güvenlik denetim izi oluşturur.

### Kilitleme Olaylarını Görüntüleme

**POS > Terminal Kilitleme Olayları** bölümüne giderek tam tarihçeyi görüntüleyebilirsiniz. Olayları aşağıdaki kriterlerle filtreleyebilirsiniz:
- Terminal
- Olay türü
- Tarih aralığı

### Olay Türleri

| Olay | Anlamı |
|-------|---------|
| **Elle Kilit** | Bir personel terminali amaçlı olarak kilitledi |
| **Otomatik Kilit (Boşta Zaman Aşımı)** | Terminal, inaktiflik nedeniyle otomatik olarak kilitlendi |
| **Kasiyer Tarafından Kilit Çözme** | Kasiyer kimlik doğrulandı ve terminali kilidi çözdü |
| **Yönetici Tarafından Kilit Çözme** | Bir yönetici kendi kimlik bilgilerini kullanarak kilidi çözdü |
| **Kartla Kilit Çözme** | Kayıtlı bir sürükleme kartı kullanılarak terminal kilidi çözüldü |
| **Biyometrikle Kilit Çözme** | Parmak izi veya yüz tanıma kullanılarak terminal kilidi çözüldü |
| **Başarısız Kilit Çözme Denemesi** | Yanlış kimlik bilgileriyle bir kilit çözme denemesi yapıldı |
| **Kilitlenme (3+ Başarısızlık)** | Rekürsif başarısız denemelerden sonra terminal kilitlendi |

### Kilit olayı kayıtları ne içerir

Her olay kaydı:
- İlgili **Terminal**
- **Olay Türü**
- Eylemi yapan kişi (**Tarafından Yapıldı**) ve kilitlenme sırasında oturum açmış kişi (**Kilitlendiği Taraf**) 
- **Yönetici Geçersizleştirme** kullanılıp kullanılmadığı
- **Kilit Çözme Yöntemi** (PIN, kart veya biyometrik)
- Bu olaydan önceki **Başarısız Denemeler** (kuvvetli kırma desenlerini tespit etmek için faydalıdır)
- Olay gerçekleştiğindeki **Sepet Toplamı** ve ürün sayısı
- İstek IP adresi

### Güvenlik sorununu araştırmak

Bir terminalin yetkisiz erişiminden şüpheleniyorsanız:

1. **POS > Terminal Kilit Olayları** menüsüne gidin
2. Sorunlu terminali filtreleyin
3. **Başarısız Kilit Çözme Denemesi** veya **Kilitlenme** türündeki olaylara bakın — bu, tekrarlı başarısız erişimleri gösterir
4. Başarılı kilit çözme olaylarında **Tarafından Yapıldı** alanını inceleyin, kimin erişim sağladığını görün
5. **POS > Şifreler** ile kayıtlı şifreleri karşılaştırın, görevli kasiyerin ne zaman görevde olması gerekiyordu onu doğrulayın

## İpuçları

- Personelin düzeyine göre indirim sınırlarını ayarlayın — yeni personel 5% ile başlayabilir, deneyimli personel 10-15% ve yöneticiler daha yüksek indirimleri onaylayabilir.
- Daha yüksek indirim sınırlarına sahip personeller için **Neden Gerekli** özelliğini etkinleştirin. Dosyada bir neden olacak şekilde ayarlamak, indirim desenlerini analiz etmenize ve herhangi bir kötüye kullanımın tespitine yardımcı olur.
- Mağazanızda birden fazla personel veya yüksek personel dövüşü varsa, haftalık olarak terminal kilit olaylarını inceleyin — düzensiz erişim desenlerini, sorun olmaya başlamadan önce fark etmek daha kolaydır.
- Bir personel işten ayrıldığında, kasiyer PIN ve kart kimlik bilgilerini hemen kaldırın, terminal erişimini engellemek için.
- Kilitlenme olayını kullanarak, otomatik kilit zaman aşımının ayarlanması gereken terminalleri tespit edin — müşteriler sık sık yanlışlıkla kilitlenmelerine neden oluyorsa, boşta zaman aşımı çok kısa ayarlanmış olabilir.
- Yönetici PIN'leri periyodik olarak değiştirilmelidir. Onları personel indirim kaydı içinde güncelleyin — yeni PIN, kaydetme sırasında hashlenir.