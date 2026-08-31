---
title: Stok Bildirimleri
---

Stok bildirimleri, tüketicilerin stokta olmayan bir ürün tekrar stoklandığında e-posta ile bilgilendirilmek için kayıt olmalarına olanak tanır. Stok görüntüleme ayarları, tüketicilerin ürün sayfalarında ne gördüğünü kontrol eder — örneğin stok durumu etiketleri, düşük stok uyarıları ve bir ürün tükendiğinde ne olacağı.

## Stok görüntüleme ayarları

Stok görüntüleme ayarları, kategori veya ürün düzeyinde geçersiz kılınmadıkça tüm ürünlere uygulanan mağaza genelinde varsayılan ayarlardır.

Bu seçenekleri yapılandırmak için **Katalog > Stok Görüntüleme Ayarları** bölümüne gidin. Mağazanız için bir ayar kaydı vardır — düzenlemek için üzerine tıklayın.

### Stok durumu görüntüleme

| Ayar | Açıklama |
|---------|-------------|
| **Stok Durumunu Göster** | Ürün sayfalarında "Stokta" veya "Stokta Yok" etiketlerini görüntüler |
| **Düşük Stok Uyarısını Göster** | Stok azaldığında "Sadece X kaldı" mesajını gösterir |
| **Düşük Stok Eşiği** | Düşük stok uyarısının göründüğü miktar (varsayılan: 5) |
| **Kesin Miktarı Göster** | Genel bir uyarı yerine kalan kesin sayıyı gösterir (ör. "Sadece 3 kaldı!") |

### Stokta yok davranışı

**Stokta Yok Eylemi** ayarı, bir ürünün stokta bulunmadığında tüketicilerin ne göreceğini belirler:

| Eylem | Tüketicilerin gördüğü |
|--------|-------------------|
| **Listelerden gizle** | Ürün, kategori sayfalarından ve arama sonuçlarından kaldırılır |
| **Mevcut değil olarak göster** | Ürün görünür ancak sepete eklenemez |
| **"Bana Bildir" düğmesini göster** | Tüketiciler, stok geri geldiğinde bilgilendirilmek için e-posta adreslerini kaydedebilir |
| **Sipariş almayı (backorder) izin ver** | Tüketiciler, stok sıfır olsa bile ürünü satın alabilir |

Bir ürün mevcut değilken gösterilen metni özelleştirmek için **Stokta Yok Mesajı** ayarını yapılandırın (varsayılan: `Stokta Yok`).

Sipariş alınabilir (backorder) ürünler için gösterilen metni özelleştirmek için **Sipariş Mesajı (Backorder Message)** ayarını yapılandırın (varsayılan: `Sipariş üzerine mevcut`).

### Kargo ve teslimat görüntüleme

| Ayar | Açıklama |
|---------|-------------|
| **"Şuradan Kargolanır" konumunu göster** | Ürün sayfasında depo adını görüntüler |
| **Tahmini Teslimatı Göster** | Depo konumundan hesaplanan tahmini teslimat tarihlerini görüntüler |

### Sipariş almayı izin ver (site genelinde)

Tüketicilerin varsayılan olarak stokta olmayan herhangi bir ürünü satın almasına izin vermek için **Sipariş Almayı İzin Ver (Allow Backorders)** seçeneğini işaretleyin. Bireysel ürünler ve kategoriler bu ayarı geçersiz kılabilir.

## Stokta var bildirimleri

Stokta yok eylemini **"Bana Bildir" düğmesini göster** olarak ayarladığınızda, tüketiciler ürün sayfasında e-posta adreslerini girebilir ve ürün yeniden stoklandığında e-posta alabilirler.

### Bildirim isteklerini görüntüleme

Tüm tüketici bildirim isteklerini görmek için **Katalog > Stok Bildirimleri** bölümüne gidin. Her kayıt şunları gösterir:
- Tüketici e-posta adresi
- Ürün ve varyant (uygunsa)
- Tercih edilen depo (tüketici bölgesel bir tercih seçtiyse)
- İsteğin oluşturulma zamanı
- Bildirim gönderildiğinde (henüz gönderilmediyse boş)

