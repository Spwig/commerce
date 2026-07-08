---
title: İade Talepleri & İşleme
---

İade talepleri, müşteri tarafından başlatılan iade sürecini tamamlanana kadar izler—müşteriler, iade etmek istediği ürünleri ve nedenleri seçer, satıcılar talepleri onaylar veya reddeder, iade etiketleri oluşturur, iade edilen ürünleri inceleyerek ve iadeleri işler. İşlem, 9 durum aşamasından (beklemede → onaylandı → etiket gönderildi → yolda → alındı → inceleme yapıldı → tamamlandı/rededildi/iptal edildi) geçer, ürün seviyesinde iade nedenleri, inceleme notları ve isteğe bağlı tekrar stoklama ücretleri içerir.

Bu yönetici sayfasını, müşteri iade taleplerini etkili bir şekilde incelemek, onaylamak ve işlemek için kullanın.

## İade Talebi İşlemi

**9 Aşamalı Süreç**:

### 1. Beklemede (Müşteri Başlatır)

Müşteri iade talebi sunar:
- Siparişten ürünleri seçer
- Ürün başına iade nedenini sağlar
- Müşteri notları (isteğe bağlı)
- Durum: `beklemede`

### 2. Onaylandı/Reddedildi (Satıcı İnceleme)

Satıcı talebi inceleyebilir:
- **Onayla**: İade izin verilir, etiket oluşturmana devam et
- **Reddet**: İade reddedilir ve reddetme nedeni belirtilir
- Durum: `onaylandı` veya `reddedildi`

### 3. Etiket Gönderildi (İade Sevkiyatı)

İade etiketi oluşturulur:
- Satıcı, iade sevkiyatı oluşturur (isteğe bağlı)
- İade etiketi müşteriye e-posta ile gönderilir
- Müşteri ürünleri geri gönderir
- Durum: `etiket gönderildi`

### 4. Yolda (Müşteri Gönderir)

Müşteri ürünleri gönderir:
- Takip, hareketi gösterir
- Taşıyıcı webhook'larından otomatik durum güncellemesi
- Durum: `yolda`

### 5. Alındı (Depoya Ulaşıldı)

Ürünler ulaşır:
- Depo, sevkiyatı tarar
- Ürünler kaydedilir
- Durum: `alındı`

### 6. İnceleme Yapıldı (Kalite Kontrolü)

Satıcı ürünleri inceleyebilir:
- Ürün durumunu kaydet (mükemmel/iyi/kabul edilebilir/hasarlı/arızalı)
- İnceleme notları ekleyin
- Gerekirse tekrar stoklama ücreti uygulayın
- Durum: `inceleme yapıldı`

### 7. Tamamlandı (İade İşlemi Yapıldı)

İade oluşturuldu:
- İlişkili iade oluşturun
- Ödeme işlemi yapılır
- İade kapatılır
- Durum: `tamamlandı`

**Alternatif Sonuçlar**:
- **İptal edildi**: Müşteri göndermeden önce iptal eder
- **Reddedildi**: Satıcı incelemeye göre reddeder

---

## İade Taleplerini İşleme

**Adım Adım**:

**Adım 1: Beklemedeki Talepleri İnceleyin**
- Siparişler > İade Talepleri'ne gidin
- Durum = "Beklemede" olarak filtreleyin
- Talebe tıklayarak detayları görüntüleyin

**Adım 2: Talebi Değerlendirin**
- Sipariş detaylarını inceleyin
- İade nedenlerini kontrol edin
- İade politikasına uygunluk kontrol edin (iade süresi içinde, ürün uygunluk)

**Adım 3: Onayla veya Reddet**
- "Onayla" tıklayarak iadeyi kabul edin
- Veya "Reddet" tıklayarak ve reddetme nedenini girin
- Kararınızı kaydedin

**Adım 4: İade Etiketi Oluşturun** (onaylandıysa)
- "İade Sevkiyatı Oluştur" tıklayın
- Taşıyıcı/hizmeti seçin
- Sistem iade etiketi oluşturur
- Etiket müşteriye otomatik olarak e-posta ile gönderilir
- Durum → `etiket gönderildi`

**Adım 5: Sevkiyatı Takip Et**
- Taşıyıcı webhook'larından otomatik olarak senkronize edilen takip güncellemeleri
- Taşıyıcı paketi tararsa durum otomatik olarak `yolda` ilerler

**Adım 6: Ürünleri Al**
- Ürünler ulaşınca "Alındı Olarak İşaretle" tıklayın
- Durum → `alındı`

**Adım 7: Ürünleri İnceleyin**
- İade talebini açın
- Ürün durumunu açılan listeden seçin:
  - Mükemmel (yeni gibi, satılabilir)
  - İyi (önemli aşınmalar, satılabilir)
  - Kabul edilebilir (görünür aşınmalar, indirimli satılabilir)
  - Hasarlı (satılabilir değil)
  - Arızalı (üretim arızası)
- İnceleme notları ekleyin
- İsteğe bağlı: Tekrar stoklama ücreti uygulayın (yüzde veya sabit)
- Durum → `inceleme yapıldı`

