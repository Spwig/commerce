---
title: Kargo Ayarı Yapma
---

# Kargo Ayarı Yapma

Bu kılavuz, mağazanız için kargonuzu nasıl yapılandıracağınızı açıklar — temel kargo yöntemlerini ayarlamaktan başlayarak, gerçek zamanlı ücretler için canlı taşıyıcı entegrasyonlarını bağlamaya kadar.

## Kargo Genel Bakış

Spwig, kargonuzu yapılandırmak için iki yaklaşım sunar:

- **El ile Kargo Yöntemleri** — Kendi tanımladığınız sabit ücretli yöntemler (örneğin, "Standart Kargo — 5,99 $")
- **Taşıyıcı Entegrasyonları** — FedEx, UPS ve DHL gibi sağlayıcılardan gerçek zamanlı ücretler

Her iki yaklaşımı da kullanabilir ya da birleşebilirsiniz.

## Kargo Yöntemleri

Kargo yöntemleri, müşterilerinizin ödeme sırasında görmesi gereken seçeneklerdir. Kargo yöntemlerini yönetmek için yan panelde **Siparişler > Kargolar** bölümüne gidin.

![Kargo Yöntemleri](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### Kargo Yöntemi Oluşturma

1. **Kargo Yöntemi Ekle**'ye tıklayın
2. Aşağıdaki detayları doldurun:
   - **Ad** — Müşterilere gösterilecek görünür ad (örneğin, "Hızlı Teslimat")
   - **Açıklama** — Hizmetin kısaca açıklaması
   - **Fiyat** — Sabit kargo maliyeti
   - **Tahmini Teslim** — Teslim süresi tahmini (örneğin, "3-5 iş günü")
3. **Kaydet**'e tıklayın

## Kargo Bölgeleri

Kargo bölgeleri, kargonuzun uygulandığı coğrafi bölgeleri tanımlar. Kargo bölgelerini yönetmek için **Kargo Bölgeleri** bölümüne gidin.

![Kargo Bölgeleri](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### Bölge Oluşturma

1. **Kargo Bölgesi Ekle**'ye tıklayın
2. Bölgenin ayarlarını yapılandırın:
   - **Bölge Adı** — İç ad (örneğin, "ABD Yerli", "Avrupa")
   - **Ülkeler** — Bu bölgeye ait olan ülkeleri seçin
   - **Eyaletler/Bölgeler** — Belirli eyaletlere daraltmak isterseniz seçin
   - **Posta Kodu Desenleri** — "9*" gibi desenler kullanarak belirli alanları hedefleyin
3. Bu bölgeye kargo yöntemlerini atayın
4. **Kaydet**'e tıklayın

### Bölge Önceliği

Bir müşterinin adresi birden fazla bölgeyle eşleşiyorsa, en spesifik bölge önceliklidir. Eyalet seviyesinde hedefleme olan bir bölge, ülke seviyesindeki bölgelerden önceliklidir.

## Taşıyıcı Entegrasyonları

Kargo taşıyıcılarıyla bağlantı kurarak, ödeme sırasında gerçek zamanlı ücretleri sunabilirsiniz.

![Kargo Taşıyıcıları](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### Kullanılabilir Sağlayıcılar

Pazar yerinden kargo sağlayıcılarını keşfedin ve yükleyin.

![Kargo Sağlayıcıları](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

Desteklenen taşıyıcılar şunları içerir:

- **FedEx** — Yerel, Hızlı, Uluslararası
- **UPS** — Yerel, 2 Gün, Gece, Dünyada
- **DHL** — Hızlı, E-ticaret
- **USPS** — Öncelikli, İlk Sınıf, Medya Postası
- Ve daha fazlası Pazar Yerinden mevcuttur

### Taşıyıcıyı Kurma

1. Kargo sağlayıcıları sayfasına gidin ve tercih ettiğiniz taşıyıcıya **Yükle**'ye tıklayın
2. Kurulum asistanını takip edin:
   - **Adım 1** — Sağlayıcı detaylarını inceleyin
   - **Adım 2** — Genel ayarları yapılandırın
   - **Adım 3** — API kimlik bilgilerinizi girin (hesap numarası, API anahtarı vb.)
   - **Adım 4** — Belirli hizmetleri etkinleştirin (Yerel, Hızlı vb.)
   - **Adım 5** — Bağlantıyı test edin
3. Bağlandıktan sonra, taşıyıcının ücretleri ödeme sırasında otomatik olarak görünür olur

### API Kimlik Bilgileri

Her taşıyıcı, bir API hesabı gerektirir:

- **FedEx** — FedEx Geliştirici Portalı'nda kayıt olun, bir uygulama oluşturun ve API anahtarınızı ve gizlinizi kopyalayın
- **UPS** — UPS Geliştirme Kitinde kayıt olun, erişim anahtarı isteyin
- **DHL** — DHL'nin iş portalı üzerinden API kimlik bilgilerini alın

## Kargo Kuralları

İleri kurallar oluşturarak kargo yöntemlerinin ne zaman ve nasıl sunulacağını kontrol edin.

### Ortak Kurallar

- **50$ üzeri ücretsiz kargo** — Ücretsiz kargo için sepet minimumu ayarlayın
- **Hafif siparişler için sabit ücret** — Sipariş ağırlığı belirli bir eşiği geçmiyorsa sabit ücret
- **Uzak bölgelerde hızlı kargo devre dışı bırak** — Posta kodlarına göre hızlı kargo seçeneklerini gizleyin
- **Yüzde markup** — Taşıyıcı ücretlerinin yüzdesi olarak bir işlem ücreti ekleyin

### Kural Oluşturma

1. Kargo kuralları bölümüne gidin
2. **Kural Ekle**'ye tıklayın
3. Koşulları ayarlayın (sepet toplamı, ağırlık, bölge vb.)
4. Eylemi tanımlayın (fiyatı ayarla, yöntemi gizle, ücretsiz kargo etkinleştir)
5. Kuralı kaydedin

Kurallar sırayla değerlendirilir — ilk eşleşen kural uygulanır.

## Ücretsiz Kargo

### Mağaza Genelinde Ücretsiz Kargo

**Ayarlar > Mağaza Ayarları** içinde global olarak ücretsiz kargo etkinleştirin:

- **Ücretsiz Kargo**'yu açın
- Seçici olarak minimum sipariş tutarını ayarlayın
- Hangi bölgelerin hak kazanacağını seçin

### Kampanyalı Ücretsiz Kargo

Sınırlı sürelı ücretsiz kargo teklifleri oluşturun:

1. **Pazarlama > Satışlar & Kampanyalar** bölümüne gidin
2. Yeni bir kampanya oluşturun
3. Koşulu ayarlayın: "Sepet toplamı X üzeri"
4. Eylemi ayarlayın: "Ücretsiz kargo"
5. Başlangıç ve bitiş tarihlerini yapılandırın

## Uluslararası Kargo

Uluslararası siparişler için ürünlerinizde şunlar olmalıdır:

- **HS Kodu** — Harmonize Sistemi Tarifesi Sınıflandırması
- **Üretim Ülkesi** — Üretim ülkesi
- **Gümrük Değeri** — Gümrük için bildirilen değer

Bu alanlar, her ürünün **Stok** sekmesinde yer alır. Taşıyıcılar bu bilgileri kullanarak gümrük belgelerini otomatik olarak oluşturur.

## İpuçları

- Mağazanızı hızlıca başlatmak için el ile kargo yöntemleriyle başlayın, daha sonra taşıyıcı entegrasyonlarını ekleyin.
- En yaygın hedefleriniz için kargo bölgeleri oluşturun.
- Farklı adreslerle test siparişler vererek kargonuzun yapılandırmasını daima test edin.
- İşlem ve ambalaj maliyetlerini karşılamak için fiyat markup özelliğini kullanın.
- Ortalama sipariş değerini artırmak için ücretsiz kargo eşiği ayarlayın.