### Bildirimlerin ne zaman gönderildiği

Spwig, bir ürünün stok seviyesi sıfırın üzerine çıktığında stokta var e-postalarını otomatik olarak gönderir. **Bildirildi (Notified At)** alanı, e-postanın ne zaman gönderildiğini kaydeder.

Tüketiciler bir bildirim e-postası alır. Bildirim yapıldıktan sonra, ürün ikinci kez stokta yok olursa tekrar kayıt olmaları gerekir.

Tek bir düz uyarıdan fazlasını göndermek isterseniz — örneğin, yeniden stoklanan ürünü bir **Öne Çıkan Ürün** içerik bloğuyla göstermek veya bir gün sonra takip etmek — **Campaign Studio > Journeys** bölümünde bir **Ürün stokta var** yolculuğu oluşturun ve **Aktif** olarak ayarlayın. Bu yolculuk oluşturulduğunda, bekleyen tüketiciler düz tek seferlik e-posta almak yerine bu yolculuğa kaydedilir; aktif bir yolculuk yoksa, bu tek seferlik e-posta yukarıda açıklandığı gibi gönderilmeye devam eder. Tetikleyicinin nasıl çalıştığı hakkında [Tetiklenen Yolculuklar](/help/triggered-journeys) bölümüne bakın.

### Bildirim isteklerini filtreleme

Şunları bulmak için yönetici filtrelerini kullanın:
- Belirli bir ürün için istekler
- Zaten bildirilmiş istekler (kimlerin bilgilendirildiğini görmek için)
- Hâlâ bekleyen istekler (yeniden stoklanmayı bekleyen tüketiciler)

## Ürün düzeyinde geçersiz kılma

Site genelindeki stok görüntüleme ayarları, ürün veya kategori bazında geçersiz kılınabilir. Ürün düzenleme formunda, global varsayılandan farklı bir ürün özel **Stok Dışı Eylemi** belirleyebileceğiniz **Stok** bölümünü arayın.

Bu, çoğu ürün için sipariş sonrası tedarik (backorder) izni verirken birkaç ürünü "Bana Bildirin" olarak ayarlamak istediğinizde — veya belirli bir ürünün stok tükendiğinde gizlenmesi gerektiğinde — faydalıdır.

## İpuçları

- Müşterilerin tamamen tükenebilmeden önce sınırlı stok durumundan haberdar olmasını sağlamak için, **Düşük Stok Eşiği**ni genellikle kullandığınız yeniden sipariş noktasına ayarlayın.
- Stok dışı ürünleri gizlemek yerine **"Bana Bildirin" düğmesini göster** seçeneğini kullanın — kayıt olan müşteriler, yeniden stok siparişini haklı kılacak gerçek bir talebi temsil eder.
- **Kesin Miktarı Göster** seçeneğini dikkatli kullanın. Çoğu mağaza için, tam envanter tablosunu ortaya koymadan aciliyet yaratmak amacıyla "Sadece 3 kaldı!" gösterimi, kesin sayıyı göstermekten daha etkilidir.
- Yeni bir sipariş vermeden önce stok bildirimleri listesini kontrol edin — bekleyen bildirim isteklerinin sayısı, o ürün için ne kadar talep olduğunu gösterir.
- Sipariş sonrası tedarik (backorder) kullanıyorsanız, doğru beklentileri oluşturmak için **Sipariş Sonrası Tedarik Mesajı**nızı güncelleyin (ör. "2-3 hafta içinde kargoya verilir — yerinizi ayırtmak için şimdi sipariş verin").
- Stok dışı bildirimlerini e-posta pazarlamasıyla birleştirin: popüler bir ürünü yeniden stokladığınızda, yalnızca otomatik bildirim e-postasını değil, kayıtlı herkese bir kampanya gönderin.