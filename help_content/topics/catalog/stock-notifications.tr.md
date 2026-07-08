---
title: Stok Bildirimleri
---

Stok bildirimleri, müşterilerin ürün yeniden stoklanınca e-posta almak için kaydolmalarını sağlar. Stok görüntüleme ayarları, ürün sayfalarında müşterilerin göreceği şeyleri kontrol eder — örneğin, stok durumu etiketleri, düşük stok uyarıları ve bir ürün tükendiğinde ne olacağını.

## Stok Görüntüleme Ayarları

Stok görüntüleme ayarları, tüm ürünler için geçerli olan mağaza genelindeki varsayılan ayarlardır, kategori veya ürün düzeyinde geçersiz kılınmazsa.

**Katalog > Stok Görüntüleme Ayarları**'na giderek bu seçenekleri yapılandırın. Mağazanız için bir ayar kaydı vardır — bunu düzenlemek için tıklayın.

### Stok Durumu Görüntüleme

| Ayar | Açıklama |
|---------|-------------|
| **Stok Durumu Göster** | Ürün sayfalarında "Stokta" veya "Stokta Yok" etiketlerini göster |
| **Düşük Stok Uyarısı Göster** | Stok düşük olduğunda "Sadece X tane kalmış" mesajı göster |
| **Düşük Stok Eşiği** | Düşük stok uyarısının görüneceği miktar (varsayılan: 5) |
| **Aynı Stok Sayısını Göster** | "Sadece 3 tane kalmış!" gibi tam sayı kalanını göster, genel bir uyarı yerine |

### Stokta Olmayan Davranışlar

**Stokta Olmayan Eylem** ayarı, bir ürünün stokta olmayan durumda olduğunda müşterilerin ne göreceğini belirler:

| Eylem | Müşterilerin Gördüğü |
|--------|-------------------|
| **Listelerden Gizle** | Ürün, kategori sayfalarından ve arama sonuçlarından kaldırılır |
| **Kullanılamaz Olarak Göster** | Ürün görünür ancak sepete eklenemez |
| **"Bildir" Butonu Göster** | Müşteriler, stok yeniden mevcut olduğunda bildirim almak için e-posta adreslerini kaydedebilir |
| **Geri Siparişleri İzin Ver** | Müşteriler, stok sıfır olduğunda bile ürünü satın alabilir |

**Stokta Olmayan Mesajı** ayarını, ürün kullanılamaz olduğunda gösterilecek metni özelleştirmek için kullanın (varsayılan: `Stokta Yok`).

**Geri Sipariş Mesajı** ayarını, geri sipariş edilebilir ürünler için gösterilecek metni özelleştirmek için kullanın (varsayılan: `Geri sipariş olarak mevcut`).

### Sevkiyat ve Teslimat Görüntüleme

| Ayar | Açıklama |
|---------|-------------|
| **"Stoktan" Konumu Göster** | Ürün sayfasında depo adını göster |
| **Tahmini Teslimat Göster** | Depo konumundan hesaplanan tahmini teslimat tarihlerini göster |

### Genel Geri Siparişleri İzin Ver

**Geri Siparişleri İzin Ver** onay kutusunu seçerek, varsayılan olarak tüm stokta olmayan ürünleri satın almak için müşterilere izin verin. Bireysel ürünler ve kategoriler bu ayarı geçersiz kılabilir.

## Stokta Olan Bildirimleri

Stokta olmayan eylemi **"Bildir" Butonu Göster** olarak ayarladığınızda, müşteriler ürün sayfasında e-posta adreslerini girerek ürün yeniden stoklandığında bir e-posta alabilir.

### Bildirim Taleplerini Görüntüleme

**Katalog > Stok Bildirimleri**'ne giderek tüm müşteri bildirim taleplerini görüntüleyin. Her kayıt şu bilgileri gösterir:
- Müşteri e-posta adresi
- Ürün ve varyant (uygunsa)
- Tercih edilen depo (müşteri bölgesel tercih seçtiyse)
- Talep oluşturulma zamanı
- Bildirim gönderme zamanı (gönderilmemişse boş bırakılır)

### Bildirimler Ne Zaman Gönderilir

Spwig, bir ürünün stok seviyesi sıfırın üzerine çıktığında otomatik olarak stokta olan e-postaları gönderir. **Bildirildi** alanı, e-postanın ne zaman gönderildiğini kaydeder.

Müşteriler bir bildirim e-postası alır. Bildirildikten sonra, ürün ikinci kez stokta olmayan duruma düştüğünde tekrar kaydolmaları gerekir.

### Bildirim Taleplerini Filtreleme

Yönetici filtrelerini kullanarak şu öğeleri bulun:
- Belirli bir ürün için talepler
- Zaten bildirilen talepler (kimlerin bildirildiğini görmek için)
- Hâlâ bekleyen talepler (yeniden stoklanmayı bekleyen müşteriler)

## Ürün Düzeyinde Geçersiz Kılma

Mağaza genelindeki stok görüntüleme ayarları, ürün veya kategori başına geçersiz kılınabilir. Ürün düzenleme formunda, **Stok** bölümünü bulun ve ürün özelinde **Stokta Olmayan Eylem** ayarını, genel varsayılan ayardan farklı olarak ayarlayabilirsiniz.

Bu, çoğu ürünün geri siparişleri izin verirken bazı ürünleri "Bildir" olarak tutmak istediğinizde veya belirli bir ürünün stokta olmayan durumda gizlenmesi gereken durumlarda yararlıdır.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Düşük Stok Seviyesi'ni** genellikle kullandığınız yeniden stoklama noktasına ayarlayın, böylece stoklar tükendiğinde müşterilere sınırlı mevcutluk hakkında uyarı verilebilir.
- **"Bildir" Butonunu Göster** seçeneğini kullanın, stokta olmayan ürünleri gizlemek yerine — kaydolan müşteriler, yeniden stoklama siparişini gerekli kılan gerçek talep temsil eder.
- **Tam Stok Sayısını Göster** seçeneğini sadece gerekli olduğunda etkinleştirin.

Çoğu mağaza için "Sadece 3 tane kala!" ifadesi, tam stok sayısını göstermekten daha iyi çalışır, çünkü bu ifade tam stok durumunu gizlerken aciliyet yaratır.
- Yeni bir sipariş vermeden önce stok bildirim listesini kontrol edin — bekleyen bildirim isteklerinin sayısı, o ürün için ne kadar talep olduğunu size söyler.
- Eğer geri siparişler kullanıyorsanız, **Geri Sipariş Mesajını** güncelleyin ve gerçekçi beklentileri belirleyin (örneğin, "2-3 hafta içinde kargo gider — şimdi sipariş verin yerinizi rezerv etin").
- Stokta olmayan bildirimleri e-posta pazarlama ile birleştirin: popüler bir ürün yeniden stoklandığında, sadece otomatik bildirim e-postası değil, kaydolan herkese bir kampanya gönderin.