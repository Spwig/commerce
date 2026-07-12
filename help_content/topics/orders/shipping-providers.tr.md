---
title: Kargo Sağlayıcıları
---

Kargo sağlayıcıları, mağazanızı canlı kargo ücretleri, etiket oluşturma ve paket takibi için taşıyıcı API'leriyle bağlar. Spwig, dünya çapında büyük taşıyıcıları destekler ve API entegrasyonu olmayan taşıyıcılar için el ile ücret tabloları oluşturmanıza da olanak tanır.

![Kargo sağlayıcıları](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Mevcut Taşıyıcılar

| Taşıyıcı | Bölgeler | Ana Özellikler |
|---------|---------|-------------|
| **FedEx** | Global | Canlı ücretler, etiket basımı, takip, çoklu paket |
| **UPS** | Global | Canlı ücretler, etiket basımı, takip, adres doğrulama |
| **USPS** | ABD | Yurtiçi ve yurtdışı ücretler, takip |
| **NinjaVan** | Güneydoğu Asya | Son kilometre teslimatı, nakit ile ödeme desteği |
| **Canada Post** | Kanada | Yurtiçi ve yurtdışı, paket ve mektup ücretleri |
| **Australia Post** | Avustralya | Yurtiçi ve yurtdışı, paket ve hızlı teslimat |

## Taşıyıcıyı Bağlama

**Ayarlar > Kargo Sağlayıcıları**'na gidin ve **Sağlayıcıyı Bağla**'ya tıklayarak kurulum asistanını başlatın.

### Adım 1: Sağlayıcıyı Seçin

Mevcut kargo taşıyıcılarından birini seçin. Her kart, taşıyıcının desteklediği bölgeleri ve özellikleri gösterir.

### Adım 2: Kurulum Talimatları

Taşıyıcıya özel kurulum kılavuzunu inceleyin:
- Taşıyıcı ile geliştirici/şirket hesabı nasıl oluşturulur
- API kimlik bilgilerinizi nereden bulursunuz
- Gerekli hesap ayarları (örneğin, gönderici numarası, metre numarası)

### Adım 3: Kimlik Bilgilerini Girin

Taşıyıcı hesabınız için API kimlik bilgilerini girin. Gerekli alanlar taşıyıcıya göre değişir:

- **API Anahtar / Gizli** — Kimlik doğrulama bilgileri
- **Hesap Numarası** — Taşıyıcı hesabınız veya gönderici numaranız
- **Metre Numarası** — Bazı taşıyıcılar tarafından gereklidir (örneğin, FedEx)
- **Deneme Modu** — Canlı karga öncesi taşıyıcının deneme API'siyle test etmek için etkinleştirin

### Adım 4: Bağlantıyı Test Etme

**Bağlantıyı Test Et**'e tıklayarak kimlik bilgilerinizi doğrulayın. Asistan şu noktaları onaylar:
- API kimlik doğrulaması başarılı
- Hesap izinleri geçerlidir
- Ücret sorguları beklenen sonuçları döndürür

### Adım 5: Yapılandır ve Kaydet

Ayarları tamamlayın:
- **Aktif** — Taşıyıcıyı etkinleştirin veya devre dışı bırakın
- **Gösterilecek Ad** — Müşterilere ödeme sırasında gösterilen ad
- **Kaynak Adresi** — Ücret hesaplamaları için depo veya teslimat adresi

## Kargo Bölgeleri

Kargo bölgeleri, ücret hesaplamaları için coğrafi alanları tanımlar. **Ayarlar > Kargo Bölgeleri**'ne gidin ve bunları yönetin.

### Bölge Oluşturma

1. **+ Bölge Ekle**'ye tıklayın
2. Bölüğe bir isim verin (örneğin, "Yurtiçi", "Avrupa", "Asya Pasifik")
3. Bölgenin kapsamını tanımlamak için bir veya daha fazla öğeyi kullanın:
   - **Ülkeler** — Belirli ülkeleri seçin
   - **Eyaletler/İlçeler** — Bir ülkenin belirli bölgelerine daraltın
   - **Posta Kodu Desenleri** — Posta/ZIP kodlarını desenlerle eşleştirmek için kullanın (örneğin, "90*" Los Angeles bölgesi için)
4. **Öncelik** ayarlayın — Bölgeler çakıştığında en yüksek öncelikli bölge kullanılır

### Bölge Eşleşmesi

Müşteri ödeme sırasında kargo adresini girerse, sistem:
1. İlk olarak posta kodu desenlerini kontrol eder (en spesifik)
2. Ardından eyalet/iller eşleşmelerini kontrol eder
3. Ardından ülke eşleşmelerini kontrol eder
4. En yüksek öncelikli eşleşen bölgeyi kullanır

## Kargo Kampanyaları

Kargo kampanyaları, kargo ücretlerine koşullu değişiklikler uygular. **Ayarlar > Kargo Kampanyaları**'na gidin ve bunları yapılandırın.

### Kampanya Türleri

| Kampanya Türü | Açıklama |
|-----------|-------------|
| **İndirim %** | Kargo ücretini bir yüzde oranında azaltın |
| **İndirim Sabit** | Kargo ücretini sabit bir miktarda azaltın |
| **Ücreti Geçersiz Kıl** | Ücreti belirli bir miktara geçersiz kılın |
| **Ücretsiz Kargo** | Kargo ücretini sıfıra ayarlayın |
| **İlave Ücret %** | Ücretin üzerine bir yüzde ek ücret ekleyin |
| **İlave Ücret Sabit** | Ücretin üzerine sabit bir ek ücret ekleyin |

### Koşullar

Her kampanya, karşılanması gereken bir veya daha fazla koşula sahip olabilir:

| Şart | Örnek |
|-----------|---------|
| **Sepet Değeri** | 100 $'a ulaşan siparişlerde ücretsiz kargo |
| **Toplam Ağırlık** | 30 kg'ı geçen siparişler için ek ücret |
| **Ürün Sayısı** | 5+ ürün içeren siparişler için indirim |
| **Kargo Bölgesi** | Yalnızca yerel kargo kampanyasına uygula |
| **Kargo Yöntemi** | Belirli taşıyıcı yöntemlerine uygula |
| **Ürünler** | Belirli ürünler için özel oranlar |
| **Müşteri Grubu** | VIP müşterilere ücretsiz kargo |
| **Tarih Aralığı** | Tatil kargo kampanyaları |

### Kampanya Önceliği

- Kampanyalar öncelik sırasına göre değerlendirilir (en düşük sayıdan başlanır)
- **Diğer Kampanyaları Durdur** — Etkinleştirildiğinde bu kampanya uymazsa, diğer kampanyalar kontrol edilmez
- Birden fazla kampanya üst üste kullanılabilir (örneğin, 10% indirim kampanyası ve ücretsiz kargo eşik kampanyası)

## Oran Tabloları

Oran tabloları, sipariş özniteliklerine göre katmanlı fiyatlandırma sağlar. **Ayarlar > Kargo Oran Tabloları**'na giderek bunları yapılandırabilirsiniz.

### Tablo Türleri

Aşağıdakilere göre oran katmanları oluşturun:
- **Ağırlık** — Toplam sipariş ağırlığına göre fiyat katmanları (örneğin, 0-1 kg = 5 $, 1-5 kg = 10 $)
- **Sipariş Değeri** — Sepet alt toplamına göre fiyat katmanları
- **Miktar** — Ürün sayısına göre fiyat katmanları

### Oran Tablosu Oluşturma

1. **+ Oran Tablosu Ekle**'ye tıklayın
2. Tabloyu isimlendirin ve katman türünü seçin
3. Min/max aralıklarını ve fiyatları ekleyin
4. Oran tablosunu bir kargo bölgesine atayın

Oran tabloları, taşıyıcı API oranlarını kullanmadığınızda ve kendi fiyatlandırma yapısınızı tanımlamak istediğinizde yararlıdır.

## Kargo Paketleri

Doğru oran hesaplamaları için standart paket boyutlarını tanımlayın. **Ayarlar > Kargo Paketleri**'ne gidin.

Her paket türü için ayarlayın:
- **Ad** — Açıklama (örneğin, "Küçük Kutu", "Büyük Sabit Fiyat")
- **Boyutlar** — Uzunluk, genişlik, yükseklik
- **Maksimum Ağırlık** — Paketin taşıyabileceği maksimum ağırlık
- **Varsayılan** — Belirli bir paket atamadan bu paketi kullan

Taşıyıcılar, boyut ağırlığı hesaplamaları için paket boyutlarını kullanır, bu da kargo ücretlerini etkileyebilir.

## Manuel Taşıyıcılar (Taşıyıcı Ön Ayarları)

API entegrasyonu olmayan taşıyıcılar için manuel taşıyıcı ön ayarları oluşturun:

1. **Ayarlar > Taşıyıcı Ön Ayarları**'na gidin
2. **+ Ön Ayar Ekle**'ye tıklayın
3. Yapılandırın:
   - **Taşıyıcı Adı** — Ödeme sırasında görüntülenecek ad
   - **İzleme URL Şablonu** — {tracking_number} yer tutuculu bir URL kalıbı (örneğin, `https://track.carrier.com/?id={tracking_number}`)
   - **Tahmini Teslimat** — Müşterilere gösterilecek teslimat zaman aralığı
4. Fiyatlandırma için bir oran tablosuyla eşleştirin

Manuel taşıyıcılar, canlı API entegrasyonu olmadan izleme bağlantıları ve teslimat tahmini sağlar.

## Çok Depolı Kargo

Birden fazla depoysanız, kargo farklı kaynaklardan hesaplanabilir:

- **Ülke Özel Depo** — Belirli ülkelere kısa kargo mesafesi için depolar atayın
- **Yedekleme Zinciri** — Başlıca depo stokta olmadığında hangi depo gönderileceğini tanımlayın
- **Ürün Bazlı Atama** — Bazı ürünler yalnızca belirli depolardan gönderilebilir

Sistem, müşteri konumu ve ürün mevculuğu temelinde en iyi depoyu otomatik olarak seçer.

## İpuçları

- Mümkün olduğunca taşıyıcı API'lerini **canlı oranlar** için bağlayın — bunlar düz oran tablolarından daha doğru olur ve ağırlık, boyutlar ve hedefe göre ayarlanır.
- **Dünya Genelinde** adında bir kargo bölgesi oluşturun — belirli bölgeleri kapsayan olmayan ülkeler için bir yakalama olarak kullanın.
- Satış teşvikleri için **Ücretsiz Kargo** kampanya türünü sepet değeri koşuluyla kullanın (örneğin, "75 $'a ulaşan siparişlerde ücretsiz kargo").
- Canlıya geçmeden önce farklı adresler ve sepet içerikleriyle kargo oranlarını test edin.
- API entegrasyonu olmayan yerel taşıyıcılar için **Taşıyıcı Ön Ayarları**'nı ayarlayın — müşteriler hala izleme bağlantıları alır.
- **Kargo Paketleri**'ni kullanarak FedEx ve UPS gibi taşıyıcılarla boyut ağırlığı fiyatlandırmasını doğru şekilde alın.