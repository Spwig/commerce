---
title: Sadakat Kampanyaları
---

Sadakat kampanyaları, günlük kazanç kurallarınızın ötesine geçen, zaman sınırlı promosyonlar ve otomatik ödüllendirme sağlar. Onları hafta sonları iki kat puan kazandırmak, müşterilerin doğum günlerinde ödüllendirmek, pasif alışverişçileri geri kazanmak ve belirli üyeler grubuna hedefli bonuslar sunmak için kullanabilirsiniz.

Her kampanya, tetikleyici veya zamanlama, uygulanacağı üyeler ve alınacak eylemleri tanımlar. Aktif hale geldikten sonra kampanyalar otomatik olarak tetiklenir — bir kez ayarladığınızda Spwig geri kalanını yönetir.

## Kampanya Türleri

| Tür | Ne Zaman Tetiklenir |
|-----|---------------------|
| **Tetikleyiciye Dayalı** | Belirli bir olay gerçekleştiğinde (örneğin, bir sipariş verildiğinde, bir doğum günü tespit edildiğinde) |
| **Zamanlanmış** | Tekrar eden bir zamanlamada (günlük, haftalık, aylık) |
| **El ile** | Sadece admin panelinden açıkça çalıştırıldığında |
| **Davranışsal** | Bir müşteri belirli bir davranış örüntüsüne uydugunda (örneğin, alışveriş yapmadan tarifelendirme) |

## Kampanya Oluşturma

**Promosyonlar > Sadakat Kampanyaları**'na gidin ve **+ Sadakat Kampanyası Ekle**'ye tıklayın.

### Adım 1: Temel Bilgiler

- **Ad** — sadece admin panelinde görünen, açıklayıcı bir isim (örneğin, `Doğum Günü Bonusu — 200 Puan`)
- **Slug** — isimden otomatik olarak oluşturulur; iç kullanımda kullanılır
- **Açıklama** — kampanyanın amacına dair isteğe bağlı notlar
- **Kampanya Türü** — yukarıdaki tablodan bir tür seçin

### Adım 2: Tetikleyici veya Zamanlama

**Tetikleyiciye Dayalı Kampanyalar** için, kampanyanın tetikleneceği **Tetikleyici Olay**'ı ayarlayın. Kullanılabilir tetikleyiciler şunlardır:

| Tetikleyici | Açıklama |
|-------------|----------|
| Sipariş Verildi | Üyeler bir sipariş tamamladığında tetiklenir |
| İlk Sipariş | Üyenin ilk siparişi olduğunda tetiklenir |
| Müşteri Doğum Günü | Üyenin doğum gününde tetiklenir |
| Üyelik Yıldönümü | Üyenin katıldığı yıldönümünde her yıl tetiklenir |
| Sepet Bırakıldı | Sepet ödeme olmadan bırakıldığında tetiklenir |
| Seviye Promosyonu | Üye daha yüksek bir seviyeye geçtiğinde tetiklenir |
| Puanlar Yakında Bitiyor | Üye puanlarının yakında bitmesi durumunda tetiklenir |
| 90 Gün Aktif Değil | Üye 90 gün içinde alışveriş yapmamışsa tetiklenir |
| Değerlendirme Gönderildi | Üye bir ürün değerlendirmesi gönderdiğinde tetiklenir |
| Referans Verilen Müşteri | Referans verilen müşteri bir alışveriş yaparsa tetiklenir |

Kampanyanın ne zaman tetikleneceğini daha da filtrelemek için **Tetikleyici Koşulları** olarak bir JSON nesnesi ekleyebilirsiniz. Örneğin, sadece 100 doların üzerindeki siparişler için tetiklemek istiyorsanız:

```json
{
  "min_order_amount": 100
}
```

**Zamanlanmış Kampanyalar** için, **Zamanlama Türü**'nü (Günlük, Haftalık, Aylık veya Özel Cron) ve **Zamanlama Yapılandırması** alanındaki zamanlamayı ayarlayın:

```json
{
  "hour": 9,
  "minute": 0
}
```

### Adım 3: Eylemler

**Eylemler** alanı, kampanya tetiklendiğinde ne olacağını tanımlar. Eylem nesneleri içeren bir JSON dizi girin. En yaygın eylem, bonus puan vermek:

