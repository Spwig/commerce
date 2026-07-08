---
title: Gönderim Sağlayıcı Hesapları
---

Gönderim sağlayıcı hesapları, mağazanızı kurye API'leri (FedEx, UPS, DHL) ile gerçek zamanlı ücret hesaplaması ve etiket satın alma otomasyonu için bağlar. Her hesap, şifrelenmiş API kimlik bilgilerini saklar, bağlantı sağlıqlığını izler ve gerçek zamanlı gönderim yöntemlerine bağlanır. Sağlayıcılar, ödeme sırasında paket boyutları, ağırlığı, köken ve hedefe göre canlı ücretleri alır—manuel ücret tablosu bakımını kaldırır ve doğru kurye fiyatlarını garanti altına alır.

Kurye tarafından hesaplanan gönderim ücretlerine veya etiket oluşturma otomasyonuna ihtiyaç duyduğunuzda sağlayıcı hesaplarını kullanın.

## Desteklenen Gönderim Sağlayıcıları

Spwig, yüklemeli sağlayıcı bileşenleri aracılığıyla büyük kuryeleri destekler:

### FedEx

**Hizmetler**: Ground, Express, Uluslararası
**API**: FedEx Web Services
**Özellikler**: Gerçek zamanlı ücretler, etiket satın alma, takip, uluslararası gümrük

### UPS

**Hizmetler**: Ground, Hava, Dünya çapında
**API**: UPS Developer API
**Özellikler**: Gerçek zamanlı ücretler, etiket oluşturma, takip, adres doğrulama

### DHL

**Hizmetler**: Express, E-ticaret, Uluslararası
**API**: DHL Express API
**Özellikler**: Uluslararası ücretler, gümrük belgeleri, takip

### Ek Sağlayıcılar

Gerekli olduğunda bileşen pazar yerinden yükleyin (USPS, Canada Post, Australia Post vb.)

---

## Sağlayıcı Hesabı Yapılandırması

Her sağlayıcı hesabı için:

### Temel Bilgi

- **Gösterim Adı**: Hesabın yönetici panelinde nasıl görüneceği (örneğin, "FedEx Üretim Hesabı")
- **Sağlayıcı**: Aşağı açılan listeden yüklenebilir sağlayıcı bileşenini seçin
- **Aktif**: Hesabı silmeden etkinleştirme/etkinleştirme
- **Varsayılan**: Bu sağlayıcı için varsayılan hesap olarak ayarla (her sağlayıcı için yalnızca bir varsayılan)

### API Kimlik Bilgileri (Şifrelenmiştir)

**Sağlayıcıya göre değişir**, genellikle şunları içerir:

**FedEx**:
- Hesap Numarası
- Ölçüm Numarası
- API Anahtarı
- API Gizli

**UPS**:
- Erişim Lisans Numarası
- Kullanıcı Kimliği
- Şifre
- Hesap Numarası

**DHL**:
- Site Kimliği
- Şifre
- Hesap Numarası

**Tüm kimlik bilgileri dinlenirken şifrelenir** ve yalnızca API çağrıları yaparken şifrelenir.

### Köken Adresi

- **Varsayılan Gönderim**: Hesaplamalar için depo/köken adresi
- Bazı sağlayıcılar, kendi panellerinde özel köken ayarlamasını gerektirir

### Ayarlar

Sağlayıcıya özel seçenekler (kuryeye göre değişir):

- **Test Modu**: Kuryenin test ortamı/sandbox API uç noktalarını kullanın
- **Tahakkuk Edilen Ücretler**: Kuryenin tahakkuk edilen ücretlerini kullanın (eğer mevcutsa)
- **Sigorta Dahil**: Ücretlerde otomatik olarak sigorta teklifini dahil et
- **Konut Ücreti**: Konut teslimat ücretlerini uygula
- **İmza Gerekli**: Varsayılan imza gereklilikleri

---

## Sağlayıcı Hesabı Oluşturma

**6 Adımlı Kurulum Süreci**:

**Adım 1: Kurye API Erişimi Alın**
1. Kurye ile hesap oluşturun (FedEx.com, UPS.com, DHL.com)
2. API/Geliştirici erişimi için başvurun
3. Kuryenin API onboarding'ını tamamlayın (1-3 iş günü sürebilir)
4. API kimlik bilgilerini e-posta veya geliştirici portalı üzerinden alın

