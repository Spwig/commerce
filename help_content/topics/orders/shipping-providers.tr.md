---
title: Kargo Sağlayıcıları
---

Kargo sağlayıcıları mağazanızı taşıyıcı API'leriyle bağlar ve canlı kargo fiyatlarını, etiket oluşturma ve paket takibi gibi işlevleri sağlar. Spwig, dünya çapında büyük taşıyıcıları destekler ve API entegrasyonu olmayan taşıyıcılar için el ile fiyat tabloları oluşturmanıza olanak tanır.

![Kargo sağlayıcıları](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Mevcut Taşıyıcılar

| Taşıyıcı | Bölgeler | Ana Özellikler |
|---------|---------|-------------|
| **FedEx** | Küresel | Canlı fiyatlar, etiket basımı, takip, çoklu paket |
| **UPS** | Küresel | Canlı fiyatlar, etiket basımı, takip, adres doğrulama |
| **USPS** | Amerika Birleşik Devletleri | Yerel ve uluslararası fiyatlar, takip |
| **NinjaVan** | Güneydoğu Asya | Son kilometre teslimatı, nakit ile ödeme desteği |
| **Canada Post** | Kanada | Yerel ve uluslararası, paket ve mektup fiyatları |
| **Australia Post** | Avustralya | Yerel ve uluslararası, paket ve kargo |

## Taşıyıcıyı Bağlama

**Ayarlar > Kargo Sağlayıcıları**'na gidin ve **Sağlayıcıyı Bağla**'ya tıklayarak kurulum asistanını başlatın.

### Adım 1: Sağlayıcıyı Seç

Mevcut kargo taşıyıcılarından birini seçin. Her kart, taşıyıcının desteklediği bölgeleri ve özellikleri gösterir.

### Adım 2: Kurulum Talimatları

Taşıyıcıya özel kurulum kılavuzunu gözden geçirin:
- Taşıyıcı ile geliştirici/şirket hesabı nasıl oluşturulur
- API kimlik doğrulama bilgilerinizi nereden alınır
- Gerekli hesap ayarları (örneğin, gönderici numarası, ölçüm numarası)

### Adım 3: Kimlik Doğrulama Bilgilerini Girin

Taşıyıcı hesabınız için API kimlik doğrulama bilgilerini girin. Gerekli alanlar taşıyıcıya göre değişebilir:

- **API Anahtar / Gizli** — Kimlik doğrulama bilgileri
- **Hesap Numarası** — Taşıyıcı hesabınız veya gönderici numaranız
- **Ölçüm Numarası** — Bazı taşıyıcılar tarafından gereklidir (örneğin, FedEx)
- **Kumanda Modu** — Canlı olarak geçmeden önce taşıyıcının kumanda API'siyle test etmek için etkinleştirin

### Adım 4: Bağlantıyı Test Et

**Bağlantıyı Test Et**'e tıklayarak kimlik doğrulamanızı doğrulayın. Asistan aşağıdaki şeyleri onaylar:
- API kimlik doğrulaması başarılı
- Hesap izinleri geçerlidir
- Fiyat sorguları beklenen sonuçları döndürür

### Adım 5: Yapılandır ve Kaydet

Ayarları tamamlayın:
- **Etkin** — Taşıyıcıyı etkinleştirmek veya devre dışı bırakmak
- **Gösterilen Ad** — Ödeme sırasında müşterilere gösterilen ad
- **Köken Adresi** — Fiyat hesaplamaları için depo veya teslimat adresi

## Kargo Bölgeleri

Kargo bölgeleri, fiyat hesaplamaları için coğrafi alanları tanımlar. **Ayarlar > Kargo Bölgeleri**'ne giderek bunları yönetin.

### Bölge Oluşturma

1. **+ Bölge Ekle**'ye tıklayın
2. Bölgenin bir ismi verin (örneğin, "Yerel", "Avrupa", "Asya Pasifik")
3. Bölgenin kapsamını bir veya daha fazla kural ile tanımlayın:
   - **Ülkeler** — Belirli ülkeleri seçin
   - **İlçeler/İl Statleri** — Bir ülkenin belirli bölgelerini daraltın
   - **Posta Kodu Desenleri** — Posta/ZIP kodlarını desenlerle eşleştirmek için (örneğin, "90*" Los Angeles bölgesi için)
4. **Öncelik** ayarlayın — Bölgeler çakıştığında en yüksek öncelikli bölge kullanılır

### Bölge Eşleşmesi

Müşteri ödeme sırasında kargo adresini girdiğinde sistem:
1. İlk olarak posta kodu desenlerini kontrol eder (en spesifik)
2. Ardından ilçeler/iller eşleşmesi
3. Ardından ülke eşleşmesi
4. En yüksek öncelikli eşleşen bölgeyi kullanır

## Kargo Kuralları

Kargo kuralları, kargo fiyatlarına koşullu değişiklikler uygular. **Ayarlar > Kargo Kuralları**'na giderek bunları yapılandırın.

### Kural Türleri

| Kural Türü | Açıklama |
|-----------|-------------|
| **İndirim %** | Kargo fiyatını bir yüzde oranında azaltın |
| **İndirim Sabit** | Kargo fiyatını sabit bir miktarda azaltın |
| **Fiyatı Ayarla** | Fiyatı belirli bir miktara göre geçersiz kılın |
| **Ücretsiz Kargo** | Kargo ücretini sıfıra ayarla |
| **İkramiye %** | Fiyata bir yüzde ikramiyesi ekleyin |
| **İkramiye Sabit** | Fiyata sabit bir ikramiye ekleyin |

### Koşullar

Her kural, karşılanması gereken bir veya daha fazla koşula sahip olabilir:

| Koşul | Örnek |
|-----------|---------|
| **Sepet Değeri** | 100 $'lık siparişlerde ücretsiz kargo |
| **Toplam Ağırlık** | 30 kg'dan fazla siparişler için ikramiye |
| **Ürün Sayısı** | 5 veya daha fazla ürün için indirim |
| **Kargo Bölgesi** | Yalnızca yerel gönderimler için kural uygula |
| **Kargo Yöntemi** | Belirli taşıyıcı yöntemlerine uygula |
| **Ürünler** | Belirli ürünler için özel fiyatlar |
| **Müşteri Grubu** | VIP müşterilere ücretsiz kargo |
| **Tarih Aralığı** | Tatil kargo teklifleri |

### Kural Önceliği

- Kurallar öncelik sırasına göre değerlendirilir (en düşük numaradan başlanır)
- **Daha Fazla Kural Durdur** — Etkinleştirildiğinde bu kural eşleşirse, diğer kurallar kontrol edilmez
- Birden fazla kural üst üste gelebilir (örneğin, 10% indirim kuralı ile ücretsiz kargo eşik kuralı)

## Fiyat Tabloları

Fiyat tabloları, sipariş özniteliklerine göre katmanlı fiyatlandırma sağlar. **Ayarlar > Kargo Fiyat Tabloları**'na giderek bunları yapılandırın.

### Tablo Türleri

Aşağıdakiler temelinde fiyat katmanları oluşturun:
- **Ağırlık** — Toplam sipariş ağırlığına göre fiyat katmanları (örneğin, 0-1 kg = 5 $, 1-5 kg = 10 $)
- **Sipariş Değeri** — Sepet alt toplamına göre fiyat katmanları
- **Miktar** — Ürün sayısına göre fiyat katmanları

### Fiyat Tablosu Oluşturma

1. **+ Fiyat Tablosu Ekle**'ye tıklayın
2. Tabloyu isimlendirin ve katman türünü seçin
3. Min/max aralıklarını ve fiyatları ekleyin
4. Fiyat tablosunu bir kargo bölgesine atayın

Fiyat tabloları, taşıyıcı API fiyatları kullanmadığınızda ve kendi fiyatlandırma yapısınızı tanımlamak istediğinizde faydalıdır.

## Kargo Paketleri

Doğru fiyat hesaplamaları için standart paket boyutlarını tanımlayın. **Ayarlar > Kargo Paketleri**'ne gidin.

Her paket türü için ayarlayın:
- **Ad** — Açıklama (örneğin, "Küçük Kutu", "Büyük Sabit Fiyat")
- **Boyutlar** — Uzunluk, genişlik, yükseklik
- **Maksimum Ağırlık** — Paketin taşıyabileceği maksimum ağırlık
- **Varsayılan** — Belirli bir paket atamadığınızda bu paketi kullanın

Taşıyıcılar, boyut ağırlık hesaplamaları için paket boyutlarını kullanır, bu da kargo fiyatlarını etkileyebilir.

## Manuel Taşıyıcılar (Taşıyıcı Ayarları)

API entegrasyonu olmayan taşıyıcılar için el ile taşıyıcı ayarları oluşturun:

1. **Ayarlar > Taşıyıcı Ayarları**'na gidin
2. **+ Ayar Ekle**'ye tıklayın
3. Yapılandırın:
   - **Taşıyıcı Adı** — Ödeme sırasında gösterilen ad
   - **Takip URL Şablonu** — {tracking_number} yer tutuculu bir URL deseni (örneğin, `https://track.carrier.com/?id={tracking_number}`)
   - **Tahmini Teslimat** — Müşterilere gösterilecek teslimat zaman aralığı
4. Fiyatlandırma için bir fiyat tablosuyla eşleştirin

Manuel taşıyıcılar, canlı API entegrasyonu olmadan takip linkleri ve teslimat tahmini sağlar.

## Çoklu Depo Kargo

Birden fazla depoınız varsa, kargo farklı kökenlerden hesaplanabilir:

- **Ülkeye Özel Depo** — Belirli ülkelere kısa kargo mesafesi için depoları atayın
- **Yedek Zinciri** — Temel depo stokta olmadığında hangi depo gönderim yapacak şekilde tanımlayın
- **Ürün Bazlı Atama** — Bazı ürünler yalnızca belirli depolardan gönderilebilir

Sistem, müşteri konumu ve ürün mevcudiyetine göre en iyi depoyu otomatik olarak seçer.

## İpuçları

- Olası durumlarda taşıyıcı API'leri için **canlı fiyatlar** kullanın — Bunlar sabit fiyat tablolarından daha doğru ve ağırlık, boyut ve hedefe göre ayarlanır.
- Belirli bölgeleri kapsayan bölgelerin dışında kalan ülkeler için **"Dünya Diğerleri"** kargo bölgesi oluşturun.
- **Ücretsiz Kargo** kural türünü sepet değeri koşuluyla kullanarak satış teşviki sağlayın (örneğin, "75 $'lık siparişlerde ücretsiz kargo").
- Canlıya geçmeden önce farklı adresler ve sepet içerikleriyle kargo fiyat hesaplamalarını test edin.
- Herhangi bir yerel taşıyıcı için API entegrasyonu olmayan taşıyıcılar için **Taşıyıcı Ayarları**'nı, {tracking_number} yer tutuculu bir URL şablonuyla oluşturun — müşteriler hala takip linkleri alır.
- **Kargo Paketleri**'ni kullanarak FedEx ve UPS gibi taşıyıcılardan boyut ağırlık fiyatlandırmasını alın.