```json
[
  {
    "type": "award_points",
    "points": 200,
    "description": "Doğum günü bonusu — üyeniz olmanız için teşekkür ederiz!"
  }
]
```

Diğer kullanılabilir eylemler arasında bir e-posta bildirimi göndermek veya bir madalya vermek yer alır. Tam liste için sağlayıcınızın bileşen belgesine bakın.

### Adım 4: Hedefleme

Kampanyanın hangi üyeler üzerinde çalışacağını hedefleme alanlarını kullanarak kontrol edin:

- **Tüm Üyeleri Hedefle** — varsayılan olarak işaretli; kampanya her aktif sadakat üyesine uygulanır
- **Segmenti Hedefle** — kampanyayı belirli bir segmentteki üyelerle sınırlayın (aşağıdaki [Segmentler](#managing-member-segments) bölümüne bakın)
- **Seviyeyi Hedefle** — kampanyayı belirli sadakat seviyelerindeki üyelerle sınırlayın

### Adım 5: Sınırlar ve Soğuma Süreleri

- **Üyeye Ait Maksimum Tetikleyiciler** — aynı üyenin bu kampanyadan ne kadar fazla yararlanabileceği. Bir doğum günü ödüllendirme gibi tek seferlik bonuslar için `1` olarak ayarlayın. Boş bırakın sınırsız olacak şekilde.
- **Soğuma Günleri** — aynı üyenin kampanya tetikleyicileri arasında geçen minimum gün sayısı. Örneğin, `365` olarak ayarlayarak bir doğum günü kampanyasının yılda bir kez tetiklenmesini önleyebilirsiniz.

### Adım 6: Kampanya Tarihleri

**Başlangıç Tarihi** ve **Bitiş Tarihi**'ni ayarlayarak kampanyayı zaman sınırlı hale getirin. Her ikisini de boş bırakın, kampanya devam eder.


Kampanyalar şu durumlardan birinde olabilir:

| Durum | Açıklama |
|--------|-------------|
| **Taslak** | Oluşturuldu ancak henüz etkin değil; yapılandırıp test etmek güvenlidir |
| **Etkin** | Çalışıyor ve koşullar karşılandığında tetiklenir |
| **Durduruldu** | Yapılandırma kaybolmadan geçici olarak durduruldu |
| **Bitti** | Bitiş tarihi geçmiş; artık tetiklenmez |
| **Arşivlendi** | Etkin listeden gizlenmiş ancak kayıtlar için korunuyor |

Tüm alanları doldurduktan sonra **Kaydet**'e tıklayın. Ardından kampanyayı başlatmak için durumu **Etkin** olarak değiştirin.

## Uygulamalı örnekler

### Örnek: Hafta sonu çift puan

**Senaryo:** Belirli bir hafta sonu sırasında yapılan tüm alışverişlere 2x puan verin.

| Alan | Değer |
|-------|-------|
| Ad | `Double Points Weekend — March` |
| Kampanya Türü | Tetikleyiciye Dayalı |
| Tetikleyici Olay | Sipariş Verildi |
| Eylemler | `["{\"type\": \"award_points_multiplier\", \"multiplier\": 2.0}"]` |
| Başlangıç Tarihi | Cuma akşamı |
| Bitiş Tarihi | Pazar gece yarısı |
| Tüm Üyeleri Hedefle | İşaretli |

### Örnek: Doğum gününde bonus

**Senaryo:** Her loyallik üyesine doğum gününde 200 bonus puan verin.

| Alan | Değer |
|-------|-------|
| Ad | `Birthday Bonus` |
| Kampanya Türü | Tetikleyiciye Dayalı |
| Tetikleyici Olay | Müşteri Doğum Günü |
| Eylemler | `["{\"type\": \"award_points\", \"points\": 200, \"description\": \"Happy birthday from us!\"}"]` |
| Üye Başına Maksimum Tetikleme | 1 |
| Soğuma Günü | 365 |
| Tüm Üyeleri Hedefle | İşaretli |

### Örnek: Geri kazanma kampanyası

**Senaryo:** 90 gün satın almamış üyelerin 100 bonus puanı gönderin.

| Alan | Değer |
|-------|-------|
| Ad | `90-Day Win-Back Bonus` |
| Kampanya Türü | Tetikleyiciye Dayalı |
| Tetikleyici Olay | 90 Gün Aktif Değil |
| Eylemler | `["{\"type\": \"award_points\", \"points\": 100, \"description\": \"We miss you — here are some bonus points\"}"]` |
| Üye Başına Maksimum Tetikleme | 1 |
| Soğuma Günü | 180 |
| Tüm Üyeleri Hedefle | İşaretli |

## Üye segmentlerini yönetme

Segmentler, loyallik üyelerinin belirli gruplarına kampanyaları hedeflemene olanak tanır. **Promosyonlar > Loya Segmentleri**'ne giderek bunları yönetin.

### Segment türleri

| Tür | Açıklama |
|------|-------------|
| **Kurallara Dayalı** | Üyelik, kurallar tarafından belirlenir (örneğin, 1.000 puanın üzerindeki üyeler) |
| **Dinamik Hesaplama** | Üyelik, gerçek zamanlı kriterlerden talep üzerine hesaplanır |
| **Elle Atama** | Üyeler segmente elle eklenir |

### Segment oluşturma

1. **Promosyonlar > Loya Segmentleri**'ne gidin ve **+ Loya Segmenti Ekle**'ye tıklayın
2. Aşağıdakileri doldurun:
   - **Ad** — açıklayıcı bir ad (örneğin, `Yüksek Değerli Müşteriler`, `Gümüş Sınıf Üyeleri`)
   - **Slug** — otomatik olarak oluşturulur
   - **Kriter Türü** — üyelik nasıl belirlendiğini belirtir
   - **Kriter Yapılandırması** — üyelik kurallarını tanımlayan JSON nesnesi
3. **Kaydet**'e tıklayın

#### Örnek: 500+ puanlı üyeler için segment

```json
{
  "min_available_points": 500
}
```

#### Örnek: Sadece Altın sınıf üyeler için segment

```json
{
  "tier_slugs": ["gold"]
}
```

Segment listesindeki **Üye Sayısı** sütunu, şu anda eşleşen üye sayısını gösterir. Bir segmenti açın ve verileriniz değiştiyse **Üye Sayısını Yeniden Hesapla** eylemini kullanarak yeniden hesaplayabilirsiniz.

## Kampanya performansını izleme

### Kampanya yürütme geçmişi

**Promosyonlar > Kampanya Yürütme Geçmişi**'ne giderek, herhangi bir üyenin için bir kampanyanın kaç kez tetiklendiğini görebilirsiniz. Her yürütme kaydı, hangi kampanyanın çalıştığını, hangi üyeye çalıştığını ve sonucu gösterir.

### Kampanya erişimini inceleme

Herhangi bir kampanya kaydını açarak **Tetiklenme Sayısı** sayısını ve kampanyanın son tetiklendiği zamanı görebilirsiniz. Bu, kampanyadan yararlanan üye sayısına hızlı bir bakış sunar.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Taslak** durumunda kampanyalar oluşturun, böylece kampanyalar canlı hale gelmeden önce tüm ayarları inceleyebilirsiniz
- **Üyenin Başına En Fazla Tetikleyici** özelliğini bir kezlik bonus kampanyalarında (doğum günü, ilk satın alma, kayıt) kullanın, böylece müşterilerin bonusu birden fazla kez kazanmasını önleyebilirsiniz
- **Hedef Segment** ile tetikleyiciye dayalı bir kampanyayı birleştirerek kat seviyesine özel promosyonlar çalıştırın — örneğin, Altın ve Platin üyeler için yalnızca satın almalar üzerinde çift puan
- Geri dönüş kampanyalarında **Soğuma Günleri** değerini ayarlayın, böylece üyeler küçük bir satın alma yaptıktan sonra kısa sürede tekrar aktif olmazlarsa, onlara yoğun şekilde ulaşılmasını önleyebilirsiniz
- Kampanya listesi, şu anda etkin olan promosyonları takip etmenin en iyi aracıdır — yeni teklifler başlatmadan önce onu inceleyin, böylece kampanyaların bilinçsiz olarak üst üste binmesini önleyebilirsiniz
- Bitmiş kampanyaları silmek yerine arşivleyin, böylece ne tür promosyonlar gerçekleştirdiğiniz ve ne zaman yaptığınızla ilgili bir tarihî kayda sahip olursunuz