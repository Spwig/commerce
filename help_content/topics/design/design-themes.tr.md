---
title: Tasarım & Temalar
---

Tasarım & Tema sistemi, mağazanızın tüm görünümünü ve hissini kontrol etmenizi sağlar — renkler ve tipografi, başlıklar, ayaklar ve sayfa düzenleri dahil. Tasarım Panosunu açmak için **Ayarlar > Tasarım & Tema**'ya gidin.

![Tasarım panosu](/static/core/admin/img/help/design-themes/theme-dashboard.webp)

## Tasarım Panosu

Panodan mağazanızın tasarım durumuna genel bir bakış verir:

- **Aktif Tema** — Hangi temanın şu anda uygulandığını, bir önizleme ve hızlı erişim butonlarını gösterir
- **Tasarım İstatistikleri** — Kurulu temaların, özel başlıkların, özel ayakların ve menülerin sayısı
- **Bölüm Kartları** — Temalar, Başlık Oluşturucu, Ayak Oluşturucu, Menüleri veya Duyurulara geçiş yapabilirsiniz

## Temalar

### Temaları Göz Atma

**Tema** bölümünü tıklayarak tüm kurulu temaları görün. Her tema kartında şunlar yer alır:
- Tema adı ve önizleme resmi
- Yazar ve sürüm
- Etkin/kapalı durumu

### Bir Temayı Etkinleştirme

1. Kullanmak istediğiniz temanın **Etkinleştir**'e tıklayın
2. Tema mağazanıza anında uygulanır
3. Aynı anda yalnızca bir tema etkin olabilir

### Tema Özelleştirme

Her tema, **tasarım token'ları** adı verilen, kod düzenlemesi yapmadan görsel görünümü kontrol eden yapılandırılamaz değerler setine sahiptir.

Etkin temanızın **Özelleştir**'e tıklayarak token editörünüze erişin. Kullanılabilir token kategorileri şunlardır:

| Kategori | Neyi Kontrol Eder |
|----------|-----------------|
| **Renkler** | Ana, ikincil, vurgu renkleri, arka planlar, metin renkleri |
| **Tipografi** | Font aileleri, boyutları, ağırlıkları, satır yükseklikleri |
| **Boşluk** | Kenar boşlukları, dolgu, elementler arası boşluklar |
| **Çizgiler** | Çizgi kalınlıkları, yuvarlaklık, renkler |
| **Gölgeler** | Kartlar, düğmeler, modeller için kutu gölgeleri |
| **Düğmeler** | Düğme stilleri, boyutları, hover etkileri |
| **Düzen** | Kapsayıcı genişlikleri, grid boşlukları, breakpoints |

Değişiklikleri kaydetmeden önce gerçek zamanlı olarak önizlenir.

## Başlık Oluşturucu

Başlık Oluşturucu, mağazanızaki başlığı sürükleyip bırakma arayüzü kullanarak tasarlamana olanak tanır.

### Başlık Oluşturma

1. **Tasarım > Başlık Oluşturucu**'ya gidin
2. **Başlık Oluştur**'a tıklayın ya da mevcut birini düzenleyin
3. Oluşturucu, üç satırdan oluşur: **Üst Çizgi**, **Ana Başlık**, ve **Alt Çizgi**
4. Araç kutusundan herhangi bir satıra widget'lar sürükleyin

### Kullanılabilir Başlık Widget'ları

- **Logo** — Yapılandırılamaz boyut ve bağlantı ile mağaza logosu
- **İşlem Menüsü** — Tanımladığınız menülerden dropdown menü
- **Arama Çubuğu** — Anlık sonuçlarla ürün araması
- **Sepet İconu** — Öge sayısı etiketi ile mini sepet
- **Hesap İconu** — Giriş/hesap dropdown'u
- **Dil Seçici** — Çoklu dil mağazaları için dil değiştirme
- **Para Birimi Seçici** — Çoklu para birimi mağazaları için para birimi değiştirme
- **İade Seçici** — Alıcıların kargo destinasyonu ülkesini seçmesine olanak tanır, satış bölgesini değiştirir (çoklu para birimi mağazaları için para birimi ile birlikte). Detaylar için **Bölge Kullanılabilirliği** rehberine bakın
- **Özel HTML** — Herhangi özel içeriğin eklenmesi
- **Sosyal İkonlar** — Sosyal medya profellerinize bağlantılar
- **Duyuru Çubuğu** — Tanıtım mesajları ve teklifler

