---
title: Blog Yönetimi
---

Blog, blogunuza gönderi, kılavuz ve haberler yayınlayarak trafiği artırmanıza ve izleyicilerinizi etkilemenize olanak tanır. Spwig'ın blogu, zengin metin düzenleyici, planlı yayın, abone bildirimleri, otomatik sosyal medya paylaşımı ve SEO araçları içerir.

![Blog gönderileri](/static/core/admin/img/help/blog-management/blog-post-list.webp)

## Bir Blog Gönderisi Oluşturma

**Pazarlama > Blog Gönderileri**'ne gidin ve **Gönderi Ekle**'ye tıklayın.

### Gönderi İçeriği

**CKEditor 5** zengin metin düzenleyicisini kullanarak gönderinizi yazın. Desteklenenler:
- Metin biçimlendirme (başlıklar, kalın, italik, listeler, alıntılar)
- Görseller ve medya (medya kütüphanesi üzerinden yükleme)
- Gömülü videolar (YouTube, Vimeo)
- Tablolar ve kod blokları
- Ürünler, kategoriler ve dış URL'lerle bağlantılar

Daha karmaşık düzenler için **Sayfa Oluşturucu** anahtarını etkinleştirmeyi unutmayın, böylece metin düzenleyicisi yerine sürükleyip bırakma sayfa oluşturucusunu kullanabilirsiniz.

### Gönderi Ayarları

| Ayar | Açıklama |
|---------|-------------|
| **Başlık** | Blog ve arama sonuçlarında gösterilen başlık |
| **Slug** | URL dostu kimlik (başlık üzerinden otomatik olarak oluşturulur, düzenlenebilir) |
| **Özet** | Blog listesi kartlarında ve RSS akımlarında gösterilen kısa özeti |
| **Öne Çıkan Görsel** | Gönderinin en üstünde ve listeleme kartlarında gösterilen ana görsel |
| **Kategori** | Gönderinin ana kategorisi |
| **Etiketler** | Filtreleme ve ilgili içerik için anahtar kelimeler |
| **Yazar** | Yazar olarak kredili verilecek personel |
| **Durum** | Taslak, Planlı, Yayınlandı veya Arşivlenmiş |
| **Öne Çıkan** | Gönderiyi blog listesi üstüne sabitleyin |

### SEO Ayarları

Her gönderi, SEO alanlarını içerir:
- **Meta Başlık** — Arama motoru sonuçları için özel başlık (varsayılan olarak gönderi başlığı)
- **Meta Açıklama** — Arama motoru sonuçlarında gösterilen özeti
- **Open Graph Görseli** — Gönderi sosyal medya üzerinde paylaşılırken kullanılan görsel

## Gönderi Durumları

| Durum | Açıklama |
|--------|-------------|
| **Taslak** | İşlem devam ediyor, halka açık değil |
| **Planlı** | Belirtilen tarih ve saatte otomatik olarak yayınlanacak |
| **Yayında** | Aktif ve ziyaretçilere açık |
| **Arşivlenmiş** | Blog listesinden gizlenir ancak doğrudan URL üzerinden hala erişilebilir |

### Gönderileri Planlama

Bir gönderiyi gelecekteki bir yayın için planlamak için:
1. Durumu **Planlı** olarak ayarlayın
2. **Yayın tarihi ve saati**'ni seçin
3. Gönderiyi kaydedin

Arka plan görevi, gönderiyi planlanan zamanda otomatik olarak yayınlar ve abone bildirimlerini tetikler.

## Kategoriler

**Pazarlama > Blog Kategorileri**'ne gidin ve içeriğinizi organize edin.

Kategoriler destekler:
- **İç İlişkiler** — Ana ve alt kategoriler oluşturun (örneğin, "Kılavuzlar" > "Başlangıç")
- **Özel URL'ler** — Her kategori kendi slug'ı ile temiz URL'ler için |
- **Açıklamalar** — Kategori arşiv sayfasında gösterilecek kategori açıklamaları |
- **Sıralama** — Menüde kategorilerin görüntülenme sırasını kontrol edin

## Etiketler

Etiketler, içerikleri sınıflandırmak için ikinci bir yoldur. Kategorilere göre (hiyerarşik) etiketler düz etiketlerdir. Ziyaretçiler bir etikete tıklayarak bu etiketle ilgili tüm gönderileri görebilir.

## Aboneler

**Pazarlama > Blog Aboneleri**'ne gidin ve abone listesini yönetin.

### Abonelik Nasıl Çalışır

