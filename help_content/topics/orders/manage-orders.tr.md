---
title: Siparişleri Yönetme
---

# Siparişleri Yönetme

Bu kılavuz, müşteri siparişlerini yönetmek için ihtiyacınız olan her şeyi kapsar — yeni siparişleri incelemekten, gönderileri işleme ve iade taleplerini işlemek kadar.

## Sipariş Listesi

Yan menüde **Siparişler > Tüm Siparişler**'e giderek tüm siparişleri görebilirsiniz. Listede her siparişin numarası, durumu, müşterisi, toplamı ve tarihi gösterilir.

![Sipariş listesi](/static/core/admin/img/help/manage-orders/order-list.webp)

Liste üstündeki filtreleri kullanarak duruma, tarih aralığına veya sipariş numarasına veya müşteri adına göre siparişleri daraltabilirsiniz.

## Sipariş Detayı

Herhangi bir siparişi tıklayarak detay sayfasını açabilirsiniz. Burada sipariş hakkında her şey açık ve düzenli şekilde bölümlere ayrılmıştır.

![Sipariş detayı](/static/core/admin/img/help/manage-orders/order-detail.webp)

### Sipariş Bilgisi

Üst bölüm şu bilgileri gösterir:

- **Sipariş Numarası** — Bu sipariş için benzersiz tanımlayıcı
- **Durum** — Mevcut sipariş durumu (Beklemede, İşleniyor, Gönderildi, Teslim Edildi, Tamamlandı, İptal Edildi)
- **Müşteri** — Siparişi veren müşterinin adı ve e-postası
- **Oluşturulma Tarihi** — Siparişin verildiği zaman

### Sipariş Öğeleri

Bu bölüm, müşterinin sipariş ettiği her şeyi listeler:

- Ürün adı ve SKU
- Sipariş edilen miktar
- Birim fiyatı ve toplam tutar
- Uygulanan indirimler

### Ödeme Detayı

Kullanılan ödeme yöntemi, işlem kimliği ve ödeme durumu gösterilir. Ödeme bekleyen siparişler için buradan ödeme geçidi durumunu takip edebilirsiniz.

### Teslimat Adresi

Müşterinin teslimat adresidir. Faturalandırma adresi farklıysa, ikisi de gösterilir.

## Sipariş Yaşam Döngüsü

Siparişler genellikle şu durumlardan geçer:

1. **Beklemede** — Yeni sipariş alınmış, ödeme onayı bekleniyor
2. **İşleniyor** — Ödeme onaylandı, gönderim için hazırlanıyor
3. **Gönderildi** — Sipariş, takip bilgisiyle gönderildi
4. **Teslim Edildi** — Müşteri siparişi aldı
5. **Tamamlandı** — Sipariş tamamlandı

## Siparişi İşleme

### 1. Siparişi İncele

Aşağıdakileri kontrol edin:

- Ürünler ve miktarlar doğru
- Teslimat adresi tam
- Ödeme alınmış
- Müşteri notları işlenmiş

### 2. Gönderi Oluştur

Siparişi göndermek için:

1. Sipariş detay sayfasındaki **Gönderi Oluştur** butonuna tıklayın
2. Hangi ürünleri dahil edeceğinizi seçin (kısmi gönderiler için sadece bazı ürünleri seçin)
3. Teslimat taşıyıcısını ve hizmeti seçin
4. Takip numarasını girin
5. **Gönderiyi Kaydet** butonuna tıklayın

Sipariş durumu otomatik olarak **Gönderildi** olarak güncellenir ve müşteri, takip bilgisiyle birlikte gönderi bildirim e-postası alır.

### 3. Teslim Edildi Olarak İşaretle

Müşteri teslimatı onayladığında veya takip bilgisi "teslim edildi" gösterdiğinde, durumu **Teslim Edildi** olarak güncelleyin ve ardından **Tamamlandı** olarak işaretleyin.

## Sipariş İşlemleri

### Not Ekleme

İç notlar veya müşteri tarafından görülebilir mesajlar ekleyin:

1. Sipariş detay sayfasındaki **Notlar** bölümüne kaydırın
2. Mesajınızı yazın
3. Bu notun iç not (yalnızca personel) olup olmadığını veya müşteri bildirimi olup olmadığını seçin
4. **Not Ekle** butonuna tıklayın

Müşteri tarafından görülebilir notlar, e-posta bildirimi tetikler.

### İade İşlemi

İade yapmak için:

1. Sipariş detay sayfasındaki **İade** butonuna tıklayın
2. İade edilecek ürünleri seçin (veya özel bir tutar girin)
3. Bir iade nedeni seçin
4. İadeyi onaylayın

İadeler, orijinal ödeme geçidi üzerinden işlenir. Müşteri, bir e-posta onayı alır.

### Siparişi İptal Etme

İptal etmek için:

1. **Siparişi İptal Et** butonuna tıklayın
2. Bir iptal nedeni seçin
3. Ürünleri geri stoklamayı seçin mi yoksa değil mi
4. Onaylayın

Müşteri otomatik olarak bilgilendirilir ve ödeme alınmışsa iade başlatılır.

## Toplu İşlemler

Sipariş listesinden, birden fazla sipariş seçerek toplu işlemleri uygulayabilirsiniz:

- **Durumu Güncelle** — Birden fazla siparişi aynı duruma taşıyın
- **Dışa Aktar** — Seçilen siparişleri CSV olarak indirin
- **Yazdır** — Ambalaj listesi veya faturalar oluşturun

## Sipariş Bildirimleri

Müşteriler, anahtar aşamalarda otomatik olarak e-postalar alır:

- **Sipariş onayı** — Sipariş verildikten hemen sonra
- **Ödeme alınması** — Ödeme onaylandığında
- **Gönderi bildirimi** — Gönderi oluşturulduğunda (takip bağlantısı içerir)
- **Teslim onayı** — Teslim edildi olarak işaretlendiğinde

**Ayarlar > E-posta Yapılandırması**'nda e-posta şablonlarını yapılandırın.

## İpuçları

- Günlük olarak siparişleri işleme, hızlı gönderim sürelerini koruyun.
- Durum filtrelerini kullanarak dikkat gerektiren siparişlere (Beklemede ve İşleniyor) odaklanın.
- Özel işleme gereksinimlerini takip etmek için iç notlar ekleyin.
- Yüksek hacimli dönemlerde, birden fazla siparişi aynı anda güncellemek için toplu işlemleri kullanın.
- Taşıyıcı seçimini sipariş ağırlığına ve hedefe göre otomatikleştirmek için teslimat kuralları kurun.