**Adım 2: Sağlayıcı Bileşenini Yükle** (önceden yüklü değilse)
1. Ayarlar > Bileşenler > Pazar Yeri'ne gidin
2. Kurye adını arayın (örneğin, "FedEx")
3. Gönderim sağlayıcısı bileşenini yükleyin
4. Yükleme tamamlanana kadar bekleyin

**Adım 3: Spwig'de Sağlayıcı Hesabı Oluşturun**
1. Ayarlar > Gönderim > Sağlayıcı Hesapları'na gidin
2. "Sağlayıcı Hesabı Ekle"yi tıklayın
3. Aşağı açılan listeden sağlayıcıyı seçin
4. Gösterim adını girin

**Adım 4: API Kimlik Bilgilerini Girin**
1. Kimlik bilgi alanlarını doldurun (sağlayıcıya göre değişir)
2. Kimlik bilgileri kaydedildiğinde otomatik olarak şifrelenir
3. Seçenek: Test modunu etkinleştirin (başlangıç testi için)

**Adım 5: Bağlantıyı Test Edin**
1. "Bağlantıyı Test Et" butonuna tıklayın
2. Sistem, kurye API'sına bir çağrı yapmaya çalışır
3. "Bağlandı" durumu görünür olduğunda doğrulayın
4. Son_tested_at zaman damgasını kontrol edin

**Adım 6: Gönderim Yöntemiyle Bağla**
1. Gönderim yöntemi oluşturun veya düzenleyin (Ayarlar > Sepet > Gönderim Yöntemleri)
2. method_type = "Gerçek Zamanlı" olarak ayarlayın
3. Aşağı açılan listeden sağlayıcı hesabını seçin
4. Yöntemi kaydedin

---

## Bağlantı Durumu İzleme

Sağlayıcı hesapları, bağlantı sağlıqlığını izler:

### Durum Değerleri

**Bilinmeyen** (gri): Asla test edilmediği ya da henüz bağlanmadığı

**Bağlandı** (yeşil): Son API çağrısı başarılı oldu, kimlik bilgileri geçerlidir

**Hata** (kırmızı): Son API çağrısı başarısız oldu, kimlik bilgileri geçersiz olabilir

### Son Test Edilen

- **Zaman Damgası**: Bağlantının son kez doğrulandığı zaman
- **Otomatik Güncellenme**: Sağlayıcı her kullanıldığında (ücret alımı, etiket satın alma)
- **El ile test**: Herhangi bir zaman "Bağlantıyı Test Et" butonuna tıklayın

### Bağlantı Hatası Giderme

**Sık Görülen Nedenler**:
- Yanlış API kimlik bilgileri (yazım hatası, fazladan boşlukla kopyalanmış)
- Kurye API anahtarının sona ermesi veya iptal edilmesi
- Test modu etkin ancak üretim kimlik bilgileri kullanılıyor (veya tam tersi)
- Kurye ile IP adresi beyaz listede değil
- Kurye API'si çökmesi

**Çözüm Adımları**:
1. Kimlik bilgilerinin kurye panosunda tam olarak eşleştiğini doğrulayın
2. Test modu ayarının kimlik bilgisi türüyle eşleştiğini kontrol edin
3. Kuryenin API durum sayfasını inceleyin
4. Kurye desteğini doğrulamak için kurye desteğini temasa geçin

---

## Ücret Arama Akışı

Ödeme sırasında gerçek zamanlı ücretler nasıl çalışır:

**1. Müşteri Adresini Girer**
- Gönderim adresi girilir
- Sepet toplam ağırlığı + boyutları hesaplar

**2. Sistem Ücret Talebi Hazırlar**
- Sağlayıcı hesap kimlik bilgilerini alır (şifrelenmiş)
- Sepet öğelerinden paket boyutlarını hesaplar (gönderim paketleri tanımlanmışsa kullanılır)
- Köken, hedef, paketlerle birlikte API isteğini hazırlar

**3. Sağlayıcı API'si Çağrılır**
- Kurye API'sine kimlik bilgileriyle istek gönderilir
- Kurye, bölge, ağırlık, boyutlara göre ücreti hesaplar
- Yanıt, hizmet seçeneklerini içerir (Ground, Express vb.)

**4. Ücretler Gösterilir**
- Sistem kurye yanıtını analiz eder
- Standart formatla normalleştirilir
- Seçenek olarak markup uygulanır (konfigüre edilmişse)
- Müşteriye ödeme sırasında ücretler gösterilir

