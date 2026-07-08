---
title: Tam Sistem Göçü
---

Tam Sistem Göçü, tüm mağazanızı -- ayarlar, ürünler, müşteriler, siparişler, medya dosyaları ve diğer tüm veriler -- bir Spwig kurulumundan diğerine aktarır. Yeni bir sunucuya geçiş yapmak veya mağazanızın tam kopyasını oluşturmak için bunu kullanın.

## Tam Göçü Ne Zaman Kullanmalısınız

- **Sunucu taşınması**: Mağazanızı yeni bir hosting sağlayıcısına veya sunucuya taşımak
- **Staj ortamı oluşturma**: Üretimden tam bir staj ortamı kurmak
- **Acil durum kurtarma**: Bir yedek örneğinden tam bir mağazayı geri yüklemek

Tam Göç, Ayar Senkronizasyonu'nun yaptığı her şeyi içerir ve bunlara ek olarak tüm işlem verilerini (ürünler, müşteriler, siparişler, incelemeler, stok, medya vb.) içerir.

## Göçülen Veriler

Tam Göç, tüm ayar kategorilerini ve bu veri kategorilerini transfer edebilir:

| Kategori | Açıklama |
|----------|-------------|
| **Yüklenebilir Bileşenler** | Temalar, sağlayıcı entegrasyonları ve paket dosyalarıyla birlikte yardımcı bileşenler |
| **Ürünler, Kategoriler & Markalar** | Ürünler, varyasyonlar, resimler, kategoriler, markalar ve öznitelikler |
| **Medya Kütüphanesi** | Tüm yüklenebilir medya dosyaları ve varlıklar |
| **Müşteriler & Adresler** | Müşteri hesapları, profiller ve adresler |
| **Sipariş Geçmişi** | Siparişler, sipariş kalemleri ve işlem kayıtları |
| **Ürün Değerlendirmeleri** | Müşteri incelemeleri ve puanlamalar |
| **Stok Seviyeleri** | Depo bazlı stok miktarları ve yeniden sipariş noktaları |
| **Diijital Ürünler & Lisanslar** | Diijital varlıklar, lisans şablonları ve lisans havuzları |
| **Hediye Çekleri & Voucher Kullanımı** | Hediye çekleri bakiyeleri ve voucher kullanım kayıtları |
| **Mağaza Kredisi & Cüzdanlar** | Müşteri cüzdan bakiyeleri ve işlem geçmişi |
| **Sadakat Programı Üyeleri** | Sadakat üyeleri, puanlar, işlemleri ve pankartlar |
| **Aktif Abonelikler** | Abonelik planları, aktif abonelikler ve fatura geçmişi |
| **Gönderimler & Takip** | Gönderim kayıtları ve takip olayları |
| **İade, İade Talepleri & Sipariş Notları** | İade kayıtları, iade talepleri ve notlar |
| **Afilasyon Üyeleri** | Afilasyon hesapları, referans kodları ve komisyon geçmişi |

## Adım Adım Kılavuz

### Adım 1: Kaynak Örneğe Bağlan

1. Yönetici yan çubuğunda **Veri Göçü > Spwig'den Spwig'e Senkronizasyon** bölümüne gidin
2. **Tam Göçü Başlat**'a tıklayın
3. Kaynak mağazaya (göçü **yapmak istediğiniz** mağaza) bağlanın:
   - Kaynak mağazanın URL'sini girin
   - Kaynak mağazadan senkronizasyon token'ını yapıştırın
   - Bağlantıyı adlandırın (örneğin, "Eski Üretim Sunucusu")
4. **Bağlantıyı Test Et**'e tıklayarak doğrulayın
5. **İleri**'ye tıklayın

> **Önemli:** Tam Göç, her zaman **bağlantılı mağazadan** bu mağazaya veri çeker. Sihirbazı **hedef** (yeni) mağazada çalıştırın.

### Adım 2: Kapsamı Seçin

Göçte dahil edilecek veri kategorilerini seçin. Kategoriler gruplara ayrılmıştır:

- **Ayarlar**: Mağaza yapılandırması, temalar, sağlayıcılar, içerik
- **Veri**: Ürünler, müşteriler, siparişler, medya ve diğer işlem verileri