### Başlık Ayarları

Her başlık şablonu için küresel ayarlar vardır:
- **Yükseklikli Başlık** — Kaydırma yaparken başlığın görünür kalması
- **Transparan Mod** — Hikâye resimleri üzerine overlay
- **Mobil Aralığı** — Mobil düzenine ne zaman geçileceği

## Ayak Oluşturucu

Ayak Oluşturucu, Başlık Oluşturucu ile aynı şekilde çalışır.

### Ayak Oluşturma

1. **Tasarım > Ayak Oluşturucu**'a gidin
2. **Ayak Oluştur**'a tıklayın ya da mevcut birini düzenleyin
3. Oluşturucu, birden fazla sütun ve satır destekler
4. Widget'ları pozisyona göre sürükleyin

### Kullanılabilir Ayak Widget'ları

- **İşlem Menüsü** — Ayakta bulunan navigasyon bağlantıları
- **Bülten Aboneliği** — E-posta abonelik formu
- **Sosyal İkonlar** — Sosyal medya bağlantıları
- **Özel HTML** — Özel içerik, badajlar, sertifikasyonlar
- **Ödeme İkonları** — Kabul edilen ödeme yöntemlerini gösterir
- **Telif Hakkı** — Yıl içeren dinamik telif hakkı metni
- **Logo** — Ayakta bulunan logo varyantı

## Menüleri Oluşturma

Menüler, başlık ve ayakta bulunan navigasyon bağlantılarını tanımlar.

### Bir Menü Oluşturma

1. 

Design > Menü'ye gidin
2.

Menü Ekle'ye tıklayın
3.

Menüye bir isim verin (örneğin, "Ana Navigasyon")
4.

Menü öğeleri ekleyin:
   - **Sayfa Bağlantısı** — Sayfa oluşturucu sayfasına bağlantı
   - **Kategori Bağlantısı** — Ürün kategorisine bağlantı
   - **Özel URL** — Herhangi bir dış veya iç URL
   - **Açılır Menü** — İç içe geçmiş alt menü öğeleri
5.

Öğeleri sıralamak için sürükleyin
6.

Menüyü bir başlık veya ayak kismı widget'ına atayın ve kaydedin

## Duyurular

Mağaza arayüzünün en üstünde görünen tanıtım bantları oluşturun.

### Bir Duyuru Oluşturmak

1. **Tasarım > Duyurular** (veya Dashboard kartı) sayfasına gidin
2. **Duyuru Ekle**'ye tıklayın
3. Yapılandırın:
   - **Mesaj** — Duyuru metni (çevirilere uygun)
   - **Link** — Tıklandığında isteğe bağlı URL
   - **Stil** — Arka plan rengi, metin rengi, simge
   - **Zamanlama** — Başlangıç ve bitiş tarihleri
   - **Kapatılabilir** — Müşterilerin kapatma imkanı olup olmadığı
4. Kaydet ve etkinleştir

Birden fazla duyuru aynı anda etkin olabilir — otomatik olarak döner.

## İpuçları

- Başlık ve ayak kismini inşa etmeden önce aktif tema customizer'ını kullanarak marka renklerinize uygun hale getirin.
 - Header ve Footer oluşturucularında **önizleme** özelliğini kullanarak yayımlamadan önce değişiklikleri görün.
 - Çok farklı düzenler gerekiyorsa masaüstü ve mobil için ayrı başlık oluşturun.
 - Navigasyonu basit tutun — kullanıcı dostu olmak için 5-7 tane üst düzey menü öğesi idealdir.
 - Kalıcı mesajlar yerine zamanında promosyonlar için duyurular kullanın.
 - Tema token düzenleyicisi gerçek zamanlı önizleme destekler — serbestçe deneyin ve yeterli geldiğinde kaydedin.