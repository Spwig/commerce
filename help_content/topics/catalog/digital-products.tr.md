---
title: Dijital Ürünler
---

Dijital ürünler, indirilebilir dosyalar, yazılım lisansları ve diğer fiziksel olmayan malları satmanızı sağlar. Spwig, yalnızca dijital ürünler için destek sağlar ve fiziksel ile dijital teslimatı birleştiren hibrit ürünler için de destek sunar.

![Lisans sağlayıcıları](/static/core/admin/img/help/digital-products/license-providers.webp)

## Dijital Ürün Türleri

### Bağımsız Dijital Ürün

Ürünlerin sadece dijital olduğu durumlarda **Ürün Türü** alanını **Dijital Ürün** olarak ayarlayın:
- Yazılım uygulamaları
- E-kitaplar ve PDF'ler
- Müzik ve ses dosyaları
- Dijital sanat eserleri ve şablonlar

### Hibrit Ürünler

Herhangi bir ürün türü, **Temel Bilgiler** sekmesinde **Dijital Ürün** seçeneğini işaretleyerek dijital teslimatı içerebilir. Bu şu durumlar için faydalıdır:
- **Değişken dijital ürünler** — Temel/Pro/Enterprise sürümleri olan yazılımlar
- **Özel dijital ürünler** — Özel tasarlanmış dijital varlıklar
- **Fiziksel + dijital paketler** — İndirilebilir bir dosya içeren bir kitap

## Dijital Ürün Kurulumu

### Adım 1: Ürün Oluşturma

1. **Ürünler > Tüm Ürünler** sekmesine gidin ve **+ Ürün Ekle**'ye tıklayın
2. **Ürün Türü** alanını **Dijital Ürün** olarak ayarlayın (veya başka bir ürün türünde **Dijital Ürün** seçeneğini işaretleyin)
3. Ürün detaylarını doldurun (ad, açıklama, fiyat)
4. Ürünü kaydedin

### Adım 2: İndirilebilir Dosyalar Ekleme

1. Ürünün **Stok** sekmesine gidin
2. **Dijital Dosyalar** bölümünde, müşteri satın aldıktan sonra alacağı dosyaları yükleyin
3. Her dosya için şu ayarları yapabilirsiniz:
   - **Dosya adı** — Müşterilere gösterilecek görüntüleme adı
   - **İndirme sınırı** — Dosyanın kaç kez indirilebileceği (0 = sınırsız)
   - **Geçerlilik günü** — İndirme bağlantısının aktif kalacağı gün sayısı

### Adım 3: Lisans Teslimatı Yapılandırması (Opsiyonel)

Dijital ürününüz lisans anahtarları gerektiriyorsa:

1. **Ayarlar > Lisans Yönetimi** sekmesine gidin
2. Bir lisans sağlayıcısı bağlayın (aşağıdaki bölümde bkz.)
3. Ürün düzenleme formunda lisans sağlayıcısını atayın

## Lisans Sağlayıcıları

Lisans sağlayıcıları, müşteri ürün satın alındığında otomatik olarak yazılım lisans anahtarlarını oluşturup yöneten harici hizmetlerdir.

### Mevcut Sağlayıcı Türleri

| Sağlayıcı | Açıklama |
|----------|-------------|
| **Spwig İçerikli Lisans Sunucusu** | Platforma entegre basit lisans anahtarı üretimi |
| **Keygen.sh** | Tam özellikli lisans yönetimi API'si |
| **LicenseSpring** | Kurumsal lisans yönetimi |
| **Cryptlex** | Çevrimdışı destekli yazılım lisanslama |
| **Özel API** | REST API aracılığıyla herhangi bir lisans sistemiyle bağlanın |

### Lisans Sağlayıcısı Bağlantısı

1. **Ayarlar > Lisans Yönetimi** sekmesine gidin
2. **Sağlayıcıyı Bağla**'ya tıklayın
3. Kurulum asistanını takip edin:
   - **Adım 1** — Sağlayıcı türünü seçin
   - **Adım 2** — Genel ayarları yapılandırın
   - **Adım 3** — API kimlik doğrulama bilgilerini girin
4. Bağlantıyı test edin ve çalıştığını doğrulayın
5. Yapılandırmayı kaydedin

### Sağlayıcı Kartı

Her bağlanan sağlayıcı şu bilgileri gösterir:
- **Durum etiketleri** — Aktif/Devre Dışı ve bağlantı durumu
- **API uç noktası** — Yapılandırılmış sunucu URL'si
- **Senkronizasyon yetenekleri** — Sipariş, Aktivasyon ve Deaktivasyon senkronizasyonu desteği
- **Aksiyon düğmeleri** — Yapılandır, Test Et ve Şimdi Senkronize

### Senkronizasyon Yetenekleri

Lisans sağlayıcıları şu olaylarda senkronize olabilir:

- **Sipariş** — Müşteri bir satın alma tamamladığında otomatik olarak bir lisans anahtarı oluşturur
- **Aktivasyon** — Müşterinin lisansını aktivasyon yaptığını izler
- **Deaktivasyon** — İade veya aktarım için lisansın deaktivasyonunu yönetir

## Müşteri Deneyimi

### Satın Alma Sonrası

Müşteri bir dijital ürün satın aldığında:

1. **Sipariş onayı** — Dijital teslimatın dahil olduğunu gösterir
2. **E-posta teslimatı** — İndirme bağlantıları ve/veya lisans anahtarları otomatik olarak gönderilir
3. **Hesap sayfası** — Müşteriler, hesap dashboard'larından indirme dosyalarına erişebilir
4. **İndirme sayfası** — Güvenli ve zaman sınırlı indirme bağlantıları

### İndirme Güvenliği

Dijital dosya indirme işlemleri şu şekilde korunur:
- Benzersiz, zaman sınırlı indirme token'ları
- İsteğe bağlı indirme sayısına sınırlama
- Linklerin aktif kalacağı gün sayısı (sonrasında geçersiz hale gelir)
- Giriş gerekliliği (kayıtlı müşteriler için)

## İpuçları

- Aşırı kullanımın önlenmesi için akıllıca indirme sınırları ayarlayın (3-5 indirme) ve yeniden indirme izni verin.
- Destek dönemini yansıtan geçerlilik günlerini kullanın (örneğin, 365 gün bir yıllık erişim için).
- Bir test siparişi ile tam satın alma akışını test edin ve indirme bağlantılarının ve lisans anahtarlarının doğru şekilde teslim edildiğinden emin olun.
- Yazılım ürünleri için lisans sağlayıcısını bağlayarak anahtar üretimi otomatik hale getirin, manuel olarak anahtar yönetimi yerine.
- Fiziksel malların dijital ekstra ürünleri içerdiği durumlarda (örneğin, basılı kitap + PDF) hibrit ürün özelliğini kullanın.