Bazı kategoriler bağımlılıklara sahiptir (örneğin, Siparişler Müşteriler ve Ürünler'e bağımlıdır). Bir kategori seçtiğinizde bağımlılıklar otomatik olarak dahil edilir.

Özel işaretlenmiş kategoriler:
- **Anahtar simgesi**: Güvenli şekilde aktarılan kimlik bilgileri içerir
- **Dosya simgesi**: İkili dosyaları içerir (görseller, medya, paketler)
- **Uyarı simgesi**: Üretim ortamları için özel dikkat gerektirir

### Adım 3: Ön Kontroller

Göç başlamadan önce, otomatik ön kontroller:

- **Bağlantı sağlığı**: Kaynak mağazası erişilebilir ve kimliği doğrulanmış
- **Sürüm uyumluluğu**: Her iki mağaza da uyumlu Spwig sürümlerini çalıştırıyor
- **Disk alanı**: Medya dosyaları için yeterli depolama alanı mevcut
- **Veritabanı hazırlığı**: Hedef veritabanı veriyi alabilir

Eğer herhangi bir kontrol başarısız olursa, devam etmeden önce sorunu çözmek için özel yönlendirmeler göreceksiniz.

### Adım 4: Göç İlerlemesi

Göç arka planda çalışır. Uzaklaşabilirsiniz -- işlem devam edecektir.

İlerleme sayfası şu bilgileri gösterir:
- Tahmini kalan süreyle birlikte genel yüzdelik
- Kategori başına tamamlanma durumu
- Transfer ayrıntılarıyla canlı etkinlik günlüğü
- Medya kategorisi için medya transfer istatistikleri (taşınan dosyalar ve bayt)

Çok sayıda ürün ve medya dosyasına sahip büyük mağazalar için geçiş bazı zaman alabilir. Medya transfer aşaması genellikle en uzun süreyi alır.

### Adım 5: Sonuçlar

Geçiş tamamlandıktan sonra, sonuçlar sayfası şu bilgileri gösterir:

- Özet istatistikler (taşınan, atlanan, başarısız öğeler)
- Kategori başına durum analizi
- Başarısız öğeler için hata ayrıntıları

## Geçiş Sonrası Kontrol Listesi

Başarılı bir geçiş yaptıktan sonra, yeni mağazanızda aşağıdaki adımları tamamlayın:

1. Yeni kurulumda **lisansınızı etkinleştirin**
2. Geçiş sırasında atlanan **ödeme sağlayıcısı kimlik bilgilerini** tekrar girin (test/sandbox anahtarları üretim ortamına aktarılmaz)
3. **DNS yapılandırmasını** yeni sunucuya yönlendirmek için ayarlayın
4. **Test siparişiyle** ödeme akışını test edin
5. **E-posta gönderiminin** düzgün çalıştığını doğrulayın
6. **Medya dosyalarını** ve görüntülerin düzgün yüklendiğini kontrol edin

## Geri Dönüşüm

Tam Geçiş tamamlandıktan sonra, **24 saat** içinde geri dönmek için bir şansınız vardır. Geri dönüşüm, hedef mağazadan tüm taşınan veriyi silerek, onu geçiş öncesi durumuna geri döndürür.

Geri dönüşüm yapmak için:
1. Sonuçlar sayfasına veya Senkronizasyon Paneline gidin
2. **Geçiş Geri Dönüşümü**'nü tıklayın ve onaylayın
3. Geri dönüşümün tamamlanmasını bekleyin

> **Uyarı:** Geri dönüşüm, tüm taşınan veriyi kalıcı olarak siler. Geçiş sonrası hedef mağazada yapılan değişiklikler (yeni siparişler, müşteri kayıtları vb.) da etkilenecektir.

24 saat sonra geri dönüşüm seçeneği sona erer.

## İpuçları

- **Hedef mağazada çalıştırın**: Tam Geçiş asistanı, **yeni** mağazada çalıştırılmalıdır, eski mağazadan veri çekilmelidir
- **Temiz bir kuruma geçin**: En iyi sonuçlar için, canlıya geçmeden önce Spwig'in temiz bir kurumunda geçiş yapın
- **Disk alanı kontrolü**: Hedefin tüm medya dosyaları için yeterli depolama olduğundan emin olun
- **Kaynak mağazayı açık tutun**: Hedefte her şeyin düzgün çalıştığını doğrulamadan kaynak mağazayı kapatmayın
- **DNS geçişi planlayın**: Geçişin doğrulanmasından sonra DNS kayıtlarını yeni sunucuya yönlendirmeyi planlayın