**Adım 8: İade İşlemi Yapın**
- "İade Oluştur" tıklayın
- Sistem iade tutarını hesaplar:
  - Orijinal ürün fiyatı
  - Tekrar stoklama ücreti (uygulanırsa) çıkar
  - İade edilemeyen sevkiyat ücreti çıkar
- İade oluşturun (iade talebi ile ilişkilendirilir)
- Durum → `tamamlandı`

---

## Ürün Seviyesinde İade Nedenleri

Müşteriler ürün başına neden seçebilir:

**Sıkça Görülen Nedenler**:
- Yanlış ürün alındı
- Ürün hasarlı/arızalı
- Aklım değiştirdi/şimdi ihtiyaç yok
- Ürün açıklamasıyla eşleşmiyor
- Daha iyi fiyat bulundu
- Yanlış sipariş verildi
- Kalite beklentilerine uymuyor

**Nedenleri Kullanın**:
- Analiz (sıkça iade nedenlerini takip etmek için)
- Kalite kontrolü (arızalı ürünleri tanımlamak için)
- Süreç iyileştirmesi (önleyici iadeleri azaltmak için)

---

## Tekrar Stoklama Ücretleri

İade işleme maliyetlerini telafi etmek için ücretler uygulayın:

**Yapılandırma**:
- **Tip**: Yüzde (örneğin, 15%) veya Sabit (örneğin, 5 $)
- **Uygulanacak Zaman**: Arızalı olmayan iadeler, açılmış ürünler, özel siparişler

**Örnek**:
```
Orijinal satın alma: 100 $
Tekrar stoklama ücreti: 15%
İade tutarı: 85 $
```

**En İyi Uygulamalar**:
- Tekrar stoklama ücreti politikasını açıkça iletişimlendirin
- Arızalı ürünler için ücret uygulaymayın
- VIP müşteriler için ücreti iptal edin

---

## İade İnceleme Kılavuzu

İnceleme kriterlerini tutarlı hale getirin:

**Mükemmel**:
- Açıklanmamış orijinal ambalaj
- Görünür aşınma yok
- Tüm aksesuarlar dahil
- Tamamıyla orijinal fiyatla satılabilir

**İyi**:
- Açıklanmış ama minimal kullanım
- Küçük ambalaj aşınması
- Tüm bileşenler mevcut
- Tam fiyatla satılabilir

**Kabul Edilebilir**:
- Görünür kullanım/aşınma
- Ambalaj hasarlı
- Gerekli olmayan aksesuarlar eksik
- İndirimli olarak satılabilir

**Hasarlı**:
- Fiziksel hasar
- Parça eksik
- Satılabilir değil
- Atılacak veya onarılacak

**Arızalı**:
- Üretim arızası
- Fonksiyonel hata
- Garanti talebi
- Üreticiye iade edilir

---

## İade Sevkiyatı Seçenekleri

**Seçenek 1: Müşteri, İade Sevkiyatını Öder**
- İade etiketi sağlanmaz
- Müşteri kendi taşıyıcısını seçer
- Manuel izleme numarası girişi

**Seçenek 2: Satıcı, Önceden Ödenmiş Etiket Sağlar**
- Taşıyıcı hesabı üzerinden iade etiketi oluşturun
- Ücret iade tutarından düşülür veya satıcı tarafından karşılanır
- Takip otomatik olarak senkronize edilir

**Seçenek 3: Ücretsiz İade Sevkiyatı**
- Satıcı, iade sevkiyatı maliyetini karşılar
- Müşteri memnuniyetini artırır
- İade oranı artar (etkisi dikkate alınmalıdır)

---

## Filtreleme & Raporlama

**Yararlı Filtreler**:
- Durum: Beklemede (eylem gerekir)
- Tarih Aralığı: Son 30 gün
- Sipariş: Belirli bir sipariş için arama
- Neden: İade nedenlerini takip etmek için

**İade Analitiği**:
- Ürün başına iade oranı
- En sık iade nedenleri
- Ortalama işleme süresi (beklemede → tamamlandı)
- Tekrar stoklama ücreti geliri

---

## İpuçları

- **Açık iade politikası belirleyin** - Pencere (30 gün), koşullar, ücretler hakkında iletişim kurun
- **Talepleri hızlıca işlemek** - Beklemedeki taleplere 24 saat içinde yanıt verin
- **Detaylı inceleme yapın** - Durumları belgeleyerek anlaşmazlıkları önleyin
- **İade nedenlerini izleyin** - Verileri kullanarak ürünleri ve açıklamaları iyileştirin
- **Otomatikleştirme** - Taşıyıcı webhook'ları sevkiyat durumunu otomatik olarak güncelleyin
- **Müşterilerle iletişim kurun** - Her durum değişikliğinde e-posta güncellemeleri gönderin
- **Tekrar stoklama ücretlerini adil şekilde uygulayın** - Konsistente uygulayın, arızalı ürünler için ücreti iptal edin
- **İade dolandırıcılığını izleyin** - Aşırı iade yapan müşterileri işaretleyin
- **Ambalajı iyileştirin** - Hasarla ilgili iadeleri azaltın
- **Stokları hızlıca güncelleyin** - İnceleme sonrası stokları geri yükleyin
- **Desenlerden Öğrenin** - Belirli bir ürün için yüksek iade oranı kalite sorununu gösterebilir
