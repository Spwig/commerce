---
title: Tamamlayıcı Oturum Ayarları
---

Tamamlayıcı, öngörülü arama veya yazarken arama olarak da bilinir, müşteriler sorgularını yazarken sonuçları görüntüler. Bu, müşterilerin ürünleri daha hızlı bulmalarını ve sıfır sonuç aramalarını azaltarak kullanıcı deneyimini büyük ölçüde iyileştirir. Bu kılavuz, tamamlayıcı davranışını, görüntü ayarlarını ve performans maliyetlerini nasıl yapılandırdığınızı açıklar.

Tamamlayıcı, varsayılan olarak mantıklı ayarlarla etkinleştirilmiştir. Sadece performans kaygılarınız veya görüntü tercihleriniz özelse bu ayarları değiştirmeyi düşünün.

![Tamamlayıcı Ayarları](/static/core/admin/img/help/configuring-autocomplete/autocomplete-settings-main.webp)

## Tamamlayıcıyı Etkinleştirme

**Arama > Arama Ayarları**'na gidin ve **Tamamlayıcı** sekmesine tıklayın.

**Tamamlayıcıyı Etkinleştir** - Öngörülü arama için ana anahtar. Etkinleştirildiğinde, müşteriler yazarken arama girdileri sonuçlar açılır penceresini görüntüler.

**Türe Göre Maksimum Sonuç Sayısı** - Varsayılan: 8 öğe. Her içerik türü (ürünler, kategoriler, markalar, blog gönderileri) için gösterilecek sonuç sayısı. Düşük değerler (5-6), API yük boyutunu azaltır ve daha hızlı işler. Yüksek değerler (10-12), müşterilere daha fazla seçenek sunar ancak yanıt hızını yavaşlatır.

## Gecikme Zamanlama

⚠️ **PERFORMANS UYARISI** - Gecikme zamanlaması sunucu yükünü önemli ölçüde etkiler.

**Gecikme Gecikme Süresi** - Varsayılan: 300ms. Son tuşun ardından bir tamamlayıcı isteğini tetiklemek için ne kadar beklemek gerektiğini belirler.

Bu ayar, yanıt verme ile sunucu yükü arasında dengeler:

| Gecikme | Kullanıcı Deneyimi | Sunucu Etkisi |
|---------|------------------|--------------|
| **100ms** | Çok hızlı yanıt | 300ms'e göre 3 kat daha fazla API çağrısı - yüksek yük |
| **200ms** | Hızlı yanıt | 300ms'e göre 1.5 kat daha fazla API çağrısı |
| **300ms** | İyi dengesi (önerilir) | Temel |
| **400ms** | Hafif gecikmeli | Daha az API çağrısı - düşük yük |
| **500ms** | Gözle görülür gecikmeli | 50% daha az çağrı ama yavaş hissedilir |

**Öneri**: 250-350ms arasında tutun. Sunucunuzun tamamlayıcı yüküyle mücadele etmesi gerekiyorsa 350ms'in üzerinde artırın. Çok hızlı bir sunucunuz ve küçük bir kataloğunuza sahip olmanız durumunda 200ms'in altına inmeyin.

## Ürünler için Görünüm Ayarları

Bu anahtarlar, ürün tamamlayıcı sonuçlarında hangi bilgilerin görüntüleneceğini kontrol eder:

**Küçük Resim Göster** - Varsayılan: AÇIK. Sonuçların yanına ürün resmini görüntüler. **Performans etkisi**: Resim sorgusu ekler ve JSON yük boyutunu artırır. Yavaş bağlantılar için daha hızlı tamamlayıcı için devre dışı bırakın.

**Açıklama Göster** - Varsayılan: KAPALI. Ürün kısa açıklamasını görüntüler. **Performans etkisi**: Metin işleme ekler ve yük boyutunu önemli ölçüde artırır. Açıklamalar ürün seçimi için kritikse açık bırakın, aksi takdirde devre dışı bırakın.

**Fiyat Göster** - Varsayılan: AÇIK. Ürün fiyatını görüntüler. **Performans etkisi**: Düşük - fiyat verisi ürünle birlikte yüklendi. Etkin bırakmak güvenlidir.

**SKU Göster** - Varsayılan: AÇIK. Ürün SKU'sunu görüntüler. **Performans etkisi**: Düşük - SKU zaten dizine alındı. B2B mağazaları için kritik.

**Stok Durumu Göster** - Varsayılan: KAPALI. **⚠️ ÖNEMLİ PERFORMANS UYARISI**

"Stokta", "Stokta Az", veya "Stokta Yok" etiketlerini görüntüler. **Büyük kataloglarda asla etkinleştirmeyin**.

Stok durumu, `with_stock_totals()` toplama işlemini gerektirir - her bir tamamlayıcı sonucunda tüm depolardaki stok miktarlarını hesaplamak. Bu ekler:
- Önemli veritabanı yükü (toplama sorguları)
- 1000'den fazla ürün olan kataloglarda 200-500ms ek gecikme
- 10000'den fazla ürün olan kataloglarda potansiyel zaman aşımları

