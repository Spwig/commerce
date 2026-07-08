---
title: Spwig Mağazanızla Başlangıç
---

Spwig'a hoş geldiniz! Bu kılavuz, admin panelinizi hızlıca tanıtıyor ve çevrimiçi mağazanızı başlatmak için gereken temel adımları size gösteriyor.

## Panel

Giriş yaptıktan sonra **Mağaza Paneli**'ne yönlendirilirsiniz — mağaza performansınızı izlemenin merkezi kontrol noktasıdır.

![Yönetici paneli](/static/core/admin/img/help/getting-started-overview/admin-dashboard.webp)

Panel, şunları gösterir:
- **Gerekli Eylemler** — bekleyen siparişler, düşük stok uyarısı, terk edilen sepetler ve mevcut güncellemeler
- **Satış Geliri** — günlük, haftalık veya aylık gruplanmış gelir ve sipariş grafikleri
- **Hızlı Navigasyon** — açılır listeden herhangi bir bölümü doğrudan erişin

## Yönetici Yan Çubuğu

Sol taraftaki yan çubuk, her şeyi bölümlere organize eder:

| Bölüm | İçindekiler |
|---------|--------------|
| **Ürünler** | Ürün kataloğu, kategoriler, abonelik planları, hediye kartları |
| **Siparişler** | Sipariş yönetimi, sepetler, sevkiyatlar, sevkiyat ayarları, vergi oranları |
| **Müşteriler** | Müşteri profilleri, analitikler, LTV ayarları |
| **Arama** | Arama analitiği, eşanlamlılar, yönlendirmeler |
| **Pazarlama** | Kampanyalar, kuponlar, ortaklar, sadakat, blog, duyurular |
| **Ayarlar** | Mağaza ayarları, ödemeler, tasarım, e-posta, çeviriler, POS |

Yan çubuğun altındaki **hamburger ikonu** (☰)'ya tıklayarak daha fazla ekran alanı için yan çubuğu daraltabilirsiniz.

## İlk Adımlar

### 1. Mağaza Ayarlarını Yapılandırın

**Ayarlar > Mağaza Ayarları**'na giderek mağaza kimliğinizi ayarlayın:
- Mağaza adı ve tagline
- Site URL'si
- Favicon ve logo
- Varsayılan dil ve saat dilimi

Ayrıntılar için [Mağaza Ayarlarını Yapılandırma](#)'ya bakın.

### 2. Ürünlerinizi Ekleyin

**Ürünler > Tüm Ürünler**'e gidin ve **+ Ürün Ekle**'ye tıklayın:
- Ürün adı, açıklaması ve SKU girin
- Medya Kütüphanesi üzerinden görseller yükleyin
- Fiyatlandırma ve indirim seçeneklerini ayarlayın
- Stok takibi yapılandırın

Ürün eklemek için [Ürün Ekleme](#)'ya bakın.

### 3. Ödeme Yöntemlerini Yapılandırın

**Ayarlar > Ödeme Paneli**'ne giderek bir ödeme sağlayıcısı ile bağlantı kurun:
- Mevcut sağlayıcıları tarayın (Stripe, PayPal ve daha fazlası)
- Ayarlamaları başlatmak için API kimlik bilgilerinizi girin
- Gerçek hayatta geçiş yapmadan önce bağlantıyı test edin

### 4. Sevkiyatı Yapılandırın

**Siparişler > Sevkiyatlar**'a giderek teslimat seçeneklerini yapılandırın:
- Sabit ücretlerle sevkiyat yöntemleri oluşturun
- Ülkeye veya bölgeye göre sevkiyat bölgelerini tanımlayın
- Gerçek zamanlı ücretler için taşıyıcı entegrasyonlarını isteğe bağlı olarak bağlayabilirsiniz

Ayrıntılar için [Sevkiyatı Yapılandırma](#)'ya bakın.

### 5. Tasarınızı Kişiselleştirin

**Ayarlar > Tasarım & Tema**'ya giderek mağazanızı kişiselleştirin:
- Etkin temanızı seçin
- Marka kimliğini özelleştirin (renkler, tipografi, boşluklar)
- Çekme-yatırma yapımcılarıyla başlık ve altbilgiyi inşa edin
- Navigasyon menülerini yapılandırın

Ayrıntılar için [Tasarım & Temalar](#)'ya bakın.

### 6. Aktif Hale Getirin

Her şey hazırsa:
1. Ürünlerinizi **Yayınlandı** durumuna ayarlayın
2. Mağaza Ayarlarında mağaza URL'nizi doğrulayın
3. Test siparişi vererek ödeme akışını test edin
4. Site durumunun **Site Aktif** olduğunu doğrulayın

## İpuçları

- Her sayfada sağ üst köşedeki **Yardım** butonunu kullanarak sayfa ile ilgili bağlam sağlayıcı yardımını alın.
- Paneldeki **Gerekli Eylemler** kartları, dikkat gerektiren öğelere doğrudan bağlantı kurar — bunlara tıklayarak doğrudan oraya sıçrayın.
- Günlük başlangıç noktası olarak paneli kaydedin ve mağaza sağlığı hakkında bilgi edinin.