1. Ziyaretçiler blogdaki bir form üzerinden abone olur (e-posta adresi gerekli)
2. **Çift onay** doğrulama e-postası gönderilir
3. Onaylandıktan sonra abone, yeni gönderiler yayınlandığında bildirimler alır

### Bildirim Sıklığı

Aboneler, bildirimleri ne sıklıkta alacaklarını seçer:

| Sıklık | Açıklama |
|-----------|-------------|
| **Hemen** | Yeni bir gönderi yayınlandığında e-posta gönderilir |
| **Haftalık Özeti** | Tüm yeni gönderilerin haftalık özeti |
| **Aylık Özeti** | Tüm yeni gönderilerin aylık özeti |

Arka plan görevleri özeti derleme ve teslimatını otomatik olarak yönetir.

### Aboneleri Yönetme

- Abone sayısını, onay durumunu ve kayıt tarihini görüntüleyin
- Dış e-posta pazarlama araçlarında kullanmak için abone listelerini dışa aktarın
- Bireysel adresleri kaldırın veya abonelikten çıkarın
- Her bildirim e-postasında bir tıklamayla **abonelikten çıkma** bağlantısı vardır

## Sosyal Medya Otomatik Paylaşımı

Spwig, gönderiler yayınlandığında yeni gönderileri sosyal medya hesaplarınıza otomatik olarak paylaşabilir.

### Sosyal Hesapları Bağlama

**Pazarlama > Sosyal Bağlayıcılar**'a gidin ve hesaplarınızı bağlayın:

| Platform | Kimlik Doğrulama |
|----------|---------------|
| **Facebook** | OAuth — Facebook Sayfanızı bağlayın |
| **Instagram** | OAuth — İş hesabı bağlayın |
| **LinkedIn** | OAuth — Şirket sayfanızı bağlayın |

### Otomatik Paylaşım Nasıl Çalışır

1. Bir veya daha fazla sosyal hesap bağlayın
2. Bir gönderi oluştururken, her bağlı hesap için **Otomatik Paylaş**'ı etkinleştirin
3. Paylaşım mesajını özelleştirin (varsayılan olarak gönderi başlığı ve özeti)
4. Gönderi yayınlanır (veya planlanan zamana ulaşır) ve otomatik olarak paylaşılır

Otomatik paylaşım, planlı gönderilerle de çalışır — sosyal paylaşım, gönderi canlı hale gelirken aynı anda gönderilir.

## RSS Akışı

Blog, otomatik olarak `/blog/feed/` adresinde bir RSS akışı oluşturur. Bu, ziyaretçilerin ve topluyucuların içeriğinize abone olmalarına olanak tanır. Akış şu bilgileri içerir:
- Gönderi başlığı ve özeti
- Yayın tarihi
- Yazar bilgisi
- Tam gönderiye doğrudan bağlantı

## Blog Ayarları

**Pazarlama > Blog Ayarları**'na gidin ve genel blog ayarlarını yapılandırın:

- **Sayfa Başına Gönderi Sayısı** — Listelemede sayfa başına gösterilecek gönderi sayısı
- **Yorumları İzin Ver** — Gönderilerde yorumları etkinleştirin veya devre dışı bırakın
- **Varsayılan Kategori** — Bir kategori atanmamış gönderiler için varsayılan kategori
- **Sosyal Paylaşım Butonları** — Bireysel gönderi sayfalarında paylaşım butonlarını göster

## İpuçları

- **SEO düşünerek** gönderiler yazın — açıklayıcı başlıklar kullanın, meta açıklamaları doldurun ve içerikte ilgili anahtar kelimeleri doğal olarak ekleyin.
- **Planlı yayın** kullanarak, manuel çaba olmadan tutarlı bir gönderi frekansı koruyun.
- **Otomatik paylaşımı** etkinleştirmek, erişimi maksimize eder — sosyal medya üzerinden kısa sürede yayınlanan gönderiler en çok etkileşim sağlar.
- Ziyaretçilerin **abone olmalarını** teşvik edin — blogunuzda abonelik formunu öne çıkarın ve güçlü bir çağrı yapın.
- **Kategorileri** geniş içerik gruplamaları için ve **etiketleri** belirli konular için kullanın — bu, ziyaretçilerin ilgili içerikleri bulmasına yardımcı olur.
- Her gönderiye bir **öne çıkan görsel** ekleyin — görsellerle birlikte gönderiler, arama sonuçlarında ve sosyal medya paylaşımında daha iyi performans gösterir.
- **Haftalık veya aylık özeti** seçeneğini, sık e-postalar istemeyen aboneler için kullanın — bu, abonelikten çıkma oranlarını azaltır.