Sadece kritik durumda ve toplam ürün sayısı 500'den azsa etkinleştirin.

## Blog Yazıları için Görünüm Ayarları

**Öne Çıkan Resim Göster** - Varsayılan: AÇIK. Blog yazısı küçük resmini tamamlayıcı sonuçlarında görüntüler.

**Özet Göster** - Varsayılan: AÇIK. Yazı içeriğinden kısa bir önizleme metni görüntüler.

**Özet Uzunluğu** - Varsayılan: 60 karakter. Kaç karakterlik önizleme metninin görüntüleneceğini belirler.

Bu ayarlar, blog yazılarının genellikle ürünlerden daha az olması nedeniyle performans üzerinde minimal etkiye sahiptir.

## Kategoriler ve Markalar için Görünüm Ayarları

**Küçük Resim/Logo Göster** - Varsayılan: AÇIK. Kategori veya marka resmini sonuçlarda görüntüler.

**Ürün Sayısı Göster** - Varsayılan: KAPALI. **⚠️ PERFORMANS UYARISI**

Her kategori veya markada kaç ürün olduğunu görüntüler (örneğin, "Elektronik (234)").

**Büyük kataloglarda asla etkinleştirmeyin**. Ürün sayıları her tamamlayıcı isteğinde yeniden hesaplanır:
- Her içerik türü için sayılara sahip olunan her içerik türü 2 ek sorgu ekler
- Sorgular birleştirmeler ve toplamalar içerir
- 100-300ms ek gecikme tipik olarak
- Kategoriler/Markalar sayısı ile lineer olarak artar

Sadece 50'den az kategori/marka ve toplam ürün sayısı 1000'den azsa etkinleştirin.

## Önbellekleme

**Tamamlayıcı Önbelleği TTL** - Varsayılan: 60 saniye (Önbellekleme sekmesinde ayarlanır).

Tamamlayıcı sonuçları, performansı artırmak için önbelleğe alınır. 60 saniyelik TTL şu anlama gelir:
- İlk müşteri "laptop" arıyor ve veritabanı sorgusu tetikler
- Sonraki 59 saniye, tüm "laptop" aramaları önbellek sonuçlarını döndürür
- 60 saniye sonra önbellek sona erer ve bir sonraki arama verileri yeniden yükler

**TTL için Öneri**:
- **45-60s**: Çoğu mağaza için iyi dengesi (varsayılan)
- **90-120s**: Ürün stokları nadiren değişiyorsa daha iyi performans
- **30s**: Ürünlerin sık sık eklendiği durumlarda daha güncel sonuçlar

Önbellek TTL'sini artırmak, tamamlayıcı performansını iyileştirmenin en kolay yoludur.

## Çok Dilli Tamamlayıcı

Birden fazla dil yapılandırılmışsa, tamamlayıcı, JSONField çevirilerinde depolanan çevrilmiş içeriği otomatik olarak arar.

**Nasıl Çalışır**:
- Müşteri İspanyolca arıyor: "zapatos"
- Sistem İspanyolca ürün isim çevirilerini arar
- Sonuçlar, JSONField verilerinden İspanyolca ürün isimlerini görüntüler
- İspanyolca çeviri eksikse temel dile geri döner

**Performans**: 1-3 dil için minimal ek yük. 5+ dil için sorgu karmaşıklığında hafif bir artış.

## Tamamlayıcıyı Test Etme

Ayarları yapılandırdıktan sonra tamamlayıcı deneyimini test edin:

1. **Mağazanızın anasayfasını** bir incognito penceresinde açın
2. **Arama kutusunu tıklayın** odaklanmak için
3. **Bir ürün ismini yavaşça yazın** (örneğin, "laptop")
4. **Gözlemleyin**:
   - Yazmayı durdurduktan sonra sonuçların ne kadar hızlı görünmesi (gecikme çalışıyor mu?)
   - Hangi bilgilerin görüntülendiği (küçük resimler, fiyatları, SKU'lar yapılandırdığınız gibi)
   - Sonuçların ilgili olup olmadığı (ilgili ağırlıkları kontrol edin eğer değilse)
5. **Mobil cihazda test edin** - Dropdown menünün dokunma dostu ve okunabilir olduğundan emin olun

## İpuçları

- **Hız için ürün açıklamalarını devre dışı bırakın** - Açıklamalar, tamamlayıcı bağlamında minimal değerle büyük ölçüde yük boyutunu artırır
- **Büyük kataloglarda asla stok durumunu etkinleştirmeyin** - Stok toplamaları tamamlayıcı performansını öldürür
- **Dokunma hedefleriyle mobil cihazda test edin** - Tamamlayıcı sonuçları telefonlarda kolayca tıklanabilir olmalıdır
- **Haftalık yanıt sürelerini izleyin** - Tamamlayıcı istekleri için hedef <200ms
- **Yavaşsa önbellek TTL'sini artırın** - Performans optimizasyonu en kolay yolu
- **Ürün sayıları pahalı - kritik değilse devre dışı bırakın** - Her kategori/marka sayısı, her tamamlayıcı isteğine 2 sorgu ekler
