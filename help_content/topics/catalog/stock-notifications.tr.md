---
title: Stok Bildirimleri
---

Stok bildirimleri, stokta olmayan bir ürün tekrar mevcut olduğunda e-posta ile bildirim almak için müşterilerin kaydolmasına olanak tanır. Stok görüntüleme ayarları, ürün sayfalarında müşterilerin ne gördüğünü kontrol eder - örneğin stok durumu etiketleri, düşük stok uyarısı ve bir ürün stokta kalmadığında ne olduğuna dair bilgiler.

## Stok görüntüleme ayarları

Stok görüntüleme ayarları, kategori veya ürün seviyesinde geçersiz kılınmadıkça tüm ürünleri etkileyen genel ayarlardır.

Bu seçenekleri yapılandırmak için **Katalog > Stok Görüntüleme Ayarları**'na gidin. Mağazanızan bir ayar kaydı vardır - düzenlemek için tıklayın.

### Stok durumu görüntüsü

| Ayar | Açıklama |
|---------|-------------|
| **Stok Durumunu Göster** | Ürün sayfalarında "Stokta Var" veya "Stokta Yok" etiketlerini göster |
| **Düşük Stok Uyarısını Göster** | Stok azaldığında "Sadece X tane kaldı" mesajını göster |
| **Düşük Stok Eşiği** | Düşük stok uyarısının görüldüğü miktar (varsayılan: 5) |
| **Mevcut Miktarı Göster** | Kalan tam sayıyı göster (örneğin, "Sadece 3 tane kaldı!") genel bir uyarı yerine |

### Stokta Yokken Davranış

**Stokta Yokken Eylem** ayarı, bir ürün stokta kalmadığında müşterilerin ne gördüğünü belirler:

| Eylem | Müşterilerin gördüğü |
|--------|-------------------|
| **Listelemeden Kaldır** | Ürün, kategori sayfalarından ve arama sonuçlarından kaldırılır |
| **Mevcut Değil Olarak Göster** | Ürün görünür ancak sepete eklenemez |
| **Bana Haber Ver butonunu Göster** | Müşteriler, stokların döndüğü zaman e-posta adreslerini kaydolabilir |
| **Gerçekten sipariş alınabilir** | Müşteriler, stok sıfır iken ürün alabilir |

**Stokta Yok Mesajı**'nı ayarlayarak, bir ürün mevcut değilken gösterilen metni özelleştirin (varsayılan: `Stokta Yok`).

**Gerçekten sipariş mesajı**'nı ayarlayarak, geri sipariş edilebilir ürünler için gösterilen metni özelleştirin (varsayılan: `Gerçekten sipariş`).

### Kargo ve teslimat görüntüsü

| Ayar | Açıklama |
|---------|-------------|
| **Kargolandığı Yeri Göster** | Ürün sayfasında depo adını göster |
| **Tahmini Teslimatı Göster** | Depo konumundan hesaplanan tahmini teslimat tarihlerini göster |

### Genel olarak geri sipariş izni

**Gerçekten sipariş izin ver**'i kontrol ederek, genel olarak stokta olmayan her ürün için müşterilerin satın almasına izin verin. Bireysel ürünler ve kategoriler bu ayarı geçersiz kılabilir.

## Stokta Kalmaya Dair Bildirimler

Stokta Yokken Eylem ayarını **Bana Haber Ver butonunu Göster** olarak ayarladığınızda, müşteriler ürün stokta kalmaya döndüğünde e-posta almak için ürün sayfasında e-posta adreslerini girebilir.

### Bildirim isteklerini görüntüleme

Bu istekleri görmek için **Katalog > Stok Bildirimleri**'ne gidin. Her kayıt şunları gösterir:
- Müşteri e-posta adresi
- Ürün ve varyant (varsa)
- Müşteri bölgesel tercihini seçtiğinde tercih edilen depo (varsa)
- İstek ne zaman oluşturuldu
- Bildirim gönderildi (henüz gönderilmemişse boş)

### Bildirimler ne zaman gönderiliyor

Stok seviyesi sıfırdan yukarıya çıktığında, Spwig otomatik olarak stokta kalmaya dair e-posta gönderir. **Bildirilen Tarih** alanı, e-postanın gönderildiği tarihi kaydeder.

Müşteriler tek bir bildirim e-postası alır. Bildirildikten sonra, ürün tekrar stokta kalmazsa, tekrar kaydolmak zorundadır.

### Bildirim isteklerini filtreleme

Aşağıdaki durumları bulmak için admin filtrelerini kullanın:
- Belirli bir ürün için istekler
- Zaten bildirilen istekler (kimlerin irtibata geçtiğini görmek için)
- Henüz bekleyen istekler (stokta kalmayı bekleyen müşteriler)

## Ürün seviyesinde geçersiz kılma

Genel stok görüntüleme ayarları, ürün veya kategori seviyesinde geçersiz kılınabilir. Ürün düzenleme formunda, genel varsayılanlardan farklı olacak şekilde ürün seviyesinde **Stok** bölümünü bulabilirsiniz.

Bu, çoğu ürünün geri sipariş edilebilir olmasını isterseniz ancak bazı ürünleri "Bana Haber Ver" olarak tutmak isterseniz veya belirli bir ürünün stokta kalmadığında gizlenmesini isterseniz yararlıdır.

## İpuçları

Tüm markdown formatlamasını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Düşük Stok Eşiğini** genellikle kullandığınız yeniden sipariş noktasına ayarlayarak, stoklar tamamen tükendiğinde değil, mevcut sınırlı olduğuna dair müşterilere uyarı verin.
- Stokta yokken ürünleri gizleme yerine **"Bana Bildir" butonunu** gösterme seçeneğini kullanın — kaydolmuş olanlar gerçek talebi temsil eder ve yeniden stoklamak için gerekçelendirme sağlar.
- **Mümkün olduğunca az** **Miktarı Göster**.

Çoğu mağaza için, "Sadece 3 tane kaldı!" yazısının tam sayı gösterilmesinden daha iyi olduğunu, çünkü stok durumunuzu açığa vurmadan aceleci bir hava yaratır.
- Yeni bir sipariş vermeden önce stok bildirimleri listesini kontrol edin — bekleyen bildirim isteklerinin sayısı, o ürün için ne kadar talep olduğunu gösterir.
- Arka sipariş kullanıyorsanız, **Arka Sipariş Mesajı** nı güncelleyerek doğru beklentileri oluşturun (örneğin, "2-3 hafta içinde kargo verilecek - rezervasyon için şimdiden sipariş verin").
- Stokta kalmayan bildirimleri e-posta pazarlama ile birleştirin: popüler bir ürün yeniden stoklandığında, sadece otomatik bildirim e-postası değil, kaydolmuş tüm kişilere kampanya gönderin.