**5. Müşteri Hizmeti Seçer**
- Müşteri tercih ettiği seçeneği seçer
- Seçilen ücret siparişe kaydedilir

**Örnek API Akışı**:
```
FedEx API'ye istek:
{
  "origin": {"postal_code": "90210", "country": "US"},
  "destination": {"postal_code": "10001", "country": "US"},
  "parcels": [{
    "weight": 2500,  // gram
    "dimensions": {"length": 30, "width": 20, "height": 15}  // cm
  }]
}

FedEx Yanıt:
[
  {"service": "FEDEX_GROUND", "rate": 12.50, "delivery_days": 5},
  {"service": "FEDEX_EXPRESS", "rate": 28.75, "delivery_days": 2}
]
```

---

## Etiket Satın Alma (Opsiyonel)

Eğer sağlayıcı etiket oluşturma destekliyorsa:

**Akış**:
1. Müşteri siparişi tamamlar
2. Satıcı, siparişi oluşturur (Siparişler > Sipariş Detayı > Sipariş Oluştur)
3. Sağlayıcı hesabı + hizmeti seçin
4. Sistem sağlayıcının etiket API'sini çağırır
5. Etiket PDF'si oluşturulur ve siparişe eklenir
6. Takip numarası otomatik olarak doldurulur
7. Etiket yazdırma hazırdır

**Avantajlar**:
- Kurye web sitesine manuel giriş yapmaya gerek yok
- Takip otomatik olarak senkronize edilir
- Uluslararası gönderimler için gümrük formları otomatik olarak oluşturulur
- Toplu etiket oluşturma mümkün

---

## Ücret Markup'u

Kurye ücretlerine satıcı markup'u ekleyin:

**Konfigürasyon** (gönderim yönteminde, sağlayıcı hesabında değil):
- **Markup Türü**: Yüzde veya Sabit
- **Markup Miktarı**: Örneğin, 15% veya $2.50

**Örnek**:
```
Kurye Ücreti: $12.50
Markup: 15%
Müşteri Öder: $14.38

YA DA

Kurye Ücreti: $12.50
Markup: $2.50 (sabit)
Müşteri Öder: $15.00
```

**Kullanım Durumları**:
- Ambalaj/İşleme maliyetlerini karşılamak
- Gönderimde kâr marjı eklemek
- Kredi kartı ücretlerini gönderebilirsiniz

---

## Birden Fazla Sağlayıcı Hesabı

Aynı sağlayıcı için birden fazla hesap oluşturabilirsiniz:

**Kullanım Durumları**:
1. **Test vs. Üretim**
   - Test Hesabı: Kurye test kimlik bilgileri
   - Üretim Hesabı: Canlı kimlik bilgileri

2. **Birden Fazla Depo**
   - A Depo Hesabı: Köken = Los Angeles
   - B Depo Hesabı: Köken = New York

3. **Farklı Tahakkuk Edilen Ücretler**
   - Hesap A: Standart ücretler
   - Hesap B: Hacim indirimli ücretler

**Her hesap, farklı gönderim yöntemlerine bağlanabilir** için esnek yapılandırma.

---

## İpuçları

- **Önce test ortamında test edin** - Canlı ortama geçmeden önce kurye test kimlik bilgilerini kullanın
- **Bağlantı durumunu izleyin** - Hata durumlarını düzenli olarak panoda kontrol edin
- **Gönderim paketlerini tanımlayın** - Doğru boyutlar ücret tekliflerini iyileştirir
- **Tahakkuk edilen ücretleri kullanın** - Kurye ile hacim indirimleri varsa etkinleştirin
- **Gerçekçi bir köken ayarlayın** - Gerçek gönderim adresini kullanarak doğru bölgeleri sağlayın
- **Kimlik bilgilerini güvenli tutun** - API anahtarlarını asla paylaşmayın, periyodik olarak döndürün
- **Yedek yöntem bulundurun** - Kurye API'si başarısız olursa sabit ücret yöntemi etkin tutun
- **Kurye API sınırlarını izleyin** - Bazı kuryeler günlük API çağrılarını sınırlar
- **Kimlik bilgilerini anında güncelleyin** - Kurye anahtarlarını döndürürse hemen güncelleyin
- **Açıklıkla ad kullanın** - "FedEx LA Depo" "FedEx 1"'den daha iyidir
